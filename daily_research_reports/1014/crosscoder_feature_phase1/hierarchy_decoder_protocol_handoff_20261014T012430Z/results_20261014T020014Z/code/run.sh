#!/usr/bin/env bash
set -euo pipefail
cd /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder
source scripts/runtime.sh
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export MPLBACKEND=Agg
python /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z/code/watchdog.py /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z
