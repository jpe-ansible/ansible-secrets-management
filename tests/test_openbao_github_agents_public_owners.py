"""Sandbox owner sets stay public-only and fail closed on malformed input."""

import json
from pathlib import Path

import yaml

from test_openbao_hatchet_killtest_policy_reach import render, role_defaults
from test_openbao_select import condition


ROOT = Path(__file__).resolve().parents[1]
MOUNT_TASKS_FILE = ROOT / "roles/openbao/tasks/init/05b-github-app-mount.yml"
SET_CHECKS_FILE = ROOT / "roles/openbao/tasks/init/05b-github-app-set-checks.yml"
PUBLIC_OWNERS_ENV = "OPENBAO_GITHUB_AGENTS_PUBLIC_OWNERS"
READ = {
    "contents": "read",
    "metadata": "read",
    "pull_requests": "read",
    "issues": "read",
    "actions": "read",
    "checks": "read",
}
WRITE = {
    "contents": "write",
    "metadata": "read",
    "pull_requests": "write",
    "issues": "write",
    "actions": "read",
    "checks": "read",
}


def _values(owners):
    values = role_defaults()
    values["openbao_platform_env"]["OPENBAO_GITHUB_AGENTS_DRYVIST_INSTALLATION_ID"] = "4242"
    values["openbao_platform_env"][PUBLIC_OWNERS_ENV] = json.dumps(owners)
    return values


def _render(expression, owners):
    return render(_values(owners), expression)


def _set_assertions():
    tasks = yaml.safe_load(SET_CHECKS_FILE.read_text(encoding="utf-8"))
    task = next(
        task for task in tasks
        if task.get("name", "").startswith("Assert the sandbox sets are public-only")
    )
    return task["ansible.builtin.assert"]["that"]


def _owner_input_assertions():
    tasks = yaml.safe_load(MOUNT_TASKS_FILE.read_text(encoding="utf-8"))
    return (
        tasks[1]["ansible.builtin.assert"],
        tasks[2]["ansible.builtin.assert"],
    )


def _passes(expressions, variables):
    return all(condition(expression, variables) for expression in expressions)


def test_empty_owner_list_keeps_the_agents_sets_and_mount_set_list_unchanged():
    values = _values([])
    definitions = render(values, "{{ openbao_github_agents_permission_set_definitions }}")
    expected = [
        {**definition, "installation_id": "4242", "public_repos_of": "dryvist"}
        for definition in definitions
    ]
    sets = render(values, "{{ openbao_github_agents_permission_sets }}")
    set_permissions = render(values, "{{ openbao_github_agents_set_permissions }}")
    mounts = render(values, "{{ openbao_github_app_mounts }}")
    agents_mount = next(mount for mount in mounts if mount["mount"] == "github-agents")

    assert render(values, "{{ openbao_github_agents_public_owners }}") == []
    assert sets == expected
    assert agents_mount["permission_sets"] == expected
    assert set_permissions == {
        definition["name"]: definition["permissions"] for definition in definitions
    }


def test_public_owners_default_to_an_empty_json_list():
    values = role_defaults()
    values["openbao_platform_env"] = {
        "OPENBAO_GITHUB_AGENTS_DRYVIST_INSTALLATION_ID": "4242",
    }
    assert render(values, "{{ openbao_github_agents_public_owners }}") == []


def test_each_owner_gets_only_org_scoped_public_read_and_write_sets():
    owners = ["example-org", "Example-User"]
    sets = _render("{{ openbao_github_agents_permission_sets }}", owners)
    owner_sets = [item for item in sets if "org_name" in item]

    assert [item["name"] for item in owner_sets] == [
        "public-read-example-org",
        "public-read-example-user",
        "public-write-example-org",
        "public-write-example-user",
    ]
    assert [item["org_name"] for item in owner_sets] == [
        "example-org",
        "Example-User",
        "example-org",
        "Example-User",
    ]
    assert [item["public_repos_of"] for item in owner_sets] == [
        "example-org",
        "Example-User",
        "example-org",
        "Example-User",
    ]
    assert [item["permissions"] for item in owner_sets] == [READ, READ, WRITE, WRITE]
    assert all("installation_id" not in item for item in owner_sets)
    assert all("private_repos_of" not in item and "repositories" not in item for item in owner_sets)

    set_permissions = _render("{{ openbao_github_agents_set_permissions }}", owners)
    assert set(set_permissions) == {
        item["name"] for item in sets if "org_name" not in item
    }
    assert set_permissions["public-read"] == READ
    assert set_permissions["public-write"] == WRITE


