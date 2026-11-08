派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R02_relation_binding/assets_and_data.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R02_relation_binding/assets_and_data.md)；研究修改仍回到原件。

---

# Checkpoints, data and test infrastructure

All six requested states exist and were actually loaded. They match exactly in valid training target tokens and optimizer steps; there is no interpolation. The frozen selection file retains its pre-load status; fresh state-level receipts and the following manifest own the completed load status.

| Model | Actual tokens | Optimizer step | Actual state path / SHA256 |
|---|---|---|---|
| Baseline | 3000000000 | 11446 | `/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/runs/formal/milestones/token_003000000000/state.pt`<br>`70c8b3b7239c4bbd47e2498b26d1eed55c392155b5c8657f92d15947764d5fd7` |
| Baseline | 15000000000 | 57224 | `/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/runs/formal/milestones/token_015000000000/state.pt`<br>`99354d417a8657ed4d9d427e4a068026baa903489e6495cd8e27231e709e90e4` |
| Baseline | 17000000000 | 64854 | `/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/runs/formal/milestones/token_017000000000/state.pt`<br>`26e08b8795bd96e46bacc727ce448c830f7050ba5e285864d31a82400afd3b59` |
| Dense | 3000000000 | 11446 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/milestones/token_003000000000/state.pt`<br>`a2ae7f02bf3f8eabf217cc9f780b0c87b0ce0f103d7ecc7f4652f191c3e6ff1b` |
| Dense | 15000000000 | 57224 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/continuation_checkpoints/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/target_015000000000_actual_015000000000_step_00057224/state.pt`<br>`1956120a63a6cd555bd90eca7883413367611117f0f3574079d1d1159bdc2c4f` |
| Dense | 17000000000 | 64854 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/continuation_checkpoints/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/target_017000000000_actual_017000000000_step_00064854/state.pt`<br>`890925657c576192f07c18d14c03a539ca7e8d6a15e29fb56c41ca48cabb6cb3` |

The readable JSON [checkpoint manifest](../../../../../../../../UNAVAILABLE.md) links each raw output. The [infrastructure receipt](../../../../../../../../UNAVAILABLE.md) verifies actual saved scalar counters, config hashes and unchanged native model sources. Exact config paths remain there. [Current input access](../../../../../../../../UNAVAILABLE.md) is an access check, separate from full hashing/loading. All model tensors and the MoE load-bias buffer were frozen. No training optimizer was used.

Dense has 281,431,040 total and conventional active parameters. Ordinary MoE Baseline has 507,988,992 total and 281,496,576 conventional active parameters, eight experts with top-2 selection at each layer. Both are eight-layer, hidden-size 1024 native models with a 2048-token context. Close conventional active counts do not establish equal realized FLOPs. The source configs, historical AdamW/data settings and training provenance remain in [R01 training assets](../R01_behavior/training_assets.md); this round checks source hashes and six actual states, rather than rerunning historical training or sample-order audits. Each model has one seed-17 trajectory, with different capacity/hardware histories. Historical data order was verified aligned only through 22,018,691,584 tokens. All selected states are before this boundary, so the later order divergence does not directly explain these six-point observations; it still limits the original full-trajectory comparison.

## Replay of R01, not copying its summary

All 37 old raw-score files were freshly hashed and their paired counts recomputed: 14 Dense and 23 Baseline states, 14,208 prompts. A fresh stat/size check found the same 37 state files, but only the selected six weights are reloaded in R02. The [original inventory](../../../../../../../../UNAVAILABLE.md) and [original asset guide](../R01_behavior/training_assets.md) retain all missing paths/aliases, not replaced with fabricated states. [Replay receipt](../../../../../../../../UNAVAILABLE.md).

| Model | R01 gap | 60% first sampled | 80% first sampled | 90% first sampled |
|---|---|---|---|---|
| Dense | 16 | 3 B (20/24) | 3 B (20/24) | 5 B (23/24) |
| Dense | 1024 | 3 B (19/24) | 15 B (21/24) | 19 B (22/24) |
| Baseline | 16 | 3 B (24/24) | 3 B (24/24) | 3 B (24/24) |
| Baseline | 1024 | 3 B (23/24) | 3 B (23/24) | 3 B (23/24) |

These are unchanged descriptive cutoffs, not stable mastery or exact acquisition times. Dense's 80% first sampled crossing is 3 B near versus 15 B far; both Baseline crossings are 3 B. Later regressions, threshold sensitivity, small exposed families and precision limits remain. At R01 p=1151, the sole correct-value token ends at e=1134/894/126 for gaps 16/256/1024. The gap is p−e−1, not the difference to the next-answer index 1152.

## Frozen binding panel and token checks

The actual tokenizer is the R01 Qwen3 tokenizer, no BOS or chat template; tokenizer.json SHA256 c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539. The [construction receipt](../../../../../../../../UNAVAILABLE.md) records every label, tokenizer/offset and context guard. [Complete frozen texts and token positions](../../../../../../../../UNAVAILABLE.md), [family definitions](../../../../../../../../UNAVAILABLE.md).

There are 24 R01-exposed main families, six templates, two worlds and two anchor gaps: 96 main prefixes per state. Six additional R01-exposed engineering families give 24 smoke prefixes per model. No family is new independent confirmation. World A has box→key and bag→spoon; world B has bag→key and box→spoon. Both query box. Values have exactly the same count, order and token positions. Only the two entity tokens differ, and each entity is exactly one token in context. A deterministic relation parser verifies the answer flip; token/byte bags, non-entity prefix bytes and candidate lengths are checked without using model scores.

| World | Anchor gap | Value token positions | Correct value | Correct-value gap | Block tokens | Prefix last / first prediction |
|---|---|---|---|---|---|---|
| A | 16 | {'key': [1128], 'spoon': [1134]} | key | 22 | 12 | 1151 / 1152 |
| B | 16 | {'key': [1128], 'spoon': [1134]} | spoon | 16 | 12 | 1151 / 1152 |
| A | 1024 | {'key': [120], 'spoon': [126]} | key | 1030 | 12 | 1151 / 1152 |
| B | 1024 | {'key': [120], 'spoon': [126]} | spoon | 1024 | 12 | 1151 / 1152 |

Every prefix has 1152 tokens and each candidate is two tokens (leading-space word plus period); the value itself is one token. Relation blocks span 10–16 tokens. The anchor is the final listed value B, with gap 16/1024; the correct value's gap is separately 16–24/1024–1032. All absolute offsets, value and relation-block spans, block-end gaps, query and first prediction index are retained per row. Both main and smoke panels passed no-truncation checks, including eight generated tokens within the 2048 context. Moving the entire block transfers 1008 filler tokens from before to after it. Total length, query, answer position and token multiset match, while absolute evidence location and attention competition remain confounded.

Nearest-value, word-frequency and fixed-candidate strategies give the same answer in the two worlds and therefore cannot pass both; this is a construct check, not a claim about the model's internal algorithm. The query entity is fixed within a family, so query role and lexical entity preference are not fully crossed. No new independent paraphrase/multihop/low-exposure panel was run.

## Scoring, generation and complete outputs

FP32 full-candidate summed conditional log probabilities are primary; ties fail. The first lexical token, no-period and length-mean variants are saved; all candidates have equal length, so averaging preserves their ranking. Greedy generation is unrestricted-vocabulary, capped at eight tokens, stopping at EOS or the first sentence mark; score only the first lexical answer word after at most one leading article. Every OTHER output is retained. An article-first generation follows a different conditional path from the word-first candidates, so candidate and generation rates are distinct.

Each of six [raw files](../../../../../../../../UNAVAILABLE.md) retains 96 binding records and 96 FP32 R01 reference records, plus a fresh state receipt. The [family table](../../../../../../../../UNAVAILABLE.md) has 288 model×progress×family×gap rows, preserving each world's correct margin, delta, candidates and generation behavior. [Sample records](../../../../../../../../UNAVAILABLE.md), [summary](../../../../../../../../UNAVAILABLE.md), [template/type](../../../../../../../../UNAVAILABLE.md), [paired near/far](../../../../../../../../UNAVAILABLE.md), [same-precision old/new](../../../../../../../../UNAVAILABLE.md), [two-trajectory differences](../../../../../../../../UNAVAILABLE.md). All stats use family pairing; template-cluster sensitivity is separate, neither is training-seed uncertainty.

Access IDs: checkpoint_family_relation_binding_3_15_17b_20261105; dataset_relation_binding_swap_r02_20261105; tokenizer_qwen3_0p6b_base; analysis_relation_binding_r02_20261105. [Reproduction](reproduce.md) and [artifact manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R02_relation_binding/artifact_manifest.json) identify source versions. Raw data and weights stay execution-side; only the measured PNG and small figure table are selected Git payloads.
