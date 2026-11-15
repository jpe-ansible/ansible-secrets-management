"""The converge policy reads the SSH host CA leaf, and nothing else under config/ssh."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "roles/openbao/templates/ansible-converge-policy.hcl.j2"
PATH_BLOCK = re.compile(r'path "([^"]+)"\s*\{\s*capabilities\s*=\s*\[([^]]+)\]\s*\}', re.MULTILINE)


def _grants() -> list[tuple[str, tuple[str, ...]]]:
    return [
        (path, tuple(re.findall(r'"([^"]+)"', capabilities)))
        for path, capabilities in PATH_BLOCK.findall(POLICY.read_text(encoding="utf-8"))
    ]


def test_converge_reads_exactly_the_ssh_host_ca_leaf() -> None:
    ssh_grants = [grant for grant in _grants() if "/ssh/" in grant[0] and "openbao_config_mount" in grant[0]]
    assert ssh_grants == [("{{ openbao_config_mount }}/data/ssh/converge", ("read",))]
