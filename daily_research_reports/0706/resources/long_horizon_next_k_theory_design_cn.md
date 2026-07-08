# 长时距预测与 Next-k-Token 课程训练：问题定义、数学模型、形式分析与经验测试

创建时间：2026-07-06

## 0. 术语解释

| 术语 | 中文含义 | 具体对象 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 词元（token） | 模型读写的最小文本单位 | $x_1,x_2,\ldots$ | 语言模型训练和预测的基本对象 | 不等于完整语义概念 |
| 下一词元预测（next-token prediction, NTP） | 用当前位置的上下文只预测下一个 token | 从 $h_T$ 预测 $x_{T+1}$ | 当前主流语言模型训练目标 | 不保证早期状态保存远未来信息 |
| 多词元预测（multi-token prediction, MTP） | 用同一个隐藏状态预测多个未来 token | 从 $h_T$ 同时预测 $x_{T+1},\ldots,x_{T+k}$ | 给同一状态施加多个未来监督 | 不保证所有任务都优于 NTP |
| Next-k-token prediction | MTP 的一种具体形式：预测未来 $k$ 个 token | $h_T\to x_{T+1:T+k}$ | 本文理论分析的核心对象 | 不等于无限长预测能力 |
| 长时距依赖（long-horizon dependency） | 早期 token 影响很远之后的 token | $x_1$ 决定 $x_{T+1}$ 或后缀 | 判断 MTP 是否有优势的关键场景 | 不代表所有长文本任务 |
| 隐藏状态（hidden state） | 模型读完某个前缀后的内部表示 | $h_T=f_\theta(X_{\le T})$ | 远未来信息是否被保留，要看它 | 隐藏状态可分离不等于可用 |
| 因果序列模型（causal sequence model） | 预测当前位置之后 token 时，只能看之前 token 的模型 | Transformer decoder 类模型 | 符合语言模型训练设定 | 不说明模型一定学到因果机制 |
| 分支键（branch key） | 早期决定未来走向的变量 | $B=X_1$ | 长时距信息的来源 | 不一定是真实语言中的语义原因 |
| 填充 token（filler tokens） | 位于分支键和预测位置之间、原则上不透露分支的信息 | $X_2,\ldots,X_T$ | 用来制造长距离和局部干扰 | 真实文本中中间内容未必无关 |
| 未来后缀（future suffix） | 预测位置之后的一串 token | $Y_{1:k}=X_{T+1:T+k}$ | MTP 要预测的多个未来目标 | 后缀预测成功不等于通用推理成功 |
| 预测时距（horizon） | 从当前状态向后预测的距离 | offset $j$ 或最大 $k$ | 表示预测有多远 | 时距大不一定信息更难 |
| 偏移（offset） | 第几个未来 token | $Y_j=X_{T+j}$ | 区分 $x_{T+1}$、$x_{T+2}$ 等目标 | 单个偏移不能代表完整后缀 |
| 交叉熵（cross-entropy, CE） | 预测分布对真实 token 的损失 | $\mathrm{CE}(p,y)$ | 训练目标的基本损失 | 低 CE 不必然说明机制正确 |
| 梯度（gradient） | 损失对参数或表示的改变方向 | $\nabla_{h_T}\ell_j$ | 分析训练压力从哪里来 | 梯度方向不等于最终表示一定形成 |
| 分支相关梯度 | 推动模型保存或暴露分支信息的梯度部分 | $\alpha_j u_B$ | MTP 优势的理论来源 | 需要假设多个未来目标梯度对齐 |
| 噪声梯度 | 与分支无关或干扰优化的梯度部分 | $\eta_j$ | 决定信号是否被淹没 | 不能单独解释全部训练动态 |
| 信噪比（signal-to-noise ratio, SNR） | 有用分支信号相对无关噪声的强度 | $\mathrm{SNR}_k$ | 衡量 MTP 是否增强长时距信号 | 是简化分析，不是完整优化理论 |
| 互信息（mutual information） | 两个变量共享多少信息 | $I(B;h_T)$ | 衡量隐藏状态是否含分支信息 | 互信息高不等于输出头能用 |
| Fano 型推理 | 用预测错误率下界反推表示必须含有多少信息 | $I(h_T;B)\ge ...$ | 连接预测准确率和表示信息量 | 依赖简化假设 |
| 单前缀后缀预测 | 固定同一个前缀隐藏状态，直接预测未来后缀 | 从 $h_T$ 预测 $Y_{1:k}$ | 比自回归展开更能检测长时距表示 | 不等于真实生成性能 |
| 教师强制续写（teacher-forced continuation） | 预测每一步时都给模型真实前文 | 训练或评估时看到真实历史 token | 容易表现好，因为每步都可用真实上下文 | 不能证明早期状态保存远未来信息 |
| 自回归展开（autoregressive rollout） | 模型一步步生成，每一步使用自己已生成的 token | 生成 $x_{T+1}$ 后再生成 $x_{T+2}$ | 测试生成链条是否能继续 | 不保证 $h_T$ 已含完整未来信息 |
| 分支置换测试（branch-swap test） | 只换早期分支 token，观察后缀预测是否改变 | $BR_1\to BR_2$ | 检查预测是否真的依赖早期变量 | 不能证明真实语义机制 |
| 课程训练（curriculum） | 训练中逐步增加预测难度或预测距离 | 先预测 1 个，再预测更多 | 检查逐步增加 horizon 是否有帮助 | 不保证优于一开始 full horizon |
| 谱诊断（spectral diagnostics） | 查看矩阵奇异值等几何结构 | LM head、future heads、attention matrices | 判断表示和输出方向是否改变 | 谱变化本身不是性能证明 |

