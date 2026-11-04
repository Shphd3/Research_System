派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_05_spectral_semantic_granularity_anchor.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_05_spectral_semantic_granularity_anchor.md)；研究修改仍回到原件。

---

# A15_27_05: Spectral position and semantic granularity

## 1. Problem Definition

In frozen Qwen3-0.6B-Base block27 residual-post representations, do equally sized
high-, middle- and low-variance subspaces differ in coarse domain and within-domain
topic readout, does the latter information add to the head, and which native A22
responses explain the reconstructed part? The parent A15_27 links actual visible
text to representation and CrossCoder responses. R07 already found head and tail
domain readability; R10 established overlapping decoder spectral distributions,
not semantic equivalence. What each band distinguishes remains unresolved.
Support would identify a bounded relative task preference; a contrary pattern
would weaken the coarse-to-fine conjecture; insufficient coverage would limit
this route. MoE design and native causal mechanism are subsequent questions.

R13 extends this owner to native next-token recovery at the same checkpoint/interface: as variance-ordered components are accumulated, do common/format predictions recover earlier, and does this represent semantics beyond frequency/energy? This is an authorized bounded extension, not unknown-T5 replication.

## 2. Physical Priors

Corpus variance, feature occurrence and input-specific response are distinct
quantities. External topic relations need not follow variance rank. A frozen
linear readout measures accessible association, not native model use. The main
rival is that vocabulary, source/format or regularization explains an apparent
granularity preference. These are hypotheses and limitations, not established
coarse-to-fine structure.

R13 prior: mean-only can induce common/format output bias. Native final normalization and fixed-head sensitivity differ from accessibility by a newly trained readout. Token-ID corpus frequency is distinct from CrossCoder feature frequency and semantic granularity.

## 3. Falsifiable Hypotheses

H1: middle/tail versus head readout advantage is larger for each named fine task
than for the coarse task under matched training budgets. Rival: information is
mixed, or head is at least as readable for fine distinctions. H2: equal-dimensional
middle/tail additions improve head readout beyond head extension/random additions.
Rival: no reproducible increment or generic dimension gain. H3: fixed original
readout scores survive native reconstruction and can be described by stable
feature coefficients. Rival: residuals carry substantial task-aligned scores or
feature/text interpretations fail on heldout documents. Each hypothesis is judged
separately; absent evidence for one does not cancel the others.

H4 (R13): under the fixed native output head, common-reference-ID/format predictions may match the original model at smaller cumulative k than other predictions. Rivals are mean/head bias, generic dimension/energy recovery and lexical/context difficulty. Frequency ordering alone cannot establish semantic ordering.

## 4. Mathematical Model

One observation is a real vector h at a prespecified common-token occurrence in
one document's already visible prefix. A fixed orthonormal basis V comes from
pooled centered R04 discovery h, ordered by decreasing covariance eigenvalue
(squared singular value up to sample normalization). Band coordinates are
\(x_B=V_B^T(h-\mu)\). The label is an externally specified domain or topic.
TRAIN-fitted linear logistic readouts minimize balanced empirical log loss with
L2 regularization; DEVELOPMENT selects strength. Balanced accuracy is the mean
of the two class recalls. Primary contrasts compare bands within the same task,
then compare those differences across tasks; absolute task accuracy is not grain.

Native shared z is jointly encoded from 14 layers. In model units reconstruction
is \(\widehat h=b+\sum_f z_f d_f\), where b includes decoder bias and inverse TRAIN
centering and RMS. With residual \(e=h-\widehat h\), any frozen linear score obeys
\(w^T h=w^T b+\sum_f z_f w^T d_f+w^T e\). This is an exact additive accounting,
not a causal or interaction model. Squared individual energies are not additive.

For R13 use h_B=mu+Q Q^T(h-mu), Q=V B for inherited PC-coordinate selectors/rotations; q_B=softmax(W RMSNorm_native(h_B)). Direct identity uses h, separate from all-PC reconstruction. Compare true successor NLL, KL(full||q), entropy, top1/top10 recovery and independent TRAIN reference frequency.

## 5. Computational Realization

Reuse R11's existing 192-token natural documents and native h27/shared-z caches.
Choose one late common-token occurrence per document without inspecting responses;
label only its visible prefix. Freeze two mathematical and two biological topics
from the inherited ontology after discovery-only label/source inspection. Use the
same selected documents for coarse and conditional fine tasks and preserve the
original document-family splits and new-platform evaluation stratum.
R11 heldout has been exposed for earlier work: this is a newly frozen exploratory
evaluation, not pristine independent confirmation.

