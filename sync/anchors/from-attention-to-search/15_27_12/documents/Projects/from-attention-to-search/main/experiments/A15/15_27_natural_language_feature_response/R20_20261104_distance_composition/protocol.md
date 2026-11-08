派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/protocol.md)；研究修改仍回到原件。

---

# Protocol: R20 distance and answer-position combinations

## 0. Approval Snapshot

APPROVED_FOR_BOUNDED_LOCAL_REANALYSIS_AND_CONTROLS, 2026-11-04T15:21:58.891249+08:00 (UTC 2026-11-04T07:21:58.891223+00:00). Current user explicitly requests complete execution without intermediate approval. User owns the question and final scientific judgment; operational metrics/tolerances below are AI definitions under this execution scope, not human scientific acceptance. Role: metric audit plus robustness check. [Focus](../../../../focus/focus_distance_composition.md) and [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_12_distance_composition_anchor.md). No training, probe fitting, interventions or competition-error mechanism.

## 1. Terminology / Definitions

Token gap d=p−e−1 excludes both endpoints; e last item token, p last prefix token. Base length320,p319ID25. Native dictionaries each30000,ReLU Top32; unselected coordinate=post-truncation zero, not proof of zero encoder response. Raw scale and unit-vector direction are separate. Family is the resampling unit; A/Blabels are local words.

## 2. Anchor Alignment

Question: how answer-position combinations change with distance, without assuming degradation. Main rival: apparent fact weakening is global gain/truncation/filler/absolute-position covariation. Old R19 six-member cosine is not an amplitude measurement. All original records/weights remain byte-preserved; new owner15_27_12 and R20only.

## 3. Tested Hypothesis

H1 mean full-native16→128same-fact member retention≥.90. H2 full-native normalized fact separation ratio in[.8,1.25]. H3 normalized separation decreases≥20%. The .90and20% tolerances are explicit local operational choices. Contrast direction is independently reported; no direction pass implies amplitude pass. No score-dependent feature selection.

## 4. Rival Explanations

Whole-code gain, differing object priors, common-question members, rank-threshold crossing, lexical/template specificity, changed filler/order, changed e/p, and incomplete SAE reconstruction. Use raw and scale-normalized metrics, full30000coordinates, fixed6sensitivity, fact-swapped reference, preTopK/h/decoder diagnostics and four supporting control frames.

## 5. Data Construction And Provenance

R19main144rows:24families×A/B×16/64/128. Retain12old discovery/12old heldout by entirefamily. Both responses/sparse representations were already exposed; no fresh-confirmation claim. Literal baseline filler multiset identical across distances. Reverse filler independently inside before/after-fact blocks, preserving role/e/p/length/multiset. Content replaces each weather sentence by a deterministic office sentence of identical tokenizer length, same replacement for a sentence across distances; final question unchanged. Fixed-e uses the old far prefix through the fact plus each old near/mid post-fact tail: e190,p207/255/319,far reused. Pos64supplies all position IDs+64on identical old text, in first heldout family per six templates. This changes encoding indices, not visible token count. Whole data/text/token/role/answer-word counts verified before any model forward.

## 6. Learning Task And Permitted Supervision

No learning task. Read complete candidate log probabilities and frozen SAE activations. Discovery task-frequency counts are a descriptive baseline, not trained parameters. No regression/probe/model/dictionary fit, labels for optimization, gradients or optimizer.

## 7. Model / Architecture And Frozen Variants

Exact R19officialQwen3-0.6B Base/tokenizer/nativeSAEweights/loaders/hashes fromconfig. ATTN: block27.self_attn.o_proj output before residual. MLPIN: actual block27.mlp preinput after residual+post_attention_layernorm. Separate IDspaces. Native lm_head, FP32CPU2threads,SDPA,physical2×328. Capture actualp (319/207/255); full candidate strings preserve leading space/item/period. Onlypos64changes explicit position_ids. Saved h is re-encoded offline with native weights, one row at a time to match original rounding.

## 8. Training Objective And Optimization

