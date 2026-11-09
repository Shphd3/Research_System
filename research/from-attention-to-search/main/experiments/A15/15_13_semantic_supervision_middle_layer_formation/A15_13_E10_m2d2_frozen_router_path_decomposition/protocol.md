# Protocol: A15_13_E10 M2D2 Frozen Router Forward-Path Decomposition

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_FULL_RUN
Approval status: HUMAN_APPROVED_EXPANDED_DIAGNOSTIC_2026-09-02
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: IMPLEMENTATION, FULL CONFIRMATION EVALUATION, ANALYSIS, CURATED RESULT WRITING
Design frozen at: 2026-09-02 Amendment C002
Purpose: locate why the learned semantic Router failed to recover the positive hard-Oracle language-modeling value
Primary Anchor: 15_13_04_m2d2_causal_lm_semantic_routing_anchor.md
Experiment role: evaluation-only root-cause audit
Primary metric: paired equal-domain confirmation NLL recovery from frozen learned hierarchical and flat checkpoints
Treatment and controls: independently crossed parent index, parent coefficient, child index, and child coefficient for hierarchy; index and coefficient for flat routing
Changed variables: inference-time expert index and coefficient only
Held fixed: E07 checkpoint, model parameters, data, causal state, experts, language head, token mask, batch order, and confirmation examples
Pass branches: INDEX_DOMINANT, COEFFICIENT_DOMINANT, JOINT, or NEITHER_RECOVERS, determined by the frozen paired decomposition below
Insufficient: either seed, any 2x2 cell, required intervention, identity guard, or paired token array is missing
Cannot claim: representation reshaping, a new trained method, deployment value, or that the gold route is operationally available
```

The confirmed active Focus is [focus_m2d2_causal_lm_semantic_routing.md](../../../../focus/focus_m2d2_causal_lm_semantic_routing.md). This protocol implements its sole no-retraining diagnostic and does not open a fourth core experiment.

## 1. Terminology And Definitions

An **expert index** is the parent or child LoRA expert selected at each causal prediction position. `P` uses the corresponding learned Router argmax; `G` forces the document's gold coarse or local fine domain. An **expert coefficient** scales one selected residual. `L` uses the learned probability assigned to that selected expert; `1` uses coefficient one. Shared LoRA remains unscaled in every cell.

The hierarchy independently applies these two choices to the parent and child paths, producing 16 cells written as parent-index/parent-coefficient/child-index/child-coefficient. The flat Router has the four `PL`, `P1`, `GL`, and `G1` cells. No gradient, optimizer update, checkpoint selection, or parameter mutation is permitted.

## 2. Anchor Alignment

E07 established that semantic supervision increased route-label agreement and made child experts non-interchangeable but worsened held-out NLL versus the architecture-identical task-only Router. E08 established positive hard-Oracle headroom. The Anchor leaves expert-index error, probability attenuation, and expert-training responsibility confounded. This audit changes only the two inference-time factors needed to separate them.

The strongest rival is training responsibility: even `G1` may remain worse than the E07 task-only checkpoint and E08 hard Oracle because the learned-semantic experts were optimized under routed, probability-scaled responsibility.

## 3. Tested Hypothesis And Typed Outcomes

Let \(N_{xy}\) be equal-domain confirmation NLL for index mode \(x\in\{P,G\}\) and coefficient mode \(y\in\{L,1\}\). Define the exact two-player Shapley decomposition of total recovery \(N_{PL}-N_{G1}\):

\[
\phi_{index}=\frac{(N_{PL}-N_{GL})+(N_{P1}-N_{G1})}{2},\qquad
\phi_{coefficient}=\frac{(N_{PL}-N_{P1})+(N_{GL}-N_{G1})}{2}.
\]

These sum exactly to total recovery for flat routing. For hierarchy, use the same exact Shapley definition over four players: parent index, parent coefficient, child index, and child coefficient. Each player's contribution is the average NLL reduction when that one factor is repaired over all eight settings of the other three factors; the four contributions sum to `PLPL` minus `G1G1`. Report the largest positive contributor only when both seeds agree and its paired pooled interval excludes zero. If repair is negative or seed directions disagree, report the signed result rather than forcing a dominant-mechanism label.

The factorial interaction \((N_{PL}-N_{GL})-(N_{P1}-N_{G1})\) is reported separately. It does not invalidate the exact Shapley accounting.

## 4. Data And Confirmation Boundary

Reuse the SHA-recorded E07 full-run M2D2 confirmation tensors: 512 non-overlapping 256-token windows per each of nine fine domains, with positions 64--255 contributing 192 next-token losses. Coarse and fine names remain absent from input. Gold domain integers enter only the forced-index diagnostic cells. The same row order and token mask must match all four cells, both seeds, E07 task-only, and E08 hard Oracle byte-for-byte.

No training, development selection, threshold fitting, or pseudo-label construction occurs. Confirmation truth is allowed because this is an explicitly Oracle-indexed evaluation diagnostic; it cannot support an operational learned method claim.

## 5. Model, Architecture, And Frozen State

Load the two E07 `LEARNED_SEMANTIC` update-144 checkpoints for seeds 17 and 29. Qwen3-0.6B-Base, language head, block-14 rank-eight shared/parent/child LoRA parameters, parent Router, and child Router are frozen. The original causal Router state at position \(j-1\) remains the only learned input used to score the path predicting token \(j\).

For a gold-index cell, parent probability is the softmax probability assigned to the gold parent; child logits and probability are evaluated inside that gold parent. For wrong-child interventions, the selected child expert is cyclically replaced while its original selected-path coefficient is held fixed, matching E07 intervention semantics.

## 6. Conditions, Seeds, And Interventions

For each E07 learned task-only, learned semantic, and shuffled-label checkpoint and each seed, run all 16 intact hierarchy cells. On `PLPL`, `P1P1`, `GLGL`, and `G1G1`, also run active-child deletion and two within-parent cyclic substitutions. For each E09 flat task-only and flat gold-nine checkpoint and each seed, run all four intact flat cells plus expert deletion and two cyclic substitutions. This gives 232 full confirmation evaluations. Existing E08 hard-Oracle arrays are read-only external references and are not rerun.

`G1` versus E07 task-only determines whether inference-path repair removes the learned-semantic task deficit. `G1` versus E08 hard Oracle measures remaining expert-training/topology gap; it is not part of the Shapley decomposition.

## 7. Frozen Analysis Plan

The observation unit is a packed confirmation window. Compute window NLL by averaging its 192 target-token losses, then average equally over nine fine domains and equally over two seeds. For each paired contrast, draw 10,000 bootstrap replicates by resampling windows independently inside each fine domain while preserving every within-row condition pairing.

Report all four NLL cells, seed values, \(\phi_{index}\), \(\phi_{coefficient}\), their difference, factorial interaction, total recovery, `task-only minus G1`, and `G1 minus hard Oracle`, each with paired 95% intervals. Interventions report changed-minus-intact NLL; positive means the child remains useful. No secondary route or representation metric can change the typed mechanism outcome.

The central figure contains a common-scale four-cell NLL panel and a zero-centered contribution panel with paired 95% intervals. A second figure shows deletion and substitution costs for all cells. Both must name units, seeds, and the lower-is-better direction.

## 8. Scientific Procedure And Guards

1. Verify every registered checkpoint hash, existing E07/E08/E09 reference arrays, data manifest, model cache, and four visible H100 GPUs.
2. Run unit tests that prove `PL` reproduces the existing forward rule, `P1` changes only scaling, `GL` scores and selects the gold path, `G1` uses gold indices with unit coefficients, and wrong-child replacement holds the selected coefficient fixed.
3. Shard one seed-by-cell intact evaluation to each GPU; each shard then runs delete, wrong-one, and wrong-two. Stop on any missing checkpoint, non-finite loss, row mismatch, parameter mutation, or shard failure.
4. Run the frozen paired analysis and completion audit. Do not retry a scientific cell with changed logic after any result is visible.

## 9. Execution And Reproducibility Boundary

Execution uses one reserved ACP worker with four H100 GPUs (`n6ls.iu.i40.4`) and no fallback.

Worker code and raw outputs live under `/data/250010109/MoE_Router/experiments/20260902_a15_13_e10_m2d2_frozen_router_path_decomposition/`. Canonical records live beside this Protocol as `summary.md`, `detailed.md`, `figures/`, and `tables/`. Required raw artifacts are per-token arrays, window arrays, route indices and probabilities, checkpoint/code/protocol hashes, job receipt, logs, analysis JSON/table, figures, and completion audit.

## 10. Success, Failure, And Claim Boundary

An eligible run yields exactly one typed mechanism outcome from Section 3 and a separate residual-gap statement. Missing or mismatched evidence yields `INSUFFICIENT`; it is not repaired by a partial cell or intervention. Even `G1` recovery proves only an inference-time causal decomposition for frozen learned-semantic checkpoints. It cannot prove that a deployable Router knows gold labels, that representations improved, or that a proposed retraining method will work.

## 11. Block Confirmation And Freeze Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A question and boundary | CONFIRMED | Anchor and researcher-approved follow-up |
| B data and provenance | CONFIRMED | E07/E08 frozen confirmation set |
| C task and supervision | CONFIRMED | evaluation-only next-token likelihood |
| D architecture | CONFIRMED | frozen E07 learned-semantic checkpoints |
| E objective and optimization | CONFIRMED | zero updates; no optimizer |
| F comparisons and evidence | CONFIRMED | registered 2x2 and residual references |
| G execution | CONFIRMED | user-selected eight-RTX5090 full audit |

Cross-block consistency: `PASS`. Scientific body frozen before implementation on 2026-09-02. Implementation, full-run evaluation, analysis, and curated result writing are explicitly approved. Any post-start change to cell logic, data, checkpoint, aggregation, uncertainty, or typed outcome rule requires an append-only amendment and an eligibility decision.

## 12. Append-Only Amendments

### C001 — 2026-09-02 — Pre-execution scope reopened

- Trigger: the researcher requested a new review of two experiments before any run.
- Execution audit: no GPU job, scientific cell, result array, or result record exists for E10; only preliminary local implementation and unit-test work exists.
- Superseded detail: the earlier body crosses predicted/gold parent and child paths together. The 0903 meeting plan instead fixes the correct coarse path in every cell and first decomposes only the fine route: predicted versus gold child index crossed with learned versus unit child coefficient.
- Candidate invariant: the parent expert index is gold and its coefficient is one in all four cells; all parameters remain frozen. A full coarse-plus-fine crossing is allowed only as a separately justified follow-up if the fine-only audit is insufficient.
- Statistical alignment: the revised candidate uses 2,000 paired bootstrap replicates as specified by the 0903 plan; any change requires confirmation before execution.
- Eligibility: `NOT_EXECUTABLE` until the researcher confirms the revised four-element plan, exact cell semantics, comparison set, resource profile, and execution scope.

### C002 — 2026-09-02 — Expanded hierarchy and flat decomposition approved

- Trigger: the researcher explicitly requested that every hierarchy level and the flat Router be decomposed, accepted confirmation-label access for this causal audit, selected reserved four-H100 execution, and authorized every full run and evaluation without further approval.
- Hierarchy cells: independently cross parent expert index in `{predicted, gold}`, parent residual coefficient in `{learned probability, one}`, child expert index in `{predicted inside the selected parent, gold}`, and child residual coefficient in `{learned probability, one}`. This gives 16 intact cells per checkpoint. A gold child is always interpreted inside the gold data parent; if the parent index is predicted while the child index is gold, the local child number is retained inside the predicted parent so the parent and child factors remain independently manipulable.
- Hierarchy checkpoints: E07 `LEARNED_TASK_ONLY`, `LEARNED_SEMANTIC`, and `LEARNED_SHUFFLED`, seeds 17 and 29. The original, predicted-index/unit-coefficient, gold-index/learned-coefficient, and gold-index/unit-coefficient paths additionally receive child deletion and both cyclic within-parent substitutions.
- Flat cells: cross predicted versus gold nine-way expert index with learned versus unit coefficient for E09 `FLAT_TASK_R24` and `FLAT_GOLD9_R24`, seeds 17 and 29. The four cells receive expert deletion and two cyclic substitutions.
- References: E08 hard semantic Oracle remains an external upper bound. No trained weight is changed in E10.
- Statistics: use 2,000 paired, within-fine-domain bootstrap replicates. Report seed values and pooled equal-domain values; no pooled interval may hide a seed sign reversal.
- Resource contract: ACP workspace `share-space`, cluster `share-cluster`, one worker, worker specification `n6ls.iu.i40.4`, four visible H100 GPUs, `reserved` quota, normal priority, and no fallback.
- Eligibility: the C001 restriction is superseded. Blocks A-G and cross-block consistency are `PASS`; implementation, full evaluation, analysis, and curated result writing are executable.
