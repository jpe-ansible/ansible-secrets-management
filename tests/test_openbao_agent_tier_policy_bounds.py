"""Agent-tier reader and reconcile grants stay on their declared leaves."""

import ast
from pathlib import Path
import re

import jinja2
import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main"
TEMPLATES = ROOT / "roles/openbao/templates"


def _defaults():
    values = {}
    for path in sorted(DEFAULTS.glob("*.yml")):
        values.update(yaml.safe_load(path.read_text(encoding="utf-8")) or {})
    return values


def _render(expression, values):
    templar = jinja2.Environment(undefined=jinja2.StrictUndefined)
    templar.filters["combine"] = lambda left, right: {**left, **right}
    return templar.from_string(expression).render(**values)


def _grants(rendered):
    return {
        (path, tuple(re.findall(r'"([^"]+)"', capabilities)))
        for path, capabilities in re.findall(
            r'path "([^"]+)"\s*\{\s*capabilities\s*=\s*\[([^]]+)\]\s*\}',
            rendered,
        )
    }


def test_generated_credentials_are_declared_only_on_agent_tier_leaves():
    values = _defaults()
    generated = _render(values["openbao_app_agent_tier_generated_app_secrets"], values)
    generated = yaml.safe_load(generated)
    base = values["openbao_generated_app_secrets"]
    for reader in values["openbao_app_agent_tier_readers"]:
        if reader.get("generated_fields"):
            assert generated[f"agent-tier-{reader['tier']}"] == reader["generated_fields"]
        if reader.get("login_fields"):
            assert generated[f"agent-tier-login-{reader['tier']}"] == reader["login_fields"]
        for field in reader.get("generated_fields", []) + reader.get("login_fields", []):
            assert sum(field in fields for fields in generated.values()) == 1
            assert field not in base.get("vikunja", [])
            assert field not in base.get("zammad", [])


def test_agent_tier_mount_is_provisioned_outside_shared_wildcard_mounts():
    values = _defaults()
    assert values["openbao_agent_tier_mount"] not in {
        mount["path"] for mount in values["openbao_kv_zone_mounts"]
    }
    task = (ROOT / "roles/openbao/tasks/init/03-kv-mounts-and-seed-secrets.yml").read_text(
        encoding="utf-8"
    )
    assert "Enable the dedicated agent-tier KV v2 mount (add-if-missing)" in task
    assert "bao secrets enable -path={{ openbao_agent_tier_mount }} -version=2 kv" in task


def test_reader_policy_grants_only_its_exact_data_and_metadata_leaf():
    values = _defaults()
    login_paths = ast.literal_eval(
        _render(values["openbao_app_agent_tier_login_paths"], values).strip()
    )
    assert login_paths == [
        reader["login_path"]
        for reader in values["openbao_app_agent_tier_readers"]
        if reader.get("login_path")
    ]
    source = (TEMPLATES / "app-agent-tier-reader-policy.hcl.j2").read_text(
        encoding="utf-8"
    )
    environment = jinja2.Environment()
    environment.filters["comment"] = str
    for reader in values["openbao_app_agent_tier_readers"]:
        rendered = environment.from_string(source).render(
            ansible_managed="", openbao_agent_tier_mount="agent-tier", item=reader
        )
        assert _grants(rendered) == {
            (f"agent-tier/data/{reader['tier']}", ("read",)),
            (f"agent-tier/metadata/{reader['tier']}", ("read",)),
        }
        if reader.get("login_path"):
            assert reader["login_path"] not in rendered
            assert not any(reader["login_path"] in path for path, _caps in _grants(rendered))
        assert not any("list" in capabilities for _path, capabilities in _grants(rendered))
        for other in values["openbao_app_agent_tier_readers"]:
            if other["tier"] != reader["tier"]:
                assert other["tier"] not in rendered


