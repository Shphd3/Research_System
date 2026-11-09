# Summary: A06_01_05_E03 Gradient/Fisher Route-State Selector

## What We Established

Gradient-based route-state selection passes on the uniform no-position bridge.
The strongest condition is the embedding-gradient selector after warmup 40:
immediate feature NMI is `1.000`, margin p05 is `10.083`, matched preserve is
`1.000`, final feature NMI is `1.000`, and final margin p05 is `9.609` across
all `32` seed/slot cells.

This supports a bounded method claim: task gradients can select the
route-relevant hidden-state population without feature labels in this synthetic
setting. It does not prove semantic feature understanding or real-DCLM
transfer.

## Setup And Definitions

Data: four uniformly sampled synthetic features, balanced slot starts, no
explicit position embeddings, sequence length `32`, slot lengths `1/2/4/8`,
and feature-specific targets. The route position is the final token of the
repeated feature slot.

Model: one causal self-attention layer, one weighted top-1 MoE layer with four
experts, and one LM head.

Gradient energy:

\[
E_{i,p}=\|\nabla_{h_{i,p}}\mathcal L_i\|_2^2.
\]

Fisher-like geometry:

\[
F=\mathbb E[g_{i,p}g_{i,p}^{\top}],\qquad
d_F(h_a,h_b)=(h_a-h_b)^\top F(h_a-h_b).
\]

Primary metric: feature NMI, the agreement between true feature id and routed
expert. It decides whether features are separated.

Primary guard: margin p05, the 5th percentile of the matched expert score
minus the strongest competing expert score. It decides whether the partition
has a lower-tail safety buffer.

## Main Result

![Core result](figures/a06_27_core_reinit_nmi_margin.png)

At warmup 40, embedding-gradient top1 and embedding-gradient direction both
reach perfect feature separation and positive lower-tail margins. Post-hidden
gradient top1 is also strong but less uniformly safe across cells. Fisher
subspace clustering improves NMI over all-position clustering, but its margin
remains negative, so it is not a method candidate yet.

| Method at warmup 40 | Immediate feature NMI | Immediate margin p05 | Immediate preserve | Final feature NMI | Final margin p05 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Embedding-gradient top1 | 1.000 | 10.083 | 1.000 | 1.000 | 9.609 |
| Embedding-gradient direction | 1.000 | 8.801 | 1.000 | 1.000 | 8.040 |
| Route-position control | 0.996 | 9.456 | 0.992 | 0.996 | 8.844 |
| Post-hidden gradient top1 | 0.990 | 8.794 | 0.981 | 0.992 | 8.298 |
| Post-hidden Fisher subspace | 0.910 | -2.516 | 0.863 | 0.925 | -2.956 |
| All-position baseline | 0.876 | -4.399 | 0.799 | 0.899 | -3.725 |

## Signal Localization

![Signal role share](figures/a06_27_gradient_signal_role_share_w40.png)

The signal audit explains why the selector works and what it cannot prove.
Post-hidden gradients place all nonzero mass on the supervised route position.
Embedding gradients place most mass on the route/slot region at warmup 40
(`route_share=0.923`, `slot_share=0.968`, `target_share=0.000`).

Therefore the supported interpretation is narrow: gradients identify the
route-relevant population. The result should not be phrased as direct evidence
that gradients discover semantic features.

## Method Implication

The next signal form should prioritize embedding-gradient hard selection or
embedding-gradient direction grouping. Fisher-only clustering should be kept as
a diagnostic because it raises NMI but does not create positive margins.

The most natural next protocol is a margin-thickened gradient-selector method:
select route-relevant states with embedding-gradient top1 or direction, build
router rows from the selected hidden states, then test row scaling/projection
or refresh schedules that preserve positive margin.

## Claim Boundary

This result is limited to the synthetic uniform no-position one-layer
Transformer plus one-layer MoE bridge. It cannot claim real-DCLM transfer,
semantic expert specialization, common/rare routing, or expert utility.

## Artifacts

- Protocol: `protocol.md`
- Runner: `scripts/run_a06_27_gradient_fisher_route_state_selector.py`
- Full run: `a06_27_gradient_fisher_full_local2gpu_20260705`
- Tables: `tables/condition_aggregate_reinit.csv`,
  `tables/condition_aggregate_final.csv`,
  `tables/selector_diagnostics_aggregate.csv`
- Figures: `figures/a06_27_core_reinit_nmi_margin.png`,
  `figures/a06_27_gradient_signal_role_share_w40.png`
