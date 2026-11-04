派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/reproduce.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/reproduce.md)；研究修改仍回到原件。

---

# Reproduce R14

Research owner: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1`. Execution owner: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R14_20261102_concept_specificity_v1`. Actual dataset is1.3, initial protocol plus amendmentsA1–A11 and the metadata erratum. Do not rerun prepare over a frozen result. The old1.2 payload is retained under versions/data_v1p2, not merged silently. Scientific acceptance isUnknown.

## Read first

- [Report](report_cn.md), [Summary](summary_cn.md), [Detailed](detailed_cn.md).
- [Actual manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/manifest.json), [initial frozen protocol](../../../../../../../../UNAVAILABLE.md), [amendments](amendments.md), [condition coverage](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/coverage.csv).
- [Full input/candidate metadata with corrected length diagnostics](../../../../../../../../UNAVAILABLE.md); [immutable actual model input source](../../../../../../../../UNAVAILABLE.md); [all positions](../../../../../../../../UNAVAILABLE.md); [family review](../../../../../../../../UNAVAILABLE.md).
- [Group members and three random seeds](../../../../../../../../UNAVAILABLE.md); [condition operations and aliases](../../../../../../../../UNAVAILABLE.md).
- [Every candidate token log probability](../../../../../../../../UNAVAILABLE.md), [every complete candidate score](../../../../../../../../UNAVAILABLE.md), [prefix scores](../../../../../../../../UNAVAILABLE.md), [family scores](../../../../../../../../UNAVAILABLE.md).
- [Primary contrasts](../../../../../../../../UNAVAILABLE.md), [each random control](../../../../../../../../UNAVAILABLE.md), [all paired contrasts](../../../../../../../../UNAVAILABLE.md), [error transitions](../../../../../../../../UNAVAILABLE.md), [length sensitivities](../../../../../../../../UNAVAILABLE.md).
- [Group spectral projections](../../../../../../../../UNAVAILABLE.md), [cross terms](../../../../../../../../UNAVAILABLE.md), [all16384member support](../../../../../../../../UNAVAILABLE.md), [representative responses](../../../../../../../../UNAVAILABLE.md), [unavailable counterexample slots](../../../../../../../../UNAVAILABLE.md).

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

[Independent raw reaggregation](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/provenance/independent_reaggregation.json) covers all167conditions/36evaluation families and paired control intervals. [Correction cache reuse](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/provenance/correction_reuse_validation.json) checks unchanged h/z and every untouched score. [Actual norm matching](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/evidence/applied_norm_matching_audit.csv) includes BF16 rounding differences and zeros. GPU and CPU phases are distinct in receipts; the only submitted job was stopped unallocated. Current scientific figures come from1.3, never an illustrative sketch.
