# Summary: A07_02 Nested Tail Common-Subspace Control

Primary anchor:
`../../../problem_anchors/07_features_overlap/07_02_common_controlled_rare_interference_anchor.md`

Protocol: `protocol.md`

## Purpose

Test whether suppressing the common-subspace component of active updates
improves rare nested tail loss after A07_01 has established a stable common
projector.

## Exact Setup

Run: `a07_nested_full_20260628_2`

Seeds: `20260628-20260635`, 8 seeds.

Data/model: same nested surface and rank-one hidden model as A07_01.

Conditions: `ce_adamw`, `confidence_gate_only`,
`subspace_suppression_only`, and `combined_gate_and_suppression`.

## Primary Metric

Primary metric:

\[
\Delta L_{\mathrm{tail}}=
L_{\mathrm{tail}}(\mathrm{CE})-
L_{\mathrm{tail}}(\mathrm{combined}).
\]

Mechanism guard:

\[
\alpha_{\mathrm{tail}}=
\frac{\|P_Cu_{\mathrm{tail}}\|^2}{\|u_{\mathrm{tail}}\|^2+\epsilon}.
\]

This decides whether the control improves tail loss and actually reduces tail
update concentration in the common subspace.

## Result

Judgment: supported on the controlled rank-one nested surface.

Key numbers:

| Condition | Tail loss | Tail acc | \(A\) loss | \(\alpha_{\mathrm{tail}}\) |
| --- | ---: | ---: | ---: | ---: |
| CE/AdamW | `0.3947` | `0.8806` | `0.0325` | `0.1387` |
| confidence gate only | `0.3242` | `0.8829` | `0.0600` | `0.1558` |
| subspace suppression only | `0.3196` | `0.8896` | `0.0325` | `0.0234` |
| combined control | `0.2872` | `0.8933` | `0.0590` | `0.0183` |

The combined control improved tail loss by `0.1075`, reduced
\(\alpha_{\mathrm{tail}}\) by `0.1204`, and kept common loss regression within
the pre-set guard (`0.0265 < 0.05`).

## Key Figures

### Figure: Tail Control Results

![Tail control results](figures/a07_02_control_results.png)

What this tests:

Anchor question: does common-subspace update control reduce nested tail loss?

Protocol question: does combined confidence gating plus subspace suppression
beat CE/AdamW and reduce \(\alpha_{\mathrm{tail}}\)?

Metric shown: tail loss and tail update fraction in \(P_C\).

Metric definition: tail loss is BCE on \(ABCD\); \(\alpha_{\mathrm{tail}}\) is the
fraction of the tail update inside the frozen common projector.

Data source: 8-seed full local CUDA run.

How to read: lower bars are better in both panels.

Observed result: combined control gives the lowest tail loss and the lowest
tail update fraction.

Allowed claim: on this controlled rank-one nested surface, common-subspace
update control reduces tail loss and the measured tail update concentration.

What this figure does not prove: full C3S-AdamW, wide-transformer behavior,
real-DCLM transfer, or MoE expert utility.

Anchor update implication: A07_02 can be marked supported-controlled, with a
strict boundary.

## Claim Boundary

Can claim: common-subspace update control works on the controlled rank-one
nested surface.

Cannot claim: full optimizer validity, real-language transfer, MoE
specialization, or dense-beating real utility.

## Next Decision

Use this as mechanism support, but keep A07 real MoE utility gated by A06 route
preservation and by the A07_06 mechanism-separation warning.
