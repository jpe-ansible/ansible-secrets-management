"""GitHub App mount credentials: first configuration and declared key rotation.

The real tasks of both callers run against a local endpoint that records every
config write, with the stored configuration supplied as a fixture.
"""

import json
import os
import shutil
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
INIT = ROOT / "roles/openbao/tasks/init"
DEFAULTS = ROOT / "roles/openbao/defaults/main/03-github-engine.yml"
SHARED = "github_app_config_write.yml"
ROTATE_VAR = "openbao_github_app_key_rotate_mounts"
MOUNT = "github-fixture"
TOKEN = "s.test"

# Per caller: its task file, the tasks between the config read and the write,
# and the variables that carry the stored configuration and the supplied App.
CALLERS = {
    "admin": {
        "file": INIT / "05-github-engine.yml",
        "tasks": [
            "Assert the GitHub engine configuration read succeeded",
            "Determine whether the GitHub App is actually configured",
            "Require the GitHub App credentials for first configuration",
            "Refuse an unexpected GitHub App ID drift",
            "Require the GitHub App private key for a declared key rotation",
            "Write the GitHub App credentials",
        ],
        "variables": lambda stored, app_id, key: {
            "openbao_github_engine_enabled": True,
            "openbao_github_mount": MOUNT,
            "openbao_github_config_check": stored,
            "openbao_github_app_id": app_id,
            "openbao_github_app_private_key": key,
        },
    },
    "per-app": {
        "file": INIT / "05b-github-app-mount.yml",
        "tasks": [
            "Assert the configuration read succeeded",
            "Determine whether the App is configured",
            "Refuse an unexpected App ID drift",
            "Require the private key for a declared key rotation",
            "Write the App credentials",
        ],
        "variables": lambda stored, app_id, key: {
            "openbao_github_app_mount_config": stored,
            # Set by the file's first task; false once the mount exists.
            "openbao_github_app_mount_absent_check_mode": False,
            "gm": {"mount": MOUNT, "app_id": app_id, "private_key": key, "permission_sets": []},
        },
    },
}


def _tasks(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _caller_tasks(caller):
    tasks = _tasks(CALLERS[caller]["file"])
    selected = []
    for prefix in CALLERS[caller]["tasks"]:
        task = dict(next(task for task in tasks if task.get("name", "").startswith(prefix)))
        if "ansible.builtin.include_tasks" in task:
            assert task["ansible.builtin.include_tasks"] == SHARED
            task["ansible.builtin.include_tasks"] = str(INIT / SHARED)
        selected.append(task)
    return selected


@pytest.fixture
def config_endpoint():
    writes = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            writes.append({
                "path": self.path,
                "token": self.headers.get("X-Vault-Token"),
                "body": json.loads(body),
            })
            self.send_response(204)
            self.end_headers()

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}", writes
    server.shutdown()
    server.server_close()


def _run(tmp_path, endpoint, caller, stored_app_id, app_id, key, rotate=None, config_rc=0):
    """Run one caller's tasks; `rotate` None leaves the role default in place."""
    address, writes = endpoint
    playbook = tmp_path / "configure.yml"
    playbook.write_text(yaml.safe_dump([{
        "name": "Verify GitHub App credential writes",
        "hosts": "localhost", "connection": "local", "gather_facts": False,
        "vars_files": [str(DEFAULTS)],
        "tasks": _caller_tasks(caller),
    }]))
    stored = {"rc": config_rc, "stdout": json.dumps({"data": {"app_id": stored_app_id}})}
    variables = {
        **CALLERS[caller]["variables"](stored, app_id, key),
        "openbao_bootstrap_token": TOKEN,
        "openbao_cli_addr": address,
        "openbao_cli_http_addr": address,
        "openbao_cli_unix_socket": "{{ omit }}",
        "openbao_cli_host": "localhost",
        "openbao_cli_become": False,
    }
    if rotate is not None:
        variables[ROTATE_VAR] = rotate
    result = subprocess.run(
        [shutil.which("ansible-playbook"), "-i", "localhost,", str(playbook),
         "-e", json.dumps(variables)],
        cwd=ROOT, env={**os.environ, "no_proxy": "127.0.0.1", "NO_PROXY": "127.0.0.1"},
        text=True, capture_output=True, timeout=120, check=False,
    )
    return result.returncode, result.stdout + result.stderr, writes


def _assert_one_write(writes, app_id, key):
    assert len(writes) == 1, writes
    assert writes[0]["path"] == f"/v1/{MOUNT}/config"
    assert writes[0]["token"] == TOKEN
    body = writes[0]["body"]
    assert set(body) == {"app_id", "prv_key", "exclude_repository_metadata"}
    assert body["app_id"] == str(app_id)
    assert body["prv_key"] == key
    assert body["exclude_repository_metadata"] is True


def test_rotate_list_defaults_to_empty():
    assert yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))[ROTATE_VAR] == []


