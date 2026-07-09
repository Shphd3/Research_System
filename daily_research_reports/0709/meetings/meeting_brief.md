# MTP 是否更高效地学习长程语义信息

## 0. 执行摘要

**研究问题：** 多词元预测（multi-token prediction, MTP）是否比下一词元预测（next-token prediction, NTP）更高效地让当前隐藏状态学到长程语义变量。这里“长程语义变量”指：早期出现在前缀中、但要到未来某个词元才第一次影响输出的变量，记为 $Z$。

**机制解释：** 我们使用一个受控构造：

$$
Y_1=A_{shared},\qquad Y_2=C_{shared},\qquad Y_3=S_Z.
$$

其中 $A_{shared}$ 和 $C_{shared}$ 对所有分支相同，不含 $Z$ 信息；$S_Z$ 是 $Z$ 的一一编码。因此：

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

MTP 的 K 步目标是：

$$
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j),
$$

其中 $h_T$ 是读完决策前缀后的当前隐藏状态，$q_j$ 是第 $j$ 个未来位置的预测头，$\operatorname{CE}$ 是交叉熵损失。

当 $K=1$ 或 $K=2$ 时，目标没有覆盖 $Y_3=S_Z$；当 $K=3$ 时，目标包含直接项：

$$
L_{direct}=\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z).
$$

这个项把远处语义变量 $Z$ 的预测误差直接作用到当前状态 $h_T$。

**主要结果：**

1. **表示定理：** 如果第 $\tau$ 个未来词元 $Y_\tau=S_Z$ 一一编码 $Z$，且 MTP 覆盖该位置并预测得足够好：

$$
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon,
$$

则当前状态必须含有 $Z$ 信息：

$$
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

这说明 MTP 的低有信息未来位置损失会强制 $h_T$ 包含长程语义信息；NTP 在同一前缀上只预测共享的 $Y_1$，没有这个表示要求。

2. **一阶效率定理：** 表示定理还不说明“学得更快”。因此我们定义读出有效语义边距：

$$
M_Z(h)=\frac1m\sum_z(u_{S_z}-\bar u)^\top h_z.
$$

这里 $h_z$ 是分支 $z$ 的当前状态，$u_{S_z}$ 是预测正确未来 token $S_z$ 的输出方向，$\bar u$ 是这些输出方向的均值。$M_Z$ 变大表示 $h_z$ 正沿着“能预测正确 $S_z$”的方向移动。

在分支初始不可区分、且 $Y_1,Y_2$ 共享、$Y_3=S_Z$ 的设置下，可以证明：

$$
G_1^{margin}=0,\qquad G_2^{margin}=0,
$$

但：

$$
G_3^{margin}=\frac{\lambda_3}{m^2}\sum_z\|u_{S_z}-\bar u\|^2>0.
$$

这说明 K3 不只是最终强制表示 $Z$，而是在训练一开始就给 $h_T$ 一个 NTP/K2 没有的读出有效语义更新方向。

3. **一般 K 推进：** 对多个有信息未来位置，定义：

$$
\mathcal I_K=\{j\le K:I(Z;Y_j\mid Y_{<j})>0\}.
$$

一般 K 的一阶边距速度为：

$$
G_K=\frac1{m^2}\sum_z\left\|\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)\right\|^2.
$$

所以结论不是“K 越大越好”，而是：新增 future horizon 只有在含有 $Z$ 信息并且读出方向与已有语义方向对齐时，才会增强学习效率。

**实验说明：**

1. A11_06 在决策前缀隔离实验中验证一阶机制：K3 的隐藏状态读出边距速度为 `0.003816`，K1/K2 近似为 `0`，且 step-0 无泄漏。
2. A11_07 在无泄漏全位置训练中验证多步边界：K3 full 和 K2 plus direct L3 都达到 `reach=1.00`、最终 $Q=1.00$、模型自身第三步预测准确率 `1.00`；K1/K2 和 masked K3 也能通过间接迁移恢复部分 $Q$，但 native H3 和 $M_Z$ 接近 0。
3. 因此，$Q$ 只能说明 $Z$ 可恢复；要证明直接监督路径，需要同时看模型自身第三步预测准确率和读出有效边距 $M_Z$。

**结论边界：** 当前可以声称：在受控长程构造中，覆盖第一个有信息未来词的 MTP 提供 NTP 没有的直接表示要求和一阶读出有效更新方向。不能声称：自然语言中 MTP 已经优于 NTP、K 越大越好、NTP 学不到长程语义、或者该结果已经推出 MoE 路由收益。

