# Detailed：A15_27 R01 自然语言 feature 响应分析

阅读顺序：第1—3节给有界答案与测量资格，第4—6节解释实际计算及主要对照，第7—8节看实例与图，第9—10节核对执行与来源。[Protocol](protocol_cn.md) 保持冻结；本记录拥有实际观察及按注册规则作出的 AI 操作性判断。机制接受与问题关闭保持 Unknown。

## 1. 有界答案与三条分析路径

本轮完成已有预训练 Qwen3-0.6B 与最后一层（零起始27）MLP 输入 SAE 的只读分析。在既有 H100 MIG 上完成288条面板前向和4条复放。按冻结条件，H1 的20个可估候选中10个支持；H2 的3个可估组中 G02／G04 有条件支持；H3 在 f26149／f16240 上支持本次距离／顺序敏感性。97个激活资格特征中仅 f12039 通过操作性等效稳定。三个结论独立，不建立语义模块或专家。

1. 行为与因素对照：只读取预定续写相容性概率；没有可靠正确性标签，不判断理解或推理成功。
2. 表征与组织：同 token 的配对响应及关系组按冻结定义复现，但保留下述词面构成限制。
3. 功能干预与测量质量：未授权或执行干预；本地重构及同条件复放通过，读数合格。

H2 最强的未排除解释是目标 token 支持构成：G02 只在六个 `bass` 案例响应，而随机组匹配的是总支持／频率／强度，没有匹配目标词支持分布。因此，本轮没有证明所有关系组超出词面分层解释。H3 同时改变距离与句序；参考频率另受旧父模型哈希缺失及旧 BF16 autocast／本轮 FP32 SAE 精度差异限制。

## 2. 实际对象与文本对照

样本是一个末尾目标 token 及其可见前缀，不读取不可见后文。原生模型28层、隐藏维度1024，hook 是零起始第27层 post-attention 归一化后的 MLP 输入。SAE 含30000个特征，原生冻结 FP32 编码／解码，使用 ReLU Top32。模型用冻结 BF16 eval/no-grad SDPA，不加输入单位范数归一化或 decoder 偏置预减。

72个案例由 Codex 构造英文自然语言并作受控编辑，不是未经修改的自然语料。A／B／C 各24例，发现／留出各12例，每例四版本；六个目标为 bank／bass／bat／crane／port／seal。合格案例权威是 `panel/qualified_cases.jsonl`，可执行分词权威是 `panel/tokenized_sequences.jsonl`；原 `cases.jsonl` 只是构造视图。每例记录完整线索区间、目标位置、确切分词、来源／构造代理、模板／实体／来源组及改变／保持对象。72个来源组独立措辞，发现／留出各36，模板／实体／来源组无跨侧重叠；相同目标／关系概念仍限制总体推广。

A 改局部修饰词，B 改前文明示词义，C 将相同中性块移到相同线索两侧。A／B 星期编辑保持长度／位置。C 版本保持总 token 长度与目标位置，线索末端距目标由近1变远40／41／45／46 token；完整区间另存，末端距离不代替线索宽度。序列长14—77，低于256。歧义排除及中性内容修订均在首次前向前完成，未按特征响应删文本。

## 3. 测量资格与实际资源

| 分割 | 序列数 | 目标NMSE均值 | 目标NMSE p90 | decoder公式最大相对误差 | 资格 |
| --- | --- | --- | --- | --- | --- |
| 发现 | 144 | 0.0762048 | 0.1059966 | 1.15e-07 | PASS |
| 留出 | 144 | 0.0667846 | 0.0935571 | 1.25e-07 | PASS |

NMSE 是目标重构误差平方和除以 hook 平方范数；门槛事前固定为均值≤0.15、p90≤0.30。手工稀疏 decoder 求和加偏置与原生重构的误差远低于1e-5。A01四版本同条件复放的目标 z 最大绝对差均为0。两阶段模型／字典哈希不变，参数更新为0、无梯度。历史验证 NMSE0.053382 只作背景，以上本地值才使本面板合格。

