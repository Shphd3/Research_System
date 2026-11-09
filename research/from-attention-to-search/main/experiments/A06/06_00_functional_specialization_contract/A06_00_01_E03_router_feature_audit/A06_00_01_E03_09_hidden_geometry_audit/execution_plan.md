# Execution Plan: H0527b Hidden Geometry Audit

Hypothesis purpose card:

The legacy purpose card was removed; this execution record is retained for
historical audit.

## 1. Run Goal

Do not retrain. Use H0526 `top1_selected_gate` checkpoints to answer:

```text
Is B-context semantic information linearly accessible at the router input, and does the learned router align with it?
```

This experiment is first in the H0527 sequence because it decides whether semantic router initialization is likely to be a meaningful causal intervention.

## 2. Data Construction

Use the same AB/CB synthetic setup as H0526:

```text
A-only
B-only
AB-composite
CB-composite
background
```

Evaluation batches should be deterministic per seed and large enough for stable probes. Recommended minimum:

```text
examples per class per checkpoint: >= 4096
source-token hidden states only for PCA/probe main plots
B-source subset for context-role probes
```

Labels to attach to each hidden state:

```text
token_id: A/B/C/r/background
position: source/query/background
context_role: A-only/B-only/AB/CB/background
target_class: y_A/y_B/y_AB/y_CB/background
routed_expert
selected_probability
seed
step
```

## 3. Model / Checkpoint Setup

Analyze H0526 model:

```text
model_variant: top1_selected_gate
load_balance: none
experts: 4
seeds: 20260521, 20260522, 20260523, 20260524
steps: 0, 100, 200, 400, 800, 1200, 1600
```

Checkpoint source:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0526_top1_sparse_router_failure_mode/
```

If intermediate checkpoints are missing, rerun the H0526 training script with checkpoint saving at the listed steps and the same config. This replay must not change model, data, optimizer, seeds, or training hyperparameters.

## 4. Configs And Commands

Planned code artifacts:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0527b_hidden_geometry_audit.json
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0527b_hidden_geometry_audit.py
```

Planned command:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search
python XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0527b_hidden_geometry_audit.py \
  --config XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0527b_hidden_geometry_audit.json
```

No full training command belongs to the primary path. Only use a checkpoint replay if required by missing artifacts.

## 5. Metrics And Artifacts

Primary metric 1:

\[
P_{\text{ctx}|B}=\mathrm{Acc}(\text{linear probe}: h_B \rightarrow \kappa)
\]

This decides whether B-context role is linearly available to the router input.

Primary metric 2:

\[
A_{\text{ctx}}=\max_{e,j}|\cos(w_e-w_j,u_{\text{ctx}})|
\]

This decides whether the trained router uses a boundary aligned with B-context information.

Supporting metrics:

```text
P_token
A_token
token variance ratio
B-context variance ratio
selected probability by seed/step
route distribution by token/context
```

Required tables:

```text
tables/probe_accuracy_by_seed_step.csv
tables/router_alignment_by_seed_step.csv
tables/variance_ratio_by_seed_step.csv
tables/hidden_collection_manifest.csv
```

Required figures:

```text
figures/pca_token_vs_context.png
figures/linear_probe_token_vs_context_trajectory.png
figures/router_boundary_alignment_trajectory.png
figures/variance_ratio_token_vs_context_trajectory.png
```

Each report figure must include a one-sentence caption explaining what it supports.

## 6. Pass / Fail Criteria

Valid audit requires:

```text
all four H0526 seeds loaded
all requested steps loaded or explicitly marked unavailable
probe train/test split separated within each seed/step
linear probe uses only router input h
PCA is not used as the primary decision metric
```

Decision rule:

```text
If P_ctx|B is low while P_token is high, hidden geometry supports token dispatch more than context dispatch.
If P_ctx|B is high but A_ctx is low, context information exists but router does not align with it.
If P_ctx|B and A_ctx are both high while S_AB remains low, the bottleneck is expert-function mismatch.
```

## 7. Failure Modes To Check

Check these before interpreting results:

```text
probe data leakage across train/test split
class imbalance in B-only / AB / CB labels
PCA fitted on a different distribution than plotted
hidden state captured after router instead of before router
missing or mismatched checkpoint configs
linear probe overfitting from too few samples
```

## 8. Result Location

Curated report files:

```text
main/experiments/H0521_router_feature_specialization/H0527b_hidden_geometry_audit/summary.md
main/experiments/H0521_router_feature_specialization/H0527b_hidden_geometry_audit/detailed.md
```

Raw or large artifacts should remain under ignored result/log directories. Only curated tables, figures, and self-contained reports should be committed.
