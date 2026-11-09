# S16：餐具权重的独立新场景复核与分析结构

**复核已完成，但结果为“覆盖及行为不足，未能确认复现”。** 新显式文本的描述性成员组权重距离为1.808个百分点，条件置换均值1.923，p=0.4859；更关键的是，固定成员覆盖没有达到预定要求，叉子二选一正确率34/48也低于0.75。因此既不能写“复现成功”，也不能写“已经证明不存在路由结构”。

当前用户明确要求执行独立新场景复核。本轮新建24场景×2家族×2类别×2表达=192前缀，只读同一33B训练token MoE和匹配SAE。输入、成员、方向、全部主统计／复算代码与协议均在新模型响应前冻结，未训练、改权重、干预路由或提交GPU作业。旧S15结果保留，新增S16支持记录，不创建新Focus或Anchor。科学接纳Unknown。

## 三条阅读路径

| 路径 | 本轮核查什么 | 实际结果 |
| --- | --- | --- |
| 行为与控制 | 二选一任务是否有效；精确配对长度；类别负载和长度分层块置换；原候选能否复现 | spoon两表达均48/48；fork均34/48不达门槛。A/B同家族同表达长度严格相等；场景长度两层14/10，未退化为单层。条件p显式0.4859、改写0.0946 |
| 表示与组织 | 原3枚spoon偏向、5枚fork偏向成员在新场景的出现和路由统计 | 显式合格0/3、1/5；改写1/3、1/5。全部192token实际专家集合均为{1,6}；可观察权重差异，但固定成员支持不足 |
| 功能与测量质量 | hook、原生router、答案因果掩码、SAE重建和CPU复算是否可信 | 全192router与SAE编码及两个表达的主统计／区间／p复算PASS；重建NMSE约0.222–0.224。没有消融、替换或学习实验，功能与学习收益仍未知 |

## 图一：同一个向量的两条观测支路

![本轮分析结构示意](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/figures/01_analysis_structure.png)

图一是计算示意，不是机制证据。先把文本送入冻结8层MoE，在最后一层、末尾`Description:`的冒号位置取实际router输入h，1024维。**SAE和router并行观察同一个h。** SAE给出30000维字典中32个正活跃坐标；router给出整个token实际入选的两个expert及其权重。SAE没有给router下指令，也没有把feature单独送往不同expert。

本轮仅追踪S15事先确定的spoon偏向[8934,17384,23973]和fork偏向[7438,15113,21724,25048,26926]。原先“共享”定义是开发侧同家族两类交集的高出现率；“偏向”是开发侧出现率差，不是独占语义标签。两种性质原本容许重叠，不能把它们想成先验互斥模块。本轮没有重新选共享／偏向成员，也没有新增其他类别。

旧S15三个问题的区别仍是：Q1在同类别内比“某成员出现时的expert分布”与类别总体负载；Q2比同一共享成员在两类中的分布；Q3比两侧不同偏向成员组的分布。本轮复核只冻结餐具的**Q3实际权重版**，不再从24或192个结果中挑更好的一个。

## 图二：怎样从feature出现算到一个路由距离

![新显式文本的类别基准与成员条件均值](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/figures/04_category_baseline.png)

对某个固定成员，先找出它在哪些目标类别文本的末冒号上活跃，再对这些token的实际8维gate权重取均值。这给出该成员“伴随怎样的token路由”的分布。对三枚spoon成员各取一个分布、等权平均；对五枚fork成员同样做，再比较两组。

设每个token的8维权重为w，某成员活跃为a=1，其类别内条件均值为p。主指标是两组概率分布的总变差距离：

$$
p_{f,c}=\operatorname{mean}_{t:\,c(t)=c,\,a_f(t)=1}w(t),\qquad
D=rac12\sum_{e=0}^7\left|ar p_{A,e}-ar p_{B,e}
ight|.
$$

这次A侧三枚、B侧五枚等权；不是将所有活跃feature行混在一起按频率重复计数。若某成员完全未出现则留NA，不能当成零路由。重采样某副本缺失成员时按冻结规则在有观测成员上取均值，并记录有效数；覆盖不足时，区间不能代表整个固定成员组已被充分测量。

