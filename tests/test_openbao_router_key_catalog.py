"""The router-key catalog drives both generated secrets and their read paths."""

from pathlib import Path
import re

import jinja2
import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main/01c-app-secrets-generated.yml"
PATH_DEFAULTS = ROOT / "roles/openbao/defaults/main/01d-app-secret-paths.yml"
PROMOTED_DEFAULTS = ROOT / "roles/openbao/defaults/main/01b-app-secrets.yml"
OPENBAO_META = ROOT / "roles/openbao/meta/main.yml"
SECRET_GENERATION_DEFAULTS = ROOT / "roles/openbao/defaults/main/01b-app-secret-generation.yml"
SECRET_GENERATION_TASK = ROOT / "roles/openbao/tasks/seed_generated_app_secret.yml"
READ_DEFAULTS = ROOT / "roles/openbao/defaults/main/05c-terrakube-and-remaining-domain-names.yml"
EXCLUDED_DEFAULTS = ROOT / "roles/openbao/defaults/main/05h-cribl-edge-readers.yml"
GENERATION = ROOT / "roles/openbao/tasks/init/03-kv-mounts-and-seed-secrets.yml"
ROSTER_DEFAULTS = ROOT / "roles/openbao/defaults/main/05k-roster-agents.yml"
OPEN_LLM_POLICY = ROOT / "roles/openbao/templates/open-llm-policy.hcl.j2"
GITHUB_MOUNT_DEFAULTS = ROOT / "roles/openbao/defaults/main/03b-github-app-mounts.yml"
APPS_POLICY = ROOT / "roles/openbao/templates/apps-policy.hcl.j2"

DEFAULTS_DATA = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8"))
PATH_DEFAULTS_DATA = yaml.safe_load(PATH_DEFAULTS.read_text(encoding="utf-8"))
PROMOTED_DATA = yaml.safe_load(PROMOTED_DEFAULTS.read_text(encoding="utf-8"))
READ_DATA = yaml.safe_load(READ_DEFAULTS.read_text(encoding="utf-8"))
EXCLUDED_DATA = yaml.safe_load(EXCLUDED_DEFAULTS.read_text(encoding="utf-8"))
OPENBAO_META_DATA = yaml.safe_load(OPENBAO_META.read_text(encoding="utf-8"))
ROSTER_DATA = yaml.safe_load(ROSTER_DEFAULTS.read_text(encoding="utf-8"))
RAW_MINT_PERMISSIONS = yaml.safe_load(GITHUB_MOUNT_DEFAULTS.read_text(encoding="utf-8"))[
    "openbao_github_agents_raw_mint_permissions"
]


def _render(value, variables):
    templar = Templar(loader=DataLoader())
    templar.available_variables = variables
    return templar.template(trust_as_template(value))


def _seed_loop_variables(seeded):
    # The seed loop reads its list through a default that is the unfiltered declaration.
    default = yaml.safe_load(
        (DEFAULTS.parent / "01b-app-secret-generation.yml").read_text(encoding="utf-8")
    )["openbao_seed_apps_to_seed"]
    return {
        "openbao_seeded_generated_app_secrets": seeded,
        "openbao_seed_apps_to_seed": trust_as_template(default),
    }


def _read_apps(router_catalog, promoted_app_secrets=None):
    return _render(
        READ_DATA["openbao_apps_read_apps"],
        {
            "openbao_generated_app_secrets": DEFAULTS_DATA["openbao_generated_app_secrets"],
            "openbao_generated_app_secret_paths": PATH_DEFAULTS_DATA["openbao_generated_app_secret_paths"],
            "openbao_promoted_app_secrets": promoted_app_secrets or {},
            "openbao_router_key_catalog": router_catalog,
            "openbao_apps_read_published_apps": READ_DATA["openbao_apps_read_published_apps"],
            "openbao_apps_read_excluded_generated_apps": EXCLUDED_DATA[
                "openbao_apps_read_excluded_generated_apps"
            ],
        },
    )


