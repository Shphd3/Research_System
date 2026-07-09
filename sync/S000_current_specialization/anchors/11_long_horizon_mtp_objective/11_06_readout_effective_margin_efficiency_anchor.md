# 11_06 Readout-Effective Margin Efficiency Anchor

Status: completed.  
Parent line: `11_long_horizon_mtp_objective`.  
Prior anchor: `11_05_semantic_efficiency_bridge_anchor.md`.

## 0. Thinking Card

**Phenomenon:** A11 has proven that covering the first informative future horizon forces the current prefix state `h_T` to contain the delayed variable `Z` when the informative-horizon loss is low. The remaining gap is learning efficiency: does the covering objective move `h_T` toward a useful `Z` representation earlier than NTP / non-covering MTP?

**Mechanism guess:** In clean `tau=3` data, K=3 contains the direct informative loss `CE(q_3(.|h_T), S_Z)`. At a branch-collapsed initialization, K=1 and K=2 produce only branch-shared updates at the decision prefix, while K=3 pushes each branch state toward the output vector of its own `S_Z`. This should create positive first-order readout-effective semantic margin growth.

**Key variables:** delayed variable `Z`; prefix state `h_T`; branch state `h_z`; first informative horizon `tau=3`; active horizon K; horizon-3 output row `u_{S_z}`; readout-effective margin `M_Z`; separation energy `E_Z`; local targets `Y_1=A`, `Y_2=C`.

**Causal relation:** If the informative-horizon term is the efficiency source, then one gradient step using K=3 should increase `M_Z` more than K=1/K=2 before multi-step training dynamics or all-position indirect transfer can intervene.

**Observable metric:** Primary metric is finite-difference margin growth `Delta M_Z / eta` after one controlled update. Secondary metrics are `Delta E_Z / eta^2`, local-loss change, and short-run `Q(t)`.

**Alternative explanation:** K=3 may appear better only because of larger gradient norm, random branch leakage, probe false positives, or all-position indirect transfer. This anchor blocks those explanations by using branch-collapsed initialization, decision-only loss, output-facing margin, and one-step counterfactuals.

**Decision rule:** Supported. In the implemented Transformer, the theorem-facing
activation-space metric `G_M_hidden` is positive for K3 and near zero for K1/K2,
with no step-0 leakage. Parameter-space finite-difference `Delta M_Z / eta` is
too small and numerically unstable, so it is kept as an auxiliary self-check
rather than the primary metric.

## 1. Problem Definition

Parent problem: prove, in a controlled meaning, that MTP learns long-horizon semantic information more efficiently than NTP.

This anchor narrows efficiency to a first-order optimization quantity:

```text
Does the informative-horizon loss create immediate readout-effective semantic margin growth at h_T?
```

This is intentionally earlier than multi-step `T_0.9`. If the one-step margin mechanism fails, later learning-curve claims become hard to interpret.

## 2. Terminology / Definitions

| Term | Plain meaning | Concrete object | Formula / unit | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| delayed variable `Z` | early branch variable needed later | branch identity in `BR_z` | categorical | target long-horizon variable | natural-language semantics |
| branch state `h_z` | decision-prefix hidden state under branch `z` | `h_T(z)` | vector | representation being shaped | all sequence states |
| informative horizon `tau` | first future offset containing `Z` | clean task has `tau=3` | token offset | defines coverage | fixed real horizon in text |
| readout-effective margin `M_Z` | whether `h_z` moves toward the correct future-token output direction | centered output-row projection | scalar | first-order efficiency target | final recovery |
| separation energy `E_Z` | whether branch states separate in hidden space | pairwise state distance | scalar | probe / route-separation proxy | output usability |
| local guard | whether shared local predictions remain intact | `Y_1/Y_2` CE and accuracy | CE / accuracy | rules out tradeoff | full LM quality |
| one-step update | controlled infinitesimal or small SGD update | clone model and update once | finite difference | isolates gradient mechanism | full training dynamics |

## 3. Physical Priors

**P1: Shared-target prior.** In the clean `tau=3` task, K=1 and K=2 only see branch-shared targets at the decision prefix. They should not create branch-specific readout-effective updates at first order.

**P2: Informative-target prior.** K=3 sees `S_Z`; its gradient should push `h_z` toward the output row for `S_z`.

**P3: Output-facing prior.** Hidden-state branch separation is not enough. The useful quantity is separation aligned with the future-token output directions.

**P4: Local-preservation prior.** An efficiency win is clean only if it does not worsen the branch-shared targets `A` and `C`.

## 4. Falsifiable Hypotheses

**H1: First-order margin advantage.**

K=3 has larger one-step readout-effective margin growth than K=1/K=2:

$$
\Delta M_Z(K=3)/\eta > \Delta M_Z(K=1)/\eta,\quad \Delta M_Z(K=2)/\eta.
$$

**H2: Non-covering horizons are first-order inactive for semantic margin.**

In branch-collapsed decision-only setup:

$$
\Delta M_Z(K=1)/\eta\approx0,\qquad \Delta M_Z(K=2)/\eta\approx0.
$$

**H3: Branch separation acceleration.**

K=3 gives positive second-order separation growth:

$$
\Delta E_Z(K=3)/\eta^2>0,
$$

while K=1/K=2 remain near zero.

**H4: Local guard.**

