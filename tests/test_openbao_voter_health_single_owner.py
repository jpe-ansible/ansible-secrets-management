"""Guard single ownership and safe retirement of the voter-health sampler."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment

_ROOT = Path(__file__).resolve().parents[1]
_OPENBAO = _ROOT / "roles/openbao"
_ROLE = _ROOT / "roles/openbao_voter_health"
_TASKS_FILE = _ROLE / "tasks/main.yml"
_DEFAULTS_FILE = _ROLE / "defaults/main.yml"
_RETIRED_LIVE_PATH_TOKENS = (
    "openbao_voter_health_env_file",
    "openbao_voter_health_script_path",
    "openbao_voter_health_service_name",
    "/etc/openbao/openbao-voter-health.env",
    "/usr/local/sbin/openbao-voter-health.sh",
    "/etc/systemd/system/openbao-voter-health.service",
    "/etc/systemd/system/openbao-voter-health.timer",
)


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _tasks() -> list[dict[str, Any]]:
    return _load_yaml(_TASKS_FILE)


def _walk_nodes(node: Any):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _walk_nodes(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk_nodes(value)


def test_openbao_role_no_longer_names_or_deploys_voter_health_files() -> None:
    for directory in ("tasks", "templates", "handlers"):
        for path in (_OPENBAO / directory).rglob("*"):
            if path.is_file():
                assert "openbao-voter-health" not in path.name, path
                assert "openbao-voter-health" not in path.read_text(encoding="utf-8"), path


def test_openbao_role_no_longer_defines_or_reads_voter_health_variables() -> None:
    for directory in ("defaults", "tasks", "templates", "handlers"):
        for path in (_OPENBAO / directory).rglob("*"):
            if path.is_file():
                assert "openbao_voter_health_" not in path.read_text(encoding="utf-8"), path


def test_voter_health_role_keeps_deploying_and_starting_its_files() -> None:
    tasks = _tasks()
    template_tasks = {
        task["ansible.builtin.template"]["src"]: task
        for task in tasks
        if "ansible.builtin.template" in task
    }
    for source in (
        "openbao-voter-health.env.j2",
        "openbao-voter-health.sh.j2",
        "openbao-voter-health.service.j2",
        "openbao-voter-health.timer.j2",
    ):
        assert source in template_tasks
        assert template_tasks[source]["when"] == "openbao_voter_health_enabled | bool"

    token_guard = next(
        task
        for task in tasks
        if task.get("name")
        == "Refuse to render the voter-health EnvironmentFile without a HEC token"
    )
    assert token_guard["when"] == "openbao_voter_health_enabled | bool"

    timer_task = next(
        task
        for task in tasks
        if task.get("name") == "Enable and start the OpenBao voter-health timer"
    )
    assert timer_task["ansible.builtin.systemd"]["state"] == "started"
    assert timer_task["ansible.builtin.systemd"]["enabled"] is True
    assert timer_task["when"] == [
        "openbao_voter_health_enabled | bool",
        "ansible_virtualization_type | default('') != 'docker'",
    ]


def test_no_repository_file_task_removes_a_live_voter_health_file() -> None:
    yaml_roots = (_ROOT / "roles", _ROOT / "playbooks", _ROOT / "molecule", _ROOT / "tests")
    for root in yaml_roots:
        for path in (*root.rglob("*.yml"), *root.rglob("*.yaml")):
            for node in _walk_nodes(_load_yaml(path)):
                for module in ("ansible.builtin.file", "file"):
                    action = node.get(module)
                    if not isinstance(action, dict) or action.get("state") != "absent":
                        continue
                    target = str(action.get("path", action.get("dest", "")))
                    assert not any(token in target for token in _RETIRED_LIVE_PATH_TOKENS), (
                        f"{path}: file task removes live voter-health path {target!r}"
                    )


def test_retired_path_is_distinct_and_guarded_before_cleanup() -> None:
    defaults = _load_yaml(_DEFAULTS_FILE)
    assert defaults["openbao_voter_health_retired_script_path"] == (
        "/usr/local/bin/openbao-voter-health.sh"
    )
    assert defaults["openbao_voter_health_script_path"] == (
        "/usr/local/sbin/openbao-voter-health.sh"
    )

    tasks = _tasks()
    guard_index = next(
        index
        for index, task in enumerate(tasks)
        if task.get("name")
        == "Assert the retired voter-health script path differs from the live path"
    )
    cleanup_index = next(
        index
        for index, task in enumerate(tasks)
        if task.get("name") == "Remove the retired OpenBao voter-health sampling script"
    )
    assert guard_index < cleanup_index

    guard = tasks[guard_index]
    condition = guard["ansible.builtin.assert"]["that"][0]
    assert guard["when"] == "openbao_voter_health_enabled | bool"
    renderer = Environment()
    condition_template = renderer.from_string("{{ " + condition + " }}")
    rendered_paths = {
        name: renderer.from_string(defaults[name]).render(defaults)
        for name in (
            "openbao_voter_health_retired_script_path",
            "openbao_voter_health_script_path",
        )
    }
    assert condition_template.render(rendered_paths) == "True"
    equal_paths = {
        **rendered_paths,
        "openbao_voter_health_retired_script_path": rendered_paths[
            "openbao_voter_health_script_path"
        ],
    }
    assert condition_template.render(equal_paths) == "False"

    cleanup = tasks[cleanup_index]
    rendered_live_path = rendered_paths["openbao_voter_health_script_path"]
    rendered_cleanup_path = renderer.from_string(
        cleanup["ansible.builtin.file"]["path"]
    ).render(defaults)
    assert rendered_cleanup_path == "/usr/local/bin/openbao-voter-health.sh"
    assert rendered_live_path == "/usr/local/sbin/openbao-voter-health.sh"
    assert rendered_cleanup_path != rendered_live_path
    assert cleanup["ansible.builtin.file"]["state"] == "absent"
    assert cleanup["when"] == "openbao_voter_health_enabled | bool"
