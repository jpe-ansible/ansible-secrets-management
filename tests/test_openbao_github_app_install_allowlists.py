"""Each GitHub App is checked against its mount's install allowlist, else the global one."""

import json

import yaml

from test_openbao_select import ROLE, condition, render, task


MOUNTS = ROLE / "defaults/main/03b-github-app-mounts.yml"
EXPOSURE = ROLE / "tasks/init/05c-github-app-exposure.yml"
CHECK = "FAIL -- webhook or unapproved installation on App {{ ga.app_id }}"
GLOBAL = ["exampleorg", "example-org", "example-client"]
PER_MOUNT = {"github-example": ["exampleorg"]}


def _defaults():
    return yaml.safe_load(MOUNTS.read_text(encoding="utf-8"))


def _allowlists(env):
    return render(_defaults()["openbao_github_app_install_allowlists"], {"openbao_platform_env": env})


def _check(mount, accounts, allowlists, global_allowlist=GLOBAL):
    node = task(CHECK, EXPOSURE)
    variables = {
        "ga": {"mount": mount, "app_id": "12345"},
        "openbao_github_app_installs": {"json": [{"account": {"login": a}} for a in accounts]},
        "openbao_github_app_hook": {"status": 404},
        "openbao_github_app_install_allowlist": global_allowlist,
        "openbao_github_app_install_allowlists": allowlists,
    }
    for name in ("_accounts", "_allowlist", "_unapproved"):
        variables[name] = render(node["vars"][name], variables)
    return all(condition(expression, variables) for expression in node["ansible.builtin.assert"]["that"])


def test_allowlists_come_from_one_json_object_and_default_to_empty():
    assert _allowlists({}) == {}
    assert _allowlists({"OPENBAO_GITHUB_APP_INSTALL_ALLOWLISTS": json.dumps(PER_MOUNT)}) == PER_MOUNT


def test_exposure_targets_carry_their_mount_and_keep_only_keyed_apps():
    variables = {
        "openbao_github_mount": "github-admin-example",
        "openbao_github_app_id": "1",
        "openbao_github_app_private_key": "fixture-key",
        "openbao_github_app_mounts": [
            {"mount": "github-example", "app_id": "2", "private_key": "fixture-key",
             "permission_sets": [{"name": "set"}]},
            {"mount": "github-unkeyed", "app_id": "3", "private_key": "", "permission_sets": []},
        ],
    }
    targets = render(_defaults()["openbao_github_app_exposure_targets"], variables)
    assert targets == [
        {"mount": "github-admin-example", "app_id": "1", "private_key": "fixture-key"},
        {"mount": "github-example", "app_id": "2", "private_key": "fixture-key"},
    ]
    unkeyed_admin = render(
        _defaults()["openbao_github_app_exposure_targets"],
        {**variables, "openbao_github_app_private_key": ""},
    )
    assert unkeyed_admin == [{"mount": "github-example", "app_id": "2", "private_key": "fixture-key"}]


def test_a_listed_mount_uses_only_its_own_allowlist():
    assert _check("github-example", ["exampleorg"], PER_MOUNT)
    assert not _check("github-example", ["exampleorg", "example-client"], PER_MOUNT)


def test_an_unlisted_mount_falls_back_to_the_global_allowlist():
    assert _check("github-other", ["exampleorg", "example-client"], PER_MOUNT)
    assert not _check("github-other", ["not-allowed"], PER_MOUNT)
    assert not _check("github-other", ["exampleorg"], PER_MOUNT, global_allowlist=[])


def test_a_malformed_or_empty_entry_fails_closed():
    assert not _check("github-example", ["exampleorg"], {"github-example": "exampleorg"})
    assert not _check("github-example", ["exampleorg"], {"github-example": []})
    assert not _check("github-example", ["exampleorg"], {"github-example": {"exampleorg": True}})
    # A null entry fails the shape condition before the difference is computed.
    node = task(CHECK, EXPOSURE)
    allowlist = render(node["vars"]["_allowlist"], {
        "ga": {"mount": "github-example"},
        "openbao_github_app_install_allowlist": GLOBAL,
        "openbao_github_app_install_allowlists": {"github-example": None},
    })
    assert not condition(node["ansible.builtin.assert"]["that"][0], {"_allowlist": allowlist})
