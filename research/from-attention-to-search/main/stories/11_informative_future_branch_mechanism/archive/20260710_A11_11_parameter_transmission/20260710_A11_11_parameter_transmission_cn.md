# 多词元预测如何更高效地学习长程语义信息

文档状态：
- 类型：研究线级 story，当前版本为理论 + 实验更新版
- 研究线：`11_long_horizon_mtp_objective`
- 语言：中文
- 写作模式：综合 + 下一阶段前瞻
- 当前核心变化：以 K=2 作为最小理论基元，将主线整理为“低损失表示保证 -> 隐藏状态空间的一阶与有限步效率 -> Transformer 参数空间传递 -> 全位置参数分解”。A11_11 已在受控参考折叠 decision-only 设置中验证：K=2 直接语义信号能通过共享编码器雅可比形成正的参数语义速度；下一步唯一问题是，在 LM-style 全位置训练中，这个直接项如何与背景损失和间接迁移分开

建议阅读顺序：先读第 1-5 节理解问题、数据和物理直觉；再读第 6-8 节掌握从表示保证到参数传递的公式与证明；随后读第 9-13 节核对实验、竞争解释和结论边界；最后读第 14-16 节理解下一步为何只做全位置参数分解。

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
| 单决策前缀训练（decision-only） | 只在待研究的当前前缀状态 $h_T$ 上计算多步预测损失 | $L_K(h_T)=\sum_{j=1}^K\lambda_j\operatorname{CE}(q_j,Y_j)$ | 隔离当前位置的直接监督 | 标准语言模型全位置训练行为 |
| 全位置训练（all-position） | 在序列每个位置都计算未来预测损失 | $L_K^{all}=\sum_t\sum_j\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j})$ | 接近语言模型训练并允许参数共享迁移 | 当前 $h_T$ 的恢复一定来自直接监督 |
| 模型自身预测（native prediction） | 直接使用训练中的预测头判断正确语义词元 | 例如第 3 未来位置准确率 | 判断模型是否实际使用 $h_T$ 中的信息 | 信息只能由直接路径学到 |
| 冻结探针（frozen probe） | 训练后固定主干，再用独立线性读出器预测 $Z$ | $P=\operatorname{Acc}(\operatorname{probe}(h_T),Z)$ | 检查 $Z$ 是否线性可读 | 模型自身预测头已经使用 $Z$ |
| 参考折叠 | 在参考参数点把各分支决策状态设为同一状态，同时保留并控制分支敏感雅可比 | $H_\alpha=\bar H_0+D_\alpha(H^{raw}-H_0^{raw})$ | 单独测量语义方向能否传入共享编码器参数 | 自然 Transformer 训练轨迹 |
| 读出有效语义 margin | $h_T$ 是否沿着正确未来 token 的输出方向移动 | $M_Z=\frac1m\sum_z(u_{S_z}-\bar u)^\top h_z$ | 是新的效率理论量 | 多步收敛或自然语言收益 |
| 分支分离能量 | 不同分支隐藏状态是否分开 | $E_Z=\frac{1}{2m^2}\sum_{z,z'}\|h_z-h_{z'}\|^2$ | 对应 probe / route 可分性 | 信息是否被输出头使用 |
| 高恢复时间 | 达到可靠语义恢复阈值的训练步数 | $T_{0.9}=\inf\{t:Q(t)\ge0.9\text{ 连续评估成立}\}$ | 实验学习效率指标 | 一阶机制原因 |
| 有限步效率 | 在若干训练步内更早越过语义 margin 或恢复阈值 | 例如 $T_\gamma=\inf\{t:M_K(t)\ge\gamma\}$ | 隐藏状态模型中已给出条件性与对称情形定理 | Transformer 参数训练不自动继承 |
| 保守恢复分数 $Q$ | 同时要求预测、探针、替换一致 | $Q=\min\{A,P,S\}$ | 防止 probe 假阳性 | 完整因果证明 |
| 有信息未来位置集合 $\mathcal I_K$ | 被 K 覆盖且含有 $Z$ 新信息的位置 | $\mathcal I_K=\{j\le K:I(Z;Y_j\mid Y_{<j})>0\}$ | 一般 K 的核心对象 | 位置越多一定越好 |
| 一般 K 合成语义方向 | 多个有信息未来位置的读出方向向量和 | $v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)$ | 决定当前状态的一阶语义更新方向 | 多步训练一定更快 |
| 隐藏状态语义速度 $G_K^{hidden}$ | 损失梯度把 $h_T$ 推向合成语义方向的速度 | $\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K)$ | A11_08 的主指标 | 参数空间长期收敛 |
| 语义切向核 $\Theta$ | 参数更新能把多少语义梯度传回当前隐藏状态 | $\Theta=JJ^\top$，其中 $J=\partial H/\partial\theta$ | 把隐藏状态定理提升到 Transformer 参数训练 | 非线性长期收敛 |
| 语义传递系数 $\kappa_K$ | 编码器在合成语义方向上的局部可训练程度 | $\kappa_K=v^{(K)\top}\Theta v^{(K)}/\|v^{(K)}\|^2$ | 区分“目标给了信号”和“模型能否吸收信号” | 自然语言收益或全局样本效率 |
| 参数净保留率 $\rho_{\theta,net}$ | 加入共享目标后，MTP 直接语义速度保留了多少且是否反号 | $G_{\theta,total}/G_{\theta,direct}$ | 判断背景项是否反转直接项 | 绝对学习速度 |
| 核余弦 $\chi_\Theta$ | 语义方向和共享目标方向经过编码器雅可比后的对齐程度 | $\cos(J^\top v,J^\top c)$ | 决定背景项方向 | 单独证明真实损害 |
| 核范数比 $r_\Theta$ | 共享目标参数方向相对语义参数方向的强度 | $\|J^\top c\|/\|J^\top v\|$ | 决定背景项幅度 | 长期优化效率 |
| `aligned_h3_h4` | 第 3/4 未来位置都含 $Z$，且输出方向对齐 | `Y3=S_z,Y4=T_z`，第 4 位置中心化输出行与第 3 位置对齐 | 一般 K 正向叠加条件 | 自然语言中真实方向对齐 |
| `low_conflict_h3_h4` | 第 3/4 未来位置都含 $Z$，但输出方向低/冲突 | 同样 `Y3=S_z,Y4=T_z`，第 4 位置中心化输出行削弱第 3 位置方向 | 一般 K falsifier 条件 | K 更大一定无益 |

## 1. 摘要

A11 的问题是：多词元预测是否比下一词元预测更高效地学习长程语义变量。最小构造从 K=2 开始：$Y_1=A$ 与分支无关，$Y_2=S_Z$ 一一编码早期变量 $Z$。若预测范围覆盖第一个含 $Z$ 的未来位置 $\tau$，低该位置损失会推出当前隐藏状态 $h_T$ 含有 $Z$；非覆盖目标在同一前缀上没有这条直接表示约束。

效率机制由读出有效语义 margin 刻画。覆盖有信息位置时，隐藏状态获得沿正确输出方向的分支相关更新；非覆盖的共享目标只产生公共更新。多个有信息未来位置按中心化输出方向向量和叠加，因此增益取决于方向对齐，而不是 K 本身。

本版把一阶机制推进到有限步。若直接优化隐藏状态，margin 每一步满足精确恒等式：