## 0.1 目的梳理

这份文档的目的，是把导师提出的直觉变成一个可证明、可实验检验的问题。

普通下一词元预测并不是完全没有长时距信号；如果 $x_{T+1}$ 真的依赖 $x_1$，那么下一词元预测的损失里确实有这个信号。问题是，在长序列中，大量局部 token 的预测更密集、更容易，长时距信号可能被局部梯度淹没。

本文要证明和测试的是：

当多个未来 token 都由同一个早期变量决定时，next-k-token prediction 会把多个未来损失同时作用到同一个隐藏状态 $h_T$ 上，从而比只预测下一个 token 更强地推动 $h_T$ 保存早期分支信息。

核心判断不是看普通困惑度，也不是看 teacher-forced 续写，而是看：同一个前缀隐藏状态能不能直接预测分支特定的未来后缀。

## 1. 问题定义

中心研究问题是：多词元预测是否比普通下一词元预测，对长时距依赖产生更强的学习压力。

考虑一个极长上下文，长度为 $T$，例如 $T=1,000,000$。模型观察到：

$$
x_1,x_2,\ldots,x_T
$$

并且必须预测：

$$
x_{T+1}
$$

如果 $x_{T+1}$ 依赖于像 $x_1$ 这样的早期 token，而不是只依赖 $x_T$ 附近的局部上下文，那么这个预测就是长时距预测。

最简单的长时距依赖形式是：

$x_1=$ 分支键，中间出现许多填充 token，而 $x_{T+1}$ 由这个分支键决定。

更强的版本，也是和多词元训练最相关的版本，是：

$x_1=$ 分支键，中间出现许多填充 token，而整个未来后缀 $x_{T+1:T+k}$ 都由这个分支键决定。

核心假设是：

**当多个未来 token 依赖同一个早期变量时，next-k-token prediction 可以比 next-token prediction 对位置 $T$ 的隐藏状态产生更强压力，使它保存早期分支信息。**

这里，next-k-token prediction 指的是同一个因果隐藏状态 $h_T$ 被训练来预测多个未来 token：

$$
h_T\to x_{T+1}
$$

$$
h_T\to x_{T+2}
$$

$$
\ldots
$$

$$
h_T\to x_{T+k}
$$

这不同于普通下一词元语言建模。普通语言建模只训练 $h_T$ 预测 $x_{T+1}$。

## 2. 先验直觉

普通下一词元预测并不是不能学习长时距依赖。如果 $x_{T+1}$ 确实依赖 $x_1$，那么位置 $T$ 的下一词元损失确实包含长时距训练信号。

问题是信号稀释。在长序列中，大多数下一词元损失都可以通过学习局部结构来降低，例如：

- 局部语法；
- 局部短语续写；
- 局部填充 token 转移；
- 短程语义一致性；
- 高频模板。

