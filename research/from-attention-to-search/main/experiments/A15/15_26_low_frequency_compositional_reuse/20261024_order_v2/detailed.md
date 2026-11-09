# Detailed: A15_26 Order V2 and symbolic auxiliary

> **Storage update, 2026-10-31:** At the researcher's request, the entire Order MoE V2 execution directory (models, optimizer states, caches, data and runtime source) was deleted. These historical results/interpretations remain unchanged, but the deleted payloads cannot be loaded or resumed. This cleanup does not close the scientific question. [Deletion receipt](/data/250010109/MoE_Router/storage_cleanup_receipts/20261031T033809Z_decommon_academic_order/completion.json).


[中文](detailed_cn.md) · [Summary](summary.md) · [Observations](observations.md) · [Protocol](protocol.md)

## Current bounded result

Final acceptance at `2026-10-25 01:02:30 Beijing time (UTC+8)`: the finite execution protocol is **COMPLETE**. Actual execution contains14 scientific training trajectories and148 scientific saved states. The129-row status ledger contains the original117 planned rows plus12 expanded-version registrations:14 actual trajectories and115 not-applicable or superseded rows. It does not represent117 executed trajectories.

Stage states are `NEGATIVE_RESULT` for S1/S2, `NOT_APPLICABLE` for the S3–S6 main contrasts and symbolic main comparisons, and `COMPLETE` for audit. Final acceptance binds21 hashed evidence records. All52 actual output assets pass strict access, covering152 checkpoint paths,4 caches and32 derived-analysis groups without handoff gaps. All5 jobs are platform `SUCCEEDED`, with no active jobs. Sources:[final audit](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/final_audit_receipt.json),[run/stage manifest](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/result_manifest.json),[final asset handoff](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/final_registration_handoff.json). Execution completion is separate from scientific closure: question OPEN, researcher judgment Unknown.

Completed parents miss the all-components VAL rule. P-J therefore serves only the permitted joint-feasibility contingency; the S3–S6 main contrasts have no identified result. Symbolic original-wording lookup and two-call controls succeed while other-wording atomic behavior falls. This record separates observations, derived quantities and eligibility. The question is OPEN; researcher mechanism judgment isUnknown. AI interpretation is separately owned.

## Actual model, task and measurement

Qwen3-0.6B Base has 28 layers and width 1024; the final layer index is 27. Initially only its attention Q/K/V/O projections update; the sole scientific revision adds that layer's feed-forward network(FFN). This is a candidate update range, not a located shared function. P is the component-trained parent, B the untouched Base, and order C a field-copy parent; prerequisite failure prevents the B/C downstream contrasts.

All amounts are integer cents: base b=unit-price p times quantity q; discounted subtotal s=b*d/100, with d the retained-price percent. Shipping is free at or above threshold T; otherwise add fee f, without discounting the fee. BASE outputs b, DISCOUNT s, SHIPPING tests the undiscounted amount, and BOTH discounts before thresholding. Atomic prompts supply the relevant component inputs; main complete orders supply no true b/s.

Native deterministic generation uses temperature 0, max 16 new tokens and unrestricted vocabulary. Strict accuracy accepts a single exact two-decimal amount or the exact Chinese threshold category. CE is correct answer-token+EOS negative log probability per valid token; per-answer NLL and length are separate saved fields. The[loader](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/source/order_model.py) and[frozen trainer](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/source_freezes/initial/source/train.py) expose masks, AdamW and restore semantics.

Three fine-tuning parents share a pretrained origin and vary training order. Numerical(p,q) or canonical atomic tuples are case units; rewrites do not add independent cases. The first-line diagnostic requires one unique amount and rejects a second numeric span; it never changes strict scoring.

## Freeze, conformance and amendments

Scientific-body hash `50517762ebf4be79d5f029f4e0234930ef529b72a7ffae1f30fa91f54cc2ddf3`, frozen`2026-10-24T15:59:10.536987+00:00`. Original negatives remain intact. Each family uses at most one scientific expansion chosen onTRAIN/VAL. ZIP, snapshots, runtime identities and job receipts are preserved in the historical provenance and[revision ledger](revisions.md).

