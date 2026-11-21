"""Declared GitHub App mounts and workload OIDC roles are selectable."""

import pytest
import yaml

from test_openbao_select import ROLE, condition, render, resolve, task


INIT = ROLE / "tasks/init.yml"
INITIALIZE = ROLE / "tasks/init/02-initialize-cluster.yml"
POLICY_SYNC = ROLE / "tasks/init/02b-policy-sync.yml"
PROFILES = ROLE / "defaults/main/00-selection.yml"
OIDC_TASKS = ROLE / "tasks/init/09c-github-oidc.yml"
APP_MOUNTS = "github_app_mounts"
OIDC_ROLES = "github_oidc_roles"
WRITE_ROLE_NAMES = [
    "openhands-write-exampleorg",
    "openhands-write-example-org",
]
CI_ROLES = [
    ("ci-evals", "openbao_ci_evals_policy_name", "05f-ci-evals.yml"),
    ("ci-ai-review", "openbao_ci_ai_review_policy_name", "05f-ci-ai-review.yml"),
    ("pr-reconcile-sweep", "openbao_github_pr_reconcile_policy_name", "05f-pr-reconcile.yml"),
    ("pr-reconcile", "openbao_github_pr_reconcile_caller_policy_name", "05f-pr-reconcile.yml"),
]


def _oidc_variables():
    variables = {
        "openbao_github_write_oidc_roles": [
            {"name": name, "org": "exampleorg", "set": {"tier": "openhands-write"}}
            for name in WRITE_ROLE_NAMES
        ],
        "openbao_ci_ai_review_enterprise_id": "12345",
        "openbao_github_pr_reconcile_enabled": True,
        "openbao_github_pr_reconcile_caller_enabled": True,
        "openbao_bootstrap_token": "test-token",
    }
    for _, policy_name, filename in CI_ROLES:
        defaults = yaml.safe_load((ROLE / "defaults/main" / filename).read_text(encoding="utf-8"))
        variables[policy_name] = defaults[policy_name]
    return variables


def _oidc_candidates(variables):
    profiles = yaml.safe_load(PROFILES.read_text(encoding="utf-8"))["openbao_select_profiles"]
    return render(profiles[OIDC_ROLES]["candidates"], variables)


def _with_oidc_selection(variables, names):
    selection = {OIDC_ROLES: names} if names else {}
    _, targets = resolve(selection, OIDC_ROLES,
                         names=[candidate["name"] for candidate in _oidc_candidates(variables)])
    return {
        **variables,
        "openbao_select": selection,
        "openbao_selected_objects": {OIDC_ROLES: targets},
        "openbao_github_oidc_role_targets": targets,
    }


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


def test_profiles_use_declared_mounts_and_oidc_role_paths():
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
    assert roles["prefix"] == "auth/{{ openbao_github_oidc_auth_path }}/role/"
    assert roles["suffixes"] == [""]
    assert roles["capability"] == "update"


@pytest.mark.parametrize("enterprise_id", ["", "12345"])
@pytest.mark.parametrize("enabled", [False, True, "false", "true"])
@pytest.mark.parametrize("name_suffix", ["", "-custom"])
def test_oidc_candidates_preserve_write_roles_and_gate_named_ci_roles(
    enterprise_id, enabled, name_suffix
):
    variables = _oidc_variables()
    variables["openbao_ci_ai_review_enterprise_id"] = enterprise_id
    variables["openbao_github_pr_reconcile_enabled"] = enabled
    for _, policy_name, _ in CI_ROLES:
        variables[policy_name] += name_suffix

    candidates = _oidc_candidates(variables)
    expected = list(variables["openbao_github_write_oidc_roles"])
    expected.append({"name": variables["openbao_ci_evals_policy_name"]})
    if enterprise_id:
        expected.append({"name": variables["openbao_ci_ai_review_policy_name"]})
    if enabled in (True, "true"):
        expected.append({"name": variables["openbao_github_pr_reconcile_policy_name"]})
    expected.append({"name": variables["openbao_github_pr_reconcile_caller_policy_name"]})
    assert sorted(candidates, key=lambda item: item["name"]) == sorted(
        expected, key=lambda item: item["name"]
    )

    del variables["openbao_github_write_oidc_roles"]
    assert _oidc_candidates(variables) == [
        candidate for candidate in candidates if candidate["name"] not in WRITE_ROLE_NAMES
    ]


@pytest.mark.parametrize(("role_name", "policy_name", "filename"), CI_ROLES)
def test_ci_oidc_names_resolve_through_the_real_selector(role_name, policy_name, filename):
    variables = _oidc_variables()
    assert variables[policy_name] == role_name
    name = variables[policy_name]
    selected = _with_oidc_selection(variables, [name])
    assert selected["openbao_selected_objects"][OIDC_ROLES] == [{"name": name}]


