# 冻结基础模型的语义能否启动先粗后细的功能路由？

```text
type: meeting_cycle_core_task
status: CYCLE_CLOSED
problem_key: A15.semantic_supervision_middle_layer_separability
focus_role: PRIMARY
conversation_owner: codex-thread:01a0508f-34cb-7d20-bda8-d9271307c0a6
ownership_status: RELEASED
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
data_definition: HUMAN_CONFIRMED
cycle_start: 2026-08-28
target_meeting: 2026-09-01
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_02_frozen_base_staged_semantic_lora_router_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E05_clinc150_frozen_base_staged_semantic_lora_router/protocol.md
source_meeting: daily_research_reports/backup/2026/08/0831/docs/0831_组会校订_训练阶段澄清与Post-training研究重定向.md
core_experiment_count: 3
execution_status: E05_FULL_RUN_AND_ANALYSIS_COMPLETE
interpretation_status: HUMAN_CONFIRMED_BOUNDARY_AND_NEXT_DECISION
```

## 1. 核心问题

冻结 Qwen3-0.6B-Base 后，能否直接从它已有的自然语言表示中找到粗领域和领域内细意图，并用这些固定标签先训练粗 Router 与粗 LoRA 专家，再固定粗 Router、增加细 Router 与细 LoRA 专家？这种先粗后细的训练，能否比没有语义监督的同结构系统和平铺专家系统，得到更接近真实语义上界的路由、有效表示和任务功能？

本轮用 CLINC150：10 个粗领域，每个领域 15 个细意图。基础模型不再后训练成教师；真实标签只给出 Oracle 上界，三种聚类标签来自冻结基础模型的训练集最终层表示。原始 Qwen 参数始终不变，变化发生在第 15 个块的一组新增低秩残差、Router 和任务分类头中。

## 2. 实验一：粗粒度语义入口

### 1. 目的

先判断真实领域标签能否训练出不坍缩且具有任务作用的粗 Router，再判断冻结基础模型的三种聚类能否给出同方向的粗分发。没有这一步，细分失败无法归因。

### 2. 假设

若架构能接收粗语义，真实领域监督应优于只靠意图任务损失形成的粗路由。若基础模型已有可用语义，至少一种聚类标签应在路由熵、与真实领域的一致程度、任务和粗专家删除效应上向 Oracle 靠近。最强竞争解释是聚类只制造了好看的负载分布，没有自然语言语义和功能。

### 3. 分析方法

1. 在完全冻结的同一 Qwen 表示上，分别固定真实领域标签、球面 K-means、高斯混合和球面方向混合标签；比较它们的稳定性、负载和与真实领域的评价性对齐。
2. 用相同的两轮训练、同一 Router 和粗 LoRA 容量，比较任务损失组、Oracle 和三种聚类组；Route 分类损失只更新 Router，专家只通过意图任务损失更新。
3. 第一眼比较单样本路由熵、专家负载熵和与 Oracle 的差距；选择性专家删除只决定方法是否具有功能，不替代 Oracle 比较。

### 4. 结论

- Oracle 也失败：本轮的层、低秩容量或目标函数不能承载粗语义，后续细分结果只能作诊断。
- Oracle 成功而聚类失败：层级架构可用，瓶颈在冻结基础模型语义的寻找方法。
- 至少一种聚类复现 Oracle 方向并通过功能门：允许解释第二阶段的粗到细传递。

## 3. 实验二：完整粗到细方法与 Baseline

### 1. 目的

检验导师要求的完整操作：先学粗分发，固定粗 Router，再在每个父分区内学习细 Router 和细 LoRA 专家；同时区分后训练、专家容量、语义标签、层级拓扑和固定随机分组的作用。

### 2. 假设

若逐级语义分发有效，真实标签层级组应优于同结构任务损失组；主要自监督层级组应恢复真实标签改善的一部分，并优于平铺自监督、平铺真实标签以外的容量解释。最强竞争解释是 Dense、平铺或打乱标签组获得同等改善。

### 3. 分析方法

1. 完成冻结 Base、Dense LoRA、平铺任务损失、平铺 Oracle、平铺球面聚类、层级任务损失、层级打乱标签、层级 Oracle 和三种层级聚类的两个种子 full run，并保持每个样本的活动低秩 rank 为 24。
2. 粗阶段训练两轮；细阶段从冻结的粗 Router 检查点继续两轮。基础模型和聚类标签始终固定，任务分类头在所有训练组中以同一规则继续更新。
3. 依次比较任务意图宏平均 F1、路由熵与语义一致、有效表示的领域内细意图线性可读性和低尾间隔，最后用专家删除判定是否形成选择性功能。

### 4. 结论

- Oracle 层级不优于同结构任务损失组：停止声称本实现承载导师机制。
- Oracle 有效、自监督无效：保留架构，只诊断语义发现和阶段间标签传递。
- 自监督在两个种子上都向 Oracle 恢复且功能门通过：支持在本数据和单层低秩实现中继续扩展。

