# Detailed: A15_00_02_E01 Gate Pooled Versus Local Residual Alignment

Primary anchor: [A15_00_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_02_gate_common_residual_preference_anchor.md)  
Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** Determine whether the trained Gate prefers the independently
pooled centered top-64 over equal-rank shard-local residual directions after
input-energy amplification is removed, and whether the native route actually
depends on that geometry.

**Hypothesis:** Pooled directions have higher equal-energy expert-relative Gate
gain and provide more native-winner margin support.

**Experiment logic:** Compare rank-64 pooled and local bases with the same Gate,
tokens, and evaluation documents; add a singular-value-preserving orientation
null and an equal-rank native-route ablation.

**Conclusion:** Both decision gates pass at the model level in decommon 80k and
replicate at 40k. With A15_00_01's stability Pass, the joint conclusion is that
the Gate prefers a cross-document-transferable centered component over a less
transferable local residual.

**Evidence:** Decommon 80k pooled/local equal-energy gain ratio is 3.08× and
pooled-minus-local margin support is 2.061 logit/token. Decommon 40k is 2.83×
and 1.998. LB shows the same direction with stronger gain ratios.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| expert-relative Gate | Gate after removing the row shared by every expert | \(\bar W=C_EW\) | Gate weight | common logit shifts cannot change routing | function |
| equal-energy gain \(G\) | expert-score power for one unit of input energy per direction | \(\|\bar WU\|_F^2/64\) | logit²/activation² | removes covariance eigenvalue amplification | actual token frequency |
| \(B_{P:L}\) | pooled gain relative to median local gain | \(\log(G_P/\mathrm{median}_sG_{L_s})\) | natural-log ratio | primary geometry metric | route usefulness |
| orientation null | same nonzero Gate singular values with random right-singular orientation | 256 Haar rotations | null distribution | excludes Gate anisotropy alone | training cause |
| margin support | native winner's margin lost when a subspace is removed | \(m(z)-m(z^{(-U)})\) | logit/token | checks current route dependence | correct expert choice |
| flip | fraction of tokens changing top-1 expert after ablation | probability | token fraction | auxiliary behavior | benefit |

## 2. Anchor Link And Decision Point

A15_00_01 owns whether the pooled candidate is actually transferable. This
experiment owns only Gate preference and native use. Joint naming is permitted
only because both experiments pass.

## 3. Protocol Compliance Audit

- all decision-bearing conditions and hard guards match actual conditions:
  **yes**;
- documented execution amendment: only 40k/80k are retained and the
  descriptive fine-gain localization profile was not executed or used;
- primary gain and margin-support metrics exist: **yes**;
- singular-value-preserving orientation null exists: **yes**, 256 draws;
- central figure/table exists: **yes**;
- paired basis/document bootstrap exists: **yes**, 2,000 replicates;
- checkpoint crossing exists: **yes**, amended \(2\times2\) 40k/80k table;
- known good/bad/confusing cases reviewed: **yes**;
- result criteria applied without a practical-effect threshold: **yes**.

Existing 30k point-diagnostic caches do not enter the evidence path.

## 4. Setup

**Data and split:** Shared with A15_00_01: 640 disjoint held-out DCLM documents,
128 for the pooled basis and eight 32-fit/32-evaluation confirmation shards.

**Models:** LB and decommon 12-layer, hidden-size-768, 8-expert, top-1 models.

**Retained checkpoints:** 40k and 80k.

**Representation:** Direct Gate-effective input.

**Conditions:** pooled centered top-64 versus eight local residual-64 bases
after the independently pooled top-64 is removed.

**Held fixed:** Gate, layer, tokens, document mapping, rank, centering, native
logits, expert order, and ablation form.

**Training/update:** None.

**Seeds/controls:** Seed 20260731; 256 Gate-orientation nulls, full/complement
Haar controls inherited from A15_00_01, wrong-layer +6, and 2,000 paired
basis/document bootstrap replicates.

## 5. Metrics And Decision Rules

\[
G_{\ell,U}=\frac{\|C_EW_\ell U\|_F^2}{64},
\qquad
B_{\ell,P:L}
=\log\frac{G_{\ell,P}}{\operatorname{median}_sG_{\ell,L_s}}.
\]

\(B>0\) means the Gate gives equal-energy pooled directions more squared
expert-relative gain. The observed model median must also exceed the
singular-value-preserving orientation-null q95.

For native use:

\[
\Delta D_{\ell,P:L}
=D_{\ell,P}-\operatorname{median}_sD_{\ell,L_s},
\]

where \(D\) is native-winner margin lost after equal-rank removal.

Registered Pass requires decommon 80k lower bounds above zero for both \(B\) and
\(\Delta D\), observed \(B\) above orientation-null q95, and decommon 40k point
estimates with the same sign.

## 6. Main Results

### Decision evidence

| Lineage | Step | \(B\) | \(\exp(B)\) | \(B\) 95% CI | \(\Delta D\) | \(\Delta D\) 95% CI | Flip difference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LB | 40k | 1.370 | 3.94× | [1.308, 1.434] | 1.873 | [1.857, 1.919] | 0.669 |
| LB | 80k | 1.516 | 4.55× | [1.459, 1.594] | 1.953 | [1.931, 1.994] | 0.681 |
| decommon | 40k | 1.039 | 2.83× | [0.970, 1.120] | 1.998 | [1.948, 2.046] | 0.592 |
| decommon | 80k | 1.125 | 3.08× | [1.040, 1.206] | 2.061 | [2.011, 2.120] | 0.594 |

Model-median orientation-null q95 is about 0.06, far below observed \(B\).

