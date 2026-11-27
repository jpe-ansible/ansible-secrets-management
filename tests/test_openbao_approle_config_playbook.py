"""Contract tests for the localhost-only admin-window AppRole playbook."""

import os
from pathlib import Path
from unittest.mock import patch

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

ROOT = Path(__file__).resolve().parent.parent
PLAYBOOK = ROOT / "playbooks" / "openbao-approle-config.yml"
ROLE_TASKS = ROOT / "roles" / "openbao" / "tasks"
INIT_TASKS = ROLE_TASKS / "init"


def _walk_tasks(nodes):
    for node in nodes or []:
        if not isinstance(node, dict):
            continue
        yield node
        for key in ("block", "rescue", "always", "pre_tasks", "tasks"):
            yield from _walk_tasks(node.get(key))


def _play_tasks(play):
    for section in ("pre_tasks", "tasks"):
        yield from _walk_tasks(play.get(section, []))


def _referenced_task_file(task, path):
    for key in ("ansible.builtin.import_tasks", "ansible.builtin.include_tasks"):
        spec = task.get(key)
        if isinstance(spec, dict):
            spec = spec.get("file")
        if isinstance(spec, str) and "{{" not in spec:
            local = path.parent / spec
            # Inside a role, a nested import may be relative to the role's tasks directory.
            return local if local.is_file() else ROLE_TASKS / spec
    role = task.get("ansible.builtin.include_role")
    if isinstance(role, dict) and role.get("name") == "dryvist.secrets_management.openbao":
        return ROLE_TASKS / role["tasks_from"]
    return None


def _included_files(path, seen=None):
    seen = set() if seen is None else seen
    path = path.resolve()
    if path in seen:
        return seen
    seen.add(path)

    tasks = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    for task in _walk_tasks(tasks):
        reference = _referenced_task_file(task, path)
        if reference is None:
            continue
        included = reference.resolve()
        assert included.is_file(), f"missing task file referenced by {path}: {reference}"
        _included_files(included, seen)
    return seen


def _named_task(tasks, name):
    return next(task for task in tasks if task.get("name") == name)


def _render_expression(expression, variables=None):
    templar = Templar(loader=DataLoader())
    templar.available_variables = variables or {}
    return templar.template(trust_as_template("{{ " + expression + " }}"))


def _assert_conditions(task, variables=None):
    conditions = task["ansible.builtin.assert"]["that"]
    if isinstance(conditions, str):
        conditions = [conditions]
    # Lazy, like assert: a later condition may depend on an earlier one holding.
    return (_render_expression(condition, variables) for condition in conditions)


def test_playbook_is_localhost_only_and_imports_only_scoped_role_tasks():
    playbook = yaml.safe_load(PLAYBOOK.read_text(encoding="utf-8"))
    assert len(playbook) == 1
    play = playbook[0]
    assert play["hosts"] == "localhost"
    assert play["connection"] == "local"
    assert play["gather_facts"] is False

    included = _included_files(PLAYBOOK)
    relative = {path.relative_to(ROOT).as_posix() for path in included}
    assert "roles/openbao/tasks/init/01-preflight-and-cluster-probe.yml" in relative
    assert "roles/openbao/tasks/init/selection-preflight.yml" in relative
    assert "roles/openbao/tasks/init/select-objects.yml" in relative
    assert "roles/openbao/tasks/init/selection-capabilities.yml" in relative
    assert "roles/openbao/tasks/init/10-approles.yml" in relative
    assert "roles/openbao/tasks/init/10c-approle-ttl-bounds.yml" in relative
    assert "roles/openbao/tasks/init/07z-load-arrangement.yml" in relative
    assert "roles/openbao/tasks/init/02b-policy-sync.yml" in relative
    assert "roles/openbao/tasks/init/02c-policy-sync-preview.yml" in relative
    assert "roles/openbao/tasks/init/08-rbac-policies.yml" in relative
    assert "roles/openbao/tasks/init/08-policy-declaration-assertions.yml" in relative
    assert "roles/openbao/tasks/init/08a-roster-live-collisions.yml" in relative
    assert "roles/openbao/tasks/init/08b-rbac-policy-writes.yml" in relative

    forbidden = {
        "roles/openbao/tasks/main/install.yml",
        "roles/openbao/tasks/main/stage_plugins.yml",
        "roles/openbao/tasks/main/configure_and_bootstrap.yml",
        "roles/openbao/tasks/init/02-initialize-cluster.yml",
        "roles/openbao/tasks/init/10b-approle-secret-ids.yml",
    }
    assert relative.isdisjoint(forbidden)
    assert not any("kv-seed" in path or "kv_seed" in path for path in relative)


def test_window_mode_setup_reuses_role_proxy_detection_and_keeps_token_empty():
    playbook = yaml.safe_load(PLAYBOOK.read_text(encoding="utf-8"))
    tasks = list(_play_tasks(playbook[0]))
    role_main = yaml.safe_load((ROLE_TASKS / "main.yml").read_text(encoding="utf-8"))

    proxy_address = _named_task(
        tasks, "Resolve the admin-window proxy address from the controller environment"
    )
    proxy_mode = _named_task(tasks, "Detect whether this run uses the admin-window proxy")
    assert proxy_address["ansible.builtin.set_fact"] == role_main[0]["ansible.builtin.set_fact"]
    assert proxy_mode["ansible.builtin.set_fact"] == role_main[1]["ansible.builtin.set_fact"]

    empty_token = _named_task(tasks, "Keep the admin-window identity out of the token environment")
    assert empty_token["ansible.builtin.set_fact"]["openbao_bootstrap_token"] == ""
    lookup = _named_task(tasks, "Look up the admin-window identity's own policies")
    assert lookup["ansible.builtin.command"]["cmd"] == "bao read -format=json auth/token/lookup-self"
    assert lookup["environment"] == "{{ openbao_window_proxy_env }}"
    assert lookup["no_log"] is True


