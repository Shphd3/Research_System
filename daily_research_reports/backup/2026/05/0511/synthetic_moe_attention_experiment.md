# 合成 Zipfian MoE-Attention 实验说明

本文档说明 `from-attention-to-search` 中的合成数据实验。实验目的，是在一个可控的 Zipfian 层级合成数据世界里，训练“一层 MoE + 一层 attention”，系统比较 `full KV` 与 `indexed/hierarchical KV` 的差距、恢复率和候选集节省效果。

这个实验同时验证三组控制变量：

1. `flat 16`：直接使用 16 个叶子专家的扁平路由。
2. `hierarchical same-representation`：使用同一份输入表示做 `coarse -> fine` 层级路由。
3. `our spectral/hierarchical design`：把 common、coarse、fine 证据分到不同子空间或头，再做层级路由与 KV 索引。

最重要的边界是：主训练不提前生成固定 `KV cache`。数据生成器只提供 token、latent labels、输入状态和监督标签；主模型中的 Q/K/V 必须由正在训练的一层 attention 在线产生。脚本可以额外输出 oracle/teacher 的 K/V/query 和 full attention 目标，但这些字段只用于 `smoke`、`oracle smoke`、上界检查和评测调试，不能作为主训练模型的输入，也不能把结果当作主模型结论汇报。

## 1. 核心问题

当 token/feature 频率服从 Zipfian 长尾分布，并且隐变量结构明确包含 `common -> coarse -> fine` 层级时，需要回答两个问题：

1. 一层 MoE 是否能恢复已知的 coarse、fine、mechanism 路由结构。
2. 一层 attention 是否能在远小于 `full KV` 的候选集合上，恢复 `full KV` attention 的 top winners、attention mass 和输出向量。

这不是最终系统基准，而是可控的正确性基准。它把 MoE 路由恢复和 KV 检索恢复放在同一个合成世界中，便于定位 indexed KV 的收益来自路由结构、候选集设计，还是 oracle 信息泄漏。

## 2. 如何生成数据

所有命令都在仓库根目录运行。默认生成命令如下：

```bash
python XingyuD/syn_data/scripts/generate_zipfian_moe_attention_data.py \
  --output-dir XingyuD/syn_data/zipfian_moe_attention_v0
```

默认配置会生成可训练的主数据，不包含固定 `keys`、`values`、`queries` 或 `full_attention_output`。输出目录已有文件时，脚本会拒绝覆盖；需要重生成时显式加 `--overwrite`。

快速 smoke 数据生成命令如下：

```bash
python XingyuD/syn_data/scripts/generate_zipfian_moe_attention_data.py \
  --preset smoke \
  --output-dir /tmp/zipfian_moe_attention_smoke \
  --overwrite
```

oracle smoke 只用于调试候选集评测器、检查 oracle 上界或验证 full-KV 指标代码。命令如下：

```bash
python XingyuD/syn_data/scripts/generate_zipfian_moe_attention_data.py \
  --preset smoke \
  --output-dir /tmp/zipfian_moe_attention_oracle_smoke \
  --include-oracle-kv-targets \
  --overwrite
```

如果需要生成较完整的 oracle 诊断数据，可以去掉 `--preset smoke`，但仍要把它标记为 oracle/debug 产物，不能混入主训练结论。

默认输出文件如下：

```text
metadata.json
prototypes.pt
train.pt
valid.pt
test.pt
```

`.pt` 数据文件不要提交到 GitHub；可以提交脚本、文档和轻量元数据说明。

## 3. 合成数据世界

每条 sequence 有一个文档级 latent path：

```text
coarse_id in {0, ..., C-1}
fine_id in {0, ..., F_per_coarse-1}
path_id = coarse_id * F_per_coarse + fine_id
```

默认配置为 `C=4`、`F_per_coarse=4`，因此共有 16 个 fine path，正好对应 `flat 16` 的 16 个叶子专家。

token/feature 来源分三类：

| 来源标签 | 中文含义 | 默认比例 |
|---|---|---:|
| `common` | 所有类别共享的高频背景或通用机制 | 0.60 |
| `coarse` | 当前 coarse 分支共享的中层机制 | 0.25 |
| `fine` | 当前 fine path 的长尾或细粒度机制 | 0.15 |

Zipfian 分布分别作用在 common、coarse、fine 各自的 token pool 内：

