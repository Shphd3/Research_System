派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R02_relation_binding/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R02_relation_binding/protocol.md)；研究修改仍回到原件。

---

# R02: minimal object–value binding check

State: APPROVED_FOR_BOUNDED_EXISTING_RESOURCE_CHECK under the current explicit Prompt2 design-and-execute instruction. Scientific acceptance Unknown. Freeze before model use. Owner A15_30; R01 bytes remain unchanged.

Question: can the query select the correct object–value relation when candidate values, frequency, order and token positions remain fixed across counterfactual worlds? Swap the two equal-token entity names, keep the query fixed, and verify the gold changes A→B. Constant candidate prior, nearest value and value word-bag rules cannot succeed in BOTH worlds. Copying the query-corresponding answer is allowed. This is controlled object–attribute selection, not general semantic understanding or multihop composition.

Use exactly six actual states: Dense/Baseline at3/15/17B valid pretraining targets, steps11446/57224/64854. Both tokens and steps match, no interpolation.24R01-exposed main families, six template clusters, two worlds, two gaps give96prefixes/state and576total. Six exposed engineering families give24smoke prefixes/model. No independent new-family confirmation is claimed. All cases survive regardless of score.

Prefix length1152; last-prefix/readout p1151; first answer position1152. Anchor e is the last token of the final listed valueB, so p-e-1=16/1024 with e1134/126. It is not necessarily the correct value in worldA. Separately save target-value gap/span, both value positions, relation-block span/length and absolute positions: target gaps16–24or1024–1032, block length10–16tokens. R01 used its sole correct value as anchor; endpoint meaning differs here. All entity names are1token and both candidates2tokens. Across worlds the token multiset, answer-value order/positions, query, total length and filler are invariant. Across near/far move the whole block while moving1008filler tokens from before to after; absolute position/competition remain confounded.

Reuse native strict models, FP32 throughout, TF32off, zero gradients/optimizer/parameter or bias updates. Sum complete leading-space word+period conditional log probabilities, retaining token/first/no-period/mean scores. Primary paired success needs both world-specific correct margins>0; ties fail. Report both margins, world preference change, within-family near/far differences and uncertainty. Equal candidate lengths remove that ranking confound, not lexical priors.

Greedy unrestricted argmax generation: at most8new tokens, stop on EOS151643 or first . newline ! ?. Score first lexical word after one optional initial the/a/an, case-insensitive exact candidate match; all other outputs OTHER. Never search later text to rescue the first answer. Retain all raw tokens/text/log probabilities/stops; report generation separately from candidate ranking.

While each model is loaded, rescore the96original R01near/far prefixes inFP32, candidates only (576auxiliary prefixes total). Save this precision bridge only inR02. It does not remove changed competitor/filler/target-gap confounds or modify original R01.

Statistics:24families,95%Wilson,10000paired family bootstrap with frozen seed, six-template cluster sensitivity. No seed-level uncertainty from family intervals. No80percent gate or result-based threshold change.

First check registry, size/fullSHA/counter/native strict-load/parameter count, then smoke both3Bmodels on24engineering prefixes each. Native shifted CE versus chain score and causal prefix hidden checks require<5e-4; parser known-good/bad fixtures must pass. Accuracy is never a smoke gate. Require<90%slice memory and projected full runtime<1800s. Sequential full6states capped1800s on existing H100MIG3g.40gb, no new job/resources/training. Preserve failures and stop on technical/budget issues; no task tuning.

Branches: near binding but weak far localizes this constructed distance condition; trajectory differences are not architectural causation; old success/new failure narrows the old reading without proving its strategy; weak near prioritizes task/prompt/implementation audit rather than a long-range deficit claim. All selected states precede22.018691584Bdata-order divergence, which still limits the older full-trajectory comparison. Unequal capacity and one trajectory/model remain.

Deliver definitions, assets, positions/labels, raw generation/scores, all families and uncertainty, examples, costs and omissions. Stop for the user's expansion decision. No new backbone/SAE/CrossCoder/router training, global-checkpoint sweep or feature analysis. Independent new families and Base-student knowledge-learning readiness are NOT RUN/not assessed here.
