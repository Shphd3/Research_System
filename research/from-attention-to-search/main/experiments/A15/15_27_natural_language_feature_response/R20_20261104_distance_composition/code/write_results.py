from common import *
from stats import *
from report import md,n,main_table,ph,ct,bh,freqt,fn
import pandas as pd
quality=pd.read_csv(R/'tables/reconstruction_quality.csv');offset=pd.read_csv(R/'tables/position_id_shift_audit.csv');atlas=pd.read_csv(R/'tables/feature_turnover_atlas.csv');threshold=pd.read_csv(R/'tables/threshold_summaries.csv')
tn=[]
for site in SITES:
 q=quality[(quality.site==site)&(quality.frame=='baseline')&(quality.split=='heldout')];a=pd.concat([q.relative_row_error_A,q.relative_row_error_B]);tn.append([site,float(a.median()),float(q.fact_relative_error.median()),float(q.reconstruction_fact_cosine.median()),float(q.reconstructed_fact_norm.median()/q.hidden_fact_norm.median())])
qt=md(['字典','逐位置重构相对误差中位数','事实差重构相对误差中位数','事实差重构方向cos中位数','重构/真实差范数中位数之比'],tn)
frows=[]
for site in SITES:
 for group in GROUPS:
  for role in ['entered','exited']:
   q=atlas[(atlas.site==site)&(atlas.frame=='baseline')&(atlas.split=='heldout')&(atlas.group==group)&(atlas.distance_left==16)&(atlas.distance_right==128)&(atlas[role+'_positions']>0)].sort_values([role+'_families',role+'_positions','atom'],ascending=[False,False,True]).head(2)
   frows.append([site,group,role,'; '.join(f'#{int(r.atom)}: {int(r[role+"_families"])} families, mean z={n(r[role+"_mean_z"])}' for _,r in q.iterrows()) or 'none'])
