# 旁路稀疏约束是否改变主干语义关系的组织与使用？

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: three_model_sae_representation_audit
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: NOT_AVAILABLE
cycle_start: 2026-09-20
target_meeting: Unknown
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E06_21b_sidecar_representation_audit/protocol.md
secondary_protocols: A15_17_E07_15b_sidecar_persistence_audit, A15_17_E08_0_10b_sidecar_early_trajectory
core_experiment_count: 3
```

2026-09-20 研究者确认这轮归入现有 A15_17 并授权修订当前设计，指定精确 21B 的 Dense、原版 SALL、重加权 S7 三模型；P、N8、PAWS 每个面板都看最后正文词元与正文均值。研究者委托 Codex 严格判定受控模板语义，要求四卡 5090 Spot smoke 通过后实测估时并提交正式任务。旧 E01/E03/E05 的事实仍由各自结果记录拥有，不因这轮设计改变。

## 1. 核心问题与边界

总问题是：训练时加一个旁路稀疏重构约束，能否让主干把同一层意思在不同说法、不同语境中组织成更稳定、更容易取用的关系，并最终被模型用于预测；还是只改变了向量大小、同类聚散、表面线索或字典的读法？这不是为某个模型设立的胜负题。旁路稀疏自编码器（SAE）的重构不进入语言模型正常推理路径，因此本轮先检验较小、可判决的一环：在同样 21B 训练词元与相同输入上，原版八层旁路 SALL 相对 Dense 的原始注意力写入，能否让未见实体和改写中的关系方向更容易被简单读出？第8层重加权单旁路 S7 仅作分叉终点诊断，不是同剂量随机对照。

这里暂把“更好的组织”限定为：不靠词面模板，在未见例子上保留关系区别并让简单读法更稳定；这不是“好表征”的完整定义。“更容易读出”只指冻结写入向量上的固定容量线性探针表现，不自动表示模型实际使用该信息、自然语言语义整体更好、容量提高或持续学习改善。领域组织仍用 N8 审核，PAWS 补自然句对语义；三个面板不合成一个总分。语言损失与既有能力结果是成本和行为护栏，不能用排名替代表征结论。

**本轮不回答：**不同主干训练种子上的因果平均效应、离线字典公平训练、不同 K 的公平训练比较，以及功能干预收益。

## 2. 可证伪预测与最强竞争解释

若旁路使可复用语义组织更可读，SALL 的原始写入在受控关系的实体与表达双留出上应优于 Dense，且不能只靠长度、词袋、模板或共同幅度解释；N8 与 PAWS 给出适用范围而非替代主指标。最强竞争解释是旁路主要改变向量尺度、类内压缩、模板/编号线索或 SAE 观察器的重构方式，原始写入并无可泛化优势。读出改善但原生任务没有相应变化时，只能承认可读性，不能称模型已使用。

## 3. 允许与禁止的信息

固定输入与来源组跨三模型一致。拟合集可学习探针和 fit-only 变换；开发集可选正则化和最多一个补查层；确认集标签、来源组与逐题成绩不能进入模板修订、层选择、阈值选择或模型取舍。P 的 AI 语义审核与版本修订在任何新模型结果前完成并留痕，不能把它写成独立人工审核。N8 的发布配置是领域标签，不是逐词元语义真值；PAWS 的标签属于句对，不属于单句。

## 4. 主实验：冻结 21B 三模型的配对写入审计

- **目的：** 找出旁路相关变化位于原始主干写入还是只位于 SAE 的读法，并判定它是否超出简单尺度、共同方向与词面/模板解释。
- **假设：** 如果主干组织确有改善，同输入、同层、同读点的跨实体与改写双留出线性读出应出现稳健的 SALL−Dense 正差；否则即使几何或字典重构改变，也不能称关系可读性改善。
- **分析方法：**

  1. 三模型逐层读取投影后、残差相加前的注意力写入；每个数据集同时计算末位和正文均值，并用范数、谱及相似结构的诊断定位变化，防止把尺度或共同方向当语义。
  2. 用受控关系正反例和未见实体/表达检查简单读出，另用自然领域与高词汇重叠句对限定它在何种语义对象上成立；所有模型共享来源分组与确认样本。
  3. 只有原始写入出现有资格的候选后，再对同一输入分开检查在线 SAE 的激活、重构和误差，保留语言损失与既有行为结果的不利证据。
- **结论（执行前分支）：**
  - **若支持：** 仅能说此训练实例在该受控关系和读点上有更好的跨表达线性可读性；是否设计选择性功能干预是下一决策。
  - **若不支持：** 若原始写入不改善而只有范数、类内压缩或 SAE 读法改变，停止把该旁路称为已改善可复用关系语义，转向最小瓶颈定位。
  - **若证据不足：** 数据语义、来源隔离、取点、模型身份、探针收敛或确认样本地板/天花板失效时，不选胜者，只修复那个具体闸门。

→ [本轮 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E06_21b_sidecar_representation_audit/protocol.md)

## 4.1 补充实验：15B 同谱系持续性审计（E07）

- **目的：** 检查主对照 Dense 与原版 SALL 的注意力原始写入差异在较早的 15B 是否已有同方向迹象，而不让 15B 改写 21B 主判据。
- **假设：** 若 21B 的跨表达可读性并非孤立终点，15B 在相同数据、取点、汇聚和简单读出下可显示可比较的模式；相反，差异也可能仅在后期出现、反向或受尺度/模板驱动。
- **分析方法：** 同一冻结面板上，依次对两模型做本地取点 Smoke；正式任务复用八层轻扫、第4/8层双汇聚读出、结构/CKA、在线观察器与语言代价，15B 结果只作持续性描述，并保留不利方向。
- **结论（执行前分支）：** 若模式同向，支持“此实例较早可见”的有限描述；若不同向，报告时间异质性，不否定或补救 21B 主结果；身份、来源或数据闸门失效则只报证据不足。

→ [E07 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E07_15b_sidecar_persistence_audit/protocol.md)

## 4.2 补充实验：0–10B 真实共同点早期轨迹（E08）

- **目的：** 确认早期写入和在线 SAE 观察变化出现于何时，并检查 15B/21B 端点是否可能只是特殊取点；它不重新定义主语义问题。
- **假设：** 若旁路相关结构和可读性变化有时间过程，真实共同词元点上的配对差值应能显示阶段性变化；竞争解释是初始化差异、尺度、训练续接分叉或词面线索。
- **分析方法：** 先核实 Dense/SALL 在 0、0.5、1、3、5、10B 的完整 checkpoint 和续接谱系；每个点使用同一 P/N8 输入、双汇聚与第4/8层线性读出，八层轻扫与配对结构诊断，不把 PAWS/所有后续方法乘满六点。
- **结论（执行前分支）：** 可描述同一实例的早期轨迹及与 15B 的关系；若差值不稳定或源于分叉/表面线索，不能称持续的语义改进；缺少精确共同点、加载或配对闸门时该点不足，不插值凑齐。

→ [E08 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E08_0_10b_sidecar_early_trajectory/protocol.md)

## 5. 轮次滚动摘要

| 日期（UTC） | 本轮问题 | 结果或 `NOT RUN` | 认识更新 |
|---|---|---|---|
| 2026-09-16，E01 | 旧串联 SAE 三模型 0–10B | 已记录于 E01 Detailed | 旧串联与本轮旁路不同，保留历史边界。 |
| 2026-09-17，E03 | 早期旁路几何与局部梯度 | 已记录于 E03 原结果 | 近 90° 不能称特殊正交机制。 |
| 2026-09-18，E05 | 五模型精确 0–10B | 已记录于 [E05 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E05_multimodel_fisher_gradient_coefficient_audit/summary_cn.md) | 几何/读出有局部正差，Dense 终点异常和旁路 NLL 不利限制了泛化。 |
| 2026-09-20，E06 | 21B 三模型双汇聚 | `NOT RUN`（无正式结果） | 本地取点 Smoke 不构成机制更新；主确认仍待正式输出。 |
| 2026-09-20，E07 | 15B 主对照持续性 | `NOT RUN`（无正式结果） | 仅工程闸门通过；15B 不替换 21B 主判断。 |
| 2026-09-20，E08 | 0–10B 早期共同点 | `NOT RUN`（无正式结果） | 仅工程闸门通过；早期差值及续接影响仍未知。 |

## 6. 待研究者决定

目前没有额外科学方向裁定要请求；新数据版本、执行范围及结果解释必须遵守本轮 Protocol。若正式结果出现，研究者仍负责最终机制判断。

## 7. 本轮总结论（研究者审计后填写）

- **我的认识更新：** `NOT AVAILABLE`。
- **仍不能说：** `NOT AVAILABLE`。
- **唯一下一决策：** 在本轮合格结果出来后，决定是否值得设计少量选择性功能干预；若主指标未显示原始写入优势，先停止此方向的干预扩张。
