"""Zone KV mounts, their broad-grant flags, and restricted mounts from the run environment."""

import json
import re

import yaml

from openbao_reconcile_bounds_helpers import (
    TEMPLATES,
    _capabilities,
    _render,
    _render_value,
    _stanzas,
    rendered_defaults,  # noqa: F401 - pytest fixture
)
from test_openbao_select import ROLE, condition


HIERARCHY_DEFAULTS = ROLE / "defaults/main/01a-kv-hierarchy.yml"
MOUNT_TASKS = ROLE / "tasks/init/03b-kv-mounts.yml"
RESTRICTED = "example-restricted"
FULL = ["create", "read", "update", "delete", "list", "patch"]


def _mounts(values):
    return _render_value(values, values["openbao_kv_mounts"])


def _set_restricted(monkeypatch):
    # The environment asks for broad grants; the role must force both flags off.
    monkeypatch.setenv(
        "OPENBAO_KV_RESTRICTED_MOUNTS",
        json.dumps([{"path": RESTRICTED, "global_read": True, "age_audit": True}]),
    )


def test_zone_mounts_declare_the_grammar_zones_and_their_flags():
    zone = yaml.safe_load(HIERARCHY_DEFAULTS.read_text(encoding="utf-8"))[
        "openbao_kv_zone_mounts"
    ]
    flags = {
        entry["path"]: {
            key: value for key, value in entry.items()
            if key in ("global_read", "age_audit")
        }
        for entry in zone
    }
    assert flags == {
        "{{ openbao_kv_mount }}": {},
        "secrets-external": {},
        "{{ openbao_config_mount }}": {"age_audit": False},
        "ext-notify": {},
        "int": {},
        "ext-saas": {},
        "ext-ai": {"global_read": False},
        "ext-critical": {"global_read": False},
        "admin": {"global_read": False, "age_audit": False},
        "state": {"age_audit": False},
    }


def test_restricted_mounts_come_from_the_environment_with_both_flags_forced_off(
    rendered_defaults, monkeypatch,  # noqa: F811 - pytest fixture
):
    values, _, _ = rendered_defaults
    monkeypatch.delenv("OPENBAO_KV_RESTRICTED_MOUNTS", raising=False)
    without = _mounts(values)
    _set_restricted(monkeypatch)
    with_restricted = _mounts(values)

    assert RESTRICTED not in [mount["path"] for mount in without]
    assert with_restricted[:-1] == without
    assert with_restricted[-1] == {
        "path": RESTRICTED, "global_read": False, "age_audit": False,
    }


def test_broad_grants_skip_flagged_and_restricted_mounts(
    rendered_defaults, monkeypatch,  # noqa: F811 - pytest fixture
):
    values, _, _ = rendered_defaults
    _set_restricted(monkeypatch)
    paths = [mount["path"] for mount in _mounts(values)]

    read_all = dict(_stanzas(_render(TEMPLATES / "ai-global-read-policy.hcl.j2", values)))
    read_mounts = {path for path in paths if f"{path}/data/*" in read_all}
    assert read_mounts == set(paths) - {"ext-ai", "ext-critical", "admin", RESTRICTED}

    age_policy = dict(_stanzas(_render(TEMPLATES / "secret-age-audit-policy.hcl.j2", values)))
    age_mounts = {path for path in paths if f"{path}/metadata/*" in age_policy}
    assert age_mounts == set(paths) - {"config", "admin", "state", RESTRICTED}

    script = (TEMPLATES / "openbao-secret-age.sh.j2").read_text(encoding="utf-8")
    expression = re.search(r'^KV_MOUNTS="(.*)"$', script, re.MULTILINE).group(1)
    assert set(_render_value(values, expression).split()) == age_mounts


def test_ai_admin_reaches_every_mount_including_restricted_ones(
    rendered_defaults, monkeypatch,  # noqa: F811 - pytest fixture
):
    values, _, _ = rendered_defaults
    _set_restricted(monkeypatch)
    stanzas = dict(_stanzas(_render(TEMPLATES / "ai-admin-policy.hcl.j2", values)))
    for path in [mount["path"] for mount in _mounts(values)]:
        assert _capabilities(stanzas[f"{path}/*"]) == FULL, path
    assert f"{RESTRICTED}/*" in stanzas and "admin/*" in stanzas


def test_mount_assert_refuses_a_restricted_path_that_is_not_one_lowercase_segment():
    tasks = yaml.safe_load(MOUNT_TASKS.read_text(encoding="utf-8"))
    checks = next(
        item for item in tasks
        if item.get("name") == "Assert the declared KV mounts are distinct and outside the control plane"
    )["ansible.builtin.assert"]["that"]
    shape = next(check for check in checks if "reject('match'" in check)

    def accepts(*paths):
        return condition(shape, {"openbao_kv_mounts": [{"path": path} for path in paths]})

    assert accepts("int", "ext-saas", RESTRICTED)
    for bad in ("Restricted", "restricted/zone", "-restricted", "restricted zone", ""):
        assert not accepts("int", bad), bad
