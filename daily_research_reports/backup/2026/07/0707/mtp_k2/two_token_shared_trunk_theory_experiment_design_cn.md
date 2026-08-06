# 双 Token 预测、共享主干梯度相互作用与最小单层 Transformer 实验设计

建立日期：2026-07-07  
版本说明：本文件是 `two_token_shared_trunk_theory_experiment_design.md` 的简体中文译本，并在正文前新增术语预先定义。英文原文仍是来源文件。

## 0. 术语预先定义

| 术语 / 缩写 | 直接含义 | 具体对象或计算 | 单位 / 公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| 多词元预测（multi-token prediction, MTP） | 用同一个前缀状态预测多个未来 token | 例如从 $h_t$ 同时预测 $x_{t+1}$ 与 $x_{t+2}$ | 训练目标类型 | 本文要判断第二个未来 token 是否给共享表示带来有用压力 | 不证明 MTP 一定优于下一词元预测 |
| 下一词元预测（next-token prediction, NTP） | 只预测下一个 token | 从 $h_t$ 预测 $x_{t+1}$ | 训练目标类型 | 作为普通语言模型训练的对照 | 不证明 NTP 不能学长时距依赖 |
| 共享主干（shared trunk） | 多个预测头共用的模型部分 | 共享 embedding、attention、MLP 或其他表示生成模块 | 参数集合 $\theta_s$ | 多个 horizon loss 会同时更新它，因此可能合作或冲突 | 不代表所有参数都共享 |
| 因果隐藏状态（causal hidden state） | 只能依赖当前与之前 token 的表示 | $h_t=f_{\theta_s}(x_{\le t})$ | 向量 | 是多个 future heads 共用的预测依据 | 不代表后续位置不能重新读取 prefix |
| 预测 horizon | 从当前位置往后预测的距离 | offset 1 是 $x_{t+1}$，offset 2 是 $x_{t+2}$ | token offset | 不同 horizon 的 loss 可能需要不同信息 | 不等于真实语义推理长度 |
| 第一个未来 token | 当前位置后的下一个 token | $Y_1=x_{t+1}$ | token | NTP 直接监督的目标 | 不一定包含 branch 信息 |
| 第二个未来 token | 当前位置后第二个 token | $Y_2=x_{t+2}$ | token | MTP 新增监督的最小远未来目标 | 不保证有用；可能是冗余或噪声 |
| 分支变量（branch variable） | 早期决定后续走向的变量 | $B\in\{1,\ldots,M\}$ | 离散标签 | 用来建模长时距依赖的早期原因 | 不代表自然语言中所有隐含语义因素 |
| 分支特定后缀（branch-specific suffix） | 不同 branch 对应不同未来后缀 | $Y_{1:k}=s_B$ | token 序列 | 检查模型是否保留早期 branch 信息 | 不证明自然语言后缀都是离散 branch |
| 分支恢复 probe（branch probe） | 从隐藏状态读出 branch 的轻量分类器 | $S_\phi(h_T)\to B$ | accuracy 或 cross-entropy | 判断 $h_T$ 是否可恢复 branch 信息 | probe 成功不代表原生 head 一定可用 |
| 交叉熵（cross-entropy, CE） | 目标 token 的负对数概率 | $\operatorname{CE}(p,y)=-\log p(y)$ | loss | 本文所有 horizon loss 的基本形式 | 不单独说明表示中含有什么信息 |
| 梯度相容性 | 两个 loss 的梯度方向是否合作 | $\langle g_1,g_2\rangle$ 或 cosine | 内积 / cosine | 判断第二个 token loss 是否干扰下一词元学习 | 不保证长时距表示有用 |
| 梯度范数比 | 第二个 token 梯度相对第一个 token 梯度的大小 | $r=\|g_2\|/\|g_1\|$ | ratio | 判断第二个 token loss 是否过强或过弱 | 不说明梯度方向是否正确 |
| refinement gain | 中间 token 被揭示后，目标变容易的程度 | $G_t=-\log p^{(2)}(x_{t+2}\mid x_{\le t})+\log p^{(1)}(x_{t+2}\mid x_{\le t+1})$ | log-prob difference | 衡量 offset-2 任务相对下一步条件预测有多难 | 不直接证明 branch 信息是否被保留 |
| KL divergence | 两个预测分布的差异 | $D_t=\operatorname{KL}(p^{(1)}(\cdot\mid x_{\le t+1})\Vert p^{(2)}(\cdot\mid x_{\le t}))$ | nats | 衡量看到 $x_{t+1}$ 后预测如何被 refined | 不说明哪个模型更好 |
| 条件互信息 | 给定一个变量后，两个变量仍共享多少信息 | $I(B;Y_2\mid Y_1)$ | nats 或 bits | 判断 $Y_2$ 是否在 $Y_1$ 之外提供 branch 信息 | 不保证模型能学到这个信息 |
| 专家分离（expert separation） | 不同 horizon 使用不同专家 / MLP 子空间 | $\theta_{e,1}$ 处理 $L_1$，$\theta_{e,2}$ 处理 $L_2$ | 架构条件 | 测试是否能降低 horizon-specific 干扰 | 不能移除共享 attention 的干扰 |
| shared-attention separate-expert | attention 共享，但 horizon-specific experts 分离 | shared attention $\to a_t$，再接 expert 1/2 | 模型条件 | 定位干扰是否主要来自 MLP / expert 子空间 | 不代表完全分离模型 |

