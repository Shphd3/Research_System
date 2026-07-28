# Protocol: A11_08 General-K Readout-Margin Dynamics

## 0. Approval Snapshot

Approval status: approved by user on 2026-07-09.

Purpose: test the minimal falsifiable claim behind general next-K MTP efficiency: when K covers multiple informative future horizons, the first-order semantic velocity should depend on the vector sum of their readout-effective directions, not on K itself.

Primary anchor: `daily_research_reports/0709/mtp_generalized_efficiency_story/anchors/11_08_general_k_readout_margin_dynamics_anchor.md`.

Anchor decision question: does first-order readout-effective semantic margin under next-K prediction equal the contribution predicted by the active informative horizons?

Anchor physical prior tested: uninformative horizons produce only shared updates at a collapsed branch state; informative horizons produce branch-specific updates; multiple informative horizons help only when their centered output directions align.

Anchor core model term tested:

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)
$$

and:

$$
G_K=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2.
$$

Anchor falsifier: under the same K, same number of informative horizons, same active loss count, and a passing leakage/local guard, if output-row geometry predicts that the aligned two-informative condition should have much larger velocity than the low/conflict two-informative condition, but the observed hidden-gradient velocity does not separate them, then the minimal general-K vector-sum mechanism is falsified or strongly weakened.

Experiment role: metric audit / theory-mechanism test. This is not a MoE bridge and not a natural-language experiment.

Primary metric from anchor: observed hidden-gradient readout-effective velocity,

$$
G_K^{hidden}=\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K).
$$

Claim boundary from anchor: this run can only support or weaken the decision-prefix first-order general-K mechanism. It cannot prove all-position dynamics, natural-language benefit, MoE routing preservation, or expert utility.

Minimal setup: clean synthetic decision-prefix training only, branch-collapsed initialization, fixed max-K heads, `Kmax=4`.

Basic configuration: 4 branches, seeds `971-975`, one-step diagnostics first, short 0-2000-step curves as secondary evidence.

Conditions to run:

```text
shared_only_k4
single_h3
aligned_h3_h4
low_conflict_h3_h4
```

Pass: geometry audit shows a clear predicted aligned-minus-low/conflict gap, observed `G_K_hidden` separates in the same direction, `single_h3` is positive, `shared_only_k4` is near zero, and local shared targets do not degrade.

Fail: after geometry, leakage, single-positive, shared-zero, and local guards pass, the observed aligned velocity is not greater than low/conflict velocity, or most seeds do not support aligned greater than low/conflict.

Insufficient: geometry construction does not create a large enough predicted gap, step-0 leakage appears, all predicted signals are too small, local guard fails, or finite-difference and hidden-gradient diagnostics conflict without localization.

Cannot claim: larger K is always better; MTP is better than NTP in natural language; all-position indirect transfer is explained; MoE routing or expert utility follows; Q alone proves direct supervision.

Approval decision: run the experiment after this canonical protocol is written.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Early variable `Z` | Prefix information needed by later tokens | Synthetic branch id | Categorical | Controlled long-horizon semantic proxy | Natural-language semantics |
| Current state `h_T` | Hidden state after the decision prefix | `h_z=h_T(Z=z)` | Vector | State whose semantic update is tested | All sequence states |
| Informative horizon | Future offset that newly contains `Z` | `Y_j=S_{j,Z}` with one-to-one branch code | Future offset | Determines whether a horizon should contribute branch-specific update | Real text horizon structure |
| `I_K` | Informative horizons covered by K | `{j <= K : I(Z;Y_j | Y_<j)>0}` | Set | Core object in the general-K theorem | Optimization speed by itself |
| Centered output direction | Correct target row after subtracting branch mean | `u_{j,z}-bar u_j` | Vector | Direction that the horizon gives to `h_T` | Downstream utility |
| Aggregate semantic direction | Sum of covered informative directions | `v_z^(K)=sum_j lambda_j(u_{j,z}-bar u_j)` | Vector | Determines predicted first-order velocity | Multi-step convergence |
| Readout-effective margin | Whether `h_T` moves toward correct future-token rows | `M_K(h)=m^-1 sum_z v_z^(K)^T h_z` | Scalar | Primary first-order efficiency target | Natural-language benefit |
| Hidden-gradient velocity | Instantaneous loss-induced movement along the aggregate semantic direction | `G_K_hidden=m^-1 sum_z v_z^(K)^T(-grad_hz L_K)` | Scalar | Primary metric | Parameter-space sample efficiency |
| Finite-difference velocity | One small parameter update's margin change | `Delta M_K / eta` | Scalar per step size | Auxiliary implementation check | Decisive mechanism evidence if numerically unstable |
| Local guard | Whether shared nearby targets are preserved | Shared target CE / accuracy | CE / accuracy | Rules out semantic gain by local-target damage | Full LM quality |

