"""Write bounded English/Chinese result records; never change original R04 owners."""
from pathlib import Path
import json,csv,shutil
O=Path(__file__).resolve().parent;A=O/'analysis';C=json.loads((O/'config.json').read_text());P=Path(C['owner_root']);J=json.loads((A/'results.json').read_text());D=J['dictionaries']

def get(d,f):
    return next(x for x in csv.DictReader((A/f'{d}_selected_feature_metrics.csv').open(encoding='utf-8-sig')) if int(x['feature'])==f)

def table():
    rows=['|字典与新方向集合|数量|DCLM频率最低—最高|DCLM中位数|原留出排序概率中位数|','|---|---:|---:|---:|---:|']
    for d in ['SAE','CC']:
        for g,lab in [('expanded_math64','数学'),('expanded_bio64','生物')]:
            q=D[d]['groups'][g];f=q['DCLM_rate_quantiles'];rows.append(f'|{d} {lab}|{q["n"]}|{100*f[0]:.4f}%—{100*f[-1]:.4f}%|{100*f[2]:.4f}%|{q["heldout_auc_quantiles"][2]:.3f}|')
    return '\n'.join(rows)

summary_cn=f'''# R04补充：哪些坐标区分数学／生物，它们在哪里？

**本次能回答频率与使用方式；共同谱位置未测。** 原R04同一套模型、文本、分割与原生字典不变。本轮只读取缓存，新增前向、分类器拟合、训练、聚类和干预均为0。旧留出已被多轮讨论，以下全部是探索性再分析。

本次的区分读数叫AUROC：随机抽一篇数学和一篇生物文档，单个feature的平均贡献能按发现集预定的领域方向把两篇排对的概率；相同给半分。0.5是机会水平，1表示本批所有跨域配对都排对，**不是分类准确率**。

新排序要求两域各至少5篇发现文档激活，SAE有1,082、CrossCoder有8,113个合格坐标；各扩为数学方向64、生物方向64。主图每字典固定发现排序前16，不按留出替换。**新集合按平均贡献的区分性排序，不是把旧“激活率比至少2倍”的定义直接扩到64**；原共有32和偏向16+16全部保留。

{table()}

表中最后一列是成员各自读数的中位数；本轮没有重新训练64维组合分类器。

只保留两条认识更新：

1. **领域区分不能只用一个频率区间概括。** SAE f391的DCLM频率仅0.0488%，原留出排序概率0.863；原共有成员f16240的频率48.39%，仍有0.850（文档区间0.720—0.960）。CrossCoder也同时有低频f9491（0.0595%，0.846）和高频f12266（42.99%，0.950）。但并非扩入的都可靠：SAE f5662从发现时的生物方向变为留出0.368（0.202—0.545），仍留在图和表里。[图2与全背景](figures_cn.md#图2区分力与独立频率)。这是有限文本的统计联系，不是频率导致区分。
2. **共同成员可以靠“用得更勤”和“用时更强”同时提供领域读数；两者不必总同向。** 原共有SAE f16240在全部40篇留出文档都有活动：数学／生物命中比例72.44%／33.00%，按文档平均的非零贡献11.89／6.62，含零平均9.58／2.62。主图16个里SAE14个两项同向、2个只有次数优势；CrossCoder16个两项同向。这些是可分开观察的使用差异，**尚未量化各自对原组合分类成绩贡献多少**。反例f29506虽有幅度差，单坐标排序概率仅0.498（0.312—0.685）；组合可读不要求每个成员单独强。[图1](figures_cn.md#图1领域使用与区分)与[真实算例](examples_cn.md)。

共同谱还不知道：R04的455个npz没有保存这批文档的两个真实hook表征；decoder已读取、哈希和尺度已核对，但不能从decoder或稀疏z反推所需真实PCA。旧R03参考谱不是两域共同谱，未混用。[图3是缺项说明卡，不是谱结果](figures_cn.md#图3共同谱未测)。

**AI建议唯一下一步：** 若要补齐导师的谱问题，批准同120篇文档的原配置重放，一次同时保存两个真实hook；120次前向，另可预留4次数值检查，总上限124。FP32只存测量窗口两hook约150MiB。本轮没有执行，也没有把旧剩余预算自动转来。

[三图逐轴解释](figures_cn.md) · [数据、公式、匹配缺项与边界](detailed_cn.md) · [精确冻结协议](protocol_cn.md)。机制接受与问题关闭由研究者判断，本记录不改变其状态。
'''
summary_en='''# R04 supplement: domain discrimination, reference frequency and missing common spectra

This cache-only exploratory reanalysis completes domain-use and frequency measurements. Common-spectrum measurements are NOT RUN because real R04 hook representations were not saved. No model forward, classifier fit, training, clustering, intervention, new task/resource or sealed TEST occurred. Original R04 files and cohorts remain unchanged; previously examined holdout documents are not new unbiased confirmation.

Eligibility requires active support in at least five discovery documents in EACH domain:1,082SAE and8,113CrossCoder coordinates. Rank individual document mean native contribution by absolute discovery AUROC minus.5, tie by ascending coordinate ID; freeze direction. Expand each dictionary to64math-direction and64biology-direction candidates, display global top16. This differs explicitly from original R04 rate-ratio>=2 selection; retain original shared32/math16/bio16 cohorts.

AUROC is the probability that a randomly drawn cross-domain document pair is ordered in the discovery-fixed direction, with half credit for ties; it is not classification accuracy.

Two bounded recognition updates:

1. Discriminating members span reference frequencies. SAE f391 has DCLM frequency.0488% and holdout AUROC.8625; original-shared f16240 has48.39% and.8500(CI.720-.960). CC f9491 has.0595%/.84625 while f12266 has42.99%/.9500. Counterexample SAE f5662 reverses to.3675(CI.202-.545); no holdout reselection. This does not establish frequency causality or pure domain concepts.
2. Shared membership permits discriminatory usage differences. SAE f16240 is present in all40holdout documents; math/bio mean hit fraction72.44%/33.00%, mean active-document conditional contribution11.89/6.62 and zero-inclusive mean9.58/2.62. Both usage differences align in14/16displayedSAE and16/16CC; twoSAE only have a hit-rate advantage. Their separate causal or classifier-performance shares were not measured. Original-shared f29506 has AUROC.4975(CI.312-.685), illustrating that combined readability does not require every member to separate alone.

Real-h audit covers all455R04npz schemas. Native decoders were freshly read/hash-verified; no reconstructed h or old-corpus PCA was substituted. Figure3 is explicitly a missing-data card, not spectral evidence. One next proposal, NOT RUN: replay the same120documents, optionally4checks, saving both true hooks(~150MiBFP32 at160positions). Scientific acceptance and closure remain researcher-owned/Unknown.
'''

