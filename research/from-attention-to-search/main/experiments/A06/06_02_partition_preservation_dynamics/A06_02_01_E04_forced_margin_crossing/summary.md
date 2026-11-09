# Summary: A06_02_01_E04 Margin Crossing Causal Stress

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## Purpose

This experiment asks whether the margin-buffer explanation from A06_02_01_E03 is
causal. The staged test is:

1. freeze the router and push feature centers toward the nearest boundary;
2. weaken the initial router margin;
3. amplify training drift with a higher learning rate.

## Exact Setup

Controlled no-position bridge, C0-C3, 4 seeds, 4 features, 4 experts, slot
length 4, route on the last slot token, no learned absolute positional
embedding, no B token. Training uses the same slot-end target cross-entropy as
A06_02_01_E03.

Run name: `a06_17_04_margin_crossing_full_20260629_1`.

## Primary Metric

The primary metric is the static crossing ratio:

\[
R_f=\frac{\lambda_f^{\mathrm{switch}}}{d_f(0)+\epsilon}.
\]

It asks whether the predicted boundary distance is a real geometric ruler. A
ratio near 1 means that the feature center switches expert when pushed by
about one initial boundary distance.

## Result

**Verdict:** partially supported.

Static geometry passes: feature centers switch near the predicted boundary
with mean center crossing ratio about `1.04-1.07` across conditions. This
supports the claim that margin is a real geometric switch boundary.

Training stress does not cross the boundary. All seven conditions preserve
final feature NMI at `1.0` with zero dynamic switch rate. Norm weakening and
LR 3x reduce dynamic margin strongly, especially `pseudo_norm0p5_lr3x`
(`dynamic_margin_min_mean = 0.701`, `boundary_consumption_max_mean = 0.718`),
but the margin remains positive and routing remains preserved.

**Addendum verdict:** forced post-hoc router-row interpolation completes the
causal chain. When matched router rows are pushed toward their nearest
competitor after training, dynamic margin becomes negative and the original
matched expert region is lost. The mean first crossing alpha is `0.578`; the
mean first feature-NMI drop below `0.95` is `0.656`. More directly, the
matched-region preserve fraction falls from `1.000` at alpha `0.0` to about
`0.80` at alpha `0.5`, `0.31` at alpha `0.75`, and near zero by alpha `1.25`.

## Key Evidence

| Condition | Static center switch ratio | Final feature NMI | Final min dynamic margin | Max boundary consumption | Dynamic switch rate |
|---|---:|---:|---:|---:|---:|
| oracle_base_lr1x | 1.039 | 1.000 | 3.361 | 0.502 | 0.000 |
| pseudo_base_lr1x | 1.039 | 1.000 | 3.467 | 0.516 | 0.000 |
| pseudo_norm0p5_lr1x | 1.045 | 1.000 | 2.115 | 0.522 | 0.000 |
| pseudo_mix0p25_lr1x | 1.066 | 1.000 | 3.281 | 0.521 | 0.000 |
| pseudo_mix0p50_lr1x | 1.055 | 1.000 | 2.509 | 0.569 | 0.000 |
| pseudo_base_lr3x | 1.039 | 1.000 | 1.535 | 0.697 | 0.000 |
| pseudo_norm0p5_lr3x | 1.045 | 1.000 | 0.701 | 0.718 | 0.000 |

Forced crossing addendum:

| Condition | First alpha margin negative | First alpha NMI < 0.95 | Preserve frac at alpha 0.75 | Preserve frac at alpha 1.25 |
|---|---:|---:|---:|---:|
| pseudo_base_lr1x | 0.578 | 0.656 | 0.312 | 0.000 |
| pseudo_norm0p5_lr3x | 0.578 | 0.656 | 0.310 | 0.031 |

## Key Figures

### Figure: Static crossing ratio by condition

![Static crossing ratio](figures/static_center_switch_ratio_by_condition.png)

What this tests: whether margin predicts the geometric switch point.

How to read: the dashed line is the predicted boundary ratio `1.0`. Values near
that line mean the frozen router switches near the predicted boundary.

Observed result: all conditions cluster near `1.0`.

Take-home: margin is a valid static geometric ruler in this controlled bridge.

What this does not prove: it does not prove that natural training will push
features across this boundary.

### Figure: Dynamic margin trajectory

![Dynamic margin trajectory](figures/dynamic_margin_trajectory.png)

What this tests: whether margin weakening and LR stress consume the dynamic
margin during training.

Observed result: LR 3x and norm 0.5 + LR 3x sharply lower dynamic margins, but
the final margins remain positive.

Take-home: the stress moves toward the boundary but does not cross it.

### Figure: Feature NMI trajectory

![Feature NMI trajectory](figures/feature_nmi_trajectory.png)

What this tests: whether feature-specialized routing fails.

Observed result: feature NMI remains `1.0` in all conditions.

Take-home: this run did not manufacture preservation failure.

### Figure: Forced crossing preserve region

![Forced crossing dynamic margin](figures/forced_crossing_dynamic_margin.png)

What this tests: whether explicitly pushing router rows across the competitor
boundary makes dynamic margin negative.

Observed result: the forced interpolation drives min dynamic margin below zero
after alpha around `0.5-0.75`.

Take-home: once we explicitly cross the router boundary, the original
feature-to-expert region is no longer preserved.

## Claim Boundary

Can claim: in the controlled no-position bridge, nearest-boundary margin is a
valid static geometric switch ruler. The tested training stresses reduce
margin but do not cross the boundary. When we explicitly force post-training
router rows across the boundary, the original feature-to-expert assignment
breaks.

Cannot claim: the exact failure threshold under training, real-DCLM behavior,
semantic experts, or expert utility.

## Next Decision

The next method-facing question is not whether crossing can break
preservation; it can. The next question is how to design label-free
initialization or early training so that discovered centers have enough
positive margin and do not approach this boundary.
