# 11_08b Output-Geometry Dynamics Audit Anchor

Status: supported by A11_08b full run on 2026-07-09.  
Parent line: `11_long_horizon_mtp_objective`.  
Purpose: audit whether the A11_08 general-K output-geometry explanation remains valid during early training.

## 0. Thinking Card

**Phenomenon:** A11_08 showed that, at initialization, general-K hidden semantic velocity is governed by the vector sum of centered output directions from informative horizons. However, the prediction heads were trainable during the short training curves, so the output-row geometry may change after step 0.

**Mechanism guess:** If the initial output geometry is a real hidden-update mechanism, then freezing prediction heads should preserve the aligned greater than low/conflict separation. If the separation only appears because trainable heads quickly rotate the low/conflict condition into an aligned geometry, then A11_08 should be kept as a one-step static-geometry result.

**Key variables:** early variable `Z`; decision hidden state `h_T`; horizon-3 semantic row `u_{S_z}^{(3)}`; horizon-4 semantic row `u_{T_z}^{(4)}`; centered row direction; current geometry; reference geometry at step 0; hidden-gradient semantic velocity; readout margin; guarded recovery score.

**Causal relation:** Output rows define the readout direction along which the horizon loss updates `h_T`. If that direction remains fixed or explanatory, hidden semantic updates should track the predicted aligned versus low/conflict geometry. If trainable output heads co-adapt, training curves may reflect changing head geometry rather than the original general-K vector-sum prediction.

**Observable metric:** Primary decision evidence is the frozen-head aligned-minus-low/conflict gap in hidden semantic velocity and readout margin. The main dynamics audit records output-row cosine, head drift, current-geometry velocity, reference-geometry velocity, current/reference readout margins, guarded recovery, and local Y1/Y2 loss and accuracy.

**Alternative explanations:** A11_08 could be a step-0 construction artifact, an output-head co-adaptation phenomenon, a local-loss tradeoff, or a probe-only recovery pattern. The trainable-versus-frozen head comparison separates these explanations.

**Decision rule:** Do 11_08b before 11_09. Support the hidden-update geometry interpretation if frozen heads preserve the A11_08 ordering and guard conditions pass. Downgrade the training-curve interpretation if trainable heads rapidly repair low/conflict geometry. Downgrade the whole dynamic mechanism if frozen heads remove the aligned greater than low/conflict gap.

## 1. Decision Question

Does the output-row geometry that explains A11_08's step-0 general-K hidden semantic velocity remain an explanatory mechanism during early training, or is the observed training behavior mainly caused by output-head co-adaptation?

## 2. Terminology / Definitions

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- | --- |
| Early variable `Z` | Controlled branch identity | `Z in {1,...,m}` | categorical | Synthetic proxy for long-horizon semantic information | Natural-language semantics |
| Decision hidden state `h_T` | State being supervised by future-token losses | Branch state `h_z(t)=h_T(Z=z,t)` | vector | Target of the hidden-update mechanism | All positions in LM training |
| Output row | Prediction-head row for a target token | `u_{S_z}^{(3)}(t)` or `u_{T_z}^{(4)}(t)` | vector | Defines the direction a target gives to `h_T` | Representation quality by itself |
| Centered output direction | Branch-specific row after removing the branch mean | `u_{S_z}^{(3)}(t)-\bar u_3(t)` | vector | Removes shared direction and keeps the semantic branch direction | Downstream utility |
| Reference geometry | Step-0 output-row geometry | rows at `t=0` | vector / scalar | Tests whether initial A11_08 geometry explains later updates | Co-adapted current heads |
| Current geometry | Output-row geometry at evaluation step `t` | rows at step `t` | vector / scalar | Tests whether trainable heads rotate or drift | Initial mechanism alone |
| Hidden semantic velocity | Loss gradient projected onto semantic readout direction | `G_K^{hidden}(t)` | scalar | Main mechanism metric | Full sample efficiency |
| Readout margin | Alignment between `h_T` and semantic output directions | `M_Z(t)` | scalar | Shows whether hidden states accumulate semantic readout signal | Whether the signal is used naturally |
| Guarded recovery score | Conservative observable recovery score | `Q_eval(t)=min(A_dec,A_probe,C_swap)` | accuracy | Prevents relying on a single fragile readout | Direct supervision proof in all-position settings |
| Local guard | Near-future target quality | Y1/Y2 CE loss and accuracy | loss / accuracy | Ensures semantic movement does not damage local prediction | Full LM quality |

## 3. Physical Priors

**P1: Static-geometry prior.** A11_08 is a first-order statement about output-row geometry at a fixed point. It should not automatically explain multi-step training if output rows move.

**P2: Frozen-head audit prior.** If the geometry is a hidden-update mechanism, freezing output heads should preserve the aligned greater than low/conflict ordering in hidden semantic velocity and readout margin.

