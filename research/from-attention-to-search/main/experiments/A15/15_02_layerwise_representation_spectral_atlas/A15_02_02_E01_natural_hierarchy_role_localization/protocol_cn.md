---
experiment_id: A15_02_02_E01_natural_hierarchy_role_localization
anchor_id: 15_02_02_natural_hierarchy_role_localization
status: executed_completed
approved_by: user
approval_date: 2026-08-01
---

# Protocol：真实层级概念 token 的频谱位置

## 0. Approval Snapshot

- **目的：**判断自然语言中粗/细层级角色是否对应不同 covariance 频带。
- **主 Anchor：**[A15_02_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_02_natural_hierarchy_role_localization_anchor_cn.md)
- **实验角色：**冻结表征的根因/操作化审计，不训练模型。
- **主指标：**同一中位概念在同一句中作为父类与子类时的频带富集配对差 \(\Delta_B\)。
- **最小设置：**32 条学科层级链、顺序平衡的 calibration/evaluation 模板、LB-80k MoE 与 Qwen3-8B。
- **Pass：**至少一类频带效应在顺序模板内同向、文档 bootstrap 区间排除零、超过随机 rank 分配，并在两模型相应深度同向。
- **Fail：**数据与基底有效，但同概念角色差异不超过零或随机对照。
- **Insufficient：**span/token 对齐、样本、covariance 稳定性或模型重放门失败。
- **不能声称：**层级导致频谱、Router 使用该方向、或该方向改善训练。
- **批准：**用户已明确要求直接开始实验并汇报。

## 1. Terminology / Definitions

| 术语 | 人话含义 | 计算 | 作用 | 不能证明 |
| --- | --- | --- | --- | --- |
| root/mid/leaf | 上位、中位、下位概念 | 字符 span 映射到 subword | 描述绝对层级 | 词汇已控制 |
| mid-child | 中位概念作为 root 的子类 | 同一句第一/第二 occurrence | 与 mid-parent 做同词配对 | 功能价值 |
| mid-parent | 同一中位概念作为 leaf 的父类 | 同一句另一 occurrence | 消除词汇身份与分词长度 | 因果机制 |
| 频带富集 \(r_B\) | token 在某带的相对能量是否高于 calibration 平均 | Anchor 公式，无量纲 log ratio | 跨宽度比较谱位置 | 总激活强度或路由收益 |

## 2. Anchor Alignment

实验测试“同一 rank 频带是否具有跨自然层级角色的稳定含义”。主 falsifier 是同词配对效应为零，或随 occurrence 顺序反转。

## 3. Tested Hypothesis

父类角色与子类角色在谱头、中段或谱尾存在稳定差异，并可跨模型复现方向。

## 4. Rival Explanations

词汇身份、subword 数、句内位置、模板句法、总向量范数和任意 rank 分组都可造成伪差异。

## 5. Data / Model / Algorithm / Objective

构造 32 条已知学科链；每句包含 root、mid-child、mid-parent、leaf 四个 span。12 个 calibration 模板与四个 evaluation 模板不重用，且 child-first/parent-first 数量相等。covariance 仅由 calibration 的全部非 padding content tokens 拟合；所有标签结论只来自 evaluation。

模型：当前 12 层 width-768 8E top-1 LB-80k MoE，抓实际 Gate 输入；本地 Qwen3-8B，抓 9 个等深度位置的 post-attention/pre-MLP norm 输出。

## 6. Conditions, Seeds, And Checkpoints

| 条件 | 作用 | 主/次证据 | 无效条件 |
| --- | --- | --- | --- |
| mid-parent vs mid-child | 消除词汇/分词混淆 | 主证据 | occurrence 未精确映射 |
| root vs leaf | 回答直观粗/细问题 | 次证据 | 不允许单独作语义结论 |
| child-first vs parent-first | 排除绝对位置 | validity guard | 方向相反 |
| 随机 rank 分配 | 排除任意频带分组 | 主对照 | 真实效应不超 q95 |
| MoE vs Qwen3-8B | 检查模型条件性 | 复现证据 | 不要求绝对值相等 |

## 7. Primary Metric

对每个 evaluation 句、概念和层计算 \(r_B\)；主量为同一 mid 的 \(r_B^{parent}-r_B^{child}\)。以 32 条概念链为重采样单位做 2,000 次 paired bootstrap。频带为 12 个等 rank 细带；粗带 H=F1、M=F2--F5、T=F6--F12，使两种宽度按相同 rank fraction 比较。

## 8. Secondary Metrics

报告 root-leaf 差、raw energy share、whitened per-dimension energy、每带 top-10% occurrence 的角色富集和逐层效应。

## 9. Known Good / Known Bad / Known Confusing Cases

known-good：每句四 span 均可定位，同 mid 两 occurrence token-id 序列相同。known-bad：只比较 mathematics 与 linear algebra。known-confusing：causal 位置与角色一致，因此必须用反向顺序模板平衡。

## 10. Stage-Level Profiling Plan

S0 数据/token span 审计；S1 两模型单句 hook smoke；S2 calibration basis 与 half-split 稳定性；S3 全量 evaluation 配对投影；S4 bootstrap/null 与结果审计。

## 11. Algorithm Specification

1. 用 offset mapping 将字符 span 映射到 subword；2. 抽取各层表征；3. calibration 上拟合 \(\mu,U,\lambda\)；4. 计算 evaluation occurrence 的 coarse/fine band 分数；5. 配对汇总；6. 随机打乱 eigenvector rank 标签形成 256 个 null；7. bootstrap 置信区间。

## 12. Success / Failure / Insufficient Evidence

Pass/Fail/Insufficient 按第 0 节执行。若两模型方向不一致，报告 model-conditioned，不写普遍结论。

## 13. What This Cannot Claim

不能由投影差异推出语义重要性、专家效用、训练效率、自然层级因果形成，或 Qwen dense 表征就是 Router 输入。

## 14. Review Notes And Protocol Changes

2026-08-01：用户授权直接执行。为消除词汇混淆，AI 将主比较从 root-vs-leaf 收紧为同一 mid 的 parent-vs-child；root-vs-leaf保留为直观次指标。

2026-08-01 结果审计修订：Protocol 已把 occurrence 顺序列为 validity guard，但初版聚合代码只检查两种顺序方向相同，不能排除效应大小被顺序支配。最终裁定前将其显式化为：两种顺序分别超过 rank null，且“child-first 效应减 parent-first 效应”的 95% 链级 bootstrap 区间必须包含零。旧的宽松结果保留为 `role_effect_candidate`，严格结果写入 `role_effect_pass`；没有依据结果改变效应方向或显著性阈值。
