"""Selection confines object loops and suppresses cross-object writes."""

import pytest
import yaml

from test_openbao_select import ROLE, condition, render, task


INIT = ROLE / "tasks/init.yml"


def selection_gate(task_node, selection):
    conditions = task_node.get("when", [])
    if isinstance(conditions, str):
        conditions = [conditions]
    gate = next(c for c in conditions if "openbao_select" in c)
    return condition(gate, {"openbao_select": selection})


@pytest.mark.parametrize("selection", [
    {"policies": ["apps"]},
    {"github_permission_sets": ["jacobpevans-ai-org-secrets"]},
    {"kv_mounts": ["ext-notify"]},
])
def test_all_cross_object_phases_are_skipped_in_selective_mode(selection):
    imports = {
        "init/03-kv-mounts-and-seed-secrets.yml",
        "init/04-aws-engine.yml", "init/04b-azure-engine.yml",
        "init/04c-transit-engine.yml", "init/05-github-engine.yml",
        "init/06-oauth-engine.yml", "init/07b-etcd-pki-engine.yml",
        "init/08c-human-gated-approle-policies.yml",
        "init/05b-github-app-mount.yml", "init/05c-github-app-exposure.yml",
        "init/09-auth-methods-and-terrakube-jwt.yml",
        "init/10a-approle-issuer-liveness.yml", "init/10b-approle-secret-ids.yml",
        "declare_disclosure_denylist_metadata.yml",
    }
    found = set()
    for node in yaml.safe_load(INIT.read_text()):
        imported = node.get("ansible.builtin.import_tasks", node.get("ansible.builtin.include_tasks"))
        if isinstance(imported, dict):
            imported = imported["file"]
        if imported in imports:
            found.add(imported)
            assert not selection_gate(node, selection)
            assert selection_gate(node, {})
    assert found == imports


@pytest.mark.parametrize("selection", [
    {"approles": ["apps"]},
    {"github_permission_sets": ["jacobpevans-ai-org-secrets"]},
])
def test_selective_mode_suppresses_policy_sync_and_cleanup(selection):
    # Policy sync is gated by the reconcile_policy selection fact; test_openbao_reconcile_policy_selection.py pins it.
    paths_and_names = [
        ("08b-rbac-policy-writes.yml", "Delete retired RBAC policies that still exist"),
        ("08b-rbac-policy-writes.yml", "Report retired RBAC policies that would be deleted in check mode"),
        ("10d-approle-undeclared-live.yml", "Delete retired AppRoles that still exist live"),
        ("10d-approle-undeclared-live.yml", "Drop the deleted AppRoles from the live set"),
    ]
    for filename, name in paths_and_names:
        node = task(name, ROLE / "tasks/init" / filename)
        assert not selection_gate(node, selection)
        assert selection_gate(node, {})


def test_policy_and_ssh_loops_use_only_their_resolved_kind():
    policies = ROLE / "tasks/init/08b-rbac-policy-writes.yml"
    for name in ("Read existing RBAC policy contents", "Write the RBAC policies that are missing or changed"):
        expression = task(name, policies)["loop"]
        values = {
            "openbao_select": {"approles": ["apps"]},
            "openbao_rbac_policy_targets": [],
            "openbao_reachable_policies": [{"name": "apps"}],
        }
        assert render(expression, values) == []
        assert render(expression, {
            **values,
            "openbao_select": {},
            "openbao_rbac_policy_targets": [{"name": "apps"}],
        }) == [{"name": "apps"}]

    ssh = ROLE / "tasks/init/07-ssh-ca-engine.yml"
    read = task("Check which SSH signing roles already exist", ssh)
    assert render(read["loop"], {"openbao_selected_objects": {"ssh_roles": []}}) == []
    for name in ("Enable the SSH secrets engine", "Generate the SSH CA signing key (first configuration only, never exported)"):
        assert not selection_gate(task(name, ssh), {"ssh_roles": ["apps"]})
        assert not selection_gate(task(name, ssh), {"kv_mounts": ["ext-notify"]})


def test_total_cap_counts_objects_across_kinds():
    check = task("Cap the resolved OpenBao selection")
    count = render(check["vars"]["_selected_count"], {
        "openbao_selected_objects": {"policies": [{"name": "apps"}], "approles": [{"name": "apps"}]},
    })
    assert count == 2
    assert not condition(check["ansible.builtin.assert"]["that"][0], {
        "_selected_count": count, "openbao_select_max": 1,
    })


def test_preflight_precedes_every_phase_import():
    init = yaml.safe_load(INIT.read_text())
    assert init[3]["ansible.builtin.import_tasks"] == "init/02-initialize-cluster.yml"
    initialize = yaml.safe_load((ROLE / "tasks/init/02-initialize-cluster.yml").read_text())
    names = [n.get("name") for n in initialize]
    assert names.index("Resolve the RBAC set this run's identity may manage") < names.index(
        "Resolve all object selections before phase writes"
    )
