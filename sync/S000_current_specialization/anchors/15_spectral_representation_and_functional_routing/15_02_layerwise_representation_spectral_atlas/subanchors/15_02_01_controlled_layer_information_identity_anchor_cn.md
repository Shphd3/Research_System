---
anchor_id: 15_02_01_controlled_layer_information_identity
status: completed_pass
canonical_language: en
companion_language: zh
thinking_card: 15_02_01_controlled_layer_information_identity_thinking_card_cn.md
parent_anchor: 15_02_layerwise_representation_spectral_atlas
updated: 2026-07-31
---

# A15_02_01 不同层的频带分别编码什么？

## 1. Problem Definition

唯一问题是：在一个已通过未见组合能力门的四层 MoE 中，同一相对 covariance 频带在不同层是否承载不同的功能变量？功能变量固定为粗条件 $a$、一步中间状态 $m=x+a$ 与两步组合结果 $y=x+a+b$（均在有限域上计算）。

主判据不是某个标签的裸准确率，而是该层该频带相对同维随机子空间的低样本线性可读性增量，以及组合模型相对一步控制模型的差分。

## 2. Physical Priors

1. 非平谱会影响 Gate 学习速度，但不指定每个方向的功能含义。
2. 逐层计算可能使中间变量和组合变量在深度上重新组织。
3. 若信息在高维状态中高度冗余，任意随机子空间都可读；这不能支持频带特异性。

## 3. Falsifiable Hypotheses

**H1：**组合训练在特定深度和频带中形成超过同维随机方向的一步状态或组合结果可读性，并且该模式在两个种子中复现。

**最强 rival：**深度趋势来自接近输出、一般训练进展或随机投影保留，而非层别频带身份。

**证伪：**模型能力有效，但所有真实频带均不超过随机方向；或频带—信息对应在两个种子间不复现；或组合增量已同样存在于一步控制模型和初始化。

## 4. Mathematical Model

数据使用有限域 $\mathbb Z_{17}$：

$$
m=(x+a)\bmod17,\qquad y=(m+b)\bmod17.
$$

对第 $\ell$ 层实际 Gate 输入 $g_\ell$ 拟合 covariance 基底 $U_\ell$。宽度 256 切为八个 32 维细带，并聚合为 head=`F1`、middle=`F2--F4`、tail=`F5--F8`。

对信息变量 $q$，以四个低样本规模的 held-out probe accuracy 平均值定义 $A_{\ell,B,q}$。方向特异性为

$$
S_{\ell,B,q}=A_{\ell,B,q}-Q_{0.95}(A_{\ell,R_{d_B},q}),
$$

其中 $R_{d_B}$ 是同维 Haar 随机子空间。组合目标相对一步控制的差分为

$$
\Gamma_{\ell,B,q}=S^{\rm compose}_{\ell,B,q}-S^{\rm one\text{-}step}_{\ell,B,q}.
$$

## 5. Computational Realization

两个模型条件共享四层 causal Transformer-MoE：width 256、8 heads、每层 8 个 top-1 experts、expert width 512；无负载均衡辅助损失，所有条件使用相同的非梯度 load-free score bias。两个条件仅改变 final-query 的目标：一步控制仍预测 $m$；组合模型预测 $y$。每个条件训练 seeds 17 与 29。

训练、验证、covariance calibration、probe fit/validation 与封存测试使用互斥 context ids。所有原子 shift/value 在训练出现；final-query 的八个 $(a,b)$ 组合形成完美匹配并只在验证/测试出现。

## 6. Minimal Falsification Tests

1. 数据生成器必须通过无泄漏、原子覆盖、均衡边际、oracle 与捷径基线审计。
2. 两个模型、两个种子均需通过一步能力门；组合模型还必须通过未见两步组合门。
3. 每层真实 Gate 输入必须可精确重放，covariance half-split 必须稳定。
4. H/M/T 与八个细带均同同维随机方向、完整表征、初始化进行比较。
5. 只有两个种子方向一致且封存测试区间支持时，才声明层别频带身份。

## 7. Current Evidence

A15_02_01_E01 已完成并按注册规则判为 Pass。一步控制与两步组合各训练 seeds 17、29；四个模型均通过未见组合、第二层中间状态、负载、专家使用和实际 Gate 输入护栏。组合模型未见 $(a,b)$ 对的 sealed-test accuracy 为 1.000/0.985。

完整表征中，组合结果 $y$ 的低样本可读性从 L1 的 0.113 上升到 L4 的 0.784，而一步控制保持在 0.103--0.156。频带身份并非对应“组合结果下沉到 tail”：没有任何 $y$ 的 H/M/T 或细带 cell 在两个种子中超过同维随机方向。真正复现的是 L3/L4 的 F1/head 特异携带中间状态 $m$，以及 F2 特异保留粗条件 $a$；其平均组合相对控制增量分别为 0.031/0.103 和 0.370/0.577。

Gate 去带审计又表明，原生 Gate 仍主要使用 F1/head；移除 F2/M/T 几乎不改变路由或答案 NLL。因此本实验同时建立了“层别频带含义会重组”和“编码位置不等于 Router 使用位置”。完整记录见 [summary_cn.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_01_E01_controlled_layer_information_profile/summary_cn.md)。

## 8. Claim Boundary And Next Decision

本实验建立的是受控四层任务中的层别频带信息重组。它不能证明自然语言中的语义层级、不能证明某频带应直接路由、也不能证明训练效率收益。第二层中间状态使用了显式训练监督，因此也不能声称该层级过程完全自发涌现。

**唯一下一决策：**把复现的层别功能坐标蒸馏为无需在线 PCA 的固定低秩读出，并送入独立的一步共同训练兼容性门；只有超过 native score、同维随机、token-shuffled 和错误层对照，才允许跨层指导的匹配训练。
