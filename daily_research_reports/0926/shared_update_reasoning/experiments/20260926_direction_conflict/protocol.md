# Protocol: controlled local directional conflict

## 0. Approval Snapshot

Document status: APPROVED_FOR_DELEGATED_EXPLORATORY_IMPLEMENTATION_SMOKE_AND_FULL.
Authorization: the researcher explicitly requested completing the theory and initial experimental support and submitting experiments without their further review. The existing session fixes four-H100 Reserved; current envelope resolves image shphd-lite-0911. Scope: one bounded allocation, implementation, local smoke,152 real-model virtual branches and aggregation. No continuous training, external publication, or confirmation-set unsealing.
Primary [Anchor](anchor.md). This continues the researcher-selected shared-update problem. The requirement to ask for a new Focus or block-by-block review is superseded by the explicit delegated execution request; no Focus is created, no AI choice is mislabeled as an individually confirmed human judgment. A–G are operationalized by Codex under that delegation. Scientific outcome and final interpretation are not pre-approved.
Role: root-cause audit of a controlled sufficient mechanism. Primary M compares target-oriented versus matched reflection. Cannot claim naturally occurring data interference or SAE identification. Frozen identity is recorded by execution registration before any new model readout.

## 1. Terminology / Definitions

Local harm = updated minus baseline target next-token loss. Source learning = baseline minus updated source readout loss. Construction gradient uses fit records; readout uses test records. A reflected update is deliberately engineered in parameter space and is not the ordinary gradient of unchanged source data. The source and target are two distinct domains from computing, mathematics, physics, biology.

## 2. Anchor Alignment

Change the orientation relevant to target prediction while holding parameter norm, distance from the ordinary source step, and source first-order improvement equal between the primary treatment/control. This tests directional sufficiency and transfer to other records. The general relation between input and error signals is derived separately; the real-model experiment does not identify why original data acquired those signals.

## 3. Tested Hypothesis

H1: target-oriented reflection causes target readout harm beyond matched reflections while source learning remains positive. Removing the adverse component reduces harm more than uniform shrinkage of the same norm. All effects must reproduce at the two frozen step sizes.

## 4. Rival Explanations

Generic update size/source-progress explanation: matched reflection controls. Generic shrinkage explanation: shrink-to-rescue-norm control. Construction-panel overfit: separate readout records, with explicit prior exposure limitation. Curvature/numerics: half step, direct nonlinear readout, zero-repeat/cache and first-order diagnostics. These controls do not match every representation perturbation or prove natural semantic causality.

## 5. Data Construction And Provenance

Reuse `/data/250010109/MoE_Router/experiments/20260925_sae_domain_activation/selected.jsonl`:1024 natural-text records,256 tokens, four domains,128 fit and128 test per domain, two subfields each. Exact cached input/targets and first128-source fit gradients are from `/data/250010109/MoE_Router/experiments/20260926_atom_mechanism/runtime/source_<domain>/`. Registration hashes every input. No new sample filtering, target relabeling, record selection by harm, or synthetic text. Test records were exposed in prior analyses; no untouched confirmation claim or article-level independence. Source workers reuse the same512 test records, not2048 independent texts.

## 6. Learning Task And Permitted Supervision

Next-token cross-entropy at positions14,30,...,254 with next positions as targets.16 targets per record; record loss is their mean; domain mean equally weights128 records. Construction uses only fit gradients and fixed random seeds. Readout target derivatives are used only for diagnostics after deltas are fixed, never to construct them.

## 7. Model / Architecture And Frozen Variants

Fresh S7 sidecar, exact21,000,000,000 training tokens; checkpoint state hash `edd781c8f747477e9f236128d26423d435c800d37da2d446c85e4a6ebc206f33`. Loader and state are the same as the predecessor. Only virtual deltas to `blocks.7.attn.o.weight`, shape1024x2048, FP32. Frozen BF16 upstream caches; FP32 output projection, residual, norm2, gate/up/SiLU/down, final norm and head. SAE and all model parameters/buffers remain fixed; SAE is not used as the intervention selector.

## 8. Training Objective And Optimization

No optimizer, cumulative training, checkpoint mutation or new training implementation. All branches reset to the base state; training TensorBoard schedules are not applicable. Let u=gA/||gA||F, v=gB/||gB||F, c=<u,v>F. gamma=rho*||W||F for rho=1e-4 and5e-5. Require0<c<1/sqrt(2) for all twelve pairs; if any pair fails, preserve the reason and stop as INSUFFICIENT_CONSTRUCTION, without selecting a subset or altering the rule. Use double precision for constructing/matching directions; cast final deltas to FP32 for the qualified model path.

## 9. Conditions, Seeds, And Checkpoints

Per source/step: full=-gamma*u; for each other target, target_reflection=gamma*(-u+2*c*v); three matched_reflections from seeds17,29,43; rescue=gamma*(-u+c*v); shrink=target_reflection*sqrt(1-c^2). For each control, draw standard-normal tensor with seed2026092600+10000*source_index+100*target_index+seed; orthogonalize against u and w=(v-c*u)/sqrt(1-c^2), normalize to r; q=c*u+sqrt(1-c^2)*r; control=gamma*(-u+2*c*q). All controls have the same norm, full-step distance and source derivative as target_reflection. Rescue is unscaled orthogonal deletion of its adverse v component. Shrink matches rescue parameter norm.

