"""Shared CLI helpers for experiment runner entrypoints."""

from __future__ import annotations

import argparse
from pathlib import Path

from .registry import EXPERIMENTS, ROOT, describe


def build_parser(exp_ids: tuple[str, ...], description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--describe",
        action="store_true",
        help="Print expected outputs and paper labels without running experiments.",
    )
    parser.add_argument(
        "--out-root",
        default=str(ROOT),
        help="Paper workspace root. Defaults to the v2 paper directory.",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Use a small smoke-test configuration once the runner is implemented.",
    )
    parser.set_defaults(exp_ids=exp_ids)
    return parser


def describe_or_fail(args: argparse.Namespace) -> None:
    if args.describe:
        for exp_id in args.exp_ids:
            print(describe(exp_id))
            print()
        return

    exp_names = ", ".join(args.exp_ids)
    runner_names = ", ".join(EXPERIMENTS[e].runner for e in args.exp_ids)
    raise SystemExit(
        f"{runner_names} is structured for {exp_names}, but the experiment "
        "implementation is not filled in yet. Use --describe to inspect the "
        "output contract."
    )


def ensure_result_dirs(exp_ids: tuple[str, ...], out_root: str) -> None:
    root = Path(out_root)
    for exp_id in exp_ids:
        result_dir = root / EXPERIMENTS[exp_id].result_dir
        (result_dir / "figures").mkdir(parents=True, exist_ok=True)

