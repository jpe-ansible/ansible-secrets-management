"""SSH role selection writes only the requested roles and never configures the CA."""

import yaml

from test_openbao_select import ROLE, condition, render, resolve, task


KIND = "ssh_roles"
SELECTION = {KIND: ["keygen"]}
INITIALIZE = ROLE / "tasks/init/02-initialize-cluster.yml"
SSH_TASKS = ROLE / "tasks/init/07-ssh-ca-engine.yml"
PROFILES = ROLE / "defaults/main/00-selection.yml"


def _when(task_node):
    conditions = task_node.get("when", [])
    return [conditions] if isinstance(conditions, str) else conditions


def _runs(task_node, variables):
    return all(condition(expression, variables) for expression in _when(task_node))


def test_ssh_role_profile_uses_declared_roles_and_exact_role_write_path():
    profile = yaml.safe_load(PROFILES.read_text(encoding="utf-8"))[
        "openbao_select_profiles"][KIND]
    assert profile["candidates"] == "{{ openbao_ssh_roles }}"
    assert profile["prefix"] == "{{ openbao_ssh_mount }}/roles/"
    assert profile["suffixes"] == [""]
    assert profile["capability"] == "update"


def test_admin_session_accepts_ssh_roles_and_rejects_unknown_role_names():
    initialize = yaml.safe_load(INITIALIZE.read_text(encoding="utf-8"))
    guard = next(
        node for node in initialize
        if node.get("name") == "Require an explicit bounded selection for ai-admin-session"
    )
    allowed = guard["ansible.builtin.assert"]["that"][2]
    assert condition(allowed, {"openbao_select": SELECTION})
    assert not condition(allowed, {"openbao_select": {"unsupported": ["keygen"]}})
    assert KIND in guard["ansible.builtin.assert"]["fail_msg"]

    matches, targets = resolve(SELECTION, KIND, names=("keygen", "test-sign-role"))
    assert [item["name"] for item in targets] == ["keygen"]
    assert matches == [{"selector": "keygen", "names": ["keygen"]}]

    unmatched, _ = resolve({KIND: ["missing-role"]}, KIND, names=("keygen",))
    require_match = task("Require every OpenBao selector to match a declared object")[
        "ansible.builtin.assert"
    ]
    assert not condition(require_match["that"][0], {"item": unmatched[0]})
    message = render(require_match["fail_msg"], {
        "item": unmatched[0], "openbao_select_kind": KIND,
    })
    assert "missing-role" in message and "matched no declared objects" in message


def test_ssh_roles_selection_skips_ca_configuration_and_scopes_role_loops():
    selection_variables = {
        "openbao_select": SELECTION,
        "openbao_bounded_rbac_mode": False,
        "openbao_bootstrap_token": "test-token",
        "openbao_ssh_engine_enabled": True,
        "openbao_ssh_mount": "ssh-client-ca",
        "openbao_mounts_raw": {"stdout": "{}"},
        "openbao_ssh_ca_check": {"rc": 1},
    }
    ca_task_names = (
        "Enable the SSH secrets engine",
        "Check whether the SSH CA is already configured",
        "Generate the SSH CA signing key (first configuration only, never exported)",
        "Read the SSH CA public key",
        "Show the SSH CA public key fingerprint (pin this in ssh_ca_trust)",
        "Report the SSH CA fingerprint",
    )
    for name in ca_task_names:
        ca_task = task(name, SSH_TASKS)
        conditions = _when(ca_task)
        selection_gates = [gate for gate in conditions if "openbao_select" in gate]
        assert len(selection_gates) == 1
        assert not condition(selection_gates[0], selection_variables)
        assert all(
            condition(gate, selection_variables)
            for gate in conditions if gate not in selection_gates
        )
        assert not _runs(ca_task, selection_variables)

    selected = [{"name": "keygen"}]
    checks = [{"rc": 0, "stdout": '{"data":{"max_ttl":60}}'}]
    read_roles = task("Check which SSH roles already exist", SSH_TASKS)
    reconcile = task("Reconcile the SSH roles", SSH_TASKS)
    assert render(read_roles["loop"], {"openbao_selected_objects": {KIND: selected}}) == selected
    assert render(reconcile["loop"], {
        "openbao_selected_objects": {KIND: selected},
        "openbao_ssh_role_checks": {"results": checks},
    }) == [[selected[0], checks[0]]]
    assert _runs(read_roles, {
        **selection_variables,
        "openbao_bootstrap_token": "test-token",
        "openbao_ssh_engine_enabled": True,
        "openbao_selected_objects": {KIND: selected},
    })


def test_check_mode_reports_selected_ssh_role_writes_and_suppresses_command():
    report = task("Report SSH roles that would be written in check mode", SSH_TASKS)
    assert render(report["ansible.builtin.debug"]["msg"], {
        "openbao_ssh_role_changes": [{"name": "keygen"}],
    }) == "Would write SSH roles: keygen"
    assert render(report["ansible.builtin.debug"]["msg"], {
        "openbao_ssh_role_changes": [],
    }) == "No SSH role writes are needed."

    write = task("Reconcile the SSH roles", SSH_TASKS)
    check_mode_gate = next(gate for gate in write["when"] if "ansible_check_mode" in gate)
    report_gate = next(gate for gate in report["when"] if "ansible_check_mode" in gate)
    assert not condition(check_mode_gate, {"ansible_check_mode": True})
    assert condition(check_mode_gate, {"ansible_check_mode": False})
    assert condition(report_gate, {"ansible_check_mode": True})
    assert not condition(report_gate, {"ansible_check_mode": False})


def test_unselected_full_run_still_reconciles_all_declared_ssh_roles():
    selection_gate = (
        "openbao_select | default({}) | length == 0 "
        "or 'ssh_roles' in (openbao_select | default({}))"
    )
    for name in (
        "Select SSH role objects",
        "Check which SSH roles already exist",
        "Reconcile the SSH roles",
    ):
        node = task(name, SSH_TASKS)
        assert any(selection_gate in " ".join(gate.split()) for gate in _when(node))
        assert condition(selection_gate, {"openbao_select": {}})
        assert condition(selection_gate, {"openbao_select": SELECTION})
        assert not condition(selection_gate, {"openbao_select": {"policies": ["apps"]}})


def test_role_change_check_uses_declared_max_ttl_for_host_roles():
    import json

    resolve_task = task("Resolve SSH roles that are missing or changed",
                        ROLE / "tasks/init/07-ssh-ca-engine.yml")
    expression = resolve_task["ansible.builtin.set_fact"]["openbao_ssh_role_changes"]
    host = {"name": "host-cert", "cert_type": "host", "ttl": 3600, "max_ttl": 7776000}
    user = {"name": "keygen", "ttl": 60}

    def changes(item, live_max_ttl):
        stdout = json.dumps({"data": {"max_ttl": live_max_ttl}})
        checks = {"results": [{"item": item, "rc": 0, "stdout": stdout}]}
        return render(expression, {"openbao_ssh_role_checks": checks})

    assert changes(host, 7776000) == []
    assert changes(host, 3600) == [host]
    assert changes(user, 60) == []
    assert changes(user, 120) == [user]