**执行动作：** 先不要桥接 MoE，也不要直接扩自然语言。下一步应沿两个理论方向推进：第一，验证一般 K 的方向对齐公式；第二，解释 all-position 中非覆盖条件的间接迁移来源。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|
| 多词元预测（MTP） | 一个当前隐藏状态预测多个未来词元 | $L_K=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j,Y_j)$ | 决定是否覆盖远处语义目标 | K 越大一定越好 |
| 下一词元预测（NTP） | 当前隐藏状态只预测下一个词元 | $L_1=\operatorname{CE}(q_1,Y_1)$ | 基线 | NTP 永远学不到长程信息 |
| 长程语义变量 $Z$ | 早期出现、未来才需要的信息 | 受控数据中是 branch id | 被写入 $h_T$ 的目标变量 | 自然语言语义全部情况 |
| 当前隐藏状态 $h_T$ | 决策前缀后的隐藏向量 | $h_T=f_\theta(X_{\le T})$ | 检查当前状态是否含 $Z$ | 后续状态的信息 |
| 第一个有信息未来位置 $\tau$ | 第一个新增 $Z$ 信息的未来位置 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | 决定 MTP 是否有直接监督 | 真实文本固定为某个 K |
| 直接语义监督 | 当前 $h_T$ 直接预测 $S_Z$ | $\operatorname{CE}(q_\tau(\cdot\mid h_T),S_Z)$ | 最短信用分配路径 | 唯一恢复路径 |
| 读出有效语义边距 $M_Z$ | $h_T$ 是否朝正确未来 token 输出方向移动 | $M_Z=\frac1m\sum_z(u_{S_z}-\bar u)^\top h_z$ | 一阶效率理论量 | 多步收敛必然成立 |
| 语义恢复分数 $Q$ | 同时要求预测、探针、分支替换通过 | $Q=\min\{A,P,S\}$ | 保守恢复指标 | 直接监督路径成立 |
| 模型自身第三步预测准确率 | 模型自己从 $h_T$ 预测 $S_Z$ 的准确率 | $\Pr[\arg\max q_3(\cdot\mid h_T)=S_Z]$ | 区分 direct prediction 和 probe-readable recovery | 下游效用 |
| 间接迁移 | 其他位置 loss 通过共享参数影响 $h_T$ | all-position 中的非直接路径 | 解释 K1/K2 也能恢复 $Q$ | 直接项无效 |
| 局部守卫 | 近端共享目标是否被破坏 | $Y_1/Y_2$ loss 和 accuracy | 排除牺牲本地学习换长程恢复 | 全局 LM 质量 |

## 2. 机制解释

最小直觉是：

> NTP 只问当前状态“下一个词是什么”；如果下一个词不需要 $Z$，它没有理由立刻把 $Z$ 写进当前状态。MTP 如果覆盖到未来第一个需要 $Z$ 的词，就会把这个远处误差直接打到当前状态。

在 clean $\tau=3$ 构造中：

$$
Y_1=A_{shared},\qquad Y_2=C_{shared},\qquad Y_3=S_Z.
$$

K1 和 K2 的直接目标都是共享目标；K3 第一次看到 $S_Z$。因此 K3 的目标函数里多出：

$$
\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z).
$$

这个项的梯度会把 $h_T(z)$ 推向 $S_z$ 的输出方向。

## 3. 主要结果

### 结果 1：旧理论证明的是“表示要求”

如果 MTP 覆盖到有信息未来位置 $\tau$，并且模型从当前状态 $h_T$ 预测 $S_Z$ 的损失很低：

$$
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon,
$$

那么交叉熵上界条件熵：

$$
H(S_Z\mid h_T)\le\varepsilon.
$$

因为 $Z\mapsto S_Z$ 一一对应，所以：

$$
I(h_T;Z)=H(Z)-H(Z\mid h_T)\ge H(Z)-\varepsilon.
$$

这证明的是：低 MTP 有信息位置损失会强制 $h_T$ 含有长程变量。实验上，K=2/K=3 受控构造已经验证了这个机制。

### 结果 2：新理论证明的是“一阶效率方向”

表示要求还不是学习效率。新的量是读出有效语义边距：

$$
M_Z(h)=\frac1m\sum_z(u_{S_z}-\bar u)^\top h_z.
$$

它问：训练一开始，$h_z$ 是否朝正确未来 token $S_z$ 的输出方向移动。

