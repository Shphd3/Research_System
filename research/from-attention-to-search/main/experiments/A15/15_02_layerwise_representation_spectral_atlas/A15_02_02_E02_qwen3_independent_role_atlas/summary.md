---
experiment_id: A15_02_02_E02_qwen3_independent_role_atlas
status: completed
verdict: pass_layer_specific_role_selectivity
date: 2026-08-02
---

# Layerwise spectral atlas of real semantic hierarchy in Qwen3-8B

## Conclusion

**The same concept exhibits different covariance-spectrum selectivity when it acts as a parent versus a child, but Qwen3-8B does not implement a depth-invariant parent=head, child=tail map.**

Raw energy is the squared projection of a target-token state onto a covariance direction and therefore retains the ordinary background variance of that direction. Whitened energy divides raw energy by the independently estimated background eigenvalue, measuring role selectivity relative to ordinary variation. Parent-minus-child is positive when the same target concept is stronger in its parent role.

The head contrast changes sign with depth: the mean paired whitened parent/child ratio is 0.961 at block 10, 1.080 at block 29, and 0.915 at block 36. The supported claim is therefore a layer-specific role atlas, not a universal hierarchy-to-rank assignment.

## Design

The frozen local `/data/share/Qwen3-8B` snapshot was hooked at the embedding output and every one of its 36 decoder-block residual outputs. Each layer's covariance basis was fit on 128 independent DCLM documents (65,536 tokens), not on the hierarchy templates. The inherited 32 three-level academic chains were rendered with four templates. Each middle concept appeared at the identical token ids, absolute position, and sequence length while acting once as a child and once as a parent.

The 4,096 covariance directions were sorted by decreasing eigenvalue. Fine resolution used 12 equal-rank bands; coarse resolution used H=first \(1/12\), M=next \(4/12\), and T=remaining \(7/12\). All band quantities are per-direction means.

## Decisive results

| Layer, head band | Parent whitened | Child whitened | Paired parent/child ratio | Reading |
| --- | ---: | ---: | ---: | --- |
| block 10 | 1.135 | 1.180 | 0.961 | child role is more head-selective; stable |
| block 29 | 0.625 | 0.578 | 1.080 | parent role is more head-selective; stable |
| block 35 | 0.369 | 0.376 | 0.982 | not distinguishable from zero |
| block 36 | 0.413 | 0.452 | 0.915 | local child-head effect; not a terminal-only reversal |

Ten layers in blocks 5--19 stably favor the child role in the whitened head, whereas all eight blocks 25--32 stably favor the parent role. At block 36 the child role is stronger in H while the parent role remains stronger in M/T, indicating terminal spectral redistribution rather than a monotone abstraction axis.

![Per-direction raw and whitened profiles](figures/figure1_direction_projection_curves.png)

![Layer by band by role heatmaps](figures/figure2_layer_band_role_heatmaps.png)

![Layerwise parent-minus-child trajectories](figures/figure3_layer_role_difference_trajectories.png)

## Validity and verdict

All 128 pairs passed exact target-token, span, absolute-position, length, and relation-before-target guards. Hidden-state replay error was zero. The maximum FP64 covariance reconstruction error was \(8.80\times10^{-15}\) and maximum projection-energy error was \(1.69\times10^{-6}\). Split-half H/M/T stability passed at all 37 representation sites, with minimum normalized excess 0.285. Inference used 32-chain paired bootstrap, label-swap permutation, BH-FDR, template and chain-direction requirements, adjacent-layer replication, and eigenvalue-floor/effective-rank sensitivity.

- **Pass:** layer-specific whitened parent/child spectrum selectivity exists in this Qwen3-8B snapshot.
- **Fail:** parents are uniformly more head-aligned than children.
- **Fail:** only the final block reverses the preceding trend.
- **Insufficient:** external validity across models, languages, calibration corpora, and ontology families.

The result does not show that covariance rank causes hierarchical semantics, that deeper layers perform compositional computation, or that any band should route experts or improve training.

The only next decision is whether to reproduce the early/intermediate child-head phase and late parent-head phase under an independent model or independent natural-corpus basis before promoting any layer-band cell to a functional candidate.

See [detailed.md](detailed.md), [band_role_summary.csv](tables/band_role_summary.csv), and the [complete actual semantic sequences](provenance/actual_semantic_text_sequences.json).
