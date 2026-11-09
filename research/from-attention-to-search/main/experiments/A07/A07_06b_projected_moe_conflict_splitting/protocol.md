# Protocol: A07_06b Projected MoE Conflict Splitting

## 0. Approval Snapshot

**Approval status:** Approved and submitted on 2026-06-28. The user explicitly
set four requirements: the method must address frequent common updates
diluting rare conflict gradients; both global/common and conflict-projected
variants should be tested; both raw-gradient and AdamW-update views should be
considered; strong support must beat dense.

**Purpose:** Test whether conflict-subspace projection in the router and
selected expert update path prevents frequent common updates from diluting rare
conflict gradients, reduces common/rare gradient conflict, and beats dense rare
loss.

**Primary anchor:**
`../../../problem_anchors/07_features_overlap/07_06_projected_common_rare_conflict_splitting_anchor.md`

**Anchor decision question:** Does projected common/rare splitting reduce
routing-weighted conflict enough to improve rare loss?

**Anchor physical prior tested:** frequent common updates can monopolize shared
experts and dilute rare conflict gradients; projecting only the harmful
conflict component can protect rare learning while preserving useful sharing.

**Anchor core model term tested:** \(\Delta\mathcal{C}_{C,R}\) with rare-loss and
common-loss guards.

**Anchor falsifier:** projection reduces geometry metrics but does not reduce
conflict and rare loss under matched guards.

**Experiment role:** method construction, gated by A07_06a diagnostic evidence.

**Primary metric from anchor:** conflict reduction
\(\Delta\mathcal{C}_{C,R}\) versus `random_top1_moe`, with rare-loss improvement
as a required guard.

**Claim boundary from anchor:** Passing supports projected MoE on the tested
controlled surface only. It does not prove real-DCLM specialization.

**Minimal setup:** A07_04-compatible neural common/rare surface with dense,
random top-1, centered split, projected-router, projected-router-plus-update,
and oracle guards.

**Basic configuration:** freeze \(P_C\) after warmup; route projected conditions
with \(h_\perp=(I-P_C)h\); optionally suppress selected preconditioned expert
updates with \(\tilde U=r_t(U-\rho UP_C)\).

**Conditions to run:** dense shared, random top-1 MoE, centered unsupervised
split MoE, projected-router MoE, projected-router-plus-update MoE, and oracle
split as a positive control.

**Pass:** projected-router-plus-update reduces
\(\mathcal{C}_{C,R}\), improves \(L_R\) versus random top-1 and centered split,
preserves \(L_C\), satisfies load guards, and beats dense shared rare loss or
closes the dense gap within the pre-registered tolerance.

**Fail:** conflict does not fall, rare loss does not improve, common loss
regresses, or gains are explained by load / capacity mismatch.

**Insufficient:** A07_06a gate fails, projector cannot be frozen, oracle guard
does not solve the task, dense comparison is not matched, or variance hides the
comparison.

**Cannot claim:** semantic experts, real-DCLM transfer, scaling, or that route
purity / load balance proves utility.

**Approval decision:** submitted as a 4GPU ACP audit job `pt-gwnh6l71`.

## 1. Anchor Alignment

**Decision question:** Does projection turn measured common/rare conflict into
functional rare-loss improvement?

**Physical prior tested:** common high-gain/update directions can monopolize
rare learning.

**Core model term tested:** \(\mathcal{C}_{C,R}\) as mediator between expert
sharing and rare loss, plus update projection fraction as a mechanism guard.

**Falsifier:** projected conditions do not improve both conflict and rare loss.

**Claim boundary:** controlled-surface method evidence only.

## 2. Tested Hypothesis

Projected router input plus selected update-space suppression reduces
common/rare conflict more than centered routing alone and improves rare loss
enough to beat the dense boundary without unacceptable common loss regression.

## 3. Rival Explanations

1. Projection only changes load, not functional conflict.
2. Rare loss changes because of capacity or parameter count mismatch.
3. Coarse common projection is sufficient; conflict projection adds no value.
4. Router-only projection is sufficient; update suppression adds no value.
5. Update suppression harms common learning and transfers the problem.
6. Dense shared training remains better, so MoE partition has no functional
   value on this surface.
7. The oracle split works only because labels hand-code the answer.

## 4. Data / Model / Algorithm / Objective

**Data:** controlled neural common/rare binary or sequence task from A07_04 or
its direct successor. Train distribution is imbalanced; evaluation is balanced.

