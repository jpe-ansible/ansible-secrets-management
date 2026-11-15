"""Converge has exact writer grants for its AI seeds and app publishers."""

from pathlib import Path
from fnmatch import fnmatchcase
import re

import jinja2
import yaml
from test_openbao_global_read_all_policy import _environment as policy_environment


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "roles/openbao/templates/ansible-converge-policy.hcl.j2"
# The policy includes its publish half; read both as one rendered source.
PUBLISH = POLICY.with_name("ansible-converge-publish-policy.hcl.j2")
DEFAULTS = ROOT / "roles/openbao/defaults/main/07c-policy-composition.yml"
PATH_BLOCK = re.compile(
    r'path "([^"]+)"\s*\{\s*capabilities\s*=\s*\[([^]]+)\]\s*\}',
    re.MULTILINE,
)
AI_SEED_APPS = ("langfuse", "langflow", "phoenix", "dify")
PUBLISH_APPS = ("grafana", "status-stack")
AGENT_PATH_DEFAULTS = ROOT / "roles/openbao/defaults/main/05k-agent-tier-secret-paths.yml"
PRIVILEGED_POLICY_TEMPLATES = {
    "operator-human-policy.hcl.j2",
    "ai-admin-policy.hcl.j2",
    "openbao-reconcile-policy.hcl.j2",
}


def _grants() -> list[tuple[str, tuple[str, ...]]]:
    return [
        (path, tuple(re.findall(r'"([^"]+)"', capabilities)))
        for path, capabilities in PATH_BLOCK.findall((POLICY.read_text(encoding="utf-8") + PUBLISH.read_text(encoding="utf-8")))
    ]


def _wildcard_covers(pattern: str, target: str) -> bool:
    if pattern.endswith("*"):
        return target.startswith(pattern[:-1])
    if "+" in pattern:
        pattern_parts = pattern.split("/")
        target_parts = target.split("/")
        return len(pattern_parts) == len(target_parts) and all(
            part == "+" or part == target_part
            for part, target_part in zip(pattern_parts, target_parts)
        )
    return False


def test_ai_seed_grants_use_exact_data_and_metadata_paths() -> None:
    grants = _grants()
    for app in AI_SEED_APPS:
        data_path = f"{{{{ openbao_kv_mount }}}}/data/ai/{app}"
        metadata_path = f"{{{{ openbao_kv_mount }}}}/metadata/ai/{app}"
        assert grants.count((data_path, ("create", "update", "read"))) == 1
        assert grants.count((metadata_path, ("read",))) == 1
        assert not any(_wildcard_covers(path, data_path) for path, _ in grants)
        assert not any(_wildcard_covers(path, metadata_path) for path, _ in grants)


def test_dify_agent_app_key_leaves_are_granted_below_the_dify_record_only() -> None:
    grants = _grants()
    leaves = "{{ openbao_kv_mount }}/data/ai/dify/agent-apps/*"
    metadata = "{{ openbao_kv_mount }}/metadata/ai/dify/agent-apps/*"
    assert grants.count((leaves, ("create", "update", "read"))) == 1
    assert grants.count((metadata, ("read",))) == 1
    assert _wildcard_covers(leaves, "{{ openbao_kv_mount }}/data/ai/dify/agent-apps/action-extractor")
    assert not _wildcard_covers(leaves, "{{ openbao_kv_mount }}/data/ai/dify-other/x")


def test_dify_agent_mcp_url_leaves_are_granted_below_the_dify_record_only() -> None:
    grants = _grants()
    leaves = "{{ openbao_kv_mount }}/data/ai/dify/agent-mcp/*"
    metadata = "{{ openbao_kv_mount }}/metadata/ai/dify/agent-mcp/*"
    assert grants.count((leaves, ("create", "update", "read"))) == 1
    assert grants.count((metadata, ("read", "list"))) == 1
    assert _wildcard_covers(metadata, "{{ openbao_kv_mount }}/metadata/ai/dify/agent-mcp/")
    assert _wildcard_covers(leaves, "{{ openbao_kv_mount }}/data/ai/dify/agent-mcp/ai-news")
    assert not _wildcard_covers(leaves, "{{ openbao_kv_mount }}/data/ai/dify/agent-apps/ai-news")


def test_new_app_publisher_buckets_are_listed_once_with_exact_template_paths() -> None:
    apps = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))[
        "openbao_credential_publish_apps"
    ]
    for app in PUBLISH_APPS:
        assert apps.count(app) == 1

    policy = (POLICY.read_text(encoding="utf-8") + PUBLISH.read_text(encoding="utf-8"))
    assert "openbao_credential_publish_apps | map('regex_replace', '^', 'apps/')" in policy
    assert (
        'path "{{ openbao_kv_mount }}/data/{{ leaf }}" {\n'
        '  capabilities = ["create", "update", "read"]\n}'
    ) in policy
    assert (
        'path "{{ openbao_kv_mount }}/metadata/{{ leaf }}" {\n'
        '  capabilities = ["read"]\n}'
    ) in policy
    assert 'path "{{ openbao_kv_mount }}/data/apps/*"' not in policy
    assert 'path "{{ openbao_kv_mount }}/metadata/apps/*"' not in policy


def test_eval_namespace_grants_are_exact_specialist_platform_leaves() -> None:
    eval_grants = [(path, caps) for path, caps in _grants() if "/ai/eval/" in path]
    expected = []
    for app in ("sim", "hermes"):
        expected += [
            (f"{{{{ openbao_kv_mount }}}}/data/ai/eval/specialist-platform/{app}", ("create", "update", "read")),
            (f"{{{{ openbao_kv_mount }}}}/metadata/ai/eval/specialist-platform/{app}", ("read",)),
        ]
    assert eval_grants == expected
    assert not any("*" in path or "+" in path for path, _ in eval_grants)


