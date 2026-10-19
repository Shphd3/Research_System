import json,csv,shutil,os,hashlib,datetime
from pathlib import Path
P=json.load(open(Path(__file__).resolve().parents[1]/'config/frozen.json'))['paths'];R=Path(P['run']);E=Path(P['experiment']);A=Path(P['anchor']);D=Path('/data/250010109/Research_System/daily_research_reports/1019');cfg=json.load(open(R/'config/frozen.json'))
def readcsv(p):return list(csv.DictReader(open(p)))
def mdtable(headers,rows):return '\n'.join(['|'+'|'.join(headers)+'|','|'+'|'.join('---' for _ in headers)+'|']+['|'+'|'.join(map(str,r))+'|' for r in rows])
def rel(p,base=E):return os.path.relpath(p,base)
def f(v,n=4):return f'{float(v):.{n}f}'
(E/'figures').mkdir(exist_ok=True);(E/'tables').mkdir(exist_ok=True);(E/'evidence').mkdir(exist_ok=True)
manifest=[]
for group in ['figures','tables']:
 for fp in (R/group).iterdir():
  if fp.is_file():
   dst=E/group/fp.name;shutil.copy2(fp,dst);manifest.append(dict(path=str(dst),source=str(fp),bytes=dst.stat().st_size,sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),purpose='selected analysis evidence requested for complete result discussion; not raw hidden/weights'))
for name in ['final_verification.json','pairing_audit.json','source_manifest.json','checkpoint_members.json','denominators.json','preparation_receipt.json','profiles_receipt.json','pipeline_status.json','analysis_receipt.json','input_access.json','engineering_failure_v1.json','figures_manifest.json']:
 shutil.copy2(R/'provenance'/name,E/'evidence'/name)
shutil.copy2(R/'smoke/receipt.json',E/'evidence/smoke_receipt.json');shutil.copy2(R/'target/recommendations.json',E/'evidence/target_recommendations.json');shutil.copy2(R/'target/oracle_ranking.json',E/'evidence/target_oracle_ranking.json');shutil.copy2(R/'texts/fixed_windows.json',E/'evidence/fixed_windows.json');shutil.copy2('/tmp/normalized_learning_final_job.json',E/'evidence/final_job.json');shutil.copy2('/tmp/normalized_learning_new_asset_ids.json',E/'evidence/output_asset_ids.json')
(E/'curated_evidence_manifest.json').write_text(json.dumps(dict(evidence=manifest,excluded=['raw hidden/z caches','base/dictionary/branch checkpoints','raw training logs and TensorBoard event payloads','full response matrices'],payload_root=str(R),outputs_registered=True),ensure_ascii=False,indent=2)+'\n')
ends=readcsv(R/'tables/all_condition_results.csv');lookup={(r['condition'],int(r['seed'])):r for r in ends};pairs=readcsv(R/'tables/paired_outcomes.csv');route={r['condition']:r for r in json.load(open(R/'metrics/routing_summary.json')) if r['split']=='eval'};base=lookup['T_S0',11];baseN=float(base['initial_overall']);baseL=float(base['initial_M_L']);target=readcsv(R/'tables/new_input_assignment.csv');finals=sorted([r for r in target if r['step']=='32'],key=lambda r:int(r['expert']));probe=readcsv(R/'tables/expert_probe.csv');ver=json.load(open(R/'provenance/final_verification.json'));peakGPU=max(r['peak_GPU_bytes'] for r in ver['main_models'])/2**30;peakCPU=max(r['peak_RSS_bytes'] for r in ver['main_models'])/2**30;disk=sum(p.stat().st_size for p in R.rglob('*') if p.is_file())/2**30
mainrows=[]
for n,label in [('T_S0','A：T原评分'),('T_S1','B：T组级校准'),('R11_S1','C：随机名单组级校准')]:
 for seed in [11,22]:
  rr=lookup[n,seed];mainrows.append([label,seed,f(rr['overall']),f(rr['M_L'])])