| Registered item | Actual | Evidence/eligibility |
| --- | --- | --- |
| Scientific body | Frozen15:59:10Z; later provenance does not change its registered hash | [snapshot](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/protocol_frozen.md) |
| Update range | QKVO initially; one attention+FFN expansion per family; steps/rates fixed | [order lock](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/configs/order_qualification_lock.json); [symbol lock](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/configs/symbolic_qualification_lock.json) |
| Budgets | 3000 parent/2000 child updates; globalbatch32; FP32; TF32 off | Actual per-trajectory counters below |
| Supervision | Answer+EOS; no true intermediate in main task;10% replay | Prompt/padding ignored;0.9 new-token mean+0.1 old-token mean |
| Eligibility | Each atomic VAL≥95%; failure allows only P-J feasibility | No executed P/B/C, U/S/F/G, frequency, expert or router main contrasts |
| Independent support | BASE/S1 TRAIN1680,VAL240,DIAG120,TEST360 | Finite support reduction recorded; BOTH512/32pq |
| Post-hoc readouts | First-line amount; S2a digit/discount strata;48 true-b/s controls | Strict score/threshold unchanged; VAL motivation and information/wording confounds explicit |

## Atomic fixed endpoints: accuracy and CE

S1 VAL/TEST N=240/360; each S2 N=256/512. Eligibility uses VAL and is not retroactively changed by higher TEST scores.

| Seed | Component | VAL accuracy | TEST accuracy | VAL CE/token | TEST CE/token |
| --- | --- | --- | --- | --- | --- |
| 29 | S1 | 92.50% | 96.94% | 0.04515 | 0.01842 |
| 29 | S2a | 38.28% | 41.41% | 0.51855 | 0.51199 |
| 29 | S2b | 100.00% | 99.61% | 0.00215 | 0.00323 |
| 29 | S2c | 96.88% | 97.46% | 0.01323 | 0.01053 |
| 29 | S2d | 96.48% | 96.29% | 0.01493 | 0.01975 |
| 43 | S1 | 93.33% | 95.28% | 0.03426 | 0.02624 |
| 43 | S2a | 41.80% | 41.80% | 0.49895 | 0.53215 |
| 43 | S2b | 100.00% | 99.61% | 0.00075 | 0.00188 |
| 43 | S2c | 96.88% | 97.66% | 0.01069 | 0.00959 |
| 43 | S2d | 94.14% | 94.92% | 0.01524 | 0.01902 |
| 71 | S1 | 92.92% | 95.28% | 0.05681 | 0.02440 |
| 71 | S2a | 46.88% | 45.90% | 0.44959 | 0.48558 |
| 71 | S2b | 96.48% | 98.83% | 0.02112 | 0.01035 |
| 71 | S2c | 98.05% | 98.83% | 0.00917 | 0.00534 |
| 71 | S2d | 96.48% | 97.27% | 0.01340 | 0.01270 |

| Atomic task | VAL seed mean | VAL range | TEST seed mean | TEST range |
| --- | --- | --- | --- | --- |
| S1 | 92.92% | 92.50%–93.33% | 95.83% | 95.28%–96.94% |
| S2a | 42.32% | 38.28%–46.88% | 43.03% | 41.41%–45.90% |
| S2b | 98.83% | 96.48%–100.00% | 99.35% | 98.83%–99.61% |
| S2c | 97.27% | 96.88%–98.05% | 97.98% | 97.46%–98.83% |
| S2d | 95.70% | 94.14%–96.48% | 96.16% | 94.92%–97.27% |

Ranges describe the three actual fine-tuned parents and are not population confidence intervals.
### S2a discount strata

