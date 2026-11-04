# Protocol A15_24_02: frequency complement analysis

## 0. Approval Snapshot

FROZEN_FOR_BOUNDED_ANALYSIS. The current user explicitly requests this analysis and results; no repeated approval is required for this bounded scope. Scientific judgment awaits reading and discussion. Parent A15_24; new requested child A15_24_02. No independent Focus is created. Question: does a complement restriction change local low-feature predictive benefit? Operationalization/proxy test, not a long training method evaluation. Local existing H100 MIG only, sequential seeds, 2 CPU threads, 12 GiB GPU allocation ceiling, 900 seconds, 1 GiB new outputs. No remote submission, continued training or publication.

## 1. Terminology / Definitions

V: 1024×16 existing TRAIN PCA; Q: saved 1024×16 random orthonormal basis. P=VVᵀ. W: experts.0.up.weight, shape1024×1024. D: final minus initialization. U: one complete scratch AdamW displacement. NLL: negative log probability of the actual next token, nat. Low/high mean original TRAIN frequency bands B1/B4, not task difficulty.

## 2. Anchor Alignment

Uses the exact linear preservation clause and finite prediction comparison in Anchor sections4–6. Its complement is input-side, not a weight SVD or whole-network functional guarantee. The strongest alternative is generic step-size change or useful shared directions.

## 3. Tested Hypothesis

At matched update norm, the selected complement has lower E0-routed low-feature macro NLL than full and random-restricted updates in both saved seeds. Practical acceptance remains pending; the descriptive numerical floor is 1e-6 nat.

## 4. Rival Explanations

Control generic edit damage with same-rank, norm-matched random rollback; control reduced step size with norm-matched complement updates; measure gradient-only AdamW leakage; retain shared low/high utility and limited support as alternatives.

## 5. Data Construction And Provenance

Tulu cached final-layer hidden states and labels: TRAIN85548 positions/1024 dialogues; DEV10340/128. Original frequency groups, routes, global PCA and initial/final T_F states are fixed. Both panels already exposed. Select the first512 E0-routed TRAIN indices in each checkpoint saved order; never select from effect sizes. DEV evaluation is complete, with edited forwards restricted to E0-hit positions because other outputs are algebraically unchanged. Six asset IDs and strict-access evidence are in frozen.json/input_access.json. No new confirmation split is claimed.

## 6. Learning Task And Permitted Supervision

One frozen-next-token task. TRAIN labels only produce the scratch gradient. DEV never contributes a gradient, direction, scale choice or stopping choice. Frequency-conditioned readouts overlap. No feature meaning is inferred from frequency.

## 7. Model / Architecture And Frozen Variants

Original top2 SwiGLU residual branch: eight experts, hidden/width1024, coefficient0.5 each, full hidden input and fixed scale. All parameters except E0 up are frozen. Parent embeddings/norm from registered Qwen3 base. Two saved seeds11/22 at168steps. Native BF16 baseline may be compared descriptively; all primary interventions and gradients use the same FP32 branch/head with TF32 disabled to avoid small updates disappearing in BF16 casts. Therefore primary NLL is not a replication of the old BF16 metric.

## 8. Objective And Optimization

CE sum /512 valid targets, microbatch64. Clip only the one eligible matrix at norm1. Restore its complete saved AdamW moments/step and group hyperparameters; use the saved terminal learning rate, beta0.9/0.95, eps1e-8, decay0.01. Each scratch optimizer call starts from the identical saved state; accepted continuation steps=0. Standard U and raw-gradient-projected U are independent proposals. No optimizer history is accepted or accumulated. Save counters, actual LR, loss, norms and state hashes. Resume trajectory/TensorBoard training contract is not applicable to this nonaccumulating analysis.

## 9. Conditions, Seeds, And Checkpoints

Per seed: identity/no-op; rollback fractions0.25/0.5 on PCA and norm-matched random projection; full U; PCA complement; random complement; both complements rescaled to norm(U); raw gradient projected to complement before AdamW as a distinct diagnostic. The model resets after each readout. Rank16 fixed before effects. Inputs remain untouched.

## 10. Primary Metric And Frozen Analysis Plan

Primary is equal-feature macro NLL over B1 IDs supported among E0-routed DEV positions. Save each feature support and mean and paired differences. NA features excluded with count reported. Full DEV low/high macros and all-position loss are secondary. Two seeds supply a descriptive paired sign rule, not a population interval. No model selection. Report absolute baseline, condition, delta and both comparator contrasts. Values below1e-6 nat are numerically small under this prespecified readout.

## 11. Secondary Metrics And Guards

No-op NLL must be elementwise equal in this FP32 environment; original input/model tensor digests match saved receipts. Finite values required. Random/matched-update norm relative error≤0.002. Precast complement leakage relative norm≤1e-6; applied response change relative to original W norm≤5e-7. Report both pre/post rounding. Measure every frozen tensor digest before/after. Retain all low/high overlap counts and per-dialogue signs. No hidden tuning of tolerance.

## 12. Known Good / Bad / Confusing Cases

Good: P is symmetric/idempotent and (I−P)V=0. Bad: a displacement along P changes WV. Confusing: raw-gradient projection can leak after AdamW; complement updates can alter mixed-input predictions. These are numerical/algebra checks, not discoveries of semantic mechanisms.

## 13. Scientific Procedure And Stage Contracts

First verify assets and identities; then baseline/no-op and fixed selectors; then four rollback effects; then derive two scratch updates and evaluate six update arms; finally independent metric recomputation from saved per-position NLL, parameter/freeze/norm audits and bilingual results. Stop only the invalid dependency when a gate fails; retain the failure. No broadening/retry to find benefit.

## 14. Algorithm, Output, And Provenance

Execution root /data/250010109/MoE_Router/experiments/20261023_frequency_complement. frozen.json owns machine values, worker.py source, per-seed .npz owns NLL/selectors, results.json owns full measurements, audits.json owns three audit passes. No trained checkpoint is emitted. Inputs are source-hashed and model digests verified. Record runtime, device, peak memory, command, code/contract hashes and deviations.

## 15. Success / Failure / Insufficient Evidence

Complete when both seeds/all specified arms and checks are accounted for. Valid signed effects are factual results; nonfinite or failed guards mark corresponding tests INVALID. Missing low-feature support is INSUFFICIENT. Predicted joint signs are recorded without an AI scientific verdict until researcher review.

## 16. What This Cannot Claim

No proof of long-training gain, general forgetting, high-frequency causation, whole-task preservation, new fresh confirmation or reproduction of the advisor algorithm. Static rollback and future-update effects have different meanings.

## 17. Block Confirmation, Freeze, And Amendment Ledger

A–G: question/scope, data, supervision, model, optimizer, comparisons and execution have been inspected against the source and this user authorization. Numerical choices are explicit AI operationalization; human mechanism judgment pending. Scientific, data/statistical and implementation audits are recorded separately. The initial draft was completed before promotion to this bounded executable revision; frozen.json and this Protocol are hashed before outcomes. Subsequent implementation repairs require a dated amendment without retuning outcomes.

Pre-execution implementation clarification: baseline evaluates E0-hit and non-hit subsets separately, using the same fixed microbatches for every repeat of the affected subset. This preserves elementwise no-op comparability without changing the complete DEV panel or metrics.
