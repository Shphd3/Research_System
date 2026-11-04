派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/provenance/aggregation_consistency_fix.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/provenance/aggregation_consistency_fix.md)；研究修改仍回到原件。

---

# 2026-10-28 numerical comparison correction

The observed cell mean was computed by nested pandas means, while null means used the exactly equivalent frozen sparse weighting operator. Final audit found two H2 cells differed from their graph-null 97.5th percentile by only 1.7347e-18 and 8.6736e-19 under those different floating-point reduction paths. Recomputing the *same saved observed values* through the same sparse operator used for every null draw gives exact equality, so neither strictly exceeds the graph-null envelope. The registered strict > comparison is unchanged; no tolerance, mask, seed, sample, outcome, threshold or draw count was changed. This is a postprocessing implementation correction, not an alternative scientific test. Pre-correction provisional verdict files are retained in pre_aggregation_consistency_fix/ and are INELIGIBLE. H1 qualifies 41 cells; final H2 count must come from the corrected table. Scientific judgment remains Unknown.
