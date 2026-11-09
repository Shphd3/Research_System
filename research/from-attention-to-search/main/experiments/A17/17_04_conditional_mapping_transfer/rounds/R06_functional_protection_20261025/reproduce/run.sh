#!/usr/bin/env bash
set -euo pipefail
source /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/scripts/runtime.sh
export CUDA_VISIBLE_DEVICES=0
python /data/250010109/MoE_Router/experiments/20261025_a17_functional_protection/source/entry.py /data/250010109/MoE_Router/experiments/20261025_a17_functional_protection/source/engine.py
