"""OpenHands org-scoped GitHub write sets and OIDC role stay narrowly bound."""

import re
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.nativetypes import NativeEnvironment


ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main"
TASKS = ROOT / "roles/openbao/tasks/init/09c-github-oidc.yml"
TEMPLATES = ROOT / "roles/openbao/templates"
OPENHANDS_PERMISSIONS = {
    "actions": "read",
    "checks": "read",
    "contents": "write",
    "metadata": "read",
    "pull_requests": "write",
}


def _defaults(name):
    return yaml.safe_load((DEFAULTS / name).read_text(encoding="utf-8"))


def _render(expression, values):
    environment = NativeEnvironment()
    environment.filters["bool"] = bool
    environment.filters["combine"] = lambda value, other: {**value, **other}
    environment.filters["regex_replace"] = lambda value, pattern, replacement: re.sub(
        pattern, replacement, value
    )
    return environment.from_string(expression).render(**values)


def _write_sets(orgs, app_id="12345"):
    defaults = _defaults("03-github-engine.yml")
    route = {
        "prefix": "openhands-write",
        "mount": "github-openhands",
        "app_id": app_id,
        "orgs": orgs,
        "workflows": [],
        "permissions": OPENHANDS_PERMISSIONS,
        "token_ttl": "5m",
        "token_max_ttl": "10m",
    }
    values = {
        **defaults,
        "openbao_github_write_routes": [route],
    }
    return _render(
        defaults["openbao_github_write_permission_sets"], values
    )


def _oidc_defaults(orgs, workflows, app_id="12345"):
    defaults = _defaults("05f-pr-reconcile.yml")
    route = {
        "prefix": "openhands-write",
        "mount": "github-openhands",
        "app_id": app_id,
        "orgs": orgs,
        "workflows": workflows,
        "permissions": OPENHANDS_PERMISSIONS,
        "token_ttl": "5m",
        "token_max_ttl": "10m",
    }
    values = {
        **defaults,
        "openbao_github_openhands_write_orgs": orgs,
        "openbao_github_openhands_write_workflows": workflows,
        "openbao_github_openhands_app_id": app_id,
        "openbao_github_write_routes": [route],
        "openbao_github_openhands_write_permission_sets": _write_sets(orgs, app_id),
        "openbao_github_write_permission_sets": _write_sets(orgs, app_id),
        "openbao_github_write_workflow_ref_suffix": "@*",
        "openbao_github_openhands_write_set_prefix": "openhands-write",
        "openbao_github_oidc_audience": "openbao",
    }
    values["openbao_github_write_oidc_roles"] = _render(
        defaults["openbao_github_write_oidc_roles"], values
    )
    for name in (
        "openbao_github_openhands_write_audience",
        "openbao_github_write_audience",
        "openbao_github_openhands_write_token_ttl",
        "openbao_github_openhands_write_token_max_ttl",
        "openbao_github_openhands_write_oidc_roles",
    ):
        values[name] = _render(defaults[name], values)
    return values


def _policy_defaults(orgs, app_id="12345"):
    defaults = _defaults("07c-base-policies.yml")
    route = {
        "prefix": "openhands-write",
        "mount": "github-openhands",
        "app_id": app_id,
        "orgs": orgs,
        "workflows": [],
        "permissions": OPENHANDS_PERMISSIONS,
        "token_ttl": "5m",
        "token_max_ttl": "10m",
    }
    expression = defaults["openbao_github_write_policies"]
    return _render(
        expression,
        {
            **defaults,
            "openbao_github_write_routes": [route],
            "openbao_github_write_permission_sets": _write_sets(orgs, app_id),
        },
    )


def _find_task(name):
    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    return next(task for task in tasks if task.get("name") == name)


def test_write_sets_are_exact_org_scoped_and_omitted_without_inputs():
    assert _write_sets([]) == []
    assert _write_sets(["ExampleOrg"], app_id="") == []

    sets = _write_sets(["ExampleOrg", "example-org"])
    assert [item["name"] for item in sets] == [
        "openhands-write-exampleorg",
        "openhands-write-example-org",
    ]
    assert [item["org_name"] for item in sets] == ["ExampleOrg", "example-org"]
    assert all(item["tier"] == "openhands-write" for item in sets)
    assert all(
        item["permissions"]
        == {
            "actions": "read",
            "checks": "read",
            "contents": "write",
            "metadata": "read",
            "pull_requests": "write",
        }
        for item in sets
    )
    assert all("installation_id" not in item for item in sets)

    engine = _defaults("03-github-engine.yml")
    mounts = _render(
        engine["openbao_github_permission_sets"],
        {
            "openbao_github_admin_permission_sets": [],
            "openbao_github_read_permission_sets": [],
            "openbao_github_personal_permission_sets": [],
            "openbao_github_openhands_permission_sets": [],
            "openbao_github_write_permission_sets_with_mounts": [
                {**item, "mount": "github-openhands"} for item in sets
            ],
            "openbao_github_openhands_mount": "github-openhands",
            "openbao_github_pepper_permission_sets": [],
            "openbao_github_everyday_mount": "github",
            "openbao_github_personal_mount": "github-personal",
            "openbao_github_pepper_mount": "github-pepper",
        },
    )
    assert [item["mount"] for item in mounts] == ["github-openhands"] * 2

    engine_values = {
        **engine,
        "openbao_github_openhands_installation_id": "303",
        "openbao_github_openhands_app_id": "12345",
        "openbao_github_openhands_pilot_repos": ["fixture-repo"],
    }
    pilot_sets = _render(
        engine["openbao_github_openhands_permission_sets"], engine_values
    )
    assert len(pilot_sets) == 1
    assert pilot_sets[0]["name"] == "openhands-pilot"
    assert pilot_sets[0]["repositories"] == ["fixture-repo"]


