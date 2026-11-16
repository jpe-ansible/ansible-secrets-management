"""Check-mode reporting exposes AppRole names and counts, never bound values."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.loader import init_plugin_loader
from ansible.template import Templar, trust_as_template
from ansible.utils.collection_loader import AnsibleCollectionConfig

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "roles/openbao/tasks/init/10c-approle-ttl-bounds.yml"
REPORT_NAME = "Report AppRoles whose TTL or bounds would be retuned in check mode"
RETUNE_NAME = "Reconcile AppRole TTL and token bounds on existing AppRoles"


def _tasks():
    return yaml.safe_load(TASKS.read_text(encoding="utf-8"))


def _task(name):
    for task in _tasks():
        if task.get("name") == name:
            return task
    raise AssertionError(f"task {name!r} not found")


def _report_task():
    return _task(REPORT_NAME)


def _retune_task():
    return _task(RETUNE_NAME)


def _mark_templates(value):
    if isinstance(value, str):
        return trust_as_template(value)
    if isinstance(value, dict):
        return {key: _mark_templates(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_mark_templates(item) for item in value]
    return value


def _render(template, variables):
    # The drift vars use community.general.to_seconds.
    if not AnsibleCollectionConfig.collection_finder:
        init_plugin_loader()
    templar = Templar(loader=DataLoader())
    templar.available_variables = _mark_templates(variables)
    return templar.template(trust_as_template(template))


def _parameters(bound_cidrs):
    return {
        "secret_id_bound_cidrs": bound_cidrs,
        "token_bound_cidrs": bound_cidrs,
        "secret_id_ttl": "1h",
        "secret_id_num_uses": 1,
        "token_ttl": "1h",
        "token_max_ttl": "2h",
        "token_explicit_max_ttl": "2h",
        "token_type": "default",
        "token_policies": ["default"],
        "bind_secret_id": True,
    }


def _live(secret_id_bounds, token_bounds):
    return {
        "secret_id_bound_cidrs": secret_id_bounds,
        "token_bound_cidrs": token_bounds,
        "secret_id_ttl": 3600,
        "secret_id_num_uses": 1,
        "token_ttl": 3600,
        "token_max_ttl": 7200,
        "token_explicit_max_ttl": 7200,
        "token_type": "default",
    }


def _context(row, live):
    block_vars = _report_task()["vars"]
    namespace = {
        "item": [row, {"rc": 0, "stdout": json.dumps({"data": live})}],
        "openbao_cli_become": False,
        "openbao_approle_cidr_class_map": {row["name"]: "machine"},
        "openbao_approle_cli_parameters": {
            row["name"]: _parameters(row["secret_id_bound_cidrs"]),
        },
    }
    for name, template in block_vars.items():
        namespace[name] = _render(template, namespace)
    return namespace


def _report_when_holds(report, context, check_mode):
    conditions = report["when"]
    return (
        "ansible_check_mode" in conditions
        and check_mode
        and "openbao_bootstrap_token is defined" in conditions
        and "openbao_bootstrap_token" in context
        and "(item.1.rc | default(1)) == 0" in conditions
        and context["item"][1]["rc"] == 0
        and "approle_bounds_drift | bool" in conditions
        and bool(context["approle_bounds_drift"])
    )


class ApproleBoundsCheckReportTest(unittest.TestCase):
    def test_drifted_bounds_make_check_report_conditions_true(self):
        row = {
            "name": "approle-drifted",
            "secret_id_bound_cidrs": "192.0.2.5/32, 192.0.2.6/32",
        }
        live = _live(
            ["192.0.2.5/32", "192.0.2.6/32", "198.51.100.7/32"],
            ["192.0.2.5", "192.0.2.6", "198.51.100.7"],
        )
        context = _context(row, live)
        context["openbao_bootstrap_token"] = "check-mode-fixture"

        self.assertTrue(context["approle_bounds_drift"])
        self.assertTrue(_report_when_holds(_report_task(), context, check_mode=True))

    def test_matching_slash32_and_bare_address_bounds_are_not_drift(self):
        row = {
            "name": "approle-matched",
            "secret_id_bound_cidrs": "192.0.2.5/32, 192.0.2.6/32",
        }
        live = _live(
            ["192.0.2.5/32", "192.0.2.6/32"],
            ["192.0.2.5", "192.0.2.6"],
        )

        self.assertFalse(_context(row, live)["approle_bounds_drift"])

    def test_drift_message_contains_only_name_counts_and_drift_flags(self):
        row = {
            "name": "approle-drifted",
            "secret_id_bound_cidrs": "192.0.2.5/32, 192.0.2.6/32",
        }
        live = _live(
            ["192.0.2.5/32", "192.0.2.6/32", "198.51.100.7/32"],
            ["192.0.2.5", "192.0.2.6", "198.51.100.7"],
        )
        message = _render(_report_task()["ansible.builtin.debug"]["msg"], _context(row, live))
        addresses = (
            "192.0.2.5",
            "192.0.2.5/32",
            "192.0.2.6",
            "192.0.2.6/32",
            "198.51.100.7",
            "198.51.100.7/32",
        )

        self.assertTrue("approle-drifted" in message, "report omitted the AppRole name")
        self.assertTrue("live_secret_id_bound_entries=3" in message, "report omitted live secret-id count")
        self.assertTrue("live_token_bound_entries=3" in message, "report omitted live token count")
        self.assertTrue("declared_bound_entries=2" in message, "report omitted declared bound count")
        self.assertTrue("ttl_or_uses=false" in message, "report omitted TTL/use drift status")
        self.assertTrue("token_type=false" in message, "report omitted token-type drift status")
        self.assertTrue("token_explicit_max_ttl=false" in message, "report omitted explicit-TTL drift status")
        self.assertTrue("bound_ranges=true" in message, "report omitted bound-range drift status")
        self.assertFalse(any(address in message for address in addresses), "report disclosed a bound value")

    def test_report_and_retune_task_structure(self):
        tasks = _tasks()
        report = _report_task()
        retune = _retune_task()

        self.assertIn("ansible.builtin.debug", report)
        self.assertEqual(report["ansible.builtin.debug"]["msg"].split(",", 1)[0], "{{ item.0.name }}")
        self.assertIs(report["changed_when"], True)
        self.assertIsNot(report.get("no_log", False), True)
        self.assertEqual(report["loop_control"]["label"], "{{ item.0.name }}")
        self.assertLess(tasks.index(report), tasks.index(retune))
        self.assertIn("ansible_check_mode", report["when"])
        self.assertIs(retune["no_log"], True)
        # One definition of the drift computation: both tasks carry the same vars.
        self.assertEqual(report["vars"], retune["vars"])

    @unittest.skipUnless(shutil.which("ansible-playbook"), "ansible-playbook is not installed")
    def test_check_mode_recap_reports_exactly_one_changed_approle(self):
        drifted_row = {
            "name": "approle-drifted",
            "secret_id_bound_cidrs": "192.0.2.5/32, 192.0.2.6/32",
        }
        matched_row = {
            "name": "approle-matched",
            "secret_id_bound_cidrs": "192.0.2.5/32, 192.0.2.6/32",
        }
        drifted_live = _live(
            ["192.0.2.5/32", "192.0.2.6/32", "198.51.100.7/32"],
            ["192.0.2.5", "192.0.2.6", "198.51.100.7"],
        )
        matched_live = _live(
            ["192.0.2.5/32", "192.0.2.6/32"],
            ["192.0.2.5", "192.0.2.6"],
        )
        fixtures = [
            (drifted_row, drifted_live),
            (matched_row, matched_live),
        ]
        targets = [row for row, _ in fixtures]
        parameters = {row["name"]: _parameters(row["secret_id_bound_cidrs"]) for row, _ in fixtures}
        checks = [
            {"rc": 0, "stdout": json.dumps({"data": live})}
            for _, live in fixtures
        ]
        playbook_data = [{
            "hosts": "localhost",
            "connection": "local",
            "gather_facts": False,
            "vars": {
                "openbao_bootstrap_token": "check-mode-fixture",
                "openbao_cli_become": False,
                "openbao_cli_host": "localhost",
                "openbao_cli_addr": "https://openbao.invalid",
                "openbao_approle_config_targets": targets,
                "openbao_manageable_approles": targets,
                "openbao_approle_cli_parameters": parameters,
                "openbao_approle_cidr_class_map": {row["name"]: "machine" for row in targets},
                "openbao_approle_checks": {"results": checks},
            },
            "tasks": [{"ansible.builtin.include_tasks": str(TASKS)}],
        }]

        with tempfile.TemporaryDirectory() as temp_dir:
            playbook = Path(temp_dir) / "approle-check-report.yml"
            playbook.write_text(yaml.safe_dump(playbook_data, sort_keys=False), encoding="utf-8")
            result = subprocess.run(
                ["ansible-playbook", "--check", "-i", "localhost,", str(playbook)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

        self.assertEqual(result.returncode, 0, "ansible-playbook check-mode fixture failed")
        output = result.stdout + result.stderr
        recap = re.search(r"^localhost\s*:\s+.*\bchanged=(\d+)\b", output, re.MULTILINE)
        self.assertTrue(recap is not None and recap.group(1) == "1", "check-mode recap did not report changed=1")
        self.assertTrue("approle-drifted" in output, "check-mode output omitted the drifted AppRole")
        self.assertFalse("check-mode-fixture" in output, "check-mode output disclosed a token fixture")
        addresses = (
            "192.0.2.5",
            "192.0.2.5/32",
            "192.0.2.6",
            "192.0.2.6/32",
            "198.51.100.7",
            "198.51.100.7/32",
        )
        self.assertFalse(any(address in output for address in addresses), "check-mode output disclosed a bound value")


if __name__ == "__main__":
    unittest.main()
