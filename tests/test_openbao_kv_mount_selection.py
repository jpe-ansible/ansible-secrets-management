"""Declared KV mounts can be selected and provisioned independently."""

import json
import re

import yaml
from ansible.plugins.loader import init_plugin_loader
from ansible.utils.collection_loader import AnsibleCollectionConfig

from openbao_reconcile_bounds_helpers import (
    TEMPLATES,
    _capabilities,
    _render,
    _render_value,
    _stanzas,
    rendered_defaults,
)
from test_openbao_select import ROLE, ROOT, condition, render, resolve, task


KIND = "kv_mounts"
DOMAINS_FILE = ROOT / "playbooks/group_vars/all/openbao_secrets.yml"
SELECTION = {KIND: ["ext-notify"]}
EXPECTED_MOUNTS = [
    "secret", "secrets-external", "config", "ext-notify",
    "int", "ext-saas", "ext-ai", "ext-critical", "admin", "state",
]
INIT = ROLE / "tasks/init.yml"
INIT_TASKS = ROLE / "tasks/init"
SELECTION_DEFAULTS = ROLE / "defaults/main/00-selection.yml"
HIERARCHY_DEFAULTS = ROLE / "defaults/main/01a-kv-hierarchy.yml"
MOUNT_TASKS = INIT_TASKS / "03b-kv-mounts.yml"
NTFY_POLICY = TEMPLATES / "ntfy-policy.hcl.j2"
SECRET_AGE_POLICY = TEMPLATES / "secret-age-audit-policy.hcl.j2"
AI_ADMIN_POLICY = TEMPLATES / "ai-admin-policy.hcl.j2"


def _import_target(node):
    for key in ("ansible.builtin.import_tasks", "ansible.builtin.include_tasks"):
        if key not in node:
            continue
        target = node[key]
        return target.get("file") if isinstance(target, dict) else target
    return None


def _flatten(tasks):
    for item in tasks:
        yield item
        for key in ("block", "rescue", "always"):
            yield from _flatten(item.get(key, []))


def _mount_names():
    # The candidates expression uses a community.general filter.
    if not AnsibleCollectionConfig.collection_finder:
        init_plugin_loader()
    profile = yaml.safe_load(SELECTION_DEFAULTS.read_text(encoding="utf-8"))[
        "openbao_select_profiles"][KIND]
    mount_defaults = yaml.safe_load(HIERARCHY_DEFAULTS.read_text(encoding="utf-8"))
    variables = {
        "openbao_kv_mount": "secret",
        "openbao_config_mount": "config",
        "openbao_config_mount_max_versions": 30,
    }
    # openbao_kv_mounts adds restricted mounts from the run environment, unset here.
    raw_mounts = mount_defaults["openbao_kv_zone_mounts"]
    mounts = []
    for entry in raw_mounts:
        mount = dict(entry)
        mount["path"] = render(mount["path"], variables)
        if "max_versions" in mount:
            mount["max_versions"] = render(mount["max_versions"], variables)
        mounts.append(mount)
    return profile, raw_mounts, mounts, render(
        profile["candidates"], {"openbao_kv_mounts": mounts}
    )


def _runs(task_node, variables):
    conditions = task_node.get("when", [])
    if isinstance(conditions, str):
        conditions = [conditions]
    return all(condition(expression, variables) for expression in conditions)


def _selection_gate(task_node, selection):
    conditions = task_node.get("when", [])
    if isinstance(conditions, str):
        conditions = [conditions]
    expression = next(value for value in conditions if "openbao_select" in value)
    return condition(expression, {"openbao_select": selection})


def test_kv_mount_profile_declares_candidates_and_exact_mount_capability():
    profile, raw_mounts, mounts, candidates = _mount_names()
    assert [item["name"] for item in candidates] == EXPECTED_MOUNTS
    assert {"path": "ext-notify"} in raw_mounts
    assert "max_versions" not in next(
        mount for mount in mounts if mount["path"] == "ext-notify"
    )
    assert profile["candidates"] == (
        "{{ openbao_kv_mounts | map(attribute='path') "
        "| map('community.general.dict_kv', 'name') | list }}"
    )
    assert profile["prefix"] == "sys/mounts/"
    assert profile["suffixes"] == [""]
    assert profile["capability"] == "update"


def test_selection_resolves_only_declared_mounts_and_refuses_unknown_names():
    selected = resolve(SELECTION, KIND, names=EXPECTED_MOUNTS)[1]
    assert selected == [{"name": "ext-notify"}]

    matches, _ = resolve({KIND: ["ext-undeclared"]}, KIND, names=EXPECTED_MOUNTS)
    assert matches[0]["names"] == []
    check = task("Require every OpenBao selector to match a declared object")[
        "ansible.builtin.assert"
    ]
    assert not condition(check["that"][0], {"item": matches[0]})
    failure = render(check["fail_msg"], {
        "item": matches[0], "openbao_select_kind": KIND,
    })
    assert "ext-undeclared" in failure and "matched no declared objects" in failure


