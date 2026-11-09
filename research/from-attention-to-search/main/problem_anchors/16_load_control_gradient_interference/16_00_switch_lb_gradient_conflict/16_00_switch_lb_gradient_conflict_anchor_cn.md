# A16_00 Switch 负载均衡梯度冲突


## 1. Problem Definition

A16 研究如何在维持稀疏专家可用负载的同时，不减慢语言模型学习或阻碍专家形成。已有证据说明真实的 token 共享 Router 输入分量会即时维持冻结 Vanilla 的坍缩，但它没有判断可微负载目标、语言模型目标、AdamW 历史或硬路由反馈中的哪一项形成了该状态。

唯一决策问题是：**在注册的早期、中期和后期状态中，从完全相同的参数、优化器状态和全局训练 batch 出发，加入 Switch 风格负载均衡梯度是否一边改善硬专家负载，一边使下一步 held-out NLL 变差；running-centering 是否同时减少该代价以及 Router-source、Gate 与路由后专家更新路径中的冲突？**

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

在训练状态 \(s_t\)，令 \(g_{LM}\) 为语言模型原始梯度，\(g_{LB}=\lambda_{LB}\nabla L_{LB}\) 为乘上系数后的负载梯度。对一个注册参数组，全局 batch 余弦为

\[
c_t=\frac{\langle g_{LM},g_{LB}\rangle}
{\lVert g_{LM}\rVert\lVert g_{LB}\rVert+\epsilon}.
\]

\(c_t<0\) 表示局部目标相反，但不能单独证明伤害。令 \(T_{AdamW}(s,g)\) 从包含 moment 与 scheduler 的完整相同状态 \(s\) 执行一个影子 AdamW 更新，主指标为

\[
\Delta NLL_{LB,t}
=NLL_{probe}\!\left(T_{AdamW}(s_t,g_{LM}+g_{LB})\right)
-NLL_{probe}\!\left(T_{AdamW}(s_t,g_{LM})\right).
\]

单位为 nat/token；正值表示当前 LB 分量使独立文本的一步预测变差。配对硬负载效应为 \(\Delta M_t=M_{LM+LB}-M_{LM}\)，\(M\) 是最忙专家占比，\(\Delta M_t<0\) 表示负载改善。这些量只能建立即时优化交换，不能证明长期因果或专家功能价值。

## 5. Computational Realization

使用已验证的四层、隐藏维 768、八专家、top-1 DCLM MoE，以及配对的 Vanilla-Full 与 Centered-Full 条件。在两个 seed 的 50M、6B、10B 注册状态上，重放完全相同的全局 optimizer batch，包括全部梯度累积 microbatch 与分布式归约；分别计算 LM-only 和 LB-only 原始梯度，不推进数据游标或优化器。

复制完整参数、AdamW moment、scheduler、随机数状态和 Router buffer。分别执行 LM-only 与 LM+LB 影子一步，再在同一组未用于更新的独立文档和固定负载 token 上评估。逐层记录 Gate 权重与 centering 前实际 Router-source 张量的余弦、范数和实际更新对齐；在固定、按领域分层的 Web of Science 文档上测量被送入同一专家的文档组之间的 LM 梯度冲突。专家参数没有直接 LB 梯度；若出现直接梯度是实现失败，专家侧测量属于路由中介效应。

## 6. Minimal Falsification Tests

决定性比较是 50M、6B、10B 三个阶段中 Centered 对配对影子一步 \(\Delta NLL_{LB}\) 的中介效应，阶段与 seed 分开报告。主规则不设人为 practical margin：两个 seed 各自冻结的阶段中位数文档 bootstrap 95% 下界都必须大于零，并且每个 seed 至少两个阶段方向一致。Router-source/Gate 冲突和路由后 WoS 专家冲突分别给 typed verdict。完整 batch 身份、精确状态复制、优化器重放、独立评估文档、确定性 Router buffer 与梯度重构是硬守卫。

known-good 包括人为构造的相反标量目标，以及能够降低已构造硬失衡的 LB-only 扰动；known-bad 包括相同目标、零 LB 系数和打乱的 LB 梯度。负余弦但 \(\Delta NLL_{LB}\) 不为正支持有益正则解释；\(\Delta NLL_{LB}>0\) 但负载不改善支持无效干扰。该测试不能选出最佳长期控制器。

## 7. Current Evidence

六个相关 30B 训练条件都使用相同的 Switch 风格系数 \(\lambda_{LB}=0.01\)，但 Vanilla-Full 深层在约 50M--100M token 接近单专家，Centered-Full 仍广泛使用专家。因此系数相同并不保证硬负载行为相同。

迁入的冻结反事实裁定为 `necessary_only`：Vanilla 去掉独立估计的真实均值后，注册深层最忙专家占比下降 0.68678，配对 95% 区间为 [0.68435, 0.68922]，远高于匹配随机 q95 0.18326；给独立训练的 Centered 加回中心则没有超过随机对照。公共分量因此即时维持当前 Vanilla 坍缩，但静态加回不能重建已经分别适配的训练路径。[迁入的子 Anchor](subanchors/16_00_01_dc_sustainer_boundary_anchor_cn.md)和[结果记录](../../../experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary_cn.md)保存该边界。

完整 12 单元审计否定“centering 在所有阶段普遍减少 LB 冲突”的解释。50M 时，Vanilla 支付了可复现的 +0.000845/+0.000617 nat/token 有效 LB 影子代价，Centered 无法区别于零，两个 seed 的 Centered 中介均为正；6B 点估计反转，10B 只有 seed 29 精确为正。seed 17 的注册三阶段中位数区间跨零、seed 29 通过，因此两 seed 结果裁定为 Fail。Router 共享路径与专家内部冲突条款也都失败。[多阶段结果](../../../experiments/A16/A16_00_02_E01_multistage_gradient_pathway_audit/summary_cn.md)。

实现审计同时发现，源 30B 轨迹并未真正收到配置中的 LB 梯度：re-entrant activation checkpointing 使嵌套辅助张量脱离计算图。A16 的有效结果因此是冻结状态上精确、真正可微的反事实影子一步，不能用来声称原轨迹在有效 LB 下训练。

## 8. Claim Boundary And Next Decision

已支持：DC 会即时维持冻结 Vanilla 坍缩；centering 会消除一个可复现的早期可微 LB 代价；LB 效应强烈依赖训练阶段。已否定：centering 并未跨两个 seed 和所有阶段普遍减少共享路径或专家内部冲突。源训练没有施加有效 LB，因此长期 LB 作用仍未解决。

本 Anchor 不能声称所有辅助损失都有害、动态 expert bias 已经更好、影子一步效应会持续到长训练，或负载更好就会形成有用专家。动态 expert bias 只是在 A16_00 支持有害干扰或 hard/soft 失配后的研究者首选干预。

多阶段审计已经完成。唯一下一决策是：Centered + dynamic expert bias 是否能比
Centered + 真正可微 LB 和 Centered 无额外负载控制更高效地维持可用硬负载。
比较必须匹配 token、初始化、数据顺序、capacity 与计算量，并联合报告 held-out
NLL/FLOP 和硬专家负载。不得把当前一步审计解释为 dynamic bias 已经更优。
