"""Every path read with the `apps` AppRole is readable by the `apps` policy.

The repo-owned domain catalog assigns each path to the `apps` AppRole.
The policy must grant each declared path. Its per-app grants come from
openbao_apps_read_apps (roles/openbao/defaults/main/05c-...), rendered here
from the real expression with the real seeding maps; infrastructure/unifi is
granted directly by apps-policy.hcl.j2.
"""

from __future__ import annotations

from pathlib import Path
import re

import jinja2
import pytest
import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles" / "openbao" / "defaults" / "main"
NAMES_FILE = DEFAULTS / "05c-terrakube-and-remaining-domain-names.yml"
GENERATED_FILE = DEFAULTS / "01c-app-secrets-generated.yml"
GENERATED_PATHS_FILE = DEFAULTS / "01d-app-secret-paths.yml"
PROMOTED_FILE = DEFAULTS / "01b-app-secrets.yml"
CRIBL_EDGE_FILE = DEFAULTS / "05h-cribl-edge-readers.yml"
DOMAINS_FILE = ROOT / "playbooks" / "group_vars" / "all" / "openbao_secrets.yml"
POLICY_TEMPLATE = ROOT / "roles" / "openbao" / "templates" / "apps-policy.hcl.j2"
MEDIA_POLICY_TEMPLATE = ROOT / "roles" / "openbao" / "templates" / "media-policy.hcl.j2"
PATH_BLOCK = re.compile(
    r'(?m)^path "([^"]+)"\s*\{\s*capabilities\s*=\s*\[([^]]*)\]'
)
WRITE_CAPABILITIES = {"create", "update", "patch", "delete", "sudo"}
EVAL_LEAVES = ("hatchet/eval",)


def _yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _read_apps(names: dict) -> set[str]:
    cribl_edge = _yaml(CRIBL_EDGE_FILE)
    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        "openbao_generated_app_secrets": _yaml(GENERATED_FILE)["openbao_generated_app_secrets"],
        "openbao_generated_app_secret_paths": _yaml(GENERATED_PATHS_FILE)["openbao_generated_app_secret_paths"],
        "openbao_promoted_app_secrets": _yaml(PROMOTED_FILE)["openbao_promoted_app_secrets"],
        "openbao_router_key_catalog": names.get("openbao_router_key_catalog", {}),
        "openbao_apps_read_published_apps": names.get("openbao_apps_read_published_apps", []),
        "openbao_cribl_edge_mac_a_app": cribl_edge["openbao_cribl_edge_mac_a_app"],
        "openbao_cribl_edge_mac_b_app": cribl_edge["openbao_cribl_edge_mac_b_app"],
    }
    templar.available_variables["openbao_apps_read_excluded_generated_apps"] = (
        [
            templar.template(trust_as_template(app))
            for app in cribl_edge["openbao_apps_read_excluded_generated_apps"]
        ]
    )
    return set(templar.template(trust_as_template(names["openbao_apps_read_apps"])))


def _apps_domain_paths() -> list[str]:
    for domain in _yaml(DOMAINS_FILE)["openbao_secrets_domains"]:
        if domain["name"] == "apps":
            return [p["path"] if isinstance(p, dict) else p for p in domain["paths"]]
    raise AssertionError("no `apps` domain in openbao_secrets_domains")


def _domain(name: str) -> dict:
    for domain in _yaml(DOMAINS_FILE)["openbao_secrets_domains"]:
        if domain["name"] == name:
            return domain
    raise AssertionError(f"no `{name}` domain in openbao_secrets_domains")


def _media_domain_paths() -> list[str]:
    return [
        item["path"] if isinstance(item, dict) else item
        for item in _domain("media")["paths"]
    ]


def _unreadable(paths: list[str], read_apps: set[str], template_text: str) -> list[str]:
    missing = []
    for path in paths:
        if path.startswith("apps/") and path.split("/", 1)[1] in read_apps:
            continue
        if f"data/{path}\"" in template_text:
            continue
        missing.append(path)
    return missing


def _render_apps_policy(read_apps: set[str]) -> str:
    environment = jinja2.Environment()
    environment.filters["comment"] = str
    return environment.from_string(POLICY_TEMPLATE.read_text(encoding="utf-8")).render(
        ansible_managed="",
        openbao_kv_mount="secret",
        openbao_apps_read_apps=sorted(read_apps),
    )


def _policy_grants(policy: str) -> set[tuple[str, tuple[str, ...]]]:
    return {
        (path, tuple(re.findall(r'"([^"]+)"', capabilities)))
        for path, capabilities in PATH_BLOCK.findall(policy)
    }


