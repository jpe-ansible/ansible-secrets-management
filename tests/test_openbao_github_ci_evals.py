"""The scheduled eval benchmark identity is bound to one workflow and reads only its two values."""

import re
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main/05f-ci-evals.yml"
REVIEW_DEFAULTS = ROOT / "roles/openbao/defaults/main/05f-ci-ai-review.yml"
TASKS = ROOT / "roles/openbao/tasks/init/09c-github-oidc.yml"
POLICIES = ROOT / "roles/openbao/defaults/main/07c-base-policies.yml"
GENERATED = ROOT / "roles/openbao/defaults/main/01c-app-secrets-generated.yml"
PATH_DEFAULTS = ROOT / "roles/openbao/defaults/main/01d-app-secret-paths.yml"
TEMPLATES = ROOT / "roles/openbao/templates"


def _find_task(tasks, name):
    for task in tasks:
        if task.get("name") == name:
            return task
        nested = task.get("block", [])
        if nested and (found := _find_task(nested, name)):
            return found
    return None


def _render_policy(template):
    environment = Environment(loader=FileSystemLoader(TEMPLATES))
    environment.filters["comment"] = lambda value: "# " + str(value)
    review_defaults = yaml.safe_load(REVIEW_DEFAULTS.read_text(encoding="utf-8"))
    return environment.get_template(template).render(
        ansible_managed="managed",
        openbao_kv_mount="secret",
        openbao_config_mount="config",
        openbao_ci_ai_review_config_path=review_defaults["openbao_ci_ai_review_config_path"],
    )


def test_ci_evals_role_is_bound_to_the_repository_workflow_and_default_branch():
    defaults = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))
    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    write = _find_task(tasks, "Reconcile the ci-evals OIDC role")
    assert write is not None

    assert defaults["openbao_ci_evals_policy_name"] == "ci-evals"
    assert defaults["openbao_ci_evals_repository"] == "JacobPEvans-ai/llm-prompt-evals"
    assert defaults["openbao_ci_evals_workflow_ref"] == (
        "JacobPEvans-ai/llm-prompt-evals/.github/workflows/scheduled-local-benchmark.yml"
        "@refs/heads/develop"
    )
    assert defaults["openbao_ci_evals_ref"] == "refs/heads/develop"
    assert defaults["openbao_ci_evals_audience"] == "openbao"
    assert defaults["openbao_ci_evals_token_ttl"] == "5m"
    assert defaults["openbao_ci_evals_token_max_ttl"] == "10m"

    claims = write["vars"]["_ci_evals_role_claims"]
    assert claims == {
        "repository": "{{ openbao_ci_evals_repository }}",
        "workflow_ref": "{{ openbao_ci_evals_workflow_ref }}",
        "ref": "{{ openbao_ci_evals_ref }}",
    }
    payload = write["ansible.builtin.command"]["stdin"]
    assert "'bound_audiences': [openbao_ci_evals_audience]" in payload
    assert "'bound_claims_type': 'string'" in payload
    assert "'user_claim': 'workflow_ref'" in payload
    assert "job_workflow_ref" not in payload
    assert "'token_policies': openbao_ci_evals_policy_name," in payload

    read = _find_task(tasks, "Read the ci-evals OIDC role")
    assert read is not None
    assert read["when"] == [
        "openbao_select | default({}) | length == 0 or openbao_ci_evals_policy_name\n"
        "   in ((openbao_selected_objects | default({})).get('github_oidc_roles', [])\n"
        "       | map(attribute='name') | list)",
        "openbao_bootstrap_token is defined",
    ]
    assert "openbao_bootstrap_token is defined" in write["when"]


def test_ci_evals_policy_reads_only_the_evals_key_and_the_ci_base_url_leaf():
    rendered = _render_policy("ci-evals-policy.hcl.j2")
    paths = re.findall(r'(?m)^path "([^"]+)" \{', rendered)
    assert paths == [
        "secret/data/apps/evals",
        "config/data/ci-ai-review",
    ]
    stanzas = re.findall(r'(?ms)^path "[^"]+" \{(.*?)^\}', rendered)
    assert len(stanzas) == len(paths)
    assert all(re.search(r'capabilities = \["read"\]', stanza) for stanza in stanzas)

    policies = yaml.safe_load(POLICIES.read_text(encoding="utf-8"))
    policy = next(
        item for item in policies["openbao_base_policies_static"]
        if item["name"] == "{{ openbao_ci_evals_policy_name }}"
    )
    assert policy["template"] == "ci-evals-policy.hcl.j2"


def test_ci_ai_review_rendered_policy_is_unchanged_by_the_evals_policy():
    rendered = _render_policy("ci-ai-review-policy.hcl.j2")
    paths = re.findall(r'(?m)^path "([^"]+)" \{', rendered)
    assert paths == [
        "secret/data/apps/github-actions-pr-review",
        "secret/data/apps/github-actions-oss",
        "config/data/ci-ai-review",
    ]


def test_evals_router_key_is_generated_at_the_app_path_convention():
    generated = yaml.safe_load(GENERATED.read_text(encoding="utf-8"))
    assert generated["openbao_generated_app_secrets"]["evals"] == ["evals_llm_router_key"]

    path_defaults = yaml.safe_load(PATH_DEFAULTS.read_text(encoding="utf-8"))
    seed_path = Environment().from_string(path_defaults["openbao_seed_app_path"]).render(
        openbao_app_agent_tier_generated_app_secret_paths={},
        openbao_generated_app_secret_paths=path_defaults["openbao_generated_app_secret_paths"],
        openbao_seed_app="evals",
    )
    assert seed_path == "apps/evals"