## 4. 实验三：固定什么以及细 Router 读取什么

### 1. 目的

用一个完整的 $2\times2$ 消融回答第二阶段的两个具体问题：粗 Router 固定后，粗专家是否还应继续接受任务梯度；细 Router 是否应读取去掉粗 Router 判别行空间的表示。

### 2. 假设

若固定已经建立的粗功能能保护父类分工，同时粗判别方向会干扰父类内部细分，那么“粗 Router 与粗专家都固定 + 细 Router 读取去粗表示”应最好。竞争解释是只需固定分发规则而让粗专家继续适应，或完整原生表示仍包含细分所需信息而优于去粗。

### 3. 分析方法

1. 在 Oracle 和主要球面聚类两种标签来源下，都运行：粗专家继续训练/冻结 × 细 Router 读取原生/去粗表示四个格子；粗 Router 在四格中始终固定。
2. 每个格子比较粗路由是否保持、细路由熵、领域内细意图有效表示、任务性能和选择性专家删除，并记录可训练参数与活动计算量。
3. 只有标签来源的主比较先成立，冻结或去粗差异才解释为机制；否则它们只描述优化行为。

### 4. 结论

- 冻结粗专家更好：保留“固定已学粗功能再学细”的严格实现。
- 只固定粗 Router 更好：保留粗路径，但允许粗专家随细任务继续适应。
- 去粗更好：只支持删除当前 Router 的线性粗判别行空间有帮助，不代表去除了全部粗语义。
- 原生表示更好：放弃当前线性去粗操作，但不否定先粗后细。

## 5. 当前认识与边界

旧 E03 已证明 Qwen3-0.6B 能学会 CLINC150，但“训练教师后验 → 中层层级 Router”相对平铺 Router 的两个种子方向不一致。旧 E04 是合成数据上 Router-only 监督的独立前驱证据；它不能替代本轮真实自然语言验证。本轮取消教师训练，直接审计冻结基础模型表示，并把语义监督限制在 Router，把专家学习限制在任务损失。

即使结果为正，也不能声称聚类发现了开放世界全部语义、原始 Qwen 参数被塑造、方法改善开放式生成、在线动态标签已成立或能够直接迁移到 MASSIVE。CLINC150 的任务输出就是意图分类，因此它首先是层级路由机制实验。

**唯一下一决策：**完成 E05 全部 32 个最终条件和两个种子的 full run 后，根据 Oracle 上界、自监督 Oracle 恢复、选择性功能门和 $2\times2$ 消融，决定进入 MASSIVE 的领域—意图—槽位扩展，还是回到合成数据逐层定位失败原因。

## 6. 执行完成后的机器证据（等待研究者闭卷确认）

32/32 个最终条件、12 个第一阶段检查点和四份父专家删除效用均已完成。注册判据给出的机器结论是 `INSUFFICIENT_ORACLE`：Oracle 相对同结构任务损失组的领域内细意图线性探针提升为两个种子 `+0.289/+0.093` 个 F1 点，合并均值 `+0.191`，但 95% 区间 `[-0.0003,+0.3866]` 仍跨零；球面聚类组提升 `+0.039/+0.093`，合并区间也跨零。

当前最稳妥的直接观察是：真实标签与聚类标签都能避免任务损失路由的坍缩，并产生为正的父专家选择性删除效用；但有效表征的细意图线性可读性、近邻正确率和类内/类间散布几乎没有变化。细专家残差远小于共享残差，是当前未形成细语义表征改善的主要机制线索。$2\times2$ 消融没有支持“冻结粗专家并对细 Router 去粗”是最佳格子。

这些文字是 AI 对机器证据的草案，不替代研究者的闭卷结果、不能声称边界和唯一下一决策。候选决策是先做 MASSIVE 英语的领域—意图—槽位机制审计；若 Oracle 在非饱和的槽位指标上仍失败，或细残差继续接近零，再回合成数据从目标函数和梯度路径逐层诊断。

## 7. 证据入口

- **会议来源：**[0831 训练阶段澄清](../0831/docs/0831_组会校订_训练阶段澄清与Post-training研究重定向.md)
- **Anchor：**[A15.13.02 Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_02_frozen_base_staged_semantic_lora_router_anchor.md)
- **E05 Protocol：**[A15.13 E05 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E05_clinc150_frozen_base_staged_semantic_lora_router/protocol.md)
- **E05 Summary：**[A15.13 E05 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E05_clinc150_frozen_base_staged_semantic_lora_router/summary.md)
- **E05 Detailed：**[A15.13 E05 Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E05_clinc150_frozen_base_staged_semantic_lora_router/detailed.md)
- **历史 E03：**[Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E03_qwen06b_clinc150_one_layer_backward_hierarchical_router/summary.md)
- **历史 E04：**[Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E04_frozen_teacher_route_only_dynamic_expert_tree/protocol.md)
