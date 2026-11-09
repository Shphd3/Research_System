# Protocol: additional always-on common expert

Frozen at 2026-10-22T10:46:42.697985+00:00

## 0. Approval Snapshot
Status: frozen exploratory extension, directly authorized by the researcher on 2026-10-22. The user requested an additional common expert for ordinary MoE and frequency routing, explicitly waived parameter matching, and required separate one-GPU Reserved jobs. Routine implementation choices below are AI operationalization under that authorization, not a claim of separately confirmed scientific judgment. No new Focus is created or promoted. Parent Anchor: [15_24](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/15_24_frequency_composition_common_path_anchor.md). This extension changes the parent's fixed-parameter/fixed-active-path constraint only for the current run; historical results retain their original contract.

Purpose: determine whether preserving both routed experts and adding an always-on learned residual improves the same low-feature prediction target. Role: operationalization test. The strongest rival is extra capacity/active compute or altered optimization, which this deliberately unmatched exploration cannot exclude. Completion means all eight final models plus paired final evaluation, or a factual partial/failure record. Scientific mechanism remains Unknown.

## 1. Terminology / Definitions
A feature is one thresholded activation coordinate of the frozen 16,384-feature CrossCoder. A feature event is one active feature at one answer-prediction position. Low features are the original B1 pool (1,694 features, TRAIN support 1–17). A routed expert reads the complete hidden state, not just its named feature group. Common means always-on and shared across positions; it does not certify semantic commonality.

## 2. Anchor Alignment
The old forced-popular condition replaced one of two experts. The current treatment keeps both and adds a new branch. This tests an additional learning path, without claiming to reproduce the advisor's rank-one algorithm or solve frequency grouping. Three analysis steps: verify paired training; compare final prediction losses; describe paired changes against fixed input coactivation.

## 3. Tested Hypothesis
Within each routing family, adding common decreases final DEV low-feature macro NLL for both paired seeds. Cross-family differences in this treatment effect are secondary. Lower NLL means better next-token prediction.

## 4. Rival Explanations
Capacity increases by 3,145,728 parameters and active experts by two to three. Common also enters global gradient clipping. Benefits may arise from these changes, shared learning, or optimization. Log component gradients, updates and clipping; do not assign a unique cause. Frozen common-off ablation measures a trained model's inference dependence, not the causal training effect.

## 5. Data Construction And Provenance
Reuse the existing Tulu cache: TRAIN 1,024 dialogues/85,548 valid answer targets; EVAL 256/22,446; DEV 128/10,340. Targets include answer EOS and exclude prompt/padding. Dataset revision 6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752. Inputs are complete Qwen3-0.6B block-28 residual-post hidden vectors, dimension 1,024, BF16. The same 14-layer joint CrossCoder and activation threshold 0.051281172782182693 define features and routes. Existing split membership and source hashes are unchanged. DEV has already been inspected in earlier work; it is an exploratory held-out panel, not fresh confirmation. Current strict input access PASS is recorded in execution provenance.

## 6. Learning Task And Permitted Supervision
Predict the next answer token with the original frozen final normalization and vocabulary head. Train only residual experts and, for ordinary MoE, its router. No base-model or CrossCoder update. Do not use DEV for stopping, tuning, feature selection or checkpoint choice.

## 7. Model / Architecture And Frozen Variants
Let h be the full cached input and s the inherited TRAIN RMS scale. Baseline: h'=h+s*sum_j w_j E_j(h/s), with two distinct routed experts. Treatment adds s*C(h/s), coefficient 1, with no replacement or division by three. Eight routed experts and common are bias-free width-1,024 SwiGLUs. T_F uses its original saved routes and weights 0.5/0.5; MoE uses learned top-2 renormalized gates, no load-balancing loss. No capacity dropping. Common uses independent seed+987031 random gate/up and exact-zero down. Initialization RNG is isolated; baseline and treatment's shared parameters and sample order must match exactly.

## 8. Training Objective And Optimization
Answer-target cross entropy only, reduced by actual valid targets per effective batch. AdamW lr 0.0003, betas (0.9,0.95), eps 1e-8, weight decay 0.01; nine-step warmup, cosine final ratio 0.1; global gradient clip 1. Effective batch 512, microbatch 128, last effective batch 44. One epoch, 168 updates, 85,548 targets per model. Original optimizer/schedule/cache code is reused and inspected; the common branch, instrumentation and serial launcher are adaptations. A full pretraining scaffold is unnecessary for this frozen-cache task. Required token/update losses, progress, learning rate, exposure and branch health are emitted to TensorBoard; no invented auxiliary-loss tags.

