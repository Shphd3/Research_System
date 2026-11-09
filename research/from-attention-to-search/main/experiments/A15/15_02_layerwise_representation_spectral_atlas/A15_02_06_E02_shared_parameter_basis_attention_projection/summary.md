# A15_02_06_E02 Summary: Shared Parameter Bases And Attention Projection

> Status: `RESULT_COMPLETE_AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## Verdict

The typed verdict is **`basis_sensitive_shift`**. The experiment does **not** establish a basis-independent right shift of conditional-fine Attention-write variance with depth.

- In the **mean parameter-response basis**, the normalized-rank centroid moves from an early-block median of 0.44549 to a late-block median of 0.47721. The registered contrast is \(T_{MR}=+0.03171\) with 95% parent-bootstrap interval \([+0.02058,+0.04433]\); expression halves A/B give +0.03304/+0.03320.
- In the **rank-consensus basis**, the early/late medians are 0.48816 and 0.48061. The registered contrast is \(T_{RC}=-0.00755\) with interval \([-0.01869,+0.00121]\); expression halves A/B give -0.00749/-0.00526.
- Both bases pass the pre-registered minimal non-random-coordinate screen in all 36 layers, but only weakly in the median: diagonal-energy ratios to the analytic Haar expectation are 1.0777 and 1.0527.

The narrow knowledge update is:

> A positive depth shift appears only when shared rank preserves parameter-gain magnitude. It disappears, and weakly reverses, when shared rank keeps only cross-layer ordinal band consensus. Therefore “deeper Attention writes move right in a common parameter spectrum” is currently a coordinate-dependent description, not a stable property that can yet support routing.

![Normalized log curves](figures/figure1_normalized_log_curves_selected_layers.png)

## Requested Experiment Card

**Experiment purpose.** Test whether different decoder blocks allocate conditional-fine variance of the isolated Attention write to different locations in one fixed cross-layer MLP input coordinate.

**Data.** Frozen Qwen3-8B; all 36 post-`o_proj`, pre-residual Attention writes; one balanced fine-only TAX cube with 8 parents × 8 children × 4 templates × 2 fact bundles = 512 records. Child means are centered within each parent. No coarse/fine comparison is made.

**One-sentence description.** Construct two parameter-only 4096-dimensional shared bases from all layers' \(W_{gate}^{\top}W_{gate}+W_{up}^{\top}W_{up}\) operators, project every layer's conditional-fine Attention-write covariance into each frozen basis, normalize variance within layer, and compare early versus late normalized-rank centroids.

**Conclusion.** Mean parameter response supports a right shift, whereas rank consensus does not; the registered result is basis-sensitive rather than a shared-coordinate right-shift pass.

**Necessary figures.** The selected- and all-layer normalized log curves are `figure1` and `figure2`; the unsmoothed layer×rank atlas is `figure3`; the registered statistic and coordinate guard are `figure4`.

## What The Two Bases Mean

For each decoder block,

\[
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}
+W_{up,\ell}^{\top}W_{up,\ell}.
\]

For a unit residual-stream direction \(x\), \(x^{\top}K_\ell x\) is the squared native MLP input-side parameter response.

### Mean parameter-response basis

Each \(K_\ell\) is trace-normalized, the 36 operators are averaged, and the average is diagonalized. Earlier rank means larger **average normalized parameter response**. This construction preserves within-layer eigenvalue magnitude. Its positive result says that, relative to this gain-sensitive average order, later-layer fine variance occupies later ranks.

### Rank-consensus basis

Each local spectrum is divided into 16 equal 256-rank bands. A direction receives only the ordinal score of its local band; the averaged score operator is then diagonalized. Earlier rank means **more consistent assignment to early local bands across layers**. This construction discards eigenvalue magnitude and is invariant to rotations inside each 256-dimensional band. It gives no positive depth shift.

The bases are not unrelated: their shared-rank correlation is 0.906, mean same-band overlap is 0.467 versus the 0.0625 Haar expectation, and mean normalized-rank displacement is 0.0665. Their semantic readings differ mainly in shallow layers: the median mean-response minus rank-consensus centroid is -0.0422 in blocks 1--12 but +0.0006 in blocks 25--35. Thus the positive \(T_{MR}\) is mostly created by locating shallow-layer variance earlier, not by a disagreement about late-layer location.

![Basis alignment and reading difference](figures/figure5_basis_alignment_and_reading_difference.png)

## Coordinate And Numerical Validity

| Quantity | Mean response | Rank consensus |
| --- | ---: | ---: |
| Layers above Haar baseline | 36/36 | 36/36 |
| Median diagonal-energy / Haar | 1.0777 | 1.0527 |
| Median diagonal-energy fraction | 0.7225 | 0.7180 |
| Registered \(T\) | +0.03171 | -0.00755 |
| 95% parent-bootstrap interval | [+0.02058, +0.04433] | [-0.01869, +0.00121] |

The coordinate screen is deliberately minimal. A ratio just above one means more local spectral structure than a random orientation; it does not mean exact simultaneous diagonalization. Median diagonal-energy fractions remain about 0.72 rather than the local-eigenbasis optimum of 1.

All model shards and 36 cached Attention files match the frozen manifests. Maximum local eigensolver residual is \(1.73\times10^{-5}\), shared-basis residual \(2.82\times10^{-6}\), orthogonality error \(2.81\times10^{-6}\), and projection-energy relative error \(2.33\times10^{-7}\). Six unit tests and the three-layer real-data smoke pass. All five central figures pass full-resolution visual audit.

## Important Normalization Boundary

The curves plot \(4096p_{\ell j}\) on a logarithmic axis, where \(\sum_jp_{\ell j}=1\) separately in every layer. They measure **where each layer places its own fine variance**, not how much fine variance the layer has. The absolute conditional-fine trace rises sharply: the late-window median is about 607 times the early-window median, and the largest layer trace is about \(1.03\times10^5\) times the smallest. That scale change is retained in the evidence table but is not a right-shift result.

![Registered statistic and coordinate guard](figures/figure4_centroid_and_coordinate_audit.png)

## Claim Boundary

This result does not prove that an Attention write is information absent from the incoming residual stream, that the write is low rank, that later shared rank means finer semantics, that individual shared directions have stable semantic identity, or that a Router using this coordinate improves training or inference. The TAX cube is one controlled semantic construction on one frozen model.

## One Next Decision

Run one held-out-coordinate falsifier only: construct both registered bases from blocks 13--24 and evaluate the unchanged blocks 1--12 versus 25--35 contrast. If the gain-sensitive and ordinal bases still disagree, close the universal common-rank right-shift hypothesis rather than trying additional bases; retain only the basis-specific geometry observation.
