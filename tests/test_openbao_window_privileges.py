"""Window service declarations render isolated, inert credential identities."""

import fnmatch
import pytest
import time
import yaml

from openbao_reconcile_bounds_helpers import (
    RECONCILE,
    TEMPLATES,
    _allowed_parameters,
    _capabilities,
    _render,
    _stanzas,
    _templar,
    _trust,
    rendered_defaults,
)
from test_openbao_rbac_policy_render import render as render_policies
from test_openbao_hatchet_killtest_policy_reach import _call, _dev_server
from test_openbao_select import (
    condition as selection_condition,
    render as selection_render,
    resolve as resolve_selection,
    task as selection_task,
)

GUARD = TEMPLATES / "ai-admin-guard-policy.hcl.j2"
WINDOW_GRANT = TEMPLATES / "ai-admin-window-policy.hcl.j2"
WINDOW_INIT = TEMPLATES.parents[0] / "tasks/init/02-initialize-cluster.yml"
IDENTITY_FAMILIES = ["entity", "entity-alias", "group", "group-alias"]
DENIED_PATHS = [
    "sys/seal", "sys/seal/child", "sys/unseal", "sys/unseal/child",
    "sys/rekey", "sys/rekey/init", "sys/rekey/verify", "sys/rekey-recovery-key/init",
    "sys/generate-root/attempt", "sys/generate-root-token/attempt",
    "sys/generate-recovery-token/attempt", "sys/rotate", "sys/rotate/keyring",
    "sys/rotate/keyring/config", "sys/rotate/root/init", "sys/rotate/recovery/update",
    "sys/raw/core/keyring", "auth/token/create-orphan", "auth/token/create/fixture",
    "auth/token/roles/fixture", "auth/token/revoke-orphan",
    "auth/approle/role/window-github", "auth/approle/role/window-github/secret-id",
    "auth/approle/role/ordinary/secret-id", "auth/approle/role/ordinary/custom-secret-id",
    "auth/approle/role/ordinary", "auth/jwt/role/fixture",
] + [f"identity/{family}{suffix}"
     for family in IDENTITY_FAMILIES
     for suffix in ("", "/id/fixture", "/name/fixture", "/id/fixture/nested", "-fixture")]


def _session_policies(values):
    role = next(role for role in values["openbao_approles"]
                if role["name"] == values["openbao_ai_admin_session_approle_name"])
    return role["token_policies"] + ["default"]


@pytest.mark.parametrize("service_name", ["github"])
def test_service_role_scope_and_render(service_name, rendered_defaults):
    values, approles, policies = rendered_defaults
    services = _templar(_trust(values)).template(_trust(values["openbao_window_services"]))
    service = next(service for service in services if service["name"] == service_name)
    name = f"window-{service_name}"
    roles = [role for role in approles if role["name"] == name]
    assert len(roles) == 1
    role = roles[0]
    assert role["policy"] == name
    assert role["manage_secret_id"] is False
    assert role["secret_id_num_uses"] == 1
    assert role["token_type"] == "batch"
    assert role["token_ttl"] == role["token_max_ttl"] == "15m"
    assert values["openbao_approle_cidr_class_map"][name] == "workstation"
    parameters = values["openbao_approle_cli_parameters"][name]
    assert parameters["token_bound_cidrs"] == values["openbao_workstation_cidrs"]
    policy = next(policy for policy in policies if policy["name"] == name)
    # Run the controller's actual nested template lookup with its item parameters.
    text = render_policies([policy])[0]["value"]
    stanzas = dict(_stanzas(text))
    assert service["credential_paths"]
    assert set(stanzas) == set(service["credential_paths"])
    assert all(path.startswith("github-admin/token/") for path in stanzas)
    assert all("*" not in path and "+" not in path for path in stanzas)
    assert all(_capabilities(body) == ["create", "update"] for body in stanzas.values())
    assert all('"*" = []' in body for body in stanzas.values())


def test_tofu_github_private_role_scope(rendered_defaults):
    values, approles, _ = rendered_defaults
    name = "window-tofu-github-private"
    role = next(role for role in approles if role["name"] == name)
    assert role["policy"] == name
    assert role["manage_secret_id"] is False
    assert role["secret_id_num_uses"] == 1
    assert role["token_type"] == "batch"
    assert role["token_ttl"] == role["token_max_ttl"] == "15m"
    assert values["openbao_approle_cidr_class_map"][name] == "workstation"
    parameters = values["openbao_approle_cli_parameters"][name]
    assert parameters["token_bound_cidrs"] == values["openbao_workstation_cidrs"]


