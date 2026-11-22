"""GitHub agent-flow roles bind exact repositories and reusable workflow refs."""

import json

import yaml

from test_openbao_select import ROLE, condition, render


DEFAULTS = yaml.safe_load(
    (ROLE / "defaults/main/05b-domain-policy-approle-names.yml").read_text(encoding="utf-8")
)
RECONCILE = ROLE / "tasks/init/reconcile-github-agent-flow.yml"
RECONCILE_TASK = next(
    task for task in yaml.safe_load(RECONCILE.read_text(encoding="utf-8"))
    if task.get("name") == "Reconcile the GitHub agent-flow OIDC role"
)
AUDIENCE = "https://github.com/dryvist"
EXTRA_AUDIENCES = [
    "https://github.com/jpe-ansible",
    "https://github.com/JacobPEvans",
    "https://github.com/jpe-nix",
    "https://github.com/JacobPEvans-ai",
]
CI_FIX_V1 = "JacobPEvans/.github-ai/.github/workflows/cc-ci-fix.yml@refs/tags/v1"
CI_FIX_V2 = "JacobPEvans/.github-ai/.github/workflows/cc-ci-fix-oidc.yml@refs/tags/v2"
REPOSITORIES = [
    "dryvist/ansible-proxmox-ai",
    "jpe-ansible/ansible-secrets-management",
    "jpe-ansible/homelab-contracts",
    "JacobPEvans/.github",
    "jpe-nix/nix-ai",
    "JacobPEvans-ai/ai-llm-prompts",
    "JacobPEvans-ai/llm-prompt-evals",
]


def _roles():
    values = {
        **DEFAULTS,
        "openbao_github_oidc_docs_repository": "docs-owner/docs-source",
    }
    values["openbao_github_router_snapshot_flow_roles"] = render(
        DEFAULTS["openbao_github_router_snapshot_flow_roles"], values
    )
    return render(DEFAULTS["openbao_github_agent_flow_roles"], values)


def _role(name):
    return next(role for role in _roles() if role["name"] == name)


def _claims(role):
    return {
        claim: render(template, {"openbao_github_agent_flow": role})
        for claim, template in RECONCILE_TASK["vars"]["_agent_flow_claims"].items()
    }


def _audiences(role):
    return render(RECONCILE_TASK["vars"]["_agent_flow_audiences"], {
        "openbao_github_agent_flow": role,
        "openbao_github_oidc_audience": AUDIENCE,
    })


def _payload(role):
    rendered = render(
        RECONCILE_TASK["ansible.builtin.command"]["stdin"],
        {
            "openbao_github_agent_flow": role,
            "openbao_github_oidc_audience": AUDIENCE,
            "_agent_flow_claims": _claims(role),
            "_agent_flow_audiences": _audiences(role),
        },
    )
    return json.loads(rendered) if isinstance(rendered, str) else rendered


def _accepts(bound_claims, presented):
    return all(
        presented[name] in expected if isinstance(expected, list)
        else presented[name] == expected
        for name, expected in bound_claims.items()
    )


def _reconcile_needed(role, live):
    return condition(RECONCILE_TASK["when"], {
        "openbao_github_agent_flow": role,
        "openbao_github_agent_flow_role_current": {"rc": 0},
        "_agent_flow_role_live": live,
        "openbao_github_oidc_audience": AUDIENCE,
        "_agent_flow_claims": _claims(role),
        "_agent_flow_audiences": _audiences(role),
        "_agent_flow_token_ttl_s": 600,
        "_agent_flow_token_max_ttl_s": 900,
    })


def test_ci_fix_accepts_a_new_repository_and_v2_workflow():
    bound_claims = _payload(_role("github-agent-ci-fix"))["bound_claims"]
    assert _accepts(bound_claims, {
        "repository": "jpe-nix/nix-ai",
        "job_workflow_ref": CI_FIX_V2,
        "event_name": "workflow_run",
    })


def test_ci_fix_refuses_an_unlisted_repository_with_the_valid_v2_workflow():
    bound_claims = _payload(_role("github-agent-ci-fix"))["bound_claims"]
    assert not _accepts(bound_claims, {
        "repository": "jpe-ansible/ansible-proxmox-apps",
        "job_workflow_ref": CI_FIX_V2,
        "event_name": "workflow_run",
    })


def test_ci_fix_accepts_the_two_new_repositories_with_the_v2_workflow():
    bound_claims = _payload(_role("github-agent-ci-fix"))["bound_claims"]
    for repository in ("JacobPEvans-ai/ai-llm-prompts", "JacobPEvans-ai/llm-prompt-evals"):
        assert _accepts(bound_claims, {
            "repository": repository,
            "job_workflow_ref": CI_FIX_V2,
            "event_name": "workflow_run",
        })