$$
M_K(t+1)-M_K(t)=\eta G_K^{hidden}(t),
$$

在固定规则单纯形输出头、共享损失不进入语义子空间的 K=2 模型中，可以进一步证明 MTP 在有限步内把语义读出概率推过任意高于随机水平的阈值，而 K=1 的反事实语义读出保持在随机水平。随机梯度版本则表明，样本命中界同时由平均语义漂移 $\mu$ 和梯度噪声 $\sigma$ 控制。

受控实验与这条机制一致：直接有信息条件具有正且早期持续的语义速度，并形成更强的模型自身预测和语义 margin；一般 K 实验支持方向向量和规律；全位置实验同时表明，非直接损失也能通过参数共享让 $Z$ 对探针可读，因此 $Q$ 不能单独证明直接监督。A11_10 的参数空间命中证书仍然过松。

A11_11 的参考折叠模型进一步证明：K=2 直接参数语义速度按雅可比强度的平方 $\alpha^2$ 缩放，共享 H1 背景项按 $\alpha$ 缩放，二者的净保留率满足 $\rho_{\theta,net}(\alpha)=1+\chi_\Theta r_\Theta/\alpha$；在原生尺度 $\alpha=1$ 时化为 $1+\chi_\Theta r_\Theta$。这说明隐藏空间中分支公共的 H1 更新虽然与语义方向正交，经过分支敏感的编码器雅可比后仍可能形成参数空间的帮助或抵消。

A11_11 的远程四卡结果支持该传递机制：`5/5` 个 seed 校准通过，K=2 直接参数语义速度在原生 $\alpha=1$ 下全为正，full K2 净速度也全为正，真实一步 margin 变化与 $\eta G_{\theta,total}$ 同号且误差很小。因此当前边界变为：受控 decision-only 的参数传递前提已经通过，但 all-position 背景损失、间接迁移、随机样本效率和自然语言收益仍未证明。下一步只研究全位置参数分解，不扩展 K，也不转向 MoE。

## 2. 研究问题

主问题：

> 在长程语义学习上，MTP 相比 NTP 到底好在哪？

当前版本将它拆成五层：

1. **表示存在**：训练后 $h_T$ 是否含有 $Z$。
2. **目标函数结构优势**：MTP 是否把含 $Z$ 的未来词元损失直接加到 $h_T$。
3. **一阶优化速度优势**：训练早期，MTP 梯度是否更快把 $h_T$ 推向正确未来输出方向。
4. **多步训练效率优势**：实际训练中是否更小 $T_{0.9}$ 或更高早期 $Q$ 曲线面积。
5. **参数空间传递**：隐藏状态上的直接语义速度，是否经过编码器雅可比后仍形成可下界的参数更新。

A11 现在已经回答第 1、第 2、第 3 层，并在额外对称几何假设下完成了隐藏状态空间的第 4 层有限步定理。A11_11 又补上了第 5 层的最小受控局部版本：在 reference-folded K=2 decision-only 设置中，目标提供的语义方向可以经过编码器雅可比形成正的参数语义速度。真正未闭合的是全位置版本：LM-style 训练中 direct 项、背景项和间接迁移项如何共同作用。

### 2.1 最终真实下游任务中的“长程语义”

真实长程语义不能只定义为“两个 token 距离很远”，也不能用复制一个早期 key 作为最终目标。令早期文本片段 $E$ 建立语义状态：

$$
Z=s(E).
$$

$Z$ 可以是人物立场、对象状态、规则、目标、承诺或因果条件。它必须对保持原意的改写近似不变，而不是等于某个表面 token。令远处决策位置的局部窗口为 $W_T$，模型需要预测或选择 $Y_{T+\tau}$。长程语义关系要求：

$$
\operatorname{distance}(E,T)\ge D,
$$

$$
I(Z;Y_{T+\tau}\mid W_T)>0.
$$

这表示只看远处决策前的局部文本不够；早期建立的语义状态仍能改变正确结果。中间文本不要求是随机 filler，它可以有完整内容、传播或更新 $Z$；真正需要控制的是局部窗口不足，而不是中间内容无意义。

还要有两个操作性守卫：

1. **改写不变性：** 把 $E$ 改写成不同表面形式但保持 $Z$ 不变，正确远处决策不变。
2. **反事实一致性：** 把 $Z=z$ 改成 $Z=z'$，同时保持远处局部窗口匹配，正确决策应随之改变。

因此最终真实下游任务瞄准“长文档延迟状态决策”：早期片段建立状态，经过有意义的长上下文后，模型在远处完成原生续写、选择或问答。它不是纯检索；模型必须把早期语义状态用于当前决策。

### 2.2 在真实任务中“MTP 比 NTP 好”的定义

MTP 的真实优势不能由最终 probe 或训练总损失定义。公平比较固定模型主干、训练文本和主干更新次数，并同时报告额外预测头计算。主判据是：

$$
T_{\gamma}^{MTP}<T_{\gamma}^{NTP},
$$

其中 $T_\gamma$ 是真实长程语义分数达到阈值所需的训练 token 或主干更新数。真实语义分数至少联合：

$$
Q_{real}
=\min\{
A_{native},
C_{counterfactual},
C_{paraphrase}
\}.
$$

$A_{native}$ 是模型自身远处预测或选择准确率，$C_{counterfactual}$ 是替换早期语义后的响应一致性，$C_{paraphrase}$ 是早期语义改写后的稳定性。同时要求局部 next-token loss 或困惑度不出现不可接受回退。

所以最终希望证明或验证的不是“MTP 最终一定更强”，而是：在同等数据与主干训练预算下，当未来目标包含局部窗口无法提供的早期语义状态时，MTP 以更短监督路径获得更高的早期语义漂移、更小阈值命中时间或更高数据效率，并保持局部语言建模。

### 2.3 从当前受控理论到 LLM 下游的判定梯子

| 层级 | 决策问题 | 当前状态 / 未来门槛 | 不能提前声称 |
|---|---|---|---|
| L0 隐藏状态机制 | 有信息未来目标是否直接推动 $h_T$ 的语义 margin | 已有 K=2、首个有信息位置、general-K 和有限步受控理论 | 参数化模型一定吸收 |
| L1 参数传递 | $v$ 是否经过编码器切向核形成正净参数速度 | A11_11 已在受控 reference-folded decision-only 设置中支持 | all-position 或自然语言收益 |
| L2 全位置参数分解 | 直接项能否压过真实 LM 背景与间接迁移 | 当前下一步 | 样本效率 |
| L3 真实语义代理审计 | 自然文本任务是否满足局部不足、改写不变和反事实一致 | 先做数据/指标审计，不先训方法 | MTP 优势 |
| L4 小语言模型效率 | 同主干、同数据预算下，MTP 是否更早达到 $Q_{real}$ | L3 通过后的第一项真实训练实验 | LLM scaling |
| L5 预训练 LLM 下游 | 继续预训练后是否改善长文档延迟状态决策且守住局部 LM | 最后阶段 | 普适 MTP 优越性 |

## 3. 为什么下一步应先推进理论闭环

A11 现在已经不缺一个简单的“再跑一次全位置曲线”。原因是：