| Seed | Split | Discount % | N | Correct | Exact accuracy |
| --- | --- | --- | --- | --- | --- |
| 29 | val | 80 | 61 | 43 | 70.49% |
| 29 | val | 85 | 63 | 9 | 14.29% |
| 29 | val | 90 | 64 | 38 | 59.38% |
| 29 | val | 95 | 68 | 8 | 11.76% |
| 29 | test | 80 | 117 | 78 | 66.67% |
| 29 | test | 85 | 122 | 26 | 21.31% |
| 29 | test | 90 | 126 | 84 | 66.67% |
| 29 | test | 95 | 147 | 24 | 16.33% |
| 43 | val | 80 | 61 | 46 | 75.41% |
| 43 | val | 85 | 63 | 13 | 20.63% |
| 43 | val | 90 | 64 | 37 | 57.81% |
| 43 | val | 95 | 68 | 11 | 16.18% |
| 43 | test | 80 | 117 | 83 | 70.94% |
| 43 | test | 85 | 122 | 24 | 19.67% |
| 43 | test | 90 | 126 | 83 | 65.87% |
| 43 | test | 95 | 147 | 24 | 16.33% |
| 71 | val | 80 | 61 | 46 | 75.41% |
| 71 | val | 85 | 63 | 14 | 22.22% |
| 71 | val | 90 | 64 | 44 | 68.75% |
| 71 | val | 95 | 68 | 16 | 23.53% |
| 71 | test | 80 | 117 | 91 | 77.78% |
| 71 | test | 85 | 122 | 26 | 21.31% |
| 71 | test | 90 | 126 | 93 | 73.81% |
| 71 | test | 95 | 147 | 25 | 17.01% |

| Seed | Split | Discount group | Full N | Main accuracy/all N | Strict parse N | Fractional cents correct | Whole yuan correct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 29 | val | 80/90 | 125 | 64.80% | 125 | 94.40% | 65.60% |
| 29 | val | 85/95 | 131 | 12.98% | 131 | 61.83% | 16.03% |
| 29 | test | 80/90 | 243 | 66.67% | 243 | 96.30% | 66.67% |
| 29 | test | 85/95 | 269 | 18.59% | 267 | 63.67% | 20.22% |
| 43 | val | 80/90 | 125 | 66.40% | 125 | 95.20% | 66.40% |
| 43 | val | 85/95 | 131 | 18.32% | 131 | 62.60% | 21.37% |
| 43 | test | 80/90 | 243 | 68.31% | 243 | 95.88% | 68.31% |
| 43 | test | 85/95 | 269 | 17.84% | 267 | 63.67% | 20.97% |
| 71 | val | 80/90 | 125 | 72.00% | 125 | 95.20% | 72.00% |
| 71 | val | 85/95 | 131 | 22.90% | 131 | 65.65% | 26.72% |
| 71 | test | 80/90 | 243 | 75.72% | 243 | 95.06% | 75.72% |
| 71 | test | 85/95 | 269 | 18.96% | 268 | 64.55% | 20.90% |

Fractional-cents correctness compares predicted/target cents modulo100; whole-yuan correctness compares integer division by100. Strictly parsed denominators,80/90 versus85/95 strata, absolute error, input-copy and dropped-fraction signatures are in the[error CSV](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/tables/error_causes.csv). These post-hoc descriptions locate error conditions without identifying their cause.

At the seed29 parent fixed 3000-update endpoint, the real TEST input is **商品基础金额609.00元，保留原价的95%。请只回答折后商品金额，保留两位小数。**. The target is `578.55` and the model generates `558.55`. `other_numeric_error` is the modal error category (297 items); this is its lowest-data_id representative. Its fractional cents are correct while the whole-yuan part is wrong, so formatting alone does not account for this error. The example illustrates the error pattern; the distribution is in the tables and per-item predictions.

## Original Base: format and monetary content

| Task | N VAL | Base strict main | Base first-line content diagnostic | Seed29 P strict main |
| --- | --- | --- | --- | --- |
| S1 | 240 | 0.00% | 92.50% | 92.50% |
| S2a | 256 | 0.00% | 22.66% | 38.28% |

Base S1 has zero strict accuracy and 92.50% first-line content accuracy; trained seed29 strict S1 is also 92.50%. The strict score therefore includes format adaptation. S2a still has numerical errors when true b is supplied; formatting cannot account for every failed prerequisite. Different score definitions are not directly called arithmetic gains.

## P-J complete orders: joint feasibility only

| Seed | BASE | DISCOUNT | SHIPPING | BOTH | Four-family macro |
| --- | --- | --- | --- | --- | --- |
| 29 | 93.61% | 21.48% | 40.23% | 8.98% | 41.08% |
| 43 | 94.72% | 19.92% | 39.06% | 8.01% | 40.43% |
| 71 | 95.00% | 19.92% | 37.11% | 5.66% | 39.42% |

