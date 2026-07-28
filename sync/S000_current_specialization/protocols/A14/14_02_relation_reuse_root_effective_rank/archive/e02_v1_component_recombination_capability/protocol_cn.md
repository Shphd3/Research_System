---
experiment_id: A14_02_E02_component_recombination_capability
status: completed_fail
run_authorized: true
approval_date: 2026-07-23
run_id: a14_02_e02_component_recombination_capability_4gpu_20260723_full_v1
job_id: pt-zecsxjd8
primary_anchor: /Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/14_02_01_component_recombination_capability_anchor.md
---

# Protocol：A14_02_E02 组件重组能力

## 0. Approval Snapshot

**批准状态：**用户明确要求保留 E01，另建小 anchor，并授权不再审核、直接在
reserved 资源完成 full run。  
**目的：**判断 shared NTP 任务是否真正支持“组件见过、配对未见”的重组。  
**主 anchor：**[A14_02_01 历史版本](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/14_02_01_component_recombination_capability_anchor_cn.md)。  
**唯一问题：**NTP 能否完成两个已见组件的未见配对？  
**主指标：**shared 未见配对 exact answer accuracy。  
**实验角色：**能力操作化与证伪实验。  
**最小设置：**shared composition 与 independent lookup；5 个配对 seeds。  
**通过：**至少 4/5 seeds 同时通过 seen-pair 能力，以及 shared 重组
accuracy $\ge0.80$、consistency $\ge0.95$。  
**否定：**两组均至少 4/5 通过 seen-pair 门，但 shared 至多 1/5 通过
重组门。  
**证据不足：**能力不匹配、2--3/5 通过、lookup 泄漏或生成器守卫失败。  
**不能声称：**低秩、自然语言层级、普遍 Transformer 机制或 Router 效用。  
**批准决定：**已批准并授权 full run。

## 1. 术语

| 术语 | 白话含义 | 具体计算 | 单位 | 决策作用 | 不能证明 |
| --- | --- | --- | --- | --- | --- |
| component | 可复用规则的一部分 | $\alpha$ 或 $\beta$ token | 类别 | 定义重组 | 语义原子 |
| seen pair | 训练中出现的组件配对 | 12 个 $(\alpha,\beta)$ 对 | pair | 能力守卫 | 组件复用 |
| unseen pair | 两组件各自见过，但配对未见 | 固定移除的 4 对 | pair | 决定性干预 | 真实语言组合 |
| 新 context accuracy | 已见映射换表面 context 后仍正确 | exact answer accuracy | 比例 | 确认任务学会 | 组合算法 |
| 重组 accuracy | 未见组件配对是否正确 | 未见配对的 exact accuracy | 比例 | 主指标 | 低表示秩 |
| semantic consistency | 等价 context 下预测是否一致 | 每个 relation 的众数预测比例均值 | 比例 | 排除不稳定猜测 | 正确性 |

## 2. Anchor Alignment

上位秩问题保持不变。本实验只裁定阻塞 E01 的能力条款。

最强 falsifier：两组均能解决 seen pair 的新 context，但 shared 的未见
配对仍接近 $1/17$。

## 3. Tested Hypothesis

对 shared seed $j$，令 $A_j^{recomb}$ 为 4 个未见配对的 exact accuracy。
支持模式为：

$$
\#\{j:A_j^{recomb}\ge0.80,\ C_j^{recomb}\ge0.95\}\ge4.
$$

只有 seen-pair 能力门通过后，才解释该指标。

## 4. Rival Explanations

1. 记住完整表，而非复用组件；
2. 只是新 context 能力失败；
3. 某个 primitive component 从未进入训练；
4. 输出类别不均衡；
5. test 参与 checkpoint 选择；
6. lookup 控制意外具有规律；
7. 只有一个简单 held-out pair 拉高均值。

## 5. 数据、模型与目标

shared rule：

$$
y=\beta(a+\alpha)\pmod {17}.
$$

固定移除：

```text
(alpha 0, beta-index 1)
(alpha 1, beta-index 3)
(alpha 2, beta-index 0)
(alpha 3, beta-index 2)
```

