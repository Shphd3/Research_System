# 结果摘要：A15_17_E03 Attention 旁支 SAE 的表征、方差与局部梯度审计

Primary Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Execution receipt: [execution_receipt.md](execution_receipt.md)  
逐类别 Fisher 与 Loss 量级事后补充：[supplement_per_class_fisher_loss_cn.md](supplement_per_class_fisher_loss_cn.md)  
Fisher、随机正交基线与 Loss 可信度审计：[fisher_gradient_reliability_cn.md](fisher_gradient_reliability_cn.md)  
Result status / eligibility: `ELIGIBLE_READ_ONLY_MEASUREMENT_WITH_RECORDED_CPU_SYNTHESIS_REPAIR`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## 1. 目的

把最后一层旁支、3+7 层旁支和全 8 层旁支三个新模型加入原有审计，在共同的 0/0.5/1/3B 检查点上回答两件事：原生语言模型内部的方差与可读结构是否改变，以及旁支重构梯度相对主语言梯度到底有多大、朝哪个方向。

## 2. 假设

如果旁支训练让领域结构更容易形成，新模型应在合成面板 P 与自然 M2D2 面板 N 的原生最后一层表征中出现共同、连续、且去掉首个主导方向后仍保留的变化。最强竞争解释是：视觉差异只来自一个共同大方向、某一个数据集，或重构梯度只是在局部存在但没有形成跨面板的原生表征优势。

## 3. 分析方法

- 在六个模型的共同 0/0.5/1/3B 点，比较最后一层 `norm2` 原生表征的类间方差 B、类内方差 W、`F=B/W`、协方差谱与线性读出；原始坐标和去掉拟合集首方向后的 B3 坐标分开。
- 对三个旁支模型，逐挂载层比较原始 Attention 输出与 SAE 重构的方差分布，P 用最后有效 token，N 用固定 32 个抽样位置的均值。
- 在四组分层 N-fit 批次上，于同一个 Attention 输出节点比较语言损失梯度和该层局部重构梯度，报告 L2 范数、数量级比、余弦与夹角；全节点和 SAE 实际抽样位置分开。

端点边界：执行冻结时 S7 的物理里程碑到 10B，S37/SALL 到 3B，三个源目录都没有 15B 里程碑。因此主比较只使用三者共同且真实存在的 0/0.5/1/3B；没有把 15B 插值、替代或混入非配对比较。

## 4. 结论

**Verdict：测量完整且合格；本轮没有看到三个旁支模型在 P 与 N 上都成立的原生最后层表征优势。梯度确实到达主干，数值角度接近 90°，但经同维随机方向校准后，绝大多数并不比高维随机方向更正交；可信的主要差别是梯度强度。该判断是 AI 草案，等待研究者确认。**

1. **旁支模型没有跨两个数据集一致胜过 Dense 参照。** 在 3B 的 B3 坐标中，P 上 Dense 的 `F=0.297`、读出 `0.961`；S7/S37/SALL 分别是 `F=0.214/0.273/0.222`、读出 `0.900/0.944/0.928`。N 上四者更接近：Dense `F=0.207`，S7/S37/SALL 为 `0.203/0.205/0.205`；读出为 `0.783/0.785/0.795/0.783`。S37 是三个旁支中最接近参照的，但不是两个面板共同的增益。

![去首方向后的类间类内方差轨迹](figures/final_fisher_b3_trajectories.png)

How to read: 横轴是共同训练 token 点，纵轴依次是类间方差 B、类内方差 W 和二者之比 F；同一面板中 F 越高表示类别均值相对类内散布更分开，但不表示语言模型实际使用了这些类别。

