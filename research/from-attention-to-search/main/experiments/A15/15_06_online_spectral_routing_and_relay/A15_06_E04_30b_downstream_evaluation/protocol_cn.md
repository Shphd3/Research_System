---
experiment_id: A15_06_E04_30b_downstream_evaluation
anchor_id: A15_06_online_spectral_routing_and_relay
status: approved_for_implementation_smoke_and_full_evaluation
approved_by: user
approval_date: 2026-08-09
resource_profile: 5090-8-spot
primary_metric: eight_task_zero_shot_accuracy_vector_at_30b
---

# Protocol：六个 30B 模型的下游任务评估

## 0. 审批摘要

**决策问题：** 六个 seed-17 模型训练到 30B 后，在八项指定 benchmark 上是否存在差异；任务结果是否与 held-out DCLM NLL 排序一致，或对其作出限定？

**条件：** 评价 Vanilla-Full、Centered-Full、Local-HMT、Local-Random-Matched、Relay-HMT、Relay-Random 的不可变 30B 终点。不能按下游结果选择 checkpoint。六臂固定 tokenizer、evaluator/task 版本、zero-shot prompt、seed、最大长度与离线缓存。

**主证据：** 分别报告 ARC-Challenge、ARC-Easy、HellaSwag、LAMBADA_OPENAI、PIQA、RACE、Social IQA、Winogrande 的准确率向量。无权重 macro average 只用于导航，不是通用能力分数。

**先过有效性门：** 计分前必须证明 Centered 与投影/Relay Router 在 eval 中读取 checkpoint 的 running mean 与部署子空间，这些 buffer 不再更新，同一输入重复前向得到完全一致的 logits 与 routes。

**批准范围：** Protocol、evaluator 适配、测试、limited smoke、单节点 8×5090 完整评估、聚合、作图和结果记录均已批准。

**不能声称：** 单 seed 不能建立方法稳定性；任务准确率不能识别收益的唯一机制、普遍 H/M/T 语义或训练效率。

## A. Anchor 对齐 — CONFIRMED

本实验实现 A15_06 E03 已注册的终点下游条款，只评价已完成的 30B 模型，不重新打开 10B 两 seed 中未通过的 Relay-HMT 证书。

## B. Checkpoint 合同 — CONFIRMED

六个 endpoint 均为 step 38,147（30,000,021,504 nominal tokens），路径为 `/data/250010109/MoE_Router/outputs/online_spectral_router_training/osrt-30b-<arm>-s17/checkpoints/checkpoint-38147/`。每个 checkpoint 必须有一个 model state 与八个 optimizer shard；下游只读取 model state。记录 checkpoint SHA-256、step、tokens、source manifest、arm 配置与 tokenizer digest。相同 step 已完成的 1,024 文档 DCLM NLL 是语言模型参考。

## C. Router eval 状态守卫 — CONFIRMED

每个 arm 使用训练时精确 runtime，并在 benchmark 前调用 `model.eval()`；smoke 和 full 前后对全部 persistent Router buffer 做 hash。

1. Vanilla-Full 必须 `router_center_input=false`，不减 running mean。
2. Centered-Full 每层必须使用 checkpoint 中非零的 `router_running_mean`；重复前向后 buffer bitwise 不变。
3. Local-HMT/Local-Random-Matched 的第 2--4 block 必须存在初始化、正交、嵌套的部署基底；有效 Gate 权重等于注册的 H/M/T 投影权重。部署基底以 BF16 保存，因此 Gram/嵌套最大残差要求不超过 \(10^{-3}\)，并报告实际残差，而不把它表述成 FP64 意义下的精确正交。
4. Relay-HMT/Relay-Random 的第 2--4 block 必须读取 block-1 Relay source，而不是本层 Router source，并使用 checkpoint 的 shared center 与部署基底。
5. 所有投影 arm 的 covariance EMA、statistics mean、U64、U320、random Haar、refresh count 和 last gamma 在 eval 中不得变化。

在固定 token batch 上，根据捕获的有效输入与权重离线重放 Router logits 与 top-1。BF16 最大 logit 误差不超过 \(2\times10^{-3}\)，除严格并列外 winner 一致率为 1.0；并列必须复现训练算子的 tie rule。两次完整前向的 logits、routes 与 buffer hash 必须一致。

