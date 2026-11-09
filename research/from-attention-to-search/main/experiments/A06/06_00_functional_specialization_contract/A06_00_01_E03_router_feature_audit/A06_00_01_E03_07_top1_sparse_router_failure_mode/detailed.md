# Detailed Report: H0526 Top-1 Sparse Router Failure Mode

## 1. Question

In a truly top-1 sparse MoE where the selected router probability multiplies the selected expert output, does ordinary no-load-balance training form functional expert specialization on the AB/CB synthetic setup?

The most important research metric is class-specific expert ablation delta:

\[
\Delta L_{c,e}=L_c(\text{ablate expert }e)-L_c(\text{full model}).
\]

The main specialization score is:

\[
S_{AB}
=
\max_e
\left[
\Delta L_{AB,e}
-
\max
\left(
\Delta L_{A,e},
\Delta L_{B,e},
\Delta L_{CB,e}
\right)
\right].
\]

Routing heatmaps are secondary. They explain route assignment, but do not decide whether an expert is functional.

## 2. Implementation

C1 model:

```text
top1_selected_gate
```

Forward:

\[
p=\mathrm{softmax}(W_rh)
\]

\[
s=\arg\max_e p_e
\]

\[
y(h)=p_s(h)E_s(h)
\]

The selected gate is not renormalized to 1. Each token activates exactly one expert, and the selected probability gives a continuous task-loss path to router logits.

External reference:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/docs/external_resources/qwen3_moe/
```

The reference is copied only as a dispatch-structure guide. H0526 runtime code is local and minimal.

## 3. Validity Audit

| Condition | Router weight grad | Router bias grad | Router logits grad | Router probs grad | Router weight delta | Active experts / token | Full soft mixture |
|---|---:|---:|---|---|---:|---:|---|
| hard top-1 no-gate | 0.000000 | 0.000000 | None | None | 0.000000 | 1 | false |
| top-1 selected gate | 0.043496 | 0.003369 | nonzero | nonzero | 0.018101 | 1 | false |

Conclusion:

```text
C1 is implementation-valid: sparse top-1 dispatch and router task-loss gradient both hold.
```

## 4. Training Setup

Run:

```text
h0526_top1_sparse_router_failure_mode_10109_20260524
```

Data:

```text
A-only, B-only, AB-composite, CB-composite, background
```

Seeds:

```text
20260521, 20260522, 20260523, 20260524
```

Training:

```text
1600 steps, batch size 384, lr 0.0008, weight decay 0.01
```

## 5. Task Readback

| Class | Mean CE | Mean accuracy |
|---|---:|---:|
| A-only | 0.000167 | 1.000000 |
| B-only | 0.000442 | 0.999844 |
| AB-composite | 0.001978 | 0.999688 |
| CB-composite | 0.010247 | 0.999063 |
| background | 8.445251 | 0.008281 |

`background` target is random and is not task-success evidence.

## 6. Functional Ablation

Per-seed \(S_{AB}\):

| Seed | \(S_{AB}\) | Interpretation |
|---:|---:|---|
| 20260521 | -0.0006 | no AB-specific expert |
| 20260522 | 0.0064 | near zero |
| 20260523 | 0.7093 | strong AB-specific expert |
| 20260524 | 0.0014 | near zero |

![Class expert ablation delta heatmap](figures/class_expert_ablation_delta_heatmap.png)

This figure shows the decisive evidence: AB-specific functional specialization appears strongly in only one seed.

Route-function alignment highlights one clear mismatch:

```text
seed 20260524, AB-composite:
dominant route expert = E0
dominant-route CE delta = 0.0014
max CE delta = 0.1388 at E2
alignment = 0.0102
```

This means the dominant routed expert is not the causal expert for AB in that seed.

## 7. Routing And Load Diagnostics

B-context routing:

![B context routing by seed](figures/b_context_routing_by_seed.png)

This figure shows B-source routing for `B_in_B_only`, `B_in_AB`, and `B_in_CB`. It varies by seed; split/same is not sufficient to decide specialization.

Final load entropy:

| Seed | Load entropy | Dominant expert fraction |
|---:|---:|---:|
| 20260521 | 1.1098 | 0.5132 |
| 20260522 | 1.1738 | 0.5384 |
| 20260523 | 0.9873 | 0.6676 |
| 20260524 | 1.1635 | 0.5483 |

![Load trajectory by seed](figures/load_trajectory_by_seed.png)

This figure shows moderate load imbalance, with seed `20260523` the most imbalanced. It is not complete expert collapse.

![Selected probability trajectory by seed](figures/selected_prob_trajectory_by_seed.png)

This figure shows selected gate confidence increases during training, especially in seed `20260521`.

## 8. Tables

```text
tables/gradient_audit.csv
tables/class_metrics_by_seed.csv
tables/load_entropy_by_seed.csv
tables/ablation_delta_class_expert.csv
tables/ab_specificity_margin_by_seed.csv
tables/route_function_alignment_by_seed.csv
tables/b_context_routing_by_seed.csv
```

## 9. Artifact / Repro Map

code workspace:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
```

src:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/src/synthetic_data_understanding/
```

runner:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0526_top1_sparse_router_failure_mode.py
```

config:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0526_top1_sparse_router_failure_mode.json
```

remote raw result dir:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0526_top1_sparse_router_failure_mode/h0526_top1_sparse_router_failure_mode_10109_20260524
```

remote figure dir:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/h0526_top1_sparse_router_failure_mode/h0526_top1_sparse_router_failure_mode_10109_20260524
```

checkpoints/logs:

```text
results/h0526_top1_sparse_router_failure_mode/h0526_top1_sparse_router_failure_mode_10109_20260524/top1_selected_gate/seed_*/model.pt
```

repro command:

```bash
python scripts/run_h0526_top1_sparse_router_failure_mode.py \
  --config configs/h0526_top1_sparse_router_failure_mode.json \
  --run-name h0526_top1_sparse_router_failure_mode_10109_20260524 \
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
No-load-balance top-1 selected-gate sparse router is trainable and task-capable, but does not reliably form stable AB-specific functional expert specialization across seeds.
```

Cannot claim:

```text
Sparse MoE generally fails, or load-balanced/top-2 variants behave the same.
```

Next decision:

```text
Add only load-balance loss next, and keep ablation delta / S_AB as the decision metric.
```
