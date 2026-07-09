# 多词元预测如何更高效地学习长程语义信息

文档状态：
- 类型：研究线级 story，当前版本为理论 + 实验更新版
- 研究线：`11_long_horizon_mtp_objective`
- 语言：中文
- 写作模式：综合 + 下一阶段前瞻
- 当前核心变化：从“表示存在定理”推进到“一阶读出有效语义速度”的一般 K 向量和机制；11_06 / 11_07 验证 K=3 直接监督机制与全位置边界，A11_08 支持一般 K 的方向对齐规律

## 0. 术语约定

| 术语 / 缩写 | 中文含义 | 具体对象或公式 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 多词元预测（MTP） | 同一个当前隐藏状态预测多个未来词元 | $L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j)$ | 研究远处目标是否提前监督当前状态 | 不代表任何 K 都更好 |
| 下一词元预测（NTP） | 当前隐藏状态只预测下一个词元 | $L_1(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),Y_1)$ | 对照训练目标 | 不代表永远学不到长程信息 |
| 早期语义变量 $Z$ | 前缀早期出现、未来才需要的信息 | 受控数据中是分支身份 | 长程语义信息的可控代理变量 | 自然语言全部语义 |
| 当前前缀状态 $h_T$ | 模型读完决策前缀后的隐藏状态 | $h_T=f_\theta(X_{\le T})$ | 判断 $Z$ 是否被写入的对象 | 后续所有状态的信息 |
| 第一个语义显现位置 $\tau$ | 第一个未来词元中新增 $Z$ 信息的位置 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | 决定 MTP 是否覆盖有效未来目标 | 真实文本中固定唯一位置 |
| 直接语义监督 | 当前 $h_T$ 直接预测含 $Z$ 的未来词元 | $\operatorname{CE}(q_\tau(\cdot\mid h_T),S_Z)$ | A11 的核心机制 | 全位置训练中的唯一通路 |
| 间接迁移 | 其他位置损失通过共享参数让 $h_T$ 可读出 $Z$ | 全位置训练中的背景更新 | 解释 K=1/K=2 也可能恢复 $Z$ | 否定直接语义监督 |
| 读出有效语义 margin | $h_T$ 是否沿着正确未来 token 的输出方向移动 | $M_Z=\frac1m\sum_z(u_{S_z}-\bar u)^\top h_z$ | 是新的效率理论量 | 多步收敛或自然语言收益 |
| 分支分离能量 | 不同分支隐藏状态是否分开 | $E_Z=\frac{1}{2m^2}\sum_{z,z'}\|h_z-h_{z'}\|^2$ | 对应 probe / route 可分性 | 信息是否被输出头使用 |
| 高恢复时间 | 达到可靠语义恢复阈值的训练步数 | $T_{0.9}=\inf\{t:Q(t)\ge0.9\text{ 连续评估成立}\}$ | 实验学习效率指标 | 一阶机制原因 |
| 保守恢复分数 $Q$ | 同时要求预测、探针、替换一致 | $Q=\min\{A,P,S\}$ | 防止 probe 假阳性 | 完整因果证明 |
| 有信息未来位置集合 $\mathcal I_K$ | 被 K 覆盖且含有 $Z$ 新信息的位置 | $\mathcal I_K=\{j\le K:I(Z;Y_j\mid Y_{<j})>0\}$ | 一般 K 的核心对象 | 位置越多一定越好 |
| 一般 K 合成语义方向 | 多个有信息未来位置的读出方向向量和 | $v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)$ | 决定当前状态的一阶语义更新方向 | 多步训练一定更快 |
| 隐藏状态语义速度 $G_K^{hidden}$ | 损失梯度把 $h_T$ 推向合成语义方向的速度 | $\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K)$ | A11_08 的主指标 | 参数空间长期收敛 |
| `aligned_h3_h4` | 第 3/4 未来位置都含 $Z$，且输出方向对齐 | `Y3=S_z,Y4=T_z`，第 4 位置中心化输出行与第 3 位置对齐 | 一般 K 正向叠加条件 | 自然语言中真实方向对齐 |
| `low_conflict_h3_h4` | 第 3/4 未来位置都含 $Z$，但输出方向低/冲突 | 同样 `Y3=S_z,Y4=T_z`，第 4 位置中心化输出行削弱第 3 位置方向 | 一般 K falsifier 条件 | K 更大一定无益 |

