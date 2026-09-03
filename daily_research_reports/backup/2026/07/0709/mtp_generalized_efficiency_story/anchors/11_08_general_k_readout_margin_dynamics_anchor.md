# 11_08 General-K Readout-Margin Dynamics Anchor

Status: supported by A11_08 full run on 2026-07-09.  
Parent line: `11_long_horizon_mtp_objective`.  
Purpose: test the general-K theorem behind MTP semantic efficiency.

## 0. researcher judgment record

**Phenomenon:** Existing A11 results show K=3 helps in a clean `tau=3` task because it is the first horizon covering `S_Z`. The current theory should not stay K=3-specific. We need to know how the mechanism behaves when several future horizons contain the early variable.

**Mechanism guess:** Each informative future horizon contributes a centered output direction `u_{j,z}-bar u_j` to the branch-specific update of `h_T(z)`. The total readout-effective margin velocity is the squared norm of the weighted sum of these centered directions. Therefore, aligned future horizons amplify the semantic update, while conflicting horizons can reduce or cancel it.

**Key variables:** early variable `Z`; current state `h_T`; active horizon K; informative horizon set `I_K`; centered output direction `u_{j,z}-bar u_j`; aggregate semantic direction `v_z^(K)`; readout-effective margin `M_K`; one-step margin velocity `G_K`.

**Causal relation:** If general-K efficiency is driven by additive aligned future supervision, then adding an informative horizon with aligned branch-output directions should increase `G_K_hidden`; adding an uninformative horizon should not; adding a conflicting informative horizon may reduce or destabilize the margin speed.

**Observable metric:** Primary metric is the one-step hidden-gradient semantic velocity `G_K_hidden`, the activation-space derivative of the aggregate readout-effective margin. Secondary metrics are `Delta M_K / eta`, `Delta E_Z / eta^2`, native informative-horizon accuracy, guarded `Q_eval`, and local-target guard.

**Alternative explanations:** Improvements may come from loss scale, more heads, probe-only recovery, or random branch leakage. Controls must keep architecture fixed, audit step-0 leakage, and compare aligned / orthogonal / conflicting informative-horizon constructions.

**Decision rule:** Support if the observed one-step hidden-gradient semantic velocity follows the vector-sum prediction across shared-only, single-informative, aligned two-informative, and low/conflicting two-informative horizon regimes.

## 1. Decision Question

Does the first-order readout-effective semantic margin under next-K prediction equal the contribution predicted by the active informative horizons, and does this explain when increasing K helps or fails?

## 2. Definitions

Let `Z in {1,...,m}` be the early variable. For each branch, the decision state is:

$$
h_z=h_T(Z=z).
$$

For each future horizon `j`, the head is:

$$
q_j(\cdot\mid h_z)=\operatorname{softmax}(U_jh_z).
$$

Informative horizons:

$$
\mathcal I_K=\{j\le K:Y_j=S_{j,Z}\text{ and }Z\mapsto S_{j,Z}\text{ is one-to-one}\}.
$$

Centered output row:

$$
a_{j,z}=\lambda_j(u_{j,z}-\bar u_j),\qquad \bar u_j=\frac1m\sum_z u_{j,z}.
$$

Aggregate branch direction:

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}a_{j,z}.
$$

Readout-effective K-margin:

$$
M_K(h)=\frac1m\sum_z v_z^{(K)\top}h_z.
$$

## 3. Physical Priors

**P1: Informative-horizon prior.** Only horizons that contain branch information should contribute branch-specific first-order updates.

**P2: Direction-alignment prior.** Multiple informative horizons help more when their centered output directions are aligned in branch space.

**P3: Non-monotonic-K prior.** Increasing K can fail if the newly added horizon is uninformative, noisy, or direction-conflicting.

**P4: Local-guard prior.** A larger margin velocity is not a clean efficiency win if shared local targets are harmed.

## 4. Mathematical Claim

Under branch-collapsed initialization:

$$
h_1=\cdots=h_m=h_0,
$$

