# 初步条件性理论：广义 MTP 与 NTP 到底有什么区别

日期：2026-07-16

状态：在显式假设下成立的初步定理包；不是普遍神经网络证明。

英文主文档：[01_general_mtp_vs_ntp_theory.md](01_general_mtp_vs_ntp_theory.md)

> **当前入口更新：**本文件保留为广义目标与正交两模式背景。共享 common
> 子空间冲突、matched 信息增量、曲率修正功能判据及明日主题已统一到
> [理论澄清与明日汇报锚点](05_theory_clarification_and_meeting_anchor_cn.md)。

> **范围修正：**第 5–6 节讨论的是正交 common/rare 模式。研究者随后把当前
> 失败定义为“rare 特征被吸收到 common 主导的共享子空间”，所以正交模型只保留
> 为背景零假设。当前 overlap 模型与必要条件见
> [录音驱动的 low-hanging fruit](04_recording_driven_low_hanging_fruit_cn.md)。

## 1. 先固定我们讨论的对象

令 $C_t=Y_{\leq t}$ 表示当前位置前缀，
$H_t=f_\theta(C_t)$ 表示共享隐藏状态。把当前讨论中的标准 MTP 抽象为：

$$
\mathcal L_K(\theta,\phi_{1:K})
=
\mathbb E_t\left[
\sum_{k=1}^{K}\lambda_k
\ell\!\left(q_{\phi_k}(H_t),Y_{t+k}\right)
\right],
$$

其中 $\lambda_k\geq0$。NTP 是 $K=1$；测试时只使用普通主头
$q_{\phi_1}$ 自回归生成。

这只是一个工作定义，不覆盖所有名为 MTP 的实现。带串行预测模块、stop
gradient、共享预测头、不同 loss normalization 或 speculative decoding
目标的方法，需要分别分析。

## 2. 目标函数层面的本质区别

定义第 $k$ 个预测距离的损失：

$$
\mathcal L_k
=
\mathbb E_t\left[
\ell\!\left(q_{\phi_k}(H_t),Y_{t+k}\right)
\right].
$$

则

$$
\mathcal L_K=\sum_{k=1}^{K}\lambda_k\mathcal L_k.
$$

如果固定表征 $H_t$，并假设每个预测头表达能力充分且被优化到最优，那么：

$$
\min_{\phi_k}\mathcal L_k=H(Y_{t+k}\mid H_t).
$$

因此：

$$
\min_{\phi_{1:K}}\mathcal L_K
=
\sum_{k=1}^{K}\lambda_k H(Y_{t+k}\mid H_t)
=
\text{常数}
-
\sum_{k=1}^{K}\lambda_k I(H_t;Y_{t+k}).
$$

直观上，在表征容量有限时：

- NTP 直接要求 $H_t$ 保留预测 $Y_{t+1}$ 所需的信息；
- MTP 直接要求 $H_t$ 同时保留对多个未来位置有预测力的信息。

这是 MTP 最干净的“物理意义”：**把多个未来约束提前施加在同一个当前状态上。**

边界：这个理想预测头恒等式不能证明优化一定到达最优，不能证明主头因果使用，
也不能证明 NTP 无法通过后续位置和共享参数学到相同信息。

## 3. 训练动力学的一阶命题

令

$$
g_1=\nabla_\theta\mathcal L_1,\qquad
g_{\mathrm{aux}}
=
\sum_{k=2}^{K}\lambda_k\nabla_\theta\mathcal L_k.
$$

为了保持主损失系数一致，MTP 的一步更新写成：

$$
\theta_M'=\theta-\eta(g_1+g_{\mathrm{aux}}),
$$

NTP 的一步更新为：

$$
\theta_N'=\theta-\eta g_1.
$$

对主 NTP 损失作 Taylor 展开：

$$
\mathcal L_1(\theta_M')-\mathcal L_1(\theta_N')
=
-\eta\langle g_1,g_{\mathrm{aux}}\rangle+O(\eta^2).
$$

因此在局部一阶意义上：

- $\langle g_1,g_{\mathrm{aux}}\rangle>0$：auxiliary 梯度帮助当前 NTP 主目标；
- $\langle g_1,g_{\mathrm{aux}}\rangle<0$：auxiliary 梯度伤害当前主目标；
- 二者正交：一阶上不改善主目标，但仍可能改变表征和后续轨迹。

所以不存在不带条件的“MTP 训练更容易”或“MTP 训练更快”。

“训练效率”还必须指定分母：