## 1. 摘要

A11 的原始问题是：MTP 是否比 NTP 更适合学习长程语义信息。现有 K=2 / K=3 结果已经证明了一个表示层结论：如果 MTP 的预测范围 $K$ 覆盖第一个语义显现位置 $\tau$，且 $Y_\tau=S_Z$ 一一编码早期变量 $Z$，那么低第 $\tau$ 个未来位置损失会推出当前状态 $h_T$ 含有 $Z$。这说明 MTP 有 NTP 在同一前缀上没有的直接表示约束。

但这还不是学习效率结论。新的理论推进是定义一个更接近“训练早期变快”的量：读出有效语义 margin。它衡量的不是 $h_T$ 最终是否含有 $Z$，而是训练一开始，目标函数的梯度是否把每个分支的 $h_T$ 朝正确未来 token $S_Z$ 的输出方向推动。

在最小 $\tau=3$ 构造 $Y_1=A, Y_2=C, Y_3=S_Z$ 中，可以证明：在分支隐藏状态初始相同的可训练前缀表示模型里，K=1 和 K=2 只产生分支无关的公共更新，对读出有效语义 margin 的一阶增长为 0；K=3 的第 3 未来位置损失产生严格正的一阶增长。这个定理把“更直接地学”推进到“在一个明确效率量上更快地学”。

现有 A11_05 表明，在无噪声 $\tau=3$ 全位置训练中，当前决策前缀上的第 3 位置监督是 K=3 速度优势的可测机制组件：给 K=2 加这个直接项几乎匹配完整 K=3，去掉 K=3 的这个直接项会变弱。但 A11_05 也暴露边界：随机初始化可能在第 0 步泄漏分支，且全位置训练存在间接迁移。

新的 11_06 / 11_07 已完成这个缺口。11_06 说明：在无泄漏、单决策前缀设置中，K=3 的隐藏状态一阶读出 margin 速度 $G_M^{hidden}$ 为正，K=1/K=2 近似为 0。11_07 说明：在无泄漏 all-position 训练中，直接 $h_T\to S_Z$ 监督让 native horizon-3 prediction、$M_Z^{ref}$、reach rate 和早期 AUC 更强；但 K=1/K=2 和 masked K3 仍能通过间接迁移让 $Z$ 对 probe 可读。因此当前 story 的边界必须更新为：$Q$ 只能说明 guarded recovery，不能单独证明 direct supervision；direct path 需要 native H3 和 $M_Z^{ref}$ 共同支持。

A11_08 把机制从 K=3 推广到一般 K。它固定 `K=4`、固定四个 active loss、固定两个有信息未来位置 `{3,4}`，只改变第 4 个有信息未来位置的中心化输出方向。结果支持向量和机制：`aligned_h3_h4` 的隐藏状态语义速度为 `0.015262`，`low_conflict_h3_h4` 为 `0.000954`，`5/5` 个 seed 都满足 aligned 大于 low/conflict；`shared_only_k4` 为 0，`single_h3` 为 `0.003816`。因此现在的结论不是“K 越大越好”，而是“K 覆盖的信息性未来位置，其读出方向是否形成有用向量和”。

## 2. 研究问题

主问题：

> 在长程语义学习上，MTP 相比 NTP 到底好在哪？

当前版本将它拆成四层：

1. **表示存在**：训练后 $h_T$ 是否含有 $Z$。
2. **目标函数结构优势**：MTP 是否把含 $Z$ 的未来词元损失直接加到 $h_T$。
3. **一阶优化速度优势**：训练早期，MTP 梯度是否更快把 $h_T$ 推向正确未来输出方向。
4. **多步训练效率优势**：实际训练中是否更小 $T_{0.9}$ 或更高早期 $Q$ 曲线面积。

A11 过去已经较好回答了第 1 和第 2 层。现在要推进第 3 层，并把第 4 层作为实验闭环。

## 3. 为什么旧 story 的后续实验需要微调

