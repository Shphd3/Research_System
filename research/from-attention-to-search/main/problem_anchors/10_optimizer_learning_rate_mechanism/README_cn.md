# A10: 优化器与学习率机制

[English](README.md) · [路线图](../../roadmap_cn.md) · [全部 Anchor](../README_cn.md)

公共梯度、奇异值集中与 SGD 稳定性。

本页只登记现有设计，不改变原文件科研状态、结论或下一决定。此线按 registry 的 registered_flat 布局保留，阅读依赖不自动变成目录父子关系。

新增 A10_03 是数值导数与实际更新的候选审查，真实回放 NOT RUN；A10_01/A10_02 保留原问题、状态与下一决定。

| 身份 | 原文问题名 | 正式设计 | 实验记录 |
|---|---|---|---|
| A10_01 | 10_01 Common-Projected SGD Learning-Rate Anchor | [原文](10_01_common_projected_sgd_lr_anchor.md) · [中文伴随版](10_01_common_projected_sgd_lr_anchor_cn.md) | [Records](../../experiments/A10/A10_01_common_projected_sgd_lr_synthetic) |
| A10_02 | 10_02 Frequency-Singular SGD Instability Anchor | [原文](10_02_frequency_singular_sgd_instability_anchor.md) · [中文伴随版](10_02_frequency_singular_sgd_instability_anchor_cn.md) | [Records](../../experiments/A10/A10_02_frequency_singular_sgd_instability) |
| A10_03 | Router 数值误差是否改变一次有限学习更新（待审阅草案） | [English](10_03_router_numerical_update_fidelity_anchor.md) · [中文](10_03_router_numerical_update_fidelity_anchor_cn.md) | [源码与校准](../../research_notes/router_numerical_fidelity/20261024_scope_audit_cn.md)；真实回放 NOT RUN |

[完整归属登记](../../anchor_ownership.json) · [组织迁移来源](../../organization_migrations/20261022/README_cn.md)
