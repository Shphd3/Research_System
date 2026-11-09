# Detailed：R09 CrossCoder 领域均值差分解

全字典重建了固定目标词领域均值差中方向一致的一部分，同时仍留下明显向量残差。原留出在`example`／`explanation`下的相对残差为0.5368／0.7214，固定Top32的误差更高，为0.7196／0.8289。发现集每域64候选中，数学16个、生物20个通过注册的**使用偏向复现**检查。频率组对均值差的贡献、成员的领域／家族变化是不同测量。距离补充已完成3,842次前向，其解释保留文本构造和复现边界。

科学owner：[Anchor15_27_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_03_domain_difference_decomposition_anchor_cn.md)；执行合同：[Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/protocol_cn.md)；主执行前不可变快照：[原协议](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/sources/main_frozen_protocol_cn.md)。本记录持有完整设置、数值证据、偏差及复现信息。主分解与频率／家族统计是可用的描述性分解，推断属于已接触数据上的探索；距离结果受构造上下文、领域／日期编辑量不同和有限家族支持约束。研究者科学接受与关闭保持Unknown。

## 1. 测量对象与目的

R07测量真实最后目标词的领域均值；R08说明，混合主空间容纳中心差方向，不等于类间变化占主要方差。R09继续问：哪些冻结字典坐标组成这个中心差，字典还遗漏多少。竞争解释是少量成员集中承担、多成员增强／抵消、措辞／结尾依赖，以及较大重建残差。

每个观测是一份最后目标token的1024维真实向量和一份16,384维共享激活。两种结尾分别分析，使每次领域比较的目标词身份固定。“成员”是字典的固定坐标；“偏向”是数学减生物平均激活差的符号；“个体”是域内主题／文本家族。三条分析路径分别是：用文本因素控制判断哪些变化有关；用表征计算向量与激活统计；用接口及数值检查确认测量质量。本轮没有功能干预或行为预测测试。

## 2. 实际数据、接口与计算

原384条构造英文输入＝48家族×2领域×2措辞×2结尾。原划分24发现／12开发／12留出家族，分别192／96／96行。固定一种结尾，旧留出有48行＝12家族×2领域×2措辞。家族与措辞等权，家族重采样时所有相关变体一起移动。对应数学／生物家族ID是构造对照单位，不表示自然主题相同。主分析保留原目标位置，并非全部239；例如F06原目标位置36。

Base为冻结Qwen3-0.6B。真实接口为零起算block27 residual-post、最终归一化之前。R08缓存了14个奇数block的真实目标向量和原生A22共享z；最后层与R07完全一致。A22仍联合编码block1、3、…、27，保留训练中心／RMS、原生学习阈值0.051281172782182693，native k256。保留旧256-token编码行加归一化零填充至1024的规则，没有最后层独立编码。checkpoint SHA256为`09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`。

完整来源与索引见[R08文本](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/../R08_within_mixed_subspaces_20261029/data/panel.jsonl)和[目标读数](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/../R08_within_mixed_subspaces_20261029/forward/target_readings.npz)。主[配置](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/config.json)登记4个必要输入asset ID；执行记录保存当前严格访问检查和精确来源hash。谱基仍是R07使用的独立自然文本共同PCA，实际保存于R04的`real_spectrum_A01/analysis/CC_common_basis.npz`，不是R08的混合面板PCA。

每种结尾／划分先平均真实向量和包含零值的激活。delta为数学均值减生物均值；成员j的贡献c_j＝激活差×block27 decoder向量×训练还原RMS374.3495121024576。c_j与delta处于同一模型坐标。全成员向量和为delta_hat，残差r＝delta−delta_hat；训练固定均值和decoder偏置相减抵消。统计使用master FP32 decoder转FP64。

报告原始长度、相对残差||r||／||delta||、两差异余弦。方向贡献a_j＝(c_j·delta)／||delta||²可以相加，全部a_j加残差方向份额等于1。负值表示抵消；偏生物成员也可能正向贡献，因为decoder方向同时参与。方向份额不测垂直误差。近零保护阈值为平均真实向量长度的1e−12，主条件均远离它。子集长度和谱能量都先合成向量再计算，保留交叉项。

## 3. 冻结顺序与实际执行一致性

