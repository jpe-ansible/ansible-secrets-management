"""Pepper receives one guest-bound reader and a routinely seeded router key."""

import pytest
import yaml

from openbao_reconcile_bounds_helpers import (
    DEFAULTS,
    ROOT,
    TEMPLATES,
    _capabilities,
    _render,
    _render_value,
    _stanzas,
)

PROOF_MODE = ROOT / "playbooks/tasks/openbao_rotate_proof_mode.yml"


@pytest.fixture
def pepper_defaults(monkeypatch):
    monkeypatch.setenv("OPENBAO_TERRAKUBE_NETWORK_WORKSPACE", "fixture-network")
    monkeypatch.setenv("OPENBAO_TERRAKUBE_AWS_WORKSPACE", "fixture-aws")
    for name in (
        "OPENBAO_GITHUB_PEPPER_APP_ID",
        "OPENBAO_GITHUB_PEPPER_APP_PRIVATE_KEY",
        "OPENBAO_GITHUB_PEPPER_REPOSITORY",
        "OPENBAO_GITHUB_PEPPER_REPOSITORIES",
        "OPENBAO_GITHUB_OPENHANDS_APP_ID",
        "OPENBAO_GITHUB_OPENHANDS_APP_PRIVATE_KEY",
        "OPENBAO_GITHUB_OPENHANDS_WRITE_ORGS",
        "OPENBAO_GITHUB_OPENHANDS_WRITE_WORKFLOWS",
    ):
        monkeypatch.delenv(name, raising=False)
    values = {}
    for path in sorted(DEFAULTS.glob("*.yml")):
        values.update(yaml.safe_load(path.read_text(encoding="utf-8")) or {})
    values.update(
        ansible_managed="test fixture",
        openbao_platform_env={"OPENBAO_PEPPER_SECRET_ID_CIDR": "pepper-fixture-cidr"},
        llm_router_key_catalog_facts={"openbao_router_key_catalog": {}},
    )
    return values


def test_pepper_policy_mints_its_set_and_reads_only_its_secret_paths(pepper_defaults):
    policies = _render_value(pepper_defaults, "{{ openbao_policies }}")
    pepper = [policy for policy in policies if policy["name"] == "pepper"]
    assert len(pepper) == 1
    stanzas = dict(_stanzas(_render(TEMPLATES / pepper[0]["template"], pepper_defaults)))
    token_path = "github-pepper/token/pepper-vault-read"
    assert list(stanzas) == [
        token_path,
        "secret/data/youtrack/pepper/rw",
        "secrets-external/data/slack/pepper/rw",
        "secrets-external/metadata/slack/pepper/rw",
        "secret/data/apps/pepper",
    ]
    assert "secret/data/ai/pepper" not in stanzas
    assert "secret/data/ai/pepper/*" not in stanzas
    assert _capabilities(stanzas[token_path]) == ["create", "update"]
    assert all(
        _capabilities(body) == ["read"]
        for path, body in stanzas.items()
        if path != token_path
    )


def test_ai_donna_policy_keeps_its_grants_and_reads_its_slack_leaf(pepper_defaults):
    policies = _render_value(pepper_defaults, "{{ openbao_policies }}")
    donna = [policy for policy in policies if policy["name"] == "ai-donna"]
    assert len(donna) == 1
    stanzas = dict(_stanzas(_render(TEMPLATES / donna[0]["template"], pepper_defaults)))

    assert list(stanzas) == [
        "secret/data/ai/donna",
        "secret/metadata/ai/donna",
        "secrets-external/data/slack/donna/rw",
        "secrets-external/metadata/slack/donna/rw",
    ]
    assert _capabilities(stanzas["secret/data/ai/donna"]) == ["read"]
    assert _capabilities(stanzas["secret/metadata/ai/donna"]) == ["read", "list"]
    assert _capabilities(stanzas["secrets-external/data/slack/donna/rw"]) == ["read"]
    assert _capabilities(stanzas["secrets-external/metadata/slack/donna/rw"]) == ["read"]


