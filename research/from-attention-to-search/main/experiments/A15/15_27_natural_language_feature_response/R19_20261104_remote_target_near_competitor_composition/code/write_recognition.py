from common import *
import pandas as pd,numpy as np,shutil,platform
from report import md,num,ph,jh,bh,mh,fh,details
prim=json.load(open(R/'results/primary_hypotheses.json'));joint=json.load(open(R/'results/joint_hypotheses.json'))
cn='''# R19 认识更新：共同成员保留事实差异，竞争下的强弱变化尚不能完整解释错误

## 这轮回答了什么

**在这批构造英语文本和固定位置上，MLP 输入 SAE 的同一组六成员同时呈现远处目标与近处物品的影响；事实差异在新家族和近远条件间保持。竞争下的组合变化伴随候选偏好下降，但完整的跨家族行为解释未通过预定门槛。** Attention SAE 的主要六成员覆盖不足，结论为证据不足。没有训练、激活干预或 feature 语义命名；科学接受和下一实验选择待共同审阅。

目的来自 R18：先前主任务 d16/64/128 各24/24成对正确，旧近处相反物品17/24。本轮要区分远目标内容、距离和近处物品对同一批 feature 的影响。仅比较旧主任务与旧竞争条件会混入填充/条款差异；旧竞争的A/B还同时改变两个词。因此原件保持不动，补96条，使每家族有远目标A/B×近处不明物品/A/B的匹配矩阵。

冻结模型为 Qwen3-0.6B Base。两个已有 SAE 分开分析：第28层 Attention o_proj 输出，以及残差与归一化之后的实际 MLP 输入。各30000成员、Top32；ID不能跨字典相认。每条前缀320tokens，观察同一个末尾冒号 p319、token ID25。距离 d=p−e−1排除两端，主e302/254/190对应16/64/128；物品多token取最后一个。24家族按模板组内拆12发现/12表征留出，整家族全部条件同侧；模板共享、旧行为已接触。全292条前向含4smoke，196条旧文本评分逐候选重放误差0。

## 行为参照：先看模型确实遇到了什么变化

'''+bh+'''表内“全部”合并发现与留出，不能称作新确认。匹配中性是近处有未指明物品，并非删除近处句子。留出中性11/12、相反9/12；平均正确分差从5.9946降到2.1802nat，家族平均下降3.8144nat，95%家族区间[2.8466,4.9116]。相反条件失败为F23/F27/F28；F28在中性条件已失败，不能把它的错误起点归于竞争。所有失败保留。一致条件12/12，支持近处词内容值得区分，但不单独证明模型采用何种策略。

## 第一层：复用与成员更换同时存在

'''+mh+'''固定事实从16到128，Attention平均共同24.79/32、MLP输入27.92/32；有竞争时仍有23.79和27.88个共同成员。固定32预算下，换入数与换出数必然相等，这个相等不是机制发现。事实互换参照中，16→128同事实Jaccard比错配事实分别高0.1973和0.1575（12家族）；所以重叠不全是固定问句的普遍公共成员。该参照仍未分离词形与物品身份。

## 第二层：哪些共同成员，以及它们怎样一起改变

发现侧固定的 Attention C=[2520,26235,29969,23899,772,2254]；MLP输入 C=[17390,25508,3011,4700,16240,27076]。对每条记录保留原始激活，并以同一C内向量的L2范数归一，描述相对搭配；每家族以自己的A−B差为参照，不把不同物品对当成同一语义方向。

H1固定近处词后看远目标A/B差与中性A/B差是否同向；H2看同族16与128的A/B差是否同向。MLP输入H1均值cos=0.7449，12/12家族严格共同激活；H2cos=0.9713，11/12家族，均通过预定区间与Holm条件。H2未纳入的F23是低频#25508在main16_A实际为0；不补换成员。Attention远矩阵仅5/12、近远仅6/12，未达8个家族。#772近远完整支持7/12，#2254远矩阵7/12；多个缺失取交集后进一步减少。第一批三个成员虽覆盖较好，按协议仅作敏感性，不能救回六成员主判断。

### 一个直观例子：抽屉里的 magnet，被近处 battery 干扰

F23原句为`The drawer was packed with the magnet.`，之后近处句为`The other container holds the object.`或`... battery.`，最终问题始终是`What was stored in the drawer?\\nAnswer:`。远目标末token在190，近词末token在309，p319，实际间隔分别128与9。完整320token原文、全部候选token、未舍入分数在[原文案例](casebook_cn.md)，没有用省略版代替原始证据。

同样远处是magnet，仅把近处object换成battery，MLP输入的真实成员从#17390=7.417934、#25508=3.940733、#16240=15.728086、#27076=13.515182，变为9.967296、3.272244、18.058294、11.246584。这些成员同时激活，却分别变强/变弱。两个完整候选分数从battery −14.919217、magnet −10.370538，变成battery −8.837065、magnet −9.626400；正确分差由+4.548679变为−0.789335nat。

固定近处battery再把远目标从magnet换成battery，#16240从18.058294到19.557859；固定近处magnet时同一远目标改变使其从15.844104到18.563541。这个成员仍有目标条件差异，但其他成员的方向与幅度也在变。不能把单个激活上升直接命名为“记忆增强”。

把两种固定近处条件的目标差平均记为T，把固定远目标下的近词差平均记为N；以中性目标差为投影参照，F23在MLP输入的T=0.6001、N=0.6631，相反对角保留=T−N=−0.0631。Attention相应为0.4903、0.4823、0.0080。**这是所选坐标中的两项接近、作差后方向很弱；T−N等式本身是代数恒等式。** 两个位置都还可见正的目标分量，不能说远处事实被完全擦除。

### 反例阻止我们把这个例子讲成统一机制

MLP输入F11(ball/die)相反对角保留−0.0234，但A/B仍正确，较难的die分差仍+0.3512nat；F19也是保留−0.0391却成对正确。F27(map/chart)保留+0.5307，目标T=0.8376，却有一条误判（−0.2278nat）。F28保留+0.7148，但中性已失败，说明候选/模板难度与行为底线也重要。原文案例保留F23和全部留出失败F27/F28，以及第一个上述成功反例F11。案例展示规则的实现修正另有时间记录，不改变任何候选、指标或检验。

## 第三层：联合模式超出单成员频率了吗

分别固定发现侧4个二元组合与4个强度组合。二元重排在每个条件内保持全部30000成员出现数和每位置32成员；强度重排保持实际成员支持与每个成员正激活值的完整多重集。每侧256次参照，二元链Rhat≤1.023、ESS≥209，6144次度约束检查全部通过。

二元联合方向在留出未通过（两侧Holm p=1）。强度联合在固定留出面板相对边际重排都偏离，Holm p=0.0156；但家族区间分别[−1.0481,1.6578]和[−0.5500,0.7673]跨0，未满足预定的稳定家族推广条件，故H4主要判断仍为证据不足。不能删去条件重排的阳性，也不能只凭该p值宣称跨家族组合已经确认。幅值参照未保持每位置总范数，通用幅值协变仍是竞争解释。

## 频率组：低频参与可见，支持与语义要分开

MLP固定C含高频#17390/#3011/#16240/#27076、中频#4700、低频#25508；Attention的#772为低频，其余C为高频。完整留出中，Attention高/中/低组实际出现160/59/22个成员，MLP为66/35/27；三组均覆盖12家族，低频位置覆盖分别140/144与144/144。频率不足和参考零次组独立保留，例如MLP#24506在旧参考为零、本任务65位置/10家族阳性；这不能推出新概念或新训练能力。

![参考频率组及实际覆盖](figures/frequency_participation.png)

图中右侧是逐成员绝对改变量乘decoder列范数后的总量占比，未表示成员间向量抵消，更不是隐藏空间能量或因果贡献。频率来自独立旧参考300文档/38400位置，分组在本次留出读取前固定。

## 逐条判定与认识边界

'''+ph+jh+'''H3的MLPρ=0.6364，95%区间[0.0397,0.9077]，原始p=0.0142，Holm p=0.0568；模板内交换p=0.25。去句号只计物品词时ρ=0.5944，区间[−0.0771,0.9070]。因此支持组合与偏好都改变这一局部现象，尚不支持完整、稳健的跨家族行为解释。Attention的H1/H2/H3均因共同成员支持不足而证据不足，不能把MLP通过、Attention未通过当成两者存在显著差异。

原始数据支持：同一批成员可同时随远目标与近词改变；部分事实差异跨距离保持；组合可观察性与最终选择存在分离反例。可能原因包括目标/近词同时投影到复用成员、其他未选成员、输出读出、候选先验、句号及模板。旧无事实基线在d128偏好battery/ball/map/card，A−B分别+1.7512/+5.1302/+1.9900/+2.5590nat；它与竞争后错误方向相容，但旧基线不是新竞争框架的精确中性消融，不能拿来扣除因果先验。候选同长度并不能消除词先验。

这里没有连续时间追踪“竞争信息到来之前与之后”的同一次生成过程；观察的是同一答案位置在配对前缀下的表征。共同激活、联合幅值结构、与行为关联也不等于模型因果使用这些成员。主距离还混有绝对位置/填充顺序；两字典重建留出相对误差中位数约0.4793/0.2878；只取6成员更不代表全部信息。模型自由生成、一般理解、训练/路由价值和跨任务泛化均未验证。

所有逐家族结果、缺失、原始向量、原始评分与联合参照均保留。[数值附录](numeric_evidence.md)、[执行记录](detailed_cn.md)、[数据定义](dataset_guide_cn.md)、[资产与复算入口](artifacts_cn.md)。**本轮已停止，等待共同审阅，再决定是否设计功能干预或训练。**
'''
en='''# R19: reused members retain fact contrasts; competition does not yet yield a complete behavioral account

## Bounded finding and purpose

In these constructed English prefixes, one discovery-fixed six-member MLP-input SAE list retains within-family target contrasts across nearby words and across main16/main128conditions. Nearby competition changes the same members' strengths and lowers candidate margins. The full family-level explanation of behavioral degradation does not pass its registered multiplicity gate. Attention's primary common list has inadequate heldout coverage. Scientific acceptance and the next experiment remain pending researcher review; no training or activation intervention occurred.

R18 main gaps16/64/128each achieved24/24paired switches; the legacy opposite-near-item condition achieved17/24. Legacy main-versus-lure also changes filler/clause, and legacy lure A/B changes both target and nearby word. We preserve all R18bytes and add96prefixes to complete a role-matched distantA/B×near unidentified/A/B factorial. Qwen3-0.6B Base, its tokenizer and both native pretrained SAEs are unchanged. Capture p319colon tokenID25in320-token prefixes: block27Attention.o_proj output before residual, and actual block27MLP input after residual/normalization. Each dictionary has30000atoms/Top32, with separate ID spaces. Gap=p−e−1excludes both endpoints; main e302/254/190gives16/64/128.

There are24families,12discovery/12representation-heldout within six shared template strata; all conditions of one family stay together. Prior behavior was exposed. All292forwards(including4smoke) completed;196legacy prefixes replay both candidate totals exactly.

## Behavior and membership

Heldout main16/64/128remain12/12paired. Matched unidentified-near-object is11/12,congruent12/12,opposite9/12. Correct-margin means drop5.9946→2.1802nat; mean loss3.8144,95%family interval[2.8466,4.9116]. Opposite failures areF23/F27/F28; F28already fails the matched-neutral baseline. Pooled old opposite remains17/24; this is not new behavioral confirmation.

Same-fact16→128pairs share24.79/32Attention and27.92/32MLP members on average. Neutral→opposite pairs share23.79and27.88,with8.21and4.13entries/exits. Fixed32makes entry=exit an identity. Same-fact Jaccard exceeds fact-swapped near/far Jaccard by0.1973and0.1575across12families, separating some fact-aligned overlap from generic question overlap without separating lexical form from object identity.

## Strength geometry, literal example and counterexamples

Attention C=[2520,26235,29969,23899,772,2254]; MLP-input C=[17390,25508,3011,4700,16240,27076]. Raw values and within-C L2-normalized strengths are retained. Every family supplies its own A−Breference; no universal cross-family semantic axis is fitted. MLP H1target alignment is0.7449(N12,CI[0.6362,0.8430],Holm p0.001465); H2near/far contrast cosine0.9713(N11,CI[0.9632,0.9794],p0.002441). F23has actual zero#25508inmain16_Aand is explicitly ineligible for primaryH2. Attention only5strict far-factorial/6strict near-far families, below the predeclared8minimum; the nested3-list cannot rescue the primary.

F23was fixed before heldout extraction. Its drawer contains magnet, the nearby other container changes object→battery, and the final drawer question is unchanged. At MLP input,#17390changes7.417934→9.967296,#25508 3.940733→3.272244,#16240 15.728086→18.058294,#27076 13.515182→11.246584. Both candidates' complete scores change from(battery−14.919217,magnet−10.370538)to(−8.837065,−9.626400); correct margin+4.548679→−0.789335nat.

The target contrast remains visible when nearby words are held fixed: e.g.#16240still changes18.058294→19.557859under nearbattery and15.844104→18.563541under nearmagnet as remote target changesmagnet→battery. The normalized average target-effect projectionT=0.6001and nearby-word-effect projectionN=0.6631nearly cancel in the opposite diagonalT−N=−0.0631. Attention values are0.4903/0.4823/0.0080. T−Nis algebra, not a newly discovered mechanism; a positive target component remains observable.

Counterexamples matter: MLPF11(ball/die)has opposite retention−0.0234yet both choices remain correct(the harder margin+0.3512); F19also retains−0.0391and succeeds. F27(map/chart)retains+0.5307,targetT0.8376yet one choice fails(−0.2278). F28retains+0.7148and already fails neutral. The full literal-prefix/token-score casebook includesF23,allthree heldout failures,and the first successful nonpositive-retention counterexampleF11. A presentation-rule implementation correction is timestamped, without changing any scientific selection/test.

MLP H3pattern loss averages0.4810,CI[0.2872,0.6900]. Its relation to margin loss isrho0.6364,CI[0.0397,0.9077],raw p0.0142,Holm p0.0568; within-template swap p0.25. Item-only rho0.5944has CI[−0.0771,0.9070]. This supports the local combination/behavior changes, not the full robust behavioral explanation. Attention H3is insufficient atN5. One site's pass and another's nonpass do not establish a site difference.

## Joint structure and frequency

Discovery fixes four pairs per site/kind. Binary Curveball preserves all30000column degrees and32members/row within condition/split; positive-value permutations preserve support and each feature's positive-value multiset. All6144degree checks pass; binaryRhat≤1.023,ESS≥209. Binary heldout direction tests fail to reject(Holm p1). Both amplitude tests reject the conditional fixed-panel null(Holm p0.01556),but family intervals[−1.0481,1.6578]and[−0.5500,0.7673]cross0. The registered conjunction therefore remains insufficient for stable cross-family replication. Neither hide the conditional positive nor upgrade it to universal combination evidence. The amplitude null does not preserve row total norm; generic amplitude covariance remains a rival.

MLP Ccontains four reference-high members,#4700middle,#25508low; Attention Ccontains low#772and fivehigh. Observed heldout high/middle/low unique members are160/59/22Attention and66/35/27MLP,allcovering12families; low-group positions140/144and144/144. Reference-insufficient and zero groups remain separate; MLP#24506was zero in the old reference but positive at65positions/10taskfamilies, not evidence of a new concept. Groups were fixed from each native dictionary's independent300document/38400position reference before heldout reads. Decoder-weighted absolute atom changes are not hidden-space energy or causal contributions.

## Interpretation and limits

The observed combination comprises reused members with distinct conditional strength changes, rather than a semantic name attached to a single atom. Fact/distance alignment replicates in the chosen MLP list; competition changes both target-related and nearby-word-related contrasts, but their observability can separate from final choice. Other members, downstream readout,candidate priors,periods and templates remain live explanations. Old no-fact d128baselines preferbattery/ball/map/card by1.7512/5.1302/1.9900/2.5590nat; these are contextual prior diagnostics, not an exact new-factorial ablation or causal subtraction. Equal token counts do not remove lexical priors.

This is a paired-prefix comparison at one answer position, not a temporal trajectory during one generation. Main distance also changes absolute position/filler order. SAE relative reconstruction error medians are0.4793/0.2878on heldout, and six selected members represent only a small part of either dictionary. Full sequence margins include later candidate/period predictions, which cannot all be localized to p319. No causal necessity, semantic atom identity, general memory/free-generation capability or training/router utility is established.

[Numeric evidence](numeric_evidence.md),[literal cases](casebook_cn.md),[Detailed](detailed.md),[data definitions](dataset_guide.md),and[artifact/replay index](artifacts.md)retain all families, zeros, failures, support counts and uncertainty. STOP for researcher review before any intervention/training design.
'''
(C/'summary_cn.md').write_text(cn);(C/'summary.md').write_text(en)
runtime='''292prefixes,288formal plus4smoke; CPU FP32,2threads,SDPA,2×328physical scoring shape. Captured hooks are no-op with exactly zero output difference; both candidate lanes have identical prefix capture. Native Top32equals manual encoder/ReLU/TopK.196old prefixes replay exactly; every candidate token score sums to the saved total. Model/tokenizer/SAE hashes were checked before/after stages. No parameters trainable, no optimizer, no training update or intervention. Strict source/output asset checks are separate from scientific acceptance.

The first heldout process received external SIGTERM(exit143)after120logged rows;130partial candidate records and no complete SAE cache were preserved. The issuer is Unknown. An identical full-stage replay was run after restoring the original runtime environment. Two import-only restart failures(missing module path and protobuf setting)performed no forward; their logs remain. The successful replay completed144rows in440.96seconds. No split/member/config/test changed. Discovery candidates/directions and primary analysis hashes precede every heldout feature forward.

Formal near-factorial rows fix gap128/e190/p319; smoke rows include gap16and128and are not factorial rows. The independent verifier initially applied the formal-frame assertion to smoke; the assertion scope was corrected, without changing data. The inherited local_suffix fields in96supplements were stale metadata only; actual text/token IDs and fresh roles were valid. A whitelisted portable view derives the actual suffix and is identity-checked on IDs/text/tokens. All136protected R18source/owner files remain byte-identical.

The original case-display implementation compared only Tprojection sign and returned no counter, missing opposite-diagonal cases. The presentation correction retains the preselectedF23and displays allheldout failuresF23/F27/F28plus firstsuccessful nonpositive-diagonalMLPF11; no hypothesis/candidate/result changed. Initial figure code/selection and both Protocol original versions are archived; UTC,visibility and affected scope are recorded. Plot legend/headroom corrections are presentational.
'''
method='''Hypothesis tests use the fixed six-member list; at least8strict families are required. H1requires allsix matched far rows' Cpositive; H2allfour main16/128rows; zeros and first3sensitivities are retained, never substitute. H1/H2exact2^Nsign swaps; H39999label permutations with family bootstrap4096; six primary p-values are Holm-adjusted including ineligible p=1. Shared-template sensitivity resamples six template means, and H3also swaps only the two heldout families within each template(64permutations). These small constructed-family intervals are conditional, not a claim about a broad text population.

Binary nulls use4chains,burn100,thin10,64draws/chain,unchanged S09C++source; proposals include no-op/failed trades. No long retry was necessary. Allfull-dictionary row/columnconstraints are checked every draw and independent saved snapshots/toy sets pass. The condition×split null does not preserve semantic family labels. Amplitude permutations independently shuffle each atom's actual positive values within its active rows/condition; they preserve support/marginal multisets but not row norms. Discovery fixes pairs and signed direction; heldout projects own-null residual onto that direction. Four H4tests receive separate Holm4;family intervals condition on fixed direction/nullcenter. MonteCarlo pminimum1/257and worst-case MCSE0.03125are explicit. Joint tests summarize pooled joint structure, not a target-specific semantic circuit.

Paired raw/relative T,N,Iand the opposite/congruent identities are retained. A/Bnames are local to a family. No classifier/probe/model/SAEfit was used. L2normalization is descriptive and can itself induce dependencies; raw-valuesensitivity and amplitude tests without row normalization are separately retained. No cross-SAEfeature alignment or site-difference claim is made. Fact-aligned/swapped Jaccards use all32positive members, separate from selected-list strength analysis.
'''
(C/'detailed.md').write_text('# Execution and statistical record\n\nScientific acceptance: Unknown. Factual computation complete; no question closure.\n\n## Execution, provenance and incidents\n\n'+runtime+'\n## Computation, controls and uncertainty\n\n'+method+'\n## Results and raw ownership\n\n[Summary](summary.md) owns interpretation; [numeric annex](numeric_evidence.md) contains all heldout family values and predeclared sensitivity summaries. Full observations remain at `'+str(R)+'`. [Artifacts](artifacts.md) lists every input/output. Processing-agent self-review only; no independent human review is claimed. The original frozen Protocol is preserved, with presentation-only appendices. The registered scope is completed and stopped.\n')
(C/'detailed_cn.md').write_text('''# R19 执行与统计记录

科学接受Unknown；计算和事实记录完成，不宣告问题关闭。[Summary](summary_cn.md)拥有认识更新，[数值附录](numeric_evidence.md)逐家族保留六成员支持、原始/相对搭配和行为。处理者为Codex /root（Codex desktop，GPT-6）；自检不冒充独立人工审查。

## 实际执行和中断

292前缀全部完成，正式288+smoke4。CPU FP32/2线程/SDPA，物理2×328候选前向；hook无操作误差0、候选两路前缀误差0、原生Top32与手工实现完全一致。196旧前缀逐候选重放总分误差0，292条token/证据位置复核通过。模型、tokenizer、两SAE执行前后哈希保持，无训练参数/优化器/训练更新/激活干预。

第一次留出进程外部SIGTERM，exit143，日志到120，部分评分130条、无完整feature缓存；发送者未知。部分文件全部保留。随后相同脚本重跑全144条；两次仅导入失败由恢复原环境变量解决，无前向。最终留出440.96秒完成，未修改样本/划分/候选/指标。发现选择、联合方向及主要分析代码的哈希冻结早于所有留出feature读取。

## 元数据与展示修正

补充96条的继承local_suffix字段过时，但实际全文/token/证据/近词位置正确；导出视图按实际文本重建后缀并验证ID/全文/token相同。四smoke误带matched_far框架标签，不作为正式矩阵，验证器的形式断言已限定正式行。原R18及旧Anchor/Focus共136文件字节保持。

初版案例展示只比较T投影符号，漏掉相反对角保留的反例；展示修正保留预先选的F23，另保留全部失败F27/F28及首个MLP非正对角但答对的F11。原展示代码/选择、原协议均归档，时间与已见数据单列。没有改动检验、成员或数值结果。图例重叠与频率标签顶部空间修正仅影响呈现。

## 统计与支持分母

主六成员严格门槛≥8家族。H1/H3要求远矩阵六条全部成员阳性，H2要求近远四条；保留零和缺失，第一批3成员不救回主门槛。H1/H2用全部2^N家族符号互换，H3用9999家族标签置换，4096次整家族bootstrap；六项主要p包含不足项p=1，再Holm校正。模板敏感性对六个模板均值取区间；H3另给模板内两家族交换的64排列p。区间限于这批构造家族，不代表一般文本分布。

两套字典各自的二元重排4链、burn100、thin10、每链64draw；本次均无需预定延长。6144个度约束快照检查通过，独立Python列计数/集合检查通过。该参照保留每条件全部列频率和每行32成员，未保留家族语义标签。幅值参照固定支持、逐feature正值多重集，未保留每行总范数。发现侧固定4对/种类和6条件×组合方向；留出相对自己的null中心做投影。四项联合检验独立Holm4；家族区间以固定方向和null中心为条件。256参照使最小p=1/257，最坏MonteCarlo标准误0.03125。

原始与相对T/N/I、相反/一致恒等式逐条保存。A/B不是跨家族通用语义标签。L2归一可能引入依赖，故原始值敏感性和不按行归一的联合幅值检验分开保留。decoder列范数约1；逐成员绝对改变量不是向量能量。无跨SAE ID对齐，无两位置显著差异的推断。两套留出重建相对误差中位数0.4793/0.2878。

## 已完成的自检与停止点

逐token评分总和、实际token距离、近词位置、完整Top32、组合恒等式、发现冻结时间、重排度约束、旧136文件哈希已核。小包另做新目录提取、全文件SHA、CRC、链接和无模型离线复算。图经实际查看；完整记录在执行侧evidence。若组织导航检查保留他人既有问题，交付记录会明确列出，不擅自改写他题。

本轮停止；不自动设计或运行功能干预、训练或下一轮模板调优。待研究者共同审阅。
''')
print('SUMMARIES_AND_DETAILS')
