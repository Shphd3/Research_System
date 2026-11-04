派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/detailed.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/detailed.md)；研究修改仍回到原件。

---

# Detailed behavior record

Purpose: with identical local question, test correct answer switching after a remote object fact changes. [Anchor](../../../../../../../../UNAVAILABLE.md), original[Protocol](protocol.md),[Summary](summary.md). Frozen Protocol body unchanged; all444prefixes retained. Eligibility: engineered/constructed-stimulus behavior with paired family statistics. Scientific acceptanceUnknown. No missing condition and no outcome-based exclusions.

## Actual procedure and why controls matter

Each record has a header, irrelevant weather/time sentences, exactly one target container fact, more of the same filler inventory, then a question without candidates. Split the filler into blocks so moving the fact yields exact gaps16/64/128while preserving320prefix length and the token multiset. Offset-derived evidence location uses whole item phrases, avoiding “cord” matching in “According”. A/B prefixes are identical outside the item. The output head separately scores every token of each hypothetical noun-phrase-plus-period completion. A score is a log probability, not an activation. Positive correct-minus-wrong margin means candidate ranking is correct; two positive margins are necessary for a paired success.

Neutral baseline replaces item identity withobject/small object and has no correctness label. Paraphrase restates the fact with a different grammatical order while leaving the family question; some near actual gaps are17/18because the item appears earlier in the fact. Other-container foil deliberately introduces the opposite candidate near the question at128and swaps it with target identity acrossA/B. Main/auxiliary inventories can differ, so mode contrasts are not pure wording interventions. No extra template round was attempted.

## Provenance, freezes and execution

Raw panel SHA256=77594e13a72d16b340c34a21d04328a8dab1e3aa8276fdc9f04713a81ac100da; family metadata SHA256=f7a88b3a1c99444d3b6ad345891591972c7fa9910039f492e49f59735d9c8e50. Model/tokenizer config and full weights SHA are in config.json. Full model hash verified before and after both stages. Tokenizer source/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json, no chat wrapping/special tokens. RuntimeTorch=2.3.0a0+6ddf5cf85e.nv24.04andTransformers4.53.3from mounted dependency directory. LocalCPU2threads,FP32,SDPA,physical2x328shape,zero gradients/optimizers. No cloudjob, no GPU allocation; job IDNOT_APPLICABLE. Smoke36prefixes took129.45s; heldout408took1580.19s. Fixed320target sampling throughout. Public full-forward token-score and prefix-only checks are in stage receipts; no precision tolerance changed.

Development construction failed once when substring “cord” matched inside “According”; repaired with whole-word regex before saved panel/freeze/forward. Old source retained in versions. Main data and scoring rules were unchanged after freeze. No Protocol amendment was needed during inference. Additional analysis implementation was hashed before heldout model start; statistical rules were already frozen inProtocol. Later report formatting is not response selection.

## Complete results and uncertainty

| actual gap | families | accuracy (prompts) | paired correct/24 | paired rate [95% Wilson] | mean correct margin [95% family CI],nat | point>=80% | evidence eligibility |
|---|---|---|---|---|---|---|---|
| 16 | 24 | 48/48 (100.0%) | 24 | 100.0% [86.2%,100.0%] | 6.0340 [5.2871,6.8575] | True | CLEARS_BOUNDED_BEHAVIOR_GATE |
| 64 | 24 | 48/48 (100.0%) | 24 | 100.0% [86.2%,100.0%] | 6.1722 [5.3768,7.0365] | True | CLEARS_BOUNDED_BEHAVIOR_GATE |
| 128 | 24 | 48/48 (100.0%) | 24 | 100.0% [86.2%,100.0%] | 6.4454 [5.6700,7.2753] | True | CLEARS_BOUNDED_BEHAVIOR_GATE |

| planned gap | actual range | paired correct/24 | correct prompts/48 | mean margin,nat |
|---|---|---|---|---|
| 16 | 16–18 | 23 | 47 | 5.4992 |
| 64 | 64–64 | 24 | 48 | 5.8085 |
| 128 | 128–128 | 24 | 48 | 6.1387 |

Foil128 paired17/24. Full repeated-family table: tables/family_pairs.csv,180pairs including84main/72paraphrase/24foil; baseline84rowsseparate. Token_scores.csvretains every candidate token. All24heldout main families appear in[families](families_cn.md). FamilyWilson binary intervals and paired bootstrap margins at10000replicatesseed20261104; template-cluster sensitivity resamples six whole template groups. Same-family distances remain paired in paired_distance_changes.csv; no distance-as-independent error bars or multiple-comparison significance claim. Means and every value survive negative outcomes.

## Evidence ledger and quality

Implementation/measurement audit: 4596checksPASS, recomputed with separate token/arithmetic implementation by the same agent; not independent human/scientific review. Every original text retokenized; prefix/candidate ID alignment, whole-item span,last evidence endpoint,p319,gap arithmetic,all token-score sums,invariance/leakage,split disjointness,pair success,margins,aggregate means andWilson interval recomputed. Frozen source/input hashes checked. Public model-forward numerical agreement is separately measured, not inferred from sum identities. Full output-head distribution was not saved; top10first-token IDs/logprobs plus complete candidate scoring were saved. No claim of rendered math verification; source check is separate.

Coverage: assets/definitions/data/smoke/all main distances/neutral baseline/paraphrases/nearest foil/full family data/figure/raw cases/scoring code/config allDONE_VALIDas execution artifacts. Representations/training/activation interventionsNOT_RUN_BY_PROTOCOL. Operational failure to meet a behavior gate does not make its measurements invalid. All scientific next decisions remain pending.

## Raw artifacts and continuation

/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/data/panel.jsonl full actual texts/IDs/offsets. /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/results/smoke.jsonl andheldout.jsonlraw scores. /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/results/casebook_all_cn.md every complete paired original. [Artifact index](artifacts.md) lists code/config/manifests/current receipts. Canonical source remains project-side; frozen execution copies are evidence, not competing editable Protocols. All further SAE activity requires discussion; STOP.