| UTC 2026-10-29 | Actual event / 真实事件 | Evidence / 凭据 |
| --- | --- | --- |
| 14:41 | Frequency/family config frozen / 频率与家族配置冻结 | [config](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/config.json) |
| 14:43:09–14:43:33 | Cache-only frequency/family run / 纯缓存分支运行 | [started](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/started.json); [completed](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/completion.json) |
| 14:47:43.979745 | Main protocol/code/input hash snapshot / 主协议与代码输入hash冻结 | [freeze](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/freeze.json) |
| 14:47:46.357405 | Discovery-only candidate lists saved / 发现集名单保存 | [candidate freeze](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/candidate_freeze.json) |
| 14:48:02.062973 | Main decomposition complete / 主分解完成 | [completion](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/main_completed.json) |
| 14:48:14.013455 | Distance extraction authorized against frozen config / 距离提取配置绑定 | [run authorization](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/run_authorized.json) |
| 14:49:16.345178 | Exact distance statistics file saved during acquisition / 提取中补存精确统计文件 | [statistics config](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/statistics_config.json) |
| 14:50:08.379676 | Independent main audit,1166checks / 独立主审计 | [audit](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/analysis/main_independent_audit.json) |
| 14:50:29.959926 | Protocol A01 records distance details and chronology / A01记录细节与顺序 | [Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/protocol.md) |
| 14:51:55.339413 | All3842distance forwards complete / 距离前向全部完成 | [completion](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/forward/completed.json) |

频率／家族分支先按自己的未改配置冻结并执行，随后才写整合Protocol。主冻结保存双语协议、Anchor、代码、配置及输入hash的不可变副本。距离提取使用冻结构造与提取配置，精确统计文件在提取中、统计分析前写入；A01如实记录顺序，不称整轮所有计算之前已有一份完整预注册。R07/R08原留出本来就是已接触数据。

| 注册项目 | 实际情况 | 对证据资格的影响 |
|---|---|---|
| 主分析原384输入及原生A22接口 | 行身份、最后层、checkpoint、normalizer、gate、decoder均核查 | 分解对象一致 |
| 先全字典后候选解释 |16,384成员×3划分×3结尾视图＝147,456行 | 合并结尾仅辅助，候选不能替代全字典 |
| 发现集选择 |14:47:46保存名单，每域64，连同Top32共141不同成员 | 旧留出不改名单和排序 |
| 独立频率参考 |65,536位置，沿用20命中支持，log／原分位／线性均保存 | 不在目标面板划频率组，支持不足不丢弃 |
| 家族不确定性 |500次固定种子，成对变体一起重采样 | 逐项探索区间；平方统计可有正偏 |
| 距离构造 |3,840派生行，位置及跨距离token多重集合核验 | 填充重排／framing仍在操纵中 |
| 距离预算与冻结 |3,842／3,842，含2重放；没有超限重试 | 参数不变；新240-token近距不是原R08短输入 |
| 数值精度 | 独立FP64恒等式和单列CPU BF16诊断 | CPU精度检查不冒充GPU逐位重放 |

原始来源均保留。没有模型／字典／router训练、新PCA、聚类、功能干预或新资源申请，没有改变旧科学状态。

## 4. 全字典与固定子集结果

下表长度均为原始模型坐标单位，区间为逐项95%家族bootstrap；两个条件各500次均有效。

| 结尾 | 真实差异长度 | 重建长度 | 残差长度 | 相对残差［95%区间］ | 余弦［95%区间］ |
| --- | --- | --- | --- | --- | --- |
| example | 103.515 | 89.285 | 55.565 | 0.536779 [0.521219, 0.579592] | 0.843928 [0.814936, 0.854051] |
| explanation | 52.972 | 38.538 | 38.215 | 0.721408 [0.684047, 0.765007] | 0.693352 [0.649164, 0.731885] |

全字典净方向份额0.727910／0.504418，残差方向份额0.272090／0.495582。它们回答沿delta对齐多少；0.536779／0.721408的残差长度比例回答完整向量还差多少。只报前者会漏掉垂直方向误差。

全部9条件如下；`all`是辅助合并结尾。