fig_cn='''# 三图逐轴解释

## 图1：领域使用与区分

![领域使用与区分](figures/figure1_domain_usage_and_discrimination.png)

- 问题：同一个坐标的领域差别表现为出现次数、激活时幅度，还是两者都有？
- 一个点／行：每行一个发现集固定feature；小点是一篇留出文档，大点是域内文档均值，横线是分域按文档重采样的95%点态区间。橙色数学，青色生物；ID后M/B为发现固定方向。上排SAE，下排CrossCoder；每排16行，不聚类、不按留出重排。
- 从左到右横轴：①每文档160位置里激活的百分比；②只在激活位置算平均贡献，零命中文档NA；③含零平均贡献；④按发现方向把一数学/一生物文档排对的概率。第②③列为便于逐行比较，除以该feature发现token贡献RMS；0—1线性、1以上对数，原空间值全部在CSV。第四列0.5虚线为机会水平。
- 直接看哪里：SAE f11667的橙色在次数、强度、含零贡献三列都更靠右，排序概率0.9725；SAE f693则次数更高、激活时平均强度并没有更高，不能统一说“数学feature总是用时更强”。后者生物条件强度仅1篇非零文档，支持量写在表中。固定前16的f11604区间跨0.5，是未被删掉的不充分例子。
- 能得出：这批文档的坐标使用差异与领域区分相伴；可以观察次数与强度的方向。
- 不能得出：模型必须依赖它、分类能力由某一项独立造成、排除了词面来源或它是抽象概念。条件均值只在有活动的文档内计算，两个域有效文档不一定相同。

## 图2：区分力与独立频率

![区分力与DCLM频率](figures/figure2_discrimination_vs_DCLM_frequency.png)

- 问题：有区分读数的成员在DCLM频率分布哪里？
- 一个点：一个同字典feature；横轴独立65,536位置DCLM激活率（百分比，对数），纵轴同图1的方向固定文档排序概率。左图SAE，右图CC，不能跨图对齐编号或把两种hook当同一空间。
- 背景：全部合格且发现方向非零的坐标。SAE2个、CC17个发现排序恰为0.5，方向NA，数量在图中注明而非伪造纵轴值。竖虚点线是该字典全坐标DCLM频率中位数。
- 符号：灰点全背景；橙/青空圈分别新64数学/生物方向；紫方块原共有32；上下三角原数学/生物16；黑星固定新前16。原名单即使不满足新双域支持门槛仍保留。部分名单相互重叠，不是互斥簇。
- 直接观察与真实例子：低频SAE f391（0.0488%，0.8625）和高频原共有f16240（48.39%，0.8500）都能提供单坐标区分。反例是仍保留的SAE f5662（7.43%，0.3675），其方向在留出反转；不是所有发现排序好的都复现。
- 匹配背景：固定前16平均排序概率SAE0.8516、CC0.9691；1000个同数量频率/文档支持分箱匹配随机集合的均值中位数0.6228/0.6185，中心95%为[0.5653,0.6803]/[0.5529,0.6855]。这不是随机化p值，不消除发现选优与旧留出再用偏差。其他组匹配不足的完整清单在Detailed，未强制保留候选。
- 能得出：成员分布跨多个频率水平；频率不是领域区分的唯一概括。
- 不能得出：频率造成区分、找到了全字典最重要坐标，或灰点下方的单坐标在组合中无用。图中没有新训练分类器。

## 图3：共同谱——未测

![共同谱缺项说明](figures/figure3_spectrum_NOT_MEASURED.png)

这是一张**缺项说明卡，没有数据横纵轴，不是第三张谱证据图**。原计划的横轴是16个各64主成分方向的排名区间，纵轴是固定feature；因为本批真实h未保存，PCA、投影占比、真实方差、领域均值差、开发/留出复现、匹配随机谱对照全部未测，不能填写颜色。

decoder可核查并不等于谱位置可核查：例如SAE f11667的原空间decoder范数可核对为约1，却没有本批真实h决定的PC方向；不能据此判断它落在谱头或谱尾。旧R03谱来自另一参考面板，是不能替代的反例。若只画一张看似合理的热图，会把未取得的表征信息当成结果，本轮未这样做。

最小补取成本：仅发现拟合60次，但为完成开发/留出冻结坐标复现须重放全部120篇，另建议最多4次数值检查；两个hook同一次Base前向保存。只存160测量位置、两个1024维FP32hook，150MiB；若存全文192位置，180MiB。没有运行时间的实测估计，也未启动这些前向。
'''

