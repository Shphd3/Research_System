# Detailed：频率混合表征与高频路径调用

Anchor：[中文](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/15_24_frequency_composition_common_path_anchor_cn.md)。[冻结Protocol](protocol_cn.md) · [Summary](summary_cn.md) · [数学对象与推断桥](model_and_inference_cn.md)。中文原Anchor、Protocol未被结果改写；英文为伴随译本。

执行根（以下简称R）：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_composition_common_path/20261019T164834Z`。文中相对R的代码、日志、数组路径均在此根下，完整链接见[artifact_manifest.json](artifact_manifest.json)。

## 0. 快速回顾与证据资格

问题：同top2预算下，固定调用高频名单组对，相对自由选择是否改善低频feature输入学习；增量是否超过匹配随机名单的同型干预？

直接结果：8/8模型各完成168步、85,548答案目标；统一DEV终点评估完成。Delta_T宏NLL差+0.00098945，交互I=+0.00246136，未满足负向支持条件。两种子方向不同，预定范围跨零，极低支持另限制宏区间解释。

资格：工程矩阵COMPLETE；点估计可用于冻结设计下的有界比较；统计与机制解释为BOUNDED。预定假设本轮NOT_SUPPORTED，不判普遍无效。研究者机制判断、问题关闭与下一决策为Unknown，未修改Focus状态。

## 1. 必要定义

| 对象 | 实际计算与单位 | 用途及边界 |
|---|---|---|
| feature频率p | TRAIN答案预测位置中z>0比例 | 频率，不是z大小、token频率或语义难度 |
| 末层幅度代理a | z乘原始第28层decoder向量范数 | 非负单项幅度；非正交字典下不是可加真实能量 |
| 频段B1…B4 | 正TRAIN p在原四段对数边界中的归属 | 本轮沿用旧边界；U为907个TRAIN零命中特征，输入不删除U |
| 当前token | cache position_id=t处已经可见的input_ids[t] | 当前位置表征预测t+1；首答案预测位在模板尾部 |
| 目标token | input_ids[t+1] | 答案监督，含EOS；只用于loss／解释，不输入路由 |
| 接收率r | feature命中时，其名单所属专家被调用比例 | 逐feature分母不同；无feature支持是NA，未接收是0 |
| 实际暴露频率q | 送入某专家的位置中feature命中比例 | 与负载满足p×r=load×q；top2总负载2 |
| 有符号PCA系数β | 频段中心化向量与真实中心化h投影的内积／真实投影平方范数 | 含残差合计1，可负，不是独占能量份额 |
| B1宏NLL | 逐feature取命中位置NLL均值，再对有命中的feature等权 | DEV838可估、856NA；同位置可被多个feature重复计入 |
| B1位置NLL | 含至少一个B1的独特位置平均NLL | DEV1,701位置，无重复位置；与宏均值回答不同问题 |

## 2. 研究来源与本轮决策点

两份Oct19会议材料完整阅读，18条实质intuition逐项记录原段落和时间；见[mentor_intuitions_audit_cn.md](mentor_intuitions_audit_cn.md)。原DOCX、逐段文本、先前只读审计在R/provenance。最重要的区分是：输入含共同成分、调用共同参数、共同参数改善任务，是不同命题。

此前已经完成评分校准、φ细分、均值中心化及epoch1专家谱。本轮复用相应证据，没有把旧结果当作新发现。重用／适配理由在R/provenance/reuse_audit.md和math_design_audit.md。当前工作不是旧φ分组学习验证；新T段内按固定hash均分，以避免旧单项子组和不稳定关系同时改变比较。

## 3. 冻结、符合性、修订与偏离

冻结时间2026-10-19T16:51:38.506659Z，即北京时间10月20日00:51。config SHA256：`dc8a3a886d97caf64d2ac97279056edc89818c7cbf727a1adfb662e47725d14e`。原trainer SHA256：`5bbbad26e2f3bdb65166bdbbbfb3a7b7cb3b6d97f699f3a5fd177fd4502d89e5`。中文Protocol SHA256：`80c68d0ca4f8fea92659b5799d70c9ee9ae6881e0fe17d459b664a89d964279d`。

| 已定项 | 实际 | 资格影响 |
|---|---|---|
| 用户自主分析、分析后学习、4H100 Reserved授权 | execution_authorization.json和冻结config保留原授权；用户续办延续原范围 | 未重新索要逐步批准，未扩大预算 |
| 数据、特征池、分数、四臂、两种子 | 全部沿用冻结config，无结果后调参 | 点比较合格 |
| 1epoch、相同168步/85,548目标 | 8/8相同；TRAIN/EVAL共同五里程点 | 无少跑条件冒充终点 |
| DEV终点在八模型完成后统一读取 | receipt明确记录；不按DEV挑checkpoint或策略 | 不是外部新数据；此前已存在提取与路由，表征分析先读过DEV |
| 1000次整对话bootstrap | 原代码执行；当次feature无命中设NA再宏平均 | 支持集合变化；范围不能保证固定838项均值的置信覆盖，原结果保留 |
| 有界执行与恢复 | 原任务文件锁EAGAIN失败；保留T_F，新增有界等待wrapper完成六模型 | 工程修复，无科学参数变化，见修订01 |
| 120分钟墙钟 | 主动时间未超；对话中断约9小时，所以连续自然墙钟超过120分钟 | 明确偏离连续墙钟，不把暂停时间当计算、不隐去超时 |
| 伴随项补充 | 名单／匹配／种子先固定，但登记时DEV部分表征已读 | exploratory，不作为新的独立确认；未据其调整四臂 |

[执行恢复修订01](execution_amendment_01_cn.md)与[探索补充01](analysis_appendix_01_cn.md)独立保存，不改原冻结正文。接口、日志、末尾logger等工程小错误及首次失败证据保留在R/logs；最终输出通过独立校验，未重算无关模型。

## 4. 实际模型、数据与优化

### 4.1 数据和位置

数据/表征资产：`data_tulu_sft_route_20261019t012300z`、`representation_tulu_sft_route_20261019t012300z`。源：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/sft_route_learning/20261019T012300Z`的data和cache。Tulu revision为`6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752`；包含cot、sharegpt、code_alpaca、gpt4_alpaca、wizardlm、flan_v2、oasst1等来源。来源不是认证语义领域。

