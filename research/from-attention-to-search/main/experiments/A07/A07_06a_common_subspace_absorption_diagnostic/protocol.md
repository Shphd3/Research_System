# Protocol: A07_06a Conflict-Subspace Absorption Diagnostic

## 0. Approval Snapshot

**Approval status:** Approved by user decision on 2026-06-28 as part of the
submitted A07_06 4GPU audit. The user required both common and conflict
projectors, both raw-gradient and AdamW-update views, and dense-beating as the
strong method guard.

**Purpose:** Test whether rare conflict gradients are absorbed or diluted by a
stable harmful common/rare conflict subspace strongly enough to justify
projected MoE method construction.

**Primary anchor:**
`../../../problem_anchors/07_features_overlap/07_06_projected_common_rare_conflict_splitting_anchor.md`

**Anchor decision question:** Does conflict-subspace projection target a real
common/rare gradient-dilution mechanism?

**Anchor physical prior tested:** frequent common updates can dominate shared
experts and dilute rare conflict gradients.

**Anchor core model term tested:** \(\alpha_R^{\mathrm{conflict}}=
\|P_{\mathrm{conflict}}u_R\|^2/(\|u_R\|^2+\epsilon)\) for both raw gradients
and AdamW-update directions.

**Anchor falsifier:** \(P_{\mathrm{conflict}}\) is unstable, or rare updates do
not project into it above shuffled / nuisance controls.

**Experiment role:** operationalization / mechanism diagnostic.

**Primary metric from anchor:** rare conflict-subspace update fraction
`rare_conflict_subspace_fraction`.

**Claim boundary from anchor:** Passing only justifies A07_06b method
construction. It does not prove MoE utility.

**Minimal setup:** controlled neural common/rare surface aligned with A07_04,
same train/eval split style, saved checkpoints, and reconstructable AdamW
preconditioned update directions for selected blocks.

**Basic configuration:** estimate raw-gradient and AdamW-update conflict
projectors after common warmup; measure rare update absorption; compare against
shuffled labels, random projector, frequency/position nuisance controls, and
norm controls.

**Conditions to run:** common projector, shuffled common projector, random
rank-matched projector, nuisance projector if the dataset exposes frequency or
position variables, and rare-update measurements.

**Pass:** \(P_{\mathrm{conflict}}\) is stable and rare
\(\alpha_R^{\mathrm{conflict}}\) is materially above all controls in the
rare-underlearning window for raw gradients and compatible for AdamW-update
directions.

**Fail:** projector drift is high, rare conflict absorption is control-matched,
or the signal is explained by norm / nuisance variables.

**Insufficient:** update directions cannot be reconstructed, rare examples are
not underlearned, or projector rank selection is unstable.

**Cannot claim:** projected MoE utility, dense-beating rare learning,
real-DCLM transfer, or semantic expert specialization.

**Approval decision:** user should approve, revise, or park this diagnostic
before any execution.

## 1. Anchor Alignment

**Decision question:** Is conflict-subspace projection a valid target for A07
common/rare conflict splitting?

**Physical prior tested:** frequent common update directions can dilute rare
conflict gradients.

**Core model term tested:** \(\alpha_R^{\mathrm{conflict}}\) and projector
stability.

**Falsifier:** no stable conflict projector or no rare absorption above
controls.

**Claim boundary:** diagnostic only; no method claim.

## 2. Tested Hypothesis

Rare updates in the A07 neural common/rare surface have elevated mass in a
stable conflict projector during the rare-underlearning window, consistent with
frequent common updates diluting the rare conflict gradient.

## 3. Rival Explanations

1. Rare examples are hard because of data scarcity, not conflict-subspace
absorption.
2. Projection signal is caused by update norm rather than direction.
3. Projection signal is a frequency, position, or load artifact.
4. The common projector is unstable, so freezing it would be invalid.
5. The chosen rank \(k\) manufactures a signal.

## 4. Data / Model / Algorithm / Objective

**Data:** controlled neural common/rare task compatible with A07_04. Training
is imbalanced; evaluation includes balanced common and rare splits.

**Model:** same small neural MoE/dense-compatible surface used for A07_04, or a
direct successor that preserves common/rare labels and per-expert gradient
audit.

**Algorithm:** train or load the baseline checkpoint; estimate common and
conflict projectors from raw gradients and AdamW-update directions; measure
rare update projection and controls.

**Objective:** standard task loss. No router or optimizer intervention is
introduced in this diagnostic.

## 5. Conditions, Seeds, And Checkpoints

Use one smoke seed first. Scale to 8 seeds only if the smoke run reconstructs
updates and produces stable rare/common validation.

