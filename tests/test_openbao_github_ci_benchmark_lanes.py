"""The optional benchmark-lanes identity gets its own key and exact OIDC bounds."""

import json
from pathlib import Path

import pytest
import yaml
from jinja2 import Environment

from openbao_reconcile_bounds_helpers import (
    DEFAULTS,
    TEMPLATES,
    _capabilities,
    _render,
    _render_value,
    _stanzas,
    _templar,
    _trust,
)

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "roles/openbao/tasks/init/09c-github-oidc.yml"
GENERATED = DEFAULTS / "01c-app-secrets-generated.yml"
CI_EVALS_DEFAULTS = DEFAULTS / "05f-ci-evals.yml"
CI_BENCHMARK_LANES_DEFAULTS = DEFAULTS / "05f-ci-benchmark-lanes.yml"
ENV_NAMES = (
    "OPENBAO_CI_BENCHMARK_LANES_REPOSITORY",
    "OPENBAO_CI_BENCHMARK_LANES_WORKFLOW_REF",
    "OPENBAO_CI_BENCHMARK_LANES_REF",
)
EXAMPLE_INPUTS = {
    ENV_NAMES[0]: "example-owner/example-benchmarks",
    ENV_NAMES[1]: (
        "example-owner/example-benchmarks/.github/workflows/"
        "benchmark-lanes.yml@refs/heads/main"
    ),
    ENV_NAMES[2]: "refs/heads/main",
}


@pytest.fixture
def benchmark_defaults(monkeypatch, request):
    inputs = getattr(request, "param", {})
    for name, value in {
        "OPENBAO_TERRAKUBE_NETWORK_WORKSPACE": "fixture-network",
        "OPENBAO_TERRAKUBE_AWS_WORKSPACE": "fixture-aws",
        "OPENBAO_AI_API_KEY_MOUNT": "secret",
        "OPENBAO_AI_API_KEY_PATH_PREFIX": "fixture-provider-keys",
        "PROXMOX_SUBDOMAIN": "example.invalid",
    }.items():
        monkeypatch.setenv(name, value)
    for name in ENV_NAMES:
        if name in inputs:
            monkeypatch.setenv(name, inputs[name])
        else:
            monkeypatch.delenv(name, raising=False)

    values = {}
    for path in sorted(DEFAULTS.glob("*.yml")):
        values.update(yaml.safe_load(path.read_text(encoding="utf-8")) or {})
    values.update(
        tofu_data={"agents": {}},
        ansible_managed="test fixture",
        llm_router_key_catalog_facts={"openbao_router_key_catalog": {}},
        openbao_management_cidrs="192.0.2.0/24",
        openbao_workstation_cidrs="198.51.100.0/24",
        openbao_ci_cidrs="203.0.113.0/24",
        openbao_ssh_source_cidrs="192.0.2.0/24",
        openbao_sandbox_agent_cidrs="203.0.113.0/24",
    )
    templar = _templar(_trust(values))
    policies = templar.template(_trust(values["openbao_policies"]))
    values["openbao_policies"] = policies
    return values, policies


def _find_task(tasks, name):
    for task in tasks:
        if task.get("name") == name:
            return task
        for key in ("block", "rescue", "always"):
            nested = task.get(key, [])
            if nested and (found := _find_task(nested, name)):
                return found
    return None


def test_unset_repository_omits_policy_and_guards_both_role_tasks(benchmark_defaults):
    _values, policies = benchmark_defaults
    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    policy_names = [policy["name"] for policy in policies]
    configured_guard = "openbao_ci_benchmark_lanes_repository | length > 0"

    assert "ci-benchmark-lanes" not in policy_names
    for name in (
        "Read the ci-benchmark-lanes OIDC role",
        "Reconcile the ci-benchmark-lanes OIDC role",
    ):
        task = _find_task(tasks, name)
        assert task is not None
        assert configured_guard in task["when"]


