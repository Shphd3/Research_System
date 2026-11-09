#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3${PYTHONPATH:+:$PYTHONPATH}
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python CUBLAS_WORKSPACE_CONFIG=:4096:8
source /data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/scripts/activate_5090_runtime.sh
# The registered allocation has two cards; the decoder needs only device0.
export CUDA_VISIBLE_DEVICES=0