**P3: Co-adaptation prior.** If trainable heads quickly rotate low/conflict rows toward aligned rows, later training curves should be interpreted as output-head co-adaptation, not as evidence that the initial geometry remained causal.

**P4: Guard prior.** `shared_only_k4` must stay near zero and `single_h3` must stay positive; otherwise the measurement is not auditing the intended mechanism.

## 4. Mathematical Model

For branch `z`, define the centered horizon-3 and horizon-4 rows:

$$
a_{3,z}(t)=\lambda_3\left(u_{S_z}^{(3)}(t)-\bar u_3(t)\right),
\qquad
a_{4,z}(t)=\lambda_4\left(u_{T_z}^{(4)}(t)-\bar u_4(t)\right).
$$

The current aggregate semantic direction is:

$$
v_z^{cur}(t)=\sum_{j\in\mathcal I_K}a_{j,z}(t).
$$

The reference aggregate semantic direction freezes the A11_08 step-0 geometry:

$$
v_z^{ref}=v_z^{cur}(0).
$$

Current-geometry hidden semantic velocity:

$$
G_{K,current}^{hidden}(t)=\frac1m\sum_z v_z^{cur}(t)^\top\left(-\nabla_{h_z}L_K(t)\right).
$$

Reference-geometry hidden semantic velocity:

$$
G_{K,ref}^{hidden}(t)=\frac1m\sum_z v_z^{ref\top}\left(-\nabla_{h_z}L_K(t)\right).
$$

Current and reference readout margins:

$$
M_Z^{current}(t)=\frac1m\sum_z v_z^{cur}(t)^\top h_z(t),
\qquad
M_Z^{ref}(t)=\frac1m\sum_z v_z^{ref\top}h_z(t).
$$

Output-geometry cosine for the two informative horizons:

$$
\cos_{34}(t)=\frac1m\sum_z
\frac{
\left(u_{S_z}^{(3)}(t)-\bar u_3(t)\right)^\top
\left(u_{T_z}^{(4)}(t)-\bar u_4(t)\right)
}{
\left\|u_{S_z}^{(3)}(t)-\bar u_3(t)\right\|
\left\|u_{T_z}^{(4)}(t)-\bar u_4(t)\right\|+\epsilon
}.
$$

Head drift norm:

$$
D_u(t)=
\left(
\sum_{j\in\{3,4\}}\sum_z
\left\|u_z^{(j)}(t)-u_z^{(j)}(0)\right\|^2
\right)^{1/2}.
$$

Guarded recovery:

$$
Q_{eval}(t)=
\min\{A_{decoder}(t),A_{probe}(t),C_{swap}(t)\}.
$$

## 5. Falsifiable Hypotheses

**H1: Frozen-head mechanism hypothesis.** With frozen output heads, `aligned_h3_h4` should have larger early `G_K_hidden`, `M_Z`, and `Q_eval` than `low_conflict_h3_h4`, while `shared_only_k4` remains near zero and `single_h3` remains positive.

**H2: Trainable-head co-adaptation hypothesis.** With trainable output heads, `low_conflict_h3_h4` may quickly increase `cos_34(t)` and reduce its geometry gap with `aligned_h3_h4`. If this happens before hidden recovery separates, A11_08 training curves cannot be explained by the initial geometry alone.

**H3: Static-only failure hypothesis.** If frozen heads remove the aligned greater than low/conflict gap, then A11_08 should be downgraded from a dynamic hidden-update explanation to a step-0 or output-head co-adaptation phenomenon.

## 6. Experimental Realization

Reuse the A11_08 clean decision-only setup:

```text
shared_only_k4:     Y1=A_SHARED, Y2=C_SHARED, Y3=A_SHARED, Y4=C_SHARED
single_h3:          Y1=A_SHARED, Y2=C_SHARED, Y3=S_z,      Y4=A_SHARED
aligned_h3_h4:      Y1=A_SHARED, Y2=C_SHARED, Y3=S_z,      Y4=T_z
low_conflict_h3_h4: Y1=A_SHARED, Y2=C_SHARED, Y3=S_z,      Y4=T_z
```

Run exactly two output-head variants:

```text
trainable_heads: A11_08 default; prediction heads train during optimization.
frozen_heads: prediction heads are fixed at initialization; trunk / hidden-state-producing parameters train.
```

Seeds:

```text
971, 972, 973, 974, 975
```

No broader ablation is included in this anchor.

## 7. Required Metrics

