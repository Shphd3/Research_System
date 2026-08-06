# Mainline Update - 0512

## One-Sentence Mainline

We test whether a hierarchy-aware MoE routing signal can serve as a causal KV retrieval index for the second Transformer block at inference time, first on synthetic reconstruction and then on DCLM language modeling.

## Current Mainline

Long-context attention is treated as candidate retrieval plus exact reranking, not as a purely dense aggregation problem. The concrete next step is not to claim full acceleration, but to test whether routing buckets produced by a trained MoE layer can retrieve the KV tokens that dense attention would have used.

## Mainline Anchor

Architecture anchor:

- Attention-as-search: long-context attention may be approximated by retrieving likely high-score candidates, then applying exact attention on the candidate set.
- H-MoE anchor: hierarchical/common-unique MoE is used because it is designed to produce stable always-on common paths plus sparse conditional unique paths.

## Safest Claim

Hierarchical MoE is a plausible design for producing structured routing buckets, but whether those buckets are useful for attention KV retrieval remains unverified.

## What Is Not Claimable

- We cannot claim H-MoE improves real inference speed.
- We cannot claim router buckets recover dense-attention winners.
- We cannot claim synthetic reconstruction results transfer to real language modeling.
- We cannot claim feature hierarchy is human-interpretable.
- We cannot claim continual-learning performance is our target; we inherit that report only for architecture/data design and routing analysis style.

## Active Hypotheses

### H1: Representation/Data Hypothesis

Synthetic data with long-tail, sparse, hierarchical features should induce non-uniform and structured routing.

### H2: Hierarchical Routing Hypothesis

H-MoE should produce more structured token-to-path distribution than flat MoE under matched parameter budget.

### H3: Retrieval Hypothesis

When tokens are bucketed by expert/path assignment, the top-k expert buckets ranked by query router logits should increasingly recover relevant KV tokens and dense-attention contributors as k grows.

### H4: Inference Hypothesis

Second-block retrieval attention using router-selected buckets should approach dense second-block attention quality with fewer KV candidates.

### H5: Real-LM Transfer Hypothesis

If H3/H4 hold on synthetic reconstruction, a small DCLM language-modeling run can test whether the same retrieval behavior appears under next-token training.

## First Closed Loop

E1 synthetic reconstruction:

1. Train TinyT-MoE-T models on synthetic hierarchical feature sequences with MSE reconstruction loss.
2. Compare flat MoE with load-balancing loss and H-MoE Common-Unique design.
3. At inference, make the second Transformer block use router-guided retrieval instead of full dense attention.
4. Plot top-k expert/path bucket recall, dense-attention mass recall, output MSE, and bucket distribution.
5. Decide whether router buckets are a valid candidate-retrieval signal.

## Next Decision

Proceed to DCLM E2 only if H-MoE or flat routing shows non-random retrieval value: top-k bucket candidates must improve recall and reconstruction quality over random/local baselines under matched candidate size.
