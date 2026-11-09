# Summary: A15_17_E04 Layer-8 Attention-Sidecar Representation Trajectory

Primary Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: `AI-DRAFT`; eligible for bounded single-seed representation-accessibility, geometry, reconstruction, and local-gradient claims through 10B tokens; ineligible for causal functional-use or generalization claims.

## 1. Purpose

Test whether a width-30,000 Top-32 SAE sidecar on the eighth block's raw Attention output produces a coherent Dense-relative representation trajectory that survives removal of the fit-only leading centered direction.

## 2. Hypothesis

A genuine residual-organization change should have a consistent sign across the controlled P panel and natural N panel and should remain visible after B3 de-commoning. The strongest rival is a panel-specific redistribution of variance caused by a local reconstruction pressure without improved semantic accessibility.

## 3. Analysis Method

- Pair `M0` and `S7` on identical P/N report rows at 0, 0.5, 1, 3, 5, and 10B tokens; report coarse Fisher and frozen-probe differences with stratum-preserving paired bootstrap intervals.
- Compare raw coordinates with B3 fit-only centering and leading-direction removal; select probe regularization on raw coordinates and reuse it unchanged for B1/B2/B3.
- Keep native final-state accessibility, covariance geometry, SAE contribution shares, reconstruction FVU, local gradient geometry, and token-aligned training loss as distinct evidence surfaces.

## 4. Conclusion

Verdict: **the sidecar learned and materially reshaped local/final geometry, but no coherent cross-panel improvement in de-commoned domain accessibility was detected.**

| Registered question | Smallest decisive result | Eligibility | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Does B3 coarse readability improve at 10B? | P: `S7-M0 = -0.0611`, 95% CI `[-0.1000,-0.0278]`; N: `+0.0025`, `[-0.0275,+0.0325]` | paired report rows; fixed raw-selected C | no coherent improvement; P decreases, N unresolved | [paired probe table](tables/paired_probe_differences.csv) |
| Does B3 Fisher separation improve at 10B? | P: `+0.1001`, 95% CI `[-0.1666,+0.1422]`; N: `+0.0040`, `[-0.0008,+0.0090]` | paired report-row bootstrap | neither endpoint excludes zero | [paired Fisher table](tables/paired_fisher_differences.csv) |
| Is the sidecar objective physically active at the hook? | 10B support norm ratio `1.4608`, cosine `0.00069`, angle `89.96°` | four frozen fit batches; structural zeros passed | strong, nearly orthogonal local pressure observed | [gradient table](tables/gradient_metrics.csv) |
| Does the SAE reconstruct its input? | 10B FVU: P `0.1799`, N `0.1358` | report rows; centered denominator | reconstruction improved; semantics not implied | [reconstruction table](tables/reconstruction_health.csv) |
| What happened to training LM loss? | S7-Dense `+10.59` millinats near 10B; maximum `+107.59` near 0.627B | token-aligned 200-update trailing mean; training only | small persistent training-loss cost is descriptive | [loss table](tables/training_loss_trajectory.csv) |

### Important Figures

![Paired representation differences](figures/03_paired_geometry_and_readability.png)

How to read: zero means no S7-Dense difference; the B3 coarse-probe signal is negative on P at 3B and 10B but remains near zero on N, so the trajectory is neither monotone nor cross-panel coherent.

![Support-only gradient geometry](figures/06_gradient_magnitude_ratio_angle_support.png)

How to read: the reconstruction gradient grows to 1.46 times the LM gradient on the sampled support while the angle stays almost exactly 90 degrees.

![Reconstruction and dictionary health](figures/09_reconstruction_fvu_trajectory.png)

How to read: reconstruction FVU falls substantially by 10B, while dictionary coverage is sparse and non-monotone; lower FVU is not semantic evidence.

![Token-aligned training loss](figures/10_training_loss.png)

How to read: both LM losses descend normally, but the sidecar curve remains slightly above Dense; the bottom panel shows the weighted auxiliary objectives that create the additional pressure.

### Claim Boundary

Can claim: this S7 trajectory learned a useful reconstruction, imposed a strong nearly orthogonal local gradient, redistributed variance, and did not show coherent cross-panel B3 readability improvement through 10B.

Cannot claim: causal LM benefit or harm, native use of SAE features, stable atom semantics, functional specialization, or generality across seeds/scales.

### Next Step Analysis

Decision: `AI PROPOSAL`, not researcher-confirmed — if causal attribution is still decision-relevant, compare the same sidecar/SAE with versus without reconstruction-gradient flow into the backbone under matched tokens, optimizer, batch, data order, and multiple seeds.

Why it follows: the current result establishes a strong local pressure but not that this pressure caused the endpoint accessibility pattern.

Unresolved uncertainty: auxiliary-gradient causality versus single-trajectory noise and panel-specific variance structure.

Completion criterion: matched held-out LM loss and B3 paired accessibility at the same token endpoint, with a seed-level uncertainty interval.

Stop or redirect condition: if the gradient-blocked control retains the same geometry/loss differences, stop attributing them to backbone-side reconstruction pressure.

Resume action: write a separately approved intervention protocol; no new run is authorized here.
