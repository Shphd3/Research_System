# Execution Plan: H0528a Route Swap and Frozen Semantic Router

## 0. 计划状态

状态：running on SCO as `pt-cikqoqlb`.

本实验直接对应：

The legacy purpose card was removed; this execution record is retained for
historical audit.

## 1. 决策问题

当 final hidden state 中存在可恢复的 semantic/context boundary 时，learned top-1 sparse router 为什么没有选择它？

本实验要判断：

```text
semantic route 是可行但未被 learned router 选择
vs
semantic route 只是 post-hoc diagnostic，不支持 expert function
vs
固定 semantic route 也不足以诱导 functional specialization
```

## 2. 实验结构

### Stage A: Route-Swap Diagnostic

不重新训练。加载 H0527a final checkpoints：

```text
source run:
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0527a_router_initialization_trajectory/h0527a_router_initialization_4gpu_20260524
```

对每个 source checkpoint 比较三种 router：

| Router | 定义 | 用途 |
|---|---|---|
| `trained_final` | checkpoint 中 learned router | baseline |
| `semantic_current` | final hidden states 上按 `B_in_B_only / B_in_AB / B_in_CB` 重建 whitened prototype router | 测 semantic route 是否可行 |
| `source_identity_current` | final hidden states 上按 `A / B / C` 重建 source identity router | shortcut 对照 |

Route swap 会临时替换模型 router weight/bias，然后用同一批 experts 和 output head 评估 task CE、ablation delta、`S_AB` 和 routing NMI。

### Stage B: Frozen Semantic Router Training

按用户要求，假设 Stage A 先成立，不等待 Stage A 审核，直接训练：

| Condition | Router init | Router trainable | 目的 |
|---|---|---:|---|
| `learned_random` | random | yes | H0526 baseline |
| `semantic_init_learned` | semantic/context prototype | yes | H0527a baseline |
| `frozen_semantic_router` | semantic/context prototype | no | 测固定 semantic route 是否诱导 functional experts |

## 3. 实现细节

Runner:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0528a_route_swap_and_frozen_semantic_router.py
```

Config:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0528a_route_swap_and_frozen_semantic_router.json
```

Submit script:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_h0528a_route_swap_and_frozen_semantic_router_4gpu_acp.sh
```

Semantic router construction:

```text
1. collect ffn_input hidden states by semantic label;
2. compute label centroids;
3. compute global mean and covariance with reg = 0.001;
4. directions = inv(cov) @ (centroid - global_mean);
5. normalize directions;
6. router row = prototype_scale * direction;
7. router bias = - row dot global_mean;
8. unused expert bias = -8.0.
```

`frozen_semantic_router` 设置：

```text
model.moe.router.weight.requires_grad = False
model.moe.router.bias.requires_grad = False
```

因此 router parameters 不更新；但 router logits/probs 仍参与 forward，hidden representation 和 experts 仍可通过 task loss 训练。

## 4. Audit Gate

Smoke run 已通过：

```text
run_name:
h0528a_route_swap_frozen_semantic_smoke2_20260524
```

必要检查：

| Condition | 预期 |
|---|---|
| learned conditions | router grad > 0, router delta > 0 |
| frozen condition | router grad = 0, router delta = 0 |
| all conditions | active experts per token = 1 |
| all conditions | full_soft_mixture = False |
| all conditions | selected_gate_renormalized = False |

## 5. 训练设置

```text
steps: 1600
batch size: 384
lr: 0.0008
weight decay: 0.01
grad clip: 1.0
seeds: 20260521, 20260522, 20260523, 20260524
conditions: learned_random, semantic_init_learned, frozen_semantic_router
GPU: SCO 4-card job
SCO job: pt-cikqoqlb
```

## 6. 主指标

Stage A:

```text
G_sem = CE(semantic_current) - CE(trained_final)
Q_sem = S_AB(semantic_current) - S_AB(trained_final)
A_learn_sem = NMI(route_trained, route_semantic)
```

Stage B:

```text
task CE / accuracy
S_AB
class x expert CE delta
route-function alignment
B-context routing heatmap
load entropy
```

## 7. 判定规则

如果 `semantic_current` 不伤 CE 且 `Q_sem > 0`，但 `A_learn_sem` 低：

```text
semantic route 是可行但未被 learned router 选择。
```

如果 `semantic_current` CE 明显变差：

```text
post-hoc semantic route 没和当前 experts 对齐，需要看 frozen training。
```

如果 `frozen_semantic_router` 学会任务且 `S_AB` 稳定高：

```text
semantic route 本身可用；learned-router drift / NTP objective mismatch 是主 failure。
```

如果 `frozen_semantic_router` 也学不会或 `S_AB` 仍低：

```text
semantic partition 不是 sufficient condition；问题还包括 expert-side objective / credit assignment。
```

## 8. 运行命令

Smoke:

```bash
python scripts/run_h0528a_route_swap_and_frozen_semantic_router.py \
  --config configs/h0528a_route_swap_and_frozen_semantic_router.json \
  --run-name h0528a_route_swap_frozen_semantic_smoke2_20260524 \
  --run-stage smoke \
  --stage all \
  --parallel \
  --max-parallel 1
```

Full SCO:

```bash
H0528A_ALLOW_REAL_SUBMIT=1 \
RUN_NAME=h0528a_route_swap_frozen_semantic_4gpu_20260524 \
JOB_NAME=ats-h0528a-route-swap-frozen-4gpu \
bash scripts/submit_h0528a_route_swap_and_frozen_semantic_router_4gpu_acp.sh
```

## 9. 输出

Raw result dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0528a_route_swap_and_frozen_semantic_router/h0528a_route_swap_frozen_semantic_4gpu_20260524
```

Raw figure dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/h0528a_route_swap_and_frozen_semantic_router/h0528a_route_swap_frozen_semantic_4gpu_20260524
```

Curated outputs will be copied after full run into:

```text
main/experiments/H0521_router_feature_specialization/H0528a_route_swap_and_frozen_semantic_router/
XingyuD/sync/0524_router_feature_specialization/H0528a_route_swap_and_frozen_semantic_router/
```
