---
experiment_id: A15_00_02_E01_gate_common_residual_preference
status: complete
verdict: pass_pooled_alignment_with_native_use
joint_verdict: joint_pass_gate_prefers_transferable_centered_common
completed: 2026-07-31
---

# Summary: Gate Preference for Pooled Versus Local Residual Modes

## Conclusion

After input-energy differences are removed, both trained Gates give the
independently pooled centered top-64 substantially more expert-relative gain
than an equal-rank shard-local residual. Removing the pooled subspace also
reduces the native winner's margin much more. This is not merely a raw-energy
effect or arbitrary Gate anisotropy.

Combined with A15_00_01, the licensed conclusion is:

> At 40k and 80k, the model-level Gate preferentially uses a
> cross-document-transferable centered component over a less transferable
> local residual.

## Decision Metrics

\(B_{P:L}\) is the log ratio between Gate squared gain per direction for the
pooled basis and the median local residual basis. It gives all directions equal
input energy, so \(\exp(B)\) is the gain ratio without covariance-eigenvalue
amplification. Margin-support difference is how much more native-winner margin
is lost when pooled rather than local residual directions are removed; its
unit is logit/token.

| Lineage | Step | \(B_{P:L}\) | Equal-energy ratio \(\exp(B)\) | \(B\) 95% CI | Margin difference | Margin 95% CI |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| LB | 40k | 1.370 | 3.94× | [1.308, 1.434] | 1.873 | [1.857, 1.919] |
| LB | 80k | 1.516 | 4.55× | [1.459, 1.594] | 1.953 | [1.931, 1.994] |
| decommon | 40k | 1.039 | 2.83× | [0.970, 1.120] | 1.998 | [1.948, 2.046] |
| decommon | 80k | 1.125 | 3.08× | [1.040, 1.206] | 2.061 | [2.011, 2.120] |

The model-level \(B\) exceeds the singular-value-preserving orientation-null q95
(about 0.06) in all four endpoints. LB passes layerwise in 12/12 layers.
Decommon passes in 11/12 layers; layer 12 is a real local exception, so the
claim is model-level rather than universal across layers. Margin support is
positive in 12/12 layers for all endpoints.

## Central Figure

![Equal-energy Gate preference and native-route dependence](figures/pooled_vs_local_gate_preference_and_use.png)

The left column removes input-energy amplification; the right column checks
whether the geometry supports the actual native winner. Bands are paired
basis/document-bootstrap 95% intervals.

## Validity

- The same actual Gate inputs, pooled/local rank 64, and target tokens are used.
- All shared object, no-op, rank, SVD reconstruction, known-good, and numerical
  guards pass.
- Each orientation-null draw preserves the Gate's nonzero singular values but
  randomizes its input orientation; observed model medians exceed q95.
- Same-layer pooled gain exceeds the wrong-layer basis in every retained
  layer, with positive minimum log ratios.
- A \(2\times2\) weight-by-basis crossing separates 40k/80k Gate and
  representation changes.
- By researcher amendment, 30k is not claim-bearing.

## Boundary And Next Decision

The result establishes current Gate geometry and native-route dependence, not
expert compatibility, semantics, validation loss, or training benefit. It
also cannot attribute the LB/decommon difference to centering alone.

The next decision is whether to run a separately approved matched intervention
that makes the residual coordinate cross-batch stable and tests whether that
stability changes expert update conflict or held-out loss/FLOP.