旧 story 把下一步设为“无泄漏全位置语义效率桥接”。这个实验仍然需要，但不应该作为第一步。原因是：

1. 全位置训练会引入间接迁移，容易把“当前前缀直接监督”与“其他位置共享参数更新”混在一起。
2. 随机初始化可能让 $Q(0)$ 已经很高，导致 $T_{0.9}$ 失去速度含义。
3. 即使全位置实验显示 K=3 更快，也还缺少一个紧贴目标函数的最小优化量来说明为什么更快。

因此，11_06 / 11_07 的结果应被读成一次 story 对照：

1. 旧 story 预期正确：覆盖 $\tau=3$ 的直接监督确实产生一阶读出 margin 优势。
2. 旧 story 的边界需要更尖锐：all-position 中的 $Q$ 恢复并不等价于直接语义监督，因为间接迁移可以制造 probe-readable recovery。

## 4. 数据和训练布局

### 4.1 K=2 最小构造

$$
X=(\operatorname{BR}_B,F_1,\ldots,F_L,U,A,S_B).
$$

当前状态：

$$
h_T^{(B)}=f_\theta(\operatorname{BR}_B,F_1,\ldots,F_L,U).
$$

未来词元：

$$
Y_1=A,\qquad Y_2=S_B.
$$

其中 $A$ 对所有分支共享，$B\mapsto S_B$ 一一对应。因此：

$$
I(B;Y_1)=0,\qquad I(B;Y_2\mid Y_1)=H(B).
$$

K=2 证明说明：next-one 可以用不区分 $B$ 的状态预测 $A$，但 next-two 的第 2 未来位置损失会惩罚这种状态。

### 4.2 K=3 第一个语义显现位置构造

$$
X=(\operatorname{BR}_Z,F_1,\ldots,F_L,U,A,C,S_Z).
$$

未来词元：

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

信息结构：

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

所以：

$$
\tau=3.
$$

K=1 和 K=2 不覆盖 $\tau$；K=3 覆盖 $\tau$。

### 4.3 单决策前缀训练与全位置训练

单决策前缀训练只在一个 $h_T$ 上计算：

$$
L_K(h_T)=\sum_{j=1}^K\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

它最适合理论隔离。

全位置训练计算：

$$
L_K^{all}=\sum_t\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j}).
$$

它更接近语言模型训练，但有间接迁移：即使当前决策前缀上的 K 没覆盖 $\tau$，其他位置损失也可能通过共享参数让 $h_T$ 可读出 $Z$。

## 5. 物理直觉

MTP 的优势不应讲成“预测更多 token 一定更好”。更准确的是：

> 当未来某个词元第一次需要早期语义变量 $Z$ 时，覆盖该位置的 MTP 会把这个远处语义误差提前加到当前状态 $h_T$ 上。

NTP 可以最终学到 $Z$，尤其在全位置训练中。但它在当前前缀上没有这个直接项。MTP 的可证明优势是监督路径更短；新的效率定理说明，这条更短路径在一个读出有效 margin 上产生严格正的一阶增长。

## 6. 数学模型

令 $Z\in\{1,\ldots,m\}$ 均匀分布。每个分支在决策前缀上有隐藏状态：

$$
h_z\in\mathbb R^d.
$$

这是最小可训练前缀表示模型。它可以看作 Transformer 当前状态 $h_T(z)$ 的局部化版本。

第 $j$ 个未来位置的预测头是线性 softmax：

$$
q_j(\cdot\mid h_z)=\operatorname{softmax}(U_j h_z).
$$

令 $u_y^{(j)}$ 表示 $U_j$ 中 token $y$ 对应的输出向量。对 $Y_3=S_z$，简写：

$$
u_z=u_{S_z}^{(3)},\qquad \bar u=\frac1m\sum_z u_z.
$$

初始化设为分支折叠：

$$
h_1(0)=h_2(0)=\cdots=h_m(0)=h_0.
$$

这对应“当前状态一开始不区分分支”。

训练损失采用分支平均：

$$
L_1=\frac1m\sum_z\operatorname{CE}(q_1(\cdot\mid h_z),A),
$$

