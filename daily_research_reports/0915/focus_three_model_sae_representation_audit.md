# SAE 的新增重构梯度，是否让预训练中的领域结构更容易形成？

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: three_model_sae_representation_audit
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: ELIGIBLE_RESULT_AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
cycle_start: 2026-09-15
target_meeting: 2026-09-16
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E01_three_model_sae_representation_audit/protocol.md
core_experiment_count: 1
```

2026-09-16 按研究者要求重写。已有审计完成；知识解释与后继建议仍由研究者裁定。本次不改变 problem_key、项目归属、已执行协议或科学状态。

阅读入口：[组会四段式报告](../0916/focus_meeting_sae_representation_update_cn.md)；[数据、方法、公平性及后继方案](../0916/sae_representation_followup/01_result_explanation_and_next_plan_cn.md)。正式结果仍由 [Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E01_three_model_sae_representation_audit/summary_cn.md) 和 [Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E01_three_model_sae_representation_audit/detailed.md) 所有。

## 核心问题与当前认识

语言模型从随机初始化预训练时，领域相关的信息能否逐渐被读出；加入 SAE 后，尤其让额外重构损失更新上游主干后，这个过程是否改变？**本轮已执行的可检验部分是三个既有模型在共同训练进度上的表征差异，不是从零配对训练的单变量因果检验。**

旧版 M1 和新版 M2 都在最后一层 MLP 前串联一个连续训练的 SAE，语言损失一直经过 SAE 反传。M1 只在额外的抽样重构分支上切断输入梯度；M2 打开这条输入梯度，并另外加入只直接训练 SAE 的防死特征损失 AuxK。不能把 M1 写成“语言梯度也断开”，不能把 M2−M1 写成纯粹的一个开关差异。

**AI 知识更新：**领域读出与稀疏使用确实随训练改变；旧版的一部分细领域几何差异在去第一方向后保留。但新版没有获得跨位置、跨面板的一致读出优势，重构更好也没有自动变成领域可读性更好。因此，“梯度接通”已核实，“促进语义形成”仍未知。命题等价不是本轮主结论，不能由领域激活图代替证明。

## 本轮唯一实验：既有三模型 0–10B 表征审计

**目的。** 分清上游原始表征、实际送入 MLP 的重构、SAE 激活和局部梯度各自改变了什么，排除仅由首个主导方向造成差异的解释。

**假设。** 如果训练配置改变了领域组织，固定文本上的配对差异应在同一表征与指标中沿训练进度持续出现，并在去第一方向后至少部分保留。最强竞争解释是词面规律、重构造成的几何重排、单一共同方向以及局部统计波动。

**分析方法。** 三模型共同快照使用同一短句面板和自然学术文本面板，分别读取 SAE 前原始状态与实际 MLP 输入；比较线性读出、父领域内部的细领域分离、稀疏贡献和损失梯度。原始分析与仅用拟合数据确定的中心化／去第一方向分析分开，模型差值共享重采样单元。具体数值与实现以既有 Protocol 为准。

**预注册结果分支。** 同一测量对象上的连续差异通过去方向检查，支持有边界的可访问结构差异；差异不分离或去方向后消失，则不支持该优势；身份、样本、抽取位置或统计资格失败则证据不足。任何分支均不自动证明语言模型使用该结构或辅助梯度带来因果收益。

## 滚动轮次摘要

| 轮次 | 证据与认识更新 | 边界与下一决策 |
|---|---|---|
| A15_17_E01，2026-09-16 | 全矩阵及不可变性审计通过。M1 实际输入的细领域 Fisher 轨迹在去方向后保留；读出优势取决于训练点和测量对象。完整数值、工程重试与资格仅见 Detailed。 | 新版梯度有非零上游作用，但没有一致领域优势；M2 同时改变 AuxK，因果归属未知。待研究者决定是否进入下述同状态最小验证。 |

## 当前唯一下一决策

**AI 建议，待批准：**是否进入“同一个 M2 10B 状态、冻结 SAE、只改变主干是否接收重构梯度”的最小局部验证？先定位梯度，再在隔离副本中比较一次真实参数更新后的留出读出变化。选择共同终点是为核查当前配置，不按最漂亮的差异挑点。

这一建议针对研究者此次强调的“新增梯度是否有帮助”，区别于旧 Summary 提名 M1 3B 来问“模型是否使用已有几何”。两者是不同问题；本次优先建议前者，不把旧建议改写成研究者决定。实施范围、指标、停止条件与预算见后继方案的决策卡；任何新 GPU 计算、参数微步、从零小模型训练均未在本次启动。

**完成条件：**研究者确认或修正本次有界认识，并裁定该局部验证是否值得进行。若进入，另行形成批准的实验契约；不以本 Focus 或工作记忆代替批准。小模型旁路已有工程 Smoke，可以复用，但不自动升级为长期训练授权。
