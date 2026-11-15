"""The rotated env document drops credentials that are now minted per call."""

from pathlib import Path

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

ROOT = Path(__file__).resolve().parents[1]
ROTATE_PLAYBOOK = ROOT / "playbooks/openbao-rotate-approles.yml"
ROTATE_TASKS = ROOT / "playbooks/tasks/openbao_rotate_one_domain.yml"


def test_rotation_replaces_domain_pair_prunes_per_call_pairs_and_keeps_siblings():
    tasks = yaml.safe_load(ROTATE_TASKS.read_text(encoding="utf-8"))
    block = next(task["block"] for task in tasks if "block" in task)
    builder = next(task for task in block if task["name"].startswith("Build the env document"))
    expression = builder["ansible.builtin.set_fact"]["rotate_env_new_data"]
    variables = {
        "rotate_env_current": {
            "json": {
                "data": {
                    "data": {
                        "OPENBAO_APPROLE_APPS_ROLE_ID": "old-role",
                        "OPENBAO_APPROLE_APPS_SECRET_ID": "old-secret",
                        "APPS_VAULT_ROLE_ID": "legacy-role",
                        "APPS_VAULT_SECRET_ID": "legacy-secret",
                        "OPENBAO_APPROLE_FLOW_LOCK_ROLE_ID": "stale-role",
                        "OPENBAO_APPROLE_FLOW_LOCK_SECRET_ID": "stale-secret",
                        "OPENBAO_APPROLE_OPENBAO_RECONCILE_ROLE_ID": "stale-role",
                        "OPENBAO_APPROLE_OPENBAO_RECONCILE_SECRET_ID": "stale-secret",
                        "OPENBAO_APPROLE_LOCAL_LLM_WORKSTATION_ROLE_ID": "host-role",
                        "OPENBAO_APPROLE_LOCAL_LLM_WORKSTATION_SECRET_ID": "host-secret",
                        "SLACK_CHANNEL": "test-channel",
                    }
                }
            }
        },
        "rotate_new_prefix": "OPENBAO_APPROLE_APPS",
        "rotate_legacy_prefix": "APPS_VAULT",
        "rotate_role_id_read": {"json": {"data": {"role_id": "new-role"}}},
        "rotate_new_secret_id": {"json": {"data": {"secret_id": "new-secret"}}},
    }
    templar = Templar(loader=DataLoader())
    templar.available_variables = variables

    rotated = templar.template(trust_as_template(expression))

    assert rotated == {
        "OPENBAO_APPROLE_APPS_ROLE_ID": "new-role",
        "OPENBAO_APPROLE_APPS_SECRET_ID": "new-secret",
        "OPENBAO_APPROLE_LOCAL_LLM_WORKSTATION_ROLE_ID": "host-role",
        "OPENBAO_APPROLE_LOCAL_LLM_WORKSTATION_SECRET_ID": "host-secret",
        "SLACK_CHANNEL": "test-channel",
    }