@pytest.mark.parametrize("benchmark_defaults", [EXAMPLE_INPUTS], indirect=True)
def test_configured_role_claims_and_ttls_match_the_fixture(benchmark_defaults):
    values, policies = benchmark_defaults
    defaults = yaml.safe_load(CI_BENCHMARK_LANES_DEFAULTS.read_text(encoding="utf-8"))
    evals_defaults = yaml.safe_load(CI_EVALS_DEFAULTS.read_text(encoding="utf-8"))
    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    write = _find_task(tasks, "Reconcile the ci-benchmark-lanes OIDC role")
    policy_names = [policy["name"] for policy in policies]
    policy = next(item for item in policies if item["name"] == "ci-benchmark-lanes")
    assert write is not None

    assert defaults["openbao_ci_benchmark_lanes_policy_name"] == "ci-benchmark-lanes"
    assert defaults["openbao_ci_benchmark_lanes_audience"] == evals_defaults[
        "openbao_ci_evals_audience"
    ]
    assert defaults["openbao_ci_benchmark_lanes_token_ttl"] == evals_defaults[
        "openbao_ci_evals_token_ttl"
    ]
    assert defaults["openbao_ci_benchmark_lanes_token_max_ttl"] == evals_defaults[
        "openbao_ci_evals_token_max_ttl"
    ]
    assert write["vars"]["_ci_benchmark_lanes_role_claims"] == {
        "repository": "{{ openbao_ci_benchmark_lanes_repository }}",
        "workflow_ref": "{{ openbao_ci_benchmark_lanes_workflow_ref }}",
        "ref": "{{ openbao_ci_benchmark_lanes_ref }}",
    }

    task_values = dict(values, **write["vars"])
    role_path = _render_value(
        values, write["ansible.builtin.command"]["cmd"]
    )
    payload = json.loads(
        _render_value(task_values, write["ansible.builtin.command"]["stdin"])
    )
    assert role_path.endswith("/role/ci-benchmark-lanes -")
    assert payload["role_type"] == "jwt"
    assert payload["user_claim"] == "workflow_ref"
    assert payload["bound_audiences"] == ["openbao"]
    assert payload["bound_claims_type"] == "string"
    assert payload["bound_claims"] == {
        "repository": EXAMPLE_INPUTS[ENV_NAMES[0]],
        "workflow_ref": EXAMPLE_INPUTS[ENV_NAMES[1]],
        "ref": EXAMPLE_INPUTS[ENV_NAMES[2]],
    }
    assert payload["token_policies"] == ["ci-benchmark-lanes"]
    assert payload["token_ttl"] == evals_defaults["openbao_ci_evals_token_ttl"]
    assert payload["token_max_ttl"] == evals_defaults["openbao_ci_evals_token_max_ttl"]
    assert policy_names.count("ci-benchmark-lanes") == 1
    assert policy["template"] == "ci-benchmark-lanes-policy.hcl.j2"


@pytest.mark.parametrize("benchmark_defaults", [EXAMPLE_INPUTS], indirect=True)
def test_benchmark_lanes_policy_matches_the_evals_leaf_and_capabilities(benchmark_defaults):
    values, _policies = benchmark_defaults
    evals = _render(TEMPLATES / "ci-evals-policy.hcl.j2", values)
    benchmark_lanes = _render(TEMPLATES / "ci-benchmark-lanes-policy.hcl.j2", values)
    evals_stanzas = list(_stanzas(evals))
    benchmark_stanzas = list(_stanzas(benchmark_lanes))

    assert len(benchmark_stanzas) == len(evals_stanzas)
    assert [body for _path, body in benchmark_stanzas] == [
        body for _path, body in evals_stanzas
    ]
    assert [path for path, _body in benchmark_stanzas] == [
        path.replace("secret/data/apps/evals", "secret/data/apps/benchmark-lanes")
        for path, _body in evals_stanzas
    ]
    assert [
        _capabilities(body) for _path, body in benchmark_stanzas
    ] == [_capabilities(body) for _path, body in evals_stanzas]
    assert "secret/data/apps/evals" not in benchmark_lanes


def test_assertion_rejects_a_workflow_ref_for_a_different_repository():
    tasks = yaml.safe_load(TASKS.read_text(encoding="utf-8"))
    assertion = _find_task(tasks, "Validate the ci-benchmark-lanes OIDC role inputs")
    assert assertion is not None
    context = {
        "openbao_ci_benchmark_lanes_repository": "example-owner/example-benchmarks",
        "openbao_ci_benchmark_lanes_workflow_ref": (
            "example-owner/other-benchmarks/.github/workflows/"
            "benchmark-lanes.yml@refs/heads/main"
        ),
        "openbao_ci_benchmark_lanes_ref": "refs/heads/main",
    }
    checks = [
        Environment().from_string("{{ " + condition + " }}").render(context)
        for condition in assertion["ansible.builtin.assert"]["that"]
    ]

    assert checks == ["True", "True", "False"]


def test_benchmark_lanes_router_key_is_generated_at_its_app_path():
    generated = yaml.safe_load(GENERATED.read_text(encoding="utf-8"))
    assert generated["openbao_generated_app_secrets"]["benchmark-lanes"] == [
        "benchmark_lanes_llm_router_key"
    ]