仅首轮user/assistant，Base格式为Instruction/Response自然语言模板。TRAIN1,024对话/85,548答案预测位置；已反复暴露EVAL256/22,446；DEV128/10,340。只训练答案目标、含EOS，不对prompt/padding计loss。cache hidden、CSR z、block_id、position_id、target可严格配回JSONL的source_file、row、input_ids、answer_start、前文。所有split的current和target逐位置核对通过；不拼不同窗口。

原prompt及标准化prompt/assistant/pair跨split精确重叠均0，近重复仍Unknown。这些split来自同一准备数据，不称外部独立总体。DEV在已检查的旧命名trainer中未作训练指标；本轮先冻结设计再做表征复核，最终loss在全部模型后揭示。

### 4.2 字典、隐藏状态和额外成本

Base/tokenizer：`/data/share/Qwen3-0.6B-Base`。CrossCoder：`.../runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt`；244,140更新、999,997,440累计训练位置。14个实际模型层2、4……28，即零基1、3……27的residual-post；F=16,384，hidden1024，冻结TRAIN中心化/vector RMS与阈值0.051281172782182693。

共享z联合读取14层；末层原始decoder从既有train_fixed.npz复用，逆变换尺度374.349512及偏移保留。不能把z称为仅末层独立激活，也不能把它在线用于任意中间层而不计算后续层。

本轮没有重新提取Base/CrossCoder。训练使用已对齐hidden/z缓存；只执行新增专家与冻结final norm/head。离线成本包括本轮路由计算，原多层提取成本未重新计入；因此端到端部署吞吐、效率收益均NA，不声称免费router。

### 4.3 名单与路由

