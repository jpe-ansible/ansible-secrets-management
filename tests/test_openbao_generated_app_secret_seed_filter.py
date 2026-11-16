"""Keep generated app-secret seed filtering safe and names-only."""

import json
from pathlib import Path
import re
import unittest

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main/01b-app-secret-generation.yml"
INIT_TASKS = ROOT / "roles/openbao/tasks/init/03-kv-mounts-and-seed-secrets.yml"
PREPARE_TASKS = ROOT / "roles/openbao/tasks/prepare_generated_app_secret_seed.yml"
ACCUMULATOR = "openbao_seeded_app_secret_values"
ACCUMULATOR_TASK = "Accumulate final generated app-secret values for later callers"


def _mark_templates(value):
    if isinstance(value, str):
        return trust_as_template(value)
    if isinstance(value, dict):
        return {key: _mark_templates(nested) for key, nested in value.items()}
    if isinstance(value, list):
        return [_mark_templates(nested) for nested in value]
    return value


def _render(value, variables):
    templar = Templar(loader=DataLoader())
    templar.available_variables = _mark_templates(variables)
    template = value
    if "{{" not in value and "{%" not in value:
        template = "{{ " + value + " }}"
    return templar.template(trust_as_template(template))


def _flatten_tasks(tasks):
    for task in tasks:
        yield task
        for key in ("block", "rescue", "always"):
            yield from _flatten_tasks(task.get(key, []))


def _task_by_name(path, name):
    for task in _flatten_tasks(yaml.safe_load(path.read_text(encoding="utf-8"))):
        if task.get("name") == name:
            return task
    raise AssertionError(f"task {name!r} not found in {path}")


def _prepare_task(name):
    return _task_by_name(PREPARE_TASKS, name)


def _set_fact(task_name, variables):
    task = _prepare_task(task_name)
    facts = task["ansible.builtin.set_fact"]
    variables.update({key: _render(value, variables) for key, value in facts.items()})
    return task


def _app_map(**fields):
    return {name: value for name, value in fields.items()}


def _seed_selection(apps, *, named=None, absent_only=False, present_by_app=None,
                    rotate_fields=None, required_apps=None):
    named = [] if named is None else named
    present_by_app = {} if present_by_app is None else present_by_app
    rotate_fields = [] if rotate_fields is None else rotate_fields
    required_apps = ["required"] if required_apps is None else required_apps
    variables = {
        "openbao_seeded_generated_app_secrets": apps,
        "openbao_seed_only_apps": named,
        "openbao_seed_absent_only": absent_only,
        "openbao_seed_rotate_list": rotate_fields,
        "openbao_seed_required_apps": required_apps,
        "openbao_seed_apps_with_absent_fields": [],
    }
    if absent_only:
        reads = []
        for app, fields in apps.items():
            present = present_by_app.get(app, fields)
            if present is None:
                reads.append({
                    "item": {"key": app, "value": fields},
                    "rc": 1,
                    "stderr": "No value found at placeholder path",
                })
            else:
                reads.append({
                    "item": {"key": app, "value": fields},
                    "rc": 0,
                    "stdout": json.dumps({"data": {"subkeys": {key: None for key in present}}}),
                })
        variables["openbao_seed_subkeys_reads"] = {"results": reads}
        _set_fact("Collect generated app leaves with absent fields", variables)
    _set_fact("Find apps with fields requested for rotation", variables)
    _set_fact("Select generated app-secret leaves by name", variables)
    _set_fact("Select generated app-secret leaves to seed", variables)
    return variables


def _loop_names(variables):
    return [item["key"] for item in variables["openbao_seed_apps_to_seed"]]