def test_youtrack_window_grants_two_exact_read_leaves(rendered_defaults):
    values, approles, policies = rendered_defaults
    name = "window-youtrack"
    role = next(role for role in approles if role["name"] == name)
    assert role["token_type"] == "batch"
    assert role["token_ttl"] == role["token_max_ttl"] == "15m"
    policy = next(policy for policy in policies if policy["name"] == name)
    stanzas = dict(_stanzas(render_policies([policy])[0]["value"]))
    assert set(stanzas) == {"secret/data/apps/youtrack", "secret/data/platform/object-storage"}
    assert all(_capabilities(body) == ["read"] for body in stanzas.values())
    allowed = _allowed_parameters(dict(_stanzas(_render(GUARD, values)))["auth/token/create"])
    assert [name] in allowed["policies"]


def test_window_policy_and_role_are_outside_routine_reconcile(rendered_defaults):
    values, _, _ = rendered_defaults
    reconcile = dict(_stanzas(_render(RECONCILE, values)))
    assert "sys/policies/acl/window-github" not in reconcile
    assert "auth/approle/role/window-github" not in reconcile
    assert "auth/approle/role/window-github/secret-id" not in reconcile
    assert "sys/policies/acl/window-tofu-github-private" not in reconcile
    assert "auth/approle/role/window-tofu-github-private" not in reconcile
    assert "auth/approle/role/window-tofu-github-private/secret-id" not in reconcile


def test_generic_template_does_not_grant_undeclared_paths(rendered_defaults):
    values, _, _ = rendered_defaults
    item = {"service": {"name": "fixture", "credential_paths": [], "scope": ["read"], "lifetime": "15m"}}
    text = _render(TEMPLATES / "window-service-policy.hcl.j2", dict(values, item=item))
    assert dict(_stanzas(text)) == {}


def test_guard_retains_protected_roles_and_policies(rendered_defaults):
    values, _, _ = rendered_defaults
    stanzas = dict(_stanzas(_render(GUARD, values)))
    human_approles = _templar(_trust(values)).template(
        _trust(values["openbao_ai_admin_window_human_gated_approles"])
    )
    guard_approles = _templar(_trust(values)).template(
        _trust(values["openbao_ai_admin_window_guard_deny_approles"])
    )
    expected_guard_roles = {
        role["name"] for role in human_approles
        if role["name"] in values["openbao_ai_admin_window_protected_approle_names"]
    }
    assert {role["name"] for role in guard_approles} == expected_guard_roles
    for name in expected_guard_roles:
        for suffix in ("", "/*"):
            assert _capabilities(stanzas[f"auth/approle/role/{name}{suffix}"]) == ["deny"]
    for name in values["openbao_ai_admin_window_protected_policy_names"]:
        for suffix in ("", "/*"):
            assert _capabilities(stanzas[f"sys/policies/acl/{name}{suffix}"]) == ["deny"]
    assert "auth/approle/role/*" in stanzas