1. 全位置训练会引入间接迁移，容易把“当前前缀直接监督”与“其他位置共享参数更新”混在一起。
2. 随机初始化可能让 $Q(0)$ 已经很高，导致 $T_{0.9}$ 失去速度含义。
3. 即使全位置实验显示 K=3 更快，也还需要一个紧贴目标函数的理论量来说明为什么更快。

因此，11_06 / 11_07 的结果应被读成一次理论收束：

1. 覆盖 $\tau=3$ 的直接监督确实产生一阶读出 margin 优势。
2. all-position 中的 $Q$ 恢复不等价于直接语义监督，因为间接迁移可以制造 probe-readable recovery。
3. 隐藏状态空间与参数空间必须分开：前者可以给出精确有限步定理，后者需要额外的语义切向核、干扰和非线性余项条件。

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

### 8.2 K=2 最小理论基元

K=2 是最小的 MTP-vs-NTP 理论单元。数据为：

$$
Y_1=A,\qquad Y_2=S_Z.
$$

其中 $A$ 对所有分支共享，$S_Z$ 一一编码 $Z$。令第 2 位置输出方向为：

$$
u_z=u_{S_z}^{(2)},\qquad \bar u=\frac1m\sum_z u_z.
$$

定义：

$$
M_Z^{(2)}(h)=\frac1m\sum_z(u_z-\bar u)^\top h_z.
$$

在分支折叠初始化、固定第 2 位置输出向量不全相同的条件下：

$$
G_1^{margin}(\theta_0)=0,
$$

但：

$$
G_2^{margin}(\theta_0)
=\frac{\lambda_2}{m^2}\sum_z\|u_z-\bar u\|^2>0.
$$

含义：next-one 只看到共享目标 $A$，不能给 $h_T$ 分支相关的一阶语义更新；next-two 直接看到 $S_Z$，因此在读出有效语义 margin 上有严格正的一阶速度。A11_01 / A11_03 是这个 K=2 基元的实验支撑。

### 8.3 $\tau=3$ 后移定理：K=3 有严格一阶读出有效 margin 增长

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

### 8.4 分支分离能量是二阶量

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

### 8.5 一般 K 的向量和定理

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

### 8.6 隐藏状态空间的精确有限步恒等式

先把 $h_1,\ldots,h_m$ 直接视为优化变量，并固定定义 margin 的输出方向 $v_z^{(K)}$。一次梯度下降为：

$$
h_z(t+1)=h_z(t)-\eta\nabla_{h_z}L_K(H_t).
$$

**定理 1（精确有限步 margin 更新）。** 对任意损失 $L_K$ 和任意步长 $\eta$，都有：

$$
M_K(t+1)-M_K(t)=\eta G_K^{hidden}(t),
$$

其中：

$$
G_K^{hidden}(t)
=\frac1m\sum_z v_z^{(K)\top}\left(-\nabla_{h_z}L_K(H_t)\right).
$$

**证明。** 因为 $M_K(H)=\frac1m\sum_zv_z^{(K)\top}h_z$ 对 $H$ 是线性的，直接代入更新式：

$$
\begin{aligned}
M_K(t+1)-M_K(t)
&=\frac1m\sum_zv_z^{(K)\top}(h_z(t+1)-h_z(t))\\
&=\eta\frac1m\sum_zv_z^{(K)\top}(-\nabla_{h_z}L_K(H_t))\\
&=\eta G_K^{hidden}(t).
\end{aligned}
$$

证毕。

**推论 1（条件性命中时间）。** 若在 $M_K(t)<\gamma$ 时恒有 $G_K^{hidden}(t)\ge g_K>0$，则：

$$
T_\gamma(K)
\le
\left\lceil\frac{\gamma-M_K(0)}{\eta g_K}\right\rceil.
$$

这里没有 $\eta^2B$ 曲率项。A11_10 中的曲率项来自“先更新参数 $\theta$，再由非线性编码器得到 $h_T(\theta)$”，不是隐藏状态空间本身的必要项。

### 8.7 K=2 对称几何下的显式有限步恢复定理

上一推论仍把速度持续性写成假设。下面在一个更强但完全可解的最小模型中把它证明出来。

假设第 2 未来位置只在 $m$ 个语义词元 $S_1,\ldots,S_m$ 上做 softmax，固定输出向量形成规则单纯形：

$$
\sum_z u_z=0,
\qquad
\|u_z\|^2=r^2,
\qquad
u_z^\top u_{z'}=-\frac{r^2}{m-1}\quad(z\ne z').
$$

初始语义分量为 $h_z(0)=0$。共享目标损失在该语义子空间中的投影为 0，因此只有 $Y_2=S_z$ 的直接项改变语义分量。信息项为：

$$
L_{info}=\frac{\lambda}{m}\sum_z\operatorname{CE}
\left(\operatorname{softmax}(U h_z),S_z\right).
$$

**定理 2（K=2 显式有限步恢复）。** 对上述模型做步长为 $\eta$ 的梯度下降，轨迹保持：

$$
h_z(t)=a_tu_z,
$$

且：

$$
a_{t+1}=a_t+\eta\frac{\lambda}{m-1}(1-p_t),
$$

其中模型自身预测正确语义词元的概率为：

$$
p_t=
\frac{1}
{1+(m-1)\exp\left(-a_t\frac{mr^2}{m-1}\right)}.
$$

对任意 $0<\delta<1-1/m$，令 $T_\delta=\inf\{t:p_t\ge1-\delta\}$，则：

$$
T_\delta
\le
\left\lceil
\frac{(m-1)^2}
{\eta\lambda\delta mr^2}
\log\frac{(m-1)(1-\delta)}{\delta}
\right\rceil.
$$

而只含共享目标的 K=1 训练没有分支相关语义梯度，所有 $h_z$ 的语义分量保持相同；在本定理的零投影条件下，它们保持为 0。若用同一个固定语义头作反事实评估，则 $p_t=1/m$，对任何 $1-\delta>1/m$ 都有 $T_\delta=\infty$。这里 K=1 的 $p_t$ 是统一评估读出，不是其训练目标中的原生第二位置预测。

**证明。** 若 $h_z=a_tu_z$，规则单纯形使所有错误类别具有同一 logit。正确类别和任一错误类别的 logit 差为：

$$
\Delta_t=a_t\frac{mr^2}{m-1},
$$

由此得到上式中的 $p_t$。错误类别向量之和为 $-u_z$，所以 softmax 期望输出向量为：

$$
\sum_y p_t(y\mid h_z)u_y
=\frac{mp_t-1}{m-1}u_z.
$$

因此：

$$
-\nabla_{h_z}L_{info}
=\frac{\lambda}{m}
\left(u_z-\sum_y p_t(y\mid h_z)u_y\right)
=\frac{\lambda(1-p_t)}{m-1}u_z,
$$

轨迹保持在 $u_z$ 方向，并得到 $a_t$ 的递推式。达到 $p_t\ge1-\delta$ 所需的系数阈值为：

$$
a_\delta
=\frac{m-1}{mr^2}
\log\frac{(m-1)(1-\delta)}{\delta}.
$$

在命中阈值之前 $1-p_t>\delta$，故每一步 $a_t$ 至少增加 $\eta\lambda\delta/(m-1)$。用 $a_\delta$ 除以该最小增量即得步数上界。K=1 的共享目标对各分支给出相同更新，不能产生分支相关语义分量。证毕。

