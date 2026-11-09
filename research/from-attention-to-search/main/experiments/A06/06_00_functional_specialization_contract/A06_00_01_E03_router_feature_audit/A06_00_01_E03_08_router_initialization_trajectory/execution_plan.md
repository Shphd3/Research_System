# Execution Plan: H0527a Router Initialization Trajectory

Hypothesis purpose card:

The legacy purpose card was removed; this execution record is retained for
historical audit.

## 1. Run Goal

Compare random router initialization against semantic/context prototype initialization under the same H0526 `top1_selected_gate` no-load-balance setup.

Decision question:

```text
Does semantic initialization produce stable final functional expert specialization, or does training erase the semantic prior?
```

## 2. Data Construction

Use the H0526 AB/CB synthetic setup without changing data generation:

```text
A-only
B-only
AB-composite
CB-composite
background
```

Main B-context diagnostic groups:

```text
B_in_B_only
B_in_AB
B_in_CB
```

Use the same seeds and evaluation batch conventions as H0526 to keep final functional ablation comparable.

## 3. Model / Training / Evaluation Setup

Model:

```text
model_variant: top1_selected_gate
experts: 4
router: linear
selected gate: enabled
active experts per token: 1
load_balance: none
top-2: disabled
z-loss: disabled
```

Conditions:

| Condition | Router init | Purpose |
|---|---|---|
| C0 | default random init | baseline aligned to H0526 |
| C1 | semantic/context prototype init | test whether init controls specialization |

Training:

```text
steps: 1600
batch size: 384
lr: 0.0008
weight decay: 0.01
seeds: 20260521, 20260522, 20260523, 20260524
checkpoint/eval cadence: 0, 100, 200, 400, 800, 1200, 1600
```

Prototype init construction:

```text
1. Collect router-input hidden states from the untrained model.
2. Estimate context centroids for intended groups, especially B-only / AB / CB B-source tokens.
3. Initialize router weights/biases to increase top-1 separation among those centroid groups.
4. Keep all other model initialization and optimizer settings fixed.
```

The exact centroid-to-router mapping must be recorded in `detailed.md`; otherwise the experiment is not reproducible.

## 4. Required Sanity Audit Before Full Run

C1 must pass step-0 checks before full training:

```text
router weight grad norm > 0
router bias grad norm > 0
router logits grad is not None
router weight delta after one optimizer step > 0
active experts per token = 1
no full soft-mixture aggregation
step-0 B-context routing NMI > C0 random-init B-context routing NMI
```

If the final NMI check fails, do not interpret C1 as semantic initialization. Fix prototype construction or run H0527b first.

## 5. Configs And Commands

Planned code artifacts:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0527a_router_initialization_trajectory.json
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0527a_router_initialization_trajectory.py
```

Planned command:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search
python XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0527a_router_initialization_trajectory.py \
  --config XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0527a_router_initialization_trajectory.json
```

Use ignored log/result directories for raw outputs. Commit only reproducible code/configs and curated tables/figures/reports.

## 6. Metrics And Artifacts

Primary metric:

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
\right]
\]

This decides whether AB-specific functional specialization becomes stable.

Validity metric:

```text
step-0 B-context routing NMI improvement over random init
router gradient and delta pass
active experts per token = 1
```

Trajectory diagnostics:

```text
S_AB(t)
B-context routing NMI(t)
token-id routing NMI(t)
load entropy(t)
selected probability(t)
router weight distance from init
router-prototype cosine similarity
class accuracy(t)
```

Required tables:

```text
tables/init_final_routing_nmi.csv
tables/ab_specificity_margin_by_init_seed.csv
tables/router_init_audit.csv
tables/class_metrics_by_init_seed.csv
```

Required figures:

```text
figures/S_AB_trajectory_by_init.png
figures/context_routing_nmi_trajectory_by_init.png
figures/router_prototype_cosine_trajectory.png
figures/init_vs_final_b_context_routing_heatmap.png
figures/class_expert_ablation_delta_by_init.png
```

Every figure in `summary.md` must have one sentence explaining what the figure
shows.

## 7. Pass / Fail Criteria

The experiment is valid only if:

```text
C1 step-0 B-context routing NMI improves over C0
C1 router receives nonzero task-loss gradient
C1 router parameters change after optimizer step
each token activates exactly one expert
training setup matches H0526 except router initialization
```

Decision rule:

```text
If C1 improves step-0 routing but not final stable S_AB, initialization is not decisive.
If C1 improves step-0 routing and stable final S_AB across seeds, initialization is a major causal factor.
If routing remains semantic but S_AB stays low, the failure is route-function mismatch.
```

## 8. Failure Modes To Check

Check these before writing claims:

```text
prototype init accidentally changes non-router parameters
prototype centroids use evaluation labels in a way not documented
condition C0 is not identical to H0526 baseline
selected gate accidentally becomes soft mixture
NMI is computed over all tokens instead of B-source tokens for the context diagnostic
functional ablation renormalizes gates after expert removal
```

## 9. Result Location

Curated report files:

```text
main/experiments/H0521_router_feature_specialization/H0527a_router_initialization_trajectory/summary.md
main/experiments/H0521_router_feature_specialization/H0527a_router_initialization_trajectory/detailed.md
```

Raw logs, checkpoints, and full result dumps should remain in ignored result directories. The committed project mainline should contain only curated small tables, figures, and self-contained reports.
