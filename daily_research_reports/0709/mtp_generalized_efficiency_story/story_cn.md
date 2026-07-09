# MTP 长程语义学习效率：从 K=2/3 到一般 K 的理论推进

文档状态：
- 类型：daily research story，A11_08 结果更新版
- 日期：2026-07-09
- 研究线：`11_long_horizon_mtp_objective`
- 作用：在现有 A11 story 后继续深化一般 K 理论，并记录 A11_08 的最小 falsifiable 实验结果；项目主线版本见 project-local story
- 当前核心：把“覆盖第一个有信息未来位置”推广到一般 K；A11_08 已支持“多个有信息未来位置的读出方向按向量和决定一阶语义速度”

## 0. 术语约定

| 术语 | 中文含义 | 具体对象 / 公式 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 多词元预测（MTP） | 同一个当前隐藏状态预测多个未来词元 | $L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j)$ | 研究远处目标是否提前监督当前状态 | K 越大一定越好 |
| 下一词元预测（NTP） | 当前隐藏状态只预测下一个词元 | $L_1(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),Y_1)$ | MTP 的对照 | NTP 永远学不到长程变量 |
| 早期变量 $Z$ | 前缀早期出现、未来才需要的信息 | 受控分支身份 | 长程语义的可控代理 | 自然语言全部语义 |
| 当前状态 $h_T$ | 决策前缀后的隐藏状态 | $h_T=f_\theta(X_{\le T})$ | 我们检查语义是否写入的位置 | 所有位置的信息 |
| 第一个有信息未来位置 $\tau$ | 第一个未来词元新增 $Z$ 信息的位置 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | 决定 K 是否覆盖直接语义监督 | 真实语料中固定唯一 |
| 有信息未来位置集合 $\mathcal I_K$ | 被 K 覆盖且含 $Z$ 新信息的位置集合 | $\mathcal I_K=\{j\le K:I(Z;Y_j\mid Y_{<j})>0\}$ | 一般 K 分析对象 | 位置越多一定越好 |
| 读出有效语义 margin | 当前状态是否沿正确未来 token 输出方向移动 | $M_K(h)=\frac1m\sum_z v_z^{(K)\top}h_z$ | 一阶效率理论量 | 多步收敛或自然语言收益 |
| 一般 K 合成语义方向 | 多个有信息未来位置的读出方向向量和 | $v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)$ | 决定一般 K 的一阶语义速度 | K 大小本身 |
| 隐藏状态语义速度 $G_K^{hidden}$ | 损失梯度把当前状态推向合成语义方向的速度 | $\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K)$ | A11_08 的主指标 | 参数空间长期收敛 |
| 分支分离能量 | 不同分支隐藏状态是否分开 | $E_Z=\frac1{2m^2}\sum_{z,z'}\|h_z-h_{z'}\|^2$ | 对应 probe / route 可分性 | 输出头是否使用该信息 |
| 直接项 | 当前 $h_T$ 自己预测含 $Z$ 的未来 token | $L_{direct}=\lambda_\tau\operatorname{CE}(q_\tau(\cdot\mid h_T),S_Z)$ | 最短信用分配路径 | 全位置训练中唯一通路 |
| 间接迁移 | 其他位置损失通过共享参数影响 $h_T$ | 由跨位置参数核 $J_TJ_s^\top$ 传递 | 解释 all-position 中 K1/K2 也能恢复 $Z$ | 直接监督无效 |
| 高恢复时间 | 达到语义恢复阈值的训练步数 | $T_\alpha=\inf\{t:M(t)\ge \alpha\}$ 或 $T_{0.9}$ | 多步效率量 | 一阶机制必然成立 |
| `shared_only_k4` | 四个未来位置都不含 $Z$ | `Y1=A,Y2=C,Y3=A,Y4=C` | A11_08 零语义速度守卫 | 全语言模型质量 |
| `single_h3` | 只有第 3 个未来位置含 $Z$ | `Y1=A,Y2=C,Y3=S_z,Y4=A` | A11_08 单信息位置正对照 | 一般 K 全部规律 |
| `aligned_h3_h4` | 第 3/4 未来位置都含 $Z$ 且读出方向对齐 | `Y3=S_z,Y4=T_z`，第 4 位置输出方向对齐第 3 位置 | 检验向量和放大 | 自然语言方向一定对齐 |
| `low_conflict_h3_h4` | 第 3/4 未来位置都含 $Z$ 但读出方向低/冲突 | 同样 `Y3=S_z,Y4=T_z`，第 4 位置削弱第 3 位置方向 | 检验方向冲突能削弱速度 | K 大一定无益 |