**推论 2（对齐多位置加速）。** 若多个有信息未来位置具有相同规则单纯形方向，并仅以非负权重 $\lambda_j$ 区别，则上述证明中的有效强度变为：

$$
\lambda_{eff}=\sum_{j\in\mathcal I_K}\lambda_j.
$$

命中时间上界随 $1/\lambda_{eff}$ 缩短。若方向不对齐，则不能用标量 $\lambda_{eff}$；必须回到第 8.5 节的向量和，冲突方向可能削弱净速度。

### 8.8 随机梯度下的条件性样本效率定理

若每一步使用一个独立训练样本或一个独立小批量，记该步沿语义 margin 的随机速度为 $\widehat G_t$。假设在达到阈值前：

$$
\mathbb E[\widehat G_t\mid\mathcal F_t]\ge\mu>0,
$$

并且噪声：

$$
\zeta_t=\widehat G_t-\mathbb E[\widehat G_t\mid\mathcal F_t]
$$

在给定历史 $\mathcal F_t$ 时是参数为 $\sigma^2$ 的次高斯随机变量。

**定理 3（高概率随机更新命中界）。** 假设 $M_K(0)<\gamma$，令 $D=(\gamma-M_K(0))/\eta$。对任意失败概率 $0<\rho<1$，只要随机更新步数 $n$ 满足：

$$
n\mu-\sigma\sqrt{2n\log(1/\rho)}\ge D,
$$

就有至少 $1-\rho$ 的概率在第 $n$ 步前达到 $M_K\ge\gamma$。一个显式充分条件是：

$$
n\ge
\left\lceil
\left(
\frac{
\sigma\sqrt{2\log(1/\rho)}
+\sqrt{2\sigma^2\log(1/\rho)+4\mu D}
}{2\mu}
\right)^2
\right\rceil.
$$

**证明。** 对首次命中时间停止后的过程应用第 8.6 节的精确累积式：

$$
M_K(n)-M_K(0)=\eta\sum_{t=0}^{n-1}\widehat G_t.
$$

条件次高斯鞅差的集中界给出，以至少 $1-\rho$ 的概率：

$$
\sum_{t=0}^{n-1}\widehat G_t
\ge n\mu-\sigma\sqrt{2n\log(1/\rho)}.
$$

若右侧至少为 $D$，则 margin 已越过 $\gamma$。令 $x=\sqrt n$ 并求解二次不等式即可得到显式充分条件。证毕。

这个定理第一次把“更省样本”拆成两个可测对象：平均语义漂移 $\mu$ 和语义梯度噪声 $\sigma$。MTP 的直接有信息项可以提高 $\mu$，但也可能增加 $\sigma$；因此真正的样本效率不由平均梯度单独决定，而由语义信号、噪声和初始阈值距离共同决定。若每步使用大小为 $b$ 的独立小批量，样本数是 $nb$，不能把更新步数直接当成样本数。当前实验只测得确定性或批平均速度，尚未验证该高概率界。

### 8.9 从隐藏状态定理提升到参数空间

令堆叠隐藏状态为 $H(\theta)=(h_1(\theta),\ldots,h_m(\theta))$，编码器雅可比和语义切向核为：

$$
J=\frac{\partial H}{\partial\theta},
\qquad
\Theta=JJ^\top\succeq0.
$$

将 $v=(v_1^{(K)},\ldots,v_m^{(K)})$ 堆叠。在分支折叠点，直接有信息损失的隐藏状态梯度可以写成：

$$
-\nabla_HL_{direct}=\frac1m v.
$$

参数梯度流下，直接项给出的 margin 瞬时速度为：

$$
G_{\theta,direct}
=\frac1{m^2}v^\top\Theta v
=\left\|\frac1mJ^\top v\right\|^2
\ge0.
$$

这说明直接项在参数空间不会自己变成负方向，但可能因 $J^\top v=0$ 而被编码器局部零空间完全阻断。标准训练还包含共享目标、其他位置损失和间接迁移。令它们的隐藏状态下降方向为 $g_{background}$，则：

$$
G_{\theta,background}
=\frac1m v^\top\Theta g_{background},
$$

$$
G_{\theta,total}
=G_{\theta,direct}+G_{\theta,background}.
$$

因此 MTP 是否学得更快，不只由输出方向 $v$ 决定，还由编码器对该方向的可训练程度和背景项决定。NTP 在当前前缀没有直接有信息目标，因此没有 $G_{\theta,direct}$；但全位置训练仍可能通过 $G_{\theta,background}$ 间接学到 $Z$。

A11_11 在 K=2 参考折叠模型中还能给出更精确的定律。共享 H1 目标在隐藏状态上的下降方向对各分支相同：

$$
c=(b,\ldots,b).
$$

因为 $\sum_zv_z=0$，有 $v^\top c=0$。所以 H1 在隐藏空间没有直接语义投影。令参考点雅可比干预为 $D_\alpha=P_\perp+\alpha P_v$，并定义：

$$
a=J_{raw}^\top v,
\qquad
d=J_{raw}^\top c.
$$

由于 $D_\alpha v=\alpha v$、$D_\alpha c=c$，可以精确证明：

$$
G_{\theta,direct}(\alpha)
=\frac{\alpha^2}{m^2}\|a\|^2,
$$

$$
G_{\theta,background}(\alpha)
=\frac{\alpha}{m^2}\langle a,d\rangle,
$$

$$
G_{\theta,total}(\alpha)
=\frac1{m^2}
\left(\alpha^2\|a\|^2+\alpha\langle a,d\rangle\right).
$$

定义核余弦和核范数比：

$$
\chi_\Theta
=\frac{\langle a,d\rangle}{\|a\|\|d\|},
\qquad
r_\Theta=\frac{\|d\|}{\|a\|}.
$$

当 $G_{\theta,direct}>0$ 时，加入 H1 后的净保留率为：

$$
\rho_{\theta,net}(\alpha)
=\frac{G_{\theta,total}(\alpha)}
{G_{\theta,direct}(\alpha)}
=1+\frac{\chi_\Theta r_\Theta}{\alpha}.
$$

这条定律把 A11_02b 的“梯度余弦是否有害”问题进一步拆清楚：$\chi_\Theta$ 决定背景项方向，$r_\Theta$ 决定背景项强度，而 $\rho_{\theta,net}$ 才决定局部净语义速度是否被反转。它还解释了为什么隐藏空间正交不代表参数空间无冲突：分支敏感的 $J$ 可以让 $J^\top v$ 与 $J^\top c$ 非正交。

对离散参数更新 $\theta^+=\theta-\eta\nabla_\theta L$，还要加入 $H(\theta)$ 的二阶余项：

$$
M_K(\theta^+)-M_K(\theta)
=\eta G_{\theta,total}+\eta^2R.
$$

A11_10 失败的是对参数传递、背景项和余项给出统一、非空且足够紧的经验界，不是否定隐藏状态空间定理。A11_11 已经证明参考点的局部代数关系，并通过远程四卡实验验证原生 $\|a\|$ 非平凡、$\rho_{\theta,net}(1)$ 为正，以及真实一步更新服从该方向。剩余问题是：在全位置训练中，direct 项、背景项和间接迁移项如何分解。

### 8.10 当前证明状态

