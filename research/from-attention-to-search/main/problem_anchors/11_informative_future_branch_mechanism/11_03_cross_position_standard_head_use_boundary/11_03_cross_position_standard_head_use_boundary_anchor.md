# Cross-Position Standard-Head Use Boundary Anchor

Status: model-local K/V causal-use and source-information audits completed; exact K/V is generically readable, while neither MTP-specific readability nor a strong-use increment is established.


## 1. Problem Definition

### Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| current-state formation | task direction exists at \(h_T\) | positive local usefulness or readable margin | prerequisite | later use |
| cross-position transport | task direction survives the transition to \(h_{T+1}\) | cross-position kernel \(J_{T+1}J_T^T\) | standard head predicts from the later state | general causal use |
| standard-head use | the ordinary next-token head benefits at the answer position | H1 margin or held-out behavior at \(h_{T+1}\) | shared outcome for NTP/MTP | real-task transfer |

**Single decision question:** Is positive current-state semantic formation sufficient to improve the standard next-token head at the answer position?

## 2. Physical Priors

1. Probe readability is not use.
2. Changing the head and changing the state position are different interventions.
3. A local positive direction can be lost or reversed by the next-token transition.

## 3. Falsifiable Hypotheses

The sufficiency hypothesis predicts positive usefulness under the standard head at both \(h_T\) and \(h_{T+1}\) and a stable behavioral MTP advantage. The position-bottleneck rival predicts positive usefulness at \(h_T\) but nonpositive usefulness at \(h_{T+1}\).

## 4. Mathematical Model

For output head \(a\) and state position \(p\), define local usefulness

\[
U_{a,p}=v_a^T J_pJ_T^T d_2,
\]

where \(d_2\) is the extra future-loss descent direction. Same-position self-kernels and cross-position kernels need not have the same sign.

## 5. Computational Realization

Hold the trained trajectory, diagnostic batch, and extra-loss gradient fixed. Cross output-head identity with state position, then test a small set of intervening tokens and finally evaluate standard-head held-out behavior.

## 6. Minimal Falsification Tests

1. Compare H1 and H2 usefulness at \(h_T\) and \(h_{T+1}\).
2. Vary only the intervening token to test whether transport is transition-conditioned.
3. Require any favorable local interaction to produce a stable held-out standard-head gain.

## 7. Current Evidence

At \(h_T\), both heads have positive usefulness in 5/5 seeds; at \(h_{T+1}\), both are negative in 5/5. This identifies position rather than head identity as the immediate bottleneck. Intervening tokens change the local geometry, but the favorable local interaction does not yield a stable held-out behavioral advantage. See [cross-position audit](../../../experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E01_head_position_cross_kernel/summary.md), [end-to-end audit](../../../experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E02_end_to_end_use_boundary/summary.md), and [subanchor 11_03_01](subanchors/11_03_01_cross_position_proxy_falsification_anchor.md).

The completed [subanchor 11_03_02](subanchors/11_03_02_standard_head_causal_use_anchor.md) directly patched model-local K/V against matched shared-aux. All guards passed, but \(\bar\Gamma_{info}=0.01675\) and 0/5 seeds reached `0.10`, so the strong behavioral increment failed; positive margin movement in 4/5 seeds remains only candidate weak influence.

The follow-up [exact source-K/V audit](../../../experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md) found perfect held-out branch readability under NTP, shared-aux, and informative-MTP in every seed. It therefore rules out absolute linear source emptiness, but not generic-path formation. The registered informative-MTP readability increment was nonpositive in 4/5 seeds, and the formal verdict was insufficient because the label-shuffle guard failed. A 5/5 Fisher nuisance-compaction pattern is secondary geometric evidence only.

## 8. Claim Boundary And Next Decision

Supported claim: formation at \(h_T\) does not guarantee usefulness at \(h_{T+1}\); cross-position transport is an additional necessary condition. Local transport geometry alone is not sufficient for behavioral superiority.

Not supported: a universal adverse-transition law, a universal bridge-token explanation, MTP-specific extra branch readability, total ordinary-head non-use, or MTP downstream efficiency.

**Exactly one next decision:** validate a `relay-required` carrier with no
direct answer bypass and a non-saturated shared-aux baseline. No layer, Q,
K-only, V-only, or shared-unembedding sweep is authorized before that gate.