投影 arm 另做 full-weight 无投影诊断，非零 route divergence 用来证明投影确实生效；该消融不能用于 benchmark 计分。

## D. Benchmark 合同 — CONFIRMED

固定 `lm-eval==0.4.12`、`transformers==4.53.3` 和训练 tokenizer。全部 zero-shot，最大长度 1,024，不用 chat template，不额外加 BOS；seed/few-shot seed 均为 42，启用 request cache，支持时使用 10,000 次 evaluator bootstrap。

| 任务 | lm-eval 名称 | 指标 |
| --- | --- | --- |
| ARC-Challenge | `arc_challenge` | `acc_norm` |
| ARC-Easy | `arc_easy` | `acc_norm` |
| HellaSwag | `hellaswag` | `acc_norm` |
| LAMBADA_OPENAI | `lambada_openai` | `acc` |
| PIQA | `piqa` | `acc_norm` |
| RACE | `race` | `acc` |
| SIQA | `social_iqa` | `acc` |
| Winogrande | `winogrande` | `acc` |

Full 前必须证明八项任务离线缓存完整。Smoke 对六臂各跑 LAMBADA、PIQA 和一个选择题任务的两条样本。缓存缺失、task 版本漂移或需要联网会阻塞 full，修复不得改变任务集。

## E. 分析合同 — CONFIRMED

报告六臂×八任务得分与 evaluator 标准误/区间。每个任务都与 Centered-Full 比较；如果 lm-eval sample output 有 item identity，给出 item-level 配对差。表中同时放入冻结的 30B DCLM NLL 与负载。

不存在一个通用 winner 标量。只有某 arm 至少 6/8 任务严格高于 Centered-Full、至多一项更低，并且至少四项的 item-level 不确定性方向相同时，才描述为“广泛下游迁移”；否则写成 task-specific mixed evidence。Macro average 无权重且只作导航。

- Pass：相对 Centered-Full 满足 breadth 规则。
- Fail：完整证据不满足广泛迁移规则；局部任务增益仍保留。
- Insufficient：checkpoint/Router 守卫、suite 身份、任务完成度或不可变结果重建失败。

## F. 执行与可复现性 — CONFIRMED

Full 使用一个 ACP `5090-8-spot` 节点。六个进程各绑定一个 GPU、一个 arm，顺序运行八项任务；其余 GPU 留给 smoke/诊断。任务名为 `a15-30b-downstream-eighttask-s17`。原始产物位于 `/data/250010109/MoE_Router/outputs/online_spectral_router_training/downstream_30b_e04/`，按 arm/task 不可变保存。

必须输出 suite YAML/hash、checkpoint manifest、环境与 package manifest、Router guard JSON、原始 lm-eval JSON、item sample、任务摘要、job ledger、日志和 source manifest；禁止覆盖结果。

## G. 失败与冻结规则 — CONFIRMED

NaN/Inf、OOM、缓存缺失、model state 不匹配、Router buffer 变化、route replay 失败、tokenizer 不一致、任务失败或 raw result 缺失会停止受影响 arm，并使完整比较在精确修复前为 Insufficient。准确率低、坍缩或与 NLL 不一致是科学结果，不能触发删除或换 checkpoint。

跨块一致性：`PASS`。首次 smoke 时冻结 suite、zero-shot 合同、arm、endpoint、指标和裁定规则；后续变化只能 append-only amendment。

## H. Amendment 1：源模型的有效 LB 状态（2026-08-09）

六条源训练均声明 `lambda_lb=0.01`，但 A16 可微性审计证实：re-entrant activation checkpointing 路径把 LB 放在未连接 backward 的嵌套辅助字典中。名义 LM+LB 与 LM-only 的配对单步重放产生了完全一致的模型张量和八个 optimizer shard；共同关闭 activation checkpointing 后，LB 才真实改变 optimizer 与模型状态。

下游实验仍然能够比较六个不可变训练模型，但必须将其表述为“配置并记录了 LB telemetry，却没有有效 LB 梯度”的模型；任何任务差异都不能归因于 LB 正则。benchmark、checkpoint、Router eval 行为、指标和裁定规则均不改变。
