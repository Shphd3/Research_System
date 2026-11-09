"""Integrate measured spectra with unchanged R04 cache analyses; preserve v1 snapshot/package."""
from pathlib import Path
import json,csv,shutil,hashlib,datetime
O=Path(__file__).resolve().parent;S=O.parent;R=S.parent;P=Path(json.loads((S/'config.json').read_text())['owner_root']);J=json.loads((O/'analysis/spectral_results.json').read_text());K=json.loads((S/'analysis/results.json').read_text());D=J['dictionaries']

def cohort_table():
    rows=['|字典／固定集合|数量|DCLM频率中位数|单位decoder落在前64方向的平均比例|匹配谱背景|','|---|---:|---:|---:|---|']
    for d in ['SAE','CC']:
        for g,lab in [('old_shared32','原共有'),('old_math16','原数学偏向'),('old_bio16','原生物偏向'),('expanded_math64','新数学方向'),('expanded_bio64','新生物方向'),('new_top16','新展示前16')]:
            a=K['dictionaries'][d]['groups'][g];b=D[d]['groups'][g];status='可比较' if b['matched_spectral_status'].startswith('DONE') else '匹配不足，NA';rows.append(f'|{d} {lab}|{a["n"]}|{100*a["DCLM_rate_quantiles"][2]:.4f}%|{100*b["unit_mean_band_projection"][0]:.2f}%|{status}|')
    return '\n'.join(rows)

summary_cn='''# R04补充完成：区分数学／生物的feature，在频率与共同谱中哪里？

**已完成两个真实hook的PCA、16段投影、原留出复现与可匹配的随机背景。** 本次新增120篇原文重放＋4次检查＝124/124次；两套字典全部重放激活与旧缓存完全一致。原R04的456次不改记，两阶段合计580次；没有模型/字典训练、聚类、干预、新任务/资源或TEST。

每套保留原共有32、偏向16＋16，另按发现集单坐标区分排序扩为数学方向64、生物方向64；主图固定前16。新名单不等于旧“激活率比至少2倍”定义直接扩容。新增读数均为对已讨论数据的探索性再分析。

文中AUROC表示：随机取一篇数学和一篇生物文档，用单个feature的含零平均贡献，按发现集固定方向排对的概率；相等给半分。0.5为机会水平，**它不是分类准确率**。

只有两条认识更新：

1. **领域区分跨越多个频率水平；共同成员也可通过使用次数和幅度提供区分。** 低频SAE f391（DCLM0.0488%）和原共有f16240（48.39%）的原留出排序概率分别0.863和0.850。f16240在全部40篇文档都有活动，数学／生物命中比例72.44%／33.00%，按文档平均的激活时贡献11.89／6.62，含零平均9.58／2.62。两个差别同时存在，但各自对原组合分类成绩贡献多少仍未分离。[图1、图2](figures_cn.md)。
2. **这批展示方向相对匹配背景更偏向谱前部，但“在前部”本身不能判定领域区分。** 前64个主成分里，SAE／CC前16单位decoder平均投影51.21%／22.43%；匹配背景中位数40.11%／9.29%，中心95%范围32.71—46.25%／7.42—12.14%。原留出两域文档均值差的平方长度有96.45%／92.16%在这里，而真实总方差占比是69.39%／45.29%——三者是不同对象。反例：原共有SAE f29506的方向有96.75%在前部，但单坐标排序概率仅0.498；CC f11710只将10.56%方向放在前部，排序概率却0.995。[图3](figures_cn.md#图3共同谱中的位置)。

因此，本轮看到的是领域标签下的使用与几何关系。词面、来源和体裁仍可解释部分区分；谱段不是语义等级，decoder位置不是功能重要性。图1的SAE f11604区间跨机会水平、扩大集合f5662方向反转，都保留。旧高频共有等部分整组没有足够匹配背景，相关比较为NA，未放宽条件。

**AI建议唯一下一步：** 固定现有名单和方向，在来源与术语受到控制的独立数学／生物文本上验证这些使用差别，先排除文本来源解释；不再自动扩大名单或加入干预。

[三图逐轴读法](figures_cn.md) · [真实算例与反例](examples_cn.md) · [全名单、统计与边界](detailed_cn.md) · [追加前向授权与精确设置](real_spectrum_A01/protocol_amendment_cn.md)。原缓存阶段缺项卡和v1包保留为历史状态，当前谱已补齐。
'''
summary_en='''# R04 completed supplement: domain-discriminating features in frequency and common spectra

Both native true-hook PCAs, complete16-band projections, reused-holdout checks and estimable matched spectral comparisons are complete. The authorized amendment used120same-document forwards+4checks=124/124; all native latent replays exactly match original R04. Original456forwards remain unchanged, cumulative580for these two stages. No LM/dictionary training, clustering, interventions, new task/resource or TEST.

Retain original shared32/math16/bio16; expand discovery-only directional ranking to64per domain per dictionary and freeze global top16. This differs from original rate-ratio>=2selection. All new analyses reuse previously discussed data and are exploratory. AUROC is the probability of correctly ordering a cross-domain document pair in discovery-fixed direction, with half credit for ties; it is not classification accuracy.

Two recognition updates:
1. Discriminating members span frequencies; shared members can carry usage differences. SAE f391(.0488%DCLM)and original-shared f16240(48.39%)have heldout AUROC.8625/.8500. The latter appears in all40documents, with math/bio hit fractions72.44%/33.00%, active-document conditional contribution11.89/6.62 and zero-inclusive mean9.58/2.62. Their separate contribution to original combined classifier performance remains unmeasured.
2. Displayed directions are enriched in the first64PCs versus matched backgrounds, but spectral position alone does not establish discrimination. Top16 mean unit-direction head projections are51.21%SAE/22.43%CC versus matched medians40.11%/9.29%(central95%32.71-46.25%/7.42-12.14%). Reused-holdout domain mean-difference squared length is96.45%/92.16%in those directions while real variance is69.39%/45.29%. These objects differ. Counterexample shared SAE f29506 has96.75%head direction but AUROC.4975; CC f11710 has10.56%head direction yet AUROC.995.

Lexical/source/genre alternatives remain; no causal/function/semantic-level claim. Inadequate matching groups stayNA, including original high-frequency shared cohorts. One next suggestion, not run: independent source/terminology-controlled domain validation with frozen candidates/directions. v1missing-data report/package are historical, not current measurement status.
'''

