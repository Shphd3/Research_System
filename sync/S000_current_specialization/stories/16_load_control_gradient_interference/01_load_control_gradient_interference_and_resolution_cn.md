# 负载控制、梯度干扰与解决路线

## 0. 定义

- **硬专家负载：** 每个专家实际接收的 top-1 token 比例；其中最大值称为最忙专家占比。
- **Switch 负载均衡目标：** $L_{LB}=E\sum_e f_e\bar p_e$，同时使用停止梯度的硬分配比例 $f_e$ 和 Router 平均软概率 $\bar p_e$。
- **梯度冲突：** 在 Gate 或 Router 上游共享参数中，语言模型（LM）与负载均衡（LB）的原始梯度方向相反；本线用完整全局 batch 测量。
- **动态 expert bias：** 根据已经观察到的硬负载更新专家 logit 偏置、但不向模型参数注入辅助损失梯度的控制器；它目前是候选干预，不是已证实结论。

## 1. 摘要

A15 匹配训练显示 Vanilla-Full 与 Centered-Full 的硬负载明显不同；迁入 A16 的冻结反事实进一步证明，真实的 token 共享 Router 输入分量会即时维持 Vanilla 坍缩。A16 随后发现，源训练虽然记录 $\lambda_{LB}=0.01$，但 re-entrant activation checkpointing 使嵌套辅助张量脱离 backward graph，因此并未真正施加 LB 梯度。合格的反事实影子审计在配对的 50M、6B、10B 状态让 LB 真正可微：centering 在 50M 可复现地消除了早期 LB 代价，但没有在后续状态普遍减少 held-out 代价、Router 路径冲突或专家内部冲突。下一问题不再是“证明 LB 普遍有害”，而是非梯度 dynamic expert bias 能否在 Centered 模型中比有效可微 LB 更高效地控制硬负载。

## 2. 研究问题

MoE 能否维持可用的专家负载，同时不减慢语言模型学习或阻碍有用的专家分化？已完成的局部诊断问：centering 是否减少有效 Switch LB 的一步 held-out 代价和梯度对立；全局答案是否定的，但存在可复现的早期例外。下一局部决策是 dynamic expert bias 能否在匹配 Centered 训练中优于有效 LB 和无额外控制器。

## 3. 为什么旧问题表述不够

相同 LB 系数不等于相同硬路由；辅助损失数值大不等于纠正能力强；梯度余弦为负不等于 held-out 受损；负载均匀也不等于专家形成了有用分工。选择修复前必须把这些对象分开。

## 4. 数据与训练对象

源系统是已验证的四层、隐藏维 768、八个稀疏专家、top-1 DCLM MoE。A16_00_02 使用 Vanilla-Full 与 Centered-Full 的 seed 17/29，在 50M、6B、10B 状态精确重放下一批 DCLM 数据、完整优化器状态和 112 篇独立 WoS 验证文档；12 个单元全部通过有效性守卫。

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

目前没有定理证明 Switch LB 普遍伤害 MoE。已经验证的命题更窄：去均值会即时降低冻结 Vanilla 的集中；centering 会消除 50M 状态可复现的有效 LB 代价；该代价并不稳定延续到 6B/10B。注册的“跨阶段普遍减少干扰”假设已经失败。

## 9. 当前机制链

```text
Router 输入公共分量
-> 专家相对的固定 logit 偏置
-> 一致赢家 margin 与硬负载集中
-> 有效 soft LB 的质量与硬负载作用依阶段变化
-> centering 只减少早期代价，而非所有后续冲突
-> 比较非梯度硬负载控制与有效 LB
```

## 10. Anchor 结构

- [A16_00 父 Anchor](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor_cn.md)拥有 LM/LB 梯度与影子一步决策。
- [A16_00_01 DC 维持因素边界](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_01_dc_sustainer_boundary_anchor_cn.md)拥有已完成的冻结反事实。
- 动态 expert bias 与长期匹配效率仍是后续阶段，不提前建立正式 Anchor。