Macros weight the four complete families equally. P/B/C transfer, normal/slow/frozen updates, exposure exchange, shared/private branches and selector utility depend on the failed premise. No method-effect contrast is estimated;NOT_APPLICABLE is not hypothesis rejection.

## Symbolic auxiliary and native-call controls

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

There are 8 permutations with32 atomic inputs each. Atomic TRAIN/VAL/TEST retain the same mapping and change wording. Each composition pair has20/6/6 train/VAL/TEST inputs, so composition TEST N=96. Original-wording256/256 lookup and 96/96 two-call controls calibrate that prompting/call implementation. Under complete lookup correctness and symbol closure,100% chaining is expected; external composability was already defined and CPU-checked. Other-wording failure preserves a context-expression rival; external chaining does not identify a single-pass internal carrier.[Diagnostic source](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/diagnostics/symbolic/summary.json).

## Matched intermediates, boundary and activation readouts

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

The[diagnostic spec](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/configs/diagnostic_spec.json) fixes 24 DIAG / 48 TEST independent recipient pairs with 8/16 same-base controls. Only two candidates exist at last-attention pre-residual output, final prompt token: full-vector andrank1. Select once on DIAG, then confirm once on TEST if qualified; otherwise keep Unknown. Full vectors may move rule/lexical information, and this late intervention can directly change the first answer token. It does not locate an earlier reusable arithmetic computation.

| Seed | Internal-reuse readout | Selected candidate | Component-parent qualified |
| --- | --- | --- | --- |
| 29 | UNKNOWN | None | False |
| 43 | UNKNOWN | None | False |
| 71 | UNKNOWN | None | False |

All DIAG readouts are UNKNOWN: the atomic premise fails and no candidate passes its screen, so the registered rule ends internal TEST confirmation. S3–S6 main contrasts close as NOT_APPLICABLE under the premise gate; no trained expert or router is produced.

| P-J seed | Fixed mixed N | Branch scale0 | Branch scale0.5 | Branch scale1 |
| --- | --- | --- | --- | --- |
| 29 | 98 | 43.88% | 43.88% | 43.88% |
| 43 | 98 | 45.92% | 45.92% | 45.92% |
| 71 | 98 | 45.92% | 45.92% | 45.92% |

For J, adapter scale0 retains the currently updated parent endpoint and is not a return to the original component P. Equal accuracy on these98 items does not prove absence of computational branch effects.

Main BOTH TEST has 512 rows/32pq, only 31 charged cases; the never-charge shortcut is481/512. Rule-changing subsets, enriched boundary pressure and held-out wording are separate. The 48-case supplement reuses already frozen stimuli and explicitly records its seed29VAL motivation; formalTEST did not select that analysis.

## Evidence eligibility and lineage

| Bounded statement | Rule | Raw evidence/computation | Eligibility |
| --- | --- | --- | --- |
| Component premise fails | Every atomic VAL≥95% | [fixed endpoints](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/tables/fixed_endpoint_metrics.csv); complete and per-item VAL | Valid qualification negatives for all three fine-tuning parents |
| P-J joint feasibility | Failure contingency permits one joint trajectory | Fixed TEST above;four-family equal macro | Feasibility only;transfer/protection estimands not applicable |
| Symbol wording difference | Separate original wording from same-mapping other wordings | [lookup/control](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/diagnostics/symbolic/summary.json); [mapping pairs](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/tables/symbolic_same_mapping_template_pairs.csv) | Bounded behavior;internal reuse Unknown |
| Format/numerical decomposition | Keep strict main score | [strata](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/tables/error_causes.csv); [parser](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/source/explain_errors.py) | Post-hoc description;no threshold replacement |
| Saved outputs reload | Independent process native generation/NLL agreement | [reload receipts](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit) | Only actual PASS scopes apply |

Item bootstrap intervals are not cross-training uncertainty. Report all seeds before mean/range, only when all fixed endpoints exist; bootstrap BOTH bypq family. No confidence interval is invented for an unrun method contrast. S4 retention, S5 exposure and S6 capacity/active-compute effects remain unidentified.

## Numerical, saved-state and reload audits

