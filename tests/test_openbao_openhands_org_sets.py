"""OpenHands org-scoped write sets and their per-App mount contract."""

import json

import pytest
import yaml

from openbao_reconcile_bounds_helpers import (
    ROOT,
    TEMPLATES,
    _render,
    _render_value,
    _stanzas,
)


DEFAULTS = ROOT / "roles/openbao/defaults/main"
MOUNT_TASKS = ROOT / "roles/openbao/tasks/init/05b-github-app-mount.yml"
SET_CHECK_TASKS = ROOT / "roles/openbao/tasks/init/05b-github-app-set-checks.yml"


@pytest.fixture
def openhands_defaults(monkeypatch):
    monkeypatch.setenv("OPENBAO_TERRAKUBE_NETWORK_WORKSPACE", "fixture-network")
    monkeypatch.setenv("OPENBAO_TERRAKUBE_AWS_WORKSPACE", "fixture-aws")
    for name in (
        "OPENBAO_GITHUB_OPENHANDS_APP_ID",
        "OPENBAO_GITHUB_OPENHANDS_APP_PRIVATE_KEY",
        "OPENBAO_GITHUB_OPENHANDS_WRITE_ORGS",
        "OPENBAO_GITHUB_OPENHANDS_WRITE_WORKFLOWS",
    ):
        monkeypatch.delenv(name, raising=False)

    values = {}
    for path in sorted(DEFAULTS.glob("*.yml")):
        values.update(yaml.safe_load(path.read_text(encoding="utf-8")) or {})
    values.update(
        ansible_managed="test fixture",
        openbao_platform_env={},
        llm_router_key_catalog_facts={"openbao_router_key_catalog": {}},
    )
    return values


def test_openhands_write_inputs_split_trim_and_deduplicate_in_order(
    openhands_defaults, monkeypatch,
):
    inputs = {
        "OPENBAO_GITHUB_OPENHANDS_WRITE_ORGS": (
            " , ExampleOrg,exampleorg,example-org,ExampleOrg, "
        ),
        "OPENBAO_GITHUB_OPENHANDS_WRITE_WORKFLOWS": (
            "example-org/example-repo/.github/workflows/release.yml, "
            "example-org/example-repo/.github/workflows/release.yml,,"
        ),
    }
    # The apps load play filters these names out of the platform document, so
    # the role reads them from the run environment only.
    openhands_defaults["openbao_platform_env"].update(inputs)
    assert _render_value(
        openhands_defaults, "{{ openbao_github_openhands_write_orgs }}"
    ) == []
    for name, value in inputs.items():
        monkeypatch.setenv(name, value)

    orgs = _render_value(
        openhands_defaults, "{{ openbao_github_openhands_write_orgs }}"
    )
    workflows = _render_value(
        openhands_defaults, "{{ openbao_github_openhands_write_workflows }}"
    )

    assert orgs == ["ExampleOrg", "example-org"]
    assert workflows == [
        "example-org/example-repo/.github/workflows/release.yml"
    ]


def test_openhands_org_write_set_and_policy_use_org_name(
    openhands_defaults, monkeypatch,
):
    monkeypatch.setenv("OPENBAO_GITHUB_OPENHANDS_WRITE_ORGS", "ExampleOrg")
    openhands_defaults["openbao_github_openhands_app_id"] = "fixture-app-id"
    sets = _render_value(
        openhands_defaults,
        "{{ openbao_github_openhands_write_permission_sets }}",
    )
    assert sets == [
        {
            "name": "openhands-write-exampleorg",
            "tier": "openhands-write",
            "org_name": "ExampleOrg",
            "permissions": openhands_defaults[
                "openbao_github_openhands_write_permissions"
            ],
        }
    ]
    assert "installation_id" not in sets[0]

    openhands_defaults["openbao_github_app_mounts"] = [
        {
            "mount": "github-openhands",
            "permission_sets": sets,
        }
    ]
    policy = _render(
        TEMPLATES / "github-mount-config-policy.hcl.j2", openhands_defaults
    )
    stanzas = dict(_stanzas(policy))
    set_path = "github-openhands/permissionset/openhands-write-exampleorg"
    assert set_path in stanzas
    assert '"org_name" = ["ExampleOrg"]' in stanzas[set_path]
    assert '"installation_id"' not in stanzas[set_path]