## 1. 摘要

现有 A11 story 已经完成两步。第一步是表示定理：如果 MTP 的预测范围覆盖第一个有信息未来位置 $\tau$，且 $Y_\tau=S_Z$ 一一编码早期变量 $Z$，那么低第 $\tau$ 个未来位置损失推出 $h_T$ 含有 $Z$。第二步是 K=3 的一阶读出 margin 定理：在 $Y_1=A,Y_2=C,Y_3=S_Z$ 的受控构造中，K=1/K=2 在分支折叠初始化处只产生公共更新，而 K=3 会把每个分支的 $h_T$ 推向正确 $S_Z$ 的输出方向。

本 story 的推进点是：这个结论不应停在 K=3。一般 K 的真正结构不是“预测更多更好”，而是“被覆盖的有信息未来位置是否给出同向、读出有效的更新”。一般 K 的一阶速度可以写成一个向量和的平方：

$$
G_K^{margin}=\frac1{m^2}\sum_z\left\|\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)\right\|^2.
$$

这说明三件事。第一，只要 K 没覆盖任何有信息位置，$G_K^{margin}=0$。第二，覆盖一个有信息位置会产生正的一阶读出 margin。第三，继续增大 K 不一定单调更好；只有新增未来位置的输出方向与已有长程方向对齐时，margin 速度才一定增加。如果新增位置方向冲突，可能抵消。

A11_08 已经把这个一般 K 机制做成最小可证伪实验。实验固定 `K=4`、固定四个 active loss、固定两个有信息未来位置 `{3,4}`，只改变第 4 个有信息未来位置的中心化输出方向。结果是：`aligned_h3_h4` 的隐藏状态语义速度 `G_hidden=0.015262`，`low_conflict_h3_h4` 的 `G_hidden=0.000954`，差值为 `0.014308`，且 `5/5` 个 seed 都满足 aligned 大于 low/conflict。`shared_only_k4` 为 0，`single_h3` 为 0.003816。本结果支持一般 K 向量和机制，没有触发 falsifier。

从概率分布学习角度，MTP 的优势来自有效监督强度 $S_K(Z)=\sum_{j\le K}\lambda_j I(Z;Y_j\mid Y_{<j})$，但它只是结构量，不等于优化效率。要把它变成学习效率，需要额外假设：每个含信息未来位置的梯度方向对 $Z$ 是可辨识且同向的。

从模型更新角度，MTP 的优势来自直接项给 $h_T$ 一个短信用分配路径。全位置训练下，NTP / 非覆盖 K 也可以通过间接迁移让 $Z$ 对 probe 可读；其理论形式是跨位置参数核 $J_TJ_s^\top$。因此全位置训练的正确理论不是“非覆盖 K 不能学”，而是：直接项给出确定的局部正贡献，间接项取决于跨位置核对齐，符号和大小都不是无条件保证。

## 2. 研究问题

当前要回答的问题是：

> 在受控长程语义构造中，MTP 相比 NTP 的“更好”能否被定义成可证明的学习效率优势？

这里把“更好”拆成四层：

1. **表示存在**：低 future loss 是否推出 $h_T$ 含 $Z$。
2. **结构监督**：MTP 是否覆盖含 $Z$ 的未来位置。
3. **一阶速度**：MTP 梯度是否立刻增加读出有效语义 margin。
4. **训练动力学**：这种一阶速度是否导致更短 $T_\alpha$ 或更高早期 AUC。