oldfig=(S/'figures_cn.md').read_text();keep=oldfig.split('## 图3：')[0]
fig3='''## 图3：共同谱中的位置

![真实共同谱](figures/figure3_true_common_spectrum.png)

研究问题：这些区分坐标的decoder方向落在共同表征的哪些变化方向？与真实方差、两域均值差和匹配feature背景相比如何？

**读图顺序。** 左列是SAE的block27 MLP输入空间，右列是CC的block27 residual-post空间，各自独立拟合；两边PC编号不对应。所有横轴都是16个主成分排名区间：第1段PC1—64，最后一段PC961—1024，每段64个方向，既不是频率分桶，也不是模型层号。蓝/灰/紫线分别为发现/开发/原留出，后两者只投影冻结基。

1. 第一行纵轴：真实表征的方差比例（百分比、对数轴）。SAE发现/原留出前64为72.74%/69.39%；CC53.07%/45.29%。前部形状大体保留，尾部在开发/留出相对升高，不能称完整谱逐值复现。
2. 第二行纵轴：数学减生物的文档平均表征差向量，在每段的平方长度占比（百分比、对数轴）。原留出前64为96.45%/92.16%；其方向与发现均值差的cosine约0.879/0.880。这只是两域平均中心差，不是全部可分类信息。
3. 中间热图：一行一个原先固定的前16feature；颜色是单位原空间decoder在该段的平方投影百分比，每行完整1024基合计100%。原空间向量先还原训练尺度，再单位化；没有截断后重新归一化。固定顺序沿用图1，不聚类。深色表示方向的更多平方长度落在这里，不能读成更重要。
4. 最下行：紫线是前16个单位方向的平均投影；灰虚线/灰带是1000组同数量、DCLM频率和文档支持分箱匹配背景的中位数/中心95%。星号表示两字典×16段共32项的探索性背景比较BH q<.05；这不控制发现选优或旧留出再用偏差。

**直接观察。** 两套前16的前64投影51.21%/22.43%，都高于匹配背景的32.71—46.25%/7.42—12.14%中心范围；对应探索性q约0.00376。两套的其余方向仍分布在后续谱段，尤其CC并非全部落在前64。

**真实例子与反例。** SAE f11667有81.95%方向在前64，单坐标文档排序概率0.9725；但f29506有96.75%方向在前64，排序概率只有0.4975。另一边CC f11710排序概率0.995，前64仅10.56%，最大单段是PC129—192。不能只看谱前部，就判断哪个feature有领域区分；也不能把同一64维段内的两个方向视为彼此对齐。

**不确定性怎么读。** 上两行阴影是按文档重采样、冻结基不变的2.5—97.5百分位范围。均值差平方比例是高维非线性量，重采样会加入估计噪声，其范围可偏离原点估计；这里只作为抽样敏感性描述，不当成保证总体覆盖率的置信区间，不据其作显著性宣称。原数值和抽样权重均保留，没有改方法来让范围包含点。

**允许解释：** 固定坐标存在相对于频率/支持匹配背景的谱几何偏置；真实方差、域均值差和feature方向有不同分布。**不能推出：** 前部就是高级语义或全部领域信息，激活频率等于特征值大小，或证明模型实际利用、长程机制、专家分工、簇形成原因。

原未测说明卡保留在`figure3_spectrum_NOT_MEASURED.png`，只记录补取之前的状态，不能与本图混作两次独立实验。
'''

