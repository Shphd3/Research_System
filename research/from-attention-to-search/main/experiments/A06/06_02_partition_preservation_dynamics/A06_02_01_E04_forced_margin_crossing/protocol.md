# Protocol: A06_02_01_E04 Margin Crossing Causal Stress

## 0. Approval Snapshot

**Approval status:** approved by user in side conversation; execute stages 1-3
in order.

**Purpose:** test whether the positive margin observed in A06_02_01_E02 /
A06_02_01_E03 is a causal geometric protection budget, not only a correlated
diagnostic.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

**Anchor decision question:** can we deliberately shrink or cross the router
margin, and does crossing predict loss of feature-specialized routing?

**Anchor physical prior tested:** top-1 dot-product router boundaries are
geometric switch surfaces; initial positive margin is a finite safety budget.

**Anchor core model term tested:** nearest-boundary signed distance
\(d_f(0)\), crossing ratio \(R_f\), boundary consumption \(B_f(t)\), and dynamic
margin \(M_f(t)\).

**Anchor falsifier:** routing does not switch near the predicted boundary in
the static calibration, or training preservation is unrelated to initial
margin / boundary consumption.

**Experiment role:** root-cause audit and causal stress test.

**Primary metric from anchor:** static crossing ratio
\(R_f=\lambda_f^{\mathrm{switch}}/(d_f(0)+\epsilon)\).

**Claim boundary from anchor:** controlled no-position bridge only; this does
not claim real-DCLM preservation, semantic experts, or utility.

**Minimal setup:** reuse the A06 controlled no-position bridge: one-layer
Transformer + top-1 MoE, 4 experts, feature slot length 4, no learned absolute
positional embedding, no B token, route on the last token of the feature slot,
C0-C3 cells.

**Basic configuration:** run 4 seeds over C0-C3. Use pseudo/oracle centers for
static calibration; use pseudo center initialization for training stress.

**Conditions to run:** baseline pseudo center; row-norm weakened pseudo
center; random-direction mixed pseudo center; higher-learning-rate drift
stress; combined low-margin plus high-drift stress; oracle baseline guard.

**Pass:** static crossing occurs near the predicted boundary, and training
stress fails earlier when initial margin is weakened or drift is amplified.

**Fail:** static crossing does not follow the boundary prediction, or training
failure/preservation is independent of margin and boundary consumption.

**Insufficient:** route-only positive control fails, snapshots cannot be
reconstructed, or margin-weakened runs lose step-0 feature routing before
training and therefore cannot test preservation.

**Cannot claim:** exact adversarial limit, real-DCLM behavior, expert utility,
or a complete training-dynamics theory.

**Approval decision:** run the staged experiment now.

## 1. Anchor Alignment

**Decision question:** whether margin is a causal geometric boundary for
preservation.

**Physical prior tested:** top-1 router hyperplanes define finite safety
regions; reducing the safety region or increasing drift should reduce
preservation.

**Core model term tested:** \(d_f(0)\), \(R_f\), \(B_f(t)\), and \(M_f(t)\).

**Falsifier:** boundary-directed movement fails to predict expert switches, or
training stress outcome is not ordered by margin/drift.

**Claim boundary:** controlled bridge only.

## 2. Tested Hypothesis

**H1 static calibration:** if router rows are frozen, moving a feature center
along the nearest boundary normal should switch the routed expert at
\(\lambda\approx d_f(0)\).

**H2 margin weakening:** if the initial margin is the protection budget, then
smaller initial logit margin or center-direction corruption should reduce
feature-route NMI after training.

**H3 drift amplification:** if training drift consumes the budget, then
higher-drift training should hurt low-margin runs earlier than strong-margin
runs.

## 3. Rival Explanations

- Margin only correlates with success and is not the switch boundary.
- Feature-cloud tails cross before the feature center crosses.
- Common or norm drift changes logits without feature-boundary crossing.
- Router rows compensate during training.
- Failure under stress is an optimization artifact, not a geometric result.

## 4. Data / Model / Algorithm / Objective

Data and model match A06_02_01_E03. Each sample has one feature slot of length 4.
The slot location is sampled uniformly from fixed slot starts. The routed
position is the last token inside the slot. The target after the slot depends
only on feature identity. No learned absolute positional embedding is used.

The training objective remains slot-end target cross-entropy. No auxiliary
router loss is introduced.

## 5. Conditions, Seeds, And Checkpoints

Seeds: `20260623, 20260624, 20260625, 20260626`.

Cells: `C0_clean, C1_mild_nuisance, C2_moderate_nuisance,
C3_weak_feature_nuisance`.

