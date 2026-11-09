from engine import *
import pandas as pd
A=pd.read_csv(R/'tables/A_overlap_references.csv');O=pd.read_csv(R/'tables/B_own_structure.csv');D=pd.read_csv(R/'tables/B_dataset_differences.csv');M=pd.read_csv(R/'tables/null_mixing.csv');CON=pd.read_csv(R/'tables/null_constraints_summary.csv');P=pd.read_csv(R/'tables/B_selected_pairs.csv');I=pd.read_csv(R/'tables/A_intersection_identity.csv');g=A[A.comparison=='pooled_gap'];cases=rows(R/'tables/concrete_pair_cases.jsonl');case=next(q for q in cases if q['dataset']=='GSM8K');freqchecks=rows(R/'tables/frequency_reference_checks.jsonl')
def mdt(df,cols):
 def val(x):
  if isinstance(x,(float,np.floating)):return f'{x:.6f}'
  return str(x)
 return '| '+' | '.join(cols)+' |\n|'+'|'.join(['---']*len(cols))+'|\n'+'\n'.join('| '+' | '.join(val(row[c]) for c in cols)+' |' for _,row in df.iterrows())+'\n'
shortg=[]
for _,r in g.iterrows():shortg.append(dict(SAE=r.site,pair=r.A+'/'+r.B,real_gap=f'{r.real_J:.6f}',discovery_frequency_gap=f'{r.discovery_Bernoulli_J:.6f}',fixed32_margin_gap=f'{r.heldout_fixed32_margin_J:.6f}',fixed32_ratio=f'{r.fixed32_gap_reproduction_ratio:.1%}',remaining_gap_CI=f'[{r.real_minus_fixed32_CI_lo:.6f},{r.real_minus_fixed32_CI_hi:.6f}]'))
gtable=mdt(pd.DataFrame(shortg),list(shortg[0]));op=O[O['mode']=='position'];dp=D[D['mode']=='position'];ownnum=int((op.status=='SUPPORTED_STATISTIC').sum());betnum=int((dp.status=='SUPPORTED_STATISTIC').sum());owntable=mdt(op,['site','dataset','heldout_real_projection','heldout_null_projection','heldout_excess','doc_CI_lo','doc_CI_hi','Holm_p']);dtable=mdt(dp,['site','A','B','heldout_A_excess','heldout_B_excess','heldout_difference','doc_CI_lo','doc_CI_hi','Holm_p']);uncertain=int(((g.real_minus_fixed32_CI_lo<=0)&(g.real_minus_fixed32_CI_hi>=0)).sum());ratio=(g.fixed32_gap_reproduction_ratio.min(),g.fixed32_gap_reproduction_ratio.max());bernratio=(g.Bernoulli_gap_reproduction_ratio.min(),g.Bernoulli_gap_reproduction_ratio.max())
cn=f'''# S09：频率能解释重叠，联合结构要另测

**认识更新。** S08同域重叠更高，主要可由成员频率差异复制；它本身不能作为联合组合的充分证据。固定每位置32个成员、每feature次数和分位后，联合统计仍在独立留出文档上高于本源零模型，源间残差差异也复现。A与B可以同时成立。

本轮的事实路径：行为/因素方面不做答案评分，仅复用文本和位置并检查token分层；表征方面分开统计频率/Jaccard与联合共同出现；功能方面没有干预、分类器或模型训练，零模型与独立复算仅用于审核测量可信度。科研接受与问题关闭Unknown，完成后等待研究者审阅。

**A：平均Jaccard的大部分差值可由边际参照重现。** 原771篇不重新抽样，各源128发现/129留出，原8位置。发现集频率生成的独立Bernoulli参照，复制了真实“平均内部−跨域”差值的{bernratio[0]:.1%}–{bernratio[1]:.1%}；它每行期望32但实际10–64或12–60个成员，并含发现频率估计误差，不能当作严格Top32零模型。用留出集本身的频率、严格行32的条件零模型，差值比值为{ratio[0]:.1%}–{ratio[1]:.1%}。后者是描述性参照，不是发现集预测，也不是因果解释率；比值不裁剪。真实减条件参照的剩余差，{uncertain}/6个文档区间跨0。

{gtable}

表中gap=两源内部均值的平均−跨域均值，单位为原始Jaccard。剩余区间给定发现划分/零模型中心；不是对所有估计阶段的无条件区间。[完整A表](tables/A_overlap_references.csv)分别保留A内、B内、跨域的真实值、两种参照及差值，不能只读上表合并差。

![真实重叠与频率参照](figures/01_overlap_vs_frequency.png)

蓝点是真实留出、黄三角是发现频率但行数目自由、绿方块是留出频率+严格32；蓝误差线为文档级95%区间，参照线为MC均值误差，不能当成新增文档。独立交集期望可求和，但本轮Jaccard均实际逐次计算。固定列次数后，完整内部文档对的平均交集严格相同；平均Jaccard仍会因交集分布不同而变。该恒等式已独立复核，最大误差0。

**B：直接检验联合统计后，有留出复现。** 每套字典在发现集按频率/文档支持固定24成员，保留全部276对；每篇先平均8个位置的共同出现，再减本源严格边际零模型。发现集仅拟合其残差方向和各源差方向，之后冻结。留出本源结构{ownnum}/6、源间差异{betnum}/6满足预设判据；两组六检验各自Holm校正，均p=0.023346。这个p来自256个条件零模型样本，原始最小p=1/257，分辨率有限。

![联合统计、零模型与留出](figures/02_joint_null_and_holdout.png)

灰色为固定次数零模型的95%范围；紫色是发现拟合值，不是验证；蓝色为留出值和整篇bootstrap区间；绿色为额外token分层的探索结果。纵轴是276对共同出现残差沿冻结单位权重的投影，**不是Jaccard、准确率或语义强度**。原始投影与零模型中心分别列于下表。

{owntable}

**具体共同出现数据。** Attention的GSM8K候选#17625/#14773，发现集共同出现比例0.214844、本源零模型0.129898；留出真实221/1032位置=0.214147，零模型0.115708，超额0.098440，94/129篇文档至少出现一次。原文例子：{case['text']} 原S08的{case['id']}，位置{case['position']}，token={case['token']!r}；两成员原激活分别{case['z_i']:.6f}、{case['z_j']:.6f}。这里观察的是两个ID的共现，不给它们自动命名概念。

**相反例子也保留。** MLP输入#20989/#24338在GSM8K发现集中为低于零模型：真实2/1024、参照0.003948；留出却为高于零模型：真实12/1032=0.011628、参照0.003138，共8篇，差0.008490。该单对没有按发现方向复现；主联合向量复现不表示每对稳定。另有发现/留出支持为0的格，不能称为反向。[全部已选12对](tables/B_selected_pairs.csv)与[276对完整分量](tables/B_all276_components.csv)均保留，未只报最显著项。

**零模型实际质量。** 每模式4链×64样本；burn100扫，每10扫取样。主留出每套字典提出4,617,600次行对交易，改变比例>99.999%；所有已检查快照行32/唯一ID和列次数精确满足，最大列误差0。判定统计的Rhat最高{M.Rhat.max():.4f}、ESS最低{M.ESS.min():.1f}，达到冻结阈值，无需延长。存在无法交换的固定成员：主留出Attention为1032/99072条激活边、MLP输入1677/99072，均已保留并逐层列ID。高交换率不被单独当成充分混合证据。

**仍未排除。** 仅按数据集×分位固定边际；探索额外按发现最常用token ` the`、` of`、`.`及OTHER分层后，联合信号仍为正，但89个层中52个少于8行，部分约束近乎锁定。它没有匹配所有词面或格式。S08主要是格式描述，**没有独立格式匹配**，本轮同样未做。完整长度中位数252/56/50、代码围栏158/257对0/257对0/257、来源/题型/学科/近重复均保留为竞争解释。跨源差异是各自边际条件下的超额共现差，并不是把两源改成相同边际后比较统一依赖参数；可达效应量仍受边际支持范围影响。

区间以文档为单位，给定发现方向和估计零模型中心，不整合发现选择、频率预测误差和所有零模型估计误差；MCSE另列。零模型打破跨位置的文档连贯性，不能理解为自然文本的因果替代。原S08文档已暴露，本轮只保证新候选未用留出联合值筛选，不声称外部新样本复现。Numina仍缺失。没有读出分类、功能或router结论。

[详细报告](detailed_cn.md) · [协议](protocol_cn.md) · [约束](tables/null_constraints_summary.csv) · [混合](tables/null_mixing.csv) · [复算](reproduce.md)。本轮停止，等待审阅。
'''
en=f'''# S09: marginal overlap explanation and replicated joint structure are different findings

A: source/position marginal frequencies reproduce most of the S08-style overlap gap. B: direct coactivation statistics still exceed exact row32/column-count nulls and replicate across the internal heldout split. Overlap alone is not sufficient evidence for combinations. No semantic, functional or router mechanism is inferred.

The factual paths are: behavior/factor controls inspect metadata and token strata without answer scoring; representation analysis separates binary overlap from coactivation; functional intervention, classifier fitting and model training are NOT_RUN. Scientific acceptance/closure Unknown; stop for researcher review after delivery.

Original771documents and8positions are unchanged; each source has128discovery/129heldout documents. Discovery Bernoulli references reproduce {bernratio[0]:.1%}–{bernratio[1]:.1%}of the pooled gap but only constrain expected rowcount32, with observed10–64/12–60counts and probability-estimation error. Exact heldout-margin/row32 nulls reproduce {ratio[0]:.1%}–{ratio[1]:.1%}; these are descriptive ratios, not causal explained fractions or discovery-only forecasts. {uncertain}/6conditional document intervals for the remaining Jaccard gap span0.

{gtable}

![A overlap and marginal references](figures/01_overlap_vs_frequency.png)

Each native dictionary uses24discovery-frequency-selected coordinates and all276pairs. Mean binary pair products over8positions/document are centered by each source's own exact-margin null. Discovery residual directions and between-source contrast directions are frozen before heldout coactivation. Own-source{ownnum}/6and between-source{betnum}/6heldout contrasts pass the registered positive-direction/document-CI/mixing/conditional-null criteria; Holm separately within the two six-test families, all adjusted p=.023346. Minimum raw conditional p=1/257from256null samples; no higher p-resolution claim.

{owntable}

{dtable}

![B coactivation null and heldout](figures/02_joint_null_and_holdout.png)

The ordinate is pair-coactivation excess projected on unit-length discovery weights, not Jaccard, accuracy or semantic intensity. Discovery points are fitted, not validation; gray bands are algorithmic null ranges, not additional documents. The conditional intervals hold discovery weights and the estimated null center fixed; discovery-selection/probability-estimation and all null-center uncertainties are not integrated. MCSE is separate.

Example ATTN GSM8K #17625/#14773: discovery real.214844vs null.129898; heldout221/1032positions=.214147vs null.115708,94/129coactive documents. Concrete text/token/native magnitudes in tables/concrete_pair_cases.jsonl. A contrary selected MLPIN pair #20989/#24338 in GSM8K changes from below null in discovery (2/1024vs.003948) to above null in heldout (12/1032vs.003138). Aggregate replication does not imply every pair replicates; all selected pairs and all276components are retained.

All checked rows remain32unique coordinates and all feature counts are exact. Primary heldout nulls propose4,617,600row trades/site,>99.999%change; maximum scalar Rhat={M.Rhat.max():.4f}, minimum ESS={M.ESS.min():.1f}. Some coordinates are forced:1032/99072ATTN active edges and1677/99072MLPIN edges. Four chains,100burn sweeps,10sweeps between64samples each; finite-time diagnostics rather than asymptotic theory establish bounded numerical adequacy. See [Curveball construction/proof](https://doi.org/10.1103/PhysRevE.91.042812); unchanged trades are retained.

Token-stratified exploratory nulls remain positive but52/89strata have<8rows, and only three literal token IDs plus OTHER are constrained. S08 described formatting and did not independently match it; neither does this round. Length medians252/56/50, code fences158/257vs0vs0, question/source/topic/near-duplicate differences remain. A between-source residual contrast conditions on each source's own margins; it is not a comparison after imposing identical margins on both sources, and attainable dependence still varies with support. Nulls break document continuity across positions. This is a new internal split on already-exposed S08 documents, not external fresh confirmation. Numina remains unavailable. No feature concepts or router efficacy are assigned.

[Detailed](detailed.md), [Protocol](protocol.md), [Reproduce](reproduce.md). Wait for review; no automatic follow-up.
'''
(R/'summary_cn.md').write_text(cn);(R/'summary.md').write_text(en)
methods_cn='''## 实验对象、公式与执行顺序

原始Qwen3-0.6B-Base（28block、宽1024）及两个block27、30000维ReLU-Top32字典，来源及hook沿用S08：Attention为o_proj输出、残差前；MLP输入为mlp实际输入、残差和post_attention_layernorm后。不同字典ID不对应。S09只读取稀疏缓存，没有加载模型/权重或重新前向。3源各257篇问题，原8个位置floor((j+.5)*min(全长,128)/8)不变。Magicoder只用problem、GSM8K/MMLU只用question，无答案或MMLU选项。S08源路径/revision/字段在源data/sources.json，实际缓存SHA在本轮冻结计划。

划分：在各源按SHA256(seed2026110409+'S09'+文档ID)排序，前128发现、后129留出，不重新抽样文本。同篇8位置不跨组。留出排序保持冻结顺序，内部全部i<j，跨源循环偏移1..64，各8256个不同文档对；同一篇不与自身比较。每对平均8个对齐位置的实际Jaccard=交集/并集，不把位置或反复参与的边当独立文档。

A预测参照：对每源每分位计算全部30000个发现频率p_f，独立Bernoulli生成129篇×8位置，重复256面板；每行只保证期望成员数32。每个模拟支持实际求Jaccard，报告真实三组均值/参考/差值及MCSE。独立文档交集期望为sum p_Af p_Bf；同域plugin的sum p_f²包含频率估计噪声，另列无偏交集估计sum c_f(c_f−1)/(128×127)，它不是Jaccard期望。对严格Top32的A解释，则使用留出自身次数的条件零模型，不能把这项描述性参照冒充发现预测。

当两行均32时，J=I/(64−I)=I/64+I²/[64(64−I)]。完整同域无序对的mean I=sum c_f(c_f−1)/(n(n−1))，列次数固定便严格不变；共同出现可改变高阶项、从而改变平均J。跨源若取全部n²对，mean I=sum c_Af c_Bf/n²；等数量循环子图不是全集，允许因行分配产生波动。两种交集/J参考都保存，避免把J剩余直接等同于所有联合结构。交集分布补充只用事前固定的8个审计快照（每链首/末），明确不是256个完整null的全部分布。

B零模型：每个源、划分和分位分别对“行=位置、列=feature”交换。等概率选不同两行，保留交集，独有成员的并集随机等分给两行（均32）；不变/失败交易也计入，保证对称性。4个独立链、burn100扫，thin10扫、每链64样本。每扫ceil(n/2)次提议。每个快照检查每行唯一/32与全30000列计数。源/位置边际严格固定，不固定其他文档属性或跨位置连贯性。原成员保留率与sum c_f²/(n²×32)的约束期望比较；检查多链Rhat/ESS，不能只用移动量宣称混合。小4×4行列次数均2的90状态空间用20000样本校准；此实现检查不是研究发现。

联合统计：发现集按pooled频率/文档支持先固定24ID，不查看联合效应挑ID；全部276对进入主要统计。每篇q_ij=8位置中两成员共同为正的比例。各源发现残差r_d=mean q_d−E_null q_d，方向v_d=r_d/||r_d||；两源方向v_AB=(r_A−r_B)/||r_A−r_B||。留出本源统计v_d·(q_test−E_null q_test)；跨源统计v_AB·(r_A,test−r_B,test)。同一源有残差并不能替代后者。独立零模型样本投影给条件null p，各自六检验Holm。方向为发现统计权重，不能命名为语义轴。置信区间由129篇整篇bootstrap999次；这是给定方向和估计null中心的条件区间，不宣称完整抽样误差已整合。null算法的蒙特卡洛误差另报，256个null不是256个新增实验文档。

补充：24成员中激活个数0..24的分布；发现集pooled最常见8个精确24bit组合+OTHER；12示例对在276对内按6个pooled正残差、6个最大源间残差范围选，须某源至少4发现文档共现。该选择规则先于留出固定，所有结果包含支持不足/零/相反情况。token探索额外固定当前token为发现最常见3ID（279=' the',315=' of',13='.'）或OTHER；使用原发现方向，不重选特征。其他分层、独立格式匹配、分类或干预均NOT_RUN。

## 数值校验与未运行项

evidence/independent_verification.json核对原S08全部80文件未改、771文档划分、200直接集合Jaccard、32审计快照的276对共同出现、768个层的列次数、固定交集恒等式、两组Holm与24个主要/探索投影重放。Rhat/ESS均达冻结阈值，无需事前允许的延长重跑。没有为了结果选更好的零模型或修改判据。独立格式匹配NOT_RUN，NuminaMISSING；分类器/模型前向/训练/功能干预NOT_RUN，科研接受/关闭Unknown。
'''
methodsen='''## Objects, operations and execution

Reuse the exact frozen official Qwen3-0.6B-Base(28blocks,width1024) native block27SAEs,30000/ReLU-Top32. Attention=o_proj output before residual addition; MLPIN=actual mlp input after residual/post_attention_layernorm. Separate dictionaries, unrelated IDs. This round reads sparse caches only, no model load or forward. Three question-only sources257documents each, original8quantile positions on first min(length,128)tokens; no answers/options. Source Arrow versions/fields remain in S08 data/sources.json; this round binds exact sparse cache/panel hashes.

Within source order SHA256(seed2026110409+'S09'+ID),128discovery/129heldout, all8positions stay together. Within all unordered pairs; cross cyclic offsets1..64,8256unique pairs/group, no self pairs. Position Jaccards are calculated and then averaged; repeated edges/positions are not independent documents.

A computes all discovery probabilities separately by source and quantile, simulates256whole heldout-size independent Bernoulli panels (expected rowcount32, not exact32), and computes actual Jaccards. E[I]=sum p_Ap_Bis exact for independent draws; plugin sum p²has finite probability-estimation bias, and the distinct unbiased discovery intersection U-statistic is reported. Neither is substituted into Jaccard. The exact heldout-count/row32 conditional reference is descriptive, not a discovery forecast. For row32, J=I/64+I²/[64(64-I)]; mean within I is fixed by column counts, higher moments can still alter mean J. Full cross mean I is likewise fixed, while the original balanced cyclic subset can fluctuate. Descriptive intersection distributions use8fixed audit snapshots only.

Curveball trades within source/split/quantile preserve row32and all feature counts; unchanged trades retained.4chains,100burn sweeps,10sweeps between64draws/chain, each sweep ceil(n/2)row-pair proposals. Check every snapshot's unique coordinates/column counts, changed-trade fraction, original-edge retention against sum c²/(n²*32), split-Rhat/ESS. The toy90-state fixed-degree space is an implementation check, not empirical research evidence. Finite diagnostics do not prove perfect mixing.

Discovery picks24IDs by marginal count/document support, all276pairs enter the primary score. Per-document pair product is averaged across8positions. Each source's discovery excess over its own null defines a unit direction; source residual differences define independent frozen contrast weights. Heldout own projections and cross-source residual contrasts test different predictions. Two six-test Holm families,256conditional-null samples,999whole-document bootstrap CIs conditional on fixed discovery weights and estimated null centers. Discovery fitting/selection uncertainty and all null-center uncertainty are not integrated into those CIs; MCSE separate. Nulls can break cross-position document continuity.

Secondary24member-count histograms, discovery-top8exact bit patterns+OTHER, all12discovery-chosen example pairs including adverse/zero results. Exploratory token-conditioned null fixes discovery-top3literal IDs279/315/13orOTHER and keeps original weights. It does not independently match formatting or every lexical item. Between-source excess differences do not impose identical source margins or identify invariant dependence parameters. No semantic labels, classifier/readout fitting, interventions or router utility.

Independent verification covers80unchanged S08files,771document split,200set Jaccards,32audit-snapshot pair vectors,768stratum-margin checks, fixed-intersection identity,24projections and two Holm families. Source counts/marginals, seed/rules and all primary/exploratory results retained. Scientific acceptance/closureUnknown, NuminaMISSING; stop for review.
'''
detailcn='# S09 详细记录：单成员频率与联合结构\n\n'+methods_cn+'\n## A全部原始组内/跨组结果\n\n'+mdt(A,['site','A','B','comparison','real_J','real_CI_lo','real_CI_hi','discovery_Bernoulli_J','real_minus_Bernoulli','heldout_fixed32_margin_J','real_minus_fixed32_margin'])+'\n## A交集与非线性审计\n\n'+mdt(I,list(I.columns))+'\n## B本源联合结构\n\n'+mdt(O,['site','dataset','mode','heldout_real_projection','heldout_null_projection','heldout_excess','doc_CI_lo','doc_CI_hi','p_null','Holm_p','mixing_pass','status'])+'\n## B源间差异（两侧保留）\n\n'+mdt(D,['site','A','B','mode','heldout_A_excess','heldout_B_excess','heldout_difference','doc_CI_lo','doc_CI_hi','p_null','Holm_p','mixing_pass','status'])+'\n## 实际约束与随机化预算\n\n'+mdt(CON,list(CON.columns))+'\n\n最高Rhat='+str(M.Rhat.max())+'；最低ESS='+str(M.ESS.min())+'。完整各统计量见null_mixing.csv，实际成员ID及锁定列在每个constraints.jsonl。\n\n## 认识更新、原文、反例及边界\n\n'+cn.split('**具体共同出现数据。**',1)[1]+'\n\n探索分布：[24成员激活个数](tables/B_member_count_distribution.csv)、[精确组合](tables/B_exact_pattern_distribution.csv)；后者pattern_code的二进制位对应data/feature_universe.json内各字典24ID顺序，OTHER=-1，0为空候选组合，不是feature0。每源每split分母为文档数×8；文档仍是独立单位。\n'
detailen='# S09 Detailed record\n\n'+methodsen+'\n## A all three means and references\n\n'+mdt(A,['site','A','B','comparison','real_J','real_CI_lo','real_CI_hi','discovery_Bernoulli_J','real_minus_Bernoulli','heldout_fixed32_margin_J','real_minus_fixed32_margin'])+'\n## A intersection identity\n\n'+mdt(I,list(I.columns))+'\n## B own-source primary/exploratory\n\n'+mdt(O,['site','dataset','mode','heldout_real_projection','heldout_null_projection','heldout_excess','doc_CI_lo','doc_CI_hi','p_null','Holm_p','mixing_pass','status'])+'\n## B source contrasts\n\n'+mdt(D,['site','A','B','mode','heldout_A_excess','heldout_B_excess','heldout_difference','doc_CI_lo','doc_CI_hi','p_null','Holm_p','mixing_pass','status'])+'\n## Actual constraints\n\n'+mdt(CON,list(CON.columns))+'\n## Recognition and remaining uncertainty\n\n'+en.split('Example ATTN GSM8K',1)[1]
(R/'detailed_cn.md').write_text(detailcn);(R/'detailed.md').write_text(detailen)
brief=f'''# 1104组会：单成员频率与联合结构的区分

**问题。** S08同域Top32重叠更高，是否主要来自单feature频率？控制这些频率后，是否仍有留出复现、随源不同的共现结构？

**观察与对照。** 固定留出每feature次数和每行32的零模型，复制原式差值的82.9%–97.0%；5/6个剩余差区间跨0。发现集频率预测也复制99.4%–127.7%，但它不固定行32且有频率估计偏差。平均Jaccard主要是边际现象，不能作为联合结构的充分证据。两类比值都是数值复制比例，不是因果解释率。

{gtable}

**联合统计结果。** 发现集按频率固定每字典24成员、全部276对；本源残差方向和源间差方向只在发现集拟合。留出本源6/6、源间差6/6通过冻结的正向/区间/混合/null判据；分别Holm6校正，p=.023346。支持本轮可测的条件共同出现结构及其跨源差异；不支持将其命名为语义或router机制。

**结论下原始数据。** Attention-GSM8K #17625/#14773，留出221/1032位置共同出现（94/129文档），固定次数零模型0.115708，真实0.214147。GSM8K原文“On a moonless night, three fireflies danced in the evening breeze...”在token ` by`的激活9.756166/12.859011。反例：MLP #20989/#24338，GSM8K发现低于null，留出高于null（2/1024→12/1032）；整体向量复现不代表每对同向。

**做法。** 原771篇与8位置不变，各源128发现/129留出；4链×64严格边际零模型，burn100/thin10。所有列次数误差0；Rhat≤{M.Rhat.max():.4f}、ESS≥{M.ESS.min():.1f}；文档bootstrap999，不能把null或token当独立文档。无新前向、训练、分类或干预，S08原文件保持。

**边界与审阅。** S08只是格式描述，没有独立格式匹配；本轮也未做。额外token分层仍为正，但52/89层<8行。位置、长度、代码格式、来源/主题、近重复、发现概率估计与条件CI范围仍限制解释。Numina缺失。科学接受/关闭Unknown；本轮结束，等待审阅。

[完整Summary]({C}/summary_cn.md) · [两张主图]({C}/figures/01_overlap_vs_frequency.png) / [联合检验]({C}/figures/02_joint_null_and_holdout.png) · [Detailed]({C}/detailed_cn.md)
''';(R/'meeting_report_cn.md').write_text(brief)
(R/'reproduce.md').write_text('''# Reproduction and audit map

Run from this S09execution folder, CPU2threads, no model/SAE loads. Original S08root in frozen_plan.json supplies read-only panel/activations. A portable input subset is included in the review packet, and portable_replay.py uses that subset without the original execution path or model.

```bash
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
python code/calibrate.py
python code/run_null.py ATTN_SAE discovery position
python code/run_null.py MLPIN_SAE discovery position
python code/lock_directions.py
python code/run_null.py ATTN_SAE heldout position
python code/run_null.py MLPIN_SAE heldout position
python code/run_null.py ATTN_SAE heldout position_token3
python code/run_null.py MLPIN_SAE heldout position_token3
python code/run_frequency.py
python code/analyze.py
python code/verify.py
python code/supplement.py
python code/figures.py
python code/report.py
```

Sampler needs g++/C++17; engine.py compiles curveball.cpp locally and omits the compiled shared library from delivery. NumPy/SciPy/pandas/matplotlib are analysis dependencies. Native input caches, exact text IDs and asset hashes remain S08-owned. prepare.py must not be rerun over a frozen plan; it creates metadata split and discovery-only feature universe once. Null/frequency scripts refuse overwrite. Reproduce in a new execution copy, preserve source inputs/frozen config, and do not replace old result paths. Longer mixing run is available only via --long under the pre-fixed protocol; no extension was required.

Data: data/document_split.jsonl retains every source ID, original index, full/visible length,8positions/token IDs/decoded tokens and whole-document split; discovery_marginals.npz includes all30000coordinate frequencies separately for8positions and3sources; feature_universe.json and discovery_directions.npz bind24IDs/all276directions and12example pairs/top8bit patterns. No heldout feature reselection.

Tables: A_overlap_references.csv keeps each source side, cross, pooled gap and two references; A_intersection_identity.csv audits exact expectations and nonlinear term; B_own_structure.csv/B_dataset_differences.csv contain all primary/exploratory outputs and separate Holm6families; B_all276_components.csv retains every pair, B_selected_pairs.csv every selected result including zero/adverse cases. Candidate count and exact bit-pattern distributions retain denominators. Each raw native source sparse activation is implied zero outside its positiveTop32IDs.

Nullcache: four-chain256panels summarized in qnull/Jnull/etc, exact seeds/constraints and8full audit snapshots per condition retained execution-side. Full per-draw intermediate states not saved. Large arrays and original source corpora/weights are indexed separately and excluded from the small review packet; selected raw cache inputs, all joint trace samples, actual example coordinates and all tables remain portable. Package manifest says exactly which files are included. Conditional bootstrap intervals do not integrate discovery-selection or all null-center/probability-estimation uncertainty. No feature semantic labels or router claims.
''')
print('REPORTS_COMPLETE')
