# Real Hierarchical Training Experiment Plan

本文档定义一个待执行的真实数据层级训练实验计划。它参考：

- `/data/250010109/MoE_Router/experiments/active/exp_hierarchical/2026-05-05-real_dclm_qwen3_hier_moe`
- `docs/flat_real_inference.md`
- `docs/model_design.md`

本计划不表示训练已经完成；“训练 1B 真实数据”仅指后续实验的训练预算：在真实 DCLM/Qwen token 流或由 Qwen 轨迹导出的 hidden/KV 流上，累计看到约 `1e9` 个训练 token/positions。

## 1. 目标

验证一个问题：

```text
在真实 DCLM/Qwen 长上下文轨迹上，训练出的 hierarchical KV indexing router
能否用更少历史 KV 候选接近 full KV cache attention，
并优于 flat 16-bucket indexing。
```

核心对比：

- `full_kv`: 原生 full KV cache attention，作为质量真值。
- `flat_indexed_kv_16`: 16 个 leaf buckets 的 flat KV index。
- `hier_indexed_kv_4x4`: `C=4,F=4,M=16` 的两级 KV index。
- `oracle_topm`: 用 full attention logits 选候选，只作误差下界和召回上限。

本实验目标是 attention-as-search / hierarchical KV indexing，不是复刻 MoE_Router 的专家机制解释实验。参考实验中的经验只迁移为训练组织、对照设置和分析方法。

## 2. 数据

固定真实数据源：

```text
/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10
```

训练预算：

```yaml
train_budget_tokens: 1_000_000_000
seed: 20260510
dataset_format: binary DCLM token stream
model_family: qwen3.6-plus trajectory, or compatible Qwen hidden/KV extraction pipeline
```

说明：

- 训练预算按真实 token 流或 hidden/KV position 计数，不能写成已经完成的 1B 训练结果。
- 若直接训练 router/indexer，样本来自 Qwen full-attention teacher-forcing 轨迹中的 `q/k/v/full attention logits/probs`。
- 若先离线抽取 hidden/KV，抽取文件只作为本地运行产物，不进入可 push 范围。

数据切分：

```text
train: 约 1B token/positions，用于 router/indexer 训练
valid: 固定 held-out offsets，约 8M token/positions，用于调参和早停
test: 与 flat_real_inference.md 相同采样协议，用于 full KV vs indexed KV 最终对比
```

test 采样沿用：

```text
context_len = [2048, 4096, 8192, 16384]
decode_len = 32
sample_count_per_context = 8
teacher_forcing = true
```

## 3. 模型结构

### 3.1 Full KV baseline

`full_kv` 不训练 router，不做候选裁剪：

```text
S_t = {0, ..., t-1}
attn_out_full = softmax(q_t K[0:t]^T / sqrt(d_h)) V[0:t]
```

它只用于提供 full logits/probs、attention output、next-token logits 的真值。

### 3.2 Flat indexed KV

flat baseline 使用 16 个 leaf buckets：

```text
route_key(k_i) -> m in {0, ..., 15}
route_query(q_t) -> top-B leaf buckets
S_t = union selected buckets + local_window
```

候选集合内必须回到原始 K/V 做 exact attention。index score 只能用于召回，不能作为 attention logit。

### 3.3 Hierarchical indexed KV

主实验使用 `C=4,F=4,M=16`：

```text
route_key(k_i) -> (c_i, f_i), leaf = 4 * c_i + f_i
route_query(q_t) -> top coarse groups, then top fine leaves
S_t = union selected hierarchical leaf buckets + local_window
```

建议实现两个层级版本：

- `hier_A_same_repr`: coarse/fine router 都看同一输入表征，回答“拆成两层本身是否有收益”。
- `hier_B_spectral_repr`: 借鉴参考实验的 `spectral_ema` 经验，coarse 看较粗谱段，fine 看更细谱段；谱段只用于 routing，不改变最终 attention 计算。

对齐 `model_design.md` 的约束：