正频率15,477项按原四段分别1,694/5,673/7,013/1,097项。T在各段按SHA256("20261020:featureID")排序均分，八组847/847/2837/2836/3507/3506/549/548。R用种子73129打散同池，保持八组大小，不匹配段内频率。成员表和每组频率范围见[tables/routing_feature_membership.csv](tables/routing_feature_membership.csv)、[组定义](tables/routing_group_definition.csv)。

组对得分为该组对成员a_i总和除其TRAIN均值；段内两个专家按原始a_i和取大者。F选最高两个不同组对；H固定第4组对加其余最高者。并列取小ID；全零仍保留输入，确定性选择小编号。实际未出现全零回退或H的固定组对零幅度事件。主门槛未调整。

### 4.4 训练

8个独立、全参数可训练bias-free SwiGLU，hidden及中间宽度均1024，非LoRA。每专家3×1024²参数，总25,165,824；top2活跃6,291,456参数，前向专家矩阵乘约12,582,912 FLOPs/位置（不含逐元素、head、Base与提取）。统一TRAIN hidden RMS尺度15.983072484195144，输入h/scale，输出乘scale，两个残差输出各乘1/2。没有减均值。

随机gate/up、零down，初始旁支输出严格0；不能把所有矩阵都置0。smoke实际logits最大差0，第一步down梯度非零、后续gate/up梯度非零。训练中专家逐步梯度和暴露有日志。配对seed11/22共享初始化和数据顺序。

1epoch；有效batch512、micro128，最后batch44；168更新、85,548有效答案目标，每条件共171,096次专家位置暴露。loss为有效答案CE总和／真实有效batch目标数，无路由正则。AdamW lr3e−4、betas(0.9,0.95)、eps1e−8、wd0.01、clip1、warmup9、cosine末端0.1。未调第二学习率。

步0/42/84/126/168共同评估完整TRAIN/EVAL。终点168预先固定，未挑EVAL最优。每seed共享初始权重；42/84/126为仅权重里程点；168保存model、optimizer、RNG、order、cursor、tokens与计数。正式Full续训没有重演；smoke下一步权重/优化器/NLL精确恢复已验证，二者分开登记。

## 5. 指标和预定判别

最低频主池是本轮T-B1全部1,694项，**不是旧cache.low_ids的964项**。同一DEV838可估池用于全部条件；每项NLL按其命中位置平均，最终feature等权。同位置可对应多个feature，不视为独立重复。另报1,701独特位置平均及整体10,340位置平均；高频宏/位置表同时交付。

主比较Delta_T=T_H−T_F，Delta_R=R_H−R_F，I=Delta_T−Delta_R。支持需Delta_T及I均负、原预定范围均在0下，并查看两seed方向。0.01 nats实用量级先固定。1000次整对话共同重采样保持策略与seed配对；不把2seed当作足够总体重复。此次主点已不满足支持，区间风险不用于改换方法挽救。

## 6. 决定性证据链

| 问题／判别 | 原始材料与计算 | 实测值 | 允许结论／限制 |
|---|---|---|---|
| 高频固定调用有无学习增量 | final_evaluation/condition_results.csv、paired_comparisons.csv；train_matched.py698–808 | Delta_T+0.00098945，I+0.00246136 | 本轮不支持；种子方向不同、范围跨0、低支持 |
| 混合是否落实为接收 | 原CSR z＋固定route；route_analysis.py；routing_summary.csv | DEV T72.76%→66.75%，R32.38%→24.08% | 固定槽挤占部分所属专家机会，不能推出功能损失 |
| 高频是否只是均值 | 真实h TRAIN PCA＋raw decoder分解；geometry_analysis.py | PC1总方差11.61%，DEV B4 β90.13%；前16 β68.30% | 与主要变化对齐；不是全空间信息比例或梯度主导 |
| token身份有多少预测力 | TRAIN current-ID均值，完整DEV冻结复核；token_context_analysis.py | 全部R².43351，已见.68679，未见15.82% | 强身份关联但非全部决定；余量不认证上下文语义 |
| 高低频有无额外伴随 | TRAIN选8项＋同箱等规模随机；cross_band_companions.py | DEV≥5支持114项，事件差+38.06pp | exploratory关联；格式/token/context未隔离 |
| 语义能否稳定命名 | 固定16项、64展示槽、50可读文本；完整前文/当前/目标分开 | B1四项DEV支持1/0/1/1 | 不能认证稳定语义或“稀有知识” |

