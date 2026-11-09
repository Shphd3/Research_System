# Summary: A17_02_E01 Fixed-Pool Frequency

[中文](summary_cn.md) · [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_02_fixed_pool_frequency/17_02_fixed_pool_frequency_anchor.md) · [Protocol](protocol.md) · [Detailed](detailed.md)

The frozen confirmation meets `REGISTERED_POSITIVE_MEDIAN_INTERACTION`: median **0.066142 nat/answer**, all six seed effects above δ=0.01. Extra same-rule practice improves B answer CE more than extra different-rule practice. Different-rule additions still improve CE relative to B-only. This is a completed policy experiment; mechanism and question-closure judgment remain researcher-owned `Unknown`.

`task_state=FULL_COMPLETED`; `result_state=MEASURED_STATISTICAL_BRANCH`; `design_state=USER_ADOPTED_FROZEN_IMPLEMENTATION`; `question_state=HUMAN_CONFIRMED` (no closure transition).

## 1. Purpose

At fixed B200, test whether increasing presentations of the same A pool from 200 to 800 changes held-out B answer loss differently under the same visible rule versus the other visible rule. FIRST selects the first item; LAST selects the last. Rule relation changes the instruction and correct selection operation. Vocabulary, list-generation process, answer marginals, prompt template and recipient B opportunities remain matched. Frequency means repeated presentations, not unique-content growth.

## 2. Hypothesis

The registered target is a practically nonzero median rule×presentation interaction across independent training seeds, with two-sided δ=0.01 nat/answer. A rival predicts an effect within ±δ, for example because extra practice mostly teaches reusable list/vocabulary handling. Both visible rules are simultaneously satisfiable. Positive interaction can reflect less help and does not establish net interference.

## 3. Analysis Method

Reset original Qwen3-0.6B Base for every trajectory. Update only layer27 Attention `o_proj` [1024,2048]; AdamW constant LR1e-4; micro5×accum4 gives20 supervised answer tokens/update; full-vocabulary answer-only CE. All other parameters are frozen. A and B each contain200 unique ordered lists, with disjoint content groups and exact20-word position/answer balance.

For each B rule, run same/different A200/800 with B200, B-only, and same/different A500/B500. Three exploratory seeds use dev; six new confirmation seeds use an unopened model test after the conditions and code were frozen. Order-new tests untrained permutations of actually trained B groups; combination-new tests untrained content groups. Average these panels and B roles equally within each seed; independent n=6, not24 cells or800 rows. Confirmation requires all six combined effects beyond the same threshold side; component panels cannot rescue the primary.

Smoke pt-cgmiw5f3 passed56/56 engineering checks and independent-process restart. Full pt-ho4byzg4 completed126 trajectories,90,000 trained answers and4500 updates; exploration508/508 and confirmation1012/1012 engineering checks passed. Actual-exposure novelty qualification passed126/126. Platform reached SUCCEEDED at2026-10-09 17:48:33 UTC (2026-10-10 01:48:33 Asia/Shanghai). All126 actually saved checkpoint families were independently SHA-verified and registered. [Evidence](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/terminal_verification.json).

## 4. Conclusion

Confirmation mean I=0.066663; median I=0.066142; conservative seed-median interval [0.051485,0.078583], coverage at least96.875% under independent identically generated seed effects. All six I>0.01 meet the frozen two-sided sign rule, p=0.03125. Every FIRST/LAST×novelty component also remains positive descriptively; its data are retained in Detailed.

All24 seed×B-rule×panel cells for each of four added-practice policies have CE below B-only. Combined median CE is0.798928 for B-only,0.582623 for same A800/B200 and0.667780 for different A800/B200. Thus this run shows stronger same-rule incremental CE benefit and positive different-rule net CE benefit. Accuracy is distinct: corresponding median accuracies are83.4375%,89.1250%,83.2500%; CE improvement does not guarantee more correct answers.

At the equal1000-answer budget, A800/B200 has higher combined CE than A500/B500 in both relations (median seed differences +0.008747 same,+0.040762 different). This compares allocation while changing B opportunities. It is not the fixed-B primary or a pure-frequency mechanism proof.

The result is conditional on one pretrained Base, these pools, final-matrix capacity and optimizer. It does not establish from-scratch acquisition, a causal functional partition, natural-corpus mechanisms, net interference, or expert utility. SAE endpoint description is a separate analysis using all36 prespecified contrasts; actual SAE analysis is still NOT_RUN and cannot rewrite this result. [Raw Full](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z) · [Confirmation](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/analysis_confirmation.json) · [Engineering](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/engineering_audit_confirmation.json) · [Terminal](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/terminal_verification.json) · [Platform](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/platform_terminal.json) · [Actual asset registration](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/asset_registration_request_registered_outputs.json)


### Completed SAE endpoint description (dev only)

The fixed36 matched-SAE endpoint pairs also completed and passed all native/array/freeze guards in `pt-h6ke4emg`. Across all9 seeds, the equal-combined dev interaction mean was0.082567 nat/answer: SAE-decoder linear0.001942, explicit residual linear0.022863, finite remainder0.057762. This is a dev endpoint account, separate from the six-seed test confirmation above. It does not establish a complete mechanism: the frozen SAE has substantial list-task reconstruction residual, and the finite remainder is essential. All actual outputs are registered as `analysis_a17_frequency_sae_actual1b_36pairs_20261009t2118z`; [the Detailed appendix](detailed.md#appendix-completed-matched-sae-endpoint-description-2026-10-10-asiashanghai) owns separate order-new/combination-new values, source lineage and boundaries. Human mechanism judgment remains Unknown.

Status clarification (2026-10-10 Asia/Shanghai): “SAE analysis is still NOT_RUN” in the preserved original Full-report body describes its status when that training report was written. The current status is completed and registered for all36 endpoint pairs, as recorded in the completed-SAE appendix above. The original six-seed test confirmation and its scientific boundary are unchanged.
