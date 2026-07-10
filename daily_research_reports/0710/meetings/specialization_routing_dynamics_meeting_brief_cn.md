# Feature Specialization：从可初始化分区到路由训练动力学

## 0. 执行摘要

**研究问题：** 对只执行最高分专家的稀疏混合专家模型，理想的特征分区已经可以在初始化时构造；当前需要解释的是，训练中的任务信号如何增厚正确路由的得分间隔、错误路由如何被纠正，以及背景梯度如何耗尽这一间隔。

**机制解释：**

1. 路由得分间隔表示特征 $f$ 离开正确专家 $a$、改投竞争专家 $b$ 还需要跨过多远的决策边界。

$$
m_{f,a,b}=(w_a-w_b)^\top\mu_f.
$$

2. 当所有专家都按概率参与输出时，正确专家相对竞争专家的功能优势决定一步间隔是增大还是减小。

$$
\Delta m_{f,a,b}
=\frac{\eta}{\tau}
\mathbb E\!\left[(p_aA_a-p_bA_b)h^\top\mu_f\mid f\right].
$$

3. 当只执行最高分专家 $r$ 时，未选专家的更新依赖当前路由概率，却不包含各自的专家输出；因此它们没有被逐个比较功能好坏。

$$
\Delta w_j
=\frac{\eta}{\tau}p_r\bigl(\mathbf 1[j=r]-p_j\bigr)B_rh.
$$

4. 长期保持取决于初始间隔、任务信号、背景压力和越界后的纠错能否形成正的累计预算。

$$
m(T)=m(0)+C_{\mathrm{signal}}(T)+C_{\mathrm{background}}(T).
$$

**主要结果：**

1. 在冻结表征的软路由模型中，局部间隔压力由专家功能决定，而不是由初始化时给专家贴上的几何标签决定。
2. 只执行一个专家的稀疏路由并非完全不能纠错，但它按当前得分排名逐个搜索；有用专家位于第 4 名时，纠错显著慢于让全部专家参与比较的软路由。
3. 背景位置多本身不会破坏路由；只有背景梯度在路由边界上形成持续同向的平均投影时，才会稳定消耗间隔，并产生彼此不同的“首次越界阈值”和“最终恢复阈值”。

**证据说明：**

1. 功能匹配时，全部特征与随机种子的一步正确间隔都增大；专家输出完全相同时更新为零；交换专家功能后，原几何绑定的间隔转为负，而功能匹配的新绑定转为正。
2. 有用专家初始位于第 4 名时，软路由平均 30 步纠正；只执行最高分专家的路由平均 153 步纠正，并经历 142 次专家切换。全部条件最终都在 200 步内纠正，因此“永久锁死”被否定。
3. 在长度 32 的序列中，即使只有 2 个特征信号位置，零均值正交背景和目标均衡的公共背景都没有越界；目标偏置的公共背景在 8 个及更少信号位置时造成三个非公共特征越界。8 个信号位置最终恢复，4 个及以下不能完整恢复。

**结论边界：** 当前结论只覆盖冻结表征、固定专家和受控合成数据；尚不能说明可训练的注意力表征网络（Transformer）、具有历史梯度缩放的自适应优化器（AdamW）或真实文本中的越界与恢复由同一机制主导，也没有证明新的路由方法有效。