def test_window_grant_and_guard_partition_the_human_gated_objects(rendered_defaults):
    values, approles, policies = rendered_defaults

    def resolve(name):
        return _templar(_trust(values)).template(_trust(values[name]))

    def names(items):
        return {item["name"] for item in items}

    human_approles = resolve("openbao_ai_admin_window_human_gated_approles")
    granted_approles = resolve("openbao_ai_admin_window_grant_approles")
    denied_approles = resolve("openbao_ai_admin_window_guard_deny_approles")
    false_approle_names = {
        role["name"] for role in approles if role.get("manage_secret_id") is False
    }
    protected_approle_names = set(values["openbao_ai_admin_window_protected_approle_names"])
    assert names(human_approles) == false_approle_names | (
        {role["name"] for role in approles} & protected_approle_names
    )
    assert names(granted_approles).isdisjoint(names(denied_approles))
    assert names(granted_approles) | names(denied_approles) == names(human_approles)
    for role_name in false_approle_names:
        assert (role_name in names(granted_approles)) + (role_name in names(denied_approles)) == 1

    human_policy_names = set(resolve("openbao_ai_admin_window_human_gated_policy_names"))
    human_policies = resolve("openbao_ai_admin_window_human_gated_policies")
    granted_policies = resolve("openbao_ai_admin_window_grant_policies")
    denied_policy_names = set(resolve("openbao_ai_admin_window_guard_deny_policy_names"))
    granted_policy_names = names(granted_policies)
    assert names(human_policies) == human_policy_names & {
        policy["name"] for policy in policies
    }
    assert granted_policy_names.isdisjoint(denied_policy_names)
    assert granted_policy_names | denied_policy_names == human_policy_names

    # The universe, computed here from the declared sources rather than from the
    # role's derived lists: every policy attached to any human-gated AppRole,
    # every reconcile-excluded policy, and every self-protecting AppRole's policies.
    def attached(role):
        return set(role.get("token_policies") or ([role["policy"]] if role.get("policy") else []))

    declared_policy_names = {policy["name"] for policy in policies}
    self_protecting_roles = set(resolve("openbao_ai_admin_window_self_protecting_approle_names"))
    assert values["openbao_policy_sync_approle_name"] in self_protecting_roles
    self_attached = set().union(*(attached(r) for r in approles if r["name"] in self_protecting_roles))
    gated_attached = declared_policy_names & set().union(
        *(attached(r) for r in approles if r["name"] in names(human_approles)))
    excluded = declared_policy_names & set(values["openbao_reconcile_policy_excluded_names"])
    assert human_policy_names >= gated_attached | excluded | self_attached
    reconcile_policy = values["openbao_reconcile_policy_name"]
    assert self_attached - {reconcile_policy} <= denied_policy_names
    assert human_policy_names - set(resolve("openbao_ai_admin_window_self_protecting_policy_names")) \
        == (gated_attached | excluded) - denied_policy_names
    if "github-mount-config" in declared_policy_names:
        assert "github-mount-config" in denied_policy_names
    assert granted_policy_names <= declared_policy_names
    if reconcile_policy in declared_policy_names:
        assert reconcile_policy in granted_policy_names

    for approle_key, policy_key in (
        ("openbao_github_admin_approle_name", "openbao_github_admin_policy_name"),
        ("openbao_github_enterprise_admin_approle_name",
         "openbao_github_enterprise_admin_policy_name"),
    ):
        approle_name = values[approle_key]
        approle = next((role for role in approles if role["name"] == approle_name), None)
        assert approle is not None
        assert approle["manage_secret_id"] is False
        assert approle_name in names(granted_approles)
        assert approle_name not in names(denied_approles)

        policy_name = values[policy_key]
        policy = next((item for item in policies if item["name"] == policy_name), None)
        # The enterprise admin policy is omitted when its installation id is unset (07c-policy-composition.yml).
        if policy is None:
            assert policy_name not in granted_policy_names | denied_policy_names
            continue
        assert policy_name in granted_policy_names
        assert policy_name not in denied_policy_names


def test_window_grant_is_exact_and_matches_only_eligible_protected_objects(rendered_defaults):
    values, _, _ = rendered_defaults
    text = _render(WINDOW_GRANT, values)
    stanzas = dict(_stanzas(text))
    oidc_path = f"auth/{values['openbao_github_oidc_auth_path']}/role/*"
    assert [path for path in stanzas if "*" in path or "+" in path] == [oidc_path]
    stanzas.pop(oidc_path)
    expected_policy_paths = {
        f"sys/policies/acl/{policy['name']}"
        for policy in values["openbao_ai_admin_window_manageable_policies"]
    } | {f"sys/policies/acl/{values['openbao_reconcile_policy_name']}"}
    expected_role_paths = {
        f"auth/approle/role/{role['name']}"
        for role in values["openbao_ai_admin_window_manageable_approles"]
    } | {
        f"auth/approle/role/{role['name']}/policies"
        for role in values["openbao_ai_admin_window_manageable_approles"]
    }
    assert {path for path in stanzas if path.startswith("sys/policies/acl/")} == expected_policy_paths
    assert {path for path in stanzas if path.startswith("auth/approle/role/")} == expected_role_paths
    assert _capabilities(stanzas[f"sys/policies/acl/{values['openbao_reconcile_policy_name']}"]) == [
        "create", "read", "update",
    ]
    assert all(_capabilities(stanzas[path]) == ["create", "read", "update"]
               for path in expected_policy_paths)
    assert all(_capabilities(stanzas[path]) == ["create", "read", "update"]
               for path in expected_role_paths if not path.endswith("/policies"))
    assert all(_capabilities(stanzas[path]) == ["create", "update"]
               for path in expected_role_paths if path.endswith("/policies"))
    assert all(role.get("manage_secret_id") is False
               for role in values["openbao_ai_admin_window_manageable_approles"])
    assert _capabilities(stanzas["sys/capabilities-self"]) == ["create", "update"]
    assert _capabilities(stanzas["sys/policies/acl"]) == ["list"]
    path_declarations = [
        line.strip().split('"', 2)[1]
        for line in WINDOW_GRANT.read_text(encoding="utf-8").splitlines()
        if line.lstrip().startswith('path "')
    ]
    assert not any("secret-id" in path for path in path_declarations)
    assert [path for path in path_declarations if "*" in path] == [
        "auth/{{ openbao_github_oidc_auth_path }}/role/*"
    ]


