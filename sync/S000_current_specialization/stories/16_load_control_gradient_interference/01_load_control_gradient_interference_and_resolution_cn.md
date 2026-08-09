# 负载控制、梯度干扰与解决路线

## 0. 定义

- **硬专家负载：** 每个专家实际接收的 top-1 token 比例；其中最大值称为最忙专家占比。
- **Switch 负载均衡目标：** $L_{LB}=E\sum_e f_e\bar p_e$，同时使用停止梯度的硬分配比例 $f_e$ 和 Router 平均软概率 $\bar p_e$。
- **梯度冲突：** 在 Gate 或 Router 上游共享参数中，语言模型（LM）与负载均衡（LB）的原始梯度方向相反；本线用完整全局 batch 测量。
- **动态 expert bias：** 根据已经观察到的硬负载更新专家 logit 偏置、但不向模型参数注入辅助损失梯度的控制器；它目前是候选干预，不是已证实结论。

## 1. 摘要

A15 的匹配训练暴露了一个独立于频带效用的负载控制问题：所有相关 arm 都使用相同的 Switch 系数 $\lambda_{LB}=0.01$，但 Vanilla-Full 深层坍缩，Centered-Full 仍广泛使用专家。迁入 A16 的冻结反事实已经证明，真实的 token 共享 Router 输入分量会即时维持当前 Vanilla 坍缩；但把该分量加给另一条已适配的 Centered Router，并不足以特异地产生坍缩。因此 A16 当前要区分三种解释：LB 是否为了改善硬负载而损害 held-out 语言建模，是否只是有益正则，或是否根本无法控制饱和的 hard top-1。A16_00 以影子一步 held-out NLL 为主指标，以完整全局 batch 的原始梯度余弦为机制指标。只有这一审计支持有害干扰或 hard/soft 失配，动态 expert bias 才作为研究者批准的第一干预进入比较。

## 2. 研究问题

MoE 能否维持可用的专家负载，同时不减慢语言模型学习或阻碍有用的专家分化？当前局部决策更具体：从完全相同的早期 AdamW 状态和全局 batch 出发，加入 Switch LB 梯度是否一边改善硬负载，一边使下一步 held-out NLL 变差，并在 Router 参数中表现为方向相反的梯度？

## 3. 为什么旧问题表述不够

相同 LB 系数不等于相同硬路由；辅助损失数值大不等于纠正能力强；梯度余弦为负不等于 held-out 受损；负载均匀也不等于专家形成了有用分工。选择修复前必须把这些对象分开。

## 4. 数据与训练对象

源系统是已验证的四层、隐藏维 768、八个稀疏专家、top-1 DCLM MoE。A15 提供配对的 Vanilla-Full 与 Centered-Full 训练轨迹；迁入的 A16_00_01 使用冻结统计与验证文本。A16_00 将使用两个注册早期状态、完整累积全局 batch、参数/AdamW moment/scheduler/RNG/Router buffer 的精确副本，以及独立 held-out probe 文档。

## 5. 物理直觉

token 共享的输入分量经过线性 Gate 后，会变成不同专家各自固定的 logit 偏置，从而让同一个专家在大量 token 上获得一致的赢家 margin。Switch 目标通过软概率产生梯度，实际部署却使用硬 top-1 赢家；margin 饱和后，辅助惩罚可以很大，但改变赢家的能力依层和训练阶段变化。当前未知是：剩余的 LB 梯度只是无效、属于有益正则，还是确实反对语言模型学习。

## 6. 决策指标

主指标为

$$
\Delta NLL_{LB,t}=NLL_{probe}(T_{AdamW}(s_t,g_{LM}+g_{LB}))-NLL_{probe}(T_{AdamW}(s_t,g_{LM})).
$$

单位是 nat/token。正值表示从相同优化器状态出发，加入 LB 后，模型在独立文本上的下一步预测更差。它证明的是即时质量代价，不能直接外推长期训练。

机制指标为

$$
c_t=\frac{\langle g_{LM},g_{LB}\rangle}{\lVert g_{LM}\rVert\lVert g_{LB}\rVert+\epsilon}.
$$

$c_t<0$ 表示两个目标在注册参数组中局部相反，但它本身不能证明伤害。负载收益用最忙专家占比的配对变化衡量；负值表示加入 LB 后更均衡。

## 7. 最小机制模型

真正执行的更新不是原始梯度本身。AdamW 会利用一阶/二阶 moment、weight decay、学习率和 scheduler 状态变换 $g_{LM}+g_{LB}$。因此 A16 比较完整的影子状态，而不把余弦当成性能代理。Gate 权重与 Router 上游参数分开测；专家参数没有直接 LB 梯度，只能通过后续路由反馈受到影响。

## 8. 理论状态

