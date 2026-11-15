"""The arrangement loader runs before RBAC and exposes one exact read leaf."""

from pathlib import Path

import yaml

from openbao_reconcile_bounds_helpers import (
    RECONCILE,
    _capabilities,
    _include_details,
    _render,
    _stanzas,
    _task_file,
    rendered_defaults,
)

ROOT = Path(__file__).resolve().parents[1]
LOADER = ROOT / "roles/openbao/tasks/init/07z-load-arrangement.yml"
INIT = ROOT / "roles/openbao/tasks/init.yml"


def _when(task):
    return task.get("when", [])


def _debug_message(task):
    debug = task.get("ansible.builtin.debug", {})
    return str(debug.get("msg", ""))


def test_arrangement_loader_reads_declared_leaf_safely():
    tasks = _task_file(LOADER)
    requests = [task for task in tasks if "ansible.builtin.uri" in task]

    assert len(requests) == 1
    task = requests[0]
    uri = task["ansible.builtin.uri"]
    assert uri["method"] == "GET"
    assert uri["url"] == (
        "{{ openbao_cli_addr }}/v1/{{ openbao_arrangement_kv_mount }}"
        "/data/{{ openbao_arrangement_kv_path }}"
    )
    assert uri["status_code"] == [200, 403, 404]
    assert uri["headers"]["X-Vault-Token"] == "{{ openbao_bootstrap_token }}"
    assert task["delegate_to"] == "{{ openbao_cli_host }}"
    assert task["become"] == "{{ openbao_cli_become }}"
    assert task["vars"]["ansible_become"] == "{{ openbao_cli_become }}"
    assert task["changed_when"] is False
    assert task["check_mode"] is False
    assert task["no_log"] is True
    failed_when = str(task["failed_when"])
    assert "status is not defined" in failed_when
    assert "status | int" in failed_when
    assert "< 0" in failed_when
    assert "openbao_bootstrap_token is defined" in str(_when(task))


def test_arrangement_loader_is_imported_before_rbac_for_selected_runs():
    tasks = yaml.safe_load(INIT.read_text(encoding="utf-8"))
    imports = [
        (index, task, _include_details(task))
        for index, task in enumerate(tasks)
        if _include_details(task) is not None
    ]
    loader_index, loader, loader_details = next(
        row for row in imports
        if row[2][1]["file"] == "init/07z-load-arrangement.yml"
    )
    rbac_index = next(
        index for index, task in enumerate(tasks)
        if task.get("name") == "Render and reconcile the RBAC policies"
    )

    assert loader_index < rbac_index
    assert "openbao_rbac" in loader.get("tags", [])
    assert loader_details[0] == "import_tasks"
    assert "when" not in loader


def test_arrangement_loader_resets_and_warns_on_unusable_documents():
    tasks = _task_file(LOADER)
    source = LOADER.read_text(encoding="utf-8")
    facts = [task for task in tasks if "ansible.builtin.set_fact" in task]
    parsed_facts = [
        task["ansible.builtin.set_fact"]
        for task in facts
        if "document" in str(task["ansible.builtin.set_fact"])
        and "from_json" in str(task["ansible.builtin.set_fact"])
    ]
    fallback = next(
        task for task in facts
        if task.get("name") == "Keep the arrangement empty when the response is unusable"
    )
    warnings = [
        task for task in tasks
        if _debug_message(task).startswith("WARNING:")
    ]

    assert parsed_facts
    assert "is mapping" in source
    assert fallback["ansible.builtin.set_fact"]["openbao_arrangement"] == {}
    assert len(warnings) == 1
    warning = warnings[0]
    assert warning.get("no_log") is False
    warning_text = _debug_message(warning).lower()
    assert "status " in warning_text
    assert "missing" in warning_text
    assert "mapping" in warning_text
    assert "openbao_arrangement_kv_mount" in warning_text
    assert "openbao_arrangement_kv_path" in warning_text
    assert "skipped" in warning_text
    assert not any(
        secret_name in warning_text
        for secret_name in ("openbao_arrangement_read.json", "document | from_json")
    )
    assert _when(warning) == _when(fallback)

    usable_summaries = [
        task for task in tasks
        if "ansible.builtin.debug" in task
        and "identities" in _debug_message(task).lower()
        and "source" in _debug_message(task).lower()
    ]
    assert len(usable_summaries) == 1
    summary = _debug_message(usable_summaries[0])
    assert "openbao_arrangement.identities | length" in summary
    assert "_openbao_arrangement_source" in summary


def test_reconcile_policy_reads_only_the_exact_arrangement_leaf(rendered_defaults):
    values, _approles, _policies = rendered_defaults
    leaf = (
        f"{values['openbao_arrangement_kv_mount']}/data/"
        f"{values['openbao_arrangement_kv_path']}"
    )
    stanzas = list(_stanzas(_render(RECONCILE, values)))
    leaf_stanzas = [body for path, body in stanzas if path == leaf]

    assert len(leaf_stanzas) == 1
    assert _capabilities(leaf_stanzas[0]) == ["read"]
