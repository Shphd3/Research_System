#!/usr/bin/env bash
set -euo pipefail
cd /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder
source scripts/runtime.sh
RUN=analysis/relation_learning/20261015T164000Z
CFG="$RUN/config/formal_R1_8.json"
export CUDA_VISIBLE_DEVICES=0
python analysis_tools/relation_learning/response_decomposition.py --root "$RUN" --config "$CFG" --arm R --seed 20261016 --device cuda:0 > "$RUN/logs/response_20261016_R.log" 2>&1
python analysis_tools/relation_learning/response_decomposition.py --root "$RUN" --config "$CFG" --arm F --seed 20261016 --device cuda:0 > "$RUN/logs/response_20261016_F.log" 2>&1
python analysis_tools/relation_learning/response_decomposition.py --root "$RUN" --config "$CFG" --arm N --seed 20261016 --device cuda:0 > "$RUN/logs/response_20261016_N.log" 2>&1
