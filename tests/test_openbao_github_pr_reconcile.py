"""PR reconciliation mints only pinned owner tokens from the raw everyday endpoint."""

import re
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.nativetypes import NativeEnvironment


ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main"
TASKS = ROOT / "roles/openbao/tasks/init/09c-github-oidc.yml"
POLICIES = DEFAULTS / "07c-base-policies.yml"
TEMPLATES = ROOT / "roles/openbao/templates"
RBAC = ROOT / "roles/openbao/tasks/init/08-rbac-policies.yml"
REPOSITORY_KEY = "OPENBAO_GITHUB_PR_RECONCILE_REPOSITORY"
OWNERS_KEY = "OPENBAO_GITHUB_PR_RECONCILE_OWNERS"
CALLER_OWNERS_KEY = "OPENBAO_GITHUB_PR_RECONCILE_CALLER_OWNERS"


def _defaults(name):
    return yaml.safe_load((DEFAULTS / name).read_text(encoding="utf-8"))


def _render_defaults(env):
    environment = NativeEnvironment()
    # A process environment value must not reach the role: inputs come only from the platform env document.
    environment.globals["lookup"] = lambda plugin, key: "process-env-must-be-ignored"
    environment.filters["bool"] = bool
    defaults = _defaults("05f-pr-reconcile.yml")
    for name, value in defaults.items():
        if isinstance(value, str) and "{{" in value:
            defaults[name] = environment.from_string(value).render(**defaults, openbao_platform_env=env)
    return defaults


def _retired(defaults):
    environment = NativeEnvironment()
    environment.filters["bool"] = bool
    expression = _defaults("07c-approle-undeclared-exceptions.yml")["openbao_retired_policies"]
    return environment.from_string(expression).render(
        **defaults,
        openbao_roster_key_reader_retired_names=[],
        openbao_roster_owned_mcp_deny_retired_names=[],
    )


def _find_task(tasks, name):
    for task in tasks:
        if task.get("name") == name:
            return task
        nested = task.get("block", [])
        if nested and (found := _find_task(nested, name)):
            return found
    return None


def _render_policy(defaults):
    environment = Environment(loader=FileSystemLoader(TEMPLATES))
    environment.filters["comment"] = lambda value: "# " + str(value)
    return environment.get_template("pr-reconcile-sweep-policy.hcl.j2").render(
        ansible_managed="managed",
        openbao_github_everyday_mount="github",
        openbao_pr_reconcile_owners=defaults["openbao_pr_reconcile_owners"],
        openbao_github_pr_reconcile_permissions=defaults[
            "openbao_github_pr_reconcile_permissions"
        ],
    )


def test_inputs_enable_reconcile_and_build_workflow_ref():
    defaults = _render_defaults({
        REPOSITORY_KEY: "example-org/example-repo",
        OWNERS_KEY: " example-org, , example-other ",
    })
    assert defaults["openbao_github_pr_reconcile_enabled"] is True
    assert defaults["openbao_pr_reconcile_owners"] == ["example-org", "example-other"]
    assert defaults["openbao_github_pr_reconcile_workflow_ref"] == (
        "example-org/example-repo/.github/workflows/pr-reconcile-sweep.yml@refs/heads/main"
    )
    assert defaults["openbao_pr_reconcile_policies"] == [
        {"name": "pr-reconcile-sweep", "template": "pr-reconcile-sweep-policy.hcl.j2"}
    ]
    assert defaults["openbao_github_pr_reconcile_policy_name"] not in _retired(defaults)
    assert defaults["openbao_github_pr_reconcile_permissions"] == {
        "actions": "write",
        "checks": "read",
        "contents": "write",
        "pull_requests": "write",
        "statuses": "write",
    }