def test_window_mode_accepts_kv_mounts_and_still_refuses_github_permission_sets():
    initialize = yaml.safe_load(
        (INIT_TASKS / "02-initialize-cluster.yml").read_text(encoding="utf-8")
    )
    guard = next(
        item for item in initialize
        if item.get("name") == "Require an explicit bounded selection for ai-admin-session"
    )
    allowed = guard["ansible.builtin.assert"]["that"][2]
    assert condition(allowed, {"openbao_select": SELECTION})
    assert not condition(allowed, {
        "openbao_select": {"github_permission_sets": ["example-permission-set"]}
    })
    assert "kv_mounts" in guard["ansible.builtin.assert"]["fail_msg"]


def test_enable_task_scopes_selection_and_full_run_to_missing_mounts():
    enable = task("Enable the declared KV v2 mounts (add-if-missing)", MOUNT_TASKS)
    assert enable["loop"] == "{{ openbao_kv_mounts }}"

    def should_run(mount, selected, present):
        variables = {
            "item": {"path": mount},
            "openbao_kv_mount_targets": [{"name": name} for name in selected],
            "openbao_mounts_raw": {
                "stdout": json.dumps({f"{name}/": {} for name in present}),
            },
        }
        return _runs(enable, variables)

    assert should_run("ext-notify", ["ext-notify"], [])
    assert not should_run("secret", ["ext-notify"], [])

    for mount in EXPECTED_MOUNTS:
        assert should_run(mount, EXPECTED_MOUNTS, ["config"]) is (mount != "config")


def test_check_mode_reports_only_selected_mounts_absent_from_listing():
    report = task("Report KV mounts that would be enabled in check mode", MOUNT_TASKS)
    assert report["ansible.builtin.debug"]["msg"] == (
        "KV v2 mount {{ item.path }} would be enabled."
    )
    variables = {
        "ansible_check_mode": True,
        "item": {"path": "ext-notify"},
        "openbao_kv_mount_targets": [{"name": "ext-notify"}],
        "openbao_mounts_raw": {"stdout": "{}"},
    }
    assert _runs(report, variables)
    assert not _runs(report, {**variables, "item": {"path": "secret"}})
    assert not _runs(report, {
        **variables,
        "openbao_mounts_raw": {"stdout": '{"ext-notify/": {}}'},
    })


def test_listing_and_kv_mount_import_run_for_selection_but_seed_phase_does_not():
    nodes = yaml.safe_load(INIT.read_text(encoding="utf-8"))
    listing = next(
        item for item in nodes
        if item.get("name") == "List the enabled secrets engines"
    )
    seed_phase = next(
        item for item in nodes
        if _import_target(item) == "init/03-kv-mounts-and-seed-secrets.yml"
    )
    mount_phase = next(
        item for item in nodes if _import_target(item) == "init/03b-kv-mounts.yml"
    )
    variables = {
        "openbao_select": SELECTION,
        "openbao_bootstrap_token": "test-token",
        "openbao_mounts_raw": {"rc": 0},
    }

    assert condition(listing["when"], {"openbao_select": SELECTION})
    assert not _runs(seed_phase, variables)
    assert _runs(mount_phase, variables)
    assert nodes.index(listing) < nodes.index(seed_phase) < nodes.index(mount_phase)
    assert set(mount_phase["tags"]) <= set(listing["tags"])

    seed_tasks = yaml.safe_load(
        (INIT_TASKS / "03-kv-mounts-and-seed-secrets.yml").read_text(encoding="utf-8")
    )
    assert any(
        item.get("name") == "Seed the external Context7 key if absent"
        for item in _flatten(seed_tasks)
    )
    mount_tasks = yaml.safe_load(MOUNT_TASKS.read_text(encoding="utf-8"))
    assert not any("seed" in item.get("name", "").lower() for item in mount_tasks)


def test_failed_listing_fails_a_selected_mount_run():
    nodes = yaml.safe_load(INIT.read_text(encoding="utf-8"))
    failure = next(
        item for item in nodes
        if item.get("name") == "Fail when the secrets-engine listing failed for selected mounts"
    )
    variables = {
        "openbao_select": SELECTION,
        "openbao_bootstrap_token": "test-token",
        "openbao_mounts_raw": {"rc": 1, "stderr": "permission denied"},
    }
    assert _runs(failure, variables)
    assert "permission denied" in render(failure["ansible.builtin.fail"]["msg"], {
        **variables, "openbao_api_addr": "https://bao.example.test",
    })


