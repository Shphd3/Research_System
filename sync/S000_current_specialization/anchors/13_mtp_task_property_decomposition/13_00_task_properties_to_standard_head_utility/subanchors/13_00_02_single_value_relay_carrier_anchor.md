# Is Single-Value Relay a Valid Minimal Carrier?

Thinking Card source:
[long_horizon_compositional_workload_thinking_card_cn.md](/daily_research_reports/0717/mtp_long_horizon_compositional_workload/long_horizon_compositional_workload_thinking_card_cn.md)

Parent anchor:
[13_00 task properties to standard-head utility](../13_00_task_properties_to_standard_head_utility_anchor.md)

## 1. Problem Definition

**Single decision question:** can a two-layer NTP Transformer reliably copy one
early value through the only legal relay path, while ignoring matched nuisance
tokens?

`Single-value relay` means the answer is always value $A$. Value $B$ and the
selector token retain the same marginal distribution but do not affect the
answer. This removes query binding while retaining state formation, transport,
and standard-head use.

## 2. Physical Priors

1. Relay necessity should be tested before query-conditioned composition.
2. Two layers are necessary under the same graph: layer 1 moves $A$ into the
   relay, and layer 2 lets the answer consume it.
3. A valid standard-head path must follow an $A$ counterfactual, ignore $B$,
   and follow an in-distribution donor relay state.

## 3. Falsifiable Hypotheses

**H1:** two-layer relay and one-layer bypass both pass held-out capability;
one-layer relay stays at chance; $A$ swaps, $B$ swaps, and relay donor patches
pass their original gates.

**Strongest rival:** the model copies through an unintended direct edge, uses a
nuisance correlation, or cannot learn the relay even without query binding.

Pass, fail, and insufficient meanings use the same six-gate conjunction as
`13_00_01`.

## 4. Mathematical Model

Let $A,B\sim\operatorname{Unif}(\mathcal V)$ and
$Q\sim\operatorname{Bernoulli}(1/2)$ be independent. Define

$$
Y=A,
\qquad
Y\perp (B,Q)\mid A.
$$

Relay-required prediction is

$$
S_1=f_{\theta,1}(A,B,Q),
\qquad
\hat Y=g_{\theta,2}(S_1),
$$

with no direct evidence-to-answer edge. The intended minimal sufficient state
is $S^\star=A$; $B$ and $Q$ are negative-control nuisances.

## 5. Computational Realization

The token sequence and attention graph remain

```text
[BOS] [value-A] [value-B] [selector] [RELAY] [ANSWER] [value-A]
```

The learner returns to width 64, two layers, four heads, and the E03 cosine
schedule. The same 409/103 disjoint triple split is used.

## 6. Minimal Falsification Tests

Primary metric:

$$
C_{\mathrm{single\ relay}}=\bigwedge_{j=1}^{6}G_j.
$$

The original thresholds are retained. The selected counterfactual now changes
$A$; the unselected counterfactual changes $B$. Donor patches are matched on
the nuisance selector and differ only in answer label for the causal-follow
test.

The main falsifier is stable two-layer accuracy without donor-label follow, or
failure to exceed capability after query binding has been removed.

## 7. Current Evidence

E01 passed all six gates after query-conditioned selection was removed, but
revealed an auxiliary-boundary entropy mismatch. E02 removed that mismatch
without changing the answer rule. On E02, two-layer NTP relay mean accuracy
was 0.9846, one-layer relay stayed near chance at 0.0577, one-layer bypass
reached 1.0000, and all counterfactual and donor-patch gates passed.

Result reading path:
[A13_00_02_E02 summary](/Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_02_E02_entropy_matched_carrier/summary.md).

## 8. Claim Boundary And Next Decision

The pass establishes only a controlled single-state relay carrier. It does not
establish MTP benefit, query composition, long token distance, code transfer,
or MoE value.

**Exactly one next decision:** freeze E02 and compare NTP, matched shared-aux,
and informative Next-2 under relay-required versus bypass access.
