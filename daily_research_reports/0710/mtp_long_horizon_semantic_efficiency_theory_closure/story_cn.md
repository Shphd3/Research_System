# A11：MTP 长程语义效率的理论闭环

文档状态：2026-07-10 理论闭环 story。  
研究线：`11_long_horizon_mtp_objective`。  
边界：受控目标函数机制线；不进入 MoE bridge；不声称自然语言收益；不声称 $K$ 越大越好；不声称一阶速度已经自动推出有限步效率。

## 0. 术语解释

| 术语 | 中文含义 | 具体对象或公式 | 为什么影响判断 | 不能证明什么 |
|---|---|---|---|---|
| 多词元预测目标（MTP） | 同一个当前隐藏状态预测多个未来词元 | $L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j)$ | 判断远处目标是否直接监督当前状态 | $K$ 越大一定越好 |
| 下一词预测目标（NTP） | 当前隐藏状态只预测下一个词元 | $L_1(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),Y_1)$ | 非覆盖对照 | NTP 永远学不到长程信息 |
| 早期语义变量 $Z$ | 前缀中已经存在、未来才显现的信息 | 受控数据中的分支身份，$Z\in\{1,\ldots,m\}$ | A11 的长程变量代理 | 自然语言全部语义 |
| 当前隐藏状态 $h_T$ | 决策前缀后的状态 | $h_z=h_T(Z=z)$ | 判断 $Z$ 是否被写入的对象 | 所有位置的状态 |
| 第一个有信息未来位置 $\tau$ | 第一个新增 $Z$ 信息的未来偏移 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | 决定 $K$ 是否覆盖有效监督 | 真实文本中固定唯一位置 |
| 有信息未来位置 | 未来目标中含有关于 $Z$ 的新信息 | $j\in\mathcal I_K$ | 只有这类位置贡献直接语义速度 | 所有未来词都有用 |
| 中心化输出方向 | 去掉分支共享成分后的 token 输出行方向 | $u_{j,z}-\bar u_j$ | 决定梯度是否沿可读出语义方向推动 $h_z$ | 下游效用 |
| 读出有效语义 margin | $h_z$ 是否朝正确未来 token 输出方向移动 | $M(h)=m^{-1}\sum_z v_z^\top h_z$ | 一阶效率的核心量 | 有限步收敛 |
| 一阶语义速度 | 损失梯度对语义 margin 的瞬时推动 | $G_K=m^{-1}\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K)$ | 判断目标函数是否直接推向语义方向 | 长期训练优势 |
| 语义恢复分数 $Q$ | 保守的可读性分数 | $Q(t)=\min\{A(t),P(t),S(t)\}$ | 防止只看 probe 假阳性 | 直接监督来源 |
| native H3 accuracy | 模型自身第三未来位置预测 $S_Z$ 的准确率 | $\Pr[\arg\max q_3(\cdot\mid h_T)=S_Z]$ | 区分模型自身读出与外部探针可读 | 下游任务收益 |
| 有限步 hitting time | 指标达到阈值所需训练步数 | $T_\gamma=\inf\{t:M(t)\ge\gamma\}$ | 学习效率目标 | 一阶局部结论本身 |

## 1. 研究问题

A11 的问题是：多词元预测目标是否能比只预测下一词的目标更直接地让当前隐藏状态 $h_T$ 保留未来才会用到的变量 $Z$。

当前稳定答案分四层：

1. **表示保证。** 如果 $K$ 覆盖第一个有信息未来位置 $\tau$，且该位置目标 $Y_\tau=S_Z$ 一一编码 $Z$，低 $Y_\tau$ loss 会强迫 $h_T$ 含有 $Z$。
2. **一阶语义速度。** 在分支折叠初始化和固定输出方向下，覆盖有信息未来位置会给 $h_T$ 正的读出有效语义速度，非覆盖位置只给公共更新。
3. **general K 向量和。** 多个有信息未来位置不是按 $K$ 大小简单叠加，而是按中心化输出方向的向量和决定。
4. **有限步效率缺口。** 当前还没有从 $G_K^{hidden}>0$ 严格推出 $T_\gamma(K)$ 更小；需要额外优化假设和最小实验验证。

## 2. 数据构造

### 2.1 K=2 最小理论基元

早期变量 $Z\in\{1,\ldots,m\}$ 均匀分布。当前状态在决策前缀后形成：

$$
h_z=h_T(Z=z).
$$

未来两个目标是：

$$
Y_1=A,\qquad Y_2=S_Z.
$$

其中 $A$ 对所有分支共享，$Z\mapsto S_Z$ 一一对应。信息结构是：

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=H(Z).
$$

