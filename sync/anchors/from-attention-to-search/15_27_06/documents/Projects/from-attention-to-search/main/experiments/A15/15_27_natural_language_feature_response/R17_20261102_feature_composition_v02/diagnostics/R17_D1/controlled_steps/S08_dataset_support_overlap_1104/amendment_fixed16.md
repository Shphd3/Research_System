派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/amendment_fixed16.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/amendment_fixed16.md)；研究修改仍回到原件。

---

# Pre-inference amendment: fixed16 context

2026-11-04T01:10:21.489566+00:00

Full-question-length matching leaves only11 Magicoder/GSM8K documents per group. Add equal16-token causal-prefix secondary control for all257 documents before reading any activation. This controls observed context length, not full source-question length or lexical content.

Original protocol, frozen plan and panel remain unchanged. Add position15 as cache axis9, after the original eight main positions and fixed32 axis8. No new model forward is required. Report this secondary comparison separately; it cannot rescue a primary failure. Use the original document-level bootstrap/permutation and pair rule.
