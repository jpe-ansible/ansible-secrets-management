"""Rendered reconcile KV grants match their named consumers."""

from openbao_reconcile_bounds_helpers import (
    _allowed_parameters, _attached_stanzas, _capabilities, _effective_policy_union, _render,
    _stanzas, rendered_defaults, FLOW_LOCK, RECONCILE
)

def test_reconcile_does_not_grant_per_app_mount_configuration(rendered_defaults):
    values, _approles, _policies = rendered_defaults
    per_app_mounts = [
        {"mount": "github-public"},
        {"mount": "github-private"},
    ]
    context = dict(values, openbao_github_app_mounts=per_app_mounts)
    reconcile = _render(RECONCILE, context)
    paths = {path for path, _body in _stanzas(reconcile)}

    assert f"{values['openbao_github_mount']}/permissionset/*" in paths
    assert "github-agents/permissionset/agents-write" in paths
    for mount in per_app_mounts:
        assert f"{mount['mount']}/permissionset/*" in paths
    assert not any(path.startswith("sys/mounts/github-") for path in paths)

def test_reconcile_kv_grants_match_named_consumers_and_keep_flow_lock_separate(
    rendered_defaults,
):
    values, _approles, _policies = rendered_defaults
    context = dict(
        values,
        openbao_kv_mount="secret",
        openbao_config_mount="config",
        openbao_promoted_app_secrets={"promoted": {"TOKEN": "TOKEN"}},
        openbao_promoted_external_secrets={"external": {"TOKEN": "TOKEN"}},
        openbao_promoted_config_values={"review": {"base_url": "LLM_ROUTER_BASE_URL"}},
        openbao_seeded_generated_app_secrets={
            "generated": ["generated_key"],
            "clickhouse": ["APP_PASSWORD"],
        },
        openbao_generated_app_secret_paths={"clickhouse": "ai/clickhouse"},
        openbao_roster_agent_generated_app_secrets={"agent-one": ["agent_key"]},
        openbao_caller_gateway_generated_app_secrets={"caller-gw": ["caller_key"]},
        openbao_rotation_exempt=["secret:apps/n8n"],
        openbao_kv_tuned_mounts=[{"path": "config", "max_versions": 30}],
    )
    reconcile = _render(RECONCILE, context)
    reconcile_stanzas = dict(_stanzas(reconcile))
    expected_data = {
        "secret/data/apps/promoted": ["create", "read", "update"],
        "secrets-external/data/external": ["create", "read", "update"],
        "config/data/review": ["create", "read", "update"],
        f"{values['openbao_arrangement_kv_mount']}/data/"
        f"{values['openbao_arrangement_kv_path']}": ["read"],
        "secret/data/apps/generated": ["create", "read", "update"],
        "secret/data/ai/clickhouse": ["create", "read", "update"],
        "secret/data/apps/agent-one": ["create", "read", "update"],
        "secret/data/apps/caller-gw": ["create", "read", "update"],
        "secret/data/apps/semaphore": ["read"],
        "secret/data/apps/grafana": ["read"],
        "secret/data/platform/splunk/main": ["read"],
        "config/data/platform/ansible/env": ["read"],
        "secret/data/platform/ansible/env": ["read"],
        "secret/data/platform/terrakube/main": ["read"],
    }
    actual_data_paths = {
        path for path in reconcile_stanzas
        if "/data/" in path and path.startswith(("secret/", "secrets-external/", "config/"))
    }
    assert actual_data_paths == set(expected_data)
    for path, capabilities in expected_data.items():
        assert _capabilities(reconcile_stanzas[path]) == capabilities, path

    expected_metadata = {
        "secret/metadata/apps/n8n",
        "secret/metadata/apps/agent-one",
        "secret/metadata/apps/caller-gw",
    }
    actual_metadata_paths = {
        path for path in reconcile_stanzas
        if "/metadata/" in path and path.startswith(("secret/", "secrets-external/", "config/"))
    }
    assert actual_metadata_paths == expected_metadata
    for path in expected_metadata:
        body = reconcile_stanzas[path]
        assert _capabilities(body) == ["read", "patch"], path
        assert _allowed_parameters(body) == {"custom_metadata": []}, path

    retention = reconcile_stanzas["config/config"]
    assert _capabilities(retention) == ["read", "update"]
    assert _allowed_parameters(retention) == {"max_versions": ["30"]}
    assert {
        path for path in reconcile_stanzas
        if path.endswith("/config") and path.startswith(("secret/", "secrets-external/", "config/"))
    } == {"config/config"}

    kv_paths = [
        path for path in reconcile_stanzas
        if path.startswith(("secret/data/", "secret/metadata/", "secrets-external/data/", "config/data/"))
    ]
    assert all("*" not in path and "+" not in path for path in kv_paths)
    assert not {
        "secret/data/apps/unlisted",
        "secret/data/ai/unlisted",
        "secret/data/ai/mcp/splunk",
        "secret/data/ai/mcp/cribl",
        "secret/metadata/apps/unlisted",
        "secret/metadata/ai/mcp/splunk",
        "secret/metadata/ai/mcp/cribl",
        "config/data/unlisted",
    } & reconcile_stanzas.keys()
    assert "secret/data/infra/rustfs" not in reconcile_stanzas

    flow_lock_stanzas = dict(_stanzas(_render(FLOW_LOCK, context)))
    assert _capabilities(flow_lock_stanzas["secret/data/locks/global"]) == [
        "create", "update", "read"
    ]
    assert _capabilities(flow_lock_stanzas["secret/metadata/locks/global"]) == [
        "delete"
    ]
    assert _capabilities(flow_lock_stanzas["secret/data/infra/*"]) == ["read"]
    assert _capabilities(flow_lock_stanzas["secret/metadata/infra/*"]) == [
        "read", "list"
    ]

    # The default generated-seed map includes semaphore; adding the dispatch
    # helper's read path must retain those named seed capabilities.
    default_context = dict(values)
    default_context["openbao_seeded_generated_app_secrets"] = default_context[
        "openbao_generated_app_secrets"
    ]
    default_reconcile_stanzas = dict(_stanzas(_render(RECONCILE, default_context)))
    assert _capabilities(default_reconcile_stanzas["secret/data/apps/semaphore"]) == [
        "create", "read", "update"
    ]
    assert _capabilities(
        default_reconcile_stanzas["secret/data/platform/splunk/main"]
    ) == ["read"]

