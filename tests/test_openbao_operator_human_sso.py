"""Contract tests for the OpenBao UI's human OIDC role and policy."""

import json
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined
import yaml


ROOT = Path(__file__).resolve().parents[1]
OPENBAO = ROOT / "roles/openbao"
DEFAULTS = OPENBAO / "defaults/main/05j-openbao-ui-operator-oidc.yml"
POLICY_DEFAULTS = OPENBAO / "defaults/main/07c-base-policies.yml"
AUTHELIA_DEFAULTS = ROOT / "roles/authelia/defaults/main/01-oidc-clients.yml"
AUTHELIA_GROUP_DEFAULTS = ROOT / "roles/authelia/defaults/main/02-notifier-and-rest.yml"
AUTHELIA_URL_DEFAULTS = ROOT / "roles/authelia/defaults/main/03-openbao-ui-public-url.yml"
SECRET_DEFAULTS = OPENBAO / "defaults/main/01c-app-secrets-generated.yml"
AUTH_TASKS = OPENBAO / "tasks/init/09g-openbao-ui-operator-oidc.yml"
AUTH_PARENT = OPENBAO / "tasks/init/09-auth-methods-and-terrakube-jwt.yml"
ROLE_TEMPLATE = "openbao-ui-operator-oidc-role.json.j2"
POLICY_TEMPLATE = "operator-human-policy.hcl.j2"

PATH_BLOCK = re.compile(
    r'path "([^"]+)"\s*\{\s*capabilities\s*=\s*\[([^]]+)\]\s*\}',
    re.MULTILINE,
)


def _agent_tier_mount() -> str:
    defaults = yaml.safe_load(
        (OPENBAO / "defaults/main/05k-agent-tier-secret-paths.yml").read_text(
            encoding="utf-8"
        )
    )
    return defaults["openbao_agent_tier_mount"]


def _render_role(group: str) -> dict:
    environment = Environment(
        loader=FileSystemLoader([str(OPENBAO / "templates"), str(OPENBAO)]),
        undefined=StrictUndefined,
    )
    environment.filters["to_json"] = lambda value: json.dumps(value)
    rendered = environment.get_template(ROLE_TEMPLATE).render(
        openbao_operator_oidc_ui_redirect_uri=(
            "https://openbao.example.test/ui/vault/auth/oidc/oidc/callback"
        ),
        openbao_operator_oidc_cli_redirect_uri="http://localhost:8250/oidc/callback",
        openbao_authelia_operator_group=group,
        openbao_operator_human_policy_name="operator-human",
        openbao_operator_oidc_token_ttl="1h",
        openbao_operator_oidc_token_max_ttl="8h",
    )
    return json.loads(rendered)


def _render_policy() -> str:
    environment = Environment(
        loader=FileSystemLoader([str(OPENBAO / "templates"), str(OPENBAO)]),
        undefined=StrictUndefined,
    )
    environment.filters["comment"] = lambda value: "# " + str(value)
    return environment.get_template(POLICY_TEMPLATE).render(
        ansible_managed="managed",
        openbao_kv_mounts=[
            {"path": "secret"},
            {"path": "secrets-external"},
            {"path": "config"},
        ],
        openbao_agent_tier_mount=_agent_tier_mount(),
    )


def _grants(policy: str) -> list[tuple[str, set[str]]]:
    return [
        (path, set(re.findall(r'"([^"]+)"', capabilities)))
        for path, capabilities in PATH_BLOCK.findall(policy)
    ]


def test_operator_role_binds_only_the_configured_group_and_policy():
    role = _render_role("operator-group-from-env")

    assert role["role_type"] == "oidc"
    assert role["allowed_redirect_uris"] == [
        "https://openbao.example.test/ui/vault/auth/oidc/oidc/callback",
        "http://localhost:8250/oidc/callback",
    ]
    assert role["user_claim"] == "preferred_username"
    assert role["groups_claim"] == "groups"
    assert role["bound_claims"] == {"groups": ["operator-group-from-env"]}
    assert role["token_policies"] == ["operator-human"]
    assert role["token_no_default_policy"] is True
    assert role["token_ttl"] == "1h"
    assert role["token_max_ttl"] == "8h"