def _find_task(tasks, name):
    for task in tasks:
        if not isinstance(task, dict):
            continue
        if task.get("name") == name:
            return task
        for section in ("block", "rescue", "always"):
            if section in task:
                found = _find_task(task[section], name)
                if found is not None:
                    return found
    raise AssertionError(f"task {name!r} not found")


def _generation_loop():
    tasks = yaml.safe_load(GENERATION.read_text(encoding="utf-8"))
    task = _find_task(
        tasks,
        "Generate + seed per-app service secrets in OpenBao (generate-if-absent)",
    )
    return task["loop"]


def _render_apps_policy(router_catalog):
    environment = jinja2.Environment()
    environment.filters["comment"] = str
    return environment.from_string(APPS_POLICY.read_text(encoding="utf-8")).render(
        ansible_managed="",
        openbao_kv_mount="secret",
        openbao_apps_read_apps=_read_apps(router_catalog),
    )


def _render_open_llm_policy(installation_id):
    environment = jinja2.Environment()
    environment.filters["comment"] = str
    return environment.from_string(OPEN_LLM_POLICY.read_text(encoding="utf-8")).render(
        ansible_managed="",
        openbao_kv_mount="secret",
        openbao_github_agents_mount="github",
        openbao_github_agents_installation_id=installation_id,
        openbao_github_agents_raw_mint_permissions=RAW_MINT_PERMISSIONS,
        openbao_sandbox_agent_read_approle_name="sandbox-agent-read",
        openbao_sandbox_agent_write_approle_name="sandbox-agent-write",
        openbao_sandbox_zcode_read_approle_name="sandbox-zcode-read",
        openbao_sandbox_zcode_write_approle_name="sandbox-zcode-write",
        openbao_sandbox_opencode_read_approle_name="sandbox-opencode-read",
        openbao_sandbox_opencode_write_approle_name="sandbox-opencode-write",
        openbao_sandbox_cursor_read_approle_name="sandbox-cursor-read",
        openbao_sandbox_cursor_write_approle_name="sandbox-cursor-write",
    )


def test_public_router_key_entries_remain_literal_and_allowlisted():
    assert DEFAULTS_DATA["openbao_router_key_catalog"] == (
        "{{ llm_router_key_catalog_facts.openbao_router_key_catalog }}"
    )
    assert {"role": "dryvist.homelab.llm_router_key_catalog", "tags": ["always"]} in (
        OPENBAO_META_DATA["dependencies"]
    )
    generated = DEFAULTS_DATA["openbao_generated_app_secrets"]
    assert generated["agy"] == ["agy_llm_router_key"]
    assert generated["hermes-private"] == ["hermes_private_llm_router_key"]
    assert generated["donna"] == ["donna_llm_router_key", "donna_a2a_token"]
    assert generated["zcode"] == ["zcode_llm_router_key"]
    assert generated["qwen-code"] == ["qwen_code_llm_router_key"]
    assert generated["opencode"] == ["opencode_llm_router_key"]
    assert generated["codex"] == ["codex_llm_router_key"]
    assert {"agy", "hermes-private", "donna", "zcode", "qwen-code", "opencode"}.issubset(
        _read_apps({})
    )
    policy = _render_apps_policy({})
    assert 'path "secret/data/apps/donna"' in policy
    assert 'path "secret/metadata/apps/donna"' in policy


def test_claude_code_launcher_keys_use_the_existing_router_key_reader_paths():
    fields = [
        "claude_code_llm_router_key",
        "claude_llm_router_key",
        "claude_ocg_router_key",
        "claude_homelab_llm_router_key",
        "claude_mac_local_key",
    ]
    assert DEFAULTS_DATA["openbao_generated_app_secrets"]["claude-code"] == fields
    assert "claude-code" in _read_apps({})

    policy = _render_apps_policy({})
    assert 'path "secret/data/apps/claude-code"' in policy
    assert 'path "secret/metadata/apps/claude-code"' in policy
    assert 'path "secret/data/apps/*"' not in policy
    assert 'path "secret/metadata/apps/*"' not in policy


