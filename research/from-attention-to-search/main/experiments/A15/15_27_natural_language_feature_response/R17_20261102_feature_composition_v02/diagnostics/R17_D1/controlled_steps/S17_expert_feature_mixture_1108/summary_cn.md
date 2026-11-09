# S17：普通MoE的专家feature组成与激活—路由对应

**按“低激活相似成员应分开”的标准，当前末层两个固定标点读取位置的硬专家分发区分度不足：低相似成员在不同token中仍大量进入同一专家对；权重保留部分区分，功能干扰尚未测量。** 这轮完成的是既有缓存CPU事后探索，未新增文本、读取位置、模型前向、GPU任务、训练、权重/bias修改或功能干预。

原始数据先给出结论边界：主样本是旧CONF显式末冒号1152位置，不代表全文路由。全部末冒号tokenID25、正文末tokenID624（句号加换行）；身份已固定，绝对位置／上下文长度仍变化。其余三表达和正文四表达分别有表，未混成一个平均。S16前轮新场景复核已经完成、因覆盖和行为不足不能确认，不在本轮覆盖或重写。

## 原始数据：先明确专家究竟接收什么

同一普通8层MoE（33B训练token、507988992参数、8expert/top2）末层router输入SAE（1024→30000、正Top32）与原生路由来自S15同位置记录。这里的“feature进入expert”指携带该坐标的完整token进入expert，不是坐标独立选择。对expert看P(feature活跃｜expert入选)，对feature看P(expert入选｜feature活跃)，两者分母不同。

主条件实际有**702个不同坐标、36,864次激活事件**。53个旧候选只覆盖18,267事件＝**49.55%**；未分类649坐标、50.45%事件均保留。跨所有旧DEV/CONF、两位置四表达的总观察坐标为1825，不能把53候选当完整字典组成。

| expert | 接收位置 | 不同成员 | 激活事件 | 场景／类别覆盖 | 可否判断选择性 |
| --- | ---: | ---: | ---: | --- | --- |
| 1 | 1129/1152 | 695 | 36,128 | 入选16场景／24类；未入选只2场景 | 近乎全选且反侧支持不足 |
| 6 | 1152/1152 | 702 | 36,864 | 入选16场景／24类；没有未入选 | 全接收恒等，不能识别偏好 |
| 7 | 23/1152 | 114 | 736 | 仅2场景，虽覆盖23类 | 不能拿23类覆盖替代跨场景支持 |
| 0/2/3/4/5 | 0 | 0 | 0 | 主条件没有接收 | 不据此声称整个模型闲置 |

这些类别来自输入文本，角色来自旧DEV激活统计；S14/S15已有家具等行为资格不足，本轮未修复，不能把角色表当成新的语义分类证据。

同expert内的频率与共享角色混合属于共同接触。源实现确认：选中expert接收完整1024维h，输出再乘该token的gate；实际训练路径回传语言模型CE，并独立调整负载bias，**没有显式的feature相似性／拆分组织目标**。这说明你的准则不是其直接优化对象，不证明加入该目标一定有益。代码与哈希见[source_architecture_audit](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/evidence/source_architecture_audit.json)。

## 结果分析一：频率与共享范围混合，主要随输入背景

![频率与角色组成](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/figures/01_frequency_and_roles.png)

上排分别是题干Q、通用DCLM G的同MoE/SAE末冒号参考频率累积分布（CDF）。横轴从0到1，小频率区域展开；纵轴是低于某频率的累计份额。灰点线按不同坐标各算一次，实线按真实出现事件加权。**成员清单和接收事件回答不同问题。**

输入总体的Q参考中位数：成员等权0.333%，事件加权11.267%；G分别0.400%与6.500%。Q均值3.227%与28.870%，G均值2.629%与22.758%。因此存在许多参考低频坐标，而少数常见坐标反复出现；这不是“高频压制低频”或长尾知识学不好的证据。

expert6接收全部token，频率画像与输入**完全相同**。expert1事件Q均值28.887%，类别配比匹配背景28.870%；G为22.750%与22.759%，这里只报告有限面板差值，不做“足够接近”的等价性声明。expert7画像有差别，但来自两场景，不能称它专门接收某类低频知识。其114成员的清单较短也受接收样本只有23条影响，不能将清单长度与1152输入直接当公平选择性比较。

下左按旧DEV角色的**确切交集**互斥展示，避免重复坐标计数；原始非互斥表仍保留。输入／expert6的至少一类对共享成员事件37.49%，至少一类对偏向成员13.55%，普遍背景21.20%，未分类50.45%；前三者有重叠，不能直接相加。八个细类对中，共享和偏向成员在同token共同出现比例64.58%至100%。它们共用expert首先反映整token路由。

