派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R01_behavior/reproduce.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R01_behavior/reproduce.md)；研究修改仍回到原件。

---

# Reproduction and actual artifacts

Execution root: `/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use`. All raw weights stay at their original manifest locations. No new training or downloads.

```bash
PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3 python /data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use/code/prepare.py
python /data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use/code/run.py smoke
python /data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use/code/run.py full
python /data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use/code/analyze.py
python /data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use/code/report.py
```

These are recorded commands, not an instruction to overwrite the frozen release. Preparation refuses an existing panel; scoring refuses incomplete output reuse and verifies complete receipts. Replay in an isolated new output root by copying code/config/data identity and retaining the originals. The current output-root constant is derived from each script location. Existing complete state scores can be reused by their raw/receipt hashes. Full execution requires the asset/engineering/budget gates in the Protocol; do not submit a new job from this note.

The run used system Python/PyTorch2.3.0 on existing H100MIG3g.40gb. The tokenizers dependency path is needed only for construction. Native source roots:20260913_dense_baseline_pretraining and20261031_dense_order_aligned_moe_baseline. Architecture/config and actual-token checks use native strict loaders. Every complete raw-score file has a sibling .receipt.json with full-state SHA, runtime, time, counts and freeze guards. audit/freeze.json retains original identities; amendment_A01.json records the estimator correction; analysis_and_native_source_identity.json identifies analysis/native code.

Data: data/panel.jsonl and families.json. State inventory: audit/checkpoints.csv and selected.json. Scores: results/full/*.jsonl. Statistics: tables/checkpoint_summary.csv, family_scores.csv, template_and_type.csv, near_far_contrasts.csv, no_evidence_preferences.csv, matched_tokens.csv and descriptive_crossings.csv. Coverage: tables/coverage_ledger.csv. Cost: audit/cost.json. Figure: figures/learning_curve.png, .pdf and .svg. Native execution/terminal logs: audit/full.log and full_terminal.json. Model pretraining counts, evaluation tokens and SAE training positions are separate counters.
