# MTP 是否更高效地学习长程语义信息

## 0. 执行摘要

**研究问题：** 多步预测目标能否比只预测下一词的目标更高效地让当前隐藏状态学到长程语义变量。

**机制解释：** 在干净 $\tau=3$ 构造中，只有覆盖第一个有信息未来词 $Y_3=S_Z$ 的目标，才会把变量 $Z$ 直接监督到决策前缀隐藏状态 $h_T$；这一机制在 06 中表现为一阶读出边距速度，在 07 中表现为无泄漏全位置训练里的更强恢复效率。

**主要结果：** 当前证据支持“直接覆盖有信息未来位置会带来更强、更稳定的长程语义恢复”，但不支持“非覆盖目标不能恢复 $Z$”或“自然语言中 MTP 一定更好”。

**证据说明：** 语义恢复分数 $Q(t)=\min\{A(t),P(t),S(t)\}$ 用来判断 $Z$ 是否可稳定读出；模型自身第三步预测准确率和读出边距 $M_Z$ 用来判断这种恢复是否来自直接 $h_T\rightarrow S_Z$ 监督。

1. 在决策前缀隔离实验中，K3 的隐藏状态读出边距速度为 $0.003816$，K1/K2 近似为 $0$，说明覆盖 $Y_3=S_Z$ 的目标提供了直接语义更新方向。
2. 在无泄漏全位置训练中，K3 和 K2 加直接第三步监督均达到 `reach=1.00`、最终 $Q=1.00$、模型自身第三步预测准确率 $=1.00$，比 K1/K2 和去掉直接项的 K3 更强。
3. K1/K2 和去掉直接项的 K3 仍能在部分 seed 中恢复较高 $Q$，但模型自身第三步预测准确率接近 $0$，说明全位置训练存在间接迁移，$Q$ 不能单独作为直接监督证据。

**结论边界：** 当前只能声称受控干净 $\tau=3$ 下的直接监督与学习效率优势，不能外推到自然语言、不能声称 K 越大越好，也不能推出 MoE 路由或专家效用。

