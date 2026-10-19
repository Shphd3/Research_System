# 已有专家分工，何时才值得新增专家？

状态：AI_DRAFT_AWAITING_HUMAN_CONFIRMATION。单问题组会讨论稿；不替代正式结果记录，不更新 Focus、Anchor 或 Protocol。按研究者要求不展示 loss 对比图。

阅读附件：[图表来源与结论索引](../../../../../../../Projects/from-attention-to-search/main/research_notes/sae_representation/20260909/evidence_index_cn.md)。本页引用的两张图片、五份精选数据表均已保存于本日目录；源码、原始运行及检查点仍在执行工作区。

## 1. 目的

判断新内容到来时，为什么要增加专家，而不只是继续训练已有专家；并明确 SAE 层级分析能补上哪一段证据。

## 2. 假设

如果已有专家确实承担不同计算，而且继续更新它们无法兼顾新旧内容，新增专家才可能有必要。最强竞争解释是：原来的专家仍能学会新内容，不需要扩容。

## 3. 分析方法

本次术语：SAE指用稀疏自编码器得到原子后生成分组；GMM指用高斯混合模型给输入生成分组概率。两者都只是分组办法，尚不是已确认的语义分类。

- 比较 SAE 和 GMM 两类分组下的两种训练策略：A 预先指定组与专家的对应，B 约束相似输入走近似路线、不同输入适度分开。两者都约束路由，不改变冻结的输入表征。
- 用专家替换检查是否“各有所长”，再检查继续更新旧专家与新增模块的适配结果。SAE 做了前一项，没有进入后面的顺序增量实验。
- 回看已有 SAE 层级证据，区分“节点更专一”“存在语义父子关系”和“这种关系有助于专家分工”。

训练为四个结构方案各三个种子、512次更新，有效批量128；路由、共享分支和专家联合更新，主干与输出头冻结，结构权重从0.01降至0.001。任务对照通过等价性检查后复用。完整设置见[训练协议](../../../../../../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6R1_online_regularized_router_decay/protocol.md)；后续阶段见[验证协议](../../../../../../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6R1_online_regularized_router_decay/post_training_analysis/protocol.md)。

## 4. 结论

### 1）有一个一致方向：约束路由关系，比预先指定对应更好；但收益小

SAE、GMM 各三个种子的六个配对比较全部同向，B 都比 A 好。SAE 的平均答案预测损失差为约0.0047，GMM约0.0034；但 B 相比只按任务训练，都有一个种子反转。因此可以讲“本设置下 B 优于 A”，不能讲“结构约束已经稳定改善任务能力”。

| 分组方法 | B减A的平均预测损失 | B优于A | B优于只按任务训练 |
|---|---:|---:|---:|
| SAE | −0.004724 | 3/3种子 | 2/3种子 |
| GMM | −0.003370 | 3/3种子 | 2/3种子 |

表1怎么读：负数表示B更好；均值给三个训练种子相同权重，单位为每答案词元的自然对数损失。不把大量词元当成独立训练重复。[精确数据表](../../tables/strategy_comparison.csv)

SAE 两种方案都训练过，也都在固定输入的专家替换中出现“不同专家各有所长”；只按任务训练也有这一现象，所以不能归为 SAE 独有的效果。B 不是“让特征本身互斥”，它同时鼓励相似输入共享路线。

| 模型 | 检查的种子数 | 两组输入上的专家优势方向相反、且各自95%区间不跨零 |
|---|---:|---:|
| 只按任务训练 | 3 | 3 |
| SAE-A／SAE-B | 各3 | 各3 |
| GMM-A／GMM-B | 各3 | 各3 |

表2怎么读：每个模型/种子只取发现集排名第一的专家对，不按验证结果重挑；还要求方向与发现集一致。这只是固定干预下的功能差异，不表示这些专家具有已确认语义，也不能比较不同模型的分工程度。[逐模型数据表](../../tables/expert_function_coverage.csv)

证据：[配对比较](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/runs/full-20260909T052900Z/S1/paired_contrasts.csv)、[专家功能干预](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/runs/full-20260909T052900Z/S3/functional_contrasts.csv)。

### 2）还没有确定“何时应该新增专家”

目前的顺序适配运行中，旧专家仍能学习；GMM-B 的自动版本在两次任务到达、三个种子中都选择了旧容量更新，没有永久扩容。这是当前运行观察，不是“新增专家普遍无用”的结论，更不是 SAE 增量实验的结论。

| 种子 | 第一项代码任务到达后 | 第二项代码任务到达后 |
|---|---|---|
| 17 | 更新旧专家 | 更新旧路由 |
| 29 | 更新旧专家 | 更新旧专家 |
| 43 | 更新旧专家 | 更新旧专家 |