def test_window_grant_does_not_pin_policy_contents_or_approle_parameters(rendered_defaults):
    values, _, _ = rendered_defaults
    for path, body in _stanzas(_render(WINDOW_GRANT, values)):
        if path == f"auth/{values['openbao_github_oidc_auth_path']}/role/*":
            continue
        assert "allowed_parameters" not in body, path
        assert "required_parameters" not in body, path


@pytest.mark.parametrize("kind", ["policies", "approles"])
def test_window_selection_resolver_accepts_granted_and_refuses_self_protecting_names(
    kind, rendered_defaults,
):
    values, approles, policies = rendered_defaults
    candidates = values[f"openbao_ai_admin_window_manageable_{kind}"]
    declared = policies if kind == "policies" else approles
    candidate_names = [item["name"] for item in candidates]
    declared_names = [item["name"] for item in declared]
    selected_name = candidate_names[0]

    _matches, accepted = resolve_selection(
        {kind: [selected_name]}, kind=kind,
        names=candidate_names, declared_names=declared_names,
    )
    assert accepted == [{"name": selected_name}]
    gate = selection_task("Require selected OpenBao objects to be manageable by this identity")
    outside = selection_render(gate["vars"]["_outside_grant"], {
        "openbao_object_targets": accepted,
        "openbao_select_candidates": candidates,
    })
    assert selection_condition(gate["ansible.builtin.assert"]["that"][0], {
        "_outside_grant": outside,
    })
    assert outside == []

    protected_name = (values["openbao_ai_admin_session_approle_name"]
                      if kind == "approles" else values["openbao_ai_admin_policy_name"])
    _matches, rejected = resolve_selection(
        {kind: [protected_name]}, kind=kind,
        names=candidate_names, declared_names=declared_names,
    )
    assert rejected == [{"name": protected_name}]
    outside = selection_render(gate["vars"]["_outside_grant"], {
        "openbao_object_targets": rejected,
        "openbao_select_candidates": candidates,
    })
    assert outside == [protected_name]
    assert "human-gated path" in selection_render(gate["ansible.builtin.assert"]["fail_msg"], {
        "_outside_grant": outside, "openbao_select_kind": kind,
    })


@pytest.mark.parametrize(("selection", "accepted"), [
    ({}, False),
    ({"secrets": ["x"]}, False),
    ({"approles": ["sandbox-agent-read"]}, True),
    ({"policies": ["apps"], "reconcile_policy": ["openbao-reconcile"]}, True),
])
def test_window_run_requires_a_nonempty_bounded_selection(selection, accepted):
    task = next(
        t for t in yaml.safe_load(WINDOW_INIT.read_text())
        if t.get("name") == "Require an explicit bounded selection for ai-admin-session"
    )
    assert task["when"] == "openbao_ai_admin_window_mode | default(false) | bool"
    results = [
        _templar(_trust({"openbao_select": selection})).template(_trust("{{ " + c + " }}")) in (True, "True")
        for c in task["ansible.builtin.assert"]["that"]
    ]
    assert all(results) is accepted


def test_window_identity_uses_lookup_self_and_preflights_before_policy_sync(rendered_defaults):
    values, _, _ = rendered_defaults
    tasks = yaml.safe_load(WINDOW_INIT.read_text(encoding="utf-8"))
    named_tasks = {task.get("name"): task for task in tasks}
    lookup = named_tasks["Look up the supplied token's own policies"]
    resolve = named_tasks["Resolve whether the supplied token is the ai-admin-session window"]
    partial_policy_guard = named_tasks[
        "FAIL — a partial admin-window policy set is present"
    ]["ansible.builtin.assert"]["that"][0]
    bounded = named_tasks["Resolve whether this run uses the bounded RBAC path"]
    early_preflight = named_tasks["Resolve ai-admin-session selections and grants before policy-sync"]
    policy_sync = named_tasks[
        "Resolve the Raft leader and sync the reconcile policy before any grant consumer runs"
    ]

    assert lookup["ansible.builtin.command"]["cmd"] == "bao read -format=json auth/token/lookup-self"
    assert lookup["environment"]["BAO_TOKEN"] == "{{ openbao_bootstrap_token }}"
    assert lookup["no_log"] is True
    expression = resolve["ansible.builtin.set_fact"]["openbao_ai_admin_window_mode"]
    policies = [
        values["openbao_ai_admin_policy_name"],
        values["openbao_ai_admin_guard_policy_name"],
        values["openbao_ai_admin_window_policy_name"],
        values["openbao_tofu_state_admin_policy_name"],
    ]
    context = dict(values, _lookup={"data": {"policies": policies}})
    assert _templar(_trust(context)).template(_trust(expression)) in (True, "True")
    partial_context = dict(values, openbao_ai_admin_window_policies=[policies[1]])
    assert not selection_condition(partial_policy_guard, partial_context)
    partial_context["openbao_ai_admin_window_policies"] = [policies[2]]
    assert not selection_condition(partial_policy_guard, partial_context)
    partial_context["openbao_ai_admin_window_policies"] = policies[:-1]
    assert not selection_condition(partial_policy_guard, partial_context)
    complete_context = dict(values, openbao_ai_admin_window_policies=policies)
    assert selection_condition(partial_policy_guard, complete_context)
    context["_lookup"] = {"data": {"policies": ["root"]}}
    assert _templar(_trust(context)).template(_trust(expression)) in (False, "False")
    assert tasks.index(early_preflight) < tasks.index(policy_sync)
    assert "openbao_ai_admin_window_mode" in str(early_preflight.get("when", []))
    bounded_mode = bounded["ansible.builtin.set_fact"]["openbao_bounded_rbac_mode"]
    bounded_context = dict(values, openbao_reconcile_mode=False, openbao_ai_admin_window_mode=True)
    assert _templar(_trust(bounded_context)).template(_trust(bounded_mode)) in (True, "True")
    selection_preflight = yaml.safe_load(
        (WINDOW_INIT.parents[0] / "selection-preflight.yml").read_text(encoding="utf-8")
    )
    assert "openbao_bounded_rbac_mode" in str(
        selection_preflight[-1].get("when", [])
    )


