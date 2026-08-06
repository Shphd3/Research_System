# A06_04 Real-Workload Expert-Utility Headroom

Status: active parent anchor; the first registered subanchor is complete and
failed on its CrossCodeEval final-layer surface.

Thinking Card source: [06_04_real_workload_utility_headroom_thinking_card.md](06_04_real_workload_utility_headroom_thinking_card.md)

## 1. Problem Definition

**Decision question:** does an unfiltered repository-code workload contain
split-stable expert-function heterogeneity that the native Router fails to
capture?

### Terminology / Definitions

| Term | Plain meaning | Concrete computation | Decision role | Cannot prove |
|---|---|---|---|---|
| Workload stratum $z$ | A registered code condition used only for evaluation | language, API family, dependency type, or paired context condition | Organizes held-out comparisons | Correct expert label |
| Matched slot swap | Replace one active routed-expert slot while keeping active count and its gate weight fixed | final-layer candidate swap used by `06_04_01` | Measures one expert's counterfactual function at matched activated compute | A deployable routing policy |
| Expert headroom $H_e^c$ | Native loss minus loss after swapping candidate expert $e$ under condition $c$ | $H_e^c=L_{native}^c-L_e^{swap,c}$, in nats per target token | Tests whether native routing missed useful expert capacity | That a learned Router can find $e$ |
| Context-expert interaction $I_{ctx}$ | Relevant context changes the relative effect of two experts | held-out difference-in-differences between candidates and context conditions | Detects context-conditioned counterfactual effects | Positive useful headroom by itself |
| Split stability | The useful-expert identity repeats across calibration partitions and held-out data | registered rank-agreement guard | Rejects calibration-only expert mining | Causal semantics |
| Oracle routing headroom | Native loss minus a calibration-selected, held-out forced-expert oracle loss | $G_{oracle}=L_{native}-L_{oracle}$ | Parent-level workload gate | Learnable Router capture |

## 2. Physical Priors

1. A semantic Router has no functional target if experts are conditionally
   interchangeable or only differ by harmful outliers.
2. Human strata may organize evaluation but may not define the correct expert.
3. Expert selection and evaluation must use different repositories or splits.
4. Relevant context benefit is not expert specialization unless it changes
   expert utility and leaves positive headroom over native routing.
5. The primary sample must not be prefiltered by observed expert utility or
   multi-token-prediction semantic latency.

## 3. Falsifiable Hypotheses

**H1:** calibration-selected useful-expert identities repeat on held-out data
and yield positive oracle headroom.

**H2:** the headroom survives load-matched, token-identity, local-only, length,
frequency, and split-overfitting controls.

The first local clause, `06_04_01`, sharpened H1 to ask whether relevant
cross-file context changes final-layer expert utility while the in-file prefix
and target remain fixed. It required both a stable expert identity and positive
absolute headroom; a positive interaction alone was deliberately insufficient.

## 4. Mathematical Model

Choose an expert on calibration data only,

$$
a_l(z)=\arg\min_e L_{z,l,e}^{cf,cal},
$$

and evaluate on held-out data,

$$
G_{oracle,l}
=L_{native,l}
-\sum_z p(z)L_{z,l,a_l(z)}^{cf,test}.
$$

For the paired-context subanchor, candidate headroom is

$$
H_e^c=L_{native}^c-L_e^{swap,c},
$$

and the registered interaction for calibration-selected experts $(a,b)$ is

$$
I_{ctx}^{test}
=\left(H_a^{rel,test}-H_b^{rel,test}\right)
-\left(H_a^{nuis,test}-H_b^{nuis,test}\right).
$$

The joint hypothesis requires reproducible expert identity, positive
$I_{ctx}$, and positive $H_a^{rel}$; interaction caused by a bad expert becoming
more harmful does not count as missed positive utility.

## 5. Computational Realization

This parent is adjudicated through bounded subanchors rather than one broad
expert sweep. The completed first subanchor froze
`Qwen3-Coder-30B-A3B-Instruct` and evaluated 256 repository-disjoint
CrossCodeEval Python examples: 64 calibration-A, 64 calibration-B, and 128
untouched test examples. Relevant cross-file context, length-matched nuisance
context, and local-only context shared the same in-file prefix and target.

At zero-based final MoE layer `47`, the intervention kept seven of eight native
routed experts and replaced only the lowest-weight slot with each of 128
candidates while retaining that slot's gate weight. No parameters were
updated. CrossCodeEval is intentionally cross-file-dependent, so it tests one
registered real-code surface rather than the parent's full unfiltered-workload
scope.

## 6. Minimal Falsification Tests

The parent passes only if a registered real-code surface jointly shows:

1. native capability on the registered context or condition;
2. calibration-to-test stability of the selected useful expert;
3. a positive held-out expert-by-condition effect when that effect is part of
   the local clause;
4. positive absolute headroom over native routing with the registered practical
   threshold and confidence interval;
5. complete numerical, split, activated-compute, and nuisance-control guards.

A passed context interaction with failed expert stability or failed absolute
headroom rejects the joint clause. It must not be promoted to functional
specialization.

## 7. Current Evidence

[`06_04_01`](subanchors/06_04_01_context_conditioned_expert_utility_anchor.md)
is complete and **failed on its registered surface**; the result is
numerically valid rather than insufficient.

- Native relevant context beat equally long nuisance context by `0.20370`
  nats per target token, 95% CI `[0.05908, 0.35929]`.
- Calibration selected experts $a=49$ and $b=53$, but expert 49 ranked 8th on
  calibration-A and 16th on calibration-B, so split stability failed.
- Held-out interaction passed: $I_{ctx}=0.01163$, 95% CI
  `[0.00336, 0.02022]`.
- Relevant absolute headroom failed: $H_{49}^{rel}=0.00540$, 95% CI
  `[-0.00105, 0.01225]`, below the registered `0.01` threshold and without a
  positive confidence lower bound.
- Expert 49's context shift was only `+0.00082`; most interaction came from
  expert 53 becoming more harmful (`-0.01081`). Test REL/NUIS utility rankings
  were similar (Spearman `0.891`), while calibration context shifts were not
  reproducible (Spearman `0.083`).
- All 256 examples, all three conditions, all 128 candidates, and all numerical
  guards completed successfully.

Canonical result records:

- [summary.md](/Projects/from-attention-to-search/main/experiments/A06/06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/summary.md)
- [detailed.md](/Projects/from-attention-to-search/main/experiments/A06/06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/detailed.md)

## 8. Claim Boundary And Next Decision

**Supported now:** relevant evidence changes final-layer expert
counterfactual effects; the native model distinguishes relevant from
length-matched nuisance context; and the matched-slot methodology is complete
and numerically validated.

**Weakened or rejected now:** on the registered CrossCodeEval final-layer
surface, the frozen expert pool does not provide split-stable,
context-favored positive headroom that a better Router could simply recover.
Context-dependent bad-expert avoidance is not positive specialization.

**Not supported now:** a conclusion for all unfiltered repository code, stable
semantic experts, a learned Router, other layers or models, training-time
utility creation, long-context scaling, or systems-level speedup. External
routing-continuity and hardware-cost reports change the cost term, not this
functional verdict.

**Exactly one next decision:** approve or reject one training-time
selective-sharing test on an explicit real rare/common workload; do not keep
mining the same frozen last-layer expert pool or create a new Router before
that human decision is recorded.