detail_append=f'''

# A01追加：真实h和共同谱已完成

本节覆盖前文缓存阶段的“BLOCKED”状态；前文保留当时真实缺项记录，不改原R04结论。追加授权来自用户明确要求执行前向补足PCA缺失读数。精确设置/时间/预算见`real_spectrum_A01/amendment.json`及protocol_amendment_cn。新增124/124，原456不改记，合计580；新资源/任务、训练、聚类、干预、TEST均0。

## 实际前向与对象一致性

原Runner源文件SHA固定，只将输出/预算台账地址重定向到新目录；模型、E16、A22、hook、归一化、门控与encoder batch不变。Base BF16固定1×256padding，每篇192可见token；同时保存SAE_h与CC_h两个真实向量（各192×1024 FP32副本），分析仍取32:192。120篇两字典的全token z相对误差0、支持Jaccard1；4次重复/128可见前缀检查也为0误差。运行torch2.5.1+cu121/transformers5.6.0.dev0，虽与历史R04版本不同，但逐token激活与所有重复/因果前缀检查一致；没有放宽门槛。模型/字典参数无更新、CCbuffers不变。

## 共同基与完整投影

每hook用60发现文档×160token=9600×1024矩阵，数学/生物各30篇、每文档等权。合并一个发现均值，不按域分别居中、不额外逐维标准化；SAE保留模型原生post-attention RMSNorm，CC保留真实residual-post单位、未施加final norm。FP64协方差/(N−1)，对称eigh，特征值降序、各列最大绝对载荷符号固定为正。两个数值秩均1024，阈值lambda_max×max(N,D)×eps；完整PC列基各1024×1024。

开发20篇/3200位置、原留出40篇/6400位置只投影到冻结基。每split实际方差在投影坐标内按pooled split方差计算，另存围绕发现均值的二阶矩，不混为一物；没有按领域另拟合均值或PCA。文档均值差始终M−B，再投影、逐64方向平方加总，原量与除以差向量平方范数的比例均存。单位decoder先还原原hook尺度再单位化，逐PC平方投影、累计投影和16段全部保存。完整投影和最大误差SAE4.67e−15、CC1.12e−15，没有未覆盖谱段或截断归一化。

## 各固定集合频率与谱位置

{cohort_table()}

“前64比例”是组内单位decoder方向投影的平均，不是实际激活贡献，更不是该组解释了多少总表征方差。原共有与新方向候选可以重叠；新排名没有重写旧角色。完整全部16段及每坐标各PC/累计投影见执行侧`real_spectrum_A01/analysis`。

## 抽样范围、匹配与辅助平方贡献

每split分域按文档重采样2000次，seed2026102806，两个hook共用对应抽样权重。基与发现均值在重采样时不再拟合；这些范围条件于已拟合共同基，不含基估计不确定性。真实方差范围是常规条件重采样，**高维域均值差平方比例的percentile范围可能偏离原点估计**：例如SAE原留出前64点96.45%，重采样范围92.22—95.95%；CC92.16%，范围84.51—90.99%。向差向量加入抽样噪声会改变归一化平方比值，这里不冒充保证总体覆盖的置信区间；无事后修正让区间变好看。前文单featureAUROC点态区间与此不同。

频率/支持匹配沿用原固定1000组ID，不重抽、不放宽。两套新前16、CC数学64、CC旧数学16完成谱匹配，其他组因原先有限池不足仍NA。主比较是两套新前16×16段共32项，两侧尾计数+1修正/1001并BH32；其余组仅描述，不把匹配不足当没有差异。原共有头部比例较大，但其极高频高支持组缺乏足够可替代坐标，不能据此声称超出匹配背景。

实际使用辅助量按每文档E[z_i²]×原空间decoder范数²×单位方向各段投影，对组内feature分别平方后相加；两域/文档等权，再给文档抽样范围。它遗漏不同feature间交叉项，不叫总解释方差，不归一化到100%。文件`activation_weighted_auxiliary.csv`保留原空间平方单位与三个显式false标记，主图仍只用单位方向几何。

## 新实测证据与反例

原留出真实方差的前64占比SAE69.39%/CC45.29%，域均值差平方比例96.45%/92.16%，两者不等同。均值差与发现方向对齐cosine0.8785/0.8802。发现/开发/原留出的前64真实方差分别SAE72.74/68.97/69.39%、CC53.07/45.20/45.29%，尾部有分布移动，未称完整谱逐值复现。固定前16单位方向前64为51.21/22.43%，匹配背景中位40.11/9.29%。不能把上述四种量相互替代。

SAE原共有f29506方向96.75%在前64，单坐标排序概率0.4975；CC f11710前64只有10.56%、最大段PC129—192，但排序概率0.995。这些反例限制了“落在头部就区分领域”的解释。域均值差只是一阶量，可分类信息还可表现为分布、方差或组合，不由此宣称已定位全部语义信息。

## 完整性与审计

追加34项独立检查通过：124次预记账、240次原激活完全一致、8项h/z重复前缀对照、输入/名单哈希、真实h直接协方差与投影方差一致、原空间文档均值差独立投影、保存decoder直接投影、完整基/累计和、分域抽样人数、辅助平方标记、BH32独立定义等。原缓存阶段106项仍保留；原R04清单563文件及原zip未改。新PCA统计拟合2次，模型/字典/分类器训练0。完整检查源和结果在`real_spectrum_A01/audit_spectrum.py`、`audit.json`，协议与三类审计分别记录对象识别、数据统计、数值实现。

|请求项|当前状态|证据／边界|
|---|---|---|
|全坐标排序、扩大64、固定16、使用量、AUROC、DCLM|DONE_EXPLORATORY|原缓存阶段保留，未重选|
|两hook真实表征补取|DONE_VALID_MEASUREMENT|120文档＋4检查，124/124|
|共同PCA、16段完整decoder投影、真实方差|DONE_EXPLORATORY|两个1024维基、完整和约1|
|开发/原留出冻结坐标投影、域均值差|DONE_EXPLORATORY|原留出再用；bootstrap范围局限已标|
|主前16匹配谱参照|DONE_EXPLORATORY|各1000组，BH32条件背景比较|
|其余整组匹配|DONE_EXPLORATORY / NOT_ESTIMABLE|原分箱可用池不足的组仍NA，未放宽|
|激活加权辅助平方贡献|DONE_EXPLORATORY|不含交叉项、不归一化、不叫总方差|
|三张主图、真实例与反例|DONE_EXPLORATORY|图1/2原样、图3实测替代当前缺项状态|
|模型/字典训练、聚类、干预、物理域、R05重做|NOT_RUN_BY_SCOPE|全部0|

只有一个AI建议见当前Summary；科学接受与问题关闭仍由研究者决定。
'''

