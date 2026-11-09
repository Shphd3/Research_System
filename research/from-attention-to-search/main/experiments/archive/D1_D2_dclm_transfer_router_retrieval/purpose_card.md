# Experiment Card: D1/D2 DCLM Transfer Router Retrieval

Hypothesis: synthetic router-bucket retrieval signals may transfer to real DCLM next-token training.

Question: After DCLM training, do router-ranked buckets recover dense block2 attention contributors better than random/local candidates?

Setup: same `TransformerBlock1 -> Router/MoE/H-MoE -> TransformerBlock2` skeleton on a small DCLM subset.

Tasks:
- D1: DCLM next-token training.
- D2: retrieval-only analysis over D1 checkpoints.

Variants: only run variants supported by R1 synthetic closure.

Baselines: `full_kv`, `oracle_topm`, `local_window`, `random_matched`.

Metrics: DCLM validation CE, dense attention sparsity, top-k dense recall, attention-mass recall, candidate ratio, output error, router diagnostics.

Can Prove: whether the synthetic-supported retrieval signal survives a small real-token transfer check.

Cannot Prove: production speedup, long-context scalability, or general LM transfer.

Status: planned; not part of R1 synthetic closure.

Next Decision: execute only after R1 concludes E2 and E2.5 have non-random retrieval value.
