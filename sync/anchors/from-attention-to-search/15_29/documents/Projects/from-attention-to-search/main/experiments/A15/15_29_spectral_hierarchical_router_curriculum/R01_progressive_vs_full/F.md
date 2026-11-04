派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/F.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/F.md)；研究修改仍回到原件。

---

# F: full-level spectral routing supervision

Formal job ID: **NOT_SUBMITTED**. Last verified state: **BLOCKED_SHARED8_SERIALIZATION_UNVERIFIED**. Target: **50,000,000,000 valid prediction tokens**. Resources: one node/eightRTX5090SPOT GPUs; active batchmicro8×acc2×world8×seq2048=262144. Fresh commoninitial/seed17; same teacher/tree/data/order/masks/optimization as the other arm. P ramps deeper coefficients by completedtoken clock; Fkeeps them1 fromstart; lambda warmup is shared.

Offline target and actual2GPU smoke/restart: PASS. Runtime/checkpoint location: /data/250010109/MoE_Router/experiments/20261031_spectral_hierarchical_router/runs/formal_F. No formal validation comparison is established. A config and launch script do not count as a submitted job. The user has not yet answered the proposed one-job serial scope amendment.

[Protocol](protocol.md) · [Detailed](detailed.md).