@pytest.mark.parametrize("org", ["example-org*", "-example-org"])
def test_openhands_org_validator_rejects_invalid_names(openhands_defaults, org):
    tasks = yaml.safe_load(MOUNT_TASKS.read_text(encoding="utf-8"))
    validation = next(
        task for task in tasks
        if task["name"].startswith("Assert OpenHands org and workflow inputs")
    )
    org_pattern = next(
        check for check in validation["ansible.builtin.assert"]["that"]
        if isinstance(check, str) and "write_orgs" in check and "reject" in check
    )
    openhands_defaults["openbao_github_openhands_write_orgs"] = [org]
    result = _render_value(openhands_defaults, "{{ " + org_pattern + " }}")

    assert result is False or result == "False"


@pytest.mark.parametrize(
    "workflow",
    [
        "example-org/example-repo/.github/workflows/*.yml",
        "example-org/example-repo/.github/workflows/release.yml@main",
        "example-org/example-repo/workflows/release.yml",
    ],
)
def test_openhands_workflow_validator_rejects_globs_refs_and_wrong_prefix(
    openhands_defaults, workflow,
):
    tasks = yaml.safe_load(MOUNT_TASKS.read_text(encoding="utf-8"))
    validation = next(
        task for task in tasks
        if task["name"].startswith("Assert OpenHands org and workflow inputs")
    )
    workflow_pattern = next(
        check for check in validation["ansible.builtin.assert"]["that"]
        if isinstance(check, str) and "write_workflows" in check and "reject" in check
    )
    openhands_defaults["openbao_github_openhands_write_workflows"] = [workflow]
    result = _render_value(openhands_defaults, "{{ " + workflow_pattern + " }}")

    assert result is False or result == "False"


def test_per_app_mount_keeps_installation_id_output_and_org_only_branch_distinct(
    openhands_defaults,
):
    openhands_defaults["openbao_github_app_mounts"] = [
        {
            "mount": "github-openhands",
            "permission_sets": [
                {
                    "name": "pilot-fixture",
                    "installation_id": "303",
                    "permissions": {"contents": "read"},
                },
                {
                    "name": "org-fixture",
                    "org_name": "example-org",
                    "permissions": {"contents": "write"},
                },
            ],
        }
    ]
    policy = _render(
        TEMPLATES / "github-mount-config-policy.hcl.j2", openhands_defaults
    )
    stanzas = dict(_stanzas(policy))

    assert '"installation_id" = ["303"]' in stanzas[
        "github-openhands/permissionset/pilot-fixture"
    ]
    assert '"org_name" = ["example-org"]' in stanzas[
        "github-openhands/permissionset/org-fixture"
    ]
    assert '"installation_id"' not in stanzas[
        "github-openhands/permissionset/org-fixture"
    ]


def test_org_and_installation_reconcile_payloads_and_drift_comparisons():
    tasks = yaml.safe_load(MOUNT_TASKS.read_text(encoding="utf-8"))
    reconcile = next(
        task for task in tasks
        if task["name"].startswith("Reconcile the permission sets")
    )
    body_template = reconcile["ansible.builtin.uri"]["body"]
    when = reconcile["when"][1]
    permissions = {"contents": "write", "metadata": "read"}

    org_set = {
        "name": "openhands-write-exampleorg",
        "org_name": "ExampleOrg",
        "permissions": permissions,
    }
    installation_set = {
        "name": "openhands-pilot",
        "installation_id": "303",
        "permissions": permissions,
    }
    org_body = _render_value({}, body_template, item=[org_set, {}])
    installation_body = _render_value({}, body_template, item=[installation_set, {}])
    assert org_body == {"org_name": "ExampleOrg", "permissions": permissions}
    assert installation_body == {
        "installation_id": "303",
        "permissions": permissions,
    }

    def needs_reconcile(desired, returned):
        result = _render_value(
            {"openbao_github_app_mount_ready": True},
            "{{ " + when + " }}",
            item=[
                desired,
                {"rc": 0, "stdout": json.dumps({"data": returned})},
            ],
        )
        return result is True or result == "True"

    common_returned = {"permissions": permissions, "repositories": []}
    assert not needs_reconcile(
        org_set,
        {**common_returned, "org_name": "ExampleOrg", "installation_id": 0},
    )
    assert needs_reconcile(
        org_set, {**common_returned, "org_name": "example-org", "installation_id": 0}
    )
    assert not needs_reconcile(
        installation_set,
        {**common_returned, "installation_id": 303},
    )
    assert needs_reconcile(
        installation_set,
        {**common_returned, "installation_id": 304},
    )