def test_selection_and_proxy_refusal_asserts_fire_for_missing_inputs():
    playbook = yaml.safe_load(PLAYBOOK.read_text(encoding="utf-8"))
    tasks = list(_play_tasks(playbook[0]))

    selection_guard = _named_task(
        tasks, "Require a nonempty AppRole, RBAC-policy or reconcile-policy selection"
    )
    assert "reconcile_policy" in selection_guard["ansible.builtin.assert"]["fail_msg"]
    assert "policies" in selection_guard["ansible.builtin.assert"]["fail_msg"]
    refused = (
        {},
        {"openbao_select": {}},
        {"openbao_select": {"approles": []}},
        {"openbao_select": {"approles": "example"}},
        {"openbao_select": {"approles": {"name": "example"}}},
        {"openbao_select": {"approles": ["example"], "reconcile_policy": []}},
        {"openbao_select": {"policies": []}},
        {"openbao_select": {"policies": "example"}},
        {"openbao_select": {"policies": {"name": "example"}}},
        {"openbao_select": {"approles": ["example"], "kv_mounts": ["example"]}},
    )
    for variables in refused:
        assert not all(_assert_conditions(selection_guard, variables)), variables
    for selection in (
        {"approles": ["example"]},
        {"policies": ["example"]},
        {"reconcile_policy": ["openbao-reconcile"]},
        {"approles": ["example"], "reconcile_policy": ["openbao-reconcile"]},
        {"approles": ["example"], "policies": ["example-policy"]},
        {"policies": ["example-policy"], "reconcile_policy": ["openbao-reconcile"]},
    ):
        assert all(_assert_conditions(selection_guard, {"openbao_select": selection})), selection

    proxy_guard = _named_task(tasks, "Require the admin-window proxy address")
    assert "BAO_AGENT_ADDR" in proxy_guard["ansible.builtin.assert"]["fail_msg"]
    for address in ("", "http://127.0.0.1:8100"):
        with patch.dict(os.environ, {"BAO_AGENT_ADDR": address}):
            assert not all(_assert_conditions(proxy_guard)), address
    with patch.dict(os.environ, {"BAO_AGENT_ADDR": "unix:///tmp/proxy.sock"}):
        assert all(_assert_conditions(proxy_guard))


def test_check_mode_reports_create_and_policy_drift_without_running_writes():
    playbook = yaml.safe_load(PLAYBOOK.read_text(encoding="utf-8"))
    tasks = list(_play_tasks(playbook[0]))
    for name in (
        "Report AppRoles that would be created in check mode",
        "Report AppRole policy attachment changes in check mode",
        "Sync selected RBAC policies through the role's policy path",
        "Compute unified diffs for selected RBAC policy changes in check mode",
        "Show selected RBAC policy diffs in check mode",
    ):
        if name.startswith("Report AppRole"):
            task = _named_task(tasks, name)
            assert task["changed_when"] is True
            assert "ansible_check_mode" in task["when"]
            assert "ansible.builtin.debug" in task
            continue
        if name == "Sync selected RBAC policies through the role's policy path":
            task = _named_task(tasks, name)
            assert (
                task["ansible.builtin.include_role"]["tasks_from"]
                == "init/08-rbac-policies.yml"
            )
            assert task["when"] == "openbao_select.policies is defined"
            continue
        task = _named_task(tasks, name)
        assert "ansible_check_mode" in task["when"]
        if name.startswith("Compute"):
            assert "ansible.utils.fact_diff" in task
        else:
            assert "ansible.builtin.debug" in task

    assert "[--check]" in PLAYBOOK.read_text(encoding="utf-8")


def test_policy_sync_reuses_declared_policy_selection_and_check_mode_path():
    policy_tasks = yaml.safe_load(
        (INIT_TASKS / "08-rbac-policies.yml").read_text(encoding="utf-8")
    )
    select = _named_task(policy_tasks, "Select RBAC policy objects")
    assert select["ansible.builtin.import_tasks"] == "init/select-objects.yml"
    assert select["vars"]["openbao_select_kind"] == "policies"
    assert select["vars"]["openbao_select_declared_candidates"] == "{{ openbao_policies }}"

    selection_tasks = yaml.safe_load(
        (INIT_TASKS / "select-objects.yml").read_text(encoding="utf-8")
    )
    unknown_guard = _named_task(
        selection_tasks, "Require every OpenBao selector to match a declared object"
    )
    assert unknown_guard["ansible.builtin.assert"]["that"] == ["item.names | length > 0"]

    policy_writes = yaml.safe_load((INIT_TASKS / "08b-rbac-policy-writes.yml").read_text(encoding="utf-8"))
    report = _named_task(policy_writes, "Report RBAC policies that would be written in check mode")
    assert "ansible_check_mode" in report["when"]
    assert "ansible.builtin.debug" in report


def test_policy_sync_inputs_are_required_and_read_through_the_proxy():
    playbook = yaml.safe_load(PLAYBOOK.read_text(encoding="utf-8"))
    tasks = list(_play_tasks(playbook[0]))

    guard = _named_task(tasks, "Require the deployment document as tofu_data")
    assert not all(_assert_conditions(guard, {}))
    assert not all(_assert_conditions(guard, {"tofu_data": {}}))
    assert all(_assert_conditions(guard, {"tofu_data": {"agents": {}}}))

    read = _named_task(tasks, "Read the env document through the window proxy")
    assert read["no_log"] is True
    assert "unix_socket" in read["ansible.builtin.uri"]
    assert "headers" not in read["ansible.builtin.uri"]