The CPU numerical audit reports `COMPLETE`, verdict `PASS`, covering 14 actual runs ; 148 scientific checkpoints are saved. Worst scalar absolute error is2.6940914×10^-7(locked tolerance5×10^-6). Six independent endpoint reloads PASS; external byte-exact recovery is separate below. Numerical audit is not scientific mechanism confirmation.

| Readout | Status | Evidence |
| --- | --- | --- |
| reload_order_seed29.json | PASS | [receipt](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/reload_order_seed29.json) |
| reload_order_seed43.json | PASS | [receipt](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/reload_order_seed43.json) |
| reload_order_seed71.json | PASS | [receipt](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/reload_order_seed71.json) |
| reload_symbolic_seed29.json | PASS | [receipt](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/reload_symbolic_seed29.json) |
| reload_symbolic_seed43.json | PASS | [receipt](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/reload_symbolic_seed43.json) |
| reload_symbolic_seed71.json | PASS | [receipt](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/reload_symbolic_seed71.json) |

Independent reload reconstructs exactBase plus saved increments and uses a fresh native forward for predictions/NLL. The external[resume receipt](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/external_resume/20261024T162457Z_shell376/resumed.json) restores engineering-smoke update 2 in another Python process,44 cumulative valid tokens, with byte-equal tensor state. Its scope is the four-row F-adapter smoke, not exhaustive resume verification of all formal checkpoints.

All52 actual output assets pass final strict access, covering152 checkpoint paths(148 scientific saves),4 caches and32 derived-analysis groups, with no handoff gaps. Identities and final access evidence are in the[asset handoff](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/final_registration_handoff.json).

## Actual runs and artifact access

| Task | Seed | Arm | Version | Updates | Valid target tokens | Endpoint receipt | Final TEST |
| --- | --- | --- | --- | --- | --- | --- | --- |
| order | 29 | J | v2-expanded | 2000 | 447845 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed29_P_J_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed29_P_J_balanced_replay_v2-expanded/predictions/test_final.jsonl) |
| order | 29 | P | v1 | 3000 | 610656 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed29_P_P_balanced_replay_v1/complete.json) | NOT_RUN_FOR_INITIAL_QUALIFICATION |
| order | 29 | P | v2-expanded | 3000 | 610656 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed29_P_P_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed29_P_P_balanced_replay_v2-expanded/predictions/test_final.jsonl) |
| order | 43 | J | v2-expanded | 2000 | 447791 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed43_P_J_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed43_P_J_balanced_replay_v2-expanded/predictions/test_final.jsonl) |
| order | 43 | P | v2-expanded | 3000 | 610665 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed43_P_P_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed43_P_P_balanced_replay_v2-expanded/predictions/test_final.jsonl) |
| order | 71 | J | v2-expanded | 2000 | 447853 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed71_P_J_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed71_P_J_balanced_replay_v2-expanded/predictions/test_final.jsonl) |
| order | 71 | P | v2-expanded | 3000 | 610678 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed71_P_P_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/order_seed71_P_P_balanced_replay_v2-expanded/predictions/test_final.jsonl) |
| symbolic | 29 | J | v2-expanded | 2000 | 236180 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed29_P_J_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed29_P_J_balanced_replay_v2-expanded/predictions/test_final.jsonl) |
| symbolic | 29 | P | v1 | 3000 | 354000 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed29_P_P_balanced_replay_v1/complete.json) | NOT_RUN_FOR_INITIAL_QUALIFICATION |
| symbolic | 29 | P | v2-expanded | 3000 | 354000 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed29_P_P_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed29_P_P_balanced_replay_v2-expanded/predictions/test_final.jsonl) |
| symbolic | 43 | J | v2-expanded | 2000 | 236180 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed43_P_J_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed43_P_J_balanced_replay_v2-expanded/predictions/test_final.jsonl) |
| symbolic | 43 | P | v2-expanded | 3000 | 354000 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed43_P_P_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed43_P_P_balanced_replay_v2-expanded/predictions/test_final.jsonl) |
| symbolic | 71 | J | v2-expanded | 2000 | 236180 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed71_P_J_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed71_P_J_balanced_replay_v2-expanded/predictions/test_final.jsonl) |
| symbolic | 71 | P | v2-expanded | 3000 | 354000 | [complete](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed71_P_P_balanced_replay_v2-expanded/complete.json) | [TEST](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/runs/symbolic_seed71_P_P_balanced_replay_v2-expanded/predictions/test_final.jsonl) |

