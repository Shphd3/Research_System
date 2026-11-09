# Execution Plan: H0521b Seq32 Contiguous AB

Hypothesis purpose card:

The legacy purpose card was removed; this execution record is retained for
historical audit.

## 1. Run Goal

在 `seq_len=32` 的连续 `[A,B]` motif-in-context setup 中，判断 source-token gating 是按 A/B/background token identity 分 expert，还是按 feature role、position、context 或 mixed hidden geometry 分 expert。

主指标是：

```text
source-token routing purity, analyzed per seed and intersected across seeds
```

## 2. Data Construction

每条输入是 32 个 token 的 prefix，目标是 next token：

```text
A-only:       background 中插入 [A, r] -> y_A
B-only:       background 中插入 [r, B] -> y_B
AB-composite: background 中插入 [A, B] -> y_AB
background:  全 background token -> r_k
```

控制：

- motif 起点在合法位置均匀采样；
- A-only、B-only、AB-composite 的 motif position 分布一致；
- source-token routing 使用 causal hidden state；
- `[A,B]` 中 A 的 source hidden 看不到后面的 B，B 的 source hidden 可以看到前面的 A。

## 3. Model / Training / Evaluation Setup

Models:

```text
dense tiny Transformer baseline
top-1 MoE tiny Transformer, no load balance
```

Config:

```text
active/synthetic_data_understanding/configs/h0521b_seq32_contiguous_ab.json
```

Runner:

```text
active/synthetic_data_understanding/scripts/run_h0521b_seq32_contiguous_ab.py
```

Main hyperparameters:

```text
seq_len = 32
d_model = 128
n_heads = 4
ffn_dim = 256
num_experts = 4
steps = 1800
batch_size = 384
lr = 8e-4
seeds = 20260521, 20260522, 20260523, 20260524
```

## 4. Metrics And Artifacts

Primary:

- `source_identity_routing_matrix`: A / B / background token routed to which expert;
- `source_role_routing_matrix`: A_in_A_only vs A_in_AB, B_in_B_only vs B_in_AB;
- `seed_rule_summary`: per-seed rules such as A_same_across_context and B_same_across_context;
- `cross_seed_rule_intersection`: only stable rules across seeds enter the main conclusion.

Supporting:

- class accuracy / CE;
- source-position routing matrix;
- prediction-position routing matrix;
- hidden probe;
- figures for identity / role / position routing.

## 5. Commands

Local smoke:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
python active/synthetic_data_understanding/scripts/run_h0521b_seq32_contiguous_ab.py \
  --config active/synthetic_data_understanding/configs/h0521b_seq32_contiguous_ab.json \
  --stage h0521b_seq32_contiguous_ab \
  --run-name h0521b_smoke \
  --variant dense_plus_moe_source_routing \
  --run-stage smoke
```

ACP full run uses:

```text
active/attention_search_hier_kv/scripts/cluster/submit_acp_stage.sh
```

## 6. Pass / Fail Criteria

Valid run:

- dense and MoE learn A/B/AB with high accuracy;
- source-token routing tables are non-empty for A, B, background;
- per-seed rule summary exists for all seeds;
- cross-seed intersection is used for the final judgment.

Decision:

- if A and B token identity route consistently across contexts in all seeds, support token-identity gating;
- if A/B routing changes by role or context, support context-dependent gating;
- if source-position dominates, support position shortcut;
- if only prediction-position routing is structured, source bucket is not enough for feature-level Reverse Index.

## 7. Result Location

ACP run:

```text
job id: pt-tpobuqga
status: SUCCEEDED
```

Runtime log:

```text
active/attention_search_hier_kv/logs/acp/h0521b_seq32_contiguous_ab_4gpu_20260521_20260521_131222.log
```

Result directory:

```text
active/synthetic_data_understanding/results/h0521b_seq32_contiguous_ab/h0521b_seq32_contiguous_ab_4gpu_20260521/
```

Figure directory:

```text
active/synthetic_data_understanding/figures/h0521b_seq32_contiguous_ab/h0521b_seq32_contiguous_ab_4gpu_20260521/
```

Local report documents:

```text
Projects/from-attention-to-search/main/experiments/A06/06_00_functional_specialization_contract/A06_00_01_E03_router_feature_audit/A06_00_01_E03_02_seq32_contiguous_ab/summary.md
Projects/from-attention-to-search/main/experiments/H0521_router_feature_specialization/H0521b_seq32_contiguous_ab/detailed.md
```
