"""Selected GitHub permission sets use the shared selector and scoped writers."""

import re

import pytest
import yaml
from jinja2 import Environment

from test_openbao_select import ROLE, condition, render, resolve, task


KIND = "github_permission_sets"
SELECTED_NAME = "jacobpevans-ai-org-secrets"
SELECTION = {KIND: [SELECTED_NAME]}
PERMISSION_SETS = ROLE / "tasks/init/05-github-permission-sets.yml"
GITHUB_DEFAULTS = ROLE / "defaults/main/03-github-engine.yml"
TERRAKUBE_DEFAULTS = ROLE / "defaults/main/05c-terrakube-and-remaining-domain-names.yml"


def changes(results):
    node = task("Resolve GitHub permission sets that are missing or changed", PERMISSION_SETS)
    return render(node["ansible.builtin.set_fact"]["openbao_github_permission_set_changes"], {
        "openbao_github_permission_set_checks": {"results": results},
    })


def test_permission_set_profile_uses_the_declared_admin_mount_sets():
    defaults = yaml.safe_load((ROLE / "defaults/main/03-github-engine.yml").read_text())
    assert "jacobpevans-ai" in {
        org["name"] for org in defaults["openbao_github_org_secrets_installations"]
    }
    candidates = render(defaults["openbao_github_org_secrets_permission_sets"], {
        "openbao_github_org_secrets_installations": [
            {"name": "jacobpevans-ai", "installation_id": 101},
            {"name": "another", "installation_id": 102},
        ],
        "openbao_github_org_secrets_permissions": {"organization_secrets": "write"},
    })
    profile = yaml.safe_load((ROLE / "defaults/main/00-selection.yml").read_text())[
        "openbao_select_profiles"][KIND]
    assert render(profile["candidates"], {
        "openbao_github_admin_permission_sets": candidates,
    }) == candidates
    assert resolve(SELECTION, KIND, tuple(item["name"] for item in candidates))[1] == [
        {"name": SELECTED_NAME},
    ]
    assert resolve({}, KIND, tuple(item["name"] for item in candidates))[1] == [
        {"name": item["name"]} for item in candidates
    ]


def test_org_secrets_names_and_workspace_reads_match_each_requested_owner():
    defaults = yaml.safe_load(GITHUB_DEFAULTS.read_text())
    installations = defaults["openbao_github_org_secrets_installations"]
    owners = [installation["name"] for installation in installations]
    assert owners == [
        "dryvist", "jacobpevans", "jacobpevans-ai", "jpe-ansible", "jpe-cribl",
        "jpe-nix", "jpe-private", "jpe-splunk", "jpe-openbao-plugin-secrets",
        "jpe-ai-agents", "jpe-claude",
    ]
    assert len(owners) == len(set(owners))

    expected_input_keys = {
        "jacobpevans": "OPENBAO_GITHUB_ADMIN_JACOBPEVANS_INSTALLATION_ID",
        "jacobpevans-ai": "OPENBAO_GITHUB_ADMIN_JACOBPEVANS_AI_INSTALLATION_ID",
        "jpe-nix": "OPENBAO_GITHUB_ADMIN_JPE_NIX_INSTALLATION_ID",
    }
    for owner, input_key in expected_input_keys.items():
        assert defaults[f"openbao_github_{owner.replace('-', '_')}_installation_id"] == (
            "{{ openbao_platform_env['" + input_key + "'] | default('', true) }}"
        )

    fixture_installations = [
        {**installation, "installation_id": str(index + 100)}
        for index, installation in enumerate(installations)
    ]
    sets = render(defaults["openbao_github_org_secrets_permission_sets"], {
        "openbao_github_org_secrets_installations": fixture_installations,
        "openbao_github_org_secrets_permissions": defaults[
            "openbao_github_org_secrets_permissions"
        ],
    })
    expected_names = [
        "dryvist-org-secrets", "jacobpevans-org-secrets", "jacobpevans-ai-org-secrets",
        "jpe-ansible-org-secrets", "jpe-cribl-org-secrets", "jpe-nix-org-secrets",
        "jpe-private-org-secrets", "jpe-splunk-org-secrets",
        "jpe-openbao-plugin-secrets-org-secrets",
        "jpe-ai-agents-org-secrets", "jpe-claude-org-secrets",
    ]
    assert [item["name"] for item in sets] == expected_names
    assert len({item["name"] for item in sets}) == len(sets)
    assert all(item["tier"] == "org-secrets" for item in sets)
    assert all(item["permissions"] == {"organization_secrets": "write"} for item in sets)
    jpe_nix = [item for item in sets if item["name"] == "jpe-nix-org-secrets"]
    assert jpe_nix == [{
        "name": "jpe-nix-org-secrets",
        "tier": "org-secrets",
        "installation_id": "105",
        "permissions": {"organization_secrets": "write"},
    }]

    workspace_defaults = yaml.safe_load(TERRAKUBE_DEFAULTS.read_text())
    workspace = next(
        item for item in workspace_defaults["openbao_terrakube_workspaces"]
        if item["name"] == "{{ openbao_terrakube_org_secrets_workspace_name }}"
    )
    api_reads = render(workspace["api_read"], {
        "openbao_github_org_secrets_permission_sets": sets,
        "openbao_github_mount": "github-configured",
    })
    assert api_reads == [f"github-configured/token/{name}" for name in expected_names]
    for name in (
        "jacobpevans-org-secrets", "jacobpevans-ai-org-secrets", "jpe-nix-org-secrets",
    ):
        assert f"github-configured/token/{name}" in api_reads