def test_missing_inputs_disable_reconcile_and_warn():
    for env in (
        {REPOSITORY_KEY: "example-org/example-repo"},
        {OWNERS_KEY: "example-org"},
        {},
    ):
        defaults = _render_defaults(env)
        assert defaults["openbao_github_pr_reconcile_enabled"] is False
        # Not declared, retired (deleted if live), and never rendered as an empty allow-list.
        assert defaults["openbao_pr_reconcile_policies"] == []
        assert defaults["openbao_github_pr_reconcile_policy_name"] in _retired(defaults)
        rendered = _render_policy(defaults)
        assert '"org_name" = []' not in rendered
        if not defaults["openbao_pr_reconcile_owners"]:
            assert re.findall(r'(?m)^path ', rendered) == []

    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    remove = _find_task(tasks, "Remove the pr-reconcile-sweep OIDC role while its inputs are unset")
    assert remove is not None
    assert " ".join(remove["ansible.builtin.command"]["cmd"].split()) == (
        "bao delete auth/{{ openbao_github_oidc_auth_path }}/role/"
        "{{ openbao_github_pr_reconcile_policy_name }}"
    )
    assert "not (openbao_github_pr_reconcile_enabled | bool)" in remove["when"]
    assert "(openbao_github_oidc_pr_reconcile_role_current.rc | default(1)) == 0" in remove["when"]
    read = _find_task(tasks, "Read the pr-reconcile-sweep OIDC role")
    assert read["when"] == [
        "openbao_select | default({}) | length == 0 or openbao_github_pr_reconcile_policy_name\n"
        "   in ((openbao_selected_objects | default({})).get('github_oidc_roles', [])\n"
        "       | map(attribute='name') | list)",
        "openbao_bootstrap_token is defined",
    ]

    warning = _find_task(
        yaml.safe_load(RBAC.read_text(encoding="utf-8")),
        "Warn when PR reconcile configuration is incomplete",
    )
    assert warning is not None
    assert REPOSITORY_KEY in warning["ansible.builtin.debug"]["msg"]
    assert OWNERS_KEY in warning["ansible.builtin.debug"]["msg"]
    assert "not (openbao_github_pr_reconcile_enabled | bool)" in warning["when"]


def test_policy_pins_owner_names_and_permission_map_on_the_raw_endpoint():
    defaults = _render_defaults(
        {REPOSITORY_KEY: "example-org/example-repo", OWNERS_KEY: "example-org,example-other"}
    )
    rendered = _render_policy(defaults)
    paths = re.findall(r'(?m)^path "([^"]+)" \{', rendered)
    assert paths == ["github/token"]
    assert 'capabilities = ["create", "update"]' in rendered
    assert 'required_parameters = ["org_name", "permissions"]' in rendered
    owners = ", ".join(f'"{owner}"' for owner in defaults["openbao_pr_reconcile_owners"])
    assert f'"org_name" = [{owners}]' in rendered
    assert (
        '"permissions" = [{ "actions" = "write", "checks" = "read", "contents" = "write", '
        '"pull_requests" = "write", "statuses" = "write" }]'
    ) in rendered
    assert '"installation_id" = []' in rendered
    assert '"repository_ids" = []' in rendered
    assert '"repositories"' not in rendered

    policies = yaml.safe_load(POLICIES.read_text(encoding="utf-8"))
    assert not [
        item for item in policies["openbao_base_policies_static"]
        if item["name"] == "{{ openbao_github_pr_reconcile_policy_name }}"
    ]
    assert "+ openbao_pr_reconcile_policies" in policies["openbao_base_policies"]


