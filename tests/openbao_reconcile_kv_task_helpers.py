"""Derive reconcile KV grants from their Ansible task sources."""

from pathlib import Path
import shlex

from openbao_reconcile_bounds_helpers import (
    ROOT,
    _command_text,
    _include_details,
    _loop_values,
    _named_task,
    _render_value,
    _task_file,
)

TASKS_03 = ROOT / "roles/openbao/tasks/init/03-kv-mounts-and-seed-secrets.yml"
TASKS_03B = ROOT / "roles/openbao/tasks/init/03b-kv-mounts.yml"
TASKS_08A = ROOT / "roles/openbao/tasks/init/08a-roster-live-collisions.yml"
PROMOTE_TASKS = ROOT / "roles/openbao/tasks/promote_app_secret.yml"
GENERATED_SEED_TASKS = ROOT / "roles/openbao/tasks/seed_generated_app_secret.yml"
ROSTER_SEED_TASKS = ROOT / "roles/openbao/tasks/seed_roster_agent_leaf.yml"
ROSTER_OWNER_TASKS = ROOT / "roles/openbao/tasks/seed_roster_agent_leaf_owner.yml"
LEGACY_AGENT_TASKS = ROOT / "roles/openbao/tasks/remove_app_agent_legacy_fields.yml"
ROTATION_TASKS = ROOT / "roles/openbao/tasks/tag_rotation_exempt.yml"

def _add_kv_command(grants, task, values):
    rendered = _command_text(task, values)
    if not rendered:
        return
    args = shlex.split(" ".join(rendered.split()))
    if args[:2] == ["bao", "kv"] and len(args) > 3:
        if args[2] == "metadata":
            action = args[3]
            target = args[-1]
            mount = next(
                (arg.split("=", 1)[1] for arg in args if arg.startswith("-mount=")),
                None,
            )
            if mount:
                target = f"{mount}/metadata/{target.lstrip('/')}"
            else:
                mount, relative = target.split("/", 1)
                target = f"{mount}/metadata/{relative}"
            capabilities = {"get": {"read"}, "list": {"list"}, "patch": {"patch"}}
        else:
            action = args[2]
            target = args[-1]
            mount, relative = target.split("/", 1)
            target = f"{mount}/data/{relative}"
            capabilities = {
                "get": {"read"},
                "list": {"list"},
                "put": {"create", "update"},
                "patch": {"patch"},
                "delete": {"delete"},
                "destroy": {"delete"},
            }
        grants.setdefault(target, set()).update(capabilities.get(action, set()))
    elif args[:2] in (["bao", "read"], ["bao", "write"]):
        target = next(
            (arg for arg in args[2:] if not arg.startswith("-") and "=" not in arg),
            "",
        )
        if target.endswith("/config"):
            grants.setdefault(target, set()).add(
                "read" if args[1] == "read" else "update"
            )

def _add_kv_uri(grants, task, values):
    uri = task.get("ansible.builtin.uri", {})
    url = uri.get("url", "")
    if "/v1/" not in url:
        return
    path = _render_value(values, url.split("/v1/", 1)[1])
    method = uri.get("method", "GET").upper()
    capabilities = {
        "GET": {"read"},
        "LIST": {"list"},
        "POST": {"create", "update"},
        "PATCH": {"patch"},
        "DELETE": {"delete"},
    }
    grants.setdefault(path, set()).update(capabilities.get(method, set()))

def _add_promoted_paths(grants, values, include_task):
    details = _include_details(include_task)
    if details is None:
        raise AssertionError(f"expected an include/import task: {include_task!r}")
    action, include, include_vars = details
    if action not in ("include_tasks", "import_tasks"):
        return
    filename = include["file"]
    if not filename.endswith("promote_app_secret.yml"):
        return
    loop_var = include_task.get("loop_control", {}).get("loop_var", "item")
    items = _loop_values(values, include_task["loop"]) if "loop" in include_task else [None]
    promote_tasks = _task_file(PROMOTE_TASKS)
    for item in items:
        context = dict(values)
        if item is not None:
            context[loop_var] = item
        for name in ("openbao_promote_app", "openbao_promote_mount", "openbao_promote_path"):
            if name in include_vars:
                context[name] = _render_value(context, include_vars[name])
        for task in promote_tasks:
            for name, expression in task.get("vars", {}).items():
                if name in ("_promote_mount", "_promote_path"):
                    context[name] = _render_value(context, expression)
            _add_kv_command(grants, task, context)
            _add_kv_uri(grants, task, context)

def _add_seeded_paths(grants, values, include_task):
    details = _include_details(include_task)
    if details is None:
        raise AssertionError(f"expected an include/import task: {include_task!r}")
    action, include, include_vars = details

    if action in ("include_tasks", "import_tasks"):
        filename = include["file"]
        if filename.endswith("seed_context7_key.yml"):
            # This legacy migration seed is explicitly disabled in reconcile mode.
            return
        if not filename.endswith(
            ("seed_generated_app_secret.yml", "seed_roster_agent_leaf.yml")
        ):
            if Path(filename).name.startswith("seed_"):
                raise AssertionError(f"unrecognized seed task include: {filename!r}")
            return
        is_roster_seed = filename.endswith("seed_roster_agent_leaf.yml")
        seed_task = _named_task(
            GENERATED_SEED_TASKS, "Call shared generate-if-absent seeding"
        )
        seed_details = _include_details(seed_task)
        if seed_details is None:
            raise AssertionError(
                "shared generated seeding task has no include_role action"
            )
        seed_action, seed_include, seed_vars = seed_details
        if (
            seed_action != "include_role"
            or seed_include["name"] != "dryvist.homelab.openbao_secrets"
            or seed_include.get("tasks_from", "main") != "seed_generated"
        ):
            raise AssertionError(
                "shared generated seeding task has an unexpected include_role"
            )
    elif action == "include_role":
        role_name = include["name"]
        tasks_from = include.get("tasks_from", "main")
        if (
            role_name != "dryvist.homelab.openbao_secrets"
            or tasks_from != "seed_generated"
        ):
            if "seed" in role_name or "seed" in str(tasks_from):
                raise AssertionError(
                    f"cannot interpret seeded include_role {role_name!r}:{tasks_from!r}"
                )
            return
        is_roster_seed = False
        seed_vars = include_vars
    else:
        raise AssertionError(f"cannot interpret seeded path source {action!r}")

    mount_expression = seed_vars.get("openbao_secrets_seed_mount")
    path_expression = seed_vars.get("openbao_secrets_seed_path")
    if not isinstance(mount_expression, str) or not isinstance(path_expression, str):
        raise AssertionError("seed include is missing its mount or path expression")

    loop_var = include_task.get("loop_control", {}).get("loop_var", "item")
    items = (
        _loop_values(values, include_task["loop"])
        if "loop" in include_task
        else [None]
    )
    for item in items:
        context = dict(values)
        if item is not None:
            context[loop_var] = item
        if "openbao_seed_app" in include_vars:
            context["openbao_seed_app"] = _render_value(
                context, include_vars["openbao_seed_app"]
            )
        mount = _render_value(context, mount_expression)
        path = _render_value(context, path_expression)
        grants.setdefault(f"{mount}/data/{path}", set()).update(
            {"create", "read", "update"}
        )
        if is_roster_seed:
            for task in _task_file(ROSTER_SEED_TASKS):
                _add_kv_command(grants, task, context)
                _add_kv_uri(grants, task, context)
            for task in _task_file(ROSTER_OWNER_TASKS):
                _add_kv_uri(grants, task, context)
