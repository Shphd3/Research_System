# Detailed: A15_02_E05 q Pseudo-Taxonomy Specificity Control

Primary anchor: [A15_02 coarse/fine semantic variance atlas](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/15_02_layerwise_representation_spectral_atlas_anchor.md)  
Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** determine whether the late-layer increase in background-normalized semantic variance is specific to the registered taxonomy.  
**Hypothesis:** true coarse and fine \(T_q\) are positive and above matched pseudo-taxonomy q95 in both expression splits.  
**Experiment logic:** preserve every child concept and its eight expressions; randomize only the 8-by-8 parent grouping; compare the true late-minus-early statistic with 2,000 matched groupings.  
**Conclusion:** the joint hypothesis fails. Fine passes both splits; coarse fails both.  
**Evidence:** [specificity table](tables/specificity_table.csv), [verdict](provenance/verdict.json), and the primary null-distribution figure below.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| \(z_\ell\) | Current layer's attention write | `self_attn.o_proj` output before residual addition | 4,096-dimensional vector | Isolates the architectural write | New Shannon information or MLP use |
| DCLM background spectrum | Natural-text variation coordinate for one layer | Eigensystem of the frozen E04 DCLM covariance | Ordered eigenvectors/eigenvalues | Supplies a data-dependent background scale | Shared direction identity across layers |
| \(q_{\ell,g,k}\) | Background-normalized class-center variance | Mean \(B_{\ell,g,i}/\max(\lambda_{\ell,i},10^{-6}\lambda_{\ell,1})\) over band \(k\) | Dimensionless | Compares semantic variance to natural variation | Within-class compactness or accuracy |
| Coarse role | Variation between eight parent means | Between-parent variance with denominator 7 | Per direction, then band mean | Tests parent-level grouping | Fine discrimination |
| Fine role | Variation among eight child means inside each parent | Mean within-parent child-mean variance | Per direction, then band mean | Tests conditional child structure | Parent accuracy |
| Pseudo-taxonomy | Matched arbitrary grouping | Permute 64 intact child nodes into 8 groups of 8 | One draw | Removes sample-count and balance explanations | Linguistic validity |
| \(T_q\) | Sustained late-versus-early change | Median \(\log_{10}q\) on blocks 25--35/all bands minus blocks 1--12/all bands | \(\log_{10}\) units | Primary specificity test | A sharp block-25 onset |
| \(J_{25}\) | Local block-25 jump | Median-band \(\log_{10}q_{25}-\log_{10}q_{24}\) | \(\log_{10}\) units | Audits the visual breakpoint | Sustained late behavior |

## 2. Anchor Link And Decision Point

The parent anchor asks where coarse and fine semantic variance appears across depth and spectrum. E04 observed a descriptive late-layer increase, including a visible block-24-to-25 change. E05 tests the strongest immediate rival: the same trajectory may arise for arbitrary balanced groups of the same texts. The result can change only the specificity boundary of \(q\); it cannot promote a functional routing coordinate.

## 3. Protocol Compliance Audit

