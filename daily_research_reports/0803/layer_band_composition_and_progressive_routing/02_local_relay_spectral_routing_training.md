# 实验二：Local / Relay 显式频带 Router 的 2B 与 10B 训练

状态：最终版；2B 三臂续训和 10B 五臂从头训练均已完成。

## 摘要

本实验问：既然线性 Gate 容易先学高方差方向，显式限制不同层 Router 读取 head、middle、tail，能否改善专家选择和未见文本预测？

我们比较了两种架构：

- **Local-HMT：**第 2/3/4 层 Gate 分别读取各自本层表征的 head/middle/tail。
- **Relay-HMT：**第 2/3/4 层 Gate 统一从第一层表征读取 head/middle/tail。

专家网络始终接收完整的本层表征；只改变 Gate 用什么信息选专家。

阶段结果经历了重要更新：

1. 2B 续训中，Relay-HMT 终点比 native 略好，但全程适应代价大；Local-HMT 减少同专家负梯度配对，却使终点 NLL 变差。
2. 更严格的 10B 从头训练中，Relay-HMT 在两个 seed 都明确劣于 Local-HMT 和 Centered-Full，也没有稳定超过同维 Relay-Random。
3. Local-HMT 在两个 seed 都取得最低终点 NLL 点估计，但只在一个 seed 明确优于 Centered-Full；又缺少 Local-Random，因此尚不能把弱优势归因于 covariance 频带身份。
4. 在线频谱更新器能平滑追踪变化的子空间并避免高置信 token 突然换专家，但工程连续性没有转化为 Relay 的质量收益。

最终认识是：

> 显式频带约束可以改变路由与局部专家梯度，但固定浅层 Relay 不是有效方法；本层动态频带是一个尚待同维随机对照复核的弱候选，而不是已经获证实的 Router 原则。

## 1. 为什么要做训练实验

冻结大模型的静态画像只能说明“某个语义差异在表征中可见”，不能回答：

- Gate 是否真的会利用它；
- 被送入同一专家的 token 是否提出相容更新；
- 专家是否形成不同功能；
- 相同计算量下的 held-out NLL 是否下降。

因此训练实验把 covariance 频带从测量坐标变成干预变量。它检验两个竞争解释：

1. **Local 假设：**各层形成自己的功能表示，应读取本层频带。
2. **Relay 假设：**本层谱坐标持续漂移会增加搜索难度，固定浅层来源可能给后层一个稳定坐标。

静态实验没有推出 H→M→T 是正确语义顺序；这个日程是需要训练结果裁定的假设。

## 2. 两种架构具体怎样使用频带

![Local 与 Relay 架构](/data/250010109/Research_System/daily_research_reports/0803/layer_band_composition_and_progressive_routing/figures/02_local_relay_architecture.svg)

四层网络记为 L1--L4。H/M/T 分别是按 covariance 特征值从大到小排序后的 64/256/448 维子空间。

### 2.1 Local-HMT

L1 使用完整 centered input；L2/L3/L4 的 Gate 分别读取：

$$
\text{L2: local }H_{64},
\qquad
\text{L3: local }M_{256},
\qquad
\text{L4: local }T_{448}.
$$

Local 问的是：每一层自己的频谱排名能否给该层 Router 一个有用的低维归纳偏置。

### 2.2 Relay-HMT

L1 仍使用完整 centered input；L2/L3/L4 的 Gate 都从同一个 L1 输出读取：

$$
\text{L2: layer-1 }H_{64},
\qquad
\text{L3: layer-1 }M_{256},
\qquad
\text{L4: layer-1 }T_{448}.
$$

Relay 问的是：一个稳定浅层坐标是否比随层变化的本地坐标更容易训练。

### 2.3 没有改变什么

- 每层专家仍接收完整本层表征；
- 每个 token 仍只激活一个稀疏专家；
- 活跃参数、数据、token 数、容量和主训练计算匹配；
- 频带只改变 Gate 的观察视角，不截断专家的功能输入。

因此，若结果变化，应解释为路由选择路径变化，而不是专家少看了信息。

## 3. 先解释评价指标

### 3.1 Held-out NLL

Held-out NLL 是模型对未见文本正确下一个 token 的平均意外程度，单位为 nat/token，越低越好。它是模型质量的主判据。