账本共292条尝试：288面板＋4复放，包括复放共前向11612个前缀 token，最长77。发现144＋4用时20.026秒，留出144用时19.664秒；CUDA峰值分配1687291392字节。用时含加载与检查，不是计算效率基准。执行面是当前容器已有 H100 80GB MIG3g.40gb（40448MiB），无 ACP job、新资源或购买。实际环境为 Torch2.5.1+cu121／Transformers4.53.3，复用 spectral-hier Python 与既有依赖 PYTHONPATH。本轮构造留出已执行；封存 TEST 未读。证据见 [execution_certificate.json](execution_certificate.json)。

## 4. 计算、候选与随机对照

激活 z 与保存的 decoder 列 d 给出原始贡献 c=z·L2(d)，单位对应原生 hook；decoder 偏置单独保留。绝对 z／c 和 c/L2(h) 分别保存，比例变化不替代绝对差。A／B 主差为 changed−base，C 为 near-changed−near-base；无关编辑对照取两次星期效应绝对值的均值，有符号向量另存。尺度是发现集全部案例／版本 c 的均方根，下限1e-8。

候选需至少六个案例及六个来源组激活，并至少六个案例／来源组有非零主响应。30000中特征83个合格；按来源组平均绝对差／RMS排序、同分按ID，冻结64个。仅发现 OLS 移除截距、总 c 对数变化和 hook 范数对数变化；留出系数不变。控制后来源组响应的 Pearson 相关定义关系，平均连接距离1−r、截断0.5、最小组三个特征，得到七组。200次发现来源组自助抽样估计原组特征对共簇率，支持需≥0.70。留出后不换算法或截断。

H1 在发现面板×目标分层固定方向，留出检验有符号语义差超过无关编辑。需≥6有效独立方向组、≥3模板、≥2/3方向一致、超额95%下界>0、BH q≤0.05、移除单模板后超额仍正、最大案例占比<0.35。方向一致率只在非零方向／响应组计算，全组一致率另报。H2 检验支持及方差合格的固定组，并对比各1000次的两类随机对照：保持边际的特征逐列行置换，以及匹配发现支持、历史频率、RMS强度的随机组。匹配各维标准化范围固定为一个标准差，每成员最近20候选，至少800次完整有效抽样；两个随机 q 均须≤0.05，同时通过自助下界与删除单模板检查。

H3 用（远changed−远base）−（近changed−近base），方向由发现固定，原始近／远／基准距离差另列。需六个独立激活及交互组、有效组方向一致≥2/3、BH q≤0.05、95%下界>0。符号翻转9999次，区间使用2000次来源组自助，种子20261026。稳定用独立冻结池检验：均值90%区间严格位于±0.2发现RMS内，平均绝对差单侧95%上界≤0.2；“不显著”不算稳定。确切规则保留在未改动 [Protocol](protocol_cn.md) 和 [statistical_plan.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/statistical_plan.json)。

## 5. H1、稳定特征与H3

64个候选中52个满足一般留出支持；20个满足全部 H1 可估要求，10个通过全部支持条件。实际通过项目为：

