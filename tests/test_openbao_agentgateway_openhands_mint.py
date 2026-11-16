"""The API gateway may mint only the configured OpenHands pilot token set."""

import pytest
import yaml

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

from openbao_reconcile_bounds_helpers import (
    DEFAULTS,
    ROOT,
    TEMPLATES,
    _capabilities,
    _render,
    _render_value,
    _stanzas,
)


APPROLE_NAME = "agentgateway-openhands-mint"
POLICY_NAME = "agentgateway-openhands-mint"
ADDRESS_KEY = "OPENBAO_AGENTGATEWAY_OPENHANDS_MINT_SECRET_ID_CIDR"
REPOSITORIES_KEY = "OPENBAO_GITHUB_OPENHANDS_PILOT_REPOS"
REPOSITORIES_VARIABLE = "openbao_github_openhands_pilot_repos"
INSTALLATION_KEY = "OPENBAO_GITHUB_OPENHANDS_DRYVIST_INSTALLATION_ID"
APP_ID_KEY = "OPENBAO_GITHUB_OPENHANDS_APP_ID"
APP_PRIVATE_KEY_KEY = "OPENBAO_GITHUB_OPENHANDS_APP_PRIVATE_KEY"
APPROLE_TASKS = ROOT / "roles/openbao/tasks/init/10-approles.yml"
APP_SET_CHECKS = ROOT / "roles/openbao/tasks/init/05b-github-app-set-checks.yml"