- 每个 optimization step；
- 每个训练 token；
- 每个 FLOP；
- 每秒 wall-clock。

如果实现中把多个 active loss 取平均，主 NTP 项的系数本身也改变。此时必须加入
matched shared-aux：第二个头仍预测相同 next token，用来排除头数、loss 项数和
名义 scale 的影响。A11 已经说明了为什么这个对照必要。

## 4. 什么叫“未来目标提供了额外信息”

令 $Z$ 是输入中可访问、且稍后决策所需的潜在特征；令 $B_t$ 表示除 $Z$
以外的其余 nuisance context。如果第 $k$ 个未来位置满足：

$$
I\!\left(
Z;Y_{t+k}
\mid B_t,Y_{t+1:t+k-1}
\right)>0,
$$

那么在计入更早未来词元后，第 $k$ 个位置仍首次或额外暴露了关于 $Z$ 的信息。
这个目标有可能在 $H_t$ 上增加直接区分 $Z$ 的梯度。

这里不能在 $Z$ 本身是前缀的确定性特征时，再把完整前缀作为条件，否则条件互信息
会被定义性地消掉；$B_t$ 明确排除了正在研究的特征。如果 $Z$ 既不在输入中，也
无法从输入推断，任何训练目标都不可能稳定预测它。

A11 在受控任务中已经支持：

- 信息性未来目标产生更早直接信号；
- 该信号能够到达共享参数。

A11 同时给出关键反例边界：

> 当前位置形成信息，不足以保证后续普通主头稳定使用它。

## 5. common/rare 目标计数引理

考虑序列内部位置 $s$ 的一个目标词元。在 $K$ 个预测距离都启用时，它会分别
作为 $s-1,\ldots,s-K$ 位置的目标。因此远离边界时，每个 common 与 rare
目标都大约被重复 $K$ 次。

类别 $a$ 的加权目标质量为：

$$
M_K(a)
=
\sum_{s:Y_s=a}
\sum_{k=1}^{\min(K,s-1)}\lambda_k.
$$

如果 common 与 rare 在序列位置上的分布一致、且忽略边界效应，则：

$$
\frac{M_K(\mathrm{rare})}{M_K(\mathrm{common})}
\approx
\frac{N(\mathrm{rare})}{N(\mathrm{common})}.
$$

所以：

> **标准 MTP 本身不是 class-frequency reweighting。**

如果 MTP 对 long tail 有相对收益，原因必须是：

- 不同预测距离上的可预测性不同；
- 梯度方向或冲突不同；
- 有限容量的表征分配不同；
- 类别与序列位置/边界相关；
- 或者另一个被明确定义的机制。

## 6. common/rare 两模式相对学习定理

### 6.1 最小模型

令共享参数 $w$ 包含两个正交方向：

- common 模式 $v_c$；
- rare 模式 $v_r$。

参数误差为：

$$
e=w-w^\star=e_cv_c+e_rv_r.
$$

假设第 $k$ 个预测距离对应精确二次总体损失：

$$
\mathcal L_k(w)
=
\frac12e^\top Q_ke,
$$

并且：

$$
Q_k=q_{k,c}v_cv_c^\top+q_{k,r}v_rv_r^\top,
\qquad q_{k,c},q_{k,r}>0.
$$

$q_{k,j}$ 表示第 $k$ 个预测距离对模式 $j$ 的**有效曲率**：它同时包含该模式
出现的频率、特征能量，以及它对该预测距离有多大可预测作用。它不等于单纯的
token frequency。

### 6.2 梯度流

MTP 的总体曲率为：

$$
Q_M=\sum_{k=1}^{K}\lambda_kQ_k.
$$

于是两个模式的梯度流分别为：

$$
\dot e_c=-Q_{M,c}e_c,\qquad
\dot e_r=-Q_{M,r}e_r,
$$

其中：

$$
Q_{M,j}=\sum_{k=1}^{K}\lambda_kq_{k,j}.
$$

所以：

$$
e_j(t)=e_j(0)\exp(-Q_{M,j}t).
$$

定义 rare 相对 common 的收敛速率比：

$$
\rho_M
=
\frac{Q_{M,r}}{Q_{M,c}}
=
\frac{\sum_k\lambda_kq_{k,r}}
{\sum_k\lambda_kq_{k,c}}.
$$

NTP 的速率比是：

$$
\rho_N=\frac{q_{1,r}}{q_{1,c}}.
$$

### 6.3 定理

MTP 提高 rare 相对 common 的学习速度，当且仅当：

