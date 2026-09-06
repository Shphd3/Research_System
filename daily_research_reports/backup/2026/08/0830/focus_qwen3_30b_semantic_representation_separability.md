# Qwen3-30B 的实际 MoE 入口对粗细语义究竟可分到什么程度？

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: A15.qwen3_30b_fixed_fact_expression_separability
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: AWAITING_HUMAN_CONFIRMATION
data_definition: VERIFIED_EXISTING_C4E_C5E_QWEN_CACHE
cycle_start: 2026-08-30
target_meeting: Unknown
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_12_semantic_representation_separability/15_12_semantic_representation_separability_anchor.md
protocols:
  - Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E01_qwen3_30b_fixed_fact_expression_separability/protocol.md
  - Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E02_expression_bank_boundary_coverage_controls/protocol.md
  - Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E03_tax_c4a_unseen_fact_package_transfer/protocol.md
source_meetings:
  - daily_research_reports/backup/2026/08/0828/docs/0828组会_逐句校订与下一步研究方向.md
  - daily_research_reports/backup/2026/08/0829/docs/gradient_consistent_hierarchical_routing_h100/focus_meeting_gradient_consistent_hierarchical_routing_h100.md
core_experiment_count: 3
e03_execution_status: NOT_RUN_RESOURCE_SELECTION_PENDING
e03_resource_status: audited_4x_candidate_waiting_user_confirmation_8x_not_frozen
```

## 1. 核心问题

在固定的 64 个语义事实上，Qwen3-30B-A3B 六个实际 MoE 门输入层中，是否存在跨未见表达模板和跨 C4E→C5E 改写仍稳定的、多粒度线性读出；如果存在，它是仅平均可读，还是对困难样本也保有正几何间隔，并且能否由一个全局 64 类线性读出同时实现粗类和细类分发？

这里不把 C5E 称为“未见事实”，因为 C4E 与 C5E 复用同一组 64 个事实。E01/E02 只审计固定事实的跨表达不变性；E03 只对一个新于探针的事实包、长度和措辞的联合偏移做压力测试，仍不回答一般的未见事实泛化。

## 2. 实验目的

本轮分三个依赖子问题：

1. 分别审计八分类父类、八个“父类已知后的八分类细类”、以及全局 64 分类联合语义是否能由线性 probe 在未见表达上读出；
2. 在平均准确率之外，检查最困难 5% 样本的尺度归一化几何间隔是否仍为正；
3. 若不稳健，定位失败发生在哪一层、哪一粒度、哪些类别对，并报告读出权重的有效秩，而不把 PCA 方差或二维图当作可分性证据。

完成标准是给每个层一个明确的诊断：全粒度表达稳健、平均可读但低尾脆弱、仅部分可读，或证据不足；同时保留所有类别级失败，不允许用宏平均掩盖一个父类中的细类失败。

**本轮不回答：**未见事实泛化、模型原生 Gate 是否使用这些方向、专家效用、语言模型收益、以及语义监督能否因果塑造新的表征。

## 3. 分析方法

1. 先只用 C4E 的 15 个 A 半模板族训练，冻结后在 C4E-B 和 C5E 上测试；若跨库失败，再用 C5E-A 内部读出、反向迁移及 C4E-A+C5E-A 合并训练对照，区分“C5E 本身不可分”和“旧边界不跨表达库稳定”。所有预处理只由各自训练半边估计。
2. 对父类、八个父类条件细类和 64 类联合标签统一计算平衡准确率、负对数似然、尺度归一化的多分类几何间隔及其低尾；以模板族为独立单位做不确定性和标签随机化校准。
3. 用混淆矩阵和类别级间隔定位失败；父类条件 probe 只回答“父类已知时能否读出”，全局 64 类 probe 才是单一语义线性 Router 的直接压力测试。完成固定事实边界诊断后，只用冻结的 C4E-A 探针压力测试一组不同事实包，不在新事实面板上重拟合。

## 4. 结论

### 执行前：两种预期结果

- **若支持：**至少一个注册层在 C4E-B 与 C5E 上的全部十个任务都显著优于标签随机化，且该层所有任务的 5% 低尾几何间隔联合下界为正。此时只支持“固定事实跨表达的全粒度线性读出在该层稳健存在”。
- **若不支持或部分支持：**若平均准确率高但联合低尾下界不为正，则结论是“可读但边界脆弱”；若父类和条件细类强、64 类联合读出弱，则结论是“局部条件可读没有自动组成一个全局线性分发空间”；若连平均读出也未超出随机化，则只在该数据与层上报告未建立。

### 执行后：AI 证据草稿，等待研究者确认

- **直接结果：**E01 的 120 个单元全部显著关联标签；C4E-A 探针在 C4E-B 六层均通过原注册低尾判据，但迁移到 C5E 后六层的最差任务观测间隔均为负。E02 中，C5E 自己训练、自己测试的六层观测瓶颈均为正，平均任务准确率约 99.1%--100%，但 48 单元同时校正后只有 Block 4、12、44 得到正下界；两种单库边界在对方库六层均未获证。没有训练量优势的双库条件只在首尾层同时稳健，完整双库条件在 Block 4、12、20、44 对两个库同时稳健。E02 共 22/48 单元获得正同时下界，完成审计和独立复算均通过。
- **AI 结论草稿：**当前表征不是“没有语义”，而是语义的线性读出与表达库纠缠。Block 4、12、44 已明确表现为“库内稳健可读、跨库边界不兼容”；Block 20、28、36 仍混有 C5E 自身低尾不够稳健的问题。完整双库训练证明部分层存在共同线性边界，但不能把修复单独归因于表达覆盖，因为训练量也增加。
- **仍不能说：**不同事实包泛化、Qwen 预训练未见事实、低预算 Router、原生 Gate 使用、专家效用和训练收益均未建立。
- **唯一下一决策：**完成 E03：冻结 E01 的 60 个探针，在 TAX-C4A 不重拟合地检查一组不同六事实包。该面板同时改变文本长度和措辞自然度，因此失败只能记为联合迁移未建立。
- **E03 当前状态：**没有创建 GPU 作业，也没有科学结果。4×RTX5090
  候选入口已通过独立静态/CPU 审计，等待用户确认；若选择 8 卡，必须
  先冻结并审计新的提交入口。

## 路径

- **研究者判断记录：**固定事实跨表达语义可分性
- **Anchor：**[A15_12 Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_12_semantic_representation_separability/15_12_semantic_representation_separability_anchor.md)
- **E01：**[Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E01_qwen3_30b_fixed_fact_expression_separability/protocol.md) · [Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E01_qwen3_30b_fixed_fact_expression_separability/summary.md) · [Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E01_qwen3_30b_fixed_fact_expression_separability/detailed.md)
- **E02：**[Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E02_expression_bank_boundary_coverage_controls/protocol.md) · [Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E02_expression_bank_boundary_coverage_controls/summary.md) · [Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E02_expression_bank_boundary_coverage_controls/detailed.md)
- **E03：**[Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E03_tax_c4a_unseen_fact_package_transfer/protocol.md)；4×RTX5090 官方入口已通过独立审计，等待用户确认卡数后执行；8 卡入口尚未冻结。
- **白话阅读包：**[0830 目录](docs/semantic_representation_separability/README.md)