**执行动作：** 在一层 Transformer、只执行最高分专家的混合专家层和全序列语言建模损失上，分别冻结表征或路由器，并比较普通随机梯度下降（SGD）与 AdamW；完成判据是确定哪一种可训练路径对首次越界与随后重新进入正确区域是必要的。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| 特征级专家专业化（Feature Specialization） | 同类输入稳定进入对它功能上更有利的专家 | 同时要求正确路由身份、正间隔和专家功能匹配 | 复合研究对象 | 是整条研究线的目标 | 不能由单一聚类指标证明 |
| 特征 $f$ | 可重复出现并决定受控任务目标的输入模式 | 合成数据中的四个均匀类别之一 | 离散类别 | 提供可控的路由对象 | 不等同于自然语言语义概念 |
| 专家 $e$ | 混合专家层中的一个子网络 | 固定或可训练的专家函数 $E_e(h)$ | 函数 | 专家功能差异产生任务反馈 | 专家编号本身没有语义 |
| 路由器 | 决定隐藏状态进入哪个专家的门控模块 | 线性得分 $s_e(h)=w_e^\top h$ | 路由分数 | 决定专家选择与边界 | 高分不表示专家有用 |
| 特征中心 $\mu_f$ | 同一特征隐藏状态的平均方向 | $\mu_f=\mathbb E[h\mid f]$ | 隐藏向量 | 定义受控路由几何 | 不代表真实文本中存在单一线性中心 |
| 匹配专家 $a(f)$ | 预先指定为应处理特征 $f$ 的专家 | 受控实验中的一一映射 | 专家编号 | 让“保持原身份”可检验 | 不能证明无标签发现 |
| 路由得分间隔 | 匹配专家相对最强竞争专家的领先量 | $m_f=\min_{b\ne a(f)}(w_{a(f)}-w_b)^\top\mu_f$ | 路由分数差 | 正负直接决定中心位于哪侧边界 | 正间隔不证明专家功能价值 |
| 软路由 | 所有专家按概率参与当前输出 | $\hat y=\sum_ep_eE_e(h)$ | 模型条件 | 可直接比较各专家功能 | 不等同于稀疏部署 |
| 只执行最高分专家的加权路由 | 只执行概率最高的专家，并保留其门控权重 | $r=\arg\max_ep_e,\ \hat y=p_rE_r(h)$ | 模型条件 | 对应当前稀疏动力学问题 | 不代表同时执行多个专家的其他实现 |
| 专家优势 $A_e$ | 略微增加专家 $e$ 权重对降低当前损失的局部收益 | $A_e=-\langle\nabla_{\hat y}\ell,E_e(h)-\hat y\rangle$ | 一阶损失变化系数 | 把专家功能连接到路由更新 | 不代表长期因果效用 |
| 路由行间隔缩放 $q$ | 在不改变专家行平均值的前提下，统一缩放路由行之间的差 | $w'_e(q)=\bar w+q(w_e-\bar w)$ | 无量纲比例 | 只改变初始间隔厚度 | 数值阈值不能迁移到其他模型 |
| 纠正步数 $T_{\mathrm{corr}}$ | 有用专家第一次成为最高分专家所需的步数 | $\min\{t:r_t=a(f)\}$ | 优化步 | 衡量错误分配的修正速度 | 不保证修正后永久稳定 |
| 首次越界 | 正确间隔第一次变为非正 | $T_{\mathrm{cross}}=\min\{t:m_f(t)\le0\}$ | 优化步 | 检测路由身份首次失守 | 不等同于最终失败 |
| 重新进入 | 越界后间隔重新变正 | 存在 $t>T_{\mathrm{cross}}$ 使 $m_f(t)>0$ | 轨迹事件 | 区分暂时脆弱与不可恢复 | 不证明真实训练也会恢复 |
| 边界投影背景偏置 | 背景梯度沿某个专家边界持续同向推动 | $\mathbb E[\Delta m^{\mathrm{background}}]<0$ | 每步间隔变化 | 是受控实验中的累计损害源 | 不等同于“所有公共成分都有害” |
| 最终低尾间隔 | 最容易失败的一小部分特征与随机种子的最终间隔 | 所有特征-种子单元最小匹配间隔的第 5 百分位 | 路由分数差 | 防止平均值掩盖少数特征失败 | 不证明专家效用 |
| 曾越界比例 | 训练中至少一次越界的特征-种子单元比例 | $R_{\mathrm{cross}}=N^{-1}\sum_i\mathbf1[\exists t:m_i(t)\le0]$ | $[0,1]$ | 衡量轨迹脆弱性 | 不等同于最终错误率 |
| 特征-种子单元 | 一个特征在一个随机初始化种子下形成的独立统计单元 | 四个特征分别在每个种子下计数 | 计数单位 | 防止只看跨特征平均值 | 随机旋转不等于独立真实数据重复 |
| 表征漂移 | 训练使同一特征的隐藏状态中心移动 | $\Delta\mu_f=\mu_f(t+1)-\mu_f(t)$ | 隐藏向量变化 | 可能在路由行不变时改变间隔 | 当前冻结实验未覆盖 |
| 注意力表征网络（Transformer） | 根据序列上下文生成路由输入隐藏状态的网络 | 下一步使用一层因果注意力表征层 | 模型组件 | 使特征中心能够随训练移动 | 当前冻结实验未覆盖其动力学 |
| 普通随机梯度下降（SGD） | 用当前梯度和统一步长直接更新参数 | $\Delta\theta=-\eta g_t$ | 参数更新 | 给出不含历史缩放的基线 | 不代表自适应优化器 |
| 自适应优化器（AdamW） | 用梯度的一阶、二阶历史统计缩放每个参数，并单独施加权重衰减 | $\Delta\theta\approx-\eta\hat m_t/(\sqrt{\hat v_t}+\epsilon)-\eta\lambda\theta_t$ | 参数更新 | 检验优化器是否改变边界方向和时间尺度 | 与 SGD 的差异不自动给出具体因果项 |
| 全序列语言建模损失 | 对序列中所有可预测位置计算下一词交叉熵 | 各位置交叉熵的平均 | 损失 | 同时包含特征位置与背景位置的训练信号 | 不等于真实文本语义质量 |