def test_other_mount_listing_readers_remain_skipped_for_kv_mount_selection():
    nodes = yaml.safe_load(INIT.read_text(encoding="utf-8"))
    reader_imports = {
        "init/04-aws-engine.yml",
        "init/04b-azure-engine.yml",
        "init/04c-transit-engine.yml",
        "init/05-github-engine.yml",
        "init/05b-github-app-mount.yml",
        "init/06-oauth-engine.yml",
        "init/07b-etcd-pki-engine.yml",
    }
    for target in reader_imports:
        node = next(item for item in nodes if _import_target(item) == target)
        assert not _selection_gate(node, SELECTION), target

    ssh_enable = task("Enable the SSH secrets engine", INIT_TASKS / "07-ssh-ca-engine.yml")
    assert not _selection_gate(ssh_enable, SELECTION)

    approle_names = task(
        "Keep the selected AppRole config objects",
        INIT_TASKS / "10-approles.yml",
    )["ansible.builtin.set_fact"]["openbao_approle_config_targets"]
    assert resolve(SELECTION, "approles", names=("apps",))[1] == []
    assert "openbao_object_targets" in approle_names


def test_ntfy_policy_reads_the_new_webhook_leaf_and_keeps_transitional_leaves():
    rendered = _render(NTFY_POLICY, {"ansible_managed": "fixture"})
    stanzas = dict(_stanzas(rendered))
    assert stanzas["ext-notify/data/slack/webhooks/rw"].strip() == (
        'capabilities = ["read"]'
    )
    assert _capabilities(stanzas["ext-notify/metadata/slack/webhooks/rw"]) == [
        "read", "list",
    ]
    assert set(stanzas) == {
        "secrets-external/data/platform/slack-webhooks",
        "secrets-external/data/slack/webhooks/rw",
        "ext-notify/data/slack/webhooks/rw",
        "secrets-external/metadata/platform/slack-webhooks",
        "secrets-external/metadata/slack/webhooks/rw",
        "ext-notify/metadata/slack/webhooks/rw",
    }
    assert "ext-notify" in rendered and "transitional" in rendered
    assert all(set(_capabilities(body)) <= {"read", "list"} for body in stanzas.values())


def test_ntfy_domain_reads_the_ext_notify_leaf_last_with_a_policy_grant():
    domains = yaml.safe_load(DOMAINS_FILE.read_text(encoding="utf-8"))["openbao_secrets_domains"]
    paths = next(domain["paths"] for domain in domains if domain["name"] == "ntfy")
    stanzas = dict(_stanzas(_render(NTFY_POLICY, {"ansible_managed": "fixture"})))
    # Paths merge in order and later paths win, so the ext-notify leaf must come last.
    assert paths[-1] == {"mount": "ext-notify", "path": "slack/webhooks/rw", "optional": True}
    for entry in paths:
        assert "read" in _capabilities(stanzas[f"{entry['mount']}/data/{entry['path']}"])


def test_secret_age_audit_grants_metadata_reads_for_every_age_audited_kv_mount(rendered_defaults):
    values, _, _ = rendered_defaults
    mounts = _render_value(values, values["openbao_kv_mounts"])
    mount_names = [
        mount["path"] for mount in mounts
        if mount.get("age_audit", True) is not False
    ]
    assert not {"config", "admin", "state"} & set(mount_names)
    rendered = _render(SECRET_AGE_POLICY, values)
    stanzas = list(_stanzas(rendered))
    paths = [path for path, _body in stanzas]
    expected_mount_paths = [f"{mount}/metadata/*" for mount in mount_names]
    expected_mount_paths += [f"{mount}/metadata" for mount in mount_names]

    assert paths[:len(expected_mount_paths)] == expected_mount_paths
    assert "ext-notify/metadata/*" in paths
    assert "ext-notify/metadata" in paths
    assert all("/data/" not in path for path in paths)
    for path, body in stanzas[:len(mount_names)]:
        assert _capabilities(body) == ["read", "list"], path
    for path, body in stanzas[len(mount_names):len(expected_mount_paths)]:
        assert _capabilities(body) == ["list"], path
    approle_stanzas = stanzas[len(expected_mount_paths):]
    assert [path for path, _body in approle_stanzas] == [
        "auth/approle/role",
        "auth/approle/role/+/secret-id",
        "auth/approle/role/+/secret-id-accessor/lookup",
    ]
    assert [_capabilities(body) for _path, body in approle_stanzas] == [
        ["list"], ["list"], ["update"],
    ]


def test_ai_admin_adds_one_full_stanza_per_declared_kv_mount(rendered_defaults, monkeypatch):
    # Restricted mounts from the caller's environment would extend the list.
    monkeypatch.delenv("OPENBAO_KV_RESTRICTED_MOUNTS", raising=False)
    values, _, _ = rendered_defaults
    mounts = [mount["path"] for mount in _render_value(values, values["openbao_kv_mounts"])]
    baseline_values = dict(values, openbao_kv_mounts=[])
    current = _render(AI_ADMIN_POLICY, values)
    baseline = _render(AI_ADMIN_POLICY, baseline_values)
    stanza = re.compile(
        r'(?ms)^path "(' + "|".join(map(re.escape, mounts)) + r')/\*" \{\n.*?^\}\n?'
    )
    matches = list(stanza.finditer(current))

    assert [match.group(1) for match in matches] == mounts == EXPECTED_MOUNTS
    assert stanza.sub("", current) == baseline
    for match in matches:
        assert _capabilities(match.group(0)) == [
            "create", "read", "update", "delete", "list", "patch",
        ]