examples=json.loads((A/'arithmetic_examples.json').read_text())
ex=next(x for x in examples if x['dictionary']=='SAE' and x['feature']==11667 and x['domain']=='math')
bio=next(x for x in examples if x['dictionary']=='SAE' and x['feature']==11667 and x['domain']=='biology')
examples_cn=f'''# 一个真实算例与反例

以下是缓存内事后解释例子，不参与候选筛选或新确认。只有当前token及可见前缀用于说明。

## 单feature如何由token变成文档读数

SAE f11667来自新固定前16。真实数学文档`{ex['seq_id']}`中，窗口内154/160个位置有激活。到token **`{ex['token']}`** 时的可见文本片段为：

> {ex['visible_prefix_excerpt'].strip()}

该token的原空间贡献为{ex['native_contribution']:.5f}；**这不是整篇平均**。整篇激活时平均贡献为{ex['active_mean_native']:.5f}，故含零平均=(154/160)×{ex['active_mean_native']:.5f}={ex['zero_inclusive_mean_native']:.5f}。分类与本轮单feature排序用的是最后一个量。

跨20篇数学／20篇生物留出文档：命中比例73.8438%／4.6250%，有活动文档内的条件贡献平均13.9312／4.6291，含零平均10.9976／0.5624。按发现数学方向抽一篇数学与一篇生物，平均贡献排对概率0.9725，文档bootstrap区间[0.9025,1.0000]。这不是该token含数学概念的概率，也不是分类准确率。

注意：域内先按文档等权求平均后，域均值的“命中比例×条件强度”一般不等于域内含零均值。恒等式只在单文档成立；相关性与零命中文档会改变域内加权。原先按所有活跃token汇总的条件均值与现在文档等权数值不同，CSV同时给出position_weighted_conditional以免混用。

## 反例一：生物文本也可强烈激活该数学方向候选

真实生物文档`{bio['seq_id']}`讲突触电位、电缆理论与神经元建模；f11667在其中133/160位置激活，含零平均{bio['zero_inclusive_mean_native']:.5f}，并非只在数学文本出现。到token`{bio['token']}`的贡献为{bio['native_contribution']:.5f}，可见片段：

> {bio['visible_prefix_excerpt'].strip()}

这说明数学／生物是人工文档标签，生物文档可包含数学建模内容。可区分不等于领域专属；这种边界例必须保留，不能因其影响解释而删去。

## 反例二：发现方向在原留出反转

新扩展SAE f5662按发现集固定为生物方向，留出排序概率0.3675，区间[0.2025,0.5451]；含零数学/生物平均0.2027/0.0958，不能说已确认生物偏向。它仍在扩展名单与图2中，没有换人。

原共有f29506也是“局部强弱差≠稳定单坐标区分”的例子：原F11相同difference上数学/生物15.19/6.05，第二措辞7.71/7.95反转；文档排序概率0.4975，区间[0.3125,0.6850]。原共有32组合能分类，不要求每个成员单独成功。

全体固定候选的token例子和各token命中次数分别保存在`analysis/selected_token_examples.csv`与`selected_token_hit_summary.csv`。每域最高3个不同文档的例子是高响应展示，不是无偏代表；token命中次数未除以token出现机会，不叫词选择性。原文档URL、序列ID和零起算位置都在表中。
'''