第 1 层已经由旧定理完成。第 2 层由 $I(Z;Y_j\mid Y_{<j})$ 定义。第 3 层可以形成一般 K 定理。第 4 层需要额外优化假设和实验验证。

## 3. 数据和训练布局

令 $Z\in\{1,\ldots,m\}$ 均匀分布。模型读完前缀后形成：

$$
h_z=h_T(Z=z).
$$

未来目标为：

$$
Y_1,Y_2,\ldots,Y_K.
$$

有些位置不含 $Z$ 信息，例如共享 token：

$$
Y_j=A_j.
$$

有些位置含 $Z$ 信息，例如：

$$
Y_j=S_{j,Z},\qquad Z\mapsto S_{j,Z}\text{ 一一对应}.
$$

定义有信息位置集合：

$$
\mathcal I_K=\{j\le K:Y_j=S_{j,Z}\text{ 且 }Z\mapsto S_{j,Z}\text{ 一一对应}\}.
$$

更一般地，可用条件互信息定义：

$$
\mathcal I_K=\{j\le K:I(Z;Y_j\mid Y_{<j})>0\}.
$$

为了证明干净，本文先使用一一编码版本。

MTP 目标为：

$$
L_K=\frac1m\sum_{z=1}^m\sum_{j=1}^K\lambda_j\operatorname{CE}(q_j(\cdot\mid h_z),Y_j(z)).
$$

其中：

$$
q_j(\cdot\mid h_z)=\operatorname{softmax}(U_jh_z).
$$

## 4. 物理直觉

MTP 不是因为“预测更多 token”自动更好。它的优势来自：多个未来 token 可能共同暴露同一个早期变量 $Z$。如果这些 token 的监督方向一致，它们会把 $h_T$ 推向同一个长程语义方向；如果它们方向冲突，增大 K 可能不会更好。

因此，一般 K 理论必须包含两个条件：

1. 新增未来位置是否含有 $Z$ 信息；
2. 新增未来位置的输出方向是否与已有语义方向对齐。

这比旧 story 更深入，因为它不仅解释 K=3 为什么有用，也解释为什么 K 更大不必然更好。

## 5. 一般 K 的读出有效 margin 定义

对每个有信息位置 $j\in\mathcal I_K$，令：

$$
u_{j,z}=u^{(j)}_{S_{j,z}},\qquad \bar u_j=\frac1m\sum_z u_{j,z}.
$$

定义 K 覆盖到的总语义方向：

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j).
$$

定义一般 K 的读出有效语义 margin：

$$
M_K(h)=\frac1m\sum_z v_z^{(K)\top}h_z.
$$

这个量的含义是：如果 $M_K$ 增大，说明 $h_z$ 沿着 K 覆盖到的、有信息未来 token 的合成输出方向移动。

## 6. 定理 1：一般 K 的一阶 margin 速度

**假设。**

1. 初始化分支折叠：$h_1=\cdots=h_m=h_0$。
2. 对无信息位置 $j\notin\mathcal I_K$，目标 $Y_j$ 对所有 $z$ 相同。
3. 对有信息位置 $j\in\mathcal I_K$，目标 $Y_j=S_{j,z}$，且输出向量 $u_{j,z}$ 不全相同。
4. 预测头在分析该一步时固定。

**定理。** 在梯度流 $\dot h_z=-\nabla_{h_z}L_K$ 下：

$$
\left.\frac{d}{ds}M_K(h(s))\right|_{s=0}
=\frac1{m^2}\sum_z\left\|\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)\right\|^2.
$$

因此：

- 若 $\mathcal I_K=\varnothing$，则该速度为 0；
- 若合成方向 $v_z^{(K)}$ 不全为 0，则该速度严格为正。

**证明。**

在折叠初始化下，每个 head 的预测分布在所有分支上相同。对任意位置 $j$，令：