def test_owner_input_assertions_accept_two_owners_and_reject_bad_values():
    shape_assert, entries_assert = _owner_input_assertions()
    valid = ["example-org", "Example-User"]
    valid_values = {"openbao_github_agents_public_owners": valid}
    assert _passes(shape_assert["that"], valid_values)
    assert _passes(entries_assert["that"], valid_values)

    bad_values = [
        1,
        None,
        "example-org",
        {"example-org": True},
        [1],
        ["example-org", None],
        [""],
        ["  "],
        ["bad/owner"],
        ["example-org", "Example-Org"],
        ["dryvist"],
        ["DryVist"],
    ]
    assert "OPENBAO_GITHUB_AGENTS_PUBLIC_OWNERS" in shape_assert["fail_msg"]
    assert "OPENBAO_GITHUB_AGENTS_PUBLIC_OWNERS" in entries_assert["fail_msg"]

    for owners in bad_values:
        variables = {"openbao_github_agents_public_owners": owners}
        assert not _passes(shape_assert["that"], variables) or not _passes(
            entries_assert["that"], variables
        ), owners


def test_invalid_owner_entries_never_reach_candidate_sets_or_policy_inputs():
    for owners in (
        "example-org",
        {"example-org": True},
        ["example-org", 42],
        ["example-org", "Example-Org"],
        ["dryvist"],
        ["bad/owner"],
    ):
        values = _values(owners)
        assert render(
            values,
            "{{ openbao_github_agents_public_owner_set_inputs }}",
        ) == [], owners


def test_sandbox_set_scope_assertion_accepts_owner_sets_and_rejects_scope_mismatch():
    expressions = _set_assertions()
    base_variables = {
        "openbao_github_agents_public_owners": ["example-org", "Example-User"],
        "openbao_github_agents_set_permissions": {
            "public-read": READ,
            "public-write": WRITE,
        },
    }
    good_sets = [
        {
            "name": f"public-{tier}-{owner.lower()}",
            "org_name": owner,
            "public_repos_of": owner,
            "permissions": permissions,
        }
        for owner in base_variables["openbao_github_agents_public_owners"]
        for tier, permissions in (("read", READ), ("write", WRITE))
    ]
    for item in good_sets:
        assert _passes(expressions, {**base_variables, "item": item}), item

    bad = {**good_sets[0], "public_repos_of": "different-owner"}
    assert not _passes(expressions, {**base_variables, "item": bad})
    assert not _passes(
        expressions,
        {**base_variables, "item": {**good_sets[0], "repositories": []}},
    )


def test_public_repository_resolution_discards_private_entries_and_counts_the_page():
    tasks = yaml.safe_load(SET_CHECKS_FILE.read_text(encoding="utf-8"))
    resolve_task = next(
        task for task in tasks
        if task.get("name", "").startswith("Resolve the set repository lists")
    )
    expression = resolve_task["ansible.builtin.set_fact"]["openbao_github_app_mount_sets"]
    variables = {
        "openbao_github_app_mount_sets": [],
        "openbao_github_app_mount_public_repos": {
            "results": [{
                "item": {"name": "public-read-example-org"},
                "json": [
                    {"name": "visible-repo", "private": False},
                    {"name": "hidden-repo", "private": True},
                ],
            }]
        },
        "item": {
            "name": "public-read-example-org",
            "org_name": "example-org",
            "public_repos_of": "example-org",
            "permissions": READ,
        },
    }

    resolved = render(variables, expression)
    assert resolved[0]["repositories"] == ["visible-repo"]
    assert resolved[0]["repository_page_count"] == 2

    refusal = next(
        task for task in tasks
        if task.get("name", "").startswith(
            "Refuse a visibility-resolved set with an empty or full-page repository list"
        )
    )
    full_page_variables = {
        **variables,
        "openbao_github_app_mount_sets": [],
        "openbao_github_app_mount_public_repos": {
            "results": [{
                "item": {"name": "public-read-example-org"},
                "json": [
                    *(
                        {"name": f"private-{index}", "private": True}
                        for index in range(99)
                    ),
                    {"name": "visible-repo", "private": False},
                ],
            }]
        },
    }
    full_page_set = render(full_page_variables, expression)[0]
    assert full_page_set["repositories"] == ["visible-repo"]
    assert full_page_set["repository_page_count"] == 100
    assert not _passes(refusal["ansible.builtin.assert"]["that"], {"item": full_page_set})
