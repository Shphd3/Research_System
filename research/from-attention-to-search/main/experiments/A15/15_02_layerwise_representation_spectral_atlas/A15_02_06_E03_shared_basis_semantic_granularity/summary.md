---
experiment_id: A15_02_06_E03_shared_basis_semantic_granularity
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
date: 2026-08-12
---

# Semantic granularity is ordered later in the mean-response parameter spectrum

## Direct result

In the frozen gain-sensitive mean-response MLP parameter basis, the Attention-write spectrum is later for fine than coarse semantic variation. Across blocks 1--35, the median rank-centroid contrast is

\[
T_{F-C}=+0.008175,qquad 95\%\ \mathrm{CI}=[+0.001964,+0.012620].
\]

Both expression halves are positive (`+0.009568`, `+0.006794`). The registered primary outcome is `fine_later_than_coarse`.

The constructed medium level lies between coarse and fine in the threshold-free centroid:

| Contrast | Median over blocks 1--35 | 95% parent-bootstrap interval | Half A / B |
| --- | ---: | ---: | ---: |
| medium − coarse | +0.005181 | [+0.001451, +0.009696] | +0.007818 / +0.002797 |
| fine − coarse | +0.008175 | [+0.001964, +0.012620] | +0.009568 / +0.006794 |
| fine − medium | +0.004089 | [+0.000958, +0.005287] | +0.003737 / +0.003570 |

Its ordered score (`0.004089`) exceeds the 95th percentile of 256 balanced random pairings (`0.001540`), so the registered medium guard passes. This supports a dataset- and basis-conditioned coarse < medium < fine ordering; it does not turn the constructed medium groups into native labels.

## Two required figures

Figure 1 is the requested single-panel reference for the selected common basis. It re-renders the unchanged fine-only E02 curves and is not the granularity test.

![Mean-response common-basis reference](figures/figure1_mean_response_common_basis_reference.png)

Figure 2 contains the decisive fine-minus-coarse redistribution, the threshold-free centroid contrasts, and the requested fixed middle-late energy-share contrasts.

![Semantic-granularity result](figures/figure2_semantic_granularity_spectral_location.png)

For the frozen normalized-rank interval `[0.50, 0.75)`, fine minus coarse middle-late share is `+0.004893` with interval `[+0.002433,+0.007840]`; both expression halves are positive. Fine minus coarse is also positive in the two registered neighboring intervals. Fine minus medium is unresolved in `[0.375,0.625)`, so no claim is made that every middle sub-band is strictly ordered.

## Claim boundary

- The centroid point estimate is positive in 28/35 registered blocks; the fixed middle-late share is positive in 23/35. The result is a trajectory-level median, not an every-layer law.
- All spectra are normalized within semantic level. They establish relative location, not greater absolute variance or greater information content.
- The mean-response basis preserves parameter-gain magnitude. The earlier rank-consensus disagreement remains; this result is not a universal common-rank statement.
- `attention_write` is the post-`o_proj`, pre-residual branch output. It is not proven to be information absent from the incoming residual.
- No effective-rank, causal MLP use, Router prediction, expert utility, training, or inference benefit was tested.

## One next decision

Human decision required: whether this basis-specific semantic ordering is sufficient to authorize a separate frozen functional Router-admission test. No Router experiment is opened by this result alone.

Evidence: [Protocol](protocol.md), [Detailed record](detailed.md), [global summary](tables/global_summary.csv), [layerwise metrics](tables/layerwise_metrics.csv), [band sensitivity](tables/middle_late_sensitivity.csv), and [random-pairing control](tables/random_pairing_control.csv).
