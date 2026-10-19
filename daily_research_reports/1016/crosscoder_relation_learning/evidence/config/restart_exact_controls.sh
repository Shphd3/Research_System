#!/usr/bin/env bash
set -euo pipefail
cd /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder
source scripts/runtime.sh
RUN=analysis/relation_learning/20261015T164000Z
export NUMBA_CACHE_DIR="$PWD/$RUN/platform/numba_cache_reserved"
mkdir -p "$NUMBA_CACHE_DIR"
nohup python analysis_tools/relation_learning/structure_a.py --mode repair-controls --input "$RUN/structure" --output "$RUN/structure/triple_counting_repair" --watch > "$RUN/logs/structure_exact_repair_restart1.log" 2>&1 < /dev/null &
echo $! > "$RUN/control/structure_repair_restart1.pid"