在分支初始折叠、$Y_1,Y_2$ 共享、$Y_3=S_Z$ 的最小模型中：

$$
G_1^{margin}=0,\qquad G_2^{margin}=0,\qquad G_3^{margin}>0.
$$

A11_06 验证了这个方向：K3 的隐藏状态 margin 速度为 `0.003816`，K1/K2 近似为 `0`。

### 结果 3：全位置训练中直接项更强，但间接迁移存在

A11_07 显示：

- K3 full 和 K2 plus direct L3 都达到 `reach=1.00`、final $Q=1.00$、native H3 `1.00`；
- K1/K2 和 masked K3 仍有非平凡 $Q$，但 native H3 和 $M_Z$ 接近 0。

解释：全位置训练可以通过共享参数让 $Z$ 对 probe 可读；但直接 $h_T\to S_Z$ 监督才稳定地产生模型自身第三步预测和读出有效边距。

### 结果 4：一般 K 的推进点

对多个有信息未来位置，定义：

$$
\mathcal I_K=\{j\le K:I(Z;Y_j\mid Y_{<j})>0\}.
$$

一般 K 的一阶语义速度是：

$$
G_K=\frac1{m^2}\sum_z\left\|\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)\right\|^2.
$$

因此：

1. 未覆盖任何有信息位置时，$G_K=0$；
2. 覆盖有信息位置且方向不抵消时，$G_K>0$；
3. 新增 K 是否有用，取决于新 horizon 的语义方向是否与已有方向对齐。

这给出下一阶段理论主线：研究一般 K 的方向对齐、间接迁移和 hitting time，而不是简单扩大 K。

## 4. 下一步判定卡

### 4.1 11_08：一般 K 读出 margin 动力学

问题：一般 K 下，新增有信息未来位置是否按理论公式增加读出有效 margin 速度？

主指标：

$$
\Delta M_K/\eta.
$$

关键对照：

```text
shared horizon
aligned informative horizon
orthogonal / weakly aligned horizon
conflicting informative horizon
noisy horizon
```

通过条件：观测到的 $\Delta M_K/\eta$ 与理论预测：

$$
G_K=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2
$$

一致。

### 4.2 11_09：全位置间接迁移动力学

问题：all-position 中 K1/K2 为什么也能恢复 probe-readable $Z$？

建模：

$$
L_K^{all}=L_{direct}+L_{indirect}+L_{shared}.
$$

其他位置 $s$ 的 loss 对当前 $h_T$ 的影响由跨位置参数核决定：

$$
\dot h_T^{(s)}=-J_TJ_s^\top\nabla_{h_s}\ell_s.
$$

主指标：位置分组 loss 的有限差分贡献：

```text
Delta M_Z
Delta E_Z
Delta Q
Delta native H3
Delta local CE
```

通过条件：能解释 non-direct 条件的 $Q$ 恢复来自哪些间接位置，同时确认 direct 条件仍然最稳定地产生 native H3 和 $M_Z$。

## 5. 当前结论边界

可以说：

```text
在受控长程语义构造中，MTP 覆盖第一个有信息未来词时，会给当前 h_T 一个 NTP 没有的直接表示要求和一阶读出有效更新方向。一般 K 的收益取决于有信息未来位置的读出方向是否对齐。
```

不能说：

```text
MTP 已经在自然语言中证明优于 NTP。
NTP 学不到长程变量。
K 越大越好。
Q 高就等于 direct supervision。
A11 已经推出 MoE 路由收益。
```

## 6. 执行动作

当前建议：

```text
先做 11_08，再做 11_09。
```

不要立刻桥接 MoE。因为我们还需要先回答：一般 K 的语义方向什么时候增强，all-position 的间接迁移到底从哪里来。

## 7. 证据索引

| 结果 | 证据 | 支持什么 | 不能证明什么 |
|---|---|---|---|
| 表示定理 | K=2/K=3 受控证明与实验 | 低有信息 future loss 强迫 $h_T$ 含 $Z$ | 学习速度 |
| A11_06 | `A11_06_readout_effective_margin_efficiency/summary.md` | K3 有一阶读出 margin 速度 | 全位置效率 |
| A11_07 | `A11_07_no_leakage_all_position_efficiency/summary.md` | direct 条件更强，间接迁移存在 | 自然语言收益 |
| 0709 story | `daily_research_reports/0709/mtp_generalized_efficiency_story/story_cn.md` | 一般 K 理论与下一步 anchors | project-local source of truth |