| feature | 留出 \|delta\| | 无关编辑 \|delta\| | 定向超额／发现RMS | 95% CI | BH q | 有效方向组数 | 方向一致率 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 18711 | 6.7276 | 0.0291 | 1.1548 | [0.7870, 1.5152] | 0.0064 | 16 | 1.000 |
| 26149 | 3.5235 | 0.0334 | 0.9872 | [0.5373, 1.4554] | 0.0096 | 10 | 1.000 |
| 3743 | 4.7924 | 0.0457 | 0.7945 | [0.4098, 1.1931] | 0.0096 | 17 | 0.824 |
| 6401 | 1.8591 | 0.0214 | 0.6847 | [0.2529, 1.1844] | 0.0442 | 7 | 1.000 |
| 12986 | 1.9306 | 0.0268 | 0.7569 | [0.3413, 1.2008] | 0.0282 | 8 | 1.000 |
| 2453 | 2.1501 | 0.0299 | 0.8859 | [0.4117, 1.4290] | 0.0282 | 8 | 1.000 |
| 20058 | 4.1274 | 0.4212 | 0.5098 | [0.2089, 0.8053] | 0.0096 | 19 | 0.947 |
| 22464 | 2.8717 | 0.0808 | 0.7209 | [0.2701, 1.2547] | 0.0282 | 8 | 1.000 |
| 16240 | 3.8582 | 0.0657 | 0.3246 | [0.1229, 0.5315] | 0.0282 | 11 | 0.818 |
| 27076 | 10.1049 | 0.2089 | 0.8565 | [0.6116, 1.0988] | 0.0064 | 23 | 0.957 |

绝对效应和无关编辑列是原生单位，不是百分比。f18711 的16个有效 A／B 方向组全部一致，但全部24组的一致数为16／24=0.667。这一区分避免把稀疏响应写成普遍响应。全部失败／不可估候选、每例原始差与比例差保留在 [H1_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H1_features.csv) 和 [holdout_case_feature_responses.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/holdout_case_feature_responses.csv)。

冻结稳定池有97个特征，只有 f12039 通过：留出支持6，平均 delta／RMS=0.0711，90%区间[0.0174,0.1419]，平均绝对差／RMS=0.0881，单侧95%上界=0.1539<0.2。f12039只在36个留出基础案例中的6个激活，其余主要为零。这是稀疏支持下本面板平均注册效应的等价，不是普遍上下文不变。来源：[stable_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/stable_features.csv)。

H3 有25个可估候选，两个通过：

| feature | 近距离语义差 | 远距离语义差 | 远−近交互 | 定向值／发现RMS | 95% CI | BH q |
| --- | --- | --- | --- | --- | --- | --- |
| 26149 | -5.6700 | -2.4511 | 3.2189 | 1.1156 | [0.6149, 1.6603] | 0.0288 |
| 16240 | 6.9704 | 1.5124 | -5.4580 | 0.5471 | [0.2905, 0.8072] | 0.0288 |

f26149 的原始交互为正，f16240 为负；定向值采用固定发现方向，q均0.0288。结果支持这种关系保留的位置移动下的距离／顺序敏感性，不能识别纯距离、长程专属或信息传播。来源：[H3_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H3_features.csv)。

### 辅助下一token读数

令候选边际L等于“基准义项兼容候选的log概率”减“改变义项兼容候选的log概率”，单位nat；比较changed版本减base版本。留出B的12案例平均变化−10.542，C近／远各12案例为−10.359／−4.354。负值表示这两个预定候选之间的相对偏好按线索方向改变；候选并非唯一正确后文，没有计算功能准确率，也不把这个诊断称为理解成功。逐序列值和候选原文见 [辅助表](tables/auxiliary_next_token_readouts.csv)，这只是描述性汇总，不新增假设检验或更改H1—H3裁决。

## 6. H2关系组、随机对照与仍存词面解释

| 组（特征数） | 发现共簇率 | 留出平均r | 95% CI | 成员最小留出支持 | 匹配／置换q | 操作判定 |
| --- | --- | --- | --- | --- | --- | --- |
| G01 (6) | 0.915 | 0.7192 | [0.6014, 0.8036] | 5 | 1.0000 / 1.0000 | INSUFFICIENT |
| G02 (3) | 1.000 | 0.8356 | [0.7541, 0.9483] | 6 | 0.0163 / 0.0023 | SUPPORT |
| G03 (4) | 0.487 | 0.4346 | [0.1966, 0.6521] | 6 | 0.0163 / 0.0023 | WEAKENED |
| G04 (4) | 0.845 | 0.6563 | [0.4988, 0.8260] | 6 | 0.0070 / 0.0023 | SUPPORT |
| G05 (5) | 0.532 | 0.4461 | [0.2627, 0.6502] | 2 | 1.0000 / 1.0000 | INSUFFICIENT |
| G06 (5) | 0.716 | 0.6957 | [0.5506, 0.8063] | 5 | 1.0000 / 1.0000 | INSUFFICIENT |
| G07 (3) | 0.727 | 0.3438 | [0.0833, 0.6504] | 5 | 1.0000 / 1.0000 | INSUFFICIENT |