- flat 与 hierarchical 都保持 16 个 leaf buckets。
- hierarchical 不是 100 experts，也不是改变 full attention 真值。
- GQA/MQA 下必须记录 `q_head_id -> kv_head_id`。

## 4. 训练阶段

### Stage 0: 轨迹与 smoke

目标是确认 teacher 信号可信：

1. 加载 Qwen 和 DCLM token bin。
2. 在小样本上运行 full KV teacher-forcing。
3. 保存或重放 RoPE 后 `q/k/v`。
4. 离线重算 full attention，校验：

```text
relative_L2(attn_out_replay, attn_out_model) <= 1e-4
top1(next_token_logits_replay) == top1(next_token_logits_model)
```

该阶段不计入 1B 训练预算。

### Stage 1: 小规模 router 试训

预算：

```yaml
tokens: 10M to 50M
context_len: 1024 or 2048
candidate_budget: [128, 512]
local_window: 128
```

产物：

- flat 与 hierarchical 均能跑通。
- 无 NaN/OOM。
- bucket usage、coarse/fine usage、candidate recall 可记录。
- full replay smoke 仍通过。

### Stage 2: 1B 真实数据训练

预算定义：

```yaml
train_budget_tokens: 1_000_000_000
seq_len: 1024 initially, then optional 2048
global_batch_positions: 参考硬件容量固定
lr: 以小规模试训稳定值为准
warmup_steps: 参考实验经验，显式记录，不和总训练步混淆
seed: 20260510
data_shuffle: fixed or disabled, but flat/hier must match
```

训练目标建议：

- `route_key`/`route_query` 的监督来自 full attention top tokens 或 attention mass bucket 标签。
- 可用 loss：top-K token recall loss、bucket-level contrastive loss、mass recall surrogate。
- 不把 approximate score 训练成最终 attention logit；最终质量必须由 exact rerank 后的 sparse attention 评估。

参考实验迁移规则：

- 成对提交 flat/hier，确保同 seed、同数据顺序、同 token budget。
- 像参考实验一样记录 `Total training tokens`、真实 optimizer steps、warmup、checkpoint tag。
- load-balance 若使用，必须作为控制变量单独标注；首轮建议 `lambda_lb=0` 或仅 warmup 使用，避免把均匀分桶误当作检索质量。
- 保持 16 leaf path 对齐，hier 只多 coarse/fine 层级，不扩大候选容量。

### Stage 3: checkpoint 选择

至少保存：

```text
checkpoint-early
checkpoint-mid
checkpoint-final
```

选择标准优先级：

1. valid `mass_recall`。
2. valid `relative_L2_attn_out`。
3. bucket usage 不坍塌。
4. lookup/index 插入开销稳定。

## 5. 评估阶段

评估必须复用 `flat_real_inference.md` 的 full KV vs indexed KV 形式。

### 5.1 Full KV 真值

对 test samples 记录或可重放：

```text
q_full
k_cache_full
v_cache_full
attn_logits_full
attn_probs_full
attn_out_full
next_token_logits_full
```

### 5.2 Indexed KV 方法

对每个 decode step、layer、KV head：

1. prefill 时按 `route_key(k_i)` 插入 flat/hier index。
2. decode 时按 `route_query(q_t)` 取 buckets。
3. 合并 `local_window`。
4. 若候选超过 budget，优先保留 local window，其余按 router/index score 截断。
5. 对候选原始 K/V 做 exact rerank 和 sparse softmax。
6. 与 full attention output 对比。

扫描：

```text
candidate_budget = [64, 128, 256, 512, 1024]
local_window = 128
top_bucket_count = [1, 2, 4]
hier_coarse_count = [1, 2]
```

`oracle_topm` 必须同步跑，用来判断误差来自候选预算不足，还是 router/index 召回不足。

## 6. Full KV vs Indexed KV 对比

最终表格至少包含：

```text
full_kv
oracle_topm
flat_indexed_kv_16
hier_A_indexed_kv_4x4
hier_B_indexed_kv_4x4
```

必须控制：

