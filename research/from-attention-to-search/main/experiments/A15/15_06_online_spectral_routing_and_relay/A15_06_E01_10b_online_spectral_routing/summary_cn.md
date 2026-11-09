---
experiment_id: A15_06_E01_10b_online_spectral_routing
legacy_experiment_id: A15_00_E01_10b_five_arm_training
status: complete
scientific_verdict: does_not_support_relay_hmt
last_updated: 2026-08-03
---

# 最终结果摘要

## 直接结论

本实验**不支持 Relay-HMT**：10B 终点上，Relay-HMT 在两个 seed 中都明确
劣于 Local-HMT 和 Centered-Full，也没有稳定超过同维 Relay-Random。

Local-HMT 在两个 seed 上都是最低 NLL 点估计，但它相对 Centered-Full 的
配对优势只在 seed 17 明确，seed 29 区间跨零，因此尚不能宣布 Local-HMT
稳定胜出。唯一大幅且跨 seed 复现的收益来自去均值：Centered-Full 相对
Vanilla-Full 分别改善 0.113 和 0.128 nat/token。

| 比较 | Seed 17，95% CI | Seed 29，95% CI | 裁定 |
|---|---:|---:|---|
| Centered − Vanilla | −0.11254 [−0.11445, −0.11074] | −0.12795 [−0.13003, −0.12596] | 去均值 Pass |
| Local − Centered | −0.00510 [−0.00654, −0.00371] | −0.00056 [−0.00211, +0.00098] | 未跨 seed 通过 |
| Relay-HMT − Local | +0.01436 [+0.01280, +0.01590] | +0.00689 [+0.00535, +0.00846] | H2 Fail |
| Relay-HMT − Relay-Random | −0.00266 [−0.00420, −0.00115] | +0.00026 [−0.00123, +0.00175] | H3 Fail |

## 在线更新结论

在线更新器成功解决了连续性问题，但没有带来 Relay 质量收益：HMT 的部署
子空间明显比不更新更接近当前目标；全部刷新中高置信 token 的最大实际翻转率
为 0，而 10B 直接硬切换目标会使 Local/Relay-HMT 约 25%--38% 的高置信
token 换专家。刷新前后的训练 loss 没有一致跳变。

## 认识边界与下一决策

现有结果不能把 Local-HMT 的弱点估计优势归因于 covariance 身份，因为没有
Local-Random。唯一下一决策是：是否增加一个目标运动量和追踪精度都匹配的
Local-Random，对 Local-HMT 与 Centered-Full 做两 seed 配对复核。

完整自包含报告：
[0803 训练报告](../../../../../../../daily_research_reports/backup/2026/08/0803/online_spectral_router_10b_training_report/report.md)。