$$
L_2=L_1+\frac{\lambda_2}{m}\sum_z\operatorname{CE}(q_2(\cdot\mid h_z),C),
$$

$$
L_3=L_2+\frac{\lambda_3}{m}\sum_z\operatorname{CE}(q_3(\cdot\mid h_z),S_z).
$$

## 7. 新效率量：读出有效语义 margin

定义：

$$
M_Z(h)=\frac1m\sum_{z=1}^m (u_z-\bar u)^\top h_z.
$$

含义：如果 $M_Z$ 变大，说明第 $z$ 个分支的隐藏状态 $h_z$ 正朝着正确未来 token $S_z$ 的输出方向移动。这个量比普通互信息更贴近学习效率，因为它看的是训练初期的方向，而不是训练完成后的存在性。

对应一阶效率量：

$$
G_K^{margin}(\theta_0)=\left.\frac{d}{ds}M_Z(h(s))\right|_{s=0},
\qquad \dot h_z=-\nabla_{h_z}L_K.
$$

## 8. 定理和证明状态

### 8.1 旧表示定理

若 $K\ge\tau$、$Y_\tau=S_Z$ 且 $Z\mapsto S_Z$ 一一对应，如果：

$$
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon,
$$

则：

$$
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

该定理说明低 MTP future loss 强迫 $h_T$ 含 $Z$，但不说明训练速度。

### 8.2 新定理：K=3 有严格一阶读出有效 margin 增长

**定理。** 在上述 $\tau=3$ 构造、分支折叠初始化、固定第 3 位置输出向量 $u_z$ 不全相同的条件下，梯度流满足：

$$
G_1^{margin}(\theta_0)=0,
$$

$$
G_2^{margin}(\theta_0)=0,
$$

但：

$$
G_3^{margin}(\theta_0)=\frac{\lambda_3}{m^2}\sum_{z=1}^m\|u_z-\bar u\|^2>0.
$$

**证明。** 对 K=1，目标 $Y_1=A$ 对所有分支相同。在分支折叠初始化下，$q_1(\cdot\mid h_z)$ 对所有 $z$ 相同，所以 $\nabla_{h_z}L_1$ 对所有 $z$ 相同。记公共速度为 $v$，则：

$$
\frac{d}{ds}M_Z=\frac1m\sum_z (u_z-\bar u)^\top v=\frac1m\left(\sum_z(u_z-\bar u)\right)^\top v=0.
$$

K=2 的新增目标 $Y_2=C$ 也对所有分支共享，因此新增更新仍是公共更新，同理：

$$
G_2^{margin}(\theta_0)=0.
$$

对 K=3，第 3 位置损失为：

$$
L_3^{info}=\frac{\lambda_3}{m}\sum_z -\log q_3(S_z\mid h_z).
$$

在折叠初始化下，令：

$$
p=\operatorname{softmax}(U_3h_0).
$$

对每个分支：

$$
\nabla_{h_z}L_3^{info}=\frac{\lambda_3}{m}(U_3^\top p-u_z).
$$

因此梯度流速度为：

$$
\dot h_z=-\nabla_{h_z}L_3^{info}=\frac{\lambda_3}{m}(u_z-U_3^\top p).
$$

代入 margin 导数：

$$
G_3^{margin}=\frac1m\sum_z (u_z-\bar u)^\top \frac{\lambda_3}{m}(u_z-U_3^\top p).
$$

公共项 $U_3^\top p$ 被消去，因为 $\sum_z(u_z-\bar u)=0$。所以：

$$
G_3^{margin}=\frac{\lambda_3}{m^2}\sum_z (u_z-\bar u)^\top u_z.
$$

又因为：

$$
\sum_z (u_z-\bar u)^\top u_z=\sum_z\|u_z-\bar u\|^2,
$$

得到：

$$
G_3^{margin}=\frac{\lambda_3}{m^2}\sum_z\|u_z-\bar u\|^2>0.
$$

证毕。

### 8.3 分支分离能量是二阶量

定义：

$$
E_Z(h)=\frac{1}{2m^2}\sum_{z,z'}\|h_z-h_{z'}\|^2.
$$

在折叠初始化下，$E_Z=0$，且一阶导数为 0。因此它不适合作为一阶效率主量。但一步梯度下降后：