**图中英文标签对应：**

| 图中标签 | 中文含义 |
|---|---|
| `identical` / `matched` / `permuted` | 专家输出相同 / 专家功能与几何绑定一致 / 专家功能被循环交换 |
| `lr` | 学习率，即每一步梯度更新的全局倍率 |
| `Mean one-step geometry-matched margin change` | 原初始化几何绑定的一步平均间隔变化 |
| `soft` / `weighted_top1` | 所有专家参与输出的软路由 / 只执行最高分专家的加权路由 |
| `Initial rank of utility-matched expert` | 功能匹配专家在初始路由得分中的名次 |
| `Mean first correction step (201 = censored)` | 平均首次纠正步数；200 步内未纠正时记为 201 |
| `signal_only` / `orthogonal_zero_mean` | 只有特征信号 / 与特征边界正交且均值为零的背景 |
| `common_balanced` / `common_biased` | 公共隐藏状态配均衡目标 / 公共隐藏状态固定配目标 0 |
| `Signal fraction` | 32 个位置中特征信号位置所占比例 |
| `Final matched-margin p05` | 最终最小匹配间隔在全部特征-种子单元中的第 5 百分位 |
| `Fraction ever crossing zero` | 训练中匹配间隔至少一次变为非正的单元比例 |

## 2. 机制解释与建模

### 2.1 从之前的工作如何过渡到当前问题

| 已建立的事实 | 直接含义 | 暴露出的缺口 | 因此转向的问题 |
|---|---|---|---|
| 路由位置的特征几何可以被聚类，并可用于构造初始路由行 | 正确分区在受控条件下可达 | 初始化正确不等于训练会保持 | 训练每一步如何改变间隔 |
| 初始间隔缩放到 $q\ge0.05$ 时保持，$q=0.02$ 时从正间隔越界 | 保持存在有限安全间隔，而非“只要初始为正即可” | 尚不知道什么信号增厚或消耗间隔 | 建立带正负来源的间隔预算 |
| 真实文本代理分区在第 0 步存在，但第 5/10 步迅速消失 | 普通训练会覆盖初始化分区 | 用不同“公共方向”定义会得到相反归因 | 不再把公共均值直接当根因，改测梯度对边界的投影 |
| 所有 32 个位置都携带特征、没有背景位置时，理想分区在 2000 步后仍保持 | 背景或非特征位置是此前侵蚀现象的必要候选 | “有背景”仍混合了数量、方差和方向偏置 | 分开背景数量、零均值波动和系统偏置 |

这一步过渡把问题从“能否找到一个中心初始化路由器”收窄为：

> 正确专家是否产生可用于增厚间隔的任务信号；稀疏路由是否能访问该信号；该信号能否跑赢背景压力并在越界后完成纠正。

### 2.2 核心数学模型

1. 路由间隔只对路由行差与特征中心的相对投影敏感。

$$
m_{f,a,b}=(w_a-w_b)^\top\mu_f.
$$

2. 对冻结表征、固定专家和软路由，链式法则给出路由行的一步更新。

