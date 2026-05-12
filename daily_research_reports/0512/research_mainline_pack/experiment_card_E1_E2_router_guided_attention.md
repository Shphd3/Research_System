# Experiment Card - E1/E2 Router-Guided Attention Retrieval

## 0. One-Sentence Conclusion

This experiment tests whether MoE expert/path assignments can be used as a causal retrieval index for the second Transformer block attention: as expert top-k increases, recall, attention quality, and reconstruction/LM accuracy should approach dense attention while candidate size stays smaller.

## 1. Experiment Purpose

Primary purpose:

```text
Verify whether route buckets are useful KV retrieval candidates for attention inference.
```

Not the purpose:

```text
Not continual learning.
Not proving H-MoE speedup.
Not proving MoE semantic hierarchy generally.
```

## 2. Hypotheses To Decide

H1: Hierarchical sparse-feature data induces structured expert/path distribution.

H2: H-MoE creates more retrieval-useful bucket structure than flat MoE under comparable parameter settings.

H3: For the current query token, ranking experts/paths by router logits gives a meaningful retrieval order: top-1, top-2, ..., top-k buckets should progressively increase relevant-token recall and dense-attention mass recall.

H4: Second-block router-retrieval attention should approach dense attention output quality as k increases.

H5: If E1 synthetic succeeds, DCLM language modeling can test whether the behavior survives real-token training.

## 3. Model

### 3.1 Architecture Name

```text
TinyT-MoE-T-Retrieval
```

### 3.2 Architecture Skeleton

```text
Input embeddings / synthetic token vectors
-> TransformerBlock1: dense causal self-attention
-> MoE block: Flat MoE or H-MoE Common-Unique
-> TransformerBlock2: dense during reference; router-retrieval during inference analysis
-> prediction head
```

### 3.3 Synthetic E1 Model Config

```text
d_model = 64
n_heads = 4
num_transformer_blocks = 2
moe_position = between block1 and block2
seq_len = {128, 256} initially
loss = reconstruction MSE
```

Flat MoE:

```text
router = Linear(64, 48)
num_unique_experts = 48
expert_dim = 50
top_k_train = 1
load_balancing_loss = enabled
router_aux_weight = 0.15 initially
```

H-MoE Common-Unique:

```text
outer_router = Linear(64, 48)
outer_branches = 48
inner_router_per_branch = Linear(64, 4)
inner_unique_experts_per_branch = 4
d1_common = 16
d2_common = 27
d2_unique = 5
top_k_train = 1 outer, 1 inner
outer and inner load balancing = enabled
router_aux_weight = 0.15 initially
```

Important:

```text
Use H-MoE Common-Unique design, not spectral router.
```

### 3.4 DCLM E2 Model Config

Use the same structural skeleton, scaled only if compute allows:

```text
TransformerBlock1 -> MoE -> TransformerBlock2
loss = next-token cross entropy
training data = 0.5B-token DCLM subset
train epochs = 3
held-out validation/test = required
```

Recommended initial LM size if compute is limited:

```text
d_model = 512
n_heads = 8
seq_len = 1024
MoE flat/hier parameter budget matched by active-parameter design, not by exact 64-d synthetic dimensions
```

If compute is tight, first run:

```text
d_model = 256
n_heads = 4
seq_len = 512
```

## 4. Data Design

### 4.1 Synthetic E1 Data

Properties to enforce:

```text
feature activation is long-tailed
feature activation is sparse
features have hierarchy
```

Each sequence contains tokens generated from latent feature paths:

```text
global feature -> middle feature -> leaf feature
```

Each token activates a sparse set of features:

```text
2 to 6 active features per token
Zipf frequency over features
```

Targets:

```text
MSE reconstruction target
```

The target should depend on a small set of earlier relevant tokens so that retrieval can be evaluated against oracle relevant positions.

### 4.2 DCLM E2 Data

```text
Dataset = DCLM subset
Size = 0.5B tokens
Split = train / validation / test
Training = 3 epochs
Objective = next-token prediction
```

## 5. Retrieval Inference Design

### 5.1 Bucket Construction

For every historical token after the MoE block:

Flat:

```text
bucket_id = flat_expert_id
```

