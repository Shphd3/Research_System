# Hypothesis Closure Draft - E1 Router-Guided Attention Retrieval

## 1. Original Purpose

Test whether expert/path routing can be used as a causal KV retrieval index for attention inference.

## 2. Mainline Anchor

Attention-as-search says dense attention can be decomposed into candidate retrieval plus exact reranking. H-MoE design says hierarchical routing may produce more stable and structured buckets than flat MoE.

## 3. Hypotheses

### H1 Data/Representation

Synthetic data with long-tail, sparse, hierarchical features induces structured routing distributions.

### H2 Routing Structure

H-MoE produces more structured feature-to-path distribution than flat MoE under matched budget.

### H3 Retrieval

For a query token, candidate KV tokens from top-k expert/path buckets ranked by router logits recover dense-attention contributors better than random or local-only baselines.

### H4 Inference Quality

Second-block router-retrieval attention approaches dense second-block attention quality as k increases.

## 4. Why This Setup Tests The Hypothesis

The architecture has MoE before the second Transformer block. Therefore, expert/path assignments are causally available before the second block attention. We can bucket historical tokens by MoE assignment, rank buckets for the current token by router logits, and compare retrieval attention against full dense attention.

## 5. Experiment Summary

Model:

```text
TinyT-MoE-T-Retrieval
TransformerBlock1 -> MoE -> TransformerBlock2
```

Comparisons:

```text
Flat MoE + LB loss
H-MoE Common-Unique
Dense full attention
Local window
Random matched buckets
Oracle latent bucket, synthetic only
```

Metric family:

```text
Recall, attention mass recall, output error/MSE, candidate ratio, bucket distribution, specialization metrics.
```

## 6. Result

TBD.

## 7. Interpretation Rules

If top-k router buckets improve over local/random and approach dense attention, router-path indexing is weakly supported.

If H-MoE improves recall/MSE over flat, H-MoE routing structure is useful for retrieval.

If only oracle latent bucket works, learned router is insufficient.

If retrieval quality does not improve with k, routing buckets are not aligned with attention contributors.

## 8. Claim Update

Before experiment:

```text
router-guided KV retrieval = unsupported
H-MoE better retrieval buckets = unsupported
```

After experiment:

```text
Update based on recall, MSE, and attention-mass curves.
```

## 9. What Cannot Be Claimed

- No real GPU speedup unless latency is profiled.
- No transfer to real LM unless DCLM E2 supports it.
- No claim that H-MoE learns human-interpretable hierarchy.
- No claim that CL forgetting results prove retrieval behavior.

## 10. Weakest Point

The synthetic data may make the hierarchy too easy; the learned router may align with synthetic latent features but not with dense attention in language modeling.

## 11. Next Decision

Proceed to DCLM E2 only if E1 shows router-bucket retrieval improves recall and MSE over matched random/local baselines.

## 12. 30s Advisor Version

We changed the first loop to directly test the advisor-facing hypothesis: whether routing buckets can serve as attention KV retrieval indexes. The model places MoE before the second Transformer block so bucket labels are available before retrieval attention. We train on synthetic sparse hierarchical reconstruction with dense attention, then run second-block retrieval inference using top-k expert/path buckets. The key curves are top-k vs recall, top-k vs MSE, expert-rank contribution, and routing distribution heatmaps. This only tests the retrieval-index hypothesis; it does not claim speedup or real-LM transfer yet.