def test_guard_pins_child_token_parameters(rendered_defaults):
    values, _, _ = rendered_defaults
    body = dict(_stanzas(_render(GUARD, values)))["auth/token/create"]
    expected = {name: [value] for name, value in _request().items()}
    expected["policies"] = _window_policy_sets(values)
    allowed = _allowed_parameters(body)
    assert allowed == expected
    assert ["window-tofu-github-private"] in allowed["policies"]


@pytest.mark.parametrize("family", IDENTITY_FAMILIES)
def test_guard_denies_identity_family_and_descendants(family, rendered_defaults):
    values, _, _ = rendered_defaults
    stanzas = dict(_stanzas(_render(GUARD, values)))
    for suffix in ("", "/*", "*"):
        assert _capabilities(stanzas[f"identity/{family}{suffix}"]) == ["deny"]


def test_guard_protects_additional_attached_policy(rendered_defaults):
    values, approles, _ = rendered_defaults
    session = next(role for role in approles
                   if role["name"] == values["openbao_ai_admin_session_approle_name"])
    session["token_policies"] = session["token_policies"] + ["fixture-attached"]
    stanzas = dict(_stanzas(_render(GUARD, values)))
    for suffix in ("", "/*"):
        assert _capabilities(stanzas[f"sys/policies/acl/fixture-attached{suffix}"]) == ["deny"]


def test_no_declared_services_denies_child_issuance(rendered_defaults):
    values, _, _ = rendered_defaults
    text = _render(GUARD, dict(values, openbao_window_service_policies=[]))
    assert _capabilities(dict(_stanzas(text))["auth/token/create"]) == ["deny"]


@pytest.fixture
def window_server(rendered_defaults):
    values, _, policies = rendered_defaults
    service_names = {
        f"window-{service['name']}"
        for service in _templar(_trust(values)).template(_trust(values["openbao_window_services"]))
    }
    window_policies = {
        policy["name"]: policy for policy in policies if policy["name"] in service_names
    }
    window = window_policies["window-github"]
    rendered = {
        values["openbao_ai_admin_policy_name"]: _render(TEMPLATES / "ai-admin-policy.hcl.j2", values),
        values["openbao_ai_admin_guard_policy_name"]: _render(GUARD, values),
        values["openbao_ai_admin_window_policy_name"]: _render(WINDOW_GRANT, values),
        values["openbao_tofu_state_admin_policy_name"]: _render(TEMPLATES / "tofu-state-admin-policy.hcl.j2", values),
        **{
            name: _render(TEMPLATES / policy["template"], dict(values, item=policy))
            for name, policy in window_policies.items()
        },
    }
    server, base = _dev_server()
    try:
        for name, text in rendered.items():
            assert _call(base, "root", "PUT", f"sys/policies/acl/{name}", {"policy": text})[0] == 204
        yield base, values, window
    finally:
        server.terminate()
        server.wait(timeout=30)


def _parent(base, values, ttl="1h"):
    status, result = _call(base, "root", "POST", "auth/token/create", {
        "policies": _session_policies(values),
        "ttl": ttl,
    })
    assert status == 200
    return result["auth"]["client_token"]


def _request():
    return {"policies": ["window-github"], "type": "batch", "ttl": "15m",
            "no_parent": False, "no_default_policy": True, "renewable": False}


def _window_policy_sets(values):
    """Exactly the child-policy sets the guard pins issuance to: one declared
    window service per set, in declaration order."""
    services = _templar(_trust(values)).template(_trust(values["openbao_window_services"]))
    return [[f"window-{service['name']}"] for service in services]


