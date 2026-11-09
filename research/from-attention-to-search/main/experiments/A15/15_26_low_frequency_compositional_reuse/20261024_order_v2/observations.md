# Order V2 and symbolic auxiliary: observations

[中文](observations_cn.md) · [Summary](summary.md) · [Detailed evidence](detailed.md)

Final acceptance at `2026-10-25 01:02:30 Beijing time (UTC+8)`: the finite execution protocol is **COMPLETE**. Actual execution contains14 scientific training trajectories and148 scientific saved states. The129-row status ledger contains the original117 planned rows plus12 expanded-version registrations:14 actual trajectories and115 not-applicable or superseded rows. It does not represent117 executed trajectories.

Stage states are `NEGATIVE_RESULT` for S1/S2, `NOT_APPLICABLE` for the S3–S6 main contrasts and symbolic main comparisons, and `COMPLETE` for audit. Final acceptance binds21 hashed evidence records. All52 actual output assets pass strict access, covering152 checkpoint paths,4 caches and32 derived-analysis groups without handoff gaps. All5 jobs are platform `SUCCEEDED`, with no active jobs. Sources:[final audit](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/final_audit_receipt.json),[run/stage manifest](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/result_manifest.json),[final asset handoff](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/final_registration_handoff.json). Execution completion is separate from scientific closure: question OPEN, researcher judgment Unknown.

Read through three paths: A, the hypothesis and intervention; B, observed outcomes and controls; C, alternatives still unresolved. AI cause judgments are in the[separate round interpretation](ai_interpretation_cn.md). The scientific question is OPEN and researcher judgment is Unknown.

## S1: multiplication qualification

**A Hypothesis and intervention.** The component-trained parent should reach95% on held-out validation. Three fine-tuning seeds share one pretrained Qwen3-0.6B Base origin. The initial range is the last attention Q/K/V/O projections; each task family consumed its one permitted expansion to last attention plus FFN, retaining3000 updates, rate and batch.

**B Observations and controls.** S1 predicts unit-price times quantity. S2a discounts a supplied true base amount; S2b compares the threshold; S2c adds an explicitly charged fee; S2d combines comparison and addition. S1 has240/360 VAL/TEST items; each S2 task has256/512. Registered eligibility uses VAL; TEST cannot retroactively change it.

| Seed | Component | VAL exact accuracy | TEST exact accuracy |
| --- | --- | --- | --- |
| 29 | S1 | 92.50% | 96.94% |
| 29 | S2a | 38.28% | 41.41% |
| 29 | S2b | 100.00% | 99.61% |
| 29 | S2c | 96.88% | 97.46% |
| 29 | S2d | 96.48% | 96.29% |
| 43 | S1 | 93.33% | 95.28% |
| 43 | S2a | 41.80% | 41.80% |
| 43 | S2b | 100.00% | 99.61% |
| 43 | S2c | 96.88% | 97.66% |
| 43 | S2d | 94.14% | 94.92% |
| 71 | S1 | 92.92% | 95.28% |
| 71 | S2a | 46.88% | 45.90% |
| 71 | S2b | 96.48% | 98.83% |
| 71 | S2c | 98.05% | 98.83% |
| 71 | S2d | 96.48% | 97.27% |

**C Unresolved alternatives.** Separate initial formatting from arithmetic using a diagnostic first-line unique amount, parsed without consulting the target. This never replaces the strict main score.

| Task | N VAL | Base strict main | Base first-line content diagnostic | Seed29 P strict main |
| --- | --- | --- | --- | --- |
| S1 | 240 | 0.00% | 92.50% | 92.50% |
| S2a | 256 | 0.00% | 22.66% | 38.28% |

Base S1 diagnostic content accuracy and seed29 trained strict accuracy are both92.50%, so the increase from zero strict Base score contains format adaptation. Trained S2a remains far below95%; numerical error requires separate analysis.

## S2: discount, comparison and addition

**A Hypothesis and intervention.** Every component must individually reach95%. **B Observations and controls.** The table above preserves all components. S2a still makes monetary errors when supplied the true base amount.

