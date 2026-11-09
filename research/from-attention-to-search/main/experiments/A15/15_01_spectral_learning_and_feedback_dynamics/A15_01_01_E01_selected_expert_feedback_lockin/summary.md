---
experiment_id: A15_01_01_E01_selected_expert_feedback_lockin
verdict: pass_feedback_lockin
completed: 2026-07-31
canonical_language: en
---

# Result: Selected-Expert Feedback Locks In The Head-First Partition

## Direct Result

**Pass.** When H/M/T all determined the loss-optimal expert, selected-only
expert co-training left M/T fine correction at chance, whereas equal-compute
oracle-functional expert coverage recovered nearly all readable M/T structure.

Fine correction accuracy \(C_{MT}\) asks, after the head bit is routed correctly,
whether the middle and tail bits also choose the correct fine expert. Its unit
is accuracy in \([0,1]\); it is not a language-model loss or real-workload gain.

| Outcome at step 6,000 | Selected-only | Oracle coverage | Paired difference |
| --- | ---: | ---: | ---: |
| \(C_{MT}\), seed median | 0.500 | 0.977 | +0.477 |
| M-bit correction difference | — | — | +0.478 |
| T-bit correction difference | — | — | +0.477 |
| Exact eight-expert route | 0.244 | 0.933 | +0.689 |

The paired-seed bootstrap 95% interval for \(\Delta C_{MT}\) is
\([0.476,0.479]\), well above the registered 0.10 practical threshold.

## Why This Separates The Mechanism

The two primary arms saw identical Router inputs, initial head margin, online
batches, route random numbers, optimizer, two expert forwards per token, and
one expert update per token. Only the update recipient changed: the sampled
expert in `selected_only`, or the loss-optimal expert in `oracle_coverage`.

In all 32 selected-only seeds, the early correct challenger received only
0.030--0.049 of eligible updates, below the registered 0.25 no-starvation
reference, while the incumbent MSE was lower than the correct challenger MSE
by a median 0.195. This is the registered incumbent-advantage/starvation
direction.

## Central Figure

![Oracle coverage restores middle/tail correction](figures/feedback_correction.png)

The left panel shows that selected-only routing remains at random fine
selection despite long training, while oracle coverage reaches the task's
noise-limited ceiling. The right panel shows every paired seed above both zero
and the 0.10 practical threshold. Bootstrap bands are narrow and overlap the
median curves visually.

## Operational Validity

- 32/32 formal paired seeds completed on one 8×5090 SPOT node.
- 32/32 finite-number, compute-match, initial-head, oracle-uniqueness,
  supervised-readability, and mature-expert bandit guards passed.
- The supervised and mature-expert controls reached about 0.933 exact route
  accuracy, matching the analytic Bayes ceiling \(\Phi(2)^3\approx0.933\).
- Remote job `pt-15rmvipu` succeeded; rank allocation was 8×4 paired seeds.

## Knowledge Update And Boundary

The result establishes a sufficiency claim:

> In a controlled MoE where lower-variance variables are genuinely useful,
> selected-expert co-adaptation can preserve an early head-only partition by
> making incumbents better and starving the fine experts that would reveal the
> correction signal.

It does not establish that natural DCLM middle/tail bands are useful, that this
mechanism caused an existing checkpoint, or that oracle coverage is deployable.
The next decision is whether a four-layer controlled hierarchy with known
layer-specific variables reproduces this effect under a sparse challenger or
counterfactual-coverage mechanism.