def test_pepper_approle_uses_only_its_guest_and_scheduled_rotation(pepper_defaults):
    roles = _render_value(pepper_defaults, "{{ openbao_approles }}")
    pepper = [role for role in roles if role["name"] == "pepper"]
    assert len(pepper) == 1
    assert pepper[0]["policy"] == "pepper"
    assert pepper[0]["manage_secret_id"] is False
    assert pepper[0]["secret_id_num_uses"] > 0
    parameters = _render_value(pepper_defaults, "{{ openbao_approle_cli_parameters }}")
    assert parameters["pepper"]["token_policies"] == "pepper"
    assert parameters["pepper"]["secret_id_bound_cidrs"] == "pepper-fixture-cidr"
    assert parameters["pepper"]["token_bound_cidrs"] == "pepper-fixture-cidr"
    ttls = _render_value(pepper_defaults, "{{ openbao_approle_secret_id_ttl_overrides }}")
    assert parameters["pepper"]["secret_id_ttl"] == ttls["hermes-private-agent"]
    assert ttls["pepper"] == pepper_defaults["openbao_rotated_domain_secret_id_ttl"]
    rotated = _render_value(pepper_defaults, "{{ openbao_secrets_domain_approle_names }}")
    assert rotated.count("pepper") == 1
    assert "hermes-private-agent" not in rotated
    # The rotation proves the new pair by lookup: the runner is outside the guest bind.
    proof_task = yaml.safe_load(PROOF_MODE.read_text(encoding="utf-8"))[0]
    proof = proof_task["ansible.builtin.set_fact"]["rotate_proof_by_lookup"]
    assert _render_value(pepper_defaults, proof, rotate_domain_name="pepper") is True
    classes = _render_value(pepper_defaults, "{{ openbao_approle_class_map }}")
    assert classes["pepper"] == "trusted-agent-read"
    leaves = _render_value(pepper_defaults, "{{ openbao_roster_agent_ai_leaf_names }}")
    assert "pepper" in leaves


def test_pepper_approle_stays_dormant_without_its_cidr(pepper_defaults, monkeypatch):
    monkeypatch.delenv("OPENBAO_PEPPER_SECRET_ID_CIDR", raising=False)
    pepper_defaults["openbao_platform_env"] = {}
    roles = _render_value(pepper_defaults, "{{ openbao_approles }}")
    assert "pepper" not in [role["name"] for role in roles]
    rotated = _render_value(pepper_defaults, "{{ openbao_secrets_domain_approle_names }}")
    assert "pepper" not in rotated
    assert "hermes-private-agent" not in rotated


def test_shared_guest_defaults_preserve_the_private_hermes_bounds(pepper_defaults):
    pepper_defaults["openbao_platform_env"]["OPENBAO_HERMES_PRIVATE_AGENT_SECRET_ID_CIDR"] = "private-fixture-cidr"
    roles = _render_value(pepper_defaults, "{{ openbao_approles }}")
    hermes = next(role for role in roles if role["name"] == "hermes-private-agent")
    pepper = next(role for role in roles if role["name"] == "pepper")
    for field in ("secret_id_num_uses", "token_ttl", "token_max_ttl", "manage_secret_id"):
        assert hermes[field] == pepper[field]
    assert hermes["secret_id_bound_cidrs"] == "private-fixture-cidr"
    assert pepper["secret_id_bound_cidrs"] == "pepper-fixture-cidr"
    rotated = _render_value(pepper_defaults, "{{ openbao_secrets_domain_approle_names }}")
    assert {"hermes-private-agent", "pepper"} <= set(rotated)


def test_pepper_cidr_can_arrive_from_the_environment(pepper_defaults, monkeypatch):
    pepper_defaults["openbao_platform_env"] = {}
    monkeypatch.setenv("OPENBAO_PEPPER_SECRET_ID_CIDR", "fallback-fixture-cidr")
    roles = _render_value(pepper_defaults, "{{ openbao_pepper_approles }}")
    assert roles[0]["secret_id_bound_cidrs"] == "fallback-fixture-cidr"