**Model:** matched dense and top-1 MoE conditions. Projected MoE uses the same
expert count and capacity as baselines.

**Algorithm:** estimate and freeze both coarse common projector \(P_C\) and
harmful conflict projector \(P_{\mathrm{conflict}}\) after warmup. Use
\((I-P_C)h\) for the coarse control and \((I-P_{\mathrm{conflict}})h\) for the main
projected router logits. For the full projected condition, suppress the
input-side conflict component of selected preconditioned expert updates.

**Objective:** standard task loss with confidence/group gate \(r_t\) for
already-learned common examples in the update-suppression condition. This gate
is required because the mechanism claim is that frequent common updates dilute
rare conflict gradients. Do not use feature labels for deployable routing
except in oracle.

## 5. Conditions, Seeds, And Checkpoints

Use one smoke seed to validate projector freezing, load, and loss. Full run:
8 seeds matching A07_04 unless resource constraints require a pre-approved
smaller seed count.

Checkpoints: step 0 / post-warmup, early training, final. Save enough state to
compute route distributions and per-expert gradients.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dense shared | dense rare-loss boundary | dense baseline rival | checks whether MoE adds value | guard | projected condition closes gap | dense remains clearly better | unmatched capacity | `tables/common_rare_loss_guard.csv` |
| Random top-1 MoE | ordinary route baseline | baseline \(\mathcal{C}_{C,R}\) | primary comparison | primary baseline | projected improves | projected no better | random collapse invalid | `tables/common_rare_gradient_conflict.csv` |
| Centered split MoE | prior best weak split | centered-router rival | tests whether projection adds beyond centering | primary baseline | projected improves | centered matches projected | load mismatch | `figures/conflict_vs_rare_loss.png` |
| Common-projected-router MoE | coarse common projection | \(h_\perp=(I-P_C)h\) | tests whether common projection is enough | secondary/control | weaker than conflict method | matches or beats conflict method | common projector invalid | `tables/route_table.csv` |
| Conflict-projected-router MoE | route conflict projection only | \(h_\perp=(I-P_{\mathrm{conflict}})h\) | isolates conflict-router effect | primary/secondary | conflict falls | no conflict reduction | projector invalid | `tables/route_table.csv` |
| Conflict-projected-router-plus-update MoE | full intervention | \(\tilde U=r_t(U-\rho UP_{\mathrm{conflict}})\) | tests update-space mechanism and common-frequency gate | primary | conflict falls and rare beats dense | loss guard fails | update projection not implemented | `figures/update_projection_fraction.png` |
| Oracle split MoE | task solvability | positive control | ensures rare learning is possible | guard | solves rare task | oracle fails | labels invalid | `tables/common_rare_loss_guard.csv` |

## 6. Primary Metric

The primary metric is:

\[
\Delta\mathcal{C}_{C,R}
=\mathcal{C}_{C,R}^{\mathrm{random\ top1}}
-\mathcal{C}_{C,R}^{\mathrm{projected}}.
\]

It decides whether the intervention reduces the mechanism target rather than
only changing load. It is not sufficient by itself; rare loss must also improve.

Pass thresholds:

- \(\Delta\mathcal{C}_{C,R}>0\) versus random top-1 and centered split;
- \(L_R\) improves versus random top-1 and centered split;
- \(L_C\) regression is within pre-set tolerance, suggested initial tolerance
  `<= 0.02` absolute loss unless the existing A07 surface uses a different
  scale;
- max load and active experts remain within the baseline guard range;
- strong support: projected full condition beats dense shared rare loss, or is
  not worse by more than a pre-set tolerance while clearly improving conflict,
  common preservation, and load guards.

## 7. Secondary Metrics

Secondary metrics: rare accuracy, common accuracy, max load, active experts,
route entropy, update projection fraction before/after suppression,
projector drift, effective rank, per-expert gradient cosine, and
gain-weighted common top-\(k\) mass if singular spectra are available.

## 8. Known Good / Known Bad / Known Confusing Cases

**Known good:** oracle split should reduce rare loss strongly.

**Known bad:** random top-1 should not be treated as evidence of utility merely
because it balances load.