$$
p_e=\operatorname{softmax}(Wh/\tau)_e,
\qquad
\hat y=\sum_ep_eE_e(h),
$$

$$
\Delta w_e=\frac{\eta}{\tau}\mathbb E[p_eA_eh],
\qquad
A_e=-\langle\nabla_{\hat y}\ell,E_e(h)-\hat y\rangle.
$$

因此，正确专家相对竞争专家的概率加权优势决定间隔方向：

$$
\Delta m_{f,a,b}
=\frac{\eta}{\tau}
\mathbb E[(p_aA_a-p_bA_b)h^\top\mu_f\mid f].
$$

3. 对只执行最高分专家的加权路由，在没有得分并列的局部区域内：

$$
B_r=-\langle\nabla_{\hat y}\ell,E_r(h)\rangle,
$$

$$
\Delta w_j
=\frac{\eta}{\tau}p_r(\mathbf1[j=r]-p_j)B_rh.
$$

当 $j\ne r$ 时，更新中没有 $E_j$。未选路由行并非没有梯度，而是没有利用自己的专家功能进行反事实比较。

4. 对冻结特征中心和普通随机梯度下降，间隔可以按信号来源精确累计。

$$
m_{f,a,b}(T)=m_{f,a,b}(0)
+\sum_{t<T}\Delta m^{\mathrm{signal}}_{f,a,b}(t)
+\sum_{t<T}\Delta m^{\mathrm{background}}_{f,a,b}(t),
$$

$$
\Delta m^s_{f,a,b}(t)
=-\eta\bigl(g^s_{w_a}(t)-g^s_{w_b}(t)\bigr)^\top\mu_f.
$$

物理先验是：期望为零的波动主要增加方差，其典型累计尺度约为 $O(\sqrt T)$；具有固定符号的平均偏置按 $O(T)$ 累积。该尺度关系是受控建模先验，不是当前对可训练 Transformer 的定理。

### 2.3 三组受控实验分别回答什么

| 机制环节 | 可证伪假设 | 控制变量 | 直接否证条件 |
|---|---|---|---|
| 正信号从哪里来 | 专家功能匹配会产生正的局部间隔压力 | 固定隐藏状态、路由几何、标签和优化，只改变专家功能映射 | 交换功能后间隔仍跟随原几何标签，或相同专家仍产生非零任务更新 |
| 稀疏路由如何纠错 | 未选专家缺少各自功能比较，因此纠错依赖初始排名 | 固定特征、专家和温度，只改变有用专家初始排名与是否执行全部专家 | 稀疏路由对排名不敏感，或能优先提升低排名但有用的未选专家 |
| 什么背景会耗尽间隔 | 只有具有非零边界投影的系统偏置会稳定造成越界 | 固定背景数量，只改变背景是否正交、目标是否均衡、是否带公共目标偏置 | 零均值或目标均衡背景与偏置背景同样越界 |

### 2.4 数学结论的状态

| 数学关系 | 状态 | 使用方式 |
|---|---|---|
| 软路由一步更新公式 | 在冻结表征、固定专家、普通随机梯度下降下由链式法则精确成立 | 实现正确性与局部机制模型 |
| 只执行最高分专家的一步更新公式 | 在当前最高分专家不发生并列的局部区域内精确成立 | 说明未选行有梯度，但没有自己的功能比较 |
| 固定中心的信号/背景预算 | 对实际普通随机梯度下降增量是代数恒等式 | 检查来源记录是否闭合，不能单独作为因果证据 |
| 偏置线性累积、零均值波动平方根累积 | 物理先验与期望尺度 | 指导背景对照，不是当前模型外的普遍定理 |
| 首次越界时间近似 | 竞争专家局部稳定且平均总增量为负时的局部近似 | 解释阈值趋势，不用于精确预测每条轨迹 |

## 3. 主要结果

**一句话总结：** 正确路由的保持不是静态聚类问题，而是“功能匹配产生的正间隔信号、稀疏路由的排名式纠错、边界投影背景偏置”三者竞争的动力学问题。

### 结果 1：在冻结表征的软路由中，局部间隔压力跟随专家功能，而不跟随初始化标签。