每个组件在剩余训练配对中出现 3 次。每个 seen pair 包含全部 17 个实体和
8 个不同训练 context；calibration 与 test 各使用 4 个互斥 context。

lookup 为每个完整配对采样独立随机 permutation。两组的 prefix、各 split
样本数和答案边际精确匹配。

```text
[alpha] [entity] [context] [beta] [ROOT] [ANSWER]
```

模型沿用 E01 的 `RootTaskLM`：2 层、1 头、宽度 64；目标为 full-position
NTP CE。checkpoint 只使用 seen-pair calibration。

## 6. 条件、seeds 与 checkpoint

| 条件／守卫 | 作用 | 证据角色 | 通过 | 证据不足 |
| --- | --- | --- | --- | --- |
| shared components | 主重组问题 | Primary | 4/5 重组通过 | 2--3/5 或能力失败 |
| lookup tables | 基础表面与泄漏控制 | Hard guard | 4/5 seen 通过；unseen $\le0.20$ | seen 失败或泄漏 |
| generator audit | 排除构造问题 | Hard gate | 全部精确检查通过 | 任一失败 |
| pair breakdown | 排除单个简单配对 | Secondary guard | 每对均值 $\ge0.70$ | 某对塌缩 |

seeds：`[0,1,2,3,4]`，两组配对。

checkpoint 为第一个连续 3 次满足 calibration accuracy $\ge0.95$ 且 CE
$\le0.10$ 的点；最多 6000 steps，不单独延长条件。

## 7. 主指标

**shared 未见配对 exact answer accuracy**：

正确 answer token 数除以全部 held-out-pair、entity 与 test-context 样本数。

它直接区分“复用组件”与“只记住 12 个完整配对表”。由于误通过会错误授权
后续秩实验，组件覆盖、生成器匹配、lookup 与 checkpoint 守卫均为硬门。

## 8. 次级指标

- seen-pair calibration/test CE 与 accuracy；
- 重组 semantic consistency；
- 4 个 held-out pair 分别的 accuracy；
- 达到能力门的训练 step；
- lookup 未见配对 accuracy（只作泄漏诊断）。

## 9. Known Good / Bad / Confusing

- known good：每个映射都是 permutation，答案均衡；
- known bad：未见 lookup 表应接近 $1/17$；
- confusing：只拟合训练集而不能过新 context 门属于记忆，结果为证据不足。

## 10. Stage Plan

```text
生成器审计
-> seen-pair calibration 能力
-> seen-pair 新 context
-> shared 未见配对重组
-> 五 seed 聚合裁定
```

## 11. Algorithm

1. 审计组件覆盖、配对 holdout、context、prefix 和答案边际；
2. 使用相同模型、优化器与预算训练；
3. 只用 seen-pair calibration 选 checkpoint；
4. 分别评估新 context 与未见组件配对；
5. 不修改阈值，聚合五 seeds。

## 12. Pass / Fail / Insufficient

除首页规则外，科学通过还要求四个 held-out pair 的平均 accuracy 分别不低于
$0.70$。任何 capability-passing lookup seed 的未见配对 accuracy 高于
$0.20$，均触发 `insufficient`，不能算支持。

## 13. What This Cannot Claim

本实验不测功能秩，不能证明 A14 条件秩定理已在 Transformer 中成立，也不能
证明自然语言层级、参数压缩或专家 specialization。

## 14. Review Notes

2026-07-23：用户明确要求保留 A14_02_E01，另建能力小 anchor，并授权直接
执行。E01 的条件、阈值、结果和文件均未修改。

2026-07-23：冻结的 10 个训练单元已投送至一个 reserved
`n6ls.iu.i40.4` worker（4 GPUs），ACP job 为 `pt-zecsxjd8`，run ID 为
`a14_02_e02_component_recombination_capability_4gpu_20260723_full_v1`。

2026-07-23：任务以 `SUCCEEDED` 完成，科学裁定为 `fail`。见
[summary_cn.md](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/summary_cn.md) 与 [detailed.md](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/detailed.md)。观察结果后
没有修改阈值、条件或任何 E01 文件。