def test_reconcile_splunk_read_uses_the_declared_mount_and_setdefault(
    rendered_defaults,
):
    values, _approles, _policies = rendered_defaults
    mount = "fixture-kv"
    context = dict(
        values,
        openbao_kv_mount=mount,
        openbao_config_mount=mount,
        openbao_promoted_config_values={
            "platform/splunk/main": {"endpoint": "SPLUNK_ENDPOINT"}
        },
    )
    stanzas = dict(_stanzas(_render(RECONCILE, context)))
    splunk_path = f"{mount}/data/platform/splunk/main"

    assert _capabilities(stanzas[splunk_path]) == ["create", "read", "update"]
    assert "secret/data/platform/splunk/main" not in stanzas

def test_workstation_reconcile_identity_reads_its_declared_leaves(rendered_defaults):
    values, approles, policies = rendered_defaults
    attached_stanzas = _attached_stanzas(
        values, approles, policies, values["openbao_reconcile_approle_name"]
    )
    env_path = values["openbao_platform_env_path"]

    for path in (
        f"{values['openbao_config_mount']}/data/{env_path}",
        f"{values['openbao_kv_mount']}/data/{env_path}",
        f"{values['openbao_kv_mount']}/data/platform/terrakube/main",
    ):
        assert _effective_policy_union(attached_stanzas, path) == {"read"}, path