def test_policy_write_capabilities_are_limited_to_two_provider_records():
    policy = _render_policy()
    grants = _grants(policy)
    agent_tier_mount = _agent_tier_mount()
    read_paths = {
        "secret/data/*",
        "secret/metadata/*",
        "secrets-external/data/*",
        "secrets-external/metadata/*",
        "config/data/*",
        "config/metadata/*",
        f"{agent_tier_mount}/data/*",
        f"{agent_tier_mount}/metadata/*",
    }
    data_read_paths = {
        "secret/data/*",
        "secrets-external/data/*",
        "config/data/*",
        f"{agent_tier_mount}/data/*",
    }
    system_metadata_paths = {
        "sys/mounts",
        "sys/auth",
        "sys/policies/acl",
        "sys/policies/acl/*",
        "sys/internal/ui/mounts",
        "sys/internal/ui/mounts/*",
    }
    write_paths = {
        "secrets-external/data/ai/saas/opencode",
        "secrets-external/data/ai/saas/zai",
        "ext-ai/data/opencode/main/rw",
        "ext-ai/data/zai/main/rw",
    }
    # Self-token and UI bootstrap grants from OpenBao's default policy; the role
    # sets token_no_default_policy, so the UI cannot load after login without them.
    self_grants = {
        "auth/token/lookup-self": {"read"},
        "auth/token/renew-self": {"update"},
        "auth/token/revoke-self": {"update"},
        "sys/capabilities-self": {"update"},
        "sys/internal/ui/resultant-acl": {"read"},
    }
    write_capabilities = {"create", "update", "delete", "patch", "sudo"}

    assert {path: capabilities for path, capabilities in grants if path in self_grants} == self_grants
    grants = [(path, capabilities) for path, capabilities in grants if path not in self_grants]
    assert {path for path, _ in grants} == read_paths | system_metadata_paths | write_paths
    assert {
        path for path, capabilities in grants if capabilities == {"read"}
    } == data_read_paths
    assert {
        path for path, capabilities in grants if capabilities == {"read", "list"}
    } == (read_paths - data_read_paths) | system_metadata_paths
    assert {
        path: capabilities
        for path, capabilities in grants
        if capabilities.intersection(write_capabilities)
    } == {
        "secrets-external/data/ai/saas/opencode": {"create", "read", "update"},
        "secrets-external/data/ai/saas/zai": {"create", "read", "update"},
        "ext-ai/data/opencode/main/rw": {"create", "read", "update"},
        "ext-ai/data/zai/main/rw": {"create", "read", "update"},
    }
    assert not any("delete" in capabilities for _, capabilities in grants)
    assert not any(
        path.startswith(("sys/", "auth/"))
        and capabilities.intersection(write_capabilities)
        for path, capabilities in grants
    )


def test_policy_is_registered_and_secret_uses_the_generated_authelia_path():
    defaults = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))
    policy_defaults = yaml.safe_load(POLICY_DEFAULTS.read_text(encoding="utf-8"))
    authelia_defaults = yaml.safe_load(AUTHELIA_DEFAULTS.read_text(encoding="utf-8"))
    authelia_group_defaults = yaml.safe_load(AUTHELIA_GROUP_DEFAULTS.read_text(encoding="utf-8"))
    authelia_url_defaults = yaml.safe_load(AUTHELIA_URL_DEFAULTS.read_text(encoding="utf-8"))
    secret_defaults = yaml.safe_load(SECRET_DEFAULTS.read_text(encoding="utf-8"))
    auth_tasks = yaml.safe_load(AUTH_TASKS.read_text(encoding="utf-8"))
    parent = yaml.safe_load(AUTH_PARENT.read_text(encoding="utf-8"))

    assert defaults["openbao_operator_oidc_auth_path"] == "oidc"
    assert defaults["openbao_operator_oidc_role_name"] == "operator"
    assert defaults["openbao_operator_human_policy_name"] == "operator-human"
    assert defaults["openbao_operator_oidc_client_id"] == authelia_defaults[
        "authelia_oidc_openbao_ui_client_id"
    ]
    assert defaults["openbao_authelia_operator_group"] == authelia_group_defaults[
        "authelia_operator_group"
    ]
    assert authelia_url_defaults["authelia_openbao_ui_public_url"] == (
        "{{ lookup('env', 'BAO_ADDR') | default('', true) | regex_replace('/+$', '') }}"
    )
    assert "OPENBAO_AUTHELIA_OPERATOR_GROUP" in defaults["openbao_authelia_operator_group"]
    assert "authelia_oidc_openbao_ui_client_secret" in secret_defaults[
        "openbao_generated_app_secrets"
    ]["authelia"]
    assert {
        "name": "{{ openbao_operator_human_policy_name }}",
        "template": "operator-human-policy.hcl.j2",
    } in policy_defaults["openbao_base_policies_static"]

    assert any(
        task.get("name") == "Refuse a conflicting auth method at the operator OIDC path"
        for task in auth_tasks
    )
    assert any(
        task.get("name") == "Configure the OpenBao UI OIDC operator login"
        and task["ansible.builtin.import_tasks"] == "09g-openbao-ui-operator-oidc.yml"
        for task in parent
    )
    secret_read = next(
        task
        for task in auth_tasks
        if task.get("name") == "Read the Authelia OpenBao UI client secret from OpenBao"
    )
    assert secret_read["no_log"] is True
    assert "authelia_oidc_openbao_ui_client_secret_path" in secret_read[
        "ansible.builtin.command"
    ]["cmd"]
