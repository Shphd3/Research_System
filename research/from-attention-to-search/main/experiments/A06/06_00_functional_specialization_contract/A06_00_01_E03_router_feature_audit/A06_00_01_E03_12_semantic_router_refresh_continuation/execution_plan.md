# Execution Plan: H0528a Semantic Router Refresh Continuation

## 1. 目的

这个实验不是新 hypothesis，而是 `H0528a_ntp_objective_mismatch_semantic_routing` 的 continuation。它补 H0528a route-swap / frozen semantic router 的关键限制：

```text
之前 frozen_semantic_router 固定的是 step-0 semantic boundary；
训练中 hidden state 会漂移，所以它不能回答 current hidden geometry 上重建 semantic router 是否有效。
```

本实验问：

> 在 trained checkpoint 的 current hidden states 上重建 semantic router，再给 experts 400-step adaptation window，是否能恢复 task CE、保持 B-context semantic routing，并形成 AB-specific functional expert specialization？

## 2. Source Checkpoints

Source result dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0528a_route_swap_and_frozen_semantic_router/h0528a_route_swap_frozen_semantic_4gpu_20260524
```

Source conditions:

```text
learned_random
semantic_init_learned
```

Seeds:

```text
20260521, 20260522, 20260523, 20260524
```

## 3. Router Refresh Construction

对每个 source checkpoint：

1. 加载 final model。
2. 用当前 checkpoint 的 `ffn_input` hidden states 收集 `B_in_B_only`、`B_in_AB`、`B_in_CB` calibration samples。
3. 用 whitened-centroid prototype 构造 router：

```text
centroid per B-context role
global mean
covariance + 0.001 * I
direction = inv(cov) @ (centroid - global_mean)
normalize direction
router row = 8.0 * direction
bias = - row dot global_mean
unused expert bias = -8.0
```

注意：这不是 clustering，也不是重新训练一个 router；它是把 router 行向量重新居中到当前 hidden geometry 的 B-context prototype direction 上。

## 4. Continuation Conditions

| Condition | 操作 | Router 是否继续训练 | 目的 |
|---|---|---:|---|
| `baseline_continue` | 加载 checkpoint 后继续训练，不改 router | yes | 控制继续训练本身 |
| `refresh_freeze_continue` | 用 current hidden states 重建 semantic router，然后冻结 router 继续训练 | no | 测 semantic route + adaptation window 是否足够 |
| `refresh_trainable_continue` | 用 current hidden states 重建 semantic router，然后继续训练所有参数 | yes | 测 semantic refresh 是否能进入并保持 semantic basin |

## 5. Training Setup

```text
model: top1_selected_gate sparse MoE
experts: 4
load balance: none
steps: 400
batch size: 384
lr: 0.0008
weight decay: 0.01
eval steps: 0, 50, 100, 200, 400
```

## 6. Validity Audit

Full run 前必须通过：

```text
source checkpoints exist
refreshed semantic router step-0 B-context NMI > baseline router
baseline_continue router grad > 0 and delta > 0
refresh_trainable_continue router grad > 0 and delta > 0
refresh_freeze_continue router grad = 0 and delta = 0
active experts per token = 1
full_soft_mixture = False
selected_gate_renormalized = False
```

Smoke run 已通过：

```text
baseline B-context NMI: 0.0399
refreshed B-context NMI: 0.1211
all continuation audits passed
```

## 7. Primary Metrics

Task recovery:

```text
G_refresh = CE(refresh after 400 steps) - CE(baseline_continue after 400 steps)
```

Functional specialization:

```text
S_AB = max_e [Delta L_AB,e - max(Delta L_A,e, Delta L_B,e, Delta L_CB,e)]
```

Semantic route retention:

```text
B_context_NMI_refresh(step)
```

Route-function alignment:

```text
A_c = Delta L_{c,r_c} / max_e Delta L_{c,e}
```

## 8. Repro Command

Smoke:

```bash
python scripts/run_h0528a_semantic_router_refresh_continuation.py \
  --config configs/h0528a_semantic_router_refresh_continuation.json \
  --run-name h0528a_refresh_continuation_smoke_20260525 \
  --run-stage smoke \
  --stage all \
  --parallel \
  --max-parallel 1
```

Full SCO:

```bash
H0528A_REFRESH_ALLOW_REAL_SUBMIT=1 \
RUN_NAME=h0528a_refresh_continuation_4gpu_20260525 \
JOB_NAME=ats-h0528a-refresh-continuation-4gpu \
bash scripts/submit_h0528a_semantic_router_refresh_continuation_4gpu_acp.sh
```

SCO job:

```text
pt-7w0hs9uf
```