这些局部损失密集且容易。它们可能主导优化轨迹。长时距信号存在，但它很稀疏，并且相对于局部梯度可能较弱。

Next-k-token prediction 改变了一个前缀状态上的压力。它不再只要求 $h_T$ 预测下一个 token，而是要求同一个 $h_T$ 暴露足够信息来预测多个未来 token。如果这些未来 token 共享同一个早期原因，那么它们的损失会产生多个方向一致的梯度信号，推动模型保存这个早期原因。

重要区别是：

下一词元预测：

$$
h_T \text{ 只需要支持 } x_{T+1}.
$$

Next-k-token prediction：

$$
h_T \text{ 需要支持 } x_{T+1},x_{T+2},\ldots,x_{T+k}.
$$

如果 $x_{T+1:T+k}$ 是一个分支特定后缀，那么 next-k 训练会增强 $h_T$ 编码分支键的压力。

## 3. 最小生成模型

我们定义一个受控序列分布。

令早期分支变量为：

$$
B=X_1\in\{1,2,\ldots,M\}.
$$

这里，$B$ 是第一个 token，或者是一个早期潜在分支键；$M$ 是可能分支的数量。

中间上下文是填充 token：

$$
X_2,\ldots,X_T\sim P_{\mathrm{filler}}.
$$

这里，$P_{\mathrm{filler}}$ 是一个不会透露分支键的填充分布。在最干净的模型中，$X_2,\ldots,X_T$ 在给定条件下与 $B$ 独立。

未来后缀由分支决定：

$$
Y_{1:k}=X_{T+1:T+k}=s_B.
$$

这里，$Y_{1:k}$ 是长度为 $k$ 的未来后缀，$s_B$ 是与分支 $B$ 对应的分支特定后缀。

例如：

$$
B=BR_1\to s_B=E\ F\ G\ H\ I\ J\ K\ L\ .
$$

$$
B=BR_2\to s_B=M\ N\ O\ P\ Q\ R\ S\ T\ .
$$

$$
B=BR_3\to s_B=U\ V\ W\ X\ Y\ Z\ AA\ AB\ .
$$

模型是一个因果序列模型。读完前缀之后，它产生隐藏状态：

$$
h_T=f_\theta(X_{\le T}).
$$

这里，$h_T$ 是预测位置的隐藏状态，$f_\theta$ 是因果 Transformer 或任意因果编码器，$X_{\le T}$ 是已观察到的上下文。

问题是：$h_T$ 是否足够强地保存了分支键 $B$，从而能够预测后缀 $s_B$。

## 4. 训练目标

### 4.1 普通下一词元预测

长时距位置上的下一词元损失是：

$$
L_1(\theta)=\mathrm{CE}(p_{\theta,1}(Y_1\mid h_T),Y_1).
$$

这里，$Y_1=X_{T+1}$ 是第一个未来 token，$p_{\theta,1}$ 是偏移 1 的预测分布，$\mathrm{CE}$ 是交叉熵。

这个目标只要求 $h_T$ 支持第一个未来 token。

### 4.2 Next-k-token prediction

同一个前缀状态上的 next-k-token 损失是：

$$
L_k(\theta)=\sum_{j=1}^{k}\lambda_j \mathrm{CE}(p_{\theta,j}(Y_j\mid h_T),Y_j).
$$

这里，$Y_j=X_{T+j}$ 是第 $j$ 个未来 token，$p_{\theta,j}$ 是偏移 $j$ 的预测分布，$\lambda_j$ 是分配给偏移 $j$ 的权重。

最简单版本中，所有权重都设为 1：

$$
\lambda_1=\lambda_2=\cdots=\lambda_k=1.
$$

这个目标要求同一个隐藏状态 $h_T$ 支持完整未来后缀。

### 4.3 确定性课程 next-k 目标

确定性课程训练会逐步增加激活的预测时距：

$$
h(t)=\min(1+\lfloor t/S\rfloor,k_{\max}).
$$

这里，$t$ 是训练步数，$S$ 是每个 horizon 阶段的步数，$k_{\max}$ 是最大预测时距。

训练步 $t$ 的损失是：

