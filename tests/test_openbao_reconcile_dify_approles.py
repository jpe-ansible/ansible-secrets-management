"""The reconcile policy manages the inert Dify agent AppRoles by exact name."""

import pytest

from openbao_reconcile_bounds_helpers import (
    RECONCILE,
    _allowed_parameters,
    _capabilities,
    _render,
    _stanzas,
    _templar,
    _trust,
    rendered_defaults,
)


@pytest.fixture(autouse=True)
def _dify_agent_cidr(monkeypatch):
    # The roles render only with a host CIDR declared; autouse runs before rendered_defaults.
    monkeypatch.setenv("OPENBAO_DIFY_AGENT_CIDR", "192.0.2.10/32")
    monkeypatch.setenv("OPENBAO_DIFY_SECRET_ID_ISSUER_SECRET_ID_CIDR", "192.0.2.11/32")


def test_reconcile_grants_each_dify_agent_approle_by_exact_name(rendered_defaults):
    values, _, _ = rendered_defaults
    roles = _templar(_trust(values)).template(_trust(values["openbao_dify_agent_approles"]))
    names = [role["name"] for role in roles]
    assert len(names) == 9
    stanzas = dict(_stanzas(_render(RECONCILE, values)))
    for name in names:
        role = stanzas[f"auth/approle/role/{name}"]
        assert _capabilities(role) == ["create", "read", "update"]
        assert _allowed_parameters(role)["token_policies"]
        assert _capabilities(stanzas[f"auth/approle/role/{name}/role-id"]) == ["read"]
        assert f"auth/approle/role/{name}/secret-id" not in stanzas
    assert not any("*" in path or "+" in path for path in stanzas if path.startswith("auth/approle/role/agent-"))