## 1. 问题定义

目标是在最简单的设定中理解：相较于普通下一词元预测，多词元预测如何改变表示学习。

具体问题不是模型原则上能不能预测未来 token。只要下一个 token 依赖远处更早的变量，普通下一词元预测本身已经含有长时距信号。更精确的问题是：

**预测额外的未来 token，会不会为共享因果主干产生有用的学习压力；或者它只是把困难、噪声、或互相干扰的梯度注入同一个共享表示？**

这一点重要，因为多词元预测架构使用一个共享主干和多个预测头。对于双 token 预测，同一个隐藏状态必须同时支持：

$$
h_t \rightarrow x_{t+1}.
$$

这里，$h_t$ 是读取 prefix $x_{\le t}$ 后的因果隐藏状态，$x_{t+1}$ 是下一个 token。

$$
h_t \rightarrow x_{t+2}.
$$

这里，同一个 $h_t$ 还被要求预测第二个未来 token $x_{t+2}$，即使中间 token $x_{t+1}$ 在位置 $t$ 尚未被模型看到。

这个设计带来核心理论张力。如果 $x_{t+2}$ 依赖 prefix 中已经存在的潜在长时距变量，第二个 token loss 可能有帮助。但如果 $x_{t+2}$ 从 $x_{\le t}$ 看来太不确定，或它的梯度与下一词元梯度在共享主干参数上冲突，它也可能有害。

我们的目标是建立一个最小理论和一个最小实验，用来区分这些可能性。

## 2. 双 Token 训练实际如何喂资料

双 token 预测不是每次从训练语料中取两个 token。它仍然使用标准因果语言模型布局，逐 token 滑动。

给定 token 序列：

$$
x_1,x_2,\ldots,x_T,
$$

普通下一词元预测训练每个位置 $t$ 预测 $x_{t+1}$。双 token 预测训练每个位置 $t$ 同时预测 $x_{t+1}$ 和 $x_{t+2}$。

因此训练目标是重叠的：

| 位置 | 主干表示的 prefix | Head 1 目标 | Head 2 目标 |
|---|---|---|---|
| $t$ | $x_{\le t}$ | $x_{t+1}$ | $x_{t+2}$ |
| $t+1$ | $x_{\le t+1}$ | $x_{t+2}$ | $x_{t+3}$ |
| $t+2$ | $x_{\le t+2}$ | $x_{t+3}$ | $x_{t+4}$ |

所以 $x_{t+2}$ 会作为 supervised target 出现两次：一次是从 prefix $x_{\le t}$ 出发的 second-token target，另一次是从 prefix $x_{\le t+1}$ 出发的 next-token target。

这种 duplicate-target 结构很重要。这两个分布不应该相同，因为它们条件化在不同信息上：

$$
p^{(2)}_\theta(x_{t+2}\mid x_{\le t}).
$$

这里，$p^{(2)}_\theta$ 是 second-token head，它在尚未看到 $x_{t+1}$ 前预测 $x_{t+2}$。

$$
p^{(1)}_\theta(x_{t+2}\mid x_{\le t+1}).
$$