detail_cn=f'''# 数据、指标与缺项

## 三条分析路径与范围

1. 行为与因素控制：本轮不新增模型输出或词袋拟合；复用R04数学/生物标签、来源/体裁限制与原组合分类，不能排除词面。原组合分类结果不被单feature排序改写。
2. 表征与组织：原生坐标的使用率、条件贡献、含零平均贡献，以及DCLM频率与单坐标可读性是本轮实际测量；两域真实共同谱缺失，未拟合。
3. 功能干预与测量质量：干预0；缓存计数重放、单坐标排序独立实现、原输入一致性及原decoder哈希/尺度核查已执行。重构贡献不是功能重要性。

## 资产与数据

Base Qwen3-0.6B-Base保持冻结；同120篇R04真实DCLM网页摘录，发现60、开发20、原留出40，域内分别30/10/20。每篇实际输入192token，测量零起算[32,192)的160个位置。发现用于资格、方向、候选与RMS；开发与原留出只计算冻结读数。参考频率复用256×256=65,536位置，与实验文档去重；254canonical URL组，样本频率不代表所有语言。AI内容审读标签、站点/子体裁/术语差异保留。

E16为FP32 ReLU Top32，block27 MLP输入（原模型post-attention layernorm后），decoder列向量原空间范数约1。A22为BF16encoder GEMM、原TRAIN居中/RMS、14层联合共享z、保存阈值0.051281172782182693；block27 residual-post最后层贡献z×decoder27范数×TRAIN_RMS27(374.3495121024576)。A22不是最后层独立激活。两种hook不拼接、不对齐编号；没有临时单分支编码。

checkpoint原SHA与本次fresh SHA一致：SAE e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65；A22 09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628。Base历史R04 SHA cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba（本轮不加载/重哈希Base）。tokenizer fresh SHA c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539。完整路径见decoder_and_token_provenance与source_manifest。

## 指标与选择

每文档每feature：c_t=z_t×原hook decoder范数；hit=正激活数/160；conditional=贡献和/正激活数，无命中NA；mean=贡献和/160。单文档mean=hit×conditional；跨文档等权均值不满足简单乘积式，另存按活跃位置加权conditional。域均值差统一数学减生物，绝对量/差值与区间都保留，避免只看比例。

AUROC=(数学分数大于生物的文档对数+相等对数/2)/(nM×nB)。发现固定方向s=sign(AUC-.5)，生物方向用1-AUC。发现方向恰为0则新选择排除，方向固定的开发/留出量NA，但raw数值保留。每域至少5发现文档非零才进新排序；abs(AUC-.5)降序、ID升序打并列。每方向64、全局前16不保证8/8。旧名单全保留并标记是否满足新门槛。新集合数学与生物方向互斥，但与旧共有可重叠，因为定义不同。

文档bootstrap2000次，seed2026102804，域内分别有放回20篇；所有坐标复用同一抽样权重。单featureAUROC先形成20×20实际文档配对比较，再使用抽样文档权重计算，不把400对当400个独立文档。区间为2.5/97.5百分位、点态探索性区间，不是同时覆盖区间。未做显著性筛选或额外多重检验；无“区间不跨0.5即全字典确认”的表述。原留出已看过，发现筛选也会使读数乐观。

`*_all_feature_metrics.csv`包含所有坐标及资格、方向、发现/开发/留出排序概率、减0.5与留出减发现差值、区间、DCLM计数、两域三个使用量；AUROC区间覆盖全部合格及保留旧坐标，三使用量区间覆盖所有固定新旧集合。其余坐标不拿来挑新候选。每文档读数在`*_per_document_metrics.npz`，原全坐标计数/和来自R04forward汇总。原zero-support条件均值始终NA。

## 扩大后的结果，不把候选改名为自然簇

{table()}

SAE新增数学64中1个留出排序概率≤0.5，生物64中2个≤0.5；CC这两组为0/0。主图SAE最低是f11604=.6575但区间跨0.5。没有根据这些读数替换名单。SAE16展示含数学9、生物7；CC含数学9、生物7（均由发现排序自然得到，不强凑）。旧集合的原比率、组合分类、同目标确认保持原结论。

## 原可分类组合与本轮读数的对应

原R04固定32维组合的留出平衡准确率：SAE共有95%、偏向100%；CC共有92.5%、偏向97.5%。这些是历史固定logistic分类器成绩，不是本轮单坐标排序概率，也不拿两者相减算信息份额。本轮逐个保留这些组合的所有成员，另外扩展方向候选；原共有标签由发现筛选固定，留出率比变化不触发重命名。新64集合没有拟合组合分类器。

## 匹配参照实际完成与缺项

固定1000次、seed2026102805（CC加1），同字典合格背景，排除被比较集合全部成员；jointbin=floor(log2(DCLM_hits+.5))×floor(发现文档总支持/5)，每bin精确同数量、组内无放回，不强留候选、不放宽。

两套新前16均完成1000组。额外完成CC数学64及CC旧数学16的匹配。其余完整集合由于至少一个jointbin背景不足，标NA，不删除难匹配候选。SAE扩大数学缺1个bin（需1可0），扩大生物缺4个bin；旧共有存在极高频高支持bin稀缺。CC生物64缺3个bin，旧共有极高频高支持bin需18可1，旧生物极低支持bin需1可0。逐bin需求/可用数在`*_matched_random_summary.json`；完整匹配ID在npz。

随机组提供频率/支持匹配的描述性背景；不能替代“重复完整发现选优流程”的零假设，也不证明因果机制。没有真实h，所有谱随机对照都NOT RUN，即使频率匹配ID已取得。没有将不完整组局部成功写成整个组成功。

## 共同谱资产审计与补取成本

检查R04全部455个npz字段与该目录其他tensor扩展，逐token缓存只有token_ids、两字典CSR与NMSE，汇总只有counts/sum_z/sum_z2/norm/ID。原Runner把SAE_h、CC_h临时返回，但sparse_save没有保存。相关R05同文档缓存的范数字段/Attention并非真实每token向量或完整协方差；本轮没有分析或重做R05。旧R03真实h/PCA来自另一语料，不能作为本题发现集共同谱。审计边界仅这些明确资产，不声称全存储绝不存在任何副本。

真实h、合并均值、PC基、特征值、有效秩、16段实际投影、开发/留出谱复现、领域均值差都MISSING/NOT RUN；不能从重构h或单位decoder补造。单位decoder已按原空间还原并存档：SAE183个、CC192个不同新旧坐标；方向单位范数误差<4e-16，范数与R04贡献读数一致。这只是方向提取资格，不是谱测量。

需要每hook120×160×1024真实表征，发现9600行用于拟合；开发3200/留出6400行只投影。两域各30发现文档等权、每文档160位置等权；一个合并均值中心化，保留原layernorm，不逐维标准化，分hook1024维完整基。16段每段64方向；单位decoder完整平方投影应和为1，真实方差与文档域均值差另报告。以上是已冻结待资产算法，不是结果。

只有60发现前向可拟合，但要满足本次复现要求需120原配置文档重放，两个hook同一次Base调用保存，另最多4检查；申请上限124，不自动用旧剩余预算。FP32测量窗口两hook150MiB，全192token180MiB；时间未基准测试，不能给实测时长。此次前向0。

## 数值与保存

25项实现检查通过：常数/正序/逆序AUROC；NA与单文档恒等式；原probe输入一致；固定发现/留出文档CSR计数与sum复放；6个对象与sklearn单坐标排序实现交叉核对。额外独立审计见audit.json。bootstrap矩阵点积有浮点尾差时仅clip到数学界[0,1]，未改变方向或规则；第一次脚本语法修复和tokenizers环境选择在engineering_notes中保留。固定候选freeze原文件不被离线重放改写。

## 覆盖账本

|请求项|状态|证据／缺项|
|---|---|---|
|原文本、分割、原候选、全坐标频率|DONE_EXPLORATORY|source_manifest、R04源文件，全部保留|
|各方向扩为64、主图固定16|DONE_EXPLORATORY|candidate_freeze及两套完整CSV|
|三种文档使用量、差值、排序概率与区间|DONE_EXPLORATORY|all/selected/display指标表和文档npz|
|native decoder尺度、单位方向|DONE_EXPLORATORY|selected_native_decoder、fresh SHA/范数核对|
|真实两域共同h与PCA|BLOCKED|两hook真实h未保存|
|16谱段、真实方差、域均值差及复现|BLOCKED|依赖上项，禁止替代|
|频率/支持匹配随机组|DONE_EXPLORATORY / BLOCKED|两前16、CC数学64/旧数学16完成；其余bin不足NA|
|谱匹配随机对照|BLOCKED|无真实共同基|
|图1、图2|DONE_EXPLORATORY|可读证据图；已渲染检查|
|图3|BLOCKED|仅缺项说明卡，不冒充结果|
|真实算例、反例、数据与脚本|DONE_EXPLORATORY|examples_cn与完整token例子|
|训练、前向、聚类、功能干预|NOT_RUN_BY_SCOPE|全部0；未新增任务/资源或TEST|

唯一下一步及边界见Summary；研究者机制接受与问题关闭Unknown，不由当前记录改变。
'''