$$
h_z^+=h_z-\eta\nabla_{h_z}L_K.
$$

K=1/K=2 仍然产生公共更新，所以：

$$
E_Z(h^+)=0.
$$

K=3 产生分支相关更新，因此：

$$
E_Z(h^+)=\frac{\eta^2\lambda_3^2}{2m^4}\sum_{z,z'}\|u_z-u_{z'}\|^2>0.
$$

这说明 K=3 在二阶意义上增加分支分离能量。该量更接近 probe / route 可分性，但不保证输出头会使用这些信息；因此它应作为辅助量。

### 8.4 一般 K 的向量和定理

令 $\mathcal I_K$ 是 K 覆盖到的有信息未来位置集合。对每个 $j\in\mathcal I_K$，定义：

$$
a_{j,z}=\lambda_j(u_{j,z}-\bar u_j),\qquad \bar u_j=\frac1m\sum_z u_{j,z}.
$$

一般 K 的合成语义方向为：

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}a_{j,z}.
$$

一般 K 的读出有效语义 margin 为：

$$
M_K(h)=\frac1m\sum_z v_z^{(K)\top}h_z.
$$

在分支折叠初始化和固定 head 的一步分析中：

$$
G_K=\left.\frac{d}{ds}M_K(h(s))\right|_{s=0}
=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2.
$$

因此，如果 $\mathcal I_K$ 为空，速度为 0；如果新增有信息未来位置 $r$，速度增量为：

$$
G_{K\cup r}-G_K
=\frac1{m^2}\sum_z\left(2v_z^{(K)\top}a_{r,z}+\|a_{r,z}\|^2\right).
$$

这个式子给出 A11_08 的核心判断：新增有信息未来位置是否帮助，取决于它与已有合成方向的内积，而不是取决于 K 本身变大。

### 8.5 推广到可训练编码器的条件

若 $h_z=f_\theta(X_{\le T}^{(z)})$，则梯度通过雅可比矩阵 $J_z=\partial h_z/\partial\theta$ 传回参数。上述结论需要一个可辨识性假设：分支 token 对编码器有可区分的参数通道，且 $J_zJ_z^\top$ 在 $\{u_z-\bar u\}$ 张成的方向上非退化。

如果所有分支在参数化上完全不可区分，即 $J_z=J_{z'}$ 且 $h_z=h_{z'}$ 永远由对称性锁死，那么任何目标函数都无法把分支分开。这不是 NTP/MTP 的问题，而是模型不可辨识。

## 9. 机制分解

| 机制环节 | 当前结论 | 主要量 | 当前证据 / 下一步 |
|---|---|---|---|
| 结构监督 | 覆盖 $\tau$ 才有直接语义目标 | $I(Z;Y_j\mid Y_{<j})$ | K=2/K=3 构造已支持 |
| 表示存在 | 低 $Y_\tau$ loss 推出 $h_T$ 含 $Z$ | $I(h_T;Z)$ 下界 | 旧定理已支持 |
| 一阶效率 | K=3 梯度使 $M_Z$ 严格增长，K=1/K=2 为 0 | $G_M^{hidden}$ | 11_06 支持：K3 为 0.003816，K1/K2 近似 0 |
| 一般 K 方向叠加 | 多个有信息未来位置按中心化输出方向向量和贡献速度 | $G_K^{hidden}$，$G_K^{pred}$ | A11_08 支持：aligned 0.015262，low/conflict 0.000954，5/5 seeds 同向 |
| 二阶可分性 | K=3 增加分支分离能量 | $E_Z$ 的速度 / 轨迹 | 11_06 辅助支持，K3 短曲线 $E_Z$ 增长 |
| 多步效率 | K=3 是否更小 $T_{0.9}$ / 更高 AUC | $Q(t),T_{0.9}$ | 11_07 支持 direct 条件更稳，但也显示 indirect transfer |
| 主线桥接 | MTP 写入的 $Z$ 是否有利于路由 | route margin / sign flip | 尚未开始，不应直接声称 |

## 10. Anchor 证据链

现有证据链应这样读：