```text
p(rank=r) 正比于 r^(-alpha)，默认 alpha=1.05
```

类别本身保持近似均匀，以避免把类别不均衡和 Zipfian token 频率混在一起。

sequence 的文档级 path 是 query 的主任务 path，但 KV memory 不是单一路径。生成器会按照 `p_primary_coarse` 和 `p_primary_fine`，在主 path token 与干扰 path token 之间混合采样。因此 `same_path_index` 只覆盖 prefix 中一部分 fine-path keys，实验才可以真实比较 `full KV scan` 与 `indexed KV candidate retrieval`。

## 4. 张量结构

每个 split 是一个 PyTorch dict。主训练会用到的字段如下：

| 字段 | 形状 | 用途 |
|---|---|---|
| `token_ids` | `[examples, seq_len]` | 合成 token/feature id |
| `input_states` | `[examples, seq_len, d]` | 一层 MoE 的输入表示 |
| `doc_coarse_id`, `doc_fine_id`, `doc_path_id` | `[examples]` | sequence 级 latent labels |
| `token_source` | `[examples, seq_len]` | common/coarse/fine 机制标签 |
| `token_frequency_bucket` | `[examples, seq_len]` | Zipf rank bucket，即 head/middle/tail |
| `moe_flat_expert_target` | `[examples, seq_len]` | 16 个扁平专家的监督目标 |
| `moe_coarse_target`, `moe_fine_target` | `[examples, seq_len]` | 层级路由监督目标 |
| `moe_mechanism_target` | `[examples, seq_len]` | common/coarse/fine 辅助监督目标 |
| `moe_teacher_hidden` | `[examples, seq_len, d]` | 可选的 teacher hidden 回归目标 |
| `key_coarse_id`, `key_fine_id`, `key_path_id` | `[examples, seq_len]` | oracle KV bucket 标签 |
| `key_spectral_bucket_id` | `[examples, seq_len]` | spectral 设计使用的 oracle bucket 标签 |

`key_spectral_bucket_id` 的编码如下：

```text
0                         -> 全局 common 桶
1 ... C                   -> coarse 桶
1 + C ... 1 + C + C*F - 1 -> fine path 桶
```

启用 `--include-oracle-kv-targets` 后，split 会额外包含以下诊断字段：

| 字段 | 形状 | 用途 |
|---|---|---|
| `keys`, `values` | `[examples, seq_len, d]` | teacher K/V，仅用于 oracle 诊断 |
| `queries` | `[examples, queries, d]` | teacher query 向量 |
| `query_*_id` | `[examples, queries]` | oracle query route/bucket 标签 |
| `query_spectral_bucket_ids` | `[examples, queries, 3]` | common、coarse、fine bucket 的 oracle 并集 |
| `prefix_len` | `[examples, queries]` | online attention prefix 长度 |
| `full_topk_indices`, `full_topk_scores` | `[examples, queries, top_k]` | teacher full-KV top-k |
| `full_topk_attention_mass` | `[examples, queries]` | teacher full top-k softmax mass |
| `full_attention_output` | `[examples, queries, d]` | teacher full-KV softmax output |

对于 teacher/oracle query，`query_spectral_bucket_ids` 给出 oracle union：

```text
全局 common 桶 + query coarse 桶 + query fine path 桶
```

这个字段只是在 oracle 诊断模式下支持 spectral/hierarchical 设计的上界检查，不代表主模型可以直接读取 oracle query bucket。主训练时，query 侧 bucket 必须从当前 query representation 预测出来。

`key_coarse_id/key_fine_id/key_path_id` 对 common tokens 使用 `-1`；coarse tokens 只有 coarse label，fine/path 为 `-1`；fine tokens 拥有完整 path label。MoE 监督仍为所有 token 提供 target，但 `moe_route_weight` 会降低 common/coarse token 的 loss 权重。

## 5. 模型族

所有可训练模型都使用一层 MoE 后接一层 attention。Q/K/V 由这一层 attention 根据当前模型 hidden states 在线计算，不读取数据文件中的固定 K/V。

### 5.1 扁平 16 专家 MoE

该模型直接预测 `moe_flat_expert_target`：

```text
input_states -> 16 专家扁平路由器 -> MoE hidden -> 可训练 Q/K/V attention
```

预期现象：fine tokens 上较强；common tokens 上可能较弱，除非辅助损失或负载均衡让通用机制得到稳定表示。

