派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/dataset_guide.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/dataset_guide.md)；研究修改仍回到原件。

---

# D1 data and reproducibility guide

Execution owner: `/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1`. Canonical scientific interpretation: [Summary](summary.md), [Detailed](detailed.md), twelve route conclusion_update records. Original R17 files remain at `/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02`. No model checkpoint is produced by this analysis.

| Object | Exact location | Meaning |
|---|---|---|
| Adopted prompt | [NEXT_ROUND_PROMPT](../../../../../../../../../../UNAVAILABLE.md) | Exact33398-byte recovery from same-thread original tool output; ZIP attachment itself unavailable on current mount |
| Input recovery provenance | [record](../../../../../../../../../../UNAVAILABLE.md) | Distinguishes recovered prompt from unrecovered originalZIP |
| Panel full texts/token IDs | [shared](../../../../../../../../../../UNAVAILABLE.md) | original_old384,corrected_old384,fresh_locked288,factor_appendix48 JSONL |
| Frozen plan | [machine contract](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/frozen_diagnostic_plan.json) | Counts, seeds, budgets, tensor locations, statistical groups |
| Fresh gate | [receipt](../../../../../../../../../../UNAVAILABLE.md) | Candidate/config/optionalbranch freeze before fresh response |
| Raw h/z/reconstruction/residual | [cache](../../../../../../../../../../UNAVAILABLE.md) | BatchedFP32 arrays, separate old/natural/fresh/factor/question/enrichment |
| Each own frequency | `{ATTN_SAE,MLPIN_SAE,CC_CORRECTED}/shared/frequency` under execution owner | Same600documents/positions, own dictionary and thresholds |
| Each route raw outputs | `{site}/H1..H4/results` under execution owner | Individual predictions/tuning/coefficients/scalers and all controls; before_original separate |
| Raw native scores | [fresh](../../../../../../../../../../UNAVAILABLE.md) · [old](../../../../../../../../../../UNAVAILABLE.md) | Sum full sequence scores, candidate IDs/lengths and two-candidate probability |
| H4 blind text and merge maps | `{site}/H4/results/blind_texts.jsonl`, `H4/evidence/blind_merge_map.json` | Visible text separated before rule merge; v4 snapshots preserved |
| H4 content-enriched views | [48prefixes](../../../../../../../../../../UNAVAILABLE.md) | One visible position/doc; searchtag not truth; never frequency baseline |
| Source recovery | [receipt](../../../../../../../../../../UNAVAILABLE.md) |600/600sourceSHA matches; payload sourcefull kept execution-side |
| Independent checks | [numeric receipt](../../../../../../../../../../UNAVAILABLE.md) | Oldimmutability, token/IDjoin, frozen gates, ledger, savedprediction/model replay |
| Current code | [code_manifest](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/code_manifest.json) | Hashes of actual executed code; code remains execution-side |

Curated small tables in [tables](../../../../../../../../../../UNAVAILABLE.md) are generated copies; raw full activations/checkpoints are excluded from portable reading and ZIP. Requested full panels/per-item predictions/coefficient files/H4blind texts are included in discussionZIP when under20MB. Hash manifests identify all copies. No private memory, remote credentials, unrelated conversation histories or full natural source documents are bundled.
