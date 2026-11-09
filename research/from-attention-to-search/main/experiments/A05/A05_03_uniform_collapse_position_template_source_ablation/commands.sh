#!/usr/bin/env bash
set -euo pipefail

# 4GPU ACP submission used for the completed run.
A0503_POSITION_ALLOW_REAL_SUBMIT=1 \
bash Projects/from-attention-to-search/main/experiments/A05/A05_03_uniform_collapse_position_template_source_ablation/scripts/submit_a05_03_position_template_source_ablation_4gpu_acp.sh

# Direct reproduction command inside the ACP worker.
python Projects/from-attention-to-search/main/experiments/A05/A05_03_uniform_collapse_position_template_source_ablation/scripts/run_a05_03_position_template_source_ablation.py \
  --config Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0605a_true_token_conditioned_inhibition_replay.json \
  --output-dir Projects/from-attention-to-search/main/experiments/A05/A05_03_uniform_collapse_position_template_source_ablation \
  --seeds 20260521,20260522,20260523 \
  --train-steps 1600 \
  --train-samples-per-slot 5000 \
  --batch-size 384 \
  --eval-batch-size 512 \
  --variants-per-key 16 \
  --run-step0 \
  --run-training \
  --parallel \
  --max-parallel 4