**执行动作：** 收束 A11 主线为“直接语义状态形成机制”，下一步若连接 MoE 主线，应先写一个最小路由相关性桥接判定卡，完成判据是语义边距变化能否转化为路由相关边距或路由边界翻转变化，并保留局部语言建模守卫。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| 多步预测目标（MTP） | 一次从当前隐藏状态预测多个未来词 | K1 预测 $Y_1$，K2 预测 $Y_1,Y_2$，K3 预测 $Y_1,Y_2,Y_3$ | $L_K=\sum_{j=1}^K \lambda_j\operatorname{CE}(q_j(\cdot\mid h),Y_j)$ | 判断目标是否覆盖第一个有信息未来词 | 自然语言中一定有效 |
| 下一词预测目标（NTP） | 只预测下一个词 | K1 条件，只激活 $Y_1$ loss | $L_1=\operatorname{CE}(q_1(\cdot\mid h),Y_1)$ | 作为非覆盖对照 | NTP 不可能学到长程信息 |
| 干净 $\tau=3$ 构造 | 第三个未来词才第一次包含 $Z$ 的受控数据 | $Y_1=A_{\mathrm{shared}},Y_2=C_{\mathrm{shared}},Y_3=S_Z$ | 未来位置偏移 | 隔离“是否覆盖第一个有信息未来词” | 真实文本也有固定 $\tau=3$ |
| 第一个有信息未来位置（informative horizon） | 第一个含有 $Z$ 信息的未来位置 | 干净 $\tau=3$ 中 $Y_3=S_Z$ | $\tau=3$ | 决定 K 是否直接覆盖语义变量 | 真实文本中的固定 horizon |
| K1 fixed 3-head | 预测头数量与 K3 匹配、但只训练下一词的对照 | 只激活 $Y_1$ loss，保留 3 个预测头 | 条件标签 | 排除“预测头数量不同”解释 | K1 不能通过全位置间接迁移恢复 $Z$ |
| K2 active | 非覆盖的两步预测对照 | 激活 $Y_1,Y_2$ loss | 条件标签 | 检查没有覆盖 $Y_3$ 时的表现 | 全位置中不能恢复 $Z$ |
| K3 full / K3 active | 覆盖 $Y_3=S_Z$ 的完整条件 | 激活 $Y_1,Y_2,Y_3$ loss | 条件标签 | 检验直接监督路径 | K 越大一定越好 |
| K3 masked direct L3 | 去掉决策前缀直接第三步监督的 K3 对照 | 保留其他 K3 全位置 loss，删除 $h_T\rightarrow S_Z$ | 条件标签 | 分离直接项和间接迁移 | 所有间接路径都被去掉 |
| K2 plus direct L3 | 在 K2 上只加决策前缀第三步监督 | K2 loss + $L_{\mathrm{direct}}$ | 条件标签 | 检验直接项是否足够产生 K3 式效果 | 完整 K3 的全部作用 |
| 决策前缀隐藏状态 | 当前要被检查的隐藏状态 | 序列前缀 `BR_z F... U...` 之后的 $h_T$ | 向量 | 表示是否含有长程变量 $Z$ | 所有位置都含有 $Z$ |
| 直接第三步监督 | 当前 $h_T$ 直接预测 $S_Z$ | $\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$ | 交叉熵 | 检验机制项是否足以带来效率优势 | 唯一恢复路径 |
| 全位置训练 | 每个位置都做语言模型式预测 | $\sum_t\sum_{j=1}^K\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j})$ | 交叉熵 | 更接近语言模型训练，也会引入间接迁移 | 自然语言泛化 |
| 间接迁移 | 非直接位置的 loss 通过共享参数让 $h_T$ 变得可读 | K1/K2 或 masked K3 中的共享参数更新 | 现象判断 | 解释非覆盖条件也能恢复 $Q$ | 直接 $h_T\rightarrow S_Z$ 预测 |
| 语义恢复分数 $Q(t)$ | 三个恢复检测的保守最小值 | $A(t)$、$P(t)$、$S(t)$ 的最小值 | $Q(t)=\min\{A(t),P(t),S(t)\}$ | 判断 $Z$ 是否稳定可读出 | 恢复路径是直接监督 |
| $A(t)$ | 从冻结 $h_T$ 解码 $Z$ 的准确率 | 有信息未来位置解码器准确率 | 准确率 | 检测 $h_T$ 是否含 $Z$ | 模型自身能预测 $S_Z$ |
| $P(t)$ | 冻结线性探针从 $h_T$ 预测 $Z$ 的准确率 | 训练后冻结表示，再用线性探针预测 $Z$ | 准确率 | 防止单一解码器偶然成功 | 因果使用 $Z$ |
| $S(t)$ | 分支交换一致性 | 交换 branch 后预测是否跟随 branch | 准确率 / 一致性 | 排除表面捷径 | 所有捷径都不存在 |
| 达到率 | 多个随机种子中有多少达到稳定恢复阈值 | 满足 $T_{0.9}$ 的种子比例 | 比例 | 衡量稳定性 | 达到种子内部的速度 |
| $T_{0.9}$ | 稳定恢复所需步数 | 连续 3 次评估满足 $Q(t)\ge0.9$ 的最早 step | 训练步 | 同时看速度和稳定性 | 最终能力来源 |
| 早期面积（early AUC Q） | 早期训练窗口内 $Q$ 的平均水平 | 0 到 3000 step 的 $Q(t)$ 平均值 | 分数 | 衡量更早学到多少 | 梯度因果来源 |
| 读出有效语义边距 $M_Z$ | $h_T$ 是否沿正确 $S_Z$ 输出方向分开 | 固定初始输出行投影 | $M_Z=\frac1m\sum_z(u^0_{S_z}-\bar u^0)^\top h_T(z)$ | 连接理论一阶机制和训练曲线 | 当前 head 自适应全部作用 |
| 分离能量 $E_Z$ | 不同 branch 的 $h_T$ 是否在隐藏空间分开 | 两两隐藏状态距离 | $E_Z=\frac{1}{2m^2}\sum_{z,z'}\|h_T(z)-h_T(z')\|^2$ | 检查隐藏状态是否分离 | 分离方向对任务有用 |
| 模型自身第三步预测准确率 | 模型从 $h_T$ 直接预测 $S_Z$ 的准确率 | $\Pr[\arg\max q_3(\cdot\mid h_T)=S_Z]$ | 准确率 | 区分直接预测和可被探针读出的恢复 | 下游效用 |
| 局部守卫 | 共享近端目标是否被破坏 | $Y_1/Y_2$ loss 和准确率 | 交叉熵 / 准确率 | 排除“牺牲近端学习换长程恢复” | 全局语言建模质量 |

## 2. 机制解释与建模

**核心模型：**

数据序列为：

