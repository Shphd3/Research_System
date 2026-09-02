# 冻结表征中的自然语言语义究竟以什么几何形式存在？

```text
type: meeting_cycle_core_task
status: RESULT_AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
problem_key: A15.m2d2_semantic_representation_geometric_form
focus_role: PRIMARY
conversation_owner: codex-thread:01a05d72-0a0c-7a61-be1d-d5df101a2ef2
ownership_status: CLAIMED
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
cycle_start: 2026-09-01
target_meeting: 2026-09-02
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_14_semantic_representation_geometric_form/15_14_semantic_representation_geometric_form_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_14_semantic_representation_geometric_form/A15_14_E01_m2d2_direction_norm_covariance_atlas/protocol.md
core_experiment_count: 1
```

## 1. 核心问题

在冻结的 Qwen3-0.6B-Base 各层表征中，M2D2 自然语言的粗领域和父类条件细领域语义，主要存在于向量方向、向量模长，还是类别相关的分布形状中；模长若不主要承载语义，它又与模型惊讶度或词汇罕见度有什么关系？

## 2. 本轮实验

### 实验 1：方向、模长与分布形状审计

#### 目的

确定冻结表征中粗、细自然语言语义最早在何层可读，以及方向、模长和分布形状各自提供多少独立信息。

#### 假设

语义主要由方向承载；若模长有独立语义作用，保留真实模长应稳定优于在同层打乱模长。

最强竞争解释是方向只给出粗略中心，真正的语义区分依赖模长或类别相关的协方差形状。

#### 分析方法

1. 冻结模型，逐层抽取同一批自然文本表征；训练集只拟合公共降维基和无监督聚类，确认集标签只负责评分。
2. 在粗类和每个父类内部的细类任务上，对比只看模长、只看方向、看完整向量，以及允许每类具有不同轴向方差的模型。
3. 保持方向不变而打乱模长，并检查模长与下一词元损失、词汇罕见度的关系，从而区分语义作用与难度或激活强度作用。

#### 结论

AI 结果草稿，等待研究者确认：固定的整窗平均表征中，方向承载主要语义，模长也通过了预注册贡献门，因此机器裁决为 `RADIUS_CONTRIBUTING`，白话是“方向为主、模长有贡献”。粗类方向 NMI 为 0.1289、模长为 0.0315；父类内细类方向为 0.3223、模长为 0.1397。独立协方差形状没有通过双重 0.02 下界。

AI 补充鲁棒性草稿，等待研究者确认：去掉 PCA、仅减去训练均值并保留全部 1,024 维后，粗类方向/模长 NMI 为 0.1298/0.0321，父类内细类为 0.3180/0.1283，粗细两级仍得到 `RADIUS_CONTRIBUTING`。细类对角密度 NMI 从 PCA-64 的 0.3569 降至原维度的 0.3151，独立协方差形状仍未建立。这说明方向与模长的定性结论不是 PCA 制造的，但高容量密度模型明显受投影维度影响。

关键边界：同层最后一个词元的方向 NMI 只有粗 0.0017、细 0.0057。当前正结果属于整段聚合表征，不能直接推出逐 token Router 已获得同样语义。第 0 层平均表征已经有细类 NMI 0.1777，因此词汇/主题组成仍是强竞争解释，不能把结果称为抽象深层语义。

## 3. 数据、模型和边界

- 数据是与 M2D2 路由实验相同的 Wikipedia 平衡 `3×3` 自然文本：文化艺术、健康健身、自然与物理科学三个粗类，每个粗类三个细类。
- 每个细类使用 1,024 个训练窗、256 个开发窗和 512 个确认窗；每窗 256 个词元，前 64 个提供上下文，后 192 个定义模型惊讶度。
- Qwen3-0.6B-Base 完全冻结，不训练 Router、专家或语言模型；本实验没有优化器更新和训练 checkpoint。
- 标签不进入降维、聚类、重启选择或层选择，只在最终评分时使用。
- 本实验回答表征可访问性和几何载体，不回答原生 Gate 是否使用、专家是否有功能差异或语言建模是否提升。

## 4. 当前唯一决策

等待研究者明确批准后，才打开后继裁决：在 block 14 比较当前 token 与部署可用的因果前缀聚合，并加入词汇控制；只有因果可见对象仍保留方向加模长信号，才把它交给逐 token Router。第二关保持下游且未获执行授权。

## 5. 认识更新边界

- **直接结果：**整窗平均表征是“方向为主、模长有贡献”；协方差独立必要性未建立。
- **可以说：**M2D2 领域信息在冻结表征的整段聚合几何中可读，并非只有方向中心一种信息。
- **不能说：**每个词元都含同样语义、原生 Gate 使用了它、专家因此更有用、或下一词元预测得到提升。
- **人的确认点：**是否同意把“先审计当前 token 与因果前缀聚合”作为唯一下一步；确认后才允许写 daily report 或打开后继协议。
