派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_feature_presence_amplitude_20261101/protocol.md)；研究修改仍回到原件。

---

# R13: feature presence, conditional amplitude and complementary readout

## 0. Approval Snapshot

APPROVED_FOR_CACHE_ONLY_ANALYSIS by the researcher’s current explicit request. Asset audit precedes this Protocol and any readout fitting. CPU only,two threads,two-hour wall ceiling,no GPU,no new LM forward,no dictionary/LM training. A15_27_04 remains scientific owner;anchor.md is this run’s scope binding,not a parallel formal Anchor. Scientific acceptance/closure Unknown. Numeric choices below are predeclared AI operationalizations under the requested analysis scope,not human acceptance of future results. Initial bytes and hashes are retained before fitting.

## 1. Question and rivals

A:does high-frequency amplitude add beyond binary presence,and is it the main readable discriminator? B:does middle/low presence add beyond high-frequency BA,and does high-frequency BA add in return? C:what actual text is corrected/newly confused,and could vocabulary,format or source explain it? These are task-specific linear-readability questions,not native routing or expert assignment. Rivals include input count,regularization,rare support,source style and finite exposed samples.

## 2. Model,data and frequency

Use the same official Qwen3-0.6B-Base,A22native14joint residual-post interfaces blocks1,3,...27,TRAIN centering/RMS and saved norm-weighted gate. z is shared across all14interfaces,not a layer27-only encoder. No Dense application. Native gate norm is sum of normalized-decoder L2norms across layers,not a concatenated global L2norm. Layer27decoder is restored to model scale(RMS374.3495121024576),with original bias. For contribution d=n*u,z_eff=z*n preserves z*d exactly;no cross-layer norm is substituted for a specified layer.

Exactly reuse R12’s96unique primary documents/target279positions,last the at96–191,with external visible-prefix labels and exact fitted IDs. Each task D8/class,V4/class;Hcoarse37,mathfine17,biofine18. Fine-ambiguous cases remain coarse-only. Original-family split is preserved,one position/document;documents across tasks are not added. Hwas already used by R11/R12,so evaluation is exploratory. Known282/292/262/297/090cases are not independent confirmation. Readout tuning policy is newly fixed and cannot be silently equated to R12’s different tuning rule.

Independent DCLMnative-positive reference denominator65,536,min20hits. Original bins low20–170,middle171–881,high≥882,hence rate boundaries.002593994140625/.0134429931640625,ties downward. Reference-insufficient members separate. Dtarget support≥3documents is the main readout eligibility;less-supported members remain descriptive. Positions/document supports are separately stored,identical for this one-position panel. No classifier label or H result enters frequency or member choice.

## 3. Encodings and equal member budgets

B=1[z>0],Z=z,A=0when absent,otherwise(z−positive-D-mean)/max(positive-D-std,1e-8). At least3positive Dsamples;constant positives yield zero A and a flag. BA concatenates B,A. Mean z=occurrence×conditional mean amplitude and is not pure strength. Every encoding column is standardized with its Dmean/std,floor1e-8,using identical Bpreprocessing in B/BA. B+0adds equally many zero channels at every split and checks no dimension-dependent penalty change. ZvsB is auxiliary,not nested.

D-only eligible low/mid/high pools are3/45/448(coarse),4/54/472(mathfine),10/42/397(biofine). Equal k=min(32,nlow,nmid,floor(nhigh/2),floor((nlow+nmid)/3))=3/4/10. Order members bySHA256(seed|task|frequency|ID),primary1101,sensitivity1101–1110,no winner selection. MLhas ktotal members,as balanced low/middle as possible with odd extra assigned middle. Each separate L/M/Hgroup has kmembers. Full eligible groups are separate secondary analyses;their dimension advantage is not frequency evidence.

## 4. Readouts,combinations and controls

All use L2logistic regression,LBFGS,class weights balanced,unpenalized intercept,tol1e-10,maxiter10000. Cgrid.01/.1/1/10,same budget for every condition. Select minimum Vordinary logloss,then higher VBA,then smaller C. D/Vstatistics and membership never use H.