Training checkpoints: `0, 1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1600`.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Static crossing | H1 | \(R_f\) / margin as geometry ruler | checks if margin predicts switches before training interpretation | primary | \(R_f\) near 1 | switch far from boundary | missing centers | crossing table |
| Pseudo baseline | H2/H3 | strong initial margin | known good reference | primary guard | NMI preserved | baseline fails | bad discovery | final table |
| Oracle baseline | H2/H3 | proxy-noise guard | checks pseudo-center noise | secondary | same as pseudo | unexplained gap | bad oracle | final table |
| Norm 0.5 | H2 | lower logit margin with same boundary direction | tests margin scale without changing step-0 assignment | primary | less robust than baseline | same robustness | step-0 fail | margin table |
| Mix 0.25 / 0.50 | H2 | center direction corruption | tests geometric direction quality | primary | monotone degradation | no relation | step-0 fail | NMI curve |
| LR 3x | H3 | stronger training drift | tests margin budget under stronger motion | primary | more boundary consumption / failure | no drift effect | unstable loss only | trajectory |
| Norm 0.5 + LR 3x | H2/H3 | low margin plus high drift | causal stress combination | primary | fails earliest | no added failure | step-0 fail | trajectory |

## 6. Primary Metric

The first metric is static crossing ratio:

\[
R_f=\frac{\lambda_f^{\mathrm{switch}}}{d_f(0)+\epsilon}.
\]

This decides whether the margin metric is a meaningful geometric ruler. If
this fails, training stress cannot cleanly support a margin-crossing story.

## 7. Secondary Metrics

- Step-0 feature-route NMI.
- Final feature-route NMI.
- Dynamic switch rate.
- Initial signed logit margin.
- Initial boundary distance.
- Boundary consumption \(B_f(t)\).
- Dynamic margin \(M_f(t)\).
- Target accuracy and full next-token loss.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: pseudo/oracle center initialization preserves C0-C3 in A06_02_01_E02
and A06_02_01_E03.

Known bad: random Gaussian does not reliably preserve feature routing.

Known confusing: row-norm scaling does not move the argmax boundary when all
rows are scaled equally, but it reduces logit scale and selected-gate
confidence. Therefore norm scaling tests logit-margin robustness, while
random mixing tests direction/boundary corruption.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Stage 1 | Is margin a geometric ruler? | frozen-row perturbation | pass if switches near predicted distance | static crossing table | summary |
| Stage 2 | Does lower initial margin hurt preservation? | weakened init training | pass if final NMI / margins degrade with weakening | final stress table | summary |
| Stage 3 | Does higher drift expose low-margin failure? | LR stress training | pass if low-margin high-drift fails first | boundary trajectory | summary |

## 10. Algorithm Specification

**Input:** A06_02_01_E03 controlled bridge generator, model, k-means discovery,
pseudo/oracle centers, and training loop.

**Parameters:** cells C0-C3, four seeds, margin weakening conditions, LR
multiplier conditions, checkpoint list.

**Intermediate variables:** feature centers, router rows, fixed expert-feature
matching, nearest competitor, perturbation direction, switch threshold,
boundary consumption, dynamic margin.

**Steps:**

1. Discover pseudo centers and oracle centers on route-position states.
2. Initialize router rows for each condition.
3. Stage 1: freeze the step-0 router and move feature centers plus held-out
   route states toward the nearest boundary until route switch.
4. Stage 2: train baseline, norm-weakened, and mix-weakened pseudo routers.
5. Stage 3: repeat baseline and low-margin conditions with increased learning
   rate.
6. Aggregate static crossing, step-0 quality, final preservation, margin, and
   boundary metrics.

**Outputs:** static crossing table, training-by-step table, final stress
aggregate, trajectory figures, `summary.md`, `detailed.md`, and anchor update.

## 11. Success / Failure / Insufficient Evidence

**Support causal margin boundary:** static crossing is near predicted distance
and training preservation degrades in the expected order:
strong margin > lower margin > direction-corrupted / high-drift low-margin.

**Weaken margin boundary:** static crossing or training outcome is not ordered
by margin / drift.

**Insufficient:** positive-control center init fails, weakened conditions lose
step-0 NMI before training, or high-LR runs only show generic optimization
failure without boundary-consumption evidence.

## 12. What This Cannot Claim

This does not prove real-DCLM preservation, semantic experts, utility, or the
best initialization method. It only tests whether margin behaves like a causal
geometric protection budget in the controlled bridge.

## 13. Review Notes And Protocol Changes

- Created after A06_02_01_E03 showed observed drift stays inside the initial
  boundary buffer.
- User requested staged execution of methods 1-3.
