# Flat Real Inference: 最小可执行实验

本文档只定义一个最小实验：在真实 `qwen3.6-plus` 推理中，测量
`indexed/backward KV candidate attention` 和 `full KV cache attention`
到底差多少。实验目标是先得到可信的误差和开销数字，不扩展成长期路线图。

## 1. 目标

回答一个问题：

```text
对 qwen3.6-plus，在 DCLM 长上下文上，
先从历史 KV 中检索少量 candidate，再对 candidate 做 exact attention，
相比完整 full KV cache attention，质量误差和系统开销分别是多少？
```

必须固定：

- 模型：`qwen3.6-plus`。
- 数据集：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10`。
- 真值：模型原生 `full KV cache attention`。
- 待测方法：`indexed/backward KV candidate attention`，候选生成后必须用原始 K/V 做 exact rerank 和 sparse softmax。

不在本实验中做：

- 不训练或改模型权重。
- 不修改 `docs/architecture.md`。
- 不用其他模型替代 `qwen3.6-plus`；如果模型不可加载，只记录 `model_available=false`。

## 2. 输入与固定配置

### 2.1 数据输入

从以下目录读取 DCLM token bin：

```text
/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10
```

取样规则：

```text
seed = 20260510
bin_files = sorted(*_processed.bin)
sample_count_per_context = 8
context_len = [2048, 4096, 8192, 16384]
decode_len = 32
guard_len = 32
batch_size = 1
dtype = bf16 if supported else fp16
decode_mode = teacher_forcing
```

每个样本从某个 bin 中截取：

```text
context_len + decode_len + guard_len
```

其中：

- 前 `context_len` token 作为 prefill prompt。
- 后 `decode_len` token 只用于 teacher-forcing，不允许参与 candidate retrieval。
- `guard_len` 只用于避免越界和格式校验，不参与评估。

### 2.2 样本清单

生成 `samples.jsonl`，每行至少包含：

```json
{
  "sample_id": "ctx8192_000",
  "source_file": "xxx_processed.bin",
  "start_offset": 123456,
  "context_len": 8192,
  "decode_len": 32,
  "seed": 20260510
}
```

## 3. Baseline: Full KV Cache Attention

baseline 是模型原生 attention：不裁剪、不索引、不近似。它提供所有指标的真值。

对每个 `(sample_id, decode_step, layer_id, head_id)` 记录或可重放得到：

```text
q_full                  # RoPE 后、真正进入 dot product 的 query
k_cache_full            # 历史 K cache，位置范围 [0, t)
v_cache_full            # 历史 V cache，位置范围 [0, t)
attn_logits_full        # q @ K^T / sqrt(head_dim)
attn_probs_full         # softmax(attn_logits_full + mask)
attn_out_full           # full attention output
next_token_logits_full  # LM head 输出
```

如果 attention backend 无法直接暴露 logits/probs，必须保存 RoPE 后的 `q/k/v`，离线重算：

```text
attn_logits_full = q_full @ k_cache_full.T / sqrt(head_dim)
attn_probs_full = softmax(attn_logits_full + causal_mask)
attn_out_full = attn_probs_full @ v_cache_full
```

smoke 校验：

```text
relative_L2(attn_out_replay, attn_out_model) <= 1e-4
top1(next_token_logits_replay) == top1(next_token_logits_model)
```

校验不通过时停止后续 indexed 实验。

## 4. Indexed/Backward KV Candidate Attention

indexed 方法保持原始 KV cache 不变，只新增候选检索路径。

对每个解码位置 `t`：

```text
q_t
-> backward/index lookup over historical K[0:t)
-> candidate positions C_t
-> exact rerank: q_t @ K[C_t].T / sqrt(head_dim)
-> sparse softmax over C_t
-> attn_out_indexed = softmax(logits_C) @ V[C_t]
```

约束：

- `C_t` 只能包含历史位置 `< t`。
- 最终 attention score 必须来自原始 K 的 exact dot product。
- approximate/index score 只能用于候选召回，不能直接作为 attention logit。
- 每个 `(layer_id, kv_head_id)` 独立维护 index。
- 如果是 GQA/MQA，记录 `q_head_id -> kv_head_id` 映射。

### 4.1 最小 candidate 方案

本最小实验只实现两个 candidate source：

1. `oracle_topm`：用 full logits 取 top-M。它不可部署，只给误差下界。
2. `backward_vector_index`：对历史 K 做近似检索，返回 candidate，再 exact rerank。

`backward_vector_index` 的最小实现可以是以下任一可在线维护结构：

- IVF/coarse centroid；
- HNSW/FAISS；
- LSH/random projection bucket；
- 现有代码库中已有的 layer/head KV index。

实现者任选一种，但输出字段必须一致。

### 4.2 Candidate Budget

扫描以下预算：

```text
candidate_budget = [64, 128, 256, 512, 1024]
local_window = 128
```

实际候选：

```text
C_t = unique(index_candidates union {t-local_window, ..., t-1})
```

如果去重后超过 `candidate_budget`：

1. 优先保留 local window。
2. 剩余名额按 index score 截断。

记录：

```text
candidate_ratio = len(C_t) / t
```

## 5. 执行步骤

### Step 1: 生成样本

1. 枚举并排序 `*_processed.bin`。
2. 使用固定 seed 选择 `(file_id, start_offset, context_len)`。
3. 写出 `samples.jsonl`。
4. 确认每条样本长度至少为 `context_len + decode_len + guard_len`。

### Step 2: 跑 full baseline

对每条样本：

1. prefill 前 `context_len` token。
2. teacher-forcing 解码 `decode_len` 步。
3. 每步记录 full attention 真值和 `next_token_logits_full`。
4. 保存必要 tensor 或 tensor reference。

### Step 3: 跑 oracle_topm

对同一批 baseline 记录：

1. 从 `attn_logits_full` 中取 top-M 历史位置。
2. 合并 local window。
3. 对候选位置重新计算 exact sparse attention。
4. 计算 indexed output 和 full output 的差异。

该步骤回答：即使候选完美，少量 KV 是否足够复现 full attention。

### Step 4: 跑 backward_vector_index

对每条样本、每层、每个 KV head：

1. prefill 时把历史 K 按位置插入 index。
2. 每个 decode step 用当前 `q_t` 查询历史 index。
3. 合并 local window 得到 `C_t`。
4. 用原始 K/V 对 `C_t` 做 exact rerank 和 sparse attention。
5. 在 teacher-forcing 轨迹上比较 `attn_out_indexed` 与 `attn_out_full`。
6. 每步把新 token 的 K/V 插入 index。

### Step 5: 可选 logits 传播检查

如果实现成本可控，增加 shadow mode：

1. 模型仍用 full attention 生成主轨迹。
2. indexed attention 并行计算。
3. 将 indexed attention output 注入后续层或整层 replay，得到 `next_token_logits_indexed`。
4. 比较 full 与 indexed 的 next-token logits。

如果暂时不能做完整注入，必须至少完成 attention-output 级别评估。

## 6. 必须记录的内容

### 6.1 Run 配置

写入 `config.yaml`：

```yaml
model_name: qwen3.6-plus
model_available: true
dataset_root: /data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10
seed: 20260510
context_len: [2048, 4096, 8192, 16384]
decode_len: 32
candidate_budget: [64, 128, 256, 512, 1024]
local_window: 128
candidate_methods: [oracle_topm, backward_vector_index]
dtype: bf16
attention_backend: "<backend name>"
gpu: "<gpu name>"
```

### 6.2 每步指标记录

写入 `metrics_step.parquet` 或 `metrics_step.jsonl`：

```text
run_id
sample_id
context_len
decode_step
layer_id
q_head_id
kv_head_id
candidate_method
candidate_budget
local_window
candidate_count
candidate_ratio
top1_recall
top8_recall
top32_recall
mass_recall
relative_L2_attn_out
cosine_error_attn_out
max_abs_error_attn_out
kl_full_indexed_logits
top1_logits_agreement
lookup_latency_us
rerank_latency_us
sparse_attention_latency_us
index_insert_latency_us
```

如果没有做 logits 注入：

```text
kl_full_indexed_logits = null
top1_logits_agreement = null
```

### 6.3 Candidate 事件记录

写入 `events_index.jsonl`：

```json
{
  "sample_id": "ctx8192_000",
  "decode_step": 7,
  "layer_id": 12,
  "q_head_id": 3,
  "kv_head_id": 1,
  "candidate_method": "backward_vector_index",
  "candidate_budget": 512,
  "candidate_positions": [8011, 8054, 8120],
  "candidate_scores_index": [0.82, 0.77, 0.75],
  "candidate_scores_exact": [12.3, 11.9, 11.1],
  "lookup_latency_us": 41,
  "rerank_latency_us": 15,
  "sparse_attention_latency_us": 9
}
```

candidate positions 可以压缩存储；但必须能重建每个 step 的 `C_t`。

## 7. 指标

### 7.1 Retrieval 指标

以 full attention logits/probs 为真值：

```text
topK_recall = |TopK_full_logits intersect C_t| / K
K = 1, 8, 32