图二只画expert6，因新数据全部选择{1,6}，expert1承接余下权重。蓝柱为同类别所有48token的均值，橙柱为固定成员的条件组均值。显式spoon为62.694%→63.581%，fork为64.278%→65.390%。两类别总体本来就相差1.584个百分点，成员组相差1.808个百分点；扣掉类别基准后的半L1残差仅0.224个百分点。残差不是两个概率分布的TV，也不替代主检验。

图中两侧都进入同一专家组合，不能单凭“共用expert”判断正确或错误。柱图中的差别大部分与类别总体差别同方向；是否还有超过类别负载的成员关联，要看下一步条件参照。

## 图三：实际结果与保留负载的随机参照

![旧候选和新场景的权重距离](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/figures/02_replication_contrast.png)

蓝点是组间距离，线是2000次整场景bootstrap的原始TV百分位95%区间；橙菱形是条件置换均值。空心表示覆盖或行为不合格，不表示零效应。

| 条件 | 成员组TV（百分点）及95%区间 | 条件null均值 | 超出null均值 | 条件p | 资格 |
| --- | ---: | ---: | ---: | ---: | --- |
| 旧S15探索 | 6.511 [5.017, 8.169] | 4.387 | 2.124 | 0.001，局部Holm8=0.008；全192校正=0.192 | 原候选，非独立确认 |
| 新场景显式（唯一主比较） | 1.808 [0.289, 3.757] | 1.923 | -0.115 | 0.4859 | 覆盖及行为不足 |
| 新场景保留类别名改写（次要） | 3.738 [1.985, 5.108] | 1.928 | 1.810 | 0.0946 | 覆盖及行为不足 |

条件参照保留类别、表达和读取位置，将**整份真实expert对及权重记录**在可交换场景／家族块间重新配对；feature出现记录不改。9999次置换保留类别负载、expert共现及一个token的完整路由，检验观察是否超出这种负载与块结构。不能单独打乱同token里的每个feature，否则会制造原模型没有做过的独立分发。

这次按模型响应前的场景平均长度中位数分两层，实际14/10簇，每层均足够，未合并。A/B配对长度精确相同，条件置换还粗分层匹配上下文长度。两者能改善长度控制，但不能排除词面、场景意义、同作者或共同后缀。

显式观察1.808低于null均值1.923，p=0.4859；改写3.738、null1.928，p=0.0946。对两表达补充Holm校正为0.4859／0.1892；改写不挽救主条件。原始距离区间下界大于0也不能宣称超过null，因为零模型本身通常产生非零距离。新旧输入分布不同，点估计改变不能写成同分布下已证明效应下降。

另外，旧S15频率匹配随机成员组的缺口仍未修复；本轮没有放宽匹配门槛或另挑可用成员。因此不能声称超出所有同频率成员组的表现。

## 图四：为什么本轮首先判为证据不足

![固定成员的新场景覆盖](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/figures/03_member_coverage.png)

左图是每个固定成员在目标类别的48家族中出现几次，右图是覆盖多少个独立构造场景。蓝圆为显式，橙方为改写。虚线12是各自门槛，只有两边都达到才填实；每个组至少80%成员合格。

| 固定成员 | 显式：家族／场景 | 改写：家族／场景 |
| --- | ---: | ---: |
| spoon #8934 | 12／9 | 17／12 ✓ |
| spoon #17384 | 7／6 | 6／5 |
| spoon #23973 | 1／1 | 1／1 |
| fork #7438 | 21／16 ✓ | 17／15 ✓ |
| fork #15113 | 12／9 | 15／10 |
| fork #21724 | 1／1 | 5／5 |
| fork #25048 | 12／10 | 9／7 |
| fork #26926 | 10／9 | 9／8 |

例如spoon #23973只在1/48家族、1/24场景出现，却按原定义占三成员组的三分之一权重。不能凭这个估计说整个spoon成员组已有稳定分布。#8934显式虽然出现12次，却只覆盖9场景，也不合格。显式spoon组0/3合格、fork1/5；改写1/3、1/5，全部低于80%要求。



