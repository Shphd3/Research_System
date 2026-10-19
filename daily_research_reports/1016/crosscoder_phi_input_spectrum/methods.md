# Raw hidden spectra for inputs selected by the frozen φ groups

This derived supplement asks whether input sets selected by the original R/F/N allocation rules have concentrated covariance spectra, and whether concentration remains after removing each group's own leading centered component. It does not change the Anchor, frozen groups, graph, learned parameters, or scientific state.

## Frozen groups and selection

R contains the original 186 φ groups. F sorts the same 13,807 features by discovery-side count, breaking ties by feature ID, then fills the original group-size sequence consecutively. N permutes R labels within ten equal-count discovery-frequency bins, preserving each R group's size and bin composition. Group sizes range from 2 to 735 and match exactly by group ID across conditions. F is not the later fixed-size-14 frequency grouping; N is not that later mixed-frequency control.

For a position, each group's binary active-member fraction is standardized using its saved discovery mean and population standard deviation. Zero-standard-deviation groups receive score zero. Unhit groups cannot compete. The largest score wins even if negative; ties follow the saved hash order of sorted member IDs. A no-hit position has winner −1, not a group inferred from the downstream four-expert fallback. The original scoring function and saved maps are reused without fitting. Reconstructed four-expert routes and independent row-wise winner calculations qualify implementation.

## Raw representation and support

All conditions use the original learning EVAL512 cache: 523,136 eligible prediction positions in 512 contexts from the same source file. Raw hidden is block 28 residual-post, before final RMSNorm, stored in BF16 and converted to FP64 for computation. No decoder, CrossCoder contribution, model forward, or training is used.

The source is an original CrossCoder TRAIN file, distinct from structural VAL. This is the existing learning evaluation window, not a new independent document confirmation. Source-document and near-duplicate independence remain unknown.

Each group samples exactly 128 winning positions without replacement using frozen deterministic priorities based on seed, member set, and absolute position. The support-only stage precedes spectrum inspection. R/F/N respectively have 176/168/171 supported groups. The primary population is the 145 group IDs supported in all three conditions, maintaining the same group-size sequence. All 186 groups per condition retain explicit support and missingness records; separate tables cover all supported groups and the R/N intersection of 161 groups. Zero original or residual variance is reported as non-estimable, never zero concentration.

The common 145 groups cover 8,814 of 13,807 members (63.84%), not the entire frozen pool. Group support is uneven, particularly for some large N groups. Group counts alone cannot establish representative member coverage.

## Centered and residual spectra

For a group's sampled raw-hidden matrix H with N=128 rows and 1,024 columns, center each column across positions to obtain Hc. Compute:

\[
C_G=\frac{H_c^\top H_c}{N-1},\qquad
q_{G,j}=\frac{\lambda_{G,j}}{\sum_k\lambda_{G,k}}.
\]

Eigenvalues are descending. Normalize within each group, then average groups equally. The original leading share is λ₁/Σλ. It measures concentration of total position-centered variance.

Remove each group's own leading centered singular component:

\[
H_c=U\Sigma V^\top,\qquad
H_{\mathrm{res}}=H_c-\sigma_1u_1v_1^\top.
\]

The residual normalized spectrum and its leading share are:

\[
q_{G,j}^{\mathrm{res}}=
\frac{\lambda_{G,j+1}}{\sum_{k\ge2}\lambda_{G,k}},\qquad
q_{G,1}^{\mathrm{res}}=
\frac{\lambda_{G,2}}{\sum_{k\ge2}\lambda_{G,k}}.
\]

Retain removed share, remaining share, and residual total variance alongside renormalized spectra. Group-specific leading directions differ. This operation does not remove a single global uncentered direction and does not identify a common feature.

Centered rank is at most 127; after removing one direction it is at most 126. These are finite-sample rank constraints, not model capacity. A position-Gram decomposition yields the same nonzero eigenvalues as the hidden covariance; direct decompositions qualify numerical equivalence.

## Interpretation

Original spectra describe concentration of total variance. Residual spectra describe concentration outside each group's largest direction. Differences concern input sets selected by a competitive, discovery-standardized allocation rule. They do not identify an intrinsic feature-group dimension or a causal effect of φ, frequency, capacity, or learning compatibility.

Report group-size strata, group-average discovery frequencies, selected-context counts, and maximum single-context shares. Same-condition groups have disjoint selected positions, but may share contexts; conditions may select overlapping positions. Positions and groups are not independent documents. No p-values or independent-document confidence claims are implied. Researcher-owned mechanism judgment and question closure remain Unknown.