def test_seed_skips_only_a_live_pair_with_the_current_role_id():
    tasks = yaml.safe_load(ROTATE_TASKS.read_text(encoding="utf-8"))
    lookup_task = next(
        task
        for task in tasks
        if task["name"].startswith("Seed run, look up the carried secret_id")
    )
    lookup = lookup_task["ansible.builtin.uri"]
    assert lookup["method"] == "POST"
    assert lookup["url"].endswith("/secret-id/lookup")
    assert lookup["status_code"] == [200, 204, 400]
    assert lookup_task["no_log"] is True

    live_fact = next(
        task
        for task in tasks
        if task["name"].startswith("Decide whether the carried secret_id is live")
    )["ansible.builtin.set_fact"]["rotate_seed_secret_id_live"]
    skip_task = next(
        task for task in tasks if task["name"].startswith("Decide whether this run skips")
    )
    skip_expression = skip_task["ansible.builtin.set_fact"]["rotate_skip_identity"]
    rotate_block = next(task for task in tasks if task["name"].startswith("Rotate "))
    old_secret_task = next(
        task
        for task in rotate_block["block"]
        if task["name"].startswith("Resolve this domain's currently-live secret_id")
    )
    old_secret_expression = old_secret_task["ansible.builtin.set_fact"]["rotate_old_secret_id"]

    cases = (
        ("dead-204", {"status": 204}, "stored-role", None, False, "", False),
        # With no live role_id read, an empty stored role_id would match it and skip
        # unless the dead secret_id alone forces the re-seed.
        ("dead-empty-role-id", {"status": 204}, "", None, False, "", False),
        (
            "dead-400",
            {"status": 400, "json": {"errors": ["invalid secret id"]}},
            "stored-role",
            None,
            False,
            "",
            False,
        ),
        (
            "unexpected-400",
            {"status": 400, "json": {"errors": ["bad request"]}},
            "stored-role",
            None,
            False,
            "",
            True,
        ),
        (
            "live",
            {"status": 200, "json": {"data": {"secret_id_accessor": "accessor"}}},
            "live-role",
            "live-role",
            True,
            "stored-secret",
            False,
        ),
        (
            "role-id-mismatch",
            {"status": 200, "json": {"data": {"secret_id_accessor": "accessor"}}},
            "old-role",
            "live-role",
            False,
            "stored-secret",
            False,
        ),
    )
    for (
        name,
        lookup_result,
        stored_role_id,
        live_role_id,
        expected_skip,
        expected_old_secret,
        expected_lookup_failure,
    ) in cases:
        document = {
            "OPENBAO_APPROLE_SLACK_ADMIN_ROLE_ID": stored_role_id,
            "OPENBAO_APPROLE_SLACK_ADMIN_SECRET_ID": "stored-secret",
        }
        variables = {
            "bootstrap_seed_only": True,
            "rotate_env_document_enabled": True,
            "rotate_new_prefix": "OPENBAO_APPROLE_SLACK_ADMIN",
            "rotate_legacy_prefix": "SLACK_ADMIN_VAULT",
            "rotate_seed_probe": {"json": {"data": {"data": document}}},
            "rotate_seed_secret_id_lookup": lookup_result,
            "rotate_env_current": {"json": {"data": {"data": document}}},
        }
        if live_role_id is not None:
            variables["rotate_seed_role_id_read"] = {
                "json": {"data": {"role_id": live_role_id}}
            }

        templar = Templar(loader=DataLoader())
        templar.available_variables = variables
        lookup_failure_expression = "{{ " + lookup_task["failed_when"] + " }}"
        lookup_failed = templar.template(trust_as_template(lookup_failure_expression))
        is_live = templar.template(trust_as_template(live_fact))
        variables["rotate_seed_secret_id_live"] = is_live
        templar.available_variables = variables
        skips = templar.template(trust_as_template(skip_expression))
        variables["rotate_skip_identity"] = skips
        rotate_expression = "{{ " + rotate_block["when"] + " }}"
        should_rotate = templar.template(trust_as_template(rotate_expression))
        old_secret = templar.template(trust_as_template(old_secret_expression))

        assert bool(lookup_failed) is expected_lookup_failure, name
        assert bool(skips) is expected_skip, name
        assert bool(should_rotate) is (not expected_skip), name
        assert old_secret == expected_old_secret, name


