派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_07_conditional_relative_strength_anchor.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_07_conditional_relative_strength_anchor.md)；研究修改仍回到原件。

---

# A15_27_07: Relative strength on fixed members

## 1. Problem Definition

Does relative strength on H1-fixed C add fine-label readability beyond binary support and total strength?

## 2. Physical Priors

A CrossCoder atom is an observation proxy for an unknown true feature. Textual containment does not entail dictionary-member containment. Wording, total scale, source and sampling are live rivals.

## 3. Falsifiable Hypotheses

Adding normalized per-member strength q to binary support b and total norm r improves heldout log loss across wordings.

## 4. Mathematical Model

Frozen official Qwen3-0.6B-Base (28 blocks, width1024); A22 jointly encodes layers1,3,...,27 into16384 shared atoms. Observe the last token of the fixed pre-answer suffix. Raw last-block reconstruction is bias + sum z_i D_i, with the residual retained. Only CPU L2 logistic probes fit on discovery; development selects regularization. Constructed matrix invertibility labels are globally consistent; coarse-only is Unknown. Frequency is estimated in300 natural discovery documents, not the semantic panel.

For last-layer raw decoder norm d_i, use u_i=z_i d_i, r=L2 norm(u), q=u/(r+1e-12), b_i=1(z_i>0). Compare [b,r] to [q,b,r]. C is not reselected on fine labels. Same-support pairs are a separately reported subset.


D1 native observation model: two independent block27SAEs (30000/ReLU-Top32), attention o_proj output before residual addition and actual MLP input after residual addition/RMSNorm. Own encoders/decoders, frequency boundaries and C/F/state IDs. A22joint14layer CC remains a separate residual-post reference. Use u=z times own decoder norm; no cross-dictionary atom correspondence.

## 5. Computational Realization

Use384 constructed rows:48 matrix families times three conditions times two wordings, plus96 nonmatrix controls. Keep24/12/12 families and related theorem groups within splits; the group split is6/3/3. Reuse600 natural documents with300/150/150 splits. Follow the exact [frozen Protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/H2/protocol.md) and [execution amendments](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/amendments.md).

### Researcher-activated natural-language hierarchy round, 2026-11-04

Purpose: inspect richer natural-text differences through SAE member combinations: animal→cat/dog and vehicle→car/bicycle, including cross-domain comparisons. The current user authorizes the complete design, execution, checks, bounded conclusion update and package. Frozen matrix hypotheses and S02–S05 remain intact. Round H1 predicts reproducible shared/recruited/lost-member associations; round H2 predicts reproducible relative-strength combinations among common members. These observable claims do not replace the older incremental-information or functional hypotheses.

Live rivals are explicit-word copying, synonym/property cues, template/suffix/position, Top32 competition, total scale, reconstruction limits and selection/small-sample effects. Observe two independent native 30000-coordinate Top32 dictionaries at the same final Description: colon. Sixteen families per domain share sixteen frame clusters; eight discovery/eight heldout, three wordings and chair/stone negatives. Distinguish per-pair common supports from discovery-fixed lists; relative q is raw z on the exact fixed list divided by its L2 norm, undefined at zero. No cross-dictionary ID correspondence.

Minimal falsifiers: heldout within/cross-domain overlap, frozen common-list joint relative differences, and synonym/property replication. Explicit-only correspondence is local; adequate but contrary comparisons do not support the tested prediction; failed behavior or support eligibility yields insufficient evidence. Anticipated update concerns category/wording dependence, not universal hierarchy or semantic directions. H3/H4 and router training remain parked. Researcher acceptance and closure remain Unknown.

Current round: completed bounded S06; scientific acceptance Unknown. The [Protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/protocol.md) owns exact frozen computations and decision rules.

### S07 intervention supplement, authorized2026-11-04