## 11. 证据链

1. A15 [10B 在线路由结果](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E01_10b_online_spectral_routing/summary.md)显示，相同 LB 系数可以对应完全不同的硬专家使用。
2. 迁入的 [DC 维持因素审计](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary_cn.md)裁定为 `necessary_only`：Vanilla 去真实均值使注册深层最忙专家占比下降 0.68678，区间 [0.68435, 0.68922]，高于匹配随机 q95 0.18326；Centered 加回中心未超过随机 q95。
3. 源训练审计发现配置中的 LB 张量脱离 backward，因此相同系数只是配置事实，不是 active loss 事实。
4. 已完成的[多阶段审计](/Projects/from-attention-to-search/main/experiments/A16/A16_00_02_E01_multistage_gradient_pathway_audit/summary_cn.md)发现，两个 seed 在 50M 的 Centered 中介都为正，但只有 seed 29 通过注册的三阶段摘要；共享路径与专家冲突条款均失败。

## 12. 竞争解释

- **有益正则：** LM/LB 梯度局部相反，但 LB 在改善负载时保持或改善 held-out NLL。
- **hard/soft 失配：** LB 改变软概率却不改变硬赢家，因此任何 NLL 代价都是无效干扰，而不是必要交换。
- **优化器历史：** 原始梯度看似无害，但 AdamW moment 把它转换成有害的实际更新。
- **路由反馈：** 一步审计无害，长期专家暴露差异才导致减速。

## 13. 结论边界

现有证据既不能说明所有辅助均衡损失有害，也不能说明 dynamic expert bias 已经更好。由于源训练没有施加有效 LB，影子审计只是冻结状态上的反事实，不能建立长期作用或有用专业化。A16 与 A15 频谱效用、A07 common/rare 专家冲突和 A05 一般 top-1 坍缩保持分离。

## 14. 方法版图与解决路线

Switch/GShard 风格辅助目标是最常见基线。Loss-Free Balancing 与 DeepSeek-V3 提供动态 expert bias 的主要先例：直接根据硬负载调专家偏置，不向 LM 参数注入可微辅助梯度。BASE 与 Expert Choice 会改变分配语义，适合作为结构性参考而不是当前的第一匹配修复。capacity、z-loss、噪声和丢弃控制属于稳定器，不能单独回答当前机制问题。

解决顺序是：

```text
A16_00 已完成阶段特异的冲突 / 正则 / 硬负载审计
-> 比较 Centered + dynamic bias / 有效 LB / 无控制器
-> 最后做同 token、同 FLOPs 与真实 wall-clock 的训练效率比较
```

## 15. 与其他研究线的关系

A15 拥有频谱与 Relay 路由性能结论，并在另一任务独立继续；A05 拥有一般 top-1 锁定与公共偏置失败机制；A07 拥有专家学习内部的 common/rare 冲突；A16 独占 LM 主目标与负载控制器之间的作用，以及据此选择修复方案。

## 16. 唯一下一决策

Vanilla/Centered 多阶段审计已经完成。唯一下一决策是 Centered + dynamic
expert bias 是否比 Centered + 真正可微 LB 和 Centered 无额外控制器更好地
维持硬负载与 held-out NLL/FLOP。比较必须匹配两个 seed、初始化、数据顺序、
capacity、token 和计算量；当前审计本身不能批准任何赢家。

## Source Map

- [Switch Transformer](https://jmlr.org/papers/v23/21-0998.html)
- [Loss-Free Balancing](https://arxiv.org/abs/2408.15664)
- [DeepSeek-V3](https://arxiv.org/abs/2412.19437)
- [BASE Layers](https://proceedings.mlr.press/v139/lewis21a/lewis21a.pdf)
- [Expert Choice Routing](https://arxiv.org/abs/2202.09368)
- [A16 研究线入口](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/README.md)
