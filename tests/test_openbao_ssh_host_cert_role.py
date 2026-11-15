"""The SSH host-certificate signing role, under the same CA as the user roles.

`openbao_ssh_roles` (05-ssh-ca-engine.yml) carries a `host-cert` entry that
must render a HOST-only role body in the reconcile task
(roles/openbao/tasks/init/07-ssh-ca-engine.yml): `allow_host_certificates`,
`allowed_domains`, `allow_subdomains`, `allow_bare_domains`, `ttl`, `max_ttl`
-- and never `allow_user_certificates`, since a role that can sign both
would let anything holding the sign endpoint mint a host cert for one of
`allowed_users` too.

These render the REAL body expression out of the task file, never a
reimplementation of the branch -- see test_openbao_terrakube_api_update_guard.py
for why that matters (retyping a template performs its own escaping and can
pass while the real expression fails).
"""

from pathlib import Path

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar, trust_as_template

ROOT = Path(__file__).resolve().parents[1]
TASK_REL = "roles/openbao/tasks/init/07-ssh-ca-engine.yml"
TASK_NAME = "Reconcile the SSH roles"
DEFAULTS = ROOT / "roles/openbao/defaults/main"


def _read_defaults(filename: str) -> dict:
    return yaml.safe_load((DEFAULTS / filename).read_text(encoding="utf-8"))


def _task():
    for task in yaml.safe_load((ROOT / TASK_REL).read_text(encoding="utf-8")):
        if task.get("name") == TASK_NAME:
            return task
    raise AssertionError(f"task {TASK_NAME!r} not found in {TASK_REL}")


def _render_body(role_entry, source_cidrs=""):
    """Render the task's own `ssh_role_body` expression for one openbao_ssh_roles entry.

    `item` is the (role_entry, check_result) tuple the real `loop: ... | zip(...)`
    produces; the check result is never read by the body, so an empty dict
    stands in for it.
    """
    task = _task()
    body_expr = task["vars"]["ssh_role_body"]
    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        "item": (role_entry, {}),
        "openbao_ssh_source_address_cidrs": source_cidrs,
    }
    return templar.template(trust_as_template(body_expr))


LIVE_SSH_ROLES = _read_defaults("05-ssh-ca-engine.yml")["openbao_ssh_roles"]


def _live_entry(name):
    for entry in LIVE_SSH_ROLES:
        if entry["name"] == name:
            return entry
    raise AssertionError(f"{name!r} not in the live openbao_ssh_roles list")


def test_live_host_cert_entry_has_no_user_cert_fields():
    entry = _live_entry("host-cert")
    assert entry["cert_type"] == "host"
    assert entry["allow_host_certificates"] is True
    assert entry["allow_subdomains"] is True
    assert entry["allow_bare_domains"] is False
    assert entry["ttl"] == 7776000
    assert entry["max_ttl"] == 7776000
    assert "principal" not in entry
    assert "extensions" not in entry


def test_host_role_body_is_host_only():
    body = _render_body(
        {
            "name": "host-cert",
            "cert_type": "host",
            "allow_host_certificates": True,
            "allowed_domains": "example.com",
            "allow_subdomains": True,
            "allow_bare_domains": False,
            "ttl": 7776000,
            "max_ttl": 7776000,
        }
    )

    assert body["allow_host_certificates"] is True
    assert body["allowed_domains"] == "example.com"
    assert body["allow_subdomains"] is True
    assert body["allow_bare_domains"] is False
    assert body["ttl"] == 7776000
    assert body["max_ttl"] == 7776000

    # The one thing that must never happen: a role that can sign both shapes.
    assert "allow_user_certificates" not in body
    assert "allowed_users" not in body
    assert "default_user" not in body


def test_user_role_body_is_unchanged():
    # Same shape the pre-existing roles rendered before this change: no
    # cert_type field at all, defaulting to 'user' in the task.
    body = _render_body(
        {
            "name": "automation-ansible",
            "principal": "ansible",
            "ttl": 7200,
            "extensions": {},
        }
    )

    assert body["allow_user_certificates"] is True
    assert body["allowed_users"] == "ansible"
    assert body["default_user"] == "ansible"
    assert body["ttl"] == 7200
    assert body["max_ttl"] == 7200
    assert "allow_host_certificates" not in body
    assert "allowed_domains" not in body


def test_explicit_user_cert_type_renders_the_same_as_the_default():
    implicit = _render_body({"name": "x", "principal": "p", "ttl": 60, "extensions": {}})
    explicit = _render_body(
        {"name": "x", "cert_type": "user", "principal": "p", "ttl": 60, "extensions": {}}
    )
    assert implicit == explicit


def test_source_address_restriction_still_applies_to_user_roles():
    body = _render_body(
        {"name": "automation-ansible", "principal": "ansible", "ttl": 7200, "extensions": {}},
        source_cidrs="192.0.2.0/24",
    )
    assert body["default_critical_options"] == {"source-address": "192.0.2.0/24"}


