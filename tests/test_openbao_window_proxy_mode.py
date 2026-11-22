"""Admin-window proxy routing keeps the token inside the controller proxy."""

import os
from unittest.mock import patch

import yaml

from test_openbao_select import ROLE, condition, render, task


TASKS = ROLE / "tasks"
DEFAULTS = yaml.safe_load((ROLE / "defaults/main/00-install-and-node.yml").read_text())
ADMIN_DEFAULTS = yaml.safe_load((ROLE / "defaults/main/08a-admin-and-ttls.yml").read_text())
MAIN = yaml.safe_load((TASKS / "main.yml").read_text())
DETECT_ADDR = MAIN[0]["ansible.builtin.set_fact"]["openbao_window_proxy_addr"]
DETECT_MODE = MAIN[1]["ansible.builtin.set_fact"]["openbao_window_proxy_mode"]
PROXY_ADDR = "http://127.0.0.1:8200"
PROXY_CONFIG = "/tmp/admin-window/bao.hcl"


def _proxy_mode(agent_addr, provisioning_token):
    environment = {
        "BAO_AGENT_ADDR": agent_addr,
        "OPENBAO_PROVISIONING_TOKEN": provisioning_token,
    }
    with patch.dict(os.environ, environment, clear=True):
        token = render(ADMIN_DEFAULTS["openbao_provisioning_token"], {})
        address = render(DETECT_ADDR, {})
        value = render(DETECT_MODE, {
            "openbao_window_proxy_addr": address,
            "openbao_provisioning_token": token,
        })
    return value is True or str(value).lower() == "true"


def _walk_tasks(nodes):
    for node in nodes or []:
        if not isinstance(node, dict):
            continue
        yield node
        for key in ("block", "rescue", "always"):
            yield from _walk_tasks(node.get(key))


def _named(nodes, name):
    return next(node for node in nodes if node.get("name") == name)


def _proxy_env(context):
    return {key: render(value, context) if isinstance(value, str) else value
            for key, value in DEFAULTS["openbao_window_proxy_env"].items()}


def _proxy_defaults(mode):
    context = {
        "openbao_window_proxy_mode": mode,
        "openbao_window_proxy_addr": PROXY_ADDR if mode else "",
        "openbao_status": {"initialized": True},
        "openbao_reconcile_addr": "http://ambient-server:8200",
        "openbao_write_addr": "http://node-local:8200",
        "inventory_hostname": "openbao-node",
    }
    context["openbao_cli_proxy_active"] = render(
        DEFAULTS["openbao_cli_proxy_active"], context
    )
    return context


def test_proxy_mode_requires_agent_address_and_empty_provisioning_token():
    with patch.dict(os.environ, {"BAO_AGENT_ADDR": PROXY_ADDR}, clear=True):
        assert render(DETECT_ADDR, {}) == PROXY_ADDR
    assert _proxy_mode(PROXY_ADDR, "")
    assert not _proxy_mode("", "")
    assert not _proxy_mode("   ", "")
    assert not _proxy_mode(PROXY_ADDR, "explicit-token")


def test_window_proxy_overrides_cli_host_and_every_cli_address():
    context = _proxy_defaults(True)
    with patch.dict(os.environ, {"BAO_AGENT_ADDR": PROXY_ADDR}, clear=True):
        assert render(DEFAULTS["openbao_cli_host"], context) == "localhost"
        assert render(DEFAULTS["openbao_cli_addr"], context) == PROXY_ADDR
        assert render(DEFAULTS["openbao_cli_become"], context) is False

    explicit = _proxy_defaults(False)
    with patch.dict(os.environ, {"BAO_AGENT_ADDR": PROXY_ADDR}, clear=True):
        assert render(DEFAULTS["openbao_cli_addr"], explicit) == "http://ambient-server:8200"
        assert render(DEFAULTS["openbao_cli_host"], explicit) == "localhost"