H-MoE:

```text
bucket_id = path_id = outer_id * num_inner + inner_id
```

Store KV positions by bucket:

```text
bucket_id -> token positions
```

### 5.2 Query-Time Bucket Ranking

For current query token:

Flat:

```text
rank experts by router logits
C_k = tokens in top-k expert buckets
```

H-MoE:

```text
rank paths by outer + inner logits
C_k = tokens in top-k path buckets
```

Evaluate both:

```text
cumulative top-k buckets: top1, top2, ..., topK
single-rank bucket effect: rank1 only, rank2 only, ..., rankK only
```

### 5.3 Attention Computation

Reference:

```text
Dense second-block attention over all previous tokens
```

Retrieval:

```text
Second-block exact attention over C_k only
```

Optional hybrid:

```text
C_k = local_window(W) union router_top_k_buckets
```

## 6. Baselines

1. Full dense attention.
2. Local window only.
3. Random buckets matched by candidate count.
4. Flat MoE bucket retrieval with LB loss.
5. H-MoE bucket retrieval.
6. Oracle latent bucket, synthetic only.
7. Oracle dense top-M candidates, diagnostic upper bound only.

## 7. Metrics

### 7.1 Retrieval Metrics

```text
oracle relevant token Recall@k
Dense-attention Top-M key Recall@k
Attention mass recall@k
Remote attention mass recall@k
Candidate ratio = |C_k| / context_length
```

### 7.2 Quality Metrics

Synthetic:

```text
MSE reconstruction
output error between retrieval attention and dense attention
```

DCLM:

```text
validation/test cross entropy
perplexity
top-1 token accuracy, optional
```

### 7.3 Routing Distribution Metrics

```text
bucket size histogram
router entropy
expert/path utilization
feature -> expert/path heatmap
rule/token-type -> expert/path heatmap
mean entropy P(path | feature)
top-1 path mass per feature
mutual information I(feature; path)
Gini coefficient over bucket traffic
```

### 7.4 Expert-Rank Effect Metrics

For expert/path rank r by router logit:

```text
attention mass captured by rank-r bucket
oracle relevant tokens in rank-r bucket
quality using rank-r bucket only
quality using cumulative top-k buckets
```

## 8. Required Figures

1. `topk_bucket_vs_oracle_recall.png`
2. `topk_bucket_vs_dense_attention_recall.png`
3. `topk_bucket_vs_attention_mass_recall.png`
4. `topk_bucket_vs_mse_or_ce.png`
5. `expert_rank_vs_attention_mass.png`
6. `bucket_size_distribution_flat_vs_hier.png`
7. `feature_to_expert_or_path_heatmap.png`
8. `candidate_ratio_vs_quality.png`
9. `dense_vs_retrieval_output_error.png`
10. DCLM only: `test_ppl_dense_vs_retrieval.png`

## 9. Expected Outcomes

If the retrieval hypothesis holds:

```text
top-k recall increases with k
attention mass recall increases with k
MSE / CE approaches dense baseline as k grows
H-MoE has better recall-quality tradeoff than flat MoE
```

If only local baseline works:

```text
attention is mostly local; router indexing is not yet justified
```

If random matched buckets match router buckets:

```text
routing has no retrieval value
```

If oracle bucket works but learned router fails:

```text
architecture/data contain useful structure, but learned router does not recover it
```

## 10. Claim Boundary

This experiment can support:

```text
In this model and dataset, routing buckets can/cannot act as candidate generators for second-block attention.
```

It cannot prove:

```text
real GPU speedup
million-token scalability
general LM transfer from synthetic data
human-interpretable hierarchy
continual-learning improvement
```

## 11. First Implementation Order

1. Implement TinyT-MoE-T with dense second-block reference.
2. Implement flat MoE + LB loss.
3. Implement H-MoE Common-Unique, no spectral router.
4. Generate synthetic hierarchical sparse-feature sequences.
5. Train with MSE reconstruction.
6. Log MoE assignments and dense second-block attention.
7. Implement bucketed retrieval inference.
8. Produce top-k and rank-r curves.
9. Compare flat vs H-MoE.
10. Only then start DCLM E2.
