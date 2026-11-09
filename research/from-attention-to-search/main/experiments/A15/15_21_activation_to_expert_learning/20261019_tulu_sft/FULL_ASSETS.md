# Full assets

Canonical reports: /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_21_activation_to_expert_learning/20261019_tulu_sft
Execution root: /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/sft_route_learning/20261019T012300Z
Actual states: training/<condition>/seed11 or seed22/epoch0.pt ... epoch3.pt, plus latest.pt for recovery. Base and dictionary are external frozen dependencies; branch files are not standalone LMs.
Cache: cache/train.pt,dev.pt,eval.pt; original source messages and exact token/label mapping:data/*.jsonl; original hashes:data/manifest.json.
Full routing: routes/*.npz; actual q/count/load matrices:metrics/exposure/*.npz. TensorBoard and steps:training/<condition>/seed*/. Source and freeze hashes:provenance/. No raw h/z, checkpoints, full per-position NLL arrays or code are included in the discussion copy.