| Split / 划分 | Ending / 结尾 | Relative residual / 相对残差 | Cosine / 余弦 | Signed total / 净方向贡献 |
| --- | --- | --- | --- | --- |
| discovery | example | 0.477198 | 0.879719 | 0.809338 |
| discovery | explanation | 0.510190 | 0.860131 | 0.730450 |
| discovery | all | 0.441285 | 0.897408 | 0.797634 |
| development | example | 0.478458 | 0.878819 | 0.803328 |
| development | explanation | 0.652052 | 0.758184 | 0.571945 |
| development | all | 0.481970 | 0.876263 | 0.757806 |
| heldout | example | 0.536779 | 0.843928 | 0.727910 |
| heldout | explanation | 0.721408 | 0.693352 | 0.504418 |
| heldout | all | 0.544345 | 0.839570 | 0.675913 |

[来源：全字典重建数表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/dictionary_reconstruction.csv)。原留出误差高于发现集，尤其`explanation`。这是实际划分间差异，没有模型更新，也不产生新总体的泛化结论。

固定发现排序的原留出误差如下。随机列是从全字典抽1,000集合的中位数，未匹配活跃度或频率。

| k | example固定名单 | explanation固定名单 | example随机中位数 | explanation随机中位数 |
| --- | --- | --- | --- | --- |
| 1 | 0.984013 | 0.986100 | 1.000000 | 1.000000 |
| 4 | 0.966011 | 0.934994 | 1.000000 | 1.000000 |
| 8 | 0.828401 | 0.916278 | 1.000000 | 1.000000 |
| 16 | 0.799584 | 0.888531 | 1.000000 | 1.000000 |
| 32 | 0.719568 | 0.828926 | 0.999977 | 1.000000 |

全字典误差0.536779／0.721408。k32固定子集95%家族区间［0.691360，0.775842］／［0.773115，0.881673］；随机k32中央95%范围［0.994242，1.000535］／［0.994127，1.000892］。[完整划分／k／随机参照](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/cumulative_reconstruction.csv)。入选小集合比均匀随机小集合更能描述差异，但32成员仍未达到完整字典水平。随机集合常含当前面板不活跃成员，因此不是匹配活跃度的集中度零模型。没有挑最佳k或强制曲线单调。

## 5. 冻结成员与“复现”的含义

主名单按每种结尾的发现集严格正向贡献排序。每域扩展名单要求四个发现“结尾×措辞”单元的激活差同号，且跨结尾平均方向贡献严格为正；不要求每个结尾分别为正。按这一平均贡献排序、同值按ID，不使用频率或留出信息。精确名单如下。

| List / 名单 | Frozen IDs in discovery order / 按发现顺序固定的ID |
| --- | --- |
| example Top32 | 13964, 516, 13472, 7971, 16122, 8963, 7388, 3464, 14, 4795, 5494, 14394, 13276, 3196, 13465, 10807, 652, 7182, 15259, 13662, 3483, 3423, 10203, 13855, 3606, 11939, 3018, 3585, 5913, 2138, 359, 12882 |
| explanation Top32 | 13964, 516, 10807, 16122, 7388, 13276, 7971, 3464, 14, 8963, 13465, 4795, 13848, 8399, 9622, 547, 15259, 8060, 1513, 16, 13472, 5494, 3483, 652, 13413, 1676, 7415, 359, 9483, 13662, 2468, 9508 |
| math64 | 516, 16122, 13472, 7388, 8963, 3464, 10807, 4795, 5494, 14394, 15259, 13848, 10203, 359, 8399, 3423, 16, 16323, 9508, 12882, 3585, 9822, 3018, 9713, 15847, 8389, 9277, 13299, 10323, 13925, 2325, 3988, 4040, 8790, 12471, 461, 7303, 11083, 952, 5265, 1237, 1713, 2109, 13473, 258, 8008, 8151, 12957, 4186, 7763, 8909, 5339, 8030, 9900, 9374, 8047, 7820, 7958, 2675, 14024, 15195, 536, 13069, 3640 |
| biology64 | 13964, 7971, 14, 13276, 13465, 652, 3483, 13662, 15057, 12820, 13413, 124, 7978, 9483, 4346, 2468, 12179, 8624, 5900, 8611, 10223, 3837, 11159, 8255, 2163, 10563, 13254, 10862, 6739, 10870, 4371, 10511, 5562, 4529, 10525, 7315, 2431, 7570, 515, 12406, 12976, 13245, 16382, 11013, 7564, 3136, 8594, 6455, 16200, 2396, 8882, 15216, 1765, 10254, 2757, 10200, 16312, 14644, 6369, 11077, 424, 9458, 16262, 3235 |