def test_openhands_write_policy_is_only_declared_for_configured_sets():
    engine = _defaults("03-github-engine.yml")
    unscheduled = _render(
        engine["openbao_unscheduled_empty_policy_names"],
        {
            "openbao_github_ci_resolver_repos": [],
            "openbao_github_ci_resolver_policy_name": "github-ci-resolver",
        },
    )
    assert unscheduled == ["github-ci-resolver"]
    assert _policy_defaults([]) == []

    policies = _policy_defaults(["ExampleOrg", "example-org"])
    assert [item["name"] for item in policies] == [
        "openhands-write-exampleorg",
        "openhands-write-example-org",
    ]
    assert [item["org"] for item in policies] == ["ExampleOrg", "example-org"]
    assert [item["set"]["name"] for item in policies] == [item["name"] for item in policies]

    environment = Environment(loader=FileSystemLoader(TEMPLATES))
    environment.filters["comment"] = lambda value: "# " + str(value)
    template = environment.get_template(policies[0]["template"])
    expected_paths = [
        "github-openhands/token/openhands-write-exampleorg",
        "github-openhands/token/openhands-write-example-org",
    ]
    for index, policy in enumerate(policies):
        rendered = template.render(
            ansible_managed="managed",
            item=policy,
        )
        paths = re.findall(
            r'(?m)^path "([^"]+)" \{\n  capabilities = \[([^\]]+)\]\n\}',
            rendered,
        )
        assert paths == [(expected_paths[index], '"create", "read", "update"')]
        assert all(path != expected_paths[1 - index] for path, _ in paths)


def test_openhands_pilot_policy_stays_scoped_to_pilot_set():
    environment = Environment(loader=FileSystemLoader(TEMPLATES))
    environment.filters["comment"] = lambda value: "# " + str(value)
    pilot_policy = environment.get_template("openhands-policy.hcl.j2").render(
        ansible_managed="managed",
        openbao_kv_mount="secret",
        openbao_github_permission_sets=[
            {
                "name": "openhands-pilot",
                "mount": "github-openhands",
                "tier": "openhands",
            },
            {
                "name": "openhands-write-exampleorg",
                "mount": "github-openhands",
                "tier": "openhands-write",
            },
            {
                "name": "openhands-write-example-org",
                "mount": "github-openhands",
                "tier": "openhands-write",
            },
        ],
    )
    assert 'path "github-openhands/token/openhands-pilot"' in pilot_policy
    assert 'path "github-openhands/token/openhands-write-exampleorg"' not in pilot_policy
    assert 'path "github-openhands/token/openhands-write-example-org"' not in pilot_policy
    assert re.findall(
        r'(?m)^path "([^"]+)" \{\n  capabilities = \[([^\]]+)\]\n\}',
        pilot_policy,
    ) == [
        (
            "github-openhands/token/openhands-pilot",
            '"create", "read", "update"',
        ),
        ("secret/data/apps/openhands", '"read"'),
        ("secret/metadata/apps/openhands", '"read"'),
        ("secret/data/apps/openhands-vikunja", '"read"'),
        ("secret/metadata/apps/openhands-vikunja", '"read"'),
    ]


def test_openhands_write_oidc_roles_are_declared_only_with_all_inputs():
    workflow = "example-org/example-repo/.github/workflows/write.yml"
    unset_orgs = _oidc_defaults([], [workflow])
    assert unset_orgs["openbao_github_openhands_write_oidc_roles"] == []
    assert _oidc_defaults(["ExampleOrg"], [])["openbao_github_openhands_write_oidc_roles"] == []
    assert _oidc_defaults(
        ["ExampleOrg"], [workflow], app_id=""
    )["openbao_github_openhands_write_oidc_roles"] == []

    values = _oidc_defaults(["ExampleOrg", "example-org"], [workflow])
    roles = values["openbao_github_openhands_write_oidc_roles"]
    assert [(role["name"], role["org"], role["set"]["name"]) for role in roles] == [
        ("openhands-write-exampleorg", "ExampleOrg", "openhands-write-exampleorg"),
        ("openhands-write-example-org", "example-org", "openhands-write-example-org"),
    ]
    assert values["openbao_github_openhands_write_workflow_ref_suffix"] == "@*"
    assert values["openbao_github_write_audience"] == values[
        "openbao_github_openhands_write_audience"
    ]
    assert unset_orgs["openbao_github_openhands_write_token_ttl"] == "5m"
    assert unset_orgs["openbao_github_openhands_write_token_max_ttl"] == "10m"