比较两个模型时定义：

$$
\Delta\mathrm{NLL}(A-B)=\mathrm{NLL}_A-\mathrm{NLL}_B.
$$

负值表示 A 更好，正值表示 A 更差。

### 3.2 同专家梯度冲突

把被路由到同一专家的独立 token 组分别求专家参数梯度 $g_A,g_B$：

$$
\operatorname{cos}(g_A,g_B)
=
\frac{\langle g_A,g_B\rangle}
{\|g_A\|\|g_B\|}.
$$

余弦小于 0 表示两组 token 希望专家朝相反方向更新。负梯度对比例越低，说明局部更新冲突更少；但它不能替代 NLL，因为冲突少也可能只是训练任务变简单或专家功能变得相似。

### 3.3 专家选择遗憾

对同一 token 强制遍历所有专家，找出当前最低 loss 的专家；实际 Router 所选专家相对这个局部最优专家多付出的 NLL 称为 route regret，越低表示当前选择更接近反事实最优。它仍是局部冻结诊断，不保证长期训练更好。

### 3.4 专家输出冗余

同一输入经过不同专家后的输出余弦越高，表示专家功能越相似。冗余较低可支持功能分化，但不能证明分化方向正确。

## 4. 2B 三臂配对续训

### 4.1 设置

| 项目 | 设置 |
| --- | --- |
| 模型 | 4 blocks，hidden 768，8 个稀疏专家 + 1 shared expert，top-1 |
| 专家宽度 | 1536 |
| 分叉点 | step 800，约 0.629B tokens |
| 终点 | step 2544，约 2.001B tokens |
| 三臂 | Native-Full、Local-HMT、Layer1-Relay-HMT |
| 复现 | continuation seeds 17、29；同 seed 三臂数据/RNG 配对 |
| 数据 | DCLM，sequence 1024，global batch 768 |
| 优化器 | AdamW，LR $10^{-4}$，betas (0.9,0.95)，weight decay 0.01 |
| 负载约束 | running center，load-balancing coefficient 0.01 |
| 硬件 | 每条轨迹一个 8×RTX5090 节点 |
| 频谱 | 分叉点拟合并冻结，不在线更新 |

### 4.2 2B 质量结果

![2B 终点配对 NLL](/data/250010109/Research_System/daily_research_reports/0803/layer_band_composition_and_progressive_routing/figures/03_terminal_nll_comparison.png)

| 比较 | 2B 配对 $\Delta$NLL，95% CI | 直接结果 |
| --- | ---: | --- |
| Local − Native | +0.002174 [0.001758, 0.002590] | Local 终点更差 |
| Relay − Native | −0.001756 [−0.002352, −0.001119] | Relay 终点略好 |
| Relay − Local | −0.003930 [−0.004504, −0.003343] | Relay 终点优于 Local |

但是，两个频带 arm 在分叉时都付出明显结构适应代价；从 0.629B 到 2B 的平均 held-out 损失曲线仍比 native 更高。Relay 是晚期恢复后略微反超，不是训练效率提高。

### 4.3 2B 梯度与专家功能

![2B 专家功能机制](/data/250010109/Research_System/daily_research_reports/0803/layer_band_composition_and_progressive_routing/figures/04_expert_function_mechanisms.png)

| 指标 | Native | Local | Relay | 越好方向 |
| --- | ---: | ---: | ---: | --- |
| route regret | 0.42485 | 0.42304 | 0.41726 | 低 |
| 负梯度对比例 | 0.5000 | **0.4635** | 0.4844 | 低 |
| 专家输出冗余 | 0.04844 | 0.04808 | 0.05130 | 低 |

Local 最稳定的正信号是负梯度配对减少，但它的 NLL 更差；这直接说明“局部冲突更少”不是质量改善的充分条件。Relay 的 route regret 更低，但输出冗余更高、其他冲突指标不一致，因此也没有形成一致的专家专业化证据链。

2B typed verdict 为 `specialization_only_without_quality_pass`。

## 5. 为什么还需要 10B 五臂从头训练

2B 仍有三个强 rival：

1. 频带从 0.629B 起冻结，会随表征变化而变陈旧；
2. Relay 的终点优势可能来自任意稳定低维瓶颈，而不是 covariance rank；
3. 去均值本身可能比频带身份更重要。