[不可变候选记录](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/candidate_freeze.json)。四名单并集141成员，扩展名单每域64，没有放宽规则补数。原留出使用偏向规则为：四单元保持发现符号，且两个结尾的激活差区间都排除零。数学16／64、生物20／64满足：

| Preference / 使用偏向 | Recurring IDs / 复现ID |
| --- | --- |
| math | 16122, 7388, 8963, 3464, 14394, 15259, 10203, 359, 13299, 8790, 12471, 461, 1237, 2109, 13473, 4186 |
| biology | 13964, 652, 3483, 12820, 7978, 8624, 10223, 3837, 2163, 4371, 5562, 4529, 12976, 16382, 7564, 16200, 2757, 16312, 6369, 424 |

[所有通过与未通过者](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/domain_candidate_replication.csv)。这36个只称**使用偏向复现候选**。另作逐项补充诊断，其中26个（两域各13）在两种结尾的有符号贡献区间都为正；全141并集中有27个。该补充不修改选择，也不把使用复现变为语义／因果稳定。[独立标记表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/candidate_replication_flags.csv)保留两个量。

真实F04例子说明区别：数学前文讨论同时被3和5整除的整数，用互质关系推得可被其乘积整除；生物前文讨论细菌利用葡萄糖／乳糖，以及葡萄糖抑制乳糖酶生产。两者接相同结尾。f13964在原留出两域、两结尾都100%发生，但example数学／生物均值为0.033092／0.044375，explanation为0.094827／0.102423。激活差−0.011284／−0.007596，有符号贡献却为＋0.023253／＋0.026597。它的explanation激活差区间排零，但贡献区间［−0.004537，0.083930］跨零。F04W0/example甚至反向：数学0.039776、生物0.034404；W1/example则为0.028789／0.042827。平均偏向不是每条文本的规律。

f16122说明有限面板的选择性：原留出example在24／24数学行、0／24生物行发生；explanation为19／24数学、0／24生物。F23预算分配数学前文接example为0.027457，接explanation为0。f7971在explanation下随措辞反转符号。f4186独立参考仅0.434875%发生，却在原留出explanation两域都100%发生。完整真实文本与反例见[实例说明](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/examples_cn.md)，并保留[逐文本激活](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/candidate_text_activations.csv)、[候选条件表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/candidate_conditions.csv)及[结尾对照](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/candidate_ending_controls.csv)。

## 6. 频率组成与家族变化

参考频率是独立DCLM的65,536位置上原生门控后z>0的比例。沿用至少20命中的支持门槛。16,384成员中13,357支持充分，3,027不足（749零次、2,278为1–19次）。本参考没有漏统计；统一表名仍含“unknown”，实际未知数为0。

| 分法 | 发生率百分比边界 | 低／中／高人数 | 含义 |
|---|---|---|---|
| 主log等宽 |0.451725536288%；6.686505701697%|5808／6917／632|每档约14.8倍的相同倍数跨度|
| 原等人数，保留同频并列 |0.2593994140625%；1.34429931640625%|4469／4437／4451|参考排名的三段|
| 原频率线性等宽 |33.0118815104167%；65.9932454427083%|13281／63／13|相同百分点跨度|

两种等宽法共用支持充分范围0.030517578125%—98.974609375%。log适合这份偏斜参考中的倍数差异，不是普适语义等级。[成员与精确边界](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/frequency_groups.json)、[连续发生率](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/all_feature_frequency.csv)均保留。候选并集为log低1、中62、高78、支持不足0；主结论仍来自全部成员。

原留出中，沿真实差异方向汇总每组全部成员的正、负贡献：

| 结尾 | 频率组 | 活跃／全部 | 正贡献 | 负贡献 | 净值 |
| --- | --- | --- | --- | --- | --- |
| example | low | 13/5808 | 0.003415 | -0.000278 | 0.003137 |
| example | middle | 321/6917 | 0.455433 | -0.007074 | 0.448360 |
| example | high | 256/632 | 0.288904 | -0.012491 | 0.276413 |
| example | low_support_or_unknown | 0/3027 | 0.000000 | 0.000000 | 0.000000 |
| example | residual | — | 0.272090 | 0.000000 | 0.272090 |
| explanation | low | 11/5808 | 0.002909 | -0.001234 | 0.001675 |
| explanation | middle | 242/6917 | 0.256824 | -0.011736 | 0.245089 |
| explanation | high | 259/632 | 0.283155 | -0.025479 | 0.257676 |
| explanation | low_support_or_unknown | 1/3027 | 0.000000 | -0.000022 | -0.000022 |
| explanation | residual | — | 0.495582 | 0.000000 | 0.495582 |