NOT APPLICABLE. All model and SAE parameters require_grad=False, inference_mode, no optimizer or weight update. Reuse R19native loader/scorer with dynamic capture position and optional position-IDoffset; do not reuse training scaffolds. NativeTop32exactness,no-ophooks and oldscore replay protect adaptation.

## 9. Conditions, Seeds, And Checkpoints

Seed2026110420. Supplemental228new forward conditions:reverse72,content72,fixed_e48,pos6436. Four smoke new conditions are reused in full stage; six old calibration prefixes cover six templates, so234scored forwards plus one no-ophook check. No new checkpoints. CPUstage ceiling1800s; no GPU/cloud escalation. Per-row atomicNPZ+JSONpermits resume without rerunning completed rows. A failed dependent stage is retained and independent offline analysis continues; no silent substitution or tolerance widening.

## 10. Primary Metric And Frozen Analysis Plan

Primary16→128,each dictionary separately,all12heldout families. H1retention=mean_A/B(|intersection|/32). Factdelta=z_A−z_B; S=||delta||/sqrt((||z_A||²+||z_B||²)/2), x=log(S128/S16). H2uses x within±log1.25,H3x<−log1.25. Bootstrap8192wholefamilies(seed2026110420+siteindex)of the family mean; exp endpoints for ratio. Exact2^12sign swaps,one-sided signed-mean upper tails: H1test(retention−.9),H2max(test(x+log1.25),test(log1.25−x)),H3test(−x−log1.25). Sixp-values Holm-adjusted. Sign-swap location tests assume symmetric independent family errors; show shared-template sensitivity using six template means/64swaps. No clipping,outlier deletion or relabeling. If a norm is zero, recordNAand actualN; fewer8eligible families is insufficient. Old6fixed list includes zeros for all12,with original strict-support replay only a sensitivity.

## 11. Secondary Metrics And Guards

Allthreepairs and allfamilies:shared/entry/exitcounts,Jaccard; complete-ID/raw-value lists; full andcommon norm ratios/cosines; per-row normalized strength differences. Exact coordinate-L2change decomposition common/entry/exit. Fact raw delta norm, S, unit-row contrast norm anddirection, raw/C6/relativeC6/preTopK/hidden/decoder views. PreTopK ReLU is truncation diagnostic,not the trainedTop32code. Decoder-weighted absolute atom change is descriptive,not output contribution/hidden energy. Threshold diagnostic: rank≥25orvalue/cutoff≤1.25,encoder responses both sides and absolute prechange divided by mean cutoff. Native reconstruct errors and fact-difference reconstruction error retained. Full/item-only/period scores separate; original complete paired rates must replay12/12at alldistances.

## 12. Known Good / Known Bad / Known Confusing Cases

Known calibration: old candidate scores and nativeTop32. Known confusion: F23MLP#25508is zero inmain16_A; keep it,not drop family. F28word-only64can fail despite full-string success. Cases selected after main recomputation only for illustration by a rule frozen now: stable=maxshared fraction averaged acrosssites/facts16→128;changing=min;attenuating=minmean logSratio excludingprevious;counter=oppositesign to overallmedianlogratio with largest magnitude,excludingprevious; if no opposite sign,largest cross-site disagreement and explicitlysaynone. Tie familyID, four unique heldout families. Show both facts,allthreefulltexts,allmembers/rawvalues/frequencygroups/scores; no case-based significance.

## 13. Scientific Procedure And Stage Contracts

Prepare/ownerfreeze→offlineR19reconstruction+metricbaseline→smoke4new+6old/no-op→fullremaining224new→registeredmetrics/controlcontrasts→figures/cases/threeaudits/summary+10/30secondbrief→verify+register+localreadingsync→STOP. Smokerequires:role/tokenchecks,positive32,exactnativeencoder,no-op0,laneerror<1e−5,oldscores<2e−5;uniformpositioncontrolnumerics are an observed result,not a gate forced to0. If models unavailable,completeofflinefromsavedarrays; prespecifymissingforwardrows andactualreason. Per-row durableoutputs and stagepid/time/throughputrecorded. No template tuning based on whether a hypothesis passes.

## 14. Algorithm, Output, And Provenance Contract