G02／G04通过注册的完整结构条件。G02匹配随机组第95分位0.3262，观察0.8356；G04随机第95分位0.1662，观察0.6563。移除任一单模板后的最低相关分别0.8058、0.5600。G03留出相关为正且两个随机比较显著，但发现共簇率0.4867低于0.70，因此按完整条件削弱。G01／G05／G06／G07均有成员少于六个独立留出激活组，即使热图相关为正也证据不足。不可估组的 p／q=1 是保守占位，不是观测到“与随机组相同”。

对冻结原始差作描述统计、不重新拟合，可见目标层面的支持构成：

| Group | target-token response-support composition | any-response cases |
| --- | --- | --- |
| G01 | {"bank": 6, "bass": 4, "bat": 4, "crane": 6, "port": 3, "seal": 4} | 27 |
| G02 | {"bass": 6} | 6 |
| G03 | {"bank": 6, "crane": 3, "port": 6} | 15 |
| G04 | {"bank": 1, "bass": 6, "bat": 1, "crane": 2} | 10 |
| G05 | {"bank": 6, "crane": 1, "port": 6} | 13 |
| G06 | {"bank": 3, "bat": 4, "port": 2, "seal": 5} | 14 |
| G07 | {"bass": 6, "bat": 6, "crane": 6, "port": 5, "seal": 6} | 29 |

G02全支持来自 `bass`，G04的10个任一响应案例中六个是 `bass`。匹配随机对照控制总激活支持、语料频率、强度，没有控制这个目标分布。同 token 配对排除了每个对比内部的目标词改变，但没有排除跨案例相关来自相同词面分层稀疏支持。因此，H2 是有条件的操作性支持，更强的“超出所有词面解释”仍证据不足。旧 E17 参考还缺产生缓存的父模型哈希，旧编码为 BF16 autocast、本轮 FP32，TopK临界支持可能不同。这些限制如实保留，不靠调参或新前向修复。各成员按目标词的支持另见 [H2_target_support_description.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H2_target_support_description.csv)。来源：[H2_groups.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H2_groups.csv) 和 [reference_frequency_provenance.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/reference_frequency_provenance.json)。

## 7. 三个固定案例与真实反例

完整可见前缀、token切分、线索区间与目标偏移见 [qualified_cases.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/panel/qualified_cases.jsonl) 和 [examples.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/examples.json)。以下实例均为发现案例，留出统计单独标明。

### A01：局部词面／搭配

目标 `bank`，token ID 6073，零起始位置 16。基准线索是“river”，改变线索是“savings”；两版均在该目标结束。f6401 在这个事前固定案例中的原始贡献为 0.0000→4.0446，差为 4.0446。案例固定为 A01/B01/C01，所示特征仅从事前冻结八个作图特征中取该案例最大绝对差。它解释读数，不给特征贴整句语义标签。 这里改 river→savings，属于局部线索；星期编辑是相同长度／位置的负对照，不能将这个例子称作长程。

### B01：前文决定词义

