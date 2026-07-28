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
from urllib.parse import unquote


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
    published_sources: set[Path] | None = None,
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

        filesystem_path = unquote(path_part)

        if filesystem_path.startswith("/"):
            resolved = repo_root / filesystem_path.lstrip("/")
            if not resolved.exists():
                missing.append(f"{source_file}: {destination}")
            return match.group(0)

        resolved = (source_file.parent / filesystem_path).resolve()
        if not resolved.exists():
            missing.append(f"{source_file}: {destination}")
            return match.group(0)

        if inside(resolved, source_root) and (
            published_sources is None or resolved in published_sources
        ):
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


def build(
    source: Path,
    target: Path,
    repo_root: Path,
    exclude_dirs: set[str] | None = None,
) -> tuple[int, int]:
    exclude_dirs = exclude_dirs or set()
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(
        source,
        target,
        ignore=lambda _directory, names: [
            name for name in names if name in exclude_dirs
        ],
    )

    published_sources = {
        path.resolve()
        for path in source.rglob("*")
        if path.is_file()
        and not any(part in exclude_dirs for part in path.relative_to(source).parts)
    }

    missing: list[str] = []
    rewritten_links = 0
    markdown_files = 0
    for target_file in sorted(target.rglob("*.md")):
        source_file = source / target_file.relative_to(target)
        raw = target_file.read_bytes()
        bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")
        updated, count = rewrite_markdown(
            text,
            source_file,
            source,
            repo_root,
            missing,
            published_sources=published_sources,
        )
        target_file.write_bytes((b"\xef\xbb\xbf" if bom else b"") + updated.encode("utf-8"))
        rewritten_links += count
        markdown_files += 1

    if missing:
        raise RuntimeError("unresolved published links:\n" + "\n".join(missing))
    return markdown_files, rewritten_links


def build_selected(
    source: Path,
    target: Path,
    repo_root: Path,
    include_names: set[str],
) -> tuple[int, int]:
    """Publish selected Markdown files while preserving their source layout."""
    selected = {
        path.resolve()
        for path in source.rglob("*.md")
        if path.name in include_names
    }
    if not selected:
        raise RuntimeError(
            "no files matched --include-name: " + ", ".join(sorted(include_names))
        )

    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    missing: list[str] = []
    rewritten_links = 0
    for source_file in sorted(selected):
        target_file = target / source_file.relative_to(source)
        target_file.parent.mkdir(parents=True, exist_ok=True)
        raw = source_file.read_bytes()
        bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")
        updated, count = rewrite_markdown(
            text,
            source_file,
            source,
            repo_root,
            missing,
            published_sources=selected,
        )
        target_file.write_bytes(
            (b"\xef\xbb\xbf" if bom else b"") + updated.encode("utf-8")
        )
        rewritten_links += count

    if missing:
        raise RuntimeError("unresolved published links:\n" + "\n".join(missing))
    return len(selected), rewritten_links


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
    parser.add_argument(
        "--include-name",
        action="append",
        default=[],
        help="publish only Markdown files with this basename; may be repeated",
    )
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="exclude directories with this basename; may be repeated",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    target = args.target.resolve()
    if not source.is_dir():
        raise SystemExit(f"source anchor tree not found: {source}")

    include_names = set(args.include_name)
    exclude_dirs = set(args.exclude_dir)

    def publish(destination: Path) -> tuple[int, int]:
        if include_names:
            return build_selected(source, destination, repo_root, include_names)
        return build(source, destination, repo_root, exclude_dirs)

    if args.check:
        with tempfile.TemporaryDirectory() as temporary:
            expected = Path(temporary) / "anchors"
            files, links = publish(expected)
            differences = directory_difference(expected, target)
            if differences:
                raise SystemExit("published mirror is stale:\n" + "\n".join(differences))
            print(f"mirror current: {files} Markdown files; {links} external links rewritten")
        return

    files, links = publish(target)
    print(f"published: {files} Markdown files; {links} external links rewritten")


if __name__ == "__main__":
    main()