def _configure_pepper_mount(monkeypatch, values, *, repository="fixture-repo"):
    monkeypatch.setenv("OPENBAO_GITHUB_PEPPER_APP_ID", "fixture-app-id")
    monkeypatch.setenv("OPENBAO_GITHUB_PEPPER_APP_PRIVATE_KEY", "fixture-private-key")
    monkeypatch.setenv("OPENBAO_GITHUB_PEPPER_REPOSITORY", repository)
    values["openbao_platform_env"]["OPENBAO_GITHUB_PEPPER_INSTALLATION_ID"] = (
        "fixture-installation"
    )


def _pepper_sets_and_mounts(values):
    sets = _render_value(values, "{{ openbao_github_pepper_permission_sets }}")
    mounts = _render_value(values, "{{ openbao_github_app_mounts }}")
    pepper_mounts = [
        mount for mount in mounts if mount["mount"] == "github-pepper"
    ]
    return sets, pepper_mounts


def test_pepper_mount_and_set_are_absent_without_inputs(pepper_defaults):
    sets, mounts = _pepper_sets_and_mounts(pepper_defaults)
    assert sets == []
    assert mounts == []


@pytest.mark.parametrize(
    "missing_input",
    [
        "OPENBAO_GITHUB_PEPPER_APP_ID",
        "OPENBAO_GITHUB_PEPPER_APP_PRIVATE_KEY",
        "OPENBAO_GITHUB_PEPPER_INSTALLATION_ID",
        "OPENBAO_GITHUB_PEPPER_REPOSITORY",
    ],
)
def test_pepper_mount_is_absent_when_any_input_is_missing(
    pepper_defaults, monkeypatch, missing_input
):
    _configure_pepper_mount(monkeypatch, pepper_defaults)
    if missing_input == "OPENBAO_GITHUB_PEPPER_INSTALLATION_ID":
        pepper_defaults["openbao_platform_env"].pop(missing_input)
    else:
        monkeypatch.delenv(missing_input, raising=False)

    sets, mounts = _pepper_sets_and_mounts(pepper_defaults)
    assert sets == []
    assert mounts == []


def test_pepper_mount_is_absent_for_a_repository_value_with_a_slash(
    pepper_defaults, monkeypatch
):
    _configure_pepper_mount(
        monkeypatch, pepper_defaults, repository="fixture-owner/fixture-repo"
    )
    sets, mounts = _pepper_sets_and_mounts(pepper_defaults)
    assert sets == []
    assert mounts == []


def test_pepper_mount_has_exactly_one_repository_scoped_read_set(
    pepper_defaults, monkeypatch
):
    _configure_pepper_mount(monkeypatch, pepper_defaults)
    sets, mounts = _pepper_sets_and_mounts(pepper_defaults)

    assert sets == [
        {
            "name": "pepper-vault-read",
            "tier": "pepper-read",
            "installation_id": "fixture-installation",
            "repositories": ["fixture-repo"],
            "permissions": {"contents": "read", "metadata": "read"},
        }
    ]
    assert len(mounts) == 1
    assert mounts[0]["app_id"] == "fixture-app-id"
    assert mounts[0]["private_key"] == "fixture-private-key"
    assert mounts[0]["permission_sets"] == sets

    registered_sets = _render_value(
        pepper_defaults, "{{ openbao_github_permission_sets }}"
    )
    pepper_registered = [
        permission_set
        for permission_set in registered_sets
        if permission_set["name"] == "pepper-vault-read"
    ]
    assert pepper_registered == [dict(sets[0], mount="github-pepper")]


def test_pepper_policy_grants_only_its_named_set_on_github_mounts(
    pepper_defaults, monkeypatch
):
    _configure_pepper_mount(monkeypatch, pepper_defaults)
    policy = _render(TEMPLATES / "pepper-policy.hcl.j2", pepper_defaults)
    stanzas = dict(_stanzas(policy))
    token_path = "github-pepper/token/pepper-vault-read"
    github_paths = [
        path
        for path in stanzas
        if path == "github" or path.startswith("github-")
    ]

    assert github_paths == [token_path]
    assert _capabilities(stanzas[token_path]) == ["create", "update"]
    assert "github-pepper/token" not in stanzas