After completed/saved S06, the researcher authorizes temporary deletion and relative-pattern edits on discovery-frozen nativeSAE combinations. Inject original h plus decoder linear delta, retaining reconstruction residual. Compare frozen count/frequency/intensity controls and measured norm controls, then native full-candidate scores, vocabulary ranks/distributions and offdomain effects on original heldout families. This tests local functional sensitivity, not uniqueness or a concept conversion. [Exact S07 Protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S07_feature_interventions_1104/protocol.md). NOT RUN at scope freeze; scientific acceptanceUnknown.

## 6. Minimal Falsification Tests

One paired heldout loss contrast with a 95 percent family interval; report theorem-cluster sensitivity and both wordings. A sign that fails across wordings limits content interpretation.

On2026-11-03 the researcher explicitly started R17_D1. Retain this original hypothesis; retest separately at native final Attention-output and MLP-input SAE sites using their own dictionaries, activation rules and natural frequencies. Keep oldCC separate. Corrected old discovery/development fit;24fresh families/288main rows plus48one-factor rows are locked test only. Every correction enters all affected H1-H4 tests with original results and recalculation scope retained.

[D1 protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/protocol.md)

## 7. Current Evidence

Execution facts and AI interpretation are owned by [the route Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/H2/summary.md) and [Detailed](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/detailed.md). The attached v0.2 original is fingerprinted, and notation-corrected analyses reuse exposed holdout. Scientific acceptance remains Unknown. These links do not rewrite the frozen hypothesis.


D1 completed bounded computation2026-11-03: H2 no-answer relative-strength gains−0.28474/−0.01238; stable cross-cue claim not supported. [Current D1 synthesis](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary.md) / [中文](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary_cn.md). Two nativeSAE routes and independent CC reference each retain originalhypothesis, before-input old48, corrected-old48 and locked-fresh192 results. Original results are not overwritten. AI verdict is evidence-limited; researcher scientific acceptance and question closure remain Unknown.

### S06 bounded result evidence, 2026-11-04

Completed384prefixes, two separate SAEs, sixteen frame clusters with fixed8/8split, native behavior, all H1/H2 and wording controls, and independent numerical replay. ATTN_SAE/vehicle: estimate=0.027506352770407007, n=8/8, Holm p=0.015625; ATTN_SAE/animal: estimate=0.040139372458710784, n=8/8, Holm p=0.0234375; MLPIN_SAE/animal: estimate=0.00478142999113622, n=7/8, Holm p=0.0234375; MLPIN_SAE/vehicle: estimate=0.05304508942780347, n=5/8, Holm p=0.03125. These are local activation-coordinate statistics; [Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/summary.md) owns candidate replication, counterexamples, cross-wording eligibility and bounded AI verdicts. H1 overlap is a subprediction, not a substitute for member events; H2 ineligible pairs remain ineligible. Original candidates and S02–S05 bytes preserved. Task completion does not change researcher acceptance, mechanism judgment or closure: Unknown.

### S07 completed local intervention evidence, 2026-11-04

S06files preserved;96original heldout prefixes,14976temporary edits. Attention animalalpha.5shows a.00623nat margin-loss excess over same-member norm-matched shuffle,95%family interval[.00135,.01340],8families,Holm p=.03125, while all16texts remain correct. Large common deletions often increase correct margins and broadly change other-domain distributions; complete deletion matching fails. Vehicle opposite-pattern prediction is unsupported or support-ineligible. This identifies bounded decoder-direction sensitivity, not unique natural mechanisms or concept conversion. [S07 Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S07_feature_interventions_1104/summary.md) owns all comparisons and AI operational verdicts. Researcher acceptance/closure remain Unknown.

S07posthoc control audit: a fixed-norm two-member Attention-vehicle list has one angular degree of freedom;6/16target/shuffle perturbations nearly coincide and10/16nearly oppose. This bounds the chosen-direction contrast, not arbitrary independent combination controls; category differences may reflect control sensitivity. Primary statistics and selection unchanged.

## 8. Claim Boundary And Next Decision

Scope is static correspondence/readability in this frozen model, dictionary and panel. The next scientific decision is Unknown, pending researcher review; labelled AI hypothesis-update suggestions are in the Summary. Training benefit, native causal use and router utility require separate evidence and authorization.
