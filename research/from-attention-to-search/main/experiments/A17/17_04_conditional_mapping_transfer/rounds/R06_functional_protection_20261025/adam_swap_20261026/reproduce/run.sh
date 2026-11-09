#!/usr/bin/env bash
set -euo pipefail
# Model runtime reproduces a separate, explicitly bounded rerun only; completed worker refuses overwrite.
# This delivery does NOT rerun GPU work. CPU-only figure/table reconstruction:
python /data/250010109/MoE_Router/experiments/20261025_a17_functional_protection/ops/analyze_adam_swap_20261026.py