@pytest.mark.parametrize("caller", CALLERS)
def test_listed_configured_mount_with_a_key_is_written(tmp_path, config_endpoint, caller):
    returncode, output, writes = _run(
        tmp_path, config_endpoint, caller, stored_app_id=42, app_id="42", key="NEW-KEY",
        rotate=[MOUNT],
    )
    assert returncode == 0, output
    _assert_one_write(writes, 42, "NEW-KEY")
    assert "NEW-KEY" not in output


@pytest.mark.parametrize("caller", CALLERS)
@pytest.mark.parametrize("rotate", [None, ["another-mount"]])
def test_unlisted_configured_mount_is_not_written(tmp_path, config_endpoint, caller, rotate):
    returncode, output, writes = _run(
        tmp_path, config_endpoint, caller, stored_app_id=42, app_id="42", key="NEW-KEY",
        rotate=rotate,
    )
    assert returncode == 0, output
    assert writes == []


@pytest.mark.parametrize("caller", CALLERS)
@pytest.mark.parametrize("app_id", ["43", ""])
def test_listed_mount_with_a_different_app_id_fails_the_drift_assert(
    tmp_path, config_endpoint, caller, app_id,
):
    returncode, output, writes = _run(
        tmp_path, config_endpoint, caller, stored_app_id=42, app_id=app_id, key="NEW-KEY",
        rotate=[MOUNT],
    )
    assert returncode != 0, output
    assert "App ID drift" in output and "differs" in output, output
    assert writes == []


@pytest.mark.parametrize("caller", CALLERS)
def test_listed_mount_with_an_empty_key_fails_with_the_message(tmp_path, config_endpoint, caller):
    returncode, output, writes = _run(
        tmp_path, config_endpoint, caller, stored_app_id=42, app_id="42", key="",
        rotate=[MOUNT],
    )
    assert returncode != 0, output
    assert f"{MOUNT} is listed in {ROTATE_VAR}" in output, output
    assert "no private key is supplied" in output, output
    assert writes == []


@pytest.mark.parametrize("caller", CALLERS)
@pytest.mark.parametrize("rotate", [None, [MOUNT]])
def test_unconfigured_mount_is_first_configured_through_the_shared_file(
    tmp_path, config_endpoint, caller, rotate,
):
    returncode, output, writes = _run(
        tmp_path, config_endpoint, caller, stored_app_id=0, app_id="42", key="FIRST-KEY",
        rotate=rotate,
    )
    assert returncode == 0, output
    assert f"{SHARED} for localhost" in output, output
    _assert_one_write(writes, 42, "FIRST-KEY")


@pytest.mark.parametrize("caller", CALLERS)
def test_failed_config_read_stops_before_writing(tmp_path, config_endpoint, caller):
    returncode, output, writes = _run(
        tmp_path, config_endpoint, caller, stored_app_id=0, app_id="42", key="FIRST-KEY",
        config_rc=2,
    )
    assert returncode != 0, output
    assert "config read failed" in output and "nothing was written" in output, output
    assert writes == []


@pytest.mark.parametrize("caller", CALLERS)
def test_private_key_asserts_are_hidden(caller):
    tasks = _tasks(CALLERS[caller]["file"])
    for task in tasks:
        assertion = task.get("ansible.builtin.assert", {})
        if "private_key" in str(assertion):
            assert task.get("no_log") is True, task["name"]


def test_shared_file_holds_the_only_config_write():
    holders = sorted(
        path.relative_to(INIT.parent).as_posix()
        for path in INIT.parent.rglob("*.yml")
        if "prv_key" in path.read_text(encoding="utf-8")
    )
    assert holders == [f"init/{SHARED}"]

    shared = _tasks(INIT / SHARED)
    assert len(shared) == 1
    write = shared[0]
    assert write["ansible.builtin.uri"]["url"] == (
        "{{ openbao_cli_http_addr }}/v1/{{ openbao_github_app_config_mount }}/config"
    )
    assert write["ansible.builtin.uri"]["unix_socket"] == "{{ openbao_cli_unix_socket }}"
    assert write["ansible.builtin.uri"]["method"] == "POST"
    assert write["ansible.builtin.uri"]["headers"] == {
        "X-Vault-Token": "{{ openbao_bootstrap_token }}",
    }
    assert write["no_log"] is True
    assert write["delegate_to"] == "{{ openbao_cli_host }}"
    assert write["become"] == "{{ openbao_cli_become }}"
    assert write["vars"] == {"ansible_become": "{{ openbao_cli_become }}"}


@pytest.mark.parametrize("caller", CALLERS)
def test_each_caller_reaches_the_config_write_only_through_the_shared_file(caller):
    tasks = _tasks(CALLERS[caller]["file"])
    includes = [task for task in tasks if task.get("ansible.builtin.include_tasks") == SHARED]
    assert len(includes) == 1
    assert set(includes[0]["vars"]) == {
        "openbao_github_app_config_mount",
        "openbao_github_app_config_app_id",
        "openbao_github_app_config_private_key",
    }
    assert includes[0]["no_log"] is True
    for task in tasks:
        url = (task.get("ansible.builtin.uri") or {}).get("url", "")
        assert not url.rstrip().endswith("/config"), task["name"]