class GeneratedAppSecretSeedFilterTest(unittest.TestCase):
    def test_defaults_keep_all_apps_and_do_not_run_the_read_pass(self):
        apps = _app_map(a=["a_key"], b=["b_key"], required=["required_key"])
        defaults = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))
        self.assertEqual(defaults["openbao_seed_only_apps"], [])
        self.assertIs(defaults["openbao_seed_absent_only"], False)
        selected = _seed_selection(
            apps,
            named=defaults["openbao_seed_only_apps"],
            absent_only=defaults["openbao_seed_absent_only"],
            required_apps=["required"],
        )
        loop = _task_by_name(
            INIT_TASKS,
            "Generate + seed per-app service secrets in OpenBao (generate-if-absent)",
        )["loop"]
        expected = _render(
            "{{ openbao_seeded_generated_app_secrets | dict2items }}", selected
        )
        self.assertEqual(_render(loop, selected), expected)

        read_task = _prepare_task("Read generated app-secret field names from KV v2 subkeys")
        self.assertFalse(_render(read_task["when"], {"openbao_seed_absent_only": False}))

    def test_named_apps_include_only_the_named_and_required_apps(self):
        apps = _app_map(a=["a_key"], b=["b_key"], required=["required_key"])
        selected = _seed_selection(apps, named=["a"], required_apps=["required"])
        self.assertEqual(_loop_names(selected), ["a", "required"])

    def test_unknown_name_fails_the_assertion_and_appears_in_its_message(self):
        task = _task_by_name(INIT_TASKS, "Reject unknown generated app-secret seed names")
        variables = {
            "openbao_seed_only_apps": ["ghost-app"],
            "openbao_seeded_generated_app_secrets": _app_map(a=["a_key"]),
        }
        conditions = task["ansible.builtin.assert"]["that"]
        self.assertFalse(_render(conditions[0], variables))
        self.assertIn("ghost-app", _render(task["ansible.builtin.assert"]["fail_msg"], variables))

        names = [task.get("name") for task in _flatten_tasks(
            yaml.safe_load(INIT_TASKS.read_text(encoding="utf-8"))
        )]
        self.assertLess(
            names.index(task["name"]),
            names.index("Enable the declared KV v2 mounts and tune retention"),
        )

    def test_absent_only_selects_partial_and_missing_leaves_plus_required_apps(self):
        apps = _app_map(a=["a_one", "a_two"], b=["b_one", "b_two"],
                        c=["c_one"], required=["required_key"])
        selected = _seed_selection(
            apps,
            absent_only=True,
            present_by_app={"a": ["a_one", "a_two"], "b": ["b_one"], "c": None,
                            "required": ["required_key"]},
            required_apps=["required"],
        )
        self.assertEqual(selected["openbao_seed_apps_with_absent_fields"], ["b", "c"])
        self.assertEqual(_loop_names(selected), ["b", "c", "required"])

    def test_named_and_absent_filters_intersect_and_keep_required_apps(self):
        apps = _app_map(a=["a_key"], b=["b_key"], c=["c_key"], required=["required_key"])
        selected = _seed_selection(
            apps,
            named=["a", "b"],
            absent_only=True,
            present_by_app={"a": ["a_key"], "b": [], "c": [], "required": ["required_key"]},
            required_apps=["required"],
        )
        self.assertEqual(_loop_names(selected), ["b", "required"])

    def test_rotation_keeps_the_app_even_when_every_field_is_present(self):
        apps = _app_map(a=["a_key"], rotated=["rotate_key"], required=["required_key"])
        selected = _seed_selection(
            apps,
            named=["a"],
            absent_only=True,
            present_by_app={"a": ["a_key"], "rotated": ["rotate_key"],
                            "required": ["required_key"]},
            rotate_fields=["rotate_key"],
            required_apps=["required"],
        )
        self.assertEqual(_loop_names(selected), ["rotated", "required"])

    def test_read_pass_is_names_only_and_executes_in_check_mode(self):
        task = _prepare_task("Read generated app-secret field names from KV v2 subkeys")
        self.assertTrue(task["no_log"])
        self.assertIs(task["check_mode"], False)
        condition = task["when"]
        condition = " ".join(condition) if isinstance(condition, list) else condition
        self.assertNotIn("check_mode", condition)
        command = task["ansible.builtin.command"]["cmd"]
        self.assertIn("bao read -format=json", command)
        self.assertRegex(command, r"/subkeys/\{\{ openbao_seed_app_path \}\}")
        self.assertNotIn("/data/", command)

        summary = _task_by_name(INIT_TASKS, "Summarize generated app-secret seed selection")
        self.assertFalse(summary.get("no_log", False))

    def test_required_apps_match_all_literal_accumulator_consumers(self):
        defaults = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))
        required = set(defaults["openbao_seed_required_apps"])
        access = re.compile(
            rf"{ACCUMULATOR}\s*\[\s*['\"](?P<app>[^'\"]+)['\"]\s*\]"
        )
        consumers = []
        for path in (ROOT / "roles/openbao/tasks").rglob("*.yml"):
            parsed = yaml.safe_load(path.read_text(encoding="utf-8")) or []
            for task in _flatten_tasks(parsed):
                if task.get("name") == ACCUMULATOR_TASK:
                    continue
                direct_values = {
                    key: value for key, value in task.items()
                    if key not in {"block", "rescue", "always"}
                }
                for value in _yaml_strings(direct_values):
                    if ACCUMULATOR not in value:
                        continue
                    matches = list(access.finditer(value))
                    self.assertEqual(
                        value.count(ACCUMULATOR), len(matches),
                        f"unclassified accumulator use in {path}: {value}",
                    )
                    consumers.extend(match.group("app") for match in matches)
        self.assertEqual(set(consumers), required)


def _yaml_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from _yaml_strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _yaml_strings(nested)


if __name__ == "__main__":
    unittest.main()
