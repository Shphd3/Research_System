---
experiment_id: A15_08_09_E02_qwen30b_all_layer_gain_and_preservation
document_status: COMPUTATION_COMPLETE_EXTERNAL_H1_GUARD_UNRESOLVED
design_frozen_at: 2026-08-24
approval_source: explicit user instruction to restart, localize Qwen3-30B-A3B layers, and complete the full rerun
anchor: ../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md
focus: ../../../../../../../daily_research_reports/backup/2026/08/0824/focus_random_projection_router_preservation.md
predecessor: ../A15_08_09_E01_random_projection_router_preservation/protocol.md
worker_root: /data/250010109/MoE_Router/experiments/20260824_a15_08_09_e01_random_projection_router_preservation
---

# Protocol: Qwen3-30B-A3B All-Layer Gain Localization And Preservation

## 0. Approval Snapshot

- **Purpose:** remove the unverified transfer of Qwen3-8B blocks 24/28 to Qwen3-30B-A3B, localize the relevant 30B-A3B layer without TEST access, and rerun the existing full-space and conditional projection gates.
- **Primary Anchor:** A15_08_09; the theorem is conditional on an already-positive full-space margin.
- **Experiment role:** model-local operationalization repair followed by a confirmatory robustness check.
- **Treatment:** true same-row $R_{U,\ell}$ added to a frozen same-layer $X_\ell$ base readout.
- **Controls:** a duplicate-$X_\ell$ correction and independently mismatched $R_{U,\ell}$ corrections.
- **Changed variable:** transformer block $\ell\in\{1,\ldots,48\}$ during localization; all data, token, labels, model weights, residualization, and probe families remain fixed.
- **Primary localization metric:** simultaneous-interval lower bound of matched added-utility excess $T_\ell$ on DEV.
- **Primary preservation metric:** unchanged E01 H3 low-tail margin gate; H4 normalized margin retention is defined only after H3 Pass.
- **Pass:** H0 has at least one positive-excess layer; H2/H3/H4 retain their separately registered meanings.
- **Fail:** no H0 layer has a positive simultaneous lower bound, or a downstream gate fails under its frozen rule.
- **Insufficient:** extraction/data/fit/uncertainty guards fail or a required human data review remains unresolved.
- **Cannot claim:** expert utility, causal specialization, distribution-free geometry, or that a failed linear readout rules out every representation.
- **Execution:** implementation, smoke, and conditional full run are approved on exactly one reserved four-H100 ACP worker. Commit, push, publication, and root sync are not approved.

## 1. Terminology / Definitions

At the final token of the common `Answer:` suffix for block $\ell$, let $X_\ell$ be the post-attention RMSNorm input before attention addition, $U_\ell=Z_\ell-X_\ell$ the attention-induced normalized update, and

$$R_{U,\ell}=U_\ell-(X_\ell\widehat B_\ell+\widehat b_\ell)$$

the update residual after a TRAIN-fitted ridge predictor of $U_\ell$ from $X_\ell$. A **gain layer** is a block whose DEV matched added-utility excess has a familywise simultaneous 95% lower bound above zero. This is a diagnostic of incremental linear label accessibility, not a proof of native Router use.

## 2. Anchor Alignment

E01 established H2 Pass and H3 Fail only for blocks 24/28. Those layers originated in a 36-block Qwen3-8B scan, so they do not establish the premise across the 48-block Qwen3-30B-A3B model. E02 changes only layer localization and then reuses the frozen theorem-aligned gate. The strongest rival is that E01 failed because the transferred layers were poor, rather than because Qwen3-30B-A3B lacks the required robust linear object.

## 3. Tested Hypothesis

- **H0:** at least one 30B-A3B block has positive controlled added utility $T_\ell$ on DEV.
- **H1:** the existing 19,200-row binding-controlled dataset passes all machine guards and the external 64-row review guard.
- **H2:** the selected full-space $R_U$ readout is stably above chance on both TEST panels.
- **H3:** both TEST panels have balanced-accuracy lower bound at least 0.90 and positive 5th-percentile true-label-margin lower bound, with the existing seed and precision guards.
- **H4:** conditional on primary-layer H3 Pass, some $m\le d/8$ meets the frozen Gaussian-projection preservation criteria.

## 4. Rival Explanations

Duplicate-$X$ gain detects regularization/capacity artifacts from adding a second linear path. Mismatched-$R_U$ gain detects chance improvement under an unrelated update. TRAIN/DEV-only selection prevents test-guided layer choice. E01 is preserved because successor evidence at another layer cannot alter its registered block-24/28 verdict.

