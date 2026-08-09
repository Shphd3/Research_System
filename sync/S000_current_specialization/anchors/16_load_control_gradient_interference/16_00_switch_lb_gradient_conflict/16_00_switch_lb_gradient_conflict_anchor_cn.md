# A16_00 Switch 负载均衡梯度冲突

Thinking Card 来源：[16_00_switch_lb_gradient_conflict_thinking_card_cn.md](16_00_switch_lb_gradient_conflict_thinking_card_cn.md)

## 1. Problem Definition

A16 研究如何在维持稀疏专家可用负载的同时，不减慢语言模型学习或阻碍专家形成。已有证据说明真实的 token 共享 Router 输入分量会即时维持冻结 Vanilla 的坍缩，但它没有判断可微负载目标、语言模型目标、AdamW 历史或硬路由反馈中的哪一项形成了该状态。

唯一决策问题是：**在最早 100M token 内，从完全相同的参数、优化器状态和全局训练 batch 出发，加入 Switch 风格负载均衡梯度是否一边改善硬专家负载，一边使下一步 held-out NLL 变差，并在受影响的 Router 参数组中出现 LM/LB 原始梯度负余弦？**

这里的“梯度冲突”是语言模型（LM）目标与负载均衡（LB）目标在 Gate 或 Router 上游共享参数中的方向相反，不是 A07 在专家参数内部测量的 common/rare 梯度冲突。Pass 使非梯度负载控制成为第一修复；Fail 保留辅助 LB 或转向 hard/soft 控制失配；影子状态不一致或全局梯度不完整则为 Insufficient。

## 2. Physical Priors

1. 可微辅助目标可以改善自己的统计量，同时在共享参数上反对主目标下降；若 LB 影子更新不使独立 LM NLL 变差，该先验不成立。
2. 原始梯度负余弦只是机制证据，不是结果证据：有意正则化也可能反对当前训练梯度，却改善 held-out NLL。
3. 负载控制只有在改变硬专家使用时才有意义；若质量变差但硬集中没有下降，这是无效干扰，不是负载—质量交换。

## 3. Falsifiable Hypotheses

- **H1，有害 LB 干扰：** LM+LB 影子一步的 held-out NLL 高于 LM-only，同时最忙专家占比下降，并且 Gate 或 Router 上游参数的 LM/LB 全局 batch 梯度余弦为负。
- **最强竞争解释，有益正则：** 原始梯度可以局部相反，但加入 LB 不使 held-out NLL 变差，甚至在负载更均衡时改善它。
- **控制失配解释：** 加入 LB 没有实际降低硬集中，因此坍缩来自 soft probability 与 hard top-1 的失配、饱和或路径反馈，而不是成功均衡所支付的代价。

Pass 要求两个注册 seed 分别出现 H1 签名。若 held-out 代价不存在或梯度机制不相反则为 Fail；若负载不改善，则转向直接硬负载控制，但不能称 LB 梯度有害。两个 seed 方向相反、影子状态不一致或缺少完整 batch 梯度时为 Insufficient。

## 4. Mathematical Model

在训练状态 $s_t$，令 $g_{LM}$ 为语言模型原始梯度，$g_{LB}=\lambda_{LB}\nabla L_{LB}$ 为乘上系数后的负载梯度。对一个注册参数组，全局 batch 余弦为

$$
c_t=\frac{\langle g_{LM},g_{LB}\rangle}
{\lVert g_{LM}\rVert\lVert g_{LB}\rVert+\epsilon}.
$$

$c_t<0$ 表示局部目标相反，但不能单独证明伤害。令 $T_{AdamW}(s,g)$ 从包含 moment 与 scheduler 的完整相同状态 $s$ 执行一个影子 AdamW 更新，主指标为

$$
\Delta NLL_{LB,t}
=NLL_{probe}\!\left(T_{AdamW}(s_t,g_{LM}+g_{LB})\right)
-NLL_{probe}\!\left(T_{AdamW}(s_t,g_{LM})\right).
$$

单位为 nat/token；正值表示当前 LB 分量使独立文本的一步预测变差。配对硬负载效应为 $\Delta M_t=M_{LM+LB}-M_{LM}$，$M$ 是最忙专家占比，$\Delta M_t<0$ 表示负载改善。这些量只能建立即时优化交换，不能证明长期因果或专家功能价值。

