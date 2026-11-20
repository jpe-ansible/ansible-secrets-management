"""The controller-side RBAC policy render must not reference an undefined
Jinja variable in ANY policy template that reads `item`, not only the
Terrakube workspace one.

`_openbao_rendered_policy_pairs` builds its dict via a Jinja `for item in
openbao_rbac_policy_targets` loop declared inline in a `vars:` expression.
That `item` is local to this expression's own render pass -- it is never
part of the task's vars, which is the context `lookup('template', ...)`
hands to the sub-template it renders. Any template referencing `item`
(terrakube-workspace-policy.hcl.j2 via `item.workspace.name`,
kv-capability-policy.hcl.j2 via `item.mode`/`item.subtree`) failed live
with "'item' is undefined", originating inside the sub-template, not the
outer expression -- both cases below reproduce that and fail identically
pre-fix.

This renders the REAL expression out of the task file, with REAL template
files, never a reimplementation.
"""

import re
from pathlib import Path
import unittest

import pytest
import yaml

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

from openbao_reconcile_bounds_helpers import (
    TEMPLATES,
    _allowed_parameters,
    _capabilities,
    _render,
    _render_value,
    _stanzas,
    rendered_defaults,
)

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "roles" / "openbao" / "tasks" / "init" / "08-rbac-policies.yml"
RENDER_TASK = "Render the RBAC policies on the controller"

UNIFI_TIERS = ("read", "write", "admin")
WINDOW_TIERS = UNIFI_TIERS + ("terrakube",)

WORKSPACE_POLICY = {
    "name": "terrakube-iac-platform",
    "template": "terrakube-workspace-policy.hcl.j2",
    "workspace": {"name": "iac-platform", "kv_read": ["iac-platform/foo"]},
}


def _task():
    for t in yaml.safe_load(TASKS.read_text(encoding="utf-8")):
        if t.get("name") == RENDER_TASK:
            return t
    raise AssertionError(f"task {RENDER_TASK!r} not found in {TASKS}")


def render(policies):
    """Render the real pairs-builder expression from the task file."""
    task = _task()
    pairs_expr = task["vars"]["_openbao_rendered_policy_pairs"]
    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        "openbao_rbac_policy_targets": policies,
        "openbao_kv_mount": "secret",
        "ansible_managed": "Ansible managed",
    }
    # lookup('template', ...) resolves relative to the role's templates/
    # dir via the search path the task's real loader would use.
    templar._loader.set_basedir(str(ROOT / "roles" / "openbao"))
    return templar.template(trust_as_template(pairs_expr))


class RenderDoesNotFailOnAnItemReferencingTemplate(unittest.TestCase):
    def test_workspace_policy_renders_without_undefined_item(self):
        pairs = render([WORKSPACE_POLICY])
        rendered = {p["key"]: p["value"] for p in pairs}
        self.assertIn("terrakube-iac-platform", rendered)
        self.assertIn("iac-platform", rendered["terrakube-iac-platform"])
        self.assertIn(
            'path "secret/data/iac-platform/foo"', rendered["terrakube-iac-platform"]
        )

    def test_non_workspace_template_referencing_item_also_renders(self):
        # Any template reading `item` hit the same undefined-variable error
        # pre-fix, not only the Terrakube workspace one.
        policy = {
            "name": "write-apps",
            "template": "kv-capability-policy.hcl.j2",
            "mode": "write",
            "subtree": "apps",
        }
        pairs = render([policy])
        self.assertEqual(pairs[0]["key"], "write-apps")
        self.assertIn('path "secret/data/apps/*"', pairs[0]["value"])


def _policy_named(policies, name):
    return next(policy for policy in policies if policy["name"] == name)


def _capability_map(text):
    return {
        path: _capabilities(body)
        for path, body in _stanzas(text)
    }


# The UniFi controller credential tiers: one exact KV leaf per tier, one
# read-only policy per leaf, rendered here exactly as 08-rbac-policies.yml
# renders them.
@pytest.mark.parametrize("tier", UNIFI_TIERS)
def test_unifi_tier_policy_grants_exactly_its_own_leaf(tier, rendered_defaults):
    values, _, policies = rendered_defaults
    policy = _policy_named(policies, values[f"openbao_unifi_{tier}_policy_name"])
    assert _capability_map(render([policy])[0]["value"]) == {
        f"secret/data/unifi/main/{tier}": ["read"],
    }


def test_unifi_is_not_a_capability_domain(rendered_defaults):
    # The tiering exists only while `unifi` stays out of openbao_ai_domains: a
    # domain entry would mint read-unifi/write-unifi over the whole subtree,
    # covering the admin and terrakube leaves too.
    values, _, policies = rendered_defaults
    assert "unifi" not in values["openbao_ai_domains"]
    names = {policy["name"] for policy in policies}
    assert "read-unifi" not in names
    assert "write-unifi" not in names


def test_ai_elevated_carries_only_the_unifi_read_tier(rendered_defaults):
    values, approles, _ = rendered_defaults
    elevated = next(role for role in approles
                    if role["name"] == values["openbao_ai_elevated_approle_name"])
    assert values["openbao_unifi_read_policy_name"] in elevated["token_policies"]


