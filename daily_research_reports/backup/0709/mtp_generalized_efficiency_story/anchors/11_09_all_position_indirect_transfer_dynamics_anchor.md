# 11_09 All-Position Indirect-Transfer Dynamics Anchor

Status: proposed daily anchor.  
Parent line: `11_long_horizon_mtp_objective`.  
Purpose: explain when all-position NTP / non-covering MTP can still make `Z` readable from `h_T`.

## 0. Thinking Card

**Phenomenon:** A11_07 shows that non-direct conditions can reach nontrivial guarded recovery `Q`, even when native `h_T -> S_Z` accuracy and readout-effective margin remain near zero. This means all-position training can create probe-readable `Z` through indirect transfer.

**Mechanism guess:** A loss at another position `s` can update the current state `h_T` through shared parameters. The first-order transfer is controlled by the cross-position parameter kernel `K_{T,s}=J_TJ_s^T`, where `J_T=partial h_T/partial theta` and `J_s=partial h_s/partial theta`. Direct supervision gives a self-position contribution; indirect transfer depends on cross-kernel alignment.

**Key variables:** decision state `h_T`; other-position state `h_s`; Jacobians `J_T,J_s`; cross-position kernel `K_{T,s}`; direct loss `L_direct`; indirect losses `L_indirect`; readout margin `M_Z`; native horizon-3 accuracy; guarded recovery `Q`.

**Causal relation:** If indirect transfer explains non-direct recovery, then positions with positive `-K_{T,s} grad_{h_s} ell_s` projection onto `grad_{h_T}M_Z` should predict increases in probe-readable `Z` or branch separation. If the projection is near zero, non-direct conditions should not improve `M_Z`.

**Observable metric:** Primary metric is finite-difference or gradient-estimated contribution of each position group to `Delta M_Z` and `Delta E_Z`. Secondary metrics are native H3 accuracy and `Q(t)`.

**Alternative explanations:** probe false positives, initialization leakage, local code leakage, decoder/evaluator artifacts, or generic regularization.

**Decision rule:** Support if the indirect transfer profile identifies positive cross-position contributions in non-direct conditions and separates them from direct native `h_T -> S_Z` learning.

## 1. Decision Question

In all-position training, when K does not cover the informative horizon at the decision prefix, can other positions still update the current state `h_T` toward branch-readable `Z`; and can we predict this using cross-position gradient transfer?

## 2. Definitions

All-position objective:

$$
L_K^{all}=\sum_t\sum_{j=1}^K\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j}).
$$

Decompose:

$$
L_K^{all}=L_{direct}+L_{indirect}+L_{shared}.
$$

Here:

- `L_direct` is the decision-prefix informative term `h_T -> S_Z`;
- `L_indirect` contains other positions whose losses can update shared parameters and affect `h_T`;
- `L_shared` contains branch-shared local targets.

Jacobians:

$$
J_T=\frac{\partial h_T}{\partial\theta},\qquad J_s=\frac{\partial h_s}{\partial\theta}.
$$

Cross-position kernel:

$$
K_{T,s}=J_TJ_s^\top.
$$

One loss at position `s` changes `h_T` by:

$$
\dot h_T^{(s)}=-J_TJ_s^\top\nabla_{h_s}\ell_s.
$$

Its contribution to margin is:

$$
\Delta_s M_Z\propto \langle \nabla_{h_T}M_Z,-K_{T,s}\nabla_{h_s}\ell_s\rangle.
$$

## 3. Physical Priors

**P1: Direct self-kernel prior.** The direct term uses `J_TJ_T^T` and should have the most local credit-assignment path.

**P2: Indirect cross-kernel prior.** Non-direct recovery depends on whether other positions have positive cross-kernel alignment with `h_T` semantic margin.

**P3: Probe/native split prior.** Indirect transfer may make `Z` probe-readable without training the native horizon-3 head to predict `S_Z` from `h_T`.

**P4: Position-source prior.** Not all positions contribute equally; the positions around `S_Z` or after branch-revealing tokens may dominate transfer.

## 4. Hypotheses

**H1: Direct self-kernel gives stronger native readout.**

Conditions with `L_direct` should have larger native H3 accuracy and `M_Z` than indirect-only controls.

**H2: Indirect transfer has measurable positive cross-position contributions.**

For K1/K2 or masked K3, nonzero `Q` recovery should correlate with positive cross-position contribution estimates.

**H3: Probe-readable and native-direct recovery are separable.**

It is possible to have high `Q` but low native H3 / `M_Z`, indicating indirect or evaluator-readable recovery rather than direct `h_T -> S_Z` learning.

## 5. Minimal Tests

| Test | Comparison | Primary metric | Support | Weaken |
|---|---|---|---|---|
| direct contribution | direct condition vs masked | self-term contribution to `Delta M_Z` | direct larger | masked matches direct native margin |
| position-source audit | group losses by position | contribution to `Delta M_Z` | specific positions dominate | no interpretable source |
| finite-difference mask | mask groups of positions | change in `Q`, native H3, `M_Z` | predicted drops | no effect |
| native/probe split | compare `Q` vs native H3 | scatter / tables | high-Q low-native cases appear | all Q is native |
| local guard | all conditions | local CE / accuracy | no degradation | tradeoff |

## 6. Computational Realization

Use clean `tau=3` all-position data from A11_07.

Conditions:

```text
K1_fixed_3head
K2_active
K3_full
K3_mask_decision_prefix_L3
K2_plus_decision_prefix_L3
```

At selected checkpoints, compute loss gradients by position group:

```text
decision_prefix_direct
positions_before_decision
positions_after_decision_before_Sz
positions_at_or_after_Sz
shared_filler_positions
```

For each group, estimate one-step changes:

```text
Delta M_Z
Delta E_Z
Delta Q proxy
Delta native H3
Delta local CE
```

If exact Jacobian kernels are too expensive, use finite-difference group updates:

1. clone checkpoint;
2. update using only one position group loss;
3. measure `Delta M_Z`, `Delta E_Z`, native H3, and local guard;
4. restore checkpoint.

## 7. Claim Boundary

Can claim if supported:

```text
All-position non-direct recovery can be explained as cross-position shared-parameter transfer. Direct decision-prefix supervision remains the only tested path that reliably produces native h_T -> S_Z readout and large readout-effective margin.
```

Cannot claim:

```text
Indirect recovery is useless.
Direct supervision is the only possible recovery path.
Natural-language transfer follows.
```

## 8. Next Decision

If 11_09 succeeds, A11 can state a sharper full training story: direct MTP gives local semantic margin; all-position NTP/non-covering K can recover through cross-position kernels, but this recovery need not train native informative-horizon prediction. If it fails, the current all-position interpretation remains empirical rather than mechanistic.