1. 11_01 证明并验证 K=2 objective-level separation。
2. 11_02 说明第二未来词元必须含有新分支信息，且梯度冲突不等于有害。
3. 11_03 把 K=2 推到学习曲线，但稳定性不足。
4. 11_04 验证 first-informative-horizon，即 $\tau=3$ 时只有 K=3 在单决策前缀中直接覆盖 $S_Z$。
5. 11_05 在全位置训练中分离直接项与间接迁移，支持“当前决策前缀第 3 位置监督”是 K=3 优势的机制组件。
6. 11_06 验证新理论量：一阶读出有效 margin 增长。结果支持：K3 的 $G_M^{hidden}$ 为正，K1/K2 近似为 0。
7. 11_07 回到无泄漏全位置训练，判断该一阶优势是否转化为多步效率。结果支持 direct 条件更强，但同时确认 all-position indirect transfer 仍然存在。
8. 11_08 将 K=3 机制推广到一般 K：在同样 `K=4` 和同样两个有信息未来位置下，读出方向 aligned 与 low/conflict 会产生不同的一阶隐藏状态语义速度，结果支持向量和公式。

## 11. 实验结果整合

A11_05 的关键信息是：K=2 加当前决策前缀第 3 位置监督后，几乎匹配完整 K=3；K=3 去掉这个直接项后变弱。这说明直接语义监督不是抽象故事，而是全位置训练中可测的机制组件。

11_06 把理论效率量补上：在 step-0 无泄漏、单决策前缀设置中，$G_M^{hidden}$ 对 K=1/K=2 近似为 0，对 K=3 为 0.003816；短曲线中 K1/K2 的早期 AUC Q 为 0.250，K3 为 0.535。

11_07 把该机制放回 all-position：所有条件 $Q(0)=0.25$，不存在初始化饱和。direct 条件最强：K3 full reach rate 1.00、early AUC Q 0.965、final Q 1.00、native H3 1.00；K2 plus direct reach rate 1.00、early AUC Q 0.969、final Q 1.00、native H3 1.00。masked K3 和 K1/K2 也能有非平凡 $Q$，但 native H3 基本为 0，$M_Z^{ref}$ 也接近 0。

A11_08 的关键信息是：同样 `K=4`、同样两个有信息未来位置 `{3,4}`、同样 active loss 数量下，输出方向对齐会显著放大一阶语义速度，输出方向冲突会显著削弱该速度。主表是：

| 条件 | 几何预测速度 | 观测隐藏状态语义速度 |
|---|---:|---:|
| `shared_only_k4` | 0.000000 | 0.000000 |
| `single_h3` | 0.003816 | 0.003816 |
| `aligned_h3_h4` | 0.015262 | 0.015262 |
| `low_conflict_h3_h4` | 0.000954 | 0.000954 |

aligned 与 low/conflict 的差值为 `0.014308`，且 `5/5` 个 seed 都支持 aligned 更大。局部语言建模守卫也通过：所有条件最终 `Y1/Y2 accuracy=1.0/1.0`。因此，新的结论不是“只有 K3 能恢复 $Z$”，而是：direct informative-horizon supervision 让 $h_T$ 沿正确输出方向移动；一般 K 的效果取决于覆盖到的有信息未来位置的读出方向向量和；all-position 中的 $Q$ 恢复必须和 native H3 / $M_Z^{ref}$ 分开读。

## 12. 反例和竞争解释

| 竞争解释 | 为什么合理 | 当前处理 | 剩余风险 |
|---|---|---|---|
| NTP 最终也能学到 $Z$ | 全位置训练有其他监督位置 | 只 claim 一阶直接 margin，不 claim NTP 学不到 | 多步上限可能相同 |
| MTP 只是多一个 loss 正则化 | 任意辅助损失可能改变优化 | A11_05 / 11_07 用加/去当前直接项分离 | 损失尺度仍需控制 |
| probe 假阳性 | 外部 probe 可读不等于模型使用 | 使用 $Q=\min\{A,P,S\}$，并额外报告 native H3 / $M_Z^{ref}$ | $Q$ 不能单独证明 direct supervision |
| 梯度夹角混合 | $g_1,g_3$ 夹角有时负 | 新理论使用 $M_Z$ 而非 cosine | 需要一步干预验证 |
| 分支分离不等于可用 | hidden 分开但输出头不用 | 主量使用 readout-effective margin | 仍不等于下游 MoE utility |
| K 变大一定更好 | 更多未来位置可能带来更多监督 | A11_08 固定 K 和信息位置，只改变方向，显示方向冲突会削弱速度 | 真实语料方向几何尚未测量 |