def test_oidc_role_has_exact_claims_one_policy_short_batch_token_and_drift_guard():
    defaults = _render_defaults(
        {REPOSITORY_KEY: "example-org/example-repo", OWNERS_KEY: "example-org"}
    )
    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    read = _find_task(tasks, "Read the pr-reconcile-sweep OIDC role")
    write = _find_task(tasks, "Reconcile the pr-reconcile-sweep OIDC role")
    assert read is not None
    assert write is not None

    assert defaults["openbao_github_pr_reconcile_policy_name"] == "pr-reconcile-sweep"
    assert defaults["openbao_github_pr_reconcile_audience"] == "openbao"
    assert defaults["openbao_github_pr_reconcile_ref"] == "refs/heads/main"
    assert defaults["openbao_github_pr_reconcile_event_names"] == [
        "schedule", "workflow_dispatch"
    ]
    assert defaults["openbao_github_pr_reconcile_runner_environment"] == "self-hosted"
    assert defaults["openbao_github_pr_reconcile_token_ttl"] == "5m"
    assert defaults["openbao_github_pr_reconcile_token_max_ttl"] == "10m"

    assert write["vars"]["_pr_reconcile_role_claims"] == {
        "repository": "{{ openbao_github_pr_reconcile_repository }}",
        "workflow_ref": "{{ openbao_github_pr_reconcile_workflow_ref }}",
        "ref": "{{ openbao_github_pr_reconcile_ref }}",
        "event_name": "{{ openbao_github_pr_reconcile_event_names }}",
        "runner_environment": "{{ openbao_github_pr_reconcile_runner_environment }}",
    }
    payload = write["ansible.builtin.command"]["stdin"]
    assert "'role_type': 'jwt'" in payload
    assert "'user_claim': 'workflow_ref'" in payload
    assert "job_workflow_ref" not in payload
    assert "job_workflow_ref" not in write["vars"]["_pr_reconcile_role_claims"]
    assert "'bound_audiences': [openbao_github_pr_reconcile_audience]" in payload
    assert "'bound_claims_type': 'string'" in payload
    assert "'token_policies': openbao_github_pr_reconcile_policy_name," in payload
    assert "'token_no_default_policy': true" in payload
    assert "'token_type': 'batch'" in payload
    assert "'token_ttl': openbao_github_pr_reconcile_token_ttl" in payload
    assert "'token_max_ttl': openbao_github_pr_reconcile_token_max_ttl" in payload

    assert "openbao_github_pr_reconcile_enabled | bool" in write["when"]
    drift_guard = write["when"][-1]
    assert "openbao_github_oidc_pr_reconcile_role_current.rc | default(1)" in drift_guard
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
    assert "changed_when" in write


def test_existing_github_sets_policies_and_oidc_roles_keep_their_own_tiers():
    github = _defaults("03-github-engine.yml")
    app_mounts = _defaults("03b-github-app-mounts.yml")
    policies = yaml.safe_load(POLICIES.read_text(encoding="utf-8"))[
        "openbao_base_policies_static"
    ]
    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))

    for document in (github, app_mounts):
        assert "pr_reconcile" not in yaml.safe_dump(document)

    existing_policy_templates = {
        "{{ openbao_github_docs_publisher_policy_name }}": "github-docs-publisher-policy.hcl.j2",
        "{{ openbao_github_ci_resolver_policy_name }}": "github-ci-resolver-policy.hcl.j2",
        "{{ openbao_github_git_mirror_policy_name }}": "git-mirror-policy.hcl.j2",
        "{{ openbao_uicheck_policy_name }}": "uicheck-policy.hcl.j2",
    }
    for name, template in existing_policy_templates.items():
        assert next(item for item in policies if item["name"] == name)["template"] == template

    for role_name in (
        "Reconcile the docs-publisher OIDC role",
        "Reconcile the uicheck OIDC role",
        "Reconcile the ci-ai-review OIDC role",
        "Reconcile the ci-evals OIDC role",
    ):
        assert _find_task(tasks, role_name) is not None


def _render_caller_policy(defaults):
    environment = Environment(loader=FileSystemLoader(TEMPLATES))
    environment.filters["comment"] = lambda value: "# " + str(value)
    return environment.get_template("pr-reconcile-policy.hcl.j2").render(
        ansible_managed="managed",
        openbao_github_everyday_mount="github",
        openbao_github_pr_reconcile_caller_owners=defaults[
            "openbao_github_pr_reconcile_caller_owners"
        ],
        openbao_github_pr_reconcile_caller_permissions=defaults[
            "openbao_github_pr_reconcile_caller_permissions"
        ],
    )