**机制对应：** 检验公式中的 $p_aA_a-p_bA_b$ 是否真是决定间隔方向的变量，而不是对初始化几何的重新命名。

**指标定义：** 正间隔变化比例统计所有特征-种子单元中，一步更新后原匹配间隔增大的比例。

$$
R_+=\frac1N\sum_{i=1}^N\mathbf1[\Delta m_i^{\mathrm{geometry}}>0].
$$

功能重定向差衡量交换专家功能后，间隔是否更偏向真正有用的专家。

$$
D_{\mathrm{redirect}}
=\Delta m^{\mathrm{utility}}-\Delta m^{\mathrm{geometry}}.
$$

**证据说明：**

| 专家功能条件 | 学习率 | 正间隔变化比例 | 原几何绑定平均变化 | 功能匹配绑定平均变化 |
|---|---:|---:|---:|---:|
| 功能与几何匹配 | 0.01 | 1.000 | +0.002391 | +0.002391 |
| 功能与几何匹配 | 0.05 | 1.000 | +0.011953 | +0.011953 |
| 所有专家输出相同 | 0.01 / 0.05 | 0.000 | 0.000000 | 0.000000 |
| 功能循环交换 | 0.01 | 0.000 | -0.001906 | +0.003219 |
| 功能循环交换 | 0.05 | 0.000 | -0.009529 | +0.016093 |

![交换专家功能会改变间隔更新方向](figures/specialization_utility_intervention_margin_change.png)

**如何读图：** 柱高于零表示原几何绑定被强化，低于零表示原绑定被削弱；比较三种功能条件即可判断更新跟随几何还是专家功能。

**解释：** 固定几何而交换专家功能后，间隔更新随功能发生反号，排除了“路由行只因对齐中心而自动强化”的解释。公式与自动微分的最大误差为 $2.61\times10^{-18}$，只说明实现闭合；真正的因果证据是功能干预导致符号翻转。

**边界：** 该结果是一步软路由局部结论，不说明有用专家会在训练中自然形成，也不说明稀疏路由能直接获得同一信号。

**来源：** [机制锚点](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_31_soft_router_advantage_margin_dynamics_anchor.md)、[实验协议](../../../Projects/from-attention-to-search/main/experiments/A06/A06_31_soft_router_advantage_margin_dynamics/protocol.md)、[结果摘要](../../../Projects/from-attention-to-search/main/experiments/A06/A06_31_soft_router_advantage_margin_dynamics/summary.md)、[完整记录](../../../Projects/from-attention-to-search/main/experiments/A06/A06_31_soft_router_advantage_margin_dynamics/detailed.md)。

### 结果 2：只执行最高分专家的稀疏路由能够纠错，但纠错按当前得分排名逐个搜索。

**机制对应：** 检验未选专家缺少各自功能比较，是否使纠正时间随有用专家初始排名迅速增长。

**指标定义：** 纠正步数是有用专家第一次成为最高分专家的训练步；排名惩罚是第 4 名与第 2 名纠正步数之差。

$$
T_{\mathrm{corr}}(f)
=\min\{t:\arg\max_es_e(\mu_f,t)=a(f)\},
$$

$$
P_{\mathrm{rank}}=T_{\mathrm{corr}}(\mathrm{rank\ 4})
-T_{\mathrm{corr}}(\mathrm{rank\ 2}).
$$

边界切换次数记录搜索过程中最高分专家改变了多少次。

$$
N_{\mathrm{switch}}
=\sum_{t=1}^{T}\mathbf1[r_t\ne r_{t-1}].
$$

未选专家功能差比较有用未选专家与其他未选专家沿特征方向的更新；正值表示有用专家被优先提升。

$$
G_{\mathrm{unselected}}
=\langle\Delta w_a,\mu_f\rangle
-\frac{1}{|\{j:j\ne r,a\}|}
\sum_{j\ne r,a}\langle\Delta w_j,\mu_f\rangle.
$$

**证据说明：**

| 路由方式 | 有用专家初始第 1 名 | 初始第 2 名 | 初始第 4 名 | 排名惩罚 |
|---|---:|---:|---:|---:|
| 所有专家参与的软路由 | 0 步 | 7 步 | 30 步 | 23 步 |
| 只执行最高分专家的加权路由 | 0 步 | 12 步 | 153 步 | 141 步 |

