# Summary: A15_08_09_E03 Native Router Representation Controls

Primary Anchor: [A15_08_09](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status: `ELIGIBLE_COMPUTATION`; external 64-row H1 review remains unresolved  
Knowledge status: `AI_EVIDENCE_RECORD_AWAITING_HUMAN_JUDGMENT`

## Result Snapshot

Both broader representations pass the registered above-chance accessibility gate. The native Router input freezes block 42 and reaches 0.77898 same-template and 0.75430 new-template balanced accuracy. The adjacent-layer Router-input difference freezes block 41 and reaches 0.76398 and 0.71211. All four 95% interval lower bounds are above the 0.125 chance level, all fits converge, and both permuted-label controls pass.

This changes the E02 boundary: the standalone weakness is specific to the constructed \(R_U\) object and must not be generalized to the model's full Router-input space. It does **not** establish native gate use or robust positive-margin geometry. Every registered 5th-percentile TEST margin remains strictly negative.

## Decision-Bearing Setup

- **Native input:** \(G_\ell=X_\ell+U_\ell\), exactly the post-attention RMSNorm state sent to the MoE gate.
- **Adjacent difference:** \(\Delta G_\ell=G_\ell-G_{\ell-1}\) for blocks 2--48; block 1 is undefined.
- **Held fixed:** Qwen3-30B-A3B, 19,200 rows, final `Answer:` token, eight parent labels and the E02 TRAIN/DEV/same/new split.
- **Selection:** all-layer GPU ridge screen on TRAIN/DEV only; one layer frozen independently per representation.
- **Confirmation:** five-seed L2 multinomial logistic probe on the frozen layer; 2,000 stratified row-and-seed bootstrap draws.
- **Primary metric:** balanced accuracy on both TEST panels; chance is 0.125.

## Verdict Basis

| Representation | Frozen block | Same-template TEST | New-template TEST | Permuted-label control | H5 |
| --- | ---: | ---: | ---: | --- | --- |
| Native Router input \(G\) | 42 | 0.77898 [0.77195, 0.78602] | 0.75430 [0.74695, 0.76164] | Pass | Pass |
| Adjacent difference \(\Delta G\) | 41 | 0.76398 [0.75664, 0.77141] | 0.71211 [0.70477, 0.71953] | Pass | Pass |

Source: [accuracy_summary.csv](tables/accuracy_summary.csv).

## Key Evidence And Figures

At the frozen blocks, TRAIN between/within total-variance ratios are only 0.04038 for \(G_{42}\) and 0.04971 for \(\Delta G_{41}\). Across all layers their maxima are 0.07449 and 0.06160. Therefore total scatter is strongly within-class dominated even where held-out linear accuracy is high. The ratio is not a separability test because it averages over all coordinates and all rows.

![Native Router-input variance and DEV accuracy](figures/native_router_input_variance.png)

![Adjacent Router-input difference variance and DEV accuracy](figures/adjacent_router_delta_variance.png)

Full curves: [native input](tables/native_router_input_layer_scan.csv) and [adjacent difference](tables/adjacent_router_delta_layer_scan.csv).

## Claim Boundary

Can claim:

- Both registered representations expose stable linear eight-class information across the same-template and new-template panels.
- The E02 \(R_U\) negative standalone result is representation-specific.
- A small global between/within variance ratio can coexist with high classification accuracy.

Cannot claim:

- Qwen's learned gate uses these parent classes.
- The parent labels identify useful experts or improve language-model loss.
- Either representation has positive low-tail margin: same/new margin \(Q_{0.05}\) is -2.1440/-2.8559 for \(G\) and -2.6626/-4.2588 for \(\Delta G\).
- The TEST evidence is pristine; E02 previously opened the same panels.

## Next Decision

Proposed decision, awaiting human judgment: representation-space learning may be opened only as an **expert-utility-aligned positive-margin** problem, with native \(G\) and \(\Delta G\) as mandatory frozen baselines. It should not be motivated as recovery of missing semantic information, because that information is already strongly readable here.