| Metric | Expression | Measures | Decision use |
| --- | --- | --- | --- |
| `cos_34(t)` | see Section 4 | Whether horizon-3 and horizon-4 semantic rows are aligned, low, or conflicting over time | Detects geometry repair or drift |
| `D_u(t)` | see Section 4 | How far semantic output rows moved from initialization | Separates static geometry from trainable-head co-adaptation |
| `G_K_hidden_current(t)` | `m^-1 sum_z v_z^cur(t)^T(-grad_hz L_K(t))` | Current-head semantic update velocity | Shows what current heads are asking `h_T` to do |
| `G_K_hidden_ref(t)` | `m^-1 sum_z v_z^ref^T(-grad_hz L_K(t))` | Step-0 geometry update velocity | Tests whether the original A11_08 geometry still explains updates |
| `M_Z_current(t)` | `m^-1 sum_z v_z^cur(t)^T h_z(t)` | Current-head semantic readout margin | Measures accumulated current-geometry branch signal |
| `M_Z_ref(t)` | `m^-1 sum_z v_z^ref^T h_z(t)` | Step-0 geometry semantic margin | Measures accumulated signal in the original A11_08 direction |
| `Q_eval(t)` | `min(A_decoder,A_probe,C_swap)` | Conservative branch recovery | Prevents relying on one readout |
| Y1/Y2 local loss and accuracy | CE and accuracy on shared targets | Local next-token quality | Guards against semantic gain by local damage |

## 8. Minimal Tests And Decision Rules

| Test | Support | Weakens / falsifies | Meaning |
| --- | --- | --- | --- |
| Frozen-head aligned gap | `aligned_h3_h4 > low_conflict_h3_h4` in early `G_K_hidden` and `M_Z`, at least 4/5 seeds | gap disappears or reverses after guards pass | Output geometry is a hidden-update mechanism |
| Trainable-head drift audit | low/conflict remains low/conflict while hidden gap follows geometry | low/conflict rapidly becomes aligned | Training curves cannot be explained by initial geometry alone |
| Shared zero guard | `shared_only_k4` stays near zero for semantic metrics | stable positive semantic signal | Leakage or metric contamination |
| Single positive guard | `single_h3` stays positive | no positive signal | Mechanism measurement failed |
| Local guard | Y1/Y2 loss and accuracy remain healthy | semantic recovery trades off local targets | Efficiency claim is not clean |

## 9. Current Evidence

A11_08b full run:

```text
job id: pt-yppwndnm
run name: a11_08b_output_geometry_dynamics_full_20260709_1225
seeds: 971, 972, 973, 974, 975
verdict: support for hidden semantic velocity mechanism; partial for final recovery
```

Primary frozen-head evidence:

| Condition | early AUC `G_hidden_ref` | early AUC `M_Z_ref` | early AUC `Q` | final `M_Z_ref` | final `Q` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `shared_only_k4` | 0.000000 | 0.000 | 0.250 | 0.000 | 0.250 |
| `single_h3` | 0.000783 | 0.758 | 0.392 | 1.198 | 0.400 |
| `aligned_h3_h4` | 0.002660 | 3.238 | 0.478 | 5.189 | 0.500 |
| `low_conflict_h3_h4` | 0.000184 | 0.128 | 0.428 | 0.180 | 0.500 |

Decision evidence:

```text
frozen aligned > low/conflict in early AUC G_hidden_ref: 5 / 5 seeds
frozen shared-only velocity: 0
frozen single-h3 velocity: positive
Y1/Y2 final accuracy: 1.0 / 1.0
trainable low/conflict cos_34: -1.000 -> -0.268
trainable low/conflict head drift: 2.194
```

Interpretation:

```text
A11_08's output geometry remains explanatory for hidden semantic velocity when
heads are frozen. Trainable heads drift substantially, so trainable curves
should be read with current geometry recorded. Final margin and Q are secondary
and less seed-stable than the velocity metric.
```

Source records:

```text
Projects/from-attention-to-search/main/experiments/A11/A11_08b_output_geometry_dynamics_audit/protocol.md
Projects/from-attention-to-search/main/experiments/A11/A11_08b_output_geometry_dynamics_audit/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_08b_output_geometry_dynamics_audit/detailed.md
```

## 10. Claim Boundary

Can claim if supported:

```text
In the controlled clean decision-only setting, A11_08's output-row geometry is
not merely a step-0 artifact: when heads are frozen, aligned informative
horizon directions still induce stronger hidden semantic updates than
low/conflicting directions.
```

Can also claim if trainable-head drift is observed:

```text
Training curves with trainable heads must be interpreted through current output
geometry, not only through the initial geometry.
```

Cannot claim:

```text
Natural-language MTP is better than NTP.
All-position indirect transfer is explained.
Larger K is generally better.
Output geometry alone proves downstream usefulness.
```

## 11. Next Decision

11_08b supports proceeding to 11_09 next-K inclusion law:

```text
Compare K=2, K=3, and K=4 to test whether semantic velocity turns on exactly
when K first includes an informative future horizon, stays near zero when K
only adds uninformative horizons, and changes by the predicted vector increment
when K adds another informative horizon.
```

If later all-position or trainable-head extensions are attempted, keep reference/current output geometry diagnostics in the protocol.
