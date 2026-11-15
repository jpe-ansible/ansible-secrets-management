"""Workstation SSH key readers stay per-host and fail closed by default."""

import json
import os
import re
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

import yaml

from test_openbao_hatchet_killtest_policy_reach import REQUIRED_ENV, render, role_defaults
from test_openbao_ssh_host_cert_role import LIVE_SSH_ROLES, _render_sign_policies


ROOT = Path(__file__).resolve().parents[1]
ROLE = ROOT / "roles/openbao"
VALIDATION_TASK = ROLE / "tasks/init/00-validate-workstation-ssh-key-hosts.yml"
INPUT_ENV = "OPENBAO_WORKSTATION_SSH_KEY_HOSTS"
EXAMPLE_HOSTS = [
    {"name": "example-host-a", "cidr": "192.0.2.10/32"},
    {"name": "example-host-b", "cidr": "192.0.2.11/32"},
]


@contextmanager
def _variables(hosts_json=None):
    environment = {**REQUIRED_ENV, INPUT_ENV: ""}
    if hosts_json is not None:
        environment[INPUT_ENV] = hosts_json
    # No init task runs here: the rotation playbook loads only these defaults,
    # so the readers must come from the defaults alone.
    with mock.patch.dict(os.environ, environment):
        yield role_defaults()


def _render(expression, hosts_json=None):
    with _variables(hosts_json) as values:
        return render(values, expression)


def test_workstation_ssh_key_hosts_default_to_empty_json_list():
    with _variables() as values:
        assert render(values, "{{ openbao_workstation_ssh_key_hosts }}") == []
        assert render(values, "{{ openbao_workstation_ssh_key_reader_approles }}") == []
        assert render(values, "{{ openbao_workstation_ssh_key_reader_policies }}") == []

    assert _render("{{ openbao_workstation_ssh_key_reader_approles }}", "[]") == []
    assert _render("{{ openbao_workstation_ssh_key_reader_policies }}", "[]") == []


def test_each_host_gets_one_cidr_bound_doppler_synced_reader_and_policy():
    hosts_json = json.dumps(EXAMPLE_HOSTS)
    with _variables(hosts_json) as values:
        roles = render(values, "{{ openbao_workstation_ssh_key_reader_approles }}")
        policies = render(values, "{{ openbao_workstation_ssh_key_reader_policies }}")
        declared_roles = render(values, "{{ openbao_approles }}")
        declared_policies = render(values, "{{ openbao_policies }}")
        cli_parameters = render(values, "{{ openbao_approle_cli_parameters }}")
        ttl_overrides = render(values, "{{ openbao_approle_secret_id_ttl_overrides }}")
        workstation_roles = render(values, "{{ openbao_approles }}")
        scheduled_roles = render(values, "{{ openbao_secrets_domain_approle_names }}")
        sync_domains = render(values, "{{ openbao_rotate_doppler_sync_domains }}")
        classes = render(values, "{{ openbao_approle_class_map }}")
        rotated_ttl = render(values, "{{ openbao_rotated_domain_secret_id_ttl }}")
        local_llm_role = next(
            role for role in workstation_roles if role["name"] == "local-llm-workstation"
        )

        names = [f"ssh-key-{host['name']}" for host in EXAMPLE_HOSTS]
        assert [role["name"] for role in roles] == names
        assert [policy["name"] for policy in policies] == names
        for host, name, role, policy in zip(EXAMPLE_HOSTS, names, roles, policies):
            assert role == {
                "name": name,
                "policy": name,
                "secret_id_bound_cidrs": host["cidr"],
                "secret_id_num_uses": local_llm_role["secret_id_num_uses"],
                "token_ttl": "15m",
                "token_max_ttl": "15m",
            }
            assert policy == {
                "name": name,
                "template": "ssh-workstation-key-policy.hcl.j2",
                "host": host["name"],
            }
            assert next(
                candidate for candidate in declared_roles if candidate["name"] == name
            ) == role
            assert next(
                candidate for candidate in declared_policies if candidate["name"] == name
            ) == policy
            assert cli_parameters[name]["secret_id_bound_cidrs"] == host["cidr"]
            assert cli_parameters[name]["token_bound_cidrs"] == host["cidr"]
            assert (
                ttl_overrides[name]
                == ttl_overrides[local_llm_role["name"]]
                == rotated_ttl
            )
            assert name in scheduled_roles
            assert name in sync_domains
            assert classes[name] == "service-runtime"


def test_reader_policy_renders_exactly_one_read_stanza_for_its_host():
    hosts_json = json.dumps(EXAMPLE_HOSTS)
    source = (ROLE / "templates/ssh-workstation-key-policy.hcl.j2").read_text(encoding="utf-8")
    with _variables(hosts_json) as values:
        policies = render(values, "{{ openbao_workstation_ssh_key_reader_policies }}")
        for host, policy in zip(EXAMPLE_HOSTS, policies):
            rendered = render({**values, "item": policy}, source)
            paths = re.findall(r'^path "([^"]+)" \{\s*$', rendered, re.MULTILINE)
            assert paths == [f"int/data/ssh/{host['name']}/self"]
            assert re.findall(r'capabilities = \[(.*?)\]', rendered) == ['"read"']