$$
p_j=\operatorname{softmax}(U_jh_0).
$$

如果 $j$ 是共享目标位置，目标为 $A_j$，则：

$$
\nabla_{h_z}L_j=\frac{\lambda_j}{m}(U_j^\top p_j-u_{A_j}),
$$

该项与 $z$ 无关，只产生公共更新。

如果 $j\in\mathcal I_K$，目标为 $S_{j,z}$，则：

$$
\nabla_{h_z}L_j=\frac{\lambda_j}{m}(U_j^\top p_j-u_{j,z}).
$$

所以由所有有信息位置产生的分支相关速度为：

$$
\dot h_z^{info}=\frac1m\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-U_j^\top p_j).
$$

共享目标位置和每个 $U_j^\top p_j$ 都是公共项。由于：

$$
\sum_z v_z^{(K)}=\sum_z\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)=0,
$$

公共项对 $M_K$ 的导数贡献为 0。因此：

$$
\frac{d}{ds}M_K=\frac1m\sum_z v_z^{(K)\top}\dot h_z
=\frac1m\sum_z v_z^{(K)\top}\frac1m\sum_{j\in\mathcal I_K}\lambda_j u_{j,z}.
$$

又因为：

$$
\sum_{j\in\mathcal I_K}\lambda_j u_{j,z}=v_z^{(K)}+\sum_{j\in\mathcal I_K}\lambda_j\bar u_j,
$$

第二项是公共项，与 $v_z^{(K)}$ 相乘后求和为 0。故：

$$
\frac{d}{ds}M_K=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2.
$$

证毕。

## 7. 推论：K 增大不必然单调更好

从定理 1 得：

$$
G_K=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2.
$$

若加入新有信息位置 $r$，令：

$$
a_{r,z}=\lambda_r(u_{r,z}-\bar u_r),
$$

则：

$$
G_{K\cup r}-G_K=\frac1{m^2}\sum_z\left(2v_z^{(K)\top}a_{r,z}+\|a_{r,z}\|^2\right).
$$

因此，如果新增位置与已有语义方向对齐，增益为正；如果强烈反向，可能抵消已有方向。

**允许 claim：** 多个未来有信息位置在方向对齐时会增强一阶语义更新。

**禁止 claim：** 只要 K 更大就更好。

## 8. 概率分布学习视角

定义有效监督强度：

$$
S_K(Z)=\sum_{j=1}^K\lambda_j I(Z;Y_j\mid Y_{<j}).
$$

这个量回答：K 覆盖的未来目标中，有多少新增关于 $Z$ 的分布信息。它比互信息表示定理更接近数据层，但仍然不是学习效率量。

**命题。** 若 $S_K(Z)=0$，则 K 覆盖的目标在分布上不要求知道 $Z$；若 $S_K(Z)>0$，则存在未来目标给 $Z$ 提供新增监督。

**边界。** $S_K(Z)>0$ 不保证优化快。它还需要：

1. 模型参数化能区分 $Z$；
2. 含信息目标的梯度方向进入 $h_T$；
3. 多个有信息目标的方向不互相抵消；
4. 本地目标梯度不破坏该方向。

所以概率分布视角适合作为必要条件和数据设计原则，不足以单独证明效率。

## 9. 参数更新视角

设短程本地损失梯度为：

$$
g_{local}=\nabla_\theta L_{local},
$$

长程直接损失梯度为：

$$
g_{long}=\nabla_\theta L_{direct}.
$$

语义恢复损失或 margin 的梯度为 $\nabla_\theta R_Z$ 或 $\nabla_\theta M_K$。

一阶语义改进条件是：

$$
\langle \nabla_\theta R_Z,g_{long}\rangle>0
$$

或等价地：沿 $-g_{long}$ 更新会增加 $M_K$。

本地不冲突条件是：

$$
\langle g_{local},g_{local}+\lambda g_{long}\rangle\ge (1-\delta)\|g_{local}\|^2.
$$

