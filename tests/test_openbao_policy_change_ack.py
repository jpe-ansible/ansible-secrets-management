"""Contract for the policy-text change acknowledgement in 08b-rbac-policy-writes.yml.

A full-set run replaces the stored text of every existing policy whose rendered
text differs from live. Selection acknowledges those changes before a write.
Missing policies need no acknowledgement.

These render the REAL Jinja expressions and `when` conditions out of the task
file, never a reimplementation of them.
"""

from pathlib import Path
import unittest

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template


ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "roles" / "openbao" / "tasks" / "init" / "08b-rbac-policy-writes.yml"

RESOLVE = "Resolve existing RBAC policies whose rendered text differs from live"
ASSERT = "Refuse policy text changes that are not acknowledged"
DIFF = "Compute a unified line diff for each existing policy whose text changed"
SHOW = "Show the policy text diffs in check mode"


def _task(name):
    for t in yaml.safe_load(TASKS.read_text(encoding="utf-8")):
        if t.get("name") == name:
            return t
    raise AssertionError(f"task {name!r} not found in {TASKS}")


def _render(expr, variables):
    templar = Templar(loader=DataLoader())
    templar.available_variables = variables
    return templar.template(trust_as_template(expr))


def _conditions_hold(task, variables):
    return all(_render("{{ " + cond + " }}", variables) for cond in task["when"])


def changes(declared, live, rendered, selector=""):
    """Render the task's OWN set_fact result for the given live and rendered text."""
    task = _task(RESOLVE)
    variables = {
        "openbao_bootstrap_token": "s.test",
        "openbao_select": {"policies": [selector]} if selector else {},
        "openbao_reachable_policies": [{"name": n} for n in declared],
        "openbao_existing_policy_names": list(live),
        "openbao_existing_policy_map": dict(live),
        "openbao_rendered_policy_map": dict(rendered),
    }
    if not _conditions_hold(task, variables):
        return None
    return _render(task["ansible.builtin.set_fact"]["openbao_policy_text_changes"], variables)


def ack_passes(changed, selector=""):
    """Evaluate the task's own assertion with full or selected targets."""
    task = _task(ASSERT)
    variables = {
        "openbao_bootstrap_token": "s.test",
        "openbao_select": {"policies": [selector]} if selector else {},
        "openbao_policy_text_changes": changed,
    }
    if not _conditions_hold(task, variables):
        return True
    return all(_render("{{ " + cond + " }}", variables) for cond in task["ansible.builtin.assert"]["that"])


def ack_message(changed):
    task = _task(ASSERT)
    variables = {
        "openbao_policy_text_changes": changed,
    }
    return _render(task["ansible.builtin.assert"]["fail_msg"], variables)


LIVE = {"hermes": "old hermes text", "apps": "apps text", "media": "media text"}
RENDERED = {"hermes": "new hermes text", "apps": "apps text", "media": "media text"}
DECLARED = ["hermes", "apps", "media"]


class PolicyTextChangeAck(unittest.TestCase):
    def test_a_changed_policy_without_an_ack_is_refused(self):
        changed = changes(DECLARED, LIVE, RENDERED)
        self.assertEqual(changed, ["hermes"])
        self.assertFalse(ack_passes(changed))

    def test_b_selection_acknowledges_the_selected_policy(self):
        changed = changes(DECLARED, LIVE, RENDERED)
        self.assertTrue(ack_passes(changed, selector="hermes"))

    def test_c_full_set_changes_report_all_names(self):
        live = {"hermes": "a", "apps": "b", "media": "c"}
        rendered = {"hermes": "a2", "apps": "b2", "media": "c"}
        changed = changes(DECLARED, live, rendered)
        self.assertEqual(changed, ["apps", "hermes"])
        self.assertFalse(ack_passes(changed))
        message = ack_message(changed)
        self.assertIn('"policies": ["apps", "hermes"]', message)

    def test_d_a_missing_policy_needs_no_ack(self):
        live = {"apps": "apps text", "media": "media text"}
        changed = changes(DECLARED, live, RENDERED)
        self.assertEqual(changed, [])
        self.assertTrue(ack_passes(changed))

    def test_e_an_unchanged_policy_needs_no_ack(self):
        changed = changes(DECLARED, LIVE, LIVE)
        self.assertEqual(changed, [])
        self.assertTrue(ack_passes(changed))

    def test_f_a_single_object_run_skips_the_check(self):
        task = _task(RESOLVE)
        variables = {
            "openbao_bootstrap_token": "s.test",
            "openbao_select": {"policies": ["hermes"]},
        }
        self.assertFalse(_conditions_hold(task, variables))
        self.assertIsNone(changes(DECLARED, LIVE, RENDERED, selector="hermes"))
        self.assertTrue(ack_passes(["hermes"], selector="hermes"))

    def test_g_the_failure_names_policies_and_never_their_text(self):
        changed = changes(DECLARED, LIVE, RENDERED)
        msg = ack_message(changed)
        self.assertIn("hermes", msg)
        self.assertIn('"openbao_select": {"policies": ["hermes"]}', msg)
        self.assertNotIn("new hermes text", msg)
        self.assertNotIn("old hermes text", msg)


    def test_h_check_mode_diffs_exactly_the_changed_policies(self):
        task = _task(DIFF)
        variables = {
            "ansible_check_mode": True,
            "openbao_bootstrap_token": "s.test",
            "openbao_select": {},
            "openbao_policy_text_changes": ["hermes"],
            "openbao_existing_policy_map": LIVE,
            "openbao_rendered_policy_map": RENDERED,
        }
        self.assertTrue(_conditions_hold(task, variables))
        self.assertEqual(_render(task["loop"], variables), ["hermes"])
        variables["item"] = "hermes"
        args = task["ansible.utils.fact_diff"]
        self.assertEqual(_render(args["before"], variables), "old hermes text")
        self.assertEqual(_render(args["after"], variables), "new hermes text")

    def test_i_policy_text_is_shown_only_in_check_mode(self):
        for name in (DIFF, SHOW):
            task = _task(name)
            variables = {
                "ansible_check_mode": False,
                "openbao_bootstrap_token": "s.test",
                "openbao_select": {},
            }
            self.assertFalse(_conditions_hold(task, variables), name)

    def test_j_the_shown_diff_is_labelled_with_its_policy(self):
        task = _task(SHOW)
        variables = {
            "openbao_policy_text_diffs": {"results": [
                {"item": "hermes", "diff_lines": ["-old", "+new"]},
                {"item": "apps", "skipped": True},
            ]},
        }
        shown = _render(task["loop"], variables)
        self.assertEqual([r["item"] for r in shown], ["hermes"])
        variables["item"] = shown[0]
        self.assertEqual(_render(task["ansible.builtin.debug"]["msg"], variables),
                         ["hermes:", "-old", "+new"])


if __name__ == "__main__":
    unittest.main()
