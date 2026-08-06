---
anchor_id: A09_01_common_band_rare_discrimination
parent_node: rq.expert_specialization
status: controlled_supported
created: 2026-06-29
canonical_language: zh-CN
source_docs:
  - ../../../../../daily_research_reports/backup/2026/06/0629/docs/nested_prediction_spectral_anisotropy_causal_rewrite_v4.md
  - ../../../../../daily_research_reports/backup/2026/06/0626/recordings/r1.md
  - ../06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/subanchors/06_01_06_spectral_reservoir_method_audit_anchor.md
---

# A09_01 常见高增益带 / 稀有判别 Anchor

Thinking Card source: [09_01_common_band_rare_discrimination_thinking_card_cn.md](09_01_common_band_rare_discrimination_thinking_card_cn.md)

## 1. 问题定义

**Parent problem:** 真实 MoE 分工不能只看路由相似度，还要证明专家分开有功能价值。

**Sharper subproblem:** 判断 common 高增益带是否压制 rare 判别，以及 MoE 分开是否真的缓解它。

**Decision question:** common 高增益带是否“大但不判别”，并且有效 MoE 分开是否能降低这种错配？

**Not in scope:** 真实语义专家、最终方法、长训练、规模外推。

## 2. 物理先验

**P1: common 高增益带可能主导分数。**
含义：common 特征的高增益方向会放大输出分数或注意力分数。
可能错：高增益带同时也是最强判别信息来源。

**P2: rare 信息可能分数小但更会判别。**
含义：rare 关系可能在剩余带里，分数小但更能区分正确目标。
可能错：rare 判别也主要来自高增益带。

**P3: 方法收益必须带来机制变化。**
含义：rare 损失降低不够；机制指标也要动。
可能错：错配差与 rare 损失完全无关。

## 3. 可证伪假设

**H1:** 失败的 rare 样本有高错配差。
支持：高增益带分数占比高，但判别占比低。
削弱：高增益带已经给出正确判别。

**H2:** 有效 common/rare 分开会降低错配差。
支持：分开降低错配差和 rare 损失，而同容量随机分开不能做到。
削弱：rare 损失改善，但错配差不动。

## 4. 数学模型

**Objects:** 隐状态 $h$, 读出矩阵 $W$, 高增益带投影 $P_k$, 正确目标 $y$, common 干扰项 $c$.

**Core decomposition:** 把输出分数拆成高增益带和剩余带。

$$
z = W P_k h + W(I-P_k)h = z^{top}+z^{res}.
$$

**Mechanism metric:** 衡量“声音大但不判别”的错配。

$$
G_{mis}(k)=C_{score}(k)-C_{disc}(k).
$$

$C_{score}(k)$：高增益带占总分数大小的比例。
$C_{disc}(k)$：高增益带占正确目标相对干扰项判别的比例。

**Falsifier:** 分开改善 rare 损失，但 $G_{mis}(k)$ 不下降，或随机分开同样下降。

## 5. 计算实现

**Input objects:** 已知 common / rare 方向的受控 nested 数据。

**Computed variables:** 高增益带、剩余带、common 干扰项差距、rare 损失、分开条件对照表。

**Algorithm stages:** 训练基线 -> 分解分数 -> 找错配 -> 测分开和对照。

**Stage-local evidence:** 分数占比曲线、判别占比曲线、rare 损失表、容量对照。

**Expected artifacts:** protocol, summary, detailed, 一张主图，一张小表。

## 6. 最小证伪测试

**Test:** 受控 common/rare 谱错配审计。

**Question:** common 高增益带是否拿走很多分数，但没有同等贡献 rare 判别？

**Intervention / comparison:** 共享模型、common/rare 分开、同容量随机分开、已知答案分开。

**Primary metric:** rare 匹配样本上的 $G_{mis}(k)$ 变化。

**通过 / 失败 / 证据不足:** 通过：基线错配差为正，分开同时降低错配差和 rare 损失；失败：错配不存在，或随机分开解释收益；证据不足：common/rare 方向不可审计。

**失败含义:** 没识别出 common 高增益带压制 rare 判别这个机制。

## 7. 当前证据

**A09_01 结果：** 受控合成数据支持该机制。audit rank 4 时，共享基线 $G_{mis}=0.486$，其中 $C_{score}=0.819$，$C_{disc}=0.332$。estimated common/rare split 把 $G_{mis}$ 降到约 0，rare 损失改善 0.996，同时 common 分支保持。

**对照：** 同容量随机分开让 rare loss 更低，但没有降低错配，并且 common 分支坏掉。因此它可以解释“rare loss 变好”，但不能解释完整机制模式。

**负控：** 打乱 rare 标签后也能通过投影降低错配，但 rare loss 变差。这说明只看错配下降也不够，必须同时看 rare loss。

**Observation:** `A06_01_06_E01/E02` 支持“稳定方向可以转成路由”的受控结果。

**Observation:** `A06_01_06_E03` 和 A07_06 提醒我们：只看损失改善，可能误判机制。

**Observation:** A06 显示初始化可以做成，但真实 DCLM 上普通训练不能稳定保存。

**Interpretation:** 下一步应测试 common/rare 功能机制，而不是只看初始化。

**Boundary:** 目前只有受控数据结论，还没有真实数据结论。

## 8. 结论边界和下一步

**当前可以声称:** 在受控数据上，common 高增益带主导是一种可测的 rare 判别失败模式；estimated common/rare split 可以降低该错配并保持 common 行为。

**不能声称:** 真实语义专家、可部署 MoE 方法、真实 DCLM 价值。

**Next decision:** 下一步测试真实模型状态或更真实 proxy rare target 上是否也能测到 $C_{score}$ / $C_{disc}$ 错配。
