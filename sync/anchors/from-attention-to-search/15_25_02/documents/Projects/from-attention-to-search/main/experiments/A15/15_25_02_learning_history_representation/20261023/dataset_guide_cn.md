派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/dataset_guide_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/dataset_guide_cn.md)；研究修改仍回到原件。

---

# 本轮数据：同一列表，两套条件规则

研究问题：学习经历如何改变条件规则的表征，以及哪些方向对任务作答最重要？

每题包含可见模式、口令和三个不同词。模式一是旧任务 A：甲取首词、乙取末词；模式二是新任务 B：甲取末词、乙取首词。实际样例“模式：一。口令：甲。列表：绿 黑 马。答案：”要求回答“绿”；只把模式改成二，正确答案变为“马”。每题只评价接下来的一个答案 token。

原数据身份为 `data_a17_conditional_mapping_v1`。本轮选已有 DEV 中 old/reversed 两世界的全部 1,600 条记录、400 个无序词组；不读取 TEST。每个词组的两个模式和两个口令始终一起划分。按无序词组 ID 的 SHA256 模二，发现集有 196 组/784 条，评估集有 204 组/816 条。这个新划分只隔离本轮选择，不能消除原实验已经查看 DEV 的事实。

| 样本面板 | 发现集 | 评估集 | 含义 |
|---|---:|---:|---|
| order_new | 396 | 404 | 原数据定义的新排列面板 |
| combination_new | 388 | 412 | 原数据定义的新组合面板 |

每个单元中旧/新世界各占一半。列表始终三词，实际输入为 19–21 个 token。长短程不是本轮操纵因素。同一题在四个模型中逐 token 相同，答案位置和目标 ID 相同。

两个训练端点均从已学会 A 的状态继续 1,200 步。只学 B 的端点看 24,000 个 B 答案；混合端点看 12,000 个 A 和 12,000 个 B 答案。此处计数是训练暴露；特征出现率是本轮输入上 CrossCoder 激活非零的比例。二者不是同一个频率，也都不是模型预训练曝光的测量。

[Protocol](protocol_cn.md) 固定分析和边界。原始逐题清单留在 `/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/data/examples.jsonl`，其 hash 由冻结清单和执行回执记录。
