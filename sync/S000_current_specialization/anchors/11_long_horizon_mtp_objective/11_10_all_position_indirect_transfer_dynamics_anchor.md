# 11_10 All-Position Indirect-Transfer Dynamics Anchor

Status: supported by A11_10 full run on 2026-07-09.  
Parent line: `11_long_horizon_mtp_objective`.  
Purpose: test whether all-position non-direct recovery is better explained by indirect shared-parameter transfer than by native decision-prefix supervision.

## 0. Thinking Card

**Phenomenon:** A11_07 showed that all-position K1/K2 or masked K3 can make the early variable `Z` recoverable by a guarded evaluator even when native horizon-3 prediction and readout-effective margin stay near zero.

**Mechanism guess:** A loss at another sequence position can update the current decision state `h_T` through shared parameters. The local first-order object is the cross-position parameter kernel `K_{T,s}=J_TJ_s^T`. Direct supervision uses the self-position path at `h_T`; indirect transfer uses other positions and can make `Z` probe-readable without training native `h_T -> S_Z` prediction.

**Key variables:** current state `h_T`; other-position state `h_s`; Jacobians `J_T,J_s`; cross-position kernel `K_{T,s}`; direct decision-prefix horizon-3 loss; indirect all-position losses; readout margin `M_Z`; native horizon-3 accuracy; guarded recovery `Q`.

**Causal relation:** If indirect transfer explains non-direct recovery, then removing only the direct decision-prefix horizon-3 loss should preserve some guarded recovery but remove native horizon-3 prediction and `M_Z`. Adding only that direct loss to K2 should recover native prediction and large `M_Z`.

**Observable metric:** Primary metric is native/direct separation: native horizon-3 accuracy and fixed readout-effective margin `M_Z_ref` versus guarded recovery `Q`. Secondary metrics are one-step hidden semantic velocity, early AUC of `Q` and `M_Z_ref`, local Y1/Y2 guards, and gradient-profile attribution.

**Alternative explanations:** Probe false positives, initialization leakage, local target damage, or generic extra-loss scale. The protocol therefore uses no-leakage initialization, the same clean `tau=3` data, local guards, and direct-add / direct-mask controls.

**Decision rule:** Support if direct conditions have high native H3 and large `M_Z_ref`, while indirect-only conditions can have nontrivial `Q` but remain low on native H3 and `M_Z_ref`.

## 1. Decision Question

In all-position training, can non-direct K1/K2/masked-K3 recovery be separated from direct native `h_T -> S_Z` learning; and does the direct decision-prefix horizon-3 term explain the readout-effective semantic margin?

## 2. Definitions

All-position objective:

$$
L_K^{all}=\sum_t\sum_{j=1}^K\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j}).
$$

Direct decision-prefix term:

$$
L_{direct}=\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z).
$$

Indirect transfer term:

$$
L_{indirect}=L_K^{all}-L_{direct}-L_{shared\ local}.
$$

Cross-position parameter kernel:

$$
J_T=\frac{\partial h_T}{\partial\theta},\qquad
J_s=\frac{\partial h_s}{\partial\theta},\qquad
K_{T,s}=J_TJ_s^\top.
$$

Contribution of loss at position `s` to the decision state:

$$
\dot h_T^{(s)}=-J_TJ_s^\top\nabla_{h_s}\ell_s.
$$

Its contribution to readout margin:

$$
\Delta_s M_Z\propto
\langle \nabla_{h_T}M_Z,\;-K_{T,s}\nabla_{h_s}\ell_s\rangle.
$$

Guarded recovery:

$$
Q=\min\{A_{decoder},A_{probe},C_{swap}\}.
$$

## 3. Physical Priors

**P1: Direct self-path prior.** The direct `h_T -> S_Z` term should be the strongest path for native horizon-3 prediction and readout-effective semantic margin.

**P2: Indirect transfer prior.** Other all-position losses can make `Z` recoverable from `h_T` through shared-parameter updates, but this need not train native H3 prediction.

**P3: Native/probe split prior.** High `Q` alone is not direct-supervision evidence; native H3 and `M_Z_ref` are required to identify the direct path.

**P4: Local guard prior.** A semantic recovery gain is not accepted if it is explained by damaging shared local targets.

