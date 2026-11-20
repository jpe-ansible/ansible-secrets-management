"""The Hatchet token publisher stays inert and scoped to the worker-token KV entry."""

from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "roles/openbao/defaults/main"
TEMPLATE = ROOT / "roles/openbao/templates/hatchet-token-publisher-policy.hcl.j2"
ISSUER = ROOT / "roles/openbao/templates/approle-issuer-policy.hcl.j2"
CATALOG = ROOT / "playbooks/group_vars/all/openbao_secrets.yml"
LEAF = "apps/hatchet/worker-token"

POLICY_NAME = "{{ openbao_hatchet_token_publisher_policy_name }}"
APPROLE_NAME = "{{ openbao_hatchet_token_publisher_approle_name }}"


def _defaults(name):
    return yaml.safe_load((DEFAULTS / name).read_text(encoding="utf-8"))


def test_policy_has_only_the_worker_token_data_and_metadata_grants():
    template = TEMPLATE.read_text(encoding="utf-8")
    path_blocks = re.findall(
        r'^path "([^"]+)" \{\n  capabilities = \[([^]]+)\]\n\}',
        template,
        flags=re.MULTILINE,
    )

    assert path_blocks == [
        (f"{{{{ openbao_kv_mount }}}}/data/{LEAF}", '"create", "read", "update"'),
        (f"{{{{ openbao_kv_mount }}}}/metadata/{LEAF}", '"read"'),
    ]
    assert len(re.findall(r'^path "', template, flags=re.MULTILINE)) == 2


def test_policy_and_inert_approle_mirror_the_nautobot_publisher():
    names = _defaults("05b-domain-policy-approle-names.yml")
    approles = _defaults("07b-base-approles.yml")["openbao_base_approles_core"]
    policies = _defaults("07c-base-policies.yml")["openbao_base_policies_static"]

    role = next(item for item in approles if item.get("name") == APPROLE_NAME)
    policy = next(item for item in policies if item.get("name") == POLICY_NAME)
    nautobot = next(
        item for item in approles
        if item.get("name") == "{{ openbao_nautobot_token_publisher_approle_name }}"
    )

    assert names["openbao_hatchet_token_publisher_policy_name"] == "hatchet-token-publisher"
    assert names["openbao_hatchet_token_publisher_approle_name"] == "hatchet-token-publisher"
    assert role["policy"] == POLICY_NAME
    assert policy["template"] == TEMPLATE.name
    assert role["manage_secret_id"] is False
    assert {k: v for k, v in role.items() if k not in ("name", "policy")} == {
        k: v for k, v in nautobot.items() if k not in ("name", "policy")
    }
    assert "secret_id_issuance" not in role
    assert "openbao_hatchet_token_publisher_approle_name" not in ISSUER.read_text(encoding="utf-8")


def test_source_class_and_taxonomy_match_the_nautobot_publisher():
    overrides = _defaults("08b-cidr-and-unlock.yml")["openbao_approle_cidr_class_overrides"]
    taxonomy = (DEFAULTS / "08d-approle-taxonomy.yml").read_text(encoding="utf-8")

    assert overrides["hatchet-token-publisher"] == overrides["nautobot-token-publisher"] == "workstation"
    assert "'hatchet-token-publisher': 'operator-admin'," in taxonomy


def test_apps_domain_grants_the_leaf_without_prefetching_it():
    published = _defaults("05c-terrakube-and-remaining-domain-names.yml")[
        "openbao_apps_read_published_apps"
    ]
    assert LEAF.removeprefix("apps/") in published

    domains = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["openbao_secrets_domains"]
    apps_paths = next(domain for domain in domains if domain["name"] == "apps")["paths"]
    declared = [item["path"] if isinstance(item, dict) else item for item in apps_paths]
    assert LEAF not in declared
