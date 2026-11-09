#!/usr/bin/env bash
set -euo pipefail
source /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/scripts/runtime.sh
# Actual CPU entrypoint, frozen original output refuses overwrite after completion:
python /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/context_dependency_20261026/execution/source/discover_support.py
# Reproduction requires a new output destination while retaining original source/settings.
