派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/sources/runtime_record_note.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/sources/runtime_record_note.md)；研究修改仍回到原件。

---

# Execution-time record

The original117-row plan is preserved. A rough pre-run tool estimate used1800–3600 seconds per trajectory (58.5–117 GPU-hours before gates), but plan regeneration replaced its estimate column with UNKNOWN. This is an operational record deviation, not observed throughput or a pre-run measured ETA. Actual stage timings remain in metrics/complete receipts and actual_runtime.csv. Qualification branches reduced the executed matrix to14 trajectories. No scientific comparison used wall-clock time or a changed training budget.
