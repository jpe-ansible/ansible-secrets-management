"""Bootstrap-token calls in the OpenBao init tasks run on the CLI host.

Scans every task file under roles/openbao/tasks/init/ and every file those
files include or import. Each task is judged on the environment, delegation,
become and vars Ansible applies to it, so a task that inherits them from an
enclosing block is judged the same as one that sets them itself.

A call carries the bootstrap token when its environment sets BAO_TOKEN or its
headers set X-Vault-Token, to openbao_bootstrap_token. Such a call must address
openbao_cli_addr and run on openbao_cli_host with openbao_cli_become. No task
may set BAO_ADDR to openbao_write_addr.
"""

from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
INIT = ROOT / "roles" / "openbao" / "tasks" / "init"

TOKEN = "openbao_bootstrap_token"
WRITE_ADDR = "{{ openbao_write_addr }}"
API_ADDR = "{{ openbao_api_addr }}"
CLI_ADDR = "{{ openbao_cli_addr }}"
CLI_HTTP_ADDR = "{{ openbao_cli_http_addr }}"  # the same address, in the form uri can open
CLI_HOST = "{{ openbao_cli_host }}"
CLI_BECOME = "{{ openbao_cli_become }}"

COMMAND_MODULES = ("ansible.builtin.command", "ansible.builtin.shell")
URI = "ansible.builtin.uri"
INCLUDE_KEYS = (
    "ansible.builtin.include_tasks",
    "ansible.builtin.import_tasks",
    "include_tasks",
    "import_tasks",
)
BLOCK_KEYS = ("block", "rescue", "always")
# The admin-window proxy reads take their whole environment from one role default.
PROXY_ENV_REF = "{{ openbao_window_proxy_env }}"
PROXY_ENV = yaml.safe_load(
    (ROOT / "roles" / "openbao" / "defaults" / "main" / "00-install-and-node.yml").read_text(encoding="utf-8")
)["openbao_window_proxy_env"]


def _environment(task):
    environment = task.get("environment") or {}
    if environment == PROXY_ENV_REF:
        return PROXY_ENV
    assert isinstance(environment, dict), f"unresolvable environment on {task.get('name')}: {environment}"
    return environment


def _tasks(nodes):
    """Every task mapping in a parsed task list, descending into blocks."""
    for task in nodes or []:
        if isinstance(task, dict):
            yield task
            for key in BLOCK_KEYS:
                yield from _tasks(task.get(key))


def _effective(nodes, inherited=None):
    """(task, scope) for each leaf task. scope holds the environment, delegate_to,
    become and vars that apply to it, with block-level keys inherited."""
    inherited = inherited or {}
    for task in nodes or []:
        if not isinstance(task, dict):
            continue
        scope = {
            "env": {**inherited.get("env", {}), **_environment(task)},
            "delegate_to": task.get("delegate_to", inherited.get("delegate_to")),
            "become": task.get("become", inherited.get("become")),
            "vars": {**inherited.get("vars", {}), **(task.get("vars") or {})},
        }
        if any(key in task for key in BLOCK_KEYS):
            for key in BLOCK_KEYS:
                yield from _effective(task.get(key), scope)
        else:
            yield task, scope


def _included(path):
    for task in _tasks(yaml.safe_load(path.read_text(encoding="utf-8"))):
        for key in INCLUDE_KEYS:
            if key in task:
                target = task[key]
                name = target["file"] if isinstance(target, dict) else target
                if "{{" in name:
                    raise AssertionError(f"{path.name}: templated include {name!r} cannot be resolved")
                local = path.parent / name
                # Ansible falls back to the role's tasks directory for a nested import.
                yield (local if local.is_file() else INIT.parent / name).resolve()


def _scanned_files():
    """init/*.yml plus everything they include, transitively."""
    pending = sorted(INIT.glob("*.yml"))
    seen = set()
    while pending:
        path = pending.pop()
        if path not in seen:
            seen.add(path)
            pending.extend(_included(path))
    return sorted(seen)


def _leaves():
    for path in _scanned_files():
        for task, scope in _effective(yaml.safe_load(path.read_text(encoding="utf-8"))):
            yield f"{path.relative_to(ROOT)}: {task.get('name')}", task, scope


def _sender(task, scope):
    """'command' or 'uri' when the call carries the bootstrap token, else None."""
    if any(module in task for module in COMMAND_MODULES):
        if TOKEN in str(scope["env"].get("BAO_TOKEN", "")):
            return "command"
    headers = (task.get(URI) or {}).get("headers") or {}
    if TOKEN in str(headers.get("X-Vault-Token", "")):
        return "uri"
    return None


def _address(task, scope, kind):
    if kind == "command":
        return str(scope["env"].get("BAO_ADDR", ""))
    return str(task[URI].get("url", ""))


class BootstrapTokenCallsRunOnTheCliHost(unittest.TestCase):
    def test_no_task_sets_bao_addr_to_the_write_address(self):
        offenders = [label for label, _, scope in _leaves() if scope["env"].get("BAO_ADDR") == WRITE_ADDR]
        self.assertEqual(offenders, [])

    def test_no_bootstrap_token_call_targets_a_node_local_address(self):
        offenders = []
        for label, task, scope in _leaves():
            kind = _sender(task, scope)
            if kind and _address(task, scope, kind).startswith((WRITE_ADDR, API_ADDR)):
                offenders.append(label)
        self.assertEqual(offenders, [])

    def test_every_bootstrap_token_call_carries_the_cli_switch(self):
        broken = []
        for label, task, scope in _leaves():
            kind = _sender(task, scope)
            if not kind:
                continue
            address = _address(task, scope, kind)
            address_ok = address == CLI_ADDR if kind == "command" else address.startswith((CLI_ADDR + "/", CLI_HTTP_ADDR + "/"))
            switch_ok = (
                scope["delegate_to"] == CLI_HOST
                and scope["become"] == CLI_BECOME
                and scope["vars"].get("ansible_become") == CLI_BECOME
            )
            if not (address_ok and switch_ok):
                broken.append(label)
        self.assertEqual(broken, [])

    def test_the_scan_reaches_included_files_and_finds_token_calls(self):
        self.assertIn(ROOT / "roles" / "openbao" / "tasks" / "seed_context7_key.yml", _scanned_files())
        self.assertTrue(any(_sender(task, scope) for _, task, scope in _leaves()))


if __name__ == "__main__":
    unittest.main()