The14 actual trajectories are verified by fixed endpoints, metrics and per-item TEST. The115 remaining status rows are not applicable or superseded. All5 jobs are verified platform SUCCEEDED with an empty active list; the[terminal index](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/final_job_terminal_index.json)and[final manifest](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/result_manifest.json)record closure of execution. Qualification negatives for S1/S2 and prerequisite-based non-applicability for S3–S6 are valid finite-protocol terminal outcomes.

| Artifact | Purpose/identity |
| --- | --- |
| [run plan](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/run_plan.csv) / [run status](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/run_status.csv) | Finite plan versus actual version/condition/seed state |
| [execution freeze](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/configs/execution_freeze.json) | Source/config/model/data hashes |
| [data manifest](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/data/data_manifest.json) / [data audit](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/data_audit.json) | Frozen split, independent labels and shortcut audit |
| [fixed endpoints](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/tables/fixed_endpoint_metrics.csv) | Native accuracy/CE with per-item lineage |
| [error strata](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/tables/error_causes.csv) | Post-hoc numerical/format/condition description |
| [CPU numerical audit](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/result_numerical_audit.json) | Counts, source/state and tensor displacement; current status above |
| [actual registration](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/registration_actual.json) | Actual saved output IDs and access receipts |
| [reproduction commands](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/reproduce_commands.txt) | Environment/frozen entrypoints/reload/read-only reaggregation |

## Scientific state and next judgment

The[scientific inference review](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/scientific_interpretation_review.json)checks model/domain/context, expected lookup calibration, valid-but-wrong outputs, seen atomic tuples and information/depth confounds. It permits a bounded next hypothesis, not researcher acceptance or mechanism confirmation.

Question OPEN; human mechanism judgment Unknown. The factual record separates formatting, atomic arithmetic and cross-context behavior. A separate AI interpretation may propose bounded causes and a next hypothesis. Research closure, priorities and the minimal next experiment remain researcher decisions. Anchor,Focus,R01 and other conversation memories are unchanged.

---

## Historical execution provenance, preserved as recorded

The following is the original 16:09Z provenance. Its RUNNING/PENDING states describe that timestamp; current state is above. Its source text is retained verbatim.

<!-- PRESERVED_PROVENANCE_START -->
# Detailed: A15_26 Order V2 And Symbolic Auxiliary

[中文](detailed_cn.md) · [Protocol](protocol.md) · [Runtime binding](sources/runtime_binding_20261024.json)

## 2026-10-24T16:09:43.995743+00:00 — Execution provenance; scientific results RUNNING

This record describes actual sources and saved runtime evidence. It is not a final Summary or a mechanism verdict. The scientific question remains open, and researcher acceptance is Unknown.

### Registered body and inputs

The scientific body was frozen at `2026-10-24T15:59:10.536987+00:00` with SHA-256 `50517762ebf4be79d5f029f4e0234930ef529b72a7ffae1f30fa91f54cc2ddf3`. Its immutable [snapshot](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/protocol_frozen.md) preserves the exact pre-start text. Later Protocol provenance notes do not rewrite that body. The [execution freeze](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/configs/execution_freeze.json) binds initial source snapshots, order generator, symbolic API, order manifest and strict access receipts. The [symbolic freeze](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/symbolic_source_freeze.json) separately enumerates source and all actually generated symbolic payload hashes.

The parent is registered asset `model_qwen3_0p6b_base_official_a5`, at `/data/250010109/model_cache/Qwen3-0.6B-Base-official`. Runtime smoke measured weight SHA-256 `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba` and config SHA-256 `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59`. Input data IDs are `data_order_moe_v2_20261024` and `data_symbolic_moe_v2_20261024`; their strict guards remain linked in the freeze. This uses no learned R05 rule checkpoint.

### Jobs and runtime evidence