下右为expert6（即输入）的“DEV稳定覆盖类别数×G参考频率”事件组成。稳定覆盖是DEV某标签≥12/24家族且≥4/8场景，只是使用范围。0表示没有达到此阈值，**不等于该成员未出现或只代表一个语义**。完整连续分布和逐对角色由[frequency_summary](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/results/frequency_summary.csv)、[role_frequency_joint](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/results/role_frequency_joint.csv)、[pair_relative_roles](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/results/pair_relative_roles.csv)持有。

## 结果分析二：按你的准则，硬选择没有把低相似成员充分分开

操作定义先固定：在576个DEV显式位置上，以二值激活模式的φ（中心化相关）衡量相似，同时报告幅值cosine；两种量不能混叫语义相似。仅从旧53坐标中按支持和不参考路由的规则固定最多5高φ、5低φ；实际只有4个高φ对达标，保留缺项，没有放宽阈值。旧CONF已被查看，所以本轮仍属事后探索。

![原始富集与激活—路由对应](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/figures/02_enrichment_and_alignment.png)

右图横轴为DEV φ；空心圆是CONF归一化硬选择分布TV（每个入选expert记1/2），方点是实际gate分布TV。越高表示两个成员伴随的路由分布越不同。这是逐成员在其活跃token上平均后的差异，不把32个共激活坐标算成32次独立选择。

| DEV冻结对 | 坐标 | DEV φ／幅值cos | CONF φ | 硬路由TV／权重TV，百分点 | 两侧独有token支持 |
| --- | --- | ---: | ---: | ---: | --- |
| high_1 | #3460 / #21462 | 0.593 / 0.648 | 0.626 | 0.221 / 1.135 | 不足 |
| high_2 | #8676 / #23551 | 0.564 / 0.564 | 0.489 | 0.222 / 0.483 | 不足 |
| high_3 | #638 / #17672 | 0.550 / 0.706 | 0.677 | 0.844 / 0.475 | 不足 |
| high_4 | #3460 / #29184 | 0.510 / 0.463 | 0.540 | 0.007 / 0.598 | 不足 |
| low_1 | #16852 / #21724 | -0.553 / 0.019 | -0.245 | 1.328 / 7.050 | 足够 |
| low_2 | #6289 / #21724 | -0.301 / 0.050 | -0.258 | 2.469 / 7.389 | 足够 |
| low_3 | #24752 / #25782 | -0.289 / 0.583 | -0.247 | 0.557 / 0.896 | 足够 |
| low_4 | #3759 / #16572 | -0.281 / 0.139 | -0.039 | 0.740 / 2.706 | 不足 |
| low_5 | #19695 / #20161 | -0.254 / 0.453 | -0.406 | 1.217 / 2.441 | 足够 |

最清楚的低相似例是 **#16852／#21724**：DEV φ=−0.553，幅值cosine=0.019；CONF φ=−0.245，留一场景仍为负。严格去掉同时含两成员的token后，两边分别有750和95位置、覆盖16和10场景；跨这两个不交集合的token配对中，**95.09%进入完全相同的expert组合**。另一对#6289／#21724的DEV幅值cosine=0.050，对应比例91.58%。四个具足够独有token支持的低φ对，其完全相同组合比例为91.58%–99.80%。这些笛卡尔配对不是独立样本量，未据此做二项检验。[不同token重合表](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/results/different_token_route_overlap.csv)

在“低相似应有硬专家分离”这一工作标准下，这是当前读取位置的实际不足。**权重不是完全不区分**：上述第一对硬TV1.328个百分点、gateTV7.050个百分点；排除同token后的TV约0.646和7.827个百分点。部分区分体现在同一expert对之间的连续权重中。9对共享成员和场景，不将这些点当9次独立架构实验；权重差也未排除类别／频率等解释。

更强的“同token中的不相似feature必须各自去不同expert”要求，当前架构没有直接接口：第一低φ对仍在83个CONF位置共同激活；这些位置的两个成员随同一个h送入同一expert集合。不能在同一次token路由里分别给它们独立专家。这个粒度限制不排除expert内部对输入分量有不同功能利用，也不等于已经测出梯度冲突。

左图是DEV固定9对端点对应的原始接收富集，全部53候选和所有观察坐标在全表中。expert6一列为0，因为全接收使P(feature｜expert6)=输入频率，属于恒等。expert7出现较大正负差，但入选和未入选侧的跨场景支持不足。**八条件均无满足预定支持的专家对照，富集p检验没有运行；这与“运行后无显著”不同。** 候选及逐类别表保留2000整场景原始差值区间和不合格原因，不用区间替代缺失对照。[candidate_enrichment](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/results/candidate_enrichment.csv)、[within_label](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/results/candidate_within_label.csv)

## 结果分析三：专家之间的差别主要受少数上下文支配

![专家输入重叠与覆盖](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/figures/03_input_overlap_and_support.png)

左图直接数不同token输入集合。expert1的1129条输入**全部也进入expert6**，expert1独有0，expert6另有23；共同接收率相对expert1为100%、相对expert6为98.00%。这不是两个expert从不同样本中发现了相似语义，而是它们接收了相同token。

