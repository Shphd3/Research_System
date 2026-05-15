# Current Research Mainline

Last updated: 2026-05-14

## Active Project

Primary project:

```text
Projects/from-attention-to-search/
Branch: Xingyu
Working context: Projects/from-attention-to-search/XingyuD/main/
```

Supporting project:

```text
Projects/MoE-Continual-Learning/
```

The primary mainline is `from-attention-to-search`. The MoE continual-learning project is supporting context: it provides the data-property, feature-definition, mapping-conflict, and expert-specialization background.

## One-Sentence Mainline

We are trying to reinterpret long-context Transformer attention as model-native search over dynamic KV memory: first retrieve a small candidate set from a learned index, then run exact sparse attention over those candidates.

## Core Research Question

Can a Transformer learn an internal memory-indexing structure so that long-context attention no longer behaves like a linear scan over all cached tokens?

More concretely:

```text
query token -> learned routing / indexing signal -> candidate KV tokens -> exact sparse attention
```

## Current Hypothesis

The broad hypothesis is:

> Useful long-context attention may require a learned index whose partitions align with the geometry that determines high attention mass, not merely with input features, token identity, or ordinary MoE utilization.

The current candidate indexing signals include:

- MoE / H-MoE router buckets;
- feature identity;
- rule or path identity;
- hidden-state similarity;
- value or output similarity;
- latent atom overlap;
- temporal locality.

## Current Evidence From `from-attention-to-search`

Current R1 result:

- Dense block2 attention is sparse enough to make retrieval meaningful.
- Attention mass is often remote, so local-only retrieval is weak.
- Oracle top-$M$ candidates can recover dense attention output.
- But current flat MoE, H-MoE, and spectral router buckets do not retrieve high-mass KV tokens better than random matched candidates.

Current safe claim:

> In the current synthetic setup, existing flat/H-MoE/spectral router buckets do not provide useful KV candidate retrieval signal beyond random matched retrieval.

This is a negative but useful result. It says the retrieval framing is meaningful, but the current router signal is not the right index.

## Current Evidence From Synthetic Data Understanding

E0/E1 supports a cleaner all-trigram corpus as a usable synthetic testbed:

- planted features are three-token context relations such as `[A,B]->[C]`;
- with `V=1000` and `N=10^6`, target-feature collision risk is near zero;
- a dense toy Transformer can read back all four planted features, including the low-frequency `JKL` feature with target count 100.

Current implication:

> The next synthetic question is no longer whether the data is clean enough, but whether MoE experts separate feature identity, frequency, or some deeper mapping/retrieval signal.

## Supporting Insight From MoE Continual Learning

The older MoE continual-learning line changed the feature definition.

Earlier weak view:

```text
forgetting comes from poor atom-level feature separation
```

Updated view:

```text
forgetting comes from feature overlap + rule/mapping conflict + insufficient routing specialization
```

Key lesson:

> Splitting helps only when the split aligns with the true mapping-level feature, not merely with raw input atoms or coarse families.

This matters for `from-attention-to-search` because a good KV index may need to align with the feature/rule/mapping geometry that predicts future attention winners. Expert IDs alone are not enough unless they align with that geometry.

## Current Claim Boundary

We can claim:

- long-context attention can be framed as an extreme-value retrieval problem;
- dense attention in the current synthetic setup is sparse enough for candidate retrieval to be meaningful;
- oracle retrieval works in the current setup;
- current MoE/H-MoE/spectral router buckets fail as useful KV indexes in R1;
- clean all-trigram synthetic data is a valid next testbed for feature-separation experiments;
- mapping-level feature definition is important background from the MoE continual-learning project.

We cannot claim:

- MoE routing is generally useless for KV retrieval;
- H-MoE is generally worse than flat MoE;
- the current synthetic result transfers to DCLM or real long-context inference;
- there is any speedup yet;
- ordinary expert specialization equals useful memory indexing;
- atom-level feature separation is sufficient for retrieval or continual-learning stability.

## Current Bottleneck

The bottleneck is identifying what dense attention actually follows.

Candidate explanations:

- latent atom overlap;
- planted rule or path identity;
- hidden-state similarity;
- value/output similarity;
- temporal locality;
- mapping-level feature identity.

Until this is diagnosed, we should not design another router/indexer as if expert IDs already define the right memory partition.

## Next Decision

Next step:

> Use the clean all-trigram synthetic corpus to test what signal predicts dense attention winners and whether MoE experts separate feature identity, frequency, or mapping/retrieval-relevant structure.

The next experiment should distinguish:

```text
feature separation
frequency specialization
mapping/rule specialization
retrieval alignment with attention mass
```

## Reading Anchor

When reading papers or blogs, connect them to this mainline only if they update one of:

- attention as retrieval/search;
- dynamic KV memory;
- learned indexing;
- sparse or hierarchical feature structure;
- MoE/H-MoE routing and expert specialization;
- mapping-level feature definition;
- evidence needed to move from synthetic diagnostics to real representations.

If a paper only provides background, say `No mainline update from this reading`.