def test_empty_org_list_declares_no_roles_policies_sets_or_write_policy_name():
    workflow = "example-org/example-repo/.github/workflows/write.yml"
    assert _write_sets([]) == []
    assert _oidc_defaults([], [workflow])["openbao_github_openhands_write_oidc_roles"] == []
    assert _policy_defaults([]) == []

    engine = _defaults("03-github-engine.yml")
    unscheduled = _render(
        engine["openbao_unscheduled_empty_policy_names"],
        {
            "openbao_github_ci_resolver_repos": [],
            "openbao_github_ci_resolver_policy_name": "github-ci-resolver",
        },
    )
    assert unscheduled == ["github-ci-resolver"]
    assert not any("openhands" in name for name in unscheduled)


def test_each_openhands_write_oidc_role_is_bound_to_one_org_and_compares_all_fields():
    workflows = [
        "example-org/example-repo/.github/workflows/write.yml",
        "example-org/example-repo/.github/workflows/build.yml",
    ]
    values = _oidc_defaults(["ExampleOrg", "example-org"], workflows)
    roles = values["openbao_github_openhands_write_oidc_roles"]
    task = _find_task("Reconcile each GitHub write OIDC role")
    payload = task["ansible.builtin.command"]["stdin"]
    claims = task["vars"]["_github_write_role_claims"]
    route = {
        "prefix": "openhands-write",
        "mount": "github-openhands",
        "app_id": "12345",
        "orgs": ["ExampleOrg", "example-org"],
        "workflows": workflows,
        "permissions": OPENHANDS_PERMISSIONS,
        "token_ttl": "5m",
        "token_max_ttl": "10m",
    }

    assert "job_workflow_ref" in claims
    assert "openbao_github_write_workflow_ref_suffix" in claims[
        "job_workflow_ref"
    ]
    assert "repository_owner" in claims
    assert claims["repository_owner"] == "{{ [item.org] }}"
    for role in roles:
        rendered_claims = _render(
            "{{ claims }}",
            {
                "claims": {
                    "job_workflow_ref": _render(
                        claims["job_workflow_ref"],
                        {
                            "_github_write_route": route,
                            "openbao_github_write_workflow_ref_suffix": "@*",
                        },
                    ),
                    "repository_owner": _render(
                        claims["repository_owner"], {"item": role}
                    ),
                }
            },
        )
        assert rendered_claims == {
            "job_workflow_ref": [f"{workflow}@*" for workflow in workflows],
            "repository_owner": [role["org"]],
        }
    assert "'role_type': 'jwt'" in payload
    assert "'user_claim': 'job_workflow_ref'" in payload
    assert "'bound_claims_type': 'glob'" in payload
    assert "'token_policies': [item.name]" in payload
    assert "'token_no_default_policy': true" in payload
    assert "'token_type': 'batch'" in payload
    assert "openbao_github_write_audience" in payload
    assert "_github_write_route.token_ttl" in payload
    assert "_github_write_route.token_max_ttl" in payload

    drift_guard = task["when"][-1]
    for field in (
        ".role_type",
        ".bound_audiences",
        ".bound_claims",
        ".bound_claims_type",
        ".user_claim",
        ".token_policies",
        ".token_no_default_policy",
        ".token_type",
        ".token_ttl",
        ".token_max_ttl",
    ):
        assert field in drift_guard

    read = _find_task("Read each GitHub write OIDC role")
    assert "openbao_github_oidc_role_targets" in read["vars"]
    assert "openbao_github_oidc_role_targets" in " ".join(read["when"])
    assert "openbao_select | default({}) | length == 0" in " ".join(task["when"])
    assert task["loop"] == read["loop"] == "{{ openbao_github_write_oidc_roles }}"
    assert task["loop_control"]["label"] == read["loop_control"]["label"] == "{{ item.name }}"
    assert task["loop_control"]["index_var"] == "openbao_github_write_role_index"
    live_role = task["vars"]["_github_write_role_live"]
    assert "openbao_github_oidc_write_roles_current.results[" in live_role
    assert "openbao_github_write_role_index" in live_role
    assert "openbao_github_oidc_write_roles_current.results[" in drift_guard
    assert "openbao_github_write_role_index" in drift_guard


def test_preexisting_oidc_tasks_are_gated_before_register_dependencies():
    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    first_openhands_task = next(
        index
        for index, task in enumerate(tasks)
        if task.get("name") == "Read each GitHub write OIDC role"
    )
    full_run_guard = "openbao_select | default({}) | length == 0"

    for task in tasks[:first_openhands_task]:
        assert task["when"][0] == full_run_guard, task["name"]

    enable = _find_task("Enable the GitHub Actions OIDC auth method")
    assert enable["when"][0] == full_run_guard