## 9. Conditions, Seeds, And Checkpoints
Two routing families × baseline/plus_common × seeds 11/22 = eight models. Two independent h100-1-reserved jobs, one family each, serial four-model execution per job. Each allocation: one node, one process, one H100, Reserved quota, spec n6ls.iu.i40.1, image shphd-lite-0911. No four-GPU job. Save initial weights; weights at steps 42/84/126; normal latest and final with optimizer/RNG/order/cursor/counts. Each latest is recoverable in the validated restore routine; automatic CLI resume is not implemented. Exception snapshots require additional validation.

## 10. Primary Metric And Frozen Analysis Plan
Primary: final step-168 DEV B1 low-feature macro NLL, mean over active DEV B1 features of each feature's mean position NLL. Report paired treatment-minus-baseline for each seed and their arithmetic mean. Negative in both seeds is exploratory support for this fixed setting; mixed/zero directions do not support stable benefit; both positive are exploratory non-support. Missing/invalid pair is insufficient. This is not a statistical significance claim. Always report overall position-mean NLL and low-union position-mean NLL separately. No post-hoc change of denominator.

Coactivation secondary: reuse the earlier TRAIN-selected eight companions per low feature and eight frequency-matched random companions. Bin each DEV low-feature event by active selected-companion count: 0, 1–2, 3–4, 5–8. Report paired NLL deltas separately by family, seed and bin, with feature-event, unique position and dialogue counts. Same-position events are dependent. Apply the identical bins to random companions as a descriptive reference. No new outcome-selected bins, and no causal claim from these strata. Input feature coactivation is fixed across training arms.

## 11. Secondary Metrics And Guards
Report high-feature and overall metrics, route loads, common/routed output norms, gradients, updates, clipping factors and actual target counts. On each trained plus_common checkpoint evaluate full, common_off and common_only at final DEV. Distinguish these frozen inference contrasts from matched training contrasts. Preserve per-position losses and feature support. No claims about long-range reasoning, semantic hierarchy, parameter efficiency or rank-one losslessness.

## 12. Known Good / Known Bad / Known Confusing Cases
Known good: zero common output exactly preserves initial logits and shared initialization. Known bad: replacing an old expert or renormalizing three branches violates this contract. Known confusing: a useful common inference contribution can coexist with no net training advantage; improved load does not establish improved prediction.

## 13. Scientific Procedure And Stage Contracts
CPU static and independent code audit precede submission. Within each job, actual GPU smoke checks source identity, data/labels, gradients, exact paired initialization/logits, a full 512-target update, next-update equality after restore, and TensorBoard values. Formal training starts only after smoke PASS with unchanged source hashes and an ETA within the active budget. Final DEV begins only after all four family models complete. No automatic retries or resource fallback.

## 14. Algorithm, Output, And Provenance Contract
Each job has a 35-minute active budget including smoke/evaluation, 16 GiB GPU allocated-memory ceiling, 16 GiB worker RSS, two CPU threads, and a 16 GiB run-output ceiling. Preserve failure/partial evidence; do not stretch scope silently. Source code, config, actual runtime GPU/image, submission receipts, logs, all saved states and per-position arrays reside in the execution run linked below. Register actually saved training assets at completion, including partials if applicable. Follow repository observability and asset lifecycle contracts.

## 15. Success / Failure / Insufficient Evidence
Engineering acceptance requires valid counts, finite losses, smoke PASS, complete same-family pairs and durable final evaluation. Scientific exploratory support/non-support follows section 10 separately for each family. A platform COMPLETED status alone is insufficient. Partial execution cannot establish a family comparison. No mechanism conclusion is automatic.

## 16. What This Cannot Claim
An unmatched extra branch cannot identify whether capacity, shared computation, learning dynamics or frequency-group structure caused an effect. Two seeds and an exposed panel do not establish broad generalization. Mixing graph depths alone is not evidence of harmful interference.

## 17. Block Confirmation, Freeze, And Amendment Ledger
User-confirmed: additional always-on expert, ordinary/frequency families, no parameter matching, remote single-GPU Reserved, execution now. Verified sources: existing data, routes, trainer, optimizer and registry inputs. AI operationalization: two seeds, common coefficient/initialization, inherited budget, analysis bins and runtime caps. No new consequential scientific decision is represented as human-confirmed. CPU static PASS and independent review PASS for initial training; actual GPU gate remains pending until executed. Source hashes are frozen by static_check.json. Amendments after first launch must be timestamped, preserve this original contract, and state whether any outcomes were already seen.

Execution run: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/shared_common_expert/20261022T103833Z`.
