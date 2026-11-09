# A15_27_08: Cross-frequency source advantage

## 1. Problem Definition

At equal member and fitting budgets, does a cross-frequency combination beat both high-only and middle/low-only sources?

## 2. Physical Priors

A CrossCoder atom is an observation proxy for an unknown true feature. Textual containment does not entail dictionary-member containment. Wording, total scale, source and sampling are live rivals.

## 3. Falsifiable Hypotheses

High and middle/low atoms provide complementary fine-concept information: mixed J improves over both H and M.

## 4. Mathematical Model

Frozen official Qwen3-0.6B-Base (28 blocks, width1024); A22 jointly encodes layers1,3,...,27 into16384 shared atoms. Observe the last token of the fixed pre-answer suffix. Raw last-block reconstruction is bias + sum z_i D_i, with the residual retained. Only CPU L2 logistic probes fit on discovery; development selects regularization. Constructed matrix invertibility labels are globally consistent; coarse-only is Unknown. Frequency is estimated in300 natural discovery documents, not the semantic panel.

For K=16, J uses 8 high+4 middle+4 low; H uses16 high; M uses8 middle+8 low. All use the same discovery effect ranking and development regularization budget. Choose largest feasible K from16,12,8 before comparisons.


D1 native observation model: two independent block27SAEs (30000/ReLU-Top32), attention o_proj output before residual addition and actual MLP input after residual addition/RMSNorm. Own encoders/decoders, frequency boundaries and C/F/state IDs. A22joint14layer CC remains a separate residual-post reference. Use u=z times own decoder norm; no cross-dictionary atom correspondence.

## 5. Computational Realization

Use384 constructed rows:48 matrix families times three conditions times two wordings, plus96 nonmatrix controls. Keep24/12/12 families and related theorem groups within splits; the group split is6/3/3. Reuse600 natural documents with300/150/150 splits. Follow the exact [frozen Protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/H3/protocol.md) and [execution amendments](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/amendments.md).

## 6. Minimal Falsification Tests

Both LL(H)-LL(J) and LL(M)-LL(J) need positive simultaneous 95 percent lower limits (two comparisons). Winning only one does not establish the full positive hypothesis.

On2026-11-03 the researcher explicitly started R17_D1. Retain this original hypothesis; retest separately at native final Attention-output and MLP-input SAE sites using their own dictionaries, activation rules and natural frequencies. Keep oldCC separate. Corrected old discovery/development fit;24fresh families/288main rows plus48one-factor rows are locked test only. Every correction enters all affected H1-H4 tests with original results and recalculation scope retained.

[D1 protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/protocol.md)

## 7. Current Evidence

Execution facts and AI interpretation are owned by [the route Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/H3/summary.md) and [Detailed](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/detailed.md). The attached v0.2 original is fingerprinted, and notation-corrected analyses reuse exposed holdout. Scientific acceptance remains Unknown. These links do not rewrite the frozen hypothesis.


D1 completed bounded computation2026-11-03: H3 neither nativeSAE meets both equal-budget advantages; no complementarity inference from classification alone. [Current D1 synthesis](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary.md) / [中文](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary_cn.md). Two nativeSAE routes and independent CC reference each retain originalhypothesis, before-input old48, corrected-old48 and locked-fresh192 results. Original results are not overwritten. AI verdict is evidence-limited; researcher scientific acceptance and question closure remain Unknown.

## 8. Claim Boundary And Next Decision

Scope is static correspondence/readability in this frozen model, dictionary and panel. The next scientific decision is Unknown, pending researcher review; labelled AI hypothesis-update suggestions are in the Summary. Training benefit, native causal use and router utility require separate evidence and authorization.
