"""Runner registration sets are limited to explicitly configured owners."""

from pathlib import Path
import re

from jinja2 import Environment, StrictUndefined
from jinja2.nativetypes import NativeEnvironment
import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main/03-github-engine.yml"
TASKS = ROOT / "roles/openbao/tasks/init/05-github-engine.yml"
TEMPLATE = ROOT / "roles/openbao/templates/github-runner-policy.hcl.j2"
TEMPLATES = ROOT / "roles/openbao/templates"
OWNERS_KEY = "OPENBAO_GITHUB_RUNNER_REGISTER_OWNERS"
BASE_RUNNER_SET = {
    "name": "runner-register-example-base",
    "tier": "runner",
    "installation_id": "101",
    "permissions": {"organization_self_hosted_runners": "write"},
}


def _render(expression, variables):
    return NativeEnvironment().from_string(expression).render(**variables)


def _resolve_templates(value, variables):
    if isinstance(value, dict):
        return {key: _resolve_templates(item, variables) for key, item in value.items()}
    if isinstance(value, list):
        return [_resolve_templates(item, variables) for item in value]
    if isinstance(value, str) and ("{{" in value or "{%" in value):
        return _render(value, variables)
    return value


def _runner_defaults(owner_csv, installations, *, use_default_base=False):
    defaults = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))
    platform_env = {
        "OPENBAO_GITHUB_ADMIN_DRYVIST_INSTALLATION_ID": "101",
        "OPENBAO_GITHUB_DRYVIST_INSTALLATION_ID": "404",
    }
    if owner_csv is not None:
        platform_env[OWNERS_KEY] = owner_csv
    variables = {
        **defaults,
        "openbao_platform_env": platform_env,
        "openbao_github_base_permission_sets": [BASE_RUNNER_SET],
        "openbao_github_org_secrets_installations": installations,
    }
    if use_default_base:
        variables["openbao_github_dryvist_installation_id"] = _render(
            defaults["openbao_github_dryvist_installation_id"], variables
        )
        variables["openbao_github_base_permission_sets"] = _resolve_templates(
            defaults["openbao_github_base_permission_sets"], variables
        )
    for name in (
        "openbao_github_runner_register_owners",
        "openbao_github_runner_register_permission_sets",
        "openbao_github_runner_register_missing_owners",
    ):
        variables[name] = _render(defaults[name], variables)
    return variables


def _admin_sets(variables):
    composition = {
        "openbao_github_base_permission_sets": variables[
            "openbao_github_base_permission_sets"
        ],
        "openbao_github_org_secrets_permission_sets": [],
        "openbao_github_docs_publisher_permission_sets": [],
        "openbao_github_dify_pr_automation_permission_sets": [],
        "openbao_github_ci_resolver_permission_sets": [],
        "openbao_github_router_snapshot_permission_sets": [],
        "openbao_github_git_mirror_permission_sets": [],
        "openbao_github_role_eval_status_permission_sets": [],
        "openbao_github_workflows_write_permission_sets": [],
        "openbao_github_dispatch_permission_sets": [],
    }
    return _render(
        variables["openbao_github_admin_permission_sets"],
        {**variables, **composition},
    )


def _policy_inputs():
    variables = _runner_defaults(
        "example-org,example-other",
        [
            {"name": "dryvist", "installation_id": "101"},
            {"name": "example-org", "installation_id": "202"},
            {"name": "example-other", "installation_id": "303"},
        ],
        use_default_base=True,
    )
    app_defaults = yaml.safe_load(
        (DEFAULTS.parent / "03b-github-app-mounts.yml").read_text(encoding="utf-8")
    )
    variables["openbao_github_everyday_mount"] = app_defaults[
        "openbao_github_everyday_mount"
    ]
    variables["openbao_github_everyday_dryvist_installation_id"] = _render(
        app_defaults["openbao_github_everyday_dryvist_installation_id"], variables
    )
    read_sets = _resolve_templates(
        app_defaults["openbao_github_read_permission_sets"], variables
    )
    permission_sets = [
        {**permission_set, "mount": variables["openbao_github_mount"]}
        for permission_set in _admin_sets(variables)
    ] + [
        {**permission_set, "mount": variables["openbao_github_everyday_mount"]}
        for permission_set in read_sets
    ]
    variables.update(
        {
            "ansible_managed": "fixture",
            "openbao_github_permission_sets": permission_sets,
            "openbao_github_runner_mount": "github-runner",
            "openbao_kv_mount": "secret",
        }
    )
    return variables