def test_org_secrets_read_policy_grants_only_declared_exact_kv_leaves():
    source = yaml.safe_load(TERRAKUBE_DEFAULTS.read_text())
    template = (ROLE / "templates/github-org-secrets-read-policy.hcl.j2").read_text()
    environment = Environment()
    environment.filters["comment"] = lambda value: "\n".join(
        "# " + line for line in str(value).splitlines()
    )
    source.pop("openbao_github_org_secrets_extra_read_paths")
    rendered = environment.from_string(template).render(
        ansible_managed="fixture",
        openbao_github_org_secrets_extra_read_paths=[],
        **source,
    )
    paths = re.findall(r'(?m)^path "([^"]+)"', rendered)
    capabilities = re.findall(r'(?m)^  capabilities = (.*)$', rendered)
    assert paths == [
        "secrets-external/data/github-org/disclosure-denylist",
        "secrets-external/data/github-org/gitleaks",
        "secrets-external/data/github-org/GH_ACTION_RELEASE_PLEASE_PRIVATE_KEY",
        "secrets-external/data/github-org/dify-pr-keeper-webhook",
        "secrets-external/data/github-org/pr-reconcile-exclude",
        "secrets-external/data/ai/saas/openrouter-provisioning",
    ]
    assert capabilities == ['["read"]'] * 6
    assert source["openbao_github_org_pr_reconcile_exclude_field"] == "repos"
    assert source["openbao_github_org_openrouter_provisioning_field"] == "provisioning_key"


def test_org_secrets_read_policy_adds_declared_extra_leaves():
    source = yaml.safe_load(TERRAKUBE_DEFAULTS.read_text())
    template = (ROLE / "templates/github-org-secrets-read-policy.hcl.j2").read_text()
    # Ansible renders templates with trim_blocks and keeps the trailing newline.
    environment = Environment(trim_blocks=True, keep_trailing_newline=True)
    environment.filters["comment"] = lambda value: "\n".join(
        "# " + line for line in str(value).splitlines()
    )
    source.pop("openbao_github_org_secrets_extra_read_paths")
    rendered = environment.from_string(template).render(
        ansible_managed="fixture",
        openbao_github_org_secrets_extra_read_paths=[
            "config/example-svc/example-instance",
            "secret/example-app/main",
        ],
        **source,
    )
    paths = re.findall(r'(?m)^path "([^"]+)"', rendered)
    capabilities = re.findall(r'(?m)^  capabilities = (.*)$', rendered)
    assert paths == [
        "secrets-external/data/github-org/disclosure-denylist",
        "secrets-external/data/github-org/gitleaks",
        "secrets-external/data/github-org/GH_ACTION_RELEASE_PLEASE_PRIVATE_KEY",
        "secrets-external/data/github-org/dify-pr-keeper-webhook",
        "secrets-external/data/github-org/pr-reconcile-exclude",
        "secrets-external/data/ai/saas/openrouter-provisioning",
        "config/data/example-svc/example-instance",
        "secret/data/example-app/main",
    ]
    assert capabilities == ['["read"]'] * 8
    assert '}\npath' not in rendered


