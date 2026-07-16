#!/usr/bin/env python3
"""Publish the complete anchor tree with repository-root-safe links."""

from __future__ import annotations

import argparse
import filecmp
import os
import re
import shutil
import tempfile
from pathlib import Path


LINK = re.compile(
    r"(?P<prefix>!?\[[^\]]*\]\()"
    r"(?P<destination><[^>]+>|[^)\s]+)"
    r"(?P<title>\s+(?:\"[^\"]*\"|'[^']*'))?"
    r"(?P<suffix>\))"
)
SCHEMES = ("http://", "https://", "mailto:", "data:", "chatgpt-conversation:")


def split_fragment(destination: str) -> tuple[str, str]:
    if "#" not in destination:
        return destination, ""
    path, fragment = destination.split("#", 1)
    return path, "#" + fragment


def inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def rewrite_markdown(
    text: str,
    source_file: Path,
    source_root: Path,
    repo_root: Path,
    missing: list[str],
) -> tuple[str, int]:
    rewrites = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal rewrites
        raw = match.group("destination")
        wrapped = raw.startswith("<") and raw.endswith(">")
        destination = raw[1:-1] if wrapped else raw

        if not destination or destination.startswith("#") or destination.startswith(SCHEMES):
            return match.group(0)

        path_part, fragment = split_fragment(destination)
        if not path_part:
            return match.group(0)

        if path_part.startswith("/"):
            resolved = repo_root / path_part.lstrip("/")
            if not resolved.exists():
                missing.append(f"{source_file}: {destination}")
            return match.group(0)

        resolved = (source_file.parent / path_part).resolve()
        if not resolved.exists():
            missing.append(f"{source_file}: {destination}")
            return match.group(0)

        if inside(resolved, source_root):
            return match.group(0)

        if not inside(resolved, repo_root):
            missing.append(f"{source_file}: link leaves repository: {destination}")
            return match.group(0)

        published = "/" + resolved.relative_to(repo_root).as_posix() + fragment
        if wrapped or " " in published:
            published = f"<{published}>"
        rewrites += 1
        return (
            match.group("prefix")
            + published
            + (match.group("title") or "")
            + match.group("suffix")
        )

    return LINK.sub(replace, text), rewrites


def build(source: Path, target: Path, repo_root: Path) -> tuple[int, int]:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)

    missing: list[str] = []
    rewritten_links = 0
    markdown_files = 0
    for target_file in sorted(target.rglob("*.md")):
        source_file = source / target_file.relative_to(target)
        raw = target_file.read_bytes()
        bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")
        updated, count = rewrite_markdown(text, source_file, source, repo_root, missing)
        target_file.write_bytes((b"\xef\xbb\xbf" if bom else b"") + updated.encode("utf-8"))
        rewritten_links += count
        markdown_files += 1

    if missing:
        raise RuntimeError("unresolved published links:\n" + "\n".join(missing))
    return markdown_files, rewritten_links


def directory_difference(expected: Path, actual: Path) -> list[str]:
    expected_files = {
        path.relative_to(expected) for path in expected.rglob("*") if path.is_file()
    }
    actual_files = {
        path.relative_to(actual) for path in actual.rglob("*") if path.is_file()
    }
    differences = [f"missing: {path}" for path in sorted(expected_files - actual_files)]
    differences += [f"extra: {path}" for path in sorted(actual_files - expected_files)]
    for relative in sorted(expected_files & actual_files):
        if not filecmp.cmp(expected / relative, actual / relative, shallow=False):
            differences.append(f"different: {relative}")
    return differences


def main() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        default=repo_root / "Projects/from-attention-to-search/main/problem_anchors",
        type=Path,
    )
    parser.add_argument(
        "--target",
        default=repo_root / "sync/S000_current_specialization/anchors",
        type=Path,
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    source = args.source.resolve()
    target = args.target.resolve()
    if not source.is_dir():
        raise SystemExit(f"source anchor tree not found: {source}")

    if args.check:
        with tempfile.TemporaryDirectory() as temporary:
            expected = Path(temporary) / "anchors"
            files, links = build(source, expected, repo_root)
            differences = directory_difference(expected, target)
            if differences:
                raise SystemExit("published mirror is stale:\n" + "\n".join(differences))
            print(f"mirror current: {files} Markdown files; {links} external links rewritten")
        return

    files, links = build(source, target, repo_root)
    print(f"published: {files} Markdown files; {links} external links rewritten")


if __name__ == "__main__":
    main()