[全部组、区间及分法敏感性](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/frequency_signed_contributions.csv)。组净值与残差相加为1。低频净份额在本面板较小，活跃仅13／11个；中高频总量更大，但组规模和活跃支持不同，所以不能把组总量当成单成员优势。f13964说明参考中很常出现，也仍可通过平均强度差参与领域差异。

另一项激活方差计算中，B＝激活均值差平方／4，表示领域中心差；F＝家族均值偏离该领域均值的平方平均；W＝家族内措辞方差。等权、同一个总体分母下T＝B＋F＋W。每成员先算B/T、F/T、W/T，再在当前有变化成员间等权平均。T＝0保留NA，不跨成员直接相加原始z方差。

| 结尾 | 频率组 | 有变化／全部 | B/T领域 | F/T家族 | W/T措辞 |
| --- | --- | --- | --- | --- | --- |
| example | low | 13/5808 | 8.94% | 57.28% | 33.77% |
| example | middle | 321/6917 | 12.93% | 52.79% | 34.28% |
| example | high | 256/632 | 11.23% | 54.19% | 34.58% |
| explanation | low | 11/5808 | 18.55% | 43.44% | 38.01% |
| explanation | middle | 242/6917 | 10.07% | 49.31% | 40.62% |
| explanation | high | 259/632 | 7.74% | 49.48% | 42.78% |

参考支持不足组example全NA；explanation仅1个有变化成员，B/F/W为42.87%／25.27%／31.86%。发生率与B/T的Spearman相关，example为−0.0434［−0.1139，0.0150］，explanation为−0.1473［−0.1814，−0.0662］；与F/T的相关两结尾均弱且区间跨零。组排序随结尾改变，explanation低频均值仅代表11个成员。[完整98,304行](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/all_feature_variance_components.csv)、[组表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/group_variance_shares.csv)、[连续相关](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/continuous_frequency_associations.csv)保留全部情况。B含平方项，有有限样本正偏，分位区间可能不含点估计；不把它设为语义显著门槛。

## 7. 独立参考谱与主图

R07自然文本基按方差序把1024PC分成16段，每段64PC。真实、重建两条曲线都除以真实差异总平方长度，先合成向量、再投影平方。首段结果为：

| 结尾 | PC1–64真实能量／真实总量 | PC1–64重建能量／真实总量 | PC1–64残差能量／真实总量 |
| --- | --- | --- | --- |
| example | 0.476980 | 0.393041 | 0.029252 |
| explanation | 0.298679 | 0.176457 | 0.075392 |

[9条件全部16谱段](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/spectral_decomposition.csv)。两种结尾的重建向量在PC1–64的能量都低于真实向量。残差能量不等于真实能量减重建能量，因为存在交叉项；重建曲线总和也不一定为1。这是在固定参考方向比较几何分布。

| 图 | 坐标与注册对照 | 实际读法及边界 | 来源 |
|---|---|---|---|
|1a残差、1b余弦|横轴结尾，纵轴完整重建相对误差或余弦，加家族区间|方向一致仍可有不完整重建，残差比0.537／0.721|[1a](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure1a_dictionary_relative_error.png)、[1b](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure1b_dictionary_cosine.png)；重建表|
|2分结尾|横轴固定成员数，纵轴原留出向量误差，显示全字典／随机|少成员接近全字典才支持强集中；本次32仍较高|[example](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure2_cumulative_example.png)、[explanation](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure2_cumulative_explanation.png)；累计表|
|3分结尾|横轴参考组，纵轴正／负／净方向份额，并标人数与残差|中高频总量高于当前低频总量，需一起读规模／活跃度／残差|[example](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure3_frequency_example.png)、[explanation](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure3_frequency_explanation.png)；频率表|
|4分结尾|横轴64PC谱段，纵轴投影平方／真实总平方|曲线差定位谱重建偏差，不能逐成员平方相加|[example](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure4_spectrum_example.png)、[explanation](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure4_spectrum_explanation.png)；谱表|

