# 07 研究线：partition 为什么有 functional value

## 裁定

07 线不是绕开 06，而是回答 06 之后必须回答的价值问题：

```text
即使 routing 不 collapse，也不能直接 claim specialization。
必须证明这个 partition 减少 feature interference，或让 routed expert 对对应
feature/group 有 causal utility。
```

## 逻辑顺序

```text
A07_01: 先证明 controlled D07 metric surface 合法
-> A07_02: 再证明 common-control 比 matched load-only 更能减少 rare loss
-> A07_03: 再证明 routed expert 与 conflict group 有 route-function binding
-> A07_04: 尝试 neural proxy，但当前证据不足
```

## Controlled D07 支持什么

A07_01 支持 D07 是合法 controlled synthetic audit surface：

```text
Delta_vs_best_null = 0.8601 +/- 0.0008
oracle rare loss 明显低于 dense 和 load-only null
shortcut guard 通过
```

A07_02 支持 common-control 有 method effect：

```text
RIR_cc = 0.9502 +/- 0.0006
common-control 与 load-only 的 load balance 匹配
rare loss 改善不是 load matching 本身造成的
```

A07_03 支持 route-function binding：

```text
selected-best rate = 1.0000
route-conditioned utility advantage 约 0.950
modal ablation delta = 0.6800
nonmodal ablation delta = 0.0000
```

这条链可以支持：

```text
在 controlled D07 中，某些 partition 不只是 balanced load，而是有 conflict
reduction 和 expert utility。
```

## A07_04 为什么不能升级 claim

A07_04 neural proxy 的结果是 insufficient evidence：

```text
centered unsupervised split 相比 random top-1 略微降低 conflict 和 rare loss；
但 rare-loss improvement 小且 noisy；
dense_shared 的 rare loss 仍低于 centered MoE；
rare accuracy 仍低。
```

因此不能 claim：

```text
functional expert specialization 已经在 neural setting 成立；
MoE partition 已经 beat dense；
真实语料可迁移。
```

## 与 06 的连接

07 要合法进入真实主线，前提是：

```text
proxy routing 被 preservation 保持；
之后再测 common/rare interference 或 expert utility。
```

如果 routing 在 step 5/10 已经被覆盖，utility test 会混淆两个问题：

```text
没有 utility
vs
routing 已经消失
```

## Source Links

```text
Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/
Projects/from-attention-to-search/main/experiments/A07/A07_01_common_rare_conflict_metric_audit/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_02_common_controlled_rare_interference/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_03_route_function_binding/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md
```

## 当前边界

可以说：

```text
controlled D07 支持 partition value 的完整机制链：
metric surface -> rare interference reduction -> route-function binding。
```

不能说：

```text
real-DCLM 已经有 functional MoE specialization；
neural A07_04 已经证明 dense-beating MoE；
07 可以替代 06 的 preservation bottleneck。
```
