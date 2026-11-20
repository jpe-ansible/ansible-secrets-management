"""Per-App GitHub grants render only declared paths and request values."""

import json
import os
import re
from pathlib import Path

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "roles/openbao/templates/github-mount-config-policy.hcl.j2"
MOUNT_TASK = ROOT / "roles/openbao/tasks/init/05b-github-app-mount.yml"
CONFIG_WRITE_TASK = ROOT / "roles/openbao/tasks/init/github_app_config_write.yml"
PERMISSION_SET_TASK = "Reconcile the permission sets on mount {{ gm.mount }}"
APP_ENVIRONMENT = {
    "github-public": (
        "OPENBAO_GITHUB_EVERYDAY_APP_ID",
        "OPENBAO_GITHUB_EVERYDAY_APP_PRIVATE_KEY",
    ),
    "github-empty": (
        "OPENBAO_GITHUB_AGENTS_APP_ID",
        "OPENBAO_GITHUB_AGENTS_APP_PRIVATE_KEY",
    ),
    "github-sets": (
        "OPENBAO_GITHUB_HERMES_APP_ID",
        "OPENBAO_GITHUB_HERMES_APP_PRIVATE_KEY",
    ),
}


def _stanzas(policy):
    for match in re.finditer(r'(?m)^path "([^"]+)" \{', policy):
        start = match.end()
        depth = 1
        for offset, char in enumerate(policy[start:]):
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    yield match.group(1), policy[start : start + offset]
                    break


def _allowed_parameter_keys(body):
    match = re.search(r"(?ms)^  allowed_parameters\s*=\s*\{\n(.*?)^  \}", body)
    assert match, "stanza has no allowed_parameters block"
    return re.findall(r'(?m)^    "([^"]+)"\s*=', match.group(1))


def _render(values):
    templar = Templar(loader=DataLoader())
    templar.available_variables = values
    return templar.template(trust_as_template(TEMPLATE.read_text(encoding="utf-8")))


def _fixture_mounts():
    return [
        {
            "mount": "github-public",
            "app_id": "101",
            "private_key": "fixture-key",
            "permission_sets": [
                {
                    "name": "public-read",
                    "installation_id": "202",
                    "public_repos_of": "public-org",
                    "permissions": {"contents": "read"},
                },
                {
                    "name": "private-read",
                    "installation_id": "303",
                    "private_repos_of": "private-org",
                    "permissions": {"metadata": "read"},
                    "repositories": ["state"],
                },
            ],
        },
        {
            "mount": "github-empty",
            "app_id": "",
            "private_key": "",
            "permission_sets": [],
        },
        {
            "mount": "github-sets",
            "app_id": "103",
            "private_key": "",
            "permission_sets": [
                {
                    "name": "static-set",
                    "installation_id": "404",
                    "permissions": {"contents": "read"},
                    "repositories": ["state"],
                },
            ],
        },
    ]


