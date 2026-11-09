# Execution Plan: H0522 Router Factor Audit Seq32

Hypothesis purpose card:

The legacy purpose card was removed; this execution record is retained for
historical audit.

## 1. Run Goal

在 `seq_len=32` 上完成 Stage 1-5：

1. existing-run factor audit；
2. router logit component decomposition；
3. route override；
4. expert-path necessity stress test；
5. factorially disentangled synthetic task。

主判断：

```text
router score/expert id 的主导 factor 是 identity、position、left context、rule/function、target，还是 mixed/seed-dependent cell。
```

## 2. Data Construction

Stage 1-4 使用 H0521b 的 `seq_len=32` A/B/AB contiguous setup。

Stage 5 使用 disentangled `seq_len=32` setup：

```text
same A identity appears in multiple rules
same rule appears across multiple A identities
target and position are balanced
```

## 3. Model / Training / Evaluation Setup

Base model:

```text
top-1 MoE tiny Transformer, no load balance
d_model = 128
n_heads = 4
ffn_dim = 256
num_experts = 4
seq_len = 32
```

Seeds:

```text
20260521, 20260522, 20260523, 20260524
```

Stage 1-3 reuse H0521b trained checkpoints.

Stage 4 trains a residual-reduced MoE stress variant.

Stage 5 trains a disentangled-rule MoE model.

## 4. Configs And Commands

Config:

```text
active/synthetic_data_understanding/configs/h0522_router_factor_audit_seq32.json
```

Runner:

```text
active/synthetic_data_understanding/scripts/run_h0522_router_factor_audit_seq32.py
```

Local smoke:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
python active/synthetic_data_understanding/scripts/run_h0522_router_factor_audit_seq32.py \
  --config active/synthetic_data_understanding/configs/h0522_router_factor_audit_seq32.json \
  --stage h0522_router_factor_audit_seq32 \
  --run-name h0522_router_factor_audit_seq32_smoke \
  --variant all_stages_seq32 \
  --run-stage smoke
```

ACP run uses:

```text
active/attention_search_hier_kv/scripts/cluster/submit_acp_stage.sh
```

## 5. Metrics And Artifacts

Primary:

- factor -> expert id accuracy / NMI;
- router-logit R^2 by factor;
- component removal flip rate;
- forced-routing Delta CE;
- stress-variant expert-path necessity;
- disentangled `NMI(rule, expert_id) - NMI(identity, expert_id)`.

Required figures:

- per-seed factor NMI bar plot;
- per-seed router-logit R^2 plot;
- component flip-rate plot;
- route override Delta CE heatmap;
- stress-test Delta CE plot;
- disentangled rule-vs-identity NMI plot.

## 6. Pass / Fail Criteria

Valid run:

- all four seeds complete;
- Stage 1-5 CSVs exist;
- at least one report-ready figure for each stage exists;
- summary can identify a winning factor or state that no factor is stable.

Failure:

- model does not learn task;
- existing checkpoints cannot be loaded;
- factor records are empty;
- results collapse to one expert for all tokens without interpretable diagnostics.

## 7. Result Location

TBD after ACP completion.