表3怎么读：六次真实新任务到达都没有选择新增；控制流不计入这六次。自动版本每次有64条缓冲记录，其中48条更新、16条选择，不能叫16条支持下的自动实验。这里只报告动作，不作公平增长优劣的因果裁决。[动作表](../../tables/automatic_new_arrival_choices.csv)

归因已经具体到三处，而不是笼统说“数据少、模型没训好”：

- 学习冲突检验被分组筛选挡住：只按首个答案位置归组，406条发现记录变成399条在一组、7条在另一组，第二组达不到16条门槛。其他已缓存答案位置能覆盖更多组，但尚不能据计数保证冲突检验成立。
- 局部适配支持过窄：32条目标记录全部是选择题，只有32个答案字母和32个结束符，却要向八类任务的探针泛化。覆盖不匹配是已确认的瓶颈，但尚未证明它解释了全部无收益。
- 顺序适配的处理间，实际重放数据和新增初始化未完全匹配，不能把差异全部归给容量或门控机制。

训练完成、梯度有限，专家干预有作用，故不支持“模型完全没学起来”；但没有更长训练对照，也不能宣称充分收敛。以上归因区分了“为什么本轮不能回答”与“新增为什么无效”，后一个问题仍未解决。

证据：[自动选择](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/runs/full-20260909T052900Z/S6/automatic/selection.csv)、[源码与样本归因审计](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/analysis_reports/20260909_meeting_attribution/attribution_audit.json)。

### 3）SAE 层级是尚未进入当前训练的候选结构，不是已经验证的答案

当前方法是将29,471个保留原子直接分成八组，没有利用父子关系。它不是“只用叶节点”：和旧深度探索图对照，已有181个深度1节点、23个深度2节点和1个深度3节点被分进当前组。**缺少的是利用层级关系，而不只是使用高层原子。**[交叉核验](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/analysis_reports/20260909_meeting_attribution/hierarchy_membership_audit.json)

![已有高层原子进入当前分组](../../figures/hierarchy_membership.png)

图1怎么读：蓝色是已经进入当前分组的原子，灰色是没有进入的原子；深度1、2、3都有蓝色。深度只来自指定旧图，不是模型层号；该图不测激活频率和训练贡献。[对应数据表](../../tables/hierarchy_membership.csv)

旧层级实验提供了可复现的候选结构，但语义验证只覆盖预设九个细类中的两个；更深节点有时更专一，并没有确立“浅层负责粗类、深层负责细类”的角色转换。[旧实验完整结论](../../../../../../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E18_dataset_conditioned_sae_semantic_hierarchy/summary.md)

![旧层级的语义覆盖边界](../../figures/historical_semantic_coverage.png)

图2怎么读：左图只有两个格子通过原定语义检验；右图额外要求原激活关系也跨数据保留，则没有交集。这是历史层级证据的边界，不是本轮路由效果图，也不是对全部 SAE 特征的否定。图片与原文件逐字节一致，原表及变换记录见图表索引。

### 备查：为什么第二组样本不足？

| 分组位置规则 | 组0 | 组1 | 组2 | 组3 | 组4 | 组5 | 组6 | 组7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 仅首答案位置 | 0 | 0 | 7 | 0 | 399 | 0 | 0 | 0 |
| 全部已缓存答案位置 | 9 | 46 | 36 | 73 | 404 | 22 | 49 | 102 |

表4怎么读：每格是发现面板中该组覆盖的唯一记录数。首位置规则只有一组达到16条；第二行的记录可跨组重复，不能相加，也不能据此声称双组支持已合格。这是筛选口径诊断，未重跑学习冲突实验。[计数表](../../tables/screening_position_counts.csv)

## 边界与唯一下一决策

目前能讲的是：**关系约束比固定对应更合适，专家也出现了功能差异；但这些还不足以证明需要新增专家。**本轮总预测指标又主要受数学长答案影响，不能代替广泛生成能力评测。

AI建议的下一决策：是否先做[两阶段离线分析](../../../../../../../Projects/from-attention-to-search/main/research_notes/sae_representation/20260909/sae_offline_two_stage_implementation_plan_cn.md)，先比较叶节点与高层节点，再在同一节点集合上比较真实父子连接与单层／打乱连接，判断是否值得训练层级路由。概念与学长参数见[背景说明](../../../../../../../Projects/from-attention-to-search/main/research_notes/sae_representation/20260909/sae_hierarchy_clustering_todo_cn.md)。

完成标准：固定 SAE 和数据，在独立样本及频率、覆盖匹配后，高层节点或真实父子连接仍提供可解释的额外区分；若优势消失，停止“高层天然更适合父聚类”的主张。

恢复动作：先核定节点类型及关系方向，再比较聚类；不先扩专家，不重新训练 SAE。新一轮正式实验及资源范围另行确认。