## 13. 结论边界

可以说：

1. 在受控 K=2 / K=3 构造中，MTP 覆盖 $\tau$ 时给 $h_T$ 直接语义监督。
2. 低第 $\tau$ 未来位置损失推出 $h_T$ 含有 $Z$。
3. 在最小可训练前缀表示模型中，K=3 对读出有效语义 margin 有严格正的一阶增长，K=1/K=2 为 0。
4. 11_06 支持该一阶机制在受控 Transformer activation-space 中可观测：K3 的 $G_M^{hidden}$ 为正，K1/K2 近似为 0。
5. 11_07 支持当前决策前缀第 3 位置监督是 all-position 训练中更强 native readout 和更稳定 recovery 的机制组件。
6. A11_08 支持一般 K 的向量和机制：同样 K 和同样两个有信息未来位置下，aligned 输出方向给出更高 $G_K^{hidden}$，low/conflict 输出方向给出更低 $G_K^{hidden}$。

不能说：

1. MTP 在自然语言中已经优于 NTP。
2. NTP 学不到长程语义。
3. K 越大越好。
4. 全位置训练中非覆盖 K 不能恢复 $Z$。
5. $Q$ 单独证明 direct supervision。
6. 一阶 margin 优势自动推出任意设置下的多步 $T_{0.9}$ 优势。
7. A11 已经证明 MoE 路由保持或专家收益。
8. A11_08 已经证明自然语言中未来 token 方向天然对齐。

## 14. Anchor 分解和下一步

| Anchor | 决策问题 | 为什么需要 | 主指标 | 失败含义 |
|---|---|---|---|---|
| 11_06：读出有效 margin 效率 | 第 $\tau$ 未来位置监督是否产生严格正的一阶读出有效 margin 增长？ | 把表示定理推进到优化效率量 | $G_M^{hidden}$，$M_Z^{ref}$，$E_Z$，local guard | 已支持：K3 正，K1/K2 近 0 |
| 11_07：无泄漏全位置效率 | 在 $Q(0)$ 不饱和时，11_06 机制是否转化为更强 all-position recovery？ | 把一步机制放回 LM-style 训练 | $Q(0)$，$T_{0.9}$，早期 AUC，native H3，$M_Z^{ref}$，本地损失 | 已支持 direct 条件更强；同时确认 indirect transfer |
| 11_08：一般 K 读出方向动力学 | 多个有信息未来位置是否按读出方向向量和贡献一阶速度？ | 避免把结论误写成 K 越大越好 | $G_K^{hidden}$，几何预测，seed 方向一致性，本地损失 | 已支持：aligned 高于 low/conflict，shared 为 0，single 为正 |
| 11_09：next-K inclusion law | K 增大时，语义速度是否只在覆盖有信息位置时打开，并按新增方向变化？ | 把固定 K=4 的方向规律变成 next-2 / next-3 / next-K 规律 | turn-on、no-increment、vector-increment、local guard | 若失败，一般 K 机制只能停留在固定 K 几何构造 |
| 未来 MoE 桥接 | 写入的 $Z$ 是否改善 route-relevant margin？ | 连接主线 | 路由 margin、sign flip、LM loss，且必须用 native H3 / $M_Z^{ref}$ 保护 direct evidence | 若无改善，A11 仍只是表示目标机制线 |

## 14.5 下一步理论规划

当前最需要严谨化的机制句是：

> 当 $K$ 覆盖有信息未来词时，MTP 会给 $h_T$ 一个直接语义更新方向；多个有信息未来位置按中心化输出方向向量和叠加；全位置训练中还有间接迁移，但直接项会带来更强的模型自身预测、更大的语义 margin、更稳定的恢复。

后续理论推进应把这句话拆成五个可证明或可实验判定的子命题：

