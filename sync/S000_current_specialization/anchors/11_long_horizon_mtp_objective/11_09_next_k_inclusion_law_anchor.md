# 11_09 Next-K Inclusion Law Anchor

Status: supported by A11_09 full run on 2026-07-09.  
Parent line: `11_long_horizon_mtp_objective`.  
Purpose: test whether semantic velocity changes when K includes informative horizons, rather than when K merely becomes larger.

## 0. Thinking Card

**Phenomenon:** A11_08 supports a general-K vector-sum mechanism at fixed K=4. The next question is whether increasing K opens semantic velocity exactly when the newly included future position contains the early variable `Z`.

**Mechanism guess:** A horizon contributes to hidden semantic velocity only if its target is a one-to-one branch code for `Z`. Adding an uninformative shared horizon should add no semantic direction. Adding a second informative horizon should change velocity by its vector increment; aligned directions amplify, low/conflicting directions weaken or cancel.

**Key variables:** prediction range `K`; early variable `Z`; informative horizon set `I_K`; centered output direction `a_{j,z}`; aggregate semantic direction `v_z^(K)`; hidden semantic velocity `G_K_hidden`.

**Causal relation:** If `K` does not cover an informative target, `v_z^(K)=0`. If `K` first covers `S_z`, semantic velocity turns on. If `K` adds only a shared target, velocity should not materially increase. If `K` adds another informative target, the velocity increment depends on direction alignment.

**Observable metric:** Primary metric is one-step / early hidden semantic velocity `G_K_hidden_ref/current`; secondary metrics are `M_Z_ref/current`, `Q_eval`, output geometry, and Y1/Y2 local guards.

**Alternative explanations:** Larger K may appear better due to more losses, larger gradient norm, output-head drift, or local target tradeoff. This anchor uses clean decision-only training with frozen heads after 11_08b smoke, fixed max heads, and local guards.

**Decision rule:** Support if K2 is near zero when it excludes `S_z`, K3 turns on when it includes `S_z`, K4 does not materially increase for a shared fourth horizon, and K4 changes according to the vector increment for aligned versus low/conflict second informative horizons.

## 1. Decision Question

When K increases from 2 to 3 to 4, does hidden semantic velocity turn on only when K includes an informative future horizon, and does the next increment follow the general-K vector-sum law?

## 2. Definitions

Informative horizons:

$$
\mathcal I_K=\{j\le K:Y_j=S_{j,Z}\text{ is a one-to-one code of }Z\}.
$$

Centered output direction:

$$
a_{j,z}=\lambda_j(u_{j,z}-\bar u_j).
$$

Aggregate semantic direction:

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}a_{j,z}.
$$

Hidden semantic velocity:

$$
G_K^{hidden}=\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K).
$$

Vector increment from a new informative horizon:

$$
G_{K+1}-G_K=
\frac1{m^2}\sum_z\left(2v_z^{(K)\top}a_{K+1,z}+\|a_{K+1,z}\|^2\right).
$$

## 3. Minimal Tests

| Case | Conditions | Prediction |
| --- | --- | --- |
| no informative horizon | `shared_only_k4`, any K | `G_K_hidden` near zero |
| K below first informative horizon | `single_h3`, `K2_active` | `G_K_hidden` near zero |
| first informative horizon included | `single_h3`, `K3_active` | semantic velocity turns on |
| added horizon is uninformative | `single_h3`, `K4_active` | no material increase over K3 |
| second informative horizon aligned | `aligned_h3_h4`, K3 to K4 | positive vector increment |
| second informative horizon low/conflict | `low_conflict_h3_h4`, K3 to K4 | weak or reduced increment |

## 4. Experimental Realization

Reuse the clean decision-only A11_08 construction with frozen heads:

```text
conditions: K2_active, K3_active, K4_active
data regimes: shared_only_k4, single_h3, aligned_h3_h4, low_conflict_h3_h4
head variant: frozen_heads
seeds: 971, 972, 973, 974, 975
```

## 5. Current Evidence

A11_09 full run:

```text
job id: pt-9an690sp
run name: a11_09_next_k_inclusion_law_full_20260709_1228
seeds: 971, 972, 973, 974, 975
head variant: frozen_heads
verdict: support
```

One-step hidden semantic velocity at `eta=0.0003`:

| Regime | K2 | K3 | K4 | K3-K2 | K4-K3 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `shared_only_k4` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `single_h3` | 0.000000 | 0.003816 | 0.003816 | 0.003816 | -0.000000 |
| `aligned_h3_h4` | 0.000000 | 0.003816 | 0.015262 | 0.003816 | 0.011447 |
| `low_conflict_h3_h4` | 0.000000 | 0.003816 | 0.000954 | 0.003816 | -0.002862 |

Seed support:

```text
single_h3: K3>K2 in 5/5, K4>K3 in 0/5
aligned_h3_h4: K3>K2 in 5/5, K4>K3 in 5/5
low_conflict_h3_h4: K3>K2 in 5/5, K4>K3 in 0/5
```

Interpretation:

```text
Direct semantic velocity turns on when K first includes an informative horizon.
Adding an uninformative horizon gives no one-step semantic increment. Adding a
second informative horizon changes velocity according to the centered
output-direction increment: aligned amplifies, low/conflict weakens.
```

Source records:

```text
Projects/from-attention-to-search/main/experiments/A11/A11_09_next_k_inclusion_law/protocol.md
Projects/from-attention-to-search/main/experiments/A11/A11_09_next_k_inclusion_law/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_09_next_k_inclusion_law/detailed.md
```

## 6. Claim Boundary

Can claim if supported:

```text
In the controlled decision-only setting, increasing K changes semantic velocity
only through newly included informative horizons and their readout-direction
alignment; larger K by itself is not the causal object.
```

Cannot claim:

```text
Natural-language MTP is more efficient than NTP.
Larger K never helps.
All-position indirect transfer follows the same clean rule.
MoE routing utility follows.
```

## 7. Next Decision

Update the A11 story from "general-K vector sum at fixed K" to "next-K inclusion law under controlled frozen-head decision-prefix dynamics." Do not bridge to MoE yet without a separate route-relevance protocol.