examples_append='''

# A01：上述真实feature在共同谱中的读数

数学文档算例SAE f11667的原空间单位decoder有81.95%平方长度落在PC1—64。该feature在原留出单坐标排序概率0.9725，说明这个例子同时有前部几何位置和可读使用差别；没有功能干预证据。

相反，原共有f29506前64有96.75%，却只有0.4975的单坐标排序概率：方向位于高方差子空间，本身不保证实际使用量携带稳定领域读数。CC f11710则只有10.56%方向在前64、最大段PC129—192，但单坐标概率0.995。两套编号不是同一个坐标，CC的z仍是14层共享读数。这说明不能直接用decoder谱位置替代激活使用模式。

本轮没有给任何谱段贴“高级/低级语义”标签；域均值差集中只说明两类文档中心差异的几何分布。
'''

for name,txt in [('summary_cn.md',summary_cn),('summary.md',summary_en),('figures_cn.md',keep+fig3),('detailed_cn.md',(O/'cache_only_before_amendment/detailed_cn.md').read_text()+detail_append),('examples_cn.md',(S/'examples_cn.md').read_text().split('# A01：')[0]+examples_append)]:
    (S/name).write_text(txt);(P/name).write_text(txt)
current=(S/'detailed_cn.md').read_text()
begin=current.index('## 共同谱资产审计与补取成本');end=current.index('## 数值与保存',begin);current=current[:begin]+current[end:]
begin=current.index('## 覆盖账本');end=current.index('# A01追加：真实h和共同谱已完成',begin);current=current[:begin]+current[end:]
current=current.replace('两域真实共同谱缺失，未拟合。','两域真实共同谱已按A01补取并拟合，见后文实测章节。').replace('没有真实h，所有谱随机对照都NOT RUN，即使频率匹配ID已取得。','匹配ID先在缓存阶段固定；A01用同一批ID完成可估计的谱随机对照，原匹配不足组仍NA。').replace('本节覆盖前文缓存阶段的“BLOCKED”状态；前文保留当时真实缺项记录，不改原R04结论。','本节记录用户追加授权后完成的真实谱。补取前的缺项报告保存在快照和v1包；原R04结论不改。')
(S/'detailed_cn.md').write_text(current);(P/'detailed_cn.md').write_text(current)
engdetail=(O/'cache_only_before_amendment/detailed.md').read_text()+'''

# A01 actual completion supersedes the historical missing-h state

User explicitly authorized forward acquisition.120same documents+4checks=124/124new calls, all native latents exactly original; causal-prefix/replay true-h checks exact. Original456count is preserved, total580for these two stages. No training/task/resource/clustering/intervention/TEST. Two statistical PCA fits only.

Each hook independently uses9600discovery rows x1024dimensions, one pooled mean, equal domains/documents, no extra standardization; FP64covariance eigh yields full1024-rank bases. Dev/holdout only project. Complete decoder squared/cumulative projections sum1within5e-15. Reused-holdout head64 real variance69.39%SAE/45.29%CC; domain-mean-difference squared fraction96.45%/92.16%; top16unit direction mean51.21%/22.43% versus1000matched medians40.11%/9.29%. Primary background testsBH32 are exploratory/conditional, not selection-corrected mechanism tests. Inadequate original matching groups remainNA.

Mean-difference squared-fraction bootstrap percentile ranges are conditional resampling dispersion and can exclude the plug-in point due high-dimensional nonlinear bias; no population coverage or significance claim. Coefficient bases stay fixed during document resampling. Auxiliary activation-weighted individual squared sums omit cross terms and are not total variance or normalized percentages. True variance/domain means/direction geometry/usage are distinct.

34independent true-h/numerical/lineage checks pass in addition to prior106cache checks. Actual raw/basis/projected moments, candidate/random IDs, native-unit geometry, CSVs, scripts/hashes and receipts are execution-side. Chinese Detailed contains all12cohort rows and requested coverage statuses. Original563R04files and v1reading package remain unchanged. Scientific acceptance/closureUnknown.
'''
(S/'detailed.md').write_text(engdetail);(P/'detailed.md').write_text(engdetail)
amend_en='''# A01 authorization and frozen spectral implementation

Current user explicitly approved acquiring missing real hook vectors and completing PCA statistics. Cap124newforwards=120sameR04documents+4replay/prefix checks. Keep original456ledger unchanged; total580for these stages. Reuse existing resource/native Runner, fixed Base/E16/A22, hooks/gates/precision/batches and original candidate/scale/frequency/random IDs. No task/resource/training/clustering/intervention/TEST. Save raw true-h; never reconstruct a PCA surrogate.

Separate60-document/9600-position pooled-centered FP64PCA bases, no extra standardization, full1024directions split16x64ranks. Dev/holdout projection only. Native unit-decoder full squared/cumulative projections, true variance, document mean difference and2000stratified-document bootstrap(seed2026102806). Existing1000matched IDs unchanged; insufficient matching staysNA. Primary top16x2x16=32background comparisons useBH32, exploratory only. Auxiliary individual squared activation contributions omit cross terms, are not total variance and not normalizedto100%. See amendment.json for exact frozen before-acquisition choices and hashes.
'''
(O/'protocol_amendment.md').write_text(amend_en);(P/'real_spectrum_A01/protocol_amendment.md').write_text(amend_en)
shutil.copy2(O/'protocol_amendment_cn.md',P/'real_spectrum_A01/protocol_amendment_cn.md')
for p in (O/'figures').glob('*.png'):shutil.copy2(p,S/'figures'/p.name);shutil.copy2(p,P/'figures'/p.name)
for f in ['amendment.json','completed.json','audit.json','raw_representation_manifest.json']:
    shutil.copy2(O/f,P/'real_spectrum_A01'/f)