$$
L_{h(t)}(\theta)=\sum_{j=1}^{h(t)}\lambda_j \mathrm{CE}(p_{\theta,j}(Y_j\mid h_T),Y_j).
$$

这个目标开始时等价于普通下一词元预测，然后周期性地加入来自更远未来 token 的压力。

## 5. 形式分析：梯度信号放大

### 5.1 分支相关梯度分解

假设表示空间中存在一个分支记忆方向。把隐藏状态写成：

$$
h_T=u_B m_T+\epsilon_T.
$$

这里，$u_B$ 是携带分支信息的方向或子空间，$m_T$ 是对 $B$ 的记忆强度，$\epsilon_T$ 是表示中与分支无关的部分。

对每个未来偏移 $j$，把相对于 $h_T$ 的梯度分解为分支相关部分和残差部分：

$$
\nabla_{h_T}\ell_j=\alpha_j u_B+\eta_j.
$$

这里，$\ell_j=\mathrm{CE}(p_{\theta,j}(Y_j\mid h_T),Y_j)$，$\alpha_j u_B$ 是推动模型编码或暴露分支键的部分，$\eta_j$ 是与分支无关或带噪声的部分。

下一词元梯度是：

$$
\nabla_{h_T}L_1=\alpha_1u_B+\eta_1.
$$

Next-k-token 梯度是：

$$
\nabla_{h_T}L_k=\sum_{j=1}^{k}\lambda_j\alpha_j u_B+\sum_{j=1}^{k}\lambda_j\eta_j.
$$

因此，分支相关信号的大小与下式成正比：

$$
A_k=\sum_{j=1}^{k}\lambda_j\alpha_j.
$$

这里，$A_k$ 是 next-k 训练下总的分支相关梯度系数。

如果每个激活的未来 token 都携带关于分支的正信息，那么这些偏移上有 $\alpha_j>0$。因此：

$$
A_k>A_1,\quad k>1.
$$

这就是基本的梯度放大结果。

### 5.2 定理 1：在未来监督对齐时，next-k 增强分支相关梯度

**定理 1。** 假设未来 token $Y_1,\ldots,Y_k$ 都依赖分支，并且它们的预测损失产生非负系数的分支相关梯度部分，即 $\alpha_j\ge 0$。如果第一个未来 token 之外至少存在一个未来偏移满足 $\alpha_j>0$，那么 next-k 目标的分支相关梯度幅度严格大于 next-token 目标。

**证明。** 下一词元预测的分支相关系数是 $A_1=\alpha_1$。Next-k 预测的分支相关系数是 $A_k=\sum_{j=1}^{k}\lambda_j\alpha_j$。如果 $\lambda_j>0$、$\alpha_j\ge 0$，并且至少存在一个 $j>1$ 使得 $\alpha_j>0$，那么：

$$
A_k=\alpha_1+\sum_{j=2}^{k}\lambda_j\alpha_j>\alpha_1=A_1.
$$

因此，next-k 有更大的分支相关分量。命题得证。

这个定理有意保持简单。它捕捉的机制是：多个依赖同一个早期分支变量的未来损失，会对保存该变量的 $h_T$ 施加方向一致的压力。

## 6. 形式分析：信噪比

上一个定理说明分支相关信号会增加。但优化取决于分支相关信号和无关梯度噪声之间的比例。

定义分支信噪比为：

$$
\mathrm{SNR}_k=
\frac{
\left\|\sum_{j=1}^{k}\lambda_j\alpha_j u_B\right\|
}{
\left(\mathbb{E}\left\|\sum_{j=1}^{k}\lambda_j\eta_j\right\|^2\right)^{1/2}
}.
$$

这里，分子是对齐的分支梯度的范数，分母是分支无关梯度的均方根范数。

假设残差梯度 $\eta_j$ 均值为零，并且不同偏移之间弱相关。那么残差噪声大约按偏移数量的平方根增长，而对齐的分支信号大约线性增长：

$$
\left\|\sum_{j=1}^{k}\lambda_j\alpha_j u_B\right\|
\approx
\sum_{j=1}^{k}\lambda_j\alpha_j.
$$

$$
\left(\mathbb{E}\left\|\sum_{j=1}^{k}\lambda_j\eta_j\right\|^2\right)^{1/2}
\approx
\left(\sum_{j=1}^{k}\lambda_j^2\sigma_j^2\right)^{1/2}.
$$

