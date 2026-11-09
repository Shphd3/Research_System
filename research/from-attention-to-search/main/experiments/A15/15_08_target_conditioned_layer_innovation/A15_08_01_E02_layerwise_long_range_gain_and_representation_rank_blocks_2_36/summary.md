# Summary: A15_08_01_E02 Layerwise Long-Range Gain, Blocks 2--36

Primary Anchor: [A15_08_01 layerwise long-range compositional innovation](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_01_layerwise_long_range_compositional_innovation_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md), Sections 1--16 SHA-256 `ad34982132b948a78998d8afef918349aaecb4dfc165725ea594b15138d6c735`  
Detailed record: [detailed.md](detailed.md)  
Registered verdict: `H2_LC_FAIL_CONTROL_DEGRADATION`

## Conclusion First

E02 does not support the claim that deep attention writes add more usable
long-range compositional information than shallow writes. The registered
necessity-by-distance interaction was larger in deep blocks,
\(T_{depth}=0.006102\) nats/example with paired 95% interval
\([0.004119,0.007669]\), but the absolute remote two-hop gain decreased from the
early to the deep region: \(A_{2F}=-0.011422\)
\([-0.013994,-0.009812]\). This triggers the registered typed Fail.

The positive interaction therefore cannot be read as positive growth of the
target quantity. It can arise from relative changes among the four cells while
the 2F accessibility gain itself becomes smaller. Headroom adjustment remained
positive, but the matched-capacity contrast crossed zero and does not rescue
the claim.

## Decisive Evidence

| Registered quantity | Estimate and paired 95% interval (nats/example) | Role |
| --- | ---: | --- |
| \(T_{depth}\) | +0.006102 [0.004119, 0.007669] | deep interaction exceeds early interaction |
| \(M_D\) | +0.003328 [0.001715, 0.004508] | deep interaction itself is positive |
| \(A_{2F}\) | **-0.011422 [-0.013994, -0.009812]** | typed Fail: absolute remote two-hop gain declines |
| \(T_{depth}^{head}\) | +0.018116 [0.014273, 0.021431] | not explained by linear old-state-loss headroom |
| \(T_{cap}\) | +0.001621 [-0.000873, 0.002821] | matched-capacity separation is unresolved |

Capability, bridge dependency, and all four representation-identity guards
passed. The result is therefore a scientific Fail under the registered
comparison, not an eligibility failure.

![Layerwise accessibility and registered decision metrics](figures/figure_1_layerwise_accessibility.png)

## Descriptive Representation Geometry

The representation spectrum is strongly non-monotonic rather than a single
low-rank-to-high-rank or high-rank-to-low-rank trajectory. On CONFIRMATION,
entropy effective rank ranges from 18.77 directions at block 2 to 350.76 at
block 9, while 80%-variance rank ranges from 10 to 338. Block 25 has
\(r_{eff}=52.04\) and \(r_{80}=36\); block 36 has \(r_{eff}=220.89\) and
\(r_{80}=181\). Because H1-REP had no frozen threshold, these are descriptive
facts only and do not establish or refute a general low-rank hypothesis.

![Representation rank and common-basis energy](figures/figure_2_representation_rank_common_basis.png)

## Claim Boundary And Decision

**Can claim:** in this frozen model/task/token/linear-readout family, the deep
necessity-by-distance interaction is positive but does not correspond to
larger absolute 2F added accessibility; H2-LC fails by its registered
\(A_{2F}\) guard.

**Cannot claim:** deep layers contain less total information, no new
information exists, representation is globally high rank, the model does or
does not natively use the signal, or a Router cannot work.

**Exactly one next decision:** before any Router experiment, decide whether to
replace the interaction-based depth hypothesis with a direct layerwise
absolute-gain question centered on \(G_{\ell,2F}\) and its matched null.
