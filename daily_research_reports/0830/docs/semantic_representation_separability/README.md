---
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
topic: qwen3_30b_semantic_representation_separability
created: 2026-08-30
canonical_result_status: E01_E02_COMPUTATION_COMPLETE_E03_PENDING_RESOURCE_SELECTION
---

# 0830：Qwen3-30B 语义表征可分性审查阅读包

本文件夹只负责把实验讲清楚。正式数值以项目内的 `summary.md`、
`detailed.md` 和冻结表格为准；在研究者确认“直接结果、不能说什么、
下一决策”之前，这里不是已确认的当日报告。

## 本包统一术语

- **混合专家模型（MoE）：**由路由机制选择或组合多个专家模块的模型；
  它不自动意味着专家已经形成有用分工。
- **路由器（Router）：**为输入选择专家或输出专家分数的机制。本包的
  离线标签分类器不是模型原生 Router。
- **原生门控层（Gate）：**本包专指 Qwen 中产生专家分数的原生 Router
  模块；“Gate 输入”是它在 top-$k$ 选择以前收到的隐藏向量。
- **模型块（Block）：**Qwen 中按深度编号的 Transformer 计算块；例如
  Block 12 不是第 12 个样本或第 12 个专家。
- **线性探针（probe）：**冻结 Qwen 后，在隐藏表示上拟合的线性分类器。
- **分类间隔（margin）：**样本到最近错误类线性边界的有符号几何距离；
  本包必须同时注明归一化方式和所用分位数。
- **E01/E02/E03：**分别指单库边界迁移审查、表达库边界覆盖对照、以及
  TAX-C4A 新于探针事实包的联合偏移压力测试。
- **类距离归一化方差（CDNV）：**类内散布除以类中心平方距离的几何
  诊断，只用于定位拥挤类别，不裁决线性可分性。

## 建议阅读顺序

1. `01_结论先行_唯一问题与结果.md`：先看我们究竟回答了什么。
2. `02_实验四段式_数据探针与指标.md`：看一条数据、表征位置、拟合流程和判据。
3. `03_图表逐张阅读_失败定位与旧实验对照.md`：学会读五张主图和失败类别。
4. `04_理论认识更新_语义可分与映射.md`：理解线性映射、非线性映射、层级读出和“足够可分”。
5. `05_文献定位_下一步与发表门槛.md`：理解与 X-MoE 等工作的关系，以及论文还缺什么。
6. `06_复现实验与自测清单.md`：按检查题确认自己真正掌握了对象、代码和结论边界。
7. `07_组会唯一认识更新_一分钟汇报.md`：最后练习只用一分钟汇报一个确定认识、边界和下一决策。

## 规范证据入口

- E01 冻结合同：[protocol.md](../../../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E01_qwen3_30b_fixed_fact_expression_separability/protocol.md)
- E01 结果摘要：[summary.md](../../../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E01_qwen3_30b_fixed_fact_expression_separability/summary.md)
- E01 完整证据：[detailed.md](../../../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E01_qwen3_30b_fixed_fact_expression_separability/detailed.md)
- E02 边界覆盖对照：[protocol.md](../../../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E02_expression_bank_boundary_coverage_controls/protocol.md)
- E02 结果摘要：[summary.md](../../../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E02_expression_bank_boundary_coverage_controls/summary.md)
- E02 完整证据：[detailed.md](../../../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E02_expression_bank_boundary_coverage_controls/detailed.md)
- E03 新事实包合同：[protocol.md](../../../../Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E03_tax_c4a_unseen_fact_package_transfer/protocol.md)
- 当前任务卡：[focus_qwen3_30b_semantic_representation_separability.md](../../focus_qwen3_30b_semantic_representation_separability.md)

## 当前证据状态

- **已核验证据：**E01 的 60 个探针、120 个评估单元和 12 个低尾瓶颈已完成；E02 的 240 个模型账本、480 个任务单元、48 个同时瓶颈和 36 个成对差值也已完成。E01 的计数、哈希与结果已由独立流程复核，但未保存独立复算的规范机器回执；E02 保存了逐件哈希和全量复算的通过回执，证据形态更强。
- **当前结论：**Block 4、12、44 明确表现为库内稳健可读但跨库边界不兼容；完整双库训练在 Block 4、12、20、44 形成两个测试库共同的正同时下界。
- **待执行：**E03 的 TAX-C4A 新事实包冻结探针测试；4×RTX5090 官方入口已通过独立审计，GPU 创建等待用户确认卡数。8 卡入口尚未冻结。
- **未知：**不同事实包迁移、自然数据复制、原生路由器使用、专家效用和语言模型收益。