Fullcode/densepreTopK/h/cache execution-sideR03; canonical bilingualAnchor/Protocol/Summary/Detailed,data+methodguide,allfamily tables,casebook,figures,artifactindex. ReferencegroupD1natural300docs/38400positions,count≥20anddocs≥5,edgesATTN35/70MLP33/62;insufficient/zero separate. Group opportunities:dictionaryeligiblecounts; at-riskleftpositions; rank-matched exits bins1–8/9–16/17–24/25–32. Entryconditionalnull512weightedwithoutreplacementdraws from inactive-at-left features, conditioning on actual entrycount,using referencep=count/38400; taskbaselineweights=discoverymainpositivecount+32×referencep. Never use heldout to fitweights;zeroexpectedgroup is uncalibrated,not infiniteenrichment. Save per-pair nullmean/MCerror andfamilyintervals; these are descriptive conditionalmodels,not additional primaryp-tests. Contrastcontrols always withinfamily,deltas andtemplateintervals; exploratorydifferences do not replace primary verdicts.

## 15. Success / Failure / Insufficient Evidence

H1support ifN≥8,95%lower≥.9andHolmp≤.05;not supportedifupper<.9;otherwiseinsufficient. H2support ifN≥8,95%ratioCIinside[.8,1.25]andHolmp≤.05;not supportedifCIwhollyoutside;otherwiseinsufficient. H3support ifN≥8,95%upperratio<.8andHolmp≤.05;not supportediflower>.8;otherwiseinsufficient. Above1.25is an allowed observed increase,not degradation. Support is an operational data judgment,not scientificacceptance. Secondaryanalyses cannot rescuefailedprimary. Reportallresults evenwhen anotherdictionary/controlfails.

## 16. What This Cannot Claim

No pure universaldistanceeffect: d=p−e−1,changing visiblelengthalsochangesfiller/context; uniformpositionIDs is a restrictedencodingcontrol. Sharedtemplates,alreadyexposedholdout,smallN,limiteddistances/objectpairs,SAElossandTop32remain. RawpostTopKdelta/normalizeddelta/direction are dictionary observables,not causal use or semantic capacity. No competitor-erroranalysis,intervention,routertrainingorautomaticfollowup.

## 17. Block Confirmation, Freeze, And Amendment Ledger

Aquestion/userpurpose confirmed by currentprompt;Bobservationaldesign delegated by completeexecutionrequest;Cdata/splits/assets verified;Dnativeinterfaces verified;Eobjective/optimizationNA;Fmetric/uncertaintyAIoperationalizations fixed above;Gboundedlocal228conditions explicit necessarycontrolscope. Cross-blockself-auditPASS,three audits stored. ScientificacceptanceUnknown. Frozen before newanalysis/forward at2026-11-04T15:21:58.891249+08:00. Preserve full protocol bytes; later changes append ID/time/before-after/reason/visibledata/affectedconditions/authorization/eligibility andretainoriginalversion. No new metric/threshold chosen afterresults. First summary may give requested operational hypotheses and one AI-suggested question,without researcher mechanism acceptance.

## Amendment A1: configuration metadata qualification / 配置元数据说明

Recorded 2026-11-04T15:52:39.307878+08:00 (UTC 2026-11-04T07:52:39.268527+00:00), after all control outputs were visible. The frozen config reused R19and retains three unused R19provenance fields: prefix_count292,new_prefixes96,panel_sha256ofR19. Actual execution used panel_rows372,new_forward_rows228,the literal panel and IDlists; none of those legacy fields controls scoring or statistics. Original config/protocol bytes remain preserved. effective_config.jsonnow scopes the inherited fields and records actual372conditions,192new texts,36same-textposition-index variants and current dataSHA. This is metadata qualification only: no text/token,split,forward,member,metric,threshold,test or result changed. Scientific eligibility is unchanged. The current user authorized the complete audit and correction; no additional experiment is implied.

已见全部结果后发现复制配置残留旧R19的292/96及旧panel哈希字段，它们没有参与R20抽样/评分/统计。实际使用的新字段是372/228和真实ID表。保留原冻结文件；effective_config.json把旧字段放入继承命名空间，给出当前哈希和192新文本+36同文位置索引条件。仅澄清元数据，不改任何科学输入/结果。
