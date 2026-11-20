"""Public GitHub repository reads use and revoke mount-minted tokens."""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TASK_FILE = ROOT / "roles/openbao/tasks/init/05b-github-app-mount.yml"


def _flatten(tasks):
    for task in tasks:
        yield task
        for section in ("block", "rescue", "always"):
            yield from _flatten(task.get(section, []))


def test_public_repository_reads_are_authenticated_and_tokens_are_revoked():
    tasks = list(_flatten(yaml.safe_load(TASK_FILE.read_text(encoding="utf-8"))))
    mint = next(task for task in tasks if task.get("name", "").startswith(
        "Mint a metadata-only token for sets that are public-only"
    ))
    read = next(task for task in tasks if task.get("name", "").startswith(
        "Read the public repositories for sets that are public-only"
    ))
    revoke = next(task for task in tasks if task.get("name", "").startswith(
        "Revoke the metadata-only tokens for public repositories"
    ))

    assert mint["ansible.builtin.uri"]["body"] == {
        "org_name": "{{ item.public_repos_of }}",
        "permissions": {"metadata": "read"},
    }
    assert mint["no_log"] is True
    assert read["ansible.builtin.uri"]["headers"]["Authorization"].startswith("Bearer ")
    assert "openbao_github_app_mount_public_tokens.results" in (
        read["ansible.builtin.uri"]["headers"]["Authorization"]
    )
    assert "data.token" in read["ansible.builtin.uri"]["headers"]["Authorization"]
    assert read["loop"] == "{{ gm.permission_sets | selectattr('public_repos_of', 'defined') | list }}"
    assert read["register"] == "openbao_github_app_mount_public_repos"
    assert read["no_log"] is True
    assert revoke["ansible.builtin.uri"]["url"] == "{{ openbao_cli_addr }}/v1/sys/leases/revoke"
    assert revoke["ansible.builtin.uri"]["body"]["lease_id"] == "{{ item.json.lease_id }}"
    assert "openbao_github_app_mount_ready | bool" in revoke["when"]
    assert any("lease_id | default('', true) | length > 0" in c for c in revoke["when"])
    assert revoke["no_log"] is True