完整对应源表、哈希及资格在artifact_manifest；代码入口与freeze receipt在执行侧。

## 7. 全部主要结果与负结果

[全部条件原值](tables/condition_results.csv)、[配对原差](tables/paired_comparisons.csv)、[全部DEV逐feature结果](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_composition_common_path/20261019T164834Z/tables/learning_final_per_feature_dev.csv)及[主B1池阅读表](tables/dev_low_feature_results.csv)；TRAIN/EVAL逐feature大表留执行侧，所有未知均NA。

T_F、T_H、R_F、R_H双seed整体DEV均值分别1.22614/1.22714/1.22720/1.22698，Base1.24887。B1宏均值分别1.05632/1.05731/1.05339/1.05192，Base1.06584。各臂整体均改善，不是全条件loss异常恶化。

Delta_T两个seed为−0.00015215、+0.00213105；Delta_R为+0.00004101、−0.00298483；I为−0.00019316、+0.00511588。均值预定范围依次[−0.00303863,+0.00478613]、[−0.00736736,+0.00352981]、[−0.00388754,+0.00983927]。不存在两个种子一致且明确的主增益。点差小不等价证明差异为零。

T_F对R_F的B1宏均值差约+0.00293，未显示频率组织优于这一随机名单；这不是随机名单总体优劣结论。R_H为四臂中最低宏点值属于事后描述，不把它晋升新最佳方案。T_F/T_H含B1位置均值1.06189/1.06276，均略高于Base1.06049；R_F/R_H为1.05525/1.05346。宏均值和位置均值权重不同，不能挑一个隐藏另一个。

TRAIN终点整体NLL八模型为0.94702–0.95967，完整学习曲线见图4。小样本smoke64位置拟合1.78766→约0.0000294，同时辅助64位置验证1.40844→7.13281；这是预限定过拟合诊断，不是八个正式模型失败。未因其扩大调参。

### 7.1 token与feature不能互换

DEV全部位置R²=.433508，已见ID8704位置R²=.686793，未见1636回退TRAIN全局均值而R²=−.116889。已见ID的平均绝对误差.00056299，TRAIN全局均值预测.00140018。EVAL全部.432356、已见.597763。排除首答案模板预测位后相近。相同ID内部方差占已见面板总方差DEV13.69%、EVAL20.11%，这是描述性分解，不是上下文因果解释率；也与TRAIN拟合预测器的R²不互补。

### 7.2 伴随结构和不确定性缺口

TRAIN对全部1,694低频项选择8个B4伴随项，按P(high|low)−p_high正差排序、tieID；匹配10个log频率箱内等数量随机，固定seed。无重新搜索路由、无EVAL挑例。

DEV所有838有命中项的宏伴随率57.87% vs21.52%，点差36.35pp。支持≥5的114项宏56.02% vs20.08%，点差35.94pp；事件等权则58.15% vs20.10%，差38.06pp、整对话百分位范围34.04–42.66pp，共831低频命中事件（不是831独特位置）。支持≥20的DEV项为0，保留NA。

TRAIN宏点差69.86pp却不落在原区间67.32–68.57pp内。只读源码审计发现重采样零命中项被排除后重新宏平均，有效项集合改变；DEV同样有此风险，点在范围内也不能认证覆盖合格。故主文只描述宏点，并用事件加权结果说明关联；保留所有原表，不重跑选更漂亮区间。事件比例也不涵盖成员选择、频率箱匹配残差和支持筛选的不确定性，且补充是探索性。

### 7.3 旧top1失败分解是背景，不是新学习对照

已复现旧φ-R1 EVAL低频宏接收72.218%，未选频段22.832个百分点，选中频段但未选子组4.950个百分点。其事后top1宏接收oracle约97.02%，只说明评分距本面板诊断上界仍远，不是部署规则。新均衡T名单与旧名单不同，新top2又不同算力，不能由两者差异认证φ或top2收益。

