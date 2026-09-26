#!/usr/bin/env python3
"""Check that PROJECTS.md current analysis and workstream links exist and are tracked.

This checks routing, not scientific correctness or approval. Run from any cwd:
    python tools/check_current_entrypoints.py
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "Projects/from-attention-to-search"
LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
FOCUS = re.compile(r"`(daily_research_reports/[^`]+\.md)`")
CODE_PATH = re.compile(r"`([^`\n]+\.md(?:#[^`\n]*)?)`")


def tracked_paths(repo: Path) -> set[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=repo)
    return {(repo / item.decode()).resolve() for item in output.split(b"\0") if item}


def section_body(text: str, heading: str) -> str:
    marker = f"## {heading}\n"
    if marker not in text:
        raise ValueError(f"Missing required PROJECTS section: {heading}")
    return re.split(r"^## ", text.split(marker, 1)[1], maxsplit=1, flags=re.M)[0]


def local_targets(cell: str) -> list[str]:
    targets = []
    for target in LINK.findall(cell) + CODE_PATH.findall(cell):
        target = target.split("#", 1)[0]
        if target and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            targets.append(target)
    return list(dict.fromkeys(targets))


def active_rows(text: str) -> list[tuple[str, str, str]]:
    section = section_body(text, "Active Research Workstreams")
    rows = []
    columns = None
    required = ("Workstream", "Current Focus", "Evidence or contract")
    for line in section.splitlines():
        if line.startswith("| Workstream |"):
            header = [cell.strip() for cell in line.strip("|").split("|")]
            if not all(name in header for name in required):
                raise ValueError("Workstream table is missing a required column")
            columns = [header.index(name) for name in required]
            continue
        if columns is None:
            continue
        if not line.startswith("|"):
            break
        if line.startswith("|---") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(header):
            raise ValueError(f"Malformed workstream row: {cells[0]}")
        rows.append(tuple(cells[index] for index in columns))
    if not rows:
        raise ValueError("No workstream rows found; refusing an empty routing check")
    return rows


def current_entrypoints(text: str) -> list[tuple[str, str]]:
    entries = []
    for name, focus_cell, evidence_cell in active_rows(text):
        targets = local_targets(focus_cell) + local_targets(evidence_cell)
        if not targets:
            raise ValueError(f"Workstream has no local entrypoint: {name}")
        entries.extend((name, target) for target in targets)
    route = section_body(text, "Default Analysis Route — Shared-Learning Mechanisms")
    targets = local_targets(route)
    if not targets:
        raise ValueError("Default analysis route has no local entrypoint")
    entries.extend(("Default analysis route", target) for target in targets)
    return list(dict.fromkeys(entries))


def main() -> int:
    try:
        entries = current_entrypoints((ROOT / "PROJECTS.md").read_text())
    except ValueError as exc:
        print(f"INVALID   {exc}")
        return 2
    tracked = tracked_paths(ROOT) | tracked_paths(PROJECT)
    failures = []
    checked = set()
    for name, target in entries:
        path = (ROOT / target).resolve()
        key = (name, path)
        if key in checked:
            continue
        checked.add(key)
        if not path.is_file():
            failures.append(f"MISSING   {name}: {target}")
        elif path not in tracked:
            failures.append(f"UNTRACKED {name}: {target}")
    for failure in failures:
        print(failure)
    print(f"Checked {len(checked)} current entrypoints; {len(failures)} issue(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