$$
BR_z,\;F_0,\ldots,F_{L-1},\;U_0,\ldots,U_3,\;A_{\mathrm{shared}},\;C_{\mathrm{shared}},\;S_z,\;STOP.
$$

在决策前缀 $h_T$ 之后，未来三个目标是：

$$
Y_1=A_{\mathrm{shared}},\qquad Y_2=C_{\mathrm{shared}},\qquad Y_3=S_Z.
$$

其中 $Y_1$ 和 $Y_2$ 不含 branch 变量 $Z$，$Y_3$ 是 $Z$ 的一一编码：

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

全位置训练 loss 为：

$$
L_K^{all}=\sum_t\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j}).
$$

直接决策前缀第三步监督项为：

$$
L_{\mathrm{direct}}=\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z).
$$

读出有效语义边距为：

$$
M_Z(t)=\frac1m\sum_z(u^0_{S_z}-\bar u^0)^\top h_T(z,t).
$$

**符号含义：**

- $Z$：早期 branch 变量，也是需要被长程保留的语义变量。
- $h_T$：在 `U` 之后、预测 $Y_1,Y_2,Y_3$ 之前的当前隐藏状态。
- $S_Z$：由 $Z$ 唯一决定的未来 token。
- $K$：预测范围；K1 不覆盖 $Y_3$，K2 不覆盖 $Y_3$，K3 覆盖 $Y_3$。
- $u^0_{S_z}$：初始化时第三步预测 head 中 $S_z$ 的输出向量。
- $\bar u^0$：所有 $S_z$ 输出向量的均值。

**机制链条：**

1. 当 K 不覆盖 $Y_3=S_Z$ 时，决策前缀上的活跃目标只包含共享 token $A_{\mathrm{shared}}$ 和 $C_{\mathrm{shared}}$，对不同 branch 给出的直接更新相同。
2. 当 K 覆盖 $Y_3=S_Z$ 时，loss 中出现 $h_T\rightarrow S_Z$，不同 branch 的 $h_T$ 被推向不同的 $S_z$ 输出方向。
3. 06 的一阶指标检验这一步是否真的发生；07 的全位置训练检验这一步是否转化为更快、更稳定的语义恢复。

**当前问题分解：**

- 需要判定的机制项：直接 $h_T\rightarrow S_Z$ 监督是否是效率优势来源。
- 最危险的替代解释：全位置训练中的间接迁移也能让 $Z$ 被 probe 读出。
- 当前实验能区分：直接监督是否带来更强模型自身第三步预测与更大 $M_Z$。
- 当前实验不能区分：该机制在自然语言中是否仍成立，或是否能提升 MoE 专家效用。

## 3. 主要结果

**一句话总结：** clean $\tau=3$ 下，覆盖第一个有信息未来词的直接监督会更快、更稳定地形成长程语义状态；但全位置训练中存在间接迁移，所以 $Q$ 高不等于直接监督成立。

### 结果 1：K3 在隔离的一阶实验中产生直接语义更新方向，K1/K2 基本不产生。

**机制对应：** 对应第 2 节机制链条的第 1 和第 2 步，即共享目标不能区分 branch，有信息目标可以区分 branch。

**指标或条件定义：** 06 使用决策前缀隔离训练。K1 只激活 $Y_1$，K2 激活 $Y_1,Y_2$，K3 激活 $Y_1,Y_2,Y_3$。核心指标 $G_M^{hidden}$ 是隐藏状态沿正确 $S_Z$ 输出方向的一阶速度。

**证据：** 完整运行已完成，远程任务编号为 `pt-57nu5dv1`。泄漏守卫通过：$Q(0)=0.25$，$M_Z(0)\approx0$，$E_Z(0)=0$，step-0 模型自身第三步预测准确率为 $0$。在 $\eta=3\times10^{-4}$ 摘要中：

| 条件 | $G_M^{hidden}$ | $G_E$ | one-step 局部 CE 变化 | 短程 early AUC Q | 短程 final Q |
|---|---:|---:|---:|---:|---:|
| K1 fixed 3-head | $7.28\times10^{-12}$ | 0.000000 | $Y_1$ 下降，$Y_2$ 近似不变 | 0.250 | 0.25 |
| K2 active | $-1.16\times10^{-11}$ | 0.000000 | $Y_1/Y_2$ 均下降 | 0.250 | 0.25 |
| K3 active | 0.003816 | 0.000060 | $Y_1/Y_2$ 均下降 | 0.535 | 0.55 |