## 5. Data Construction And Provenance

Use the frozen `data_v2/metadata.jsonl` with 64 fine classes nested in eight parent labels and exactly 19,200 rows: 11,520 TRAIN, 2,560 DEV, 2,560 same-template TEST, and 2,560 new-template TEST. The model input is `prompt`; the parent label is supervision. No generation or data rewriting is allowed. Dataset hashes, split isolation, direct-label, 5-gram, length, class balance, bag-of-words, and review-pack receipts are inherited and rechecked. The two TEST panels have been opened by E01; therefore E02 is a pre-registered successor on new layer-wise observables, not a pristine new-dataset replication.

## 6. Learning Task And Permitted Supervision

All residualizers and readouts fit on TRAIN. Hyperparameters and the layer selector use DEV only. TEST labels are inaccessible until `layer_freeze.json` exists. The output is the eight-way parent label. No fine label, split name, template identifier, answer text, or test statistic may enter a fitted model or selector.

## 7. Model / Architecture And Frozen Variants

The frozen model is `/data/share/Qwen3-30B-A3B`, 48 blocks, hidden size 2048, BF16 evaluation, no generation and no parameter update. Extract $(X_\ell,U_\ell)$ for every block in one full forward pass. Final H2/H3 uses the same five-seed L2 multinomial-logistic family as E01. H4 uses independent dense Gaussian matrices and frozen projected weights; it never retrains in projected space.

## 8. Training Objective And Optimization

For localization, use deterministic ridge multi-class scores with one-hot targets and $\lambda\in\{10^{-6},\ldots,10^2\}$. First fit a base score $s^X_\ell$. Fit an additive correction on true $R_U$, on duplicate $X$, and on 30 independently mismatched $R_U$ datasets. Select every ridge penalty by DEV cross-entropy within its TRAIN-fitted family. Final H2/H3 uses E01's L2 logistic grid $C\in\{10^{-6},\ldots,10^2\}$ and five fixed seeds.

## 9. Conditions, Seeds, And Checkpoints

- Layers: all 48 for localization; one primary and one replication for confirmation.
- Replication separation: absolute layer-index difference at least four.
- Probe seeds: 24001--24005; primary seed 24001.
- Mismatch seeds: 8240921000--8240921029.
- Bootstrap seed: 8240922001; 2,000 stratified draws for formal results.
- Gaussian dimensions and 30 matrices per dimension: unchanged from E01.

## 10. Primary Metric And Frozen Analysis Plan

For DEV example $i$, let cross-entropy reductions over the same frozen base score be $G_\ell^{\mathrm{true}}$, $G_\ell^{\mathrm{dupX}}$, and $G_{\ell,j}^{\mathrm{mis}}$. Define

$$T_\ell=G_\ell^{\mathrm{true}}-\max\left(G_\ell^{\mathrm{dupX}},Q_{0.95}\{G_{\ell,j}^{\mathrm{mis}}\}_{j=1}^{30}\right).$$

Stratified bootstrap resamples DEV rows and recomputes all 48 values in each draw. The simultaneous one-sided 95% lower bound subtracts the 95th percentile of the bootstrap maximum centered error across layers. H0 Pass requires at least one layer with lower bound $>0$. TEST is not used.

The primary layer is the positive-excess layer with the largest DEV 5th-percentile true-label margin under a standalone ridge $R_U$ readout, then higher balanced accuracy, then smaller layer index. The replication layer applies the same ordering among layers at least four blocks away. If H0 fails, the same ordering over all layers produces a diagnostic fallback pair; H0 remains Fail. The freeze file stores all metrics, selector version, inputs, and hashes before TEST evaluation.

H2, H3, and H4 computations, thresholds, uncertainty, missing-row handling, and seed rules are exactly E01's registered rules. The primary layer determines H4; the replication layer cannot rescue it.

## 11. Secondary Metrics And Guards

Publish raw true gain, duplicate-$X$ gain, mismatch q95, controlled excess, standalone DEV balanced accuracy, and standalone DEV margin q05 for all layers. Recompute exact within/between distances, supervised functional rank, and spectral coherence only at the frozen layers. These diagnostics cannot rescue H0--H4.

## 12. Known Good / Known Bad / Known Confusing Cases

Synthetic tests must recover a planted incremental layer, reject duplicate-only and mismatched-only gains, enforce the four-layer replication separation, and preserve deterministic tie-breaking. E01 block 24/28 values are known opened outcomes and are never used as expected values or selection inputs.

