派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/assets_and_data.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/assets_and_data.md)；研究修改仍回到原件。

---

# Actual assets and recomputation

Execution root: /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention
Model/checkpoint/tokenizer/input IDs and hashes: manifest.json; original mainline:R13; no Dense/R15 cohort mixing.
Raw per-position candidate records: /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/analysis/raw_outputs.jsonl (all conditions native top10 IDs/probabilities).
Metrics: /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/analysis/position_metrics.csv; document_metrics.csv; summary_metrics.csv; scope_contrasts.csv; group_coverage.csv; head64_token_transitions.csv; legacy_replay.csv; PCA_and_identity.csv.
Reference: data/reference_documents.jsonl (60docs), data/reference_cache/*.npy (native residual activations); data/bases/layer01..28.npz (means/full eigensystems); data/random1031..1033.npy. Evaluation: data/evaluation_documents.jsonl; data/positions.jsonl exact737current+successor IDs/fullvisibleprefixes; data/eval_targets/*.npz actual untouched target vectors for all28layers. Reference/endpoints do not provide unseen-pretraining status.
Recompute with frozen scripts/run_gpu.py --stage fit_smoke, then --stage evaluate --rank0/1 only on authorized5090; analyze/validate/render (initial prose draft:deliver) onCPU with2threads. Use unchanged freeze inputs, skip only valid complete chunks, no resampling. run_gpu.py performs no optimization. Per-document complete JSONs are resume units.
Code/protocol/input freeze: freeze.json plus provenance/prestart_implementation_review.json. Numerical audits: audit/03_numerics_smoke.json and audit/validation.json. Resources/logs: execution_certificate.md, terminal_rank0/1.json,acp_receipts/pod/*.log,logs/rank0/1.log. Manifest completion is separate from immutable design.
Project evidence is a selected small copy, not every raw tensor. No commit/push/publication; scientific acceptance Unknown.

Exact required registry IDs and current access:provenance/input_assets.json.