| 命题 | 状态 | 条件边界 |
|---|---|---|
| 低有信息位置损失推出 $I(h_T;Z)$ 下界 | 已证明 | 一一编码目标，使用该位置交叉熵 |
| 覆盖首个有信息位置产生正一阶语义速度 | 已证明 | 分支折叠、固定输出方向的局部模型 |
| 一般 K 按有信息位置方向向量和改变速度 | 已证明 | 固定输出头的一步隐藏状态模型 |
| 正隐藏状态语义速度推出有限步 margin 命中上界 | 已证明 | 阈值前速度有正下界 |
| K=2 在规则单纯形模型中有限步恢复，而 K=1 的统一反事实语义读出不恢复 | 已证明 | 固定规则单纯形头、共享损失不进入语义子空间 |
| 对齐的多个有信息位置按总权重缩短上界 | 已证明 | 各位置语义方向相同且权重非负 |
| 正平均语义漂移和有界梯度噪声推出高概率样本命中界 | 已证明 | 阈值前条件均值下界与次高斯噪声假设 |
| K=2 参考折叠点的直接/背景参数传递定律 | 已证明 | 确定性分支前缀、固定正交 H1/H2 头、冻结 embedding/head、参考点雅可比干预 |
| 受控 reference-folded K=2 decision-only 参数传递 | 已验证 | A11_11 支持原生 $J^\top v$ 非零、$\rho_{\theta,net}>0$、一步更新服从局部速度；仍是受控参考点机制 |
| all-position Transformer 参数训练中分离 direct / background / indirect 项 | 未证明 | 缺少全位置背景损失和间接迁移的参数空间分解 |
| 自然语言 MTP 样本效率优于 NTP | 未证明 | 缺少真实语义变量、方向几何和分布外验证 |

## 9. 机制分解

| 机制环节 | 当前结论 | 主要量 | 当前证据 / 下一步 |
|---|---|---|---|
| 结构监督 | 覆盖 $\tau$ 才有直接语义目标 | $I(Z;Y_j\mid Y_{<j})$ | K=2/K=3 构造已支持 |
| 表示存在 | 低 $Y_\tau$ loss 推出 $h_T$ 含 $Z$ | $I(h_T;Z)$ 下界 | 旧定理已支持 |
| K=2 最小效率基元 | next-two 的 $Y_2=S_Z$ 项给 $h_T$ 严格正的一阶语义速度 | $G_2^{margin}$ | A11_01 / A11_03 支持：K=2 能比 fixed next-one 更早恢复 $Z$，但有优化不稳定 |
| 一阶效率 | K=3 梯度使 $M_Z$ 严格增长，K=1/K=2 为 0 | $G_M^{hidden}$ | 11_06 支持：K3 为 0.003816，K1/K2 近似 0 |
| 一般 K 方向叠加 | 多个有信息未来位置按中心化输出方向向量和贡献速度 | $G_K^{hidden}$，$G_K^{pred}$ | A11_08 / A11_09 支持：aligned 0.015262，low/conflict 0.000954，K3 turn on，shared H4 无增量 |
| 全位置 native/probe split | 非 direct loss 可让 $Z$ 可读，但不必然形成 native $h_T\to S_Z$ | $Q$，native H3，$M_Z^{ref}$ | A11_10 支持：K2 / masked K3 有非平凡 $Q$ 但 native H3=0，direct 条件 native H3=1 |
| 二阶可分性 | K=3 增加分支分离能量 | $E_Z$ 的速度 / 轨迹 | 11_06 辅助支持，K3 短曲线 $E_Z$ 增长 |
| 隐藏状态有限步效率 | 正语义速度是否累积成有限步 margin / 模型自身预测恢复 | $T_\gamma$，$T_\delta$ | 第 8.6 节给出精确累积式；第 8.7 节在规则单纯形 K=2 模型中给出显式步数上界 |
| 受控参数训练效率 | 直接条件是否有更小 $T_{0.9}$ / 更高早期 AUC | $Q(t),T_{0.9}$，模型自身 H3，$M_Z^{ref}$ | 11_07 / A11_10 支持直接条件更稳，但也显示间接迁移和证书松弛 |
| 参数空间传递 | 隐藏状态语义信号能否经过编码器参数化后保持正净速度 | $\kappa_2$，$\rho_{\theta,net}$，$\chi_\Theta$，$r_\Theta$，$R_2$ | A11_11 支持：原生直接项为正、full K2 净速度为正、一步更新保真 |
| 全位置参数分解 | all-position 中 direct 项、背景项和间接迁移如何共同改变 $h_T$ | direct $G_\theta$、background $G_\theta$、indirect transfer、native readout | 下一步；尚未证明 |

## 10. Anchor 证据链

现有证据链应这样读：

1. 11_01 证明并验证 K=2 objective-level separation：next-two 学会共享 $Y_1$ 的同时，让 $h_T$ 对 $S_Z$ 可预测、可探针、可 branch-swap。
2. 11_02 说明第二未来词元必须含有新分支信息，且梯度冲突不等于有害。
3. 11_02b 补齐导师设计：A-clean 的模型自身预测、probe、branch swap 和最终任务定向梯度共同支持有用信号；$\lambda$ 审计显示 next-token 交叉熵有小幅局部减速，但最终准确率不受损。
4. 11_03 把 K=2 推到学习曲线，但稳定性不足。
5. 11_04 验证 first-informative-horizon，即 $\tau=3$ 时只有 K=3 在单决策前缀中直接覆盖 $S_Z$。
6. 11_05 在全位置训练中分离直接项与间接迁移，支持“当前决策前缀第 3 位置监督”是 K=3 优势的机制组件。
7. 11_06 验证新理论量：一阶读出有效 margin 增长。结果支持：K3 的 $G_M^{hidden}$ 为正，K1/K2 近似为 0。
8. 11_07 回到无泄漏全位置训练，判断该一阶优势是否转化为多步效率。结果支持 direct 条件更强，但同时确认 all-position indirect transfer 仍然存在。
9. 11_08 将 K=3 机制推广到一般 K：在同样 `K=4` 和同样两个有信息未来位置下，读出方向 aligned 与 low/conflict 会产生不同的一阶隐藏状态语义速度，结果支持向量和公式。
10. 11_08b 检查 A11_08 是否只是 step-0 静态 output geometry，结果支持 frozen-head 下的 hidden velocity 机制，同时发现 trainable head 会漂移。
11. 11_09 验证 next-K inclusion law：K 只在新增有信息 horizon 时打开或改变语义速度；新增 shared horizon 没有直接一阶语义增量，新增 aligned / low-conflict 信息 horizon 分别增强 / 削弱。
12. 11_10 验证全位置模型自身预测 / 探针可读性分离：直接条件产生模型自身 H3 预测与大 $M_Z^{ref}$，非直接条件可以有非平凡 $Q$，但模型自身 H3 为 0、$M_Z^{ref}$ 近 0。
13. 11_10 finite-step audit 验证直接有信息条件在早期窗口保持正 $G_K^{ref}$，但原参数空间曲率证书过松。本版理论说明：隐藏状态空间的有限步累积是精确的；A11_11 随后补上受控 decision-only 的编码器切向核传递证据，剩余缺口转为 all-position 背景干扰、间接迁移和非线性余项的分解。
14. 11_11 证明并验证 K=2 参考折叠点的参数传递规律：直接项按 $\alpha^2$、分支公共 H1 背景项按 $\alpha$ 缩放，且 $\rho_{\theta,net}=1+\chi_\Theta r_\Theta$。远程四卡结果支持原生共享编码器的 $J^\top v$ 非零，full K2 净速度为正，真实一步更新服从 $\eta G_{\theta,total}$。

