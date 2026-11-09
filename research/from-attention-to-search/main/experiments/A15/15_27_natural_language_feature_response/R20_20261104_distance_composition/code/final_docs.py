from common import *
import pandas as pd,shutil,re
stamp=now();local=local_now();primary=json.load(open(R/'results/primary_hypotheses.json'))
guide='''# Data and methods

The actual panel has372conditions:144R19main prefixes,192new literal prefixes(reverse72,office72,fixed-e-near/mid48),and36same-textposition-IDvariants. A fixed-e distant point reuses the old main128row;24far rows are aliases in that analysis,not additional samples. The new scored LM calls are228control conditions plus6old calibrations;4new smoke conditions are included in228and not rerun. A further no-opforward checks hook identity without adding an observation. Old cached hook inputs are re-encoded288times(two dictionaries×144prefixes),with zero LM forwards and exact Top32agreement.

panel.jsonlretains complete English prefixes,alltokenIDs/offsets,last-item/answer positions and full candidate IDs. Each native postTop32code has30000coordinates; indices/values list all32positive coordinates and every other coordinate is post-truncation zero. Inactive does not imply a zero encoder response. IMPORTANT: the cache key `pre_relu` is a legacy field name for `relu(encoder(h))` BEFORE TopK,not the signed linear pre-ReLU vector. It is a threshold diagnostic,not another trained dictionary. h and reconstruction retain actual1024-dimensional hook input and native decoder reconstruction.

ATTN_SAEcaptures block27.self_attn.o_projoutput before residual; MLPIN_SAEcaptures actualblock27.mlpinput after residual and post_attention_layernorm. Native metadata matches layer/model configuration; the exact official model/tokenizer and both weight/loader hashes are in the frozen configuration. No dictionary ID is shared across sites. No normalization precedes native encoding. The sourceSAEs were previously trained; none was trained or modified inR20.

Gap d=p−e−1excludes both endpoints,e=last object token. Baseline/reverse/office prefixes have320tokens,p319colonID25,e302/254/190. Fixed-e has e190,p207/255/319. Pos64retains identical text and token positions but supplies allpositionIDs+64; visiblep319corresponds suppliedID383. It is a computational encoding-index test,not64addedvisible tokens. Full candidate strings include leading space,item and period,with equal token counts within each family.

The12old heldout families remain primary;12discovery families remain exploratory. Both old behavior and sparse results were exposed before this round. New controls reuse the same families and shared six templates,not new independent families. Facts/distances/controls stay together under family bootstrap. The four case rules are fixed inProtocol; all others remain in raw tables.

Full-code fact separation is ||zA-zB||/sqrt((||zA||²+||zB||²)/2). Raw difference norm,totalcode scale and direction are separately stored. Common-member changes and allentering/exiting strengths are retained. Coordinate squared-change sums and decoder-norm-weighted absolute changes do not equal hidden-space energy,output contribution or causal importance. Fixed6members use literal zeros and allfamilies; old strict-support is only a replay sensitivity.

Frequency labels exactly reuse each native D1reference:300natural discoverydocuments,38400positions;count≥20anddocumentcoverage≥5for high/middle/low. Attention edges35/70;MLP33/62;tied boundaries upward. Insufficient and zero groups are separate. Both source cache/table/metadata hashes are current and bins are recomputed. Reference occurrence is not training exposure,word frequency,spectral location or semantic importance. Natural- and discovery-task-weighted conditional opportunities and rank-matched exits are descriptive models,not hidden causal controls.

Frozenconfig.jsoncontains three inherited,unused R19provenance fields(prefix_count292,new_prefixes96,panel_sha256ofR19). Actual execution used the correctR20panel_rows372/new_forward_rows228and literal IDlists. effective_config.jsonscopes those legacy fields and supplies currentSHA/counts/actual assetIDs. The frozen original is retained; A1qualifies metadata only. No numerical input or result was changed.
'''
(C/'dataset_guide.md').write_text(guide);(C/'dataset_guide_cn.md').write_text('''# 数据与计算定义

实际372条件=144旧主任务+192新全文+36同文位置索引变体。固定e的远距24条复用旧行，不当新样本；4新smoke并入228控制前向，不重复；另6旧校准和1次无操作前向。旧h的288次SAE再编码不是语言模型前向。

原始全文/token/offset/候选完整序列在panel.jsonl。两套原生字典分别30000维、ReLU/Top32，indices/values给出全部阳性，未列坐标为截断后实际零。缓存键pre_relu实际指relu(encoder(h))、即ReLU之后TopK之前的响应，不是带负数的线性pre-ReLU；仅作阈值诊断。h/reconstruction是1024维真实输入与原生decoder重构。父模型配置/接口已由checkpoint元数据核验，未训练或修改权重。

距离d=p−e−1排除两端，e取物品最后token。主/反转/办公p319、e302/254/190；固定e190时p207/255/319；pos64保持真实文本/索引，只把position IDs统一+64，p319的供给编码ID383。后三者不能混叫物理文本位置平移。候选含前导空格、完整物品词和句号，族内等token数。后续候选/句号分数不能全归因于p319的feature。

全部12旧留出保留，12发现仅探索；旧结果已暴露，六模板共享；每族A/B、距离与所有对照共同重采样，不能把372条件当372独立样本。四案例选择规则先冻结，全部其余家族仍保存。

相对事实差异=||zA−zB||/sqrt((||zA||²+||zB||²)/2)，同时保留原始差范数/全码尺度/方向。固定六成员实际零不删，旧严格支持另作复核。完整坐标平方差分解与decoder列范数加权绝对差都不是隐藏能量、输出或因果贡献。

频率原定义：独立自然参考300文档/38400位置，count≥20且doc≥5，Attention35/70、MLP33/62，边界并入较高组；不足与零单列。参考频率不是训练曝光、词频或谱位置。机会统计含字典基数、左端风险、旧排名四档匹配换出，以及自然/发现任务加权的换入期待；零期待是未校准，不算无穷富集。

原冻结config继承的prefix_count292/new_prefixes96/旧panel哈希仅为未使用的R19元数据，实际代码用372/228与ID表。effective_config.json给出完整当前清单并隔离旧字段，A1记录澄清，原冻结配置不改。此修正没有改变文本、采样、评分或检验。
''')
detail='''# Detailed execution and evidence record

Factual measurements complete; scientific acceptance Unknown. This is the user's complete authorized distance-only study. [Summary](summary.md) owns the bounded recognition update; [numeric evidence](numeric_evidence.md) lists every heldout family. No competition-error mechanism,feature intervention or training occurred.

## Actual setup and computation

R19literal main prefixes are paired by family/fact/distance; changing the remote fact changes only the item. Prefix length/answer position are fixed; moving the fact reallocates the same filler multiset before/afterit. Two native interfaces/dictionaries remain separate. Capture is at the lastprefix token(actualp319,or207/255in fixed-e),without any activation modification. The native outputhead separately scores every token of each leading-spaceitem-plus-period candidate. Dynamiccapture/position_idsare the adaptation from R19; FP32CPU2threads/SDPA/physical2×328and frozen assets are reused. Original six calibration scores,no-opoutputs and candidateprefix lanes agree exactly. There are no trainable parameters,optimizer,new modelcheckpointorSAEfit.

Full native vectors include every30000coordinate with postTopKzeros. Common-member norms/cosines,rawfullnorms and per-member raw/relativechanges are distinct. FactA/Bdifference raw norm and scale-normalizednorm are stored per distance; raw and unit-row contrast directions are separate. Allthreepairs and allfamilies are retained. PreTopKReLU,actualh and native reconstruction are diagnostic views; they do not replace the primary nativecode. The cache fieldpre_relu is rectifiedpreTopKdespite its short name.

## Exact statistical contract

Primary:16→128,all12oldheldout families,withA/Baveraged insidefamily. H1retention≥.9,H2relative fact-separation ratioinside[.8,1.25],H3ratio<.8.8192familybootstrap,site seed2026110420+index; exact paired sign swaps and six-testHolm. Location-sign tests require symmetric family errors. H2maxes both boundaryp-values; operational judgments require the declaredCIand correctedpconjunction. Discovery12is exploratory. Six shared templates are a sensitivity via clustermeans/64signflips,not evidence of unseen-templategeneralization. Otherpairs/frequencyconditions are descriptive,not additional uncorrected confirmatoryp-tests. Numericalbootstrapendpoints can differ slightly betweenprimarysite-specificseed and descriptivecommonseed; point estimates agree. No outlier removal or support-basedfamilyselection.

Frequencygroups reuse verifiednative natural reference and ties/eligibility. Entryopportunities exclude left-active atoms,condition on observed entrycount,and sample512weightedwithoutreplacementsets using referencefrequency or discoverymaincounts+32referencep. Exits compare at-riskcounts and matches oldranks in bins1–8,9–16,17–24,25–32. The nullmodels do not preserve futuretaskmarginals or semanticfamilies. Per-group counts/proportions,rawstrengths,zeroexpectedcases,MCSEand whole-familyintervals are retained. Rare members' actual familycoverage is exposed rather than changingdefinitions.

## Controlled supplements and remaining covariation

Reverseweather reverses filler sentences separately before/afterthe fact,keeping320tokens,e/p/questionandthemultiset. Officefiller deterministically replaces eachweatherline by an equallytokenizednon-answerline;topic,lexicalidentityand repetition change together. Fixed-e190splices the original farprefixthroughfact with eachnear/midafterfacttail;answerp207/255/319andtotalvisiblelengthchange. Pos64keepsidenticaltokensand suppliedencodingIDsall+64on six template-coveringfamilies; analyze it against the same six baselinefamilies,notagainstthe twelve-familymean. It is not64extra visible tokens. The identityd=p−e−1prevents allthreefactors beingindependent; these are complementarylimitedcontrols,not an identified universalcausal law.

Reverse/content/fixed-e mean normalized fact-separationratios remain above1atbothsites. Uniformindexshift retains everyTop32member;smallfloat32hidden/scorediscrepancies are observed,not forced toexactzero. Candidateaccuracy is a reference,not evidence that these particularmembers causally causeananswer. Fullchain scores include later candidate/periodpositions; theycannot all be localized to thecapturedp.

## Quality, failure and eligibility

NativeSAEweights/configmetadata/hookidentity are verified, and all144oldprefixes reproduce their32members/values exactly after offlineencoding. Thus the large fact-difference reconstruction error is not hidden by a changed dictionary or input-interface substitution. Ordinary rowreconstruction and actualA/Bdifference reconstruction are separatelyreported. Median relativefacterrors≈.994/.984limit any claim that code norms represent totalfactualinformation. PreTopKgeometry is a diagnostic,not a modelintervention or a replacement trainedcode.

Originalfullcandidatepairedaccuracy remains12/12at16/64/128;item-only64is11/12. Newreverse16hasonefailureF28stamp,margin−.084757nat;its64/128counterparts arecorrect. Office/fixed-eare12/12;pos64is6/6. Allfailuretext/token/scoresremain. These are eligible observations,not failedcalibration or excludedfamilies.

Beforefreeze, preparation foundmissingtimezone database;explicitShanghaiUTC+08timezone was used,withthepartialattemptpreserved. JSONmembershipserialization required convertingNumPyIDs to Pythonint;no data/statisticchanged. A reportcolumnlookupunderscore was corrected;the failedsource is archived. The original frozenconfigretains three unusedR19provenancefields;effective_config.jsonandappend-onlyA1scope themcorrectly. Actualsampling/scoringusedthecorrect372/228andIDlists. OriginalscientificProtocolbodyandownersare preserved in versions; laterfactualownerupdatesare resolved byhash. No threshold,data,family,modelorcontrolwas changed toobtain a desiredresult.

## Evidence lineage and completeness

|Claim or check|Raw observation|Computation|Unit / uncertainty|Eligibility / limit|
|---|---|---|---|---|
|Membership and strength changes|Literal Top32IDs/values/h|analyze.py pair/member tables|Family;A/Bfirstaveraged|ELIGIBLE dictionary observations;fixedbudgetidentitynotfinding|
|Fact magnitude and direction|All30000native coordinates,not selectedonly|A/Bdelta,rawnorm,totalRMS,cosine|All12heldout;8192bootstrap/Holm6|ELIGIBLE operationaltest;semanticinformationUnknown|
|Frequencyrole/opportunity|Independentreferencegroups;discoverycounts;rawmembers|frequency.py and frequency_roles.py|Family;512conditionalnull draws|BOUNDED descriptivepropensity,notcausalimportance|
|Filler/position robustness|All228newconditions plusreusedfarrows|Samefamilycontrast/control_family_differences|12families;pos64only6matchedfamilies|BOUNDED bylinkedlength/filler/position|
|Answerpreference|Bothcandidates'alltokenlogp|math.fsum,correctmargin,bothfactsrequired|Family pairedswitches|Completechainranking,notfreegenerationoralllocalizedp|
|Truncation/reconstructionquality|NativepreTopK,h,reconstruction|Threshold/cutoffandfactresidualaudit|Per-familyanddescriptivemedian|Diagnosticonly;doesnotrescueprimary|

## Round identity and next decision

R20has one question/hypothesisfamily,one setup with supportingcontrols,no trainingdata,fixedold discovery/heldoutfamilies,complete results and boundedknowledgeupdate. Complete setup/fields are in[datasetguide](dataset_guide.md),literalexamplesin[casebook](casebook.md),and actualoutputpaths in[artifacts](artifacts.md). Processing-agent threeaudits are self-review,notindependenthumanreview. Scientificmechanismacceptance remainsUnknown. Stopforreview; the soleAI-suggestednextquestionconcernswhich preservedcodefactdifferencesareactuallyreadfortheanswer. No followupdesigned/executed.
'''
(C/'detailed.md').write_text(detail)
(C/'detailed_cn.md').write_text('''# R20执行与证据记录

事实计算完成，科学接受Unknown。[Summary](summary_cn.md)拥有认识更新，[数值附录](numeric_evidence.md)逐家族保留结果。当前用户完整授权的是距离观察与必要对照；没有竞争错误机制分析、干预或训练。

## 实际如何比较

旧144条主文本按族/事实/距离配对，A/B只改物品。总长320与p319不变，事实移动同时把同一填充集合重新分配到前后。两原生SAE分别读第28层Attention投影输出、实际MLP输入，不混ID。新前向沿用原CPU2线程/FP32/SDPA/物理2×328、原生lm_head，只适配动态p和可选position IDs；hook不修改输出。所有候选token含物品与句号逐个条件评分。6条旧评分、两候选前缀激活、无操作hook误差均为0。

全部30000坐标的截断码为主要对象，零和所有家族都保留。共同成员范数/方向、完整码范数、A/B差异原始范数、相对尺度及方向分别计算。全坐标平方改变的三项分解只表示坐标改变，不是隐藏能量。缓存pre_relu字段实际是ReLU后、TopK前的响应，h/reconstruction为真实输入/原生decoder重构；前者仅作截断诊断，不替代训练好的Top32码。

## 对照改变与固定了什么

反转天气：事实前/后各自反转填充句，保持词句集合、320token、e/p和问题；替换办公：每行token长度匹配，保持位置/问题，但话题、词汇和重复同时变化。固定e190：旧far事实前缀与各near/mid事实后尾部拼接，p207/255/319，总长度改变，far24行复用。pos64同文统一位置索引+64，6族须与同6族原文比较，不拿12族均值作因果差；没有增加64可见token。d=p−e−1的代数约束意味着三者不能完全分离，当前对照只缩小解释范围。

## 统计、频率与支持量

主16→128，12原留出均保留，A/B先在族内平均。8192整族bootstrap；主种子按字典+index，描述表用共同种子，端点可有小的蒙特卡洛差，点值一致。三假设×两字典Holm6；精确符号互换位置检验假设族误差对称。H2等效取两个边界p最大值；H1至少90%保留、H2比[.8,1.25]、H3至少下降20%均先固定。模板六均值区间/64符号敏感性单列，不称未见模板验证。发现12族探索，旧留出已暴露；多距离/多条件/多token不是新的独立样本。

频率来自各字典旧自然参考300文档/38400位置，完整分组/计数/覆盖与源哈希已核。换入在非左端成员中、固定实际换入预算，按自然参考或发现主任务计数+32参考概率加权无放回抽512次。换出看左端可用数，并按旧排名四档匹配。它们是有限参照模型，不保留未来任务所有边际，更不证明语义重要性。全部共同/进入/退出的数量、比例、原始/相对强度、字典机会、零期待、MC误差和实际家族支持在频率表中。

## 质量与真实失败

全部旧144×两SAE再编码Top32精确一致；checkpoint父模型配置/接口元数据核实。普通逐位置重构相对误差约0.48/0.29，真实h的A/B差重构误差中位数约0.994/0.984，部分>1，保留而不删。该大误差限制语义解释：码的距离不是模型事实信息量。未截断响应只用于测量敏感性，无新字典训练或模型内替换。

原完整候选三距离12/12保留，物品词独立评分64为11/12。补充反转近距F28/stamp错，分差−0.084757，其远距正确；完整原文/每token分数保留。其他办公/固定e三距离12/12，位置索引6/6。它们是合格的负观察，不是测量失败，不剔除。完整候选的后续token/句号分数不能全归到回答前p的激活。

## 偏差、修正与事实资格

冻结前容器缺时区库，改用明确上海UTC+08并保留首次构造输出；未改文本设计。NumPy ID的JSON序列化改显式int，报告列名缺下划线亦修正并归档；没有改统计。复制配置残留旧R19的292/96/旧panel哈希，但代码实际使用372/228与ID表；effective_config.json隔离旧字段，协议A1只澄清元数据，保留原冻结正文和原件。没有因显著性更换模板、家族、指标、阈值或资源。

|结果|原始来源→计算|统计单位|资格与边界|
|---|---|---|---|
|成员/原始与相对强度|全部Top32→pair/member表|族内A/B平均后整族区间|合格；32预算等式不是发现|
|事实幅度/方向|完整30000码→A/B差与RMS归一|12原留出；Holm6|操作判定合格；总信息量Unknown|
|频率参与与机会|固定自然参考+发现计数→条件抽样/排名匹配|族；512参照|描述性/参照模型有限|
|填充/位置对照|228新条件+far复用→同族差分|12族；pos64同6族|长度/填充/索引不能全独立|
|行为|两个候选所有token→完整分差/成对判断|族|非自由生成，非因果证明|
|截断/重构|真实h/preTopK/decoder→阈值/残差|族及描述中位数|质量诊断，不救主假设|

详细设置及文件见[数据定义](dataset_guide_cn.md)、[案例](casebook_cn.md)、[实际资产与复算路径](artifacts_cn.md)。三项审计为处理者自检，不冒充独立人工审查。本轮停止；唯一AI建议的后续问题是保留的码差异哪些被答案读取，不自动设计或执行功能实验。
''')
art=f'''# Actual artifacts and reproducibility

Canonical owner:{C}. [Anchor](anchor.md),[Protocol](protocol.md),[Summary](summary.md),[Detailed](detailed.md),[numeric annex](numeric_evidence.md),[cases](casebook.md),[frequency](frequency.md).

|Artifact|Actual absolute location|Role|
|---|---|---|
|Literal texts,tokenIDs/offsets/candidates|{R/'data/panel.jsonl'}|372conditions,192newtexts,36same-textindexvariants|
|Condition aliases and unchanged splits|{R/'data/condition_mapping.json'};{R/'data/families.json'}|Fixed-e128reusesoldfar,wholefamily12/12|
|Frozen config and effective metadata|{R/'config.json'};{R/'effective_config.json'}|Originalretained;actualcounts/SHAsresolved|
|Oldnative codes/h/preTopK/reconstruction|{R/'cache/ATTN_SAE_old_main.npz'};{R/'cache/MLPIN_SAE_old_main.npz'}|144prefixes×twodictionaries,exactoldTop32|
|Every newraw observation|{R/'cache/new_rows'}|228atomicperconditionNPZ,32IDs/values,preTopK,h,reconstruction|
|All scores|{R/'results/behavior_old.jsonl'};{R/'results/new_rows'}|Bothfullcandidatechains,per-tokenanditem/periodparts|
|All pairing/member/contrast records|{R/'tables'}|baseline_*andcontrols_*;everyfamily/memberincludingzeros|
|Frequency labels/opportunities/support|{R/'data'};{R/'tables/frequency_roles.csv'};{R/'tables/feature_turnover_atlas.csv'}|CompletefixedreferenceCSV/bins,actualIDs,counts/proportions/amplitudes|
|Exact member sets|{R/'results/baseline_membership.jsonl'};{R/'results/controls_membership.jsonl'}|Common,entry,exitIDswithoutdeletion|
|Scripts|{R/'code'}|Construction,scoring,analysis,frequency,case/figure/report,offline replay|
|Freeze,sourceprotection,run/verification/audits|{R/'evidence'}|OriginalR19protected;time/source/hashes/currentassets|
|Original designandfailedversions|{R/'versions'}|Pre-runowners/Protocols,preparationandimplementationhistory|
|Figures|{C/'figures'}|Mainmeetingfigureandcompleteaudits/caseswithprovenance|
|Conversationmemory|{SYS/'.research/memory/conversations/1104-长短程依赖分析/memory.md'}|Noncanonicalappend-onlyworkinglog|
|Resultpacket|{SYS/'daily_research_reports/1104/20261104_R20_distance_composition.zip'}|Portablekeyrawobservations,code,recordsandno-modelreplay|

Model/SAEweights/tokenizerremainintheiroriginalassetpaths;omitted_assets.jsonin thepacketlistsbytes/SHAandavailableoriginalcaches. No new weights were saved or modified. R19source/owners/packetremainunchanged. No commit,pushorexternalpublication.
'''
(C/'artifacts.md').write_text(art);(C/'artifacts_cn.md').write_text('# 实际文件位置\n\n[完整路径与用途清单](artifacts.md)列出372条件全文、原始激活/分数、所有家族与频率表、代码/配置、冻结/审计和记忆。执行根：`'+str(R)+'`。\n\n[认识更新](summary_cn.md)、[案例与反例](casebook_cn.md)、[数字附录](numeric_evidence.md)、[频率](frequency_cn.md)供审阅。原始数据和大缓存保留执行侧，项目只有选定小证据；权重仍是原登记资产，不复制。冻结配置旧字段的限定见effective_config，不改任何数值。未commit/push或外部发布。\n')
rep='''# Reproduction

Extract the result packet and run `python code/offline_replay.py` at itsroot. Python3.10+andNumPysuffice; no model,GPUor network. It recomputes everyrawcandidate-scoresum,everypairednative membership/normchange and allsixprimaryeffect/CI/p/Holmfromsparseobservations. Fullrawencoder/h/reconstructionviewsand statisticalcodeareincludedforadditionalaudit. Metadata/packetmanifestidentifylosslessdeduplicationofrepeateddecodernormarrays,ifapplied;originalscorecacheSHAsrefer toexecution originals,whilepacketmanifestownsthetransformedfiles.

Exact inference environment: torch2.3.0a0+6ddf5cf85e.nv24.04; existingTransformerstree throughPYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3;PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python;TOKENIZERS_PARALLELISM=false;CPU2threads,FP32,SDPA,physical2×328. Weights/loaders/config hashesinconfig.jsonandcurrentstrictassetreceipts. Shanghaihuman-facingtimestampsuseUTC+08;memory/machineeventsretainUTC.

Actualalgorithm:prepare.py→record_design.py→encode_old.py(noLM)→run_forward.pysmoke→run_forward.pyfull(reuses4smoke)→analyze.pybaseline/controls→frequency.pybaseline/controls→control_summary.py→describe.py→frequency_roles.py→quality.py→select_cases.py(fixedruleonoldonly)→figures.py/report.py/write_results.py→verify.pyall→offline_replay.py→curation/assetregistration/package. Case-selectionruleandprimaryformulaswerefrozenbeforederivedresults;implementationhashesprecedeaggregatesupplementalreads. display/reportcodehasnoscientificselectionauthority.

Theforwardrunnerkeepsper-rowatomiccache+scorefilesandverifiessourcecode/cachehashesonresume;neveroverwritescompletedrows. Beforeamodelrerun,useafreshoutputrootandresolvepreservedpre-runowner/protocolversionsagainstthefreeze-resolver;thecurrentownerlatercontainsfactualupdates. Retainfailedversions,notoldsourceedits. No rerun is needed to reviewthese completedresults. Training,interventionsornewconditionsarenotpartoftheofflinecommand.
''';(C/'reproduce.md').write_text(rep);(C/'reproduce_cn.md').write_text('# 复算\n\n解压包后在根目录运行`python code/offline_replay.py`，只需Python/NumPy，不需模型、GPU、网络。从真实稀疏激活与逐token分数重算全部成对成员/范数以及六项主结果的区间和校正p。原始完整h/截断前响应、分组、统计/作图/评分代码均可继续审计。若包去重重复decoder_norm，manifest注明转换；原评分cache_sha指执行原件，包内SHA由包manifest拥有。\n\n重新前向需原模型/SAE权重及原环境，详见[英文执行顺序与环境](reproduce.md)。原件/失败版本/协议修改均保留，复算不授予训练或干预权限。\n')
brief=SYS/'daily_research_reports/1104/meeting_report/meeting_brief_R20_distance_composition_cn.md';brief.write_text(f'''# 长短程认识更新：成员更替不等于事实差异衰减

## 给导师的10秒讲法

物品事实离答案更远时，SAE成员会换，但事实差异没有平均变弱；这个任务窗口里，成员更替不能直接叫作信息丢失。

## 给导师的30秒讲法

我们重算12个留出家族，并补了填充和位置对照。16到128token，Attention平均换掉7.2个成员，MLP换4.1个，但相对事实差异约为近距1.08和1.20倍。换填充、固定事实位置后也没出现平均衰减。多数换入成员此前已有阈值下响应；这个局部观察不等于一般长上下文或因果记忆结论。

## 主图与读法

![距离、成员与事实差异]({C/'figures/main_distance.png'})

左图是仍共同使用的成员数，右图是A/B差的范数相对整体码尺度，再与近距作比。共同成员变少、事实差异幅度仍在可以同时发生。固定六成员方向cos约0.94/0.96不能替代完整码；完整事实差方向约0.60/0.73，幅度与方向必须分开说。

## 必须保留的反例与边界

F11保留较多成员仍有轻微差异减弱；F19的Attention约0.79倍、MLP约1.89倍，回答均正确。反转填充还使近距F28一条失败，分差−0.0848；不能按距离单调解释成功率。原主任务完整候选仍三距12/12，物品词单独评分64为11/12。SAE重构真实A/B差的误差接近1，所以码范数不是模型事实信息量。d=p−e−1也使事实位置/回答位置/距离不能完全独立。

## 唯一值得继续追问的问题（AI建议）

这些随距离重组但未平均衰减的事实差异，哪些真正被答案读取？

本轮不设计或运行相应干预/训练；待共同审阅。[完整结果]({C/'summary_cn.md'}) · [四组全文与反例]({C/'casebook_cn.md'}) · [所有原始数据/方法/代码]({C/'artifacts_cn.md'})。
''')
idx=SYS/'daily_research_reports/1104/README_cn.md';s=idx.read_text();s+='\n- [距离与SAE组合：主图、反例及导师10秒/30秒讲法](meeting_report/meeting_brief_R20_distance_composition_cn.md)；R20结果包：`20261104_R20_distance_composition.zip`。\n';idx.write_text(s)
# Factual owner update after preserving original scientific design bytes.
for anchor in [A,A.with_name(A.stem+'_cn.md')]:
 s=anchor.read_text();start=s.index('## 7.');end=s.index('## 8.',start);text=(f'## 7. Current Evidence\n\nR20completed{local}. [Summary]({C/"summary.md"}) owns the bounded interpretation; all12old heldoutfamilies retained.16→128meancommon24.79/32and27.92/32;normalizedfact-separationratios1.0803and1.1989. H1≥90%retentionnot supportedboth;H2toleranceequivalence supportedAttention,MLPinsufficientbecauseuppergrowthexceeds1.25;H3≥20%attenuationnot supportedboth. All228controlscompletedwithoutweightchanges;reverse/content/fixed-emeanratiosremainabove1. F28reverse16isaretainedfailure;alloriginalmainpairedrates12/12. Fact-differencereconstructionerrors≈.994/.984limitsemanticinformationclaims. [Detailed]({C/"detailed.md"}) recordsmetadataA1/quality/lineage. ScientificacceptanceUnknown;nofunctionalintervention/training.\n\n' if not anchor.stem.endswith('_cn') else f'## 7. 当前证据\n\nR20于{local}完成事实记录。[Summary]({C/"summary_cn.md"})拥有认识更新，全部12原留出保留。16→128平均共同24.79/32、27.92/32；相对事实差异比1.0803、1.1989。H1至少90%保留两侧未支持；H2容差内等效Attention支持、MLP因增长区间上界大于1.25而不足；H3至少20%平均衰减两侧未支持。228对照完成且权重保持，反转/办公/固定e均值比>1。保留反转近距F28失败，旧主候选三距12/12。事实差重构误差约.994/.984限制信息量解释。[Detailed]({C/"detailed_cn.md"})保留A1元数据澄清及证据链。科学接受Unknown，无功能干预/训练。\n\n');anchor.write_text(s[:start]+text+s[end:])