@pytest.mark.parametrize("name", ["ci-ai-review", "pr-reconcile-sweep", "unknown-role"])
def test_unavailable_ci_oidc_roles_fail_the_selector_match_guard(name):
    variables = _oidc_variables()
    variables["openbao_ci_ai_review_enterprise_id"] = ""
    variables["openbao_github_pr_reconcile_enabled"] = False
    matches, targets = resolve(
        {OIDC_ROLES: [name]}, OIDC_ROLES,
        names=[candidate["name"] for candidate in _oidc_candidates(variables)],
    )
    guard = task("Require every OpenBao selector to match a declared object")["ansible.builtin.assert"]
    assert targets == []
    assert not condition(guard["that"][0], {"item": matches[0]})
    assert name in render(guard["fail_msg"], {"item": matches[0], "openbao_select_kind": OIDC_ROLES})


@pytest.mark.parametrize("action", ["Read", "Reconcile"])
@pytest.mark.parametrize(("role_name", "policy_name", "filename"), CI_ROLES)
def test_ci_oidc_tasks_admit_only_their_resolved_selection_and_keep_token_gates(
    action, role_name, policy_name, filename
):
    node = task(f"{action} the {role_name} OIDC role", OIDC_TASKS)
    variables = _oidc_variables()
    own_name = variables[policy_name]
    assert _runs(node, _with_oidc_selection(variables, [own_name]))
    for other_name in WRITE_ROLE_NAMES + [
        variables[other_policy] for _, other_policy, _ in CI_ROLES if other_policy != policy_name
    ]:
        assert not _runs(node, _with_oidc_selection(variables, [other_name]))
    assert not _runs(node, {
        **variables,
        "openbao_select": {APP_MOUNTS: ["github-openhands"]},
        "openbao_selected_objects": {},
        "openbao_github_oidc_role_targets": [],
    })
    assert _runs(node, _with_oidc_selection(variables, []))
    del variables["openbao_bootstrap_token"]
    assert not _runs(node, _with_oidc_selection(variables, [own_name]))
    assert not _runs(node, _with_oidc_selection(variables, []))


@pytest.mark.parametrize("action", ["Read", "Reconcile"])
def test_ci_oidc_full_runs_keep_input_gates_and_pr_cleanup_read(action):
    variables = _oidc_variables()
    variables["openbao_ci_ai_review_enterprise_id"] = ""
    variables["openbao_github_pr_reconcile_enabled"] = "false"
    full_run = _with_oidc_selection(variables, [])
    assert not _runs(task(f"{action} the ci-ai-review OIDC role", OIDC_TASKS), full_run)
    assert _runs(task(f"{action} the ci-evals OIDC role", OIDC_TASKS), full_run)
    assert _runs(task(f"{action} the pr-reconcile-sweep OIDC role", OIDC_TASKS), full_run) == (
        action == "Read"
    )


def test_skip_and_remove_oidc_tasks_remain_full_only():
    skip = task("Skip the ci-ai-review OIDC role without an enterprise ID", OIDC_TASKS)
    remove = task("Remove the pr-reconcile-sweep OIDC role while its inputs are unset", OIDC_TASKS)
    variables = _oidc_variables()
    variables.update({
        "openbao_ci_ai_review_enterprise_id": "",
        "openbao_github_pr_reconcile_enabled": False,
        "openbao_github_oidc_pr_reconcile_role_current": {"rc": 0},
    })
    full_run = _with_oidc_selection(variables, [])
    assert _runs(skip, full_run)
    assert _runs(remove, full_run)
    for name in [variables["openbao_ci_evals_policy_name"], *WRITE_ROLE_NAMES]:
        selected = _with_oidc_selection(variables, [name])
        assert not _runs(skip, selected)
        assert not _runs(remove, selected)
    assert not _runs(skip, {**full_run, "openbao_ci_ai_review_enterprise_id": "12345"})
    assert not _runs(remove, {**full_run, "openbao_github_pr_reconcile_enabled": True})
    assert not _runs(remove, {
        **full_run, "openbao_github_oidc_pr_reconcile_role_current": {"rc": 1},
    })
    del full_run["openbao_bootstrap_token"]
    assert not _runs(remove, full_run)


@pytest.mark.parametrize("action", ["Read", "Reconcile"])
def test_ci_evals_selection_does_not_enter_the_generic_write_role_loop(action):
    node = task(f"{action} each GitHub write OIDC role", OIDC_TASKS)
    variables = _oidc_variables()
    selected = _with_oidc_selection(variables, [variables["openbao_ci_evals_policy_name"]])
    loop_items = render(node["loop"], selected)
    assert loop_items == variables["openbao_github_write_oidc_roles"]
    for index, item in enumerate(loop_items):
        assert not _runs(node, {**selected, "item": item})
        assert _runs(node, {
            **_with_oidc_selection(variables, [item["name"]]),
            "item": item,
            "openbao_github_write_role_index": index,
            "openbao_github_oidc_write_roles_current": {"results": [{"rc": 1}] * len(loop_items)},
        })


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
