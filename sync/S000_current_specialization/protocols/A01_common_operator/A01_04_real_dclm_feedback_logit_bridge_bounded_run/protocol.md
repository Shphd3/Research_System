# Protocol: A01_04 Real-DCLM Feedback Logit Bridge Bounded Run

## 0. Approval Snapshot

Approval status: user requested execution in the active goal on 2026-06-29.

Purpose: Recover real-DCLM step-0/5/10 gate-logit drift artifacts and test
whether feedback-logit common explains proxy-route collapse by replay/removal.

Primary anchor: `01_04_feedback_common_preservation_bridge_anchor.md`.

Anchor decision question: Does estimated feedback common explain step-0 to
step-5/10 proxy-route NMI collapse?

Anchor physical prior tested: preservation failure can be dynamic; step-0
proxy routing can be valid but overwritten by shared feedback drift.

Anchor core model term tested: gate-logit drift
$\Delta z_t=z_t-z_0$, where $z_t=W_t h_t$ is the captured gate output.

Anchor falsifier: real-DCLM proxy routing collapses under full logit drift, but
top feedback-logit drift replay does not reproduce the collapse and removal
does not rescue it.

Experiment role: real-data bridge audit.

Primary metric from anchor: `proxy_nmi_drop_explained_by_feedback_logit_common`.

Claim boundary from anchor: real gate-logit replay/removal only; this is not a
hidden-state projector claim and not a method claim.

Minimal setup: Reuse the `A06_01_04_E03` real-DCLM proxy-center setup, run raw-center
initialization for model seeds 0, 1, and 2, save gate logits at steps 0, 5, and
10, then run logit-drift replay/removal.

Basic configuration: 6-layer Qwen3-MoE toy model on DCLM-bin, raw-center
router initialization, audit layers 3/4/5, 65,536 eval tokens per layer,
checkpoints 0/5/10, max train steps 10.

Conditions to run: raw-center variant only, seeds 0/1/2, layers 3/4/5, steps
5 and 10.

Pass: feedback-logit replay explains most full-drift NMI drop and
feedback-logit removal rescues most of the drop for the collapsed layer/step
cells; random controls do not match.

Fail: full logit drift collapses proxy routing but feedback-logit replay/removal
does not explain it.

Insufficient: step-0 proxy NMI is weak, full drift does not collapse, or
denominator-valid cells are too few.

Cannot claim: hidden-state feedback projector, LM-loss-neutral intervention,
real preservation rescue, residualized MoE utility, or final anti-feedback
method.

Approval decision: execute the bounded real-DCLM gate-logit bridge.

## 1. Anchor Alignment

Decision question: can feedback common explain real step-0 to step-5/10 proxy
route collapse?

Physical prior tested: early training changes gate inputs in a shared direction
that overwrites proxy routing.

Core model term tested: gate-logit drift $\Delta z_t$.

Falsifier: top logit-drift subspace cannot reproduce or rescue collapse.

Claim boundary: real gate-logit bridge only.

## 2. Tested Hypothesis

H1: The top feedback-logit drift subspace explains most proxy-route NMI drop in
collapsed real-DCLM layer/step cells.

H2: Removing the top feedback-logit drift subspace rescues proxy-route NMI.

## 3. Rival Explanations

R1: Collapse is not visible in gate logits.

R2: Collapse is distributed across residual logit drift rather than common
logit drift.

R3: The top logit-drift subspace is no better than a random subspace.

R4: Step-0 proxy labels are not stable enough for bridge interpretation.

## 4. Data / Model / Algorithm / Objective

The run reuses `A06_01_04_E03`:

- DCLM-bin data under `/data/share/109_cache_dir/hf_data/dclm_bin`;
- Qwen3-MoE toy model from `/data/250010109/MoE_Router`;
- raw-center proxy initialization;
- fixed step-0 proxy labels from raw hidden-state k-means.

Captured object:

$$
z_{\ell,t}=W_{\ell,t}h_{\ell,t}
$$

Replay/removal object:

$$
\Delta z_{\ell,t}=z_{\ell,t}-z_{\ell,0}
$$

The feedback-logit projector is the top eigenspace of:

$$
\Delta z_{\ell,t}^\top \Delta z_{\ell,t}
$$

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw_center_seed0 | H1/H2 | real logit drift | reproduces A06 collapse surface | primary | replay/removal explains collapse | no explanation | no collapse | tables |
| raw_center_seed1 | H1/H2 | seed stability | checks seed-level stability | primary | same sign | no explanation | no collapse | tables |
| raw_center_seed2 | H1/H2 | seed stability | checks seed-level stability | primary | same sign | no explanation | no collapse | tables |
| random projector | R3 | random logit subspace | negative control | secondary | below feedback | matches feedback | denominator invalid | figures |

Checkpoints: 0, 5, 10.

Audit layers: 3, 4, 5.

## 6. Primary Metric

`proxy_nmi_drop_explained_by_feedback_logit_common`:

$$
\frac{\mathrm{NMI}(z_0)-\mathrm{NMI}(z_0+P_{\mathrm{fb}}\Delta z_t)}
{\mathrm{NMI}(z_0)-\mathrm{NMI}(z_t)+\epsilon}
$$

Unit: fraction of full proxy-route NMI drop.

Denominator-valid cells require full NMI drop at least 0.05.

## 7. Secondary Metrics

- `feedback_logit_removal_rescue_fraction`;
- `step0_proxy_nmi`;
- `full_step_proxy_nmi`;
- `feedback_only_proxy_nmi`;
- `residual_only_proxy_nmi`;
- random projector explanation and rescue;
- route max load.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: `A06_01_04_E03` raw-center should show step-0 alignment and step-5/10
collapse in at least some layer/seed cells.

Known bad: random projector controls should not explain the collapse as well
as top logit drift.

Known confusing: a top logit-drift projector may capture collapse but may also
include gate-weight drift, hidden-state drift, or both. This run cannot
separate them.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| artifact recovery | Are real logits saved at steps 0/5/10? | npz files | expected seed/layer/step files exist | artifacts dir | detailed |
| collapse audit | Does full drift collapse NMI? | score table | denominator-valid cells exist | summary csv | summary |
| replay/removal | Does top logit drift explain/rescue? | bridge rows | pass/fail rule applies | figures | summary |
| controls | Is random projector weaker? | random rows | random below feedback | summary csv | detailed |

## 10. Algorithm Specification

input: seed, raw-center variant, DCLM-bin data.

parameters: layers 3/4/5, checkpoints 0/5/10, 65,536 eval tokens per layer.

intermediate variables: step-0 labels, logits $z_{\ell,t}$, drift
$\Delta z_{\ell,t}$, top feedback projector, random projector.

steps:

1. Fit step-0 raw proxy labels and raw-center gate rows.
2. Train raw-center model to step 10.
3. Save gate logits at steps 0, 5, and 10.
4. Compute full, feedback-only, residual-only, and random-control route NMI.
5. Aggregate by seed, layer, and step.

outputs: recovered artifacts, CSV tables, JSON pass summary, and figures.

## 11. Success / Failure / Insufficient Evidence

Success supports a real-DCLM gate-logit feedback bridge.

Failure weakens the feedback-logit explanation.

Insufficient evidence means real hidden/logit collapse was not recovered in
this bounded run.

## 12. What This Cannot Claim

This run cannot claim hidden-space feedback projector causality, LM loss after
intervention, training rescue, residualized MoE utility, or layerwise final
rules.

## 13. Review Notes And Protocol Changes

This protocol was added after the controlled feedback bridge passed and after
local inspection showed that `A06_01_04_E03/E04` did not save replayable drift
artifacts.