这里，$p^{(1)}_\theta$ 是 next-token head，它在 $x_{t+1}$ 已经被揭示后预测同一个 token。

正确的概率关系是 refinement 关系，不是 equality：

$$
p(x_{t+2}\mid x_{\le t})
=\sum_a p(x_{t+2}\mid x_{\le t},x_{t+1}=a)p(x_{t+1}=a\mid x_{\le t}).
$$

这里，$a$ 遍历所有可能的下一个 token。这个等式来自全概率公式。它表示：从 $x_{\le t}$ 做 second-token prediction，是对可能 next-token branches 的边际预测；而在 $t+1$ 的 next-token prediction，是实际下一个 token 已揭示后的 refined forecast。

这给出 second-token loss 更精确的解释。它不只是要求模型猜更远的 token，而是要求当前隐藏状态 $h_t$ 在中间 token 未知之前，就編码足够信息以预测未来延续分布。

## 3. 最小数学模型

我们使用 branch-controlled sequence distribution，因为它能隔离多词元预测理应帮助的长时距依赖。

令 $B$ 为早期 branch 变量：

$$
B\in\{1,2,\ldots,M\}.
$$

这里，$B$ 是潜在或显式 branch key，$M$ 是可能 branch 的数量。

模型观察到一段包含 $B$ 的长 prefix，接着是一些不透露新 branch 信息的 filler tokens。在预测位置附近，所有 branch 共享相同 local context。然后未来 suffix 依赖 $B$：

$$
Y_{1:k}=X_{T+1:T+k}=s_B.
$$

这里，$Y_{1:k}$ 是 future suffix，$s_B$ 是 branch-specific suffix，$T$ 是预测位置。

一个典型合成序列是：

```text
BR_i  filler filler filler ...  A B C D  R0 R1  suffix_i
```

共享 local context $A B C D$ 在各 branch 间刻意保持相同。因此，只依赖 local context 的模型无法知道应该接哪个 suffix。它必须保留关于 $BR_i$ 的信息。

因果主干产生：

$$
h_T=f_{\theta_s}(x_{\le T}).
$$

这里，$f_{\theta_s}$ 是参数为 $\theta_s$ 的共享主干，$h_T$ 是 prediction heads 使用的 hidden state。

对双 token 预测，位置 $T$ 的 losses 是：

$$
L_1=\operatorname{CE}(p^{(1)}_\theta(Y_1\mid h_T),Y_1).
$$

这里，$L_1$ 是下一词元交叉熵，$p^{(1)}_\theta$ 是 offset-1 head，$Y_1=X_{T+1}$。

$$
L_2=\operatorname{CE}(p^{(2)}_\theta(Y_2\mid h_T),Y_2).
$$

这里，$L_2$ 是 second-token cross-entropy，$p^{(2)}_\theta$ 是 offset-2 head，$Y_2=X_{T+2}$。

合併后的双 token 目标是：

$$
L=L_1+\lambda L_2.
$$

这里，$\lambda$ 控制 second-token loss 的貢獻强度。

## 4. 未来 Token 梯度代表什么？

$L_1$ 的梯度表示：更新模型，使 $h_T$ 更好地预测 immediate next token $Y_1$。

$L_2$ 的梯度表示：更新模型，使 $h_T$ 在 $Y_1$ 尚未被观察前，更好地预测 $Y_2$。

这两者不是等價学习信号。如果 $Y_2$ 和 $Y_1$ 依赖同一个 branch 变量 $B$，那么 $L_2$ 可能推动 $h_T$ 保留 $B$。如果 $Y_2$ 是随机的，或主要由 $Y_1$ 决定，那么从 $h_T$ 的角度看，$L_2$ 可能是噪声。

相关的共享主干梯度是：

$$
g_1=\nabla_{\theta_s}L_1,\qquad g_2=\nabla_{\theta_s}L_2.
$$

这里，$g_1$ 是下一词元 loss 对共享参数的梯度，$g_2$ 是 second-token loss 对相同共享参数的梯度。

双 token 训练在共享参数上的合併更新方向是：

$$
g=g_1+\lambda g_2.
$$

这里，$g$ 是双 token 训练使用的共享参数梯度。

加入 $L_2$ 对下一词元优化的一阶影响由下式决定：

$$
\langle g_1,g\rangle=\|g_1\|^2+\lambda\langle g_1,g_2\rangle.
$$

