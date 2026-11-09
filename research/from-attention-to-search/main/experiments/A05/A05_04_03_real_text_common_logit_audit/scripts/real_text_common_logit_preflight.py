#!/usr/bin/env python3
"""Preflight checks for the DCLM real-text common-logit audit.

This script does not run the experiment. It checks whether the protocol's
data, source, model, and manifest assumptions are explicit enough before a
full run is approved.
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import hashlib
import json
import os
import platform
import re
import socket
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_DATA_PATH = Path("/data/share/109_cache_dir/hf_data/dclm_bin")
DEFAULT_CODE_ROOT = Path("/data/250010109/MoE_Router")
DEFAULT_MODEL_SOURCE = DEFAULT_CODE_ROOT / "src/model/qwen3_moe"
DEFAULT_TRAIN_SCRIPT = DEFAULT_CODE_ROOT / "train_qwen3_moe.py"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def run_cmd(cmd: list[str], cwd: Path | None = None) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd is not None else None,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception as exc:  # pragma: no cover - defensive environment capture
        return {"ok": False, "stdout": "", "stderr": repr(exc), "returncode": None}
    return {
        "ok": proc.returncode == 0,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "returncode": proc.returncode,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def file_list_digest(root: Path) -> dict[str, Any]:
    files = sorted(p for p in root.rglob("*.py") if p.is_file())
    h = hashlib.sha256()
    rows = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        digest = sha256_file(path)
        rows.append({"path": rel, "sha256": digest, "bytes": path.stat().st_size})
        h.update(rel.encode("utf-8"))
        h.update(digest.encode("ascii"))
    return {"root": str(root), "combined_sha256": h.hexdigest(), "files": rows}


def scan_bin_files(data_path: Path, dtype_bytes: int) -> dict[str, Any]:
    files = [Path(p) for p in sorted(glob.glob(str(data_path / "**/*.bin"), recursive=True))]
    rows = []
    total_tokens = 0
    for path in files:
        size = path.stat().st_size
        tokens = size // dtype_bytes
        rows.append(
            {
                "path": str(path),
                "bytes": size,
                "tokens": tokens,
                "start_token_global": total_tokens,
                "end_token_global": total_tokens + tokens,
            }
        )
        total_tokens += tokens
    return {"files": rows, "total_tokens": total_tokens}


def locate_offset(file_rows: list[dict[str, Any]], global_offset: int) -> dict[str, Any]:
    for row in file_rows:
        if row["start_token_global"] <= global_offset < row["end_token_global"]:
            return {
                "shard_path": row["path"],
                "start_token_offset": global_offset - row["start_token_global"],
                "global_token_offset": global_offset,
            }
    last = file_rows[-1] if file_rows else None
    return {
        "shard_path": None if last is None else last["path"],
        "start_token_offset": None,
        "global_token_offset": global_offset,
        "error": "offset_out_of_range",
    }


def build_manifest_preview(
    file_rows: list[dict[str, Any]],
    split: str,
    start_sample: int,
    num_sequences: int,
    sequence_length: int,
    sample_stride: int,
    max_rows: int,
) -> list[dict[str, Any]]:
    out = []
    for i in range(min(num_sequences, max_rows)):
        sample_index = start_sample + i
        global_offset = sample_index * sample_stride
        ref = locate_offset(file_rows, global_offset)
        row = {
            "dataset": "DCLM-bin",
            "split": split,
            "loader_sample_index": sample_index,
            "sequence_length": sequence_length,
            "input_token_start_delta": 0,
            "input_token_count": sequence_length,
            "target_token_start_delta": 1,
            "target_token_count": sequence_length,
            "span_length": sequence_length + 1,
            "sample_stride": sample_stride,
        }
        row.update(ref)
        out.append(row)
    return out


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def grep(pattern: str, text: str) -> bool:
    return re.search(pattern, text, flags=re.MULTILINE) is not None


def static_code_checks(code_root: Path, model_source: Path, train_script: Path) -> list[dict[str, Any]]:
    checks = []
    myqwen = model_source / "myqwen.py"
    qconfig = model_source / "qwen3config.py"
    train_text = read_text(train_script) if train_script.exists() else ""
    myqwen_text = read_text(myqwen) if myqwen.exists() else ""
    qconfig_text = read_text(qconfig) if qconfig.exists() else ""

    def add(name: str, ok: bool, detail: str, severity: str = "info") -> None:
        checks.append({"name": name, "ok": bool(ok), "severity": severity, "detail": detail})

    add(
        "linear_router_bias_false",
        "self.gate = nn.Linear(self.routing_input_dim, config.num_experts, bias=False)" in myqwen_text,
        "Main linear MoE gate is bias-free in MyQwen3SparseMoeBlock.",
        "error",
    )
    add(
        "shared_expert_disabled_contract",
        "use_shared_expert" in myqwen_text and "if self.use_shared_expert else None" in myqwen_text,
        "Protocol requires an explicit use_shared_expert switch so the main audit can disable the always-on shared path.",
        "error",
    )
    add(
        "train_default_top_k",
        '--num_experts_per_tok", type=int, default=2' not in train_text,
        "train_qwen3_moe.py defaults top_k to 2; full run must pass --num_experts_per_tok 1 and log it.",
        "warning",
    )
    add(
        "top1_output_weight_training_contract",
        '--norm_topk_prob", action="store_true"' in train_text,
        "For Phase 3/4, keep norm_topk_prob=false with top_k=1 so task loss can still reach router logits through the selected softmax probability.",
        "info",
    )
    add(
        "train_default_load_balance_off",
        '--lambda_lb", type=float, default=0.01' not in train_text,
        "train_qwen3_moe.py defaults lambda_lb to 0.01; full run must pass --lambda_lb 0.0.",
        "warning",
    )
    add(
        "train_default_gating_reference_hidden",
        '--gating_reference", type=str, default="oracle"' not in train_text,
        "Default gating_reference is oracle; protocol wants router input hidden states, so full run must use a non-oracle value and record it.",
        "warning",
    )
    add(
        "router_input_hidden_states_returned",
        "router_input_hidden_states" in myqwen_text or "return_router_logits" in myqwen_text,
        "Current block returns selected_experts and losses, but not router-input hidden states or raw router logits.",
        "warning",
    )
    add(
        "small_config_override_available",
        '--num_layers", type=int' in train_text and "--mlp_ratio" in train_text,
        "Training script can override layer count and MLP ratio, but hidden size/head count require a config directory.",
        "info",
    )
    add(
        "qwen_config_has_moe_fields",
        "num_experts" in qconfig_text and "num_experts_per_tok" in qconfig_text,
        "Qwen3Config stores MoE expert count and top-k fields.",
        "info",
    )
    add(
        "git_status_access",
        run_cmd(["git", "status", "--short", "--branch"], cwd=code_root)["ok"],
        "If false, source_manifest cannot record git status until safe.directory or an alternate source hash policy is used.",
        "warning",
    )
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-path", type=Path, default=DEFAULT_DATA_PATH)
    parser.add_argument("--code-root", type=Path, default=DEFAULT_CODE_ROOT)
    parser.add_argument("--model-source", type=Path, default=DEFAULT_MODEL_SOURCE)
    parser.add_argument("--train-script", type=Path, default=DEFAULT_TRAIN_SCRIPT)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--sequence-length", type=int, default=256, help="Input token length used by the model.")
    parser.add_argument("--span-length", type=int, default=257, help="Token span needed for input plus shifted LM target.")
    parser.add_argument("--audit-num-sequences", type=int, default=8192)
    parser.add_argument("--train-num-sequences", type=int, default=32768)
    parser.add_argument("--sample-stride", type=int, default=257)
    parser.add_argument("--dtype-bytes", type=int, default=4)
    parser.add_argument("--manifest-preview-rows", type=int, default=16)
    parser.add_argument("--write-snapshot", action="store_true")
    args = parser.parse_args()

    timestamp = dt.datetime.now(dt.timezone.utc).isoformat()
    output_dir = args.output_dir
    if output_dir is None:
        exp_dir = Path(__file__).resolve().parents[1]
        output_dir = exp_dir / "source_list/real_text_common_logit_audit_v5_preflight"

    errors = []
    warnings = []
    for path_name, path in [
        ("data_path", args.data_path),
        ("code_root", args.code_root),
        ("model_source", args.model_source),
        ("train_script", args.train_script),
    ]:
        if not path.exists():
            errors.append(f"{path_name} does not exist: {path}")

    bin_scan = {"files": [], "total_tokens": 0}
    audit_preview: list[dict[str, Any]] = []
    train_preview: list[dict[str, Any]] = []
    if args.data_path.exists():
        bin_scan = scan_bin_files(args.data_path, args.dtype_bytes)
        if not bin_scan["files"]:
            errors.append(f"No .bin files found under {args.data_path}")
        else:
            needed_samples = args.audit_num_sequences + args.train_num_sequences
            needed_tokens = (needed_samples - 1) * args.sample_stride + args.span_length
            if bin_scan["total_tokens"] < needed_tokens:
                errors.append(
                    f"Not enough tokens for requested manifest: need {needed_tokens}, found {bin_scan['total_tokens']}"
                )
            audit_preview = build_manifest_preview(
                bin_scan["files"],
                "audit",
                0,
                args.audit_num_sequences,
                args.sequence_length,
                args.sample_stride,
                args.manifest_preview_rows,
            )
            train_preview = build_manifest_preview(
                bin_scan["files"],
                "train",
                args.audit_num_sequences,
                args.train_num_sequences,
                args.sequence_length,
                args.sample_stride,
                args.manifest_preview_rows,
            )

    if args.span_length != args.sequence_length + 1:
        warnings.append("span_length should usually be sequence_length + 1 for next-token LM samples.")
    if args.sample_stride != args.span_length:
        warnings.append("sample_stride should equal span_length for deterministic non-overlapping LM samples.")

    source_manifest = {
        "timestamp_utc": timestamp,
        "machine": socket.gethostname(),
        "platform": platform.platform(),
        "python": sys.version.replace("\n", " "),
        "data_source_path": str(args.data_path),
        "model_architecture_source_path": str(args.model_source),
        "execution_script_source_path": str(args.train_script),
        "train_script_sha256": sha256_file(args.train_script) if args.train_script.exists() else None,
        "model_source_digest": file_list_digest(args.model_source) if args.model_source.exists() else None,
        "git_rev_parse_head": run_cmd(["git", "rev-parse", "HEAD"], cwd=args.code_root),
        "git_status_short_branch": run_cmd(["git", "status", "--short", "--branch"], cwd=args.code_root),
    }

    checks = static_code_checks(args.code_root, args.model_source, args.train_script) if args.train_script.exists() else []
    for check in checks:
        if not check["ok"] and check["severity"] == "error":
            errors.append(f"{check['name']}: {check['detail']}")
        elif not check["ok"] and check["severity"] == "warning":
            warnings.append(f"{check['name']}: {check['detail']}")

    report = {
        "status": "fail" if errors else "pass_with_warnings" if warnings else "pass",
        "timestamp_utc": timestamp,
        "errors": errors,
        "warnings": warnings,
        "protocol_parameters": {
            "sequence_length": args.sequence_length,
            "span_length": args.span_length,
            "audit_num_sequences": args.audit_num_sequences,
            "train_num_sequences": args.train_num_sequences,
            "sample_stride": args.sample_stride,
            "dtype_bytes": args.dtype_bytes,
        },
        "dataset_scan": {
            "bin_file_count": len(bin_scan["files"]),
            "total_tokens": bin_scan["total_tokens"],
            "first_files": bin_scan["files"][:5],
        },
        "static_code_checks": checks,
        "audit_manifest_preview": audit_preview,
        "train_manifest_preview": train_preview,
        "source_manifest_preview": source_manifest,
    }

    if args.write_snapshot:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "preflight_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        (output_dir / "source_manifest.json").write_text(json.dumps(source_manifest, indent=2, sort_keys=True), encoding="utf-8")
        write_jsonl(output_dir / "audit_manifest_preview.jsonl", audit_preview)
        write_jsonl(output_dir / "train_manifest_preview.jsonl", train_preview)

    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
