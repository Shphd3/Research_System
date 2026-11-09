# A06_03_03_E01 Bounded-Challenger Router: Summary

## What We Established

A label-free, two-expert challenger is sufficient to escape the learned
specialist blind basin under the full LM loss. With the useful expert initially
at rank 2, full-loss pair routing corrects `128/128` cells. At rank 4 it corrects
`125/128` (`97.6563%`). Task-only pair routing corrects `128/128` at both ranks.
Selected-only top-1 remains `0/128` under full loss at both ranks.

The decisive update is that **bounded candidate utility coverage is sufficient
for identity discovery in this controlled system; oracle semantic-position
credit is not necessary for eventual correction**. Task credit remains useful
for efficiency: at rank 4, median correction time drops from `192.5` updates
under full-pair to `118.5` under task-pair, and median normalized regret drops
from `0.6810` to `0.4582`.

## Method

The Router evaluates the current top-1 expert and one challenger. For every
selected expert, a seed-random schedule cycles uniformly through the other
three expert IDs. It uses no task label, target token, or useful-expert identity.
Candidate probabilities are renormalized within the pair; evaluation reads the
ordinary top-1 route, so success requires a real identity crossing.

## Primary Results

| Useful rank | Full top-1 | Task top-1 | Full pair | Task pair | Task soft |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 0.0% | 32.8125% | 100.0% | 100.0% | 100.0% |
| 4 | 0.0% | 0.0% | 97.6563% | 100.0% | 100.0% |

The generalist rank-4 task-pair control forms an arbitrary target identity in
`0/128` cells. Thus pair correction depends on learned expert utility rather
than the challenger schedule mechanically imposing task IDs.

![Factorial correction rates](figures/factorial_correction_rates.png)

This figure asks whether credit source, utility coverage, or their interaction
is necessary for sustained top-1 correction. Pair coverage is the dominant
factor. The task-pair versus full-pair correction-rate interaction at rank 4 is
only `0.0234`, with 95% confidence interval `[0, 0.0547]`; the interval does not
support a necessary positive interaction.

![Rank-4 discovery trajectory](figures/rank4_discovery_trajectory.png)

This figure shows median useful-expert probability from rank 4. Full-pair and
task-pair both grow while top-1 branches remain flat. Task weighting accelerates
growth, and all-expert soft remains fastest. The figure does not prove that the
same challenger dose is compute-optimal.

## Hypothesis Update

- Joint semantic credit plus pair coverage is sufficient, but joint necessity
  is not supported.
- Credit-only is rejected: task-top1 remains `0/128` at rank 4.
- Coverage-only is supported: full-pair exceeds 90% at both ranks.
- Two-expert insufficiency is rejected at the current horizon and utility scale.

## Claim Boundary And Next Decision

The result establishes a controlled Router primitive: periodically evaluating
one unselected expert can reveal enough counterfactual utility to correct a
wrong route with two activated experts. It does not establish pretrained-LLM
specialization, natural semantic experts, end-to-end compute savings, or an
optimal exploration schedule.

The next anchor must minimize exploration duty cycle: how infrequently can the
Router audition a challenger while preserving rank-4 correction and low regret?
MTP-derived semantic credit is now an optional accelerator to prioritize
auditions, not a prerequisite for identity discovery.
