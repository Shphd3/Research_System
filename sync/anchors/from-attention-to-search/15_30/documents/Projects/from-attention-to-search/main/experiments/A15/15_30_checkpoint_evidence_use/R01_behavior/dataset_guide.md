派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R01_behavior/dataset_guide.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R01_behavior/dataset_guide.md)；研究修改仍回到原件。

---

# Dataset and asset guide

The frozen panel contains480constructed English prefixes:96engineering and384main per native model state. Main analysis has24content families nested in6template strata,8families each for object, color and destination. Fact versions, distances and controls repeat within family; training-pattern exposure is unknown. Every record stores full text/token IDs/offsets, evidence character/token positions, last-prefix position, actual gap, candidates and filler inventory. See the Chinese companion for the same field meanings and the execution construction receipt for exact hashes.

Main prefix length1152, last-prefix position1151. Evidence-last positions1134/894/126 give exact gaps16/256/1024. The1408-prefix control at gap1024has evidence-last position382. All complete candidates have exactly2tokens: one lexical token and a period. Sum both conditional log probabilities; retain first-token/no-period/mean scores. First-token and no-period results must agree here. No multiword-candidate empirical result exists. All inputs fit2048context; no truncation.

Wrong-entity and no-evidence conditions have no gold label. Main distance comparisons preserve each family's token multiset and answer position; factual position and filler order change. Fixed-gap prefix extension adds filler as well as absolute position. These are controlled completion tasks, not arbitrary long-document comprehension.

Actual checkpoint inventory includes missing paths and equal-state-hash aliases.37unique states (14Dense,23Baseline) are frozen in execution audit/selected.json; match only real equal-token states. Existing Dense temporal CrossCoder binds1/5/15/31B, all8layers, while ordinary MoE SAE binds33B router input only. Dictionary training progress is separate from underlying model progress. Official28-layer Qwen and S7 dictionaries belong to other models. No dictionary is loaded here.

[Full tokenized panel](../../../../../../../../UNAVAILABLE.md) · [Construction](../../../../../../../../UNAVAILABLE.md) · [Actual checkpoints](../../../../../../../../UNAVAILABLE.md) · [Dictionary bindings](../../../../../../../../UNAVAILABLE.md).