这说明 next-one 在当前 $h_T$ 上只看共享目标 $A$；next-two 才第一次把关于 $Z$ 的目标 $S_Z$ 放到同一个 $h_T$ 的损失里。K=2 因此是最小理论基元。

### 2.2 $\tau=m$ first-informative-horizon 构造

推广到第 $m$ 个未来位置第一次含有 $Z$ 的情形：

$$
I(Z;Y_j\mid Y_{<j})=0,\qquad j<m,
$$

$$
Y_m=S_Z.
$$

前 $m-1$ 个未来目标可以被不区分 $Z$ 的状态解决；第 $m$ 个未来目标一一编码 $Z$。因此只有 $K\ge m$ 时，当前 $h_T$ 才包含直接语义监督项。

### 2.3 general K 构造

一般情况下，多个未来位置可能含有关于 $Z$ 的新信息。定义：

$$
\mathcal I_K=\{j\le K:Y_j\text{ contains new information about }Z\}.
$$

对每个 $j\in\mathcal I_K$，第 $j$ 个预测头中正确 token 的输出行为 $u_{j,z}$，分支均值为：

$$
\bar u_j=\frac1m\sum_z u_{j,z}.
$$

中心化加权方向是：

$$
a_{j,z}=\lambda_j(u_{j,z}-\bar u_j).
$$

general K 的合成语义方向是：

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}a_{j,z}.
$$

这才是 $K$ 的一阶语义效率对象。$K$ 变大本身不是机制；新增位置是否含有新信息、方向是否对齐才是机制。

## 3. 表示保证

表示保证回答“低未来词 loss 是否强迫当前状态含有 $Z$”。若 $K\ge\tau$、$Y_\tau=S_Z$ 且 $Z\mapsto S_Z$ 一一对应，如果：

$$
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon,
$$

则：

$$
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

含义是：如果当前状态能低损失预测一一编码 $Z$ 的未来 token，它就不能对 $Z$ 盲。该结论是表示层结论，不是训练速度结论。

## 4. 一阶语义速度定理

### 4.1 K=2 最小基元

对 K=2 数据：

$$
Y_1=A,\qquad Y_2=S_Z.
$$

定义第 2 未来位置的正确输出行：

$$
u_z=u_{S_z}^{(2)},\qquad \bar u=\frac1m\sum_z u_z.
$$

第 2 位置读出 margin 定义为：

$$
M_Z^{(2)}(h)=\frac1m\sum_z(u_z-\bar u)^\top h_z.
$$

假设分支折叠初始化：

$$
h_1(0)=\cdots=h_m(0)=h_0.
$$

K1 损失只含共享目标 $A$，所以所有分支的 $h_z$ 得到相同速度 $b$。因此：

$$
G_1^{margin}=\frac1m\sum_z(u_z-\bar u)^\top b=0.
$$

K2 的有信息项是：

$$
L_2^{info}=\frac{\lambda_2}{m}\sum_z-\log q_2(S_z\mid h_z).
$$

在折叠点，令 $p=\operatorname{softmax}(U_2h_0)$。梯度流速度为：

$$
\dot h_z=-\nabla_{h_z}L_2^{info}=\frac{\lambda_2}{m}(u_z-U_2^\top p).
$$

代入 margin 导数：

$$
G_2^{margin}=\frac1m\sum_z(u_z-\bar u)^\top\frac{\lambda_2}{m}(u_z-U_2^\top p).
$$

公共项 $U_2^\top p$ 被中心化消去，得到：

$$
G_2^{margin}=\frac{\lambda_2}{m^2}\sum_z\|u_z-\bar u\|^2>0,
$$

只要 $u_z$ 不全相同。结论：K=2 是最小基元，因为它第一次给当前 $h_T$ 直接语义速度。

### 4.2 $\tau=m$ 覆盖定理

在 $\tau=m$ 构造中：

$$
I(Z;Y_j\mid Y_{<j})=0,\qquad j<m,
$$

$$
Y_m=S_Z.
$$

若 $K<m$，所有 active targets $Y_1,\ldots,Y_K$ 都不含关于 $Z$ 的新信息。在分支折叠点，损失对每个分支给出相同更新；任何中心化语义 margin 的一阶导数为 0。因此 $K<m$ 没有直接语义速度。

若 $K\ge m$，损失中出现：

$$
\lambda_m\operatorname{CE}(q_m(\cdot\mid h_T),S_Z).
$$

对第 $m$ 位置输出行 $u_z^{(m)}=u_{S_z}^{(m)}$，同样得到：

$$
G_m^{margin}=\frac{\lambda_m}{m^2}\sum_z\|u_z^{(m)}-\bar u^{(m)}\|^2>0.
$$

这就是 first-informative-horizon law：语义速度在 $K$ 第一次覆盖有信息未来位置时打开。

