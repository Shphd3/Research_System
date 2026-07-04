#!/usr/bin/env python3
"""Run V1 E6 only: balanced-assignment control."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> None:
    root = Path(__file__).resolve().parent
    outdir = root / "results" / "by_experiment" / "e6_balanced_assignment"
    cmd = [sys.executable, str(root / "run_synthetic.py"), "--experiments", "E6", "--outdir", str(outdir), "--full"]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()

