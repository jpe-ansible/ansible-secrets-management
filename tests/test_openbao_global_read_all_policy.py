"""Global read-all stays limited to KV and approved non-secret metadata."""

from pathlib import Path
import posixpath
import re

from jinja2 import Environment, FileSystemLoader, StrictUndefined
import yaml


ROOT = Path(__file__).resolve().parents[1]
OPENBAO = ROOT / "roles/openbao"
DEFAULTS = OPENBAO / "defaults/main"
TEMPLATES = OPENBAO / "templates"
ROLE_DEFAULTS = DEFAULTS / "07b-base-approles.yml"
POLICY_DEFAULTS = DEFAULTS / "07c-base-policies.yml"
ELEVATED_ROLE_DEFAULTS = DEFAULTS / "07f-elevated-approles.yml"
READ_LIST = {"read", "list"}
READ_ONLY = {"read"}
SYSTEM_METADATA_PATHS = {
    "sys/mounts",
    "sys/auth",
    "sys/policies/acl",
    "sys/policies/acl/*",
    "sys/internal/ui/mounts",
    "sys/internal/ui/mounts/*",
}
EXCLUDED_PATHS = [
    re.compile(r"^github(?:-[^/]*)?/"),
    re.compile(r"^(?:database|db|ssh(?:-[^/]*)?|pki)/"),
    re.compile(r"^identity/oidc/token(?:/|$)"),
    re.compile(r"^auth/[^/]+/role/[^/]+/secret-id(?:/|$)"),
    re.compile(r"^sys/raw(?:/|$)"),
    re.compile(r"^sys/audit(?:/|$)"),
]


def _defaults():
    values = {}
    for path in sorted(DEFAULTS.glob("*.yml")):
        values.update(yaml.safe_load(path.read_text(encoding="utf-8")) or {})
    return values


def _mount_entries():
    """The declared KV mounts with rendered paths and their flags.

    openbao_kv_mounts adds restricted mounts from the run environment, which
    is unset here, so the zone list is the whole list.
    """
    values = _defaults()
    renderer = Environment(undefined=StrictUndefined)
    return [
        dict(mount, path=renderer.from_string(str(mount["path"])).render(**values))
        for mount in values["openbao_kv_zone_mounts"]
    ]


def _mounts():
    return [mount["path"] for mount in _mount_entries()]


def _no_global_read_mounts():
    return {
        mount["path"] for mount in _mount_entries()
        if mount.get("global_read", True) is False
    }


