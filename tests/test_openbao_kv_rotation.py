"""Contracts for private, data-driven KV value rotation."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "roles/openbao/templates/approle-secret-id-rotate-policy.hcl.j2"
DEVELOP_BASELINE = "c6fa6dc649bc317298324c9b5b14822685ad56bf"
DEVELOP_TEMPLATE_SHA256 = "dba687fba4dacce8a86667b86a8ccc3ebfa4c3b144910a14e30fd19dea3ae020"
AGE_TEMPLATE = ROOT / "roles/openbao/templates/openbao-secret-age.sh.j2"
VALIDATION_PLAY = ROOT / "tests/openbao_kv_rotation/verify_target_validation.yml"
ROTATION_TASKS = ROOT / "playbooks/tasks/openbao_rotate_kv_target.yml"


def _policy_context(targets: list[dict], *, scheduled: bool = False) -> dict:
    return {
        "ansible_managed": "Ansible managed",
        "item": {"scheduled_only": scheduled},
        "openbao_secrets_domain_approle_names": ["svc-a"],
        "openbao_approle_secret_id_rotate_scheduled_approle_name": "rotator-scheduled",
        "openbao_host_secret_zero_approle_names": ["seed-a"],
        "openbao_roster_router_key_reader_name": "router-reader",
        "openbao_roster_gateway_key_reader_name": "gateway-reader",
        "openbao_kv_mount": "example",
        "openbao_rotate_doppler_token_kv_path": "system/doppler-token",
        "openbao_kv_rotation_targets": targets,
        "openbao_kv_rotation_semaphore_token": {},
        "openbao_kv_rotation_terrakube_token": {},
    }


def _render_source(source: str, context: dict) -> str:
    templar = Templar(loader=DataLoader())
    templar.available_variables = context
    return templar.template(trust_as_template(source))


def _develop_policy_source() -> str:
    result = subprocess.run(
        [
            "git",
            "show",
            f"{DEVELOP_BASELINE}:roles/openbao/templates/approle-secret-id-rotate-policy.hcl.j2",
        ],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode == 0:
        assert hashlib.sha256(result.stdout.encode()).hexdigest() == DEVELOP_TEMPLATE_SHA256
        return result.stdout

    # Shallow CI checkouts may not include origin/develop. The new table block
    # is appended at EOF, so use the unchanged template prefix as that baseline.
    source = POLICY.read_text(encoding="utf-8")
    marker = "\n{% set _kv_rotation_write_paths = [] -%}"
    assert marker in source
    baseline = source.split(marker, maxsplit=1)[0] + "\n"
    assert hashlib.sha256(baseline.encode()).hexdigest() == DEVELOP_TEMPLATE_SHA256
    return baseline


def _row(name: str, path: str) -> dict:
    return {
        "name": name,
        "mount": "example",
        "path": path,
        "field": "api_key",
        "secret_in_url": True,
        "generate": {"kind": "random", "length": 40},
        "push": {"kind": "none", "consumer_reads_openbao": True},
        "probe": {
            "url": "https://svc-a.example.invalid/check?token=__VALUE__",
            "method": "GET",
            "headers": {},
            "expect_status": 200,
        },
        "invalidate": {
            "kind": "http",
            "url": "https://svc-a.example.invalid/revoke?token=__OLD__&replacement=__NEW__",
            "method": "POST",
            "headers": {},
            "expect_status": 204,
        },
        "old_dead_status": [401, 403],
    }


def test_empty_kv_table_keeps_develop_policy_render_byte_identical():
    develop_policy = _develop_policy_source()
    for scheduled in (False, True):
        context = _policy_context([], scheduled=scheduled)
        rendered = _render_source(POLICY.read_text(encoding="utf-8"), context)
        baseline = _render_source(develop_policy, context)
        assert rendered == baseline


def test_two_kv_rows_add_only_exact_data_metadata_admin_and_push_token_paths():
    first = _row("svc-a", "apps/svc-a")
    first["push"] = {"kind": "semaphore", "project_id": 1, "template_id": 2}
    second = _row("svc-b", "apps/svc-b")
    second["generate"] = {
        "kind": "vendor_roll",
        "url": "https://svc-b.example.invalid/rotate",
        "method": "POST",
        "headers": {"Authorization": "Bearer __ADMIN_CREDENTIAL__"},
        "value_from": "data.api_key",
        "admin_credential": {
            "mount": "example",
            "path": "system/vendor-admin",
            "field": "token",
        },
    }
    second["push"] = {
        "kind": "terrakube",
        "organization_id": "example",
        "workspace_id": "svc-a",
    }
    context = _policy_context([first, second])
    context["openbao_kv_rotation_semaphore_token"] = {
        "mount": "example",
        "path": "system/semaphore-token",
        "field": "token",
    }
    context["openbao_kv_rotation_terrakube_token"] = {
        "mount": "example",
        "path": "system/terrakube-token",
        "field": "token",
    }

    policy_source = POLICY.read_text(encoding="utf-8")
    rendered = _render_source(policy_source, context)
    expected = {
        "example/data/apps/svc-a": '["read", "create", "update"]',
        "example/metadata/apps/svc-a": '["read"]',
        "example/data/apps/svc-b": '["read", "create", "update"]',
        "example/metadata/apps/svc-b": '["read"]',
        "example/data/system/vendor-admin": '["read"]',
        "example/data/system/semaphore-token": '["read"]',
        "example/data/system/terrakube-token": '["read"]',
    }
    for path, capabilities in expected.items():
        assert f'path "{path}" {{\n  capabilities = {capabilities}\n}}' in rendered

    paths = re.findall(r'(?m)^path "([^"]+)"', rendered)
    baseline_paths = re.findall(
        r'(?m)^path "([^"]+)"', _render_source(_develop_policy_source(), context)
    )
    assert len(paths) == len(set(paths))
    assert set(paths) == set(baseline_paths) | set(expected)
    assert 'path "example/data/*"' not in rendered
    assert 'path "example/metadata/*"' not in rendered


def test_policy_omits_token_stanzas_for_incomplete_mappings():
    semaphore = _row("svc-a", "apps/svc-a")
    semaphore["push"] = {"kind": "semaphore", "project_id": 1, "template_id": 2}
    terrakube = _row("svc-b", "apps/svc-b")
    terrakube["push"] = {
        "kind": "terrakube",
        "organization_id": "example",
        "workspace_id": "svc-a",
    }
    context = _policy_context([semaphore, terrakube])
    context["openbao_kv_rotation_semaphore_token"] = {
        "mount": "example",
        "path": "system/semaphore-token",
    }
    context["openbao_kv_rotation_terrakube_token"] = {
        "mount": "example",
        "path": "system/terrakube-token",
        "field": "",
    }

    rendered = _render_source(POLICY.read_text(encoding="utf-8"), context)
    assert 'path "example/data/system/semaphore-token"' not in rendered
    assert 'path "example/data/system/terrakube-token"' not in rendered


def _run_validation(
    rows: list[dict],
    *,
    semaphore_token: dict | None = None,
    terrakube_token: dict | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    for key in (
        "OPENBAO_KV_ROTATION_TARGETS",
        "OPENBAO_KV_ROTATION_SEMAPHORE_TOKEN",
        "OPENBAO_KV_ROTATION_TERRAKUBE_TOKEN",
    ):
        env.pop(key, None)
    env["OPENBAO_KV_ROTATION_TARGETS"] = json.dumps(rows)
    if semaphore_token is not None:
        env["OPENBAO_KV_ROTATION_SEMAPHORE_TOKEN"] = json.dumps(semaphore_token)
    if terrakube_token is not None:
        env["OPENBAO_KV_ROTATION_TERRAKUBE_TOKEN"] = json.dumps(terrakube_token)
    return subprocess.run(
        [
            "ansible-playbook",
            "-i",
            "localhost,",
            "-c",
            "local",
            str(VALIDATION_PLAY),
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        check=False,
        text=True,
    )


def test_target_schema_assertions_accept_valid_row_and_reject_bad_rows():
    valid = _row("svc-a", "apps/svc-a")
    assert _run_validation([valid]).returncode == 0

    missing_field = dict(valid)
    missing_field.pop("field")
    bad_generate_kind = {**valid, "generate": {"kind": "other"}}
    duplicate_name = [valid, {**_row("svc-a", "apps/svc-b")}]
    skipped_old_probe = {
        **valid,
        "push": {"kind": "none"},
        "invalidate": {"kind": "none"},
        "old_dead_status": [],
    }

    for bad_rows in ([missing_field], [bad_generate_kind], duplicate_name, [skipped_old_probe]):
        result = _run_validation(list(bad_rows))
        output = result.stdout + result.stderr
        assert result.returncode != 0, output
        assert "KV rotation target" in output


def _assert_target_rejected(row: dict, **token_refs: dict) -> str:
    result = _run_validation([row], **token_refs)
    output = result.stdout + result.stderr
    assert result.returncode != 0, output
    assert row["name"] in output, output
    return output


def test_target_paths_and_fields_allow_only_safe_segments():
    valid = _row("svc-a", "apps/svc-a")
    invalid_segments = (
        "",
        "/leading",
        "trailing/",
        "apps//svc-a",
        "apps/../svc-a",
        "apps/*",
        "apps/+",
        "apps/svc a",
    )
    for key in ("mount", "path"):
        for value in invalid_segments:
            _assert_target_rejected({**valid, key: value})

    for field in ("", "api/key", "api key", "api*key", "api+key"):
        _assert_target_rejected({**valid, "field": field})


def test_nonempty_push_token_references_must_be_complete_and_safe():
    valid = _row("svc-a", "apps/svc-a")
    semaphore_row = {
        **valid,
        "push": {"kind": "semaphore", "project_id": 1, "template_id": 2},
    }
    terrakube_row = {
        **valid,
        "push": {
            "kind": "terrakube",
            "organization_id": "example",
            "workspace_id": "svc-a",
        },
    }
    invalid_refs = (
        {"mount": "example"},
        {"mount": "example", "path": "system/token"},
        {"mount": "example", "path": "system/../token", "field": "token"},
        {"mount": "example", "path": "system/token", "field": "token/name"},
    )
    for token in invalid_refs:
        _assert_target_rejected(semaphore_row, semaphore_token=token)
        _assert_target_rejected(terrakube_row, terrakube_token=token)


def test_http_invalidation_without_push_requires_consumer_read_contract():
    row = _row("svc-a", "apps/svc-a")
    row["push"] = {"kind": "none"}
    _assert_target_rejected(row)

    row["push"]["consumer_reads_openbao"] = True
    assert _run_validation([row]).returncode == 0


def test_invalidate_none_cannot_claim_old_value_dead_statuses():
    row = _row("svc-a", "apps/svc-a")
    row["push"] = {"kind": "semaphore", "project_id": 1, "template_id": 2}
    row["invalidate"] = {"kind": "none"}
    row["old_dead_status"] = [401]
    _assert_target_rejected(row)


def test_semaphore_ids_must_be_positive_integer_values():
    row = _row("svc-a", "apps/svc-a")
    for key, value in (
        ("project_id", "not-an-id"),
        ("template_id", "0"),
        ("project_id", 0),
        ("template_id", 1.5),
    ):
        bad = {
            **row,
            "push": {"kind": "semaphore", "project_id": 12, "template_id": 34},
        }
        bad["push"][key] = value
        _assert_target_rejected(bad)

    for value in (7, "007"):
        valid = {
            **row,
            "push": {"kind": "semaphore", "project_id": value, "template_id": 34},
        }
        assert _run_validation([valid]).returncode == 0


def test_vendor_roll_requires_admin_credential_placeholder_during_validation():
    row = _row("svc-a", "apps/svc-a")
    row["generate"] = {
        "kind": "vendor_roll",
        "url": "https://api.example.invalid/rotate",
        "method": "POST",
        "headers": {},
        "value_from": "data.api_key",
        "admin_credential": {"mount": "example", "path": "system/admin", "field": "token"},
    }
    _assert_target_rejected(row)

    tasks = yaml.safe_load(ROTATION_TASKS.read_text(encoding="utf-8"))
    runtime_check = _find_task(tasks, "Require a vendor admin credential placeholder")
    assert "__ADMIN_CREDENTIAL__" in runtime_check["ansible.builtin.assert"]["that"][0]


def test_secret_placeholders_in_urls_require_explicit_opt_in():
    row = _row("svc-a", "apps/svc-a")
    row["secret_in_url"] = False
    _assert_target_rejected(row)

    row["probe"]["url"] = "https://api.example.invalid/check"
    row["invalidate"]["url"] = "https://api.example.invalid/revoke"
    assert _run_validation([row]).returncode == 0


def _find_task(tasks: list[dict], name: str) -> dict:
    for task in tasks:
        if task.get("name") == name:
            return task
        for section in ("block", "rescue", "always"):
            nested = task.get(section)
            if isinstance(nested, list):
                try:
                    return _find_task(nested, name)
                except LookupError:
                    pass
    raise LookupError(name)


def _render_expression(expression: str, context: dict) -> object:
    templar = Templar(loader=DataLoader())
    templar.available_variables = context
    return templar.template(trust_as_template(expression))


def test_body_builders_allow_missing_optional_bodies_and_uri_omits_them():
    tasks = yaml.safe_load(ROTATION_TASKS.read_text(encoding="utf-8"))
    cases = (
        (
            "Prepare the vendor roll request",
            "rotate_kv_vendor_body",
            "Request a vendor-rolled replacement",
        ),
        (
            "Prepare the new-value probe request",
            "rotate_kv_new_probe_body",
            "Probe the replacement value",
        ),
        (
            "Prepare the invalidation request body",
            "rotate_kv_invalidate_body",
            "Invalidate the previous value",
        ),
        (
            "Prepare the old-value probe request",
            "rotate_kv_old_probe_body",
            "Probe that the previous value is dead",
        ),
    )
    context = {
        "rotate_kv_target": {
            "generate": {
                "kind": "vendor_roll",
                "url": "https://api.example.invalid/roll",
                "headers": {},
            },
            "probe": {"url": "https://api.example.invalid/probe", "headers": {}},
            "invalidate": {
                "kind": "http",
                "url": "https://api.example.invalid/revoke",
                "headers": {},
            },
        },
        "rotate_kv_admin_credential": "admin-token",
        "rotate_kv_new_value": "new-token",
        "rotate_kv_old_value": "old-token",
        "omit": "OMIT",
    }
    for prep_name, result_key, request_name in cases:
        prep = _find_task(tasks, prep_name)
        built = _render_expression(prep["ansible.builtin.set_fact"][result_key], context)
        built_body = yaml.safe_load(built) if isinstance(built, str) else built
        assert built_body == {}
        request = _find_task(tasks, request_name)
        omitted = _render_expression(request["ansible.builtin.uri"]["body"], context)
        assert omitted == "OMIT"


def test_secret_values_are_url_encoded_at_each_url_substitution():
    tasks = yaml.safe_load(ROTATION_TASKS.read_text(encoding="utf-8"))
    context = {
        "rotate_kv_target": {
            "generate": {
                "url": "https://api.example.invalid/roll?token=__ADMIN_CREDENTIAL__"
            },
            "probe": {"url": "https://api.example.invalid/check?token=__VALUE__"},
            "invalidate": {
                "url": "https://api.example.invalid/revoke?old=__OLD__&new=__NEW__"
            },
        },
        "rotate_kv_admin_credential": "a+b&c",
        "rotate_kv_new_value": "a+b&c",
        "rotate_kv_old_value": "a+b&c",
    }
    cases = (
        ("Prepare the vendor roll request", "rotate_kv_vendor_url"),
        ("Probe the replacement value", "url"),
        ("Invalidate the previous value", "url"),
        ("Probe that the previous value is dead", "url"),
    )
    for task_name, key in cases:
        task = _find_task(tasks, task_name)
        expression = (
            task["ansible.builtin.set_fact"][key]
            if "ansible.builtin.set_fact" in task
            else task["ansible.builtin.uri"][key]
        )
        rendered = _render_expression(expression, context)
        assert "a%2Bb%26c" in rendered, rendered
        assert "a+b&c" not in rendered, rendered


def test_push_poll_retries_are_timeout_divided_by_the_shared_delay():
    tasks = yaml.safe_load(ROTATION_TASKS.read_text(encoding="utf-8"))
    assert tasks[0]["vars"]["rotate_kv_push_poll_delay_sec"] == 5
    context = {
        "rotate_kv_push_poll_delay_sec": 5,
        "openbao_kv_rotation_push_timeout_sec": 1500,
    }
    for task_name in (
        "Wait for the Semaphore task to finish",
        "Wait for the Terrakube job to finish",
    ):
        task = _find_task(tasks, task_name)
        retries = _render_expression(task["retries"], context)
        delay = _render_expression(task["delay"], context)
        assert int(retries) == 300
        assert int(delay) == 5


def test_due_selection_jinja_handles_age_forcing_and_all():
    tasks = yaml.safe_load(ROTATION_TASKS.read_text(encoding="utf-8"))
    due_task = next(
        task for task in tasks[0]["block"]
        if task.get("name") == "Decide whether the KV target is due"
    )
    expression = due_task["ansible.builtin.set_fact"]["rotate_kv_target_is_due"]

    for age_seconds, selected, expected in (
        (2_592_000, [], True),
        (2_591_999, ["svc-a"], True),
        (0, ["all"], True),
        (2_591_999, [], False),
    ):
        templar = Templar(loader=DataLoader())
        templar.available_variables = {
            "rotate_kv_targets_normalized": selected,
            "rotate_kv_target": {"name": "svc-a"},
            "rotate_kv_target_age_seconds": age_seconds,
            "openbao_rotation_target_days": 30,
        }
        result = templar.template(trust_as_template(expression))
        assert str(result).lower() == str(expected).lower()


def _render_secret_age(dashboard_url: str, slack_member_id: str = "") -> str:
    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        "ansible_managed": "Ansible managed",
        "openbao_secret_age_schedule": "*-*-* 06:05:00 UTC",
        "openbao_secret_age_target_days": 30,
        "openbao_secret_age_warn_days": 40,
        "openbao_secret_age_max_days": 47,
        "openbao_api_port": 8200,
        "openbao_secret_age_report_path": "/var/log/openbao/secret-age.json",
        "openbao_secret_age_ntfy_url": "https://ntfy.example.invalid/secrets-security",
        "openbao_secret_age_healthcheck_url": "",
        "openbao_secret_age_dashboard_url": dashboard_url,
        "openbao_secret_age_slack_member_id": slack_member_id,
        "openbao_kv_mounts": [{"path": "example", "age_audit": True}],
        "openbao_absent_stderr_marker": "example marker",
        "openbao_approles": [],
        "openbao_group": "openbao",
        "openbao_audit_log_dir": "/var/log/openbao",
    }
    return templar.template(trust_as_template(AGE_TEMPLATE.read_text(encoding="utf-8")))


def test_secret_age_warn_threshold_and_optional_dashboard_render():
    without_dashboard = _render_secret_age("")
    assert "WARN_DAYS=40" in without_dashboard
    assert "Due soon, rotation should have run" in without_dashboard
    assert "https://dashboard.example.invalid" not in without_dashboard

    with_dashboard = _render_secret_age("https://dashboard.example.invalid/secret-age")
    assert "https://dashboard.example.invalid/secret-age" in with_dashboard

    with_mention = _render_secret_age("", "svc-a")
    assert 'SLACK_MEMBER_ID="svc-a"' in with_mention
    assert 'body="<@${SLACK_MEMBER_ID}> ${body}"' in with_mention
