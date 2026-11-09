---
experiment_id: A15_00_01_E01_cross_document_subspace_stability
status: complete
verdict: pass_stable_centered_less_stable_local_residual
completed: 2026-07-31
---

# Summary: Cross-Document Stability of the Centered Common Subspace

## Conclusion

The centered Router representation is not a collection of unrelated
batch-local residual spaces. A top-64 basis fitted on one DCLM document group
transfers strongly to disjoint documents in both LB and decommon models. After
an independently pooled top-64 is removed, the local residual top-64 also
transfers above a matched random-direction null, but consistently less.

Thus the strong hypothesis that demeaning leaves no stable learning coordinate
is falsified. The supported statement is narrower: a transferable centered
component exists and captures more held-out energy than an equal-rank local
residual. A direct projector comparison further shows that the residual basis
itself is also highly shared across the random document shards.

## Decision Metric

Cross-capture is the fraction of target-document centered activation energy
captured by a basis fitted on different documents. \(\Gamma\) subtracts the
target's matched Haar-64 q95. Positive \(\Gamma\) means transfer beyond random
directions; \(\Gamma_{\mathrm{top}}-\Gamma_{\mathrm{res}}>0\) means the centered
top-64 transfers more strongly than the residual top-64.

| Lineage | Step | \(\Gamma_{\mathrm{top}}\) | \(\Gamma_{\mathrm{res}}\) | Gap | Gap 95% CI |
| --- | ---: | ---: | ---: | ---: | ---: |
| LB | 40k | 0.584 | 0.409 | 0.162 | [0.158, 0.165] |
| LB | 80k | 0.564 | 0.392 | 0.167 | [0.161, 0.169] |
| decommon | 40k | 0.600 | 0.414 | 0.179 | [0.175, 0.182] |
| decommon | 80k | 0.580 | 0.402 | 0.176 | [0.172, 0.179] |

All 12 layers have positive top transfer, positive residual transfer, and a
positive top-minus-residual gap in all four retained endpoints. The decommon
80k primary and 40k replication satisfy the registered Pass rule.

Projector overlap directly measures whether two fitted 64-dimensional spaces
occupy the same directions:

\[
O_{s,t}=\frac{\|U_s^\top U_t\|_F^2}{64}.
\]

\(O=1\) means identical projectors. Matched random q95 is 0.086 for the full
768-dimensional space and 0.094 inside the 704-dimensional residual
complement.

| Lineage | Step | Centered-top overlap | Residual overlap |
| --- | ---: | ---: | ---: |
| LB | 40k | 0.791 | 0.729 |
| LB | 80k | 0.766 | 0.719 |
| decommon | 40k | 0.784 | 0.730 |
| decommon | 80k | 0.760 | 0.704 |

Both projectors therefore overlap strongly across random document shards.
The centered top is only modestly higher at the model level, with local layer
exceptions. The energy-transfer gap cannot be interpreted as evidence that
the residual directions rotate almost randomly by shard.

## Central Figure

![Centered top-64 and local residual-64 cross-document transfer](figures/centered_common_vs_residual_transfer.png)

The lines are observed layerwise effects and the bands are paired
document-bootstrap 95% intervals. Both spaces transfer; the centered top-64 is
uniformly stronger.

## Validity

- 640 held-out DCLM documents are disjoint from the earlier Q1 and Q2 sets.
- Actual Gate-input replay, native top-1 replay, center invariance, rank,
  within-shard known-good, SVD, and numerical guards all pass.
- Demeaning changes the DC term but not the centered covariance: decommon's
  maximum covariance discrepancy is 0.000881 and minimum top-64 overlap is
  0.999999.
- Fit-document counts 8, 16, and 32 preserve the direction of the main gap.
- Per-document bootstrap used 2,000 replicates; layers were not treated as
  independent seeds.
- By researcher amendment, 30k is not claim-bearing; the result uses 40k and
  80k only.

## Boundary And Next Decision

“Common” here means cross-document statistical transfer, not shared semantics
or training utility. The result does not show that residual directions are
useless, that instability caused decommon's loss behavior, or that the pooled
component should be retained or removed.

The current shards are stable-hash random mixtures of DCLM documents, not
semantic conditions. They cannot rule out condition-specific low-dimensional
modes hidden inside a globally shared residual envelope. The next decision is
whether to construct domain/topic-stratified shards and jointly test projector
overlap and cross-capture before any matched training intervention.
