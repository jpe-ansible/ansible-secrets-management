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
CLUSTER = ROOT / "roles/openbao/tasks/init/02-initialize-cluster.yml"


def _when(task):
    return task.get("when", [])


def _debug_message(task):
    debug = task.get("ansible.builtin.debug", {})
    return str(debug.get("msg", ""))


def test_arrangement_loader_reads_declared_leaf_safely():
    tasks = _task_file(LOADER)
    requests = [task for task in tasks if "ansible.builtin.uri" in task]

    assert len(requests) == 2
    direct, proxy = requests
    leaf = "/v1/{{ openbao_arrangement_kv_mount }}/data/{{ openbao_arrangement_kv_path }}"
    assert direct["ansible.builtin.uri"]["url"] == "{{ openbao_cli_addr }}" + leaf
    assert direct["ansible.builtin.uri"]["headers"]["X-Vault-Token"] == "{{ openbao_bootstrap_token }}"
    assert "not (openbao_cli_proxy_active | default(false) | bool)" in _when(direct)
    assert proxy["ansible.builtin.uri"]["url"] == "http://localhost" + leaf
    assert "openbao_window_proxy_addr" in proxy["ansible.builtin.uri"]["unix_socket"]
    assert "headers" not in proxy["ansible.builtin.uri"]
    assert "openbao_cli_proxy_active | default(false) | bool" in _when(proxy)
    for task in requests:
        uri = task["ansible.builtin.uri"]
        assert uri["method"] == "GET"
        assert uri["status_code"] == [200, 403, 404]
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
    select = next(t for t in tasks if t.get("name") == "Keep the arrangement read result from the branch that ran")
    assert select["no_log"] is True
    assert "_openbao_arrangement_read_proxy" in select["ansible.builtin.set_fact"]["openbao_arrangement_read"]
    assert "openbao_bootstrap_token is defined" in str(_when(task))


def test_arrangement_loader_is_imported_before_policy_sync_for_every_run():
    tasks = yaml.safe_load(CLUSTER.read_text(encoding="utf-8"))
    imports = {
        _include_details(task)[1]["file"]: (index, task, _include_details(task))
        for index, task in enumerate(tasks)
        if _include_details(task) is not None
    }
    loader_index, loader, loader_details = imports["07z-load-arrangement.yml"]
    sync_index = imports["02b-policy-sync.yml"][0]
    cluster = next(
        task for task in yaml.safe_load(INIT.read_text(encoding="utf-8"))
        if (_include_details(task) or (None, {}))[1].get("file")
        == "init/02-initialize-cluster.yml"
    )

    assert loader_index < sync_index
    assert loader_details[0] == "import_tasks"
    assert "when" not in loader
    assert "always" in cluster.get("tags", [])
    assert "07z-load-arrangement.yml" not in INIT.read_text(encoding="utf-8")


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


def test_arrangement_loaded_flag_is_set_only_on_an_accepted_mapping():
    tasks = _task_file(LOADER)
    setters = {
        task["name"]: task["ansible.builtin.set_fact"]["openbao_arrangement_loaded"]
        for task in tasks
        if "openbao_arrangement_loaded" in task.get("ansible.builtin.set_fact", {})
    }
    assert setters == {
        "Initialize the arrangement as empty for this run": False,
        "Accept the parsed arrangement mapping": True,
    }