def test_other_identity_policies_do_not_grant_the_pepper_token_path(
    pepper_defaults, monkeypatch
):
    _configure_pepper_mount(monkeypatch, pepper_defaults)
    token_path = "github-pepper/token/pepper-vault-read"
    for template_name in (
        "github-mint-policy.hcl.j2",
        "github-read-policy.hcl.j2",
        "open-llm-policy.hcl.j2",
        "ai-orchestrator-policy.hcl.j2",
    ):
        policy = _render(TEMPLATES / template_name, pepper_defaults)
        assert token_path not in dict(_stanzas(policy)), template_name

    agent_sets = _render_value(
        pepper_defaults, "{{ openbao_github_agents_permission_sets }}"
    )
    assert all(item["name"] != "pepper-vault-read" for item in agent_sets)


def _configure_openhands_mount(monkeypatch, values, *, installation_id="303"):
    monkeypatch.setenv("OPENBAO_GITHUB_OPENHANDS_APP_ID", "fixture-app-id")
    monkeypatch.setenv(
        "OPENBAO_GITHUB_OPENHANDS_APP_PRIVATE_KEY", "fixture-private-key"
    )
    values["openbao_platform_env"][
        "OPENBAO_GITHUB_OPENHANDS_DRYVIST_INSTALLATION_ID"
    ] = installation_id
    monkeypatch.setenv("OPENBAO_GITHUB_OPENHANDS_WRITE_ORGS", "example-org")
    monkeypatch.setenv("OPENBAO_GITHUB_OPENHANDS_PILOT_REPOS", "fixture-repo")


def _openhands_sets_and_mounts(values):
    sets = _render_value(values, "{{ openbao_github_openhands_permission_sets }}")
    mounts = _render_value(values, "{{ openbao_github_app_mounts }}")
    openhands_mounts = [
        mount for mount in mounts if mount["mount"] == "github-openhands"
    ]
    return sets, openhands_mounts


def test_openhands_mount_and_set_are_absent_without_inputs(pepper_defaults):
    sets, mounts = _openhands_sets_and_mounts(pepper_defaults)
    assert sets == []
    assert mounts == []


def test_openhands_mount_and_pilot_are_declared_without_a_private_key(
    pepper_defaults, monkeypatch
):
    monkeypatch.setenv("OPENBAO_GITHUB_OPENHANDS_APP_ID", "fixture-app-id")
    monkeypatch.setenv("OPENBAO_GITHUB_OPENHANDS_APP_PRIVATE_KEY", "")
    monkeypatch.setenv("OPENBAO_GITHUB_OPENHANDS_WRITE_ORGS", "example-org")
    monkeypatch.setenv("OPENBAO_GITHUB_OPENHANDS_PILOT_REPOS", "fixture-repo")
    pepper_defaults["openbao_platform_env"][
        "OPENBAO_GITHUB_OPENHANDS_DRYVIST_INSTALLATION_ID"
    ] = "303"

    sets, mounts = _openhands_sets_and_mounts(pepper_defaults)
    assert sets == [
        {
            "name": "openhands-pilot",
            "tier": "openhands",
            "installation_id": "303",
            "repositories": ["fixture-repo"],
            "permissions": {
                "actions": "read",
                "checks": "read",
                "contents": "write",
                "metadata": "read",
                "pull_requests": "write",
            },
        }
    ]
    write_sets = _render_value(
        pepper_defaults, "{{ openbao_github_openhands_write_permission_sets }}"
    )
    assert len(write_sets) == 1
    assert len(mounts) == 1
    assert mounts[0]["app_id"] == "fixture-app-id"
    assert mounts[0]["private_key"] == ""
    assert mounts[0]["permission_sets"] == sets + write_sets