for f in [FOCUS,FOCUS.with_name(FOCUS.stem+'_cn.md')]:
 s=f.read_text().replace('`AUTHORIZED_EXECUTION`','`COMPLETED_AWAITING_REVIEW`').replace('`NOT_RUN_THIS_ROUND`','`FACTUAL_COMPLETE_SCIENTIFIC_REVIEW_PENDING`');s+=f'\nResults: [Summary]({C/("summary_cn.md" if f.stem.endswith("_cn") else "summary.md")}). Next scientific choice remains researcher-owned; STOP before any follow-up.\n';f.write_text(s)
resolved=[]
for f in [A,A.with_name(A.stem+'_cn.md'),FOCUS,FOCUS.with_name(FOCUS.stem+'_cn.md'),C/'protocol.md',C/'protocol_cn.md']:
 original=R/'versions'/f.name;resolved.append(dict(path=str(f),frozen_sha256=sha(original),preserved_original=str(original),current_sha256=sha(f),reason='Factual owner update or append-only metadataA1; no scientific metric/data change'))
dump(R/'evidence/freeze_resolution.json',dict(UTC=stamp,local_time=local,records=resolved,scientific_acceptance='Unknown',original_protocol_body_preserved=all((C/name).read_bytes().startswith((R/'versions'/name).read_bytes()) for name in ['protocol.md','protocol_cn.md'])))
ledger=[dict(task=t,status=status,evidence=ev,missing_dependency=None) for t,status,ev in [('R19input/token/frequency/scoreaudit','DONE_VALID','evidence/R19_replay.json;evidence/frequency_validation.json'),('membership/strength/threepairedgaps','DONE_VALID','tables/baseline_pair_metrics.csv;tables/baseline_member_values.csv'),('full/Six/raw/relativefactcontrasts','DONE_VALID','tables/baseline_fact_contrasts.csv;results/primary_hypotheses.json'),('behaviorandperiodsensitivity','DONE_VALID','tables/*behavior*;supplement_failures.md'),('frequencycounts/proportions/opportunities/IDs','DONE_VALID','tables/*frequency*;tables/feature_turnover_atlas.csv'),('fourrulechosencasesandcounterexamples','DONE_VALID','results/case_selection.json;cases/'),('228boundednewforwardcontrols','DONE_VALID','evidence/full_complete.json;tables/control_family_differences.csv'),('template/multiplicity/reconstruction/thresholdchecks','DONE_VALID','evidence/final_three_audits.json;tables/reconstruction_quality.csv;tables/threshold_summaries.csv'),('discoverysideobservations','DONE_EXPLORATORY','tables/*split=discovery'),('mainfigure/auditfigures/shorttalk/code/config','DONE_VALID','figures/;meetingbrief;code/;effective_config.json')]];dump(R/'evidence/task_coverage.json',dict(UTC=stamp,entries=ledger,excluded_by_scope=['competition-error mechanism','functional interventions','training','universal pure-distance law'],resource_gaps=[]))
print('FINAL_DOCS',local)