detail_en='''# Detailed evidence and limitations

The three paths are: behavior/factor controls (reuse R04 labels, original probes and lexical/source limits; no new predictions); representation organization (cache-derived coordinate usage, independent reference frequency, single-coordinate ordering; spectra missing); functional interventions/measurement quality (no interventions; numerical and provenance checks only).

Inputs are original120documents, discovery60/development20/previously examined holdout40, domain-balanced, fixed positions32:192. Native E16 MLP-input and joint A22 residual-post decoder contributions remain separate. Conditional mean is NA for a zero-hit document; group statistics average active documents, while a separate position-weighted conditional statistic preserves the earlier aggregation convention. The per-document identity mean=hit_fraction*conditional does not imply a product of group means.

All new ranking and directions use discovery. Require >=5active discovery docs EACH domain. Order by abs(single-feature discovery AUROC-.5), ID ascending. Keep64per direction/global top16; preserve original shared32/math16/bio16 without retroactive redefinition. New direction cohorts can overlap original shared features. Full metrics retain all failures; SAE expanded math/bio have1/2holdout scores<=.5. CC has0/0. The display naturally has9math/7bio in each dictionary, with no forced balance.

AUROC is a cross-domain document-pair ranking probability, half credit for ties; use1-AUC for a discovery-fixed biology direction. Discovery ties have no fixed direction and remain NA rather than fabricated. Bootstrap2,000,seed2026102804,resamples documents independently within domain;20x20pair weights encode document draws, not400independent observations. Intervals are exploratory pointwise, not simultaneous/multiplicity-corrected confirmations. No classifier refitting or p-value selection.

Matched random sets:1,000draws,seed2026102805(CC+1),exclude entire target cohort, exact joint bins floor(log2(DCLM_hits+.5)) and floor(total_discovery_doc_support/5). No fallback or forced retention. Both top16, CC math64 and old CC math16 match; remaining full cohorts are NA for inadequate bins. These descriptive backgrounds do not reproduce discovery selection. Spectral nulls are NOT RUN regardless of available random IDs.

All455R04npz schemas were inspected: sparse activations and reconstruction error/latent aggregate moments, not true token h. The loader's transient h was not persisted. Related R05 same-document caches contain attention/norm summaries, not required real-h vectors/covariance; old R03 h/PCA uses different texts. Search scope is bounded to named assets/registered lineage. No reconstructed-h or old-basis substitution.

Native selected decoder vectors were read with fresh checkpoint SHA checks:183SAE/192CCunion coordinates; native norms match R04 and unit-norm error<4e-16. Their spectral location remains unavailable. Pooled discovery mean, covariance/eigenbasis, true variance, rank, decoder16-band projections, domain mean-difference projections and dev/holdout reproduction are all NOT RUN. Obtaining both hooks for120documents costs120Baseforwards, optionally4checks,~150MiBFP32at160positions(~180MiBat192); no measured timing available. The60discovery calls alone would not satisfy dev/holdout reproduction. No such calls launched.

25numerical checks cover algebra, conditional NA/identity, original probe input agreement, fixed CSR replays and scalar sklearn AUROC. Independent audit adds bootstrap/null/provenance guards. Numerical rounding is clipped to theoretical AUC[0,1]; no scientific setting changes. Original R04 sources and candidate-freeze files remain unchanged. Full formulas/configuration, Chinese readable examples, coverage statuses, source hashes and script references accompany this record. Scientific acceptance/closure remains Unknown.
'''