@pytest.fixture
def gateway_defaults(monkeypatch):
    for name in (
        ADDRESS_KEY,
        REPOSITORIES_KEY,
        APP_ID_KEY,
        APP_PRIVATE_KEY_KEY,
        "OPENBAO_GITHUB_OPENHANDS_WRITE_ORGS",
        "OPENBAO_GITHUB_OPENHANDS_WRITE_WORKFLOWS",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("OPENBAO_TERRAKUBE_NETWORK_WORKSPACE", "fixture-network")
    monkeypatch.setenv("OPENBAO_TERRAKUBE_AWS_WORKSPACE", "fixture-aws")

    values = {}
    for path in sorted(DEFAULTS.glob("*.yml")):
        values.update(yaml.safe_load(path.read_text(encoding="utf-8")) or {})
    values.update(
        ansible_managed="test fixture",
        openbao_management_cidrs="192.0.2.0/24",
        openbao_platform_env={},
        llm_router_key_catalog_facts={"openbao_router_key_catalog": {}},
    )
    return values


def _configure_openhands_pilot(values, monkeypatch, *, repos=None):
    monkeypatch.setenv(APP_ID_KEY, "fixture-app-id")
    monkeypatch.setenv(APP_PRIVATE_KEY_KEY, "fixture-private-key")
    values["openbao_platform_env"][INSTALLATION_KEY] = "303"
    if repos is None:
        monkeypatch.delenv(REPOSITORIES_KEY, raising=False)
    else:
        monkeypatch.setenv(REPOSITORIES_KEY, repos)


def _gateway_identity(values, address):
    values["openbao_platform_env"][ADDRESS_KEY] = address
    roles = _render_value(values, "{{ openbao_approles }}")
    policies = _render_value(values, "{{ openbao_policies }}")
    values["openbao_approles"] = roles
    values["openbao_policies"] = policies
    return roles, policies


def _named(items, name):
    return [item for item in items if item["name"] == name]


def _assert_task(path, starts_with):
    for task in yaml.safe_load(path.read_text(encoding="utf-8")):
        if task.get("name", "").startswith(starts_with):
            return task
    raise AssertionError(f"assert task starting {starts_with!r} not found in {path}")


def test_agentgateway_openhands_mint_identity_is_absent_without_address(gateway_defaults):
    roles, policies = _gateway_identity(gateway_defaults, "")
    rotated = _render_value(
        gateway_defaults, "{{ openbao_secrets_domain_approle_names }}"
    )

    assert _named(roles, APPROLE_NAME) == []
    assert _named(policies, POLICY_NAME) == []
    assert APPROLE_NAME not in rotated


def test_agentgateway_openhands_mint_address_key_is_a_platform_bind_input(
    gateway_defaults,
):
    keys = _render_value(gateway_defaults, "{{ openbao_platform_bind_keys }}")
    assert ADDRESS_KEY in keys


def test_agentgateway_openhands_mint_identity_is_bound_and_rotated_with_address(
    gateway_defaults,
):
    roles, _policies = _gateway_identity(gateway_defaults, "192.0.2.30/32")
    role, = _named(roles, APPROLE_NAME)
    gateway_defaults["openbao_approles"] = roles

    role_class = _render_value(
        gateway_defaults, "{{ openbao_approle_cidr_class_map }}"
    )[APPROLE_NAME]
    parameters = _render_value(
        gateway_defaults, "{{ openbao_approle_cli_parameters }}"
    )[APPROLE_NAME]
    ttls = _render_value(
        gateway_defaults, "{{ openbao_approle_secret_id_ttl_overrides }}"
    )
    openhands = next(item for item in roles if item["name"] == "openhands")
    rotated = _render_value(
        gateway_defaults, "{{ openbao_secrets_domain_approle_names }}"
    )

    assert role["secret_id_bound_cidrs"] == "192.0.2.30/32"
    assert role_class == "machine"
    assert role.get("token_policies", [role.get("policy")]) == [POLICY_NAME]
    assert parameters["token_policies"] == POLICY_NAME
    assert role["secret_id_num_uses"] == 0
    assert parameters["secret_id_num_uses"] == "0"
    assert role["token_ttl"] == openhands["token_ttl"] == "1h"
    assert role["token_max_ttl"] == openhands["token_max_ttl"] == "1h"
    assert ttls[APPROLE_NAME] == ttls["openhands"]
    assert rotated.count(APPROLE_NAME) == 1


def test_agentgateway_openhands_mint_policy_has_only_the_pilot_token_grant(
    gateway_defaults, monkeypatch
):
    _configure_openhands_pilot(gateway_defaults, monkeypatch, repos="fixture-repo")
    roles, policies = _gateway_identity(gateway_defaults, "192.0.2.30/32")
    gateway_defaults["openbao_approles"] = roles
    gateway_defaults["openbao_policies"] = policies
    gateway_defaults["openbao_github_permission_sets"] = _render_value(
        gateway_defaults, "{{ openbao_github_permission_sets }}"
    )
    policy, = _named(policies, POLICY_NAME)

    rendered = _render(TEMPLATES / policy["template"], gateway_defaults)
    stanzas = list(_stanzas(rendered))
    assert [path for path, _body in stanzas] == [
        "github-openhands/token/openhands-pilot"
    ]
    assert _capabilities(stanzas[0][1]) == ["create", "read", "update"]
    assert "data/" not in rendered
    assert "metadata/" not in rendered
    assert "*" not in rendered


def test_agentgateway_openhands_mint_policy_without_pilot_is_empty_and_unscheduled(
    gateway_defaults,
):
    _roles, policies = _gateway_identity(gateway_defaults, "192.0.2.30/32")
    gateway_defaults["openbao_policies"] = policies
    policy, = _named(policies, POLICY_NAME)

    rendered = _render(TEMPLATES / policy["template"], gateway_defaults)
    assert list(_stanzas(rendered)) == []

    # An empty policy document stays out of the scheduled policy writer, so it
    # cannot replace a live policy with no grants.
    unscheduled = _render_value(
        gateway_defaults, "{{ openbao_unscheduled_empty_policy_names }}"
    )
    assert POLICY_NAME in unscheduled


def test_openhands_pilot_repository_input_is_optional_and_csv_parsed(
    gateway_defaults, monkeypatch
):
    _configure_openhands_pilot(gateway_defaults, monkeypatch)
    sets = _render_value(
        gateway_defaults, "{{ openbao_github_openhands_permission_sets }}"
    )
    assert len(sets) == 1
    assert "repositories" not in sets[0]

    monkeypatch.setenv(REPOSITORIES_KEY, " fixture-repo , ,")
    repos = _render_value(gateway_defaults, "{{ %s }}" % REPOSITORIES_VARIABLE)
    sets = _render_value(
        gateway_defaults, "{{ openbao_github_openhands_permission_sets }}"
    )
    assert repos == ["fixture-repo"]
    assert sets[0]["repositories"] == ["fixture-repo"]


def test_malformed_openhands_pilot_repository_fails_the_runtime_name_predicate(
    gateway_defaults, monkeypatch
):
    _configure_openhands_pilot(
        gateway_defaults,
        monkeypatch,
        repos="fixture-valid,fixture-invalid/name",
    )
    repos = _render_value(gateway_defaults, "{{ %s }}" % REPOSITORIES_VARIABLE)
    sets = _render_value(
        gateway_defaults, "{{ openbao_github_openhands_permission_sets }}"
    )
    assert repos == ["fixture-valid", "fixture-invalid/name"]
    assert sets[0]["repositories"] == repos

    task = _assert_task(APP_SET_CHECKS, "Assert the dedicated OpenHands pilot set")
    predicates = [
        predicate
        for predicate in task["ansible.builtin.assert"]["that"]
        if "repositories" in predicate
        and "match" in predicate
        and "A-Za-z0-9_.-" in predicate
    ]
    assert len(predicates) == 1

    context = dict(
        gateway_defaults,
        gm={"mount": "github-openhands", "permission_sets": sets},
        _openhands_pilot_sets=sets,
        _openhands_set=sets[0],
    )
    assert not _render_value(context, "{{ " + predicates[0] + " }}")


def test_agentgateway_openhands_mint_address_assertion_rejects_a_wider_range():
    task = next(
        task
        for task in yaml.safe_load(APPROLE_TASKS.read_text(encoding="utf-8"))
        if "ansible.builtin.assert" in task
        and any(
            "openbao_agentgateway_openhands_mint_secret_id_cidr" in predicate
            for predicate in task["ansible.builtin.assert"]["that"]
        )
    )
    (predicate,) = task["ansible.builtin.assert"]["that"]

    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        "openbao_agentgateway_openhands_mint_secret_id_cidr": "192.0.2.0/24"
    }
    result = templar.template(trust_as_template("{{ " + predicate + " }}"))
    assert result is False