10B 实验因此从初始化训练五个 arm，并在线平滑更新频谱：

| Arm | Gate 读取什么 | 分离的因素 |
| --- | --- | --- |
| Vanilla-Full | 未去均值的完整本层输入 | 标准参考 |
| Centered-Full | 去 running mean 的完整本层输入 | 去均值本身 |
| Local-HMT | 在线更新的本层 H/M/T | 动态本层频带 |
| Relay-HMT | 在线更新的第一层 H/M/T | 固定浅层来源 |
| Relay-Random | 第一层同维随机嵌套子空间 | covariance 身份对照 |

模型仍为四层 H768、8 个稀疏专家 + 1 shared expert、top-1。每个 arm 使用 seeds 17、29，共 10 条独立 8×5090 轨迹；每条训练 12,716 steps，即 10.00027B nominal tokens。所有任务完整结束，零平台重试。

## 6. 10B 决定性结果

### 6.1 终点 NLL

| Arm | Seed 17 | Seed 29 | 两 seed 排名 |
| --- | ---: | ---: | --- |
| Local-HMT | **3.59874** | **3.60203** | 1 / 1 |
| Centered-Full | 3.60384 | 3.60259 | 2 / 2 |
| Relay-HMT | 3.61309 | 3.60892 | 3 / 4 |
| Relay-Random | 3.61576 | 3.60866 | 4 / 3 |
| Vanilla-Full | 3.71639 | 3.73053 | 5 / 5 |

![10B 五臂 NLL 轨迹](/data/250010109/Research_System/daily_research_reports/0803/layer_band_composition_and_progressive_routing/figures/09_10b_five_arm_nll_trajectory.png)

横轴是累计训练 tokens，纵轴是 held-out NLL，越低越好。Local-HMT 约从 2B 后成为最低点估计；Relay-HMT 没有在更长训练中追上 Local-HMT。

### 6.2 配对裁定

![10B 终点配对差](/data/250010109/Research_System/daily_research_reports/0803/layer_band_composition_and_progressive_routing/figures/10_10b_endpoint_paired_delta_nll.png)

| 比较 | Seed 17，95% CI | Seed 29，95% CI | 裁定 |
| --- | ---: | ---: | --- |
| Centered − Vanilla | −0.11254 [−0.11445, −0.11074] | −0.12795 [−0.13003, −0.12596] | 去均值 Pass |
| Local − Centered | −0.00510 [−0.00654, −0.00371] | −0.00056 [−0.00211, +0.00098] | 未跨 seed 通过 |
| Relay-HMT − Local | +0.01436 [+0.01280, +0.01590] | +0.00689 [+0.00535, +0.00846] | Relay Fail |
| Relay-HMT − Centered | +0.00925 [+0.00769, +0.01080] | +0.00633 [+0.00476, +0.00791] | Relay Fail |
| Relay-HMT − Relay-Random | −0.00266 [−0.00420, −0.00115] | +0.00026 [−0.00123, +0.00175] | covariance 身份 Fail |

最明确的收益来自去均值。Local-HMT 是两 seed 的最低点估计，但只在 seed 17 明确优于 Centered-Full；不能写成稳定胜出。Relay-HMT 在两个 seed 都明确劣于 Local 和 Centered，并且没有稳定超过随机 Relay。

### 6.3 在线更新器通过，但方法没有通过

在线更新器在固定统计语料上追踪当前 covariance 子空间，用平滑 Grassmann 更新限制刷新幅度。

![在线追踪与连续性](/data/250010109/Research_System/daily_research_reports/0803/layer_band_composition_and_progressive_routing/figures/11_10b_online_tracking_continuity.png)

- HMT 部署子空间明显比“从不更新”更接近当前目标；
- 192 次注册刷新中，高置信 token 的最大实际换专家率为 0；
- 直接硬切换到当前目标则会使 Local/Relay-HMT 约 25%--38% 的高置信 token 换专家；
- 刷新前后的训练 loss 没有一致跳变。

所以“如何平滑更新频带”这个工程问题已经解决；“应该更新到什么功能坐标”仍未解决。

### 6.4 10B 梯度与专家机制