def test_openhands_mount_has_one_repository_scoped_set_with_exact_permissions(
    pepper_defaults, monkeypatch
):
    _configure_openhands_mount(monkeypatch, pepper_defaults)
    sets, mounts = _openhands_sets_and_mounts(pepper_defaults)

    assert sets == [
        {
            "name": "openhands-pilot",
            "tier": "openhands",
            "installation_id": "303",
            "repositories": ["fixture-repo"],
            "permissions": {
                "actions": "read",
                "checks": "read",
                "contents": "write",
                "metadata": "read",
                "pull_requests": "write",
            },
        }
    ]
    assert len(mounts) == 1
    assert mounts[0]["app_id"] == "fixture-app-id"
    assert mounts[0]["private_key"] == "fixture-private-key"
    write_sets = _render_value(
        pepper_defaults, "{{ openbao_github_openhands_write_permission_sets }}"
    )
    assert mounts[0]["permission_sets"] == sets + write_sets

    registered_sets = _render_value(
        pepper_defaults, "{{ openbao_github_permission_sets }}"
    )
    openhands_registered = [
        permission_set
        for permission_set in registered_sets
        if permission_set["name"] == "openhands-pilot"
    ]
    assert openhands_registered == [dict(sets[0], mount="github-openhands")]


def test_openhands_policy_mints_only_its_dedicated_set(pepper_defaults, monkeypatch):
    _configure_openhands_mount(monkeypatch, pepper_defaults)
    policies = _render_value(pepper_defaults, "{{ openbao_policies }}")
    openhands = [policy for policy in policies if policy["name"] == "openhands"]
    assert len(openhands) == 1

    stanzas = dict(
        _stanzas(_render(TEMPLATES / openhands[0]["template"], pepper_defaults))
    )
    token_path = "github-openhands/token/openhands-pilot"
    github_paths = [
        path
        for path in stanzas
        if path == "github" or path.startswith("github-")
    ]

    assert github_paths == [token_path]
    assert _capabilities(stanzas[token_path]) == ["create", "read", "update"]
    assert "github-openhands/token" not in stanzas


def test_openhands_approle_has_only_its_policy_and_one_hour_tokens(pepper_defaults):
    roles = _render_value(pepper_defaults, "{{ openbao_approles }}")
    openhands = [role for role in roles if role["name"] == "openhands"]
    assert len(openhands) == 1
    assert openhands[0]["policy"] == "openhands"
    assert openhands[0]["token_ttl"] == "1h"
    assert openhands[0]["token_max_ttl"] == "1h"

    parameters = _render_value(
        pepper_defaults, "{{ openbao_approle_cli_parameters }}"
    )
    assert parameters["openhands"]["token_policies"] == "openhands"


@pytest.mark.parametrize(
    ("variable", "key"),
    [
        ("openbao_sandbox_agent_cidrs", "OPENBAO_SANDBOX_AGENT_CIDRS"),
        ("openbao_ai_runner_secret_id_cidr", "OPENBAO_AI_RUNNER_SECRET_ID_CIDR"),
        ("openbao_open_llm_secret_id_cidr", "OPENBAO_AI_SANDBOX_SECRET_ID_CIDR"),
        ("openbao_openhands_secret_id_cidr", "OPENBAO_OPENHANDS_SECRET_ID_CIDR"),
        ("openbao_hermes_private_agent_secret_id_cidr", "OPENBAO_HERMES_PRIVATE_AGENT_SECRET_ID_CIDR"),
        ("openbao_pepper_secret_id_cidr", "OPENBAO_PEPPER_SECRET_ID_CIDR"),
        ("openbao_dify_agent_cidrs", "OPENBAO_DIFY_AGENT_CIDR"),
    ],
)
def test_guest_binds_read_the_platform_env_before_the_process_env(
    pepper_defaults, monkeypatch, variable, key
):
    monkeypatch.setenv(key, "process-fixture-cidr")
    pepper_defaults["openbao_platform_env"][key] = "platform-fixture-cidr"
    assert _render_value(pepper_defaults, "{{ %s }}" % variable) == "platform-fixture-cidr"
    del pepper_defaults["openbao_platform_env"][key]
    assert _render_value(pepper_defaults, "{{ %s }}" % variable) == "process-fixture-cidr"
    pepper_defaults["openbao_platform_env"][key] = "   "
    assert _render_value(pepper_defaults, "{{ %s }}" % variable) == "process-fixture-cidr"
    pepper_defaults["openbao_platform_env"][key] = None
    assert _render_value(pepper_defaults, "{{ %s }}" % variable) == "process-fixture-cidr"
    monkeypatch.delenv(key)
    assert _render_value(pepper_defaults, "{{ %s }}" % variable) == ""