At the seed29 parent fixed 3000-update endpoint, the real TEST input is **商品基础金额609.00元，保留原价的95%。请只回答折后商品金额，保留两位小数。**. The target is `578.55` and the model generates `558.55`. `other_numeric_error` is the modal error category (297 items); this is its lowest-data_id representative. Its fractional cents are correct while the whole-yuan part is wrong, so formatting alone does not account for this error. The example illustrates the error pattern; the distribution is in the tables and per-item predictions.

**C Unresolved alternatives.** Discount, fractional-cents, whole-yuan and magnitude strata are post-hoc error descriptions, not an identified internal arithmetic module. Full stratification is in[Detailed](detailed.md) and the[error table](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/tables/error_causes.csv).

## S3: component-training help

**A Hypothesis and intervention.** The registered transfer contrast is P versus untouched B and field-copy C under identical downstream J learning. J updates original parent parameters and a zero-output-initialized bottleneck branch. **B Observations and controls.** Completed seeds miss the all-components premise, activating only one P-J joint-feasibility trajectory. The P/B/C contrast is NOT_APPLICABLE. Fixed2000-update TEST is:

| Seed | BASE | DISCOUNT | SHIPPING | BOTH | Four-family macro |
| --- | --- | --- | --- | --- | --- |
| 29 | 93.61% | 21.48% | 40.23% | 8.98% | 41.08% |
| 43 | 94.72% | 19.92% | 39.06% | 8.01% | 40.43% |
| 71 | 95.00% | 19.92% | 37.11% | 5.66% | 39.42% |

**C Unresolved alternatives.** This is joint feasibility from an unqualified parent, not an estimate of component-pretraining help. Format familiarity, arithmetic skill and new learning remain entangled.

## S4: slower parent updates

**A Hypothesis and intervention.** Matched J/S/F respectively normally update, slowly update and freeze parent weights, with U/G controls. **B Observations and controls.** These arms depend on a qualified parent and are NOT_APPLICABLE for the adjudicated seeds. **C Unresolved alternatives.** Qualification failure does not test slow-update utility; the observed chain remains true-base discount error followed by low complete-order feasibility. Adapter scaling uses the postprocessing record. For J, scale0 disables only the added branch while retaining updated J-parent weights; it does not return to the original P parent. Accuracy is unchanged across scales on the fixed98 mixed items(43/98,45/98,45/98 by seed); equal accuracy is not a claim of no computational branch effect.

## S5: paired exposure frequency

**A Hypothesis and intervention.** Exchange high/low8:1 discount-threshold exposure while fixing marginals. **B Observations and controls.** Scientific frequency trajectories were not run under the prerequisite gate; they are NOT_APPLICABLE. CPU balancing is implementation evidence. **C Unresolved alternatives.** No frequency manipulation occurred in these failures.

## S6: branches and selection

**A Hypothesis and intervention.** Shared/private capacity lines separate total parameters from active computation, followed by fixed-branch routing controls. **B Observations and controls.** The premise fails, leaving branch/router comparisons NOT_APPLICABLE. **C Unresolved alternatives.** No expert-utility or routing-failure contrast exists; both candidates completed DIAG screening for all seeds and no internal-reuse candidate qualified; all results are UNKNOWN and no selected TEST confirmation occurred. No expert or prototype router was trained.

## Symbolic auxiliary: same mapping, different wording

| Seed | TRAIN wording (256 mappings) | VAL wording (256) | TEST wording (256) | Two native calls (96) | True-intermediate (96) |
| --- | --- | --- | --- | --- | --- |
| 29 | 100.00% | 16.41% | 6.25% | 100.00% | 100.00% |
| 43 | 100.00% | 20.70% | 6.25% | 100.00% | 100.00% |
| 71 | 100.00% | 15.63% | 7.03% | 100.00% | 100.00% |


| Seed | Wording split | N | Format valid | Valid but mapping wrong | Correct |
| --- | --- | --- | --- | --- | --- |
| 29 | val | 256 | 224 | 182 | 42 |
| 29 | test | 256 | 169 | 153 | 16 |
| 43 | val | 256 | 228 | 175 | 53 |
| 43 | test | 256 | 181 | 165 | 16 |
| 71 | val | 256 | 213 | 173 | 40 |
| 71 | test | 256 | 190 | 172 | 18 |