def test_claude_launcher_key_fields_use_the_shared_router_key_format():
    defaults = yaml.safe_load(SECRET_GENERATION_DEFAULTS.read_text(encoding="utf-8"))
    tasks = yaml.safe_load(SECRET_GENERATION_TASK.read_text(encoding="utf-8"))
    field_task = _find_task(tasks, "Add a shared declaration for each generated app-secret field")
    expression = field_task["ansible.builtin.set_fact"]["openbao_seed_shared_fields"]
    variables = {
        **defaults,
        "openbao_seed_shared_fields": [],
    }

    for field in ("claude_homelab_llm_router_key", "claude_mac_local_key"):
        declaration = _render(expression, {**variables, "item": field})[0]
        assert declaration == {
            "name": field,
            "length": defaults["openbao_app_secret_length"],
            "charset": "alnum",
            "prefix": defaults["openbao_app_secret_router_key_prefix"],
            "valid_pattern": "^sk-",
        }


def test_glance_tile_key_is_generated_and_readable_by_the_apps_reader():
    generated = DEFAULTS_DATA["openbao_generated_app_secrets"]
    assert generated["glance"] == ["glance_llm_router_key"]
    assert "glance" in _read_apps({})
    assert 'path "secret/data/apps/glance"' in _render_apps_policy({})


def test_pepper_router_key_is_in_the_reconcile_seed_set():
    seeded = _render(
        ROSTER_DATA["openbao_seeded_generated_app_secrets"],
        {
            "openbao_generated_app_secrets": DEFAULTS_DATA["openbao_generated_app_secrets"],
            "openbao_router_key_catalog": {},
        },
    )
    generated = _render(_generation_loop(), _seed_loop_variables(seeded))
    assert [entry for entry in generated if entry["key"] == "pepper"] == [
        {"key": "pepper", "value": ["pepper_llm_router_key"]}
    ]
    assert "pepper" in _read_apps({})
    assert 'path "secret/data/apps/pepper"' in _render_apps_policy({})
    assert _render(
        PATH_DEFAULTS_DATA["openbao_seed_app_path"],
        {
            "openbao_generated_app_secret_paths": PATH_DEFAULTS_DATA["openbao_generated_app_secret_paths"],
            "openbao_seed_app": "pepper",
        },
    ) == "apps/pepper"


def test_langflow_router_key_is_generated_and_readable_by_the_apps_reader():
    generated = DEFAULTS_DATA["openbao_generated_app_secrets"]
    assert generated["langflow"] == ["langflow_llm_router_key"]
    assert "langflow" in _read_apps({})
    assert 'path "secret/data/apps/langflow"' in _render_apps_policy({})


def test_sandbox_agent_router_key_is_generated_and_readable_by_the_apps_reader():
    generated = DEFAULTS_DATA["openbao_generated_app_secrets"]
    excluded = EXCLUDED_DATA["openbao_apps_read_excluded_generated_apps"]
    assert generated["sandbox-agent-router"] == [
        "sandbox_agent_router_llm_router_key",
        "sandbox_agent_local_router_llm_router_key",
    ]
    assert "sandbox-agent" not in generated
    assert "sandbox-agent-router" not in excluded
    assert "sandbox-agent-router" in _read_apps({})


def test_openhands_fields_are_generated_and_readable_by_the_apps_reader():
    generated = DEFAULTS_DATA["openbao_generated_app_secrets"]
    assert generated["openhands"] == [
        "openhands_llm_router_key",
        "openhands_backend_api_key",
        "openhands_secret_key",
        "openhands_webhook_secret",
    ]
    assert "openhands" in _read_apps({})
    assert 'path "secret/data/apps/openhands"' in _render_apps_policy({})
    assert 'path "secret/metadata/apps/openhands"' in _render_apps_policy({})