需同时保留的观察是：出现率差的方向在显式条件7/8与旧偏向一致、1个并列，改写为8/8同向。这是从已有计数事后导出的描述表，没有重新选成员或加显著性检验；小幅同向不等于强度或语义复现。**覆盖不足不能读成所有成员的类别偏向消失。** 见[出现率方向表](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/results/member_presence_transfer.csv)。

行为资格也失败：完整` spoon.`／` fork.`两token答案序列评分中，spoon两表达均48/48，fork均34/48=70.83%，低于75%。所有文本保留，未剔除错误样本后重算“通过”。这只检查显式类别名能否被任务读出，不证明无类别名概念能力。

工具本身没有出现明显接口失配：末层norm2与router输入完全相同，全部192个CPU router及SAE正Top32集合复算一致；平均重建相对平方误差显式0.2241、改写0.2225，重建输入的Top2集合一致率96.875%／98.958%。这些指标检查接线及部分信息保真，不能挽救所选八成员的跨场景覆盖，更不能证明其语义固定。

## 从一个真实输入看计数对象

冻结首个家族输入为：`During the evening stock count, a spoon was placed in an empty drawer. The clerk recorded the object before closing the drawer.`，下一行固定`Description:`。对照只把spoon换成fork，两侧均27token，读取零起索引26的冒号。

spoon实际权重expert6=0.637325、expert1=0.362675；fork为0.655940／0.344060。spoon上#8934活跃，fork上#7438/#15113/#25048活跃；它们各自承接相应token的同一份路由。**这对文本可以说明如何记录，不能替代跨48家族、逐成员等权的统计。** [完整实际输入、八成员值与原始行号](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/actual_cases_cn.md)。

## 交付、状态和待判断的断点

采集192prefix（384候选答案序列及有界校准），既有本机MIG耗时9.85秒、峰值2.207GiB。独立CPU复算全部192router、全部192SAE编码、两表达点估计／方向／区间及9999置换p均通过，冻结源码与原模型／SAE全文件摘要保持一致。没有训练、权重输出、路由操作、资源申请或发布。

| 项目 | 状态 | 证据 |
| --- | --- | --- |
| 新文本、24场景、配对长度与旧文本近重复核查 | DONE_VALID | [data_preflight](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/evidence/data_preflight.json)、[全部文本](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/data/panel.jsonl)；最大旧文4-gram Jaccard=0.05，无标签掩码精确重复 |
| 原成员／方向／主代码预响应冻结 | DONE_VALID | [freeze](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/evidence/freeze.json)、[协议](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/protocol.md) |
| 原生路由与行为采集、固定统计、独立复算 | DONE_VALID | [inference](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/evidence/inference_complete.json)、[结果CSV](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/results/replication.csv)、[verification](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/evidence/verification.json) |
| 固定组跨场景覆盖与行为资格 | INVALID_FOR_CONFIRMATORY_CLAIM | [逐成员](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/results/member_expert.csv)、[行为](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/results/behavior.csv)；按预定标准不足 |
| 独立复现成立 | INSUFFICIENT | 不能把描述性p或同方向当作完整复现 |
| 频率匹配支持域、自然来源泛化、功能与学习收益 | BLOCKED_OR_NOT_RUN | 旧匹配不足；新文本为同作者构造；未干预或训练 |

这里完成的是新场景测量与复算，**没有完成“该路由结构稳定且有学习价值”的证明**。AI对断点的定位是：旧固定成员在这些新场景上支持不足，任务行为也未全过门槛；这不同于仅仅一次p没过。机制判断、是否调整测量对象及下一实验由研究者确认，不自动补样、重选feature或进入训练。

[详细配置与复算入口](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/detailed_cn.md) · [全部原始逐位置表](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/results/token_routes.csv) · [完整结果](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/results/replication.csv) · [图证据来源](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/figure_lineage.md) · [产物清单](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/artifact_manifest.json)