![有用专家初始排名越低，稀疏路由纠正越慢](figures/specialization_top1_correction_time_by_rank.png)

**如何读图：** 横轴是有用专家的初始名次，纵轴越高表示纠错越慢；两条曲线的差距衡量稀疏选择带来的额外排名惩罚。

第 4 名条件下，软路由只切换 1 次，稀疏路由切换 142 次。未选专家功能差为 `+0.02167` 和 `-0.00736`：前者表示软路由会优先提升有用的未选专家，后者表示稀疏路由最初反而更偏向当前排名更高的替代专家。

**解释：** “未选专家没有梯度”是错误表述。未选行通过概率分母发生更新，但更新不知道各自专家是否有用，因此纠错表现为按当前排名进行的边界搜索。

**边界：** 全部特征-种子单元最终都在 200 步内恢复，故“永久锁死”和“完全没有修正机制”均被否定。该实验也不证明软路由在可训练混合专家模型中整体更优。

**来源：** [机制锚点](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_32_top1_counterfactual_correction_dynamics_anchor.md)、[实验协议](../../../Projects/from-attention-to-search/main/experiments/A06/A06_32_top1_counterfactual_correction_dynamics/protocol.md)、[结果摘要](../../../Projects/from-attention-to-search/main/experiments/A06/A06_32_top1_counterfactual_correction_dynamics/summary.md)、[完整记录](../../../Projects/from-attention-to-search/main/experiments/A06/A06_32_top1_counterfactual_correction_dynamics/detailed.md)。

### 结果 3：破坏间隔的不是背景位置多，而是背景梯度在路由边界上具有持续同向投影。

**机制对应：** 检验累计背景项 $C_{\mathrm{background}}$ 的方向是否比背景位置数量更能决定越界。

**指标定义：** 对每个特征先取它相对所有竞争专家的最小最终间隔，再对全部特征-种子单元取第 5 百分位。

$$
m_{\min}(f,T)=\min_{b\ne a(f)}m_{f,a(f),b}(T),
$$

$$
M_{0.05}=Q_{0.05}\bigl(\{m_{\min}(f,T)\}\bigr).
$$

曾越界比例与最终正确路由比例分别区分“过程脆弱”和“最终失败”。

$$
R_{\mathrm{cross}}
=\frac1N\sum_i\mathbf1[\exists t:m_i(t)\le0],
\qquad
R_{\mathrm{final}}
=\frac1N\sum_i\mathbf1[r_i(T)=a(f_i)].
$$

**证据说明：**

| 背景条件 | 特征信号比例 | 最终低尾间隔 | 曾越界比例 | 最终正确路由比例 |
|---|---:|---:|---:|---:|
| 只有特征信号 | 1.000 | 2.826 | 0.000 | 1.000 |
| 零均值正交背景 | 0.0625 | 1.260 | 0.000 | 1.000 |
| 公共状态、目标均衡 | 0.0625 | 1.260 | 0.000 | 1.000 |
| 公共状态、目标偏置 | 0.500 | 1.154 | 0.000 | 1.000 |
| 公共状态、目标偏置 | 0.250 | 0.424 | 0.750 | 1.000 |
| 公共状态、目标偏置 | 0.125 | -0.001 | 0.750 | 0.734 |
| 公共状态、目标偏置 | 0.0625 | -1.128 | 0.750 | 0.250 |

![有方向的背景偏置产生首次越界与最终恢复两个阈值](figures/specialization_background_margin_budget_threshold.png)

**如何读图：** 左图越低表示最终安全间隔越薄，低于零表示最终仍在错误边界一侧；右图大于零表示训练过程中至少发生过一次越界。

**解释：** 背景占 30/32 时，两个均衡对照仍完全安全，因此“背景多就会坍塌”被否定。目标偏置公共背景只损害特征 1--3、帮助特征 0，所以曾越界比例稳定为 0.75。信号比例 0.25 时虽然三类受损特征都曾越界，但到第 500 步全部重新进入；因此首次越界与最终失败必须分开建模。