def test_native_composition_denies_dangerous_and_protected_paths(window_server):
    base, values, _ = window_server
    parent = _parent(base, values)
    protected_approles = values["openbao_ai_admin_window_protected_approle_names"]
    protected_policies = values["openbao_ai_admin_window_protected_policy_names"]
    paths = DENIED_PATHS + [f"auth/approle/role/{name}{suffix}"
                            for name in protected_approles
                            for suffix in ("", "/nested", "/nested/descendant")] + [
        f"sys/policies/acl/{name}{suffix}"
        for name in protected_policies
        for suffix in ("", "/nested", "/nested/descendant")
    ]
    status, result = _call(base, "root", "POST", "sys/capabilities", {"token": parent, "paths": paths})
    assert status == 200
    assert {path: result[path] for path in paths} == dict.fromkeys(paths, ["deny"])
    status, result = _call(base, parent, "GET", "auth/token/lookup-self")
    assert status == 200, result if status != 200 else ""
    assert _call(base, parent, "POST", "auth/token/renew-self", {})[0] == 200


def test_native_window_grant_allows_exact_rbac_paths_and_keeps_self_protection(window_server):
    base, values, _ = window_server
    parent = _parent(base, values)
    policy = values["openbao_ai_admin_window_manageable_policies"][0]["name"]
    approle = values["openbao_ai_admin_window_manageable_approles"][0]["name"]
    apps_policy = values.get("openbao_apps_policy_name", "apps")
    plane_policy = values["openbao_ansible_converge_policy_name"]
    paths = [
        "sys/capabilities-self",
        "sys/policies/acl",
        f"sys/policies/acl/{policy}",
        f"sys/policies/acl/{values['openbao_reconcile_policy_name']}",
        f"auth/approle/role/{approle}",
        f"auth/approle/role/{approle}/policies",
        f"sys/policies/acl/{apps_policy}",
        f"sys/policies/acl/{plane_policy}",
        "auth/approle/role/openbao-reconcile",
        "auth/approle/role/approle-issuer",
        "auth/approle/role/ai-admin-session",
        f"sys/policies/acl/{values['openbao_ai_admin_window_policy_name']}",
    ]
    status, result = _call(base, "root", "POST", "sys/capabilities", {"token": parent, "paths": paths})
    assert status == 200
    assert result["sys/capabilities-self"] == ["create", "update"]
    assert result["sys/policies/acl"] == ["list"]
    assert result[f"sys/policies/acl/{policy}"] == ["create", "read", "update"]
    assert result[f"sys/policies/acl/{values['openbao_reconcile_policy_name']}"] == [
        "create", "read", "update",
    ]
    assert result[f"auth/approle/role/{approle}"] == ["create", "read", "update"]
    assert result[f"auth/approle/role/{approle}/policies"] == ["create", "update"]
    assert result[f"sys/policies/acl/{apps_policy}"] == ["create", "read", "update"]
    assert result[f"sys/policies/acl/{plane_policy}"] == ["create", "read", "update"]
    for path in paths[8:]:
        assert result[path] == ["deny"]


def test_native_session_cannot_write_attached_policies_or_widen_issuance(window_server):
    base, values, _ = window_server
    parent = _parent(base, values)
    policy = ('path "auth/token/create" { capabilities = ["create", "update", "sudo"] }\n'
              'path "sys/rekey/init" { capabilities = ["update", "sudo"] }')
    for name in _session_policies(values):
        for suffix in ("", "/nested", "/nested/descendant"):
            path = f"sys/policies/acl/{name}{suffix}"
            for method in ("POST", "PUT", "DELETE"):
                assert _call(base, parent, method, path, {"policy": policy})[0] == 403
    assert _call(base, parent, "POST", "auth/token/create", _request())[0] == 200
    assert _call(base, parent, "POST", "auth/token/create", _request() | {"ttl": "1h"})[0] == 403
    assert _call(base, parent, "POST", "auth/token/create", _request() | {"policies": ["ai-admin"]})[0] == 403


@pytest.mark.parametrize("family", ["entity", "group"])
def test_native_session_cannot_attach_policy_through_identity(family, window_server):
    base, values, _ = window_server
    parent = _parent(base, values)
    policy_name = "fixture-identity-policy"
    policy = 'path "sys/rekey/init" { capabilities = ["update", "sudo"] }'
    assert _call(base, parent, "PUT", f"sys/policies/acl/{policy_name}", {"policy": policy})[0] == 204
    path = f"identity/{family}"
    status, result = _call(base, "root", "POST", path, {"name": "fixture", "policies": []})
    assert status == 200
    identity_id = result["data"]["id"]
    request = {"name": "fixture", "policies": [policy_name]}
    for target in (path, f"{path}/id/{identity_id}", f"{path}/name/fixture"):
        for method in ("POST", "PUT", "DELETE"):
            assert _call(base, parent, method, target, request)[0] == 403
    assert _call(base, parent, "POST", path, request | {"name": "fixture-new"})[0] == 403
    status, result = _call(base, "root", "GET", f"{path}/id/{identity_id}")
    assert status == 200
    assert result["data"]["policies"] == []