这里，$\sigma_j^2=\mathbb{E}\|\eta_j\|^2$ 是偏移 $j$ 的残差梯度方差。

如果 $\alpha_j=\alpha$、$\sigma_j=\sigma$ 且 $\lambda_j=1$，那么：

$$
\mathrm{SNR}_k\approx \frac{k\alpha}{\sqrt{k}\sigma}
=\sqrt{k}\frac{\alpha}{\sigma}.
$$

这给出了更强的结果：在信号对齐且噪声弱相关的条件下，next-k prediction 可以使长时距分支信号的相对强度提升约 $\sqrt{k}$ 倍。

### 定理 2：在独立残差噪声下，next-k 改善分支信噪比

**定理 2。** 假设每个未来偏移都贡献相同的分支相关系数 $\alpha>0$，并且分支无关残差梯度具有相同方差 $\sigma^2$，且不同偏移之间不相关。那么 next-k prediction 下的分支相关梯度信噪比，是 next-token prediction 下信噪比的 $\sqrt{k}$ 倍。

**证明。** 对下一词元预测，分支信号为 $\alpha$，残差噪声尺度为 $\sigma$，所以 $\mathrm{SNR}_1=\alpha/\sigma$。对 next-k prediction，对齐的分支信号为 $k\alpha$。独立残差噪声尺度为 $\sqrt{k}\sigma$。因此：

$$
\mathrm{SNR}_k=\frac{k\alpha}{\sqrt{k}\sigma}
=\sqrt{k}\frac{\alpha}{\sigma}
=\sqrt{k}\mathrm{SNR}_1.
$$

命题得证。

这个定理形式化地说明了为什么多词元预测可能更适合长时距学习：即使每个单独未来 token 只提供很弱的信息，它也可以提高分支相关梯度的相对强度。

## 7. 形式分析：信息论压力

梯度分析解释的是优化压力。信息论解释的是表示需求。

如果模型能从 $h_T$ 预测未来后缀 $Y_{1:k}$，那么 $h_T$ 必须包含关于分支变量 $B$ 的信息，因为 $Y_{1:k}$ 由 $B$ 决定。

数据处理不等式给出：

只有当 $\hat{Y}_{1:k}$ 是 $h_T$ 的可恢复函数，并且预测器足够准确时，才有：

$$
I(B;h_T)\ge I(B;\hat{Y}_{1:k}).
$$

更可操作的说法使用预测准确率。如果分支后缀彼此不重叠，并且模型以错误概率 $p_e$ 预测正确后缀，那么 Fano 风格的推理意味着：

$$
I(h_T;B)\ge \log M-H(p_e)-p_e\log(M-1).
$$

这里，$M$ 是分支数量，$p_e$ 是从 $h_T$ 选择错误分支后缀的概率，$H(p_e)$ 是错误事件的二元熵。

这意味着：高准确率的单前缀后缀预测，迫使 $h_T$ 包含关于 $B$ 的信息。

现在比较 next-token 和 next-k 目标。如果只监督 $Y_1$，表示只需要保存足以预测第一个未来 token 的信息。如果监督完整后缀 $Y_{1:k}$，并且后缀是分支特定的，那么表示必须保存足以在整个后缀上区分分支的信息。

关键单调性事实是：

$$
I(B;Y_{1:k})\ge I(B;Y_1).
$$

这来自互信息链式法则：

$$
I(B;Y_{1:k})=I(B;Y_1)+I(B;Y_{2:k}\mid Y_1).
$$

由于条件互信息非负，加入未来 token 不会减少关于分支的信息。

### 定理 3：多词元后缀预测施加更强的信息要求

**定理 3。** 如果未来后缀 token $Y_{1:k}$ 含有超出 $Y_1$ 的额外分支信息，即 $I(B;Y_{2:k}\mid Y_1)>0$，那么成功的 next-k prediction 要求隐藏状态 $h_T$ 暴露比分成功 next-token prediction 更多的分支信息。

**证明。** 根据链式法则：

$$
I(B;Y_{1:k})=I(B;Y_1)+I(B;Y_{2:k}\mid Y_1).
$$

