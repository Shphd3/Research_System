#!/usr/bin/env bash
set -euo pipefail
cd /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder
source scripts/runtime.sh
RUN=analysis/relation_learning/20261015T164000Z
CFG="$RUN/config/formal_R1_8.json"
export CUDA_VISIBLE_DEVICES=2
python analysis_tools/relation_learning/intervene.py --config "$CFG" --checkpoint "$RUN/learning/seed_20261018/R/checkpoints/update_03060.pt" --output "$RUN/intervention/seed_20261018/R" --arm R --seed 20261018 --device cuda:0 > "$RUN/logs/intervene_20261018_R.log" 2>&1
python analysis_tools/relation_learning/intervene.py --config "$CFG" --checkpoint "$RUN/learning/seed_20261018/F/checkpoints/update_03060.pt" --output "$RUN/intervention/seed_20261018/F" --arm F --seed 20261018 --device cuda:0 > "$RUN/logs/intervene_20261018_F.log" 2>&1
python analysis_tools/relation_learning/intervene.py --config "$CFG" --checkpoint "$RUN/learning/seed_20261018/N/checkpoints/update_03060.pt" --output "$RUN/intervention/seed_20261018/N" --arm N --seed 20261018 --device cuda:0 > "$RUN/logs/intervene_20261018_N.log" 2>&1
