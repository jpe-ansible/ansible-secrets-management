"""The Semaphore policy grants only the router's declared app reads."""

from pathlib import Path

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "roles" / "openbao" / "templates" / "semaphore-policy.hcl.j2"


def _render(kv_mount: str, config_mount: str = "config") -> str:
    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        "ansible_managed": "Ansible managed",
        "openbao_kv_mount": kv_mount,
        "openbao_config_mount": config_mount,
        "openbao_github_everyday_mount": "github-everyday",
        "openbao_semaphore_github_raw_read_permissions": {"contents": "read"},
        "openbao_semaphore_github_read_permission_sets": [],
        "openbao_github_dispatch_permission_sets": [],
    }
    return templar.template(trust_as_template(POLICY.read_text(encoding="utf-8")))


def test_router_app_entries_render_as_exact_read_only_kv_v2_grants():
    kv_mount = "secrets-store"
    policy = _render(kv_mount)

    for app in ("benchmark", "sandbox-agent"):
        assert (
            f'path "{kv_mount}/data/apps/{app}" {{\n  capabilities = ["read"]\n}}'
        ) in policy
        assert (
            f'path "{kv_mount}/metadata/apps/{app}" {{\n'
            '  capabilities = ["read", "list"]\n'
            "}"
        ) in policy

    assert f'path "{kv_mount}/data/apps/*"' not in policy
    assert f'path "{kv_mount}/metadata/apps/*"' not in policy


def test_run_environment_document_is_declared_by_the_converge_policy_only():
    policy = _render("secrets-store", config_mount="topology-config")

    assert "platform/ansible/env" not in policy
    assert 'path "topology-config/data/*"' not in policy


def test_raw_github_mint_allows_the_read_map_and_the_census_map_only():
    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        "ansible_managed": "Ansible managed",
        "openbao_kv_mount": "secret",
        "openbao_config_mount": "config",
        "openbao_github_everyday_mount": "github",
        "openbao_semaphore_github_raw_read_permissions": {"contents": "read", "metadata": "read"},
        "openbao_semaphore_github_census_read_permissions": {
            "contents": "read",
            "metadata": "read",
            "pull_requests": "read",
        },
        "openbao_semaphore_github_read_permission_sets": [],
        "openbao_github_dispatch_permission_sets": [],
    }
    policy = templar.template(trust_as_template(POLICY.read_text(encoding="utf-8")))

    assert (
        '    "permissions" = [{ "contents" = "read", "metadata" = "read" }, '
        '{ "contents" = "read", "metadata" = "read", "pull_requests" = "read" }]'
    ) in policy


def test_raw_github_mint_without_census_map_keeps_the_single_read_map():
    policy = _render("secret")

    assert '    "permissions" = [{ "contents" = "read" }]' in policy