### 5.2 同表示层级 MoE

该模型用同一份输入表示分别喂给 coarse router 和 fine router：

```text
input_states -> coarse 路由器 -> 选中 coarse 内的 fine 路由器 -> MoE hidden -> 可训练 Q/K/V attention
```

监督目标包括：

```text
moe_coarse_target
moe_fine_target
moe_mechanism_target 作为可选辅助目标
```

这组实验检验标准层级路由是否能恢复已知的 `coarse -> fine` 树，同时与 `flat 16` 在相同 16 叶子预算下比较。

### 5.3 我们的 spectral/hierarchical 设计

该模型先把 common、coarse、fine 证据分配到不同子空间或不同 heads，再进行路由：

```text
common 子空间 -> 全局/common 专家或残差路径
coarse 子空间 -> coarse 路由器
fine/tail 子空间 -> fine 叶子路由器
```

数据通过以下标签支持训练和诊断：

```text
token_source
token_frequency_bucket
key_spectral_bucket_id
```

主训练时，query 侧 spectral buckets 必须由当前 query representation 预测。只有在 `--include-oracle-kv-targets` 诊断模式中，split 才会保存 `query_spectral_bucket_ids`，用于 oracle common/coarse/fine bucket union 的上界检查。

预期现象：在 Zipfian tail features 上恢复更好，并且在相同 recall 下使用更小的 indexed-KV 候选集。

## 6. Attention 候选方法

训练和评测时，主实验的 ground truth 是“对当前模型在线产生的 K/V cache 做 full attention”。也就是说，full baseline 和 indexed 方法都使用当前模型在线产生的 Q/K/V，只是候选集合不同。

如果启用了 `--include-oracle-kv-targets`，teacher K/V 字段可以在 trainable attention 实现完成前用于快速 smoke 测试评测器；这类结果必须标注为 `oracle_kv_smoke`。

候选方法如下：

| 方法 | 候选集合 |
|---|---|
| `full_kv` | prefix 中所有 keys；精确基线 |
| `oracle_topm` | 来自模型或 teacher logits 的精确 full-KV top-m keys；固定候选预算下的上界 |
| `same_path_index` | oracle 诊断时使用 `key_path_id == query_path_id`；主实验使用已学习或预测的 query path |
| `same_coarse_index` | oracle 诊断时使用 `key_coarse_id == query_coarse_id`；主实验使用已学习或预测的 query coarse bucket |
| `spectral_union_index` | oracle 诊断时使用 `key_spectral_bucket_id` 是否属于 `query_spectral_bucket_ids`；主实验使用已学习或预测的 spectral bucket 并集 |
| `flat_router_indexed_kv` | 已学习的 flat router 预测候选 leaf bucket |
| `hier_router_indexed_kv` | 已学习的 coarse/fine router 预测层级 bucket |
| `spectral_router_indexed_kv` | 已学习的 spectral router 预测 common/coarse/fine bucket 并集 |

所有 indexed 方法都应当先用当前模型的 Q/K 对候选 keys 重新计算精确点积，再在候选集合上计算 sparse softmax attention。

## 7. 训练任务

推荐损失如下：

| 任务 | 目标 | 损失 |
|---|---|---|
| 扁平路由 | `moe_flat_expert_target` | 交叉熵，并用 `moe_route_weight` 加权 |
| 层级路由 | `moe_coarse_target`, `moe_fine_target` | 交叉熵 |
| 机制恢复 | `moe_mechanism_target` | 辅助交叉熵 |
| MoE 隐状态模仿 | `moe_teacher_hidden` | MSE 或余弦损失 |
| attention 输出恢复 | 同一训练模型的在线 full-KV output；oracle smoke 中可选用 `full_attention_output` | MSE 或相对 L2 |
| top-k 候选恢复 | 同一训练模型的在线 full-KV top-k；oracle smoke 中可选用 `full_topk_indices` | recall 指标，通常不必作为训练损失 |

主训练流程：训练 MoE + attention block，让 Q/K/V 从 `input_states` 经模型在线产生，然后比较 full-KV 输出与 indexed-KV 输出。

可选诊断流程：启用 `--include-oracle-kv-targets` 后，可以固定 teacher Q/K/V，仅用于调试候选生成、指标实现和 oracle 上界。这条流程必须命名为 `oracle_kv_smoke`，不要报告为主模型结果。

