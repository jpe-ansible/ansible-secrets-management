"""Router-key declarations make the shared seed task repair invalid prefixes."""

from pathlib import Path
import unittest

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "roles/openbao/tasks/seed_generated_app_secret.yml"
DEFAULTS = yaml.safe_load(
    (ROOT / "roles/openbao/defaults/main/01b-app-secret-generation.yml").read_text()
)
FIELD_TASK = "Add a shared declaration for each generated app-secret field"


def _field_declaration(name):
    tasks = yaml.safe_load(SEED.read_text(encoding="utf-8"))
    task = next(task for task in tasks if task.get("name") == FIELD_TASK)
    expression = task["ansible.builtin.set_fact"]["openbao_seed_shared_fields"]
    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        **DEFAULTS,
        "openbao_seed_shared_fields": [],
        "item": name,
    }
    return templar.template(trust_as_template(expression))[0]


class RouterKeyPrefixRegeneration(unittest.TestCase):
    def test_explicit_contract_router_field_requires_prefix(self):
        field = _field_declaration("router_key")
        self.assertEqual(field["prefix"], "sk-")
        self.assertEqual(field["valid_pattern"], "^sk-")

    def test_second_explicit_contract_router_field_requires_prefix(self):
        field = _field_declaration("claude_ocg_router_key")
        self.assertEqual(field["prefix"], "sk-")
        self.assertEqual(field["valid_pattern"], "^sk-")

    def test_namespaced_router_field_requires_prefix(self):
        for name in (
            "open_webui_llm_router_key",
            "next_ai_drawio_llm_router_key",
            "langflow_llm_router_key",
            "grafana_llm_router_key",
            "openhands_llm_router_key",
        ):
            with self.subTest(field=name):
                field = _field_declaration(name)
                self.assertEqual(field["prefix"], "sk-")
                self.assertEqual(field["valid_pattern"], "^sk-")

    def test_ordinary_field_has_no_router_repair_pattern(self):
        field = _field_declaration("ordinary_password")
        self.assertEqual(field["prefix"], "")
        self.assertNotIn("valid_pattern", field)

    def test_hermes_profile_api_server_key_is_plain_alphanumeric(self):
        for name in ("hermes_eval_api_server_key", "hermes_youtrack_clerk_api_server_key"):
            with self.subTest(field=name):
                field = _field_declaration(name)
                self.assertEqual(field["prefix"], "")
                self.assertEqual(field["charset"], "alnum")
                self.assertEqual(field["length"], DEFAULTS["openbao_app_secret_length"])
                self.assertNotIn("valid_pattern", field)
                self.assertNotIn(name, DEFAULTS["openbao_app_secret_router_key_fields"])
                self.assertNotIn(name, DEFAULTS["openbao_app_secret_valid_patterns"])


class AppFormatPatternRegeneration(unittest.TestCase):
    def test_hatchet_admin_password_takes_its_app_pattern(self):
        field = _field_declaration("hatchet_admin_password")
        pattern = DEFAULTS["openbao_app_secret_valid_patterns"]["hatchet_admin_password"]
        self.assertEqual(field["valid_pattern"], pattern)
        self.assertEqual(field["charset"], "alnum")

    def test_hatchet_pattern_rejects_a_lowercase_only_value(self):
        import re

        pattern = DEFAULTS["openbao_app_secret_valid_patterns"]["hatchet_admin_password"]
        self.assertIsNone(re.match(pattern, "a1" * 24))
        self.assertIsNone(re.match(pattern, "Aa1" * 22))
        self.assertIsNotNone(re.match(pattern, "Aa1" * 13))

    def test_hatchet_cookie_secret_is_one_32_char_alnum_key(self):
        import re

        field = _field_declaration("hatchet_server_auth_cookie_secrets")
        self.assertEqual(field["length"], 32)
        self.assertEqual(field["charset"], "alnum")
        pattern = field["valid_pattern"]
        self.assertIsNotNone(re.match(pattern, "Ab3" * 10 + "Cd"))
        # The stored two-part hex value and a 40-char default both fail, so the seed regenerates them.
        self.assertIsNone(re.match(pattern, "a" * 64 + " " + "b" * 64))
        self.assertIsNone(re.match(pattern, "A1" * 20))

    def test_fields_without_a_length_override_keep_the_default(self):
        self.assertEqual(_field_declaration("ordinary_password")["length"], DEFAULTS["openbao_app_secret_length"])
        self.assertEqual(_field_declaration("secret_key")["length"], DEFAULTS["openbao_app_secret_key_length"])


if __name__ == "__main__":
    unittest.main()