这里，$\langle g_1,g\rangle$ 衡量合併更新是否保留沿着 next-token gradient 的進展。这个等式来自展开 $g_1$ 与 $g_1+\lambda g_2$ 的内积。

如果 $\langle g_1,g_2\rangle>0$，second-token loss 在共享参数上与 next-token learning 局部相容。如果 $\langle g_1,g_2\rangle<0$，second-token loss 会干扰 next-token learning。如果内积接近 0 但 $\|g_2\|$ 很大，second-token gradient 可能像高变异辅助噪声。

这还不是完整故事。second-token gradient 可以干扰 $L_1$，但仍对长时距表示有用；也可以与 $L_1$ 相容，但与 branch 变量无关。因此我们需要第二个診断：$L_2$ 是否增加 $h_T$ 中的 branch 信息。

令 $S_\phi(h_T)$ 为一个从 $h_T$ 恢复 $B$ 的 linear probe 或 classifier。定义 branch-recovery objective：

$$
R_\phi=\operatorname{CE}(S_\phi(h_T),B).
$$

这里，较低的 $R_\phi$ 表示 branch 信息更容易从 $h_T$ 中恢复。

有用的长时距表示条件是：

$$
\langle \nabla_{\theta_s}R_\phi,g_2\rangle>0
$$

其中两个梯度都定义为 loss gradient。

这里，$g_2=\nabla_{\theta_s}L_2$。因为 gradient descent 沿着 $-g_2$ 移动，当 $\langle \nabla_{\theta_s}R_\phi,g_2\rangle>0$ 时，branch-recovery loss $R_\phi$ 会下降。这是一阶 Taylor statement：沿 $-\eta g_2$ 移动会让 $R_\phi$ 約改变 $-\eta\langle \nabla R_\phi,g_2\rangle$。

因此，如果 $L_2$ 指向能降低 branch-probe loss 的方向，它就对长时距表示有用，即使它不總是与 $L_1$ 对齐。

## 5. 目标层级信息：什么时候 $L_2$ 应该有帮助？

除非 $Y_2$ 包含 local continuation 尚未捕捉到的 branch 信息，否则 second-token loss 不能帮助长时距表示。

一个干净的数据层级条件是：

$$
I(B;Y_2\mid Y_1)>0.
$$

这里，$I(B;Y_2\mid Y_1)$ 是条件互信息。它衡量第二个未来 token 是否在第一个未来 token $Y_1$ 之外，仍包含 branch 变量 $B$ 的信息。

如果 $I(B;Y_2\mid Y_1)=0$，那么在已知 $Y_1$ 后，$Y_2$ 不再添加 branch 信息。在这种情况下，second-token loss 可能仍帮助 local continuation，但不应添加新的长时距 branch signal。

如果 $I(B;Y_2\mid Y_1)>0$，那么成功的双 token 预测比单純下一词元预测有更强的信息需求。

对长度为 $k$ 的 suffix，单调信息关系是：

$$
I(B;Y_{1:k})=I(B;Y_1)+I(B;Y_{2:k}\mid Y_1).
$$

这里，第二项依互信息鏈式法则非负。因此加入 future suffix tokens 不会减少 branch information；当 $I(B;Y_{2:k}\mid Y_1)>0$ 时，它会增加 branch information。

这解释了多词元预测何时有原理上的帮助：未来 tokens 必须揭示一个 shared latent cause，且这个 cause 不能已经被 immediate next token 完全揭示。

## 6. 隐藏状态与共享主干相互作用

horizon losses 会在两个不同位置相互作用。

第一，它们在 hidden state 层面相互作用：

$$
c_h=\frac{\langle \nabla_{h_T}L_1,\nabla_{h_T}L_2\rangle}{\|\nabla_{h_T}L_1\|\|\nabla_{h_T}L_2\|}.
$$

这里，$c_h$ 衡量两个 heads 是否要求同一个 hidden state 朝相容方向移动。

第二，它们通过共享主干 Jacobian 后相互作用：

$$
c_s=\frac{\langle \nabla_{\theta_s}L_1,\nabla_{\theta_s}L_2\rangle}{\|\nabla_{\theta_s}L_1\|\|\nabla_{\theta_s}L_2\|}.
$$

