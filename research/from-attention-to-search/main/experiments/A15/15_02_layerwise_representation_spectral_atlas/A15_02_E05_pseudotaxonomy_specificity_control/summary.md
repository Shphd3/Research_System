# Summary: A15_02_E05 q Pseudo-Taxonomy Specificity Control

Primary anchor: [A15_02 coarse/fine semantic variance atlas](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/15_02_layerwise_representation_spectral_atlas_anchor.md)  
Protocol: [approved protocol](protocol.md)  
Detailed record: [detailed.md](detailed.md)

## Result Snapshot

**Protocol verdict:** `generic_or_unresolved_q_depth_shift` — the registered joint taxonomy-specificity rule failed.

**What we established:** the true hierarchy does not show one shared coarse-and-fine late-layer specificity effect. Fine within-parent variation has a larger late-minus-early increase than 2,000 matched arbitrary groupings in both expression splits. Coarse parent variation instead has a smaller increase than the pseudo-taxonomy median in both splits.

**What the experiment shows:** the descriptive rise in background-normalized between-class variance after block 25 cannot by itself be read as the onset of hierarchy-specific semantic processing. The result separates a fine-role trajectory effect from a more generic coarse grouping depth effect.

**What we do next:** the AI-proposed next decision, pending researcher correction, is to stop treating unconditional variance of the attention write as the final processing quantity and test the write's marginal functional contribution: how much the intact sample-specific write improves the model's held-out correct-label loss relative to a matched shuffled write at the same layer. A capability gate must pass before this can be interpreted.

## Purpose

Test whether the late-layer increase in background-normalized semantic between-class variance, denoted \(q\), depends on the registered 8-by-8 taxonomy rather than occurring for arbitrary balanced groupings of the same 64 intact child concepts.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Attention write | What one attention layer adds to the residual stream | Post-`o_proj`, pre-residual vector \(z_\ell\) | 4,096-dimensional vector | Frozen representation under audit | Information-theoretic novelty or causal usefulness |
| \(q\) | Semantic class-center variation relative to natural background variation | Between-class variance in one DCLM covariance direction divided by that direction's background eigenvalue, then averaged in a 256-direction band | Dimensionless | Removes direction-wise background scale | Accuracy or within-class compactness |
| Pseudo-taxonomy | An arbitrary but size-matched hierarchy | Uniformly permute 64 intact child nodes and partition them into eight groups of eight | One random grouping | Strongest registered rival | A meaningful alternative linguistic taxonomy |
| \(T_q\) | Late-versus-early change in \(q\) | Median \(\log_{10}q\) over blocks 25--35 and all bands minus the corresponding median over blocks 1--12 | \(\log_{10}\) units | Primary statistic | A unique transition at block 25 |

## Exact Setup

- **Data:** the frozen E04 512-record semantic set: 8 parents, 8 children per parent, and 8 expressions per child. Each child and all eight expressions remain intact during randomization.
- **Representation:** all 36 Qwen3-8B post-`o_proj`, pre-residual attention writes at the registered readout token.
- **Background coordinate:** the frozen per-layer E04 DCLM covariance eigensystem, grouped into 16 bands of 256 directions.
- **Changed variable:** assignment of 64 child nodes to eight parent groups.
- **Held fixed:** texts, node size, parent size, model, layers, readout position, representation, DCLM bases, expression splits, metric, and decision windows.
- **Null:** 2,000 pseudo-taxonomies from NumPy PCG64 seed 1701; the same draw is used across layers, roles, and splits.
- **Validity:** E04 \(q\) replay maximum relative error \(6.83\times10^{-14}\); balanced-ANOVA formula error \(1.38\times10^{-7}\); all state hashes, rows, assignments, draw counts, and visual checks passed.
- **Code:** [/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_05_e05_q_pseudotaxonomy_specificity_control/analyze_pseudotaxonomy.py](/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_05_e05_q_pseudotaxonomy_specificity_control/analyze_pseudotaxonomy.py)

## Primary Metric Result

The registered role passes only when the true \(T_q\) is positive and exceeds the pseudo-null 95th percentile in both expression splits.

| Split | Role | True \(T_q\) | Pseudo median | Pseudo q95 | Empirical one-sided \(p\) | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Design | Coarse | 0.802 | 0.913 | 0.973 | 0.9985 | Fail |
| Confirmation | Coarse | 0.818 | 0.924 | 0.980 | 0.9990 | Fail |
| Design | Fine | 0.951 | 0.912 | 0.921 | 0.0005 | Pass |
| Confirmation | Fine | 0.970 | 0.924 | 0.931 | 0.0005 | Pass |

The joint rule fails because both coarse cells fail. This is a valid negative result for the joint proxy-specificity hypothesis, not an insufficient run.

The block-25 jump is also not a shared hierarchy-specific onset. Fine \(J_{25}\) is smaller than every pseudo draw in both splits; coarse exceeds pseudo q95 only in the confirmation split, not in design.

## Key Figure

![True taxonomy late-minus-early change versus matched pseudo-taxonomies](figures/figure1_primary_null_distributions.png)

**What this tests:** whether the observed late-minus-early \(q\) change is exceptional under matched arbitrary parent assignments.  
**Metric and unit:** \(T_q\) in \(\log_{10}\) units.  
**Data and aggregation:** 36 frozen layers, 16 bands, 2,000 intact-child pseudo-taxonomies, separately for two roles and two expression splits.  
**How to read:** red is the true taxonomy; the histogram is the pseudo null; the black dashed line is null q95.  
**Observed:** true fine is beyond q95 in both splits; true coarse lies below almost the entire null in both.  
**Allowed claim:** only the fine role has a taxonomy-specific late-minus-early trajectory under this control.  
**Does not prove:** composition, information creation, MLP use, a cross-layer shared direction, or routing utility.

## Claim Boundary

**Can claim:** for this frozen Qwen3-8B representation and taxonomy, fine within-parent \(q\) grows more from early to late layers than matched arbitrary groupings, while coarse parent \(q\) does not. The prior joint coarse-and-fine specificity claim is unsupported.

**Cannot claim:** block 25 is the onset of semantic computation; \(z_\ell\) contains information absent from the pre-write state; larger \(q\) is better classification; fine semantics occupy one shared spectral direction across layers; or any band should be routed.

## Human Judgment Scaffold

- **Question:** Does the true taxonomy produce a coarse-and-fine late-layer \(q\) increase beyond arbitrary balanced groupings?
- **Direct result:** fine passes in both expression splits; coarse fails in both; the registered joint verdict fails.
- **Updated judgment:** researcher to confirm or correct the AI proposal that \(q(z_\ell)\) should be retained as a write-geometry diagnostic but replaced by a downstream incremental-use metric for the processing-distribution question. A15_02_06 has already measured the actual MLP-input increment \(\Delta n_\ell\) and found stable gain-weighted location but no confirmed nonlinear-use effect, so repeating another \(\Delta n\) location plot is not the missing test.
- **Cannot claim:** hierarchy-specific block-25 onset, information novelty, or Router utility.
- **Exactly one next decision:** decide whether to formalize a layerwise intact-write versus matched-shuffled-write correct-label loss intervention as the next anchor-aligned experiment.