def test_policy_renders_only_declared_mounts_and_constrained_paths():
    mounts = _fixture_mounts()
    rendered = _render({"ansible_managed": "Ansible managed", "openbao_github_app_mounts": mounts})
    stanzas = list(_stanzas(rendered))
    paths = [path for path, _body in stanzas]

    expected = {
        "sys/mounts/github-public",
        "sys/mounts/github-empty",
        "sys/mounts/github-sets",
        "github-public/config",
        "github-empty/config",
        "github-sets/config",
        "github-public/token",
        "github-public/permissionset/public-read",
        "github-public/permissionset/private-read",
        "github-sets/permissionset/static-set",
        "github-public/permissionset",
        "github-public/permissionset/*",
        "github-empty/permissionset",
        "github-empty/permissionset/*",
        "github-sets/permissionset",
        "github-sets/permissionset/*",
        "sys/leases/revoke",
    }
    assert set(paths) == expected
    assert len(paths) == len(expected)
    assert not any(path.startswith("sys/policies/acl/") for path in paths)
    assert not any(path.startswith("auth/") for path in paths)

    bodies = dict(stanzas)
    expected_capabilities = {
        "sys/mounts/github-public": ["update"],
        "sys/mounts/github-empty": ["update"],
        "sys/mounts/github-sets": ["update"],
        "github-public/config": ["create", "read", "update"],
        "github-empty/config": ["create", "read", "update"],
        "github-sets/config": ["create", "read", "update"],
        "github-public/token": ["create", "update"],
        "github-public/permissionset/public-read": ["create", "read", "update"],
        "github-public/permissionset/private-read": ["create", "read", "update"],
        "github-sets/permissionset/static-set": ["create", "read", "update"],
        "github-public/permissionset": ["list"],
        "github-public/permissionset/*": ["delete"],
        "github-empty/permissionset": ["list"],
        "github-empty/permissionset/*": ["delete"],
        "github-sets/permissionset": ["list"],
        "github-sets/permissionset/*": ["delete"],
        "sys/leases/revoke": ["update"],
    }
    for path, expected_caps in expected_capabilities.items():
        capabilities = re.search(r"capabilities\s*=\s*(\[[^]]*\])", bodies[path])
        assert capabilities, path
        assert json.loads(capabilities.group(1)) == expected_caps

    assert _allowed_parameter_keys(bodies["github-public/config"]) == [
        "app_id",
        "prv_key",
        "exclude_repository_metadata",
    ]
    assert '"app_id" = []' in bodies["github-public/config"]
    assert '"prv_key" = []' in bodies["github-public/config"]
    assert '"exclude_repository_metadata" = [true]' in bodies["github-public/config"]
    assert "required_parameters" not in bodies["github-public/config"]
    for mount in ("github-public", "github-empty", "github-sets"):
        assert '"app_id" = []' in bodies[f"{mount}/config"]
        assert '"prv_key" = []' in bodies[f"{mount}/config"]
        assert '"exclude_repository_metadata" = [true]' in bodies[f"{mount}/config"]

    token = bodies["github-public/token"]
    assert _allowed_parameter_keys(token) == ["org_name", "installation_id", "permissions"]
    assert '"org_name" = ["public-org"]' in token
    assert '"installation_id" = [\n      "303"\n    ]' in token
    assert '"permissions" = [{ "metadata" = "read" }]' in token
    assert '"repositories"' not in token
    assert '"repository_ids"' not in token

    assert "github-empty/token" not in paths
    assert "github-sets/token" not in paths

    public_set = bodies["github-public/permissionset/public-read"]
    assert _allowed_parameter_keys(public_set) == [
        "installation_id",
        "permissions",
        "repositories",
    ]
    assert "required_parameters" not in public_set
    assert '"installation_id" = ["202"]' in public_set
    assert '"permissions" = [{\n      "contents" = "read"\n    }]' in public_set
    assert '"repositories" = []' in public_set

    private_set = bodies["github-public/permissionset/private-read"]
    assert _allowed_parameter_keys(private_set) == [
        "installation_id",
        "permissions",
        "repositories",
    ]
    assert '"installation_id" = ["303"]' in private_set
    assert '"permissions" = [{\n      "metadata" = "read"\n    }]' in private_set
    assert '"repositories" = []' in private_set
    assert "required_parameters" not in private_set
    static_set = bodies["github-sets/permissionset/static-set"]
    assert '"installation_id" = ["404"]' in static_set
    assert '"repositories" = [["state"]]' in static_set

    leases = bodies["sys/leases/revoke"]
    assert _allowed_parameter_keys(leases) == ["lease_id"]
    assert '"lease_id" = ["github-public/token/*"]' in leases


def test_config_policy_text_is_independent_of_app_environment(monkeypatch):
    env_names = [name for pair in APP_ENVIRONMENT.values() for name in pair]

    def render_from_environment():
        mounts = _fixture_mounts()
        for mount in mounts:
            app_id_env, private_key_env = APP_ENVIRONMENT[mount["mount"]]
            mount["app_id"] = os.environ.get(app_id_env, "")
            mount["private_key"] = os.environ.get(private_key_env, "")
        return _render({"ansible_managed": "Ansible managed", "openbao_github_app_mounts": mounts})

    for name in env_names:
        monkeypatch.delenv(name, raising=False)
    unset = render_from_environment()

    for index, (app_id_env, private_key_env) in enumerate(APP_ENVIRONMENT.values(), start=1):
        monkeypatch.setenv(app_id_env, str(100 + index))
        monkeypatch.setenv(private_key_env, f"fixture-private-key-{index}")
    set_values = render_from_environment()

    for index, (app_id_env, private_key_env) in enumerate(APP_ENVIRONMENT.values(), start=1):
        monkeypatch.setenv(app_id_env, str(200 + index))
        monkeypatch.setenv(private_key_env, f"different-private-key-{index}")
    different_values = render_from_environment()

    assert unset == set_values == different_values
    assert all(secret not in unset for secret in ("fixture-private-key", "different-private-key"))