### Layer coverage

- LB: \(B\) exceeds the layer-specific orientation q95 in 12/12 layers at both
  checkpoints; margin difference is positive in 12/12.
- Decommon: \(B\) exceeds q95 in 11/12 layers at both checkpoints; layer 12 has
  \(B\le0\). Margin difference remains positive in 12/12.
- The conclusion is therefore model-level and has a documented decommon
  layer-12 exception.

### Checkpoint crossing

| Lineage | Gate step | Basis step | Median \(B\) |
| --- | ---: | ---: | ---: |
| LB | 40k | 40k | 1.370 |
| LB | 40k | 80k | 1.513 |
| LB | 80k | 40k | 1.369 |
| LB | 80k | 80k | 1.516 |
| decommon | 40k | 40k | 1.039 |
| decommon | 40k | 80k | 1.114 |
| decommon | 80k | 40k | 1.018 |
| decommon | 80k | 80k | 1.125 |

The crossing shows persistence under fixed Gate or fixed basis but is not an
online-gradient decomposition.

### Controls

- Same-layer pooled gain exceeds the wrong-layer (+6) basis in every retained
  layer; minimum log same/wrong is 0.584.
- Gate SVD reconstruction relative error is at most about \(2.2\times10^{-6}\).
- All shared object and route-replay guards pass.
- Raw pooled response is much larger than local response, but the verdict does
  not use raw response alone.

## 7. Visualization Results

### Equal-energy preference and native-route dependence

![Pooled versus local Gate preference and use](figures/pooled_vs_local_gate_preference_and_use.png)

**Purpose:** Jointly show weight geometry and actual native-route dependence.

**Setup:** Same Gate and held-out target tokens; pooled/local rank 64; paired
basis/document bootstrap.

**Metric/unit:** Left, \(B\) in natural-log squared-gain ratio. Right,
pooled-minus-local native margin support in logit/token.

**How to read:** Values above zero favor pooled. A left-only effect would be
alignment without route use; both columns above zero satisfy the two-gate Pass.

**Observed:** Both columns are positive at the model level in both lineages and
checkpoints. Decommon layer 12 is the sole layerwise \(B\) exception.

**Take-home:** The trained Gate is not merely capable of reading the pooled
space; the native route relies on it more than on a same-rank local residual.

**Remaining uncertainty:** The native winner may still be functionally
suboptimal.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Verdict | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| S0 shared object | hashes, Gate shapes, token identity | passed | none | coordinate mismatch |
| S1 metric implementation | unit tests, right-singular known good, SVD replay | passed | none | broken \(G/B\) |
| S2 endpoint geometry | \(B>0\), above orientation q95 | passed model-level | decommon layer-12 exception | energy-only and arbitrary anisotropy |
| S3 native use | \(\Delta D>0\) and flip difference >0 | passed | none | geometry with no current route effect |
| S4 crossing | 40k/80k \(2\times2\) table | descriptive | no dense trajectory | simple endpoint-only artifact |
| S5 joint naming | A15_00_01 Pass plus this Pass | passed | none | unsupported “stable” label |

**Falsified rival:** raw input energy alone explains pooled dominance.

**Falsified rival:** any Gate orientation with the same singular values would
produce the observed pooled/local ratio.

**Remaining rivals:** the pooled component may be useful shared structure or an
easy-to-learn nuisance; current route dependence cannot distinguish them.

## 9. Full Experiment Record

The experiment reused A15_00_01's frozen endpoint caches and did no additional
model forward pass. Gain, orientation null, wrong-layer, route ablation, and
checkpoint crossing were computed from the same actual Gate inputs and weights.

The paired bootstrap uses the same 2,000 resampled document indices as the
stability experiment. GPU covariance aggregation plus CPU-parallel exact
top-64 eigensolvers were validated against the original GPU formula in every
layer. All retained endpoint arrays have shape 2,000×12 and contain no NaN or
Inf.

No remote or training job was submitted.

## 10. Interpretation

Subtracting the mean changes the DC contribution and the training path, but it
does not erase stable centered covariance structure. The Gate's equal-energy
preference shows that pooled dominance is encoded in Gate orientation, not
only in larger input eigenvalues. The route ablation shows that this orientation
participates in actual decisions. Decommon reduces the gain ratio relative to
LB but does not reverse it at the model level.

## 11. Claim Boundary

Established: model-level Gate preference and native margin dependence for the
cross-document-transferable pooled component at 40k/80k.

Not established: semantics, expert compatibility, validation benefit,
center-only causality, or online optimization dynamics. Route flip is a behavior
change, not a utility metric.

## 12. Next Decision

Decide whether to formalize a matched training intervention in which the
residual coordinate is explicitly stabilized across batches, with a
shard-local residual and matched random subspace as controls.

## 13. Links And Artifact Map

- anchor: [A15_00_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_02_gate_common_residual_preference_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- central figure: [PNG](figures/pooled_vs_local_gate_preference_and_use.png)
- tables: [model summary](tables/model_summary.csv), [layer metrics](tables/layer_metrics.csv), [route metrics](tables/route_metrics.csv), [orientation null](tables/orientation_null_model.csv), [checkpoint crossing](tables/checkpoint_crossing.csv), [wrong layer](tables/wrong_layer.csv), [guards](tables/hard_guards.csv)
- historical code workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit` (not present in the current checkout)
- result directory: `analysis: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit/runs/a15_00_02_03/analysis`
- key code: `core.py: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit/core.py`, `analyze.py: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit/analyze.py`, `bootstrap_hybrid.py: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit/bootstrap_hybrid.py`
- remote job ID: none