这里，$c_s$ 衡量两个 horizon losses 在共享主干参数上是合作还是冲突。

鏈式法则连结二者：

$$
\nabla_{\theta_s}L_j=J_{\theta_s}(h_T)^\top\nabla_{h_T}L_j.
$$

这里，$J_{\theta_s}(h_T)$ 是 hidden state 对共享参数的 Jacobian。这个等式解释为什么 hidden-state alignment 和 shared-parameter alignment 不一定相同。主干幾何可以放大、抑制、或旋转 horizon-specific gradients。

这是我们需要 profiling 而不是口头解释的核心原因。多词元预测可能在 target-information 层面有用，但在 shared-optimization 层面仍然困难。

## 7. 专家分离：它能修什么，不能修什么？

我们的设计为不同 prediction horizons 加入 separate experts。这会改变梯度相互作用结构。

一个简化的参数分解是：

$$
\theta=(\theta_{\mathrm{attn}},\theta_{e,1},\theta_{e,2},\theta_{h,1},\theta_{h,2}).
$$

这里，$\theta_{\mathrm{attn}}$ 是共享 self-attention trunk，$\theta_{e,1}$ 和 $\theta_{e,2}$ 是 horizon-specific expert parameters，$\theta_{h,1}$ 和 $\theta_{h,2}$ 是 output heads。

在 separated-expert design 中，$L_1$ 更新 $\theta_{e,1}$ 和 $\theta_{h,1}$，而 $L_2$ 更新 $\theta_{e,2}$ 和 $\theta_{h,2}$。但除非 attention 也被分离，两个 losses 仍会更新共享 attention 参数 $\theta_{\mathrm{attn}}$。

因此，expert separation 可以降低 expert 或 MLP 子空间中的干扰，但不能完全移除 shared attention 中的干扰。

这给出一个可证偽机制：

如果 $L_1$ 与 $L_2$ 的有害相互作用主要位于 expert / MLP parameters，那么 separate experts 应该能保留 next-token performance，同时允許 $L_2$ 学到 branch-relevant features。

如果有害相互作用主要位于 shared attention，那么 separate experts 不能完全解決问题。我们仍应观察到 $\theta_{\mathrm{attn}}$ 上负向或不稳定的 $c_s$。

## 8. 理论主张边界

理论不应主张双 token 预测總是有帮助。有效主张是有条件的。

**Claim.** 当 $Y_2$ 含有额外 branch 信息、second-token gradient 增加 $h_T$ 中 branch 可恢复性，且其在共享主干参数上的投影梯度不会破坏性地反对 next-token gradient 时，双 token 预测应能改善长时距表示。

这个主张依赖三个可测量条件：

$$
I(B;Y_2\mid Y_1)>0.
$$

这是数据层级条件：第二个未来 token 必须包含额外 branch 信息。

$$
\langle \nabla_{\theta_s}R_\phi,g_2\rangle>0.
$$

这是表示条件：下降 $L_2$ 应降低 branch-probe loss。

$$
\langle g_1,g_2\rangle
$$

不应在关键共享参数上强烈为负。

这是优化条件：second-token gradient 不应破坏 next-token update direction。

这些条件也产生干净的 falsification criteria。如果 $Y_2$ 含 branch 信息，但 $g_2$ 不增加 branch recoverability，则模型沒有利用未来监督。如果 $g_2$ 增加 branch recoverability 但强烈冲突于 $g_1$，则双 token 预测可能帮助长时距 features，同时傷害 local next-token learning。如果 expert separation 修复 attention 外部的冲突但修不了 attention 内部的冲突，则剩余 bottleneck 是 shared attention layer。

## 9. 最小实验

最简单的实验应使用一层因果 Transformer 和双 token 预测。目的不是打敗 benchmark，而是暴露 future-token supervision、shared representations 与 expert separation 之间的相互作用。

### 9.1 数据集

使用含三种 regimes 的 branch-controlled suffix dataset。

#### Regime A：有用的 second-token branch signal

每个序列包含一个早期 branch key，并在 prediction site 之前有共享 local prefix：

```text
BR_i  F_1 F_2 ... F_m  A B C D  Y_1^{(i)} Y_2^{(i)}
```

$Y_1^{(i)}$ 和 $Y_2^{(i)}$ 都依赖 $BR_i$。这个 regime 测试双 token 预测是否加强 branch memory。