## 5. Computational Realization

使用已验证的四层、隐藏维 768、八专家、top-1 DCLM MoE，以及配对的 Vanilla-Full 与 Centered-Full 条件。在两个 seed 的注册早期状态上，重放完全相同的全局 optimizer batch，包括全部梯度累积 microbatch 与分布式归约；分别计算 LM-only 和 LB-only 原始梯度，不推进数据游标或优化器。

复制完整参数、AdamW moment、scheduler、随机数状态和 Router buffer。分别执行 LM-only 与 LM+LB 影子一步，再在同一组未用于更新的独立文档和固定负载 token 上评估。逐层记录 Gate 权重与 Router 输入上游参数的余弦、范数和实际更新对齐；把梯度投影到独立注册的 DC 与去中心残差方向，以衔接已完成的 DC 审计。专家参数没有直接 LB 梯度，其变化属于后续路由反馈问题。

## 6. Minimal Falsification Tests

决定性比较是配对影子一步的 $\Delta NLL_{LB}$。结果在预注册早期状态和文档上聚合，但两个 seed 分开报告。主规则不设人为 practical margin：两个 seed 各自的文档 bootstrap 95% 下界都必须大于零。机制支持还要求同一参数组的注册全局 batch 余弦为负，并且最忙专家占比配对下降。完整 batch 身份、精确状态复制、优化器重放、独立评估文档、确定性 Router buffer 与梯度重构是硬守卫。

known-good 包括人为构造的相反标量目标，以及能够降低已构造硬失衡的 LB-only 扰动；known-bad 包括相同目标、零 LB 系数和打乱的 LB 梯度。负余弦但 $\Delta NLL_{LB}$ 不为正支持有益正则解释；$\Delta NLL_{LB}>0$ 但负载不改善支持无效干扰。该测试不能选出最佳长期控制器。

## 7. Current Evidence

六个相关 30B 训练条件都使用相同的 Switch 风格系数 $\lambda_{LB}=0.01$，但 Vanilla-Full 深层在约 50M--100M token 接近单专家，Centered-Full 仍广泛使用专家。因此系数相同并不保证硬负载行为相同。

迁入的冻结反事实裁定为 `necessary_only`：Vanilla 去掉独立估计的真实均值后，注册深层最忙专家占比下降 0.68678，配对 95% 区间为 [0.68435, 0.68922]，远高于匹配随机 q95 0.18326；给独立训练的 Centered 加回中心则没有超过随机对照。公共分量因此即时维持当前 Vanilla 坍缩，但静态加回不能重建已经分别适配的训练路径。[迁入的子 Anchor](subanchors/16_00_01_dc_sustainer_boundary_anchor_cn.md)和[结果记录](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary_cn.md)保存该边界。

同一审计没有发现“坍缩后 LB 梯度普遍归零”的统一规律：局部 softmax 杠杆随层和检查点变化。LM/LB 全局 batch 梯度、AdamW 实际更新和影子一步 NLL 尚未测量，因此 A16_00 仍未获得实验裁定。

## 8. Claim Boundary And Next Decision

已支持：DC 是冻结 Vanilla 当前坍缩的方向特异即时维持因素，相同系数不等于相同硬负载控制。仍未解决：辅助 LB 是否付出 held-out 学习代价、是否属于有益正则，或是否只是无法改变饱和硬路由。

本 Anchor 不能声称所有辅助损失都有害、动态 expert bias 已经更好、早期一步效应会持续到长训练，或负载更好就会形成有用专家。动态 expert bias 只是在 A16_00 支持有害干扰或 hard/soft 失配后的研究者首选干预。

研究者已经批准 Vanilla-Full 与 Centered-Full 的早期梯度—影子更新实验，
授权范围包括 Protocol、实现、smoke 与直接执行。唯一下一决策改为：在获得
合格结果后，选择 dynamic expert bias、保留可微 LB，或修复 hard/soft 控制
失配。完成标准是两个 seed、两种模型条件都保持全局 batch 与完整 optimizer
状态一致，并按冻结规则重建 $\Delta NLL_{LB}$、硬负载变化和 batch 梯度余弦。
恢复时先冻结并执行该 Protocol，不先启动 dynamic bias 长训。
