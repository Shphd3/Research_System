#!/usr/bin/env python3
"""Run V1 E5 only: anisotropy and whitening."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> None:
    root = Path(__file__).resolve().parent
    outdir = root / "results" / "by_experiment" / "e5_anisotropy_whitening"
    cmd = [sys.executable, str(root / "run_synthetic.py"), "--experiments", "E5", "--outdir", str(outdir), "--full"]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()

