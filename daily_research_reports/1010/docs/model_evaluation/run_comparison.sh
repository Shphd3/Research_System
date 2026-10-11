#!/usr/bin/env bash
# Local, read-only inference. No package installation, training or job submission.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
MODEL_EVAL_PYTHON="${MODEL_EVAL_PYTHON:-python}"
MODEL_EVAL_DEPS_DIR="${MODEL_EVAL_DEPS_DIR:-/data/250010109/dependency_packages/hf_transformers_qwen3}"
if [[ -d "$MODEL_EVAL_DEPS_DIR/tokenizers" ]]; then
  export PYTHONPATH="$MODEL_EVAL_DEPS_DIR${PYTHONPATH:+:$PYTHONPATH}"
fi
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1
export PYTHONIOENCODING=utf-8
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-4}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-4}"
# No prompt enters interactive mode; a quoted first argument selects one-shot.
if [[ $# -gt 0 && "$1" != -* ]]; then
  MODEL_EVAL_PROMPT="$1"
  shift
  set -- --prompt "$MODEL_EVAL_PROMPT" "$@"
fi
exec "$MODEL_EVAL_PYTHON" "$SCRIPT_DIR/compare_models.py" "$@"
