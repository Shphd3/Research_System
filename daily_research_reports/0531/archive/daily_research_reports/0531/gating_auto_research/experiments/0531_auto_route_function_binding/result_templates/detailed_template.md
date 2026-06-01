# Detailed Result: 0531_auto_route_function_binding

Anchor:

```text
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_gating_anchor.md
```

Story:

```text
在 synthetic NTP 中测试 routing/training 机制是否能形成稳定 route-function binding。
```

## 0. Quick Recap

目的：

```text

```

假设：

```text

```

实验思路：

```text

```

结论：

```text

```

证据：

```text

```

## 1. Anchor Link And Decision Point

Anchor:

Parent question:

This experiment updates:

## 2. Purpose

## 3. Hypothesis And Rival Explanations

## 4. Experiment Logic

## 5. Setup

### Data Construction

### Models

### Training

### Seeds

### Compute / Job IDs

## 6. Primary Metric And Decision Rule

## 7. Main Result

## 8. Key Figures

![route heatmap](figures/route_heatmap_baseline_vs_best.png)

Supports:

```text

```

![forced loss heatmap](figures/forced_loss_heatmap_baseline_vs_best.png)

Supports:

```text

```

![checkpoint trajectory](figures/checkpoint_binding_trajectory.png)

Supports:

```text

```

![factor attribution](figures/factor_attribution_router_logits.png)

Supports:

```text

```

## 9. Evidence Walkthrough

### Single-observation evidence

### Change evidence

### Summary evidence

## 10. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / Failed / Unclear | Failure Reason | What This Rules Out |
|---|---|---|---|---|
| S0 sanity | | | | |
| S1 baseline replication | | | | |
| S2 factor attribution | | | | |
| S3 write-in check | | | | |
| S4 candidate smoke | | | | |
| S5 candidate full | | | | |
| S6 inference stability | | | | |

Falsified physical prior:

```text

```

Falsified operationalization / proxy:

```text

```

Remaining rival explanations:

```text

```

## 11. Goal / Metric Audit, If Triggered

Trigger:

Old goal / metric:

Repeated failure pattern:

Downstream decision:

Revised goal / metric:

Errors now acceptable:

Errors still harmful:

## 12. Full Experiment Record

### Commands

```bash

```

### Configs

```text

```

### Raw/Curated Artifact Paths

```text

```

## 13. Interpretation

## 14. Claim Boundary

## 15. Next Decision

## 16. Links And Artifact Map

```text
anchor:
summary:
detailed:
code workspace:
runner:
config:
key code files:
data / manifest:
result dir:
figure dir:
key tables:
logs / checkpoints:
repro command:
job id:
```
