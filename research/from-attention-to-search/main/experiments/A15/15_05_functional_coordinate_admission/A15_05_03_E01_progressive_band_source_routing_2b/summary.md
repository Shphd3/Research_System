---
experiment_id: A15_05_03_E01_progressive_band_source_routing_2b
status: completed_specialization_only_without_quality_pass
completed: 2026-08-02
---

# Summary: 2B Matched Training With Progressive Band Sources

## Conclusion

Explicit spectral routing changed dispatch and some expert-function diagnostics,
but it did not establish that the earlier absence of useful hierarchical
differentiation was merely caused by the native Router not dispatching by band.

Local-HMT routed blocks 2/3/4 through their own H64/M256/T448 views. Its pooled
2B held-out effect versus native was **+0.002174 nat/token** (95% CI
\([0.001758,0.002590]\)), hence worse. Layer-1-relay-HMT routed all three blocks
through H/M/T views of the block-1 output. Its pooled endpoint effect was
**-0.001756 nat/token** (95% CI \([-0.002352,-0.001119]\)), with both paired
continuations favorable.

The relay result is not a training-efficiency win. Switching the Router view at
the 0.629B branch imposed a large immediate NLL penalty, and relay's mean NLL
over the matched continuation remained **+0.02135 nat/token** above native.
It recovered and slightly crossed native late rather than learning more
efficiently over the registered interval.

Relay consistently reduced forced-expert route regret, but expert utility
dispersion decreased and output redundancy increased; other conflict metrics
were mixed. Local-HMT reduced negative gradient-pair frequency and output
redundancy in both replicas, yet its language-model quality was worse. The
typed verdict is therefore **specialization-only without quality pass**; the
functional evidence is partial rather than a coherent specialization profile.

## Metrics in Plain Terms

- Held-out NLL is average next-token surprise in nat/token; lower is better.
- NLL AUC is the average height of the held-out loss curve from the common
  branch to 2B; lower means better quality at matched cumulative compute.
- Route disagreement is the fraction of fixed tokens assigned to a different
  expert than native; it is a manipulation check, not a benefit metric.
- Forced-expert route regret is the extra loss from the Router's selected
  expert relative to the best of eight forced experts on the same token.

## Primary Comparisons

| Comparison | 2B paired \(\Delta\) NLL | NLL-AUC difference | Reading |
| --- | ---: | ---: | --- |
| local − native | +0.002174 \([0.001758,0.002590]\) | +0.02298 | local HMT is worse |
| relay − native | −0.001756 \([-0.002352,-0.001119]\) | +0.02135 | late endpoint gain, worse efficiency |
| relay − local | −0.003930 \([-0.004504,-0.003343]\) | −0.00163 | shallow fixed source beats local source |

![Held-out NLL at matched analytic FLOPs](figures/figure1_heldout_nll_vs_flops.png)

Both treatments pay an immediate adaptation cost. Relay catches native around
the late milestones and ends slightly lower, but its curve integral is worse.

![Final paired effects](figures/figure2_final_paired_nll.png)

Negative values favor the left arm. Relay is favorable at 2B in both
continuations; local is not.

## Validity and Mechanism

Mean block-2--4 route disagreement was 7.12% for local and 19.70% for relay.
The minimum registered-milestone load entropy was 0.974 and maximum expert
share was 17.9%. All six runs completed 2.000683B tokens with zero retry,
identical paired batch hashes, no dead expert, and no capacity drop.

Mean forced-expert route regret across replicas was 0.42485/0.42304/0.41726
nat/token for native/local/relay. This supports a route--utility change, but
does not establish stronger expert differentiation because relay's utility
dispersion fell and output redundancy rose.

![Manipulation and load guards](figures/figure3_route_and_load_guards.png)

![Expert-function diagnostics](figures/figure4_expert_function_mechanisms.png)

## Boundary and Decision

The result is limited to two paired post-0.629B continuations from one
four-layer DCLM checkpoint. There is no equal-rank random schedule, so no
positive relay effect can be attributed uniquely to covariance rank. It does
not establish an optimal HMT order, natural-language semantic hierarchy,
from-initialization formation, or improved training efficiency.

**Next decision:** close fixed HMT rank scheduling as a functional routing
principle. Any later cross-layer Router should first show held-out expert
utility or update-compatibility gain over equal-rank random and wrong-layer
controls before matched training.

See [detailed.md](detailed.md) for the complete evidence ledger.