频率分布、分法敏感性和家族方差分别另存补充图，见[分支说明](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/summary_cn.md)。人数与NA标记是图中证据的一部分。

## 8. 受控距离测量

扩展保留每条原领域核心、措辞和结尾，把原中性postfix移到核心前，并把同一批中性填充块在核心前后搬移。每条派生文本240token、最终目标位置239；语义核心终点到目标距离16／32／64／96／144，对应核心终点223／207／175／143／95。每种基础文本配一次紧接核心日期句的Monday→Tuesday单token编辑。每源文本跨距离的token多重集合完全一致。5家族在重分词后需前导`brief`补齐，影响18原输入、180／3,840派生行；[构造QA](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/construction_audit.json)、[全部实际文本](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/panel.jsonl)、[实例](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/examples.md)保留标记。

3,840派生行加2次原R08重放全部完成，3,842／3,842尝试。使用现有H10080GB MIG3g.40gb，峰值GPU分配4,540,560,896字节，提取实测165.964秒。两次真实联合向量与z重放完全一致，原生门控检查通过，模型和A22参数hash前后相同。没有全零z行或非有限值，每行活跃成员212—259。[完成凭据](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/forward/completed.json)、[资格检查](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/forward/qualification.json)。

距离尺度s_j是每成员在原R08全部192条发现输入的激活RMS，与训练还原尺度374.35不同。D为数学减生物平均激活差除s_j，定向版本再乘原发现偏向符号。E为领域成对激活差的绝对幅度，减去两域Monday／Tuesday变化绝对幅度的平均，再按家族、措辞平均并除s_j。有符号D保留绝对值E会掩盖的反转，同时保存原始激活和decoder幅度单位。留存比D_d/D_16在abs(D_16)≤1e−6时NA，d16家族区间跨零时另标不稳定。

所有距离、成员和候选用500次成对家族bootstrap，seed2026102913。仅distance144的E，在12原留出家族上做全部4,096单侧符号翻转，再对141不同候选×2结尾＝282项做一次BH。符号翻转参考需家族零假设对称。E只描述超过这一单token日期编辑对照的幅度；替换整段领域核心的编辑量更大，填充重排和framing也随距离操纵。新的240-token、d16条件不是原R08短输入。

144处E的q<.05者为example83、explanation72；若另要求两种措辞均保持原发现领域方向，只剩37和26，两结尾交集14。因此83／72不能称稳定领域偏向。141候选的原发现RMS都非零，但全字典有15,487成员的原发现RMS为零，标准化距离量为NA。log低频5,808成员中只有20个原发现RMS非零；新留出example在d16／d144只有4／4个低频成员活跃，explanation为5／6，不能据此概括全低频组的距离范围。

[距离统计汇总](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analysis/summary.json)、[候选曲线](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/tables/candidate_distance_metrics.csv)、[全成员频率统计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/tables/all_feature_frequency_distance.csv)、[全成员估计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analysis/all_feature_estimates.npz)、[家族量](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analysis/family_metrics.npz)保存全部距离、结尾、对照、符号、原始单位和不足支持。名单交集及真实成功／失败实例完整列于下文。


### 距离复现、分母支持与真实实例

下表远距条件同时要求：144处E通过BH，且两措辞均保持原发现领域方向。它比“E显著”更窄，是描述性交集。

| Candidate population / 候选范围 | N | example far | explanation far | Both endings / 两结尾 |
| --- | --- | --- | --- | --- |
| all141 | 141 | 37 | 26 | 14 |
| domain_math64 | 64 | 10 | 6 | 1 |
| domain_biology64 | 64 | 22 | 17 | 12 |
| domain128 | 128 | 32 | 23 | 13 |
| original_replication36 | 36 | 11 | 12 | 7 |

两种远距结尾都通过的14个中，log中频9个、高频5个。再要求两个新d16结尾也保留原方向，全141剩10个。原36使用偏向复现候选中，7个通过两远距结尾，3个同时保持两新近距结尾：f424、f4529、f7564。原36中，本来就只有9个在新的近距两结尾保持方向。因此另外27个不能全说成因距离变长而丧失原偏向；240-token框架在近处就已改变响应。

