#!/usr/bin/env python3
"""Run V1 E1 only: uniform sphere and prototype geometry."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> None:
    root = Path(__file__).resolve().parent
    outdir = root / "results" / "by_experiment" / "e1_uniform_sphere"
    cmd = [sys.executable, str(root / "run_synthetic.py"), "--experiments", "E1", "--outdir", str(outdir), "--full"]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()

