"""Declared GitHub App mounts and OpenHands OIDC roles are selectable."""

import yaml

from test_openbao_select import ROLE, condition, render, resolve


INIT = ROLE / "tasks/init.yml"
INITIALIZE = ROLE / "tasks/init/02-initialize-cluster.yml"
POLICY_SYNC = ROLE / "tasks/init/02b-policy-sync.yml"
PROFILES = ROLE / "defaults/main/00-selection.yml"
APP_MOUNTS = "github_app_mounts"
OIDC_ROLES = "github_oidc_roles"
WRITE_ROLE_NAMES = [
    "openhands-write-exampleorg",
    "openhands-write-example-org",
]


def _when(task_node):
    conditions = task_node.get("when", [])
    return [conditions] if isinstance(conditions, str) else conditions


def _runs(task_node, variables):
    return all(condition(expression, variables) for expression in _when(task_node))


def _import_target(task_node):
    for key in ("ansible.builtin.import_tasks", "ansible.builtin.include_tasks"):
        target = task_node.get(key)
        if isinstance(target, dict):
            return target.get("file")
        if target:
            return target
    return None


def test_profiles_use_only_declared_mounts_and_generic_write_oidc_roles():
    profiles = yaml.safe_load(PROFILES.read_text(encoding="utf-8"))["openbao_select_profiles"]
    mounts = profiles[APP_MOUNTS]
    roles = profiles[OIDC_ROLES]

    assert mounts["candidates"] == (
        "{{ openbao_github_app_mounts | map(attribute='mount') "
        "| map('community.general.dict_kv', 'name') | list }}"
    )
    assert mounts["prefix"] == "sys/mounts/"
    assert mounts["suffixes"] == [""]
    assert mounts["capability"] == "update"
    assert roles["candidates"] == "{{ openbao_github_write_oidc_roles | default([]) }}"
    assert roles["prefix"] == "auth/{{ openbao_github_oidc_auth_path }}/role/"
    assert roles["suffixes"] == [""]
    assert roles["capability"] == "update"


def test_mount_and_oidc_selections_resolve_only_declared_candidates():
    declared_mounts = ("github-openhands", "github-org-write")
    assert resolve({APP_MOUNTS: ["github-openhands"]}, APP_MOUNTS,
                   names=declared_mounts)[1] == [{"name": "github-openhands"}]

    role_matches, role_targets = resolve(
        {OIDC_ROLES: WRITE_ROLE_NAMES}, OIDC_ROLES, names=WRITE_ROLE_NAMES
    )
    assert role_targets == [{"name": name} for name in WRITE_ROLE_NAMES]
    assert [match["names"] for match in role_matches] == [[name] for name in WRITE_ROLE_NAMES]
    no_role_matches, no_role_targets = resolve(
        {OIDC_ROLES: WRITE_ROLE_NAMES}, OIDC_ROLES, names=(), declared_names=()
    )
    assert no_role_targets == []
    assert no_role_matches[0]["names"] == []


def test_mount_selection_runs_its_listing_and_only_selected_per_app_mounts():
    selection = {APP_MOUNTS: ["github-openhands"]}
    nodes = yaml.safe_load(INIT.read_text(encoding="utf-8"))
    listing = next(node for node in nodes if node.get("name") == "List the enabled secrets engines")
    failure = next(
        node for node in nodes
        if node.get("name") == "Fail when the secrets-engine listing failed for selected mounts"
    )
    mount_phase = next(node for node in nodes if node.get("name") == "Configure the per-App GitHub mounts")
    mounts = [
        {"mount": "github-openhands", "app_id": "111"},
        {"mount": "github-org-write", "app_id": "222"},
    ]
    selected_objects = {APP_MOUNTS: [{"name": "github-openhands"}]}

    assert condition(listing["when"], {"openbao_select": selection})
    assert not condition(listing["when"], {"openbao_select": {OIDC_ROLES: [WRITE_ROLE_NAMES[0]]}})
    assert _runs(failure, {
        "openbao_select": selection,
        "openbao_bootstrap_token": "test-token",
        "openbao_mounts_raw": {"rc": 1},
    })
    assert {"openbao_github_mounts", "github"} <= set(failure["tags"])

    assert render(mount_phase["loop"], {
        "openbao_github_app_mounts": mounts,
        "openbao_selected_objects": selected_objects,
        "openbao_select": selection,
    }) == [mounts[0]]
    assert render(mount_phase["loop"], {
        "openbao_github_app_mounts": mounts,
        "openbao_select": {},
        "openbao_selected_objects": {},
    }) == mounts
    assert render(mount_phase["vars"]["_per_app_mount_paths"], {
        "openbao_selected_objects": selected_objects,
        "openbao_github_app_mounts": mounts,
        "openbao_select": selection,
    }) == ["sys/mounts/github-openhands"]
    assert render(mount_phase["vars"]["_per_app_mount_paths"], {
        "openbao_selected_objects": {},
        "openbao_github_app_mounts": mounts,
        "openbao_select": {},
    }) == ["sys/mounts/github-openhands", "sys/mounts/github-org-write"]


