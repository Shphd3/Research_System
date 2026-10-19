# Detailed: normalized routing and frozen-base expert learning

[中文完整记录](detailed_cn.md) · [Summary](summary.md) · [Protocol](protocol.md). Question and hypothesis are unchanged from the supplied Anchor plus pre-execution scoring supplement. Main execution COMPLETE, registered learning hypothesis NOT SUPPORTED in this setting; scientific approval Unknown.

## 1. Purpose, hypotheses and model

Test whether frequency-organized fixed routing calibrated to TRAIN response improves held-out next-token prediction on low-feature-hit inputs under a fixed architecture/budget. H1 predicts increased target reception; H2 requires primary T_S1 to beat both T_S0 and R11_S1 by at least.01low-feature macro NLL, overall harm at most.01, in both paired seeds. Greater participation/exposure rather than frequency organization is a rival. Reception, actual within-expert frequency and learning are distinct.

Frozen base/dictionary/norm/tied head; eight bias-free full1024-wide SwiGLU experts have25,165,824parameters, learned references add8192router parameters. h is block28residual-post before global norm; u=h/TRAINscalarRMS without centering; h_out=h+scalar*gate*expert(u). Fixedgate1; learned selected-softmax gate. gate/up random std1/sqrt1024, down0. No transformer training or new representation extraction. Joint14-layer z and its teacher cost are explicit; layer28 contribution c=z||D28|| is separate from routing a=z*sum14decoder norms.

## 2. Data, scoring and exact contract

TRAIN130712positions/128contexts, EVAL65402/64 from different bins. Reliable9615, low964, high962; T/R11candidate9605 and identical group sizes1257/1347/1506/1629/1824/1189/523/330. R11 is one fixed list; modelseeds11/22 are separate. p=TRAINhit probability, m=TRAINconditional positive a mean. S0mean(a), S1S0/meanTRAIN(S0), S2mean(a/m), S3mean(a/(p*m)); original group denominators, inactive0, no composition or quotas. Positive-class median*1e-6 floors and original0handling are frozen; no zeros/floor triggers occurred. S2's TRAINmean equals groupmean p; S1/S3mean1does not imply balanced argmax.

Threeepochs,768updates/392136positions per main model; batch512/micro128/tail152; exact paired PCG64permutations. AdamW3e-4,(.9,.95),eps1e-8,wd.01,clip1,39warmupsteps then cosine to.1lr. FP32parameters/Adam/CE with BF16GEMMs. Full-batch LB8sum stopgrad(f)*meanP, coefficient.01onlyLearnedLB,0Learned; fixedarmsnoLB. Save complete initial/epoch states and64-step recovery, optimizer/RNG/orders/counters/config. Token-indexed TensorBoard was verified on all20runs.

## 3. Main evidence and eligibility