## 13. Scientific Procedure And Stage Contracts

1. Recheck data/model preflight and extract all 48 layers; stop on any identity, finite-value, architecture, partition, or overwrite guard.
2. Fit all residualizers and run TRAIN/DEV localization. Write and hash `layer_freeze.json`; assert no TEST split was loaded by the selection script.
3. Run H2/H3 and selected-layer diagnostics on both TEST panels. If primary H3 is not Pass, emit `SKIPPED_H3_NOT_PASS` for H4.
4. If primary H3 passes, run the unchanged Gaussian dimension scan. Render the layer curve and gate summary from canonical JSON/CSV only.

## 14. Algorithm, Output, And Provenance Contract

Worker outputs live under `runs/e02-all-layer-<mode>-<stamp>/`. Required artifacts are preflight; extraction/residualizer manifests; `layer_scan.csv`; `layer_scan.json`; `layer_freeze.json`; selected-layer probe result and routers; conditional projection result; diagnostics; canonical figures; and a completion audit. Every artifact records hashes, code paths, model path, data hash, seeds, and the reserved ACP job receipt.

## 15. Success / Failure / Insufficient Evidence

H0--H4 each receive `Pass`, `Fail`, `Insufficient`, or registered `SKIPPED_H3_NOT_PASS`. A scientific Fail is immutable. Only an implementation fault that violates the frozen contract may be repaired, with the failed attempt retained. Missing external review makes H1 and therefore overall closure `Insufficient`, even if computational gates complete.

## 16. What This Cannot Claim

The experiment cannot show that the pretrained model natively routes by the label, that a class label is an expert-utility target, that random projection creates information, that the smallest passing empirical dimension is a tight theorem bound, or that failure excludes nonlinear or task-aligned learned representations.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A. Question/boundary | CONFIRMED | user restart instruction; approved Anchor |
| B. Data/provenance | CONFIRMED | frozen E01 data and receipts |
| C. Task/supervision | CONFIRMED | unchanged parent-routing task |
| D. Architecture | CONFIRMED | all 48 Qwen3-30B-A3B blocks; user-requested model-local scan |
| E. Objective/optimization | CONFIRMED | prior added-accessibility design plus frozen E01 final probe |
| F. Evidence/verdict | CONFIRMED | user-requested gain curve and unchanged H2--H4 gates |
| G. Execution/reproducibility | CONFIRMED | explicit reserved 4xH100 full-run authorization |

Cross-block consistency: **PASS**. Confirmation leakage guard: **PASS by construction** because localization consumes only TRAIN/DEV and must write the freeze receipt before TEST. Scientific body is frozen at first implementation. Post-start changes require an append-only amendment with eligibility impact.

### Amendment A01 — BF16 native-input identity tolerance (2026-08-24)

- **Before:** the inherited E01 native-MLP-input relative-error threshold was `1e-5`.
- **After:** for the 48-layer BF16 extraction only, the threshold is `1e-3`; replay, finite-value, $U=Z-X$, and attention-output-projection thresholds are unchanged.
- **Reason:** the first approved smoke observed isolated per-layer relative differences of $2.6\times10^{-4}$--$3.3\times10^{-4}$ while every algebraic and replay identity remained exact. The old threshold was calibrated on only blocks 24/28 and is below BF16 rounding scale.
- **Data visible:** smoke inputs and identity receipts only; no layer gain, TEST, H2, H3, or H4 result existed.
- **Approval:** engineering-fault self-repair authorized by the user's full-rerun instruction.
- **Eligibility impact:** the failed smoke remains ineligible and retained; a new smoke must pass the amended guard before a full run. No scientific metric, selector, or verdict rule changes.

### Amendment A02 — result-figure disambiguation (2026-08-24)

- **Before:** the completed layer curve marked the frozen H3 primary and replication layers, but did not explicitly annotate the distinct layer with maximum controlled added utility.
- **After:** rerender the same frozen JSON/CSV with an annotation for the maximum controlled-gain layer and simultaneous interval, the number of H0-admitted layers, and the unchanged primary/replication markers.
- **Reason:** the formal result has two deliberately different selections—maximum incremental utility and best H3-readiness among H0-admitted layers. The first rendered artifact could visually invite readers to conflate them.
- **Data visible:** all formal results were already complete; no fit, selector, threshold, gate, or numeric artifact changed.
- **Eligibility impact:** visualization-only; the original formal computation remains eligible. The rerendered figure must pass the same artifact contract and completion audit before delivery.