and fixed heads for the one-step analysis, gradient flow on:

$$
L_K=\frac1m\sum_z\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_z),Y_j(z))
$$

gives:

$$
G_K=\left.\frac{d}{ds}M_K(h(s))\right|_{s=0}=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2.
$$

Consequences:

1. If `I_K` is empty, then `G_K=0`.
2. If `v_z^(K)` is not identically zero, then `G_K>0`.
3. Adding a new informative horizon `r` changes the velocity by:

$$
G_{K\cup r}-G_K=\frac1{m^2}\sum_z(2v_z^{(K)\top}a_{r,z}+\|a_{r,z}\|^2).
$$

Therefore monotonic improvement requires alignment, not merely larger K.

## 5. Minimal Tests

| Test | Construction | Primary metric | Support | Weaken |
|---|---|---|---|---|
| uninformative added horizon | add shared `Y_r=A_r` | `G_K_hidden` | no increase | increase without leakage explanation |
| aligned informative horizon | `a_{r,z}` aligned with existing `v_z` | `G_K_hidden` | predicted increase | no increase |
| orthogonal informative horizon | centered directions orthogonal on average | velocity increases by norm term only | match prediction | mismatch |
| conflicting informative horizon | centered directions partly negative | velocity reduces or grows less | non-monotonic pattern appears | K always improves despite conflict |
| local guard | all regimes | Y1/Y2/shared CE | no degradation | semantic gain trades off local targets |

## 6. Experimental Realization

Use decision-only training with synthetic branch suffixes. Create horizon regimes where the output rows or target codes induce different centered direction relations.

The implemented minimal falsifier controls output-row geometry directly because
target-code permutation alone may not create a large enough geometry gap in high
dimension:

```text
shared_only_k4:     Y1=A, Y2=C, Y3=A,   Y4=C
single_h3:          Y1=A, Y2=C, Y3=S_z, Y4=A
aligned_h3_h4:      Y1=A, Y2=C, Y3=S_z, Y4=T_z
low_conflict_h3_h4: Y1=A, Y2=C, Y3=S_z, Y4=T_z
```

For each regime, run one-step diagnostics from matched initialization and
compare observed `G_K_hidden` with the theorem prediction computed from output
rows.

## 7. Current Evidence

A11_08 full run:

```text
run name: a11_08_general_k_readout_margin_full_20260709_051147
seeds: 971, 972, 973, 974, 975
K: 4
active horizons: 1, 2, 3, 4
verdict: support
```

Primary result:

| Condition | `G_pred_batch_scaled` | `G_hidden` |
|---|---:|---:|
| `shared_only_k4` | 0.000000 | 0.000000 |
| `single_h3` | 0.003816 | 0.003816 |
| `aligned_h3_h4` | 0.015262 | 0.015262 |
| `low_conflict_h3_h4` | 0.000954 | 0.000954 |

Decision evidence:

```text
geometry precondition: pass
aligned > low/conflict: 5 / 5 seeds
shared zero guard: pass
single positive guard: pass
local Y1/Y2 guard: pass
falsifier: did not fire
```

Source records:

```text
Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/protocol.md
Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/detailed.md
```

## 8. Claim Boundary

Can claim if supported:

```text
General-K MTP efficiency is governed by the vector sum of readout-effective branch directions from informative horizons; larger K helps only when added horizons contribute aligned branch-relevant directions.
```

Cannot claim:

```text
K larger is always better.
Natural-language MTP benefit follows.
All-position training will follow the same monotonic pattern without indirect transfer controls.
```

## 9. Next Decision

Do not move to MoE yet. The next anchor should test the next-2 / next-3 /
next-K inclusion law:

```text
When K increases, does first-order semantic velocity turn on exactly when K
first includes an informative future horizon, remain near zero when the added
horizon is uninformative, and change by the predicted vector increment when the
added horizon is informative?
```

If this inclusion-law anchor passes, the story can then use the aggregate
semantic direction as a cleaner candidate bridge object for route-relevance or
MoE geometry.