## 8. 五图及读法

[完整图外解释](figures/reading_cn.md)对每图给出观察、允许结论和设计影响；同名source CSV和plot_manifest记录来源SHA。

1. [图1 current-ID预测](figures/figure1_token_identity.png)：横轴EVAL/DEV，纵轴R²；并列已见与全部，再列未见支持。显示身份有预测力，但不等于语义解释。
2. [图2 有符号几何](figures/figure2_signed_geometry.png)：TRAIN拟合PC1/前16子空间，各频段β与总方差覆盖分开。误差为固定投影下整对话重采样；不能把β当独占能量或整个信息量。
3. [图3 静态分发](figures/figure3_static_routing.png)：同一B1池的接收、第4组对调用、专家负载分开；总负载200%。H的100%组对调用由规则强制，不作机制证据。
4. [图4 学习曲线](figures/figure4_learning_curves.png)：横轴真实已更新答案目标数0/21504/43008/64512/85548；完整TRAIN与已暴露EVAL的整体及B1宏NLL分开，两seed保留。显示旁支确实学习，不能用EVAL选终点后称独立验证。
5. [图5 终点DEV](figures/figure5_terminal_dev.png)：四臂两个seed原值、三种配对差、零线与原百分位范围；图中明确可估feature集合随重采样变化。主方向不支持，不把范围当固定838项的正式覆盖保证。

全部PNG实际查看通过；PDF另存可放大。详见rendering_review.json。没有生成额外花哨图来代替问题判断。

## 9. 阶段失败与原因区分

| 阶段 | 事实／检查 | 排除什么 | 仍未区分 |
|---|---|---|---|
| 位置和监督 | 全三split current/target对齐，标签shift与EOS通过 | 本轮不是错配窗口／prompt loss冒充答案loss | 近重复未知、来源混合 |
| 初始保真与梯度 | smoke logits差0、down先有梯度，上投影后有梯度、精确恢复通过 | 全零矩阵死支、立即改变Base logits | 不证明所有专家已学到有用功能 |
| 原任务失败 | blocking AFS flock EAGAIN；六模型正式更新前退出 | 不是模型数值崩溃，不改学习参数即可恢复 | 共享存储仍可能有未来锁语义问题 |
| 完整训练 | 8模型相同168步，TRAIN下降，整体DEV优于Base | 全条件实现异常恶化解释不成立 | 不保证低频各feature改善或充分收敛 |
| 主假设 | Delta_T/I不满足支持，种子不一致 | 不能由混合表征直接推出固定高频调用收益 | 高频代理错、固定槽挤占、有限预算、Base已够用等仍竞争 |
| 语义与统计 | 低支持、bootstrap有效池变化 | 无法以少数高激活例命名稳定知识 | feature意义、同token上下文与任务有用方向 |

本轮没有验证某个物理机制已被反证。被削弱的是从频率/共现/PCA代理直接推到固定调用有益的决策跳跃。

## 10. 完整轮次、成本与恢复

北京时间10月20日00:48开始本轮：完整读会议→冻结假设及设置→CPU token/几何/路由→通过分析门槛→GPU smoke→原正式任务部分成功、存储锁失败。后续用户续办时先确认原任务FAILED，保留T_F两模型并恢复其余六模型，最后统一DEV与报告。R目录UTC日期10月19日不代表这是另一日新实验。

原GPU任务pt-gzle2ypd，FAILED，主动109.453秒；恢复pt-4kefocs4，SUCCEEDED，平台2026-10-20T02:03:08Z—02:05:12Z。恢复监督器正式记录119.481秒，累计228.934秒，约3.82分钟；调度／平台边界时间另列。中断约9小时没有训练执行，不计主动预算；连续自然墙钟120分钟未满足，已明确修订记录。未开并行第二预约。