**Known confusing:** conflict falls while rare loss does not; rare loss
improves but common loss regresses; projected-router helps but update
suppression hurts; dense shared remains better despite lower conflict.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| A07_06a gate | is projected method justified? | diagnostic summary | pass only if user-approved gate holds or user explicitly waives it | `tables/projector_diagnostic.csv` | protocol note |
| Projector freeze | does \(P_C\) remain usable during method run? | projector drift | fail if drift exceeds diagnostic tolerance | `figures/projector_drift.png` | detailed |
| Router audit | does conflict-projected \(h_\perp\) change routes without collapse? | route table / load table | pass if load guard holds | `tables/route_table.csv` | summary if central |
| Conflict audit | does conflict fall? | gradient conflict table | pass by primary metric | `tables/common_rare_gradient_conflict.csv` | summary |
| Loss guard | does rare improve without common damage? | loss table | pass only if rare and common guards hold | `tables/common_rare_loss_guard.csv` | summary |
| Update audit | does suppression reduce \(P_{\mathrm{conflict}}u_t\)? | projection fraction table | pass if conflict fraction falls in full condition | `figures/update_projection_fraction.png` | detailed/summary |

## 10. Algorithm Specification, If Nontrivial

**input:** training data, common/rare audit labels, model config, warmup
checkpoint, frozen projectors \(P_C\) and \(P_{\mathrm{conflict}}\), optimizer
state, and selected parameter blocks.

**parameters:** projector rank \(k\), rank selection rule, suppression strength
\(\rho_{\max}\), confidence or group gate \(r_t\), selected blocks, seeds, and
checkpoint schedule.

**initial fixed settings:** choose \(k\) from A07_06a; use a single
\(\rho_{\max}\) value, suggested `0.5`, for the first approved run; use router
projection for all projected conditions; apply update suppression after AdamW
preconditioning only to selected expert input-side blocks in the full
condition.

**intermediate variables:** \(h_\perp\), route logits, \(q_{f,e}\), \(g_{f,e}\),
\(\mathcal{C}_{C,R}\), \(U_tP_C\), \(\tilde U_t\), \(L_R\), \(L_C\), load, and active
experts.

**steps:**
1. Warm up baseline until common performance is stable.
2. Freeze \(P_C\) and \(P_{\mathrm{conflict}}\) using the A07_06a-approved
   estimator and rank.
3. Train matched conditions.
4. For common-projected-router MoE, compute router logits from \((I-P_C)h\).
5. For conflict-projected-router MoE, compute router logits from
   \((I-P_{\mathrm{conflict}})h\).
6. For conflict-projected-router-plus-update MoE, compute AdamW preconditioned update
   \(U_t\) for selected blocks and replace it with
   \(\tilde U_t=r_t(U_t-\rho U_tP_{\mathrm{conflict}})\) before weight decay.
7. Save checkpoints and audit route distributions, gradient conflict, loss,
   load, and update projection.
8. Apply pass / fail / insufficient rules before writing any stronger claim.

**outputs:** protocol-compliant summary, detailed evidence ledger, conflict
table, loss guard table, route table, load table, update projection table, and
central figures.

**debug artifacts:** projector drift, update norms, per-block suppression
fractions, and seed-level tables.

**pass conditions:** primary metric and all required guards pass.

**fail conditions:** conflict or rare loss does not improve, common loss
regresses, dense boundary remains unaddressed, or load/capacity mismatch
explains gains.

**failure reasons:** invalid diagnostic gate, wrong projector, router collapse,
update suppression too strong, no true common/rare conflict, data scarcity, or
dense baseline advantage.

## 11. Success / Failure / Insufficient Evidence

**Success:** full conflict-projected condition reduces conflict and rare loss
versus random and centered baselines, preserves common loss, satisfies load
guards, and beats dense rare loss or closes the dense gap within tolerance.

**Failure:** projected method does not improve conflict and rare loss together,
or it transfers harm to common examples.

**Insufficient evidence:** A07_06a gate fails, oracle control fails, variance is
too high, or implementation cannot verify update suppression.

## 12. What This Cannot Claim

This protocol cannot claim real-DCLM utility, semantic expert specialization,
or scaling. It cannot claim that projection is generally better than dense
training unless the dense boundary passes. It cannot use route NMI, load
balance, or conflict reduction alone as evidence of functional specialization.

## 13. Review Notes And Protocol Changes

Approved and submitted on 2026-06-28 as ACP job `pt-gwnh6l71`. Record full
results in `summary.md` and `detailed.md`; do not update the anchor from smoke
or partial logs.
