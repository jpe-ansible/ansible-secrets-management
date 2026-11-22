"""The routine reconcile identity may write only the named agent-flow roles, each pinned to its own policy."""

import re
from pathlib import Path

from openbao_reconcile_bounds_helpers import (
    _allowed_parameters, _capabilities, _render, _stanzas, rendered_defaults, RECONCILE
)

ROLE_PREFIX = "auth/github-actions/role/"
NAMED = "github-agent-ci-fix"
OTHER_FLOW = "github-agent-pr-review"


def _role_stanzas(values):
    stanzas = dict(_stanzas(_render(RECONCILE, values)))
    return {
        path.removeprefix(ROLE_PREFIX): body
        for path, body in stanzas.items()
        if path.startswith(ROLE_PREFIX)
    }


def _denied_keys(body):
    match = re.search(r"denied_parameters\s*=\s*\{([^}]*)\}", body)
    return set(re.findall(r'"([^"]+)"', match.group(1))) if match else set()


def _permits(stanzas, name, capability, params):
    # An exact path outranks the single-segment wildcard, as in the ACL.
    body = stanzas.get(name, stanzas.get("+"))
    if body is None or capability not in _capabilities(body):
        return False
    if any(key in _denied_keys(body) for key in params):
        return False
    if "allowed_parameters" not in body:
        return True
    allowed = _allowed_parameters(body)
    for key, value in params.items():
        if key in allowed:
            # The ACL compares the request value as sent with each listed item: a JSON array
            # never equals a scalar item, so a pinned list must be matched with a scalar value.
            if allowed[key] and value not in allowed[key]:
                return False
        elif "*" not in allowed:
            return False
    return True


def test_only_the_named_agent_flow_role_has_an_exact_grant(rendered_defaults):
    values, _approles, _policies = rendered_defaults
    assert values["openbao_reconcile_agent_flow_role_names"] == [NAMED]
    stanzas = _role_stanzas(values)
    assert set(stanzas) == {"+", NAMED}
    assert _capabilities(stanzas[NAMED]) == ["create", "read", "update"]
    assert _capabilities(stanzas["+"]) == ["read"]
    assert _denied_keys(stanzas[NAMED]) == {"groups_claim", "claim_mappings"}


def test_the_named_role_is_pinned_to_its_own_policy(rendered_defaults):
    values, _approles, _policies = rendered_defaults
    flow = next(role for role in values["openbao_github_agent_flow_base_roles"] if role["name"] == NAMED)
    allowed = _allowed_parameters(_role_stanzas(values)[NAMED])
    assert allowed["token_policies"] == [flow["policy"]]
    assert allowed["policies"] == [flow["policy"]]
    assert allowed["token_no_default_policy"] == [True]


def test_the_role_write_sends_the_policy_as_a_scalar():
    # The pinned list only matches a scalar request value, so the write must not wrap it in a list.
    task = (Path(__file__).parent.parent / "roles/openbao/tasks/init/reconcile-github-agent-flow.yml").read_text()
    assert "'token_policies': openbao_github_agent_flow.policy," in task
    assert "'token_policies': [" not in task


def test_an_unlisted_role_path_is_refused_for_writes(rendered_defaults):
    values, _approles, _policies = rendered_defaults
    stanzas = _role_stanzas(values)
    body = {"token_policies": OTHER_FLOW}
    for name in (OTHER_FLOW, "docs-router-snapshot", "not-a-declared-role"):
        assert _permits(stanzas, name, "read", {})
        assert not _permits(stanzas, name, "update", body)
        assert not _permits(stanzas, name, "create", body)
    assert not _permits(stanzas, NAMED, "delete", {})


def test_a_different_token_policy_set_is_refused_on_the_named_role(rendered_defaults):
    values, _approles, _policies = rendered_defaults
    stanzas = _role_stanzas(values)
    own = {
        "role_type": "jwt",
        "token_policies": NAMED,
        "token_no_default_policy": True,
        "bound_claims_type": "string",
    }
    assert _permits(stanzas, NAMED, "update", own)
    assert not _permits(stanzas, NAMED, "update", {**own, "token_no_default_policy": False})
    for key in ("token_policies", "policies"):
        assert not _permits(stanzas, NAMED, "update", {**own, key: OTHER_FLOW})
        assert not _permits(stanzas, NAMED, "update", {**own, key: f"{NAMED},default"})
        assert not _permits(stanzas, NAMED, "update", {**own, key: [NAMED]})
    assert not _permits(stanzas, NAMED, "update", {**own, "groups_claim": "groups"})
