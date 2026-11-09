# Execution Plan: R3 Perfect Router Retrieval

## 1. Run Goal

直接 full run 两个数据版本，检验 perfect feature-aligned router bucket 是否能作为 block2 KV retrieval index。

## 2. Data Construction

Uniform:

```text
ABC = DEF = GHI = JKL = 5000
```

Feature-long-tail:

```text
ABC = 10000
DEF = 5000
GHI = 500
JKL = 100
```

说明：这里的 long-tail 是 feature-count long-tail，不是严格 token-level Zipf corpus。

## 3. Model / Training / Evaluation Setup

Model:

```text
seq_len = 32
d_model = 64
n_heads = 4
routing_buckets = 4
expert_hidden = 32
```

Variant:

```text
moe_router_ce
```

Training:

```text
loss = NTP_CE + 1.0 * RouterFeatureCE
batch_size = 128
feature_router_batch_size = 128
train_steps = 10000
lr = 6e-4
weight_decay = 0
```

RouterFeatureCE 只用于 feature query position：

```text
ABC -> expert 0
DEF -> expert 1
GHI -> expert 2
JKL -> expert 3
```

## 4. Configs And Commands

Run root:

```text
XingyuD/Attention_Search_Experiments/active/r2_eseries_router_retrieval/
```

Configs:

```text
configs/r3_perfect_router_uniform_full.json
configs/r3_perfect_router_longtail_full.json
```

Submit script:

```text
scripts/submit_r3_perfect_router_4seed_acp.sh
```

ACP plan:

```text
Job 1: uniform, 4 GPUs, seeds 20260518..20260521
Job 2: feature-long-tail, 4 GPUs, seeds 20260518..20260521
```

每张 GPU 跑一个 seed。

## 5. Metrics And Artifacts

Specialization sanity:

```text
feature_to_bucket_heatmap.csv
eval_metrics.json: NMI / ARI
train_metrics.jsonl: router_acc / router_ce
feature_readback.csv
```

Dense attention sparsity:

```text
attention_sparsity.csv
TopM_mass
Mass90_support
EffectiveSupport
```

Retrieval:

```text
retrieval_metrics.csv
DenseTop16Recall@K
AttentionMassRecall@K
CandidateRatio@K
MeanCandidateKVTokens@K
OutputRelativeL2@K
CE_delta@K
RankKOnlyRecall
RankKOnlyMass
```

K sweep:

```text
K = 1, 2, 3, 4
```

K=4 must match full prefix sanity.

## 6. Pass / Fail Criteria

Specialization precondition:

```text
NMI >= 0.98
fixed-label alignment visually clean
router_acc near 1.0
feature readback accuracy near 1.0
```

Retrieval success:

```text
router top-K beats same-count random/local
candidate ratio remains meaningfully below 1
output L2 and CE_delta close to full attention
rank-K-only has meaningful front-loaded contribution
```

Retrieval failure:

```text
router ~= random/local
or high recall only at K=4/full prefix
or recall high but output/CE quality poor
```

## 7. Failure Modes To Check

- Router CE did not achieve clean specialization.
- K=4 does not equal full prefix sanity.
- Candidate ratio too high for useful index.
- Dense attention not sparse.
- Feature-long-tail rare features under-sampled.

## 8. Result Location

Run outputs:

```text
active/r2_eseries_router_retrieval/outputs_r3_perfect_uniform/
active/r2_eseries_router_retrieval/outputs_r3_perfect_longtail/
```

Figures:

```text
active/r2_eseries_router_retrieval/figures_r3_perfect_uniform/
active/r2_eseries_router_retrieval/figures_r3_perfect_longtail/
```

Mainline report:

```text
main/experiments/R3_perfect_router_retrieval/
```