Compare 64-dimensional head/middle/tail and random subspaces, full h, and equal
128-dimensional head-plus-band controls. Check TRAIN-only standardization against
unstandardized input. Then apply the original fitted projections/readouts to
reconstruction and residual; separately refit residual readouts. Use D-selected
features, native presence/amplitude, independent DCLM occurrence and signed score
contributions; validate text hypotheses and frequency-controlled relations on H.
A15_07's Qwen3-8B layer-innovation analysis is methodological precedent with a
different object and cannot supply this round's results or aligned coordinates.

R13 keeps all37 R12/the evaluation documents and an output-blind175-document/700-natural-position panel. Legacy h failed5090 native replay, so refresh the SAME official weights/hook/fixed text; keep original TRAIN mu/V and all condition/label positions.21 fixed conditions, no training or classifier. Exact contract/provenance in the round Protocol.

## 6. Minimal Falsification Tests

Require full-space readability before assigning absent signal to a band. Use
chance/label permutation, equal dimensions, matched training budgets, source/format
and document-family holdout controls. Document-stratified paired intervals assess
within-task differences; multiplicity is reported. A positive lower interval
supports only the named contrast; a precise nonpositive contrast weakens that
prediction; wide intervals or failed qualification yield insufficient evidence.
For reconstruction report fixed-readout accuracy, score changes, residual score
contribution and overall normalized squared error separately. Text examples cannot
replace prevalence and heldout counterexamples.

R13 guards require native interface, same-shape causal-prefix/cache replay and true identity/full-PC checks before decoding. Compare equal64D bands and equal128D head additions with three orthogonal random additions, report retained variance/energy and document bootstrap. Common-token mass is not itself recovered correct semantics.

## 7. Current Evidence

Prior R07: head16 accuracy98.96%, tail16 90.62%, tail64 97.92% on constructed
math/biology contexts. R10: main433/527 decoder distributions overlap0.9493;
special head bias is not established against finer matching. R04/R07/R10 use the
same pooled two-domain discovery basis, not independent spectral replications.
R09: relative domain-difference residual norms0.5368/0.7214 show that reconstruction
can omit material differences. R11:450 documents and462 original forwards saved;
legacy16 all respond in physics H. These motivate but do not answer this round.
The initial revision recorded NOT RUN. Completed R12 now has96common-token documents(39D/20V/37H);each task uses16D/8Vand fine Hsizes17/18. Head/middle/tail balanced accuracies are94.7/62.3/51.3%for domain,81.9/57.6/58.3%for math fine,and88.9/88.9/77.8%for biology fine. Fine-minus-coarse interactions do not clear Holm4;middle/tail additions have no established gain beyond128Dcontrols. Complete reconstruction retains82.1/79.6/81.2%of fixed mean score contrasts;separately refitted residual readouts reach76.3/75.7/88.9%. Fine strict source/genre/position matching gives only1/3pairs;Hwas exposed. Thus the hierarchy is NOT_ESTABLISHED,and residual omission remains material. These are bounded AI interpretations,not researcher scientific acceptance.

The complete [R12 Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R12_spectral_semantic_granularity_20261031/summary.md) and [Detailed evidence](../../../../../../../../UNAVAILABLE.md) own results. Prior evidence remains separately owned by [R07](../../../../../../../../UNAVAILABLE.md), [R10](../../../../../../../../UNAVAILABLE.md), [R09](../../../../../../../../UNAVAILABLE.md) and [R11 A02](../../../../../../../../UNAVAILABLE.md).

R13 native result:737 positions/180 physical documents,21 frozen conditions, no training. Fresh native replay/causal NLL and all-PC identity errors0. Natural-panel head64 NLL5.901→head2563.914→full2.342; non-format common/other original-top1 recover at64 at30.3%/2.0%. Mean-only already has55.5% whitespace/punctuation mass. Middle/tail addition gains0.427/0.151nat, versus next-head64 gain0.924; middle does not consistently beat random additions. Fixed text shows actual context candidates and accuracy/fidelity reversals. These are exploratory output/frequency observations; coarse-to-fine semantics and mechanism remain Unknown.

2026-11-02 user-authorized native supplement comparesPC1/PC2alone andfirst8/16;onlyPC2/first8are new,panels/headunchanged. Natural grouped recovery: k1:common2.15%,format10.49%,other0.00%; pc2:common6.95%,format3.70%,other0.00%; k8:common9.46%,format27.57%,other0.00%; k16:common14.37%,format26.13%,other0.00%. Common group includes digits,subwords and dollar/equals;not semantic granularity. [supplement](../../../../../../../../UNAVAILABLE.md)