def test_permission_set_policy_matches_task_bodies_for_each_set_kind():
    mounts = _fixture_mounts()
    resolved_sets = {
        "public-read": {
            **mounts[0]["permission_sets"][0],
            "repositories": ["fixture-a", "fixture-b"],
        },
        "private-read": {
            **mounts[0]["permission_sets"][1],
            "repositories": ["fixture-a", "fixture-b"],
        },
        "static-set": mounts[2]["permission_sets"][0],
    }
    policy = _render({"ansible_managed": "Ansible managed", "openbao_github_app_mounts": mounts})
    stanzas = dict(_stanzas(policy))
    tasks = yaml.safe_load(MOUNT_TASK.read_text(encoding="utf-8"))
    task = next(item for item in tasks if item.get("name") == PERMISSION_SET_TASK)
    body_template = task["ansible.builtin.uri"]["body"]
    expected_bodies = {
        "public-read": {
            "installation_id": "202",
            "permissions": {"contents": "read"},
            "repositories": ["fixture-a", "fixture-b"],
        },
        "private-read": {
            "installation_id": "303",
            "permissions": {"metadata": "read"},
            "repositories": ["fixture-a", "fixture-b"],
        },
        "static-set": {
            "installation_id": "404",
            "permissions": {"contents": "read"},
            "repositories": ["state"],
        },
    }

    for name, resolved_set in resolved_sets.items():
        templar = Templar(loader=DataLoader())
        templar.available_variables = {"item": (resolved_set, {})}
        task_body = templar.template(trust_as_template(body_template))
        assert task_body == expected_bodies[name]
        path = (
            "github-public/permissionset/"
            + name
            if name != "static-set"
            else "github-sets/permissionset/static-set"
        )
        stanza = stanzas[path]
        assert '"repositories"' in stanza
        if name == "static-set":
            assert '"repositories" = [["state"]]' in stanza
        else:
            assert '"repositories" = []' in stanza


def test_mount_task_touches_only_declared_permission_set_names():
    tasks = yaml.safe_load(MOUNT_TASK.read_text(encoding="utf-8"))
    names = [task.get("name", "") for task in tasks]
    commands = "\n".join(
        task.get("ansible.builtin.command", {}).get("cmd", "")
        for task in tasks
    )

    assert any("List the permission sets" in name for name in names)
    assert any("Delete undeclared permission sets" in name for name in names)
    assert "bao list -format=json {{ gm.mount }}/permissionset" in commands
    assert "bao delete {{ gm.mount }}/permissionset/{{ item }}" in commands


def _flatten_tasks(tasks):
    for task in tasks:
        yield task
        for section in ("block", "rescue", "always"):
            yield from _flatten_tasks(task.get(section, []))


def test_mount_task_sends_numeric_github_ids_as_strings():
    tasks = list(_flatten_tasks(yaml.safe_load(MOUNT_TASK.read_text(encoding="utf-8"))))
    config = yaml.safe_load(CONFIG_WRITE_TASK.read_text(encoding="utf-8"))[0]
    private_token = next(
        task for task in tasks if "private-only on mount" in task.get("name", "")
    )
    permission_sets = next(
        task for task in tasks if task.get("name", "").startswith("Reconcile the permission sets")
    )

    assert config["ansible.builtin.uri"]["body"]["app_id"] == (
        "{{ openbao_github_app_config_app_id | int | string }}"
    )
    assert private_token["ansible.builtin.uri"]["body"]["installation_id"] == (
        "{{ item.installation_id | int | string }}"
    )
    assert "'installation_id': item.0.installation_id | int | string" in (
        permission_sets["ansible.builtin.uri"]["body"]
    )


def test_derive_read_mount_grants_only_its_pinned_mint_and_read_set():
    mount = {
        "mount": "github-derived",
        "app_id": "105",
        "private_key": "",
        "permission_sets": [],
        "derive_read": True,
        "installation_id": "505",
    }
    rendered = _render({"ansible_managed": "Ansible managed", "openbao_github_app_mounts": [mount]})
    bodies = dict(_stanzas(rendered))

    assert set(bodies) == {
        "sys/mounts/github-derived",
        "github-derived/config",
        "github-derived/token",
        "github-derived/permissionset/read",
        "github-derived/permissionset",
        "github-derived/permissionset/*",
        "sys/leases/revoke",
    }
    token = bodies["github-derived/token"]
    assert _allowed_parameter_keys(token) == ["installation_id"]
    assert '"installation_id" = ["505"]' in token
    assert 'required_parameters = ["installation_id"]' in token
    read_set = bodies["github-derived/permissionset/read"]
    assert _allowed_parameter_keys(read_set) == ["installation_id", "permissions"]
    assert '"installation_id" = ["505"]' in read_set
    assert '"lease_id" = ["github-derived/token/*"]' in bodies["sys/leases/revoke"]
