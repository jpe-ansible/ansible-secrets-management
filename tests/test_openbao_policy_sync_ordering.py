"""Ordering contract for the reconcile-mode policy-sync pair in the openbao
role's init sequence.

A reconcile-mode login only carries the `policy-sync` policy when it is the
inert `openbao-policy-sync` AppRole, and only THAT identity may rewrite the
live `openbao-reconcile` policy from the declared set (see
tasks/init/02-initialize-cluster.yml and
templates/openbao-reconcile-policy.hcl.j2). Every other init step that
consumes a reconcile grant for a NEWLY declared name -- SSH signing roles
(init/07) and AppRoles (init/10) -- 403s against a live reconcile policy that
predates that name, because the write it needs is exactly what policy-sync
was about to grant. Running the sync AFTER those consumers (it used to live
in init/08, run via tasks/init/08-rbac-policies.yml) is a chicken-and-egg: the
403 aborts the play before the sync ever gets a chance to run.

This test parses the REAL task files (init.yml's own include order, plus
each included file's own task list) rather than reimplementing the ordering,
and asserts the sync pair comes before every reconcile-grant consumer it
could otherwise starve.
"""

from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
INIT_ENTRYPOINT = ROOT / "roles" / "openbao" / "tasks" / "init.yml"
INIT_DIR = ROOT / "roles" / "openbao" / "tasks" / "init"

SYNC_TASK = "Sync the reconcile policy from the declared set (policy-sync)"
ASK_TASK = "Ask whether this identity may sync the reconcile policy"
ARRANGEMENT_READ_TASK = "Read the arrangement KV leaf"

# Reconcile-grant consumers that write to a path keyed by a DECLARED NAME
# (SSH role, AppRole) rather than a stable mount-level wildcard -- these are
# exactly the tasks a live reconcile policy that predates a new name will
# 403 on.
GRANT_CONSUMERS = [
    "Reconcile the SSH roles",
    "Create the missing AppRoles bound to their policy",
    "Reconcile token_policies on existing AppRoles",
]


def _included_init_files():
    """The init/*.yml files init.yml imports, in the order it imports them."""
    tasks = yaml.safe_load(INIT_ENTRYPOINT.read_text(encoding="utf-8"))
    files = []
    for task in tasks:
        target = task.get("ansible.builtin.import_tasks")
        if isinstance(target, str) and target.startswith("init/"):
            files.append(INIT_DIR.parent / target)
    return files


def _flatten(tasks, order, base_dir):
    """Depth-first task names in document order.

    Recurses into block/rescue/always AND into any sibling-file
    import_tasks/include_tasks whose target is a plain string (the dynamic,
    `loop`-driven include in init/03 passes a dict instead and is skipped --
    it carries no task names of interest here).
    """
    for task in tasks or []:
        if not isinstance(task, dict):
            continue
        if "name" in task:
            order.append(task["name"])
        for key in ("block", "rescue", "always"):
            if key in task:
                _flatten(task[key], order, base_dir)
        for key in ("ansible.builtin.import_tasks", "ansible.builtin.include_tasks"):
            target = task.get(key)
            if isinstance(target, str):
                included = base_dir / target
                _flatten(
                    yaml.safe_load(included.read_text(encoding="utf-8")),
                    order,
                    included.parent,
                )


def _global_task_order():
    order = []
    for path in _included_init_files():
        _flatten(yaml.safe_load(path.read_text(encoding="utf-8")), order, path.parent)
    return order


class PolicySyncRunsBeforeItsGrantConsumers(unittest.TestCase):
    def test_sync_task_exists_exactly_once(self):
        order = _global_task_order()
        self.assertEqual(
            order.count(SYNC_TASK),
            1,
            f"expected exactly one '{SYNC_TASK}' task across the init "
            "sequence -- found it duplicated or missing",
        )

    def test_ask_task_exists_exactly_once(self):
        order = _global_task_order()
        self.assertEqual(order.count(ASK_TASK), 1)

    def test_arrangement_is_read_once_before_the_sync_render(self):
        """The sync render reads openbao_policies, which carries the
        arrangement policies only after the arrangement document is loaded."""
        order = _global_task_order()
        self.assertEqual(order.count(ARRANGEMENT_READ_TASK), 1)
        self.assertLess(order.index(ARRANGEMENT_READ_TASK), order.index(SYNC_TASK))

    def test_sync_precedes_every_reconcile_grant_consumer(self):
        order = _global_task_order()
        sync_index = order.index(SYNC_TASK)
        for consumer in GRANT_CONSUMERS:
            self.assertIn(
                consumer,
                order,
                f"expected to find task {consumer!r} in the init sequence -- "
                "did it get renamed?",
            )
            consumer_index = order.index(consumer)
            self.assertLess(
                sync_index,
                consumer_index,
                f"'{SYNC_TASK}' (index {sync_index}) must run before "
                f"'{consumer}' (index {consumer_index}): the consumer writes "
                "to a path keyed by a declared name, which a live reconcile "
                "policy that predates that name will 403 on -- exactly the "
                "grant policy-sync is about to write.",
            )

    def test_sync_pair_is_adjacent_to_the_reconcile_login(self):
        """The sync pair belongs directly after the reconcile login succeeds,
        not buried later in the sequence -- keep it next to the bootstrap token
        and bounded execution-mode facts it depends on."""
        order = _global_task_order()
        login_index = order.index("Use the per-call reconcile token when it authenticated")
        ask_index = order.index(ASK_TASK)
        sync_index = order.index(SYNC_TASK)
        # Nothing that writes to a declared-name path may sit between the
        # login and the sync pair.
        for consumer in GRANT_CONSUMERS:
            consumer_index = order.index(consumer)
            self.assertFalse(
                login_index < consumer_index < sync_index,
                f"'{consumer}' runs between the reconcile login and the "
                "policy-sync pair -- move policy-sync earlier",
            )
        self.assertLess(login_index, ask_index)
        self.assertLess(ask_index, sync_index)


if __name__ == "__main__":
    unittest.main()