def test_ci_fix_refuses_another_repository_of_the_same_owner():
    bound_claims = _payload(_role("github-agent-ci-fix"))["bound_claims"]
    assert not _accepts(bound_claims, {
        "repository": "JacobPEvans-ai/llm-prompt-evals-fork",
        "job_workflow_ref": CI_FIX_V2,
        "event_name": "workflow_run",
    })


def test_ci_fix_keeps_the_original_repository_and_v1_workflow():
    bound_claims = _payload(_role("github-agent-ci-fix"))["bound_claims"]
    assert _accepts(bound_claims, {
        "repository": "dryvist/ansible-proxmox-ai",
        "job_workflow_ref": CI_FIX_V1,
        "event_name": "workflow_run",
    })


def test_ci_fix_accepts_each_configured_owner_audience():
    bound_audiences = _payload(_role("github-agent-ci-fix"))["bound_audiences"]
    assert bound_audiences == [AUDIENCE, *EXTRA_AUDIENCES]
    assert all(audience in bound_audiences for audience in [AUDIENCE, *EXTRA_AUDIENCES])


def test_ci_fix_refuses_unlisted_and_bare_github_audiences():
    bound_audiences = _payload(_role("github-agent-ci-fix"))["bound_audiences"]
    assert "https://github.com/other-owner" not in bound_audiences
    assert "https://github.com/JacobPEvans-ai-other" not in bound_audiences
    assert "https://github.com/JacobPEvans-ai/" not in bound_audiences
    assert "https://github.com" not in bound_audiences


def test_ci_fix_audiences_are_exact_and_keep_the_base_first():
    bound_audiences = _payload(_role("github-agent-ci-fix"))["bound_audiences"]
    assert bound_audiences[0] == AUDIENCE
    assert all(not any(char in audience for char in "*?") for audience in bound_audiences)
    assert all(not any(char.isspace() for char in audience) for audience in bound_audiences)


def test_ci_fix_claim_lists_are_exact_and_keep_existing_values_first():
    role = _role("github-agent-ci-fix")
    assert role["repository"] == REPOSITORIES
    assert role["job_workflow_ref"] == [CI_FIX_V1, CI_FIX_V2]
    assert CI_FIX_V2 == "JacobPEvans/.github-ai/.github/workflows/cc-ci-fix-oidc.yml@refs/tags/v2"
    assert all(not any(char in value for char in "*?[")
               for value in role["repository"] + role["job_workflow_ref"])
    assert role["event_names"] == ["workflow_run"]
    assert role["policy"] == "github-agent-ci-fix"
    assert role["token_ttl"] == "10m"
    assert role["token_max_ttl"] == "15m"


def test_other_flow_roles_keep_scalar_repository_and_workflow_claims():
    pr_review = _payload(_role("github-agent-pr-review"))["bound_claims"]
    assert pr_review["repository"] == "dryvist/ansible-proxmox-ai"
    assert pr_review["job_workflow_ref"] == (
        "JacobPEvans/.github-ai/.github/workflows/cc-pr-review-responder.yml@refs/tags/v1"
    )
    assert isinstance(pr_review["repository"], str)
    assert isinstance(pr_review["job_workflow_ref"], str)

    snapshot = _payload(_role("docs-router-snapshot"))["bound_claims"]
    assert snapshot["repository"] == "docs-owner/docs-source"
    assert snapshot["job_workflow_ref"] == (
        "docs-owner/docs-source/.github/workflows/router-snapshot.yml@refs/heads/main"
    )
    assert isinstance(snapshot["repository"], str)
    assert isinstance(snapshot["job_workflow_ref"], str)


def test_other_flow_roles_keep_the_single_base_audience():
    for name in ("github-agent-pr-review", "docs-router-snapshot"):
        assert _payload(_role(name))["bound_audiences"] == [AUDIENCE]


def test_live_claim_comparison_is_idempotent_for_scalar_and_list_roles():
    for name in ("github-agent-ci-fix", "github-agent-pr-review", "docs-router-snapshot"):
        role = _role(name)
        payload = _payload(role)
        live = {
            **payload,
            "token_policies": [payload["token_policies"]],  # the role reads back as a list
            "token_ttl": 600,
            "token_max_ttl": 900,
        }
        assert not _reconcile_needed(role, live)

        reordered = {
            **live,
            "bound_audiences": list(reversed(payload["bound_audiences"])),
        }
        assert not _reconcile_needed(role, reordered)

        drifted = {
            **live,
            "bound_claims": {
                **payload["bound_claims"],
                "job_workflow_ref": "different-workflow-ref",
            },
        }
        assert _reconcile_needed(role, drifted)

    ci_fix = _role("github-agent-ci-fix")
    payload = _payload(ci_fix)
    live = {
        **payload,
        "token_policies": [payload["token_policies"]],
        "token_ttl": 600,
        "token_max_ttl": 900,
        "bound_audiences": [
            audience for audience in payload["bound_audiences"]
            if audience != EXTRA_AUDIENCES[0]
        ],
    }
    assert _reconcile_needed(ci_fix, live)