def test_proxy_import_forwards_agent_and_window_config_and_clears_token():
    configure = yaml.safe_load((TASKS / "main/configure_and_bootstrap.yml").read_text())
    bootstrap = _named(configure, "Bootstrap OpenBao (init, KV, policies, AppRoles)")
    with patch.dict(os.environ, {
        "BAO_AGENT_ADDR": PROXY_ADDR,
        "BAO_CONFIG_PATH": PROXY_CONFIG,
    }, clear=True):
        proxy_env = _proxy_env({"openbao_window_proxy_addr": PROXY_ADDR})
        inherited = render(bootstrap["environment"], {
            "openbao_cli_proxy_active": True,
            "openbao_window_proxy_env": proxy_env,
        })
    assert inherited == {
        "BAO_ADDR": PROXY_ADDR,
        "BAO_AGENT_ADDR": PROXY_ADDR,
        "BAO_CONFIG_PATH": PROXY_CONFIG,
        "BAO_TOKEN": "",
    }

    explicit = render(bootstrap["environment"], {"openbao_cli_proxy_active": False})
    assert explicit == {"BAO_AGENT_ADDR": ""}

    preflight = yaml.safe_load((TASKS / "init/01-preflight-and-cluster-probe.yml").read_text(encoding="utf-8"))
    config_guard = _named(preflight, "Require the proxy CLI config in admin-window mode")
    assert condition(config_guard["when"], {"openbao_window_proxy_mode": True})
    assert not condition(config_guard["when"], {"openbao_window_proxy_mode": False})
    assert "token helper" in config_guard["ansible.builtin.assert"]["fail_msg"]


def test_every_task_bao_token_environment_renders_empty_in_proxy_mode():
    context = {
        "openbao_bootstrap_token": "",
        "openbao_window_proxy_mode": True,
        "openbao_window_proxy_addr": PROXY_ADDR,
        "openbao_cli_proxy_active": True,
        "openbao_write_addr": "http://node-local:8200",
        "openbao_cli_addr": PROXY_ADDR,
        "openbao_cli_host": "localhost",
        "openbao_cli_become": False,
    }
    inherited = {
        "BAO_AGENT_ADDR": PROXY_ADDR,
        "BAO_CONFIG_PATH": PROXY_CONFIG,
        "BAO_TOKEN": "",
    }
    count = 0
    with patch.dict(os.environ, {"BAO_CONFIG_PATH": PROXY_CONFIG}, clear=True):
        for path in sorted(TASKS.rglob("*.yml")):
            for task_node in _walk_tasks(yaml.safe_load(path.read_text(encoding="utf-8"))):
                task_environment = task_node.get("environment") or {}
                # The templated import-level environment is asserted in its own test above.
                if not isinstance(task_environment, dict) or "BAO_TOKEN" not in task_environment:
                    continue
                effective = {**inherited, **task_environment}
                rendered = {
                    key: render(value, context) if isinstance(value, str) else value
                    for key, value in effective.items()
                }
                assert not str(rendered.get("BAO_TOKEN", "")).strip(), path
                assert rendered["BAO_AGENT_ADDR"] == PROXY_ADDR, path
                assert rendered["BAO_CONFIG_PATH"] == PROXY_CONFIG, path
                if "BAO_ADDR" in rendered and rendered["BAO_ADDR"] != PROXY_ADDR:
                    assert path.name in {
                        "tag_rotation_exempt.yml",
                        "declare_disclosure_denylist_metadata.yml",
                    }, path
                count += 1
    assert count > 0


def test_no_proxy_uses_the_existing_reconcile_login_and_token_facts():
    initialize = yaml.safe_load(
        (TASKS / "init/02-initialize-cluster.yml").read_text(encoding="utf-8")
    )
    context = {
        "openbao_status": {"initialized": True},
        "openbao_provisioning_token": "",
        "openbao_window_proxy_mode": False,
    }
    lookup = _named(initialize, "Look up the supplied token's own policies")
    login = _named(initialize, "Authenticate to the AppRole issuer for routine reconciliation")
    assert not all(condition(check, context) for check in lookup["when"])
    assert all(condition(check, context) for check in login["when"])

    token_fact = _named(initialize, "Use the per-call reconcile token when it authenticated")
    assert token_fact["ansible.builtin.set_fact"] == {
        "openbao_bootstrap_token": "{{ openbao_reconcile_login.login.auth.client_token }}",
        "openbao_reconcile_mode": True,
    }

    defaults = _proxy_defaults(False)
    with patch.dict(os.environ, {"BAO_AGENT_ADDR": "", "BAO_ADDR": "http://reconcile:8200"}, clear=True):
        defaults["openbao_reconcile_addr"] = "http://reconcile:8200"
        assert render(DEFAULTS["openbao_cli_host"], defaults) == "localhost"
        assert render(DEFAULTS["openbao_cli_addr"], defaults) == "http://reconcile:8200"


def test_explicit_provisioning_token_wins_over_agent_address():
    assert not _proxy_mode(PROXY_ADDR, "explicit-token")
    defaults = _proxy_defaults(False)
    with patch.dict(os.environ, {"BAO_AGENT_ADDR": PROXY_ADDR}, clear=True):
        assert render(DEFAULTS["openbao_cli_addr"], defaults) == "http://ambient-server:8200"

    initialize = yaml.safe_load(
        (TASKS / "init/02-initialize-cluster.yml").read_text(encoding="utf-8")
    )
    context = {"openbao_status": {"initialized": True}, "openbao_provisioning_token": "explicit-token"}
    supplied = _named(initialize, "Use the supplied provisioning token against a live cluster")
    login = _named(initialize, "Authenticate to the AppRole issuer for routine reconciliation")
    assert all(condition(check, context) for check in supplied["when"])
    assert not all(condition(check, context) for check in login["when"])
    lookup = _named(initialize, "Look up the supplied token's own policies")
    assert render(lookup["environment"]["BAO_TOKEN"], {"openbao_bootstrap_token": "explicit-token"}) == "explicit-token"


