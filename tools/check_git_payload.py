#!/usr/bin/env python3
"""Fail if generated daily-report payload is tracked in the root repository."""

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
GENERATED = {".csv", ".png", ".svg", ".pdf", ".jsonl", ".npz", ".npy", ".html"}


def prohibited(path: str) -> bool:
    if not path.startswith("daily_research_reports/"):
        return False
    parts = path.split("/")
    suffix = Path(path).suffix.lower()
    return (
        suffix in GENERATED
        or "/report_assets/fonts/" in path
        or (suffix == ".json" and any(part in {"tables", "figures", "results"} for part in parts))
    )


def main() -> int:
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).split(b"\0")
    bad = [raw.decode() for raw in tracked if raw and prohibited(raw.decode())]
    for path in bad:
        print(path)
    print(f"Root generated payload tracked: {len(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
