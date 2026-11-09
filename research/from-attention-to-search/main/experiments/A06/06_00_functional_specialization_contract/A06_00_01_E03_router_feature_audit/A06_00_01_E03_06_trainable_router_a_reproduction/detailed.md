# Detailed Report: H0525a Trainable-Router A Reproduction

## 1. Question

Can the H0524a B-only vs AB B source-token same/split routing pattern be reproduced when the router genuinely receives task-loss gradients and changes parameters?

The decisive metric is:

```text
final B_in_B_only vs B_in_AB dominant expert same/split by seed
```

Reason: this directly tests whether the old qualitative A result survives after correcting the router gradient path.

## 2. Implementation

New model variant:

```text
moe_soft_mixture
```

For hidden state \(h\), the router computes:

\[
p_i(h)=\mathrm{softmax}(W_r h)_i
\]

The MoE output is:

\[
\mathrm{MoE}(h)=\sum_i p_i(h) E_i(h)
\]

The diagnostic expert assignment remains:

\[
e^*(h)=\arg\max_i p_i(h)
\]

This gives a differentiable task-loss path to `router_logits` and `router_probs`, while preserving H0524a-style argmax routing diagnostics.

## 3. Gradient Audit

| Path | Router weight grad norm | Router bias grad norm | Router logits grad | Router probs grad | Router weight delta after step |
|---|---:|---:|---|---|---:|
| hard top-1 negative control | 0.000000 | 0.000000 | None | None | 0.000000 |
| `moe_soft_mixture` | 0.075563 | 0.006685 | nonzero | nonzero | 0.018102 |

Optimizer includes router weight/bias in both paths. The difference is the differentiable weighting path, not optimizer membership.

![Router gradient audit](figures/router_gradient_audit.png)

This figure shows the corrected soft-mixture path has router gradient and parameter update, while hard top-1 has none.

## 4. Training Setup

Run:

```text
h0525a_trainable_router_a_reproduction_10109_20260524
```

Data:

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

## 5. Router Parameter Change During Training

| Seed | Final router weight delta | Final router bias delta | Final router weight grad norm |
|---:|---:|---:|---:|
| 20260521 | 1.737050 | 0.116780 | 0.016737 |
| 20260522 | 1.745191 | 0.170578 | 0.030577 |
| 20260523 | 1.681612 | 0.194535 | 0.027444 |
| 20260524 | 1.683998 | 0.183693 | 0.011527 |

![Router weight delta over training](figures/router_weight_delta_over_training.png)

This figure shows router parameters are not fixed; they move throughout corrected A training.

## 6. Class Readback

| Class | Mean CE | Mean accuracy |
|---|---:|---:|
| A-only | 0.000379 | 0.999844 |
| B-only | 0.000131 | 1.000000 |
| AB-composite | 0.001394 | 0.999844 |
| CB-composite | 0.002607 | 0.999375 |
| background | 8.372727 | 0.008125 |

`background` target is random background token and is not used as task-success evidence.

![Class metrics by seed](figures/class_metrics_by_seed.png)

This figure shows the model learned the signal classes, so the routing judgment is made after successful task learning.

## 7. Init / Final B Routing

| Seed | Init same | Init experts B-only / AB | Final same | Final experts B-only / AB | Final JS | Final logit L2 |
|---:|---:|---|---:|---|---:|---:|
| 20260521 | 1 | 2 / 2 | 1 | 2 / 2 | 0.053950 | 2.7162 |
| 20260522 | 1 | 0 / 0 | 1 | 2 / 2 | 0.016287 | 1.1259 |
| 20260523 | 0 | 2 / 0 | 1 | 0 / 0 | 0.044002 | 1.7970 |
| 20260524 | 1 | 2 / 2 | 1 | 1 / 1 | 0.014881 | 0.9888 |

Main result:

```text
Final same-route = 4/4 seeds.
Final split seed = none.
```

This does not reproduce H0524a, where seed `20260524` split.

![B-context routing by seed](figures/b_context_routing_by_seed.png)

This figure shows the corrected final routing pattern: B-only and AB B source-tokens have the same dominant expert in all four seeds.

![Init vs final B routing by seed](figures/init_vs_final_b_routing_by_seed.png)

This figure shows final routing changes from initialization, but the final corrected pattern removes the old split seed.

## 8. Tables

```text
tables/router_gradient_audit_seed20260524.json
tables/router_delta_over_training_by_seed.csv
tables/init_final_seed_summary.csv
tables/class_metrics.csv
tables/class_metrics_by_seed.csv
```

## 9. Artifact / Repro Map

code workspace:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
```

runner:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0525a_trainable_router_a_reproduction.py
```

config:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0525a_trainable_router_a_reproduction.json
```

result dir:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0525a_trainable_router_a_reproduction/h0525a_trainable_router_a_reproduction_10109_20260524
```

figure dir:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/h0525a_trainable_router_a_reproduction/h0525a_trainable_router_a_reproduction_10109_20260524
```

logs/checkpoints:

```text
results/h0525a_trainable_router_a_reproduction/h0525a_trainable_router_a_reproduction_10109_20260524/moe_soft_mixture/seed_*/model.pt
logs/h0525a_trainable_router_a_reproduction_10109_20260524.log
```

repro command:

```bash
python scripts/run_h0525a_trainable_router_a_reproduction.py \
  --config configs/h0525a_trainable_router_a_reproduction.json \
  --run-name h0525a_trainable_router_a_reproduction_10109_20260524 \
  --run-stage full \
  --parallel
```

job id:

```text
local remote process on 10109, no SCO/ACP job id
```

## 10. Conclusion Boundary

Can claim:

```text
Corrected A is a valid trainable-router run, and it does not reproduce the H0524a split pattern.
```

Cannot claim:

```text
All trainable sparse MoE routers would remove the split.
```

Next decision:

```text
Do not proceed to H0524b-style B trajectory. First redesign the trainable sparse-router condition or rerun factor attribution under corrected routing.
```