![One-step hidden readout-margin velocity](../A11_06_readout_effective_margin_efficiency/figures/one_step_hidden_margin.png)

**解释：** K1/K2 的目标在决策前缀上对所有 branch 相同，因此一阶更新不产生 $Z$ 方向的读出边距。K3 直接看到 $S_Z$，因此产生正的 $G_M^{hidden}$。局部 CE 没有恶化，说明该一阶语义方向不是通过破坏近端目标得到的。

**边界：** 06 只能证明隔离决策前缀的一阶机制，不能单独证明全位置训练效率，也不能说明 K1/K2 在全位置训练中无法恢复 $Z$。

**来源：** `../A11_06_readout_effective_margin_efficiency/summary.md`，`../A11_06_readout_effective_margin_efficiency/detailed.md`，`../A11_06_readout_effective_margin_efficiency/figures/one_step_hidden_margin.png`。

### 结果 2：无泄漏全位置训练中，直接第三步监督比间接路径更强、更稳定。

**机制对应：** 对应第 2 节机制链条的第 3 步，即直接语义更新方向是否转化为训练曲线上的效率优势。

**指标或条件定义：** 07 使用全位置语言模型式训练。`K3 full` 包含直接 $h_T\rightarrow S_Z$ 项；`K3 masked direct L3` 删除该直接项但保留其他 K3 全位置 loss；`K2 plus direct L3` 在 K2 上只加直接第三步监督，用来检验直接项是否足够。

**证据：** 完整运行已完成，远程任务编号为 `pt-nkdwrd8k`。所有条件泄漏守卫通过：$Q(0)=0.25$，$M_Z(0)\approx0$，$E_Z(0)=0$，step-0 模型自身第三步预测准确率为 $0$。

| 条件 | 达到率 | 达到种子的平均 $T_{0.9}$ | 早期面积 Q | 全程面积 Q | 最终 Q | 模型自身第三步预测 | 最终 $M_Z$ | 最终 $E_Z$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| K1 fixed 3-head | 0.60 | 250 | 0.838 | 0.834 | 0.85 | 0.05 | -0.000 | 0.002 |
| K2 active | 0.60 | 333 | 0.771 | 0.731 | 0.85 | 0.00 | -0.000 | 0.005 |
| K2 plus direct L3 | 1.00 | 250 | 0.969 | 0.994 | 1.00 | 1.00 | 3.735 | 82.573 |
| K3 full | 1.00 | 300 | 0.965 | 0.993 | 1.00 | 1.00 | 2.430 | 50.922 |
| K3 masked direct L3 | 0.60 | 833 | 0.817 | 0.750 | 0.70 | 0.00 | 0.004 | 0.010 |

![Guarded recovery curves](figures/q_curves.png)

![Readout margin curves](figures/margin_curves.png)

**解释：** 加入直接第三步监督后，K2 从 `reach=0.60` 提升到 `1.00`，early AUC Q 从 `0.771` 提升到 `0.969`，模型自身第三步预测从 `0.00` 提升到 `1.00`。在 K3 中去掉直接项后，reach 从 `1.00` 降为 `0.60`，reached $T_{0.9}$ 从 `300` 变慢到 `833`，final $M_Z$ 从 `2.430` 降到 `0.004`。这说明效率优势主要来自直接 $h_T\rightarrow S_Z$ 项，而不只是 K3 loss 更多。

**边界：** K1 的达到种子平均 $T_{0.9}$ 数字较小，但达到率只有 `0.60` 且模型自身第三步预测仅 `0.05`，不能把它解释为直接学习更快。K1 也不训练 $Y_2$，因此只作为预测头数量匹配的 NTP 对照。

**来源：** `summary.md`，`detailed.md`，`tables/condition_summary.csv`，`figures/q_curves.png`，`figures/margin_curves.png`。

### 结果 3：全位置训练存在间接迁移，所以 $Q$ 不能单独作为直接监督证据。

**机制对应：** 对应第 2 节的替代解释：共享参数和其他位置 loss 可以让 $Z$ 在 $h_T$ 中变得可被探针读出。

**指标或条件定义：** $Q$ 检查 $Z$ 是否可读，模型自身第三步预测和 $M_Z$ 检查是否沿直接 $h_T\rightarrow S_Z$ 路径学习。两类指标必须联合解释。

