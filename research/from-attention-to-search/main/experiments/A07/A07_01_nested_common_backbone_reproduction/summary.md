# Summary: A07_01 Nested Common Backbone Reproduction

Primary anchor:
`../../../problem_anchors/07_features_overlap/07_01_common_rare_conflict_metric_audit_anchor.md`

Protocol: `protocol.md`

## Purpose

Test whether the new nested-prefix surface reproduces the mentor mechanism:
the frequent parent feature \(A\) forms a stable common subspace, and the common
gain continues to grow after that subspace stabilizes.

## Exact Setup

Run: `a07_nested_full_20260628_2`

Seeds: `20260628-20260635`, 8 seeds.

Data: nested binary feature chain \(A -> AB -> ABC -> ABCD\). Train frequencies
are skewed `[4096, 1024, 256, 64]`; evaluation is balanced with 1024 examples
per level. The target requires the parent sign plus child corrections, and
child-only shortcut accuracy is audited.

Model: rank-one hidden readout MLP (`hidden_dim=1`) trained with CE/AdamW.
This intentionally matches the mentor's two-phase minimal model more closely
than a wide MLP.

## Primary Metric

Primary metric: stable-late-gain signature. It passes when post-warmup common
projector drift is low and common projected energy grows:

\[
\delta_C(t)=\|P_C(t)-P_C(T_0)\|_2,\qquad
S_C(t)=\|W_1(t)P_C\|_F^2.
\]

This metric decides whether the surface can reproduce the common-backbone
geometry before any control or MoE utility claim.

## Result

Judgment: supported on the controlled nested surface.

Key numbers:

| Metric | Mean over 8 seeds |
| --- | ---: |
| stable-late-gain pass rate | `1.0000` |
| post-warmup max drift \(\delta_C\) | `0.1373` |
| late common energy gain | `1.5115` |
| final \(A\) accuracy | `1.0000` |
| final \(ABCD\) accuracy | `0.8768` |
| child-only tail shortcut accuracy | `0.6187` |
| true-\(A\) alignment of final projector | `0.7932` |

The balanced-frequency guard had lower final true-\(A\) alignment (`0.2121`) and
lower pass rate (`0.3750`), so the observed common backbone depends on the
frequency-skewed nested setup rather than appearing equally in the balanced
guard.

## Key Figures

### Figure: Common Backbone Curves

![Common backbone curves](figures/a07_01_backbone_curves.png)

What this tests:

Anchor question: does CE/AdamW on nested data produce a stable common subspace
with continued gain growth?

Protocol question: does \(P_C\) stabilize after warmup while \(S_C\) continues to
increase?

Metric shown: per-level accuracy, common projector drift, and common projected
energy.

Metric definition: \(\delta_C\) is projector drift; \(S_C\) is weight energy inside
the frozen common projector.

Data source: 8-seed full local CUDA run.

How to read: the mechanism is supported when \(A\) accuracy is saturated,
\(\delta_C\) stays low after \(T_0\), and \(S_C\) continues upward.

Observed result: \(A\) saturates, post-warmup drift remains low, and common
energy keeps growing.

Allowed claim: the controlled nested surface reproduces the mentor's
common-backbone / late-gain geometry.

What this figure does not prove: it does not prove that this common subspace is
harmful for tail features, nor that C3S or MoE works.

Anchor update implication: A07_02 can use this surface and frozen projector as
a controlled mechanism target.

## Claim Boundary

Can claim: the new nested synthetic surface is a valid first reproduction
surface for the common-backbone mechanism.

Cannot claim: tail interference, optimizer benefit, route-function binding,
real-DCLM behavior, or semantic experts.

## Next Decision

Use the A07_01 surface as the gate for A07_02 common-subspace update control.