def test_native_child_is_scoped_and_stops_with_parent(window_server):
    base, values, window = window_server
    parent = _parent(base, values)
    status, result = _call(base, parent, "POST", "auth/token/create", _request())
    assert status == 200, result if status != 200 else ""
    assert result["auth"]["token_type"] == "batch"
    assert result["auth"]["policies"] == ["window-github"]
    assert result["auth"]["renewable"] is False
    assert result["auth"]["lease_duration"] <= 900
    child = result["auth"]["client_token"]
    allowed = window["service"]["credential_paths"]
    denied = ["secret/data/apps/fixture", "secrets-external/data/fixture", "aws/sts/fixture",
              "github-admin/config", "github-admin/token", "github-admin/token/undeclared",
              "auth/token/create", "auth/token/create-orphan", "sys/seal"]
    status, result = _call(base, "root", "POST", "sys/capabilities", {"token": child, "paths": allowed + denied})
    assert status == 200
    assert all(result[path] == ["create", "update"] for path in allowed)
    assert all(result[path] == ["deny"] for path in denied)
    assert _call(base, "root", "POST", "auth/token/revoke", {"token": parent})[0] == 204
    assert _call(base, "root", "POST", "sys/capabilities", {"token": child, "paths": allowed})[0] == 400


def test_native_tofu_github_private_child_is_scoped(window_server):
    base, values, _ = window_server
    services = _templar(_trust(values)).template(_trust(values["openbao_window_services"]))
    service = next(item for item in services if item["name"] == "tofu-github-private")
    allowed = {grant["path"]: grant["capabilities"] for grant in service["grants"]}
    assert allowed
    parent = _parent(base, values)
    config_mount = values["openbao_config_mount"]
    assert _call(base, "root", "POST", f"sys/mounts/{config_mount}", {
        "type": "kv", "options": {"version": "2"},
    })[0] == 204
    assert _call(base, "root", "POST", f"{config_mount}/data/github/orgs", {
        "data": {"value": "fixture"},
    })[0] == 200
    github_mount = values["openbao_github_mount"]
    assert _call(base, "root", "POST", f"sys/mounts/{github_mount}", {"type": "kv"})[0] == 204
    request = _request() | {"policies": ["window-tofu-github-private"]}
    status, result = _call(base, parent, "POST", "auth/token/create", request)
    assert status == 200, result if status != 200 else ""
    assert result["auth"]["policies"] == ["window-tofu-github-private"]
    child = result["auth"]["client_token"]
    denied = "github-admin/token/undeclared"
    paths = list(allowed) + [denied]
    status, result = _call(base, "root", "POST", "sys/capabilities", {"token": child, "paths": paths})
    assert status == 200
    # OpenBao reports capabilities sorted, not in declared order.
    assert all(sorted(result[path]) == sorted(capabilities) for path, capabilities in allowed.items())
    assert result[denied] == ["deny"]
    status, result = _call(base, child, "GET", "auth/token/lookup-self")
    assert status == 200, result if status != 200 else ""
    status, result = _call(base, child, "GET", f"{config_mount}/data/github/orgs")
    assert status == 200, result if status != 200 else ""
    assert _call(base, child, "GET", f"{config_mount}/data/other")[0] == 403
    assert _call(base, child, "POST", f"{github_mount}/token", {
        "org_name": "fixture-org", "permissions": ["contents:read"],
    })[0] == 403


def test_native_child_stops_when_remaining_window_expires(window_server):
    base, values, window = window_server
    parent = _parent(base, values, "2s")
    status, result = _call(base, parent, "POST", "auth/token/create", _request())
    assert status == 200, result if status != 200 else ""
    child = result["auth"]["client_token"]
    time.sleep(3)
    assert _call(base, "root", "POST", "sys/capabilities", {
        "token": child, "paths": window["service"]["credential_paths"],
    })[0] == 400