2. **全层旁支在合成数据上把方差压得更集中，但这种现象没有复制到 M2D2。** 3B 时，P 上 SALL 的第一方向方差占比为 `0.204`、参与率为 `14.69`，Dense 为 `0.146/17.85`；也就是更多能量挤到少数方向。N 上 SALL 为 `0.104/32.33`，Dense 为 `0.103/31.45`，几乎重合。并且在 P 上，S7/S37/SALL 的原始 F 去掉首方向后只保留 `52.1%/53.6%/55.0%`，说明不少“看起来分开”的结构依赖一个主导方向。

![原生最后层协方差分布轨迹](figures/final_variance_distribution_trajectories.png)

How to read: `top1_share` 越高、`participation_ratio` 越低，表示方差越集中在少数方向；这说明表示更“尖”，不等于语义更好或功能更强。

3. **梯度用白话说：两支箭头的夹角确实约为 90°，但在 26 万维空间中，随机箭头本来就会如此。** 3B 的 SAE 抽样位置上，所有平均夹角都在 `89.91°–90.17°`，余弦接近 0；然而 176 个比较组成的 44 个 checkpoint-layer 组中，43 个与同维随机方向相容，0 个比随机更接近严格正交，唯一偏离的 SALL-1B-L0 反而离 0 更远。3B 的 11 个组全部与随机相容。强度差别仍然成立：最后一层单旁支约为同位置语言梯度的 `0.653` 倍；双层模型的 L3/L7 为 `0.170/0.245` 倍；全层模型每层约 `0.012–0.047` 倍。S37 的 L7 在 0.5B/1B 曾达到 `1.20/1.56` 倍，3B 又降到 `0.245`。

![梯度余弦与同维随机方向](figures/gradient_cosine_vs_dimension_matched_random.png)

How to read: 纵轴是余弦乘以同一比较维度的平方根，灰带是独立同维随机方向的 95% 区间。落在灰带附近表示“与随机近正交相容”，不是学得了特殊正交机制；它也不能推出长期训练“互不影响”。

### Claim Boundary

Can claim: 三种旁支模型在两个冻结面板上的表征方差、读出和局部梯度轨迹已完成；旁支重构梯度在注册节点非零、AuxK 对该节点为结构零；局部余弦接近 0 且强度随挂载数、层和检查点显著变化；现有角度大多与同维随机方向相容。

Cannot claim: 旁支带来语言模型收益；SAE 特征被原生前向使用；全层旁支更优；梯度具有比随机更强的特殊正交性；近 90° 意味着训练中没有干扰；这些相关轨迹单独证明了因果机制、路由或专家专门化。

### Next Step Analysis

Decision: **AI 建议，待研究者确认：[E05 草案](../A15_17_E05_multimodel_fisher_gradient_coefficient_audit/protocol.md) 先做参数空间的“合起来到底多大”审计，并等待 0/0.5/1/3/5/10/15B 的真实共同 checkpoint；不直接开始系数续训。**

Why it follows: 当前结果只量到“每个 SAE 自己在自己节点上的局部推力”。对 SALL 而言，八个局部梯度会在共享的下游/上游参数上叠加，也可能互相抵消；仅看每层 `1/8` 后的小比例，不能知道真实参数更新上的总作用。

Unresolved uncertainty: S37 在 0.5B/1B 的 L7 强度峰值，以及 SALL 八层的小梯度，在 Attention/MLP/Norm 参数组上相加后，是仍然小、稳定正交，还是出现可观的对齐、冲突或抵消。

Completion criterion: 在同一四组 N-fit 批次、0.5/1/3B 三点上，计算 LM、全部重构项合计、逐层 leave-one-out 的参数组范数与夹角，并验证总和等于逐层向量和。

Stop or redirect condition: 若跨批次与检查点的总重构/LM 比值仍低一个数量级且无稳定同向或反向结构，停止把旁支梯度当作主要机制；只有出现稳定、可重复的参数级作用，才设计同起点的 LM-only 对照与短程配对续训。

Resume action: 研究者确认这一最小参数审计的阈值与预算后，再写独立 Protocol；本 Summary 不授权新的 GPU 运行。
