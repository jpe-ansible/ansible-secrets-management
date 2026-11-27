"""The RBAC write must be a no-op when the server already holds the policy.

The write fires when the stored text differs from the rendered text, so it is
idempotent only if those two can ever compare equal. They could not, for two
independent reasons:

  * `bao policy read -format=json` returns {"policy": ...} at TOP LEVEL. The
    expression read `.data.policy`, which does not exist, so every entry
    resolved to '' and every policy looked changed on every converge.
  * The server appends a trailing newline on write, so even with the correct
    key the stored text is the rendered text plus "\\n", and an exact !=
    is always true.

Either defect alone rewrites every policy on every run while the task honestly
reports "changed" -- so fixing one without the other looks like a fix and
changes nothing. Both are asserted here.

Measured live before the fix: rendered 475 bytes, stored 476, differing only in
that newline.

These render the REAL expressions out of the task file, never a reimplementation.
"""

from pathlib import Path
import json
import unittest

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "roles" / "openbao" / "tasks" / "init" / "08b-rbac-policy-writes.yml"
POLICY_TASKS = ROOT / "roles" / "openbao" / "tasks" / "init" / "08-rbac-policies.yml"
POLICY_DECLARATION_TASKS = ROOT / "roles" / "openbao" / "tasks" / "init" / "08-policy-declaration-assertions.yml"
EXISTING_TASK = "Build the existing RBAC policy content map"
WRITE_TASK = "Write the RBAC policies that are missing or changed"
DENIED_READ_TASK = "FAIL -- an existing RBAC policy read was DENIED, so absence cannot be concluded"
POLICY_NAMES_TASK = "Resolve existing RBAC policy names from the roster audit or list result"

# What the CLI actually returns: no `data` envelope, trailing newline appended.
POLICY_BODY = 'path "sys/policies/acl/apps" {\n  capabilities = ["read"]\n}\n'
SERVER_STORED = POLICY_BODY + "\n"


def _task(name, path=TASKS):
    for t in yaml.safe_load(path.read_text(encoding="utf-8")):
        if t.get("name") == name:
            return t
    raise AssertionError(f"task {name!r} not found in {path}")


def _render(expr, variables, wrap=False):
    templar = Templar(loader=DataLoader())
    templar.available_variables = variables
    return templar.template(
        trust_as_template("{{ " + expr + " }}" if wrap else expr)
    )


def existing_map(name, stdout):
    """Render the existing-map expression for one read result, exactly as the
    real task does: the `vars` pairs-builder first, then the final
    items2dict expression fed from that result."""
    task = _task(EXISTING_TASK)
    pairs_expr = task["vars"]["_openbao_existing_policy_pairs"]
    final_expr = task["ansible.builtin.set_fact"]["openbao_existing_policy_map"]
    results = [{"item": {"name": name}, "stdout": stdout, "rc": 0}]
    pairs = _render(
        pairs_expr, {"openbao_existing_policy_reads": {"results": results}}
    )
    return _render(final_expr, {"_openbao_existing_policy_pairs": pairs})


def write_fires(name, existing, rendered):
    """Render the write task's own content-comparison condition."""
    cond = [
        c for c in _task(WRITE_TASK)["when"]
        if "openbao_rendered_policy_map" in str(c)
    ]
    assert len(cond) == 1, f"expected one comparison condition, got {cond}"
    return _render(
        cond[0],
        {
            "item": {"name": name},
            "openbao_existing_policy_names": [name],
            "openbao_existing_policy_map": existing,
            "openbao_rendered_policy_map": rendered,
        },
        wrap=True,
    )


class ExistingMapReadsTheRightKey(unittest.TestCase):
    def test_top_level_policy_key_is_read(self):
        got = existing_map("apps", json.dumps({"policy": SERVER_STORED}))
        self.assertEqual(got["apps"], POLICY_BODY.strip())

    def test_a_data_envelope_is_NOT_what_the_cli_returns(self):
        # Guards the original defect directly: if the expression goes back to
        # `.data.policy`, this shape is what it would need, and the real CLI
        # never sends it. An empty result here means every policy looks changed.
        got = existing_map("apps", json.dumps({"data": {"policy": SERVER_STORED}}))
        self.assertEqual(got["apps"], "", "sanity: no top-level policy key")