目标 `bank`，token ID 6073，零起始位置 32。基准线索是“The account describes land beside a river, with water washing against soft soil.”，改变线索是“The account describes an office handling money, with clerks arranging new loans.”；两版均在该目标结束。f12986 在这个事前固定案例中的原始贡献为 0.0000→4.4283，差为 4.4283。案例固定为 A01/B01/C01，所示特征仅从事前冻结八个作图特征中取该案例最大绝对差。它解释读数，不给特征贴整句语义标签。 目标附近保持“The bank”，词义线索完整位于前文；只有整个留出 H1 表的重复支持才支持跨措辞响应。

### C01：同关系的近远距离

目标 `bank`，token ID 6073，零起始位置 62。展示的近／远版本均保留同一句线索“A stream runs past the strip of soil that forms its outer edge.”，两版均在该目标结束；金融线索只用于另外的同距离词义对照。f26149 在这个事前固定案例中的原始贡献为 4.1442→0.0000，差为 -4.1442。案例固定为 A01/B01/C01，所示特征仅从事前冻结八个作图特征中取该案例最大绝对差。它解释读数，不给特征贴整句语义标签。 同一基准线索的近／远末端距离为 1／40 token，目标位置不变；f26149 的近距离语义差 -4.1442、远距离语义差 0.0000。移动相同中性块也改变句序，因此该例不是纯距离因果证据。

### 反例 C10：单例变化大，留出复现仍不足

按固定规则，首个未支持 H1 的发现候选是 f24995，它在发现集最大变化发生于 C10（目标 `crane`）。原始贡献 10.5743→0.0000，delta=-10.5743。留出 A/B 只有 4 个有效方向组，低于六组；q=0.1072，最大单案例绝对超额占比 0.5069，超过0.35。即使该特征的平均定向超额为正，也不能把这张大响应图当成跨表达复现。判定是证据不足，而非证明不存在响应。

## 8. 图的直接证据角色

**图1：**研究问题是固定前缀实例在各 token 处如何响应；对象是八个冻结作图特征的原始 SAE z。编辑前后共用色标，青色标出目标／线索，保留全文和token。直接观察是第7节量化的实例变化。允许解释为这些实例的激活分布，不能推出聚类稳定、整句含义或功能成功。数据为 token缓存与 `token_cache_index.json`；阅读图为 [token热图](figures/figure1_token_feature_heatmaps.png)。

**图2：**研究问题是哪些配对响应关系复现；对象是控制后贡献差的发现／留出 Pearson 相关，顺序固定为发现树。直接观察是七个发现组、两个完整通过、一个削弱、四个支持不足组。伴随注释表列原生基准／变化幅度、参考频率及支持。允许解释为本构造面板上的既定关系组，颜色块不能验证语义模块、专家或导师未定义的cluster。数据为发现／留出冻结统计及H2表；阅读图为 [响应关系](figures/figure2_response_relations.png) 与 [特征注释](figures/figure2_feature_annotations.png)。

**图3：**研究问题是在近远构造下关系响应是否改变；对象是留出C中前八个冻结候选的平均原始changed−base。直接观察是匹配位置间各候选均值线变化，只有完整H3表裁定哪些变化通过。允许解释为该位置移动下的距离／顺序敏感性，不能推出纯距离因果或长程专家。均值线仅描述，区间／q见第5节及完整H3表。阅读图为 [近远对比](figures/figure3_distance_pairs.png)。图契约／来源保留在 [figure_contracts.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/figure_contracts.json)。易读版只改排版，不改冻结统计或候选身份。

## 9. 协议符合性、失败与完整轮次

前向冻结时间为2026-10-26T10:57:10.043841+00:00，当时模型前向为零、未观察特征筛文本。首次发现启动为2026-10-26T10:57:20.343895+00:00。候选冻结 SHA256 为`a54c37ab0854c4a2e9c535c87d9720cdc8a03c719d19856ae148ad3ea66b5838`；留出144条前向开始收据记录的正是该哈希。当前主runner／分析／计划／配置／合格清单及两种语言Protocol均匹配冻结哈希。未观察到开始后的实质修订、替换候选、放宽门槛、参数更新、激活干预或新资源。各分割各一份启动收据，账本无重试。冻结前的文本／精度澄清不是看结果选样。执行证书保留当前源码核验。