primarytable=mdtable(['条件','训练seed','整体NLL','低频主指标M_L'],[['冻结基座','—',f(baseN),f(baseL)]]+mainrows)
nextcn='AI建议：先用独立开发集确定各条件共用、较小的旁支更新强度，再在新留出文本上复核A/B/C；用这一项比较区分当前过度拟合/更新幅度问题与评分组织本身的差异。尚未获下一轮执行授权。'
summary=f'''# 一页概要：接收改善没有转化为本轮留出学习收益

本轮已完成10条件×2种子、各3epoch；另完成同输入专家探针、参数/响应谱及一个目标留出更新场景。以下是预定规则下的事实与AI解释，研究者的机制判断和科学状态仍为Unknown。

## 目的与模型

检验：固定频率名单上的评分校准，能否帮助包含低频feature的输入学习。Qwen3-0.6B Base、14层联合CrossCoder、原final norm/head冻结；在第28层末端加8个完整SwiGLU残差专家。每位置选1个专家，原h完整保留。低频指TRAIN激活频率低，不等于难词或未掌握知识。

## 三条认识更新

1. **保留“评分尺度会阻碍接收”的判断，撤回“只修条件幅度就够了”。** T的S1使EVAL低频目标接收率从0.0023%到33.4033%，零接收960→5；S2仍为0%/964项零接收。S3接收41.6942%，但不是学习最优。接收率是逐feature“命中时到达指定专家”的比例再等权平均。[图5](figures/figure5_dispatch_outcomes.png)、[原表](tables/routing_before_after.csv)。
2. **本轮不支持“接收改善足以带来留出学习收益”。** 主方案B对A的M_L差为+0.1807/+0.1853，方向变差；B对随机C为−0.0326/−0.0256，虽相对较好，仍未通过两对照联合门槛。20个终点的整体和M_L均差于冻结基座。TRAIN拟合下降而EVAL上升，指向本设置的泛化问题，尚未唯一归因于数据、更新幅度或分组。[学习曲线](figures/figure7_primary_learning_curves.png)、[配对差](figures/figure8_primary_paired_differences.png)、[全部20终点](tables/all_condition_results.csv)。
3. **本例不能交付安全的新输入归属规则。** TRAIN选定feature2，独立背景排除其269个位置更新；8专家匹配适配后，94个目标EVAL位置的NLL均上升，旧输入损害0.0206–0.0517，全部超过0.01门槛。无安全候选。名单/实际路由推荐0，适配前TRAIN预测推荐5；不能将事后未达安全线的expert6称为推荐成功。[图10](figures/figure10_target_assignment.png)、[逐项表](tables/new_input_assignment.csv)。

{primarytable}

NLL单位nat/token，越低越好。M_L是固定964个低频feature各自命中位置NLL的等权均值；位置可重叠。B=T_S1为事前主方案；R11固定一个随机名单，训练seed11/22不是两个随机名单。

## 边界与下一决策

T的S1确实降低了评分选择对高频项的依赖，但完整专家输入仍含高频信息；同频分工不由接收或负载图保证。教师联合z有额外获取成本。本轮仅冻结表征旁支，不能证明从头预训练容量或φ的学习价值。TRAIN/EVAL来自不同bin，原文档去重未知；EVAL已被查看，两seed和块区间只描述本设置。

{nextcn}

[完整报告](detailed_cn.md) · [图外解读](figures_cn.md) · [合并Protocol](protocol_cn.md) · [工程核验](evidence/final_verification.json)。计算约615.9秒，使用原授权4卡H100；本轮停止，不追加实验。
'''
(E/'summary_cn.md').write_text(summary)
allrows=[[r['condition'],r['seed'],f(r['overall']),f(r['M_L']),f(r['train_diagnostic'])] for r in ends]
alltable=mdtable(['条件','seed','EVAL整体NLL','EVAL M_L','TRAIN诊断NLL'],allrows)
pr=[r for r in pairs if r['role'].startswith('primary')];pairtable=mdtable(['比较','seed','ΔM_L','块95%区间','Δ整体NLL','实践门槛'],[[r['A']+'−'+r['B'],r['seed'],f(r['delta_M_L']),f(r['ML_CI_low'])+'～'+f(r['ML_CI_high']),f(r['delta_overall']),r['practice_gate']] for r in pr])
rt=mdtable(['固定路由','低频接收率','零接收/964','B≤2占固定964'],[[n,f(100*route[n]['low_receive_macro'])+'%',route[n]['low_zero_receive'],f(100*route[n]['B_le2_fixed964'])+'%'] for n in route])
tt=mdtable(['专家','适配前C_eval NLL','32步后绝对NLL','收益before−after','旧输入损害'],[[r['expert'],f(next(q['C_absolute_NLL'] for q in target if q['expert']==r['expert'] and q['step']=='0')),f(r['C_absolute_NLL']),f(r['gain_before_minus_after']),f(r['B_old_cost'])] for r in finals])
full=f'''# 完整报告：归一化路由与冻结表征上的专家学习

[一页概要](summary_cn.md) · [冻结Protocol](protocol_cn.md) · [Anchor]({rel(A/'anchor.md')})。记录日期：2026-10-19，北京时间。执行事实COMPLETE；主学习假设按预登记规则NOT SUPPORTED；研究者机制判断、科学批准与下一轮状态Unknown。

## 1 目的与本轮问题

长期目标是在固定参数和计算预算下改善专家有效分工。本轮只问：保持原表征、名单、专家与训练预算时，按TRAIN常态校准的评分是否改变实际接收，并改善包含低频CrossCoder feature的位置的留出NTP预测。频率、条件幅度、共同出现和学习收益是四个对象，不能相互替代。

## 2 结论：三条认识与研究决策

第一，原竞争尺度确实阻碍了接收。S1的接收33.4033%、零接收5；S0为0.0023%、960。S2只去掉条件幅度差异，依旧0%接收。S3达到41.6942%、无零接收，但不因此成为学习最优。**保留校准分数的必要性，撤回条件幅度校准必然足够的直觉。**

![分发](figures/figure5_dispatch_outcomes.png)

图5左是实际位置负载，中是逐feature接收率的宏平均，右是零接收数，三个分母不同。源表：[接收/全q](tables/routing_before_after.csv)、[组到实际专家](tables/group_to_actual_expert.csv)。

第二，**接收变好不足以推出学习变好**。S1比S0低频NLL高0.1807/0.1853，却只比随机S1低0.0326/0.0256。B相对C的两个实践门槛通过，B相对A的两个失败；联合H2不支持。所有20条件整体与低频终点都差于原基座。TRAIN诊断样本NLL下降、EVAL逐epoch上升，观察更符合当前有限训练泛化失败；本轮没有唯一识别更新幅度、过拟合、数据分布与分组各自份额。**暂不以更高接收率、均衡或谱形状选策略；优先解决学习比较的基座保真度。**

![主曲线](figures/figure7_primary_learning_curves.png)

图7横轴累计有效预测位置，纵轴nat/token的NLL；实线/虚线为seed11/22。所有条件训练到同一392136位置终点，不挑最好epoch。

第三，目标条件留出场景也没有安全适配。所有8项目标NLL上升，旧输入损害均>0.01，故安全oracle集合为空。**不把原始最低终点expert6当成可部署归属，也不把失败唯一归因于路由挑错。**

![目标适配](figures/figure10_target_assignment.png)

图10左横轴为收益before−after，负值表示变差；纵轴为旧输入损害，虚线是0.01。右侧同时保留各起点与绝对终点，避免把下降量和最终表现混为一谈。

## 3 机制直觉、事前假设和竞争解释

H1：同T名单下，S1相对S0提高低频目标接收，按本轮定义得到支持。H2：S1相对原评分及随机名单S1同时改善M_L≥0.01，整体恶化≤0.01，两个seed均满足；没有得到支持。S2/S3是用户训练前追加的扩展，不按EVAL选最好者后回写假设。

解释：原评分a_i=z_i w_i，既受频率p_i影响，也受激活时幅度m_i影响。由E[a_i]=p_i m_i，S2的TRAIN组均分是组内平均p；S1/S3的TRAIN组均分均为1。它们只是均值恒等式，不保证argmax负载、实际q或学习收益。[完整推导](score_mean_derivation_cn.md)。本轮原正分母无0、无地板触发，排除了极小地板造成分数爆炸这一解释。

同频名单本来就不移除输入h内的common信息。所有T/R11都不让原Top10参与评分，但它们仍可随完整h进入任何专家。上一轮φ调整489次交换、175个成员后实际路由未改变；本轮没有Tφ训练，不能称为φ学习效用验证。此前记录只作为来源背景，不与本轮损失合并。

## 4 模型、冻结对象与成本

冻结Qwen3-0.6B Base、CrossCoder、final RMSNorm和原绑定词表头。缓存h是第28层residual-post、final norm前；共享z来自14选层联合编码，不能当作14套独立激活。单层贡献c=z||D28||使用原字典中心化vector-RMS坐标，与路由a=zΣ14||D_l||分开。

u=h/a，a=sqrt(mean_TRAIN||h||²/1024)，不减均值。8个独立无偏置SwiGLU，1024→1024→1024，每expert三矩阵3145728参数，总25165824；学习router另8192。每位置top1，专家前向约6291456矩阵FLOPs，未含激活函数、原head和教师；学习router约16384矩阵FLOPs。固定路由用同一原h，校准改变选择权，不凭空增强低频信号。

h_out=h+a×门乘数×expert(u)，经过原BF16 norm/head计算NTP。固定条件门乘数1；D/E选中softmax概率，不归一化回1。头参数冻结但输入梯度开启。gate/up std1/sqrt1024，down初始0，初始logits误差0；不是全参数置0。缓存省去本轮重复教师前向，未来在线联合编码仍需14层表征和约469762048矩阵FLOPs/token的稠密编码，不能称免费中间层router。

## 5 条件、评分与数据

S0=组内a_i均值；S1=S0/本组TRAIN均值；S2=组内a_i/m_i均值；S3=组内a_i/(p_i m_i)均值。不叠加，未激活0、分母原组人数。T/R11固定9605候选、人数1257/1347/1506/1629/1824/1189/523/330；R11只一个名单，模型seed11/22是另外一层随机性。D/E普通学习gating，E加完整有效batch均衡项8Σstopgrad(f_e)mean(P_e)，λ=.01，D为0；固定路由无LB。

TRAIN130712位置、128上下文；EVAL65402位置、64上下文，来自不同bin。原文档/近重复独立性未知；字典训练见过文本，EVAL先前已查看。p/m/μ、名单、低频L964、高频H962只由TRAIN确定，未用学习结果调节。完整源文件/旧缓存/模型身份见[输入访问](evidence/input_access.json)和执行侧cache_preparation_receipt来源链。

每个主模型3epoch，AdamWlr3e-4，betas(.9,.95)，eps1e-8，wd.01，clip1；warmup39步、cosine至.1lr；有效batch512、micro128、尾批152，PCG64按seed逐epoch不放回。FP32参数/优化器、BF16矩阵乘、FP32CE。20个模型均768步/392136曝光，总7842720；背景510步/260886，8适配共16384，总正式曝光8119990，均不是独立源样本数。64位置拟合与10步计时副本另计，不进入正式初始状态。

## 6 已实测的激活画像和分发

两个固定源顺序64token窗、z/c同网格、全局p独立侧栏、全split正激活事件的幅度中位数/IQR、所选低频feature全64位置排名及前5片段均已交付。展示规则按窗口最大c取4个Top10/4其他/8低频，非语义或loss挑选。原始文本及完整可见前缀在[文本附录](text_profiles_cn.md)。右文仅事后阅读，绝不进入路由。

第28层重建EVAL raw相对平方误差0.048508，中心化坐标0.136072；TRAIN为0.049927/0.138394。差别来自原均值和范数的分母，不是两个FVE互相矛盾。公式均为Σ||误差||²/Σ||对应原向量||²，非位置比值平均。原z和c训练后逐项不变已实测复读通过。[重建表](tables/reconstruction28.csv)。

{rt}

B是原Top10相对目标在指定专家内q的正log10优势均值；B≤2不是每个头部项都在100倍内，更不是相同频率。S1只有69/964达到B≤2，S3为45/964：更好接收仍不等于已经同频分工。空专家q记NA，零接收/∞/NA不删；所有962高频feature的union覆盖全部EVAL，故高频union NLL等于整体NLL，高频逐feature宏均值另存。

附加、事后描述“选中组内最大评分项”显示：T_S0有99.9985%的位置该项来自TRAIN定义H，S1为21.2623%，S2为100%，S3为16.0790%。这是对选择依赖的有界代理，不证明单个common语义主导，更不表明原h没有高频信息。[完整来源](tables/winning_contributor_frequency.csv)。

![组到实际专家](figures/figure13_group_to_actual_expert.png)

图13按feature命中事件计数，同一位置可命中多个组，行不是互斥token类别。图14的q分布包含所有9615项，q=0进入累计比例，空专家单列NA。

## 7 学习结果与预定判断

{alltable}

固定TRAIN诊断2048位置；初始NLL3.21169。S1降至约1.80而EVAL升至3.36/3.38；这不是“完全学不动”。有限训练下降/留出上涨与过度拟合或分布差异一致，尚不单独证明哪项是根因。

M_L先对每个固定L在其EVAL命中位置求NLL，再对可估feature等权平均；本次全964均可估，位置重叠且low union约75%，不等于独立罕见知识任务。冻结基座M_L={baseL:.6f}，整体={baseN:.6f}；低频宏NLL本来更低，也不能把“低频”自动理解为“困难”。逐feature/分频率档、位置均值与全曲线见tables。

{pairtable}

![配对差](figures/figure8_primary_paired_differences.png)

区间为1000次EVAL原上下文块配对bootstrap，seed20261019。原全数据L964均可估，重采样最少961，不填0。表30行包含不同角色下重复的同一数值比较，实际26个唯一条件对×seed记录；不能作为30个独立实验计数。两seed不是总体稳定性保证，区间不称严格独立确认。

可学习参考D整体3.0966/3.1123，E为3.1142/3.1151；λ=.01没有改善本轮留出质量，负载更分散也不能替代学习。其门幅度不同于固定路由，A/D整体差别不能全归因于频率。

## 8 同输入专家功能与谱

固定EVAL探针由上下文分层最多1024位置和最多512个L命中位置去重组成，所有expert输入完全一致、每行等权，不能当成整体EVAL分布。强制探针门1；自然替换保留原选中门。seed11时T_S1八专家强制NLL范围3.2102–3.4469，同probe零旁支3.0248；撤回旁支相对自然路由ΔNLL=−0.3269。专家输出和替换损失确有差别，但没有由此证明有用语义分工，也没有检验所有可能router。

初始/终点/ΔW的gate/up/down完整谱及前16、Frobenius范数和全能量均保存；归一化分母是完整σ²总和，down初始0记NA。ΔW含AdamW衰减，不纯粹是任务方向。响应是同probe输出，按位置轴中心化后的协方差，幅度trace和归一化形状分开。跨策略不按同ID认定功能相同；图以专家分布汇总。未更新专家可有0响应谱，这不是对所有输入“无用”的判定。详见[图11/12解释](figures_cn.md)和[谱表](tables/parameter_response_spectra.csv)。

## 9 目标条件留出更新：无安全候选

只用TRAIN按ID先取u=2，269命中/98上下文。独立T_S1/seed11背景排除这些位置，只训练其余130443位置2epoch；p/m/μ仍来自全TRAIN，故可见无标签目标统计，主干/字典也可能见过内容。不是真正新知识。

三推荐在适配前仅由TRAIN冻结：名单0、实际路由众数0（69/269）、当前强制NLL最低5。8份同背景、每份只更新expertj，完全同C_train顺序，32步×64，lr1e-4、AdamW零状态，强制门1。C_eval94位置40上下文，B_eval其余位置按原背景自然路由评价；没有将旧输入全送适配专家。

{tt}

适配后最低绝对目标NLL为expert6的2.7831，但其旧损害0.0461，且目标比自身起点更差。所有旧损害0.0206–0.0517都大于.01，安全集合为空，不能给安全oracle排名。下降量排序另存，负“收益”明确表示恶化。一次目标、一次背景seed，不外推普适归属规律。

## 10 协议一致性、修复与缺项

|项目|预定与实际|资格|
|---|---|---|
|8固定＋2学习×2seed|20/20，均3epoch/768步/392136|ELIGIBLE当前有限比较|
|原基座/字典/输出头冻结|无优化器参数，初始logits误差0，终点probe基座NLL一致|PASS|
|配对初始化/数据顺序|同seed10条件hash相同，PCG64顺序逐项核对|PASS|
|完整batch均衡/有效位置CE|D/E按完整512/尾批，micro数加权；固定不加LB|PASS，见代码/日志|
|保存/恢复|80主milestone、背景3、适配24实存；20终点新鲜SHA；独立Smoke下一更新逐位相同|正式各臂续训NOT RUN，不冒充已执行|
|原画像冻结|训练后重读两窗z/c逐项一致|PASS|
|全功能/谱/目标分支|20/20＋20/20＋8/8|COMPLETE|
|资源|4H100；GPU allocated最大{peakGPU:.3f}GiB/卡；主训练单进程RSS最大{peakCPU:.3f}GiB；执行目录约{disk:.2f}GiB|低于32GiB/卡与64GiB磁盘；aggregate峰值未独立采样，4并发与逐进程记录保留|

工程修复均保留证据：旧SCO响应新增service_time_expression导致创建前失败，仅本轮传输副本过滤非资源字段；TensorBoard采用Python protobuf实现规避环境ABI；首次任务在状态哈希误处理标量时停止，正式训练0步。将标量reshape后哈希，科学定义不变。原平台任务pt-r697pchx显示SUCCEEDED但内部门槛BLOCKED，不能称训练成功；平台禁止重启，确认终态后同4卡替换pt-falmqs6x，最终平台SUCCEEDED、内部全阶段完成。画像与统计没有重跑。

没有因负载、阴性结果而删条件、改LR、换seed/名单或缩步数；没有额外PCA/φ训练、原模型推理、完整共现重计或额外GPU预约。科学负结果不是可静默更换超参数的工程错误。

## 11 证据链与产物归属

|关键主张|原始/派生来源|计算|边界|
|---|---|---|---|
|校准改变接收|routes＋原CSR；routing_before_after.csv|指定专家命中/原命中，feature宏平均|不等于学习|
|主方案联合门槛失败|各epoch eval NLL；paired_outcomes.csv|固定L宏均值、配对上下文重采样|EVAL已查看、文档独立性未知|
|TRAIN/EVAL分离|training_steps.csv/训练诊断/全EVAL|相同样本预算与冻结endpoint|未唯一识别过拟合成因|
|同输入输出不同|functional/*/probe.npz、expert_probe.csv|强制8专家、门1；自然替换保留门|不据此赋语义或断容量|
|无安全目标归属|target/adapt/*/eval_step32.npz|绝对目标NLL＋旧损害≤.01|1目标/1背景seed|
|实际保存与工程有效|final_verification/source/checkpoint manifests、资产检查|计数/顺序/原窗口复读/TB/选定终点SHA|访问与工程通过不是科学批准|

实际执行根：`{R}`。旧缓存、base、字典没有复制到文档仓库。正式代码/原JSONL/TensorBoard/所有完整恢复状态均在执行侧；研究侧只保留请求的精选证据表/图、公开审计及来源清单。24项资产ID见[输出资产](evidence/output_asset_ids.json)，当前访问快照见资产指南；每个条件终点和80主milestone路径/字节/hash策略见[checkpoint清单](evidence/checkpoint_members.json)。

## 12 什么改变、什么仍未知、下一步

原以为：低频目标进对专家后可能形成有效学习。今天证据：接收明显改善，却训练拟合更强、留出更差；单目标的8种适配也都不安全。保留：评分校准确实改变分发。缩窄：分发性质不足以证明有用学习，更不能证明φ、语义功能或容量。未答：更新幅度、有限数据泛化、曝光分散与频率组织的相对作用。

{nextcn}

本轮执行与交付完成后停止；未更新Focus科学结论、未关闭问题、未commit/push。
'''
(E/'detailed_cn.md').write_text(full)
(E/'summary.md').write_text(f'''# Summary: improved reception did not produce held-out learning benefit

[中文](summary_cn.md) · [Detailed](detailed.md) · [Protocol](protocol.md). All10conditions times2seeds completed3epochs, plus20functional/spectral analyses and8target adaptations. Researcher scientific judgment remains Unknown.

The purpose is useful specialization under a fixed budget. A frozen Qwen3-0.6B Base and14-layer joint CrossCoder feed a residual branch of8full SwiGLU experts after block28, before frozen original norm/head. Low frequency denotes TRAIN feature hit probability, not hard/unlearned knowledge.

1. T/S1 raises EVAL low-feature assigned reception from0.0023% to33.4033% (zero-reception960to5). S2 remains0%/964zeros; S3 reaches41.6942%. This supports calibration of this competition scale, not learning usefulness. [Figure5](figures/figure5_dispatch_outcomes.png), [table](tables/routing_before_after.csv).
2. Primary S1-S0 low-feature macro NLL differences are+0.1807/+0.1853, worse. S1-R11/S1 is−0.0326/−0.0256, relatively better, but the joint preregistered criterion fails. All20endpoints worsen overall and low-feature NLL against the frozen baseline ({baseN:.6f}/{baseL:.6f}). TRAIN diagnostic improves while EVAL worsens; generalization/update size remains a live explanation. [Curves](figures/figure7_primary_learning_curves.png), [paired outcomes](tables/paired_outcomes.csv).
3. Independent target-feature2background excludes269TRAIN hits. All8matched adaptations worsen target EVAL NLL on94positions/40contexts and incur old-input harm0.0206–0.0517, exceeding.01; no safe assignment exists. List/modal-route recommend0, pre-adapt TRAIN prediction recommends5. Unsafe retrospective expert6 is not a validated recommendation. [Figure10](figures/figure10_target_assignment.png).

M_L equally averages each fixed L964feature's mean hit-position NLL; positions overlap. Negative differences are better. The primary S1 must beat both S0 and fixed R11/S1 by.01without overall harm>.01 in both model seeds. One random organization is not two independent random lists. Context-block intervals are descriptive; different bin files do not establish document independence and EVAL was previously inspected.

This rejects reception as sufficient evidence of learning benefit in the present setting. It does not establish from-scratch capacity, meaningful semantic expert roles, or phi-learning utility. Original high-frequency information remains in full h. AI next proposal, not authorized: use a separate development set to predefine one shared smaller update scale, then recheck A/B/C on fresh held-out text to separate update/generalization failure from organization effects. No follow-on experiment was started.
''')
(E/'detailed.md').write_text(f'''# Detailed: normalized routing and frozen-base expert learning

[中文完整记录](detailed_cn.md) · [Summary](summary.md) · [Protocol](protocol.md). Question and hypothesis are unchanged from the supplied Anchor plus pre-execution scoring supplement. Main execution COMPLETE, registered learning hypothesis NOT SUPPORTED in this setting; scientific approval Unknown.

## 1. Purpose, hypotheses and model

Test whether frequency-organized fixed routing calibrated to TRAIN response improves held-out next-token prediction on low-feature-hit inputs under a fixed architecture/budget. H1 predicts increased target reception; H2 requires primary T_S1 to beat both T_S0 and R11_S1 by at least.01low-feature macro NLL, overall harm at most.01, in both paired seeds. Greater participation/exposure rather than frequency organization is a rival. Reception, actual within-expert frequency and learning are distinct.

Frozen base/dictionary/norm/tied head; eight bias-free full1024-wide SwiGLU experts have25,165,824parameters, learned references add8192router parameters. h is block28residual-post before global norm; u=h/TRAINscalarRMS without centering; h_out=h+scalar*gate*expert(u). Fixedgate1; learned selected-softmax gate. gate/up random std1/sqrt1024, down0. No transformer training or new representation extraction. Joint14-layer z and its teacher cost are explicit; layer28 contribution c=z||D28|| is separate from routing a=z*sum14decoder norms.

## 2. Data, scoring and exact contract

TRAIN130712positions/128contexts, EVAL65402/64 from different bins. Reliable9615, low964, high962; T/R11candidate9605 and identical group sizes1257/1347/1506/1629/1824/1189/523/330. R11 is one fixed list; modelseeds11/22 are separate. p=TRAINhit probability, m=TRAINconditional positive a mean. S0mean(a), S1S0/meanTRAIN(S0), S2mean(a/m), S3mean(a/(p*m)); original group denominators, inactive0, no composition or quotas. Positive-class median*1e-6 floors and original0handling are frozen; no zeros/floor triggers occurred. S2's TRAINmean equals groupmean p; S1/S3mean1does not imply balanced argmax.

Threeepochs,768updates/392136positions per main model; batch512/micro128/tail152; exact paired PCG64permutations. AdamW3e-4,(.9,.95),eps1e-8,wd.01,clip1,39warmupsteps then cosine to.1lr. FP32parameters/Adam/CE with BF16GEMMs. Full-batch LB8sum stopgrad(f)*meanP, coefficient.01onlyLearnedLB,0Learned; fixedarmsnoLB. Save complete initial/epoch states and64-step recovery, optimizer/RNG/orders/counters/config. Token-indexed TensorBoard was verified on all20runs.

## 3. Main evidence and eligibility

All20models completed identical budgets. [All endpoints](tables/all_condition_results.csv), [per-feature](tables/per_feature_learning.csv), [curves](tables/training_metrics.csv), [all steps](tables/training_steps.csv), [actual exposures](tables/expert_training_exposures.csv).

{alltable}

NLL nat/token, lower better. M_L first averages NLL at each fixed lowfeature's hits then equally averages features;964estimable, overlapping positions. Lowunion is about75%ofEVAL; highunion covers allEVAL and equals overall, with separate highfeaturemacro available. Frozen baseline overall={baseN:.6f},M_L={baseL:.6f}. Lowfeaturemacro being lower than overall warns against equating low frequency with difficulty.

{pairtable}

The B-Cpractice criteria pass both seeds, B-Afail both, so joint H2fails. All20endpoints worsen both metrics against baseline. TRAINdiagnostic starts3.21169andT_S1drops to about1.80while EVALrises; this is not failure to optimize TRAIN. Current evidence is consistent with overfitting/update magnitude/distribution differences, not a uniquely identified cause.1000paired EVALcontext-block bootstraps, seed20261019, minimum961estimable features in a resample; NAis never zero-filled.30role rows represent26unique pair/seedvalues, not30independent experiments. EVALalreadyviewed/documentindependenceunknown; only2modelseeds and1randomorganization.

## 4. Activation, dispatch and function

Two preselected source-ordered64token windows; actual z/c grids, globalTRAINp, whole-split positiveeventquartiles and full low-position rankings/text are saved. Display selection by peak c is descriptive, not representative semantic sampling. Following text is posthoc only. Reconstruction EVALrawrelativeerror.048508vscentered.136072, with actual inverse raw_hat=hat*rms28+mean28; no coordinate mix. After all training, reread z/c matched original profiles exactly. [Text](text_profiles_cn.md), [reconstruction](tables/reconstruction28.csv).

{rt}

Reception is hits sent to listedowner/alloriginalhits, then feature-macro; q=featurehits/actualexpertpositions. Legacy field assigned_reception_a is reception, not routing amplitudea_i(t). Top10remains in full inputs/qeven when absent from lists. HeadgapB averages positive log10ratios, B<=2does not bound each head individually. S1only69/964pass B<=2, so better reception is not same-frequency input. [All q](tables/routing_before_after.csv), [group hit matrix](tables/group_to_actual_expert.csv), [frequency plots](figures/figure14_expert_frequency_distributions.png).

A posthoc descriptive largest-score-term diagnostic finds T_S0Hmembership99.9985%,S1=21.2623%,S2=100%,S3=16.0790%; it is not semantic common dominance or absence of highfrequency information. Previousphi reorganization changed175members after489swapsbut no route; no phi training ran here.

Fixed common EVALprobe: contextstratified general<=1024plus<=512Lhit positions, deduplicated/uniformrowweights. Gate1forced8expertlosses and naturalgate-preserving replacements are distinct; seed11T_S1forcedNLLrange3.2102–3.4469against same-probezero-branch3.0248; zero-natural difference−.3269. Different outputs/replacementlosses do not certify semantic roles or every possible router. Full initial/final/delta gate/up/down spectra and centered response covariance spectra are saved. Normalize by full energy, zerodowninitial=NA. DeltaW includes AdamWdecay, spectra are neither directions nor capacity. No cross-policy functional IDmatching.

## 5. Independent target scene

TRAIN-only firsteligiblefeature2has269hits/98contexts. Independent T_S1seed11background excludes them:130443uniquepositions,2epochs/510steps/260886exposures. Frozen routing statistics see unlabeled target features; base/dictionary may know content. Recommendations fixed before adaptation using TRAIN: owner0,modalroute0,currentforcedprediction5. Eight copies eachupdateonlyexpertj,identical target order,32stepsbatch64/lr1e-4/resetAdamW,gate1; eval0/8/32. C_eval94positions/40contexts; B_eval uses background natural routes.

{tt}

All8worsen targetNLL and violate oldharm<=.01. Safeoracleempty; expert6lowest final2.7831still unsafe and worse than its own start. Rank by absolute adaptedloss, not only improvement. This one-target/one-backgroundseed result is neither truly new knowledge nor an assignment algorithm.

## 6. Conformance, failures and authority

New scientific definitions/budget unchanged. Sole engineering fixes: scopedSCOunknownresponsefield filter; PythonprotobufTensorBoardcompatibility; scalarstatehashreshape. Initial jobpt-r697pchxhad platformSUCCEEDEDbut internalengineeringBLOCKEDbeforeformalupdates; immutablejobworkspacepreventedrestart. Terminalconfirmed, replacementpt-falmqs6xusedthesame4H100profilewithnooverlap/reservationexpansion, reused profiles/statistics, thencompleted. Formal budget/finitenegativeconditionswerenotchanged.

Initiallogitsmaxerror0, postfirstexpertupdatelearnedrouterCEgradientnonzero,64positionsfit to~1e-6,exactnextupdateSmoke replayPASS. All20formalstateshaveoptimizer/RNG/orders/counters; formalindividualcontinuationsNOTRUN. FinalcheckpointSHAfresh; othermilestonesbytes/accessonly. Datasetposition+1labelscheckedallpositions; native32-positionfullmodel/head equivalence inherited from qualified parent extraction, not rerun here. Newzero-branch/frozenprobe checks are separate.

All20functional,20spectral,8targetbranchescompleted. FourH10080GB,2CPUthreads/worker,actualquota88CPU;GPUallocatedmax{peakGPU:.3f}GiB,mainworkerRSSmax{peakCPU:.3f}GiB,executiondiskabout{disk:.2f}GiBagainst32GiB/GPUand64GiBdisklimits. PreciseaggregateRSSpeakwasnotsampled; retainperprocessrecords/4workerconcurrencyratherthaninventit. Pipeline615.9secondsplusfirstfailedengineering32.1seconds; these are processwalltimes, not purekerneltime/financialcost. No new GPUor trainingafterthisround.

## 7. Provenance and evidence ownership

Executionroot `{R}` owns code, full raw JSONL/TensorBoard/checkpoints/caches and response matrices. This project holds curated plots/tables and [payload manifest](curated_evidence_manifest.json).24actualoutputassets/currentselectedaccess recorded in assets/normalized_route_learning.md; [IDs](evidence/output_asset_ids.json), [states](evidence/checkpoint_members.json), [source](evidence/source_manifest.json), [verification](evidence/final_verification.json), [frozen config](design_freeze.json). Code/source/currentnativecontext and parent identities are separate from scientific eligibility. Large payloads stay execution-side.

## 8. Interpretation and next decision

Retain: competition-scale calibration changes actual reception. Weaken: better reception is sufficient for useful learning; current expert adaptation offers safe assignment. Unknown: the relative roles of update scale, finite-data generalization, exposure and frequency organization. No from-scratch capacity/semantic common-unique/phiutilityclaim. Researcher judgment Unknown; noFocusclosure,commit,pushorfollow-onrun.

AIproposalonly: use an independent development set to predefine one shared smaller branchupdatescale, then recheckA/B/Confreshheldouttext to distinguish generalization/updatefailure from organizationdifferences. This is not authorized execution.
''')
print(E)