### 4.3 general K vector-sum theorem

定义：

$$
\mathcal I_K=\{j\le K:Y_j\text{ contains new information about }Z\},
$$

$$
a_{j,z}=\lambda_j(u_{j,z}-\bar u_j),
$$

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}a_{j,z}.
$$

general K 读出 margin 是：

$$
M_K(h)=\frac1m\sum_z v_z^{(K)\top}h_z.
$$

在分支折叠初始化、固定输出头、一步梯度流分析下：

$$
G_K=\left.\frac{d}{ds}M_K(h(s))\right|_{s=0}
=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2.
$$

若新增一个有信息 horizon $r$，其方向为 $a_{r,z}$，则：

$$
G_{K\cup r}-G_K
=\frac1{m^2}\sum_z(2v_z^{(K)\top}a_{r,z}+\|a_{r,z}\|^2).
$$

解释：

1. 新增无信息 horizon 不改变 $\mathcal I_K$，因此不带来直接语义增量。
2. 新增 aligned informative horizon 时，$2v_z^{(K)\top}a_{r,z}$ 为正，速度增强。
3. 新增 low/conflict informative horizon 时，内积项可能很小或为负，速度可能削弱。
4. 因此不是 $K$ 越大越好；真正对象是有信息 horizon 的中心化读出方向向量和。

## 5. next-K inclusion law

next-K inclusion law 是 general K 定理的动态读法：当 $K$ 从小到大增加时，语义速度只通过新纳入的有信息未来位置改变。

在 clean decision-only、frozen-head 条件中，当前证据支持以下模式：

| 情形 | 预测 | 稳定解释 |
|---|---|---|
| $K$ 未覆盖有信息位置 | $G_K\approx0$ | 当前 $h_T$ 没有直接 $Z$ 监督 |
| $K$ 第一次覆盖 $S_Z$ | $G_K>0$ | 语义速度打开 |
| 新增共享未来词 | $G$ 无直接增量 | 只是多一个无信息目标 |
| 新增对齐有信息词 | $G$ 增大 | 中心化方向向量和增强 |
| 新增冲突有信息词 | $G$ 减小或弱增 | 中心化方向抵消 |

这条规律把 A11 从“覆盖 $\tau$ 才有直接监督”推广到“增加 $K$ 的效果由新增有信息方向决定”。

## 6. 有限步效率缺口

当前已经支持的是一阶速度：

$$
G_K^{hidden}>0.
$$

尚未证明的是有限步学习效率：

$$
G_K^{hidden}>0
\quad\Rightarrow\quad
T_\gamma(K)\text{ 更小}.
$$

这一步不能直接从一阶导数推出，因为训练中可能出现四类变化：

1. 语义速度可能只在 step 0 为正，随后消失。
2. 输出头可能漂移，导致参考 margin 不再对应当前模型读出。
3. 全位置训练中的 shared / indirect loss 可能给 margin 带来负向扰动。
4. margin 变大未必足够预测 native H3 accuracy 或 $Q$ 阈值跨越。

## 7. 有限步效率定理候选

定义参考语义 margin：

$$
M_K(t)=\frac1m\sum_z v_z^{ref\top}h_z(t).
$$

定义 hitting time：

$$
T_\gamma(K)=\inf\{t:M_K(t)\ge\gamma\}.
$$

一个可尝试证明的条件命题是：如果在 $t<T_\gamma(K)$ 的早期窗口内存在常数 $g_K>0$、$B\ge0$ 和扰动上界 $\bar\epsilon\ge0$，使得：

$$
M_K(t+1)\ge M_K(t)+\eta g_K-\eta^2B-\epsilon_t,
$$

且：

$$
\epsilon_t\le\bar\epsilon,
$$

并且净增量为正：

$$
\eta g_K-\eta^2B-\bar\epsilon>0,
$$

则：

$$
T_\gamma(K)
\le
\left\lceil
\frac{\gamma-M_K(0)}
{\eta g_K-\eta^2B-\bar\epsilon}
\right\rceil.
$$

证明只需要把每步下界累加：

$$
M_K(t)\ge M_K(0)+t(\eta g_K-\eta^2B-\bar\epsilon).
$$

当右侧达到 $\gamma$ 时，得到上述 hitting-time bound。

这个命题本身不是 A11 已经完成的定理。它把需要证明或实验验证的假设暴露出来。

### 7.1 已证明

