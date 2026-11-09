---
experiment_id: A15_06_E03_30b_single_seed_extension
status: complete
scientific_verdict: complete_seed17_persistence_with_relay_failure
last_updated: 2026-08-09
---

# 最终结果摘要

六个 seed-17 模型均完整续训到30B。Local-HMT 的 DCLM NLL 最低
（3.391913），相对 Centered-Full 低 0.004072 nat/token，相对 Local-Random
低 0.004886，逐文档配对区间均支持该方向；Relay-HMT 则相对 Local-HMT
高 0.015617、相对 Centered 高 0.011545，明确更差。

这只证明 seed 17 的晚期排序持续存在，不能恢复跨 seed 的 covariance 身份结论，
因为注册的 seed 29 10B 对照没有复现。A16 后续还发现这些源训练虽然日志记录了
LB 值，但 LB 辅助张量没有真正参与反向；六模型比较仍有效，却不是有效 LB 正则
的证据。

完整八任务结果见 [A15_06_E04](../A15_06_E04_30b_downstream_evaluation/summary_cn.md)。