| Check | Result | Evidence |
| --- | --- | --- |
| All A--G blocks confirmed before execution | Pass | [protocol ledger](protocol.md#17-block-confirmation-ledger-and-review-notes) |
| Cross-block consistency | Pass | Protocol confirmation note |
| Execution scope explicitly approved | Pass | Implementation, smoke, full local analysis, figures, records |
| Approved conditions match implementation | Pass | 64-draw smoke; 2,000-draw full; exact windows, roles, splits, bands, seed |
| Primary metric exists | Pass | [specificity_table.csv](tables/specificity_table.csv) |
| Central figures/tables exist | Pass | Three audited figures and seven curated tables |
| Seed recorded | Pass | PCG64 seed 1701 |
| Known good/bad/confusing cases checked | Pass | Row, assignment, replay, formula, draw-count, numerical, and visual guards |
| Decision criteria applied without subset rescue | Pass | Joint Fail because coarse fails both splits |

## 4. Setup

**Research question:** does the true hierarchy's late-minus-early \(q\) increase exceed that of arbitrary size-matched hierarchies?  
**Data provenance:** exact E04 semantic state cache, dataset identifier inherited from E04, 512 rows forming 64 child nodes with eight expressions each.  
**Split:** templates 0--1 are design; templates 2--3 are confirmation; each child contributes four expressions to each split.  
**Learning task:** none. Labels are used only to form class means and between-class variance.  
**Model:** frozen Qwen3-8B; 36 post-`o_proj`, pre-residual attention writes at the registered readout token.  
**Background:** exact E04 DCLM eigensystem for each layer; 16 contiguous 256-rank bands; eigenvalue floor \(10^{-6}\lambda_{\ell,1}\).  
**Randomization:** one PCG64 seed 1701 generates 2,000 permutations of all 64 child nodes; each permutation is reshaped into eight pseudo parents of eight children. The same draw is shared across layers, roles, and splits.  
**Changed variable:** only the child-to-parent assignment.  
**Held fixed:** texts, child units, group sizes, representation, model, layer, basis, eigenvalues, expression split, metric, and aggregation windows.  
**Optimization/checkpoints:** not applicable.  
**Hardware for analysis:** one local NVIDIA H100; the projection uses PyTorch float32 matmul precision `high` to exactly replay the original E04 RTX-5090/PyTorch-2.8 result; the balanced ANOVA null accumulates in float64.  
**Worker result:** `/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_05_e05_q_pseudotaxonomy_specificity_control/runs/a15-01-05-e05-20260807/full`.

### Computational reuse

The run performs no model forward and no eigendecomposition. It reuses E04 semantic states, row manifest, background means, bases, and eigenvalues. For each layer and split, child means are whitened by the frozen eigenvalues. A balanced one-way ANOVA identity reduces each pseudo grouping to 16 bandwise Gram-matrix sums, avoiding materialization of 2,000 full semantic cubes.

## 5. Metrics And Decision Rules

For role \(g\) and expression split \(s\),

\[
T_{q,g,s}=\operatorname{median}_{\ell\in25:35,k\in1:16}\log_{10}q_{\ell,g,k}
-\operatorname{median}_{\ell\in1:12,k\in1:16}\log_{10}q_{\ell,g,k}.
\]

Each cell passes when the true statistic is positive and above the empirical q95 of 2,000 pseudo-taxonomies. The joint result passes only when coarse and fine pass in both design and confirmation. Empirical one-sided probability is

\[
p_{emp}=\frac{1+\sum_b\mathbf{1}[T_q(P_b)\ge T_q(P_{true})]}{2001}.
\]

The registered secondary statistic \(J_{25}\) has no effect on the primary verdict.

## 6. Main Results

### Decision evidence

| Split | Role | True \(T_q\) | Null median | Null q05 | Null q95 | True minus null median | \(p_{emp}\) | Result |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Design | Coarse | 0.8018 | 0.9129 | 0.8502 | 0.9734 | -0.1111 | 0.9985 | Fail |
| Confirmation | Coarse | 0.8177 | 0.9242 | 0.8681 | 0.9800 | -0.1066 | 0.9990 | Fail |
| Design | Fine | 0.9512 | 0.9115 | 0.9041 | 0.9211 | +0.0397 | 0.0005 | Pass |
| Confirmation | Fine | 0.9701 | 0.9241 | 0.9178 | 0.9312 | +0.0460 | 0.0005 | Pass |

The run is valid and the joint proxy-specificity hypothesis fails. No subset is used to rescue the joint claim.

### Secondary block-25 evidence

| Split | Role | True \(J_{25}\) | Null median | Null q95 | True percentile | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Design | Coarse | 0.6941 | 0.6538 | 0.7089 | 0.8865 | Not above q95 |
| Confirmation | Coarse | 0.7637 | 0.6799 | 0.7320 | 0.9990 | Above q95 in one split only |
| Design | Fine | 0.6139 | 0.6507 | 0.6597 | 0.0000 | Below every pseudo draw |
| Confirmation | Fine | 0.6050 | 0.6843 | 0.6920 | 0.0000 | Below every pseudo draw |

Thus the visually salient block-25 jump is not a replicated fine-taxonomy-specific onset.

### Absolute level versus depth change

True coarse \(q\) is above pseudo coarse \(q\) across the trajectory, while true fine \(q\) is below pseudo fine \(q\). This is expected from the grouping operation: semantically coherent parents concentrate child-mean differences between parents, whereas arbitrary parents mix unrelated children and inflate conditional within-parent child variance. The primary result concerns the **change from early to late**, not these absolute offsets. Fine passes because its true late-minus-early change is larger despite a lower absolute level.

## 7. Visualization Results

### Primary late-minus-early specificity test

![Primary null distributions](figures/figure1_primary_null_distributions.png)

**Purpose:** apply the registered pass/fail rule.  
**Setup:** 2,000 matched pseudo-taxonomies, two roles, two expression splits.  
**Metric/unit:** \(T_q\) in \(\log_{10}\) units.  
**How to read:** red is true, histogram is null, dashed black is q95.  
**Expected if jointly supported:** red lies right of q95 in all four panels.  
**Observed:** both fine panels pass; both coarse panels fail.  
**Take-home:** the coarse-and-fine joint specificity claim is unsupported.  
**Does not prove:** semantic computation onset or usefulness.

### Layerwise true and pseudo trajectories

![Layerwise true and pseudo q](figures/figure2_layerwise_q_curves.png)

**Purpose:** show whether the primary statistic comes from a sustained, readable trajectory.  
**Metric/unit:** median over 16 bands of \(\log_{10}q\).  
**How to read:** red is true; blue is pseudo median with q05--q95 ribbon; vertical dashed line marks the block-24/25 boundary.  
**Observed:** all roles rise non-monotonically late. True coarse is absolutely above pseudo but rises less; true fine is absolutely below pseudo but rises more across the registered windows.  
**Take-home:** absolute taxonomy separation and depth amplification are different quantities.  
**Does not prove:** that ranks identify the same directions across layers.

### Layer-band absolute taxonomy excess

![Layer-band true minus pseudo median](figures/figure3_true_minus_pseudo_heatmaps.png)

**Purpose:** diagnose whether the true-versus-pseudo absolute offset is confined to one spectral band.  
**Metric/unit:** true \(\log_{10}q\) minus pseudo-median \(\log_{10}q\) per layer and band.  
**How to read:** red means true is larger; blue means pseudo is larger; all panels share a symmetric scale.  
**Observed:** coarse excess and fine deficit are broad across bands rather than isolated to a middle/tail band.  
**Take-home:** the control does not reveal a narrow taxonomy-specific spectral location.  
**Does not prove:** bandwise causal use; this figure is not the primary depth-change test.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Result | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| Contract | 512 rows, 64 complete nodes, exact state hashes | Pass | None | Row loss or child-unit breakage |
| First replay attempt | H100 `highest` mode differed from E04 by up to 0.41% in the smallest tail band | Debug fail | Cross-hardware matmul precision mismatch | Treating the first mismatch as semantic drift |
| Precision-matched replay | PyTorch `high` mode reproduces E04 \(q\) to \(6.83\times10^{-14}\) | Pass | None | Basis/table drift |
| 64-draw smoke | Formula error \(1.18\times10^{-7}\); all guards pass | Pass | None | Incorrect balanced grouping formula |
| 2,000-draw full | All layers, roles, splits, and draws complete | Pass | None | Missing-condition explanation |
| Primary decision | Fine 2/2 Pass; coarse 0/2 Pass | Joint Fail | Coarse trajectory not taxonomy-specific | Joint hierarchy-specific depth shift |
| Visual audit | Axes, units, legends, thresholds, and shared scales inspected | Pass | None | Plot-label or clipping explanation |

**Falsified physical prior:** the registered prior that both parent-level and conditional child-level \(q\) depth shifts exceed matched arbitrary groupings.  
**Not falsified:** the weaker observation that \(q\) rises late, or the fine-only depth-trajectory specificity result.  
**Falsified operationalization/proxy:** \(q(z_\ell)\) as a single joint coarse-and-fine marker of hierarchy-specific processing onset.  
**Falsified implementation:** no; all validity guards pass.  
**Falsified metric:** no numerical defect was found, but the metric remains non-functional and does not measure incremental use.  
**Remaining rival:** fine trajectory specificity may reflect changing readability of child contrasts without any downstream use by the MLP or Router.

## 9. Full Experiment Record

- Unit tests: 2/2 passed.
- Registered smoke: layers 1, 25, 36; 64 pseudo-taxonomies; passed.
- Full analysis: 36 layers; 2 roles; 2 expression splits; 16 bands; 2,000 pseudo-taxonomies.
- Runtime: 19.49 seconds for the full local analysis after cache reuse.
- Random generator: NumPy `Generator(PCG64)`, seed 1701.
- Projection precision: PyTorch float32 matmul `high`; ANOVA accumulation float64.
- Primary verdict: `generic_or_unresolved_q_depth_shift`.
- Raw numerical arrays and all 2,000 draw statistics remain on the worker surface; curated decision tables and figures are local to this record.

## 10. Interpretation

The experiment changes the meaning of the earlier block-25 observation. The late \(q\) rise is real as a descriptive property of post-`o_proj` writes, but it is not one replicated coarse-and-fine hierarchy-specific transition. Fine conditional contrasts show an exceptional late-versus-early amplification, while the coarse late increase is weaker than arbitrary regroupings even though the true coarse signal is absolutely stronger throughout.

This indicates that unconditional covariance of \(z_\ell\) is a geometry diagnostic, not yet a measure of how much useful information the layer adds or processes. A processing claim requires a baseline state and a functional consequence of adding the write.

## 11. Claim Boundary

**Supported:** valid fine-only taxonomy-specific late-minus-early \(q\) amplification under the registered matched-grouping control.  
**Unsupported:** one joint hierarchy-specific block-25 onset; coarse trajectory specificity; a narrow middle/tail taxonomy location; information novelty; causal MLP use; Router utility.  
**Scope:** one frozen Qwen3-8B, one 8-by-8 balanced taxonomy, one readout token, post-`o_proj` writes, per-layer local DCLM bases.

## 12. Next Decision

**AI proposal pending researcher confirmation:** formalize one model-native incremental-use audit. At each layer keep the pre-attention local state \(x_{\ell,t}\) fixed and compare the final correct-label negative log-likelihood after the intact sample-specific write \(z_{\ell,t}\) with a matched shuffled or norm-matched write. The primary quantity would be

\[
U_{\ell,g}=\operatorname{NLL}_g(y\mid x_{\ell,t}+z^{shuffle}_{\ell,t})
-\operatorname{NLL}_g(y\mid x_{\ell,t}+z_{\ell,t}),
\]

so positive \(U_{\ell,g}\) means the correct write, rather than generic write magnitude, helps the model's own prediction. First require an untouched capability gate for the coarse and fine label targets; otherwise the result is insufficient and a cross-fitted readout may be used only as an accessibility diagnostic. A15_02_06 has already tested \(\Delta n_\ell\) location and immediate nonlinear response, with the former passing only after parameter-gain weighting and the latter unconfirmed. Therefore another \(\Delta n\) spectral-location plot would not close the missing functional link. No spectral band should be localized until the layerwise functional increment replicates across both expression splits.

## 13. Links And Artifact Map

- **Anchor:** [A15_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/15_02_layerwise_representation_spectral_atlas_anchor.md)
- **Protocol:** [protocol.md](protocol.md)
- **Summary:** [summary.md](summary.md)
- **Worker code:** `/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_05_e05_q_pseudotaxonomy_specificity_control/analyze_pseudotaxonomy.py`
- **Worker tests:** `/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_05_e05_q_pseudotaxonomy_specificity_control/test_pseudotaxonomy.py`
- **Full worker result:** `/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_05_e05_q_pseudotaxonomy_specificity_control/runs/a15-01-05-e05-20260807/full`
- **Smoke result:** `/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_05_e05_q_pseudotaxonomy_specificity_control/runs/a15-01-05-e05-20260807/smoke`
- **Primary table:** [specificity_table.csv](tables/specificity_table.csv)
- **Block-25 table:** [block25_jump.csv](tables/block25_jump.csv)
- **Layerwise table:** [layerwise_q.csv](tables/layerwise_q.csv)
- **Layer-band table:** [layer_band_excess.csv](tables/layer_band_excess.csv)
- **Replay guards:** [replay_validation.csv](tables/replay_validation.csv), [formula_replay.csv](tables/formula_replay.csv)
- **Verdict:** [verdict.json](provenance/verdict.json)
- **Contract validation:** [contract_validation.json](provenance/contract_validation.json)
- **Draw manifest:** [draw_manifest.json](provenance/draw_manifest.json)
- **Run configuration:** [run_config.json](provenance/run_config.json)
- **Visual audit:** [visualization_audit.json](provenance/visualization_audit.json)
- **Artifact hashes:** [artifact_manifest.json](provenance/artifact_manifest.json)
- **Reproduction:** `python analyze_pseudotaxonomy.py --mode full --output <result-dir> --device cuda:0`
- **Remote job/checkpoint:** not applicable; this is local deterministic cache analysis.