中图独立核实：23个主冒号例外中，22来自N029、1来自N051的fork。右图逐一移除16场景：去掉catalogue_recovery后expert7只剩1位置，去掉annotation_boundary剩22，其余均23。移除N029／N051两个家族后，剩1104位置都走{1,6}，全部9对成员的硬路由TV变为0；这是同一输入选择的恒等敏感性结果，不能另立为“更好”的主样本或证明无结构。权重差仍保留，不因硬编号相同自动归零。

因此这些固定读取位置中观察到的少量硬编号差异，不能支持稳定的跨场景feature分工。当前缓存的绝对读取索引仍随前缀长度变化，S15条件长度层曾合并；这轮没有宣称已排除长度。正文末token本身也全为ID624，不是随机普通正文位置；其主专家对变为{4,7}，正文还沿用冒号参考频率/角色，单独报告不混作原生确认。[全部28对重叠](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/results/expert_overlap.csv)、[留一场景与家族](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/results/leave_one_scene_and_family.csv)、[真实token身份](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/results/position_token_inventory.csv)

## 稳定搭配：输入里确有避开关系，不能归给expert

对固定9对额外完成了一个**输入共激活零模型**：在每个场景×类别的3家族块内作Curveball换边，保持每个位置恰32成员、每个坐标在各块出现次数不变。4链共1000抽样，端点行列约束独立复算通过，非退化候选Rhat约1.00。此参照不保留具体家族跨标签的完整耦合，不能当成排除所有模板因素或真实模型干预。

5个低φ对的共激活均低于该参照，按计划10项（含未补齐一项）校正，4项约p=0.010、另一项约0.030。它们不是仅凭单成员频率、Top32和场景/类别边际就必然出现的随机搭配。low_4的整体φ在留一场景时可跨0，稳定性较弱。3个高φ对在这个强条件参照下共现数完全固定，无法检验；剩一高φ对p≈0.285，不支持额外共现。

这说明**可测输入组织与硬路由缺乏分离可以并存**。本轮没有继续检验近乎全接收expert的“专属搭配”；输入避开关系不等于专家机制、功能协作或学习干扰。[输入搭配参照全表](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/results/input_pair_coactivation_null.csv)

## 认识更新：哪里不足，哪里尚不能判坏

| 判断层级 | 本轮可以说什么 | 不能跨过的边界 |
| --- | --- | --- |
| 按用户的激活组织准则评估 | 这些末层标点读取位置中，低相似成员通常仍进入同一专家对；硬输入划分粒度不足，部分区分由gate权重承载 | 不推广成整个模型/所有层无路由结构 |
| 架构可表达性 | 原生expert接收整个h，无法直接将同token的SAE子成员分别硬路由；当前LM/负载目标也未显式优化该准则 | expert可在内部不同利用同一h；没有证明独立feature路由一定更优 |
| 共同接触与选择性 | 专家接收高低参考频率、共享和偏向成员的混合，主要expert画像跟随输入总体 | 混合本身不等于错误；无合格反侧支持，选择性不足以裁定 |
| 功能干扰与效率 | 本轮没有损失、梯度、消融或训练对照 | 不声称高频压制低频、长尾学坏或效率下降 |

**唯一下一步AI建议**是批准一轮同模型同层的既有DCLM普通正文位置测量，改进输入支持域；不直接训练正则项。已有6000条自然文本缓存可用，但旧冒号参考不能自动替代新位置频率，也不能给自然文本强贴粗细类角色。具体768文档、1536位置、DEV/评估/参考隔离、资源与停止条件见[待审批配置](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/next_measurement_proposal_cn.md)，当前NOT RUN。

## 完成范围与复核入口

本轮完成8条件全组成、频率/角色交叉、双向概率、候选区间、28对expert重叠、共同/独有部分、场景/家族敏感性、9对激活—路由、保持Top32及边际的输入搭配参照、真实案例和独立复算。49,008行完整成员表中48,232行是实际观察成员，776行是额外保留的缺失候选；缺失分母留NA。独立复算256个频率均值、全部224条expert重叠、实际观察成员/富集、例外与输入null，最大误差3.33e−16；补充不同token重合率独立误差0。仅CPU，源缓存和冻结代码摘要不变。

未完成的是缺少识别条件的专家富集／专属搭配检验、普通正文新位置测量与任何功能训练实验；它们没有被删去或算作“未显著”。模型无关合成矩阵的无关联／植入关联／全选expert／全活跃成员检查通过，只证明代码性质，不是模型结果。

[详细证据与字段](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/detailed_cn.md) · [实际文本／反例／不可判定案例](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/casebook_cn.md) · [全观察成员](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/results/all_observed_feature_expert.csv) · [完整交付入口](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/README_cn.md) · [独立复算](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/evidence/verification.json) · [补充复算](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/evidence/addendum_verification.json)
