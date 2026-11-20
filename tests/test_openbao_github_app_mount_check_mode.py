"""GitHub App mount JSON reads and token cleanup run during check mode."""

import re
from pathlib import Path

import yaml


TASKS = (
    Path(__file__).resolve().parents[1]
    / "roles"
    / "openbao"
    / "tasks"
    / "init"
    / "05b-github-app-mount.yml"
)
TASK_SECTIONS = ("block", "rescue", "always")


def _walk_tasks(node):
    if isinstance(node, list):
        for item in node:
            yield from _walk_tasks(item)
    elif isinstance(node, dict):
        if "name" in node:
            yield node
        for key in TASK_SECTIONS:
            if key in node:
                yield from _walk_tasks(node[key])


def _expanded_tasks(path):
    for task in _walk_tasks(yaml.safe_load(path.read_text(encoding="utf-8"))):
        yield path, task
        included = task.get("ansible.builtin.include_tasks")
        if isinstance(included, str) and "{{" not in included:
            yield from _expanded_tasks(path.parent / included)


def _strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, list):
        for item in node:
            yield from _strings(item)
    elif isinstance(node, dict):
        for key, value in node.items():
            if key not in TASK_SECTIONS:
                yield from _strings(value)


def _uses_json(task, registered):
    strings = list(_strings(task))
    result = re.escape(registered)
    direct_json = re.compile(rf"\b{result}\s*\.\s*json\b")
    results = re.compile(rf"\b{result}\s*\.\s*results\b")
    if any(
        direct_json.search(value)
        or (results.search(value) and re.search(r"\.\s*json\b", value))
        for value in strings
    ):
        return True

    loop_var = re.escape(task.get("loop_control", {}).get("loop_var", "item"))
    item_json = re.compile(rf"\b{loop_var}\s*\.\s*json\b")
    return bool(results.search(task.get("loop", ""))) and any(
        item_json.search(value) for value in strings
    )


def test_uri_json_results_are_available_in_check_mode():
    # Repository-list results are consumed by a later static task include.
    tasks = list(_expanded_tasks(TASKS))
    producers = [
        task
        for index, (path, task) in enumerate(tasks)
        if path == TASKS
        and "ansible.builtin.uri" in task
        and "register" in task
        and any(_uses_json(later, task["register"]) for _, later in tasks[index + 1 :])
    ]

    assert {task["register"] for task in producers} >= {
        "openbao_github_app_mount_public_tokens",
        "openbao_github_app_mount_public_repos",
        "openbao_github_app_mount_private_tokens",
        "openbao_github_app_mount_private_repos",
        "openbao_github_app_mount_grant",
    }
    assert [task["name"] for task in producers if task.get("check_mode") is not False] == []


def test_token_mints_always_revoke_in_check_mode():
    tasks = list(_walk_tasks(yaml.safe_load(TASKS.read_text(encoding="utf-8"))))
    mints = [
        task
        for task in tasks
        if task.get("ansible.builtin.uri", {}).get("method") == "POST"
        and task["ansible.builtin.uri"].get("url", "").endswith("/token")
    ]

    assert {mint["register"] for mint in mints} == {
        "openbao_github_app_mount_public_tokens",
        "openbao_github_app_mount_private_tokens",
        "openbao_github_app_mount_grant",
    }
    for mint in mints:
        assert mint.get("check_mode") is False, f"{mint['name']} skips in check mode"
        enclosing_blocks = [
            task
            for task in tasks
            if any(child is mint for child in _walk_tasks(task.get("block", [])))
        ]
        revokes = [
            task
            for block in enclosing_blocks
            for task in _walk_tasks(block.get("always", []))
            if task.get("ansible.builtin.uri", {}).get("method") == "PUT"
            and task["ansible.builtin.uri"].get("url", "").endswith("/sys/leases/revoke")
            and _uses_json(task, mint["register"])
        ]

        assert revokes, f"{mint['name']} must revoke its token in always"
        assert [task["name"] for task in revokes if task.get("check_mode") is not False] == []
