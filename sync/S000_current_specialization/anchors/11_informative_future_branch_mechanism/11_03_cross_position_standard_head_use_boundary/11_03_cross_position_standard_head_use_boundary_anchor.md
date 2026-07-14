# Cross-Position Standard-Head Use Boundary Anchor

Status: completed; the sufficiency claim is weakened and this diagnostic branch is closed.

## 0. Thinking Card

**Phenomenon:** MTP can create a task-useful direction at the current state without improving the standard answer one token later.

**Mechanism guess:** Use requires transport through the intervening token. The cross-position Jacobian can rotate a useful direction into an adverse one even when changing the output head does not.

**Observable metric:** standard-head usefulness before and after the state transition, followed by a conservative held-out behavioral score.

**Decision:** current-state formation is not sufficient for standard-head benefit; stop enumerating bridge tokens or training lengths on this proxy.

## 1. Problem Definition

### Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| current-state formation | task direction exists at $h_T$ | positive local usefulness or readable margin | prerequisite | later use |
| cross-position transport | task direction survives the transition to $h_{T+1}$ | cross-position kernel $J_{T+1}J_T^T$ | standard head predicts from the later state | general causal use |
| standard-head use | the ordinary next-token head benefits at the answer position | H1 margin or held-out behavior at $h_{T+1}$ | shared outcome for NTP/MTP | real-task transfer |

**Single decision question:** Is positive current-state semantic formation sufficient to improve the standard next-token head at the answer position?

## 2. Physical Priors

1. Probe readability is not use.
2. Changing the head and changing the state position are different interventions.
3. A local positive direction can be lost or reversed by the next-token transition.

## 3. Falsifiable Hypotheses

The sufficiency hypothesis predicts positive usefulness under the standard head at both $h_T$ and $h_{T+1}$ and a stable behavioral MTP advantage. The position-bottleneck rival predicts positive usefulness at $h_T$ but nonpositive usefulness at $h_{T+1}$.

## 4. Mathematical Model

For output head $a$ and state position $p$, define local usefulness

$$
U_{a,p}=v_a^T J_pJ_T^T d_2,
$$

where $d_2$ is the extra future-loss descent direction. Same-position self-kernels and cross-position kernels need not have the same sign.

## 5. Computational Realization

Hold the trained trajectory, diagnostic batch, and extra-loss gradient fixed. Cross output-head identity with state position, then test a small set of intervening tokens and finally evaluate standard-head held-out behavior.

## 6. Minimal Falsification Tests

1. Compare H1 and H2 usefulness at $h_T$ and $h_{T+1}$.
2. Vary only the intervening token to test whether transport is transition-conditioned.
3. Require any favorable local interaction to produce a stable held-out standard-head gain.

## 7. Current Evidence

At $h_T$, both heads have positive usefulness in 5/5 seeds; at $h_{T+1}$, both are negative in 5/5. This identifies position rather than head identity as the immediate bottleneck. Intervening tokens change the local geometry, but the favorable local interaction does not yield a stable held-out behavioral advantage. See [cross-position audit](../../../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E01_head_position_cross_kernel/summary.md), [end-to-end audit](../../../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E02_end_to_end_use_boundary/summary.md), and [subanchor 11_03_01](subanchors/11_03_01_cross_position_proxy_falsification_anchor.md).

## 8. Claim Boundary And Next Decision

Supported claim: formation at $h_T$ does not guarantee usefulness at $h_{T+1}$; cross-position transport is an additional necessary condition. Local transport geometry alone is not sufficient for behavioral superiority.

Not supported: a universal adverse-transition law, a universal bridge-token explanation, or MTP downstream efficiency.

**Exactly one next decision:** hand this boundary to
[A12](../../12_structured_compositional_mtp_workload/README.md). No additional
A11 bridge-token or training-length sweep is justified unless A12 contradicts
the controlled boundary.