Checkpoints: common warmup checkpoint, rare-underlearning checkpoint, and one
later checkpoint. If only one checkpoint is affordable, use the
rare-underlearning checkpoint.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Raw conflict projector | harmful common/rare direction | \(P_{\mathrm{conflict}}^{raw}\) | primary diagnostic object | primary | stable and rare conflict mass high | unstable or no rare mass | gradient reconstruction fails | `tables/projector_diagnostic.csv` |
| AdamW conflict projector | actual update-space direction | \(P_{\mathrm{conflict}}^{adam}\) | checks optimizer-space target | primary/guard | compatible with raw conflict signal | contradicts raw signal | optimizer state unavailable | `tables/projector_diagnostic.csv` |
| Common projector | coarse common-subspace rival | \(P_C\) | tests whether conflict is sharper than common | secondary | weaker than conflict projector | common explains all signal | hidden/update samples too small | `tables/projector_diagnostic.csv` |
| Shuffled conflict projector | label artifact rival | shuffled \(P\) | guards against arbitrary rank effect | guard | rare mass lower than real conflict \(P\) | matches real \(P\) | shuffle invalid | `tables/projector_controls.csv` |
| Random rank-matched projector | rank / norm rival | random \(P\) | guards against high-dimensional mass | guard | rare mass lower than real conflict \(P\) | matches real \(P\) | rank unstable | `tables/projector_controls.csv` |

## 6. Primary Metric

The primary metric is:

\[
\alpha_R^{\mathrm{conflict}}=
\frac{\|P_{\mathrm{conflict}}u_R\|^2}{\|u_R\|^2+\epsilon}.
\]

It decides the diagnostic because projected MoE is only mechanism-aware if rare
updates actually use the harmful conflict subspace more than controls.

Operational pass threshold:

- projector drift \(\|P_C(t)-P_C(T_0)\|_2 \leq 0.30\) over the audit window, or
  a pre-registered equivalent stability statistic if the implementation uses
  covariance overlap rather than spectral norm;
- rare \(\alpha_R^{\mathrm{conflict}} \geq 0.15\);
- rare \(\alpha_R^{\mathrm{conflict}}\) at least `1.5x` the strongest shuffled / random / nuisance
  control.

These thresholds are decision gates, not universal claims.

## 7. Secondary Metrics

Secondary metrics: common top-\(k\) spectral energy, effective rank, update norm,
rare loss, common loss, route load, active experts, and per-block projection
fractions for router, expert input, and output blocks.

## 8. Known Good / Known Bad / Known Confusing Cases

**Known good:** A07_05 showed nonzero rare overlap with a common-update
projector on a controlled surface.

**Known bad:** a random rank-matched projector should not match the real common
projector.

**Known confusing:** high projection overlap with no rare-loss harm; stable raw
gradient projector but unstable AdamW update projector; rare absorption
explained by load or frequency controls.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Data audit | is rare underlearned while common is learned? | common/rare loss table | pass if common is learned and rare remains worse | `tables/loss_window.csv` | summary table |
| Update reconstruction | can \(u_t\) be measured for selected blocks? | optimizer/update logs | pass if block updates are finite and norm-stable | `tables/update_norms.csv` | detailed |
| Projector stability | can \(P_C\) be frozen? | checkpoint projector overlap | pass by stability threshold | `figures/projector_drift.png` | summary if central |
| Absorption audit | do rare updates use \(P_{\mathrm{conflict}}\)? | projection table | pass by primary threshold | `figures/update_projection_fraction.png` | summary |
| Control audit | do nuisance projectors explain the signal? | control projection table | fail if strongest control matches real \(P_C\) | `tables/projector_controls.csv` | detailed |

## 10. Algorithm Specification, If Nontrivial

**input:** checkpoints, common/rare batches, feature labels for audit, selected
parameter blocks, AdamW optimizer state, and control labels.

**parameters:** projector rank rule, selected blocks, audit checkpoint window,
and control projectors.

**intermediate variables:** common update covariance, conflict-gradient
covariance, \(P_C\), \(P_{\mathrm{conflict}}\),
\(\alpha_R^{\mathrm{conflict}}\), projector drift, update norm, and control
projection fractions.

**steps:**
1. Identify the rare-underlearning checkpoint window.
2. Reconstruct or sample preconditioned AdamW update directions for common and
   rare batches.
3. Estimate \(P_C\) from common updates and estimate \(P_{\mathrm{conflict}}\)
   from common directions whose cosine with rare updates is negative.
4. Choose rank \(k\) by fixed energy threshold or pre-registered rank.
5. Measure projector drift across checkpoints.
6. Measure rare \(\alpha_R^{\mathrm{conflict}}\) and all controls.
7. Report pass / fail / insufficient before any method construction.

**outputs:** projector diagnostic table, control table, update projection
figure, and pass/fail decision.

**debug artifacts:** update norm table, spectral energy table, and per-block
projection table.

**pass conditions:** all approval-snapshot pass criteria hold.

**fail conditions:** projector instability or control-matched rare absorption.

**failure reasons:** no stable common projector, no rare absorption, nuisance
shortcut, update reconstruction failure, or rank artifact.

## 11. Success / Failure / Insufficient Evidence

**Success:** the diagnostic gate passes and A07_06b becomes eligible for
execution.

**Failure:** rare absorption is absent, unstable, or explained by controls.
Projected MoE should be parked or redesigned.

**Insufficient evidence:** implementation cannot measure preconditioned updates
or the rare-underlearning window is not present.

## 12. What This Cannot Claim

This protocol cannot claim that projection improves MoE, that routing has
functional value, or that the mechanism transfers to real DCLM. It only decides
whether A07_06b is a justified method-construction test.

## 13. Review Notes And Protocol Changes

User approved the diagnostic as part of the combined 4GPU audit on 2026-06-28.
The submitted job is `pt-gwnh6l71`.