def test_openhands_write_permissions_have_a_fixed_five_permission_ceiling():
    tasks = yaml.safe_load(SET_CHECK_TASKS.read_text(encoding="utf-8"))
    dedicated = next(
        task for task in tasks
        if task["name"].startswith("Assert the dedicated OpenHands set")
    )
    fixed_map_assertion = next(
        check for check in dedicated["ansible.builtin.assert"]["that"]
        if isinstance(check, str)
        and "openbao_github_openhands_write_permissions" in check
        and "actions" in check
    )

    assert "'actions': 'read'" in fixed_map_assertion
    assert "'checks': 'read'" in fixed_map_assertion
    assert "'contents': 'write'" in fixed_map_assertion
    assert "'metadata': 'read'" in fixed_map_assertion
    assert "'pull_requests': 'write'" in fixed_map_assertion
    assert "'workflows'" not in fixed_map_assertion


def test_unconfigured_and_check_mode_mount_paths_are_guarded():
    tasks = yaml.safe_load(MOUNT_TASKS.read_text(encoding="utf-8"))
    report = next(
        task for task in tasks
        if task["name"].startswith("Report the planned enable and configuration")
    )
    enable = next(
        task for task in tasks
        if task["name"].startswith("Enable GitHub App mount")
    )
    config_read = next(
        task for task in tasks
        if task["name"].startswith("Read the configuration")
    )
    absent_context = {
        "ansible_check_mode": True,
        "gm": {
            "mount": "github-openhands",
            "app_id": "fixture-app-id",
            "private_key": "fixture-private-key",
        },
        "openbao_mounts_raw": {"stdout": "{}"},
    }
    absent_expression = tasks[0]["ansible.builtin.set_fact"][
        "openbao_github_app_mount_absent_check_mode"
    ]
    absent = _render_value(absent_context, absent_expression)
    assert absent is True or absent == "True"

    check_mode_context = {
        **absent_context,
        "openbao_github_app_mount_absent_check_mode": True,
    }
    assert all(
        _render_value(check_mode_context, "{{ " + condition + " }}")
        in (False, "False")
        for condition in enable["when"]
        if "absent_check_mode" in condition
    )
    assert _render_value(
        check_mode_context, "{{ " + config_read["when"] + " }}"
    ) in (False, "False")
    assert _render_value(
        check_mode_context, "{{ " + report["when"] + " }}"
    ) in (True, "True")
    rendered_report = _render_value(check_mode_context, report["ansible.builtin.debug"]["msg"])
    assert "would enable github-openhands and write its App config" in rendered_report
    check_mode_context["gm"]["private_key"] = ""
    rendered_report_without_key = _render_value(
        check_mode_context, report["ansible.builtin.debug"]["msg"]
    )
    assert "would enable github-openhands." in rendered_report_without_key
    assert "write its App config" not in rendered_report_without_key

    ready_task = next(
        task for task in tasks
        if task["name"].startswith("Determine whether the App on mount")
    )
    ready_expression = ready_task["ansible.builtin.set_fact"][
        "openbao_github_app_mount_ready"
    ]
    unconfigured_context = {
        "openbao_github_app_mount_absent_check_mode": False,
        "openbao_github_app_mount_configured": False,
        "openbao_github_openhands_mount": "github-openhands",
        "gm": {"mount": "github-openhands", "app_id": "fixture-app-id", "private_key": ""},
    }
    not_ready = _render_value(unconfigured_context, ready_expression)
    assert not_ready is False or not_ready == "False"
    warning = next(
        task for task in tasks
        if task["name"].startswith("Warn that the unconfigured OpenHands mount")
    )
    assert all(
        _render_value(unconfigured_context, "{{ " + condition + " }}")
        in (True, "True")
        for condition in warning["when"]
    )
    assert "OPENBAO_GITHUB_OPENHANDS_APP_PRIVATE_KEY" in warning[
        "ansible.builtin.debug"
    ]["msg"]

    for prefix in (
        "Mint a metadata-only token for sets that are public-only",
        "Mint a metadata-only token for sets that are private-only",
        "Reconcile the permission sets",
        "Delete undeclared permission sets",
    ):
        task = next(task for task in tasks if task["name"].startswith(prefix))
        assert "openbao_github_app_mount_ready | bool" in str(task.get("when"))

    ceiling = next(
        task for task in tasks
        if task["name"].startswith("Assert every set declares an administration-free ceiling")
    )
    ceiling_text = str(ceiling["ansible.builtin.assert"]["that"])
    assert "item.installation_id is defined" in ceiling_text
    assert "item.org_name is defined" in ceiling_text
