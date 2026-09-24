#!/usr/bin/env python3
"""Check that PROJECTS.md active-workstream entrypoints are local and tracked.

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


def tracked_paths(repo: Path) -> set[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=repo)
    return {(repo / item.decode()).resolve() for item in output.split(b"\0") if item}


def active_rows(text: str) -> list[tuple[str, str, str]]:
    section = text.split("## Active Research Workstreams", 1)[1]
    rows = []
    in_table = False
    for line in section.splitlines():
        if line.startswith("| Workstream |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            break
        if line.startswith("|---") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 5:
            rows.append((cells[0], cells[2], cells[3]))
    return rows


def main() -> int:
    tracked = tracked_paths(ROOT) | tracked_paths(PROJECT)
    failures = []
    checked = set()
    for name, focus_cell, evidence_cell in active_rows((ROOT / "PROJECTS.md").read_text()):
        targets = FOCUS.findall(focus_cell) + LINK.findall(evidence_cell)
        for target in targets:
            target = target.split("#", 1)[0]
            if not target or target.startswith(("http:", "https:")):
                continue
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
