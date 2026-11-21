"""Sandbox and Dify agent policies render their declared leaves and token sets."""

from pathlib import Path
import re
import unittest

from jinja2 import Environment, FileSystemLoader
import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "roles" / "openbao" / "templates"
IDENTITY_DEFAULTS = ROOT / "roles" / "openbao" / "defaults" / "main" / "05l-dify-agent-identities.yml"
IDENTITIES = yaml.safe_load(IDENTITY_DEFAULTS.read_text(encoding="utf-8"))
DIFY_AGENT_POLICY_NAMES = [
    value
    for name, value in IDENTITIES.items()
    if name.startswith("openbao_dify_agent_")
    and name.endswith("_policy_name")
    and value not in {
        "agent-pr-keeper",
        "agent-github-clerk",
        "agent-merge-steward",
        "agent-zammad-triage",
    }
]
POLICIES = (
    "sandbox-agent-read-policy.hcl.j2",
    "sandbox-agent-write-policy.hcl.j2",
)


def _render(policy):
    environment = Environment(loader=FileSystemLoader(TEMPLATES))
    environment.filters["comment"] = lambda value: "# " + str(value)
    return environment.get_template(policy).render(
        ansible_managed="managed",
        openbao_kv_mount="secret",
        openbao_github_agents_mount="github-agents",
        **IDENTITIES,
    )


class AgentPolicies(unittest.TestCase):
    def test_policies_do_not_read_external_secrets_or_wildcard_secret_paths(self):
        for policy in POLICIES:
            with self.subTest(policy=policy):
                rendered = _render(policy)
                self.assertNotIn("secrets-external", rendered)
                self.assertIsNone(
                    re.search(r'path "secret/(?:data|metadata)/[^"*+]*[*+][^"]*"', rendered)
                )

    def test_read_policy_reads_both_sandbox_leaves_and_the_read_token_set(self):
        rendered = _render(POLICIES[0])
        self.assertCountEqual(
            re.findall(
                r'path "([^"]+)" \{\s*capabilities = \[([^\]]+)\]\s*\}', rendered
            ),
            [
                ("secret/data/apps/sandbox-agent", '"read"'),
                ("secret/data/apps/sandbox-agent-router", '"read"'),
                ("github-agents/token/public-read", '"create", "update"'),
            ],
        )
        self.assertNotIn('path "github-agents/token/public-write"', rendered)

    def test_write_policy_reads_both_sandbox_leaves_and_mints_write_tokens(self):
        rendered = _render(POLICIES[1])
        self.assertCountEqual(
            re.findall(r'path "([^"]+)"', rendered),
            [
                "secret/data/apps/sandbox-agent",
                "secret/data/apps/sandbox-agent-router",
                "github-agents/token/public-write",
            ],
        )
        self.assertCountEqual(
            re.findall(
                r'path "([^"]+)" \{\s*capabilities = \[([^\]]+)\]\s*\}',
                rendered,
            ),
            [
                ("secret/data/apps/sandbox-agent", '"read"'),
                ("secret/data/apps/sandbox-agent-router", '"read"'),
                ("github-agents/token/public-write", '"create", "update"'),
            ],
        )
        self.assertNotIn("secrets-external", rendered)
        self.assertIsNone(
            re.search(r'path "secret/(?:data|metadata)/[^"*+]*[*+][^"]*"', rendered)
        )
        self.assertNotIn('path "secret/metadata', rendered)
        self.assertNotIn('path "github-agents/token/public-read"', rendered)

    def test_per_tool_policies_have_only_their_exact_grants(self):
        credentials = {
            "zcode": "secrets-external/data/ai/saas/zai",
            "opencode": "secret/data/apps/sandbox-agent-router",
            "cursor": "secrets-external/data/ai/saas/cursor",
        }
        for tool, credential in credentials.items():
            for tier in ("read", "write"):
                with self.subTest(tool=tool, tier=tier):
                    rendered = _render(f"sandbox-{tool}-{tier}-policy.hcl.j2")
                    paths = re.findall(r'path "([^"]+)"', rendered)
                    grants = re.findall(
                        r'path "([^"]+)" \{\s*capabilities = \[([^\]]+)\]\s*\}', rendered
                    )
                    self.assertEqual(paths, [credential, f"github-agents/token/public-{tier}"])
                    self.assertEqual(grants, [
                        (credential, '"read"'),
                        (f"github-agents/token/public-{tier}", '"create", "update"'),
                    ])
                    for other in credentials.values():
                        if other != credential:
                            self.assertNotIn(other, paths)
                    self.assertEqual([p for p in paths if p.startswith("secret/data/apps/")],
                                     [credential] if tool == "opencode" else [])
                    self.assertFalse(any("llm-router" in p or p.startswith("sys/")
                                         or "/metadata/" in p or "*" in p for p in paths))
                    self.assertNotIn('"list"', rendered)
                    # The only external ai/saas leaf a tool policy may read is
                    # its own credential; no sibling provider leaf is reachable.
                    self.assertEqual([p for p in paths if "/ai/saas/" in p],
                                     [credential] if "/ai/saas/" in credential else [])

    def test_fleet_agent_policies_mint_only_their_named_set(self):
        for name in DIFY_AGENT_POLICY_NAMES:
            with self.subTest(name=name):
                rendered = _render(f"{name}-policy.hcl.j2")
                path = f"github-agents/token/{name}"
                paths = re.findall(r'path "([^"]+)"', rendered)
                grants = re.findall(
                    r'path "([^"]+)" \{\s*capabilities = \[([^]]+)\]\s*\}',
                    rendered,
                )
                self.assertEqual(paths, [path])
                self.assertEqual(grants, [(path, '"create", "update"')])
                self.assertFalse(any(
                    p.startswith(("secret/data/", "secret/metadata/", "sys/"))
                    or "*" in p or (p.startswith("github-agents/token/") and p != path)
                    for p in paths
                ))

    def test_zammad_triage_policy_reads_only_its_runtime_leaf(self):
        rendered = _render("agent-zammad-triage-policy.hcl.j2")
        leaf = "secret/data/ai/dify/agent-runtime/zammad-triage"
        grants = re.findall(r'path "([^"]+)" \{\s*capabilities = \[([^]]+)\]\s*\}', rendered)
        self.assertEqual(re.findall(r'path "([^"]+)"', rendered), [leaf])
        self.assertEqual(grants, [(leaf, '"read"')])


if __name__ == "__main__":
    unittest.main()