mass_recall = sum(prob_full[i] for i in C_t)

max_logit_miss =
  max(logits_full) - max(logits_full[j] for j in C_t)
```

### 7.2 Attention output 误差

```text
relative_L2 = ||attn_out_indexed - attn_out_full||_2 / (||attn_out_full||_2 + eps)
cosine_error = 1 - cosine(attn_out_indexed, attn_out_full)
max_abs_error = max(abs(attn_out_indexed - attn_out_full))
```

### 7.3 Logits 误差

仅在完成 shadow/replay 注入时记录：

```text
KL(full || indexed)
top1_logits_agreement
top5_logits_agreement
gold_token_logprob_delta
```

### 7.4 系统开销

分别计时，不只报端到端：

```text
full_attention_latency_us
lookup_latency_us
candidate_materialize_latency_us
rerank_latency_us
sparse_attention_latency_us
index_insert_latency_us
total_indexed_attention_latency_us
kv_cache_memory_mb
index_memory_mb
```

## 8. 输出文件

每次实验写入一个 run 目录：

```text
runs/{run_id}/config.yaml
runs/{run_id}/samples.jsonl
runs/{run_id}/metrics_step.parquet
runs/{run_id}/events_index.jsonl
runs/{run_id}/summary_by_context.csv
runs/{run_id}/summary_by_layer_head.csv
runs/{run_id}/README.md
```

`summary_by_context.csv` 至少包含：

```text
context_len,
candidate_method,
candidate_budget,
median_candidate_ratio,
p50_top32_recall,
p50_mass_recall,
p50_relative_L2_attn_out,
p90_relative_L2_attn_out,
p50_kl_full_indexed_logits,
top1_logits_agreement,
p50_total_indexed_attention_latency_us,
p50_full_attention_latency_us
```

`summary_by_layer_head.csv` 至少包含：

```text
layer_id,
q_head_id,
kv_head_id,
candidate_method,
candidate_budget,
p50_mass_recall,
p90_relative_L2_attn_out,
p99_relative_L2_attn_out,
worst_context_len
```

`README.md` 用 10 行以内写清：

- 模型是否成功加载。
- baseline replay 是否通过 smoke 校验。
- oracle_topm 最小可用 budget。
- backward_vector_index 与 oracle 的差距。
- 是否达到通过判据。

## 9. 通过判据

实验完成的最低标准：

1. 生成了固定 `samples.jsonl`。
2. `qwen3.6-plus` baseline 在至少 `2048` 和 `4096` context 上跑通；若模型不可用，写明 `model_available=false` 并停止质量结论。
3. full attention replay smoke 通过：

```text
relative_L2(attn_out_replay, attn_out_model) <= 1e-4
```

4. `oracle_topm` 完成所有可运行 context 和 budget。
5. `backward_vector_index` 至少完成 `context_len=[2048, 4096, 8192]`、`candidate_budget=[128, 512, 1024]`。
6. 输出 `summary_by_context.csv` 和 `summary_by_layer_head.csv`。

认为 indexed 方法在本轮最小实验中“值得继续”的判据：

```text
candidate_ratio <= 2%
p50_mass_recall >= 0.98
p50_relative_L2_attn_out <= 1e-2
p90_relative_L2_attn_out <= 5e-2
```

如果完成 logits 注入，还需要：

```text
p50_KL(full || indexed) <= 1e-3
top1_logits_agreement >= 0.98
```

如果系统计时可用，还需要至少在一个 context length 上满足：

```text
total_indexed_attention_latency_us < full_attention_latency_us
index_memory_mb <= 0.25 * kv_cache_memory_mb
```

不满足这些阈值也不是失败；结论应明确写成：

```text
当前 candidate/index 方案与 full KV cache attention 的差距是多少，
瓶颈来自 candidate recall、sparse attention output error，还是系统开销。
```
