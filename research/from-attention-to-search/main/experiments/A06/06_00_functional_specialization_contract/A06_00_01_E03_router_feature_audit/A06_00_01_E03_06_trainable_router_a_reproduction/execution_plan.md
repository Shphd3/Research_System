# Execution Plan: H0525a Trainable-Router A Reproduction

## 1. Purpose

修正 H0524a/H0524b 的实现边界：旧 `moe_top1_no_lb` 是 hard `argmax` top-1 router，task loss 不能反传到 router。H0525a 只做 corrected A：先验证一个确实有 router 梯度路径的 MoE variant 是否还能复现 B-only / AB 中 B source-token 的 same/split routing pattern。

## 2. Model Variant

主模型：

```text
moe_soft_mixture
```

Forward rule:

\[
p_i(h)=\mathrm{softmax}(W_r h)_i
\]

\[
\mathrm{MoE}(h)=\sum_i p_i(h) E_i(h)
\]

诊断 routing 仍记录：

\[
e^*(h)=\arg\max_i p_i(h)
\]

这样 primary metric 可以和 H0524a 的 expert assignment 指标对齐。

Hard `moe_top1_no_lb` 只作为 gradient audit negative control。

## 3. Data And Training

Data setup 沿用 H0524a:

```text
B_only:       [r, B] -> y_B
AB_composite: [A, B] -> y_AB
CB_composite: [C, B] -> y_CB
```

Seeds:

```text
20260521, 20260522, 20260523, 20260524
```

Training:

```text
steps: 1600
batch size: 384
lr: 0.0008
weight decay: 0.01
```

## 4. Decision Metrics

Primary metric:

```text
final B_in_B_only vs B_in_AB dominant expert same/split by seed
```

This decides whether the H0524a routing pattern survives after the router has a real task-loss gradient path.

Required validity metric:

```text
router.weight/router.bias grad nonzero and router parameter delta > 0
```

This decides whether A is a valid trainable-router reproduction rather than another fixed-boundary run.

## 5. Run Commands

Gradient audit:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search
CUDA_VISIBLE_DEVICES=1 python XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/audit_h0525_router_gradient_path.py \
  --config XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0525a_trainable_router_a_reproduction.json \
  --seed 20260524 \
  --batch-size 64 \
  --out main/experiments/H0521_router_feature_specialization/H0525a_trainable_router_a_reproduction/tables/router_gradient_audit_seed20260524.json \
  --figure-out main/experiments/H0521_router_feature_specialization/H0525a_trainable_router_a_reproduction/figures/router_gradient_audit.png
```

Full run:

```bash
cd XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
python scripts/run_h0525a_trainable_router_a_reproduction.py \
  --config configs/h0525a_trainable_router_a_reproduction.json \
  --run-name h0525a_trainable_router_a_reproduction_10109_20260524 \
  --run-stage full \
  --parallel
```

## 6. Pass / Fail Criteria

Pass validity if `moe_soft_mixture` has nonzero router gradients and nonzero router parameter delta, while hard top-1 remains zero/None.

Pass A reproduction only if the corrected run reproduces the old qualitative H0524a pattern: `3/4` same and seed `20260524` split.

If all or most seeds become same-route under trainable router, H0524a/H0524b should be treated mainly as fixed-router-boundary artifacts and B trajectory should not continue without redesign.
