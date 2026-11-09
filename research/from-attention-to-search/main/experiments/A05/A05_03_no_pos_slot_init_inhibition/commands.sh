#!/usr/bin/env bash
set -euo pipefail

# Smoke validation used before ACP submission.
python Projects/from-attention-to-search/main/experiments/A05/A05_03_no_pos_slot_init_inhibition/scripts/run_a05_03_no_pos_slot_init_inhibition.py \
  --config Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0605a_true_token_conditioned_inhibition_replay.json \
  --output-dir Projects/from-attention-to-search/main/experiments/A05/A05_03_no_pos_slot_init_inhibition \
  --run-name smoke_20260608 \
  --run-stage smoke \
  --modes multi_b_primary \
  --conditions R0-dot,S0-dot,R1-dot,S1-dot \
  --seeds 20260521 \
  --train-samples-per-slot 64 \
  --eval-samples-per-slot 64 \
  --batch-size 32 \
  --eval-batch-size 64 \
  --variants-per-key 2 \
  --smoke-steps 2 \
  --max-parallel 1

# Full 4GPU ACP submission.
A0503_NOPOS_SLOT_ALLOW_REAL_SUBMIT=1 \
bash Projects/from-attention-to-search/main/experiments/A05/A05_03_no_pos_slot_init_inhibition/scripts/submit_a05_03_no_pos_slot_init_inhibition_4gpu_acp.sh

# Job id:
# pt-rzr278jh

