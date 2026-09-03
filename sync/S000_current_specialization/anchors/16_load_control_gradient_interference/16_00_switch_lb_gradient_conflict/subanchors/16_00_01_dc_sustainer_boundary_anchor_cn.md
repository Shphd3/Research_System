# A16_00_01 DC 维持因素边界


## 1. Problem Definition

本子 Anchor 现归入 A16_00 的负载控制机制线，只裁定一个已经完成的局部不确定性：实际 Router 输入在 token 之间共享的均值，是否直接维持 Vanilla-Full 深层硬路由坍缩，并使同一个 Switch 风格负载均衡目标更难改变赢家。它原由 A15 频谱训练暴露，迁移只改变证据所有权，不改变实验、数值或裁定。

唯一决策问题是：**冻结 token、Gate 权重、专家和检查点后，去掉真实公共均值能否恢复 Vanilla 路由；把已保存公共中心加回 Centered 后能否重新造成集中；而且二者都超过同幅随机平移与错误层平移？** 本实验是当前路由的根因审计，不回答语言模型质量或训练干预收益。

## 2. Physical Priors

对线性 Gate，token 共享的输入分量会变成 token 共享、但专家之间不同的固定 logit 偏置，它可以让同一专家在大量 token 上获得一致的赢家 margin。若真实均值去除不比匹配对照更有效，或 Centered 加回中心后没有响应，该先验就不能作为冻结状态的主要解释。

## 3. Falsifiable Hypotheses

- **H1，DC 必要性：** 冻结 Vanilla 减去独立估计的层均值后，最忙专家占比下降、路由熵上升，并且效应超过随机与错误层平移。
- **H2，DC 充分性：** 冻结 Centered 加回检查点 running center 后，最忙专家占比上升、路由熵下降，并且效应超过匹配对照。
- **H3，LB 饱和机制：** 坍缩的原生 Vanilla 同时具有较高 Switch 辅助损失和较低的逐 token logit 梯度杠杆；去中心反事实恢复该杠杆。
- **最强竞争解释：** 已学习的 Gate 几何或 Router--Expert 反馈本身足以造成坍缩，公共分量只相关而非主因。

H1 与 H2 同时成立才是 Pass；只有 H1 为 `necessary_only`，只有 H2 为 `sufficient_only`，二者都不成立为 Fail。原生重放、数据身份或检查点证据失效则为 Insufficient。H3 只能解释，不能挽救 H1/H2 的失败。

## 4. Mathematical Model

把实际去中心前 Router 来源写成 $h=\mu+\delta$，其中 $\mu$ 是固定统计 token 上的公共均值，$\delta$ 是 token 间变化。Gate 为 $W$，用 $C_E=I-\mathbf 1\mathbf 1^\top/E$ 去掉不会改变专家比较的共同 logit 方向，则

$$
C_EWh=C_EW\mu+C_EW\delta.
$$

$C_EW\mu$ 是与路由决策有关的 DC 偏置。Switch 负载损失为 $L_{LB}=E\sum_e f_e\bar p_e$，$f_e$ 是硬 top-1 token 占比，$\bar p_e$ 是平均软概率。把 $f$ 视为不反传，样本数归一后的导数是

$$
N\frac{\partial L_{LB}}{\partial z_{t,j}}
=E p_{t,j}\left(f_j-\sum_e f_ep_{t,e}\right).
$$

当概率已经饱和时，导数可以趋近零，即使 $L_{LB}$ 仍很大。它只描述瞬时 Gate 压力，不能代表叠加语言模型梯度与 AdamW 状态后的总参数更新。

## 5. Computational Realization

在 seed-17 的 Vanilla-Full 与 Centered-Full 固定检查点上，用冻结统计文本和验证文本捕获每层去中心前的真实 `gating_reference`。每个模型、检查点、层都只用独立 statistics split 拟合一个均值；先精确重放原生 logits，再离线只改变常数输入分量：

- Vanilla：原生 raw 输入与减去独立均值；
- Centered：原生 centered 输入与加回检查点 running center；
- 对照：循环错误层平移，以及在专家相对 logit 范数上匹配的确定性随机平移。

反事实不执行专家，只测 Router 决策。早期与晚期检查点用于定位关系何时出现，不能把层或检查点当作独立重复实验。

## 6. Minimal Falsification Tests

主指标是最忙专家占比，即验证 token 中被分给使用量最大专家的比例。Vanilla 的正向“恢复量”等于原生占比减去去均值占比；Centered 的正向“破坏量”等于加回中心占比减去原生占比。注册摘要对 layer 3/4 在 50M、100M、250M、500M、1B、10B、20B 的固定单元等权平均；文档是 bootstrap 独立单位，层与检查点只是固定重复视图。

每个方向都要求文档配对 95% 下界大于零，且大于 256 个匹配随机平移的聚合效应 q95。原生 logit/winner 重放、token hash、检查点身份与确定性对照是硬守卫。归一化路由熵、margin、DC 对齐、$L_{LB}$ 与解析 LB logit 梯度杠杆只用于解释，不能替代主裁定。

## 7. Current Evidence

已核验的训练证据表明六个 arm 都使用相同的 $0.01$ LB 系数。20B 时，Vanilla 四层最忙专家占比分别为 49.4%、66.0%、99.9%、99.8%，Centered 为 21.3%、29.3%、27.0%、23.9%；Vanilla 第 3/4 层在约 50M token 已接近 99%。

A16_00_01_E01 已完成全部 16 个注册冻结单元，裁定为 `necessary_only`。在第 3/4 层和七个非零保存点上，Vanilla 去独立真实均值使最忙专家占比平均下降 0.68678，文档 bootstrap 95% 区间为 [0.68435, 0.68922]，远高于匹配随机 q95 0.18326；72.63% 路由发生翻转，且 DC 在 99.75% token 上支持原生赢家相对第二名。反向地，给独立训练的 Centered 加回保存中心只产生 0.14225 [0.14010, 0.14446] 的变化，低于随机 q95 0.22588，平均也低于错误层平移。公共项因此即时维持当前 Vanilla 坍缩，但在 Centered 已适配的 Gate 几何中不构成方向特异的充分原因。

LB 机制不是统一的“坍缩后无梯度”。Vanilla 坍缩后 LB 数值长期接近上限，第 4 层在部分饱和保存点的局部 logit 杠杆很小，但第 3 层并未普遍消失。因此惩罚数值大小不能直接代表纠正能力。

Protocol：[A16_00_01_E01](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/protocol_cn.md)

结果：[Summary](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary_cn.md)

## 8. Claim Boundary And Next Decision

本审计已经建立当前 Vanilla 坍缩对真实公共分量的方向特异即时依赖；它不能证明累计历史中的唯一因果、离线干预的语言模型收益或最佳 LB 修复。反向干预失败说明单纯静态偏置解释不够，已学习路径适配仍是最强剩余解释。

唯一下一决策由父 Anchor A16_00 接管：使用已经批准的 Vanilla/Centered 配对
梯度—影子更新结果，选择 dynamic expert bias、保留可微 LB，或修复 hard/soft
控制失配。恢复入口为 A16_00 父 Anchor，执行前先冻结其 Protocol。