def test_seed_reseeds_dead_pairs_only_in_human_gated_modes():
    tasks = yaml.safe_load(ROTATE_TASKS.read_text(encoding="utf-8"))
    pair_fact = next(
        task
        for task in tasks
        if task["name"].startswith("Decide whether the carried pair needs a re-seed")
    )["ansible.builtin.set_fact"]["rotate_seed_pair_needs_reseed"]
    skip_expression = next(
        task for task in tasks if task["name"].startswith("Decide whether this run skips")
    )["ansible.builtin.set_fact"]["rotate_skip_identity"]
    refusal_fact = next(
        task
        for task in tasks
        if task["name"].startswith("Decide whether an unattended run refuses")
    )["ansible.builtin.set_fact"]["rotate_seed_unattended_refusal"]
    rotate_block = next(task for task in tasks if task["name"].startswith("Rotate "))
    scheduled_guard = next(
        task
        for task in rotate_block["block"]
        if task["name"].startswith("Refuse an unattended re-seed")
    )
    rescue_record = next(
        task
        for task in rotate_block["rescue"]
        if task["name"].startswith("Record a failed rotation")
    )["ansible.builtin.set_fact"]["rotate_human_gated_seed_domains"]
    mint_index = next(
        index
        for index, task in enumerate(rotate_block["block"])
        if task["name"].startswith("Mint a fresh secret_id")
    )
    guard_index = rotate_block["block"].index(scheduled_guard)
    assert guard_index < mint_index

    cases = (
        ("dead-preissued", 204, "stored-role", "live-role", "preissued", False, True, False, True, True),
        ("dead-human", 400, "stored-role", "live-role", "human", False, True, False, True, True),
        ("dead-scheduled", 204, "stored-role", "live-role", "scheduled", False, True, True, False, True),
        # Fail-closed: a run that is neither human-gated nor pre-issued is refused
        # even if no mode flag names it as scheduled.
        ("dead-no-mode", 204, "stored-role", "live-role", "none", False, True, True, False, True),
        ("mismatched-preissued", 200, "old-role", "live-role", "preissued", False, True, False, True, True),
        ("mismatched-scheduled", 200, "old-role", "live-role", "scheduled", False, True, True, False, True),
        ("live-preissued", 200, "live-role", "live-role", "preissued", True, False, False, False, True),
        ("live-human", 200, "live-role", "live-role", "human", True, False, False, False, True),
        ("live-scheduled", 200, "live-role", "live-role", "scheduled", True, False, False, False, True),
        ("missing-scheduled", None, "live-role", "live-role", "scheduled", False, False, False, True, False),
    )
    for (
        name,
        status,
        stored_role_id,
        live_role_id,
        mode,
        expected_skip,
        expected_reseed,
        expected_refusal,
        expected_mint,
        secret_present,
    ) in cases:
        lookup_result = None
        if status is not None:
            lookup_result = (
                {"status": status}
                if status == 204
                else {"status": status, "json": {"errors": ["invalid secret id"]}}
                if status == 400
                else {"status": status, "json": {"data": {"secret_id_accessor": "accessor"}}}
            )
        document = {"OPENBAO_APPROLE_SLACK_ADMIN_ROLE_ID": stored_role_id}
        if secret_present:
            document["OPENBAO_APPROLE_SLACK_ADMIN_SECRET_ID"] = "stored-secret"
        variables = {
            "bootstrap_seed_only": True,
            "rotate_env_document_enabled": True,
            "rotate_domain_name": "slack-admin",
            "rotate_new_prefix": "OPENBAO_APPROLE_SLACK_ADMIN",
            "rotate_seed_probe": {
                "json": {
                    "data": {
                        "data": {
                            **document,
                        }
                    }
                }
            },
            "rotate_scheduled_mode": mode == "scheduled",
            "rotate_human_mode": mode == "human",
            "rotate_preissued_mode": mode == "preissued",
        }
        if lookup_result is not None:
            variables["rotate_seed_secret_id_lookup"] = lookup_result
        variables["rotate_seed_role_id_read"] = (
            {"json": {"data": {"role_id": live_role_id}}}
            if secret_present
            else {"skipped": True}
        )
        templar = Templar(loader=DataLoader())
        templar.available_variables = variables
        live_fact = next(
            task
            for task in tasks
            if task["name"].startswith("Decide whether the carried secret_id is live")
        )["ansible.builtin.set_fact"]["rotate_seed_secret_id_live"]
        variables["rotate_seed_secret_id_live"] = (
            templar.template(trust_as_template(live_fact)) if secret_present else True
        )
        templar.available_variables = variables
        variables["rotate_seed_pair_needs_reseed"] = templar.template(trust_as_template(pair_fact))
        variables["rotate_skip_identity"] = templar.template(trust_as_template(skip_expression))
        templar.available_variables = variables

        variables["rotate_seed_unattended_refusal"] = templar.template(
            trust_as_template(refusal_fact)
        )
        templar.available_variables = variables
        refusal = bool(
            templar.template(trust_as_template("{{ " + scheduled_guard["when"] + " }}"))
        )
        records_human_gate = "slack-admin" in templar.template(
            trust_as_template(rescue_record)
        )
        enters_rotate_block = bool(
            templar.template(trust_as_template("{{ " + rotate_block["when"] + " }}"))
        )
        reaches_mint = enters_rotate_block and not refusal and guard_index < mint_index

        assert bool(variables["rotate_seed_pair_needs_reseed"]) is expected_reseed, name
        assert bool(variables["rotate_skip_identity"]) is expected_skip, name
        assert refusal is expected_refusal, name
        assert records_human_gate is expected_refusal, name
        assert reaches_mint is expected_mint, name
        if expected_refusal:
            message = templar.template(
                trust_as_template(scheduled_guard["ansible.builtin.fail"]["msg"])
            )
            assert "slack-admin" in message, name
            assert "human-gated run is required" in message.lower(), name


def test_scheduled_seed_failure_retains_human_gate_guidance():
    playbook = yaml.safe_load(ROTATE_PLAYBOOK.read_text(encoding="utf-8"))
    final_failure = next(
        task
        for task in playbook[0]["tasks"]
        if task["name"].startswith("Fail the run when any identity or KV target did not rotate")
    )
    message = final_failure["ansible.builtin.fail"]["msg"]
    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        "rotate_failed_domains": ["slack-admin"],
        "rotate_human_gated_seed_domains": ["slack-admin"],
    }

    rendered = templar.template(trust_as_template(message))

    assert "AppRole rotation failed for: slack-admin." in rendered
    assert "A human-gated run is required to re-seed slack-admin." in rendered
    assert "openbao-unlock --via yubikey approle-secret-id-rotate" in rendered
    assert "OPENBAO_ROTATE_TOKEN=$BAO_TOKEN" in rendered
    assert "-e bootstrap_seed_only=true" in rendered
