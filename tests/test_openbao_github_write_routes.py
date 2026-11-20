"""Generic org-scoped GitHub App write routes stay isolated and least-privileged."""

import json
import re
from pathlib import Path

import pytest
import yaml

from openbao_reconcile_bounds_helpers import (
    TEMPLATES,
    _render as render_template,
    _render_value as render_value,
    rendered_defaults,  # noqa: F401 - pytest fixture
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main"
OIDC_TASKS = ROOT / "roles/openbao/tasks/init/09c-github-oidc.yml"

OPENHANDS_PERMISSIONS = {
    "actions": "read",
    "checks": "read",
    "contents": "write",
    "metadata": "read",
    "pull_requests": "write",
}
CLAUDE_PERMISSIONS = {
    "checks": "write",
    "contents": "read",
    "metadata": "read",
    "pull_requests": "write",
}

ROUTE_ENV = (
    "OPENBAO_GITHUB_OPENHANDS_APP_ID",
    "OPENBAO_GITHUB_OPENHANDS_APP_PRIVATE_KEY",
    "OPENBAO_GITHUB_OPENHANDS_WRITE_ORGS",
    "OPENBAO_GITHUB_OPENHANDS_WRITE_WORKFLOWS",
    "OPENBAO_GITHUB_CLAUDE_APP_ID",
    "OPENBAO_GITHUB_CLAUDE_APP_PRIVATE_KEY",
    "OPENBAO_GITHUB_CLAUDE_WRITE_ORGS",
    "OPENBAO_GITHUB_CLAUDE_WRITE_WORKFLOWS",
    "OPENBAO_GITHUB_EVERYDAY_APP_ID",
    "OPENBAO_GITHUB_GATE_CHECKS_ORGS",
    "OPENBAO_GITHUB_GATE_CHECKS_WORKFLOWS",
    "OPENBAO_GITHUB_PR_RECONCILE_REPOSITORY",
    "OPENBAO_GITHUB_PR_RECONCILE_OWNERS",
)


@pytest.fixture
def write_route_defaults(request, monkeypatch):
    for name in ROUTE_ENV:
        monkeypatch.delenv(name, raising=False)
    # Resolve the shared repository fixture after clearing the route inputs so
    # its pre-rendered policy catalog cannot inherit the invoking shell's env.
    return request.getfixturevalue("rendered_defaults")


def _set_inputs(monkeypatch, **values):
    for name in ROUTE_ENV:
        monkeypatch.delenv(name, raising=False)
    for name, value in values.items():
        monkeypatch.setenv(name, value)


def _expression_values(values, **overrides):
    defaults = values[0] if isinstance(values, tuple) else values
    return dict(defaults, **overrides)


def _rendered(values, expression, **overrides):
    return render_value(_expression_values(values, **overrides), expression)


def _route_policy_paths(policy_text):
    return re.findall(
        r'(?m)^path "([^"]+)" \{\n  capabilities = \[([^\]]+)\]\n\}',
        policy_text,
    )


def _policy_lines(policy_text):
    return [
        line
        for line in policy_text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _write_route_values(values):
    defaults, _approles, _policies = values
    return {
        "routes": _rendered(defaults, "{{ openbao_github_write_routes }}"),
        "sets": _rendered(
            defaults, "{{ openbao_github_write_permission_sets }}"
        ),
        "policies": _rendered(defaults, "{{ openbao_github_write_policies }}"),
        "roles": _rendered(defaults, "{{ openbao_github_write_oidc_roles }}"),
        "mounts": _rendered(defaults, "{{ openbao_github_app_mounts }}"),
        "permission_sets": _rendered(
            defaults, "{{ openbao_github_permission_sets }}"
        ),
    }


def _render_route_policy(defaults, policy):
    return render_template(
        TEMPLATES / policy["template"],
        dict(defaults, item=policy, ansible_managed="test fixture"),
    )


def test_openhands_only_keeps_literal_existing_outputs_and_selection_candidates(
    write_route_defaults, monkeypatch,
):
    workflow = "example-org/example-repo/.github/workflows/write.yml"
    _set_inputs(
        monkeypatch,
        OPENBAO_GITHUB_OPENHANDS_APP_ID="12345",
        OPENBAO_GITHUB_OPENHANDS_WRITE_ORGS="ExampleOrg",
        OPENBAO_GITHUB_OPENHANDS_WRITE_WORKFLOWS=workflow,
    )
    defaults, _approles, _policies = write_route_defaults
    output = _write_route_values(write_route_defaults)

    openhands_route = output["routes"][0]
    assert openhands_route == {
        "prefix": "openhands-write",
        "mount": "github-openhands",
        "app_id": "12345",
        "orgs": ["ExampleOrg"],
        "workflows": [workflow],
        "permissions": OPENHANDS_PERMISSIONS,
        "token_ttl": "5m",
        "token_max_ttl": "10m",
    }
    assert [route["prefix"] for route in output["routes"]] == [
        "openhands-write",
        "claude-write",
        "gate-checks",
    ]

    expected_set = {
        "name": "openhands-write-exampleorg",
        "tier": "openhands-write",
        "org_name": "ExampleOrg",
        "permissions": OPENHANDS_PERMISSIONS,
    }
    assert output["sets"] == [expected_set]
    assert set(output["sets"][0]) == {"name", "tier", "org_name", "permissions"}

    assert [policy["name"] for policy in output["policies"]] == [
        "openhands-write-exampleorg"
    ]
    policy_text = _render_route_policy(defaults, output["policies"][0])
    assert _policy_lines(policy_text) == [
        'path "github-openhands/token/openhands-write-exampleorg" {',
        '  capabilities = ["create", "read", "update"]',
        "}",
    ]
    assert _route_policy_paths(policy_text) == [
        (
            "github-openhands/token/openhands-write-exampleorg",
            '"create", "read", "update"',
        )
    ]

    expected_role = {
        "name": "openhands-write-exampleorg",
        "org": "ExampleOrg",
        "set": expected_set,
    }
    assert output["roles"] == [expected_role]
    assert set(output["roles"][0]) == {"name", "org", "set"}
    profile = yaml.safe_load((DEFAULTS / "00-selection.yml").read_text())[
        "openbao_select_profiles"
    ]["github_oidc_roles"]
    assert _rendered(defaults, profile["candidates"]) == [expected_role, {"name": "ci-evals"}]
    assert [
        item["name"]
        for item in output["permission_sets"]
        if item["tier"] == "openhands-write"
    ] == ["openhands-write-exampleorg"]


def test_claude_route_creates_one_org_bound_set_policy_and_role_per_org(
    write_route_defaults, monkeypatch,
):
    workflow = "example-org/example-repo/.github/workflows/review.yml"
    _set_inputs(
        monkeypatch,
        OPENBAO_GITHUB_CLAUDE_APP_ID="12345",
        OPENBAO_GITHUB_CLAUDE_WRITE_ORGS="ExampleOrg,example-org",
        OPENBAO_GITHUB_CLAUDE_WRITE_WORKFLOWS=workflow,
    )
    defaults, _approles, _policies = write_route_defaults
    output = _write_route_values(write_route_defaults)

    claude_route = next(
        route for route in output["routes"] if route["prefix"] == "claude-write"
    )
    assert claude_route == {
        "prefix": "claude-write",
        "mount": "github-claude",
        "app_id": "12345",
        "orgs": ["ExampleOrg", "example-org"],
        "workflows": [workflow],
        "permissions": CLAUDE_PERMISSIONS,
        "token_ttl": "15m",
        "token_max_ttl": "15m",
    }
    claude_sets = [
        item for item in output["sets"] if item["tier"] == "claude-write"
    ]
    expected_sets = [
        {
            "name": "claude-write-exampleorg",
            "tier": "claude-write",
            "org_name": "ExampleOrg",
            "permissions": CLAUDE_PERMISSIONS,
        },
        {
            "name": "claude-write-example-org",
            "tier": "claude-write",
            "org_name": "example-org",
            "permissions": CLAUDE_PERMISSIONS,
        },
    ]
    assert claude_sets == expected_sets

    claude_policies = [
        item for item in output["policies"] if item["name"].startswith("claude-write-")
    ]
    assert [item["name"] for item in claude_policies] == [
        "claude-write-exampleorg",
        "claude-write-example-org",
    ]
    for policy in claude_policies:
        rendered = _render_route_policy(defaults, policy)
        assert _policy_lines(rendered) == [
            f'path "github-claude/token/{policy["name"]}" {{',
            '  capabilities = ["create", "read", "update"]',
            "}",
        ]
        assert _route_policy_paths(rendered) == [
            (
                f"github-claude/token/{policy['name']}",
                '"create", "read", "update"',
            )
        ]

    claude_roles = [
        item for item in output["roles"] if item["name"].startswith("claude-write-")
    ]
    assert [(item["name"], item["org"]) for item in claude_roles] == [
        ("claude-write-exampleorg", "ExampleOrg"),
        ("claude-write-example-org", "example-org"),
    ]
    assert [item["set"] for item in claude_roles] == expected_sets
    assert all(set(item) == {"name", "org", "set"} for item in claude_roles)
    assert [
        item["mount"]
        for item in output["mounts"]
        if item["mount"] == "github-claude"
    ] == ["github-claude"]
    claude_mount = next(
        item for item in output["mounts"] if item["mount"] == "github-claude"
    )
    assert claude_mount["permission_sets"] == expected_sets

    profile = yaml.safe_load((DEFAULTS / "00-selection.yml").read_text())[
        "openbao_select_profiles"
    ]["github_oidc_roles"]
    candidates = _rendered(defaults, profile["candidates"])
    assert [item["name"] for item in candidates] == [
        "claude-write-exampleorg",
        "claude-write-example-org",
        "ci-evals",
    ]


def test_gate_checks_route_binds_main_and_release_tags_on_the_everyday_mount(
    write_route_defaults, monkeypatch,
):
    workflows = [
        "example-org/example-repo/.github/workflows/gate.yml",
        "example-org/example-repo/.github/workflows/check.yml",
    ]
    _set_inputs(
        monkeypatch,
        OPENBAO_GITHUB_EVERYDAY_APP_ID="12345",
        OPENBAO_GITHUB_GATE_CHECKS_ORGS="ExampleOrg,example-org",
        OPENBAO_GITHUB_GATE_CHECKS_WORKFLOWS=",".join(workflows),
    )
    defaults, _approles, _policies = write_route_defaults
    output = _write_route_values(write_route_defaults)

    route = next(item for item in output["routes"] if item["prefix"] == "gate-checks")
    assert route == {
        "prefix": "gate-checks",
        "mount": "github",
        "app_id": "12345",
        "orgs": ["ExampleOrg", "example-org"],
        "workflows": workflows,
        "workflow_ref_suffixes": ["@refs/heads/main", "@refs/tags/v*"],
        "permissions": {"checks": "write", "metadata": "read"},
        "token_ttl": "15m",
        "token_max_ttl": "15m",
    }
    gate_sets = [item for item in output["sets"] if item["tier"] == "gate-checks"]
    assert [item["name"] for item in gate_sets] == [
        "gate-checks-exampleorg",
        "gate-checks-example-org",
    ]
    everyday = next(item for item in output["mounts"] if item["mount"] == "github")
    assert everyday["permission_sets"] == (
        _rendered(defaults, "{{ openbao_github_read_permission_sets }}") + gate_sets
    )
    for policy in (
        item for item in output["policies"] if item["name"].startswith("gate-checks-")
    ):
        assert _route_policy_paths(_render_route_policy(defaults, policy)) == [
            (f"github/token/{policy['name']}", '"create", "read", "update"')
        ]
    claims = next(
        task
        for task in yaml.safe_load(OIDC_TASKS.read_text(encoding="utf-8"))
        if task.get("name") == "Reconcile each GitHub write OIDC role"
    )["vars"]["_github_write_role_claims"]
    assert _rendered(
        defaults, claims["job_workflow_ref"], _github_write_route=route
    ) == [
        f"{workflow}{suffix}"
        for workflow in workflows
        for suffix in ("@refs/heads/main", "@refs/tags/v*")
    ]
    for template_name in ("ai-orchestrator-policy.hcl.j2", "openhands-policy.hcl.j2"):
        rendered = render_template(
            TEMPLATES / template_name,
            dict(
                defaults,
                openbao_kv_mount="secret",
                openbao_github_permission_sets=output["permission_sets"],
                ansible_managed="test fixture",
            ),
        )
        assert "gate-checks-" not in rendered


@pytest.mark.parametrize(
    (
        "app_id",
        "orgs",
        "workflows",
        "expected_sets",
        "expected_policies",
        "expected_roles",
        "expected_mount",
    ),
    [
        (
            "",
            "ExampleOrg",
            "example-org/example-repo/.github/workflows/review.yml",
            0,
            0,
            0,
            False,
        ),
        (
            "12345",
            "",
            "example-org/example-repo/.github/workflows/review.yml",
            0,
            0,
            0,
            False,
        ),
        ("12345", "ExampleOrg", "", 1, 1, 0, True),
    ],
)
def test_claude_route_is_omitted_or_limited_by_its_configured_inputs(
    write_route_defaults,
    monkeypatch,
    app_id,
    orgs,
    workflows,
    expected_sets,
    expected_policies,
    expected_roles,
    expected_mount,
):
    env = {
        "OPENBAO_GITHUB_CLAUDE_APP_ID": app_id,
        "OPENBAO_GITHUB_CLAUDE_WRITE_ORGS": orgs,
        "OPENBAO_GITHUB_CLAUDE_WRITE_WORKFLOWS": workflows,
    }
    _set_inputs(monkeypatch, **env)
    output = _write_route_values(write_route_defaults)
    assert len(
        [item for item in output["sets"] if item["tier"] == "claude-write"]
    ) == expected_sets
    assert len(
        [
            item
            for item in output["policies"]
            if item["name"].startswith("claude-write-")
        ]
    ) == expected_policies
    assert len(
        [item for item in output["roles"] if item["name"].startswith("claude-write-")]
    ) == expected_roles
    assert (
        any(item["mount"] == "github-claude" for item in output["mounts"])
        is expected_mount
    )


def test_claude_orgs_deduplicate_case_insensitively(write_route_defaults, monkeypatch):
    _set_inputs(
        monkeypatch,
        OPENBAO_GITHUB_CLAUDE_APP_ID="12345",
        **{
            "OPENBAO_GITHUB_CLAUDE_WRITE_ORGS": (
                "ExampleOrg,exampleorg,example-org,EXAMPLE-ORG"
            ),
            "OPENBAO_GITHUB_CLAUDE_WRITE_WORKFLOWS": (
                "example-org/example-repo/.github/workflows/review.yml"
            ),
        },
    )
    output = _write_route_values(write_route_defaults)
    claude_sets = [
        item for item in output["sets"] if item["tier"] == "claude-write"
    ]
    assert [item["org_name"] for item in claude_sets] == [
        "ExampleOrg",
        "example-org",
    ]


def test_claude_write_tier_never_enters_tier_selected_policies(
    write_route_defaults, monkeypatch,
):
    _set_inputs(
        monkeypatch,
        OPENBAO_GITHUB_CLAUDE_APP_ID="12345",
        OPENBAO_GITHUB_CLAUDE_WRITE_ORGS="ExampleOrg",
        **{
            "OPENBAO_GITHUB_CLAUDE_WRITE_WORKFLOWS": (
                "example-org/example-repo/.github/workflows/review.yml"
            )
        },
    )
    defaults, _approles, _policies = write_route_defaults
    output = _write_route_values(write_route_defaults)
    assert any(item["tier"] == "claude-write" for item in output["permission_sets"])
    assert _rendered(defaults, "{{ openbao_ai_orchestrator_github_tiers }}") == [
        "read"
    ]

    for template_name, context in (
        (
            "ai-orchestrator-policy.hcl.j2",
            dict(defaults, openbao_github_permission_sets=output["permission_sets"]),
        ),
        (
            "openhands-policy.hcl.j2",
            dict(
                defaults,
                openbao_kv_mount="secret",
                openbao_github_permission_sets=output["permission_sets"],
            ),
        ),
    ):
        rendered = render_template(
            TEMPLATES / template_name,
            dict(context, ansible_managed="test fixture"),
        )
        assert "claude-write-" not in rendered

    tier_templates = []
    for path in TEMPLATES.glob("*policy.hcl.j2"):
        source = path.read_text(encoding="utf-8")
        if "selectattr('tier'" in source:
            tier_templates.append(source)
    assert tier_templates
    assert all(
        "selectattr('tier', 'equalto', 'claude-write')" not in source
        for source in tier_templates
    )
    assert all(
        not re.search(
            r"selectattr\('tier',\s*'equalto',\s*[^']*[A-Za-z_][A-Za-z0-9_.]*\s*\)",
            source,
        )
        for source in tier_templates
    )


def test_generic_oidc_role_task_inputs_preserve_openhands_payload_and_add_claude_ttl(
    write_route_defaults, monkeypatch,
):
    _set_inputs(
        monkeypatch,
        OPENBAO_GITHUB_OPENHANDS_APP_ID="12345",
        OPENBAO_GITHUB_OPENHANDS_WRITE_ORGS="ExampleOrg",
        **{
            "OPENBAO_GITHUB_OPENHANDS_WRITE_WORKFLOWS": (
                "example-org/example-repo/.github/workflows/write.yml"
            ),
        },
        OPENBAO_GITHUB_CLAUDE_APP_ID="12345",
        OPENBAO_GITHUB_CLAUDE_WRITE_ORGS="example-org",
        **{
            "OPENBAO_GITHUB_CLAUDE_WRITE_WORKFLOWS": (
                "example-org/example-repo/.github/workflows/review.yml"
            ),
        },
    )
    defaults, _approles, _policies = write_route_defaults
    output = _write_route_values(write_route_defaults)
    tasks = yaml.safe_load(OIDC_TASKS.read_text(encoding="utf-8"))
    reconcile = next(
        task
        for task in tasks
        if "Reconcile each GitHub write OIDC role" in task.get("name", "")
    )
    assert reconcile["loop"] == "{{ openbao_github_write_oidc_roles }}"
    assert reconcile["loop_control"]["label"] == "{{ item.name }}"
    assert reconcile["loop_control"]["index_var"] == "openbao_github_write_role_index"
    assert "openbao_github_oidc_write_roles_current.results[" in str(reconcile["vars"])

    payload_expression = reconcile["ansible.builtin.command"]["stdin"]
    for role, expected_claims, expected_ttl, expected_max_ttl in (
        (
            next(
                item
                for item in output["roles"]
                if item["name"] == "openhands-write-exampleorg"
            ),
            {
                "job_workflow_ref": [
                    "example-org/example-repo/.github/workflows/write.yml@*"
                ],
                "repository_owner": ["ExampleOrg"],
            },
            "5m",
            "10m",
        ),
        (
            next(
                item
                for item in output["roles"]
                if item["name"] == "claude-write-example-org"
            ),
            {
                "job_workflow_ref": [
                    "example-org/example-repo/.github/workflows/review.yml@*"
                ],
                "repository_owner": ["example-org"],
            },
            "15m",
            "15m",
        ),
    ):
        route = next(
            item for item in output["routes"] if item["prefix"] == role["set"]["tier"]
        )
        route_context = dict(
            defaults,
            item=role,
            _github_write_route=route,
            _github_write_role_claims=expected_claims,
        )
        rendered_payload = render_value(route_context, payload_expression)
        payload = json.loads(rendered_payload)
        assert payload == {
            "role_type": "jwt",
            "bound_audiences": [defaults["openbao_github_oidc_audience"]],
            "bound_claims": expected_claims,
            "bound_claims_type": "glob",
            "user_claim": "job_workflow_ref",
            "token_policies": [role["name"]],
            "token_no_default_policy": True,
            "token_type": "batch",
            "token_ttl": expected_ttl,
            "token_max_ttl": expected_max_ttl,
        }
