---
experiment_id: A16_00_02_E01_multistage_gradient_pathway_audit
status: complete
scientific_verdict: fail_global_centering_mediation_with_early_stage_relief
last_updated: 2026-08-09
---

# 最终结果摘要

## 直接结论

严格假设不通过：**running-centering 没有跨两个种子和早、中、晚三个阶段普遍减少可微负载均衡（LB）目标的即时语言学习代价，也没有普遍减少 Router-source、Gate 和专家内部冲突。**

成立的是一个更窄的阶段性结论：在约 50M token 的早期状态，Vanilla 加入一次真正可微的 LB 更新，会使独立 WoS 文本的 NLL 上升 \(0.000845/0.000617\) nat/token；Centered 的对应变化接近零。两种模型之差为 \(+0.000839/+0.000630\)，两个种子的文档配对区间都高于零。因此 centering 在早期确实消除了一个可重复的 LB 即时代价，但该优势没有在所有后续阶段保持。

## 主指标

“LB 即时代价”是：从完全相同的参数、AdamW 状态和下一批 DCLM token 出发，分别做一次 LM-only 与 LM+LB 更新，再比较 112 篇独立 WoS 文档的 NLL。正值表示加入 LB 后下一步语言预测更差。Centered 中介效应

\[
M=\Delta NLL_{LB}^{Vanilla}-\Delta NLL_{LB}^{Centered}
\]

为正时，表示 centering 减少了这一代价。

| Seed | 50M 的 \(M\) | 6B 的 \(M\) | 10B 的 \(M\) | 三阶段中位数及 95% 区间 | 裁定 |
| --- | ---: | ---: | ---: | ---: | --- |
| 17 | +0.000839 | -0.001466 | +0.000242 | +0.000242 [\(-0.001474\), +0.000961] | Fail |
| 29 | +0.000630 | -0.000685 | +0.002152 | +0.000630 [+0.000376, +0.000938] | Pass |

Protocol 要求两个 seed 都通过，因此结果命题为 **Fail**，不是证据不足。

![Centering 中介效应](figures/figure2_centering_mediation.png)

## 梯度路径与专家机制

- **Router 共享路径：Fail。** 50M 时，Centered 的 Router-source 和 Gate 的 LM/LB 梯度余弦在两个 seed 中都更高，即目标较少相反；但 6B 与 10B 的两项增益转为负值，不能支持跨阶段冲突减少。
- **专家内部冲突：Fail。** 以 routed token 加权的专家负余弦质量在 Vanilla 中几乎为零，而 Centered 在 6B/10B 为约 \(4.0\times10^{-4}\) 到 \(5.5\times10^{-4}\)。这不应解释为 Vanilla 的专家更健康：Vanilla 的高度集中路由可把相似文档聚入少数专家，从而机械降低条件内冲突；它只否定“Centered 在该指标上更低”的预注册预测。
- **硬负载响应：** 一步 LB 使 Vanilla 四层平均最忙专家占比下降约 0.74--1.49 个百分点，而 Centered 只变化约 \(-0.18\) 到 \(+0.02\) 个百分点。Centered 本来更均衡，因此 LB 可施加的硬负载修正更小；该结果不能证明长期均衡已经解决。

![梯度路径](figures/figure3_pathway_cosine_gains.png)

## 有效性与边界

12/12 个“条件 × seed × 阶段”单元全部通过 checkpoint/optimizer、相同全局 batch、WoS hash、影子分支、同层专家直接导数为零和产物重建守卫；四个正式 8×5090 任务均成功结束。LM-only 修复分支与原 LM-only 更新逐张量相同；LM+LB 分支改变 130 个模型张量和全部八个 optimizer shard。

源 30B 训练还有一个关键边界：配置虽记录 `lambda_LB=0.01`，但 re-entrant activation checkpointing 使嵌套 LB 张量脱离 backward graph，因此这些 checkpoint **没有实际受到有效 LB 梯度训练**。本实验测量的是在冻结状态上让 LB 真正可微的一步反事实，不是原轨迹中 LB 的长期作用。

所以不能声称：centering 的长期优势来自普遍减少 LB 梯度冲突；专家负余弦越低必然越好；或一步结果可以预测 30B 训练效率。

## 下一决策

不把 A16 的首个解决方案定义成“去掉有害 LB 梯度”。下一步应比较 **Centered + 动态 expert bias、Centered + 真正可微 LB、Centered 无额外负载控制**，直接检验非梯度 hard-load 控制能否在不付出可微 LB 即时代价的情况下保持专家可用负载。