如果 $I(B;Y_{2:k}\mid Y_1)>0$，那么：

$$
I(B;Y_{1:k})>I(B;Y_1).
$$

一个能够从 $h_T$ 准确恢复 $Y_{1:k}$ 的预测器，必须在 $h_T$ 中编码足够的分支信息来区分后缀。因此，next-k prediction 下的表示要求强于 next-token prediction。命题得证。

当第一个未来 token 含糊，或者只弱依赖分支，但多 token 后缀强依赖分支时，这个定理尤其重要。

## 8. 重要反例与声明边界

我们想要的结论并不是普遍成立的。必须明确说明以下反例。

### 反例 1：第二个 token 不携带分支信息

如果在给定局部上下文后，$Y_2$ 与 $B$ 独立，那么它的损失不会增加分支相关信号。在梯度记号中，就是 $\alpha_2=0$。这时 next-two prediction 不会改善长时距分支压力。

### 反例 2：未来损失产生冲突梯度

如果 $Y_1$ 和 $Y_2$ 需要互不兼容的特征，它们的梯度可能不对齐。在这种情况下，加入 $Y_2$ 可能增加优化噪声或干扰，而不是增加有用的分支压力。

### 反例 3：下一词元目标已经完美识别分支

如果 $Y_1$ 单独就能唯一识别 $B$，并且模型已经很容易学到它，那么 next-k 可能不会改善最终准确率。它仍然可能影响训练速度或谱几何，但行为收益可能饱和。

### 有效声明边界

严格结论应该是：

**当多个未来 token 共享同一个早期原因，并且它们的分支相关梯度正向对齐时，next-k-token prediction 预期会比 next-token prediction 更好地促进长时距学习。**

这是一个有条件的定理和可证伪的经验假设，不是无条件保证。

## 9. 与真实大语言模型学习的关系

在真实大语言模型预训练中，长时距依赖经常具有和合成分支模型相同的结构。

例子包括：

- 故事早期引入的人物，控制后面的代词指代；
- 程序早期定义的变量，控制后面的代码生成；
- 合同早期引入的法律条件，控制后面的条款；
- prompt 开头的用户指令，控制后面的回答格式；
- 证明早期引入的定理假设，控制后面的证明步骤。

预测位置附近的局部上下文可能不足够。模型必须在许多中间 token 之间保存一个早期潜在变量。

普通下一词元损失原则上包含这种信号。然而，大多数 token 位置奖励的是局部续写。多词元预测可以增强一个前缀隐藏状态暴露更多未来语义续写信息的压力。

合成分支数据集就是这个真实挑战的受控实验室版本：

$$
BR_k\ldots A\ B\ C\ D\to suffix_k.
$$

这里，$BR_k$ 对应早期语义条件，$A B C D$ 对应共享局部上下文，$suffix_k$ 对应由早期条件决定的未来续写。

理想的经验证据模式是：

标准下一词元训练：

- teacher-forced 续写强；
- 单前缀后缀预测弱。

Next-k 课程训练：

- 单前缀后缀预测更强；
- 分支特定 horizon 激活后，suffix-only loss 更低；
- 分支特定后缀上的最低目标概率更高。

## 10. 小型经验测试

### 10.1 数据集

使用一个分支控制后缀数据集。

模板：

$$
BR_k\ F00\ F01\ldots F\{m-1\}\ A\ B\ C\ D\ R00\ R01\ldots R\{d-1\}\ suffix_k\ .
$$

推荐 V1 参数：

- `num_branches = 3`
- `branch_delay_len = 8`
- `post_prefix_delay_len = 4`
- `shared_prefix_len = 4`
- `suffix_len = 8`
- `max_horizon = 13`
- `sequence_length = 96`
- `structured_example_probability = 0.30`
- `random_filler_probability = 0.70`

`max_horizon = 13` 的原因是：

- 偏移 1 到 4：干扰 token，即 `R00 R01 R02 R03`；
- 偏移 5 到 12：分支特定后缀 token；
- 偏移 13：停止 token `.`。

第一个分支特定 horizon 在这里激活：

$$
h_{\mathrm{branch}}=\mathrm{post\_prefix\_delay\_len}+1=5.
$$

如果 horizon 间隔 $S=100$，它会在 step 400 激活。

