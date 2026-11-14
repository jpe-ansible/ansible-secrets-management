"""Render and exercise per-identity policies from a secrets arrangement."""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest
from ansible.errors import AnsibleError

from _ports import loopback_port
from openbao_reconcile_bounds_helpers import (
    TEMPLATES,
    _capabilities,
    _render,
    _stanzas,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "secrets_arrangement.json"
TEMPLATE = TEMPLATES / "arrangement-policy.hcl.j2"


def _arrangement() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _render_identity(arrangement: dict, name: str) -> str:
    return _render(
        TEMPLATE,
        {
            "ansible_managed": "Ansible managed",
            "item": {"name": name, "arrangement": arrangement},
        },
    )


def _policy_map(rendered: str) -> dict[str, list[str]]:
    return {path: _capabilities(body) for path, body in _stanzas(rendered)}


def test_every_identity_renders_the_exact_path_set():
    arrangement = _arrangement()
    expected = {
        "example-everyday": {
            "example-zone/data/+/+/ro",
            "config/data/+/+",
            "config/metadata/+/+",
            "admin/*",
            "example-held/*",
        },
        "example-service": {
            "example-zone/data/example-svc/example-instance/self",
            "config/data/example-svc/example-instance",
            "example-engine/token/example-set",
            "admin/*",
            "example-held/*",
        },
        "example-sandbox": {
            "example-ext/data/example-vendor/main/ro",
            "admin/*",
            "example-held/*",
        },
        "example-automation": {
            "example-zone/data/example-svc/+/rw",
            "admin/data/example-zone/example-svc/example-instance/management",
            "state/example-flow/*",
        },
        "example-sudo": {"admin/data/example-ext/example-vendor/main/owner"},
        "example-restricted": {"example-held/data/example-tracker/main/rw"},
        "example-operator": {
            "+/data/+/+/+",
            "+/metadata/+/+/+",
            "admin/data/+/+/+/+",
            "admin/metadata/+/+/+/+",
            "sys/generate-root/*",
        },
    }

    assert set(expected) == set(arrangement["identities"])
    for name in arrangement["identities"]:
        assert set(_policy_map(_render_identity(arrangement, name))) == expected[name]

    everyday = _policy_map(_render_identity(arrangement, "example-everyday"))
    assert everyday["example-zone/data/+/+/ro"] == ["read"]
    assert everyday["config/data/+/+"] == ["read"]
    assert everyday["config/metadata/+/+"] == ["list", "read"]

    automation = _policy_map(_render_identity(arrangement, "example-automation"))
    assert automation["example-zone/data/example-svc/+/rw"] == [
        "read",
        "create",
        "update",
        "patch",
    ]
    assert automation["state/example-flow/*"] == ["read", "create", "update"]


@pytest.mark.parametrize(
    "name", ["example-everyday", "example-service", "example-sandbox"]
)
def test_unprivileged_policies_deny_admin_and_restricted_zones(name: str):
    policy = _policy_map(_render_identity(_arrangement(), name))
    assert policy["admin/*"] == ["deny"]
    assert policy["example-held/*"] == ["deny"]


def test_operator_has_no_class_guard_denies():
    policy = _policy_map(_render_identity(_arrangement(), "example-operator"))
    assert "admin/*" not in policy
    assert "example-held/*" not in policy
    assert policy["sys/generate-root/*"] == ["deny"]


@pytest.mark.parametrize("grant_key", ["grants", "raw_grants"])
def test_rejects_grant_for_unknown_identity(grant_key: str):
    arrangement = _arrangement()
    grant = copy.deepcopy(arrangement[grant_key][0])
    grant["identity"] = "missing-identity"
    arrangement[grant_key].append(grant)

    with pytest.raises(AnsibleError, match="unknown identity"):
        _render_identity(arrangement, "example-everyday")


@pytest.mark.parametrize(
    ("grant_key", "path"),
    [
        ("grants", "+/example-svc/example-instance/ro"),
        ("raw_grants", "+engine/token/example-set"),
    ],
)
def test_rejects_nonoperator_grants_starting_with_plus(grant_key: str, path: str):
    arrangement = _arrangement()
    grant = copy.deepcopy(arrangement[grant_key][0])
    grant.update(identity="example-everyday", path=path)
    if grant_key == "grants":
        grant.pop("capabilities", None)
    else:
        grant["capabilities"] = ["read"]
    arrangement[grant_key].append(grant)

    with pytest.raises(AnsibleError, match="only operator identities"):
        _render_identity(arrangement, "example-everyday")


@pytest.mark.parametrize(
    ("identity", "path"),
    [
        (
            "example-everyday",
            "admin/example-zone/example-svc/example-instance/management",
        ),
        ("example-everyday", "example-held/example-tracker/main/rw"),
        (
            "example-service",
            "admin/example-zone/example-svc/example-instance/management",
        ),
        ("example-service", "example-held/example-tracker/main/rw"),
        (
            "example-sandbox",
            "admin/example-zone/example-svc/example-instance/management",
        ),
        ("example-sandbox", "example-held/example-tracker/main/rw"),
    ],
)
def test_rejects_unprivileged_admin_or_restricted_zone_grants(identity: str, path: str):
    arrangement = _arrangement()
    arrangement["grants"].append({"identity": identity, "path": path})

    with pytest.raises(
        AnsibleError, match="forbidden admin/restricted-zone grant"
    ):
        _render_identity(arrangement, identity)


def test_rejects_nonoperator_admin_grant_with_zone_wildcard():
    arrangement = _arrangement()
    arrangement["grants"].append(
        {"identity": "example-sudo", "path": "admin/+/example-vendor/main/owner"}
    )

    with pytest.raises(AnsibleError, match="only operator identities"):
        _render_identity(arrangement, "example-sudo")


def test_rejects_raw_grant_into_a_declared_zone():
    arrangement = _arrangement()
    arrangement["raw_grants"].append(
        {
            "identity": "example-automation",
            "path": "example-held/data/example-tracker/main/rw",
            "capabilities": ["read"],
        }
    )

    with pytest.raises(AnsibleError, match="raw grant targets a declared zone"):
        _render_identity(arrangement, "example-automation")


def test_rejects_zone_leaf_grant_for_undeclared_zone():
    arrangement = _arrangement()
    arrangement["grants"].append(
        {
            "identity": "example-operator",
            "path": "missing-zone/example-svc/example-instance/ro",
        }
    )

    with pytest.raises(AnsibleError, match="undeclared zone"):
        _render_identity(arrangement, "example-operator")


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


@pytest.fixture(scope="module")
def arrangement_capabilities():
    binary = shutil.which("bao")
    if not binary:
        pytest.skip(
            "bao is not on PATH; live policy capability checks require a bao dev server"
        )

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
        assert status == 200, body
        mounts = json.loads(body)["data"]
        for mount in ("example-zone", "example-ext", "example-held", "admin", "config"):
            mount_path = f"{mount}/"
            if mount_path not in mounts:
                status, body = _call(
                    base,
                    "root",
                    "POST",
                    f"sys/mounts/{mount}",
                    {"type": "kv", "options": {"version": "2"}},
                )
                assert status == 204, body
            else:
                assert mounts[mount_path]["options"].get("version") == "2"

        arrangement = _arrangement()
        # Only this live copy adds config, which the byte-identical fixture lacks.
        arrangement["grants"].append(
            {
                "identity": "example-operator",
                "path": "config/example-svc/example-instance",
                "capabilities": ["read", "create", "update", "delete"],
            }
        )
        policies = {}
        tokens = {}
        for identity in arrangement["identities"]:
            policy_name = f"arrangement-{identity}"
            rendered = _render_identity(arrangement, identity)
            status, body = _call(
                base,
                "root",
                "PUT",
                f"sys/policies/acl/{policy_name}",
                {"policy": rendered},
            )
            assert status == 204, body
            policies[identity] = rendered

            status, body = _call(
                base,
                "root",
                "POST",
                "auth/token/create",
                {"policies": [policy_name], "no_default_policy": True, "ttl": "15m"},
            )
            assert status == 200, body
            tokens[identity] = json.loads(body)["auth"]["client_token"]

        yield lambda identity, paths: _call(
            base,
            "root",
            "POST",
            "sys/capabilities",
            {"token": tokens[identity], "paths": paths},
        )
    finally:
        server.terminate()
        server.wait(timeout=30)


def _capabilities_for(
    arrangement_capabilities, identity: str, paths: list[str]
) -> dict[str, list[str]]:
    status, body = arrangement_capabilities(identity, paths)
    assert status == 200, body
    return json.loads(body)["data"]


def test_live_everyday_and_restricted_capabilities(arrangement_capabilities):
    everyday_paths = [
        "admin/data/example-zone/example-svc/example-instance/management",
        "example-held/data/example-tracker/main/rw",
        "example-zone/data/example-svc/example-instance/ro",
    ]
    everyday = _capabilities_for(
        arrangement_capabilities, "example-everyday", everyday_paths
    )
    assert everyday[everyday_paths[0]] == ["deny"]
    assert everyday[everyday_paths[1]] == ["deny"]
    assert everyday[everyday_paths[2]] == ["read"]

    restricted_path = "example-held/data/example-tracker/main/rw"
    restricted = _capabilities_for(
        arrangement_capabilities, "example-restricted", [restricted_path]
    )
    assert restricted[restricted_path] == ["read"]


def test_live_operator_capabilities_cover_each_kv2_mount(arrangement_capabilities):
    paths = [
        "example-zone/data/example-svc/example-instance/rw",
        "example-ext/data/example-vendor/main/ro",
        "example-held/data/example-tracker/main/rw",
        "admin/data/example-zone/example-svc/example-instance/management",
        "config/data/example-svc/example-instance",
    ]
    operator = _capabilities_for(arrangement_capabilities, "example-operator", paths)
    required = {"create", "read", "update", "delete"}
    for path in paths:
        assert required <= set(operator[path])

    root_attempt = "sys/generate-root/attempt"
    root_capability = _capabilities_for(
        arrangement_capabilities, "example-operator", [root_attempt]
    )
    assert root_capability[root_attempt] == ["deny"]
