#!/usr/bin/env python3
"""Extract embedded section-0 Thinking Cards into subject-bearing files."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


SECTION = re.compile(r"(?m)^## 0\. (?:Thinking Card|思考卡)\s*$")
NEXT_H2 = re.compile(r"(?m)^## (?!0\. (?:Thinking Card|思考卡)).+$")
TITLE = re.compile(r"(?m)^#\s+(.+?)\s*$")


def card_name(anchor: Path) -> str:
    name = anchor.name
    if name.endswith("_anchor_cn.md"):
        return name[: -len("_anchor_cn.md")] + "_thinking_card_cn.md"
    if name.endswith("_anchor.md"):
        return name[: -len("_anchor.md")] + "_thinking_card.md"
    if name.endswith("_cn.md"):
        return name[: -len("_cn.md")] + "_thinking_card_cn.md"
    if name.endswith(".md"):
        return anchor.stem + "_thinking_card.md"
    raise ValueError(f"not a Markdown filename: {anchor}")


def migrate(anchor: Path, *, check: bool) -> tuple[bool, str]:
    raw = anchor.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    start_match = SECTION.search(text)
    if not start_match:
        return False, "no embedded card"

    next_match = NEXT_H2.search(text, start_match.end())
    if not next_match:
        raise RuntimeError(f"no section after Thinking Card: {anchor}")

    title_match = TITLE.search(text)
    if not title_match:
        raise RuntimeError(f"missing anchor title: {anchor}")

    body = text[start_match.end() : next_match.start()].strip()
    target = anchor.with_name(card_name(anchor))
    if target.exists():
        raise RuntimeError(f"Thinking Card already exists: {target}")

    migrated_note = (
        f"> Migrated from [{anchor.name}]({anchor.name}) without changing the "
        "historical judgment. This file is the human-facing source; the anchor "
        "owns formal design and evidence."
    )
    card = f"# Thinking Card — {title_match.group(1)}\n\n{migrated_note}\n\n{body}\n"

    link = f"Thinking Card source: [{target.name}]({target.name})\n\n"
    updated = text[: start_match.start()] + link + text[next_match.start() :]
    updated = re.sub(
        r"(?m)^source_draft:\s*00_handwrite_anchor\.md\s*$",
        f"thinking_card_source: {target.name}",
        updated,
    )

    if not check:
        target.write_text(card, encoding="utf-8")
        encoded = updated.encode("utf-8")
        anchor.write_bytes((b"\xef\xbb\xbf" if bom else b"") + encoded)
    return True, target.name


def inherited_card(anchor: Path) -> Path | None:
    if anchor.parent.name == "subanchors":
        parent_stem = anchor.parent.parent.name
        candidate = anchor.parent.parent / f"{parent_stem}_thinking_card.md"
        return candidate if candidate.exists() else None
    if anchor.name.endswith("_anchor_cn.md"):
        stem = anchor.name[: -len("_anchor_cn.md")]
        candidate = anchor.with_name(f"{stem}_thinking_card.md")
        return candidate if candidate.exists() else None
    return None


def link_inherited(anchor: Path, *, check: bool) -> tuple[bool, str]:
    raw = anchor.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    if "Thinking Card source:" in text:
        return False, "already linked"
    card = inherited_card(anchor)
    if card is None:
        return False, "no inherited card"
    title_match = TITLE.search(text)
    if not title_match:
        raise RuntimeError(f"missing anchor title: {anchor}")
    relative = Path(os.path.relpath(card, anchor.parent)).as_posix()
    link = f"Thinking Card source: [{card.name}]({relative})"
    updated = (
        text[: title_match.end()].rstrip()
        + "\n\n"
        + link
        + "\n"
        + text[title_match.end() :].lstrip("\n")
    )
    if not check:
        encoded = updated.encode("utf-8")
        anchor.write_bytes((b"\xef\xbb\xbf" if bom else b"") + encoded)
    return True, relative


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "root",
        nargs="?",
        default="Projects/from-attention-to-search/main/problem_anchors",
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    anchors = sorted(
        path for path in root.rglob("*.md") if "_thinking_card" not in path.name
    )
    migrated = []
    for anchor in sorted(set(anchors)):
        changed, detail = migrate(anchor, check=args.check)
        if changed:
            migrated.append((anchor, detail))

    inherited = []
    for anchor in sorted(
        path
        for path in root.rglob("*.md")
        if (path.name.endswith("_anchor.md") or path.name.endswith("_anchor_cn.md"))
        and "_thinking_card" not in path.name
    ):
        changed, detail = link_inherited(anchor, check=args.check)
        if changed:
            inherited.append((anchor, detail))

    mode = "would migrate" if args.check else "migrated"
    print(f"{mode}: {len(migrated)} Thinking Cards")
    for anchor, target in migrated:
        print(f"{anchor.relative_to(root)} -> {target}")
    inherited_mode = "would link" if args.check else "linked"
    print(f"{inherited_mode}: {len(inherited)} anchors to inherited Thinking Cards")
    for anchor, target in inherited:
        print(f"{anchor.relative_to(root)} -> {target}")


if __name__ == "__main__":
    main()
