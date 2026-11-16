"""The secret-age digest count stays after its stable correlation title."""

from __future__ import annotations

import re
from pathlib import Path

_TEMPLATE = (
    Path(__file__).resolve().parents[1]
    / "roles"
    / "openbao"
    / "templates"
    / "openbao-secret-age.sh.j2"
)


def test_changing_overdue_counts_keep_the_same_correlation_title() -> None:
    script = _TEMPLATE.read_text(encoding="utf-8")
    match = re.search(
        r'ntfy_send urgent "rotating_light,key" "(secrets overdue[^"]+)"', script
    )
    assert match is not None

    title_template = match.group(1)
    titles = [
        title_template.replace("${overdue_count}", count)
        for count in ("136", "137")
    ]

    assert titles == [
        "secrets overdue — 136 item(s)",
        "secrets overdue — 137 item(s)",
    ]
    assert [title.split(" — ", maxsplit=1)[0] for title in titles] == [
        "secrets overdue",
        "secrets overdue",
    ]


def test_due_digest_count_follows_its_stable_title() -> None:
    script = _TEMPLATE.read_text(encoding="utf-8")
    match = re.search(r'ntfy_send default key "([^"]+)"', script)

    assert match is not None
    assert match.group(1).replace("${daily_count}", "52") == (
        "secret rotation due — 52 item(s)"
    )
