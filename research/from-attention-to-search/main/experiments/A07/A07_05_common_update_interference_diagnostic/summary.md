# Summary: A07_05 Common-Update Interference Diagnostic

Primary anchor: `../../../problem_anchors/07_features_overlap/07_05_common_update_interference_diagnostic_anchor.md`

Protocol: `protocol.md`

## Purpose

Test whether common-example updates causally increase rare/conflict loss beyond
norm-matched controls on a controlled nested-conflict surface.

## Exact Setup

Run: `a07_05_common_update_full_local_2gpu_20260625_1`

Seeds: `20260623-20260630`, 8 seeds.

Execution: local two-H100 full run, two shards, then aggregate.

Data: controlled four-group nested-conflict classification surface. Groups `0`
and `2` are common parent examples; groups `1` and `3` are rare exceptions that
share parent structure with the common groups.

Model: small MLP classifier trained on common examples only before the
perturbation audit. This keeps update directions reconstructable and avoids a
MoE utility claim.

Perturbations from the same checkpoint: `common_update`,
`random_update`, `unrelated_update`, and `rare_update_sanity`. All perturbation
directions are norm-matched to the common-update norm.

## Primary Metric

Primary metric: `common_to_rare_loss_effect`.

It is the rare-loss increase from a common update minus the worse matched
control:

\[
\text{effect}=\Delta L_R(\text{common})-\max(\Delta L_R(\text{random}), \Delta L_R(\text{unrelated})).
\]

The pre-set pass threshold was `0.005`.

## Result

Judgment: weakened / insufficient for promoting common-update interference as
the next A07 utility mechanism.

The direction is visible, but too small. Common updates increase rare loss more
than matched controls, and rare updates reduce rare loss, but the primary
effect is only `0.00168`, below the `0.005` threshold.

Key numbers:

| Metric | Mean | Std |
| --- | ---: | ---: |
| `common_to_rare_loss_effect` | `0.00168` | `0.00055` |
| `common_update_rare_loss_delta` | `0.00168` | `0.00053` |
| `random_update_rare_loss_delta` | `0.00000` | `0.00006` |
| `unrelated_update_rare_loss_delta` | `-0.00278` | `0.00089` |
| `rare_update_sanity_rare_loss_delta` | `-0.00406` | `0.00140` |
| `rare_common_update_fraction` | `0.22076` | `0.03321` |
| `projector_stability` | `0.85250` | `0.04114` |

Pass/fail guards:

| Guard | Result |
| --- | --- |
| common update harms rare beyond controls | fail by threshold |
| rare update projects into common subspace | pass |
| common projector is stable | pass |
| rare update sanity does not hurt rare loss | pass |
| rare examples are underlearned | pass |

## Key Figures

### Figure: Rare-Loss Effect

![Rare-loss effect](figures/rare_loss_effect.png)

What this tests: whether common-update direction causes a rare-loss increase
that matched controls do not explain.

How to read: positive bars mean rare loss increases after the perturbation.
The common-update bar should be clearly above both controls to support the
anchor.

Observed result: common update is positive, random is approximately zero, and
unrelated / rare-sanity updates reduce rare loss.

Take-home: the direction is specific, but the causal effect is too small for
the A07_05 pass criterion.

What this does not prove: MoE utility, real-DCLM transfer, semantic
specialization, or preserved partition value.

### Figure: Rare Update Projection

![Rare update projection](figures/projection_fraction.png)

What this tests: whether rare updates have measurable mass in the common-update
subspace.

How to read: larger values mean more rare update energy lies in the common
projector.

Observed result: both rare groups show nonzero projection, with aggregate
`rare_common_update_fraction = 0.22076`.

Take-home: overlap exists, but overlap alone did not yield a strong enough
causal rare-loss harm.

## Claim Boundary

Can claim: on this controlled surface, common-update direction has a small,
direction-specific rare-loss harm, and rare updates measurably overlap the
common-update subspace.

Cannot claim: common-update interference is a sufficient A07 utility mechanism,
that MoE partitioning would help, or that the mechanism transfers to real DCLM.

## Next Decision

Do not promote A07_05 to a partition-value anchor yet. Keep A07 common-update
interference as mechanism reserve, and return to A06 preservation or design a
separate checkpoint-window audit only if this mechanism becomes mainline again.