for name,text in [('summary_cn.md',summary_cn),('summary.md',summary_en),('figures_cn.md',fig_cn),('examples_cn.md',examples_cn),('detailed_cn.md',detail_cn),('detailed.md',detail_en)]:
    (O/name).write_text(text);(P/name).write_text(text)
(P/'figures').mkdir(exist_ok=True);(P/'evidence').mkdir(exist_ok=True)
for f in (O/'figures').glob('*.png'):shutil.copy2(f,P/'figures'/f.name)
for f in ['config.json','source_manifest.json','representation_cache_audit.json','pre_analysis_audits.json','decoder_and_token_provenance.json']:
    shutil.copy2(O/f,P/'evidence'/f)
for f in ['candidate_freeze.json','results.json','numerical_checks.json','SAE_display16_metrics.csv','CC_display16_metrics.csv','SAE_selected_feature_metrics.csv','CC_selected_feature_metrics.csv','SAE_matched_random_summary.json','CC_matched_random_summary.json','arithmetic_examples.json']:
    shutil.copy2(A/f,P/'evidence'/f)
readme='''# R04 domain discriminability: reading entry\n\nRead [中文一页结论](summary_cn.md), then [three figure explanations](figures_cn.md), [a real worked example and counterexamples](examples_cn.md), and [complete methods/limits](detailed_cn.md). [English summary](summary.md).\n\nFigures1/2 are cache-derived exploratory evidence. Figure3 is explicitly a missing-data card, not a spectral result. Native model forwards/training/clustering/interventions:zero. The old R04 artifacts are untouched.\n'''
(P/'README.md').write_text(readme);(O/'README.md').write_text(readme)
print('RECORDS_WRITTEN',P)