| 项目 | 注册条件 | 实际及证据 | 资格 |
| --- | --- | --- | --- |
| 面板 | 72例/288序列，≤256token | 72/288，14—77，合格manifest哈希一致 | ELIGIBLE |
| 前向预算 | 288面板+4计划复放，总≤1000 | 292条，完整序列账本 | ELIGIBLE |
| 测量 | 均NMSE≤.15,p90≤.30及公式/复放 | 发现/留出PASS，4条复放完全一致 | ELIGIBLE |
| 发现→留出 | 仅发现尺度/候选/树，先冻结 | 留出启动记录候选哈希 | ELIGIBLE |
| H1 | 完整冻结条件 | 20可估，10通过 | ELIGIBLE_BOUNDED |
| H2 | 两null+稳定+支持 | 3可估，2通过，仍有词面构成解释 | BOUNDED |
| H3 | 同关系/长度/位置 | 25可估，2通过，句序共同改变 | BOUNDED |
| 功能成功/干预 | 未授权 | 未运行，只有相容性概率 | NOT_RUN |
| 训练/封存TEST/新资源 | 禁止 | 0更新，封存TEST false，0新资源 | CONFORMING |

本轮六项内容齐全：问题／H1—H3；一套冻结父模型／SAE及受控版本；无新训练数据或更新（保留旧SAE／参考来源）；独立构造发现／留出；真实测量及上述失败；有界解释和下一决策。测量资格通过；支持稀疏、发现组不稳和目标构成分别解释不同未通过，不能将它们写成未测试因果机制被否定。

## 10. 证据链、产物与下一决策

| 判定 | 原始读数→计算 | 独立单位／不确定性 | 有界结果 |
| --- | --- | --- | --- |
| 测量 | 目标h/z/hhat→NMSE/公式/复放 | 每侧144序列，4复放 | 两侧合格 |
| H1 | 目标c→方向语义差减无关幅度 | 来源组，2000boot/9999sign/BH | 20可估，10通过 |
| H2 | 控制后c差→相关及两类null | 来源组，200次稳定/2000CI/1000null | G02/G04操作通过，词面分层解释仍存 |
| H3 | C四版本→语义差的差 | 来源组，2000boot/9999sign/BH | 2通过，仅距离/顺序 |
| 稳定 | 原始主差/RMS→等效性 | 冻结97池，90%均值CI/单侧95%绝对上界 | 仅f12039 |
| 实例 | 固定案例+冻结8作图特征+确定反例规则 | 单实例，不是复现单位 | A01/B01/C01及f24995C10 |

完整产物账本如下。每项保留在既有执行owner并记录确切身份，不建立第二份可编辑原始数据。核心事实记录完成，原始NPZ／表格保留全部候选、支持、缺失与失败组；选中图是派生阅读副本。本轮没有新训练检查点。本轮文本、保存的表征及分析已登记为 `data_natural_language_feature_panel_20261026`、`representation_natural_language_feature_response_20261026`、`analysis_natural_language_feature_response_20261026`，三项当前严格访问检查通过；登记不扩大科学结论。

