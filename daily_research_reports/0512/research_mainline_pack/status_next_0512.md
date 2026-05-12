# Status and Next Actions - 0512

## Current Status

The research mainline has shifted from general H-MoE/CL analysis to route-guided KV retrieval for inference.

The immediate experiment should not measure continual learning. It should measure whether expert/path routing can serve as a KV candidate generator for the second Transformer block.

## Completed Inputs

- architecture.pdf: defines attention-as-search and dynamic KV indexing motivation.
- main_cn.pdf: provides H-MoE Common-Unique architecture and systems motivation.
- Draft.docx: provides early data-design motivation: long-tail, sparse, hierarchical features.
- moe_continual_learning_experiment_card_diagnostic.md: provides prior synthetic setup, flat/H-MoE matching, metrics, results, and claim-boundary style.

## Next Step: E1 Synthetic Retrieval Loop

Implement TinyT-MoE-T-Retrieval:

```text
Input sequence
-> TransformerBlock1, dense attention
-> MoE block, flat or H-MoE
-> TransformerBlock2, retrieval attention at inference
-> reconstruction head
```

Primary target:

```text
MSE reconstruction on synthetic hierarchical sparse-feature sequences
```

Primary analysis:

```text
As expert/path top-k increases, measure recall, attention mass, reconstruction MSE, and candidate ratio.
```

Required figures:

1. top-k expert/path vs oracle relevant-token recall.
2. top-k expert/path vs dense-attention top-token recall.
3. top-k expert/path vs MSE / output error.
4. expert/path rank vs attention contribution.
5. bucket size distribution.
6. feature/rule/token-type to expert/path heatmap.
7. flat vs H-MoE retrieval comparison.

## Next Step After E1: E2 DCLM LM Loop

Only after E1 shows non-random retrieval value:

- train the same architecture as a language model on a 0.5B-token DCLM subset for 3 epochs;
- evaluate dense second-block attention vs router-retrieval second-block attention on held-out test set;
- report perplexity/CE, dense-attention approximation, candidate ratio, and retrieval behavior.

## Blocking Questions

1. Exact synthetic sequence generator: how many tokens per sequence and how target reconstruction is defined.
2. Whether second-block retrieval is used only at inference or also during training.
3. DCLM tokenizer and exact subset sampling.
4. Compute budget for 0.5B-token x 3 epochs.

## Current Recommendation

Train with dense second-block attention first, then evaluate retrieval attention at inference. This isolates whether routing buckets are useful retrieval indexes before changing training dynamics.