def test_native_issuance_rejects_policy_lifetime_and_orphan_overrides(window_server):
    base, values, _ = window_server
    parent = _parent(base, values)
    changes = [
        {"policies": ["root"]}, {"policies": []}, {"policies": ["ai-admin"]},
        {"policies": ["window-github", "default"]}, {"type": "service"},
        {"ttl": "16m"}, {"no_parent": True}, {"no_default_policy": False},
        {"renewable": True}, {"period": "1h"}, {"role_name": "fixture"},
        {"entity_alias": "fixture"},
    ]
    for change in changes:
        assert _call(base, parent, "POST", "auth/token/create", _request() | change)[0] == 403
    for parameter in _request():
        request = _request()
        del request[parameter]
        assert _call(base, parent, "POST", "auth/token/create", request)[0] == 403


def test_window_oidc_role_grant_limits_attachable_policies(rendered_defaults):
    values, _, _ = rendered_defaults
    oidc_path = f"auth/{values['openbao_github_oidc_auth_path']}/role/*"
    body = dict(_stanzas(_render(WINDOW_GRANT, values)))[oidc_path]
    assert _capabilities(body) == ["create", "read", "update"]
    allowed = _allowed_parameters(body)
    templar = _templar(_trust(values))
    expected = templar.template(_trust(values["openbao_ai_admin_window_oidc_role_policies"]))
    assert allowed == {"*": [], "token_policies": expected, "policies": expected}
    protected = (templar.template(_trust(values["openbao_ai_admin_window_protected_policy_names"]))
                 + templar.template(_trust(values["openbao_ai_admin_window_guard_deny_policy_names"])))
    assert expected and protected
    assert not [name for name in protected for allowed_name in expected
                if fnmatch.fnmatchcase(name, allowed_name)]
    guard = dict(_stanzas(_render(GUARD, values)))
    admin_roles = (f"auth/{values['openbao_github_oidc_auth_path']}/role/"
                   f"{values['openbao_ai_admin_approle_name']}*")
    assert _capabilities(guard[admin_roles]) == ["deny"]
    assert all(_capabilities(guard[path]) == ["deny"]
               for path in ("auth/*", "auth/approle/role/*", "auth/token/*", "sys/seal", "sys/raw*"))


def test_native_window_writes_oidc_roles_only_with_declared_policies(window_server):
    base, values, _ = window_server
    mount = values["openbao_github_oidc_auth_path"]
    assert _call(base, "root", "POST", f"sys/auth/{mount}", {"type": "jwt"})[0] == 204
    assert _call(base, "root", "POST", "sys/auth/approle", {"type": "approle"})[0] == 204
    parent = _parent(base, values)
    set_policy = values["openbao_github_pr_reconcile_policy_name"]
    undeclared = f"{values['openbao_github_gate_checks_set_prefix']}-undeclared"

    def role(policies, field="token_policies"):
        return {"role_type": "jwt", "user_claim": "sub",
                "bound_audiences": ["https://github.com/ExampleOrg"],
                "bound_claims": {"repository": "ExampleOrg/example"}, field: policies}

    path = f"auth/{mount}/role/{set_policy}"
    # The converge sends each role's one policy as a string (09c-github-oidc.yml).
    assert _call(base, parent, "POST", path, role(set_policy))[0] == 204
    assert _call(base, parent, "GET", path)[0] == 200
    assert _call(base, parent, "POST", f"auth/{mount}/role/{values['openbao_ci_evals_policy_name']}",
                 role(values["openbao_ci_evals_policy_name"]))[0] == 204
    admin = values["openbao_ai_admin_policy_name"]
    # A list is compared as a whole value, so no list matches the string limits.
    for body in (role(admin), role([admin]), role([set_policy]), role([set_policy, admin]),
                 role(admin, field="policies"), role(f"{set_policy},{admin}"),
                 role(f"{set_policy}, {admin}"), role(undeclared), role(f"{undeclared},{admin}")):
        assert _call(base, parent, "POST", path, body)[0] == 403, body
    assert _call(base, parent, "DELETE", path)[0] == 403
    for name in (values["openbao_ai_admin_approle_name"],
                 values["openbao_ai_admin_session_approle_name"]):
        for admin_path in (f"auth/{mount}/role/{name}", f"auth/approle/role/{name}"):
            assert _call(base, parent, "POST", admin_path, role(set_policy))[0] == 403, admin_path
    status, live = _call(base, "root", "GET", path)
    assert status == 200 and live["data"]["token_policies"] == [set_policy]


def test_window_oidc_role_policies_are_exact_declared_names(rendered_defaults):
    values, _, _ = rendered_defaults
    write_role = {"name": "gate-checks-exampleorg"}
    rendered = _templar(_trust(dict(values, openbao_github_write_oidc_roles=[write_role]))).template(
        _trust(values["openbao_ai_admin_window_oidc_role_policies"]))
    assert "gate-checks-exampleorg" in rendered
    assert values["openbao_ci_evals_policy_name"] in rendered
    assert not [name for name in rendered if "*" in name or "," in name]
