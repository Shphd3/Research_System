# A15_02_04_E01 Summary: Compositional Attention-Write Spectral Atlas

## Verdict

The registered verdict is **`insufficient_capability`**. The experiment therefore does not assign a scientific Pass or Fail to compositional rank redistribution.

In the primary isolated post-`o_proj` attention write, the late-minus-early increase of the D2-minus-D0 local rank-centroid gap is

\[
T_{\mathrm{rank,post}}=0.00276,
\]

equivalent to 11.3 of 4096 within-layer ranks. Its world-bootstrap 95% interval is \([-0.00269,0.01229]\) and it is below the paired condition-swap q95 of 0.00792. Thus the post site shows no positive registered rank-shift diagnostic even before mandatory gates are applied. Composition-relative discriminability also moves in the wrong direction: \(T_D=-0.547\), 95% interval \([-0.933,-0.222]\).

The pre-`o_proj` concatenated-head diagnostic is positive (\(T_{\mathrm{rank,pre}}=0.02409\), 98.7 ranks, interval \([0.00189,0.02811]\), null q95 0.01393), but it cannot be interpreted as evidence: capability fails and early cross-template semantic covariance is below the reliability floor. The isolated post site additionally fails the node-position guard.

The narrow knowledge update is:

> “Deeper layers encode more complex information” does not logically imply that composition variance must move toward the tail. The valid cross-layer observable is a change in the distribution over each layer's own covariance-rank percentiles, not movement of the same eigenvector. In this controlled task, the primary post-`o_proj` diagnostic does not show that redistribution, while the task interface is too weakly solved to adjudicate the general hypothesis.

![Decisive rank redistribution and failed gates](figures/figure1_decisive_rank_redistribution.png)

## Data And Capability

Each frozen world contains five single-token entities and four spatial-relation edges. The same four facts define a seven-node tree: four one-edge leaves (D0), two two-edge internal nodes (D1), and one four-edge root (D2). Every prompt presents all four facts; only the queried endpoints change. A frozen Latin schedule selects one leaf and one internal node per world, plus the root, so the primary D0/D1/D2 comparison has equal world count without fixing depth to one node position. All seven nodes are also audited separately.

The corpus has 256 worlds, four paraphrase templates, eight balanced compass answers, 7,168 all-node core prompts, 3,072 primary prompts, 768 same-token required-edge counterfactuals, and 768 query-binding reversals. Core prompt length is fixed within template at 160, 166, 167, or 160 tokens. The primary confirmation split has 512 records per depth.

Registered eight-way accuracy is 26.2% for D0, 22.7% for D1, and 23.0% for D2, versus required thresholds 70%, 55%, and 40%; every Wilson lower bound must also exceed 25%, but the three values are 22.6%, 19.2%, and 19.6%. Required-edge counterfactual log-odds shifts are positive at all depths (bootstrap lower bounds 1.483, 0.490, and 0.365), showing that predictions respond to the required facts, but not that the model reliably executes the requested composition.

## Representation And Metric

The frozen model is Qwen3-8B (36 blocks, hidden size 4096, 32 heads of width 128). At the final `Answer:` colon the experiment captures:

1. the 4096-dimensional concatenation of all head outputs immediately before `o_proj`;
2. the direct 4096-dimensional `o_proj` output before residual addition.

No residual stream, MLP state, SAE feature, parameter spectrum, learned probe, or model update is used. For every layer and site, an independent 65,536-token DCLM activation covariance defines a fresh local eigenspace. The 4096 local ranks are grouped into 16 equal bands of 256 directions. \(V\) is total between-answer-class variance; \(D=B/W\) is between-class variance divided by within-class world/template variation; \(\rho^{(16)}\) is the normalized centroid of semantic variance over the 16 local rank bands. \(V\) and cross-template covariance decide whether the signal is reliable; \(\rho\) decides location only after that gate passes.

![Scale and location audit](figures/figure2_scale_location_audit.png)

## Spectral And Node Diagnostics

Early blocks 1--12 have negative cross-template covariance estimates for both D0 and D2 at both sites, with zero of 12 early blocks positive. Late blocks contain positive signal, but the registered location contrast requires a reliable early baseline. Post node substitutions preserve the positive primary sign for only one of four leaves; pre preserves it for all four. Consequently the apparently positive pre trajectory is a boundary diagnostic, not evidence for the hypothesis.

The band maps show descriptive late-layer changes, but they cannot rescue a failed scale/reliability gate. They also show that raw variance scale and semantic-to-nuisance discriminability differ strongly by hierarchy level; normalized rank location must not be compared without those companion quantities.

![Layer-by-band maps](figures/figure3_layer_band_heatmaps.png)

![Seven-node hierarchy audit](figures/figure5_seven_node_hierarchy_heatmaps.png)

## Boundary And Next Decision

This run establishes neither “variance shifts to the tail” nor its negation in general. It establishes that the registered post-`o_proj` effect is absent in this task diagnostic and that the current prompt/model capability prevents a valid general composition-spectrum verdict. It does not track one direction across layers, prove where composition is computed, identify SAE features as nodes, or test routing utility.

The one next decision is whether to repair the behavioral interface while preserving the frozen seven-node world manifest and spectral protocol. A repair is eligible for a new confirmatory run only if a held-out pre-spectral capability screen reaches D0/D1/D2 accuracy of at least 70%/55%/40%, all Wilson lower bounds exceed 25%, and the early D0/D2 cross-template covariance lower bounds are positive. No spectral statistic from a repair candidate may be inspected before those gates pass.