## 11. 实验结果整合

A11_01 / A11_03 的关键信息是：K=2 是最小可验证基元。A11_01 中 fixed-next-one 学会共享 $Y_1=A$ 但保持 branch-blind，而 next-two 的 offset-2 accuracy、frozen probe、branch-swap consistency 都达到 1.0。A11_03 进一步显示，在 clean K=2 decision-only 中，next-two 比 fixed-next-one 有更高早期 AUC 和 reach rate；但 identical initialization 下只成功 2/5 seeds，因此它支持“直接监督有用”，不支持“优化必然成功”。

A11_02b 把 K=2 导师设计补齐。在 all-position A-clean shared K=2 中，head-2 / probe / branch swap 都为 `1.00`；C-noisy 的 head-2 只有 `0.0656`，接近 $1/16$ 机会水平，但 probe 为 `0.875`，再次说明 probe 不能单独证明模型使用。A-clean 最终 $U_2>0$ 为 `10/10`，与冻结读出梯度的方向余弦为 `0.983`。同时，$\lambda=0.25,0.5,1.0$ 相对 NTP 的标准化 $L_1$ AUC 成本为 `0.59% / 0.83% / 1.07%`，最终 Y1 accuracy 仍为 `1.00`。因此共享目标冲突有可测的小幅局部代价，但不是最终性能失败。

A11_04 的关键信息是：当第一个有信息未来位置后移到 $\tau=3$，decision-only 中 K=1/K=2 不恢复，K=3 恢复；all-position 中 K=3 仍最强，但 K=1/K=2 可通过间接迁移恢复。因此 $\tau$ 后移实验把 K=2 基元推广成 first-informative-horizon 规律，同时给出了 all-position claim boundary。

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

A11_08b 的关键信息是：A11_08 的方向机制不是纯 step-0 artifact。冻结 output heads 时，`aligned_h3_h4` 的 early AUC `G_hidden_ref=0.002660`，`low_conflict_h3_h4=0.000184`，且 `5/5` seeds 支持 aligned 更大。但可训练 head 下 `low_conflict_h3_h4` 的 `cos_34` 从 `-1.000` 漂移到 `-0.268`，所以多步 trainable 曲线必须记录 current geometry，不能只用初始化几何解释。

A11_09 的关键信息是：next-K inclusion law 通过。`single_h3` 中 one-step `G_hidden` 为 `K2=0, K3=0.003816, K4=0.003816`，说明首次覆盖有信息 H3 时语义速度打开，新增 shared H4 没有直接增量；`aligned_h3_h4` 为 `0, 0.003816, 0.015262`，说明新增对齐信息位置增强；`low_conflict_h3_h4` 为 `0, 0.003816, 0.000954`，说明新增冲突信息位置削弱。这个结果把“固定 K=4 方向几何”推进成“next-K 增量规律”。

A11_10 的关键信息是：全位置训练里必须把 guarded recovery 和 native direct readout 分开。`K2_active` 与 `K3_mask_decision_prefix_L3` 的 final Q 为 0.75 / 0.70，但 native H3 为 0，final $M_Z^{ref}$ 为 0 / 0.004；`K3_active` 与 `K2_plus_decision_prefix_L3` 的 final Q 都为 1.0，native H3 都为 1.0，final $M_Z^{ref}$ 为 2.430 / 3.766。本地守卫通过：所有条件最终 Y1/Y2 accuracy 都为 1.0。因此 direct H3 是当前受控设置中产生 native readout 和大 margin 的可靠路径，而 non-direct all-position loss 可以产生 probe-readable recovery。

A11_10 finite-step audit 的关键信息是：所有直接有信息条件在 `5/5` 个 seed 的审计早期窗口都保持正语义速度；全位置 `K3_active` 和 `K2_plus_direct_H3` 都达到最终模型自身 H3 准确率 `1.0` 与 $Q=1.0$。但经验曲率修正后的参数空间证书经常非正，或给出远大于实际训练长度的上界。因此实验支持“正方向持续并伴随更强恢复”，不支持“已经得到紧的 Transformer 命中时间上界”。

### 11.1 A11_11：K=2 语义信号能否传入 Transformer 参数

**实验问题。** 隐藏状态上的正语义速度并不自动意味着可训练的 Transformer 参数能产生同方向更新。A11_11 因此只问：冻结词嵌入和预测头后，K=2 的直接语义信号是否能通过共享编码器参数传递，并在加入共享 $Y_1=A$ 损失后保持正净速度。

**最小设置。** 数据为 $Y_1=A,\;Y_2=S_Z$，包含四个确定性分支；模型是一层因果 Transformer。参考折叠令各分支在 step 0 的隐藏状态与预测完全相同，再用 $\alpha\in\{0,0.5,1\}$ 只控制编码器雅可比沿语义方向的强度。比较共享第一词元损失、仅第二词元直接损失、二者之和三类目标。

**主指标。** 参数语义速度定义为：

$$
G_{\theta,total}
=-\langle\nabla_\theta M_2,\nabla_\theta L_{total}\rangle
=G_{\theta,direct}+G_{\theta,background}.
$$

其中 $G_{\theta,direct}$ 测第二词元 $S_Z$ 对语义 margin 的直接推动，$G_{\theta,background}$ 测共享第一词元损失经过参数共享后形成的帮助或抵消。一步保真度比较真实变化 $\Delta M_2$ 与一阶预测 $\eta G_{\theta,total}$。

**结果。** 远程四卡任务 `pt-50l5l908` 完成 `35/35` 个任务，五个随机种子全部通过实现校准。

| 判定量 | 实测结果 | 说明 |
|---|---:|---|
| 原生直接参数语义速度 $G_{\theta,direct}(1)$ | 均值 `0.056388`，最小值 `0.038651`，`5/5` 为正 | 共享编码器对语义方向不是局部零空间 |
| 原生背景速度 $G_{\theta,background}(1)$ | `[-0.005970, 0.014910]` | 共享目标可帮助也可抵消，符号本身不是最终判据 |
| 原生净速度 $G_{\theta,total}(1)$ | 均值 `0.059908`，最小值 `0.045335`，`5/5` 为正 | 本实验中背景项没有反转直接语义速度 |
| 净保留率 $\rho_{\theta,net}(1)$ | 均值 `1.089587`，最小值 `0.886259` | 所有种子都保留正净语义速度 |
| 半尺度直接项比值 | `0.25`，`5/5` 一致 | 符合已证明的 $\alpha^2$ 实现校准规律 |
| 半尺度背景项比值 | `0.50`，`5/5` 一致 | 符合已证明的 $\alpha$ 实现校准规律 |
| 一步方向一致 | `20/20` | 真实一步更新与一阶预测同号 |
| 一步最大相对误差 | `0.033786` | 低于协议阈值 `0.25`，当前步长下二阶余项没有主导 |