一个更强的变体让 $Y_1$ 部分模糊，但 $Y_2$ branch-specific：

```text
BR_1 ... A B C D  U  P
BR_2 ... A B C D  U  Q
BR_3 ... A B C D  U  R
```

在这个变体中，branch point 的 next-token prediction 看到跨 branch 相同的 $Y_1=U$，而 second-token prediction 必须区分 $P,Q,R$。这直接测试 $L_2$ 是否創造 $L_1$ 缺少的 branch-learning pressure。

#### Regime B：冗余的 second-token signal

$Y_1$ 和 $Y_2$ 都可由 local context 预测，且 $Y_2$ 在 $Y_1$ 之外幾乎不添加 branch 信息。这个 regime 测试双 token 预测是否只是 redundant。

#### Regime C：噪声 second-token target

$Y_1$ 可预测，但 $Y_2$ 是随机的，或在给定 prefix 后与 $B$ 无关。这个 regime 测试所提出的 diagnostics 是否能辨识有害或无用的 future-token supervision。

### 9.2 模型条件

用相同资料与 optimizer settings 训练以下模型。

| 条件 | 描述 | 目的 |
|---|---|---|
| NTP baseline | 单层 Transformer，一个 head，loss $L_1$ | baseline local 和 branch learning |
| Shared-trunk two-token | 单层 Transformer，共享 trunk，两个 heads，loss $L_1+\lambda L_2$ | 测试普通双 token 相互作用 |
| Shared-attention separate-expert | 共享 attention，分离 horizon experts，两个 heads | 测试 expert separation 是否降低干扰 |
| Fully separated control | embedding 后或 attention 后分离 branches | 给出 separation benefit 上界 |

主要比较是 NTP baseline、shared-trunk two-token model、和 shared-attention separate-expert model。

### 9.3 架构

使用最小单层因果 Transformer：

```text
token embedding + position embedding
one causal self-attention layer
one MLP or expert block
LayerNorm / residual path
prediction head(s)
```

shared-trunk two-token model：

```text
shared attention + shared MLP -> h_t
h_t -> head_1 -> x_{t+1}
h_t -> head_2 -> x_{t+2}
```

separate-expert model：

```text
shared attention -> a_t
expert_1(a_t) -> h_t^{(1)} -> head_1 -> x_{t+1}
expert_2(a_t) -> h_t^{(2)} -> head_2 -> x_{t+2}
```

这个架构隔离了问题：分离 horizon-specific MLP / expert subspace，是否能在 attention 仍共享的情况下降低冲突？

### 9.4 训练设定

使用小模型和短训练，让多 seed 测试能快速完成。

建議预设值：

| 参数 | 建議值 |
|---|---:|
| vocab size | 64 到 128 |
| branches 数量 | 3 到 8 |
| sequence length | 64 或 128 |
| branch delay | 16 到 64 tokens |
| model dimension | 64 或 128 |
| attention heads | 2 或 4 |
| layers | 1 |
| batch size | 128 或 256 |
| training steps | 5k 到 20k |
| optimizer | AdamW |
| learning rate | $10^{-3}$ 到 $3\times 10^{-4}$ |
| seeds | 至少 5 |
| $L_2$ 的 $\lambda$ | 0.25、0.5、1.0 |

run 应足够便宜，让 Codex 可以实现并对 regimes、seeds、$\lambda$ 做 sweeps。

## 10. 要监控什么

实验应监控普通 loss、长时距行为、与梯度幾何。

### 10.1 基礎 Loss 指标

追蹤：

**$L_1$**：下一词元 loss。

**$L_2$**：second-token loss。

**$L_1+\lambda L_2$**：總 active training loss。

这些应分别对所有 tokens 和 structured branch-controlled positions 記录。structured-position metrics 比 global average loss 更重要，因为 global loss 可能被 filler tokens 主导。

### 10.2 Branch-Specific Prediction 指标

在共享 local context 位置，評估模型是否能从 single prefix 预测 branch-specific suffix。

监控：

```text
single_prefix_head1_accuracy
single_prefix_head2_accuracy
single_prefix_joint_two_token_accuracy
branch_suffix_exact_match
branch_swap_preference
```

