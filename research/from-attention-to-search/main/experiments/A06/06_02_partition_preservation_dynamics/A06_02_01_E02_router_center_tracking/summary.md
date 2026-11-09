---
experiment_id: A06_02_01_E02_router_center_tracking
anchor_id: A06_02_01_E02_router_center_tracking
status: completed
run_name: a06_17_02_router_center_tracking_full_20260626_024804
job_id: local-two-gpu
canonical_language: en
---

# Summary: A06_02_01_E02 Router-Center Tracking Preservation

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol:
`protocol.md`

## Purpose

This experiment asks how clean feature routing is preserved after good
feature-center or pseudo-center router initialization in the corrected A06
no-position bridge.

The decision is not whether final routing is clean. A06_01_03_E03 already suggested
that. The decision is whether preservation happens by active router-center
tracking, by a stable positive route margin, by random rediscovery, or by
common / norm drift.

## Exact Setup

Full local two-GPU run:
`a06_17_02_router_center_tracking_full_20260626_024804`.

Data / model:

- one-layer Transformer + top-1 MoE, 4 experts, `d_model=128`;
- no learned absolute positional embedding;
- feature slot length 4, route on the last slot token;
- slot starts `[2, 10, 18]`, balanced feature id, nuisance id, and slot start;
- C0-C3 bridge conditions, 8 seeds, 1600 training steps;
- snapshots at steps 0, 1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1600.

Conditions:

- pseudo-center initialization;
- oracle-center initialization;
- random Gaussian initialization;
- equal-norm random initialization;
- label-shuffled center guard.

## Primary Metric

Primary metric: matched movement-direction alignment,

\[
A_{\mathrm{move}}(t)=
\frac{1}{F}\sum_e
\cos\left(\Delta w_e(t),\Delta \tilde{\mu}_{\pi(e)}(t)\right).
\]

It decides the active-tracking hypothesis. If router rows actively track their
matched feature centers, \(A_{\mathrm{move}}\) should be positive and high while
feature-route NMI stays high.

Guard metrics decide the preservation mode:

- feature-route NMI;
- raw route margin at feature centers;
- matched router-center dot product;
- common-logit share;
- row-norm growth;
- fixed step-0 matching versus per-step matching.

## Result

Active tracking is not supported. Center-initialized routers preserve the
feature partition perfectly, but their row movement is not aligned with
feature-center movement.

The supported mechanism is margin-preserving center initialization: initial
center rows create a feature-specific routing margin that remains positive
through training.

Final step, averaged over C0-C3 and 8 seeds:

| Condition | Final feature NMI mean | Final feature NMI min | \(A_{\mathrm{move}}\) mean | Raw margin min mean | Common share mean | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pseudo-center | 1.000 | 1.000 | -0.412 | 3.544 | 0.265 | preserved by positive margin, not active tracking |
| Oracle-center | 1.000 | 1.000 | -0.398 | 3.647 | 0.262 | same as pseudo-center |
| Random Gaussian | 0.797 | 0.000 | -0.119 | -3.662 | 0.427 | task learned, clean feature partition not preserved |
| Equal-norm random | 0.792 | 0.000 | -0.108 | -3.879 | 0.433 | norm control does not recover the partition |
| Label-shuffled center | 0.861 | 0.637 | -0.146 | -1.609 | 0.780 | center-like norm is not enough; correct matching matters |

All conditions reach target accuracy 1.0 by the final step, so task success
alone does not imply feature-specialized routing.

## Key Figures

### Figure: Feature NMI Trajectory

![Feature NMI trajectory](figures/feature_nmi_trajectory.png)

What this tests:
whether the route assignment remains aligned with feature id through training.

Anchor question:
which preservation mode explains clean routing after center initialization.

Protocol question:
does center initialization preserve routing differently from random and guard
initializations?

Metric shown:
feature-route NMI at each snapshot.

Metric definition:
normalized mutual information between feature id and top-1 expert assignment.

Data source:
`tables/router_center_metrics_by_step.csv`.

How to read:
higher is cleaner feature routing. A value of 1.0 means the four features are
perfectly separated by experts up to expert permutation.

Observed result:
pseudo-center and oracle-center remain at 1.0 in every cell and seed. Random
and equal-norm random learn the task but do not reliably preserve the feature
partition.

Allowed claim:
good feature-center initialization preserves the controlled route partition.

What this figure does not prove:
it does not prove active tracking, expert utility, or real-DCLM behavior.

Anchor update implication:
the anchor should treat preservation as real, then classify its mechanism with
movement and margin guards.

### Figure: Movement Alignment Trajectory

![Movement alignment trajectory](figures/movement_alignment_trajectory.png)

What this tests:
whether router-row displacement points in the same direction as matched
feature-center displacement.

Observed result:
center-initialized rows have negative final \(A_{\mathrm{move}}\) across all
C0-C3 cells. Pseudo-center final mean is -0.412; oracle-center final mean is
-0.398.

Allowed claim:
the active center-tracking explanation is weakened in this bridge.

What this figure does not prove:
negative movement alignment does not mean routing failed; margins show routing
remained clean.

Anchor update implication:
the next mechanism should not assume that good initialization works because
router rows follow feature centers.

### Figure: Route Margin Trajectory

![Route margin trajectory](figures/route_margin_trajectory.png)

What this tests:
whether matched feature centers stay inside the intended router regions.

Observed result:
pseudo-center and oracle-center keep positive raw margins through training.
Random, equal-norm random, and shuffled-center guards have negative final
margins.

Allowed claim:
center initialization works by preserving a feature-specific decision margin
in the raw router logits.

What this figure does not prove:
positive margin does not prove semantic feature value or reduced interference.

Anchor update implication:
the next anchor should test how to create and preserve margin in less
controlled or real route-relevant hidden states.

### Figure: Common And Norm Guard

![Common and norm guard](figures/common_norm_guard_trajectory.png)

What this tests:
whether preservation is mostly explained by common-direction projection or
norm growth.

Observed result:
center initialization keeps common share low, about 0.26 at the final step.
The shuffled-center guard has much higher common share, about 0.78, and does
not achieve clean preservation.

Allowed claim:
common / norm drift is not the main explanation for successful center
preservation in this controlled bridge.

What this figure does not prove:
it does not rule out common-component effects in real-DCLM training.

Anchor update implication:
the important object is a feature-specific margin after removing or controlling
common confounds.

## Claim Boundary

Can claim:
in the corrected no-position A06 bridge, pseudo-center and oracle-center router
initialization preserve the feature partition across training, and preservation
is better explained by stable positive route margins than by active
row-center tracking.

Cannot claim:
real-DCLM preservation, semantic features, expert utility, RoPE behavior, or a
general deployable initialization method.

## Next Decision

Next anchor: test whether the same positive-margin condition can be created
from label-free route-relevant states when the feature definition is unknown.
Plainly: do not ask whether the router follows centers; ask whether a discovered
proxy can give each candidate feature a positive, training-stable routing
margin without relying on labels.