目前没有定理证明 Switch LB 普遍伤害 MoE。已经验证的命题更窄：在注册的冻结 Vanilla 检查点上，减去独立估计的真实均值会方向特异地降低深层路由集中；Centered 的反向加回不具有方向特异充分性。A16_00 的梯度与影子更新命题仍未实验裁定。

## 9. 当前机制链

```text
Router 输入公共分量
-> 专家相对的固定 logit 偏置
-> 一致赢家 margin 与硬负载集中
-> soft LB 的纠正杠杆依层和阶段变化
-> LM/LB 更新关系仍未知
-> 按机制选择负载控制器
```

## 10. Anchor 结构

- [A16_00 父 Anchor](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor_cn.md)拥有 LM/LB 梯度与影子一步决策。
- [A16_00_01 DC 维持因素边界](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_01_dc_sustainer_boundary_anchor_cn.md)拥有已完成的冻结反事实。
- 动态 expert bias 与长期匹配效率仍是后续阶段，不提前建立正式 Anchor。

## 11. 证据链

1. A15 [10B 在线路由结果](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E01_10b_online_spectral_routing/summary.md)显示，相同 LB 系数可以对应完全不同的硬专家使用。
2. 迁入的 [DC 维持因素审计](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary_cn.md)裁定为 `necessary_only`：Vanilla 去真实均值使注册深层最忙专家占比下降 0.68678，区间 [0.68435, 0.68922]，高于匹配随机 q95 0.18326；Centered 加回中心未超过随机 q95。
3. 同一审计发现局部 LB logit 杠杆具有层与阶段异质性，而不是普遍梯度死亡。
4. 完整全局 batch 的 LM/LB 梯度、AdamW 实际作用与 held-out 影子一步 NLL 尚未测量。

## 12. 竞争解释

- **有益正则：** LM/LB 梯度局部相反，但 LB 在改善负载时保持或改善 held-out NLL。
- **hard/soft 失配：** LB 改变软概率却不改变硬赢家，因此任何 NLL 代价都是无效干扰，而不是必要交换。
- **优化器历史：** 原始梯度看似无害，但 AdamW moment 把它转换成有害的实际更新。
- **路由反馈：** 一步审计无害，长期专家暴露差异才导致减速。

## 13. 结论边界

现有证据不能说明所有辅助均衡损失有害、动态 expert bias 已经更好、一步效应会持续到长训练，或负载均匀会自然产生功能专家。A16 研究负载控制干扰；A15 在另一任务独立继续，A07 的 common/rare 专家参数梯度冲突仍是不同问题，A05 保留一般 top-1 坍缩机制。

## 14. 方法版图与解决路线

Switch/GShard 风格辅助目标是最常见基线。Loss-Free Balancing 与 DeepSeek-V3 提供动态 expert bias 的主要先例：直接根据硬负载调专家偏置，不向 LM 参数注入可微辅助梯度。BASE 与 Expert Choice 会改变分配语义，适合作为结构性参考而不是当前的第一匹配修复。capacity、z-loss、噪声和丢弃控制属于稳定器，不能单独回答当前机制问题。

解决顺序是：

```text
A16_00 区分有害冲突 / 有益正则 / 无效控制
-> 若有害冲突或 hard/soft 失配：比较动态 expert bias
-> 若有益正则：保留 LB，研究饱和与尺度
-> 最后做同 token、同 FLOPs 与真实 wall-clock 的训练效率比较
```

## 15. 与其他研究线的关系

A15 拥有频谱与 Relay 路由性能结论，并在另一任务独立继续；A05 拥有一般 top-1 锁定与公共偏置失败机制；A07 拥有专家学习内部的 common/rare 冲突；A16 独占 LM 主目标与负载控制器之间的作用，以及据此选择修复方案。

## 16. 唯一下一决策

Vanilla/Centered 的 A16_00 审计已获 Protocol、实现、smoke 与直接执行授权。
合格结果将裁定第一干预是 dynamic expert bias、保留可微 LB，还是修复
hard/soft 控制失配。完成标准是：LM-only 与 LM+LB 影子分支使用完全相同的
全局 batch 和完整优化器状态；冻结两个 seed 的早期状态与独立 probe 文档；
可重建原始梯度、硬负载变化与影子一步 NLL。结果产生前不启动 dynamic
expert bias 长训练。

## Source Map

- [Switch Transformer](https://jmlr.org/papers/v23/21-0998.html)
- [Loss-Free Balancing](https://arxiv.org/abs/2408.15664)
- [DeepSeek-V3](https://arxiv.org/abs/2412.19437)
- [BASE Layers](https://proceedings.mlr.press/v139/lewis21a/lewis21a.pdf)
- [Expert Choice Routing](https://arxiv.org/abs/2202.09368)
- [A16 研究线入口](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/README.md)