def test_caller_owner_list_alone_declares_the_caller_policy():
    defaults = _render_defaults({CALLER_OWNERS_KEY: " example-org, , example-other "})
    assert defaults["openbao_github_pr_reconcile_caller_enabled"] is True
    assert defaults["openbao_github_pr_reconcile_enabled"] is False
    assert defaults["openbao_github_pr_reconcile_caller_owners"] == ["example-org", "example-other"]
    assert defaults["openbao_pr_reconcile_policies"] == [
        {"name": "pr-reconcile", "template": "pr-reconcile-policy.hcl.j2"}
    ]
    retired = _retired(defaults)
    assert "pr-reconcile" not in retired
    assert "pr-reconcile-sweep" in retired

    both = _render_defaults({
        REPOSITORY_KEY: "example-org/example-repo",
        OWNERS_KEY: "example-org",
        CALLER_OWNERS_KEY: "example-org",
    })
    assert [item["name"] for item in both["openbao_pr_reconcile_policies"]] == [
        "pr-reconcile-sweep", "pr-reconcile"
    ]
    assert not {"pr-reconcile-sweep", "pr-reconcile"} & set(_retired(both))


def test_empty_caller_owner_list_retires_the_caller_policy_and_removes_its_role():
    defaults = _render_defaults({REPOSITORY_KEY: "example-org/example-repo", OWNERS_KEY: "example-org"})
    assert defaults["openbao_github_pr_reconcile_caller_enabled"] is False
    assert "pr-reconcile" in _retired(defaults)
    assert re.findall(r'(?m)^path ', _render_caller_policy(defaults)) == []

    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    remove = _find_task(tasks, "Remove the pr-reconcile OIDC role while its owner list is empty")
    assert " ".join(remove["ansible.builtin.command"]["cmd"].split()) == (
        "bao delete auth/{{ openbao_github_oidc_auth_path }}/role/"
        "{{ openbao_github_pr_reconcile_caller_policy_name }}"
    )
    assert remove["when"] == [
        "openbao_select | default({}) | length == 0",
        "openbao_bootstrap_token is defined",
        "not (openbao_github_pr_reconcile_caller_enabled | bool)",
        "(openbao_github_oidc_pr_reconcile_caller_role_current.rc | default(1)) == 0",
    ]


def test_caller_policy_requires_repositories_and_pins_owners_and_a_narrower_permission_map():
    defaults = _render_defaults({CALLER_OWNERS_KEY: "example-org,example-other"})
    caller = defaults["openbao_github_pr_reconcile_caller_permissions"]
    sweep = defaults["openbao_github_pr_reconcile_permissions"]
    assert caller == {"contents": "write", "pull_requests": "write", "statuses": "write"}
    # Never wider than the sweep: every scope is one the sweep holds at the same level.
    assert all(sweep.get(name) == level for name, level in caller.items())
    rendered = _render_caller_policy(defaults)
    assert re.findall(r'(?m)^path "([^"]+)" \{', rendered) == ["github/token"]
    assert 'capabilities = ["create", "update"]' in rendered
    assert 'required_parameters = ["org_name", "permissions", "repositories"]' in rendered
    assert '"org_name" = ["example-org", "example-other"]' in rendered
    assert (
        '"permissions" = [{ "contents" = "write", "pull_requests" = "write", "statuses" = "write" }]'
    ) in rendered
    assert '"repositories" = []' in rendered
    assert '"installation_id" = []' in rendered
    assert '"repository_ids" = []' in rendered
    for scope in ('"actions"', '"checks"', '"issues"', '"workflows"'):
        assert scope not in rendered


