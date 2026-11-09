---
experiment_id: A14_02_E02_component_recombination_capability
status: completed_fail
verdict: fail
run_id: a14_02_e02_component_recombination_capability_4gpu_20260723_full_v1
job_id: pt-zecsxjd8
canonical: summary.md
---

# 结果摘要：A14_02_E02 组件重组能力

主 subanchor：
[A14_02_01 历史组件重组能力 anchor](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/14_02_01_component_recombination_capability_anchor_cn.md)

协议：[protocol.md](protocol.md) · [中文协议](protocol_cn.md)

## 直接结果

**预注册裁定为 `fail`。**生成器审计全部通过，10/10 个 condition-seed
训练单元完成。两组都学会了在新 nuisance context 中完成已见组件配对：

- shared components：5/5 通过，平均 accuracy 0.9990；
- independent lookup：5/5 通过，平均 accuracy 0.9949。

但是，决定性的 shared 未见组件配对测试为 **0/5 通过**。平均 accuracy 为
0.2125，低于 0.80 门槛；平均 semantic consistency 为 0.9485，低于
0.95 门槛。四个 held-out pair 的平均 accuracy 也全部低于 0.70 的配对
守卫。

lookup 在未见配对上的平均 accuracy 为 0.0640，接近随机水平
$1/17=0.0588$，没有触发泄漏守卫。

## 确定认识

本实验把“基础任务没有学会”与“没有重组能力”分开了。模型能够在互斥的新
context 中完成已见映射，因此负结果不能归因于 seen task 没学会，也不能
归因于 nuisance-context shift。

但当前 shared 任务没有形成可靠的“组件分别见过，就能在新配对中复用”的
能力。shared 在五个配对 seeds 中都高于 lookup，但数值在 0.088 到 0.515
之间波动，且没有 seed 达到能力门。这最多提示模型利用了部分共享结构，不能
称为已经学会组合算法。

## 核心图

![讨论表示秩之前必须先通过能力门](capability_before_rank.png)

左图确认两组的已见配对能力匹配；右图显示没有 shared seed 达到未见组件
配对门槛。

## 汇总

| 条件 | 已见配对通过 | 平均已见 accuracy | 重组通过 | 平均重组 accuracy |
| --- | ---: | ---: | ---: | ---: |
| Shared components | 5/5 | 0.9990 | 0/5 | 0.2125 |
| Independent lookup | 5/5 | 0.9949 | 0/5（预期） | 0.0640 |

shared 四个 held-out pair 的平均 accuracy 分别为 0.1382、0.2147、
0.2647 和 0.2324，均低于冻结的 0.70 配对守卫。

## Claim Boundary

可以声称：

> 在这一受控 NTP 任务上，多样 context 训练足以形成已见配对的 context
> invariance，但不足以形成可靠的未见组件配对重组能力。

不能声称：NTP 普遍不能学习组合；模型只用了 lookup 记忆；shared 规则会
降低或提高 ROOT 功能秩；条件功能秩定理被否定；自然语言没有层级结构；或
该结果已经给出 Router 设计。

E02 没有测量或解释任何表示秩。

## 唯一下一决策

决定是否暂停当前 A14_02 合成 shared-versus-lookup 表面，而不是在未通过
组合能力门的任务上授权 ROOT 功能秩比较。