## 4. Experimental Realization

Use the clean `tau=3` all-position data:

```text
BR_z F00 ... F15 U00 U01 U02 U03 A_SHARED C_SHARED S_z STOP
```

Core four-run condition set:

| Condition | Active loss | Role |
|---|---|---|
| `K2_active` | all-position horizons 1 and 2 | non-covering MTP control |
| `K3_active` | all-position horizons 1, 2, and 3 | full direct + indirect condition |
| `K3_mask_decision_prefix_L3` | K3, but remove only direct `h_T -> S_Z` | indirect-only K3 control |
| `K2_plus_decision_prefix_L3` | K2 plus direct `h_T -> S_Z` | direct-term sufficiency test |

No-leakage initialization:

```text
init_mode: identical_branch
```

Seeds:

```text
971, 972, 973, 974, 975
```

## 5. Minimal Tests

| Test | Primary metric | Support | Weaken |
|---|---|---|---|
| Direct sufficiency | `K2_plus_decision_prefix_L3` minus `K2_active` on native H3 and `M_Z_ref` | large positive gap | direct-add does not improve native H3 / margin |
| Direct necessity | `K3_active` minus `K3_mask_decision_prefix_L3` | removing direct term removes native H3 / margin | masked K3 matches direct native readout |
| Indirect recovery | non-direct `Q` versus native H3 / `M_Z_ref` | non-direct can have `Q>chance` but low native H3 / margin | `Q` and native H3 indistinguishable |
| Local guard | Y1/Y2 accuracy and CE | local targets preserved | semantic gain trades off local targets |
| Gradient profile | horizon/parameter-group gradients | H3 direct gradients align with margin gap | no interpretable separation |

## 6. Current Evidence

A11_10 full run:

```text
run name: a11_10_all_position_indirect_transfer_full_20260709_164227
shards: 4 completed
conditions: K2_active, K3_active, K3_mask_decision_prefix_L3, K2_plus_decision_prefix_L3
seeds: 971, 972, 973, 974, 975
verdict: support
```

Main result:

| Condition | Reach rate | Early AUC Q | Final Q | Native H3 | Final `M_Z_ref` | Final `E_Z` |
|---|---:|---:|---:|---:|---:|---:|
| `K2_active` | 0.60 | 0.773 | 0.75 | 0.00 | 0.000 | 0.005 |
| `K3_mask_decision_prefix_L3` | 0.60 | 0.773 | 0.70 | 0.00 | 0.004 | 0.010 |
| `K3_active` | 1.00 | 0.965 | 1.00 | 1.00 | 2.430 | 50.915 |
| `K2_plus_decision_prefix_L3` | 1.00 | 0.965 | 1.00 | 1.00 | 3.766 | 83.262 |

Decision evidence:

```text
direct sufficiency: supported
direct necessity for native/margin in K3: supported
non-direct Q recovery: supported
Q-alone-as-direct-evidence: rejected
local Y1/Y2 guard: pass
```

Source records:

```text
Projects/from-attention-to-search/main/experiments/A11/A11_10_all_position_indirect_transfer_dynamics/protocol.md
Projects/from-attention-to-search/main/experiments/A11/A11_10_all_position_indirect_transfer_dynamics/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_10_all_position_indirect_transfer_dynamics/detailed.md
```

## 7. Claim Boundary

Can claim if supported:

```text
In the controlled clean all-position tau=3 setting, non-direct objectives can make Z probe-readable, but direct decision-prefix horizon-3 supervision is the tested path that reliably creates native h_T -> S_Z prediction and large readout-effective semantic margin.
```

Cannot claim:

```text
Indirect recovery is useless.
Direct supervision is the only possible way to learn Z.
The same separation holds automatically in natural language.
MoE routing utility follows from this result.
```

## 8. Next Decision

A11_10 supports the split. A11 should now state the all-position boundary as:

```text
MTP's controlled advantage is a direct local semantic velocity term; all-position training also has indirect shared-parameter transfer, so recovery metrics must separate native readout from probe-readable recovery.
```

The next anchor should be theory closure: under which optimization assumptions does positive first-order semantic velocity imply a smaller finite-step semantic-margin hitting time?