## 2. Anchor Alignment

Decision question: whether general next-K first-order semantic efficiency is governed by the vector sum of readout-effective directions from active informative horizons.

Physical prior tested: shared targets produce common updates; informative branch-coded targets produce branch-specific updates; alignment determines whether adding an informative horizon helps or cancels.

Core model term tested: `v_z^(K)` and `G_K`.

Falsifier: a passing geometry audit predicts aligned greater than low/conflict, but observed hidden-gradient velocity does not separate them.

Claim boundary: decision-prefix, first-order, controlled synthetic only.

## 3. Tested Hypothesis

Minimal judgment:

```text
Under the same K=4 and the same two informative horizons, the second informative
horizon's output-row direction determines first-order semantic velocity.
```

Minimal comparison:

```text
aligned_h3_h4:
  Y3 = S_z, Y4 = T_z
  head-4 T_z directions are aligned with head-3 S_z directions.

low_conflict_h3_h4:
  Y3 = S_z, Y4 = T_z
  head-4 T_z directions are constructed to be low/conflicting relative to head-3 S_z.
```

Both conditions use the same K, active horizon count, and target informativeness. The changed object is the output-row direction of the second informative horizon.

Falsifiable prediction:

$$
G^{pred}_{aligned}
=\frac1{m^2}\sum_z\|a_{3,z}+a_{4,z}^{aligned}\|^2
$$

$$
G^{pred}_{low/conflict}
=\frac1{m^2}\sum_z\|a_{3,z}+a_{4,z}^{low/conflict}\|^2.
$$

If:

$$
G^{pred}_{aligned}-G^{pred}_{low/conflict}
\ge 0.5G^{pred}_{single},
$$

then observed hidden-gradient velocity should satisfy:

$$
G^{hidden}_{aligned}>G^{hidden}_{low/conflict}.
$$

Strong support requires the aligned-minus-low/conflict observed gap to be positive in at least 4 of 5 seeds. Strong weakening is recorded if fewer than 4 of 5 seeds support the direction, or if the observed gap is below 25% of the predicted gap after the geometry audit passes.

## 4. Rival Explanations

| Rival explanation | Why plausible | How this protocol separates it |
| --- | --- | --- |
| Loss-scale effect | Larger K has more active losses | Compare same K=4 and same active horizon count; report gradient norm |
| More-head effect | Higher K may have more heads | Use fixed max-K heads in all conditions |
| Probe false positive | Probe-readable does not mean output-row use | Primary metric is output-row-facing margin, not probe accuracy |
| Step-0 branch leakage | Initialization may already encode `Z` | Require chance `Q(0)`, near-zero `M_K(0)`, near-zero `E_Z(0)` |
| Failed conflict construction | Permutation or geometry may not create low/conflict directions | Require output geometry audit before interpreting pass/fail |

## 5. Data / Model / Algorithm / Objective

Data shape:

```text
BR_z F00 ... F15 U00 U01 U02 U03 Y1 Y2 Y3 Y4 STOP
```

Regimes:

```text
shared_only_k4:     Y1=A, Y2=C, Y3=A,   Y4=C
single_h3:          Y1=A, Y2=C, Y3=S_z, Y4=A
aligned_h3_h4:      Y1=A, Y2=C, Y3=S_z, Y4=T_z
low_conflict_h3_h4: Y1=A, Y2=C, Y3=S_z, Y4=T_z
```

For `aligned_h3_h4`, head-4 rows for `T_z` are set to align with head-3 rows for `S_z` at initialization. For `low_conflict_h3_h4`, head-4 rows for `T_z` are set to a low/conflicting transform of head-3 centered rows. The transform is recorded in the output-geometry table. This makes the minimal falsifier sharp; target-code permutation alone is kept as a later, weaker naturalization step.

Objective:

$$
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

Scope: decision-only.

## 6. Conditions, Seeds, And Checkpoints

Seeds: `971-975`.

One-step primary eta: `3e-4`; auxiliary eta: `1e-4`, `1e-3`.

Short curve: 0-2000 steps, evaluation every 100 steps, secondary evidence only.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `shared_only_k4` | Uninformative horizons give zero semantic velocity | `I_K=empty` | Zero guard | Required guard | Near-zero `G_K_hidden` | Stable positive margin | Leakage or implementation error | `zero_guard.csv` |
| `single_h3` | One informative horizon is positive | One `a_3,z` | Positive control | Required guard | Positive `G_K_hidden` | Not positive | Predicted signal too small | `single_info.csv` |
| `aligned_h3_h4` | Aligned informative horizons amplify | `a_3,z+a_4,z` | Minimal positive case | Primary | High observed velocity | Not above low/conflict | Alignment not realized | `aligned.csv` |
| `low_conflict_h3_h4` | Direction dependence / non-monotonic K | Small or negative increment | Minimal falsifier case | Primary | Lower than aligned | Matches/exceeds aligned despite predicted gap | Conflict not realized | `low_conflict.csv` |
| local guard | Local targets not harmed | Shared CE / accuracy | Exclude tradeoff | Secondary | No material CE increase | CE degradation | Target too easy to interpret | `local_guard.csv` |

## 7. Primary Metric

Predicted quantity:

$$
G_K^{pred}=\frac1{m^2}\sum_z\left\|\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)\right\|^2.
$$

Implementation-scaled predicted quantity:

$$
G_{K,batch}^{pred}=G_K^{pred}/n_{branch},
$$

where `n_branch` is the number of samples per branch in the one-step batch. This accounts for cross-entropy reduction over the full batch.

Observed quantity:

$$
G_K^{hidden}=\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K).
$$

Minimal falsification thresholds:

1. Geometry precondition: `G_pred_aligned - G_pred_low_conflict >= 0.5 * G_pred_single`.
2. Falsifier: under that precondition, `mean(G_hidden_aligned) <= mean(G_hidden_low_conflict)`.
3. Strong weakening: aligned is greater than low/conflict in fewer than 4 of 5 seeds, or observed gap is less than 25% of the predicted batch-scaled gap.
4. Zero guard: shared-only observed velocity is no more than 10% of the single-informative positive-control scale.

## 8. Secondary Metrics

| Metric | Meaning | Why secondary |
| --- | --- | --- |
| `Delta M_K / eta` | One small parameter update's margin change | Parameter finite-difference can be numerically unstable |
| `Delta E_Z / eta^2` | Branch hidden separation growth | Shows separability, not output-row use |
| Native informative accuracy | Whether the model itself predicts `S_z` or `T_z` | Useful for curves, not one-step mechanism |
| `Q(t)` | Guarded recovery | Auxiliary curve evidence, not direct-supervision evidence |
| Local CE / accuracy | Shared target preservation | Rules out local-loss tradeoff |
| Gradient norm | Loss-scale guard | Rules out larger K as merely larger gradient norm |

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: `single_h3` should reproduce the A11_06 pattern: positive K3-style hidden velocity.