$$
\frac{\sum_k\lambda_kq_{k,r}}
{\sum_k\lambda_kq_{k,c}}
>
\frac{q_{1,r}}{q_{1,c}}.
$$

等价地：

$$
\sum_{k=2}^{K}\lambda_k
\left(q_{k,r}q_{1,c}-q_{k,c}q_{1,r}\right)>0.
$$

证明：$\nabla\mathcal L_K=Q_Me$。分别投影到 $v_c$ 和 $v_r$，就得到两个
标量微分方程及其指数解。因为所有分母均为正，比较 $\rho_M$ 与 $\rho_N$ 后
交叉相乘，恰好得到上面的等价符号条件。

### 6.4 三个直接推论

1. 如果所有预测距离的 rare/common 曲率比相同，MTP 只会整体加速或改变时间
   尺度，不会改变 rare 相对 common 的落后程度。
2. 如果更远预测距离相对富集 rare 模式，MTP 才会相对帮助 rare。
3. 如果更远预测距离更加富集 common 模式，MTP 反而会加剧相对失衡。

这给出当前最小、最明确的答案：

> **标准 MTP 不会自动解决 common/long-tail 冲突。它是否有效，取决于新增
> horizon 改变了什么模式的有效信息。**

## 7. 它与 0625 两阶段奇异模式证明是什么关系

0625 文档在单个 rank-one 模式中精确证明：

$$
1-c(t)^2
=
\left(1-c_0^2\right)
\exp\!\left(-(\sigma(t)^2-\sigma_0^2)\right).
$$

它说明：

- 特征方向的对齐可以较早饱和；
- 交叉熵压力仍可继续增大奇异值增益。

但它没有定义：

- 哪一个模式是 common，哪一个是 rare；
- 两个模式如何竞争；
- MTP 相对 NTP 改变了什么。

本文件的两模式定理补上的是“模式之间的相对学习率”这一层。二者合起来只支持
一个候选机制：

> common 模式可能较早找到方向并持续放大；MTP 只有在新增 horizon 改变
> common/rare 的相对有效能量或相互作用时，才会改变这种失衡。

A07_01/A07_02 只在受控 rank-one 表面支持 common backbone 与显式控制效果；
它们不是“MTP 自动完成这种控制”的证据。

## 8. 现实任务中的直观意义

在位置 $t$：

- NTP 要求状态支持一个紧邻条件预测；
- MTP 要求同一个状态同时满足多个未来约束。

当表征容量有限时，MTP 可能迫使状态更早概括一个能够共同解释多个未来输出的
潜变量。

目前最强但仍安全的直观表述是：

> **MTP 可以把有用的未来约束提前到当前计算位置。**

不能直接说：

- MTP 学会了多步推理；
- MTP 保持了中间状态；
- MTP 主头使用了该状态；
- MTP 因而更适合代码或规划。

这些都需要独立 gate。

## 9. NTP 主头利用 MTP 信息的必要条件

如果我们要声称“是 MTP 新增的未来信息导致普通主头受益”，至少需要：

1. **条件新颖性**：未来目标包含 matched next-token 目标没有的任务相关信息。
2. **共享可达性**：auxiliary 梯度改变了普通主头可以访问的共享参数。
3. **状态形成**：相关潜变量确实改变共享状态。
4. **保持或运输**：该变化到达真正作出决策的位置。
5. **读出敏感性**：普通主头输出依赖该状态分量。
6. **目标一致性**：这种依赖降低正确测试分布上的风险。
7. **结构必要性**：若要声称“必要使用”，移除该分量后行为必须受损，且
   bypass/shortcut 已被控制。

注意：条件新颖性不是“一般正则化收益”的必要条件；它是“额外 MTP 信息造成
收益”这一更强因果主张的必要条件。

## 10. 初步结论与边界

在显式假设下已经得到：

- MTP 增加 horizon-specific 梯度，但其与 NTP 梯度没有固定对齐符号；
- MTP 本身不会自动重加权 common/rare 目标频率；
- 在两模式二次模型中，MTP 相对帮助 rare 的充要条件就是 horizon 曲率比条件。

尚未得到：

- 真实神经网络中的相同动力学；
- 代码/规划的 causal effect；
- 长上下文价值；
- 普通主头因果使用；
- 表征解耦；
- Router 效用。

本文件原先提出的“两模式相对学习率”决定已降为背景问题。当前唯一下一决定改为
[Thinking Card](03_mtp_mainline_thinking_card_cn.md) 中的同点 matched
rare-loss 一步问题。