def test_org_secrets_read_policy_renders_unchanged_without_extra_leaves():
    source = yaml.safe_load(TERRAKUBE_DEFAULTS.read_text())
    template = (ROLE / "templates/github-org-secrets-read-policy.hcl.j2").read_text()
    # The file without its trailing loop is the policy as it was before extra leaves existed.
    baseline, marker, _ = template.partition("{# Estate-specific leaves")
    assert marker
    environment = Environment(trim_blocks=True, keep_trailing_newline=True)
    environment.filters["comment"] = lambda value: "\n".join(
        "# " + line for line in str(value).splitlines()
    )
    render_template = environment.from_string(template)
    variables = {
        key: value for key, value in source.items()
        if key != "openbao_github_org_secrets_extra_read_paths"
    }
    without_variable = render_template.render(ansible_managed="fixture", **variables)
    with_empty_list = render_template.render(
        ansible_managed="fixture",
        openbao_github_org_secrets_extra_read_paths=[],
        **variables,
    )
    expected = environment.from_string(baseline).render(ansible_managed="fixture", **variables)
    assert without_variable == with_empty_list == expected


def test_org_secrets_extra_read_paths_drop_duplicates_and_rejected_entries(monkeypatch):
    source = yaml.safe_load(TERRAKUBE_DEFAULTS.read_text())
    monkeypatch.setenv(
        "OPENBAO_GITHUB_ORG_SECRETS_READ_PATHS",
        "config/example-svc/main, config/example-svc/main,sys/policies/acl/x,,"
        "secret/example-app/main",
    )
    raw = render(source["openbao_github_org_secrets_extra_read_paths_raw"], {})
    assert raw == ["config/example-svc/main", "sys/policies/acl/x", "secret/example-app/main"]
    assert render(source["openbao_github_org_secrets_extra_read_paths"], {
        "openbao_github_org_secrets_extra_read_paths_raw": raw,
        "openbao_github_org_secrets_extra_read_path_pattern":
            source["openbao_github_org_secrets_extra_read_path_pattern"],
    }) == ["config/example-svc/main", "secret/example-app/main"]


def test_org_secrets_extra_read_path_pattern():
    source = yaml.safe_load(TERRAKUBE_DEFAULTS.read_text())
    pattern = source["openbao_github_org_secrets_extra_read_path_pattern"]
    # The template renders these paths whole, so this pattern is the only mount limit.
    agent_tier_mount = yaml.safe_load(
        (ROLE / "defaults/main/05k-agent-tier-secret-paths.yml").read_text()
    )["openbao_agent_tier_mount"]
    for path in (f"{agent_tier_mount}/example-tier", "admin/int/example-svc/main"):
        assert not re.match(pattern, path)
    for path in (
        "config/example-svc/example-instance",
        "secret/example-app/main",
        "secrets-external/example-zone/example-svc/ro",
    ):
        assert re.match(pattern, path)
    for path in (
        "config/example/*",
        "config/+/x",
        "sys/policies/acl/x",
        "config/data/example",
        "secret/metadata/example",
        "config/example/",
        "config",
        "config//example",
    ):
        assert not re.match(pattern, path)


def test_selected_permission_set_capability_probe_names_one_exact_endpoint():
    profile = yaml.safe_load((ROLE / "defaults/main/00-selection.yml").read_text())[
        "openbao_select_profiles"][KIND]
    profile["prefix"] = render(profile["prefix"], {"openbao_github_mount": "github-configured"})
    expression = task(
        "Resolve the API paths addressed by selected OpenBao objects",
        ROLE / "tasks/init/selection-capabilities.yml",
    )["ansible.builtin.set_fact"]["openbao_selected_paths"]
    assert render(expression, {
        "openbao_select_profiles": {KIND: profile},
        "openbao_selected_objects": {KIND: [{"name": SELECTED_NAME}]},
    }) == [{
        "name": f"{KIND}: {SELECTED_NAME}",
        "path": f"github-configured/permissionset/{SELECTED_NAME}",
        "capability": "update",
    }]


