#!/usr/bin/env python3
"""Run V1 E4 only: covariance-isotropy counterexample."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> None:
    root = Path(__file__).resolve().parent
    outdir = root / "results" / "by_experiment" / "e4_covariance_counterexample"
    cmd = [sys.executable, str(root / "run_synthetic.py"), "--experiments", "E4", "--outdir", str(outdir), "--full"]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()

