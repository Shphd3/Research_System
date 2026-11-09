from common import *
import os,re,shutil
assert not (R/'evidence/freeze.json').exists()
cfg=json.load(open(R/'config.json'));stamp=now();local=local_now()
focus_en=f'''# Distance and the feature combination at the answer position

problem_key: `当同一事实距离回答位置越来越远时，回答位置的 SAE feature 组合怎样变化？`
anchor_id: `15_27_12`
question_state: `USER_ACTIVATED`
design_state: `FROZEN_BOUNDED_DISTANCE_OBSERVATION`
task_state: `AUTHORIZED_EXECUTION`
result_state: `NOT_RUN_THIS_ROUND`
scientific_acceptance: `Unknown`

The current user asks for a complete, auditable analysis of distance16/64/128: membership, raw and relative strengths, fact-contrast magnitude and direction, frequency opportunities, cases and bounded controls. The question does not presume degradation. Three steps: verify/recompute R19 without modifying it; analyze all family-paired sparse vectors and execute the declared filler/position controls; deliver uncertainty, counterexamples and one meeting figure. Stable composition, turnover with retained contrasts, and weakened contrasts are distinct possible outcomes. A wide interval or unavailable dependency is insufficient, not evidence of absence. No competition-error mechanism, feature intervention or training is in scope. Next decision: review which distance-associated changes remain after the controls, then choose one unresolved question. Current execution is explicitly authorized without intermediate confirmation; operational definitions are AI choices under that scope, not scientific acceptance.

[Anchor]({A}) · [Protocol]({C/'protocol.md'}).
'''
focus_cn=f'''# 距离改变时，回答位置的 feature 组合怎样变化

problem_key: `当同一事实距离回答位置越来越远时，回答位置的 SAE feature 组合怎样变化？`
anchor_id: `15_27_12`
question_state: `USER_ACTIVATED`
design_state: `FROZEN_BOUNDED_DISTANCE_OBSERVATION`
task_state: `AUTHORIZED_EXECUTION`
result_state: `NOT_RUN_THIS_ROUND`
scientific_acceptance: `Unknown`

本轮由当前用户明确激活并授权完整执行：核验R19，分别检查16/64/128距离的成员、原始与相对强度、事实差异幅度/方向、频率机会、案例和适量对照，不预设距离一定造成退化。三个步骤：保护原件并重算；完成全家族分析及填充/位置补充前向；交付区间、反例和组会主图。组合基本稳定、更替但差异保持、差异减弱是分开的可能结论；区间宽或资源缺口保留证据不足。不研究竞争答错机制，不做feature干预或训练。下一决定是共同审阅哪些变化在对照后仍出现，再选择唯一一个未解问题。无需中途再确认；具体操作定义由AI在本次完整执行授权内固定，不冒充研究者科学接受。

[Anchor]({A.with_name(A.stem+'_cn.md')}) · [Protocol]({C/'protocol_cn.md'})。
'''
FOCUS.write_text(focus_en);FOCUS.with_name(FOCUS.stem+'_cn.md').write_text(focus_cn)
en=f'''# Distance-associated changes in answer-position SAE combinations

## 1. Problem Definition

When the same object fact is16,64or128tokens from the answer position, how do the members, amplitudes and fact contrasts of its SAE representation change? This inherits the natural-language context-response question, using R19's behaviorally usable object-fact task. R19 established member overlap and six-member contrast direction; it did not establish unchanged magnitude. The present uncertainty is whether turnover accompanies retained or weaker fact differences, and how filler/position covariation limits attribution. The user's purpose is descriptive discrimination among these possibilities, not a mechanism presuming degradation. Support narrows the observed pattern; non-support rules out that operational claim only; insufficient evidence preserves uncertainty. Competition-error mechanisms, interventions and training are excluded.

## 2. Physical Priors

A nonnegative Top32 code has a fixed active budget: member changes, common-member strength changes and full-code scale are different observables. Unit normalization removes scale. Absolute evidence index e, answer index p and gap d obey d=p−e−1, so all three cannot vary independently. These are mathematical/implementation constraints; no causal memory-loss prior is assumed.

## 3. Falsifiable Hypotheses

AI operationalizations under the explicit complete-study scope: H1 membership is approximately stable (mean16→128retained fraction at least0.90). H2 the full-code fact-contrast norm, relative to total code scale, remains within[0.8,1.25]of near (a local tolerance, not a universal ability standard). H3 that relative fact contrast decreases by at least20%. These are distinct from positive contrast-direction alignment. Live alternatives are substantial turnover with stable/increased fact contrast, generic activation gain, Top32ranking, filler variation and position covariation. No threshold is changed after results. New controls are supporting checks of attribution, not new gates selected for passing.

## 4. Mathematical Model

For one dictionary, z is the30000-dimensional post-ReLU/Top32 vector at the last answer-prefix token; inactive coordinates equal observed post-truncation zero. Let S be its32positive indices. For factA/B at distance d, delta_d=z_A,d−z_B,d. Separate its raw norm from relative separation s_d=||delta_d||/sqrt((||z_A,d||²+||z_B,d||²)/2). The primary magnitude change is log(s_128/s_16); contrast direction is the cosine between deltas, reported independently. Common-member norm ratios and cosines distinguish amplitude from relative arrangement. Squared full coordinate change decomposes exactly into common-member changes plus entering amplitudes plus exiting amplitudes; it is not hidden-space energy or output attribution. Existing six IDs remain fixed with zeros and their strict-support sensitivity.

## 5. Computational Realization

Reuse144main R19prefixes (24families×2facts×3distances), their exact scores/h/Top32and the two native block27SAEs separately. Primary families are the old12heldout, already exposed; discovery12is exploratory, not refit. Re-encode saved h without an LM forward to verify Top32and inspect pre-truncation ReLU responses. Complete30000-coordinate post-Top32 is primary; untruncated responses and decoder/hidden differences are truncation/reconstruction diagnostics, not a replacement dictionary.

Execute228new forward conditions in the same frozen model:72reverse-order weather prefixes,72length-matched office-filler prefixes,48fixed-evidence-near/mid prefixes,36uniform+64position-index shifts in six template-covering families. Fixed-e128reuses24old far rows. Reverse/content keep p319/e302,254,190; fixed-e keeps e190and p207,255,319; uniform position shifts keep identical tokens/visible positions and change only supplied position IDs. The latter isolates an encoding-coordinate shift, not added visible context. New controls remain limited by filler amount/order and cannot identify a pure universal distance effect.

## 6. Minimal Falsification Tests

All12heldout families remain in full-code analyses; do not select by six-member support or behavior. Aggregate facts within family, then bootstrap8192families and report exact paired sign-swap tests with a six-test Holm family (two dictionaries×H1–H3). H1passes only with lower95%interval≥0.9and corrected p≤.05; an upper interval<0.9does not support it. H2requires a95%ratio interval entirely within[.8,1.25]and corrected two-boundary equivalence test; an interval wholly outside does not support it. H3requires upper ratio interval<.8and corrected boundary test; lower>.8does not support a20%decline. Otherwise insufficient. Preserve direction/raw norms, all three distance pairs and template sensitivities. Frequency changes use group base counts, at-risk exits, rank-matched exits and reference/discovery-weighted entry opportunities. No arbitrary group size becomes semantic importance.

## 7. Current Evidence

R19reported24.79/32Attention and27.92/32MLP common members for16→128on12heldout families. Its strict six-member direction cosines0.9678(N6)and0.9713(N11)do not establish constant amplitude. Allthree full-candidate paired accuracies were12/12; period sensitivity remains separate. Current R20recomputation and controls are NOT RUN. Construction and current strict asset access are verified; scientific acceptance remains Unknown.

## 8. Claim Boundary And Next Decision

This round can describe within-family code changes in this task, model, hooks and16–128gap window, and test robustness to declared filler/position changes. It cannot establish a causal distance mechanism, semantic atom identity, general long-context law, intervention utility or router-training value. Old heldout is exposed and shared templates limit extrapolation. Deliver all raw pairs, four rule-chosen cases/counterexamples, main/audit figures and10/30second explanations, then stop for researcher review. The one next decision is which remaining explanation most needs a distinguishing check; no follow-up is launched automatically.
'''
cn=f'''# 回答位置的SAE组合随事实距离怎样改变

## 1. 问题定义

同一物品事实距回答位置16、64、128tokens时，组合成员、强弱和事实差异怎样改变？本题继承自然语言上下文响应方向，采用R19行为可用的任务。旧结果展示成员重叠及六成员差异方向，未证明幅度不变。本轮区分组合基本稳定、更替但差异保持、差异减弱；检查填充与位置共变。不预设记忆退化，不研究竞争答错机制、干预或训练。支持只限定当前可观察模式；未支持仅针对操作假设；区间宽保留不足。

## 2. 约束与先验

Top32是固定的阳性预算，成员改变、共同成员强弱与全局尺度是不同对象。单位归一化会去掉尺度。证据位置e、回答位置p、距离d满足d=p−e−1，三者不能全独立操纵。这些是计算约束，不是距离造成遗忘的因果先验。

## 3. 可证伪假设

在当前完整执行授权内由AI预先固定操作口径：H1成员基本稳定（16→128平均保留比例≥0.90）；H2完整码中相对于总体尺度的事实差异幅度保持在近距的[0.8,1.25]；H3该相对差异至少减弱20%。这些不是模型普适标准，也不同于差异方向相似。可信替代包括更替但差异保持/增强、总体激活增益、Top32排名、填充或位置影响。结果后不改阈值；对照不作为挑选过关条件。

## 4. 数学对象

每套字典的z是回答前最后token处30000维ReLU/Top32码，未列坐标是截断后的实际零。S是32个阳性ID。每族两事实之差delta_d=z_A,d−z_B,d。原始幅度||delta_d||与相对差异s_d=||delta_d||/sqrt((||z_A,d||²+||z_B,d||²)/2)分开；主要幅度改变为log(s_128/s_16)，差异方向另用cosine报告。共同成员的范数比与方向分别看幅度/搭配。全坐标平方改变严格分成共同成员改变、换入幅度、换出幅度；不是隐藏空间能量或输出贡献。旧六成员ID固定，缺失置实际零，同时保留旧严格支持敏感性。

## 5. 可执行实现

复用144条旧主任务（24族×两事实×三距离）的真实全文、评分、h与Top32，两个第28层原生SAE分开。旧12留出是主分析单位，但已暴露，不能称全新确认；发现12族仅探索。保存的h离线再编码，核对Top32并看截断前ReLU；完整30000维截断码是主要对象，未截断码、decoder/hidden差仅作截断/重构诊断。

新增228条件：72条反转天气填充、72条同token长度替换办公填充、48条固定事实e的近/中距文本、六模板覆盖家族的36次统一位置索引+64。固定e的24条远距复用旧数据。前两组保持p319与e302/254/190；固定e190时p为207/255/319；位置索引组保持真实文本/可见位置，只移动供给模型的position IDs，检验编码坐标而不是增加可见上下文。填充量、顺序和位置仍不能完全分离。

## 6. 最小判别与判定

完整码分析保留全部12留出族，不按行为或六成员共同支持筛选。族内先汇总两事实，再做8192整族bootstrap和精确成对符号互换；两字典×三主假设共六项Holm。H1需95%区间下界≥.9且校正p≤.05，上界<.9为未支持。H2需95%比值区间全在[.8,1.25]且双边界等效检验通过；全在区间外为未支持。H3需比值上界<.8且边界检验通过；下界>.8为未支持20%下降。其余不足。方向、原始尺度、三个配对与模板敏感性分别保留。频率统计保留组基数、可换出成员、按旧排名匹配的换出参照，以及自然参考/发现任务频率加权的换入机会。

## 7. 当前证据

R19留出16→128平均共同成员Attention24.79/32、MLP27.92/32；旧严格六成员方向cos分别0.9678（6族）、0.9713（11族），不等于幅度不变。三个距离完整候选成对均12/12；去句号敏感性另列。本轮重算/补充对照尚未运行。构造及当前资产可读检查已核，不构成科学接受。

## 8. 边界和下一决定

仅回答此任务/模型/两接口/16–128区间的配对码变化与已列对照，不推出因果距离机制、语义feature身份、一般长上下文规律、干预或router价值。旧留出已暴露且模板共享。交付全部原始对、规则选择四案例/反例、主/审计图和10/30秒讲法后停止。唯一下一决定由研究者共同审阅后选择最值得区分的剩余解释；不自动开展后续。
'''
A.write_text(en);A.with_name(A.stem+'_cn.md').write_text(cn)
for name,target in [('anchor.md',A),('anchor_cn.md',A.with_name(A.stem+'_cn.md'))]:(C/name).symlink_to(os.path.relpath(target,C))
sections=[
('0. Approval Snapshot',f'APPROVED_FOR_BOUNDED_LOCAL_REANALYSIS_AND_CONTROLS, {local} (UTC {stamp}). Current user explicitly requests complete execution without intermediate approval. User owns the question and final scientific judgment; operational metrics/tolerances below are AI definitions under this execution scope, not human scientific acceptance. Role: metric audit plus robustness check. [Focus]({FOCUS}) and [Anchor]({A}). No training, probe fitting, interventions or competition-error mechanism.'),
('1. Terminology / Definitions','Token gap d=p−e−1 excludes both endpoints; e last item token, p last prefix token. Base length320,p319ID25. Native dictionaries each30000,ReLU Top32; unselected coordinate=post-truncation zero, not proof of zero encoder response. Raw scale and unit-vector direction are separate. Family is the resampling unit; A/Blabels are local words.'),
('2. Anchor Alignment','Question: how answer-position combinations change with distance, without assuming degradation. Main rival: apparent fact weakening is global gain/truncation/filler/absolute-position covariation. Old R19 six-member cosine is not an amplitude measurement. All original records/weights remain byte-preserved; new owner15_27_12 and R20only.'),
('3. Tested Hypothesis','H1 mean full-native16→128same-fact member retention≥.90. H2 full-native normalized fact separation ratio in[.8,1.25]. H3 normalized separation decreases≥20%. The .90and20% tolerances are explicit local operational choices. Contrast direction is independently reported; no direction pass implies amplitude pass. No score-dependent feature selection.'),
('4. Rival Explanations','Whole-code gain, differing object priors, common-question members, rank-threshold crossing, lexical/template specificity, changed filler/order, changed e/p, and incomplete SAE reconstruction. Use raw and scale-normalized metrics, full30000coordinates, fixed6sensitivity, fact-swapped reference, preTopK/h/decoder diagnostics and four supporting control frames.'),
('5. Data Construction And Provenance','R19main144rows:24families×A/B×16/64/128. Retain12old discovery/12old heldout by entirefamily. Both responses/sparse representations were already exposed; no fresh-confirmation claim. Literal baseline filler multiset identical across distances. Reverse filler independently inside before/after-fact blocks, preserving role/e/p/length/multiset. Content replaces each weather sentence by a deterministic office sentence of identical tokenizer length, same replacement for a sentence across distances; final question unchanged. Fixed-e uses the old far prefix through the fact plus each old near/mid post-fact tail: e190,p207/255/319,far reused. Pos64supplies all position IDs+64on identical old text, in first heldout family per six templates. This changes encoding indices, not visible token count. Whole data/text/token/role/answer-word counts verified before any model forward.'),
('6. Learning Task And Permitted Supervision','No learning task. Read complete candidate log probabilities and frozen SAE activations. Discovery task-frequency counts are a descriptive baseline, not trained parameters. No regression/probe/model/dictionary fit, labels for optimization, gradients or optimizer.'),
('7. Model / Architecture And Frozen Variants','Exact R19officialQwen3-0.6B Base/tokenizer/nativeSAEweights/loaders/hashes fromconfig. ATTN: block27.self_attn.o_proj output before residual. MLPIN: actual block27.mlp preinput after residual+post_attention_layernorm. Separate IDspaces. Native lm_head, FP32CPU2threads,SDPA,physical2×328. Capture actualp (319/207/255); full candidate strings preserve leading space/item/period. Onlypos64changes explicit position_ids. Saved h is re-encoded offline with native weights, one row at a time to match original rounding.'),
('8. Training Objective And Optimization','NOT APPLICABLE. All model and SAE parameters require_grad=False, inference_mode, no optimizer or weight update. Reuse R19native loader/scorer with dynamic capture position and optional position-IDoffset; do not reuse training scaffolds. NativeTop32exactness,no-ophooks and oldscore replay protect adaptation.'),
('9. Conditions, Seeds, And Checkpoints','Seed2026110420. Supplemental228new forward conditions:reverse72,content72,fixed_e48,pos6436. Four smoke new conditions are reused in full stage; six old calibration prefixes cover six templates, so234scored forwards plus one no-ophook check. No new checkpoints. CPUstage ceiling1800s; no GPU/cloud escalation. Per-row atomicNPZ+JSONpermits resume without rerunning completed rows. A failed dependent stage is retained and independent offline analysis continues; no silent substitution or tolerance widening.'),
('10. Primary Metric And Frozen Analysis Plan','Primary16→128,each dictionary separately,all12heldout families. H1retention=mean_A/B(|intersection|/32). Factdelta=z_A−z_B; S=||delta||/sqrt((||z_A||²+||z_B||²)/2), x=log(S128/S16). H2uses x within±log1.25,H3x<−log1.25. Bootstrap8192wholefamilies(seed2026110420+siteindex)of the family mean; exp endpoints for ratio. Exact2^12sign swaps,one-sided signed-mean upper tails: H1test(retention−.9),H2max(test(x+log1.25),test(log1.25−x)),H3test(−x−log1.25). Sixp-values Holm-adjusted. Sign-swap location tests assume symmetric independent family errors; show shared-template sensitivity using six template means/64swaps. No clipping,outlier deletion or relabeling. If a norm is zero, recordNAand actualN; fewer8eligible families is insufficient. Old6fixed list includes zeros for all12,with original strict-support replay only a sensitivity.'),
('11. Secondary Metrics And Guards','Allthreepairs and allfamilies:shared/entry/exitcounts,Jaccard; complete-ID/raw-value lists; full andcommon norm ratios/cosines; per-row normalized strength differences. Exact coordinate-L2change decomposition common/entry/exit. Fact raw delta norm, S, unit-row contrast norm anddirection, raw/C6/relativeC6/preTopK/hidden/decoder views. PreTopK ReLU is truncation diagnostic,not the trainedTop32code. Decoder-weighted absolute atom change is descriptive,not output contribution/hidden energy. Threshold diagnostic: rank≥25orvalue/cutoff≤1.25,encoder responses both sides and absolute prechange divided by mean cutoff. Native reconstruct errors and fact-difference reconstruction error retained. Full/item-only/period scores separate; original complete paired rates must replay12/12at alldistances.'),
('12. Known Good / Known Bad / Known Confusing Cases','Known calibration: old candidate scores and nativeTop32. Known confusion: F23MLP#25508is zero inmain16_A; keep it,not drop family. F28word-only64can fail despite full-string success. Cases selected after main recomputation only for illustration by a rule frozen now: stable=maxshared fraction averaged acrosssites/facts16→128;changing=min;attenuating=minmean logSratio excludingprevious;counter=oppositesign to overallmedianlogratio with largest magnitude,excludingprevious; if no opposite sign,largest cross-site disagreement and explicitlysaynone. Tie familyID, four unique heldout families. Show both facts,allthreefulltexts,allmembers/rawvalues/frequencygroups/scores; no case-based significance.'),
('13. Scientific Procedure And Stage Contracts','Prepare/ownerfreeze→offlineR19reconstruction+metricbaseline→smoke4new+6old/no-op→fullremaining224new→registeredmetrics/controlcontrasts→figures/cases/threeaudits/summary+10/30secondbrief→verify+register+localreadingsync→STOP. Smokerequires:role/tokenchecks,positive32,exactnativeencoder,no-op0,laneerror<1e−5,oldscores<2e−5;uniformpositioncontrolnumerics are an observed result,not a gate forced to0. If models unavailable,completeofflinefromsavedarrays; prespecifymissingforwardrows andactualreason. Per-row durableoutputs and stagepid/time/throughputrecorded. No template tuning based on whether a hypothesis passes.'),
('14. Algorithm, Output, And Provenance Contract','Fullcode/densepreTopK/h/cache execution-sideR03; canonical bilingualAnchor/Protocol/Summary/Detailed,data+methodguide,allfamily tables,casebook,figures,artifactindex. ReferencegroupD1natural300docs/38400positions,count≥20anddocs≥5,edgesATTN35/70MLP33/62;insufficient/zero separate. Group opportunities:dictionaryeligiblecounts; at-riskleftpositions; rank-matched exits bins1–8/9–16/17–24/25–32. Entryconditionalnull512weightedwithoutreplacementdraws from inactive-at-left features, conditioning on actual entrycount,using referencep=count/38400; taskbaselineweights=discoverymainpositivecount+32×referencep. Never use heldout to fitweights;zeroexpectedgroup is uncalibrated,not infiniteenrichment. Save per-pair nullmean/MCerror andfamilyintervals; these are descriptive conditionalmodels,not additional primaryp-tests. Contrastcontrols always withinfamily,deltas andtemplateintervals; exploratorydifferences do not replace primary verdicts.'),
('15. Success / Failure / Insufficient Evidence','H1support ifN≥8,95%lower≥.9andHolmp≤.05;not supportedifupper<.9;otherwiseinsufficient. H2support ifN≥8,95%ratioCIinside[.8,1.25]andHolmp≤.05;not supportedifCIwhollyoutside;otherwiseinsufficient. H3support ifN≥8,95%upperratio<.8andHolmp≤.05;not supportediflower>.8;otherwiseinsufficient. Above1.25is an allowed observed increase,not degradation. Support is an operational data judgment,not scientificacceptance. Secondaryanalyses cannot rescuefailedprimary. Reportallresults evenwhen anotherdictionary/controlfails.'),
('16. What This Cannot Claim','No pure universaldistanceeffect: d=p−e−1,changing visiblelengthalsochangesfiller/context; uniformpositionIDs is a restrictedencodingcontrol. Sharedtemplates,alreadyexposedholdout,smallN,limiteddistances/objectpairs,SAElossandTop32remain. RawpostTopKdelta/normalizeddelta/direction are dictionary observables,not causal use or semantic capacity. No competitor-erroranalysis,intervention,routertrainingorautomaticfollowup.'),
('17. Block Confirmation, Freeze, And Amendment Ledger',f'Aquestion/userpurpose confirmed by currentprompt;Bobservationaldesign delegated by completeexecutionrequest;Cdata/splits/assets verified;Dnativeinterfaces verified;Eobjective/optimizationNA;Fmetric/uncertaintyAIoperationalizations fixed above;Gboundedlocal228conditions explicit necessarycontrolscope. Cross-blockself-auditPASS,three audits stored. ScientificacceptanceUnknown. Frozen before newanalysis/forward at{local}. Preserve full protocol bytes; later changes append ID/time/before-after/reason/visibledata/affectedconditions/authorization/eligibility andretainoriginalversion. No new metric/threshold chosen afterresults. First summary may give requested operational hypotheses and one AI-suggested question,without researcher mechanism acceptance.')]
prot='# Protocol: R20 distance and answer-position combinations\n\n'+'\n\n'.join('## '+name+'\n\n'+text for name,text in sections)+'\n';(C/'protocol.md').write_text(prot)
cnintro=f'''# R20协议：距离与回答位置组合

## 授权与冻结

当前用户明确授权完整重算、必要补充实验与交付，不中途等待确认。冻结时间{local}（UTC{stamp}）。问题由用户确认，以下阈值/计算细节为AI在授权内固定的操作口径，不冒充普适标准或研究者科学接受。机制判断Unknown。不训练，不干预，不研究竞争答错。

## 数据、模型与识别

复用R19主144条，24族各两事实×三距离；原12留出为主要单位但已暴露，12发现仅探索。两个原生SAE各30000/Top32：第28层Attention投影输出、实际MLP输入，ID不跨字典相认。原prefix320，p319，e302/254/190，d=p−e−1排除两端。当前模型/SAE/reference资产strict通过，原件哈希保护。

新前向228条件：反转填充72、同token长度办公填充72、固定e190的近/中距48、六模板覆盖族position IDs统一+64的36；固定e远距24条复用。前两者固定e/p/token数，固定e组p207/255/319；位置索引组不改可见文本/位置。三变量仍不能完全分离。四smoke并入正式结果不重跑，六旧校准另列；共234条评分前向和一次无操作校验。CPU2线程/FP32/SDPA/物理2×328，每阶段1800秒，不升级GPU/云资源；单条原子保存，可从已有条目续跑。

## 主要量与判定

全部12留出保留，事实先在族内平均，不按六成员或答题好坏筛选。主比较16→128。H1平均共同成员/32≥.90；H2完整30000维截断码中，相对事实差异比保持[.8,1.25]；H3相对差异至少降20%。令delta=z_A−z_B，s=||delta||/sqrt((||z_A||²+||z_B||²)/2)，x=log(s128/s16)。幅度与delta方向cos独立报告。两字典×三假设共六p做Holm；8192整族bootstrap；精确2^12符号互换，假设位置误差对称。等效p取两边界单侧p的最大值，H3检验−x−log1.25；模板六均值/64符号敏感性另列。H1区间下界≥.9/H2比值区间全在[.8,1.25]/H3比值上界<.8，同时校正p≤.05且N≥8才支持。H1上界<.9、H2全在范围外、H3下界>.8分别未支持；其他不足。增大也是合法观察，不改口径找退化。方向相似不代替幅度不变。

## 完整分析与频率机会

三个距离对分别保留成员ID/频率/原始与相对强度，共同/换入/换出、全码与共同成员范数/方向。平方坐标改变分解为共同改变+换入+换出，不是隐藏能量或输出因果贡献。旧六ID固定、缺失为实际零，旧严格子样本只复核，不替代全族。保存h离线再编码核对Top32，截断前ReLU仅作阈值敏感性；看排名25–32、激活/阈值≤1.25、换入之前的未截断响应，避免把掉出Top32当作真实消失。

频率复用独立D1参考300文档/38400位置，count≥20且doc≥5；Attention35/70、MLP33/62，零和不足单列。列组字典基数、左端可换出数、旧排名四档匹配的换出期待；换入在非左端成员里按参考频率无放回抽512次，固定实际换入数。另用发现主任务出现次数+32×参考概率作任务机会敏感性，不用留出拟合。期待零只报告未校准，不算无穷富集。这些为描述性机会模型，不增设主要检验。

## 案例、可靠性与交付

规则先固定：四个不重复留出族，依次取两字典平均共同成员最多、最少、剩余中平均相对事实差异log比最小、与总体中位趋势反号且幅度最大的族。若无反号，取字典分歧最大并说明没有反号；平手按ID。仅为展示，不用案例作统计确认。两事实三距离全文/评分/频率/全部成员保留。F23低频成员零和F28物品词/句号不同结果作为已知混淆校验。新增对照无论支持与否都保存；资源缺口只阻塞依赖部分。

阶段：构造/冻结→旧缓存重算→4新+6旧smoke→其余224新前向→预定统计/对照→三审计/案例/图/双语Summary与Detailed→实际资产登记/核验/本地阅读同步→停止。旧文件保护、原生编码/无操作/候选前缀校验、逐token分数与实际距离独立复算。主要结果、探索与新增前向分别标记。交付主图、全审计图、10秒/30秒讲法及唯一一个AI建议的后续问题；科学接受与后续执行待共同审阅。

## 原版和变更

英文[完整协议](protocol.md)拥有逐项设置，与本中文说明一致。冻结后不改科学正文；变更必须追加时间、前后值、原因、已见数据、影响、权限和证据资格，保留原版本。不因结果不显著而换定义或模板。
''';(C/'protocol_cn.md').write_text(cnintro)
for f in [A,A.with_name(A.stem+'_cn.md'),FOCUS,FOCUS.with_name(FOCUS.stem+'_cn.md'),C/'protocol.md',C/'protocol_cn.md']:shutil.copyfile(f,R/'versions'/f.name)
audits=[dict(kind='scientific_identification',status='PASS',question='distance-associated combination change, no presumed degradation',rival='gain/truncation/filler/position',limits='p-e-ddependent; no pure causal distance claim',human_scope='Current complete-study request; mechanism acceptanceUnknown'),dict(kind='data_statistics',status='PASS',families=24,primary12=True,exposure='oldheldoutalreadyexposed',unit='wholefamily',multiplicity=6,frequency='fixedindependentreference;discoveryonlytaskopportunity'),dict(kind='implementation_numerics',status='PASS_BEFORE_SMOKE',parameters_trainable=0,optimizer=False,hashes='sourceweights/currentstrictchecks',smoke='exactnativecode,no-op,lanes,oldreplay',resume='per-rowatomicrecords',runtime='samecurrentCPUcontainer;2threads,1800s/stage')]
dump(R/'evidence/pre_run_audits.json',dict(UTC=stamp,audits=audits,scientific_acceptance='Unknown'))
paths=[R/'config.json',R/'data/panel.jsonl',R/'data/condition_mapping.json',R/'data/R19_candidates.json',A,A.with_name(A.stem+'_cn.md'),FOCUS,FOCUS.with_name(FOCUS.stem+'_cn.md'),C/'protocol.md',C/'protocol_cn.md']
dump(R/'evidence/freeze.json',dict(UTC=stamp,local_time=local,hashes={str(p):sha(p) for p in paths},old_results_visible=True,new_forward_reads=0,code_gate='Each executable implementation is hashed in its stage receipt before output; core formulas and selection fixed here'))
mem=SYS/'.research/memory/conversations/1104-长短程依赖分析/memory.md';s=mem.read_text();s=re.sub(r'^Latest update at: .*$', 'Latest update at: '+stamp,s,flags=re.M);s+=f'\n\n## {stamp} -- 用户授权R20纯距离问题，原件保护与协议冻结\n\nProcessed by: Codex /root (harness: Codex desktop; model: GPT-6)\n\n- Summary: 用户要求完整核验/离线分析/必要补实验/组会结果，不预设退化，不研究竞争错误或训练/干预。新15_27_12/R20，不改R19。12旧留出已暴露；幅度与方向分开，完整Top32与固定六成员都保留零。\n- Current work: 构造228新增条件：填充反转/等长换内容/固定e/位置编码平移，当前strict资产通过，实际协议与操作判据冻结，尚无新前向。\n- Next action: 旧h离线重编码→smoke→剩余对照→逐家族/频率机会/案例/图/报告→核验交付并停止。无中途重复审批；科学接受Unknown。\n- References: {A}; {C/"protocol.md"}; {R/"evidence/freeze.json"}; {R/"evidence/R19_protected_snapshot.json"}.\n';mem.write_text(s)
print('FROZEN',local)