def _render_policy(template_name, variables):
    environment = Environment(undefined=StrictUndefined)
    environment.filters["comment"] = lambda value: "# " + str(value)
    template = (TEMPLATES / template_name).read_text(encoding="utf-8")
    return environment.from_string(template).render(**variables)


def _paths(rendered):
    return re.findall(r'(?m)^path "([^"]+)" \{', rendered)


def _warning_tasks():
    return yaml.safe_load(TASKS.read_text(encoding="utf-8"))


def test_empty_owner_list_adds_no_sets_and_warns_with_the_configuration_key():
    for owner_csv in (None, ""):
        variables = _runner_defaults(owner_csv, [])
        assert variables["openbao_github_runner_register_owners"] == []
        assert variables["openbao_github_runner_register_permission_sets"] == []
        assert variables["openbao_github_runner_register_missing_owners"] == []
        assert _admin_sets(variables) == [BASE_RUNNER_SET]

    tasks = _warning_tasks()
    empty_warning = next(
        task for task in tasks
        if task.get("name") == "Warn when runner registration owners are not configured"
    )
    assert "WARNING:" in empty_warning["ansible.builtin.debug"]["msg"]
    assert OWNERS_KEY in empty_warning["ansible.builtin.debug"]["msg"]
    assert "openbao_github_runner_register_owners | length == 0" in empty_warning["when"]


def test_two_example_owners_generate_only_their_runner_policy_paths():
    variables = _runner_defaults(
        " example-org, example-other ",
        [
            {"name": "example-org", "installation_id": "101"},
            {"name": "example-other", "installation_id": "202"},
        ],
    )
    additional = [
        {
            "name": "runner-register-example-org",
            "tier": "runner",
            "installation_id": "101",
            "permissions": {"organization_self_hosted_runners": "write"},
        },
        {
            "name": "runner-register-example-other",
            "tier": "runner",
            "installation_id": "202",
            "permissions": {"organization_self_hosted_runners": "write"},
        },
    ]
    assert variables["openbao_github_runner_register_owners"] == [
        "example-org", "example-other"
    ]
    assert variables["openbao_github_runner_register_permission_sets"] == additional
    expected = [BASE_RUNNER_SET, *additional]
    assert _admin_sets(variables) == expected

    permission_sets = [
        {**permission_set, "mount": "github-admin"} for permission_set in expected
    ] + [{"name": "read-fixture", "tier": "read", "mount": "github-admin"}]
    rendered = _render_policy(
        TEMPLATE.name,
        {
            "ansible_managed": "fixture",
            "openbao_github_mount": "github-admin",
            "openbao_github_permission_sets": permission_sets,
            "openbao_github_runner_mount": "github-runner",
            "openbao_kv_mount": "secret",
        },
    )
    paths = _paths(rendered)
    set_paths = [path for path in paths if path.startswith("github-admin/token/")]
    assert set_paths == [
        "github-admin/token/runner-register-example-base",
        "github-admin/token/runner-register-example-org",
        "github-admin/token/runner-register-example-other",
    ]
    stanzas = dict(re.findall(r'(?ms)^path "([^"]+)" \{(.*?)^\}', rendered))
    assert all(
        'capabilities = ["read", "create", "update"]' in stanzas[path]
        for path in set_paths
    )


def test_owner_without_installation_id_is_skipped_and_warned_by_owner():
    variables = _runner_defaults(
        "example-org,example-other",
        [
            {"name": "example-org", "installation_id": "101"},
            {"name": "example-other", "installation_id": ""},
        ],
    )
    assert variables["openbao_github_runner_register_permission_sets"] == [{
        "name": "runner-register-example-org",
        "tier": "runner",
        "installation_id": "101",
        "permissions": {"organization_self_hosted_runners": "write"},
    }]
    assert variables["openbao_github_runner_register_missing_owners"] == ["example-other"]
    assert [permission_set["name"] for permission_set in _admin_sets(variables)] == [
        "runner-register-example-base",
        "runner-register-example-org",
    ]

    missing_warning = next(
        task for task in _warning_tasks()
        if task.get("name") == "Warn when a runner registration owner has no installation ID"
    )
    assert missing_warning["loop"] == "{{ openbao_github_runner_register_missing_owners }}"
    assert "WARNING:" in missing_warning["ansible.builtin.debug"]["msg"]
    assert "{{ item }}" in missing_warning["ansible.builtin.debug"]["msg"]


