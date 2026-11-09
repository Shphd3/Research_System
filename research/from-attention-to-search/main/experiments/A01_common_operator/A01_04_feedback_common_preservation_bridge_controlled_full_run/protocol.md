# Protocol: A01_04 Feedback Common Preservation Bridge Controlled Full Run

## 0. Approval Snapshot

Approval status: user requested execution in the active goal on 2026-06-29.

Purpose: Test whether feedback-common drift can causally explain and rescue
proxy-route NMI collapse in a controlled bridge.

Primary anchor: `01_04_feedback_common_preservation_bridge_anchor.md`.

Anchor decision question: Does estimated feedback common explain step-0 to
step-5/10 proxy-route NMI collapse?

Anchor physical prior tested: Preservation failure can be dynamic rather than
static; step-0 proxy geometry can be valid but overwritten by shared feedback
drift.

Anchor core model term tested: drift decomposition
\(\Delta h=P_{\mathrm{fb}}\Delta h+(I-P_{\mathrm{fb}})\Delta h\).

Anchor falsifier: full drift collapses proxy routing but feedback-common replay
does not reproduce the collapse and feedback-common removal does not rescue it.

Experiment role: root-cause / bridge audit.

Primary metric from anchor: `proxy_nmi_drop_explained_by_feedback_common`.

Claim boundary from anchor: controlled feedback bridge only; no real-DCLM
feedback claim without hidden/checkpoint drift artifacts.

Minimal setup: Generate valid step-0 proxy routing, add controlled drift, and
measure route NMI under full, feedback-only, residual-only, and random-control
drift replay.

Basic configuration: hidden dimension 32, eight groups/experts, twenty seeds,
600 samples per group.

Conditions to run: common feedback, mixed feedback and residual drift, residual
drift control, nuisance drift control, weak feedback.

Pass: In feedback regimes, feedback-only replay explains most full-drift NMI
drop and residual-only replay rescues most of the drop; controls do not match.

Fail: feedback replay/removal does not explain collapse, or random controls
match feedback common.

Insufficient: step-0 proxy routing is weak, full drift does not collapse
routing, or NMI/drop denominators are unstable.

Cannot claim: real-DCLM feedback causality, preservation rescue, MoE utility,
or final anti-feedback method.

Approval decision: execute the controlled full run.

## 1. Anchor Alignment

Decision question: can feedback-common drift explain proxy-route collapse?

Physical prior tested: early-training drift can overwrite valid step-0 routing.

Core model term tested: replay/removal of \(P_{\mathrm{fb}}\Delta h\).

Falsifier: feedback drift replay/removal has no causal effect.

Claim boundary: controlled bridge only.

## 2. Tested Hypothesis

H1: Feedback-only drift reproduces most of full-drift proxy-route NMI collapse.

H2: Removing feedback-common drift rescues proxy-route NMI relative to full
drift.

## 3. Rival Explanations

R1: Proxy labels or step-0 router are invalid.

R2: Collapse is caused by group-specific residual drift.

R3: Collapse is caused by activation nuisance drift.

R4: The estimated feedback projector is no better than random.

## 4. Data / Model / Algorithm / Objective

Step-0 hidden states are generated so a linear router recovers proxy groups.
The router also has a common-margin direction for one expert. Feedback drift
adds a shared component along this common-margin direction; residual drift adds
group-specific components.

Interventions:

- `step0`: original hidden states.
- `full_drift`: \(h_0+\Delta h\).
- `feedback_only`: \(h_0+P_{\mathrm{fb}}\Delta h\).
- `residual_only`: \(h_0+(I-P_{\mathrm{fb}})\Delta h\).
- `random_feedback_only`: random projector replay.
- `random_residual_only`: random projector removal.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| common_feedback | H1/H2 | shared feedback drift | positive feedback-collapse case | primary | feedback explains/rescues | no effect | weak step0/full drop | figures |
| mixed_feedback_residual | H1/H2 | shared plus residual drift | tests partial residual nuisance | primary | feedback still explains main drop | residual dominates | unstable | figures |
| residual_drift_control | R2 | group-specific drift | negative control | secondary | feedback does not falsely explain | false positive | weak step0 | tables |
| nuisance_drift_control | R3 | activation nuisance drift | negative control | secondary | feedback does not falsely explain | false positive | unstable | tables |
| weak_feedback | H1/H2 | smaller common drift | sensitivity case | secondary | partial explanation | no signal | denominator small | tables |

Seeds: 0-19.

No real-DCLM hidden tensors are used in this controlled run.

## 6. Primary Metric

`proxy_nmi_drop_explained_by_feedback_common`:

\[
\frac{\mathrm{NMI}_0-\mathrm{NMI}_{\mathrm{feedback\ only}}}
{\mathrm{NMI}_0-\mathrm{NMI}_{\mathrm{full}}+\epsilon}
\]

Unit: fraction of full NMI drop.

Why it decides: feedback common is relevant only if replaying it explains the
route collapse.

## 7. Secondary Metrics

- `feedback_removal_rescue_fraction`.
- `step0_proxy_nmi`.
- `full_drift_proxy_nmi`.
- `feedback_only_proxy_nmi`.
- `residual_only_proxy_nmi`.
- `route_max_load`.
- random projector control drop and rescue fractions.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: `common_feedback` should collapse under full and feedback-only
drift, and should rescue under residual-only drift.

Known bad: random projector controls should not match feedback-common replay.

Known confusing: `weak_feedback` may have a small denominator; treat it as a
sensitivity case, not as the main pass/fail condition.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| generation | Is step-0 proxy routing valid? | step0 NMI | high step0 NMI | score table | detailed |
| drift | Does full drift collapse when intended? | full NMI drop | large drop in feedback regimes | summary table | summary |
| estimator | Does \(P_{\mathrm{fb}}\) capture feedback drift? | replay/removal effects | feedback beats random | control table | detailed |
| aggregation | Is explanation stable? | seed means/win rates | pass/fail rule applies | figures | summary |

## 10. Algorithm Specification

input: regime config and seed.

parameters: hidden dimension 32, groups 8, samples per group 600, feedback rank
1, seeds 0-19.

intermediate variables: step-0 hidden states, router, proxy labels, drift,
estimated feedback projector, random projector, NMI per intervention.

steps:

1. Generate route-separable step-0 hidden states.
2. Build router rows from group centers plus a common-margin direction.
3. Generate feedback, residual, and nuisance drift.
4. Estimate \(P_{\mathrm{fb}}\) from drift second moment.
5. Evaluate route NMI under replay/removal interventions.
6. Aggregate drop-explained and rescue fractions over seeds.

outputs: CSV tables, JSON summary, and central figures.

debug artifacts: run config, per-seed intervention score table.

pass conditions: feedback regimes show high drop explained and rescue;
controls remain low.

fail conditions: feedback replay/removal does not explain collapse.

failure reasons: invalid proxy geometry, poor projector estimate, or collapse
caused by non-common drift.

## 11. Success / Failure / Insufficient Evidence

Success supports feedback-common replay/removal as a controlled preservation
mechanism.

Failure weakens the feedback-common bridge.

Insufficient evidence requires redesigning controlled drift before real-DCLM
artifact recovery.

## 12. What This Cannot Claim

This run cannot claim real-DCLM feedback common, real preservation rescue, or
MoE utility because local A06 artifacts contain trajectory metrics but not
hidden/checkpoint drift tensors for replay/removal.

## 13. Review Notes And Protocol Changes

Initial protocol created after A01_03 passed and after local A06 artifact
inspection found metric trajectories but no hidden drift tensors.