| Arm | route regret s17/s29 | 负梯度对比例 s17/s29 | 输出冗余 s17/s29 |
| --- | ---: | ---: | ---: |
| Centered-Full | 0.363 / 0.380 | 0.495 / 0.457 | 0.043 / 0.047 |
| Local-HMT | 0.371 / 0.375 | **0.454 / 0.449** | **0.042 / 0.045** |
| Relay-HMT | 0.394 / 0.389 | 0.497 / 0.486 | 0.049 / 0.051 |
| Relay-Random | 0.425 / 0.408 | 0.504 / 0.512 | 0.048 / 0.049 |

Local-HMT 的负梯度对比例和输出冗余点估计较低，与其较好的 NLL 排序相容；但它的 route regret 没有稳定优于 Centered-Full。Relay 的遗憾更高、输出更冗余，与其没有 NLL 收益相容。

这些局部指标用于解释结果，不能替代两 seed 的配对 NLL。

## 7. 两轮训练联合改变了什么认识

1. **2B Relay 的晚期正结果没有在更严格的 10B 从头训练中复现。** 固定第一层频带不是一个稳定的有益路由原则。
2. **去均值比频带身份更可靠。** Centered-Full 相对 Vanilla 在两个 seed 都大幅改善，并避免后层专家负载坍缩。
3. **Local-HMT 是弱候选，不是已证实方法。** 两 seed 的终点点估计都最低，但只有一个 seed 的配对区间明确，且缺少 Local-Random。
4. **局部梯度冲突减少不保证质量。** 2B Local 更少冲突却更差；10B Local 的机制与质量方向较一致，但因果链仍未闭合。
5. **平滑子空间跟踪不等于功能路由。** 更新器连续性 Pass，Relay 质量仍 Fail。
6. **静态语义频谱画像不能直接推出训练架构。** 语义差异广泛跨谱、同名 band 跨层含义不固定，固定 H→M→T 日程缺少功能依据。

## 8. Claim Boundary

### 已建立

- 显式频带约束会真实改变路由和局部专家梯度关系。
- 在当前四层 H768 DCLM MoE、两个 seed、10B 预算下，Relay-HMT 不优于 Local、Centered 或随机 Relay 的注册组合。
- 去均值是唯一跨两个 seed 都明确产生大幅 NLL 收益的改动。
- 在线 covariance 子空间可在不翻转高置信路由的情况下平滑更新。

### 不能声称

- 不能说 H/M/T 对应普遍的粗/中/细语义层级。
- 不能说 Local-HMT 已经稳定提高模型质量。
- 不能把 Local 的点估计优势归因于 covariance rank；缺少 Local-Random。
- 不能说 Relay 的失败证明浅层信息永远不能指导深层；这里只否定当前第一层 H/M/T 设计。
- 不能用负载均衡、margin、梯度冲突或 route regret 单独替代 held-out NLL。
- 不能外推到更大模型、更多层、更多专家或其他语料。

### Typed verdict

- 2B：`specialization_only_without_quality_pass`。
- 10B：`does_not_support_relay_hmt`；Local-HMT `not yet supported`；online continuity `pass`。

### 唯一下一决策

增加一个与 Local-HMT 在维度、目标运动量、更新器和追踪精度上匹配的 Local-Random，与 Local-HMT、Centered-Full 做两 seed 配对复核。只有 Local-HMT 在两个 seed 都明确优于这两个对照，才把本层 covariance 频带升级为功能路由候选。

## 9. 证据入口

- [2B 中文摘要](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_01_shallow_head_guided_deep_routing/A15_01_04_E01_progressive_band_source_routing_2b/summary_cn.md)
- [2B 完整证据](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_01_shallow_head_guided_deep_routing/A15_01_04_E01_progressive_band_source_routing_2b/detailed.md)
- [10B 自包含完整报告](/data/250010109/Research_System/daily_research_reports/0803/online_spectral_router_10b_training_report/report.md)
- [10B 中文摘要](/data/250010109/Research_System/Projects/online-spectral-router-training/main/experiments/A15/A15_00_E01_10b_five_arm_training/summary_cn.md)
- [10B 终点表](tables/09_10b_endpoint_nll.csv)
- [10B 配对差表](tables/10_10b_endpoint_pairwise_nll.csv)
- [10B 在线刷新表](tables/11_10b_online_refresh_summary.csv)
