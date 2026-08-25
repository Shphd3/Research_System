---
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
source_report: docs/random_projection_router_meeting_report.md
---

# 随机投影 Router：组会最小汇报

## 核心问题：

Qwen3-30B-A3B 的 $R_U$ 在哪一层真正增加了 $X$ 之外的预测信息；这种信息是否已经形成可独立使用的稳定正-margin Router 空间；若形成，随机投影能否保持？

## 目的：

区分三种瓶颈：旧层号迁移错误、$R_U$ 没有新增信息、已有信息但尚未组织成稳健路由几何，从而决定是继续压缩还是转向表征空间学习。

## 分析方法：

1. 冻结 taxonomy 与 19,200 条 binding 数据，复核词袋、泄漏、分片和表征代数守卫；
2. 在 Qwen3-30B-A3B 全 48 层测 $R_U$ 超过同层 $X$、重复 $X$ 和错配 $R_U$ 后的受控增益，只用 TRAIN/DEV 冻结层；
3. 在冻结 block 48/38 上检验 H2/H3，仅在主层 H3 通过时运行 H4，并以精确全对距离和监督正交功能秩解释边界。

## 结论：

**理论证据：** 稠密高斯投影只能保持已有的正距离/正 margin，不能创造原空间不存在的线性可分性；H3 因而是 H4 的硬门槛。

**实验信息证据：** H0 `Pass`。31/48 层有正受控增量效用；峰值是 block 39，0.10994 nat/样本，95% 同时区间 [0.09872, 0.12080]。所以 $R_U$ 不是“没有信息”。

**实验几何证据：** 按独立 $R_U$ DEV 低尾 margin 冻结的主层 48、重复层 38 在 TEST 上都 H3 `Fail`；四个 5% margin 为 -5.82955、-11.19046、-3.52356、-6.66276，区间全部低于 0。精确距离比为 0.2027--0.3321，全部小于 1。H4 因此 `SKIPPED_H3_NOT_PASS`。

**白话结论：** 信息已经以“依赖同层 $X$ 的增量”形式存在，但还没有被整理成 $R_U$ 单独可用的稳定 Router 空间。层选错不是唯一问题；当前根本问题是信息组织方式，而不是随机投影维数。

**建议决策：** 确认开启表征空间学习，但先做最小实验：以真实专家效用或可审计 proxy 为目标，比较 learned standalone representation 与 joint $(X,R_U)$，用真正 held-out 的低尾 margin 是否转正作停止门槛。独立人工 H1 review 和本段认识更新仍需研究者确认。

![最核心结果图](../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/figures/qwen30b_ru_layer_gain_curve.png)