def _render_media_policy(external_paths: tuple[str, ...] = ()) -> str:
    environment = jinja2.Environment()
    environment.filters["comment"] = str
    return environment.from_string(MEDIA_POLICY_TEMPLATE.read_text(encoding="utf-8")).render(
        ansible_managed="",
        openbao_kv_mount="secret",
        openbao_media_external_paths=list(external_paths),
    )


def test_every_apps_domain_path_is_granted_to_the_apps_reader():
    read_apps = _read_apps(_yaml(NAMES_FILE))
    missing = _unreadable(_apps_domain_paths(), read_apps, POLICY_TEMPLATE.read_text(encoding="utf-8"))
    assert not missing, (
        f"the `apps` domain reads {missing}, which the `apps` policy does not grant; "
        "the domain fetch fails on the 403. Add the bucket to a seeding map or to "
        "openbao_apps_read_published_apps."
    )


@pytest.mark.parametrize("app,field", [
    ("langflow", "langflow_llm_router_key"),
    ("grafana-llm", "grafana_llm_router_key"),
    ("crawl4ai", "crawl4ai_api_token"),
    ("next-ai-drawio", "next_ai_drawio_llm_router_key"),
])
def test_generated_apps_have_exact_read_only_grants(app, field):
    names = _yaml(NAMES_FILE)
    assert _yaml(GENERATED_FILE)["openbao_generated_app_secrets"][app] == [field]
    assert app not in names["openbao_apps_read_published_apps"]
    assert app not in _yaml(GENERATED_PATHS_FILE)["openbao_generated_app_secret_paths"]

    grants = _policy_grants(_render_apps_policy(_read_apps(names)))
    app_grants = {
        (path, capabilities)
        for path, capabilities in grants
        if path.endswith(f"/apps/{app}")
    }
    assert app_grants == {
        (f"secret/data/apps/{app}", ("read",)),
        (f"secret/metadata/apps/{app}", ("read", "list")),
    }
    assert not any(
        path.startswith(("secret/data/apps/", "secret/metadata/apps/"))
        and ("*" in path or "+" in path)
        for path, _ in grants
    )


def test_grafana_service_bucket_stays_outside_the_apps_reader():
    assert "grafana" not in _yaml(GENERATED_FILE)["openbao_generated_app_secrets"]
    assert "grafana" not in _read_apps(_yaml(NAMES_FILE))
    grants = _policy_grants(_render_apps_policy(_read_apps(_yaml(NAMES_FILE))))
    for kind in ("data", "metadata"):
        assert not any(
            path in {f"secret/{kind}/apps/grafana", f"secret/{kind}/apps/*"}
            for path, _ in grants
        )


def test_retired_dify_eval_leaf_is_not_granted_to_the_apps_reader():
    read_apps = _read_apps(_yaml(NAMES_FILE))
    assert "dify/eval" not in read_apps
    grants = _policy_grants(_render_apps_policy(read_apps))
    assert not any(path.endswith("/apps/dify/eval") for path, _ in grants)


@pytest.mark.parametrize("leaf", EVAL_LEAVES)
def test_eval_leaf_adds_only_its_exact_read_grant_for_the_apps_reader(leaf):
    names = _yaml(NAMES_FILE)
    published = names["openbao_apps_read_published_apps"]
    assert published.count(leaf) == 1

    without_leaf = dict(names)
    without_leaf["openbao_apps_read_published_apps"] = [
        app for app in published if app != leaf
    ]
    previous_apps = _read_apps(without_leaf)
    read_apps = _read_apps(names)
    assert read_apps - previous_apps == {leaf}

    previous_grants = _policy_grants(_render_apps_policy(previous_apps))
    grants = _policy_grants(_render_apps_policy(read_apps))
    added_grants = grants - previous_grants
    assert added_grants == {
        (f"secret/data/apps/{leaf}", ("read",)),
        (f"secret/metadata/apps/{leaf}", ("read", "list")),
    }
    assert not any(
        WRITE_CAPABILITIES.intersection(capabilities)
        for _, capabilities in added_grants
    )


def test_hatchet_apps_reader_has_exact_read_only_leaf_grants():
    policy = _render_apps_policy(_read_apps(_yaml(NAMES_FILE)))
    grants = _policy_grants(policy)

    assert {
        ("secret/data/apps/hatchet/worker-token", ("read",)),
        ("secret/metadata/apps/hatchet/worker-token", ("read", "list")),
        ("secret/data/apps/hatchet/eval", ("read",)),
        ("secret/metadata/apps/hatchet/eval", ("read", "list")),
    } <= grants
    assert not any(
        path.endswith("apps/hatchet/*") for path, _ in grants
    )
    assert not any(
        WRITE_CAPABILITIES.intersection(capabilities)
        for path, capabilities in grants
        if path.startswith(("secret/data/apps/hatchet", "secret/metadata/apps/hatchet"))
    )