def test_reconcile_grant_has_no_list_or_other_agent_tier_path():
    values = _defaults()
    source = (TEMPLATES / "openbao-reconcile-policy.hcl.j2").read_text(
        encoding="utf-8"
    )
    loop = re.search(
        r"{% for reader in openbao_app_agent_tier_readers %}.*?{% endfor %}",
        source,
        re.DOTALL,
    )
    assert loop
    rendered = jinja2.Environment().from_string(loop.group(0)).render(
        openbao_agent_tier_mount="agent-tier",
        openbao_app_agent_tier_readers=values["openbao_app_agent_tier_readers"],
    )
    expected = set()
    for reader in values["openbao_app_agent_tier_readers"]:
        expected.add(
            (f"agent-tier/data/{reader['tier']}", ("create", "read", "update"))
        )
        expected.add((f"agent-tier/metadata/{reader['tier']}", ("read",)))
        if reader.get("login_path"):
            expected.add(
                (f"agent-tier/data/{reader['login_path']}", ("create", "read", "update"))
            )
            expected.add((f"agent-tier/metadata/{reader['login_path']}", ("read",)))
    assert _grants(rendered) == expected
    assert "list" not in rendered
    assert "*" not in rendered
    assert "+" not in rendered
    assert source.count("openbao_agent_tier_mount") == 4


def test_legacy_removal_is_field_scoped_and_uses_kv_check_and_set():
    task = (ROOT / "roles/openbao/tasks/remove_app_agent_legacy_fields.yml").read_text(
        encoding="utf-8"
    )
    declarations = _defaults()["openbao_app_agent_tier_readers"]
    fields = [
        field
        for row in declarations
        for field in row.get("generated_fields", []) + row.get("login_fields", [])
    ]
    assert "status_code: [200, 403, 404]" in task
    assert "rejectattr('key', 'in', openbao_agent_tier_legacy_remove_fields)" in task
    assert "cas:" in task
    assert "changed_when: true" in task
    assert "no_log: true" in task
    assert fields == [
        "vikunja_agent_read_password",
        "vikunja_agent_write_password",
        "vikunja_agent_clerk_password",
        "zammad_agent_write_api_token",
    ]
    assert "login_path | default(openbao_agent_tier_reader.tier)" in task
    assert "Remove the migrated password from the token leaf" in task
    assert "_login.get(_field, '') | string == _token.get(_field, '') | string" in task
    assert "openbao_agent_tier_reader.generated_fields" in task
    assert "openbao_agent_tier_reader.login_fields" in task


def _login_migration(tasks, field, destination, token_source, legacy_source):
    prepare = next(
        task for task in tasks
        if task.get("name") == "Prepare the login leaf without overwriting an existing password"
    )["ansible.builtin.set_fact"]
    merge = next(
        task for task in tasks
        if task.get("name") == "Merge the migrated login fields into the existing login leaf"
    )["ansible.builtin.set_fact"]
    variables = {
        "openbao_agent_tier_reader": {"tier": "vikunja-read", "login_fields": [field]},
        "openbao_agent_tier_login_existing": {"json": {"data": {"data": destination}}},
        "openbao_agent_tier_token_migration_source": {"json": {"data": {"data": token_source}}},
        "openbao_agent_tier_legacy_migration_source": {"json": {"data": {"data": legacy_source}}},
    }
    results = {}
    # Every key of one set_fact renders against the facts from before that task.
    for set_fact in (prepare, merge):
        rendered = {
            name: ast.literal_eval(_render(expression, variables).strip())
            for name, expression in set_fact.items()
        }
        results.update(rendered)
        variables.update(rendered)
    return results


def _token_removals_after_copy(tasks, field, destination, token_source):
    prepare = next(
        task for task in tasks
        if task.get("name") == "Prepare the token leaf after its login leaf holds the password"
    )["ansible.builtin.set_fact"]["openbao_agent_tier_token_remove_fields"]
    variables = {
        "openbao_agent_tier_reader": {"login_fields": [field]},
        "openbao_agent_tier_current": {"json": {"data": {"data": destination}}},
        "openbao_agent_tier_token_current": {"json": {"data": {"data": token_source}}},
    }
    return ast.literal_eval(_render(prepare, variables).strip())


def _legacy_removals_after_copy(tasks, field, destination, legacy_source):
    prepare = next(
        task for task in tasks
        if task.get("name") == "Prepare the legacy leaf with only provisioned tier fields removed"
    )["ansible.builtin.set_fact"]["openbao_agent_tier_legacy_remove_fields"]
    variables = {
        "openbao_agent_tier_reader": {"generated_fields": [], "login_fields": [field]},
        "openbao_agent_tier_current": {"json": {"data": {"data": destination}}},
        "openbao_agent_tier_legacy_current": {"json": {"data": {"data": legacy_source}}},
    }
    return ast.literal_eval(_render(prepare, variables).strip())


