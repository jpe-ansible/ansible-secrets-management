"""The central AI review identity is bound and granted only its three values."""

import re
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main/05f-ci-ai-review.yml"
TASKS = ROOT / "roles/openbao/tasks/init/09c-github-oidc.yml"
POLICIES = ROOT / "roles/openbao/defaults/main/07c-base-policies.yml"
TEMPLATES = ROOT / "roles/openbao/templates"


def _find_task(tasks, name):
    for task in tasks:
        if task.get("name") == name:
            return task
        nested = task.get("block", [])
        if nested and (found := _find_task(nested, name)):
            return found
    return None


def _render_policy():
    environment = Environment(loader=FileSystemLoader(TEMPLATES))
    environment.filters["comment"] = lambda value: "# " + str(value)
    defaults = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))
    return environment.get_template("ci-ai-review-policy.hcl.j2").render(
        ansible_managed="managed",
        openbao_kv_mount="secret",
        openbao_config_mount="config",
        openbao_ci_ai_review_config_path=defaults["openbao_ci_ai_review_config_path"],
    )


def test_ci_ai_review_role_uses_the_required_bounds_and_enterprise_claim():
    defaults = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))
    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    write = _find_task(tasks, "Reconcile the ci-ai-review OIDC role")
    assert write is not None

    assert defaults["openbao_ci_ai_review_policy_name"] == "ci-ai-review"
    assert defaults["openbao_ci_ai_review_job_workflow_ref"] == (
        "JacobPEvans/.github-ai/.github/workflows/ai-review.yml@refs/tags/v1"
    )
    assert defaults["openbao_ci_ai_review_enterprise_id"] == (
        "{{ openbao_platform_env['OPENBAO_GITHUB_ENTERPRISE_ID'] | default('', true) }}"
    )
    assert defaults["openbao_ci_ai_review_audience"] == "openbao"
    assert defaults["openbao_ci_ai_review_runner_environment"] == "self-hosted"
    assert defaults["openbao_ci_ai_review_token_ttl"] == "5m"
    assert defaults["openbao_ci_ai_review_token_max_ttl"] == "10m"

    claims = write["vars"]["_ci_ai_review_role_claims"]
    assert claims == {
        "job_workflow_ref": "{{ openbao_ci_ai_review_job_workflow_ref }}",
        "enterprise_id": "{{ openbao_ci_ai_review_enterprise_id }}",
        "runner_environment": "{{ openbao_ci_ai_review_runner_environment }}",
    }
    payload = write["ansible.builtin.command"]["stdin"]
    assert "'bound_audiences': [openbao_ci_ai_review_audience]" in payload
    assert "'bound_claims_type': 'string'" in payload
    assert "'user_claim': 'job_workflow_ref'" in payload
    assert "'token_policies': [openbao_ci_ai_review_policy_name]" in payload

    read = _find_task(tasks, "Read the ci-ai-review OIDC role")
    skip = _find_task(
        tasks, "Skip the ci-ai-review OIDC role without an enterprise ID"
    )
    assert read is not None
    assert skip is not None
    assert "openbao_ci_ai_review_enterprise_id | length > 0" in read["when"]
    assert "openbao_ci_ai_review_enterprise_id | length > 0" in write["when"]
    assert skip["when"] == [
        "openbao_select | default({}) | length == 0",
        "openbao_ci_ai_review_enterprise_id | length == 0",
    ]
    assert "OPENBAO_GITHUB_ENTERPRISE_ID is empty" in skip[
        "ansible.builtin.debug"
    ]["msg"]


def test_ci_ai_review_policy_reads_only_the_two_keys_and_its_config_leaf():
    rendered = _render_policy()
    paths = re.findall(r'(?m)^path "([^"]+)" \{', rendered)
    assert paths == [
        "secret/data/apps/github-actions-pr-review",
        "secret/data/apps/github-actions-oss",
        "config/data/ci-ai-review",
    ]
    stanzas = re.findall(r'(?ms)^path "[^"]+" \{(.*?)^\}', rendered)
    assert len(stanzas) == len(paths)
    assert all(re.search(r'capabilities = \["read"\]', stanza) for stanza in stanzas)

    policies = yaml.safe_load(POLICIES.read_text(encoding="utf-8"))
    policy = next(
        item for item in policies["openbao_base_policies_static"]
        if item["name"] == "{{ openbao_ci_ai_review_policy_name }}"
    )
    assert policy["template"] == "ci-ai-review-policy.hcl.j2"


def test_ci_ai_review_base_url_is_promoted_to_config_from_existing_input():
    defaults = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))
    config_map = Environment().from_string(
        defaults["openbao_promoted_config_values"]
    ).render(openbao_ci_ai_review_config_path=defaults["openbao_ci_ai_review_config_path"])
    assert yaml.safe_load(config_map) == {
        defaults["openbao_ci_ai_review_config_path"]: {"base_url": "LLM_ROUTER_BASE_URL"}
    }