- 同一 test samples。
- 同一 Qwen 权重和 attention backend。
- 同一 dtype。
- 同一 candidate budget。
- 同一 local window。
- 同一 exact rerank 实现。
- 同一 layer/head 范围。
- 同一 teacher-forcing decode 轨迹。

结论写法应是：

```text
在 candidate_ratio = X% 时，hier indexed KV 相比 full KV 的误差为 Y，
相比 flat indexed KV 的 recall/误差/延迟变化为 Z。
```

不能只报告 loss，也不能只报告 router usage。

## 7. 指标

### 7.1 质量指标

```text
top1_recall
top8_recall
top32_recall
mass_recall
relative_L2_attn_out
cosine_error_attn_out
max_abs_error_attn_out
```

若完成 logits 注入或 layer replay：

```text
KL(full || indexed)
top1_logits_agreement
top5_logits_agreement
gold_token_logprob_delta
```

### 7.2 系统指标

```text
candidate_count
candidate_ratio
lookup_latency_us
candidate_materialize_latency_us
rerank_latency_us
sparse_attention_latency_us
index_insert_latency_us
total_indexed_attention_latency_us
full_attention_latency_us
kv_cache_memory_mb
index_memory_mb
```

### 7.3 层级结构指标

从参考实验迁移，但解释为 KV index 结构：

```text
leaf_usage_norm
active_leaf_buckets
coarse_usage_norm
active_coarse_buckets
coarse_within_vs_between_distance
query_key_bucket_agreement
bucket_attention_mass_concentration
```

这些指标只说明结构是否成形，不能替代 full KV vs indexed KV 质量指标。

## 8. 最小里程碑

M0 文档与配置：

- 本计划文档落地。
- 明确 run config schema。
- 不运行训练。

M1 smoke：

- 小样本 full KV replay 通过。
- flat/hier index 能构建并返回合法历史候选。

M2 试训：

- 10M-50M 真实 token/positions router 训练跑通。
- flat 与 hier 有同等预算结果。

M3 1B 训练：

- flat 与 hier 在同一真实数据预算下完成 `1e9` token/positions 训练。
- 记录 checkpoint、训练步数、warmup、loss、usage。

M4 full KV vs indexed KV：

- test context `[2048, 4096, 8192]` 必跑。
- `[16384]` 尽量跑，若硬件不足要写明。
- 输出按 context/layer/head 的 summary。

M5 结论：

- 写清 hierarchical 是否优于 flat。
- 写清差距来自 recall、attention output error、logits propagation，还是系统开销。

## 9. 控制变量

必须固定或显式记录：

```yaml
dataset_root: /data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10
seed: 20260510
model_name: qwen3.6-plus
dtype: bf16 or fp16
attention_backend: recorded
context_len: [2048, 4096, 8192, 16384]
decode_len: 32
candidate_budget: [64, 128, 256, 512, 1024]
local_window: 128
leaf_buckets: 16
hier_factorization: 4x4
exact_rerank: true
teacher_forcing: true
```

禁止混入的变量：

- hierarchical 使用更多 leaf buckets。
- indexed 方法直接使用 approximate score 作为 attention logits。
- flat/hier 使用不同训练数据顺序。
- 对 full KV baseline 使用不同 backend 或 dtype。
- 用训练集 offsets 作为最终 test。

## 10. 输出与可 push 文件边界

建议 run 目录：

```text
runs/real_hierarchical_training/{run_id}/
  config.yaml
  samples.jsonl
  metrics_step.parquet
  summary_by_context.csv
  summary_by_layer_head.csv
  summary_by_method.csv
  README.md
```

本轮计划阶段可 push：

```text
docs/real_hierarchical_training_experiment.md
```

后续实现阶段可 push：

```text
configs/*.yaml
scripts/*.py
scripts/*.sh
docs/*.md
small smoke metadata or tiny json examples
```

不可 push：

```text
checkpoints/
large hidden/KV dumps
large parquet/jsonl metrics
raw DCLM data
logs with large tensor dumps
Research_System changes
```

本次任务明确不修改 `Research_System`，不启动训练，不生成大数据。