| Job | Role | Submitted UTC | Durable receipt | Evidence state |
| --- | --- | --- | --- | --- |
| `pt-nanedkok` | engineering smoke | 2026-10-24T15:24:45Z | [submit-order-v2-engineering-smoke-1024-20261024T152444Z.json](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/acp_receipts/submit-order-v2-engineering-smoke-1024-20261024T152444Z.json) | SMOKE_PASS_ARTIFACT_VERIFIED |
| `pt-b784zfqv` | order full finite pipeline | 2026-10-24T15:59:42Z | [submit-order-v2-full-1024-20261024T155941Z.json](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/acp_receipts/submit-order-v2-full-1024-20261024T155941Z.json) | RUNNING_LAST_REPORTED;TERMINAL_NOT_VERIFIED |
| `pt-tvcwfc9w` | symbolic auxiliary pipeline | 2026-10-24T15:59:50Z | [submit-symbolic-v2-full-1024-20261024T155949Z.json](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/acp_receipts/submit-symbolic-v2-full-1024-20261024T155949Z.json) | RUNNING_LAST_REPORTED;TERMINAL_NOT_VERIFIED |

Receipt acceptance proves submission only. [Smoke](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/smoke.json) supplies the bounded engineering evidence: actual H100, FP32, native last-layer index27/width1024, zero-output insertion, frozen-parent identity, zero-LR no change, multi-token answer/EOS masks, 22 independently counted target tokens and cached/native maximum logit error0 with equal argmax. Strengthened next-update recovery is separately represented only where the current smoke receipt contains it. This is not arithmetic learning qualification. Raw Base generations include trailing text/units, retained as format errors under the strict registered score.

Full pipelines are still RUNNING as last reported. A planned 117 trajectories is not an actual completed count. Initial and expanded-range qualification-lock versions remain separate; the locked scientific revision uses only TRAIN/VAL, retains initial negative evidence and does not change step/LR budgets. Final three-seed eligibility, downstream applicability, all required test records and result audits remain pending.

### Data and inference limits already known before qualification

The [CPU audit](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/data_audit.json) checks labels, canonical uniqueness and split disjointness. Unique BASE/S1 support is1680 TRAIN/240 VAL/120 DIAG/360 TEST, rather than inventing 2048 independent numerical pairs. BOTH's512 test examples have only32 independent `(p,q)` families; never adding shipping scores93.945%, and only31 examples charge shipping. S2b always-free baseline is481/512 on TEST and234/256 on VAL. Therefore rule-switching and enriched boundary strata must accompany aggregate accuracy; these are distribution limits, not measured model mechanisms.

### Saved states, loading and result audit

Actual runs write `runs/<run_id>/checkpoints/step_*.pt`, `metrics.jsonl`, TensorBoard, validation predictions, heartbeat/state and eventual `complete.json`/fixed-test predictions. The execution [loader](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/source/order_model.py) first constructs the exact Base, resets the declared parent/range/adapter architecture, then restores saved original last-layer weights and adapter/router increments. Full restart additionally requires optimizer, RNG, counters and data cursor. This is a loading entry, not a statement that all saved checkpoints have passed independent restore. Actual saved output asset IDs and family manifests are **PENDING registration**.

The CPU [aggregator](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/source/aggregate.py) separates protocol version/hash, validates nonempty endpoint/metrics/test artifacts and produces [run status](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/run_status.csv), [stage ledger](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/analysis/stage_ledger.json), [fixed-endpoint tables](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/tables/fixed_endpoint_metrics.csv) and [live reading](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/morning_readme.md). Last-reported RUNNING does not replace current platform inspection. No positive, negative or NOT_APPLICABLE stage is final without its required evidence; overall completion additionally requires three result audits, independent endpoint reloads and actual output registration. The packaged manifest checker validates structure/hashes, not science.

### Completion boundary

Final observations, cause analysis and hypothesis update will be grounded in actual fixed-endpoint predictions. Three pre-run audits exist in this round; result-stage data/statistics, implementation/numerics and scientific-identification reviews will append actual evidence. No unrun result or causal reason is supplied in this entry. Parallel R01 retains its own Protocol, data, execution root and Focus; this record changes none of them.

## Final execution-time trace

[Timing record](sources/runtime_record_note.md) preserves an operational record deviation: regenerating the original plan overwrote its rough pre-run estimate field. Actual job start/end times remain in execution-side tables/actual_runtime.csv. Scientific budgets/comparisons and all117 initial plan rows were preserved.