**证据：** K1/K2 和 masked K3 都能达到非平凡 $Q$：K1 final Q 为 `0.85`，K2 final Q 为 `0.85`，masked K3 final Q 为 `0.70`。但它们的模型自身第三步预测分别为 `0.05`、`0.00`、`0.00`，final $M_Z$ 也接近 `0`。

![Final Q versus native H3](figures/final_q_vs_native_h3.png)

**解释：** 如果只看 $Q$，会误以为非覆盖条件也学到了同样的直接语义预测；但模型自身第三步预测和 $M_Z$ 显示，这些条件主要是让 $Z$ 可被探针或辅助解码器读出，并没有学成原生 $h_T\rightarrow S_Z$ 预测。因此当前结论必须表述为“直接监督更强、更稳定”，不能表述为“只有 K3 能学到 $Z$”。

**边界：** 这不否定间接迁移的价值，也不说明可被探针读出的表示无用；它只说明可读出的 $Q$ 不是直接监督机制的充分证据。

**来源：** `summary.md`，`detailed.md`，`figures/final_q_vs_native_h3.png`。

## 4. 执行动作

**下一步动作：** 将 A11 当前轮收束为受控机制故事；若继续向主线推进，先建立一个最小路由相关性桥接判定卡，而不是继续扩 K 或进入自然语言实验。

**目的：** 检验“由 MTP 形成的长程语义状态”是否能影响 MoE 主线真正关心的路由相关几何，例如路由边距、路由边界翻转、稀有特征边距，而不是只停留在可被探针读出的表示。

**完成判据：** 新判定卡必须有一个决策问题、一个路由相关主指标、一个局部语言建模守卫，并明确区分 $M_Z$、模型自身第三步预测与 $Q$；只有当语义状态变化与路由相关指标同向变化时，才能进入更大实验。

## 5. 证据索引

| 结果 | 证据 | 主要指标或图 | 支持什么 | 不能证明什么 | 来源 |
|---|---|---|---|---|---|
| 结果 1 | 06 决策前缀一阶实验 | $G_M^{hidden}$；one-step hidden margin figure | K3 有直接语义更新方向，K1/K2 近零 | 全位置效率、自然语言收益 | `../A11_06_readout_effective_margin_efficiency/summary.md` |
| 结果 2 | 07 无泄漏全位置训练 | $T_{0.9}$、early AUC Q、模型自身第三步预测、$M_Z$ | 直接第三步监督更强、更稳定 | K1/K2 不能恢复 $Z$ | `summary.md` |
| 结果 3 | 07 直接项与间接项对照 | 最终 Q 对模型自身第三步预测图 | 全位置间接迁移存在，$Q$ 不是直接证据 | 可被探针读出的表示无价值 | `summary.md`，`detailed.md` |

## 6. 来源索引

**Anchor：**

- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_06_readout_effective_margin_efficiency_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_07_no_leakage_all_position_efficiency_anchor.md`

**Protocol：**

- `../A11_06_readout_effective_margin_efficiency/protocol.md`
- `protocol.md`

**Summary：**

- `../A11_06_readout_effective_margin_efficiency/summary.md`
- `summary.md`

**Detailed：**

- `../A11_06_readout_effective_margin_efficiency/detailed.md`
- `detailed.md`

**Figures：**

- `../A11_06_readout_effective_margin_efficiency/figures/one_step_hidden_margin.png`
- `figures/q_curves.png`
- `figures/margin_curves.png`
- `figures/final_q_vs_native_h3.png`

**Tables：**

- `../A11_06_readout_effective_margin_efficiency/tables/one_step_summary.csv`
- `tables/condition_summary.csv`
- `tables/decision_contrasts.csv`

## 7. 补充材料

局部目标守卫通过：K2、K3、K2 加直接第三步监督、masked K3 的最终 $Y_1/Y_2$ accuracy 均为 `1.00`。K1 的 $Y_1$ accuracy 为 `1.00`，$Y_2$ accuracy 为 `0.00`，这是因为 K1 不训练 $Y_2$，不能作为 K1 的失败解释。

当前最稳妥 claim：

```text
在受控干净 tau=3 构造中，覆盖第一个有信息未来词的直接监督会让当前 h_T 更快、更稳定地形成可用于 S_Z 预测的语义状态；全位置训练中存在间接迁移，因此 Q 必须和模型自身第三步预测、M_Z 联合解释。
```

当前最危险 overclaim：

```text
MTP 已经证明在自然语言中比 NTP 更高效，或 K1/K2 不能学到长程变量。
```
