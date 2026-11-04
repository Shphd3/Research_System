派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/P.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/P.md)；研究修改仍回到原件。

---

# P: progressive spectral routing supervision

Formal job ID: **om-867vcrpa**. Last verified state: **STARTING**. Target: **50,000,000,000 valid prediction tokens**. Resources: one node/eightRTX5090SPOT GPUs; active batchmicro8×acc2×world8×seq2048=262144. Fresh commoninitial/seed17; same teacher/tree/data/order/masks/optimization as the other arm. P ramps deeper coefficients by completedtoken clock; Fkeeps them1 fromstart; lambda warmup is shared.

Offline target and actual2GPU smoke/restart: PASS. Runtime/checkpoint location: /data/250010109/MoE_Router/experiments/20261031_spectral_hierarchical_router/runs/formal_P. No formal validation comparison is established. P accepted first; F remains unsubmitted to preserve the researchers shared8GPUlimit.

[Protocol](../../../../../../../../UNAVAILABLE.md) · [Detailed](detailed.md).
