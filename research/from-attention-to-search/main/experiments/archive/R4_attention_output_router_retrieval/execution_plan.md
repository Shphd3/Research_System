# Execution Plan: R4 Attention-Output Router Retrieval

## 1. Run Goal

跑两个数据分布：

- uniform all-trigram
- feature-long-tail all-trigram

每个数据分布用一个 4-GPU ACP job，四张卡并行：

```text
attn_route_ntp_only      seed 20260522
attn_route_ntp_only      seed 20260523
attn_route_router_ce     seed 20260522
attn_route_router_ce     seed 20260523
```

## 2. Data Construction

沿用 E-series all-trigram 数据：

```text
seq_len = 32
vocab_size = 1000
corpus_length = 1,000,000
task = next-token prediction
```

## 3. Model / Training / Evaluation Setup

模型：

```text
TokenEmbedding + PosEmbedding
-> TransformerBlock1
-> Router/MoE
-> TransformerBlock2
-> LMHead
```

R4 路由输入：

```text
router_input = block1 attention output without residual
expert_input = block1 hidden after residual + FFN
```

训练：

```text
train_steps = 10000
batch_size = 128
lr = 6e-4
weight_decay = 0
routing_buckets = 4
expert_hidden = 32
```

损失：

```text
attn_route_ntp_only: NTP CE
attn_route_router_ce: NTP CE + RouterFeatureCE
```

## 4. Configs And Commands

配置：

```text
active/r2_eseries_router_retrieval/configs/r4_attn_route_uniform_full.json
active/r2_eseries_router_retrieval/configs/r4_attn_route_longtail_full.json
```

提交脚本：

```text
active/r2_eseries_router_retrieval/scripts/submit_r4_attn_route_2variant_2seed_acp.sh
```

## 5. Metrics And Artifacts

训练：

```text
valid CE
feature readback probability / accuracy
router CE / router accuracy
```

Retrieval：

```text
DenseTop16Recall@K
AttentionMassRecall@K
OutputRelativeL2@K
CE_delta@K
sparse_CE@K
candidate_count / candidate_ratio
rank-K-only recall/mass
```

对照：

```text
same-count random
same-count local
same-count oracle
full prefix sanity
```

## 6. Pass / Fail Criteria

支持 R4 假设：

```text
router top-K 在 CE_delta 和 output L2 上明显优于 random/local，且不是只靠接近 full prefix 的高 candidate ratio。
```

削弱 R4 假设：

```text
router alignment 或 readback 好，但 CE_delta/output L2 仍差于 local/random。
```

## 7. Failure Modes To Check

- attention output 表示过于混合，不能形成稳定 feature bucket；
- RouterFeatureCE 只改善 feature alignment，不改善 dense-attention KV recall；
- block2 dense attention 主要依赖 local/token identity，而不是 feature identity；
- NTP CE 好不代表 sparse reverse-index CE 好。

## 8. Result Location

运行侧：

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/r2_eseries_router_retrieval/outputs_r4_attn_route_uniform/
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/r2_eseries_router_retrieval/outputs_r4_attn_route_longtail/
```

主线侧：

```text
Projects/from-attention-to-search/main/experiments/R4_attention_output_router_retrieval/
```