All20models completed identical budgets. [All endpoints](tables/all_condition_results.csv), [per-feature](FULL_ASSETS.md#asset-5f35835f75d4), [curves](tables/training_metrics.csv), [all steps](FULL_ASSETS.md#asset-425a830665b8), [actual exposures](tables/expert_training_exposures.csv).

|条件|seed|EVAL整体NLL|EVAL M_L|TRAIN诊断NLL|
|---|---|---|---|---|
|T_S0|11|3.1444|2.7097|2.7148|
|T_S0|22|3.1508|2.7169|2.7103|
|T_S1|11|3.3632|2.8904|1.7991|
|T_S1|22|3.3759|2.9022|1.8019|
|T_S2|11|3.1445|2.7098|2.7144|
|T_S2|22|3.1505|2.7166|2.7098|
|T_S3|11|3.3925|2.9141|1.7505|
|T_S3|22|3.3929|2.9132|1.7788|
|R11_S0|11|3.3864|2.9223|1.8000|
|R11_S0|22|3.3852|2.9245|1.7956|
|R11_S1|11|3.3934|2.9230|1.7717|
|R11_S1|22|3.3906|2.9279|1.7767|
|R11_S2|11|3.3966|2.9354|1.7613|
|R11_S2|22|3.3893|2.9348|1.7512|
|R11_S3|11|3.4043|2.9359|1.7066|
|R11_S3|22|3.4027|2.9356|1.7150|
|Learned|11|3.0966|2.6649|2.9341|
|Learned|22|3.1123|2.6791|2.8662|
|LearnedLB|11|3.1142|2.6825|2.8330|
|LearnedLB|22|3.1151|2.6835|2.8011|

NLL nat/token, lower better. M_L first averages NLL at each fixed lowfeature's hits then equally averages features;964estimable, overlapping positions. Lowunion is about75%ofEVAL; highunion covers allEVAL and equals overall, with separate highfeaturemacro available. Frozen baseline overall=3.023366,M_L=2.593718. Lowfeaturemacro being lower than overall warns against equating low frequency with difficulty.

|比较|seed|ΔM_L|块95%区间|Δ整体NLL|实践门槛|
|---|---|---|---|---|---|
|T_S1−T_S0|11|0.1807|0.1675～0.1928|0.2188|False|
|T_S1−T_S0|22|0.1853|0.1730～0.1988|0.2251|False|
|T_S1−R11_S1|11|-0.0326|-0.0469～-0.0199|-0.0302|True|
|T_S1−R11_S1|22|-0.0256|-0.0372～-0.0143|-0.0147|True|

The B-Cpractice criteria pass both seeds, B-Afail both, so joint H2fails. All20endpoints worsen both metrics against baseline. TRAINdiagnostic starts3.21169andT_S1drops to about1.80while EVALrises; this is not failure to optimize TRAIN. Current evidence is consistent with overfitting/update magnitude/distribution differences, not a uniquely identified cause.1000paired EVALcontext-block bootstraps, seed20261019, minimum961estimable features in a resample; NAis never zero-filled.30role rows represent26unique pair/seedvalues, not30independent experiments. EVALalreadyviewed/documentindependenceunknown; only2modelseeds and1randomorganization.

## 4. Activation, dispatch and function

Two preselected source-ordered64token windows; actual z/c grids, globalTRAINp, whole-split positiveeventquartiles and full low-position rankings/text are saved. Display selection by peak c is descriptive, not representative semantic sampling. Following text is posthoc only. Reconstruction EVALrawrelativeerror.048508vscentered.136072, with actual inverse raw_hat=hat*rms28+mean28; no coordinate mix. After all training, reread z/c matched original profiles exactly. [Text](text_profiles_cn.md), [reconstruction](tables/reconstruction28.csv).

|固定路由|低频接收率|零接收/964|B≤2占固定964|
|---|---|---|---|
|T_S0|0.0023%|960|0.4149%|
|T_S1|33.4033%|5|7.1577%|
|T_S2|0.0000%|964|0.0000%|
|T_S3|41.6942%|0|4.6680%|
|R11_S0|16.6280%|31|4.5643%|
|R11_S1|15.8412%|19|4.4606%|
|R11_S2|13.8674%|21|2.3859%|
|R11_S3|26.3917%|7|7.6763%|

Reception is hits sent to listedowner/alloriginalhits, then feature-macro; q=featurehits/actualexpertpositions. Legacy field assigned_reception_a is reception, not routing amplitudea_i(t). Top10remains in full inputs/qeven when absent from lists. HeadgapB averages positive log10ratios, B<=2does not bound each head individually. S1only69/964pass B<=2, so better reception is not same-frequency input. [All q](FULL_ASSETS.md#asset-d27f7cd7ce74), [group hit matrix](tables/group_to_actual_expert.csv), [frequency plots](figures/figure14_expert_frequency_distributions.png).

A posthoc descriptive largest-score-term diagnostic finds T_S0Hmembership99.9985%,S1=21.2623%,S2=100%,S3=16.0790%; it is not semantic common dominance or absence of highfrequency information. Previousphi reorganization changed175members after489swapsbut no route; no phi training ran here.

Fixed common EVALprobe: contextstratified general<=1024plus<=512Lhit positions, deduplicated/uniformrowweights. Gate1forced8expertlosses and naturalgate-preserving replacements are distinct; seed11T_S1forcedNLLrange3.2102–3.4469against same-probezero-branch3.0248; zero-natural difference−.3269. Different outputs/replacementlosses do not certify semantic roles or every possible router. Full initial/final/delta gate/up/down spectra and centered response covariance spectra are saved. Normalize by full energy, zerodowninitial=NA. DeltaW includes AdamWdecay, spectra are neither directions nor capacity. No cross-policy functional IDmatching.

EVAL positive-event pooled low/high medians are z=.02606/.01792, routing a=.14808/.11566, layer28 c=.01938/.02290, with131652/8997930events. These are event-pooled rather than equal-feature distributions: low frequency is not uniformly smaller amplitude and the three quantities cannot substitute for one another.

## 5. Independent target scene

TRAIN-only firsteligiblefeature2has269hits/98contexts. Independent T_S1seed11background excludes them:130443uniquepositions,2epochs/510steps/260886exposures. Frozen routing statistics see unlabeled target features; base/dictionary may know content. Recommendations fixed before adaptation using TRAIN: owner0,modalroute0,currentforcedprediction5. Eight copies eachupdateonlyexpertj,identical target order,32stepsbatch64/lr1e-4/resetAdamW,gate1; eval0/8/32. C_eval94positions/40contexts; B_eval uses background natural routes.

|专家|适配前C_eval NLL|32步后绝对NLL|收益before−after|旧输入损害|
|---|---|---|---|---|
|0|2.5019|2.9292|-0.4273|0.0473|
|1|2.4947|2.9334|-0.4387|0.0517|
|2|2.4883|2.8932|-0.4050|0.0390|
|3|2.4945|2.9788|-0.4842|0.0211|
|4|2.5875|3.0080|-0.4205|0.0280|
|5|2.4188|2.8785|-0.4597|0.0252|
|6|2.4970|2.7831|-0.2861|0.0461|
|7|2.5195|2.8924|-0.3729|0.0206|

All8worsen targetNLL and violate oldharm<=.01. Safeoracleempty; expert6lowest final2.7831still unsafe and worse than its own start. Rank by absolute adaptedloss, not only improvement. This one-target/one-backgroundseed result is neither truly new knowledge nor an assignment algorithm.

## 6. Conformance, failures and authority

New scientific definitions/budget unchanged. Sole engineering fixes: scopedSCOunknownresponsefield filter; PythonprotobufTensorBoardcompatibility; scalarstatehashreshape. Initial jobpt-r697pchxhad platformSUCCEEDEDbut internalengineeringBLOCKEDbeforeformalupdates; immutablejobworkspacepreventedrestart. Terminalconfirmed, replacementpt-falmqs6xusedthesame4H100profilewithnooverlap/reservationexpansion, reused profiles/statistics, thencompleted. Formal budget/finitenegativeconditionswerenotchanged.

Initiallogitsmaxerror0, postfirstexpertupdatelearnedrouterCEgradientnonzero,64positionsfit to~1e-6,exactnextupdateSmoke replayPASS. All20formalstateshaveoptimizer/RNG/orders/counters; formalindividualcontinuationsNOTRUN. FinalcheckpointSHAfresh; othermilestonesbytes/accessonly. Datasetposition+1labelscheckedallpositions; native32-positionfullmodel/head equivalence inherited from qualified parent extraction, not rerun here. Newzero-branch/frozenprobe checks are separate.

All20functional,20spectral,8targetbranchescompleted. FourH10080GB,2CPUthreads/worker,actualquota88CPU;main-trainingGPUallocatedmax1.055GiB,mainworkerRSSmax2.550GiB,executiondiskabout26.80GiBagainst32GiB/GPUand64GiBdisklimits. PreciseaggregateRSSpeakwasnotsampled; retainperprocessrecords/4workerconcurrencyratherthaninventit. Pipeline615.9secondsplusfirstfailedengineering32.1seconds; these are processwalltimes, not purekerneltime/financialcost. No new GPUor trainingafterthisround.

## 7. Provenance and evidence ownership

Executionroot `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/normalized_route_learning/20261018T173143Z` owns code, full raw JSONL/TensorBoard/checkpoints/caches and response matrices. This project holds curated plots/tables and [payload manifest](FULL_ASSETS.md#asset-efa7317b1a29).24actualoutputassets/currentselectedaccess recorded in assets/normalized_route_learning.md; [IDs](evidence/output_asset_ids.json), [states](evidence/checkpoint_members.json), [source](evidence/source_manifest.json), [verification](evidence/final_verification.json), [frozen config](design_freeze.json). Code/source/currentnativecontext and parent identities are separate from scientific eligibility. Large payloads stay execution-side.

## 8. Interpretation and next decision

Retain: competition-scale calibration changes actual reception. Weaken: better reception is sufficient for useful learning; current expert adaptation offers safe assignment. Unknown: the relative roles of update scale, finite-data generalization, exposure and frequency organization. No from-scratch capacity/semantic common-unique/phiutilityclaim. Researcher judgment Unknown; noFocusclosure,commit,pushorfollow-onrun.

AIproposalonly: use an independent development set to predefine one shared smaller branchupdatescale, then recheckA/B/Confreshheldouttext to distinguish generalization/updatefailure from organizationdifferences. This is not authorized execution.