def test_lane_walk_probe_key_is_generated_and_readable_by_the_apps_reader():
    generated = DEFAULTS_DATA["openbao_generated_app_secrets"]
    assert generated["lane-walk-probe"] == ["lane_walk_probe_llm_router_key"]
    assert "lane-walk-probe" in _read_apps({})
    assert 'path "secret/data/apps/lane-walk-probe"' in _render_apps_policy({})


def test_sandbox_agent_promotion_is_readable_by_the_apps_reader():
    assert "sandbox-agent" not in _read_apps({})
    promoted_apps = PROMOTED_DATA["openbao_promoted_app_secrets"]
    assert "sandbox-agent" in _read_apps({}, promoted_apps)
    assert "ci-resolver" not in _read_apps({}, promoted_apps)


def test_router_catalog_entries_feed_generation_and_the_apps_read_paths():
    catalog = {"contract-fixture": ["contract_fixture_llm_router_key"]}
    seeded = _render(
        ROSTER_DATA["openbao_seeded_generated_app_secrets"],
        {
            "openbao_generated_app_secrets": DEFAULTS_DATA["openbao_generated_app_secrets"],
            "openbao_router_key_catalog": catalog,
        },
    )
    generated = _render(_generation_loop(), _seed_loop_variables(seeded))
    assert {entry["key"]: entry["value"] for entry in generated}["contract-fixture"] == catalog[
        "contract-fixture"
    ]
    assert set(_read_apps(catalog)) - set(_read_apps({})) == set(catalog)

    policy = _render_apps_policy(catalog)
    assert 'path "secret/data/apps/contract-fixture"' in policy
    assert 'path "secret/metadata/apps/contract-fixture"' in policy
    assert 'path "secret/data/apps/*"' not in policy
    assert 'path "secret/metadata/apps/*"' not in policy


def test_hermes_eval_api_server_key_stays_outside_the_router_catalog():
    api_server_key = "hermes_eval_api_server_key"
    generated = DEFAULTS_DATA["openbao_generated_app_secrets"]
    catalog = {"contract-fixture": ["contract_fixture_llm_router_key"]}
    seeded = _render(
        ROSTER_DATA["openbao_seeded_generated_app_secrets"],
        {
            "openbao_generated_app_secrets": generated,
            "openbao_router_key_catalog": catalog,
        },
    )

    assert generated["hermes-eval"] == ["hermes_eval_llm_router_key", api_server_key]
    assert "hermes-eval" not in catalog
    assert all(api_server_key not in fields for fields in catalog.values())
    assert seeded["hermes-eval"] == generated["hermes-eval"]


def test_open_llm_fields_mirror_the_generated_router_fields():
    tasks = yaml.safe_load(GENERATION.read_text(encoding="utf-8"))
    capture = _find_task(tasks, "Capture generated router keys for the open-llm merge")
    assert capture["no_log"] is True
    assert capture["ansible.builtin.set_fact"] == {
        "openbao_zcode_router_key_source": (
            "{{ openbao_seeded_app_secret_values['zcode']['zcode_llm_router_key'] }}"
        ),
        "openbao_opencode_router_key_source": (
            "{{ openbao_seeded_app_secret_values['opencode']['opencode_llm_router_key'] }}"
        ),
        "openbao_opencode_local_router_key_source": (
            "{{ openbao_seeded_app_secret_values['sandbox-agent-router']"
            "['sandbox_agent_local_router_llm_router_key'] }}"
        ),
        "openbao_qwen_code_router_key_source": (
            "{{ openbao_seeded_app_secret_values['qwen-code']['qwen_code_llm_router_key'] }}"
        ),
    }
    merge = _find_task(tasks, "Merge generated router keys into open-llm")
    assert merge["vars"]["openbao_promote_fields"] == {
        "ZCODE_ROUTER_KEY": "openbao_zcode_router_key_source",
        "OPENCODE_ROUTER_KEY": "openbao_opencode_router_key_source",
        "OPENCODE_LOCAL_ROUTER_KEY": "openbao_opencode_local_router_key_source",
        "QWEN_CODE_ROUTER_KEY": "openbao_qwen_code_router_key_source",
    }


