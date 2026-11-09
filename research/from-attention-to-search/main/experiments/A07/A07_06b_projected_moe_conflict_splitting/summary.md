# Summary: A07_06b Projected MoE Conflict Splitting

Primary anchor:
`../../../problem_anchors/07_features_overlap/07_06_projected_common_rare_conflict_splitting_anchor.md`

Protocol: `protocol.md`

## Purpose

Test whether conflict-subspace projection in a top-1 MoE router and selected
expert update path can prevent frequent common updates from diluting rare
conflict gradients.

## Exact Setup

Run: `a07_06_conflict_projected_moe_full_20260628_1`

ACP job: `pt-gwnh6l71`

Seeds: `20260628-20260704`, 8 seeds.

Conditions: `dense_shared`, `random_top1_moe`,
`centered_unsup_split_moe`, `common_projected_router_moe`,
`conflict_projected_router_moe`, `conflict_projected_router_update_moe`,
and `oracle_split_moe`.

Data: controlled neural common/rare binary task inherited from A07_04. Train is
common-heavy; evaluation is balanced.

## Primary Metric

Primary metric: \(\Delta\mathcal{C}_{C,R}\), the reduction in
routing-weighted negative common/rare gradient conflict.

Required guard: rare loss must improve and strong support must beat or close
the dense-shared rare-loss boundary while preserving common loss.

## Result

Judgment: insufficient for the full mechanism claim, but positive for the
method effect on rare loss.

What passed: `conflict_projected_router_update_moe` improved rare loss versus
random top-1, centered split, and dense shared. It also reduced the selected
update's conflict-projection fraction after suppression.

What did not close: route-level conflict reduction was tiny, the raw conflict
projector stability guard failed, and rare accuracy did not improve. Therefore
the result does not prove that the intended routing-weighted conflict mechanism
caused the rare-loss gain.

Key numbers:

| Metric | Value |
| --- | ---: |
| rare conflict fraction, raw | `0.7934` |
| rare conflict fraction, AdamW-like | `0.1690` |
| raw projector stability | `0.3309` |
| AdamW-like projector stability | `0.7327` |
| full method \(\Delta\mathcal{C}\) vs random | `0.0036` |
| full method rare-loss improvement vs random | `0.2848` |
| full method rare-loss improvement vs centered | `0.2155` |
| full method rare-loss margin vs dense | `-0.1538` |
| full method common-loss regression vs random | `0.0292` |

Decision summary: `weakened_or_insufficient`.

## Key Figures

### Figure: Conflict Versus Rare Loss

![Conflict versus rare loss](figures/conflict_vs_rare_loss.png)

What this tests: whether lower measured common/rare conflict corresponds to
lower rare loss.

Anchor question: does projected MoE reduce harmful common/rare conflict enough
to beat dense rare loss?

Protocol question: does `conflict_projected_router_update_moe` reduce
\(\mathcal{C}_{C,R}\) and \(L_R\) versus random / centered baselines and dense?

Metric shown: routing-weighted gradient conflict and rare loss.

Metric definition:
\(\mathcal{C}_{C,R}=\sum_e q_{C,e}q_{R,e}[-\cos(g_{C,e},g_{R,e})]_+\).

Data source: 8-seed full ACP run.

How to read: lower-left is better. A supported mechanism should move left and
down.

What this figure decides: whether the conflict metric and rare-loss guard move
together.

Observed result: the full projected-update method moves down in rare loss but
barely moves left in conflict.

Allowed claim: the update intervention improved rare loss on the controlled
surface.

What this does not prove: that routing-weighted conflict reduction explains the
gain.

Anchor update implication: mark as insufficient for the mechanism claim.

### Figure: Update Projection Fraction

![Update projection fraction](figures/update_projection_fraction.png)

What this tests: whether the diagnostic projector captures rare update mass
above random controls.

Anchor question: is there a conflict subspace worth suppressing?

Protocol question: does rare update mass concentrate in the conflict projector
above controls?

Metric shown: rare projection fraction into raw conflict, AdamW-like conflict,
and random-control projectors.

Data source: 8-seed full ACP run.

How to read: higher conflict bars than random suggest a real projection target.

What this figure decides: whether the diagnostic gate is compatible with the
intervention.

Observed result: raw conflict mass is high, but raw projector stability is below
threshold; AdamW-like stability is stronger but mass is modest.

Allowed claim: there is projection signal, but the frozen raw projector is not
stable enough for a clean mechanism claim.

What this does not prove: that the projected update gain came from stable
conflict-subspace isolation.

Anchor update implication: revise the projector diagnostic before stronger
claims.

## Claim Boundary

Can claim: on this controlled surface, conflict-projected update suppression
with a common confidence gate improved rare loss and beat dense shared rare
loss, while keeping common loss within the guard.

Cannot claim: route-level conflict splitting, dense-beating functional expert
specialization, real-DCLM transfer, semantic experts, or that the intended
conflict projector is stable enough.

## Next Decision

Revise A07_06 around the discrepancy: rare loss improves without meaningful
route-level conflict reduction. The next minimal test should separate whether
the gain comes from confidence-gated common undertraining, update-norm
regularization, or true conflict-subspace suppression.
