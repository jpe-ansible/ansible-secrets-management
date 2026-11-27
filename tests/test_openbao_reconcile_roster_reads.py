"""Roster collision reads use exact policy fields and preserve write bounds."""

import json
import shlex

import pytest

from openbao_reconcile_bounds_helpers import (
    RECONCILE,
    ROOT,
    _capabilities,
    _command_text,
    _named_task,
    _render,
    _render_value,
    _stanzas,
    rendered_defaults,
)

COLLISIONS = ROOT / "roles/openbao/tasks/init/08a-roster-live-collisions.yml"
RBAC_TASKS = ROOT / "roles/openbao/tasks/init/08-rbac-policies.yml"
ROSTER = {"docs-updater": {}, "ci-fixer": {}}
pytestmark = pytest.mark.parametrize(
    "rendered_defaults", [{"agents": ROSTER}], indirect=True,
)


def test_roster_read_grants_are_exact_and_leave_write_stanzas_unchanged(rendered_defaults):
    values, _approles, _policies = rendered_defaults
    baseline = [
        (path, body)
        for path, body in _stanzas(_render(RECONCILE, dict(values, openbao_ai_agents={})))
        if path.startswith("auth/approle/")
    ]
    actual = [
        (path, body) for path, body in _stanzas(_render(RECONCILE, values))
        if path.startswith("auth/approle/")
    ]
    added = [(path, body) for path, body in actual if (path, body) not in baseline]

    assert len(added) == len(ROSTER)
    assert {path for path, _body in added} == {
        f"auth/approle/role/{agent}/policies" for agent in ROSTER
    }
    for _path, body in added:
        assert _capabilities(body) == ["read"]
        assert "parameters" not in body
    assert [stanza for stanza in actual if stanza not in added] == baseline


@pytest.mark.parametrize(
    ("window_mode", "bounded_mode", "expected"),
    [(True, True, False), (False, False, True), (False, True, True)],
    ids=[
        "bounded-window-selection-skips-audit",
        "full-run-keeps-audit",
        "bounded-reconcile-keeps-audit",
    ],
)
def test_live_roster_collision_audit_runs_only_outside_window_mode(
    rendered_defaults, window_mode, bounded_mode, expected,
):
    values, _approles, _policies = rendered_defaults
    task = _named_task(RBAC_TASKS, "Refuse live objects that collide with roster agent names")
    assert task["ansible.builtin.import_tasks"] == "init/08a-roster-live-collisions.yml"
    context = dict(
        values,
        openbao_ai_agents=ROSTER,
        openbao_ai_admin_window_mode=window_mode,
        openbao_bounded_rbac_mode=bounded_mode,
    )
    conditions = task["when"] if isinstance(task["when"], list) else [task["when"]]
    runs = all(
        _render_value(context, "{{ " + condition + " }}") in (True, "True")
        for condition in conditions
    )
    assert runs is expected


@pytest.mark.parametrize("policies", [None, [], ["docs-updater"], ["docs-updater", "other"]])
def test_roster_check_reads_only_policies_and_compares_the_response(rendered_defaults, policies):
    values, _approles, _policies = rendered_defaults
    agent = "docs-updater"
    read = _named_task(COLLISIONS, "Read live AppRoles with a marked roster policy")
    for name in ROSTER:
        assert shlex.split(_command_text(read, dict(values, item=name))) == [
            "bao", "read", "-format=json", f"auth/approle/role/{name}/policies",
            f"token_policies={name}",
        ]
    assert read["no_log"] is True
    assert read["changed_when"] is False
    assert _render_value(values, read["loop"]) == list(ROSTER)

    response = {"data": {} if policies is None else {"token_policies": policies}}
    resolve = _named_task(COLLISIONS, "Resolve live roster AppRole configurations")
    pairs = _render_value(
        values, resolve["vars"]["_approle_pairs"],
        openbao_roster_live_approle_reads={"results": [
            {"item": agent, "rc": 0, "stdout": json.dumps(response)},
            {"item": "ci-fixer", "skipped": True},
        ]},
    )
    assert pairs == [{"key": agent, "value": response}]
    conflicts = _render_value(
        values, values["openbao_roster_live_approle_conflicts"],
        openbao_roster_live_approle_names=[agent],
        openbao_roster_live_policy_names=[agent],
        openbao_roster_live_policy_conflicts=[],
        openbao_roster_live_approle_configs={agent: response},
    )
    assert (conflicts == []) is (policies == [agent])