def _render_user_roles(ssh_roles):
    """Render 07a's real two-step openbao_ssh_user_roles derivation, in the
    same dependency order Ansible resolves it in (openbao_ssh_host_role_names
    first, then openbao_ssh_user_roles reads it)."""
    derived = _read_defaults("07a-derived-rollups-and-ttls.yml")
    templar = Templar(loader=DataLoader())
    templar.available_variables = {"openbao_ssh_roles": ssh_roles}
    host_names = templar.template(
        trust_as_template(derived["openbao_ssh_host_role_names"])
    )
    templar.available_variables = {
        "openbao_ssh_roles": ssh_roles,
        "openbao_ssh_host_role_names": host_names,
    }
    return templar.template(trust_as_template(derived["openbao_ssh_user_roles"]))


def test_ssh_user_roles_view_excludes_host_cert():
    """openbao_ssh_user_roles (07a) is what every user-cert-only consumer --
    molecule/openbao/verify/ssh_signing.yml's items2dict among them -- must
    read instead of the full table. Render it for real against the LIVE
    table (which includes host-cert) and prove the crash molecule hit is
    gone: items2dict over the filtered view must not raise, and it must
    contain exactly the principal-bearing roles."""
    user_roles = _render_user_roles(LIVE_SSH_ROLES)

    names = {entry["name"] for entry in user_roles}
    assert "host-cert" not in names
    assert names == {
        "automation-ai",
        "automation-ai-diag",
        "automation-ansible",
        "automation-semaphore",
        "ci-runner",
    }

    # The exact operation that crashed in CI (PR #2203, run 36232738114):
    # items2dict(key_name='name', value_name='principal') over a table that
    # includes a principal-less entry.
    by_name = {entry["name"]: entry["principal"] for entry in user_roles}
    assert by_name["automation-ai"] == "ai-agent"
    assert by_name["automation-ai-diag"] == "ai-diag"


def test_exec_only_roles_share_one_body_and_diag_is_short_lived_and_ptyless():
    """The exec-channel-only roles are one anchored body with per-role
    overrides, so a new one cannot drift in extensions; the trusted-AI
    diagnostic role is the shortest-lived cert and never gets a pty."""
    by_name = {r["name"]: r for r in LIVE_SSH_ROLES}
    for name in ("automation-ansible", "automation-semaphore", "ci-runner", "automation-ai-diag"):
        assert by_name[name]["extensions"] == {}, name
    diag = by_name["automation-ai-diag"]
    assert diag["ttl"] == 900
    # keygen only issues a discarded certificate and grants no login.
    assert diag["ttl"] == min(
        r["ttl"] for r in LIVE_SSH_ROLES if "principal" in r and r["name"] != "keygen"
    )
    assert diag["principal"] not in {"ansible", "semaphore", "ai-agent", "root", "*"}


def test_ssh_user_roles_view_keeps_a_future_explicit_user_cert_type():
    # The filter must not accidentally drop an entry that later spells 'user'
    # out explicitly, nor crash on one that omits cert_type entirely.
    roles = [
        {"name": "explicit-user", "cert_type": "user", "principal": "p"},
        {"name": "implicit-user", "principal": "q"},
        {"name": "host-cert", "cert_type": "host"},
    ]
    names = {e["name"] for e in _render_user_roles(roles)}
    assert names == {"explicit-user", "implicit-user"}


def _render_sign_policies(ssh_roles, engine_enabled=True):
    """Render 07a's real openbao_ssh_sign_policies expression, resolving the
    same dependency chain Ansible would: host_role_names -> user_roles ->
    sign_policies."""
    derived = _read_defaults("07a-derived-rollups-and-ttls.yml")
    user_roles = _render_user_roles(ssh_roles)
    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        "openbao_ssh_user_roles": user_roles,
        "openbao_ssh_engine_enabled": engine_enabled,
    }
    return templar.template(trust_as_template(derived["openbao_ssh_sign_policies"]))


def test_ssh_sign_policies_never_include_a_standalone_host_cert_leaf():
    """A host-cert role gets NO ssh-sign-<role> policy of its own -- a new
    policy name can only be written by a privileged provisioning run, and
    ssh-sign-host-cert was exactly that new name (PR #2203)."""
    policies = _render_sign_policies(LIVE_SSH_ROLES)

    names = [p["name"] for p in policies]
    assert "ssh-sign-host-cert" not in names
    # The pre-existing user-cert leaves are still derived, unchanged.
    assert set(names) == {
        "ssh-sign-automation-ai",
        "ssh-sign-automation-ai-diag",
        "ssh-sign-automation-ansible",
        "ssh-sign-automation-semaphore",
        "ssh-sign-ci-runner",
    }