全log低／中／高组中，原发现RMS非零者为20／500／376。新留出近／远活跃数，example为4／4、224／198、215／195，explanation为5／6、157／156、190／181。近距区间排零，可支持数值远／近比的分别2／99／101和3／52／54个；再要求近距两措辞保持原方向，中／高频比例中位数example为0.672／0.702，explanation为0.600／0.687，对应低频样本仅1和3个。这是有条件样本描述，不是整个频率组的时间范围排序。[完整分母支持及所有分法](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/tables/frequency_near_far_support.csv)。

一个真实成功实例沿用原留出F06的矩形地面铺砖与叶片气孔前文。距离144时核心终点95，目标仍在239。example、W0下，f424数学／生物激活0.010436746／0.012389871，带符号差−0.001953125；改Tuesday后为0.010925028／0.012634012。两域日期编辑绝对变化平均0.000366211，因此该家族、该措辞的超出绝对响应为0.001586914。完整文本见[F06表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/tables/fixed_F06_raw_examples.csv)。这个实例与下方12家族汇总是不同证据层次。

f424完整五距离原留出曲线如下，单位为原发现激活RMS：

| 距离 | example D | example E | explanation D | explanation E |
| --- | --- | --- | --- | --- |
| 16 | -0.7223 | 0.7391 | -0.1680 | 0.1798 |
| 32 | -0.7031 | 0.7622 | -0.1801 | 0.1707 |
| 64 | -0.7471 | 0.8301 | -0.1432 | 0.1314 |
| 96 | -0.4793 | 0.5687 | -0.1627 | 0.1815 |
| 144 | -0.6987 | 0.6048 | -0.1916 | 0.1764 |

f424在example的远／近比为0.967［0.602，1.547］，五点曲线并不单调。中频f8624在example为0.390［0.198，0.563］，explanation为0.664［0.482，0.822］；高频f9900在example为0.904［0.727，1.078］，但explanation远距激活为零、近距分母不稳定。清楚的反例是高频f14：example的D在16处＋0.1174、144处＋0.0652，近处就与原偏生物方向相反，但E144仍为正（q＝0.002732）。其E响应因此不能称保留了原领域偏向。[全部留存区间](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/tables/candidate_retention_intervals.csv)。

距离分支已完成，保存[英文报告](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/summary.md)、[中文报告](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/summary_cn.md)、[六图读法](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/figures_cn.md)及[52文件manifest](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/artifact_manifest.json)。这些交集与实例没有增加前向。

## 9. 数值检查与三轮审计

主[数值核验](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/numerical_audit.json)：残差闭合误差为0，有符号求和最大误差2.22e−16；独立FP64“先解码再均值”与“先均值再解码”最大差1.93084e−13。CPU BF16 decoder精度诊断相对真实差异长度为0.00172—0.0036067，单列于明显更大的实测残差；它不声称GPU核逐位复现。第二份实现重算checkpoint／scale／gate、9条件均值与bootstrap、候选、谱、频率和随机对照，共1,166项通过、0失败。[独立审计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/analysis/main_independent_audit.json)。

家族方差恒等式最大绝对误差1.73472e−18、相对误差1.09131e−15，98,304行保留全部成员。[家族核验](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/analysis/checks.json)。距离重放与参数检查是实际GPU前向核验，与CPU精度诊断分开。

三轮审计分别检查：科学识别（问题、四竞争解释、重建与语义／因果区别）；数据统计（家族、暴露划分、候选冻结、独立频率、区间与控制）；实现数值（原生接口、尺度／门控、零更新、恒等式及实际凭据）。见[审计](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/audits.md)、[覆盖表](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/coverage.md)。current-entrypoints检查发现31项既有untracked／stale-map问题，未改变资产身份。链接／数学源码检查不等于渲染验证或科学接受。

## 10. 证据链与资产位置

