---
experiment_id: A15_02_01_E01_controlled_layer_information_profile
anchor_id: 15_02_01_controlled_layer_information_identity
status: completed_pass
verdict: pass_with_negative_composite_band_result
completed: 2026-07-31
---

# Layer × Band × Information Profile in a Four-Layer MoE

## Conclusion

The registered question passes: relative covariance rank does not carry an invariant meaning across layers. In capability-valid four-layer MoEs, composition training reproducibly made F1/head specific to the intermediate state \(m=x+a\) at layers 3--4 and made the adjacent F2 band specific to the coarse condition \(a\). Both effects beat equal-rank random directions, were absent in the matched one-step controls, and replicated across seeds 17 and 29.

The stronger claim that the composed result moves into middle or tail with depth fails. Full-state readability of \(y=x+a+b\) rose from 0.113 at layer 1 to 0.784 at layer 4 under the composition objective, while remaining near 0.10--0.16 in the one-step controls. Yet no H/M/T or fine-band \(y\) cell beat its equal-rank random-direction control in both seeds.

The resulting knowledge update is:

> Layerwise computation changes representational content, but functional information does not move monotonically down covariance rank. A band name is a within-layer variance coordinate, not a cross-layer semantic identity.

## Measurement Meaning

Low-sample readability is the mean sealed-test accuracy of a ridge-linear readout fitted with 32, 64, 128, and 256 labeled examples. It measures how easily a variable can be linearly recovered from a representation; it does not show that the Router uses that variable.

Band specificity is

\[
S_{\ell,B,q}=A_{\ell,B,q}-Q_{0.95}(A_{\ell,R_{d_B},q}),
\]

where the second term is the 95th percentile over 64 equal-rank Haar-random subspaces. The composition contrast is

\[
\Gamma=S^{\rm composition}-S^{\rm one\text{-}step}.
\]

A positive replicated \(\Gamma\) therefore identifies organization induced by the two-step objective rather than generic depth, random projection preservation, or the shared training pipeline.

## Capability Gate

The data use \(\mathbb Z_{17}\) with \(m=(x+a)\bmod17\) and \(y=(m+b)\bmod17\). Eight final-query \((a,b)\) pairs form a held-out perfect matching. Both conditions were trained twice.

| Condition | Seed | Unseen final accuracy | Unseen final NLL | Verdict |
| --- | ---: | ---: | ---: | --- |
| One-step control | 17 | 1.000 | \(1.88\times10^{-8}\) | Pass |
| One-step control | 29 | 1.000 | \(3.73\times10^{-9}\) | Pass |
| Composition | 17 | 1.000 | \(2.85\times10^{-4}\) | Pass |
| Composition | 29 | 0.985 | 0.0279 | Pass |

All layer-2 intermediate-state, load, actual-Gate-input replay, expert-use, and bias guards passed. Because the layer-2 intermediate head is an explicit capability constraint, the experiment does not claim spontaneous emergence of the intermediate computation.

## Decisive Evidence

![Full-state hierarchy and band specificity](figures/final_knowledge_update.png)

The replicated composition-specific cells are:

| Layer-band | Variable | Composition specificity | Control specificity | \(\Gamma\) |
| --- | --- | ---: | ---: | ---: |
| L3-F1/head | Intermediate \(m\) | 0.024 | -0.007 | +0.031 |
| L3-F2 | Coarse \(a\) | 0.168 | -0.202 | +0.370 |
| L4-F1/head | Intermediate \(m\) | 0.097 | -0.006 | +0.103 |
| L4-F2 | Coarse \(a\) | 0.369 | -0.207 | +0.577 |

None passed at initialization. All trained coarse and fine bases passed split-half stability; the minimum overlaps for F1, F2, H, M, and T were 0.997, 0.966, 0.997, 0.951, and 0.964.

## Native Router Use

Removing F1/head from composition-model Gate logits produced mean route-flip rates of 0.377, 0.724, 0.718, and 0.743 across layers 1--4 and mean answer-NLL increases of 0.423, 1.177, 0.780, and 0.373. Both seeds beat equal-rank random controls.

Removing F2, M, or T typically flipped fewer than 1.5% of routes and changed NLL by approximately zero. Thus F2 contains a reproducible coarse coordinate while the native Gate still relies almost entirely on F1/head. Encoded information and routing use are distinct.

## Boundary And Next Decision

The result applies to the registered controlled finite-field task. It does not establish a natural-language hierarchy, cross-layer routing benefit, or improved NLL/FLOP.

The next decision is whether to convert the replicated layer-specific functional coordinates into fixed low-rank readouts that require no online PCA and submit them to an independent one-step compatibility gate. Cross-layer matched training remains blocked until those readouts beat native-score, equal-dimensional random, and wrong-layer controls.

See [detailed.md](detailed.md) and the complete [tables](tables).
