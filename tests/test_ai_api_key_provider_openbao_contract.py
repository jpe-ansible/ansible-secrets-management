"""Static contracts for provider-level API credentials in OpenBao."""

import re
from pathlib import Path

import jinja2
import yaml


ROOT = Path(__file__).resolve().parents[1]
PROVIDERS = [
    "openrouter",
    "gemini",
    "alibaba",
    "openai",
    "anthropic",
    "grok",
    "deepseek",
    "zai",
    "nvidia",
    "moonshotai",
    "opencode",
]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _read_defaults(filename: str) -> dict:
    return yaml.safe_load(_read(f"roles/openbao/defaults/main/{filename}"))


def _render_local_llm_policy() -> str:
    environment = jinja2.Environment()
    environment.filters["comment"] = lambda value: "# " + str(value)
    return environment.from_string(
        _read("roles/openbao/templates/local-llm-policy.hcl.j2")
    ).render(ansible_managed="test fixture", openbao_kv_mount="secret")


def _policy_grants(policy: str) -> list[tuple[str, list[str]]]:
    stanzas = re.findall(
        r'(?ms)^path "([^"]+)" \{\s*capabilities = \[([^\]]+)\]\s*\}',
        policy,
    )
    return [
        (path, [capability.strip().strip('"') for capability in capabilities.split(",")])
        for path, capabilities in stanzas
    ]


def test_provider_inventory_is_complete_and_single_sourced():
    names = _read_defaults("05c-terrakube-and-remaining-domain-names.yml")

    assert names["openbao_ai_api_key_providers"] == PROVIDERS

    derived = _read("roles/openbao/defaults/main/07a-derived-rollups-and-ttls.yml")
    assert "openbao_ai_api_key_policy_names" in derived
    assert "openbao_ai_api_key_policies" in derived
    assert "ai-api-key-\\1" in derived
    assert '"provider": "\\1"' in derived

    defaults_source = _read(
        "roles/openbao/defaults/main/05c-terrakube-and-remaining-domain-names.yml"
    )
    assert "OPENBAO_AI_API_KEY_MOUNT" in defaults_source
    assert "OPENBAO_AI_API_KEY_PATH_PREFIX" in defaults_source
    # 2 provider-key vars + 2 environment-specific Terrakube workspace names.
    assert defaults_source.count("default(undef(") == 4


def test_provider_policy_is_external_exact_and_read_only():
    template = _read("roles/openbao/templates/ai-api-key-provider-policy.hcl.j2")
    declarations = [
        line for line in template.splitlines() if line.startswith('path "')
    ]

    assert declarations == [
        'path "{{ openbao_ai_api_key_mount }}/data/{{ openbao_ai_api_key_path_prefix }}/{{ item.provider }}" {',
        'path "{{ openbao_ai_api_key_mount }}/metadata/{{ openbao_ai_api_key_path_prefix }}/{{ item.provider }}" {',
    ]
    assert 'capabilities = ["read"]' in template
    assert 'capabilities = ["read", "list"]' in template
    assert "create" not in template
    assert "update" not in template
    assert "ai/saas" not in template
    assert "openbao_kv_mount" not in template


def test_local_llm_attaches_the_derived_provider_policy_set():
    approles = _read("roles/openbao/defaults/main/07b-base-approles.yml")
    policies = _read("roles/openbao/defaults/main/07c-policy-composition.yml")

    assert "[openbao_local_llm_policy_name] + openbao_ai_api_key_policy_names" in approles
    assert "+ openbao_ai_api_key_policies" in policies
    assert "ai_saas" not in approles
    assert "ai_saas" not in policies


def test_legacy_internal_provider_area_remains_denied():
    grants = dict(_policy_grants(_render_local_llm_policy()))

    assert grants["secret/data/ai/saas/*"] == ["deny"]
    assert grants["secret/metadata/ai/saas/*"] == ["deny"]
    assert [path for path in grants if path.startswith("secret/data/ai/saas/")] == [
        "secret/data/ai/saas/*"
    ]
    assert [path for path in grants if path.startswith("secret/metadata/ai/saas/")] == [
        "secret/metadata/ai/saas/*"
    ]


def test_local_llm_reads_only_the_declared_external_data_leaves():
    declarations = _policy_grants(_render_local_llm_policy())
    grants = dict(declarations)
    external_paths = [
        path for path, _capabilities in declarations if path.startswith("secrets-external/")
    ]

    assert [path for path, _capabilities in declarations] == [
        "secret/data/ai/*",
        "secret/metadata/ai/*",
        "secret/data/ai/saas/*",
        "secret/metadata/ai/saas/*",
        "secrets-external/data/ai/saas/qwencloud",
        "secrets-external/data/ai/saas/zai",
        "secret/data/ai/clickhouse",
        "secret/metadata/ai/clickhouse",
        "secret/data/ai/clickhouse-ingest",
        "secret/metadata/ai/clickhouse-ingest",
        "secret/data/ai/clickhouse-wall",
        "secret/metadata/ai/clickhouse-wall",
    ]
    assert external_paths == [
        "secrets-external/data/ai/saas/qwencloud",
        "secrets-external/data/ai/saas/zai",
    ]
    assert all(grants[path] == ["read"] for path in external_paths)


def test_qwencloud_external_secret_promotes_only_the_known_verbatim_fields():
    promoted = _read_defaults("01b-app-secrets.yml")["openbao_promoted_external_secrets"]

    # The following readiness check consumes the final promotion result for Z.ai.
    assert list(promoted)[-1] == "zai-coding"
    assert promoted["ai/saas/qwencloud"] == {
        "QWEN_API_TOKEN": "QWEN_API_TOKEN",
        "QWEN_URL_OPENAI": "QWEN_URL_OPENAI",
    }


def test_each_agent_tier_reader_policy_reads_only_its_own_leaf():
    policy_defaults = _read("roles/openbao/defaults/main/05k-agent-tier-secret-paths.yml")
    local_policy = _read("roles/openbao/templates/local-llm-policy.hcl.j2")
    reader_policy = _read("roles/openbao/templates/app-agent-tier-reader-policy.hcl.j2")
    paths = yaml.safe_load(policy_defaults)
    mount = paths["openbao_agent_tier_mount"]
    readers = paths["openbao_app_agent_tier_readers"]

    assert "openbao_agent_tier_mount" not in local_policy
    assert 'path "{{ openbao_agent_tier_mount }}/data/{{ item.tier }}"' in reader_policy
    assert 'path "{{ openbao_agent_tier_mount }}/metadata/{{ item.tier }}"' in reader_policy
    leaves = [reader["tier"] for reader in readers]
    assert len(leaves) == len(set(leaves))
    assert all("*" not in leaf and "+" not in leaf for leaf in leaves)
    assert mount == "agent-tier"
    assert mount != yaml.safe_load(_read("roles/openbao/defaults/main/01a-kv-hierarchy.yml"))["openbao_kv_mount"]


def test_ai_runner_uses_external_provider_leaves():
    runner_policy = _read("roles/openbao/templates/ai-runner-policy.hcl.j2")
    fetch_defaults = _read("playbooks/group_vars/all/openbao_secrets.yml")

    assert "{{ openbao_ai_api_key_mount }}/data/{{ openbao_ai_api_key_path_prefix }}/{{ provider }}" in runner_policy
    assert "{{ openbao_ai_api_key_mount }}/metadata/{{ openbao_ai_api_key_path_prefix }}/{{ provider }}" in runner_policy
    assert "['anthropic', 'openai']" in runner_policy
    assert "ai/saas" not in runner_policy
    assert "ai/saas" not in fetch_defaults