def test_window_lookup_self_uses_proxy_without_a_token_and_keeps_selection_guard():
    initialize = yaml.safe_load(
        (TASKS / "init/02-initialize-cluster.yml").read_text(encoding="utf-8")
    )
    lookup = _named(initialize, "Look up the supplied token's own policies")
    context = {
        "openbao_status": {"initialized": True},
        "openbao_provisioning_token": "",
        "openbao_window_proxy_mode": True,
        "openbao_bootstrap_token": "",
        "openbao_window_proxy_addr": PROXY_ADDR,
        "openbao_cli_addr": PROXY_ADDR,
        "openbao_cli_host": "localhost",
        "openbao_cli_become": False,
    }
    assert all(condition(check, context) for check in lookup["when"])
    assert render(lookup["environment"]["BAO_ADDR"], context) == PROXY_ADDR
    assert render(lookup["environment"]["BAO_TOKEN"], context) == ""
    assert render(lookup["delegate_to"], context) == "localhost"

    reconcile_tasks = (
        "Authenticate to the AppRole issuer for routine reconciliation",
        "Read the declared reconcile role_id through the issuer",
        "Mint a single-use reconcile secret_id through the issuer",
        "Log in as openbao-reconcile with the single-use secret_id",
        "Destroy the single-use reconcile secret_id by accessor",
    )
    for name in reconcile_tasks:
        assert not all(condition(check, context) for check in _named(initialize, name)["when"])

    bounded = _named(initialize, "Require an explicit bounded selection for ai-admin-session")
    assert condition(bounded["when"], {"openbao_ai_admin_window_mode": True})
    assert not condition(bounded["ansible.builtin.assert"]["that"][1], {"openbao_select": {}})


def test_guest_side_bao_calls_are_delegated_or_gated_by_fresh_init():
    preflight = yaml.safe_load(
        (TASKS / "init/01-preflight-and-cluster-probe.yml").read_text(encoding="utf-8")
    )
    status = _named(preflight, "Read OpenBao status")
    proxy_status = _named(preflight, "Read OpenBao status through the admin-window proxy")
    assert not condition(status["when"], {"openbao_window_proxy_mode": True})
    assert condition(proxy_status["when"], {"openbao_window_proxy_mode": True})
    assert proxy_status["delegate_to"] == "localhost"
    assert proxy_status["environment"] == "{{ openbao_window_proxy_env }}"
    proxy_env = _proxy_env({"openbao_window_proxy_addr": PROXY_ADDR})
    assert proxy_env["BAO_ADDR"] == proxy_env["BAO_AGENT_ADDR"] == PROXY_ADDR
    assert proxy_env["BAO_TOKEN"] == ""

    leader = yaml.safe_load((TASKS / "init/02b-policy-sync.yml").read_text(encoding="utf-8"))
    leader_status = _named(leader, "Read OpenBao status again to resolve the current Raft leader")
    proxy_leader_status = _named(
        leader,
        "Read OpenBao status through the admin-window proxy to resolve the current Raft leader",
    )
    assert not condition(leader_status["when"], {"openbao_cli_proxy_active": True})
    context = {
        "openbao_cli_proxy_active": True,
        "openbao_window_proxy_addr": PROXY_ADDR,
    }
    assert condition(proxy_leader_status["when"], context)
    assert render(proxy_leader_status["delegate_to"], context) == "localhost"
    assert proxy_leader_status["environment"] == "{{ openbao_window_proxy_env }}"

    init = yaml.safe_load((TASKS / "init/02-initialize-cluster.yml").read_text(encoding="utf-8"))
    fresh_init = _named(init, "Initialize OpenBao (recovery keys via static-key auto-unseal)")
    fresh_context = {
        "openbao_status": {"initialized": True},
        "openbao_existing_cluster_present": False,
        "openbao_allow_fresh_init": True,
    }
    fresh_expression = task(
        "Decide fresh-init vs join (join preserves an existing cluster's data)",
        TASKS / "init/01-preflight-and-cluster-probe.yml",
    )["ansible.builtin.set_fact"]["openbao_do_fresh_init"]
    fresh_value = render(fresh_expression, fresh_context)
    fresh_context["openbao_do_fresh_init"] = fresh_value is True or str(fresh_value).lower() == "true"
    assert not condition(fresh_init["when"], fresh_context)

    role_init = yaml.safe_load((TASKS / "init.yml").read_text(encoding="utf-8"))
    rotation = _named(role_init, "Tag operator-declared rotation-exempt paths (write-if-changed)")
    disclosure = _named(
        role_init,
        "Declare the disclosure-denylist entry's custom_metadata (write-if-changed)",
    )
    proxy_context = {
        "openbao_cli_proxy_active": True,
        "openbao_window_proxy_addr": PROXY_ADDR,
        "openbao_bootstrap_token": "",
        "openbao_select": {},
    }
    assert not all(condition(check, proxy_context) for check in rotation["when"])
    assert not all(condition(check, proxy_context) for check in disclosure["when"])


