# Protocol: A06_02_01_E03 Feature Drift Margin Boundary

## 0. Approval Snapshot

**Approval status:** approved by user in side conversation; execute minimal
audit.

**Purpose:** quantify whether A06_02_01_E02 preservation holds because observed
feature-center drift stays inside the initial routing-margin buffer.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

**Anchor decision question:** do feature switches or margin failures occur when
feature-center drift consumes the initial distance to the nearest expert
boundary?

**Anchor physical prior tested:** top-1 dot-product routers define finite
linear boundary buffers; preservation should fail when feature centers cross or
nearly consume this buffer unless router movement compensates.

**Anchor core model term tested:** signed boundary distance
\(d_f^{\mathrm{frozen}}(t)\) and dynamic margin \(M_f(t)\).

**Anchor falsifier:** feature switch occurs while frozen boundary distance and
dynamic margin remain positive, or preservation holds despite negative dynamic
margin.

**Experiment role:** root-cause audit / geometric boundary audit.

**Primary metric from anchor:** maximum boundary consumption
\(B_f(t)=1-d_f^{\mathrm{frozen}}(t)/d_f(0)\), guarded by dynamic margin and switch
flags.

**Claim boundary from anchor:** controlled no-position bridge only; this does
not claim real-DCLM behavior or a full perturbation phase diagram.

**Minimal setup:** rerun the A06_02_01_E02 controlled bridge with extra per-feature
boundary metrics at snapshots.

**Basic configuration:** one-layer Transformer + top-1 MoE, 4 experts,
feature slot length 4, no learned absolute positional embedding, route on last
slot token, C0-C3 cells.

**Conditions to run:** pseudo-center init, oracle-center init, random Gaussian
guard.

**Pass:** preserved center-init features keep positive frozen distance and
positive dynamic margin; any degraded/random cases show boundary erosion,
negative dynamic margin, or switch.

**Fail:** switch or routing failure occurs with low boundary consumption and
positive dynamic margin, or high boundary consumption does not affect margin.

**Insufficient:** vector snapshots cannot be reconstructed, feature-center
matching is unstable, or route-only positive control fails.

**Cannot claim:** exact maximum tolerable synthetic perturbation, real-DCLM
preservation, expert utility, or semantic feature specialization.

**Approval decision:** execute this minimal audit now.

## 1. Anchor Alignment

**Decision question:** whether observed feature-center drift stays within the
initial margin boundary.

**Physical prior tested:** routing preservation has a finite geometric drift
budget.

**Core model term tested:** frozen step-0 boundary distance and dynamic margin.

**Falsifier:** routing switches without boundary or margin erosion.

**Claim boundary:** observed training trajectory in the controlled bridge only.

## 2. Tested Hypothesis

**H1 margin-buffer boundary:** correct center initialization preserves because
feature centers do not consume the initial boundary distance.

**H2 router compensation:** router movement can compensate hidden drift, so
dynamic margin remains positive even when frozen boundary consumption is high.

**H3 non-margin failure:** random or failed cases are not explained by feature
center boundary consumption, implying common/load or feature-cloud effects.

## 3. Rival Explanations

- margin buffer explains preservation;
- router movement compensates boundary erosion;
- common or norm drift moves logits without center-boundary crossing;
- feature cloud tails cross before the feature center crosses;
- expert matching artifact.

## 4. Data / Model / Algorithm / Objective

Data/model match A06_02_01_E02: controlled no-position bridge, C0-C3, 4 features,
4 experts, feature slot length 4, route on the last slot token. Objective is
the same slot-end target cross-entropy. The experiment does not introduce a
new training objective.

## 5. Conditions, Seeds, And Checkpoints

Seeds: `20260623` to `20260630`.

Conditions: `pseudo_center_init`, `oracle_center_init`, `random_gaussian_init`.

Checkpoints: `0, 1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1600`.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pseudo-center | successful preservation boundary | margin buffer | main condition | primary | positive distance/margin, no switch | switch without erosion | missing vectors | boundary trajectory |
| Oracle-center | upper bound | pseudo noise guard | checks proxy noise | secondary | same as pseudo | different unexplained boundary | missing | condition table |
| Random Gaussian | failed/weak guard | non-margin failure | distinguishes preservation from task learning | guard | negative margin or switches explain low NMI | clean preservation like center init | missing | scatter/heatmap |