Known bad: `shared_only_k4` should be near zero.

Known confusing: exact low/conflict geometry may be too strong or too weak. Interpret pass/fail only after the output geometry table verifies the predicted gap.

Known confusing: finite-difference may disagree with hidden-gradient velocity. In that case, the result is analyzed as an implementation/parameterization issue in `detailed.md`; the hidden-gradient metric remains primary.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Data audit | Are horizons informative as intended? | Generated examples | Target-Z relation matches regime | `sample_table.csv` | detailed |
| Output geometry audit | Was alignment/conflict actually realized? | Output rows | Predicted gap has intended size | `output_geometry.csv` | summary |
| Leakage audit | Is `Z` already visible at step 0? | `Q(0)`, `M(0)`, `E(0)` | Chance / near zero | `leakage_audit.csv` | summary |
| One-step gradient | Main theory test | Gradients at `h_T` | Observed follows predicted | `one_step_metrics.csv` | summary |
| Finite-difference check | Does a small parameter step agree? | Cloned update | No gross contradiction | `finite_diff.csv` | detailed |
| Short curve | Does one-step mechanism appear in early training? | 0-2000 step run | Secondary only | curve figures | summary if useful |
| Local guard | Are shared targets preserved? | CE / accuracy | No material regression | `local_guard.csv` | summary |

## 11. Algorithm Specification

Input: regime config, branch count, `Kmax=4`, seed list, target-code mapping, output-row transform.

Parameters: `num_branches=4`, seeds `971-975`, primary eta `3e-4`, auxiliary eta `1e-4` and `1e-3`, training steps `2000`.

Intermediate variables: `u_j,z`, `bar_u_j`, `a_j,z`, `v_z^(K)`, `G_K_pred`, `G_K_hidden`, `Delta M_K / eta`, `Delta E_Z / eta^2`.

Steps:

1. Build data regimes.
2. Initialize fixed max-K-head model with branch-collapsed branch embeddings.
3. Apply general-K head-4 geometry for aligned or low/conflict regimes.
4. Run leakage and output-geometry audits.
5. Compute hidden-gradient velocity.
6. Run finite-difference one-step checks.
7. Run short decision-prefix curves.
8. Aggregate tables and write `summary.md` / `detailed.md`.

Outputs: `one_step_metrics.csv`, `one_step_summary.csv`, `output_geometry.csv`, `curve_metrics.csv`, `condition_summary.csv`, figures, `summary.md`, `detailed.md`.

Failure reasons: theory wrong, geometry construction failed, leakage, implementation mismatch, local target tradeoff, or parameter finite-difference instability.

## 12. Success / Failure / Insufficient Evidence

Success: aligned and low/conflict separate in the predicted direction; `single_h3` is positive; `shared_only_k4` is near zero; leakage and local guards pass.

Failure: after all guards pass, aligned does not exceed low/conflict in observed hidden-gradient velocity, or most seeds do not support aligned greater than low/conflict.

Insufficient evidence: geometry gap is too small, predicted signals are too small, leakage appears, local guard fails, or finite-difference conflict cannot be localized.

## 13. What This Cannot Claim

This experiment cannot claim larger K is always better, natural-language MTP benefit, all-position indirect-transfer mechanism, MoE routing preservation, expert utility, or direct-supervision evidence from `Q` alone.

Allowed claim if supported:

```text
In controlled decision-prefix next-K training, first-order MTP semantic efficiency
is governed by the vector sum of readout-effective directions from informative
future horizons. Larger K helps only when added informative horizons contribute
aligned branch-relevant directions.
```

## 14. Review Notes And Protocol Changes

The user accepted the minimal falsifier, the geometry gap precondition, and the 4/5 seed direction rule. The only protocol sharpening added here is that the primary implementation uses geometry-controlled head-4 rows for the aligned and low/conflict conditions, because random target-code permutation alone may not create a large enough output-row geometry gap in high dimension.