def test_mount_exposure_checks_filter_to_selected_apps_with_keys():
    nodes = yaml.safe_load(INIT.read_text(encoding="utf-8"))
    exposure = next(node for node in nodes if node.get("name") == "Check each GitHub App with a key in this run for exposure")
    mounts = [
        {"mount": "github-openhands", "app_id": "111"},
        {"mount": "github-org-write", "app_id": "222"},
        {"mount": "github-no-key", "app_id": "333"},
    ]
    targets = [
        {"app_id": "admin", "private_key": "admin-key"},
        {"app_id": "111", "private_key": "openhands-key"},
    ]
    selected_targets = targets + [{"app_id": "333", "private_key": ""}]

    selected = render(exposure["loop"], {
        "openbao_select": {APP_MOUNTS: ["github-openhands"]},
        "openbao_github_app_exposure_targets": selected_targets,
        "openbao_github_app_mounts": mounts,
        "openbao_selected_objects": {APP_MOUNTS: [
            {"name": "github-openhands"}, {"name": "github-no-key"},
        ]},
    })
    full = render(exposure["loop"], {
        "openbao_select": {},
        "openbao_github_app_exposure_targets": targets,
        "openbao_github_app_mounts": mounts,
        "openbao_selected_objects": {APP_MOUNTS: [
            {"name": "github-openhands"}, {"name": "github-org-write"},
        ]},
    })
    assert selected == [targets[1]]
    assert full == targets
    assert _runs(exposure, {
        "openbao_select": {APP_MOUNTS: ["github-openhands"]},
        "openbao_bounded_rbac_mode": True,
    })
    assert not _runs(exposure, {
        "openbao_select": {},
        "openbao_bounded_rbac_mode": True,
    })


def test_selected_oidc_run_imports_only_the_selection_aware_role_flow():
    nodes = yaml.safe_load(INIT.read_text(encoding="utf-8"))
    selected_import = next(
        node for node in nodes if _import_target(node) == "init/09c-github-oidc.yml"
    )
    assert _runs(selected_import, {
        "openbao_select": {OIDC_ROLES: [WRITE_ROLE_NAMES[0]]},
        "openbao_bootstrap_token": "test-token",
    })
    assert not _runs(selected_import, {
        "openbao_select": {APP_MOUNTS: ["github-openhands"]},
        "openbao_bootstrap_token": "test-token",
    })
    assert not _runs(selected_import, {
        "openbao_select": {},
        "openbao_bootstrap_token": "test-token",
    })


def test_window_mode_accepts_both_new_selection_kinds_and_keeps_policy_sync_reads():
    initialize = yaml.safe_load(INITIALIZE.read_text(encoding="utf-8"))
    guard = next(
        node for node in initialize
        if node.get("name") == "Require an explicit bounded selection for ai-admin-session"
    )
    allowed = guard["ansible.builtin.assert"]["that"][2]
    assert condition(allowed, {"openbao_select": {APP_MOUNTS: ["github-openhands"]}})
    assert condition(allowed, {"openbao_select": {OIDC_ROLES: [WRITE_ROLE_NAMES[0]]}})
    assert not condition(allowed, {"openbao_select": {"github_permission_sets": ["example"]}})
    assert "github_app_mounts" in guard["ansible.builtin.assert"]["fail_msg"]
    assert "github_oidc_roles" in guard["ansible.builtin.assert"]["fail_msg"]

    policy_sync = yaml.safe_load(POLICY_SYNC.read_text(encoding="utf-8"))
    capability_read = next(
        node for node in policy_sync
        if node.get("name") == "Ask whether this identity may sync the reconcile policy"
    )
    command = capability_read["ansible.builtin.command"]["cmd"]
    assert "sys/capabilities-self" in command
    assert "openbao_github_app_mounts" in command