1. K=2 最小基元：$Y_1=A,Y_2=S_Z$ 时，K2 给 $h_T$ 直接语义速度，K1 没有。
2. $\tau=m$ 覆盖规律：$K<m$ 没有直接语义速度，$K\ge m$ 时速度打开。
3. general K 一阶公式：在分支折叠、固定输出头、一步分析中，$G_K=m^{-2}\sum_z\|v_z^{(K)}\|^2$。
4. 新增有信息 horizon 的一阶增量公式：$m^{-2}\sum_z(2v_z^\top a_z+\|a_z\|^2)$。

### 7.2 需要作为假设

1. **velocity persistence：** 早期窗口中 $G_K^{hidden}(t)$ 保持正下界，而不是只在 step 0 为正。
2. **局部平滑误差：** 离散更新的二阶项可由 $\eta^2B$ 上界。
3. **head drift bound：** 参考输出方向与当前输出方向保持正相关，或 reference theorem 按漂移收缩。
4. **shared / indirect perturbation bound：** 全位置训练中非直接 loss 对 $M_K$ 的负向贡献有上界 $\epsilon_t$。
5. **margin-to-recovery calibration：** 当 $M_K(t)$ 达到阈值 $\gamma$ 时，native H3 accuracy 或 $Q(t)$ 会跨越相应阈值。

### 7.3 需要实验验证

A11_10 的最小实验应验证：

1. $G_K^{hidden}(t)$ 是否在早期窗口保持正下界。
2. $M_K(t)$ 是否预测 native H3 accuracy 或 $Q(t)$ 的阈值跨越。
3. current output direction 与 reference output direction 是否保持正相关。
4. shared / indirect loss 是否给 $M_K$ 带来可界定的负向扰动。

### 7.4 不能写成定理的内容

1. 不能写成“$G_K^{hidden}>0$ 自动推出所有训练设置下 $T_\gamma$ 更小”。
2. 不能写成“全位置训练中非覆盖 K 不能恢复 $Z$”。
3. 不能写成“自然语言中 MTP 已经更高效”。
4. 不能写成“MoE 路由保持或专家效用已经由 A11 证明”。

## 8. 当前实验证据

| Anchor | 已支持内容 | 对 A11_10 的作用 |
|---|---|---|
| 11_01 | K=2 branch-delayed next-two 让 $h_T$ 支持 $S_Z$，next-one 不需要 | 最小表示基元 |
| 11_04 | $\tau=3$ 时 K3 覆盖 first informative horizon，K1/K2 不覆盖 | 覆盖律证据 |
| 11_06 | K3 的 $G_M^{hidden}=0.003816$，K1/K2 近 0；step-0 无泄漏 | 一阶速度证据 |
| 11_07 | direct 条件 native H3 和 $M_Z^{ref}$ 强；K1/K2 仍可通过 indirect transfer 有非平凡 $Q$ | 说明 $Q$ 不能单独证明 direct path |
| 11_08 | 同样 K=4 和同样两个有信息 horizon 下，aligned $G=0.015262$，low/conflict $G=0.000954$ | general K 向量和证据 |
| 11_08b | frozen heads 下 aligned 仍有更大早期 $G_{hidden}^{ref}$；trainable heads 会漂移 | head drift 是 A11_10 必要假设 |
| 11_09 | K2 为 0，K3 打开，shared H4 无增量，aligned H4 增强，low/conflict H4 削弱 | next-K inclusion law 证据 |

## 9. Claim boundary

可以说：

1. 在受控构造中，MTP 覆盖 first informative horizon 时给当前 $h_T$ 直接语义监督。
2. 低 $Y_\tau=S_Z$ loss 推出 $h_T$ 含有 $Z$。
3. 在分支折叠、固定输出方向的一阶模型中，覆盖有信息 horizon 产生正的读出有效语义速度。
4. general K 的一阶速度由中心化输出方向向量和决定，不由 $K$ 大小单独决定。
5. A11_09 已支持 next-K inclusion law：新增无信息 horizon 无直接增量，对齐有信息 horizon 增强，冲突有信息 horizon 可削弱。

不能说：

1. MTP 在自然语言中已经优于 NTP。
2. NTP 或非覆盖 K 不能通过全位置训练恢复 $Z$。
3. $K$ 越大越好。
4. $Q$ 单独证明 direct supervision。
5. 一阶语义速度已经自动推出有限步 hitting-time 优势。
6. A11 已证明 MoE 路由保持或专家效用。

## 10. 下一步理论问题

A11_10 的核心问题是：

> 在哪些可检验优化假设下，一阶语义速度 $G_K^{hidden}>0$ 可以推出有限步 semantic margin hitting-time bound，并且该 margin 阈值是否能预测 native H3 accuracy 或 $Q$ 的恢复阈值？

最小下一步只做 A11 内部理论闭环：验证 velocity persistence、margin-to-recovery calibration、head drift bound、shared / indirect perturbation bound。不要进入 MoE bridge，不要做 broad ablation。