## 6. Primary Metric

For feature \(f\), matched expert \(e(f)\), nearest step-0 competitor \(j^*(f)\):

\[
n_f(0)=w_{e(f)}(0)-w_{j^*(f)}(0).
\]

Initial signed distance:

\[
d_f(0)=\frac{n_f(0)^\top \mu_f(0)}{\|n_f(0)\|+\epsilon}.
\]

Frozen-boundary distance:

\[
d_f^{\mathrm{frozen}}(t)=
\frac{n_f(0)^\top \mu_f(t)}{\|n_f(0)\|+\epsilon}.
\]

Boundary consumption:

\[
B_f(t)=1-\frac{d_f^{\mathrm{frozen}}(t)}{d_f(0)+\epsilon}.
\]

Why it decides: this directly measures how much of the initial safety buffer is
used by observed feature-center drift.

## 7. Secondary Metrics

- Euclidean drift ratio \(\|\mu_f(t)-\mu_f(0)\|/(d_f(0)+\epsilon)\).
- Dynamic margin \(M_f(t)=\min_{j\neq e(f)}(w_{e(f)}(t)-w_j(t))^\top\mu_f(t)\).
- Frozen assignment switch under \(W(0)\).
- Dynamic assignment switch under \(W(t)\).
- Feature NMI and route heatmap.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: A06_02_01_E02 pseudo/oracle center initialization preserves feature NMI.

Known bad: random Gaussian does not reliably preserve clean feature routing.

Known confusing: Euclidean drift can be large but orthogonal to the nearest
boundary. Therefore signed boundary distance is primary, Euclidean drift is a
guard only.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Snapshot audit | can vectors be reconstructed? | rerun model snapshots | pass if metrics exist per feature | boundary table | detailed |
| Matching audit | is step-0 feature-expert identity stable? | fixed match and heatmap | pass if center init has stable mapping | match table | detailed |
| Boundary audit | does drift consume initial buffer? | \(B_f(t)\) | pass if preserved cases stay below crossing | trajectory | summary |
| Dynamic margin audit | does router movement compensate? | \(M_f(t)\) | compensation if frozen erosion high but dynamic margin positive | scatter | summary |
| Failure audit | do weak cases show boundary/margin failure? | random guard | pass if random has negative margin or switch | table | detailed |

## 10. Algorithm Specification

**Input:** A06_02_01_E02 config, controlled data generator, model, and training loop.

**Parameters:** C0-C3 cells, 8 seeds, 3 conditions, snapshot steps above.

**Intermediate variables:** \(\mu_f(t)\), \(w_e(t)\), \(e(f)\), \(j^*(f)\),
\(d_f(0)\), \(d_f^{\mathrm{frozen}}(t)\), \(B_f(t)\), \(M_f(t)\).

**Steps:**

1. Run the A06_02_01_E02 training loop for each cell, seed, and condition.
2. At step 0, compute feature centers, fixed matching, nearest competing
   boundary, and initial signed distance.
3. At every snapshot, recompute feature centers and router rows.
4. Compute frozen-boundary distance, boundary consumption, Euclidean drift
   ratio, dynamic margin, and switch flags.
5. Aggregate by condition/cell/step and produce figures.

**Outputs:** `boundary_by_step.csv`, `boundary_aggregate.csv`,
`condition_final_boundary.csv`, trajectory/scatter figures.

**Failure reasons:** missing vectors, bad positive control, unstable matching,
or contradictory switch/margin evidence.

## 11. Success / Failure / Insufficient Evidence

**Support margin-buffer boundary:** center-init preserved features keep
positive frozen distance and dynamic margin; weak cases show erosion or
negative margin.

**Support router compensation:** frozen distance erodes but dynamic margin
stays positive and routing remains preserved.

**Weaken boundary model:** switches occur while both frozen distance and
dynamic margin are safely positive.

**Insufficient:** rerun cannot reconstruct vectors or positive controls fail.

## 12. What This Cannot Claim

This protocol cannot claim the exact adversarial perturbation limit, real-DCLM
behavior, utility, semantic experts, or that margin is sufficient under all
training objectives.

## 13. Review Notes And Protocol Changes

- Created after A06_02_01_E02 weakened active tracking and supported positive
  margin preservation.
- User requested minimal anchor and execution under name `06_17_03`.