def test_vikunja_generated_password_coexists_with_promoted_fields():
    generated = _yaml(GENERATED_FILE)["openbao_generated_app_secrets"]["vikunja"]
    promoted = _yaml(PROMOTED_FILE)["openbao_promoted_app_secrets"]["vikunja"]
    readers = _yaml(DEFAULTS / "05k-agent-tier-secret-paths.yml")[
        "openbao_app_agent_tier_readers"
    ]
    tier_fields = {
        field
        for reader in readers
        if reader["tier"].startswith("vikunja-")
        for field in reader.get("login_fields", [])
    }

    assert {"vikunja_agent_read_password", "vikunja_agent_write_password"} == tier_fields
    assert not any("vikunja_agent_" in field for reader in readers for field in reader.get("generated_fields", []))
    assert not tier_fields.intersection(generated)
    assert promoted
    assert not set(generated).intersection(promoted)
    assert "vikunja" in _read_apps(_yaml(NAMES_FILE))


def test_vikunja_generated_login_fields_cover_the_openhands_bot_user():
    generated = _yaml(GENERATED_FILE)["openbao_generated_app_secrets"]["vikunja"]
    assert generated == [
        "donna_login_password",
        "hermes_login_password",
        "ai_jobs_login_password",
        "openhands_login_password",
        "svc_mcp_clerk_password",
    ]
    assert "vikunja" in _read_apps(_yaml(NAMES_FILE))


def test_zammad_agent_write_token_is_generated_with_the_app_credentials():
    generated = _yaml(GENERATED_FILE)["openbao_generated_app_secrets"]
    promoted = _yaml(PROMOTED_FILE)["openbao_promoted_app_secrets"]
    readers = _yaml(DEFAULTS / "05k-agent-tier-secret-paths.yml")[
        "openbao_app_agent_tier_readers"
    ]
    zammad_reader = next(reader for reader in readers if reader["tier"] == "zammad-write")

    assert zammad_reader["generated_fields"] == ["zammad_agent_write_api_token"]
    assert "zammad_agent_write_api_token" not in generated["zammad"]
    assert len(generated["zammad"]) == len(set(generated["zammad"]))
    assert "zammad_agent_write_api_token" not in promoted.get("zammad", {})


def test_youtrack_write_tier_reader_generates_no_field():
    readers = _yaml(DEFAULTS / "05k-agent-tier-secret-paths.yml")[
        "openbao_app_agent_tier_readers"
    ]
    reader = next(reader for reader in readers if reader["tier"] == "youtrack-write")

    assert "generated_fields" not in reader
    assert "login_path" not in reader
    assert reader["trust_class"] == "trusted-agent-read"


def test_idrac_console_user_paths_are_not_prefetched_and_have_exact_reads():
    paths = _domain("apps")["paths"]
    console_paths = {
        item["path"] if isinstance(item, dict) else item: item
        for item in paths
        if (item["path"] if isinstance(item, dict) else item).startswith("apps/idrac-kvm-")
    }
    assert console_paths == {}

    promoted_apps = _yaml(PROMOTED_FILE)["openbao_promoted_app_secrets"]
    assert not {"idrac-kvm-r410", "idrac-kvm-r710"} & set(promoted_apps)

    policy = _render_apps_policy(_read_apps(_yaml(NAMES_FILE)))
    for app in ("idrac-kvm-r410", "idrac-kvm-r710"):
        assert f'path "secret/data/apps/{app}" {{\n  capabilities = ["read"]\n}}' in policy
        assert f'path "secret/metadata/apps/{app}" {{\n  capabilities = ["read", "list"]\n}}' in policy
    assert 'path "secret/data/apps/idrac-kvm-*"' not in policy


def test_media_domain_prefetches_sortarr_and_autobrr_paths():
    media_paths = _media_domain_paths()

    assert "apps/media/sortarr" in media_paths
    assert "apps/media/autobrr" in media_paths
    assert "apps/media/autobrr-private" in media_paths
    assert "apps/media/autobrr-priority" in media_paths


def test_every_media_domain_path_has_a_media_reader_grant():
    media_paths = _media_domain_paths()
    policy = _render_media_policy()
    read_grant = 'path "secret/data/apps/media/*" {\n  capabilities = ["read"]\n}'

    assert media_paths
    assert all(path.startswith("apps/media/") for path in media_paths)
    assert read_grant in policy



