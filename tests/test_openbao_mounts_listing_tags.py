"""The enabled-engines listing runs under every tag of every task that reads it.

Each task that reads openbao_mounts_raw is reached through init.yml under its
own tags, so the listing that registers the variable must carry those tags and
be imported before them. Otherwise a scoped run (for example --tags github)
reads an undefined variable.
"""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "roles/openbao/tasks"
INIT = TASKS / "init.yml"
LISTING = "init/03a-list-secrets-engines.yml"
SEED = "init/03-kv-mounts-and-seed-secrets.yml"
KV_MOUNTS = "init/03b-kv-mounts.yml"
GITHUB_ENGINE = "init/05-github-engine.yml"
GITHUB_MOUNT = "init/05b-github-app-mount.yml"
KNOWN_READERS = {
    SEED,
    KV_MOUNTS,
    "init/04-aws-engine.yml",
    "init/04b-azure-engine.yml",
    "init/04c-transit-engine.yml",
    GITHUB_ENGINE,
    GITHUB_MOUNT,
    "init/06-oauth-engine.yml",
    "init/07-ssh-ca-engine.yml",
    "init/07b-etcd-pki-engine.yml",
}


def _entries():
    """(file, tags) for each top-level import or include in init.yml, in run order."""
    entries = []
    for node in yaml.safe_load(INIT.read_text(encoding="utf-8")):
        for key in ("ansible.builtin.import_tasks", "ansible.builtin.include_tasks"):
            if key not in node:
                continue
            target = node[key]
            tags = set(node.get("tags", []))
            if isinstance(target, dict):
                tags |= set(target.get("apply", {}).get("tags", []))
                target = target["file"]
            entries.append((target, tags))
    return entries


def _reads_mounts(target):
    return "openbao_mounts_raw" in (TASKS / target).read_text(encoding="utf-8")


def test_listing_carries_every_tag_of_every_reader_and_runs_first():
    entries = _entries()
    targets = [target for target, _ in entries]
    listing_tags = next(tags for target, tags in entries if target == LISTING)
    readers = {target for target in targets if target != LISTING and _reads_mounts(target)}
    assert KNOWN_READERS <= readers
    for target, tags in entries:
        if target in readers:
            assert tags <= listing_tags, (target, sorted(tags - listing_tags))
            assert targets.index(LISTING) < targets.index(target), target


def test_github_only_run_resolves_the_listing_before_the_github_tasks():
    ran = [target for target, tags in _entries() if tags & {"github"}]
    assert LISTING in ran
    assert SEED not in ran
    assert ran.index(LISTING) < ran.index(GITHUB_ENGINE)
    assert ran.index(LISTING) < ran.index(GITHUB_MOUNT)