def test_ssh_sign_host_cert_absent_from_both_unattended_identities():
    """Neither ansible-converge nor semaphore may carry a standalone
    ssh-sign-host-cert policy -- that grant is folded into their own
    ssh-sign-automation-{ansible,semaphore} policy CONTENT instead (see
    ssh-sign-policy.hcl.j2), which the reconcile identity already owns."""
    approles = _read_defaults("07b-base-approles.yml")["openbao_base_approles_core"]

    def _find(name_needle):
        for role in approles:
            if name_needle in role["name"]:
                return role
        raise AssertionError(f"no AppRole entry with {name_needle!r} in its name")

    converge_role = _find("openbao_ansible_converge_approle_name")
    semaphore_role = _find("openbao_semaphore_approle_name")

    templar = Templar(loader=DataLoader())

    templar.available_variables = {
        "openbao_ansible_converge_policy_name": "ansible-converge",
        "openbao_config_write_policy_name": "config-write",
        "openbao_ssh_engine_enabled": True,
    }
    converge_policies = templar.template(trust_as_template(converge_role["token_policies"]))
    assert "ssh-sign-host-cert" not in converge_policies
    assert "ssh-sign-automation-ansible" in converge_policies

    templar.available_variables = {
        "openbao_ansible_converge_policy_name": "ansible-converge",
        "openbao_semaphore_policy_name": "semaphore",
        "openbao_reconcile_policy_name": "reconcile",
        "openbao_ssh_engine_enabled": True,
    }
    semaphore_policies = templar.template(trust_as_template(semaphore_role["token_policies"]))
    assert "ssh-sign-host-cert" not in semaphore_policies
    assert "ssh-sign-automation-semaphore" in semaphore_policies


def test_ssh_sign_host_cert_absent_when_engine_disabled():
    """The existing ssh_engine_enabled kill switch must still cover the new
    leaf -- disabling the engine strips every ssh-sign-* grant, host included."""
    approles = _read_defaults("07b-base-approles.yml")["openbao_base_approles_core"]
    converge_role = next(
        r for r in approles if "openbao_ansible_converge_approle_name" in r["name"]
    )

    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        "openbao_ansible_converge_policy_name": "ansible-converge",
        "openbao_config_write_policy_name": "config-write",
        "openbao_ssh_engine_enabled": False,
    }
    policies = templar.template(trust_as_template(converge_role["token_policies"]))
    assert "ssh-sign-host-cert" not in policies
    assert "ssh-sign-automation-ansible" not in policies


def _render_sign_leaf(ssh_role_name, host_cert_signer_roles):
    """Render the REAL ssh-sign-policy.hcl.j2 template for one ssh_role,
    via the same lookup('template', ...) + template_vars={'item': item} the
    controller-side render task (08-rbac-policies.yml) uses -- never a
    reimplementation of the template's own Jinja."""
    tasks = yaml.safe_load(
        (ROOT / "roles/openbao/tasks/init/08-rbac-policies.yml").read_text(encoding="utf-8")
    )
    render_task = next(t for t in tasks if t.get("name") == "Render the RBAC policies on the controller")
    pairs_expr = render_task["vars"]["_openbao_rendered_policy_pairs"]

    item = {
        "name": f"ssh-sign-{ssh_role_name}",
        "template": "ssh-sign-policy.hcl.j2",
        "ssh_role": ssh_role_name,
    }
    templar = Templar(loader=DataLoader())
    templar.available_variables = {
        "openbao_reachable_policies": [item],
        "openbao_rbac_policy_targets": [item],
        "openbao_ssh_mount": "ssh-client-ca",
        "openbao_ssh_host_role_names": ["host-cert"],
        "openbao_ssh_host_cert_signer_roles": host_cert_signer_roles,
        "ansible_managed": "Ansible managed",
    }
    templar._loader.set_basedir(str(ROOT / "roles" / "openbao"))
    pairs = templar.template(trust_as_template(pairs_expr))
    return {p["key"]: p["value"] for p in pairs}[item["name"]]


def test_automation_signer_leaves_gain_an_update_only_host_cert_grant():
    """openbao_ssh_host_cert_signer_roles is the ONE variable deciding which
    user-cert sign leaves also carry the host-cert grant -- proven against
    the real template, not a reimplementation of its Jinja."""
    host_cert_signer_roles = ["automation-ansible", "automation-semaphore"]

    ansible_leaf = _render_sign_leaf("automation-ansible", host_cert_signer_roles)
    assert 'path "ssh-client-ca/sign/host-cert"' in ansible_leaf
    assert 'capabilities = ["update"]' in ansible_leaf

    semaphore_leaf = _render_sign_leaf("automation-semaphore", host_cert_signer_roles)
    assert 'path "ssh-client-ca/sign/host-cert"' in semaphore_leaf
    assert 'capabilities = ["update"]' in semaphore_leaf

    # A role NOT listed in openbao_ssh_host_cert_signer_roles never picks up
    # the extra grant -- ai-elevated's ssh-sign-automation-ai must stay
    # confined to exactly its own sign endpoint.
    ai_leaf = _render_sign_leaf("automation-ai", host_cert_signer_roles)
    assert "sign/host-cert" not in ai_leaf