def test_fresh_operator_init_remains_on_the_openbao_guest():
    initialize = yaml.safe_load(
        (TASKS / "init/02-initialize-cluster.yml").read_text(encoding="utf-8")
    )
    init = _named(initialize, "Initialize OpenBao (recovery keys via static-key auto-unseal)")
    assert "delegate_to" not in init
    assert init["environment"]["BAO_ADDR"] == "{{ openbao_api_addr }}"
    assert "BAO_TOKEN" not in init["environment"]

    configure = yaml.safe_load((TASKS / "main/configure_and_bootstrap.yml").read_text())
    bootstrap = _named(configure, "Bootstrap OpenBao (init, KV, policies, AppRoles)")
    fresh_context = {
        "openbao_window_proxy_mode": True,
        "openbao_status": {"initialized": False},
    }
    fresh_context["openbao_cli_proxy_active"] = render(
        DEFAULTS["openbao_cli_proxy_active"], fresh_context
    )
    assert fresh_context["openbao_cli_proxy_active"] is False or str(
        fresh_context["openbao_cli_proxy_active"]
    ).lower() == "false"
    environment = render(bootstrap["environment"], fresh_context)
    assert environment == {"BAO_AGENT_ADDR": ""}


def test_status_reads_keep_their_failure_rules_and_separate_registers():
    # A skipped task overwrites its register, so the plain and proxy reads must not share one.
    preflight = yaml.safe_load((TASKS / "init/01-preflight-and-cluster-probe.yml").read_text(encoding="utf-8"))
    status = _named(preflight, "Read OpenBao status")
    proxy_status = _named(preflight, "Read OpenBao status through the admin-window proxy")
    assert status["register"] != proxy_status["register"]
    assert status["failed_when"] == f"{status['register']}.rc not in [0, 2]"
    assert proxy_status["failed_when"] == f"{proxy_status['register']}.rc not in [0, 2]"

    leader = yaml.safe_load((TASKS / "init/02b-policy-sync.yml").read_text(encoding="utf-8"))
    leader_status = _named(leader, "Read OpenBao status again to resolve the current Raft leader")
    proxy_leader_status = _named(
        leader,
        "Read OpenBao status through the admin-window proxy to resolve the current Raft leader",
    )
    assert leader_status["failed_when"] is False
    assert proxy_leader_status["failed_when"] is False
    assert leader_status["register"] != proxy_leader_status["register"]


def test_uri_tasks_reach_a_unix_socket_proxy_by_socket_path():
    def addresses(proxy_addr):
        context = _proxy_defaults(True) | {"openbao_window_proxy_addr": proxy_addr, "omit": "OMIT"}
        context["openbao_cli_addr"] = render(DEFAULTS["openbao_cli_addr"], context)
        return (render(DEFAULTS["openbao_cli_http_addr"], context),
                render(DEFAULTS["openbao_cli_unix_socket"], context))

    assert addresses("unix:///run/window/bao.sock") == ("http://localhost", "/run/window/bao.sock")
    assert addresses(PROXY_ADDR) == (PROXY_ADDR, "OMIT")

    direct = []
    for path in sorted(TASKS.rglob("*.yml")):
        for node in _walk_tasks(yaml.safe_load(path.read_text())):
            uri = node.get("ansible.builtin.uri")
            url = str(uri.get("url")) if isinstance(uri, dict) else ""
            if "openbao_cli_http_addr" in url:
                assert uri.get("unix_socket") == "{{ openbao_cli_unix_socket }}", node["name"]
                assert node.get("delegate_to") == "{{ openbao_cli_host }}", node["name"]
            elif "openbao_cli_addr" in url:
                direct.append(node["name"])
    # The one direct read is gated to runs without the proxy; its proxy twin follows it.
    assert direct == ["Read the arrangement KV leaf"]
