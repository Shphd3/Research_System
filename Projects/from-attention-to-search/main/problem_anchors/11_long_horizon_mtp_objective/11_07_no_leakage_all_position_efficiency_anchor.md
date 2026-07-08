# 11_07 No-Leakage All-Position Efficiency Anchor

Status: proposed follow-up anchor after 11_06.  
Parent line: `11_long_horizon_mtp_objective`.  
Prior anchor: `11_06_readout_effective_margin_efficiency_anchor.md`.

## 0. Thinking Card

**Phenomenon:** A11_05 shows that full K=3 and K2 plus decision-prefix horizon-3 supervision are strongest in clean all-position `tau=3` training. However, random initialization can saturate `Q(0)`, and K=1/K=2 can recover `Z` indirectly through all-position shared-parameter training.

**Mechanism guess:** If the 11_06 readout-effective margin mechanism is real, then after controlling initialization leakage and preventing indirect transfer from saturating the metric, conditions with direct decision-prefix horizon-3 supervision should still reach high guarded recovery earlier or with higher early AUC.

**Key variables:** branch variable `Z`; decision prefix state `h_T`; direct horizon-3 loss; all-position indirect losses; branch-collapsed initialization; step-0 leakage score; guarded recovery `Q`; `T_0.9`; early AUC; local `Y_1/Y_2` guard; readout-effective margin `M_Z`.

**Causal relation:** Direct `h_T -> S_Z` supervision should produce earlier multi-step semantic recovery when the metric is not saturated at initialization and non-covering all-position transfer is not already sufficient.

**Observable metric:** Primary metric is `T_0.9` with a required `Q(0)` guard. Secondary metrics are early AUC, `M_Z(t)`, `E_Z(t)`, local target loss, and native informative-horizon accuracy.

**Rival explanations:** recovery may come from random branch leakage, all-position indirect losses, generic auxiliary regularization, larger loss scale, or local-target degradation.

**Decision rule:** Support if direct horizon-3 conditions improve `T_0.9` or early AUC over indirect-only controls under `Q(0)` near chance and intact local targets. Weaken if indirect-only controls match direct conditions after leakage control.

## 1. Problem Definition

This anchor tests whether the one-step margin mechanism from 11_06 survives in a more language-model-like all-position setting.

The question is not whether K=3 can recover `Z` at all. A11_05 already supports that. The sharper question is:

```text
After controlling initialization leakage, does direct decision-prefix horizon-3 supervision still improve multi-step semantic recovery efficiency beyond all-position indirect transfer?
```

## 2. Terminology / Definitions

| Term | Plain meaning | Concrete object | Formula / unit | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| leakage guard | whether `Z` is already recoverable at step 0 | `Q(0)`, probe at step 0, branch-swap at step 0 | score | validates speed metric | all shortcut absence |
| direct condition | includes decision-prefix `h_T -> S_Z` loss | K3 full or K2 plus decision-prefix L3 | CE | tests direct supervision | only recovery path |
| indirect-only condition | all-position training excluding direct decision-prefix L3 | K3 masked direct term | CE | measures shared-parameter transfer | all indirect mechanisms |
| recovery efficiency | faster or more stable `Z` recovery | `T_0.9`, early AUC | steps / score | multi-step efficiency | first-order cause |
| margin trajectory | readout-effective geometry during training | `M_Z(t)` | scalar | links to 11_06 theorem | final performance |

## 3. Physical Priors

**P1: No-leakage prior.** If `Q(0)` is high, speed metrics are invalid. The experiment must use branch-collapsed or otherwise audited initialization.

**P2: Indirect-transfer prior.** K=1/K=2 can recover `Z` in all-position training. The question is whether direct supervision makes recovery faster or more stable, not whether non-covering horizons are impossible.

**P3: Margin-to-curve prior.** If 11_06 is the correct mechanism, early `M_Z(t)` should move before or along with `Q(t)`.

**P4: Local-guard prior.** Faster `Z` recovery is not a clean efficiency win if it worsens shared targets `A` and `C`.

## 4. Falsifiable Hypotheses

**H1: Direct all-position efficiency.**

Direct horizon-3 conditions have smaller `T_0.9` or higher early AUC than indirect-only controls under leakage guard.

**H2: Margin predicts recovery.**

Early `M_Z(t)` separates direct conditions before or together with `Q(t)`.

**H3: Indirect transfer remains but is weaker.**

Masked K3 and K1/K2 may recover, but should be slower or lower-AUC than direct conditions.

**H4: Local target preservation.**

Direct conditions preserve `Y_1/Y_2` accuracy and CE within tolerance.

## 5. Mathematical Model

Clean `tau=3` data:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

All-position loss:

$$
L_K^{all}=\sum_t\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j}).
$$

Direct decision-prefix term:

$$
L_{direct}=\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z).
$$

Masked K3 removes `L_direct` but keeps other all-position K=3 losses.

K2 plus direct adds `L_direct` to K=2 all-position training.

Readout-effective margin:

$$
M_Z(t)=\frac1m\sum_z(u_{S_z}^{(3)}-\bar u)^\top h_T(z,t).
$$

## 6. Computational Realization

Run only after 11_06 passes or is at least interpretable.

Core conditions:

```text
K1_fixed_3head_all_position
K2_active_all_position
K3_full_all_position
K3_mask_decision_prefix_L3
K2_plus_decision_prefix_L3
```

Required initialization:

```text
identical_branch / branch-collapsed initialization as primary
random initialization only as boundary diagnostic
```

Required leakage gate:

```text
Q(0) <= 0.35 for 4 branches
M_Z(0) near 0
E_Z(0) near 0
native informative accuracy near chance
```

If the leakage gate fails, do not interpret `T_0.9`.

## 7. Minimal Tests

| Test | Comparison | Primary metric | Support | Weaken |
|---|---|---|---|---|
| Leakage gate | step 0 all conditions | `Q(0)`, `M_Z(0)`, `E_Z(0)` | near chance / near zero | saturation |
| Direct vs indirect | K3 full vs K3 masked | `T_0.9`, early AUC | masking delays / lowers | masking no effect |
| Direct sufficiency | K2 vs K2 plus direct L3 | `T_0.9`, early AUC | direct improves K2 | no improvement |
| Full comparison | K1/K2/K3 full | `Q(t)`, `M_Z(t)` | K3 strongest | K1/K2 match without direct term |
| Local guard | all conditions | `Y1/Y2` CE and accuracy | preserved | local degradation |

## 8. Claim Boundary

Can claim if supported:

```text
Under no-leakage clean tau=3 all-position training, direct decision-prefix informative-horizon supervision improves semantic recovery efficiency beyond indirect transfer, as measured by T_0.9 or early AUC, while preserving local targets.
```

Cannot claim:

```text
NTP cannot learn Z.
Direct supervision is the only all-position recovery path.
This proves natural-language or MoE routing value.
```

## 9. Next Decision

If 11_07 passes, then the line can consider a route-relevance bridge anchor that asks whether MTP-induced `Z` margins improve routing margin or preservation. If 11_07 fails, keep A11 as a direct-representation and one-step-efficiency mechanism line only.