这表示加入长程目标后，本地下降方向没有被明显破坏。

**条件定理。** 若损失函数局部光滑，步长 $\eta$ 足够小，且：

$$
\langle \nabla_\theta R_Z,g_{long}\rangle\ge\gamma>0,
$$

则一步更新：

$$
\theta^+=\theta-\eta(g_{local}+\lambda g_{long})
$$

相对只用 $g_{local}$ 的更新，额外降低语义恢复损失至少：

$$
\eta\lambda\gamma-O(\eta^2).
$$

若同时满足本地不冲突条件，则该语义收益不是通过牺牲本地目标得到的。

**边界。** 这是条件优化定理，不是无条件 MTP 优势。A11_06 / A11_07 的作用正是检查这些条件的可观测版本。

## 10. 全位置训练动力学

全位置训练可以分解为：

$$
L_K^{all}=L_{direct}+L_{indirect}+L_{shared}.
$$

其中：

- $L_{direct}$ 是当前决策前缀上的 $h_T\to S_Z$；
- $L_{shared}$ 是不含 $Z$ 的共享目标；
- $L_{indirect}$ 是其他位置中含 $Z$ 或能通过共享参数影响 $h_T$ 的损失。

令 $J_T=\partial h_T/\partial\theta$，另一个位置 $s$ 的隐藏状态雅可比为 $J_s=\partial h_s/\partial\theta$。位置 $s$ 的损失梯度为：

$$
\nabla_\theta \ell_s=J_s^\top \nabla_{h_s}\ell_s.
$$

该损失对 $h_T$ 的一阶影响为：

$$
\dot h_T^{(s)}=-J_TJ_s^\top\nabla_{h_s}\ell_s.
$$

这里：

$$
K_{T,s}=J_TJ_s^\top
$$

是跨位置参数核。它决定“其他位置的 loss 是否会改变当前 $h_T$”。

**命题。** 间接迁移是否增加 $M_K(h_T)$，取决于：

$$
\langle \nabla_{h_T}M_K,\; -K_{T,s}\nabla_{h_s}\ell_s\rangle.
$$

该量可以为正、为零或为负；因此全位置训练下 NTP / 非覆盖 K 可能恢复 $Z$，但这种恢复不是由当前 $h_T\to S_Z$ 的直接项保证。

这解释了 A11_07：K1/K2/masked K3 可以有较高 $Q$，但 native H3 与 $M_Z^{ref}$ 接近 0；它们更多是 probe-readable 或间接迁移恢复，而不是原生 $h_T\to S_Z$ 预测。

## 11. 从一阶速度到收敛 / hitting time

若能证明在一个训练区间内：

$$
\frac{d}{dt}M(t)\ge\gamma_K>0,
$$

且目标阈值为 $M^*$，初始为 $M(0)$，则：

$$
T_K\le \frac{M^*-M(0)}{\gamma_K}.
$$

若 NTP / 非覆盖 K 的直接速度为 0，但存在间接速度 $\gamma_{ind}$，而 MTP 具有：

$$
\gamma_{MTP}\ge \gamma_{ind}+\gamma_{direct},\qquad \gamma_{direct}>0,
$$

则在同一阈值下：

$$
T_{MTP}\le \frac{M^*-M(0)}{\gamma_{ind}+\gamma_{direct}}<\frac{M^*-M(0)}{\gamma_{ind}}.
$$

这就是从一阶速度到多步效率的最小理论桥。

**但要注意：** 这个结论需要区间内速度下界、head 方向稳定、步长稳定和本地目标不冲突。当前 A11 还没有无条件证明这些假设，只能通过 11_07 这类实验观察其近似成立。

## 12. 接下来还能推进的理论方向

### 方向 A：next-K inclusion law

研究：当 K 从 next-2 到 next-3 再到 next-K 增大时，一阶语义速度是否只在 K 覆盖有信息未来位置时打开；新增无信息未来位置是否不给语义增量；新增第二个有信息未来位置是否按向量增量改变速度。核心量是：