def test_agent_tier_mount_has_exact_publisher_and_router_grants_only() -> None:
    defaults = yaml.safe_load(AGENT_PATH_DEFAULTS.read_text(encoding="utf-8"))
    mount = defaults["openbao_agent_tier_mount"]
    readers = defaults["openbao_app_agent_tier_readers"]
    leaves = [reader["tier"] for reader in readers]
    login_paths = [reader["login_path"] for reader in readers if reader.get("login_path")]
    assert leaves and mount != "secret"
    environment = jinja2.Environment(loader=policy_environment().loader)
    environment.filters["comment"] = lambda value: ""
    context = {
        "ansible_managed": "",
        "openbao_kv_mount": "secret",
        "openbao_agent_tier_mount": mount,
        "openbao_app_agent_tier_paths": leaves,
        "openbao_app_agent_tier_login_paths": login_paths,
        "openbao_app_agent_tier_readers": readers,
    }

    def mount_grants(name: str) -> set[tuple[str, tuple[str, ...]]]:
        source = (ROOT / "roles/openbao/templates" / name).read_text(encoding="utf-8")
        return {
            (path, tuple(re.findall(r'"([^\"]+)"', caps)))
            for path, caps in PATH_BLOCK.findall(environment.from_string(source).render(**context))
            if path.startswith(f"{mount}/")
        }

    data = {f"{mount}/data/{leaf}" for leaf in leaves}
    metadata = {(f"{mount}/metadata/{leaf}", ("read",)) for leaf in leaves}
    login_reads = {
        (f"{mount}/data/{leaf}", ("read",)) for leaf in login_paths
    } | {
        (f"{mount}/metadata/{leaf}", ("read",)) for leaf in login_paths
    }
    # Exact equality: no extra leaf, no glob, no broader capability on the mount.
    assert mount_grants("ansible-converge-policy.hcl.j2") == {
        (path, ("create", "update", "read")) for path in data
    } | metadata | login_reads
    assert mount_grants("local-llm-policy.hcl.j2") == set()

    for reader in readers:
        reader_context = context | {"item": reader}
        source = (ROOT / "roles/openbao/templates/app-agent-tier-reader-policy.hcl.j2").read_text(
            encoding="utf-8"
        )
        rendered = environment.from_string(source).render(**reader_context)
        grants = {
            (path, tuple(re.findall(r'"([^\"]+)"', caps)))
            for path, caps in PATH_BLOCK.findall(rendered)
        }
        assert grants == {
            (f"{mount}/data/{reader['tier']}", ("read",)),
            (f"{mount}/metadata/{reader['tier']}", ("read",)),
        }
        assert not any("list" in caps for _path, caps in grants)
        assert not any(
            f"{mount}/data/{other}" in path
            for path, _caps in grants
            for other in set(leaves) - {reader["tier"]}
        )

    # Every other non-admin policy must not reach the mount at all: no reference to
    # the mount variable or name, and no pattern that matches any tier endpoint.
    endpoints = data | {path for path, _ in metadata}
    role_defaults: dict = {}
    for path in sorted((ROOT / "roles/openbao/defaults/main").glob("*.yml")):
        role_defaults.update(yaml.safe_load(path.read_text(encoding="utf-8")) or {})

    def literal(match: re.Match) -> str:
        # A literal default resolves exactly; anything computed stays a wildcard.
        value = role_defaults.get(match.group(1))
        return value if isinstance(value, str) and "{{" not in value else "*"

    for template in (ROOT / "roles/openbao/templates").glob("*.hcl.j2"):
        if template.name in {
            "ansible-converge-policy.hcl.j2",
            "app-agent-tier-reader-policy.hcl.j2",
            *PRIVILEGED_POLICY_TEMPLATES,
        }:
            continue
        source = template.read_text(encoding="utf-8")
        assert "openbao_agent_tier_mount" not in source, template.name
        assert f'"{mount}/' not in source, template.name
        for path, _ in PATH_BLOCK.findall(source):
            pattern = re.sub(r"{{\s*(\w+)\s*}}", literal, path.replace("{{ openbao_kv_mount }}", "secret"))
            pattern = re.sub(r"{{[^}]+}}", "*", pattern)
            if pattern == "*":
                continue  # fully data-driven path; covered by the defaults check below
            assert not any(fnmatchcase(endpoint, pattern) for endpoint in endpoints), (
                f"{template.name} path {path} reaches the {mount} mount"
            )

    # Seed-path and policy-registry defaults may name the mount and reader
    # policies. Actual grants remain limited to the templates checked above.
    for template in (ROOT / "roles/openbao/templates").glob("*.hcl.j2"):
        if template.name not in {
            "ansible-converge-policy.hcl.j2",
            "app-agent-tier-reader-policy.hcl.j2",
            "openbao-reconcile-policy.hcl.j2",
        }:
            assert "openbao_agent_tier_mount" not in template.read_text(encoding="utf-8"), template.name

    # Policies that loop over the declared KV mounts use whole-path expressions,
    # which the static check above skips; the agent-tier mount must stay out of that list.
    # Restricted mounts join the zone list only from the run environment; the
    # 03b assert refuses the agent-tier mount among them at run time.
    kv_mounts = {
        re.sub(r"{{\s*(\w+)\s*}}", literal, entry["path"])
        for entry in role_defaults["openbao_kv_zone_mounts"]
    }
    assert "*" not in kv_mounts and mount not in kv_mounts, kv_mounts