最重要的指标是 ambiguous-$Y_1$ regime 中的 head-2 branch accuracy。如果 $Y_1$ 在各 branch 间相同但 $Y_2$ 不同，普通 next-token loss 在该位置沒有直接 branch signal，而 two-token loss 有。

### 10.3 Duplicate-Target Refinement 指标

因为 $x_{t+2}$ 既由位置 $t$ 的 head 2 预测，也由位置 $t+1$ 的 head 1 预测，所以需要监控两者关系。

定义：

$$
D_t=\operatorname{KL}\left(p^{(1)}_\theta(\cdot\mid x_{\le t+1})\,\|\,p^{(2)}_\theta(\cdot\mid x_{\le t})\right).
$$

这里，$D_t$ 衡量 $t+1$ 的 refined next-token distribution 与 $t$ 的 earlier second-token distribution 差多少。大的 $D_t$ 表示 intermediate token $x_{t+1}$ 揭示了关于 $x_{t+2}$ 的大量信息。

定义：

$$
G_t=-\log p^{(2)}_\theta(x_{t+2}\mid x_{\le t})+\log p^{(1)}_\theta(x_{t+2}\mid x_{\le t+1}).
$$

这里，$G_t$ 是 refinement gain：揭示 $x_{t+1}$ 后，目标变得容易多少。高 $G_t$ 位置表示 second-token task 本质上比 one-step-later next-token task 更难。

这些指标把「future-token prediction 很难」这句模糊说法变成可测量量。

### 10.4 梯度相互作用指标

在 profiling intervals，optimizer step 前分别计算 $L_1$ 和 $L_2$ 的梯度。

对每个 parameter group，计算：

$$
c_s=\frac{\langle g_1,g_2\rangle}{\|g_1\|\|g_2\|}.
$$

这里，$g_1$ 和 $g_2$ 分别是同一 parameter group 上由 $L_1$ 和 $L_2$ 产生的梯度。

分别对以下 group 计算 $c_s$：

```text
embedding parameters
shared attention parameters
shared MLP parameters
expert_1 parameters
expert_2 parameters
head_1 parameters
head_2 parameters
```

对 separated experts，cross-horizon expert gradient conflict 应该因架构而不存在或明显降低。剩下重要相互作用在 embeddings 与 shared attention。

还要监控：

$$
r=\frac{\|g_2\|}{\|g_1\|}.
$$

这里，$r$ 衡量 second-token gradient 相对 next-token gradient 是否太大或太小。

$$
\rho=\frac{\langle g_1+\lambda g_2,g_1\rangle}{\|g_1\|^2}.
$$

这里，$\rho$ 衡量 combined update 保留 next-token update direction 的程度。如果 $\rho<1$，second-token gradient 弱化 next-token progress。如果 $\rho<0$，它反转 next-token direction。

### 10.5 表示指标

训练或週期性拟合一个从 $h_T$ 到 branch label $B$ 的 linear probe：

```text
branch_probe_accuracy
branch_probe_cross_entropy
```

在幾个位置测量：

```text
after branch token
middle of filler
shared local context A/B/C/D
prediction site before suffix
```

关键指标是 branch information 是否存活到 prediction site。

也计算 representation separation：

$$
\Delta_h=\mathbb{E}_{B\ne B'}\|\mu_B-\mu_{B'}\|^2.
$$

这里，$\mu_B$ 是 branch $B$ 在 prediction site 的平均 hidden state。较大的 $\Delta_h$ 表示 branches 在 representation space 中更分离。

### 10.6 依 Refinement Difficulty 的条件化 Profiling

按 $G_t$ 将 structured positions 分成 low、medium、high refinement gain buckets。

每个 bucket 報告：

```text
L1
L2
head2 accuracy
gradient cosine between L1 and L2
gradient norm ratio
branch probe accuracy
```

这很重要，因为 second-token gradient 可能在 low-$G_t$ 位置有用，但在训练早期对 high-$G_t$ 位置有害。实验应揭示这种结构，而不是用平均值掩蓋它。

## 11. 预期结果与解释

### Outcome 1：双 token 预测改善 branch representation

预期模式：

```text
shared-trunk two-token > NTP baseline on head2 branch accuracy
shared-trunk two-token > NTP baseline on branch probe accuracy
c_s is positive or mildly negative, not destructive
G_t decreases over training on structured positions
```

