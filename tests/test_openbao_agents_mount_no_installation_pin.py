"""Sandbox token policies use only named sets and never pin installation IDs."""

from pathlib import Path
import re

from jinja2 import Environment
import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "roles/openbao/templates"
GITHUB_MOUNT_DEFAULTS = ROOT / "roles/openbao/defaults/main/03b-github-app-mounts.yml"
IDENTITY_DEFAULTS = ROOT / "roles/openbao/defaults/main/05l-dify-agent-identities.yml"
AGENTS_MOUNT = "github-agents"
PUBLIC_OWNERS = ["example-org", "Example-User"]
IDENTITIES = yaml.safe_load(IDENTITY_DEFAULTS.read_text(encoding="utf-8"))
ALLOWED_NAMED_SETS = {"public-read", "public-write"} | {
    f"public-{tier}-{owner.lower()}"
    for owner in PUBLIC_OWNERS
    for tier in ("read", "write")
} | {
    value
    for name, value in IDENTITIES.items()
    if name.startswith("openbao_dify_agent_")
    and name.endswith("_policy_name")
    and value not in {
        "agent-pr-keeper",
        "agent-github-clerk",
        "agent-merge-steward",
    }
}
RAW_MINT_PERMISSIONS = yaml.safe_load(GITHUB_MOUNT_DEFAULTS.read_text(encoding="utf-8"))[
    "openbao_github_agents_raw_mint_permissions"
]


def _agents_policy_templates():
    return sorted(
        path
        for path in TEMPLATE_DIR.rglob("*.j2")
        if "openbao_github_agents_mount" in path.read_text(encoding="utf-8")
    )


def _render_policy_source(source, owners=PUBLIC_OWNERS):
    environment = Environment(keep_trailing_newline=True, trim_blocks=True)
    environment.filters["comment"] = str
    return environment.from_string(source).render(
        ansible_managed="",
        openbao_kv_mount="secret",
        openbao_github_agents_mount=AGENTS_MOUNT,
        openbao_github_agents_public_owners=owners,
        openbao_github_agents_public_owner_set_inputs=owners,
        openbao_github_agents_installation_id="4242",
        openbao_github_agents_raw_mint_permissions=RAW_MINT_PERMISSIONS,
        openbao_sandbox_agent_read_approle_name="sandbox-agent-read",
        openbao_sandbox_agent_write_approle_name="sandbox-agent-write",
        openbao_sandbox_zcode_read_approle_name="sandbox-zcode-read",
        openbao_sandbox_zcode_write_approle_name="sandbox-zcode-write",
        openbao_sandbox_opencode_read_approle_name="sandbox-opencode-read",
        openbao_sandbox_opencode_write_approle_name="sandbox-opencode-write",
        openbao_sandbox_cursor_read_approle_name="sandbox-cursor-read",
        openbao_sandbox_cursor_write_approle_name="sandbox-cursor-write",
        **IDENTITIES,
    )


def _render_policy(path, owners=PUBLIC_OWNERS):
    return _render_policy_source(path.read_text(encoding="utf-8"), owners)


def test_empty_owner_list_emits_no_bytes_from_sandbox_policy_loops():
    templates = [
        TEMPLATE_DIR / f"{name}-policy.hcl.j2"
        for name in (
            "sandbox-agent-read",
            "sandbox-agent-write",
            "sandbox-cursor-read",
            "sandbox-cursor-write",
            "sandbox-opencode-read",
            "sandbox-opencode-write",
            "sandbox-zcode-read",
            "sandbox-zcode-write",
        )
    ]
    assert all(path.is_file() for path in templates)

    for template in templates:
        source = template.read_text(encoding="utf-8")
        baseline = re.sub(
            r"(?ms)^\{% for owner in openbao_github_agents_public_owner_set_inputs \| default\(\[\]\) %\}\n"
            r".*?^\{% endfor -%\}\n?",
            "",
            source,
        )
        assert (
            _render_policy_source(source, []) == _render_policy_source(baseline, [])
        ), template.name


def test_each_sandbox_policy_grants_the_base_set_and_each_public_owner_set():
    templates = [
        TEMPLATE_DIR / f"{name}-policy.hcl.j2"
        for name in (
            "sandbox-agent-read",
            "sandbox-agent-write",
            "sandbox-cursor-read",
            "sandbox-cursor-write",
            "sandbox-opencode-read",
            "sandbox-opencode-write",
            "sandbox-zcode-read",
            "sandbox-zcode-write",
        )
    ]
    assert len(templates) == 8

    for template in templates:
        rendered = _render_policy(template)
        tier = "read" if "-read-policy" in template.name else "write"
        expected = [
            f"{AGENTS_MOUNT}/token/public-{tier}",
            *(f"{AGENTS_MOUNT}/token/public-{tier}-{owner.lower()}" for owner in PUBLIC_OWNERS),
        ]
        stanzas = re.findall(r'(?ms)^path "([^"]+)" \{\n(.*?)^\}', rendered)
        grants = [
            (path, body)
            for path, body in stanzas
            if path.startswith(AGENTS_MOUNT + "/token/")
        ]
        assert [path for path, _body in grants] == expected, template.name
        assert [re.findall(r"capabilities = (.*)", body) for _path, body in grants] == [
            ['["create", "update"]'] for _path in expected
        ], template.name


def test_agents_mount_policies_have_no_installation_pin_or_undeclared_token_sets():
    templates = _agents_policy_templates()
    assert templates, "no policy templates reference openbao_github_agents_mount"
    failures = []

    for template in templates:
        rendered = _render_policy(template)
        stanzas = []
        for match in re.finditer(
            r'(?ms)^path "([^"]+)"\s*\{\n(.*?)^\}', rendered
        ):
            path = match.group(1)
            if path == AGENTS_MOUNT or path.startswith(AGENTS_MOUNT + "/"):
                stanzas.append((path, match.group(2)))
        assert stanzas, f"{template.name}: no rendered stanza on {AGENTS_MOUNT}"

        for path, body in stanzas:
            allowed_parameters = re.search(
                r"(?ms)^[ \t]*allowed_parameters[ \t]*=\s*\{(.*?)^  \}", body
            )
            if allowed_parameters and re.search(
                r'(?m)^[ \t]*"installation_id"[ \t]*=', allowed_parameters.group(1)
            ):
                failures.append(
                    f"{template.name}: stanza {path!r} allows installation_id"
                )

            named_set = re.fullmatch(
                re.escape(AGENTS_MOUNT) + r"/token/([^/]+)", path
            )
            if named_set and named_set.group(1) not in ALLOWED_NAMED_SETS:
                failures.append(
                    f"{template.name}: stanza {path!r} names an unapproved token set"
                )

    assert not failures, "\n".join(failures)