**边界：** 当前背景偏置是人为构造的受控算子，不是对真实文本公共成分的识别。预算最大闭合误差 $1.79\times10^{-14}$ 只验证记录正确，不能证明同一分解适用于表征会移动或使用 AdamW 的训练。

**来源：** [机制锚点](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_33_background_bias_margin_budget_anchor.md)、[实验协议](../../../Projects/from-attention-to-search/main/experiments/A06/A06_33_background_bias_margin_budget/protocol.md)、[结果摘要](../../../Projects/from-attention-to-search/main/experiments/A06/A06_33_background_bias_margin_budget/summary.md)、[完整记录](../../../Projects/from-attention-to-search/main/experiments/A06/A06_33_background_bias_margin_budget/detailed.md)。

## 4. 执行动作

**下一步动作：** 在原有一层 Transformer、只执行最高分专家的混合专家层、长度 32 和全序列语言建模损失上，围绕临界信号比例进行四个冻结干预。专家函数在第一轮保持固定；主条件使用目标偏置公共背景下的 $8/32$ 和 $4/32$ 特征信号，另保留全特征信号和目标均衡公共背景作为安全对照。

| 条件 | 可训练部分 | 优化器 | 回答的问题 |
|---|---|---|---|
| 路由器单独移动 | 只训练路由行，冻结表征与专家 | 普通随机梯度下降 | 路由行漂移是否足以造成越界或恢复 |
| 表征单独移动 | 训练 Transformer 表征，冻结路由行与专家 | 普通随机梯度下降 | 特征中心漂移是否足以造成越界或恢复 |
| 联合训练 | 同时训练表征与路由器 | 普通随机梯度下降 | 两条路径的耦合是否是必要条件 |
| 联合训练加自适应缩放 | 同时训练表征与路由器 | AdamW | 历史梯度缩放是否改变越界与恢复时间尺度 |

**目的：** 判断完整训练中的首次越界和重新进入，究竟需要路由行移动、特征中心移动、二者耦合，还是还需要优化器的逐参数历史缩放。

完整模型中的间隔为：

$$
m_t=(w_a(t)-w_b(t))^\top\mu_f(t).
$$

一步变化可精确写成：

$$
\Delta m
=(\Delta w_a-\Delta w_b)^\top\mu_f
+(w_a-w_b)^\top\Delta\mu_f
+(\Delta w_a-\Delta w_b)^\top\Delta\mu_f.
$$

三项依次表示路由行移动、表征中心移动和二者同一步耦合。这个等式是代数恒等式，只能用于轨迹核对；因果判断必须来自冻结干预。

**完成判据：**

1. 同时报告首次越界比例、首次越界步数、重新进入比例、重新进入步数和最终低尾间隔，不能只报告最终聚类纯度。
2. 若冻结表征后越界消失，则表征更新对越界是必要的；若冻结路由器后越界消失，则路由器更新对越界是必要的。恢复事件按同一逻辑单独判断。
3. 如果路由器单独移动和表征单独移动都不能复现，而联合训练能够复现，则支持“表征与路由耦合是必要机制”。
4. 只有 AdamW 相对普通随机梯度下降稳定改变事件率或时间尺度时，才把优化器传递效应保留为下一层机制变量。

## 5. 证据索引

| 结果 | 主要指标或图 | 支持什么 | 不能证明什么 | 来源 |
|---|---|---|---|---|
| 专家功能决定局部间隔方向 | 正间隔变化比例；功能交换后的符号翻转；功能干预图 | 功能优势是软路由局部强化变量 | 长期保持、可训练专家自然形成 | [结果摘要](../../../Projects/from-attention-to-search/main/experiments/A06/A06_31_soft_router_advantage_margin_dynamics/summary.md) |
| 稀疏路由按排名纠错 | 纠正步数、排名惩罚、边界切换次数；初始排名图 | 未选专家缺少自己的功能比较 | 永久锁死、生产模型优劣 | [结果摘要](../../../Projects/from-attention-to-search/main/experiments/A06/A06_32_top1_counterfactual_correction_dynamics/summary.md) |
| 有方向背景偏置耗尽间隔 | 最终低尾间隔、曾越界比例、最终正确路由比例；阈值图 | 背景方向比背景数量更关键；越界与最终失败不同 | 真实文本公共算子、AdamW 归因 | [结果摘要](../../../Projects/from-attention-to-search/main/experiments/A06/A06_33_background_bias_margin_budget/summary.md) |