| Artifact | Role | SHA256 |
| --- | --- | --- |
| [pre_forward_freeze.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/pre_forward_freeze.json) | provenance / statistics | 29f5b17169f5f15c2e9ec61214b2ecf8edbd4574e9eaeebe38848def865594a9 |
| [analysis_config.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/analysis_config.json) | provenance / statistics | 1f57d8d70a865fed205e5531395d70b29af61fe2c5e35be410c4da72874f7bbb |
| [asset_audit.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/asset_audit.json) | provenance / statistics | f2743c3d64f9cdcb8c852ce97e26ef6b62545ca6a7688d580e57972327884cd0 |
| [qualified_cases.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/panel/qualified_cases.jsonl) | provenance / statistics | 33a2f75ae0ea6ed6225e089d4d4ac7ae6230390af6e1ca3ddb06e1f93be4f4ee |
| [tokenized_sequences.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/panel/tokenized_sequences.jsonl) | provenance / statistics | 945914b9007a4a576f6de99b00b791af56e8daf4464de9169959e733b20d2246 |
| [discovery.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/forward/discovery.npz) | raw measurement | 51793c0bb38b05517a21f2a961ff4471e0c5edaf5c5085198b7f7613959fb2f5 |
| [holdout.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/forward/holdout.npz) | raw measurement | c9331111ba0cf318f488500b47ee68ab26556be3c5cd025eddc6e754cfe7b8e2 |
| [forward_ledger.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/forward/forward_ledger.jsonl) | provenance / statistics | 85d26d14062a5eafa1359ee29e63e417fcdedddeee225964ccad036438ac8a9f |
| [discovery_qualification.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/forward/discovery_qualification.json) | provenance / statistics | b2636fdf593228ba2dc81000dc1536570001b88981a14207431c6b46e1c7c82c |
| [holdout_qualification.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/forward/holdout_qualification.json) | provenance / statistics | 4d4b9c86682a10b81676c75801f33a125359beb8040e450e41fe70c2c1597b5b |
| [candidate_freeze.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/candidate_freeze.json) | provenance / statistics | a54c37ab0854c4a2e9c535c87d9720cdc8a03c719d19856ae148ad3ea66b5838 |
| [discovery_statistics.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/discovery_statistics.npz) | raw measurement | 927852281b420118a6a27aba34f9dfd779c32d440295d897735a73a10a6e2279 |
| [holdout_statistics.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/holdout_statistics.npz) | raw measurement | 1af6339236f348a0c22fe6f160a3e568be426b924f19a7f32b25513f6d380f74 |
| [statistical_plan.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/statistical_plan.json) | provenance / statistics | 2d316e8fa20d0d0843ea5e8afe995c32c30f4b7e390594331fb2ed497c170f03 |
| [results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/results.json) | provenance / statistics | 4b4c69c2b3cac2e261d17eb5dd2bebbfc55d2e16b56e0e01600345dededf4bca |
| [H1_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H1_features.csv) | provenance / statistics | 8693b45019abb03e79701faa040517b24056568e46aa129561629c9136c256db |
| [H2_groups.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H2_groups.csv) | provenance / statistics | f65b409d6024eee20112a4d0ca361b14f75742eb27501983074e43aa6846021c |
| [H3_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H3_features.csv) | provenance / statistics | c81e8e2d015418aa9eea2c0e7480dca2e8ae3ea357a437437f5db312fe110361 |
| [stable_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/stable_features.csv) | provenance / statistics | cc50e9c089298101e6b2ed6d235c9d6fe31ad8b1806cd11af552fadb77aff51c |
| [examples.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/examples.json) | provenance / statistics | 97092d984abc33db74f27815871cb732a632ea2e1aff91f112a25efea09a8530 |
| [reference_frequency_provenance.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/reference_frequency_provenance.json) | provenance / statistics | c66039cc69bf6238cf52831d68d9e2720d0f8c856e81d3c8fb64e246f8558fb6 |
| [figure_contracts.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/figure_contracts.json) | provenance / statistics | 7eb2a4efac6a0afddf507d0c15e204f6015cb0e837f3bc2841f5a81300f4d377 |

唯一下一决策仍由研究者作出：用本轮有界结果明确关系定义，再决定是否进入功能干预和专家分工。**AI建议的最小后续问题：**固定 bass 并匹配目标词条件支持后，G02／G04组内关系是否仍复现？本轮没有执行或自动授权该新实验；这个问题直接针对最强未排除解释，不把已有关系组升格为专家。机制接受与关闭保持 Unknown。
