# Cross-Position Proxy Falsification

## 0. Thinking Card

**Phenomenon:** The branch variable is useful at the decision state but not at the later state used by the ordinary next-token head.
**Mechanism guess:** the intervening state transition rotates or suppresses the useful direction.
**Key variables:** state position, output-head identity, intervening token, held-out standard-head behavior.
**Causal relation:** hold the extra-loss direction fixed, vary head and position, then require any local gain to survive a behavioral test.
**Observable metric:** position-by-head usefulness followed by held-out standard-head gain.
**Rival explanations:** wrong auxiliary head; one special bridge token; insufficient training duration.
**Decision:** close these proxy variants because none establishes stable use.

## 1. Problem Definition

**Parent problem:** [11_03 cross-position standard-head use boundary](../11_03_cross_position_standard_head_use_boundary_anchor.md).
**Decision question:** Is positive current-state usefulness sufficient for later standard-head behavior?
**Not in scope:** structured composition or natural-language transfer.

**Usefulness** here means that the extra MTP descent direction locally improves the ordinary answer margin at the state actually consumed by the standard head. It is stronger than probe readability but still weaker than causal task benefit.

## 2. Physical Priors

**P1:** Head identity and state position are independent possible bottlenecks.
**P2:** Favorable local geometry must survive a held-out behavioral test before it supports a use claim.

## 3. Falsifiable Hypotheses

The sufficiency claim predicts positive usefulness at both $h_T$ and $h_{T+1}$. The position-bottleneck rival predicts a sign loss after the transition.

## 4. Mathematical Model

$$
U_{a,p}=v_a^T J_pJ_T^T d_2.
$$

Changing $a$ tests the head; changing $p$ tests the state transition. Stable behavioral gain is the guard against a proxy-only result.

## 5. Computational Realization

Cross two head identities with two state positions, vary only the bridge token in a bounded follow-up, and evaluate the common standard head on held-out data.

## 6. Minimal Falsification Tests

1. Compare usefulness by head and position.
2. Require any favorable bridge condition to improve held-out standard-head behavior.

## 7. Current Evidence

The [head-position audit](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E01_head_position_cross_kernel/summary.md) finds positive usefulness at $h_T$ and negative usefulness at $h_{T+1}$ in 5/5 seeds for both heads. The [end-to-end audit](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E02_end_to_end_use_boundary/summary.md) finds no stable held-out advantage.

## 8. Claim Boundary And Next Decision

**Can claim:** formation at one state is not sufficient for later standard-head use.
**Cannot claim:** a universal adverse transition law or a successful repair.
**Next decision:** move the use question to A12, where the task itself requires an intermediate state; do not add more proxy bridge variants here.