def test_caller_oidc_role_binds_the_reusable_workflow_owners_push_and_runner():
    defaults = _render_defaults({CALLER_OWNERS_KEY: "example-org"})
    assert defaults["openbao_github_pr_reconcile_caller_policy_name"] == "pr-reconcile"
    assert defaults["openbao_github_pr_reconcile_caller_workflow_refs"] == [
        "JacobPEvans/.github-ai/.github/workflows/pr-reconcile.yml@refs/heads/main",
        "JacobPEvans/.github-ai/.github/workflows/pr-reconcile.yml@refs/tags/v*",
    ]
    assert defaults["openbao_github_pr_reconcile_caller_event_names"] == ["push"]
    assert defaults["openbao_github_pr_reconcile_caller_refs"] == [
        "refs/heads/develop", "refs/heads/main"
    ]

    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    read = _find_task(tasks, "Read the pr-reconcile OIDC role")
    guard = _find_task(tasks, "Reconcile the pr-reconcile OIDC role")
    write = _find_task(tasks, "Write the pr-reconcile OIDC role")
    assert read["register"] == "openbao_github_oidc_pr_reconcile_caller_role_current"
    assert guard["vars"]["_pr_reconcile_caller_role_claims"] == {
        "job_workflow_ref": "{{ openbao_github_pr_reconcile_caller_workflow_refs }}",
        "repository_owner": "{{ openbao_github_pr_reconcile_caller_owners }}",
        "event_name": "{{ openbao_github_pr_reconcile_caller_event_names }}",
        "ref": "{{ openbao_github_pr_reconcile_caller_refs }}",
        "runner_environment": "{{ openbao_github_pr_reconcile_runner_environment }}",
    }
    payload = write["ansible.builtin.command"]["stdin"]
    for fragment in (
        "'role_type': 'jwt'",
        "'user_claim': 'job_workflow_ref'",
        "'bound_audiences': [openbao_github_pr_reconcile_audience]",
        "'bound_claims_type': 'glob'",
        "'token_policies': openbao_github_pr_reconcile_caller_policy_name,",
        "'token_no_default_policy': true",
        "'token_type': 'batch'",
        "'token_ttl': openbao_github_pr_reconcile_token_ttl",
        "'token_max_ttl': openbao_github_pr_reconcile_token_max_ttl",
    ):
        assert fragment in payload

    assert "openbao_github_pr_reconcile_caller_enabled | bool" in guard["when"]
    drift_guard = guard["when"][-1]
    assert "openbao_github_oidc_pr_reconcile_caller_role_current.rc | default(1)" in drift_guard
    for field in (
        ".role_type", ".bound_audiences", ".bound_claims", ".bound_claims_type", ".user_claim",
        ".token_policies", ".token_no_default_policy", ".token_type", ".token_ttl", ".token_max_ttl",
    ):
        assert f"_pr_reconcile_caller_role_live{field}" in drift_guard


def test_caller_oidc_role_write_is_named_in_check_mode_and_its_error_is_shown():
    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    guard = _find_task(tasks, "Reconcile the pr-reconcile OIDC role")
    report, write, refused = guard["block"]

    assert report["when"] == "ansible_check_mode"
    assert "token_policies {{ openbao_github_pr_reconcile_caller_policy_name }}" in report[
        "ansible.builtin.debug"]["msg"]

    assert write["name"] == "Write the pr-reconcile OIDC role"
    assert write["register"] == "openbao_github_oidc_pr_reconcile_caller_role_write"
    assert write["no_log"] is True
    assert write["failed_when"] is False

    assert "ansible.builtin.fail" in refused
    assert refused["when"] == "(openbao_github_oidc_pr_reconcile_caller_role_write.rc | default(0)) != 0"
    assert "openbao_github_oidc_pr_reconcile_caller_role_write.stderr" in refused[
        "ansible.builtin.fail"]["msg"]
