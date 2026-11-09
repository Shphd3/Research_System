#!/usr/bin/env bash
set -euo pipefail
source scripts/runtime.sh
python -u scripts/run_gpu.py --stage smoke --rank 0
python -u scripts/run_gpu.py --stage evaluate --rank 0 > logs/rank0.log 2>&1 &
p0=$!
python -u scripts/run_gpu.py --stage evaluate --rank 1 > logs/rank1.log 2>&1 &
p1=$!
wait "$p0"
wait "$p1"