def test_legacy_login_password_copy_branch_copies_before_source_removal():
    tasks = yaml.safe_load(
        (ROOT / "roles/openbao/tasks/remove_app_agent_legacy_fields.yml").read_text(
            encoding="utf-8"
        )
    )
    field = next(
        reader["login_fields"][0]
        for reader in _defaults()["openbao_app_agent_tier_readers"]
        if reader.get("login_fields")
    )
    source = {field: "copied-password"}
    prepared = _login_migration(tasks, field, {}, {}, source)

    assert prepared["openbao_agent_tier_login_migrate_conflicts"] == []
    assert prepared["openbao_agent_tier_login_migrate_fields"] == source
    assert prepared["openbao_agent_tier_login_migrated_data"] == source
    assert _legacy_removals_after_copy(tasks, field, source, source) == [field]


def test_legacy_login_password_equal_branch_removes_only_the_equal_source():
    tasks = yaml.safe_load(
        (ROOT / "roles/openbao/tasks/remove_app_agent_legacy_fields.yml").read_text(
            encoding="utf-8"
        )
    )
    field = next(
        reader["login_fields"][0]
        for reader in _defaults()["openbao_app_agent_tier_readers"]
        if reader.get("login_fields")
    )
    existing = {field: "same-password"}
    prepared = _login_migration(tasks, field, existing, existing, {})

    assert prepared["openbao_agent_tier_login_migrate_conflicts"] == []
    assert prepared["openbao_agent_tier_login_migrate_fields"] == {}
    assert _token_removals_after_copy(tasks, field, existing, existing) == [field]


def test_legacy_login_password_mismatch_fails_before_any_write_or_delete():
    tasks = yaml.safe_load(
        (ROOT / "roles/openbao/tasks/remove_app_agent_legacy_fields.yml").read_text(
            encoding="utf-8"
        )
    )
    field = next(
        reader["login_fields"][0]
        for reader in _defaults()["openbao_app_agent_tier_readers"]
        if reader.get("login_fields")
    )
    destination = {field: "new-password"}
    source = {field: "old-password"}
    prepared = _login_migration(tasks, field, destination, source, {})
    fail_index, fail_task = next(
        (index, task) for index, task in enumerate(tasks)
        if task.get("name") == "Refuse a conflicting existing app-agent login password"
    )
    side_effect_indices = [
        index for index, task in enumerate(tasks)
        if (task.get("ansible.builtin.uri") or {}).get("method") in {"POST", "DELETE"}
    ]

    assert prepared["openbao_agent_tier_login_migrate_conflicts"] == [field]
    assert prepared["openbao_agent_tier_login_migrate_fields"] == {}
    assert _render(
        "{{ " + fail_task["when"] + " }}",
        {"openbao_agent_tier_login_migrate_conflicts": prepared["openbao_agent_tier_login_migrate_conflicts"]},
    ) == "True"
    assert side_effect_indices and all(index > fail_index for index in side_effect_indices)
    assert source[field] == "old-password"

    disagreeing_sources = _login_migration(
        tasks,
        field,
        {},
        {field: "token-password"},
        {field: "legacy-password"},
    )
    assert disagreeing_sources["openbao_agent_tier_login_migrate_conflicts"] == [field]
    assert disagreeing_sources["openbao_agent_tier_login_migrate_fields"] == {
        field: "token-password"
    }
    assert _render(
        "{{ " + fail_task["when"] + " }}",
        {"openbao_agent_tier_login_migrate_conflicts": disagreeing_sources[
            "openbao_agent_tier_login_migrate_conflicts"
        ]},
    ) == "True"


def test_check_mode_reads_the_leaves_and_reports_each_skipped_write():
    tasks = yaml.safe_load(
        (ROOT / "roles/openbao/tasks/remove_app_agent_legacy_fields.yml").read_text(encoding="utf-8")
    )
    reads = [task for task in tasks if task.get("ansible.builtin.uri", {}).get("method") == "GET"]
    writes = [index for index, task in enumerate(tasks) if task.get("ansible.builtin.uri", {}).get("method") == "POST"]
    assert len(reads) == 6
    assert all(task["check_mode"] is False for task in reads)
    assert len(writes) == 3
    for index in writes:
        report = tasks[index - 1]
        assert report["when"] == ["ansible_check_mode"] + tasks[index]["when"]
        assert "_data" not in report["ansible.builtin.debug"]["msg"]
        assert "no_log" not in report