1. **next-K inclusion law。** K 增大时，如果新增未来位置不含 $Z$，则不应带来一阶语义增量；如果首次覆盖有信息未来位置，则语义速度 turn on；如果新增第二个有信息未来位置，则增量由 $2v^\top a+\|a\|^2$ 决定。

2. **全位置 loss 分解。** 将全位置训练写成：

$$
L_K^{all}=L_{\mathrm{direct}}+L_{\mathrm{indirect}}+L_{\mathrm{shared}},
$$

其中 $L_{\mathrm{direct}}=\lambda_\tau\operatorname{CE}(q_\tau(\cdot\mid h_T),S_Z)$ 是当前决策前缀上的有信息未来词监督。目标是证明或界定：$L_{\mathrm{direct}}$ 对 $M_Z$ 给出正的一阶贡献，而 $L_{\mathrm{shared}}$ 在分支折叠处只给公共更新；$L_{\mathrm{indirect}}$ 可以让 $Z$ 可读，但不必然增加 native $h_T\to S_Z$ 预测。

3. **从一阶 margin 到多步效率。** 现有定理只证明 $G_M^{hidden}>0$，还没有证明 $T_{0.9}$ 必然更小。下一步需要给出额外优化假设，例如小步长、局部平滑、读出 margin 与 native H3 accuracy 的单调关系，才能把一阶速度推出早期 AUC 或 hitting time 优势。

4. **固定读出与可训练 head 的关系。** 当前 $M_Z^{ref}$ 使用初始化输出行 $u^0_{S_z}$，可以稳定对齐一阶理论；但训练中预测 head 也会变化。需要补充一个 lemma：若 head 漂移有界，或当前 head 与初始语义方向夹角保持正相关，则 $M_Z^{ref}$ 的增长可以解释 native H3 的提高。

5. **间接迁移的理论位置。** 11_07 显示 K1/K2/masked K3 可以恢复非平凡 $Q$。因此理论不能写成“非覆盖 K 不能学 $Z$”，而应写成：非覆盖 K 缺少当前决策前缀上的直接 $M_Z$ 一阶驱动；它仍可能通过共享参数和其他位置 loss 产生 probe-readable recovery。

这些待办的边界是：第 1 点和第 4 点最接近局部定理或局部机制命题；第 2 点和第 5 点更像理论分解加受控实验；第 3 点通常需要额外优化假设。

## 15. 与主线的关系

项目主线仍是 top-1 MoE 路由中的特征级专家专业化，当前瓶颈是保持性。A11 不是替代主线，而是目标函数层面的候选机制：如果 MTP 能更早、更读出有效地把长程变量写入当前状态，它未来可能帮助形成更稳定的 route-relevant hidden states。

但这还没有被证明。连接 MoE 之前，必须先完成 next-K inclusion law，确保一般 K 的故事不是只在固定 K=4 的几何构造中成立。

## 16. 下一步唯一决策

当前唯一下一步：

> 先开 11_09 next-K inclusion law anchor：比较 K=2/K=3/K=4，验证语义速度是否只在 K 覆盖有信息未来位置时打开，新增无信息位置是否无显著增量，新增第二个有信息位置是否按向量增量变化。

不要先做 MoE bridge，也不要只重复 all-position $Q$ 曲线。11_06 / 11_07 已经说明：direct supervision 的证据应由 $G_M^{hidden}$、$M_Z^{ref}$、native H3 和 guarded recovery 联合给出；A11_08 又说明：一般 K 的增益必须按输出方向向量和审计，而不是按 K 大小审计。

## Source Map

- `sync/S000_current_specialization/stories/11_long_horizon_mtp_objective/story_cn.md`
- `sync/S000_current_specialization/anchors/11_long_horizon_mtp_objective/11_05_semantic_efficiency_bridge_anchor.md`
- `sync/S000_current_specialization/anchors/11_long_horizon_mtp_objective/README.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_06_readout_effective_margin_efficiency/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_06_readout_effective_margin_efficiency/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_07_no_leakage_all_position_efficiency/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_07_no_leakage_all_position_efficiency/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/detailed.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_08_general_k_readout_margin_dynamics_anchor.md`
