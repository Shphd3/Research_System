# A15_07_E02 Result Summary

## Conclusion First

The experiment does **not** establish a compact, fixed-basis domain-direction
atlas suitable for a layerwise Router. Full candidate-update access has
positive unseen-expression function for 15 of 16 domain-layer pairs, but every
domain requires the freely learned model's full seven independent class
contrasts to reach the development 90%-gain crossing, and none of the three
fixed spectra passes the complete held-out robustness gate.

The result nevertheless provides a bounded spectral update. The learned
rank-seven spaces consistently concentrate in the tail of both parameter-
response spectra and mostly outside the activation-PCA top-500 span. Learned
spaces also have substantial cross-domain geometric overlap, especially at
block 28. These are spectral-band and geometry observations; because no compact
fixed-axis condition qualifies, they do not identify a shared functional axis,
a domain-specific functional axis, or a credible axis-level semantic label.

**Decision:** do not modify the Router proxy from these directions. The active
cycle now awaits the researcher's result/boundary confirmation.

## Direct Results

### 1. The candidate update usually adds held-out fine-class function

On the sealed 1,920-row unseen-expression bank, full-\(R_U\) admission passes for
all eight domains at block 28 and seven of eight at block 24. Block-24
mathematics is unresolved: full gain is 0.02295 nats/example, but the margin
over the strongest duplicate/mismatch control is -0.00255 with simultaneous
interval [-0.02811, 0.02302]. All other admission lower bounds are positive.

This establishes linear added accessibility for those 15 pairs. It does not
establish new knowledge or native causal use.

### 2. Direct low-rank learning does not find a nontrivial compact space

For every domain at both blocks, development selects rank seven, the full
independent contrast ceiling for eight classes. The C5 point retention is
0.991--1.009 for the 15 admitted pairs, and their gain beyond label-permutation
q95 has a simultaneous positive lower bound. However, no rank at most four
reaches the registered development crossing, and the rank-seven simultaneous
retention lower bounds are only 0.765--0.783, below the strict 0.80 boundary.

Thus fine-class function is accessible, but this experiment does not show that
it is compressible into the requested rank-1/2/4 space.

### 3. No fixed spectrum supplies qualified compact axes

The fixed-axis score selects axes with large between-fine-class separation and
small within-class expression variation. The selected axes were compared with
the spectral head, same-size random axes, end-to-end label permutations, and a
tenfold denominator shrinkage. No `(layer, domain, basis)` condition passes all
registered gates.

The two closest compact candidates are still non-verdict-bearing:

- block-28 physics, common mean-response spectrum: 8 axes, point retention
  0.7996, excess gain 0.01608, unchanged under the denominator stress test;
- block-28 medicine, local parameter-response spectrum: 16 axes, point
  retention 0.8310, stressed retention 0.8045, excess gain 0.02268.

Neither survives the simultaneous familywise confidence gate. Their axis ranks
remain candidates, not semantic directions.

### 4. Spectral-band localization is stable across domains

For the learned rank-seven spaces, the final one-sixteenth of the two full
parameter-response spectra (ranks 3,841--4,096) carries the largest energy:

| Block | Local parameter tail | Common mean-response tail | Matched-Haar q95 |
| --- | ---: | ---: | ---: |
| 24 | 0.2461 | 0.2695 | about 0.0659 |
| 28 | 0.4107 | 0.4350 | about 0.0659 |

All eight domains exceed the matched-Haar q95 in this final band at both
blocks. In the activation-PCA ruler, 0.7514 of block-24 energy and 0.6208 of
block-28 energy lies outside the identified top-500 span. The first top-500
band carries another 0.1348 and 0.2645 respectively.

This supports “classification-targeted function is not ordered by maximum
activation variance.” It does not establish that a particular tail axis is
functional.

### 5. Domains reuse geometry, but shared function is unresolved

The normalized pairwise projector overlap of learned rank-seven spaces is
0.1522 on average at block 24 and 0.2970 at block 28; all 28 domain pairs at
each block exceed the matched random q95 of 0.00230. Same-domain cross-layer
overlap ranges from 0.1475 to 0.1510.

This is substantial non-random geometric reuse and it grows with depth. It
cannot be promoted to a shared functional component because the experiment did
not qualify a compact fixed axis or separately test a shared learned component
on C5.

## Per-Domain Candidate Dimension Atlas

Values are the smallest DEVELOPMENT dimension reaching 90% of full-update
gain; `>64` means no registered fixed-axis crossing. These are descriptive
candidates because none passes the full C5 gate.

| Block | Domain | Local parameter | Common response | Activation PCA | Learned free rotation |
| --- | --- | ---: | ---: | ---: | ---: |
| 24 | mathematics | >64 | >64 | >64 | 7 |
| 24 | physics | >64 | >64 | 64 | 7 |
| 24 | chemistry | >64 | >64 | >64 | 7 |
| 24 | biology | 32 | >64 | >64 | 7 |
| 24 | computer science | >64 | >64 | >64 | 7 |
| 24 | economics | 64 | >64 | >64 | 7 |
| 24 | medicine | >64 | >64 | >64 | 7 |
| 24 | linguistics | >64 | 64 | >64 | 7 |
| 28 | mathematics | >64 | 64 | 64 | 7 |
| 28 | physics | 16 | 8 | 32 | 7 |
| 28 | chemistry | >64 | >64 | >64 | 7 |
| 28 | biology | 64 | 64 | 8 | 7 |
| 28 | computer science | 32 | >64 | 32 | 7 |
| 28 | economics | >64 | 32 | 32 | 7 |
| 28 | medicine | 16 | 16 | 16 | 7 |
| 28 | linguistics | >64 | 32 | >64 | 7 |

## Figures

![Functional dimension curves](figures/figure_1_functional_dimension_curves.png)

![Direction and spectral-band atlas](figures/figure_2_direction_and_spectral_band_atlas.png)

Six individual spectral curves: [local L24](figures/figure_2a_local_parameter_block24_curve.png),
[local L28](figures/figure_2b_local_parameter_block28_curve.png),
[common L24](figures/figure_2c_mean_response_block24_curve.png),
[common L28](figures/figure_2d_mean_response_block28_curve.png),
[activation-PCA L24](figures/figure_2e_activation_pca_block24_curve.png), and
[activation-PCA L28](figures/figure_2f_activation_pca_block28_curve.png).

![Learned overlap and qualified-axis boundary](figures/figure_3_overlap_and_fine_class_fingerprint.png)

## Claim Boundary

Established: unseen-expression full-\(R_U\) added accessibility in 15 pairs;
failure to establish rank-\(\le4\) compactness or any fixed-basis qualifier;
tail/complement localization of the learned full-contrast spaces; non-random
learned-space geometric overlap.

Not established: trustworthy axis semantics, function-qualified shared or
domain-specific axes, Router utility, expert specialization, native causal use,
new knowledge, natural-data transfer, or model/layer universality.

## Evidence

- [Protocol](protocol.md)
- [Complete evidence record](detailed.md)
- [Self-contained Chinese explanation](detailed_cn.md)
- [Domain-layer verdict table](tables/domain_layer_atlas.csv)
- [Functional curves](tables/functional_curves.csv)
- [Selected-axis candidates](tables/selected_axes.csv)
- [Learned spectral energy](tables/learned_spectral_energy.csv)
- [Learned subspace overlap](tables/learned_subspace_overlap.csv)