class WriteIsIdempotent(unittest.TestCase):
    def test_unchanged_policy_does_NOT_fire_the_write(self):
        # The whole point: stored == rendered + "\n" must compare equal.
        existing = existing_map("apps", json.dumps({"policy": SERVER_STORED}))
        self.assertFalse(
            write_fires("apps", existing, {"apps": POLICY_BODY.strip()})
        )

    def test_a_genuinely_changed_policy_still_fires_the_write(self):
        # The guard must not disable the behaviour it protects.
        existing = existing_map("apps", json.dumps({"policy": SERVER_STORED}))
        self.assertTrue(
            write_fires("apps", existing, {"apps": 'path "other" {}'})
        )

    def test_trailing_whitespace_alone_is_never_a_change(self):
        existing = existing_map(
            "apps", json.dumps({"policy": POLICY_BODY + "\n\n  "})
        )
        self.assertFalse(
            write_fires("apps", existing, {"apps": POLICY_BODY.strip()})
        )


class CombineLoopCollapseIsEquivalent(unittest.TestCase):
    """Both the render and existing-map tasks moved from a per-item `combine`
    (O(n^2) over ~60 policies -- every iteration re-copies the whole
    accumulated dict) to appending {key, value} pairs once and dict-ifying
    at the end. Proves the two reductions agree on the same input,
    independent of `lookup('template', ...)` or a live bao read."""

    SAMPLE = {"apps": "path a", "aws-write": "path b", "ssh-ca": "path c"}

    def _old_combine_result(self):
        acc = {}
        for name, value in self.SAMPLE.items():
            acc = _render(
                "{{ acc | combine({name_: value_}) }}",
                {"acc": acc, "name_": name, "value_": value},
            )
        return acc

    def _new_pairs_result(self):
        pairs_expr = (
            "{%- set _pairs = [] -%}"
            "{%- for name, value in items -%}"
            "{%- set _ = _pairs.append({'key': name, 'value': value}) -%}"
            "{%- endfor -%}"
            "{{ _pairs }}"
        )
        pairs = _render(pairs_expr, {"items": list(self.SAMPLE.items())})
        return _render("{{ pairs | items2dict }}", {"pairs": pairs})

    def test_old_and_new_reductions_agree(self):
        self.assertEqual(self._old_combine_result(), self._new_pairs_result())