def test_org_secrets_selection_checks_its_map_and_full_runs_check_every_map():
    assertions = {
        "repo-create": "Assert the repo-create permission map is exactly administration:write",
        "ci-resolver": "Assert the CI resolver permission map is exactly its four write permissions",
        "openhands": "Assert the OpenHands permission map is exactly its four permissions",
        "org-admin": "Assert the org-admin permission map is exactly organization_administration:write",
        "org-secrets": "Assert the org-secrets permission map is exactly organization_secrets:write",
    }
    cases = [
        (SELECTION, [{"name": SELECTED_NAME, "tier": "org-secrets"}], {"org-secrets"}),
        ({}, [], set(assertions)),
    ]
    for selection, targets, expected in cases:
        variables = {
            "openbao_select": selection,
            "openbao_github_permission_set_targets": targets,
            "openbao_bootstrap_token": True,
            "openbao_github_engine_enabled": True,
        }
        active = {
            tier for tier, name in assertions.items()
            if all(condition(gate, variables) for gate in task(name, PERMISSION_SETS)["when"])
        }
        assert active == expected


def test_shared_permission_set_reconcile_is_available_through_the_rbac_tag():
    selected = task("Reconcile selected GitHub permission sets", ROLE / "tasks/init.yml")
    assert selected["ansible.builtin.import_tasks"] == "init/05-github-permission-sets.yml"
    assert "openbao_rbac" in selected["tags"]
    assert all(condition(gate, {"openbao_select": SELECTION}) for gate in selected["when"])
    for selection in ({}, {"policies": ["apps"]}):
        assert not all(condition(gate, {"openbao_select": selection}) for gate in selected["when"])
    site_play = yaml.safe_load((ROLE.parents[1] / "playbooks/site/04a-openbao.yml").read_text())[0]
    assert "openbao" in site_play["tags"]
    full_tasks = yaml.safe_load((ROLE / "tasks/init/05-github-engine.yml").read_text())
    assert any(
        node.get("ansible.builtin.import_tasks") == "05-github-permission-sets.yml"
        for node in full_tasks
    )


def test_permission_set_reads_and_writes_use_only_selected_objects_and_the_run_token():
    desired = {"name": SELECTED_NAME, "installation_id": 101, "permissions": {"organization_secrets": "write"}}
    unselected = {"name": "another-org-secrets", "installation_id": 102}
    selector = task("Select GitHub permission set objects", PERMISSION_SETS)
    assert selector["ansible.builtin.import_tasks"] == "select-objects.yml"
    assert selector["vars"]["openbao_select_kind"] == KIND
    assert render(selector["vars"]["openbao_select_candidates"], {
        "openbao_github_admin_permission_sets": [desired, unselected],
    }) == [desired, unselected]
    keep = task("Keep the selected GitHub permission set objects", PERMISSION_SETS)
    targets = render(keep["ansible.builtin.set_fact"]["openbao_github_permission_set_targets"], {
        "openbao_object_targets": [desired],
    })
    read = task("Read the GitHub token permission sets", PERMISSION_SETS)
    assert render(read["loop"], {"openbao_github_permission_set_targets": targets}) == [desired]
    assert read["check_mode"] is False
    assert read["changed_when"] is False
    assert read["ansible.builtin.uri"]["status_code"] == [200, 404]
    assert read.get("failed_when") is not False
    pending = changes([{"status": 404, "item": desired}])
    assert pending == [desired]
    write = task("Reconcile the GitHub token permission sets", PERMISSION_SETS)
    assert render(write["loop"], {"openbao_github_permission_set_changes": pending}) == [desired]
    for node in (read, write):
        assert node["ansible.builtin.uri"]["headers"]["X-Vault-Token"] == "{{ openbao_bootstrap_token }}"
        assert node["ansible.builtin.uri"]["follow_redirects"] == "none"
        assert node["ansible.builtin.uri"]["use_proxy"] is False
        assert node["no_log"] is True
    initialization = task(
        "Use the per-call reconcile token when it authenticated", ROLE / "tasks/init/02-initialize-cluster.yml",
    )
    assert initialization["ansible.builtin.set_fact"]["openbao_bootstrap_token"] == (
        "{{ openbao_reconcile_login.login.auth.client_token }}"
    )


