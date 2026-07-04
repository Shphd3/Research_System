#!/usr/bin/env python3
"""Run V1 E3 only: expert spectral prototypes."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> None:
    root = Path(__file__).resolve().parent
    outdir = root / "results" / "by_experiment" / "e3_spectral_prototypes"
    cmd = [sys.executable, str(root / "run_synthetic.py"), "--experiments", "E3", "--outdir", str(outdir), "--full"]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()