$$
\sum_z v_z^{(K)\top}a_{r,z}.
$$

如果该项非负，则新增未来位置有益；若为负且幅度大，新增未来位置可能削弱语义方向。A11_08 已经验证了固定 `K=4` 下 aligned 与 low/conflict 的方向差异；下一步要验证随 K 递增时的 turn-on / no-increment / vector-increment 规律。

### 方向 B：概率分布到梯度信号的桥梁

研究：$I(Z;Y_j\mid Y_{<j})$ 如何转化为输出向量方向 $u_{j,z}-\bar u_j$ 的可分性。一个可行假设是：未来 token 的 branch code 越可分，输出行中心化能量越大。

### 方向 C：全位置训练的跨位置核理论

研究：非覆盖 K 为什么也能恢复 $Z$。核心是 $K_{T,s}=J_TJ_s^\top$ 的正对齐。可以实验测量哪些位置的损失对 $h_T$ 的 $M_Z$ 有正贡献。

### 方向 D：本地目标冲突理论

研究：长程目标是否与短程目标冲突。不能只看梯度 cosine；应看两个量：

$$
\Delta M_Z>0,\qquad \Delta L_{local}\le 0\text{ 或不显著上升}.
$$

### 方向 E：固定输出方向与可训练 head 的关系

A11_06 使用固定初始输出方向 $u^0_{S_z}$ 定义 $M_Z^{ref}$。后续需要证明或测量：训练中当前 head 的方向与 $u^0_{S_z}$ 保持正相关，否则 $M_Z^{ref}$ 只能作为参考 margin。

## 13. 下一步建议

不要马上桥接 MoE，也不要扩到自然语言。A11_08 已支持一般 K 的方向对齐机制；下一步最小理论实验应是：

1. **11_09：next-K inclusion law 实验。** 系统比较 K=2/K=3/K=4：K 未覆盖有信息位置时应近零；K 首次覆盖有信息位置时应 turn on；K 只新增无信息位置时应无显著语义增量；K 新增第二个有信息位置时应按向量增量变化。
2. **11_10：全位置跨位置核实验。** 在 inclusion law 完成后，再测量 $J_TJ_s^\top$ 或其有限差分近似，判断间接迁移来自哪些位置，是否与 $M_Z$ 方向对齐。

这两个实验比直接做 MoE bridge 更必要。因为它们能回答：MTP 的效率优势什么时候随 K 增强，什么时候只是新增了无信息目标，什么时候会被方向冲突或间接迁移覆盖。

## 14. 当前允许的最终表述

可以说：

> 在受控长程语义构造中，MTP 的优势不是“预测更多 token”，而是“覆盖含有早期变量的未来 token”。在分支折叠初始化和固定输出方向下，覆盖的有信息未来位置给当前状态一个严格正的一阶读出有效语义 margin 增长；一般 K 的增长等于各有信息未来位置中心化输出方向之和的平方。A11_08 支持该向量和机制：同样 `K=4`、同样两个有信息未来位置时，aligned 输出方向给出高 `G_hidden`，low/conflict 输出方向给出低 `G_hidden`。多步训练优势需要额外假设或实验验证，全位置训练还存在跨位置间接迁移。

不能说：

> MTP 在自然语言中已经更好；K 越大越好；NTP 不能学长程变量；probe-readable recovery 等价于 direct prediction；A11 已经证明 MoE 路由收益。

## Source Map

- `daily_research_reports/0709/meetings/meeting_brief.md`
- `daily_research_reports/0709/mtp_generalized_efficiency_story/anchors/11_08_general_k_readout_margin_dynamics_anchor.md`
- `daily_research_reports/0709/mtp_generalized_efficiency_story/protocols/11_08_protocol.md`
- `Projects/from-attention-to-search/main/stories/11_long_horizon_mtp_objective/story_cn.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_08_general_k_readout_margin_dynamics_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/detailed.md`