Cross every L/M/H/MLgroup with B,Z,BA. Primary joint=[H_BA,ML_B],3kcolumns. Bilateral contrasts compare joint with H_BAand ML_B. Same-dimensional H_reserve=[H_BA,knew disjoint high B]and ML_reserve=[ML_B,2knew disjoint ML B]also have3kcolumns. Reserve order is label-blind fixed hash. MLreserve samples the remaining MLunion;its within-union frequency mix may differ and is reported. No support relaxation. No arbitrary permutation is claimed as conditional independence.

## 5. Metrics,uncertainty and decision rules

Report balanced accuracy(two class recalls equally),ordinary document predictive logloss,classwise correct/total,and every Hscore/probability. Paired5,000stratified document-family bootstrap(seed11101),not tokens;BAaverages class recalls,LLretains original class proportions. Fifteen primary BAcontrasts(5/task:HBA−HB,joint−HBA,joint−MLB,joint−Hreserve,joint−MLreserve)have95%pointwise and99.6667%Bonferroni simultaneous percentile intervals;LLgain=oldLL−newLL,95%pointwise. Small-sample classwise exact binomial bounds are separate from possibly degenerate bootstrap.

Amplitude increment requires simultaneousBAlower>0,LLgainlower95>0,and≥8/10member seeds positive BA. Saying mainly amplitude additionally requires95%lower of(LL_B−LL_BA)/(LL_prior−LL_BA)>.5;undefined denominator≤1e-8is not reported. Zwinningalone is insufficient.

Unique bilateral complement requires both directional gains and both same-dimensional contrasts to have simultaneousBAlower>0,LLgainlower95>0,and≥8/10seeds positive. Otherwise state no unique complementary evidence yet,not low-frequency uselessness. Judge tasks separately. Even a pass remains exploratory on exposed H.

## 6. Errors,text and confounds

Save all corrected,new-error,both-correct,both-wrong documents. Analyze all5known cases;ordinary cases are first Hhash per class;counterexample is first hash newly wrong document,none if absent. Show complete visible prefix,the full target word,position,source,label,predictions,B/Achanges and signed linear readout terms,not only a high-response subtoken. Terms are model-score attribution,not causal importance;refitting changes old-channel weights. Following text is post-hoc only.

Target identity is exactly controlled. Source/genre/position/prefix length/formula/punctuation metadata and training-only1000feature1–2gramTFIDF baselines get the same D/V/Cbudget. Report Hsource strata and maximum cross-class same-platform/same-genre matching with position difference≤32,without responses;≥10pairsprimary descriptive,5–9exploratory,<5insufficient. Vocabulary/source confounds not controlled by these comparisons remain.

## 7. Spectrum,reconstruction and residual supplement

Use exactly R12fixed1024PCs at matching Qwen/block27/model units. Keep orientation q(unit decoder),actual use z,and signed class-difference contribution distinct. Partition all16384decoder coordinates by independent reference L/M/H/insufficient,not merely readout-eligible features. v_g=sum z_f d_f,full r=b+sum_gv_g,residual h−r. Project actual summed vectors before squaring to retain cross terms. Save signed per-PC class differences,64PCgroup energies,within/between-group cancellation,and fixed-h-head signed score contributions. Constant,all groups and residual exactly reproduce original scores.

Train one original-h head on D/V,hold it fixed on full reconstruction,each group+b,and residual;report errors,agreement and error swaps. Separately refit heads on reconstruction/groups/residual to assess remaining readability. Full relative squared error||h−r||²/||h||²,group approximation error and residual component norm are explicitly distinguished. Symmetric occurrence/amplitude decomposition is interpretable only with≥3positive documents in both classes;zero-side conditional means stay NA. Low reconstruction error is not complete category explanation.

## 8. Execution and delivery

Freeze this Protocol,config,code and Dselected memberships before Hnumeric access;freeze fitted D/Vmodels before H. Preserve initial_protocol.md bytes,append amendments rather than overwrite. Raw arrays,models and code remain execution-side;canonical reports stay here. Main figures limited to three groups:frequency×encoding,bilateral gain with dimensional controls,error exchanges and real cases. Spectrum/reconstruction is supplementary. Save all conditions/seeds/negatives,predictions,raw statistics and reproducible entry. Maintain three audit rounds and coverage ledger. At completion append factual evidence/boundaries to the existing main Anchor and one best next question,without new conversations or automatic additional experiments.
