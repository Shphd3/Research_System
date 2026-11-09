#!/usr/bin/env bash
set -euo pipefail
source scripts/runtime.sh
# Bounded same-allocation recovery avoids fresh scheduling for an ordinary implementation fix.
# Only a researcher-authorized operator on shared storage may request restart after preserving failure/freeze.
for attempt in 1 2 3; do
  set +e
  python -u scripts/run_gpu.py
  result=$?
  set -e
  [[ "$result" == 0 ]] && exit 0
  echo "FAILED_GATE attempt=$attempt result=$result; awaiting explicit local resume.request for at most300s"
  date -u +%s > audit/recovery_waiting.txt
  for second in $(seq 1 300); do
    if [[ -f audit/resume.request ]]; then
      mv audit/resume.request "audit/resume.consumed.$attempt"
      echo 'Documented operator repair requested same-allocation resume'
      break
    fi
    sleep 1
  done
  [[ -f "audit/resume.consumed.$attempt" ]] || exit "$result"
done
exit 1