def test_owner_already_in_base_sets_is_not_duplicated():
    variables = _runner_defaults(
        "example-base",
        [{"name": "example-base", "installation_id": "101"}],
    )
    assert variables["openbao_github_runner_register_permission_sets"] == []
    assert _admin_sets(variables) == [BASE_RUNNER_SET]


def test_ai_orchestrator_omits_runner_register_sets():
    variables = _policy_inputs()

    rendered = _render_policy("ai-orchestrator-policy.hcl.j2", variables)

    assert not any("/token/runner-register" in path for path in _paths(rendered))


def test_github_runner_policy_keeps_base_and_owner_runner_sets():
    variables = _policy_inputs()

    rendered = _render_policy("github-runner-policy.hcl.j2", variables)
    runner_paths = [
        path for path in _paths(rendered)
        if path.startswith("github-admin/token/runner-register")
    ]

    assert runner_paths == [
        "github-admin/token/runner-register-dryvist",
        "github-admin/token/runner-register-example-org",
        "github-admin/token/runner-register-example-other",
    ]


def test_ai_orchestrator_keeps_read_tier_permission_sets():
    variables = _policy_inputs()

    rendered = _render_policy("ai-orchestrator-policy.hcl.j2", variables)

    assert "github/token/read-dryvist-all" in _paths(rendered)


def test_ai_orchestrator_omits_all_reserved_permission_set_names():
    variables = _policy_inputs()
    reserved_names = (
        "runner-register-dryvist",
        "dryvist-repo-create",
        "dryvist-org-admin",
        "exporter-dryvist",
    )

    rendered = _render_policy("ai-orchestrator-policy.hcl.j2", variables)
    paths = _paths(rendered)

    assert all(
        not any(path.endswith(f"/token/{name}") for path in paths)
        for name in reserved_names
    )


def test_ai_orchestrator_omits_unknown_and_undefined_tiers():
    variables = _policy_inputs()
    variables["openbao_github_permission_sets"] = [
        *variables["openbao_github_permission_sets"],
        {
            "name": "example-new-tier-set",
            "tier": "example-new-tier",
            "mount": "github-admin",
        },
        {"name": "example-no-tier-set", "mount": "github-admin"},
    ]

    rendered = _render_policy("ai-orchestrator-policy.hcl.j2", variables)
    paths = _paths(rendered)

    assert "github-admin/token/example-new-tier-set" not in paths
    assert "github-admin/token/example-no-tier-set" not in paths


def test_dedicated_policies_keep_their_reserved_permission_set_paths():
    variables = _policy_inputs()
    cases = (
        ("github-repo-create-policy.hcl.j2", "dryvist-repo-create"),
        ("github-org-admin-policy.hcl.j2", "dryvist-org-admin"),
        ("github-exporter-policy.hcl.j2", "exporter-dryvist"),
        ("github-runner-policy.hcl.j2", "runner-register-dryvist"),
    )

    for template_name, set_name in cases:
        rendered = _render_policy(template_name, variables)
        assert f"github-admin/token/{set_name}" in _paths(rendered)


def test_router_snapshot_set_follows_the_docs_repository_owner():
    defaults = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))
    catalog = [
        {"name": "dryvist", "installation_id": "101"},
        {"name": "jpe-private", "installation_id": "202"},
        {"name": "jpe-claude", "installation_id": ""},
    ]

    def resolve(repository):
        variables = {
            "openbao_github_org_secrets_installations": catalog,
            "openbao_github_oidc_docs_repository": repository,
            "openbao_github_router_snapshot_set_name": "docs-router-snapshot",
            "openbao_github_docs_publisher_permissions": {"contents": "write"},
        }
        variables["openbao_github_router_snapshot_installation_id"] = str(
            _render(defaults["openbao_github_router_snapshot_installation_id"], variables)
        )
        sets = _render(defaults["openbao_github_router_snapshot_permission_sets"], variables)
        return variables["openbao_github_router_snapshot_installation_id"], sets

    installation, sets = resolve("dryvist/docs-example")
    assert installation == "101"
    assert sets == [{
        "name": "docs-router-snapshot",
        "tier": "agents",
        "installation_id": "101",
        "repositories": ["docs-example"],
        "permissions": {"contents": "write"},
    }]
    assert resolve("Jpe-Private/docs-example")[1][0]["installation_id"] == "202"
    for repository in ("", "jpe-claude/docs-example", "other-owner/docs-example"):
        assert resolve(repository) == ("", [])
