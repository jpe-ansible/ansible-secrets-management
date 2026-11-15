"""Reconcile KV grants cover task paths and declared seed operations."""

from openbao_reconcile_bounds_helpers import (
    RECONCILE,
    _capabilities,
    _include_details,
    _loop_values,
    _named_task,
    _render,
    _render_value,
    _stanzas,
    _task_file,
    rendered_defaults,
)
from openbao_reconcile_kv_task_helpers import (
    LEGACY_AGENT_TASKS,
    ROTATION_TASKS,
    TASKS_03,
    TASKS_03B,
    TASKS_08A,
    _add_kv_command,
    _add_kv_uri,
    _add_promoted_paths,
    _add_seeded_paths,
)

def test_reconcile_kv_task_paths_have_exact_grants(rendered_defaults):
    values, _approles, _policies = rendered_defaults
    context = dict(
        values,
        tofu_data={"agents": {"review-agent": {}}},
        agent_callers_registry={"review-caller": {}},
    )
    tasks = _task_file(TASKS_03)
    grants = {}

    # The tuned-config read and write use the same mount loop in init/03b.
    config_read = _named_task(
        TASKS_03B, "Read the current version-retention config of each tuned KV mount"
    )
    config_write = _named_task(
        TASKS_03B, "Set KV v2 version retention on the tuned mounts (write-if-changed)"
    )
    for mount in _loop_values(context, config_read["loop"]):
        _add_kv_command(grants, config_read, dict(context, item=mount))
        _add_kv_command(grants, config_write, dict(context, item=(mount, {})))

    # Promotion and generate-if-absent paths come from the concrete task
    # includes and the target mount/path passed to the shared seed role.
    for task in tasks:
        if _include_details(task) is None:
            continue
        _add_promoted_paths(grants, context, task)
        _add_seeded_paths(grants, context, task)

    # The live roster collision probe reads all three candidate metadata paths
    # for each valid roster name, including the legacy ai/<agent> leaf.
    metadata_read = _named_task(
        TASKS_08A, "Read live metadata for roster agent KV paths"
    )
    for item in _loop_values(context, metadata_read["loop"]):
        _add_kv_command(grants, metadata_read, dict(context, item=item))

    readers = _render_value(context, context["openbao_app_agent_tier_readers"])
    for reader in readers:
        reader_context = dict(context, openbao_agent_tier_reader=reader)
        for task in _task_file(LEGACY_AGENT_TASKS):
            if (
                "login_path is defined" in str(task.get("when", ""))
                and "login_path" not in reader
            ):
                continue
            _add_kv_uri(grants, task, reader_context)

    rotation_exempt = _render_value(context, context["openbao_rotation_exempt"])
    for entry in rotation_exempt:
        mount, path = entry.split(":", 1)
        rotation_context = dict(
            context,
            openbao_rotation_exempt_entry=entry,
            openbao_rotation_exempt_mount=mount,
            openbao_rotation_exempt_path=path,
            openbao_rotation_exempt_metadata_path=f"{mount}/metadata/{path}",
        )
        for task in _task_file(ROTATION_TASKS):
            _add_kv_command(grants, task, rotation_context)

    rendered = _render(RECONCILE, context)
    stanzas = dict(_stanzas(rendered))
    for path, capabilities in grants.items():
        assert path in stanzas, f"no exact reconcile stanza covers task KV path {path}"
        assert "*" not in path and "+" not in path, path
        assert capabilities <= set(_capabilities(stanzas[path])), (path, capabilities)