for f in ['spectral_results.json','real_variance_and_domain_mean_difference.csv','cohort_matched_background.csv','primary_matched_background_tests.csv']:
    shutil.copy2(O/'analysis'/f,P/'real_spectrum_A01'/f)
(P/'code/real_spectrum_A01').mkdir(exist_ok=True)
for p in O.glob('*.py'):shutil.copy2(p,P/'code/real_spectrum_A01'/p.name)
combined={'current_status':'COMPLETE_ALL_ESTIMABLE_STATISTICS','cache_only_phase':{'results':str(S/'analysis/results.json'),'candidate_freeze_sha256':hashlib.sha256((S/'analysis/candidate_freeze.json').read_bytes()).hexdigest(),'new_forwards':0},'A01_true_h_and_spectrum':{'raw_manifest':str(O/'raw_representation_manifest.json'),'results':str(O/'analysis/spectral_results.json'),'new_forwards':124,'PCA_fits':2,'checks':34},'original_R04_forwards':456,'R04_plus_supplement_forwards':580,'remaining_matching_gaps':'originalwholecohortbinpoolinsufficiency,notmissingrawh','main_figures':['figure1_domain_usage_and_discrimination.png','figure2_discrimination_vs_DCLM_frequency.png','figure3_true_common_spectrum.png'],'historical_gap_card':'figure3_spectrum_NOT_MEASURED.png','old_results_unchanged':True,'scientific_acceptance':'Unknown'}
(S/'combined_results.json').write_text(json.dumps(combined,ensure_ascii=False,indent=2)+'\n');(P/'combined_results.json').write_text(json.dumps(combined,ensure_ascii=False,indent=2)+'\n')
readme='''# R04 completed domain-discriminability supplement\n\nRead [一页中文结论](summary_cn.md), [三图逐轴说明](figures_cn.md), [真实算例与反例](examples_cn.md), and [完整数据与A01追加结果](detailed_cn.md). [English](summary.md).\n\nCurrent three figures include the measured true-hook spectrum. Historical NOT_MEASURED card/v1package are preserved, not current status. Authorized newforward124/124; no training, clustering or interventions. All new reused-holdout statistics are exploratory.\n'''
(S/'README.md').write_text(readme);(P/'README.md').write_text(readme)
audits={'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'recording_phase':'post-completion audit against before-acquisition frozen amendment, not a retrospective preregistration','scientific_identification':{'question':'frequency,usageandcommon-spacepositionofR04domain-readablecoordinates','rival':'terminology/source/genre;nativejointznotlastlayerindependent','scope':'geometryandreadability,notfunctionalorfrequencycausality'},'data_statistics':{'fit':'60originaldiscoverydocsbalanced30/30,160tokens/doc','heldout':'previouslyexamined,reuseexploratory','fixed_direction_candidates':True,'PCA_domains_not_separately_centered':True,'bootstrap':'stratifieddocuments,frozenbasis;nonlinearmean-difference-ratiointervalbiasreported','matching':'reusefrozenIDs;insufficientgroupsNA'},'implementation_numerics':{'LM_SAE_CC_parameters_updated':0,'statistical_PCA_fits':2,'forward_count':124,'all_original_latents_exact':True,'full_basis':1024,'numerical_checks':34,'dtype':'nativeBF16Basetrueh->FP32save->FP64PCA','optimizer':'N/Aclosedformcovarianceeigh'},'human_scientific_acceptance':'Unknown'}
(O/'three_audits.json').write_text(json.dumps(audits,ensure_ascii=False,indent=2)+'\n');shutil.copy2(O/'three_audits.json',P/'real_spectrum_A01/three_audits.json')
print('COMPLETE_RECORDS_WRITTEN',P)