def test_media_policies_have_only_the_requested_exact_new_grants():
    internal = {
        "sonarr/main/rw", "radarr/main/rw", "prowlarr/main/rw", "seerr/main/rw",
        "qbittorrent/main/admin", "sortarr/main/admin", "autobrr/main/admin",
        "autobrr/priority/ro",
    }
    external = {
        "plex/main/rw",
    }
    expected = {
        (f"{mount}/{kind}/{path}", ("read",))
        for mount, paths in (("secret", internal), ("secrets-external", external))
        for path in paths for kind in ("data", "metadata")
    }
    cutover = {
        ("secret/data/apps/media/*", ("read",)),
        ("secret/metadata/apps/media/*", ("read", "list")),
    }
    assert _policy_grants(_render_media_policy()) == expected | cutover
    listed = ("example-vpn/primary/rw", "example-vpn/backup/rw", "example-indexer/main/rw")
    assert _policy_grants(_render_media_policy(listed)) == expected | cutover | {
        (f"secrets-external/{kind}/{path}", ("read",))
        for path in listed for kind in ("data", "metadata")
    }

    environment = jinja2.Environment()
    environment.filters["comment"] = str
    rotate = environment.from_string(
        (MEDIA_POLICY_TEMPLATE.parent / "media-rotate-policy.hcl.j2").read_text(encoding="utf-8")
    ).render(ansible_managed="", openbao_kv_mount="secret")
    rotated = internal - {"autobrr/priority/ro"}
    assert _policy_grants(rotate) == {
        (f"secret/{kind}/{path}", capabilities)
        for path in rotated
        for kind, capabilities in (("data", ("read", "update")), ("metadata", ("read", "patch")))
    }
    assert rotate.count('allowed_parameters = { "custom_metadata" = [] }') == len(rotated)


def test_media_external_paths_accept_only_exact_four_segment_entries():
    pattern = re.compile(_yaml(NAMES_FILE)["openbao_media_external_path_pattern"])
    for good in ("example-vpn/primary/rw", "example-indexer/main/ro", "x/main/admin"):
        assert pattern.match(good)
    for bad in ("*", "example/*", "example/main", "example/main/rw/extra", "Example/main/rw",
                "example/main/write", "../main/rw"):
        assert not pattern.match(bad)


def test_openproject_secret_is_promoted_and_prefetched():
    assert "apps/openproject" in _apps_domain_paths()
    assert _yaml(PROMOTED_FILE)["openbao_promoted_app_secrets"]["openproject"] == {
        "openproject_secret_key_base": "OPENPROJECT_SECRET_KEY_BASE"
    }


def test_vikunja_task_webhook_secret_is_its_own_generated_apps_leaf():
    generated = _yaml(GENERATED_FILE)["openbao_generated_app_secrets"]
    assert generated["vikunja-task-webhook"] == ["vikunja_task_webhook_secret"]
    assert not any(
        "vikunja_task_webhook_secret" in fields for app, fields in generated.items() if app != "vikunja-task-webhook"
    )
    assert "apps/vikunja-task-webhook" in _apps_domain_paths()
    assert "vikunja-task-webhook" in _read_apps(_yaml(NAMES_FILE))

    policy = _render_apps_policy(_read_apps(_yaml(NAMES_FILE)))
    for kind in ("data", "metadata"):
        assert f'path "secret/{kind}/apps/vikunja-task-webhook"' in policy


def test_openhands_fields_are_prefetched_by_the_apps_domain():
    generated = _yaml(GENERATED_FILE)["openbao_generated_app_secrets"]["openhands"]
    assert generated == [
        "openhands_llm_router_key",
        "openhands_backend_api_key",
        "openhands_secret_key",
        "openhands_webhook_secret",
    ]
    assert "apps/openhands" in _apps_domain_paths()
    assert "openhands" in _read_apps(_yaml(NAMES_FILE))

    policy = _render_apps_policy(_read_apps(_yaml(NAMES_FILE)))
    for kind in ("data", "metadata"):
        assert f'path "secret/{kind}/apps/openhands"' in policy
    assert 'path "secret/data/apps/*"' not in policy


def test_benchmark_and_promoted_sandbox_agent_paths_render_in_apps_policy():
    policy = _render_apps_policy(_read_apps(_yaml(NAMES_FILE)))

    for app in ("benchmark", "sandbox-agent"):
        assert f'path "secret/data/apps/{app}"' in policy
        assert f'path "secret/metadata/apps/{app}"' in policy