![A11_11 参数语义传递与有限步动力学](../../../../experiments/A11/A11_11_k2_semantic_tangent_kernel_transmission/figures/a11_11_transmission_and_dynamics.png)

读图时，上左检查直接项的 $\alpha^2$ 与背景项的 $\alpha$ 缩放；上右比较每个随机种子的直接、背景和净速度；下左比较一步真实 margin 变化与一阶预测；下右检查早期训练是否保持 $\alpha=1>0.5>0$ 的 margin 顺序。

**联合结论。** 代数缩放规律本身是参考干预内置的实现守卫，不是实验发现；真正的实验发现是原生 $J^\top v$ 非零、净参数语义速度在 `5/5` 个种子中为正，而且真实一步更新服从该局部方向。因此，K=2 直接语义信号不仅存在于隐藏状态目标中，也确实能在这个受控单决策前缀设置下传入共享编码器参数。

**边界。** 该结果没有证明全位置语言模型训练保留同样的分解，也没有测量随机小批量下的样本命中时间。一个种子的最终第二词元准确率为 `0.5`，但其 margin 仍为正；这提醒我们 A11_11 判定的是局部参数传递和一步保真度，不是每个种子 200 步都收敛。

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

1. K=2 是最小理论基元：当 $Y_1$ 共享、$Y_2=S_Z$ 时，next-two 给 $h_T$ 直接语义监督，而 next-one 在同一前缀上没有该项。
2. 低第 $\tau$ 未来位置损失推出 $h_T$ 含有 $Z$。
3. 在最小可训练前缀表示模型中，覆盖第一个有信息未来位置会带来严格正的一阶读出有效 margin 增长；非覆盖目标只给公共更新。
4. 在直接优化隐藏状态、固定语义读出方向时，margin 的每步增量精确等于 $\eta G_K^{hidden}$；若速度有正下界，就得到有限步命中时间上界。
5. 在规则单纯形输出几何、共享损失不进入语义子空间的 K=2 模型中，MTP 有显式有限步模型自身预测恢复上界，而 NTP 的分支语义分量保持为零。
6. 在随机梯度模型中，若平均语义漂移为正且噪声次高斯，则可以得到由 $\mu$、$\sigma$ 和阈值距离共同控制的高概率随机更新命中界。这是条件性结论，不是当前实验已经验证的样本效率结论。
7. 一般 K 的直接效率由有信息未来位置的中心化输出方向向量和决定；新增共享位置无直接增量，新增冲突方向可能削弱净速度。
8. 11_06 至 A11_10 的受控实验共同支持：直接有信息目标产生正且早期持续的语义速度，并对应更强的模型自身预测和语义 margin；全位置非直接损失仍可通过参数共享让 $Z$ 对探针可读。
9. A11_11 支持：在受控 reference-folded K=2 decision-only 设置中，直接语义方向 $v$ 能通过共享编码器雅可比形成正的参数语义速度；共享 H1 背景项可正可负，但本 run 中没有反转 full K2 净速度。

不能说：

1. MTP 在自然语言中已经优于 NTP。
2. NTP 学不到长程语义。
3. K 越大越好。
4. 全位置训练中非覆盖 K 不能恢复 $Z$。
5. $Q$ 单独证明直接语义监督。
6. 隐藏状态空间定理已经自动提升为一般 Transformer 参数空间定理；A11_11 只验证了受控 reference-folded K=2 decision-only 局部传递，尚未覆盖 all-position、随机批量、AdamW 或自然语言。
7. 当前已经实验证明更省样本；第 8.8 节只是带明确随机梯度假设的条件性定理。
8. A11 已经证明 MoE 路由保持或专家收益。
9. 自然语言中的多个未来目标方向天然对齐。
10. 当前已经给出真实长文档任务上的 MTP 优势；第 2.1-2.3 节只是目标定义和判定梯子。

## 14. Anchor 分解和下一步

| Anchor | 决策问题 | 为什么需要 | 主指标 | 失败含义 |
|---|---|---|---|---|
| 11_06：读出有效 margin 效率 | 第 $\tau$ 未来位置监督是否产生严格正的一阶读出有效 margin 增长？ | 把表示定理推进到优化效率量 | $G_M^{hidden}$，$M_Z^{ref}$，$E_Z$，local guard | 已支持：K3 正，K1/K2 近 0 |
| 11_07：无泄漏全位置效率 | 在 $Q(0)$ 不饱和时，11_06 机制是否转化为更强 all-position recovery？ | 把一步机制放回 LM-style 训练 | $Q(0)$，$T_{0.9}$，早期 AUC，native H3，$M_Z^{ref}$，本地损失 | 已支持 direct 条件更强；同时确认 indirect transfer |
| 11_08：一般 K 读出方向动力学 | 多个有信息未来位置是否按读出方向向量和贡献一阶速度？ | 避免把结论误写成 K 越大越好 | $G_K^{hidden}$，几何预测，seed 方向一致性，本地损失 | 已支持：aligned 高于 low/conflict，shared 为 0，single 为正 |
| 11_08b：output geometry dynamics audit | A11_08 的方向几何是否只是 step-0 静态构造？ | 区分 hidden velocity 机制和 output-head co-adaptation | $G_{hidden}^{ref/current}$，$M_Z^{ref/current}$，$\cos_{34}$，head drift | 已支持 frozen-head velocity 机制；可训练 head 曲线必须记录 current geometry |
| 11_09：next-K inclusion law | K 增大时，语义速度是否只在覆盖有信息位置时打开，并按新增方向变化？ | 把固定 K=4 的方向规律变成 next-2 / next-3 / next-K 规律 | turn-on、no-increment、vector-increment、local guard | 已支持：K2 近 0，K3 turn on，shared H4 无直接增量，aligned 增强，low/conflict 削弱 |
| 11_10：全位置间接迁移动力学 | 全位置非 direct recovery 是否等同于 native direct readout？ | 把 $Q$ 与 native H3 / margin 分开 | $Q$，native H3，$M_Z^{ref}$，local guard | 已支持：非 direct 可有 $Q$ 但 native/margin 近 0，direct 条件 native/margin 强 |
| 11_10 finite-step：有限步效率审计 | 一阶语义速度优势在参数训练中能否给出可用命中界？ | 定位隐藏状态理论与参数训练之间的缺口 | $T_\gamma$，margin-growth 下界，head drift | 速度持续得到支持；参数空间曲率证书过松 |
| 11_11：K=2 语义切向核传递 | 直接语义信号能否经过编码器雅可比形成可预测的参数空间速度？ | 把隐藏状态有限步定理提升到参数训练的第一步 | $G_\theta$，$\kappa_2$，$\rho_{\theta,net}$，$\chi_\Theta$，$r_\Theta$，$R_2$ | 已支持：direct 原生速度为正，full K2 净速度为正，一步更新保真 |
| 11_12：全位置参数分解 | all-position 训练中，direct、background、indirect transfer 能否被参数空间分开？ | 把 11_11 的 decision-only 传递机制放回 LM-style 训练 | direct/background/indirect 的 $G_\theta$ 分解，native readout，local LM guard | 下一步；若失败，不能把 decision-only 参数传递推广到全位置效率 |

## 14.5 下一步理论规划

当前最清楚的机制句是：

> MTP 的目标优势来自有信息未来词提供的直接语义方向 $v$；隐藏状态上的有限步增长由 $v$ 决定，而 Transformer 参数训练中的实际增长还要乘上编码器对该方向的传递能力，并减去其他损失干扰与非线性余项。

