---
experiment_id: A15_06_E06_2b_10b_router_expert_specialization_audit
result_status: complete
eligibility: eligible_single_seed_frozen_audit
typed_verdict: mixed_not_supportive
updated: 2026-08-10
---

# Summary: A15_06_E06 Router--Expert Specialization And Utilization Audit

Primary Anchor: [A15_06_02 Router--Expert Specialization](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/subanchors/15_06_02_router_expert_specialization_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result eligibility: **eligible for a frozen, seed-17, 2B--10B mechanism claim**.

## Result Snapshot

**Verdict: `mixed_not_supportive`.** The experts are already functionally
non-interchangeable and the Router uses part of that token-conditional
variation, but covariance-ranked H/M/T routing does not use it better than its
dimension-matched random control.

At 10B, Local-HMT minus Local-Random expert-choice regret was
\(-0.01042\) nat/token, but its paired 95% interval \([-0.02878,0.00753]\)
crossed zero; its Router score--utility difference was essentially zero
(\(-0.00022\), interval \([-0.01313,0.01278]\)). Relay-HMT pointed in the
unfavorable direction on both metrics: regret \(+0.01352\) nat/token
(\([-0.00361,0.03052]\)) and score--utility correlation \(-0.01121\)
(\([-0.02745,0.00481]\)). Neither path passed its Holm-adjusted sign-flip tests.

What is established is more specific than “specialization failed.” Across the
five arms at 10B, mean same-input expert-output linear CKA was only
\(0.326\)--\(0.335\), forced-expert NLL standard deviation was
\(0.467\)--\(0.505\) nat/token, oracle-expert entropy was \(0.996\)--\(0.997\), and
the largest oracle share was only \(0.145\)--\(0.155\). Thus experts produce
different same-input transformations, those differences affect next-token
loss, and no single expert is globally best. The Router selects the
counterfactual oracle about \(34\%\) of the time and has a positive but modest
score--utility Spearman correlation (\(0.130\)--\(0.162\)): utilization is real
but incomplete.

**Knowledge update:** expert differentiation is not the missing prerequisite
in these models. The unresolved problem is learning a Router coordinate that
predicts token-specific expert utility; covariance rank by itself does not
provide that certificate.

## Decision-Bearing Setup

- **Question:** do Local-HMT or Relay-HMT form and exploit more useful expert
  specialization than matched random-subspace routers?
- **Treatments and controls:** Local-HMT versus Local-Random-Matched;
  Relay-HMT versus Relay-Random; Vanilla-Full as an unrestricted reference.
- **Checkpoints:** seed 17 at 2B, 5B, and 10B training tokens; 15 tasks total.
- **Primary metric:** expert-choice regret, the next-token NLL paid by the
  native Router relative to the best of eight one-token, one-layer forced
  expert counterfactuals; lower is better.
- **Second required metric:** within-token Spearman correlation between eight
  Router logits and negative forced-expert NLL; higher means Router scores rank
  experts more consistently with immediate utility.
- **Independent unit:** held-out document; 10B confirmation uses 128 documents
  and eight target positions.
- **Known limitation:** one seed and a frozen, local intervention cannot show
  that specialization caused terminal language-model quality.

## Verdict Basis

| Registered comparison | Regret difference, nat/token (95% CI) | Score--utility difference (95% CI) | Holm-adjusted \(p\) | Verdict |
| --- | ---: | ---: | --- | --- |
| Local-HMT minus Local-Random | \(-0.01042\) \([-0.02878,0.00753]\) | \(-0.00022\) \([-0.01313,0.01278]\) | \(0.268 / 0.975\) | not supported |
| Relay-HMT minus Relay-Random | \(+0.01352\) \([-0.00361,0.03052]\) | \(-0.01121\) \([-0.02745,0.00481]\) | \(0.240 / 0.352\) | not supported |

Source: [primary_comparisons.csv](tables/primary_comparisons.csv).

## Key Evidence

1. **Experts are not interchangeable.** Same-input CKA decreases from roughly
   \(0.38\)--\(0.42\) in layer 1 to \(0.24\)--\(0.32\) in layers 3--4, while forcing
   different experts changes next-token NLL substantially.
2. **The utility target is token conditional.** Oracle entropy is near one and
   the largest expert wins only about \(15\%\) of targets, close to the uniform
   \(12.5\%\) reference; swap cost is not caused by one global best expert.
3. **The Router only partly exploits specialization.** Best-match rate is about
   \(34\%\), above chance but far from one, and margin--regret correlation is
   mostly positive rather than the desired negative direction.
4. **HMT identity is not the missing ingredient.** Local-HMT and Local-Random
   are almost identical on Router score--utility alignment; Relay-HMT is
   descriptively worse than Relay-Random.
5. **Parameters retain a common backbone.** Rank-8 dominant input/output
   subspace overlap is \(0.14\)--\(0.23\), far above the matched Haar q95
   (\(0.0135\)), even while same-input outputs diverge. Parameter sharing and
   functional differentiation therefore coexist.

## Central Figures

![Decisive matched comparisons](figures/figure3_primary_matched_comparisons.png)

Figure 3 shows the registered 10B effects. A covariance-specific certificate
would require both bars for a path to lie entirely on their favorable sides of
zero; neither path does.

![Expert-specialization ladder](figures/figure2_specialization_ladder.png)

Figure 2 separates parameter geometry, same-input output geometry, functional
swap cost, and Router utilization. It shows why low CKA is not itself a Router
success criterion.

## Claim Boundary

**Can claim:** at the registered seed and scale, experts are functionally
non-interchangeable and token-conditionally useful, the Router exploits them
only partially, and covariance-ranked H/M/T identity does not beat matched
random routing on the registered frozen functional certificate.

**Cannot claim:** experts have no semantic specialization; random routing is
universally superior; CKA differences caused model quality; H/M/T can never be
useful; results reproduce across seeds or scales; LM and load-balancing
gradients conflict; or PCGrad would improve these models.

## Next Decision

Do not tune another covariance-band Router from this result. The next A15
decision remains whether A15_07 can identify a cross-expression,
conditional-fine direction that first passes a semantic certificate and then
predicts counterfactual expert utility beyond Router scores and matched random
directions. Completion requires a held-out functional admission result; the
resume action is to review the six pending A15_07 design choices.