def test_a_published_only_bucket_is_missing_without_the_published_list():
    names = dict(_yaml(NAMES_FILE))
    names["openbao_apps_read_published_apps"] = []
    read_apps = _read_apps(names)
    missing = _unreadable(_apps_domain_paths(), read_apps, POLICY_TEMPLATE.read_text(encoding="utf-8"))
    assert "apps/pve-exporter" in missing


def test_the_ci_resolver_bucket_is_not_granted_to_the_apps_reader():
    assert "ci-resolver" in _yaml(PROMOTED_FILE)["openbao_promoted_app_secrets"]
    assert "ci-resolver" not in _read_apps(_yaml(NAMES_FILE))


def test_postgres_backup_domain_reuses_apps_credentials_and_is_optional():
    domain = _domain("postgres_backup_s3")

    assert domain["credential_domain"] == "apps"
    assert domain["paths"] == [
        {"path": "rustfs/dryvist-homelab-pgbackrest/rw", "optional": True}
    ]


def test_postgres_backup_paths_have_exact_read_grants():
    policy = _render_apps_policy(_read_apps(_yaml(NAMES_FILE)))

    for bucket in ("dryvist-homelab-backups", "dryvist-homelab-pgbackrest"):
        assert (
            f'path "secret/data/rustfs/{bucket}/rw" {{\n'
            '  capabilities = ["read"]\n}'
        ) in policy
    assert 'path "secret/data/rustfs/*"' not in policy


@pytest.mark.parametrize("service", ["homebox", "nautobot"])
def test_backblaze_domain_reuses_apps_credentials_and_is_optional(service):
    domain = _domain(f"{service}_backup_b2")

    assert domain["credential_domain"] == "apps"
    assert domain["paths"] == [
        {
            "mount": "secrets-external",
            "path": f"backblaze/dryvist-{service}-backups/rw",
            "optional": True,
        }
    ]


@pytest.mark.parametrize("service", ["homebox", "nautobot"])
def test_backblaze_path_has_exact_external_grants_and_no_wildcard(service):
    policy = _render_apps_policy(_read_apps(_yaml(NAMES_FILE)))

    for kind in ("data", "metadata"):
        assert (
            f'path "secrets-external/{kind}/backblaze/dryvist-{service}-backups/rw" {{\n'
            '  capabilities = ["read"]\n}'
        ) in policy
    assert 'path "secrets-external/data/backblaze/*"' not in policy
    assert 'path "secrets-external/metadata/backblaze/*"' not in policy


def test_opencode_key_has_one_exact_external_read_grant():
    policy = _render_apps_policy(_read_apps(_yaml(NAMES_FILE)))

    assert (
        'path "secrets-external/data/ai/saas/opencode" {\n'
        '  capabilities = ["read"]\n}'
    ) in policy
    assert 'path "secrets-external/data/ai/saas/*"' not in policy
    assert 'path "secrets-external/data/ai/*"' not in policy


def test_grafana_alerts_domain_reads_one_exact_external_leaf_for_the_apps_reader():
    domain = _domain("grafana-alerts")

    assert domain["credential_domain"] == "apps"
    assert domain["paths"] == [
        {
            "mount": "secrets-external",
            "path": "slack/homelab-ops/rw",
            "optional": True,
        }
    ]


def test_grafana_alerts_path_has_exact_read_only_data_and_metadata_grants():
    policy = _render_apps_policy(_read_apps(_yaml(NAMES_FILE)))
    grants = _policy_grants(policy)

    for kind in ("data", "metadata"):
        assert (
            f'path "secrets-external/{kind}/platform/slack-ops" {{\n'
            '  capabilities = ["read"]\n}'
        ) in policy
        assert (
            f'path "secrets-external/{kind}/slack/homelab-ops/rw" {{\n'
            '  capabilities = ["read"]\n}'
        ) in policy
    assert {
        ("secrets-external/data/platform/slack-ops", ("read",)),
        ("secrets-external/metadata/platform/slack-ops", ("read",)),
        ("secrets-external/data/slack/homelab-ops/rw", ("read",)),
        ("secrets-external/metadata/slack/homelab-ops/rw", ("read",)),
    } <= grants
    assert not any(
        WRITE_CAPABILITIES.intersection(capabilities)
        for path, capabilities in grants
        if "slack-ops" in path or "slack/homelab-ops" in path
    )
    assert 'path "secrets-external/data/platform/*"' not in policy
    assert 'path "secrets-external/metadata/platform/*"' not in policy
    assert 'path "secrets-external/data/slack/*"' not in policy
    assert 'path "secrets-external/metadata/slack/*"' not in policy
    assert 'path "secrets-external/data/*"' not in policy