def test_ai_apply_unifi_carries_exactly_the_write_and_read_tiers(rendered_defaults):
    # Mirrors the generated ai-apply-<svc> unlock window (6h/12h, inert) but is
    # declared explicitly, so pin the whole shape here.
    values, approles, _ = rendered_defaults
    role = next(role for role in approles if role["name"] == "ai-apply-unifi")
    assert role["token_policies"] == [
        values["openbao_unifi_write_policy_name"],
        values["openbao_unifi_read_policy_name"],
    ]
    assert role["token_ttl"] == "6h"
    assert role["token_max_ttl"] == "12h"
    assert role["manage_secret_id"] is False
    assert role["secret_id_ttl"] == "15m"
    assert role["secret_id_num_uses"] == 1
    # Both classifications every declared role must carry.
    assert values["openbao_approle_cidr_class_map"]["ai-apply-unifi"] == "workstation"
    class_map = _render_value(values, values["openbao_approle_class_map"])
    assert class_map["ai-apply-unifi"] == "operator-admin"


def test_unifi_window_service_reaches_exactly_the_four_tier_leaves(rendered_defaults):
    values, approles, policies = rendered_defaults
    policy = _policy_named(policies, "window-unifi")
    stanzas = _capability_map(render([policy])[0]["value"])
    assert stanzas == {
        f"secret/data/unifi/main/{tier}": ["create", "update", "read"]
        for tier in WINDOW_TIERS
    }
    role = next(role for role in approles if role["name"] == "window-unifi")
    assert role["manage_secret_id"] is False
    assert values["openbao_approle_cidr_class_map"]["window-unifi"] == "workstation"


def test_github_window_service_keeps_the_parameter_deny(rendered_defaults):
    # The deny_all_parameters opt-out exists for KV-v2 writes; the github mint
    # keeps the parameter-free pinning that denies every parameter.
    _, _, policies = rendered_defaults
    policy = _policy_named(policies, "window-github")
    for _path, body in _stanzas(render([policy])[0]["value"]):
        assert "denied_parameters" in body


def test_tofu_github_private_window_renders_only_its_exact_grants(rendered_defaults):
    values, _, policies = rendered_defaults
    policy = _policy_named(policies, "window-tofu-github-private")
    rendered = render([policy])[0]["value"]
    stanza_pairs = list(_stanzas(rendered))
    stanzas = dict(stanza_pairs)
    config_mount = values["openbao_config_mount"]
    kv_mount = values["openbao_kv_mount"]
    github_mount = values["openbao_github_mount"]
    transit_mount = values["openbao_transit_mount"]
    state_key = values["openbao_tofu_state_transit_key"]

    expected = {
        f"{config_mount}/data/github/orgs": ["create", "update", "read"],
        f"{config_mount}/metadata/github/orgs": ["read", "update"],
        f"{config_mount}/data/terrakube/local-workspaces": [
            "create", "update", "read"
        ],
        f"{config_mount}/metadata/terrakube/local-workspaces": ["read", "update"],
        f"{kv_mount}/data/infrastructure/tofu-github/private-overrides": [
            "create", "update", "read"
        ],
        f"{kv_mount}/metadata/infrastructure/tofu-github/private-overrides": [
            "read", "update"
        ],
        f"{kv_mount}/data/infrastructure/tofu-github/private-overrides-jpe-ai-agents": [
            "create", "update", "read"
        ],
        f"{kv_mount}/metadata/infrastructure/tofu-github/private-overrides-jpe-ai-agents": [
            "read", "update"
        ],
        f"{github_mount}/token": ["create", "update"],
        f"{transit_mount}/datakey/plaintext/{state_key}": ["update"],
        f"{transit_mount}/decrypt/{state_key}": ["update"],
        "auth/token/lookup-self": ["read"],
    }
    assert _capability_map(rendered) == expected
    assert len(stanza_pairs) == len(expected)
    assert set(stanzas) == set(expected)
    assert all("*" not in path and "+" not in path for path in stanzas)

    token_path = f"{github_mount}/token"
    for path, body in stanza_pairs:
        assert not re.search(
            r"(?m)^\s*(?:denied_parameters|required_parameters)\s*=", body
        )
        has_allowed_parameters = bool(
            re.search(r"(?m)^\s*allowed_parameters\s*=", body)
        )
        assert has_allowed_parameters == (path == token_path)
    assert _allowed_parameters(stanzas[token_path]) == {"org_name": []}


def test_scheduled_secret_id_rotator_grants_each_rotated_approle(rendered_defaults):
    values, _approles, policies = rendered_defaults
    scheduled_policy = _policy_named(
        policies, values["openbao_approle_secret_id_rotate_scheduled_policy_name"]
    )
    rendered = _render(
        TEMPLATES / scheduled_policy["template"],
        dict(values, item=scheduled_policy),
    )
    grants = _capability_map(rendered)

    domain_names = _render_value(
        values, "{{ openbao_secrets_domain_approle_names }}"
    )
    scheduled_name = values[
        "openbao_approle_secret_id_rotate_scheduled_approle_name"
    ]
    scheduled_names = sorted(set(domain_names + [scheduled_name]))
    rotated_ttl = _render_value(values, "{{ openbao_rotated_domain_secret_id_ttl }}")
    ttl_overrides = _render_value(
        values, "{{ openbao_approle_secret_id_ttl_overrides }}"
    )
    rotated_names = {
        name for name in scheduled_names if ttl_overrides.get(name) == rotated_ttl
    }

    assert rotated_names == set(scheduled_names)
    expected_capabilities = {
        "role-id": ["read"],
        "secret-id": ["create", "update"],
        "secret-id/lookup": ["update"],
        "secret-id-accessor/destroy": ["update"],
    }
    for name in rotated_names:
        for suffix, capabilities in expected_capabilities.items():
            assert grants[f"auth/approle/role/{name}/{suffix}"] == capabilities


if __name__ == "__main__":
    unittest.main()