解释：second-token supervision 提供共享主干可以吸收的有用长时距压力。

### Outcome 2：双 token 预测有有用信号，但造成共享干扰

预期模式：

```text
L2 improves branch probe accuracy
but L1 worsens or learns slower
c_s is negative on shared MLP or attention
rho < 1 or rho < 0 during early training
```

解释：future-token supervision 有用，但在共享参数中与 next-token optimization 冲突。这支持 expert separation 或 loss scheduling。

### Outcome 3：Separate experts 降低干扰

预期模式：

```text
separate-expert model preserves L1 better than shared-trunk two-token
separate-expert model keeps or improves head2 branch accuracy
conflict disappears in expert parameters
remaining conflict is mostly in shared attention or embeddings
```

解释：expert design 有效，因为它分离 horizon-specific gradient subspaces，同时仍让 shared attention 承載 common context information。

### Outcome 4：Separate experts 沒有帮助

预期模式：

```text
separate-expert model still shows L1 degradation
shared attention gradient conflict remains strong
branch probe does not improve
```

解释：bottleneck 不在 expert / MLP subspace。干扰存在于 attention、embeddings，或资料本身不含有用 second-token branch information。

### Outcome 5：Noisy second-token control 被正确辨识

Regime C 的预期模式：

```text
I(B;Y2 | Y1) approximately zero
head2 branch accuracy near chance
branch probe does not improve from L2
c_s unstable or near zero
r may be large while useful progress is small
```

解释：diagnostics 可以区分有用 future supervision 和噪声 auxiliary targets。

## 12. 证伪标准

如果以下现象跨 seeds 成立，主 conjecture 被削弱：

```text
Y2 contains branch information, but L2 does not improve branch probe accuracy.
Two-token prediction improves neither head2 branch accuracy nor suffix prediction.
Gradient conflict metrics do not correlate with L1 degradation.
Separate experts do not reduce any measured conflict or improve any branch metric.
Duplicate-target refinement metrics do not distinguish useful and noisy regimes.
```

expert-separation conjecture 会被特别削弱，如果：

```text
shared-trunk and separate-expert models have the same L1 degradation
shared attention conflict dominates all conditions
expert separation does not improve branch retention or head2 prediction
```

future-token-usefulness conjecture 会被特别削弱，如果：

```text
Regime A and Regime C behave similarly
head2 performs no better when Y2 is branch-specific than when Y2 is random
branch probe accuracy is unchanged by two-token loss
```

## 13. Codex 实现注意事项

实现应优先考虑診断清晰度，而不是規模。

必要组件：

```text
synthetic dataset generator with regimes A/B/C
one-layer causal Transformer
NTP baseline
shared-trunk two-token model
shared-attention separate-expert model
loss logging by horizon and by structured positions
gradient profiling for L1 and L2 separately
branch probe evaluation
refinement metrics D_t and G_t
multi-seed experiment runner
CSV/JSON logging for all metrics
simple plotting script
```

重要实现细节：gradient profiling 不应改变 training。在 profiling step 上，用同一 batch 计算 $L_1$ 和 $L_2$，使用 separate backward passes 或 autograd gradients 收集 $g_1$ 和 $g_2$，计算 metrics，然后清空 gradients，再執行正常 training backward pass。

第一版实现只使用 $n=2$。不要加入 curriculum、MoE routing complexity、或 long horizons。目的在于建立基本的 theory-to-measurement bridge。

## 14. 总结

双 token 预测創造了一种 overlapping supervision structure：同一个 token $x_{t+2}$ 既作为从 $x_{\le t}$ 出发的 second-token target 被预测，也作为从 $x_{\le t+1}$ 出发的 next-token target 被预测。这表示 second-token head 被训练成较早的 marginal forecast，而下一步的 next-token head 则做 refined conditional forecast。

future-token loss 只有在特定条件下才会帮助长时距学习。未来目标必须包含关于 latent branch variable 的额外信息。它的梯度必须增加 shared hidden state 中 branch recoverability。而它在共享主干参数上的投影梯度不能破坏性地反对 next-token gradient。

最小单层 Transformer 实验正是为了测试这些条件。它应揭示 second-token prediction 是有用、冗余、噪声、还是干扰性的，以及 separate experts 是否降低相互作用中的有害部分。
