# E3 Gating Failure Mode Diagnostic

E3 诊断一个核心现象：当 hidden representation 已经包含可分的 synthetic feature identity 时，linear top-1 MoE router 为什么仍然没有自然形成 clean feature-aligned expert partition。

阅读顺序：

1. `purpose_card.md`：目的链条和假设。
2. `execution_plan.md`：可运行设置和验收标准。
3. `summary.md`：full run 后的结论闭环。
4. `detailed.md`：完整表格、指标解释和图片索引。

旧的 `E3_synthetic_vs_real_statistics/` 暂缓；本文件夹是当前 E3 优先方向。