2026-11-02 isolatedbands/tailnative decoding completed:700naturalpositions,11bands,12fixedfullprefixcaseswithcurrentID/zero-andone-basedpositions;312same-tokenother-documentcontrolpositions/158documents. b16_32 NLL9.139; b32_64 NLL9.299; b64_128 NLL8.956; b128_256 NLL8.662; b256_512 NLL8.037; b512_768 NLL8.769; b768_960 NLL9.416; b960_1025 NLL10.203. Nativeisolated-outputplausibility,targetprobabilityandcontextassociationareseparate;isolatedfailuredoesnotestablishstorednoise. [result](../../../../../../../../UNAVAILABLE.md)

## 8. Claim Boundary And Next Decision

Claims cover selected exposed English prefixes, this checkpoint/interface and reference spectrum, R12 readout accessibility and R13 fixed-native-decoder interventions. They do not establish a knowledge ontology, coarse-to-fine semantic hierarchy, causal feature mechanism, learning dynamics or MoE benefit. Execution completion is not scientific acceptance; researcher mechanism judgment and closure remain Unknown.

AI suggestion only: one frequency-matched, same-token minimal context comparison with externally specified object/relation alternatives. No new layer/classifier/semantic experiment is executed under that suggestion. R12's evidence and prior proposal remain in its immutable result record.

[R13 native round extension](../../../../experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/anchor.md) · [Protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/protocol.md) · [complete measurements and raw reading](../../../../experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/summary.md). Completed2026-11-01; R12 preserved.


R14 authorized 1102 round: [task-bound concept specificity](../../../../experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/anchor.md), [protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/protocol.md). Frequency-group deletion is primary; full spectral matrix secondary. Initial state NOT RUN; scientific acceptance Unknown.


### 2026-11-02 R14 recognition update (bounded AI reading)

The researcher fixed task-bound feature-frequency contribution as primary, with all spectral conditions secondary. [R14 Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/summary.md), [Protocol plus amendments](../../../../experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/protocol.md), [report](../../../../experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/report_cn.md) and [raw source entry](../../../../experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/reproduce.md) own the round. Full-candidate native log likelihoods, not new classifiers, define the contrast. A22 shared coefficients still jointly read14selected layers; only original-scale last-layer group contributions are subtracted, retaining residual and biases.

Completed data1.3:48families/288prefixes;36evaluation families,12/domain;167unique conditions+19aliases. Full cue contrast1.539352; low/middle/high deletion1.558407/1.440587/1.152103. High excess over same-count controls0.357905 has simultaneous interval[-0.030736,0.777969]; excess over norm-matched controls0.161457 has95%[-0.171627,0.498732]. No frequency specialization or less-replaceable group is established under both controls and independent-family consistency. This is not evidence that a group contains no information. Full sibling correctness102/144 and both-side correctness31/72also limit ability claims. High deletion harms upper judgments204/216→173/216 and changes overall output distribution. Candidate-bias movement can make answers wrong even when the cue contrast rises; fixed ribosome/lysosome text provides a real example. Reconstruction contrast0.955978 is not a percentage of information retained.

Text-only data repair removed20literal upper-name prefixes, preserving old data/results and recomputing80branches/166positions;2474untouched h/z and every untouched score are exact. The repair changes a local same-count simultaneous positive inference; both old and corrected norm controls remain inconclusive. A false high-response label on inactive counterexample members was corrected with missing eligibility retained. No thresholds/families were selected by success. Actual runtime was existing CPU2threads after unallocated Spot was stopped; weights/measurement unchanged, new native/cache/causal checks passed. No training, H100 or new model. Scientific acceptance and closure remainUnknown.

Exactly one proposed next uncertainty: does extra high-group cue loss remain when overall prediction damage is matched? This is AI_PROPOSAL,NOT_RUN; no new experiment is authorized by completion. Prior readout accessibility, current deletion effects and externally defined concept cues remain distinct evidence layers.


### R15 completed bounded natural-text update (2026-11-02)

R15 covers 600 real web records from 557 hosts, with 300 discovery, 150 development and 150 validation documents and 76,800 sampled positions. Separate pre-norm h and post-norm y reference spectra were fitted on discovery only; the old 60-document math/bio reference is historical. The 128 primary band-energy comparisons establish no qualifying selective association; all four frozen feature interpretations fail validation. The development gate did not trigger confirmation interventions.

Signed quantitative completion A6 followed inspection of the main table and is explicitly exploratory. Recent blank lines and digit contexts share associations with a leading h direction; the strongest candidate is blank lines toward negative index 2 (−0.249 discovery SD; 146 documents and 1,029 pairs), with position/digit sensitivities remaining negative. This is neither fresh confirmation nor a functional partition. Actual blank-line-pair unit output gain is 1.0057 times the isotropic reference, without strong selective amplification. Source cohorts are keyword screens, not discipline gold labels; training-unseen status is not established.

[Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/summary.md), [Chinese report](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/report_cn.md), [frozen protocol and amendments](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/protocol.md), [actual evidence eligibility](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/detailed_cn.md), [raw data and code](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/reproduce.md). The sole next AI proposal is to preregister the signed blank-line metric and replicate on unviewed natural text, distinguishing transferable association from late-metric/context adaptation. It has not been run. CPU two threads, GPU zero, no training; scientific acceptance and closure remain Unknown. Older rounds and their boundaries are preserved.


2026-11-02 user-authorized R16: single-layer head64 projection followed by remaining network across28 Qwen3 Base blocks. Separate all-prefix and target-only scopes; same60 TRAIN documents for each layer PCA, same700/37 evaluation panels. [Round](../../../../../../../../UNAVAILABLE.md), [Protocol](../../../../../../../../UNAVAILABLE.md). Initial NOT RUN; scientific acceptance Unknown.


### R16 completed bounded layerwise intervention (2026-11-02)

[Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/summary.md) and [protocol/amendment](../../../../../../../../UNAVAILABLE.md) own28single-layer head64 interventions, eachwithfull-prefix andtarget-onlyscope, layer-specific PCA fromsame60TRAINdocuments, same700natural/37thepositions. No training. All-prefix/target-only natural overalltop1preservation at1/7/14/21/28:21.00/15.86/16.00/27.29/23.00% vs77.43/78.00/74.71/41.00/23.00%. All-prefixdepthresponse isnonmonotonic; scope matters strongly. Earlypreservation cannot distinguish retained sufficiency from downstreamcontext/compensation. Same64rankrandom references retainonly~6%energy vshead~37–49%,so energy remainsconfounded. Fixed biology/math cases showunchangedcommonfirstchoice despiteactualtargetprobabilityloss. All737unmodifiedh/NLLreproduceR13exactly; tie-orderbugfixedonCPUwithoutchangingprobabilities/groups;legacyheadtop1reproduces737/737. Completedengineeringobservations do notpromote semanticorder, layerimportance, mechanismacceptance orclosure (Unknown).


2026-11-04 user-authorized R16 complementdeletion supplement: [Protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/protocol.md), [round](../../../../experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/anchor.md). Exactsame28PCA/model/737positions,deletehead64retain960,two scopes witholdkeep64comparison. InitialNOT_RUN; scientificacceptanceUnknown.


### R16 complement deletion completed (2026-11-04)

[Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/summary.md) / [中文](../../../../experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/summary_cn.md) ownsame-model/text/28PCAcomplement deletion results;165825new+41272reusedrecords,zeroPCA/training. Current-onlykeep64/delete64preservation at1/14/25/28:77.43/50.71%,74.71/57.43%,34.29/51.43%,23.00/32.57%;relativeadvantage reverses withstage. At28other-nonformatIDpreservation2.00/27.60%,pairedgain25.60pp[17.47,32.93];format/commongainsuncertain.344/700positionsretainneitheroperation. Fixedrelationfragmentsamecanbe supportedbyremaining960,whilepolygons/humans failuresremain. Commonfrequencydoesnotdefinsemanticgrain;rank/energy/context/suffixremainrivals. Originalall28targetstates/outputreplayzeroerror. TheseareboundedAIobservations,notsemanticpartition,intrinsicimportance,knowledgeerasureorfunctioninteraction. Researcheracceptance/closureUnknown.


2026-11-04 user-authorized equal-rank/mean supplement: [round](../../../../../../../../UNAVAILABLE.md), [protocol](../../../../../../../../UNAVAILABLE.md). Same28PCA/model/737positions;16disjoint64-dimensional bands, affine mean-restored versus centered projection without mean, bothscopes. InitialNOT_RUN; no newfit/training. ScientificacceptanceUnknown.


### R16 equal-rank bands and mean control completed (2026-11-04)

[Summary](../../../../../../../../UNAVAILABLE.md) / [中文](../../../../../../../../UNAVAILABLE.md) owns1,403,985unique records and preservedsingleton-repairversions. Withmeanrestoration,head64attains the highest observed retention atall28layers/bothscopes; target-onlyhead with/withoutmean at1/14/25/28:77.43/17.71%,74.71/40.71%,34.29/12.71%,23.00/4.29%. Other-nonformat finalhead retention2.00→5.07%withoutmean while NLLworsens. Thisqualifies collective960-versus64 reasoning: noindividualequallysizedlaterband replaceshead here. Equalrankdoesnotmatchenergy; mean/nativegeometry/past/suffix remainrivals. All737oldreplays exact after5aux-onlyarithmeticrepairs, withmainstatisticsunchanged. BoundedAIreading only; scientificacceptance/granularity/compensationmechanism/closureUnknown.