def _task_dicts(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _task_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _task_dicts(child)


def _role_created_kv_mounts():
    values = _defaults()
    renderer = Environment(undefined=StrictUndefined)
    mounts = []
    for task_file in sorted((OPENBAO / "tasks").rglob("*.yml")):
        tasks = yaml.safe_load(task_file.read_text(encoding="utf-8")) or []
        for task in _task_dicts(tasks):
            command = task.get("ansible.builtin.command")
            if isinstance(command, dict):
                command = command.get("cmd", "")
            if not isinstance(command, str) or not re.search(
                r"\bbao\s+secrets\s+enable\b.*\bkv\s*$", command, re.DOTALL
            ):
                continue
            assert re.search(r"-version=2\b", command), task_file

            loop = task.get("loop")
            if loop:
                loop_match = re.fullmatch(r"\s*{{\s*(\w+)\s*}}\s*", loop)
                assert loop_match, (task_file, loop)
                loop_items = values[loop_match.group(1)]
                if loop_match.group(1) == "openbao_kv_mounts":
                    loop_items = values["openbao_kv_zone_mounts"]
                for item in loop_items:
                    path = item.get("path", item) if isinstance(item, dict) else item
                    mounts.append(
                        renderer.from_string(str(path)).render(**values)
                    )
                continue

            path_match = re.search(r"-path=\s*{{\s*([^}]+?)\s*}}", command)
            assert path_match, (task_file, command)
            expression = "{{ " + path_match.group(1) + " }}"
            mounts.append(renderer.from_string(expression).render(**values))

    assert mounts, "No KV v2 mount creation tasks were found in the OpenBao role"
    assert len(mounts) == len(set(mounts)), mounts
    return mounts


def _environment():
    environment = Environment(
        loader=FileSystemLoader([str(TEMPLATES), str(OPENBAO)]),
        undefined=StrictUndefined,
    )
    environment.filters["comment"] = lambda value: "# " + str(value)
    environment.filters["dirname"] = posixpath.dirname
    return environment


def _render(template):
    values = _defaults()
    environment = _environment()
    values["openbao_kv_mounts"] = _mount_entries()
    values["openbao_actuating_credential_leaves"] = [
        environment.from_string(str(leaf)).render(**values)
        for leaf in values["openbao_actuating_credential_leaves"]
    ]
    values["openbao_actuating_credential_dedicated_parents"] = [
        environment.from_string(str(parent)).render(**values)
        for parent in values["openbao_actuating_credential_dedicated_parents"]
    ]
    return environment.get_template(template).render(
        ansible_managed="managed",
        **values,
    )


def _actuating_credential_leaves(values):
    environment = _environment()
    return [
        environment.from_string(str(leaf)).render(**values)
        for leaf in values["openbao_actuating_credential_leaves"]
    ]


def _grants(policy):
    return {
        path: set(re.findall(r'"([^"]+)"', capabilities))
        for path, capabilities in re.findall(
            r'path "([^"]+)"\s*\{\s*capabilities\s*=\s*\[([^]]+)\]\s*\}',
            policy,
        )
    }


def _expected_global_read_grants():
    grants = {
        path: READ_LIST.copy()
        for path in SYSTEM_METADATA_PATHS
    }
    for mount in _global_read_kv_mounts():
        grants[f"{mount}/data/*"] = READ_ONLY.copy()
        grants[f"{mount}/metadata/*"] = READ_LIST.copy()
    return grants


def _global_read_kv_mounts():
    return [
        mount
        for mount in _role_created_kv_mounts()
        if not any(pattern.search(f"{mount}/data/*") for pattern in EXCLUDED_PATHS)
        and mount not in _no_global_read_mounts()
    ]


def test_both_global_read_policies_account_for_every_role_created_kv_mount():
    expected = _expected_global_read_grants()
    for template in ("ai-global-read-policy.hcl.j2", "operator-human-policy.hcl.j2"):
        grants = _grants(_render(template))
        assert {path: grants.get(path) for path in expected} == expected

    created = set(_role_created_kv_mounts())
    covered = set(_global_read_kv_mounts())
    excluded = created - covered
    assert covered | excluded == created
    assert covered.isdisjoint(excluded)
    assert all(
        any(pattern.search(f"{mount}/data/*") for pattern in EXCLUDED_PATHS)
        or mount in _no_global_read_mounts()
        for mount in excluded
    )
    assert _no_global_read_mounts() == {"ext-ai", "ext-critical", "admin"}
    assert {"int", "ext-saas", "ext-notify", "state"} <= covered


def test_actuating_credential_leaves_are_denied_only_for_ai_global_read():
    values = _defaults()
    leaves = _actuating_credential_leaves(values)
    environment = _environment()
    dedicated_parents = [
        environment.from_string(str(parent)).render(**values)
        for parent in values["openbao_actuating_credential_dedicated_parents"]
    ]
    ai_grants = _grants(_render("ai-global-read-policy.hcl.j2"))
    operator_grants = _grants(_render("operator-human-policy.hcl.j2"))

    assert leaves
    assert all("deny" not in capabilities for capabilities in operator_grants.values())
    for leaf in leaves:
        for kind in ("data", "metadata"):
            path = f"{values['openbao_kv_mount']}/{kind}/{leaf}"
            assert ai_grants[path] == {"deny"}
    for parent in {posixpath.dirname(leaf) for leaf in leaves}:
        path = f"{values['openbao_kv_mount']}/metadata/{parent}/"
        if parent in dedicated_parents:
            assert ai_grants[path] == {"deny"}
        else:
            assert ai_grants.get(path) != {"deny"}
    assert "apps" not in dedicated_parents
    assert ai_grants.get(f"{values['openbao_kv_mount']}/metadata/apps/") != {"deny"}


def test_workstation_ssh_key_paths_are_denied_only_for_ai_global_read():
    mount = "int"
    paths = (
        f"{mount}/data/ssh/*",
        f"{mount}/metadata/ssh/*",
        f"{mount}/metadata/ssh/",
    )
    ai_grants = _grants(_render("ai-global-read-policy.hcl.j2"))
    operator_grants = _grants(_render("operator-human-policy.hcl.j2"))

    assert mount in _mounts()
    assert all(ai_grants[path] == {"deny"} for path in paths)
    assert all(path not in operator_grants for path in paths)


def test_shared_read_all_block_has_only_read_and_list():
    grants = _grants(_render("templates/global-read-all-policy-block.j2"))
    assert grants == _expected_global_read_grants()
    assert all(capabilities in (READ_ONLY, READ_LIST) for capabilities in grants.values())
    assert not any(
        capabilities.intersection({"create", "update", "delete", "patch", "sudo"})
        for capabilities in grants.values()
    )


def test_read_all_policies_exclude_credential_mint_and_sensitive_system_paths():
    for template in ("ai-global-read-policy.hcl.j2", "operator-human-policy.hcl.j2"):
        for path in _grants(_render(template)):
            assert not any(pattern.search(path) for pattern in EXCLUDED_PATHS), path


def test_only_trusted_ai_roles_attach_global_read_and_elevation_split_is_unchanged():
    values = _defaults()
    roles = yaml.safe_load(ROLE_DEFAULTS.read_text(encoding="utf-8"))[
        "openbao_base_approles_core"
    ]
    by_name = {role["name"]: role for role in roles}
    trusted_readonly = by_name['{{ openbao_ai_readonly_approle_name }}']
    trusted_elevated = by_name['{{ openbao_ai_elevated_approle_name }}']
    untrusted_ai = by_name['{{ openbao_ai_public_approle_name }}']

    assert values["openbao_ai_global_read_policy_name"] == "ai-global-read"
    assert "openbao_ai_global_read_policy_name" in values[
        "openbao_ai_trusted_read_all_policies"
    ]
    assert trusted_readonly["token_policies"] == (
        "{{ openbao_ai_trusted_read_all_policies }}"
    )
    assert "openbao_ai_trusted_read_all_policies" in trusted_elevated[
        "token_policies"
    ]
    assert untrusted_ai["policy"] == "{{ openbao_ai_public_policy_name }}"
    assert "openbao_ai_global_read_policy_name" not in str(untrusted_ai)

    operator_workstation = next(
        row
        for row in yaml.safe_load(ELEVATED_ROLE_DEFAULTS.read_text(encoding="utf-8"))[
            "openbao_base_approles_elevated"
        ]
        if row["name"] == "operator-workstation"
    )
    assert "openbao_read_all_policies" in operator_workstation["token_policies"]
    assert "openbao_ai_trusted_read_all_policies" not in operator_workstation[
        "token_policies"
    ]

    elevation = {row["name"]: row["policy"] for row in values["openbao_elevate_roles"]}
    assert elevation == {
        "elevate-trusted": "{{ openbao_human_unlock_policy_name }}",
        "elevate-untrusted": "{{ openbao_human_unlock_untrusted_policy_name }}",
        "elevate-policy-sync": "{{ openbao_policy_sync_unlock_policy_name }}",
    }

    policies = yaml.safe_load(POLICY_DEFAULTS.read_text(encoding="utf-8"))[
        "openbao_base_policies_static"
    ]
    assert {
        "name": "{{ openbao_ai_global_read_policy_name }}",
        "template": "ai-global-read-policy.hcl.j2",
    } in policies


def test_authelia_signing_leaf_is_denied_to_ai_global_read():
    """The key that signs elevation tokens is never in the ambient AI read tier."""
    values = _defaults()
    leaves = _actuating_credential_leaves(values)
    leaf = values["openbao_authelia_service_secrets_kv_path"]
    assert leaf in leaves
    ai_grants = _grants(_render("ai-global-read-policy.hcl.j2"))
    for kind in ("data", "metadata"):
        assert ai_grants[f"{values['openbao_kv_mount']}/{kind}/{leaf}"] == {"deny"}


def test_authelia_signing_leaf_matches_the_authelia_role():
    """Both roles name the same leaf, so the deny always covers what the seed writes."""
    authelia = yaml.safe_load(
        (ROOT / "roles" / "authelia" / "defaults" / "main" / "00-core.yml").read_text(encoding="utf-8")
    )
    assert _defaults()["openbao_authelia_service_secrets_kv_path"] == authelia["authelia_service_secrets_kv_path"]