| 证据问题 | 输入与实际计算 | 结果来源 | 资格与剩余边界 |
|---|---|---|---|
| 字典描述多少真实差异 | 同384 h/z，归一化还原decoder线性和 |[长度／余弦](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/dictionary_reconstruction.csv)、[向量](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/decomposition_vectors.npz)|描述分解有效，保留残差|
| 是否集中于固定少量成员 | 发现正贡献排序、原留出向量和、1000随机集合 |[子集表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/cumulative_reconstruction.csv)、[冻结](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/candidate_freeze.json)|固定名单探索复核，随机未匹配活跃度|
| 使用偏向是否复现 | 四留出符号加两激活差区间 |[复现表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/domain_candidate_replication.csv)、[条件表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/candidate_conditions.csv)|36使用候选，贡献另看|
| 哪些频率组组成差异 | 独立分组、全成员有符号和 |[贡献表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/frequency_signed_contributions.csv)、[频率](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/all_feature_frequency.csv)|组总量含规模／活跃差，不是单成员优势|
| 领域还是域内家族变化 | 每成员、结尾、划分嵌套B/F/W |[全分解](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/all_feature_variance_components.csv)|T0为NA，平方项bootstrap偏差保留|
| 重建谱是否一致 | 合成向量再投到固定R07谱段 |[谱表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/spectral_decomposition.csv)|共用真实分母的几何分布|
| 距离变化怎样 | 匹配长度／库存文本、日期控制、原生共享z |[原始分片](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/forward)、[统计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analysis/summary.json)|构造上下文响应，词序／编辑量限制保留|

生产脚本为`main/analyze.py`、`frequency_family/analyze.py`、`frequency_family/render.py`、`distance/prepare.py`、`distance/acquire.py`、`distance/analyze.py`。精确hash／输入见[主冻结](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/freeze.json)、[频率manifest](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/artifact_manifest.json)、[距离授权](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/run_authorized.json)、[距离统计冻结](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analysis/pre_statistics_freeze.json)。decoder／scale因子、向量、完整表和原始分片留执行侧，研究记录不复制checkpoint载荷。主与家族分支新增前向0，距离3,842，所有分支参数更新0。

## 11. 复现与完成边界

下列是保存环境与冻结文件对应的实际阶段入口。主脚本拒绝覆盖已完成结果；复现需独立输出工作区并保留来源hash。这是执行记录，不自动再次运行。

```bash
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/analyze.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/render.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/main/analyze.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/audit_main.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/prepare.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/acquire.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analyze.py
```

保存的协议／配置包含500次bootstrap、种子2026102910／11／13、随机对照seed2026102912加结尾偏移、固定名单及精确输入版本。没有训练或选择新checkpoint。本轮完成的是有边界的重建与响应描述：已量化残差、成员组合需求、结尾依赖，以及参考频率和家族变化的区别。唯一下一决定由研究者审阅这些观察后作出，不自动新增实验、字典、router、干预或发布。


## 12. 实际输出登记与纯缓存补充

[独立 A–D 补充](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/supplement_ABCD_cn.md)记录追加请求、固定定义与事后分析身份，连接全部 141 名候选、单位 decoder 谱、全字典和匹配背景、频率 × 谱段有符号贡献矩阵。原冻结 Protocol 和主输出数组没有改写。C/D 独立复算通过 2,141 项检查，单位 decoder 能量与联合贡献的最大差分别为 2.11e-15、2.22e-16。D 含残差的行和等于 B 的有符号组贡献，列和等于真实差异的分段谱能量，全部格子和为 1；残差存在于各谱段。[C/D 独立审计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/supplement_ABCD_20261029/analysis/independent_CD_audit.json)。背景比较另通过 26 项审计。这些检查验证计算，不建立语义或因果确认。

距离分支在提取和主报告完成后通过全部 16,239 项独立构造与统计检查。审计复算所有已存成员／候选量及固定的 282 个远距假设，保留零 RMS 的 NA 与家族符号翻转参照的前提。[距离独立审计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/analysis/distance_independent_audit.json)。

六类实际产物均已登记，精确 ID 见[资产登记索引](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/asset_registration.json)，对象与输入边界见[资产说明](/data/250010109/Research_System/assets/domain_difference_decomposition_r09_20261029_cn.md)。[当前严格访问记录](/data/250010109/Research_System/assets/checks/20261029T152118Z_r09_actual_outputs.json)于 2026-10-29 15:21 UTC 六项全部通过；没有声称产生训练检查点。[执行总清单](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/artifact_manifest.json)包含 67 份主／补充文件与各分支清单。[阅读载荷清单](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/payload_manifest.json)和[来源指南](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/sources_cn.md)保存本地交付所选图表的精确身份。资产登记与本地阅读同步不改变科学接受状态，也不等于发布。