class SelectedPolicyLoops(unittest.TestCase):
    CANDIDATES = [{"name": "apps"}, {"name": "ssh-ca"}]

    def _policy_loop(self, task_name, selector="", selected=None):
        expression = _task(task_name)["loop"]
        targets = selected if selected is not None else self.CANDIDATES
        return _render(expression, {
            "openbao_select": {"policies": [selector]} if selector else {},
            "openbao_rbac_policy_targets": targets,
            "openbao_reachable_policies": self.CANDIDATES,
        })

    def test_empty_selector_keeps_the_full_policy_target_list(self):
        for task_name in (
            "Read existing RBAC policy contents",
            WRITE_TASK,
        ):
            self.assertEqual(self._policy_loop(task_name), self.CANDIDATES)

    def test_valid_selector_limits_only_the_policy_read_and_write_loops(self):
        selected = [self.CANDIDATES[1]]
        self.assertEqual(
            self._policy_loop("Read existing RBAC policy contents", "ssh-ca", selected),
            selected,
        )
        self.assertEqual(self._policy_loop(WRITE_TASK, "ssh-ca", selected), selected)

    def test_policy_selection_candidate_is_the_reachable_declared_set(self):
        task = _task("Select RBAC policy objects", POLICY_TASKS)
        candidates = task["vars"]["openbao_select_candidates"]
        self.assertIn("openbao_reachable_policies", candidates)
        self.assertIn("openbao_policies", candidates)
        self.assertEqual(task["vars"]["openbao_select_kind"], "policies")

        task_names = [task.get("name") for task in yaml.safe_load(POLICY_TASKS.read_text(encoding="utf-8"))]
        self.assertLess(
            task_names.index("Select RBAC policy objects"),
            task_names.index("Render the RBAC policies on the controller"),
        )
        self.assertLess(
            task_names.index("Render the RBAC policies on the controller"),
            task_names.index("Assert no scheduled RBAC policy rendered empty"),
        )
        self.assertLess(
            task_names.index("Select RBAC policy objects"),
            task_names.index("Refuse live objects that collide with roster agent names"),
        )
        self.assertLess(
            task_names.index("Assert no scheduled RBAC policy rendered empty"),
            task_names.index("Read the stored RBAC policies and write what differs"),
        )

    def test_policy_render_and_empty_guard_use_the_resolved_targets(self):
        render = _task("Render the RBAC policies on the controller", POLICY_TASKS)
        pairs = render["vars"]["_openbao_rendered_policy_pairs"]
        self.assertIn("for item in openbao_rbac_policy_targets", pairs)
        empty_guard = _task("Assert no scheduled RBAC policy rendered empty", POLICY_TASKS)
        self.assertIn("openbao_rbac_policy_targets", empty_guard["vars"]["_openbao_empty_rendered_policies"])

    def test_full_reconcile_gap_guard_runs_only_for_full_set_runs(self):
        task = _task("FAIL -- the reconcile identity cannot manage every declared policy", POLICY_TASKS)
        variables = {
            "openbao_select": {"policies": ["apps"]},
            "openbao_bootstrap_token": "s.test",
            "openbao_reconcile_mode": True,
            "openbao_bounded_rbac_mode": True,
            "openbao_ungranted_policy_names": ["human-gated"],
        }
        self.assertFalse(all(
            _render(condition, variables, wrap=True) for condition in task["when"]
        ))
        variables["openbao_select"] = {}
        self.assertTrue(all(
            _render(condition, variables, wrap=True) for condition in task["when"]
        ))

    def test_declaration_assertions_are_imported_before_policy_work(self):
        imported = _task("Assert RBAC policy declaration invariants", POLICY_TASKS)
        self.assertEqual(
            imported["ansible.builtin.import_tasks"], "init/08-policy-declaration-assertions.yml"
        )
        tasks = yaml.safe_load(POLICY_DECLARATION_TASKS.read_text(encoding="utf-8"))
        self.assertEqual(
            [task["name"] for task in tasks],
            [
                "Assert every Terrakube workspace policy names the workspace it points at",
                "Assert no AI domain name is a wildcard or the all rollup",
                "Assert every KV rotation target renders only exact policy paths",
            ],
        )
        self.assertTrue(all(task.get("run_once") for task in tasks))


class LiveNameReuseAndDeniedReads(unittest.TestCase):
    def test_policy_list_reuses_the_roster_fact_or_parses_the_fallback(self):
        expression = _task(POLICY_NAMES_TASK)["ansible.builtin.set_fact"][
            "openbao_existing_policy_names"]
        self.assertEqual(_render(expression, {
            "openbao_roster_live_check_enabled": True,
            "openbao_roster_live_policy_names": ["apps", "ssh-ca"],
            "openbao_policies_raw": {"stdout": '["fallback"]'},
        }), ["apps", "ssh-ca"])
        self.assertEqual(_render(expression, {
            "openbao_roster_live_check_enabled": False,
            "openbao_policies_raw": {"stdout": '["fallback"]'},
        }), ["fallback"])

    def test_policy_list_fallback_runs_in_check_mode(self):
        """The roster live check runs only on a real converge, so its
        role-default empty list is not the live list in check mode -- the
        fallback must run there, or every declared policy looks missing and
        the check-mode report lists unchanged policies as pending writes."""
        task = _task("List existing policies")
        self.assertIn("ansible_check_mode", task["when"])
        # The role default defines the roster fact on every play, so an
        # `is not defined` gate here can never fire.
        self.assertNotIn("failed_when", task)
        for condition in task["when"]:
            self.assertNotIn("openbao_roster_live_policy_names is not defined", str(condition))

    def test_a_denied_existing_policy_read_fails_instead_of_becoming_absent(self):
        task = _task(DENIED_READ_TASK)
        denied = _render(task["vars"]["_denied"], {
            "openbao_existing_policy_reads": {"results": [{
                "item": {"name": "apps"},
                "rc": 1,
                "stderr": "permission denied (403)",
            }]},
        })
        self.assertEqual(denied, ["apps"])
        self.assertFalse(_render(
            task["ansible.builtin.assert"]["that"][0], {"_denied": denied}, wrap=True
        ))


if __name__ == "__main__":
    unittest.main()
