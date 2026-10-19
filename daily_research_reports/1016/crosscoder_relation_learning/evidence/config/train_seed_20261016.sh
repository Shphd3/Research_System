#!/usr/bin/env bash
set -euo pipefail
cd /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder
source scripts/runtime.sh
RUN=analysis/relation_learning/20261015T164000Z
CFG="$RUN/config/formal_R1_8.json"
export CUDA_VISIBLE_DEVICES=0
python analysis_tools/relation_learning/train_adapters.py --config "$CFG" --output "$RUN/learning/seed_20261016/R" --arm R --seed 20261016 --device cuda:0 > "$RUN/logs/train_20261016_R.log" 2>&1
python analysis_tools/relation_learning/train_adapters.py --config "$CFG" --output "$RUN/learning/seed_20261016/F" --arm F --seed 20261016 --device cuda:0 > "$RUN/logs/train_20261016_F.log" 2>&1
python analysis_tools/relation_learning/train_adapters.py --config "$CFG" --output "$RUN/learning/seed_20261016/N" --arm N --seed 20261016 --device cuda:0 > "$RUN/logs/train_20261016_N.log" 2>&1
