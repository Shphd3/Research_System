# 11_08 General-K Readout-Margin Dynamics Anchor

Status: proposed daily anchor.  
Parent line: `11_long_horizon_mtp_objective`.  
Purpose: test the general-K theorem behind MTP semantic efficiency.

## 0. Thinking Card

**Phenomenon:** Existing A11 results show K=3 helps in a clean `tau=3` task because it is the first horizon covering `S_Z`. The current theory should not stay K=3-specific. We need to know how the mechanism behaves when several future horizons contain the early variable.

**Mechanism guess:** Each informative future horizon contributes a centered output direction `u_{j,z}-bar u_j` to the branch-specific update of `h_T(z)`. The total readout-effective margin velocity is the squared norm of the weighted sum of these centered directions. Therefore, aligned future horizons amplify the semantic update, while conflicting horizons can reduce or cancel it.

**Key variables:** early variable `Z`; current state `h_T`; active horizon K; informative horizon set `I_K`; centered output direction `u_{j,z}-bar u_j`; aggregate semantic direction `v_z^(K)`; readout-effective margin `M_K`; one-step margin velocity `G_K`.

**Causal relation:** If general-K efficiency is driven by additive aligned future supervision, then adding an informative horizon with aligned branch-output directions should increase `Delta M_K / eta`; adding an uninformative horizon should not; adding a conflicting informative horizon may reduce or destabilize the margin speed.

**Observable metric:** Primary metric is `Delta M_K / eta` from one-step decision-prefix updates. Secondary metrics are `Delta E_Z / eta^2`, native informative-horizon accuracy, and local-target guard.

**Alternative explanations:** Improvements may come from loss scale, more heads, probe-only recovery, or random branch leakage. Controls must keep architecture fixed, audit step-0 leakage, and compare aligned / orthogonal / conflicting informative-horizon constructions.

**Decision rule:** Support if the observed one-step margin velocity follows the vector-sum prediction across aligned, orthogonal, uninformative, and conflicting horizon regimes.

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
| uninformative added horizon | add shared `Y_r=A_r` | `Delta M/eta` | no increase | increase without leakage explanation |
| aligned informative horizon | `a_{r,z}` aligned with existing `v_z` | `Delta M/eta` | predicted increase | no increase |
| orthogonal informative horizon | centered directions orthogonal on average | velocity increases by norm term only | match prediction | mismatch |
| conflicting informative horizon | centered directions partly negative | velocity reduces or grows less | non-monotonic pattern appears | K always improves despite conflict |
| local guard | all regimes | Y1/Y2/shared CE | no degradation | semantic gain trades off local targets |

## 6. Experimental Realization

Use decision-only training with synthetic branch suffixes. Create horizon regimes where the output rows or target codes induce different centered direction relations.

The preferred implementation is to control target-code assignment across horizons rather than manually editing model weights:

```text
aligned: S_{2,z}, S_{3,z} use same branch ordering
permuted/orthogonal: S_{3,z} uses a balanced permutation with low centered correlation
conflicting: S_{3,z} uses reversed or antagonistic branch mapping when output geometry permits
uninformative: Y_j shared or noise independent of Z
```

For each regime, run one-step diagnostics from matched initialization and compare observed `Delta M/eta` with the theorem prediction computed from output rows.

## 7. Claim Boundary

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

## 8. Next Decision

If 11_08 passes, use the measured direction-alignment law to design harder multi-horizon datasets. If it fails, the current K=3 margin theorem remains valid but does not generalize as a simple additive-direction story.
