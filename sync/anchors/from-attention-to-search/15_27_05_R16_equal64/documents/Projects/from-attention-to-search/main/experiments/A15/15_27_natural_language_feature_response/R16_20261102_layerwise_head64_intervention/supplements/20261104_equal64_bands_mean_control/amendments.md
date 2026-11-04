派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/amendments.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/amendments.md)；研究修改仍回到原件。

---

# Amendment E2: singleton-document batch arithmetic repair

Full replay found5documents with maxheadNLLdifference>0.05nat or a changedheadtop1: R11_A02_090/262/282/292/297. All5 are the-only documents with exactlyone target; the main175/700panel haszero headreplay error. Original102batch smoke used4targets/document and did not cover this shape.10of41272headcomparisonrows changedtop1, all auxiliary; maximumNLLdifference0.219782nat.

Under the existing routine implementation/numerical repair authorization, recompute all34conditions x28layers x2scopes for these5documents with one condition per batch, preserving native R16 batch2sequence shape. No condition or position is selected by scientific performance; no tolerance is widened. Old180chunks remain immutable. New5chunks are stored separately underanalysis/batch1_repair_chunks and used as versioned replacements for the sameUIDs only after exact replay/guard success. All other175chunks, including the entire mainpanel, remain unchanged.

Same original model/PCA/data/frozen contract and same authorized2RTX5090profile/image. No concurrent oldjob, training, newPCA or new scientific hypothesis. Original job/replay failure retained. A separate repair_freeze binds new runner code and document list; originalfreeze/protocol snapshots remain immutable. Canonical protocol links this amendment; output lineage explicitly records mixedbatch arithmetic and replacementpaths. Globalreplay checked again before delivery.