def test_entry_may_bind_a_comma_separated_cidr_list():
    two = "192.0.2.10/32,192.0.2.12/32"
    with _variables(json.dumps([{"name": "example-host-a", "cidr": two}])) as values:
        cli = render(values, "{{ openbao_approle_cli_parameters }}")["ssh-key-example-host-a"]
        assert cli["secret_id_bound_cidrs"] == cli["token_bound_cidrs"] == two

    tasks = yaml.safe_load(VALIDATION_TASK.read_text(encoding="utf-8"))
    check = next(
        task for task in tasks[0]["block"]
        if task["name"] == "Validate workstation SSH key host names and CIDRs"
    )
    condition = "{{ " + check["ansible.builtin.assert"]["that"][-1].strip() + " }}"
    for cidr, valid in ((two, True), ("192.0.2.10/32,not-a-cidr", False), ("192.0.2.10/32,", False)):
        assert render({"item": {"name": "example-host-a", "cidr": cidr}}, condition) is valid, cidr


def test_empty_name_or_cidr_entry_declares_no_reader_or_policy():
    hosts_json = json.dumps([
        {"name": "", "cidr": "192.0.2.10/32"},
        {"name": "example-host-a", "cidr": ""},
        {"name": "example-host-b"},
    ])
    assert _render("{{ openbao_workstation_ssh_key_reader_approles }}", hosts_json) == []
    assert _render("{{ openbao_workstation_ssh_key_reader_policies }}", hosts_json) == []


def test_malformed_host_json_is_rescued_with_a_clear_environment_error():
    tasks = yaml.safe_load(VALIDATION_TASK.read_text(encoding="utf-8"))
    parse_task = tasks[0]
    assert parse_task["name"] == "Parse and validate OPENBAO_WORKSTATION_SSH_KEY_HOSTS"
    defaults = yaml.safe_load(
        (ROLE / "defaults/main/07l-workstation-ssh-key-readers.yml").read_text(encoding="utf-8")
    )
    assert "from_json" in defaults["openbao_workstation_ssh_key_hosts"]
    # The first assert evaluates the decoded default, so a decode error is rescued.
    assert "openbao_workstation_ssh_key_hosts" in str(parse_task["block"][0])
    assert "rescue" in parse_task
    failure = parse_task["rescue"][0]["ansible.builtin.fail"]["msg"]
    assert INPUT_ENV in failure
    assert "JSON list" in failure
    assert "Input values are omitted" in failure

    initialize = yaml.safe_load(
        (ROLE / "tasks/init/02-initialize-cluster.yml").read_text(encoding="utf-8")
    )
    assert initialize[0]["ansible.builtin.import_tasks"] == (
        "00-validate-workstation-ssh-key-hosts.yml"
    )
    assert initialize.index(next(
        task for task in initialize
        if task.get("name") == "Resolve the RBAC set this run's identity may manage"
    )) > 0


def test_keygen_is_short_lived_and_absent_from_derived_sign_and_issue_policies():
    ssh_defaults = yaml.safe_load(
        (ROLE / "defaults/main/05-ssh-ca-engine.yml").read_text(encoding="utf-8")
    )
    keygen = next(
        role for role in ssh_defaults["openbao_ssh_roles"] if role["name"] == "keygen"
    )
    assert keygen == {
        "name": "keygen",
        "principal": "x:keygen",
        "ttl": 60,
        "extensions": {},
    }
    assert "keygen" not in ssh_defaults["openbao_agent_ssh_sign_roles"]
    sign_policies = _render_sign_policies(LIVE_SSH_ROLES)
    assert all(policy["ssh_role"] != "keygen" for policy in sign_policies)
    assert all(policy["name"] != "ssh-sign-keygen" for policy in sign_policies)

    derived = yaml.safe_load(
        (ROLE / "defaults/main/07a-derived-rollups-and-ttls.yml").read_text(encoding="utf-8")
    )
    issue_policies = (
        _render("{{ openbao_ssh_issue_policies }}")
        if "openbao_ssh_issue_policies" in derived
        else []
    )
    assert all(
        policy.get("ssh_role") != "keygen"
        and policy.get("role") != "keygen"
        and policy.get("name") != "ssh-issue-keygen"
        for policy in issue_policies
    )
    assert all(
        policy.get("ssh_role") != "keygen"
        and policy.get("role") != "keygen"
        and policy.get("name") != "ssh-issue-keygen"
        for policy in _render("{{ openbao_policies }}")
    )