现在 A11_11 已支持受控 decision-only 的参数传递。下一步不应扩展 K，也不应先做自然语言实验，而应把同一分解放回全位置训练。

**唯一决策问题：** 在 $Y_1=A,Y_2=S_Z$ 的最小构造中，all-position LM-style 训练里的当前决策状态 $h_T$ 语义变化，能否分解为直接 decision-prefix K=2 项、其他位置背景项和间接迁移项？

核心分解仍是：

$$
G_\theta
=G_{\theta,direct}+G_{\theta,background}.
$$

但现在要把 $G_{\theta,background}$ 进一步拆开：

$$
G_{\theta,total}^{all}
=G_{\theta,direct\ at\ T}
+G_{\theta,other\ positions}
+G_{\theta,local\ shared}
+R_{\theta,nonlinear}.
$$

需要记录的量是：

1. $\kappa_2=v^\top\Theta v/\|v\|^2$：模型参数能否沿目标给出的语义方向改变 $h_T$。
2. $G_{\theta,background}$：共享 H1 目标经过雅可比后对语义速度的帮助或抵消。
3. $\chi_\Theta$：语义方向与共享目标方向经过雅可比后的参数梯度余弦。
4. $r_\Theta$：共享目标参数梯度相对语义参数梯度的范数比。
5. $R_2$：离散参数更新后，线性预测与真实 margin 变化之间的二阶余项。

其中 1-5 已在 A11_11 的 decision-only 参考折叠设置中验证。全位置版本要额外记录：

6. 其他位置损失对当前 $h_T$ 语义 margin 的参数速度。
7. 当前 decision-prefix direct 项被 mask 后，$Q$、native H2 / H3 与 $M_Z$ 是否仍能通过 indirect transfer 恢复。
8. local next-token loss / accuracy 是否保持，防止把语义速度误读为局部 LM 退化。

不用重复证明 A11_11 的 $\alpha$ 比例关系。最小可证伪设计应保持 K=2、clean 数据、固定输出头和冻结 embedding；只改变 loss mask，把当前位置 direct 项、其他位置含 $Z$ 的项、共享本地项分开。A11_11 中的参考折叠公式仍作为 step-0 守卫：

$$
\kappa_2(\alpha)\propto\alpha^2,
\qquad
G_{\theta,direct}(\alpha)\propto\alpha^2,
\qquad
G_{\theta,background}(\alpha)\propto\alpha.
$$

在 A11_11 的参考折叠模型中，这个比例关系已经被证明和验证：

$$
G_{\theta,direct}(\alpha)
=\frac{\alpha^2}{m^2}v^\top\Theta_{raw}v
=\alpha^2\left\|\frac1mJ_{raw}^\top v\right\|^2.
$$

所以后续实验不再把 $\alpha^2$ 当作科研发现；它只是实现校准。真正未知的是：全位置训练中，当前决策前缀 direct 项是否仍是主要正项，其他位置损失是帮助、抵消，还是通过间接迁移制造 probe-readable 但 non-native 的恢复。

在 $\alpha=1$ 上，净速度是否反转由下式精确判断：

$$
\rho_{\theta,net}
=1+\chi_\Theta r_\Theta.
$$

因此负余弦本身仍不等于有害；只有余弦、相对范数和真实有限步变化联合起来，才能说明共享目标是否抵消 MTP 的直接语义速度。

该下一步可以区分三种失败：若 decision-only 传递成立但 all-position direct 项被其他位置抵消，瓶颈在全位置背景干扰；若 direct 项存在但 non-direct mask 也产生高 $Q$ 而 native readout 不变，说明 indirect transfer 主要制造 probe-readable recovery；若所有参数速度都正但训练曲线不跟随，瓶颈在核漂移或非线性余项。只有全位置参数分解通过后，才进入样本效率的 $\mu/\sigma$ 审计或真实语义任务。

## 15. 与主线的关系

项目主线仍是 top-1 MoE 路由中的特征级专家专业化，当前瓶颈是保持性。A11 不是替代主线，而是目标函数层面的候选机制：如果 MTP 能更早、更读出有效地把长程变量写入当前状态，它未来可能帮助形成更稳定的 route-relevant hidden states。

但这不是当前下一步。A11 已经把 K=2、$\tau=m$、一般 K 的隐藏状态机制，以及受控 decision-only 的参数传递机制统一起来；现在应先判断这条语义方向在 all-position 训练中如何与背景损失和间接迁移相互作用。只有全位置参数分解成立，A11 才有资格继续讨论样本效率或是否会形成可迁移的路由相关隐藏状态。

## 16. 下一步唯一决策

当前唯一下一步：

> 构造并执行 11_12 全位置参数分解：在 K=2 clean 构造中，把当前决策前缀 direct 语义项、其他位置损失、共享本地项和间接迁移分开，判断 A11_11 的正参数传递是否能在 LM-style all-position 训练中作为主要机制保留下来。

不要再只重复全位置 $Q$ 曲线，也不要现在转向 MoE。隐藏状态空间有限步定理已经完成，decision-only 参数传递已经通过；现在要回答的是 all-position 里的直接项和间接项如何共同作用。若 11_12 通过，再讨论样本效率的 $\mu/\sigma$ 审计；若失败，就把效率结论限制在受控 decision-only 参数传递，而不推广到 LM-style 训练。

## Source Map

- `sync/S000_current_specialization/stories/11_long_horizon_mtp_objective/story_cn.md`
- `sync/S000_current_specialization/anchors/11_long_horizon_mtp_objective/11_05_semantic_efficiency_bridge_anchor.md`
- `sync/S000_current_specialization/anchors/11_long_horizon_mtp_objective/README.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_01_k2_branch_delayed_next_two_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/detailed.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_02_two_token_shared_trunk_signal_interference_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/detailed.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_02b_advisor_design_completion_audit_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02b_advisor_design_completion_audit/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02b_advisor_design_completion_audit/detailed.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_03_k2_semantic_efficiency_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/detailed.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_04_k3_first_informative_horizon_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/detailed.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_05_semantic_efficiency_bridge_anchor.md`
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
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_08b_output_geometry_dynamics_audit_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_08b_output_geometry_dynamics_audit/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_08b_output_geometry_dynamics_audit/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_08b_output_geometry_dynamics_audit/detailed.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_11_k2_semantic_tangent_kernel_transmission_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_11_k2_semantic_tangent_kernel_transmission/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_11_k2_semantic_tangent_kernel_transmission/protocol_cn.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_11_k2_semantic_tangent_kernel_transmission/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_11_k2_semantic_tangent_kernel_transmission/detailed.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_09_next_k_inclusion_law_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_09_next_k_inclusion_law/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_09_next_k_inclusion_law/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_09_next_k_inclusion_law/detailed.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_10_all_position_indirect_transfer_dynamics_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_10_all_position_indirect_transfer_dynamics/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_10_all_position_indirect_transfer_dynamics/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_10_all_position_indirect_transfer_dynamics/detailed.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_10_finite_step_semantic_efficiency_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_10_finite_step_semantic_efficiency/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_10_finite_step_semantic_efficiency/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_10_finite_step_semantic_efficiency/detailed.md`