### 10.2 模型条件

使用同架构内部比较。

- `standard_lm + standard_next_token`
- `direct_heads + fixed_next_token`
- `direct_heads + deterministic_curriculum_next_k`
- `direct_heads + fixed_full_horizon`
- `latent_decoder + fixed_next_token`
- `latent_decoder + deterministic_curriculum_next_k`
- `latent_decoder + fixed_full_horizon`

关键比较是：

直接头模型：

- `fixed_next_token` vs `deterministic_curriculum_next_k` vs `fixed_full_horizon`

潜在解码器模型：

- `fixed_next_token` vs `deterministic_curriculum_next_k` vs `fixed_full_horizon`

对 `fixed_next_token`，保持完整架构不变，只把 `active_horizon` 固定为 1。

### 10.3 指标

主要预测指标：

- `single_prefix_exact_match_suffix_only`
- `single_prefix_min_prob_suffix_only`
- `single_prefix_mean_prob_suffix_only`
- `worst_branch_suffix_only_min_prob`
- `branch_swap_suffix_preference`

主要训练动态：

- `global_active_loss`
- `structured_active_loss`
- `random_active_loss`
- `single_prefix_suffix_loss`
- `single_prefix_suffix_loss_by_offset`
- `loss_by_offset_all_positions`

诊断指标：

- `teacher_forced_exact_match`
- `autoregressive_rollout_exact_match`
- `single_prefix_exact_match_all_offsets`

谱诊断：

- LM head 的奇异值；
- direct future heads 的奇异值；
- decoder output head 的奇异值；
- encoder attention matrices 的奇异值；
- decoder self-attention 和 cross-attention matrices 的奇异值。

### 10.4 预期结果模式

如果在同一架构内出现：

$$
\mathrm{deterministic\_curriculum\_next\_k}
>
\mathrm{fixed\_next\_token},
$$

并且优势体现在 suffix-only 单前缀指标上，那么强支持该假设，尤其是这些指标：

- `single_prefix_exact_match_suffix_only`
- `single_prefix_min_prob_suffix_only`
- `worst_branch_suffix_only_min_prob`

同时，训练曲线应显示：

- 新 horizon 激活；
- active loss 上升；
- 新激活 offset 的 loss 随后下降。

尤其是在 $h=5$ 之后，也就是第一个分支特定 horizon 激活之后。

一个有用但较弱的结果是：课程训练优于 fixed-next-token，但不优于 fixed-full-horizon。这说明多词元监督重要，但课程 schedule 不一定优于从 step 0 开始就训练 full horizon。

负结果是：teacher-forced 续写很强，但 suffix-only 单前缀预测仍然很弱。这说明模型学到了局部续写链，但没有把分支特定后缀存进 $h_D$。

## 11. 什么算形式上的经验证伪？

如果以下现象跨随机种子同时成立，假设会被削弱：

- `fixed_next_token` 在 suffix-only 单前缀预测上匹配 curriculum；
- branch-specific horizon 激活后，curriculum 没有降低 `single_prefix_suffix_loss`；
- curriculum 下 `branch_swap_suffix_preference` 没有改善；
- 谱诊断没有显示输出相关几何的一致差异。

如果提升只出现在 teacher-forced 续写中，而不出现在单前缀指标中，假设也会被削弱。这意味着训练方法改善的是局部 rollout，而不是长时距表示。

## 12. 总结

理论机制是有条件但精确的。

当下一个 token 依赖早期变量时，下一词元预测确实包含长时距信号。然而，这个信号可能被大量局部损失稀释。

当多个未来 token 依赖同一个早期变量时，next-k-token prediction 会增强长时距学习。在这种情况下，多个未来损失会在同一个前缀隐藏状态上产生对齐的分支相关梯度。在独立残差噪声下，分支信噪比可以大约提升 $\sqrt{k}$。从信息论角度看，准确的后缀预测要求隐藏状态包含足够的早期分支键信息。

因此，经验测试应该关注单前缀后缀预测，而不是只看普通困惑度。

简洁声明是：

**在分支控制后缀分布中，确定性 next-k-token 课程训练可以比普通下一词元预测对因果隐藏状态产生更强压力，使其保存并暴露长时距分支信息。**