@pytest.mark.parametrize("optional_fields", [
    {},
    {"permissions": {"organization_secrets": "write"}},
    {"permissions": {"contents": "write"}, "repositories": ["selected-repository"]},
])
def test_permission_set_write_preserves_the_declared_request_shape(optional_fields):
    write = task("Reconcile the GitHub token permission sets", PERMISSION_SETS)
    assert render(write["ansible.builtin.uri"]["body"], {
        "item": {"name": SELECTED_NAME, "installation_id": "101", **optional_fields},
    }) == {"installation_id": 101, **optional_fields}


@pytest.mark.parametrize("live_change", [
    {"installation_id": 102},
    {"permissions": {"contents": "read"}},
    {"repositories": ["another-repository"]},
])
def test_permission_set_drift_in_each_stored_field_is_reported(live_change):
    desired = {
        "name": "selected-set", "installation_id": 101,
        "permissions": {"contents": "write"}, "repositories": ["selected-repository"],
    }
    live = {key: value for key, value in desired.items() if key != "name"}
    assert changes([{"status": 200, "item": desired, "json": {"data": {**live, **live_change}}}]) == [desired]


def test_unchanged_permission_sets_are_absent_from_the_would_change_list():
    desired = {"name": SELECTED_NAME, "installation_id": "101"}
    assert changes([{
        "status": 200, "item": desired,
        "json": {"data": {"installation_id": 101, "permissions": None, "repositories": None}},
    }]) == []
    report = task("Report GitHub permission sets that would be written in check mode", PERMISSION_SETS)
    assert render(report["ansible.builtin.debug"]["msg"], {
        "openbao_github_permission_set_changes": [],
    }) == "No GitHub permission set writes are needed."


def test_check_mode_reports_the_single_missing_set_and_never_posts():
    desired = {"name": SELECTED_NAME, "installation_id": 101}
    pending = changes([{"status": 404, "item": desired}])
    report = task("Report GitHub permission sets that would be written in check mode", PERMISSION_SETS)
    assert render(report["ansible.builtin.debug"]["msg"], {
        "openbao_github_permission_set_changes": pending,
    }) == f"Would write GitHub permission sets: {SELECTED_NAME}"
    write = task("Reconcile the GitHub token permission sets", PERMISSION_SETS)
    check_guard = next(gate for gate in write["when"] if "ansible_check_mode" in gate)
    report_guard = next(gate for gate in report["when"] if "ansible_check_mode" in gate)
    assert not condition(check_guard, {"ansible_check_mode": True})
    assert condition(check_guard, {"ansible_check_mode": False})
    assert condition(report_guard, {"ansible_check_mode": True})
    assert not condition(report_guard, {"ansible_check_mode": False})


def test_github_only_selection_leaves_every_other_object_writer_empty():
    selected = {
        kind: resolve(SELECTION, kind)[1]
        for kind in ("policies", "approles", "ssh_roles", "rotation_exempt")
    }
    assert selected == {kind: [] for kind in selected}

    policy_write = task(
        "Write the RBAC policies that are missing or changed",
        ROLE / "tasks/init/08b-rbac-policy-writes.yml",
    )
    assert render(policy_write["loop"], {"openbao_rbac_policy_targets": selected["policies"]}) == []

    approle_writers = [
        ("10-approles.yml", "Create the missing AppRoles bound to their policy"),
        ("10-approles.yml", "Reconcile token_policies on existing AppRoles"),
        ("10c-approle-ttl-bounds.yml", "Reconcile AppRole TTL and token bounds on existing AppRoles"),
    ]
    for filename, name in approle_writers:
        assert render(task(name, ROLE / "tasks/init" / filename)["loop"], {
            "openbao_approle_config_targets": selected["approles"],
            "openbao_manageable_approles": [{"name": "unselected"}],
            "openbao_approle_checks": {"results": [{"item": {"name": "unselected"}, "rc": 1}]},
        }) == []

    ssh_write = task("Reconcile the SSH signing roles", ROLE / "tasks/init/07-ssh-ca-engine.yml")
    assert render(ssh_write["loop"], {
        "openbao_selected_objects": selected,
        "openbao_ssh_role_checks": {"results": []},
    }) == []
    rotation_write = task(
        "Tag operator-declared rotation-exempt paths (write-if-changed)", ROLE / "tasks/init.yml",
    )
    assert render(rotation_write["loop"], {"openbao_selected_objects": selected}) == []