## 8. 指标

必报检索指标如下：

| 指标 | 定义 |
|---|---|
| `Top1Recall` | 候选集合是否包含 `full_topk_indices[..., 0]` |
| `TopKRecall@K` | 精确 full top-K keys 中有多少比例落入候选集合 |
| `AttentionMassRecall` | 候选集合覆盖的 full softmax mass 总和 |
| `OutputMSE` | 稀疏候选 attention output 与 full attention output 的均方误差 |
| `OutputRelativeL2` | `||o_indexed - o_full||_2 / max(||o_full||_2, eps)` |
| `CandidateRatio` | 候选 key 数量除以 `prefix_len` |

必报路由指标如下：

| 指标 | 定义 |
|---|---|
| `FlatExpertAccuracy` | `moe_flat_expert_target` 上的准确率 |
| `CoarseAccuracy` | `moe_coarse_target` 上的准确率 |
| `FineAccuracy` | `moe_fine_target` 上的准确率，可分别报告是否依赖 coarse 正确 |
| `MechanismAccuracy` | common/coarse/fine token source 的准确率 |
| `RoutingRecovery` | 相同候选预算下，已学习 indexed-KV recall 除以 oracle bucket recall |

`full KV` 与 `indexed KV` 的差距按如下方式报告：

```text
TopKRecallGap      = 1.0 - TopKRecall_indexed
MassRecallGap      = 1.0 - AttentionMassRecall_indexed
OutputMSEGap       = OutputMSE_indexed - OutputMSE_full
RelativeL2Gap      = OutputRelativeL2_indexed - OutputRelativeL2_full
CandidateSaving    = 1.0 - CandidateRatio_indexed
```

因为 `full_kv` 是精确基线，所以：

```text
OutputMSE_full = 0
OutputRelativeL2_full = 0
```

恢复率需要相对两个参照报告：

```text
RecallRecoveryVsOracle = Recall_method / max(Recall_oracle_bucket, eps)
ErrorRecoveryVsRandom  = 1 - Error_method / max(Error_random_same_budget, eps)
```

第一个恢复率回答已学习路由器是否恢复了 oracle 结构。第二个恢复率回答 indexing 是否明显优于同预算随机候选集。

## 9. 第一组实验矩阵

最小实验矩阵如下：

| MoE 设置 | KV 方法 | 目的 |
|---|---|---|
| 无 MoE 或冻结 QKV | `full_kv` | 精确 attention 基线 |
| 无 MoE 或冻结 QKV | `oracle_topm` | 固定预算上界 |
| 无 MoE 或冻结 QKV | `same_path_index` | 叶子级 oracle 索引 |
| 无 MoE 或冻结 QKV | `spectral_union_index` | oracle spectral bucket 并集 |
| `flat 16` | `flat_router_indexed_kv` | 已学习的扁平路由加 indexed KV |
| `hierarchical same-representation` | `hier_router_indexed_kv` | 标准层级控制变量 |
| `our spectral/hierarchical design` | `spectral_router_indexed_kv` | 提议的 spectral/hierarchical 设计 |

前四行只是在 teacher K/V 存在时使用的 smoke/oracle 诊断。主训练实验从 `flat 16` 开始，并在相同 16 叶子预算下比较 `hierarchical same-representation` 与 `our spectral/hierarchical design`。

每个方法都应在多个候选预算或 bucket union 设置下报告，并绘制以下关系：

```text
CandidateRatio 相对 Top1Recall
CandidateRatio 相对 AttentionMassRecall
CandidateRatio 相对 OutputRelativeL2
RoutingAccuracy 相对 KVRecovery
```

## 10. 预期正确性检查

训练前应检查：

1. `metadata.json` 中的 source fractions 应接近 0.60/0.25/0.15。
2. token frequency buckets 应呈现长尾分布：head ranks 样本多，但 middle/tail 覆盖非零。
3. `same_path_index` 的 candidate ratio 应显著小于 1.0。
4. `spectral_union_index` 的 candidate ratio 应大于 same-path，但应恢复更多 common/coarse attention mass。
5. `full_topk_attention_mass` 应显著高于随机水平，说明 attention 目标具有选择性。

这些检查用于确认合成数据有足够结构，能够同时测试 MoE routing recovery 和 indexed KV recovery。
