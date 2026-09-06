# 注意力层实际取回的语义是否集中在少数查询头中？

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: A15.headwise_causal_semantic_retrieval_audit
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: AWAITING_HUMAN_CONFIRMATION
cycle_start: 2026-09-04
target_meeting: Unknown
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_16_headwise_causal_semantic_retrieval/15_16_headwise_causal_semantic_retrieval_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_16_headwise_causal_semantic_retrieval/A15_16_E01_headwise_gold_label_linear_readability/protocol.md
source_meeting: daily_research_reports/0903/docs/0902_组会逐句校订_结论_架构审计与两日计划.md
core_experiment_count: 1
```

## 1. 核心问题

在冻结的 Qwen3-0.6B-Base 中，每个注意力查询头为当前词元实际取回的上下文向量，对 M2D2 真实粗领域和父类内部细领域的线性可读性是否稳定不同？如果不同，粗、细语义是否呈现不同的逐头分布？

这里的“查询头取回向量”是一个查询头对因果历史中的 Value 向量加权求和后、进入注意力输出投影前的 128 维向量。Qwen3-0.6B 的两个查询头共享一组 Key/Value，因此本实验审核 16 个查询头的实际取回结果，不把它们误写成 16 份独立的 KV cache。

**本轮不回答：**历史中可用的信息是否多于实际检索的信息；某个头是否因果地帮助下一词元预测；KV cache 能否压缩；哪一层或哪一头应当加入 LoRA 混合专家模块。

## 2. 本轮实验

### 实验 1：真实粗细标签的逐层逐头线性可读性审计

#### 目的

检查注意力检索结果中的语义信息是均匀分布，还是集中在可重复识别的少数查询头中，从而判断第二阶段是否值得精确到头设计历史聚合对照和因果干预。

#### 假设

主要假设是：同一层的不同查询头对真实粗、细语义的线性可读性存在可重复差异，而且粗、细任务的高可读头分布不完全相同。最强竞争解释是所有头只有相近的弱信号，开发集中的“最佳头”只是从 28 层乘 16 个头中挑选造成的偶然极值。

#### 分析方法

1. 冻结模型，在全部 28 个块截取 16 个查询头进入注意力输出投影前的实际取回向量；每个头独立训练同容量线性分类器，分别预测三个粗领域和真实父领域内的三个细领域。
2. 以每个窗口为独立单位，比较同层最好头、头间可读性分散程度和开发集选出的前四个头相对其余头的交叉熵增益；确认集只检验开发集冻结的层与头集合。
3. 用 2,000 次窗口标签置换形成覆盖全部层和头搜索的最大统计量空对照，并用 2,000 次分层窗口重采样检查开发集前四个头在确认集上的优势是否稳定，从而排除“多看了很多头后必然出现一个最好头”的解释。

#### 结论

**人工智能结果草案，等待研究者确认**

- **直接结果：**粗分类与条件细分类都在开发集选择第 20 块和查询头 `[4,5,13,7]`。确认集前四头相对其余 12 头的增益分别为 `0.300311 [0.293544,0.306483]` nat 和 `0.354685 [0.347546,0.362285]` nat，四个探针种子全部同向。
- **实验结论：**注册裁决是 `NO_REPRODUCIBLE_HEAD_HETEROGENEITY`。两项任务在开发集和确认集的真实头间分散程度都低于标签置换阈值，不能把稳定的头排序登记为标签特异的逐头语义分工。
- **仍不能说：**这些头被模型因果使用，能够改善 KV 检索，适合加入专家，或者能够提高下一词元任务。
- **对后续实验的影响：**粗细任务逐层头排序的平均相关系数为 `0.971534`，第 20 块前四头完全相同。因此若继续实验 2，只能把这些头称为“两个任务共同高可读的候选头”，不能按粗头与细头分别构造模块。

## 3. 核心任务卡总结论

- **我的认识更新：**人工智能草案认为，逐头读出出现稳定但粗细共享的排序；注册空对照不支持标签特异的头分工。等待研究者确认或修正。
- **仍不能说：**逐头线性可读性不等于注意力原生因果使用、专家功能或下一词元收益。
- **唯一下一决策：**研究者检查实验 1 的四段式结果后，决定是否推进并完整设计实验 2；在此之前不设计或执行实验 2。

## 路径

- **实验协议：**[A15.16 E01 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_16_headwise_causal_semantic_retrieval/A15_16_E01_headwise_gold_label_linear_readability/protocol.md)
- **结果摘要：**[Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_16_headwise_causal_semantic_retrieval/A15_16_E01_headwise_gold_label_linear_readability/summary.md)
- **完整证据：**[Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_16_headwise_causal_semantic_retrieval/A15_16_E01_headwise_gold_label_linear_readability/detailed.md)
- **每日研究报告：**研究者确认结果后再写
- **待研究问题清单：**[Parking Lot](../../Projects/from-attention-to-search/main/parking_lot/README.md)