## 6. 来源索引

**当前三个机制锚点：**

- [专家功能到间隔动力学](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_31_soft_router_advantage_margin_dynamics_anchor.md)
- [稀疏路由反事实纠错动力学](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_32_top1_counterfactual_correction_dynamics_anchor.md)
- [背景偏置与间隔预算](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_33_background_bias_margin_budget_anchor.md)

**实验协议：**

- [专家功能干预协议](../../../Projects/from-attention-to-search/main/experiments/A06/A06_31_soft_router_advantage_margin_dynamics/protocol.md)
- [稀疏纠错协议](../../../Projects/from-attention-to-search/main/experiments/A06/A06_32_top1_counterfactual_correction_dynamics/protocol.md)
- [背景预算协议](../../../Projects/from-attention-to-search/main/experiments/A06/A06_33_background_bias_margin_budget/protocol.md)

**结果摘要与完整记录：**

- [专家功能结果摘要](../../../Projects/from-attention-to-search/main/experiments/A06/A06_31_soft_router_advantage_margin_dynamics/summary.md)；[完整记录](../../../Projects/from-attention-to-search/main/experiments/A06/A06_31_soft_router_advantage_margin_dynamics/detailed.md)
- [稀疏纠错结果摘要](../../../Projects/from-attention-to-search/main/experiments/A06/A06_32_top1_counterfactual_correction_dynamics/summary.md)；[完整记录](../../../Projects/from-attention-to-search/main/experiments/A06/A06_32_top1_counterfactual_correction_dynamics/detailed.md)
- [背景预算结果摘要](../../../Projects/from-attention-to-search/main/experiments/A06/A06_33_background_bias_margin_budget/summary.md)；[完整记录](../../../Projects/from-attention-to-search/main/experiments/A06/A06_33_background_bias_margin_budget/detailed.md)

**过渡证据：**

- [真实文本代理路由坍塌与公共方向定义不稳](../../../Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/summary.md)
- [有限安全间隔阈值](../../../Projects/from-attention-to-search/main/experiments/A06/A06_23_top1_lockin_margin_threshold/summary.md)
- [无背景全特征序列的长期保持](../../../Projects/from-attention-to-search/main/experiments/A06/A06_30_noise_free_full_slot_preservation/summary.md)

**本简报图：**

- `figures/specialization_utility_intervention_margin_change.png`
- `figures/specialization_top1_correction_time_by_rank.png`
- `figures/specialization_background_margin_budget_threshold.png`

## 7. 补充材料

### 当前假设更新

| 旧说法 | 当前判断 | 更新后的精确说法 |
|---|---|---|
| 正确中心初始化会在训练中自动保持 | 否定 | 保持需要足够初始间隔，并需要后续正信号不被负预算耗尽 |
| 未选专家没有梯度，所以最高分路由不能纠错 | 否定 | 未选路由行有概率竞争梯度，但没有自己的专家功能比较，因此纠错慢且依赖排名 |
| 背景噪声导致路由坍塌 | 过强，否定 | 背景数量和目标均衡公共状态都不充分；受控充分原因是具有非零决策边界投影的平均偏置 |
| 间隔一旦变负就代表不可恢复 | 否定 | 首次越界是脆弱性事件；最终失败还取决于越界后的纠正是否能重新进入 |
| 当前应立即设计新路由器 | 暂不支持 | 先确定完整训练中路由行漂移、表征漂移和优化器缩放各自的因果作用，再决定方法靶点 |

### 当前最小机制图景

$$
\boxed{
\text{功能匹配产生正间隔信号}
\;\longrightarrow\;
\text{稀疏路由按排名访问该信号}
\;\longleftrightarrow\;
\text{边界投影背景偏置消耗间隔}
}
$$

如果正信号先建立足够间隔，路由保持；如果负预算先使间隔越界，但纠错仍快于后续消耗，路由可以重新进入；如果纠错速度长期落后于负预算，最终绑定失败。下一步只需要判定这一图景在表征可训练和 AdamW 条件下由哪条路径实现。
