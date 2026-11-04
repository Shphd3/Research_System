# Reproduce R14

Research owner: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1`. Execution owner: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1`. Actual dataset is1.3, initial protocol plus amendmentsA1–A11 and the metadata erratum. Do not rerun prepare over a frozen result. The old1.2 payload is retained under versions/data_v1p2, not merged silently. Scientific acceptance isUnknown.

## Read first

- [Report](report_cn.md), [Summary](summary_cn.md), [Detailed](detailed_cn.md).
- [Actual manifest](manifest.json), [initial frozen protocol](provenance/protocol_frozen_v1.md), [amendments](amendments.md), [condition coverage](coverage.csv).
- [Full input/candidate metadata with corrected length diagnostics](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/data/prefixes_effective_metadata.jsonl); [immutable actual model input source](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/data/prefixes.jsonl); [all positions](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/data/positions.jsonl); [family review](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/audit/semantic_review_48families.json).
- [Group members and three random seeds](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/data/feature_groups.json); [condition operations and aliases](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/data/conditions.json).
- [Every candidate token log probability](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/candidate_token_logprob.csv.gz), [every complete candidate score](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/candidate_sequence_scores.csv.gz), [prefix scores](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/prefix_scores.csv.gz), [family scores](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/family_metrics.csv).
- [Primary contrasts](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/primary_feature_contrasts.csv), [each random control](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/individual_random_contrasts.csv), [all paired contrasts](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/all_paired_contrasts.csv), [error transitions](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/error_transition_counts.csv), [length sensitivities](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/length_sensitivity.csv).
- [Group spectral projections](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/group_spectral_contributions.csv.gz), [cross terms](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/group_spectral_cross_terms.csv.gz), [all16384member support](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/all_feature_support.csv), [representative responses](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/representative_member_responses.csv), [unavailable counterexample slots](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1/analysis/member_counterexample_eligibility.json).

## CPU reaggregation from existing raw arrays

```bash
cd /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1
export OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2
/root/anaconda3/envs/spectral-hier/bin/python scripts/analyze.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/spectrum_members.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/validate.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/correction_impact.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/render.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/casebook.py
/root/anaconda3/envs/spectral-hier/bin/python scripts/report.py
```

These steps do not load a new classifier or train anything. They overwrite derived current views; preserve a new version before making scientific changes. Fresh forward reproduction uses `scripts/run_cpu_corrected.py`, actual exact model/CC weights from manifest, the same mounted transformers dependency,CPU2threads and frozen preflight. Source cache1.2 is accepted only through declared parent-freeze and exact per-sequence input-ID/index checks; corrected positions are never reused from the old text. `run_gpu.py` is the original authorized implementation, not an instruction to launch another allocation. No new run is started by this document.

## Numeric verification

[Independent raw reaggregation](provenance/independent_reaggregation.json) covers all167conditions/36evaluation families and paired control intervals. [Correction cache reuse](provenance/correction_reuse_validation.json) checks unchanged h/z and every untouched score. [Actual norm matching](evidence/applied_norm_matching_audit.csv) includes BF16 rounding differences and zeros. GPU and CPU phases are distinct in receipts; the only submitted job was stopped unallocated. Current scientific figures come from1.3, never an illustrative sketch.