The 8×32 atomic mappings are identical across TRAIN/VAL/TEST; wording uses templates 0/1/2. Each seed obtains 256/256 on the original training wording and 96/96 for two native calls and the true-intermediate control. Given complete lookup correctness and symbol closure, chaining 100% is expected implementation calibration; external composition was already defined as G(F(x)). This is a cross-context behavioral difference. Extra calls/information are diagnostic advantages; single-pass internal reuse remains Unknown. Symbol and order scores are not pooled. Source:[symbolic diagnostic records](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/diagnostics/symbolic/summary.json).

## Matched intermediate-value readouts

| Run | BOTH | S1 | S2a (true b) | S2b (true s) | S2c (true s) | S2d (true s) | BOTH + true b |
| --- | --- | --- | --- | --- | --- | --- | --- |
| order_seed29_P_J_balanced_replay_v2-expanded | 4.17% | 100.00% | 77.08% | 97.92% | 100.00% | 85.42% | 10.42% |
| order_seed43_P_J_balanced_replay_v2-expanded | 10.42% | 100.00% | 75.00% | 100.00% | 97.92% | 89.58% | 6.25% |
| order_seed71_P_J_balanced_replay_v2-expanded | 10.42% | 100.00% | 77.08% | 100.00% | 97.92% | 89.58% | 12.50% |

The same 48 frozen TEST orders are paired. True intermediates add information and change the prompt; these are behavioral controls and internal mediation remains Unknown.

The matched behavior recurs at the three P-J endpoints: seed29/43/71 have29/27/30of all48frozen TEST orders with all five atomic answers correct and the complete BOTH answer wrong. Each denominator remains all48; component successes are not selected as a new qualified population. Atomic-answer conjunction and single-pass combination success differ here; the original component-parent P qualification remains failed.

| Seed | Fixed total N | All atomic correct/BOTH correct | All atomic correct/BOTH wrong | Atomic not all correct/BOTH correct | Atomic not all correct/BOTH wrong |
| --- | --- | --- | --- | --- | --- |
| 29 | 48 | 2 | 29 | 0 | 17 |
| 43 | 48 | 4 | 27 | 1 | 16 |
| 71 | 48 | 4 | 30 | 1 | 13 |

For seed29, the modal cell is(True, False). Its lowest stable recipient ID gives: 商品单价82.00元，购买3件。商品金额乘以80%，即保留原价的80%。按折后商品金额判断，达到100.00元包邮，否则加10.00元运费。运费不参与折扣。请只回答最终支付金额，保留两位小数。 Target`196.80`, BOTH output`319.60`. All five independent atomic answers are correct=True. Selection uses modal cell and stable ID, not whether a true intermediate happens to rescue this example. Source:[all48 paired rows](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed29_P_J_balanced_replay_v2-expanded/diagnostics/matched_components/complete.json).

| P-J run | Fixed N | S1 TRAIN seen | S2a TRAIN seen | S2b TRAIN seen | S2c TRAIN seen | S2d TRAIN seen |
| --- | --- | --- | --- | --- | --- | --- |
| order_seed29_P_J_balanced_replay_v2-expanded | 48 | 0 | 21 | 4 | 3 | 1 |
| order_seed43_P_J_balanced_replay_v2-expanded | 48 | 0 | 21 | 4 | 3 | 1 |
| order_seed71_P_J_balanced_replay_v2-expanded | 48 | 0 | 21 | 4 | 3 | 1 |

Global qualification uses component-parent P on VAL; the 48-case readout uses the later P-J fixed endpoint and cannot repair P eligibility. Exact atomic TRAIN-tuple overlap is below, especially S2a: 21/48; the atomic inputs are not all unseen. Giving true b adds information and changes prompting. S2d with true s additionally removes multiplication and discount computation, so information, wording and computation depth change together.

## Evidence scope

The 512 BOTH TEST questions contain32 independent(p,q) families. Never charging shipping achieves481/512=93.945%; only 31 questions charge shipping. Report aggregate, charged and enriched-boundary results separately. Three fine-tuned parents do not yield a precise population distribution. Detailed preserves per-item sources, original negative endpoints, actual counts and final audits.