The K=3 one-step margin gain must not increase local `Y_1/Y_2` loss beyond tolerance.

## 5. Mathematical Model

Clean `tau=3` data:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

Trainable branch-prefix states:

$$
h_z\in\mathbb R^d,\qquad z=1,\ldots,m.
$$

Prediction heads:

$$
q_j(\cdot\mid h_z)=\operatorname{softmax}(U_jh_z).
$$

Let:

$$
u_z=u_{S_z}^{(3)},\qquad \bar u=\frac1m\sum_z u_z.
$$

Define readout-effective semantic margin:

$$
M_Z(h)=\frac1m\sum_z (u_z-\bar u)^\top h_z.
$$

Define branch separation energy:

$$
E_Z(h)=\frac{1}{2m^2}\sum_{z,z'}\|h_z-h_{z'}\|^2.
$$

Assume branch-collapsed initialization:

$$
h_1(0)=\cdots=h_m(0)=h_0.
$$

Losses:

$$
L_1=\frac1m\sum_z\operatorname{CE}(q_1(\cdot\mid h_z),A),
$$

$$
L_2=L_1+\frac{\lambda_2}{m}\sum_z\operatorname{CE}(q_2(\cdot\mid h_z),C),
$$

$$
L_3=L_2+\frac{\lambda_3}{m}\sum_z\operatorname{CE}(q_3(\cdot\mid h_z),S_z).
$$

## 6. Theorem State

**Theorem: first-order readout-effective margin separation.**

Under the mathematical model above, if output rows `u_z` are not all equal, gradient flow on the branch states gives:

$$
G_1^{margin}=0,\qquad G_2^{margin}=0,\qquad G_3^{margin}=\frac{\lambda_3}{m^2}\sum_z\|u_z-\bar u\|^2>0,
$$

where:

$$
G_K^{margin}=\left.\frac{d}{ds}M_Z(h(s))\right|_{s=0},\qquad \dot h_z=-\nabla_{h_z}L_K.
$$

**Proof sketch:** K=1/K=2 shared targets produce identical branch updates, so centered output-row projections cancel. K=3 includes target `S_z`; the gradient-flow velocity is proportional to `u_z - U_3^T p`, and the common `U_3^T p` term cancels after centering, leaving the positive sum of squared centered output rows.

**Auxiliary theorem: second-order separation energy.**

At branch-collapsed initialization, one-step K=3 updates create positive hidden-state separation:

$$
E_Z(h^+)=\frac{\eta^2\lambda_3^2}{2m^4}\sum_{z,z'}\|u_z-u_{z'}\|^2>0,
$$

while K=1/K=2 remain zero in the ideal model.

## 7. Computational Realization

Use the existing clean `tau=3` synthetic generator:

```text
BR_z F... U A_SHARED C_SHARED S_z
```

Run decision-only training first.

Conditions:

```text
K1_fixed_3head
K2_active
K3_active
```

Primary diagnostic is one-step controlled SGD from the same initialization.

Required outputs:

```text
Delta_M_over_eta
G_M_hidden
Delta_E_over_eta2
Delta_local_Y1_CE
Delta_local_Y2_CE
Delta_Q_after_one_step
short_curve_Q
short_curve_M_Z
short_curve_E_Z
```

## 8. Minimal Tests

| Test | Comparison | Primary metric | Support | Weaken |
|---|---|---|---|---|
| Margin one-step | K1/K2/K3 from same init | `Delta M_Z / eta` | K3 positive, K1/K2 near zero | K3 not larger |
| Separation one-step | K1/K2/K3 | `Delta E_Z / eta^2` | K3 positive | K1/K2 also positive without leakage explanation |
| Local guard | before/after one step | `Delta Y1/Y2 CE` | no local degradation | local CE worsens materially |
| Short learning curve | 0-2000 steps | `Q(t)`, `M_Z(t)`, `E_Z(t)` | K3 rises earlier | no early difference |
| Leakage audit | step 0 | `Q(0)`, `M_Z(0)`, `E_Z(0)` | near chance / near zero | saturated at init |

## 9. Claim Boundary

Current evidence:

```text
A11_06 full run completed on job pt-57nu5dv1. Step-0 leakage gate passed:
Q(0)=0.25, M_Z(0)≈0, E_Z(0)=0, native H3=0. The theorem-facing metric
G_M_hidden was near zero for K1/K2 and positive for K3:
K1=7.28e-12, K2=-1.16e-11, K3=0.003816 at eta=3e-4 summary. Short
decision-only curves also separated: K1/K2 early AUC Q=0.250, K3 early AUC
Q=0.535, K3 reach rate=0.40.
```

Can claim:

```text
In the controlled tau=3 decision-prefix setup, the informative K=3 target creates strictly positive first-order readout-effective semantic margin growth, while non-covering K=1/K=2 do not under branch-collapsed assumptions.
```

Cannot claim:

```text
Full multi-step efficiency is proven.
All-position NTP cannot recover Z.
Natural-language MTP benefit follows.
MoE route utility follows.
```

## 10. Next Decision

Completed: 11_07 was run after 11_06. The next line-level decision is to update
the A11 story: direct informative-horizon supervision is supported as a
first-order hidden-state margin mechanism, while full all-position recovery
must be interpreted with indirect-transfer controls.