19 branches/source/step,38/source,152 total. Each reads all512 records; baseline is additional. No self-target reflection. Report all cross pairs and both steps, no best-step selection.

## 10. Primary Metric And Frozen Analysis Plan

For ordered pair A,B, target harm H is mean_B(loss_after-loss_base). Primary M_AB=H_target_reflection-mean3(H_matched_reflection). M is equal mean over twelve ordered pairs. Rescue contrast Z_AB=H_shrink-H_rescue; positive means targeted deletion reduces harm more than uniform shrinkage. T is equal mean target-reflection harm over twelve pairs. Compute separately for both steps.

Use2000 paired record bootstrap draws, seed2026092601, stratified within target domain/subfield; reuse the same record indices across every source/branch. Each pair and each control seed receive equal weights; domains have equal counts. Percentile two-sided95% intervals condition on checkpoint, construction gradients, all selected records and controls. Pairs/seeds/steps are not independent replications. Per-cell intervals are descriptive, not simultaneous claims. No outlier removal or omitted failures.

Source qualification: every registered branch's own-source readout help has lower95% bound>0. SUPPORT requires qualification and M,T,Z lower bounds>0 at both steps, with all engineering guards passed. NON_SUPPORT requires qualification and M upper bound<=0 at both steps. Otherwise INSUFFICIENT/HETEROGENEOUS; numerical failures INELIGIBLE. A positive M without target harm does not support harmful interference. No secondary diagnostic can rescue a gate.

## 11. Secondary Metrics And Guards

Save per-record harm, first-order loss prediction <dL/da,deltaW*c>, native displacement norm, actual source readout help, fitted gradient cosines and analytic matched quantities. Report full-update harm and harm fractions descriptively, without selecting negative records. Check match relative error<=2e-6 for norm, distance, source derivative and rescue/shrink norm, and abs(dot)<=2e-6 for constructed orthogonality. Parameter norm matching is not representation norm matching.

## 12. Known Good / Known Bad / Known Confusing Cases

Analytic squared-loss model W=0, unit inputs with overlap alpha in{0,.5,1}, unit residuals with inner product beta in{-1,0,1}, eta in{.01,.005}: exact target delta=-eta*alpha*beta+.5*eta^2*alpha^2. Check all18 cases to1e-12; orthogonal inputs give zero effect; beta<0 with positive overlap gives harm; beta=0 can have positive finite-step curvature despite zero first-order effect. Also test reflection equality and inequalities on random32-dimensional unit vectors at cosines .1,.3,.6. This validates derivation/implementation, not empirical natural-data prevalence.

## 13. Scientific Procedure And Stage Contracts

1. Freeze exact documents, scripts and source identities; run analytic guards. Failure stops model work.
2. Local engineering smoke: source computing, same full fit gradients, first two readout records per domain/subfield (16 total), all38 branches. Require finite losses, matching guards, repeat/reset exactly zero, base cache agreement atol2e-5/rtol2e-6 and unchanged model/buffers. Its scientific signs are not selection criteria.
3. One four-H100 Reserved allocation, one independent source worker per GPU,38 branches each. Repeat identity/finite/matching/cache/reset checks. No source worker may silently skip a branch. Runtime ceiling3600seconds.
4. Aggregate only four complete workers; write Summary/Detailed, figure, lineage and source hashes. If queued beyond bounded startup, preserve submitted state; do not fabricate completed real-model evidence.

## 14. Algorithm, Output, And Provenance Contract

Execution root `/data/250010109/MoE_Router/experiments/20260926_direction_conflict`; scripts and raw arrays there. Worker `scripts/run_worker.py`; construction and analytic tests `scripts/core.py`; aggregate `scripts/analyze.py`; runtime `scripts/runtime.sh`; launch `scripts/run_four_h100.sh`. Registration records all source/target gradient and cache hashes, loader/runtime/model-source identities and current documents/scripts. Preserve failures in separate attempt folders. Report token predictions/branch and actual numeric dtype, not invented optimizer steps.

Resource profile `h100-4-reserved`, image `shphd-lite-0911`, ACP, one node/four independent processes, at most4 GPU-hours. Submit through repository envelope template after dry run and smoke. Receipt records actual image, devices, logs and monitoring owner. No resource fallback. Authoritative new records live in this requested dated collection's experiment folder; prior experiment copies remain copies.

## 15. Success / Failure / Insufficient Evidence

Use only section10 rules. SUPPORT establishes constructed local directional sufficiency under stated conditions; NON_SUPPORT rejects this construction's expected transfer contrast; insufficient evidence identifies the failed or uncertain gate. None establishes a new natural-data selection rule or automatically launches a follow-up.

## 16. What This Cannot Claim

No claim that source-data SGD spontaneously generates reflected updates; that natural domains conflict on average; that language semantics, input overlap alone or SAE overlap causes harm; that independent examples at another checkpoint behave the same; or that isolation/router training helps. No trained model is produced. Source progress matching is exact to first order on fit, with independent source success verified rather than assumed.

## 17. Block Confirmation, Freeze, And Amendment Ledger

A–G are AI-operationalized under explicit delegated implementation/smoke/full authorization; cross-block audit PASS before registration. Human final mechanism judgment remains Unknown. Existing question and previous evidence were read; no independent Focus was invented to satisfy a workflow. Freeze occurs in `registration.json` before new model readouts. Any later science change requires a visible amendment and eligibility reassessment; implementation-only correction preserves failed attempts and prior hashes. Source cache panels are historically exposed and reported as such.
