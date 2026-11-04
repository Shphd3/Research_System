派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/audit_implementation_numerics.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/audit_implementation_numerics.md)；研究修改仍回到原件。

---

# Implementation and numerical audit

Registered at 2026-10-24T15:57:22.723159+00:00 before formal testing.

Protocol §§7/8/11/14 requires actual trainable counts, unchanged frozen weights, zero-output insertion, zero-LR, multi-token masks/EOS, native generation, optimizer displacement, cache calibration, telemetry and external next-step resume. Real coordinator receipts supply PASS evidence; this document does not infer checks from source inspection.