本轮CPU统计实测token16.61秒、几何约23.04秒、路由约29.16秒、探索伴随8.27秒；线程按独立分工总额≤8，单任务峰值约0.90–2.49GiB。GPU阶段总CPU限制8、采样worker峰RSS约6.69GiB（不含监督器轻量开销），单卡峰allocated约1.01GiB；监督器完成时R独立文件大小5.26GiB，后续小表/文档另见最终回执。均低于64GiB RSS、16GiB每卡allocated、24GiB磁盘及35分钟主动GPU上限。原提取成本不在本轮，不给端到端效率结论。

八模型全量里程点、日志、TensorBoard、终点可恢复状态均留执行侧。没有重复训练已完成T_F，没有新Base/字典训练、全量10M关系统计或额外模型提取。

## 11. 解释：本轮真正改变哪条认识

原来可以想象：“低频输入同时含common，补一条高频路径就能更好学习。”今天的证据把它拆成三层：表征确实混合；固定调用也确实改变机会；学习收益却没有出现预定支持。需要保留混合表征事实，撤回“因此应固定高频专家”的直接推断。

高频向量可能携带主要变化，但它们不自动与任务有用的共同更新方向一致。完整Base已提供共同计算；新增高频专家也未通过功能干预认证为common。因此不能把阴性说成common没用。反过来，T_F目标接收明显高于R_F，留出低频loss却没有相应优势，也说明所属接收率不是充分设计目标。

## 12. 不能推断

不能推断共同语义模块、token语义难度、rare知识掌握、参数梯度干扰、attention因果来源、跨模型能力变化、从头容量提升、φ训练效用、top1对top2同算力优势或原始h谱就是W谱。没有去首方向重新提取z，不把旧中心化分布外退化当成功去common。

## 13. 唯一下一决策

研究者决策Unknown。AI建议先问：**在固定已训检查点上，高频名单专家是否有可替换验证的任务贡献？** 通过保持2专家预算的固定权重调用替换，才能把名单/表征代理与实际功能更接近地联系起来；它仍不直接解释训练中介。此建议未执行，不能当新授权或自动延伸本轮。

## 14. 资产、源表、文本与哈希

输入访问、代码复用、实现审计、恢复审计、统计限制、figure source与输出哈希，统一见[artifact_manifest.json](artifact_manifest.json)、[completion_receipt.json](completion_receipt.json)。所有逐feature、逐路由、逐组、交叉项和完整NLL数组保留R；项目只携带必要小表及五图，未复制原缓存或权重。

8个正式checkpoint family、1个真实smoke恢复状态、1个analysis已登记assets/catalog.json，并通过本轮strict访问检查。登记确认存在/保存状态，不替代科学资格；正式续训是SAVED_NOT_REPLAYED。访问快照：`assets/checks/2026-10-20_020552_frequency_composition_outputs.json`（Research_System根相对）。

固定16feature证据及50个可用文本展示槽（位置可能重复）在[文本索引](texts/feature_meaning_reading_cn.md)、[逐条文本](texts/token_context_cases_cn.md)。两个审计的区间警告优先于其中早期照录的宏CI，不把原阅读笔记当主结论。完整机器可读列表、context与原始表都可追溯。

## 15. 导航与完成边界

[中文Summary](summary_cn.md) · [English Summary](summary.md) · [English Detailed](detailed.md) · [Protocol](protocol_cn.md) · [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/15_24_frequency_composition_common_path_anchor_cn.md) · [五图读法](figures/reading_cn.md) · [导师直觉审计](mentor_intuitions_audit_cn.md)。

执行结束，没有挂起训练。代码、源数据、日志、权重继续由MoE_Router所有；Daily只作讨论入口。未自动提交下一实验、修改科学状态、commit、push或外部同步。

## 16. 2026-10-21 用户要求的冻结诊断

上述停止状态指原轮次。后续用户授权的替换结构、逐位置异质性及冻结残差检查见[诊断结果与数值边界](diagnostics_20261021/results_cn.md)。本地GPU前向已完成，旧T_H NLL重放门槛未通过；原主指标与结论保留。普通MoE对照的恢复提交单独记录在该诊断执行次序中。
