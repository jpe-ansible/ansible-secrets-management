"""The Dify agent SecretID issuer policy grants exact paths on each Dify agent AppRole."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from unittest import mock

import pytest
import yaml
from ansible.errors import AnsibleError

from test_openbao_hatchet_killtest_policy_reach import REQUIRED_ENV, render, role_defaults

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main"
TEMPLATE_NAME = "seed-writer-dify-secret-id-issuer-policy.hcl.j2"
DECLARED_ROLES = (
    "agent-code-simplifier",
    "agent-ci-fixer",
    "agent-vikunja-clerk",
    "agent-vikunja-triage",
    "agent-zammad-triage",
    "agent-docs-updater",
    "agent-pr-keeper",
    "agent-github-clerk",
    "agent-merge-steward",
)
CAPABILITIES = {
    "role-id": ["read"],
    "secret-id": ["create", "update", "list"],
    "secret-id-accessor/lookup": ["update"],
    "secret-id-accessor/destroy": ["update"],
}
STANZA = re.compile(r'(?ms)^path "([^"]+)" \{\s*capabilities = (\[[^\]]+\])\s*\}')


def _yaml(name: str) -> dict:
    return yaml.safe_load((DEFAULTS / name).read_text(encoding="utf-8"))


def _render(role_names) -> str:
    """Render the real template the way the policy row does: lookup() with item."""
    item = {"targets": list(role_names)}
    expression = "{{ lookup('template', '%s', template_vars={'item': %s}) }}" % (
        TEMPLATE_NAME,
        json.dumps(item),
    )
    return render(role_defaults(), expression)


def _stanzas(policy: str) -> list[tuple[str, list[str]]]:
    return [(path, json.loads(caps)) for path, caps in STANZA.findall(policy)]


ISSUER_CIDR_KEY = "OPENBAO_DIFY_SECRET_ID_ISSUER_SECRET_ID_CIDR"


def _rendered(
    expression,
    *,
    dify_cidr="192.0.2.10/32",
    issuer_cidr="198.51.100.10/32",
    issuer_env=None,
    overrides=None,
):
    environment = {
        **REQUIRED_ENV,
        ISSUER_CIDR_KEY: issuer_cidr if issuer_env is None else issuer_env,
    }
    with mock.patch.dict(os.environ, environment):
        defaults = role_defaults()
        defaults["openbao_platform_env"][ISSUER_CIDR_KEY] = issuer_cidr
        variables = {
            **defaults,
            "openbao_dify_agent_cidrs": dify_cidr,
            **(overrides or {}),
        }
        return render(variables, "{{ " + expression + " }}")


def test_declared_role_names_are_exactly_the_dify_agent_roles():
    names = _yaml("05l-dify-agent-identities.yml")
    declared = [
        value
        for key, value in names.items()
        if key.startswith("openbao_dify_agent_") and key.endswith("_approle_name")
    ]
    assert sorted(declared) == sorted(DECLARED_ROLES)


def test_rendered_policy_has_exactly_four_paths_per_declared_role():
    paths = [path for path, _ in _stanzas(_render(DECLARED_ROLES))]
    expected = {
        f"auth/approle/role/{role}/{kind}"
        for role in DECLARED_ROLES
        for kind in CAPABILITIES
    }
    assert len(paths) == len(DECLARED_ROLES) * len(CAPABILITIES)
    assert len(set(paths)) == len(expected)
    assert set(paths) == expected


def test_capabilities_per_path_kind_are_exact():
    for path, caps in _stanzas(_render(DECLARED_ROLES)):
        parts = path.split("/")
        assert parts[:3] == ["auth", "approle", "role"], path
        kind = "/".join(parts[4:])
        assert caps == CAPABILITIES[kind], path


def test_rendered_policy_has_no_wildcard_characters():
    for line in _render(DECLARED_ROLES).splitlines():
        assert "*" not in line and "+" not in line, line


def test_role_names_come_from_the_list_not_the_template():
    base = {path for path, _ in _stanzas(_render(DECLARED_ROLES))}
    extended = {
        path for path, _ in _stanzas(_render(DECLARED_ROLES + ("agent-extra-role",)))
    }
    added = extended - base
    assert added == {
        f"auth/approle/role/agent-extra-role/{kind}" for kind in CAPABILITIES
    }
    assert base <= extended


def test_empty_target_list_fails_validation():
    with pytest.raises(AnsibleError, match="must name at least one AppRole"):
        _render(())


@pytest.mark.parametrize(
    "name", ["agent+grant", "agent/grant", "agent*grant", "", "Agent-grant"]
)
def test_target_names_reject_values_outside_the_agent_slug_pattern(name):
    with pytest.raises(
        AnsibleError, match=r"item\.targets\[0\]"
    ) as error:
        _render((name,))
    if name:
        assert name not in str(error.value)


def test_target_name_matching_the_agent_slug_pattern_renders():
    assert {path for path, _ in _stanzas(_render(("agent-valid-2",)))} == {
        f"auth/approle/role/agent-valid-2/{kind}" for kind in CAPABILITIES
    }


def test_second_target_list_renders_disjoint_policy_paths():
    first = {path for path, _ in _stanzas(_render(("synthetic-target-a",)))}
    second = {path for path, _ in _stanzas(_render(("synthetic-target-b",)))}
    assert first == {f"auth/approle/role/synthetic-target-a/{kind}" for kind in CAPABILITIES}
    assert second == {f"auth/approle/role/synthetic-target-b/{kind}" for kind in CAPABILITIES}
    assert first.isdisjoint(second)


def test_issuer_policy_body_is_generated_from_targets_with_one_source():
    body = (ROOT / "roles/openbao/templates" / TEMPLATE_NAME).read_text(encoding="utf-8")
    assert "{% for name in item.targets %}" in body
    assert not [role for role in DECLARED_ROLES if role in body]
    literal_copies = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "roles").rglob("*")
        if path.is_file()
        and path.name != TEMPLATE_NAME
        and "/defaults/" not in path.as_posix()
        and "seed-writer-dify-secret-id-issuer" in path.read_text(encoding="utf-8", errors="ignore")
    ]
    assert literal_copies == []


def test_second_entry_in_the_seed_writer_list_becomes_a_second_approle():
    synthetic = {
        "name": "synthetic-issuer-b",
        "token_policies": ["{{ openbao_ansible_converge_policy_name }}"],
        "token_type": "batch",
        "token_ttl": "{{ openbao_approle_token_ttl }}",
        "token_max_ttl": "{{ openbao_approle_token_ttl }}",
        "secret_id_num_uses": 0,
    }
    seed_writer_approles = _rendered("openbao_seed_writer_approles")
    names = _rendered(
        "openbao_base_approles | map(attribute='name') | list",
        overrides={"openbao_seed_writer_approles": seed_writer_approles + [synthetic]},
    )
    assert names.count("dify-agent-secret-id-issuer") == 1
    assert names.count("synthetic-issuer-b") == 1


def test_policy_is_registered_and_attached_only_to_the_issuer_approle():
    policy_name = _rendered("openbao_seed_writer_dify_secret_id_issuer_policy_name")
    policies = _rendered("openbao_policies")
    approles = _rendered("openbao_approles")
    rows = [row for row in policies if row["name"] == policy_name]
    assert len(rows) == 1
    assert rows[0]["template"] == TEMPLATE_NAME

    seed_rows = approles
    writer_name = _rendered("openbao_ansible_converge_writer_approle_name")
    issuer_name = _rendered("openbao_dify_secret_id_issuer_approle_name")
    writers = [row for row in seed_rows if row["name"] == writer_name]
    assert len(writers) == 1
    assert policy_name not in writers[0]["token_policies"]
    issuers = [row for row in seed_rows if row["name"] == issuer_name]
    assert len(issuers) == 1
    assert issuers[0]["token_policies"] == [policy_name]
    for row in seed_rows:
        if row is not issuers[0]:
            assert policy_name not in row.get("token_policies", [])

    owners = {
        path.name
        for path in DEFAULTS.iterdir()
        if path.is_file()
        and "openbao_seed_writer_dify_secret_id_issuer_policy_name"
        in path.read_text(encoding="utf-8")
    }
    assert owners == {
        "05l-dify-agent-identities.yml",
        "07c-base-policies.yml",
        "07i-seed-writer-approles.yml",
    }


def test_dify_agent_approle_rows_stay_inert():
    text = (DEFAULTS / "07j-dify-agent-approles.yml").read_text(encoding="utf-8")
    inert = text.count("'manage_secret_id': false")
    entries = len(re.findall(r"'name':", text))
    assert inert == entries == len(DECLARED_ROLES)


def test_issuer_approle_uses_its_dedicated_bound_cidr():
    issuer_cidr = "198.51.100.10/32"
    approles = _rendered("openbao_approles", issuer_cidr=issuer_cidr)
    name = _rendered(
        "openbao_dify_secret_id_issuer_approle_name", issuer_cidr=issuer_cidr
    )
    assert name == "dify-agent-secret-id-issuer"
    issuer_rows = [role for role in approles if role["name"] == name]
    assert len(issuer_rows) == 1
    assert issuer_rows[0]["secret_id_bound_cidrs"] == issuer_cidr

    parameters = _rendered("openbao_approle_cli_parameters", issuer_cidr=issuer_cidr)[
        name
    ]
    assert parameters["token_policies"] == "seed-writer-dify-secret-id-issuer"
    assert parameters["token_type"] == "batch"
    token_ttl = _rendered("openbao_approle_token_ttl", issuer_cidr=issuer_cidr)
    assert parameters["token_ttl"] == token_ttl
    assert parameters["token_max_ttl"] == token_ttl
    assert parameters["secret_id_num_uses"] == "0"
    assert parameters["secret_id_ttl"] == _rendered(
        "openbao_rotated_domain_secret_id_ttl", issuer_cidr=issuer_cidr
    )

    assert parameters["secret_id_bound_cidrs"] == issuer_cidr
    assert parameters["token_bound_cidrs"] == issuer_cidr


def test_empty_issuer_bound_cidr_fails_with_dify_targets():
    with pytest.raises(
        AnsibleError,
        match="OPENBAO_DIFY_SECRET_ID_ISSUER_SECRET_ID_CIDR is empty",
    ):
        _rendered("openbao_approles", issuer_cidr="")


def test_issuer_bound_cidr_reads_the_environment_document_before_the_process_environment():
    expression = "openbao_dify_secret_id_issuer_secret_id_cidr"
    assert (
        _rendered(expression, issuer_cidr="198.51.100.10/32", issuer_env="192.0.2.11/32")
        == "198.51.100.10/32"
    )
    assert _rendered(expression, issuer_cidr="", issuer_env="192.0.2.11/32") == "192.0.2.11/32"
    assert _rendered(expression, issuer_cidr=None, issuer_env="192.0.2.11/32") == "192.0.2.11/32"


def test_blank_issuer_bound_cidr_in_the_environment_document_counts_as_empty():
    # A blank platform value is empty, so the process environment value applies.
    assert (
        _rendered(
            "openbao_dify_secret_id_issuer_secret_id_cidr",
            issuer_cidr="   ",
            issuer_env="192.0.2.11/32",
        )
        == "192.0.2.11/32"
    )
    assert _rendered("openbao_dify_secret_id_issuer_secret_id_cidr", issuer_cidr="   ", issuer_env="  ") == ""
    with pytest.raises(
        AnsibleError,
        match="OPENBAO_DIFY_SECRET_ID_ISSUER_SECRET_ID_CIDR is empty",
    ):
        _rendered("openbao_approles", issuer_cidr="   ", issuer_env="")


def test_issuer_bound_cidr_does_not_change_other_approle_bounds():
    approles = _rendered("openbao_approles")
    issuer = _rendered("openbao_dify_secret_id_issuer_approle_name")
    previous_approles = [role for role in approles if role["name"] != issuer]
    previous_parameters = _rendered(
        "openbao_approle_cli_parameters",
        overrides={"openbao_approles": previous_approles},
    )
    current_parameters = _rendered("openbao_approle_cli_parameters")
    bound_parameters = ("secret_id_bound_cidrs", "token_bound_cidrs")
    assert {
        name: {key: current_parameters[name][key] for key in bound_parameters}
        for name in current_parameters
        if name != issuer
    } == {
        name: {key: previous_parameters[name][key] for key in bound_parameters}
        for name in previous_parameters
    }


def test_issuer_approle_is_on_the_rotation_ttl_map_and_domain_list():
    name = _rendered("openbao_dify_secret_id_issuer_approle_name")
    overrides = _rendered("openbao_approle_secret_id_ttl_overrides")
    assert overrides[name] == _rendered("openbao_rotated_domain_secret_id_ttl")
    assert name in _rendered("openbao_secrets_domain_approle_names")


def test_no_other_approle_carries_the_issuer_policy():
    policy = _rendered("openbao_seed_writer_dify_secret_id_issuer_policy_name")
    name = _rendered("openbao_dify_secret_id_issuer_approle_name")
    parameters_by_role = _rendered("openbao_approle_cli_parameters")
    carriers = sorted(
        role
        for role, parameters in parameters_by_role.items()
        if policy in parameters["token_policies"].split(",")
    )
    assert carriers == [name]


def test_shared_writer_keeps_only_its_converge_policy():
    writer = _rendered("openbao_ansible_converge_writer_approle_name", dify_cidr="")
    parameters = _rendered("openbao_approle_cli_parameters", dify_cidr="")
    policies = parameters[writer]["token_policies"].split(",")
    assert policies == [_rendered("openbao_ansible_converge_policy_name", dify_cidr="")]
    policy_name = _rendered(
        "openbao_seed_writer_dify_secret_id_issuer_policy_name", dify_cidr=""
    )
    assert policy_name not in policies


def test_issuer_catalog_entries_follow_dify_targets():
    issuer = "dify-agent-secret-id-issuer"
    policy_name = "seed-writer-dify-secret-id-issuer"
    approles = _rendered("openbao_approles", dify_cidr="", issuer_cidr="")
    policies = _rendered("openbao_policies", dify_cidr="", issuer_cidr="")
    domain_names = _rendered(
        "openbao_secrets_domain_approle_names", dify_cidr="", issuer_cidr=""
    )
    ttl_overrides = _rendered(
        "openbao_approle_secret_id_ttl_overrides", dify_cidr="", issuer_cidr=""
    )
    assert issuer not in {role["name"] for role in approles}
    assert policy_name not in {policy["name"] for policy in policies}
    assert issuer not in domain_names
    assert issuer not in ttl_overrides

    approles = _rendered("openbao_approles")
    policies = _rendered("openbao_policies")
    domain_names = _rendered("openbao_secrets_domain_approle_names")
    ttl_overrides = _rendered("openbao_approle_secret_id_ttl_overrides")
    assert issuer in {role["name"] for role in approles}
    assert policy_name in {policy["name"] for policy in policies}
    assert issuer in domain_names
    assert issuer in ttl_overrides
