# Summary: A15_17_E03 Attention-Sidecar Representation, Variance, And Local-Gradient Audit

Primary Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Execution receipt: [execution_receipt.md](execution_receipt.md)  
Post-hoc per-class Fisher and loss-scale supplement: [supplement_per_class_fisher_loss.md](supplement_per_class_fisher_loss.md)  
Fisher, random-orthogonality, and LM-loss reliability audit: [fisher_gradient_reliability.md](fisher_gradient_reliability.md)  
Result status / eligibility: `ELIGIBLE_READ_ONLY_MEASUREMENT_WITH_RECORDED_CPU_SYNTHESIS_REPAIR`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## 1. Purpose

Add the new final-layer, layers-3+7, and all-eight-layer Attention-output SAE sidecar models to the common-checkpoint representation audit and directly measure variance organization and local auxiliary-versus-LM gradient geometry.

## 2. Hypothesis

If sidecar training improves accessible organization, a native final-state change should be coherent across the synthetic P and M2D2 N panels and remain after fit-only first-direction removal. The strongest rival is a panel-specific or dominant-direction effect accompanied only by a local auxiliary gradient.

## 3. Analysis Method

- Compare native final-block post-norm2 B/W/F, covariance spectra, and frozen readouts for M0/M1/M2/S7/S37/SALL at common 0/0.5/1/3B checkpoints under raw and B3 coordinates.
- Compare each sidecar layer's Attention output and SAE reconstruction variance organization on P and N.
- On four stratified N-fit batches, compare LM and local reconstruction gradients at the identical Attention-output node using norms, ratios, cosines, and angles on the full node and the 32-position SAE support.

Endpoint boundary: at execution freeze, S7 had physical milestones through 10B, S37/SALL through 3B, and none of the three source trees had a 15B milestone. The main comparison therefore uses only the real common 0/0.5/1/3B intersection; no 15B point was interpolated, substituted, or mixed into an unmatched comparison.

## 4. Conclusion

**Verdict: the registered measurement is complete and eligible, but none of the three sidecar conditions shows a native final-state advantage that holds across both panels. Local reconstruction gradients reach the backbone and have near-90-degree numerical angles, but most are not more orthogonal than dimension-matched random directions; their credible main difference is magnitude. This is an AI draft awaiting researcher confirmation.**

At 3B under B3, P Fisher/readout values are M0 `0.297/0.961`, S7 `0.214/0.900`, S37 `0.273/0.944`, and SALL `0.222/0.928`. N Fisher values cluster at M0 `0.207` and S7/S37/SALL `0.203/0.205/0.205`, with readouts `0.783/0.785/0.795/0.783`.

![B3 Fisher trajectories](figures/final_fisher_b3_trajectories.png)

SALL concentrates P variance at 3B (`top1=0.204`, `PR=14.69`) relative to M0 (`0.146`, `17.85`), but this does not replicate on N (`0.104/32.33` versus `0.103/31.45`). B3 retains only 52.1%, 53.6%, and 55.0% of raw P Fisher for S7/S37/SALL.

![Native final-state covariance distribution](figures/final_variance_distribution_trajectories.png)

At 3B on SAE-supported positions, all mean angles fall in `89.91°–90.17°`. Across 44 checkpoint-layer groups, however, 43 are compatible with the exact isotropic random null in the same 262,144-dimensional support, none is unusually closer to zero, and the only departure (SALL 1B L0) has larger absolute cosine. All 11 groups at 3B are random-compatible. Reconstruction-to-LM norm ratios are S7 L7 `0.653`, S37 L3/L7 `0.170/0.245`, and SALL per-layer `0.012–0.047`.

![Dimension-calibrated local gradient cosine](figures/gradient_cosine_vs_dimension_matched_random.png)

### Claim Boundary

Can claim: eligible cross-checkpoint representation and local-gradient measurements; nonzero reconstruction gradients; structurally zero AuxK node gradients; near-zero local cosines that are mostly compatible with dimension-matched random directions; placement-dependent scale.

Cannot claim: LM benefit, native use of SAE reconstruction, learned special orthogonality, causal long-run mechanism, superior multi-layer placement, routing, or expert specialization.

### Next Step Analysis

Decision: `AI suggestion pending researcher confirmation` — use the [E05 draft Protocol](../A15_17_E05_multimodel_fisher_gradient_coefficient_audit/protocol.md) to measure summed reconstruction gradients in shared parameter groups and wait for the exact 0/0.5/1/3/5/10/15B common grid before authorizing any coefficient continuation.

Completion criterion: exact vector-sum identity plus batch/checkpoint-stable parameter-group norm and angle estimates. Stop treating the sidecar gradient as a primary mechanism if the summed effect remains an order of magnitude below LM with no stable alignment or opposition; proceed to matched LM-only versus sidecar continuation only if a reproducible parameter-level effect survives.