# Correct field lookup in a compact atlas without redefining candidate features.
for row in frows:row[-1]=row[-1].replace('families,','families,')
freqdoc='# Frequency groups: support, opportunities and literal IDs\n\n'+freqt+fn+md(['dictionary','reference group','role','Literal examples ranked by family support, then count and ID'],frows)+'\nThese are descriptive reading examples, not new candidates. All IDs, entry/exit families and raw values remain in feature_turnover_atlas.csv and *_member_values.csv. Groups retain the independent D1definitions; reference zero/insufficient are separate. Opportunity nulls condition on the observed entry budget and fixed left support; they do not preserve future task feature marginals or prove semantic importance.\n';(C/'frequency.md').write_text(freqdoc);(C/'frequency_cn.md').write_text('# 频率组：参与不等于重要性\n\n'+freqt+fn+'## 实际换入与换出的成员\n\n'+md(['字典','参考组','角色','按家族支持排序的真实ID/平均强度'],frows)+'\n上表只为阅读，全部ID与每家族强度在执行侧feature_turnover_atlas.csv及*_member_values.csv，不据此重新选择组合。Attention高频换入均值4.33，参考期待4.43；MLP低频换入0.708，参考期待0.321、发现任务期待0.402，但家族区间跨零，不能宣称低频特别易换入。逐族机会、字典基数、旧活跃基数与旧排名四档匹配均保留；参考未出现组的零期待是未校准，不算无穷富集。高频绝对改变量占比大，不等于输出贡献、因果重要性或谱位置。\n')
cn='''# R20：成员会更替，码中的事实差异没有平均衰减

**在本任务的16–128 token区间，结果更符合“成员重组、事实差异幅度保留”，而不是统一衰减。共同成员的相对搭配很相似，但成员名单和A/B差异方向仍会改变。** 这里描述的是两套固定SAE的码，不把范数直接称为模型记忆量。

本轮按三个分析路径展开：①行为与因素对照：核验原候选排序并检查填充/位置；②表征与层次组织：分别测成员、强度及事实差异的幅度/方向；③功能干预与测量质量：功能干预未按本轮范围运行，已完成原生编码、重构与数值质量审计。

## 原先的可能与实际观察

原先保留三种可能：组合基本稳定；成员更替但两事实仍可区分；事实相关差异减弱。R19的六成员方向相似不足以区分这些情况，因此本轮复用全部144条主任务，检查两个字典各30000维的完整Top32码，保留所有12个原留出家族；12个发现家族只作探索。旧留出已经暴露，本轮不称全新确认。

模型为冻结Qwen3-0.6B Base。Attention取第28层o_proj输出，MLP输入取同层残差与归一化后的实际输入，各30000成员、ReLU后Top32，ID不跨字典相认。原文本固定320token，回答前冒号p319/tokenID25；物品最后token位置e302/254/190，对应排除两端的d=p−e−1=16/64/128。

'''+main_table+'''“相对事实差异”先计算同族A/B激活之差的范数，再除以两条码长度的均方根。这样可区分事实差异本身与整体激活增益：Attention原始差异约1.046倍，码总体尺度约0.968倍，归一后约1.080倍；MLP原始差异约1.184倍，整体尺度0.987倍，归一后1.199倍。归一化没有被用来隐藏整体变弱。

![组会主图](figures/main_distance.png)

左图显示相对d16还共同使用多少成员，右图显示相对事实差异的比值；两图是不同对象，不能从换人直接推导信息减少。区间以整家族重采样，两事实先在族内平均。d16的32和1是参考定义。

## 成员、强度与差异方向怎样一起变化

16→128平均换入/换出Attention7.21个、MLP4.08个，但仍共同使用24.79与27.92个。固定32预算必然令换入数等于换出数，不作为发现。三个配对的全部族分布、真实ID和原始强度均保留。

共同成员原始范数约为近距的0.9675/0.9876，方向cos为0.9976/0.9987：它们整体略弱，搭配仍很相似。这个大向量稳定，并不等于A/B之间那一小段差异稳定。完整Top32的原始事实差方向cos仅0.5978/0.7307；按每条码先单位化再做A/B差，也为0.5929/0.7260。

固定六成员保留实际零、纳入全部12族后，相应单位化事实差方向cos是0.9427/0.9614。旧严格子样本的0.9678（6族）/0.9713（11族）已精确复现，但它们不能代表完整码，更不能证明幅度不变。

约88%/83%的换入换出实例位于预定阈值附近口径（低排名或激活≤1.25倍cutoff），约99%的换入成员此前已有正的、阈值下编码响应。解除Top32截断仅作测量诊断时，事实差方向cos提高到0.8833/0.9080。因此，名单更替既包括强度变化，也受排名截断影响；不能直接称作新语义出现或旧语义消失。

## 高频、中频、低频各怎样参与

在三个主距离的72个留出位置中，Attention高/中/低组分别出现136/50/18个成员，低频覆盖70位置、12族；MLP为63/30/25个，三组均覆盖72位置、12族。零参考和支持不足单列，不并入低频。频率来自旧独立自然参考300文档/38400位置，不是词频、训练曝光或谱位置。

Attention的高频换入最多，但其4.33个与按自然频率机会期待的4.43个接近；不能只据人数宣布其更容易进入。MLP低频平均换入0.708个，自然参考/发现任务机会分别约0.321/0.402，但家族区间跨零，仍不足以确认特殊偏好。共同成员、换入换出的数量/比例、强度、基数、排名匹配与真实ID详见[频率分析](frequency_cn.md)。

## 补充实验：模式是否依赖旧填充或位置

旧结果为缓存重算；新执行228个对照前向条件，其中192条新文本、36条相同文本的位置索引变体。四条smoke已并入，另有六条旧文本校准；没有重复扩样调模板。

'''+ct+'''反转填充及替换同token长度办公填充都保留320长度、e/p、最终提问；固定e190时，回答p为207/255/319，分别对应d16/64/128，远距24条直接复用旧数据。上表各条件均为相同12族。三组都未出现平均差异减弱，但替换内容也改变了重复和词汇，不能当作单一领域因果实验。

另一组六族同文position IDs整体+64，成员全部32/32保持，最大候选总分差仅约3.9×10⁻⁵nat；它检验编码索引平移，不等于在可见文本里增加64token。事实位置e、回答位置p和d满足一个等式，无法三者全独立；对照缩小了解释范围，没有识别普适的纯距离效应。

原主任务三个距离仍各12/12成对正确，平均完整候选分差6.4209/6.6187/6.8925nat。原d64仅物品词评分是11/12，完整答案含句号才12/12，该敏感性没有抹掉。新反转填充d16为11/12，其余反转距离及办公/固定e条件均12/12。失败为F28/stamp，分差−0.084757nat，全文保留。近处失败而远处成功也提示填充顺序值得控制，不能按距离单调解释。

## 四个案例与反例

[F11 ball/die](cases/F11_cn.md)成员相对保留最多，却是总体均值下的轻微差异减弱例；[F15 cookie/cake](cases/F15_cn.md)更替最多，差异幅度仍保留；[F27 map/chart](cases/F27_cn.md)两字典接近稳定但方向不完全一致；[F19 toy car/toy truck](cases/F19_cn.md)Attention相对差异约0.79倍、MLP约1.89倍，回答均正确。选择规则事先固定，四族都展示A/B、三个距离的全文、成员与候选评分；没有删除其他家族或选择最漂亮的例子。[案例入口](casebook_cn.md)同时保留新增的F28失败。

## 操作假设判定与认识更新

H1是“至少90%成员保留”，H2是“相对事实差异比落入[0.8,1.25]”，H3是“该比至少下降20%”。容差是本轮AI预先固定的工作口径，不是普适能力标准；正的方向cos也不替代幅度判定。

'''+ph+'''MLP的H2证据不足来自增长区间上界超过1.25，不是出现衰减。Attention支持容差内保持，也不等于精确相等。H3针对至少20%的家族平均下降未获支持，不排除局部家族减弱。模板六组敏感性、全部家族、其他距离对和原始分数见[数值附录](numeric_evidence.md)。

认识更新是：在这个任务窗口内，模型成功利用事实时，回答处的码可以通过成员更替和强弱微调来变化；这些变化没有表现为统一的事实差异幅度损失。完整事实差的方向会重组，截断和所选成员范围都会影响我们看到的“稳定性”。

## 解释边界与唯一下一问

两套SAE对真实输入A/B差的重构相对误差中位数约0.994/0.984，明显高于普通逐位置重构误差。这限制了强解释：这里的码范数不是模型事实信息总量；观察到差异和答对，也不证明这些成员因果支撑答案。未截断码仅作诊断，不当作另一个训练好的字典。共享模板、已暴露留出、参考语料有限和16–128局部窗口同样保留。

**AI建议唯一继续追问：这些随距离重组但未平均衰减的事实差异，哪些真正被答案读取？** 本轮不设计或运行相应干预，也不训练router，科学接受仍待共同审阅。

|覆盖|状态|证据|
|---|---|---|
|旧数据、成员/强度/事实差、频率机会、四案例|DONE_VALID（发现侧探索单列）|逐族/逐成员表、原文、原生编码重放|
|228补充前向、行为参照、测量质量|DONE_VALID|固定协议、全部结果及失败、数值与重构审计|
|主/审计图、方法/代码/配置、短讲与可复算数据|DONE_VALID|[完整位置清单](artifacts_cn.md)|

本轮完成并停止；不把执行完成当作科学接受或后续执行授权。
'''
(C/'summary_cn.md').write_text(cn)
en='''# R20: member turnover without average loss of code-level fact separation

In this object-fact task at gaps16–128tokens, the observations favor membership reorganization with retained fact-contrast magnitude, rather than uniform attenuation. Common members retain a very similar relative arrangement, while member identity and the direction of the small A-minus-B contrast change. These are fixed-SAE code measurements, not a measure of total model memory.

Three analysis paths are kept distinct: (1)behavior and factor controls; (2)representations and layerwise organization; (3)functional interventions and measurement quality. Functional interventions were not run by scope; numerical and reconstruction quality were audited.

## Question, objects and original evidence

The alternatives were stable composition, turnover with retained differences, and attenuated fact differences. R19's selected-six direction did not resolve magnitude. We reuse all144main prefixes and retain all12old heldout families, with12discovery families exploratory. Prior heldout responses were exposed; this is a reanalysis, not untouched confirmation.

The model is frozen Qwen3-0.6B Base. Native SAEs observe block27Attention.o_proj output and actual post-residual/post-normalizationMLP input, separately; each has30000coordinates/ReLU Top32. Prefix length320, p319colon tokenID25. Gap=p−e−1excludes both endpoints; e302/254/190gives16/64/128. Missing selected coordinates are actual postTop32zero; no favorable-family filtering is used.

## Main observations

Across16→128, mean common members are24.79/32Attention and27.92/32MLP; entries/exits7.21and4.08. Their equality follows the fixed budget. Common-member raw norm ratios are0.9675/0.9876and common direction cosines0.9976/0.9987. A stable large common vector does not imply a stable small fact difference.

Raw full-code fact-difference norm ratios are1.0456/1.1839; total code RMS-scale ratios0.9679/0.9874. Relative separation divides the A-minus-Bnorm by RMS of the two row norms, removing uniform scale. Its ratios are1.0803,95%familyCI[0.9899,1.1725],and1.1989,[1.0976,1.3307]. Whole-code magnitude does not uniformly shrink. Full raw fact-direction cosines are0.5978/0.7307; unit-row contrasts give0.5929/0.7260. Fixed-six unit-row contrasts across all12families give0.9427/0.9614; the old strict six/family subsets0.9678(N6)/0.9713(N11)are reproduced exactly. Selected-six stability cannot substitute for the whole code or magnitude.

About88%/83%of turnover instances meet the predeclared cutoff-near rule, and about99%of entrants already have a positive encoder response belowTop32at near distance. Rectified preTopK direction cosines are0.8833/0.9080. This is a truncation diagnostic, not a newly trained SAE or an intervention. Turnover is not equivalent to new/erased semantics, nor is every threshold crossing merely noise.

## Frequency, controls and behavior

In72main heldout positions, reference-high/middle/low observed members are136/50/18Attention and63/30/25MLP. Low groups cover70and72positions,all12families. Reference-zero/insufficient remain separate. Frequency is fixed from independent300document/38400position native reference corpora, not word frequency, spectral position or training exposure.

Attention's4.33high-frequency entrants are close to4.43expected from reference-weighted opportunity. MLP's0.708low entrants exceed natural/discovery-task expectations0.321/0.402at the mean, but family intervals cross zero. Dictionary sizes, left-at-risk counts, rank-matched exits and conditional entry opportunities are reported; raw group counts do not establish importance.

New execution comprises228control conditions:192new texts and36same-textposition-IDvariants. Reverse weather and length-matched office filler each use72prefixes; fixed evidence e190adds48near/midprefixes and reuses24old far rows; uniform positionIDs+64uses36rows in six template-covering families. Four smoke rows are reused; six old rows calibrate exact scoring. No weights,optimizer or training change occurs.

Relative fact-separation128/16ratios under reverse/content/fixed-e areAttention1.123/1.104/1.079andMLP1.138/1.118/1.137(allN12). None shows mean attenuation. Office replacement also changes repetition/lexical content. Uniform position-index shifts retain32/32members with max candidate-score discrepancy about3.9e−5nat. This computational coordinate shift does not add visible text. Because d=p−e−1,these controls do not identify an unrestricted pure-distance effect.

Original full-candidate paired accuracy remains12/12at every distance; mean margins6.4209/6.6187/6.8925nat. Item-only64is11/12and is retained separately. Reverse16has one failure(F28stamp,margin−0.084757); reverse64/128and office/fixed-e remain12/12. All failed texts/scores are preserved. Filler order can matter even near the answer.

## Cases, operational hypotheses and knowledge update

The frozen rule selectsF11(relatively high retention,yet slightly smaller contrasts),F15(largest turnover without weaker contrast),F27(small mixed changes),andF19(Attention ratio0.79versusMLP1.89,all answers correct). Full two-fact/three-distance texts and all union members are linked in the casebook. No other family is deleted.

H1retention≥90%is not supported at either site. H2relative magnitude within[0.8,1.25]is supported forAttention(Holm p0.01465); MLP is insufficient because its growth interval extends above1.25,not because of attenuation. H3mean attenuation≥20%is not supported at either site. These are registered AI operational tolerances, not universal ability criteria. Six tests use Holm;8192whole-family bootstrap and six-template sensitivity retain all families. Exact paired sign-swap tests assume symmetric family location errors.

The knowledge update is that successful fact use in this window can coexist with membership turnover and small shared-member strength changes,without average loss of code-level fact-separation magnitude. The fact-difference direction reorganizes, and the choice of members/truncation affects apparent stability.

## Measurement limit and one next question

SAE reconstruction of actual hook-input A-minus-Bdifferences has median relative error about0.994/0.984,much worse than ordinary row reconstruction. Code norms are therefore not total factual information. Shared templates,exposed holdout,limited reference corpus and the local gap range also limit claims. No causal necessity,general memory law,semantic atom identity or router benefit is established.

AI-suggested sole next question: which of these reorganized,but not on-average attenuated,fact differences are actually used to read out the answer? No intervention/training design is executed automatically; scientific acceptance remains pending review.

[Numeric annex](numeric_evidence.md),[cases](casebook.md),[frequency](frequency.md),[Detailed](detailed.md),and[artifact index](artifacts.md)retain complete evidence. Coverage: old-data analysis,cases/frequency,228controls and numerical quality DONE_VALID; discovery-only observations remain exploratory; figures,code/configuration,short talks and reproducible evidence are delivered. STOP for review.
'''
(C/'summary.md').write_text(en)
print('RESULT_SUMMARIES_WRITTEN')
