# A06_01_01_E04 High-Dimensional Gaussian Gate Norm Variation Protocol

## 0. Approval Snapshot

Approval status:
Approved by the user in the current turn for local execution.

Anchor:
`Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/subanchors/06_01_01_common_geometry_nuisance_controls_anchor.md`

Decision question:
Does removing only row-norm variation reduce the Gaussian-scaled gate's true decision-cell imbalance toward the normalized-direction baseline?

Physical prior tested:
Dot-product gate score depends on both direction and row norm:
$z_e=w_e^\top x=\rho_e u_e^\top x$.

Model term tested:
The norm scale term $\rho_e$.

Primary metric:
True cell imbalance $m\max_e |p_e-1/m|$.

Falsifier:
If the norm-controlled Gaussian condition remains as imbalanced as the Gaussian-scaled condition after row-norm variation is removed, row-norm variation is not the main extra source.

Claim boundary:
Pure gate-only top-1 routing with uniform high-dimensional inputs. No attention, residual stream, training, semantic specialization, learned MoE collapse, or final router method claim.

Minimal run:
Compare normalized random directions, standard Gaussian-scaled gates, and norm-controlled Gaussian gates over matched sampled directions, with finite-token observed loads used only to separate sampling error from fixed true-cell imbalance.

## 1. Purpose

The 0620 gate-only evidence already separates finite-token sampling noise from a fixed gate-specific decision-cell floor. It also shows that standard Gaussian-scaled gates have larger true cell imbalance than normalized random directions. This protocol tests whether that extra fixed floor is causally explained by row-norm variation.

This is a mechanism audit, not a method proposal.

## 2. Conditions

Condition A: `normalized_directions`
Use unit-normalized Gaussian row directions $u_e$ and score $z_e=u_e^\top x$.

Condition B: `gaussian_scaled`
Use the original Gaussian rows $w_e=\rho_e u_e$ and score $z_e=\rho_e u_e^\top x$.

Condition C: `norm_controlled_gaussian`
Use the same directions as condition B but set all row norms equal to the mean sampled norm. Top-1 assignments should match condition A for the paired directions while preserving the Gaussian-derived direction set.

## 3. Basic Configuration

Local minimal grid:

| Field | Value |
|---|---|
| dimensions | 32, 128, 512 |
| experts | 8, 32 |
| seeds | 8 |
| true-cell Monte Carlo tokens | 50,000 per seed |
| observed finite-token loads | 4,096 and 32,768 |
| input distribution | random Gaussian vectors normalized to unit length |

The run is intentionally smaller than the 0620 sweep because the decision is paired and targeted: compare the same Gaussian directions before and after removing row-norm variation.

## 4. Metrics

Primary metric:
`true_cell_imbalance = m * max_e abs(p_e - 1/m)`.

Secondary metrics:
`observed_load_error = m * max_e abs(p_hat_e - 1/m)`, `sampling_error = m * max_e abs(p_hat_e - p_e)`, `row_norm_cv = std(rho) / mean(rho)`, and `max_abs_direction_corr`.

Metric interpretation:
The primary metric decides whether row-norm variation changes the fixed gate cell geometry. The observed and sampling metrics only check that finite-token noise is not being mistaken for fixed imbalance.

## 5. Protocol Alignment Gate

Anchor decision question:
Does removing only row-norm variation reduce the Gaussian-scaled gate's true decision-cell imbalance toward the normalized-direction baseline?

Anchor physical prior:
Larger row norm can expand the region where one row wins the top-1 comparison.

Anchor model term:
$\rho_e$ in $z_e=\rho_e u_e^\top x$.

Anchor falsifier:
Norm-controlled Gaussian gates remain close to Gaussian-scaled gates instead of moving toward normalized directions.

Anchor primary metric:
True cell imbalance.

Anchor claim boundary:
Gate-only, random-init, high-dimensional uniform-input mechanism evidence.

## 6. Expected Readout

Support row-norm variation as the main extra source if:
`gaussian_scaled` has higher true cell imbalance than `norm_controlled_gaussian`, and `norm_controlled_gaussian` is close to `normalized_directions` with `row_norm_cv=0`.

Weaken the claim if:
`norm_controlled_gaussian` remains close to `gaussian_scaled` even though row-norm variation is removed.

Insufficient evidence if:
Monte Carlo noise is too large, paired conditions are not matched by direction, or the observed finite-token loads disagree with the estimated true-cell floor.

## 7. Planned Outputs

Tables:
`tables/results.csv`, `tables/aggregate_by_condition.csv`, `tables/paired_gaussian_vs_norm_controlled.csv`.

Figures:
`figures/true_cell_imbalance_by_condition.png`, `figures/sampling_error_by_tokens.png`.

Reports:
`summary.md`, `detailed.md`, and a short anchor update in the current evidence section.
