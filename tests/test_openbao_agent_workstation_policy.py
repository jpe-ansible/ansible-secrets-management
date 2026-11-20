"""The agent-workstation AppRole reads only its declared KV leaves."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest
import yaml

from _ports import loopback_port
from test_openbao_rbac_policy_render import render as render_policy_pairs

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main"
POLICY_NAME_VARIABLE = "{{ openbao_agent_workstation_policy_name }}"
ROLE_NAME_VARIABLE = "{{ openbao_agent_workstation_approle_name }}"
READS = (
    "secret/data/apps/nautobot",
    "secret/data/ai/mcp",
    "secret/data/ai/mcp/zammad",
    "secret/data/ai/mcp/vikunja",
    "secret/data/ai/youtrack",
    "secret/data/ai/dify/agent-apps/test-app",
    "secrets-external/data/slack/claude-reader/ro",
)
DENIED_READS = (
    "secret/data/ai/hermes",
    "secret/data/ai/hermes/embedding",
    "secret/data/ai/mcp/hermes",
    "secret/data/apps/sandbox-agent",
    "secret/data/apps/youtrack",
    "secrets-external/data/slack/claude-reader/rw",
    "secrets-external/metadata/slack/claude-reader/ro",
)
DENIED_WRITES = READS + (
    "secret/data/ai/hermes/embedding",
    "secret/data/apps/sandbox-agent",
)


def _yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _policy_details() -> tuple[str, str]:
    names = _yaml(DEFAULTS / "05c-terrakube-and-remaining-domain-names.yml")
    policy_name = names["openbao_agent_workstation_policy_name"]
    policy_rows = _yaml(DEFAULTS / "07c-base-policies.yml")[
        "openbao_base_policies_static"
    ]
    rows = [row for row in policy_rows if row["name"] == POLICY_NAME_VARIABLE]
    assert len(rows) == 1
    return policy_name, rows[0]["template"]


def _render_policy() -> tuple[str, str]:
    policy_name, template = _policy_details()
    pairs = render_policy_pairs([{"name": policy_name, "template": template}])
    assert len(pairs) == 1
    return policy_name, pairs[0]["value"]


def _call(base: str, token: str, method: str, path: str, body=None):
    request = urllib.request.Request(
        f"{base}/v1/{path}",
        data=None if body is None else json.dumps(body).encode(),
        method=method,
        headers={"X-Vault-Token": token},
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def test_agent_workstation_approle_attaches_only_its_dedicated_policy():
    policy_name, template = _policy_details()
    assert policy_name == "agent-workstation"
    assert template == "agent-workstation-policy.hcl.j2"

    role_rows = _yaml(DEFAULTS / "07f-elevated-approles.yml")[
        "openbao_base_approles_elevated"
    ]
    rows = [row for row in role_rows if row["name"] == ROLE_NAME_VARIABLE]
    assert len(rows) == 1
    assert rows[0]["policy"] == POLICY_NAME_VARIABLE
    assert "token_policies" not in rows[0]


def test_rendered_agent_workstation_policy_contains_only_its_exact_reads():
    _, policy = _render_policy()
    stanzas = re.findall(
        r'(?ms)^path "([^"]+)" \{\s*capabilities = (\[[^\]]+\])\s*\}',
        policy,
    )
    assert stanzas == [
        ("secret/data/apps/nautobot", '["read"]'),
        ("secret/data/ai/mcp", '["read"]'),
        ("secret/data/ai/mcp/zammad", '["read"]'),
        ("secret/data/ai/mcp/vikunja", '["read"]'),
        ("secret/data/ai/youtrack", '["read"]'),
        ("secret/data/ai/dify/agent-apps/*", '["read"]'),
        ("secrets-external/data/slack/claude-reader/ro", '["read"]'),
    ]


@pytest.fixture(scope="module")
def agent_workstation_token():
    binary = shutil.which("bao")
    assert binary, "the bao binary must be on PATH: this test runs a real OpenBao dev server"
    port = loopback_port()
    base = f"http://127.0.0.1:{port}"
    server = subprocess.Popen(
        [
            binary,
            "server",
            "-dev",
            "-dev-root-token-id=root",
            "-dev-no-store-token",
            f"-dev-listen-address=127.0.0.1:{port}",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(60):
            try:
                if _call(base, "root", "GET", "sys/health")[0] == 200:
                    break
            except OSError:
                pass
            time.sleep(0.5)
        else:
            pytest.fail("the bao dev server did not become healthy")

        status, body = _call(base, "root", "GET", "sys/mounts")
        assert status == 200
        mounts = json.loads(body)["data"]
        for mount in ("secret", "secrets-external"):
            mount_path = f"{mount}/"
            if mount_path not in mounts:
                status, _ = _call(
                    base,
                    "root",
                    "POST",
                    f"sys/mounts/{mount}",
                    {"type": "kv", "options": {"version": "2"}},
                )
                assert status == 204
            else:
                assert mounts[mount_path]["options"].get("version") == "2"

        status, body = _call(base, "root", "GET", "sys/auth")
        assert status == 200
        if "approle/" not in json.loads(body)["data"]:
            status, _ = _call(
                base, "root", "POST", "sys/auth/approle", {"type": "approle"}
            )
            assert status == 204

        policy_name, policy = _render_policy()
        status, _ = _call(
            base,
            "root",
            "PUT",
            f"sys/policies/acl/{policy_name}",
            {"policy": policy},
        )
        assert status == 204

        role_rows = _yaml(DEFAULTS / "07f-elevated-approles.yml")[
            "openbao_base_approles_elevated"
        ]
        role = next(row for row in role_rows if row["name"] == ROLE_NAME_VARIABLE)
        assert role["policy"] == POLICY_NAME_VARIABLE
        assert "token_policies" not in role
        role_name = _yaml(DEFAULTS / "05c-terrakube-and-remaining-domain-names.yml")[
            "openbao_agent_workstation_approle_name"
        ]
        status, _ = _call(
            base,
            "root",
            "POST",
            f"auth/approle/role/{role_name}",
            {
                "token_policies": policy_name,
                "token_ttl": "15m",
                "token_max_ttl": "15m",
            },
        )
        assert status == 204

        for path in READS + DENIED_READS:
            if "/metadata/" in path:
                continue
            status, _ = _call(
                base,
                "root",
                "POST",
                path,
                {"data": {"probe": "test-value"}},
            )
            assert status == 200

        status, body = _call(
            base,
            "root",
            "GET",
            f"auth/approle/role/{role_name}/role-id",
        )
        assert status == 200
        role_id = json.loads(body)["data"]["role_id"]
        status, body = _call(
            base,
            "root",
            "POST",
            f"auth/approle/role/{role_name}/secret-id",
            {},
        )
        assert status == 200
        secret_id = json.loads(body)["data"]["secret_id"]
        status, body = _call(
            base,
            "root",
            "POST",
            "auth/approle/login",
            {"role_id": role_id, "secret_id": secret_id},
        )
        assert status == 200
        auth = json.loads(body)["auth"]
        token = auth["client_token"]
        policies = set(auth["policies"])
        assert policy_name in policies
        assert policies <= {"default", policy_name}

        yield lambda method, path, body=None: _call(base, token, method, path, body)
    finally:
        server.terminate()
        server.wait(timeout=30)


@pytest.mark.parametrize("path", READS)
def test_direct_agent_workstation_token_can_read_its_declared_leaves(
    agent_workstation_token, path
):
    assert agent_workstation_token("GET", path)[0] == 200


@pytest.mark.parametrize("path", DENIED_READS)
def test_direct_agent_workstation_token_cannot_read_other_agent_or_app_leaves(
    agent_workstation_token, path
):
    assert agent_workstation_token("GET", path)[0] == 403


@pytest.mark.parametrize("path", DENIED_WRITES)
def test_direct_agent_workstation_token_cannot_write_kv_leaves(
    agent_workstation_token, path
):
    assert (
        agent_workstation_token("POST", path, {"data": {"probe": "denied"}})[0]
        == 403
    )
