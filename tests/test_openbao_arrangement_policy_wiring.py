"""Arrangement identities join the declared policy set under a name prefix."""

import json
from pathlib import Path

import yaml

from openbao_reconcile_bounds_helpers import (  # noqa: F401
    RECONCILE,
    _render,
    _render_value,
    _writable_policy_names,
    rendered_defaults,
)
from test_openbao_rbac_policy_render import render

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = Path(__file__).parent / "fixtures" / "secrets_arrangement.json"
COMPOSITION = ROOT / "roles/openbao/defaults/main/07c-policy-composition.yml"


def _declared_policies(values, arrangement):
    raw = yaml.safe_load(COMPOSITION.read_text(encoding="utf-8"))["openbao_policies"]
    return _render_value(values, raw, openbao_arrangement=arrangement)


def test_empty_arrangement_adds_no_policies(rendered_defaults):
    _, _, policies = rendered_defaults
    assert not [p for p in policies if p["name"].startswith("arrangement-")]


def test_each_arrangement_identity_is_declared_and_renders(rendered_defaults):
    values, _, _ = rendered_defaults
    arrangement = json.loads(FIXTURE.read_text(encoding="utf-8"))

    declared = [
        p for p in _declared_policies(values, arrangement)
        if p["name"].startswith("arrangement-")
    ]
    assert sorted(p["name"] for p in declared) == sorted(
        f"arrangement-{name}" for name in arrangement["identities"]
    )

    rendered = {pair["key"]: pair["value"] for pair in render(declared)}
    assert 'path "admin/*"' in rendered["arrangement-example-everyday"]
    assert 'path "admin/*"' not in rendered["arrangement-example-operator"]


def test_reconcile_render_grants_every_loaded_arrangement_policy(rendered_defaults):
    values, _, _ = rendered_defaults
    arrangement = json.loads(FIXTURE.read_text(encoding="utf-8"))
    policies = _declared_policies(values, arrangement)

    writable = _writable_policy_names(
        _render(RECONCILE, dict(values, openbao_policies=policies))
    )
    expected = {f"arrangement-{name}" for name in arrangement["identities"]}
    assert expected <= writable
    assert len(expected) == len(arrangement["identities"]) > 0
