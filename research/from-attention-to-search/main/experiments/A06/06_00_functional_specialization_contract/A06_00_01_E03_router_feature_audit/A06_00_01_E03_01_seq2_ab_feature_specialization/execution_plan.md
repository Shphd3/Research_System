# Execution Plan: H0521 AB Feature Specialization

Hypothesis purpose card:

The legacy purpose card was removed; this execution record is retained for
historical audit.

## 1. Run Goal

判断普通 no-load-balance top-1 MoE 在最小 A/B/AB synthetic setup 中，是按 feature 分 expert，还是把 A-only、B-only、AB-composite 放进同一个 mixed token-context bundle。

第一版同时保留两个模型：

- dense tiny Transformer baseline：确认任务可学；
- no-load-balance top-1 MoE tiny Transformer：诊断 router / expert cell。

## 2. Data Construction

输入是长度为 2 的 prefix，目标是下一 token：

```text
A-only:       [A, r] -> y_A
B-only:       [r, B] -> y_B
AB-composite: [A, B] -> y_AB
background:  [r_i, r_j] -> r_k
```

其中 \(r, r_i, r_j, r_k\) 都来自非特殊 background token。background 沿用之前 synthetic 实验的原则：它不是 planted feature prefix，target 是普通随机背景 next token，不承载 A/B/AB 规则。

第一版保持四类样本计数平衡。

## 3. Model / Training / Evaluation Setup

Workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

Config:

```text
active/synthetic_data_understanding/configs/h0521_ab_feature_specialization.json
```

Runner:

```text
active/synthetic_data_understanding/scripts/run_h0521_ab_feature_specialization.py
```

Default full run:

- seeds: `20260521, 20260522, 20260523, 20260524`
- train samples per class: `6000`
- eval samples per class: `1600`
- model: `d_model=96`, `n_heads=4`, `ffn_dim=192`
- MoE experts: `4`
- training steps: `1600`

## 4. Metrics And Artifacts

Most important metric:

```text
class-specific expert ablation delta CE
```

It answers whether removing expert `e` mainly hurts A-only, B-only, AB-composite, background, or several classes together. This decides whether an expert is feature-specific or shared-functional.

Supporting metrics:

- class accuracy / CE: confirm dense and MoE learn the task;
- routing matrix: class-to-expert assignment;
- forced routing: whether router-chosen expert is functionally best;
- within-expert commonality audit: for each expert, class composition, signal fraction, dominant class, class entropy, affected classes;
- hidden probe: whether hidden state retains A/B/AB/background class information.

Expected output:

```text
active/synthetic_data_understanding/results/h0521_ab_feature_specialization/<run_name>/
active/synthetic_data_understanding/figures/h0521_ab_feature_specialization/<run_name>/
```

## 5. Commands

Local smoke:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
python active/synthetic_data_understanding/scripts/run_h0521_ab_feature_specialization.py \
  --config active/synthetic_data_understanding/configs/h0521_ab_feature_specialization.json \
  --stage h0521_ab_feature_specialization \
  --run-name h0521_smoke \
  --variant dense_plus_moe \
  --run-stage smoke
```

ACP 4-card full run uses:

```text
active/attention_search_hier_kv/scripts/cluster/submit_acp_stage.sh
```

with:

```text
TASK_ENTRYPOINT=active/synthetic_data_understanding/scripts/run_h0521_ab_feature_specialization.py
CONFIG_PATH=/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0521_ab_feature_specialization.json
GPU_COUNT=4
WORKER_SPEC=n6ls.iu.i40.4
RUN_STAGE=full
```

## 6. Pass / Fail Criteria

Valid run requires:

- dense baseline learns A-only, B-only, AB-composite with high accuracy;
- MoE learns the same task well enough that routing diagnostics are meaningful;
- result folder contains class metrics, routing matrix, ablation deltas, forced routing, commonality audit, hidden probe, and figures.

Main hypothesis support:

- support bundle routing if one expert receives A/B/AB together and ablation hurts multiple signal classes;
- support feature specialization if A-only, B-only, and AB-composite route to different experts and each expert's ablation mostly hurts its own class;
- redirect if dense learns but MoE fails or if routing is mixed but function is separated.

## 7. Result Location

ACP full run:

```text
job id: pt-527v9od5
job name: ats-h0521-ab-feature-specialization-4gpu-guaranteed
status: SUCCEEDED
submit log: active/attention_search_hier_kv/logs/acp/h0521_ab_feature_specialization_4gpu_guaranteed_20260521_submit_20260521_104207.log
runtime log: active/attention_search_hier_kv/logs/acp/h0521_ab_feature_specialization_4gpu_guaranteed_20260521_20260521_104425.log
result dir: active/synthetic_data_understanding/results/h0521_ab_feature_specialization/h0521_ab_feature_specialization_4gpu_guaranteed_20260521/
figure dir: active/synthetic_data_understanding/figures/h0521_ab_feature_specialization/h0521_ab_feature_specialization_4gpu_guaranteed_20260521/
```