def test_open_llm_policy_reads_only_its_own_bucket():
    rendered = _render_open_llm_policy("")
    app_paths = [
        path
        for path in re.findall(r'^path "([^"]+)"', rendered, re.MULTILINE)
        if re.match(r"secret/(?:data|metadata)/apps/", path)
    ]
    assert sorted(app_paths) == [
        "secret/data/apps/open-llm",
        "secret/metadata/apps/open-llm",
    ]


def test_open_llm_policy_mints_raw_and_named_agents_tokens():
    rendered = _render_open_llm_policy("4242")
    paths = re.findall(r'^path "([^"]+)"', rendered, re.MULTILINE)
    assert paths == [
        "secret/data/apps/open-llm",
        "secret/metadata/apps/open-llm",
        "secrets-external/data/ai/saas/zai",
        "github/token",
        "github/token/public-write",
        "auth/approle/role/sandbox-agent-read/role-id",
        "auth/approle/role/sandbox-agent-read/secret-id",
        "auth/approle/role/sandbox-agent-write/role-id",
        "auth/approle/role/sandbox-agent-write/secret-id",
        "auth/approle/role/sandbox-zcode-read/role-id",
        "auth/approle/role/sandbox-zcode-read/secret-id",
        "auth/approle/role/sandbox-zcode-write/role-id",
        "auth/approle/role/sandbox-zcode-write/secret-id",
        "auth/approle/role/sandbox-opencode-read/role-id",
        "auth/approle/role/sandbox-opencode-read/secret-id",
        "auth/approle/role/sandbox-opencode-write/role-id",
        "auth/approle/role/sandbox-opencode-write/secret-id",
        "auth/approle/role/sandbox-cursor-read/role-id",
        "auth/approle/role/sandbox-cursor-read/secret-id",
        "auth/approle/role/sandbox-cursor-write/role-id",
        "auth/approle/role/sandbox-cursor-write/secret-id",
    ]

    raw_token = re.search(r'(?ms)^path "github/token" \{\n(.*?)^\}', rendered)
    assert raw_token is not None
    assert 'capabilities = ["create", "update"]' in raw_token.group(1)
    allowed_parameters = re.search(
        r"(?ms)^  allowed_parameters = \{\n(.*?)^  \}", raw_token.group(1)
    )
    denied_parameters = re.search(
        r"(?ms)^  denied_parameters = \{\n(.*?)^  \}", raw_token.group(1)
    )
    assert allowed_parameters is not None
    assert denied_parameters is not None
    assert (
        'required_parameters = ["repositories", "permissions"]'
        in raw_token.group(1)
    )
    assert re.findall(r'(?m)^    "([^"]+)" =', allowed_parameters.group(1)) == [
        "org_name",
        "repositories",
        "permissions",
    ]
    assert '"org_name" = []' in allowed_parameters.group(1)
    assert '"repositories" = []' in allowed_parameters.group(1)
    assert re.findall(r'(?m)^    "([^"]+)" =', denied_parameters.group(1)) == [
        "installation_id",
        "repository_ids",
    ]
    assert '"installation_id" = []' in denied_parameters.group(1)
    assert '"repository_ids" = []' in denied_parameters.group(1)
    assert (
        '"permissions" = [{ "contents" = "write", "pull_requests" = "write" }, '
        '{ "contents" = "read" }]'
    ) in raw_token.group(1)

    public_write = re.search(
        r'(?ms)^path "github/token/public-write" \{\n(.*?)^\}', rendered
    )
    assert public_write is not None
    assert 'capabilities = ["create", "update"]' in public_write.group(1)
