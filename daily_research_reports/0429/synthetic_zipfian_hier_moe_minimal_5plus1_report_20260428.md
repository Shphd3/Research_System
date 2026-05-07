# Synthetic Natural Zipfian Hierarchical MoE：核心结果简报

## 1. 目的

构建一个满足 Zipfian 分布的 synthetic natural language dataset，观察我们的初级 top-1 sparse Hierarchical MoE 是否能训出有效的层级专家分工。

数据真实层级是：

$$\text{coarse label} \rightarrow \text{fine label} \rightarrow \text{common / coarse / fine phrases}$$

我们要回答的问题很简单：模型是否真的学会了按这个层级进行 routing，并且这种 routing 是否带来更好的 next-token prediction。

## 2. 数据集构造

每条 document 先均匀采样一个 `coarse_label`，再在该 coarse 下均匀采样一个 `fine_label`。文本由自然语言模板生成，模板槽位来自三类 phrase pool：

- `common`：跨领域通用短语，例如 study、method、baseline process。
- `coarse`：大领域短语，例如 computing 里的 algorithm。
- `fine`：细主题短语，例如 network security 里的 packet trace。

词和短语的出现频率按 Zipfian 控制，但类别采样保持均衡。因此这个数据集同时有真实层级标签、自然语言表面形式、以及长尾词频结构。

所有模型都写成：

$$M(h)=M_0(h)+\Delta(h)$$

其中 $h\in\mathbb{R}^{1024}$ 是 Qwen3-0.6B layer-8 replacement block 的输入，$M_0(h)$ 是冻结原始 MLP，$E_r(z)$ 表示一个输入和输出都是 $1024$ 维、中间维度为 $r$ 的 adapter expert。

投影输入为：

$$x_{\text{head}}=P_{1:16}(h-\mu),\quad x_M=P_{17:207}(h-\mu),\quad x_{\text{Mcc}}=P_{17:80}(h-\mu),\quad x_{\text{Mtail}}=P_{81:207}(h-\mu)$$

## 3. 结果总表

| 模型 | 类型 | trainable params | router 看什么 | expert 看什么 | loss ↓ | fine-source loss ↓ | rare-bucket loss ↓ | coarse recovery ↑ | fine recovery ↑ | oracle regret ↓ |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| `G0_dense_matched` | matched dense 对照 | 3.67M | 无 router | $h$ | 1.1770 | 2.1167 | 2.1572 | NA | NA | NA |
| `G1_flat_raw_lb` | flat MoE + LB | 3.69M | $h$ | $h$ | 1.1696 | 2.1099 | 2.1521 | 0.1466 | 0.0831 | 1.5755 |
| `G2_flat_middle` | middle-band flat MoE | 3.69M | $x_M$ | $h$ | 1.1841 | 2.1513 | 2.1977 | 0.1121 | 0.0995 | 1.9429 |
| `B2_top1_ccM_tailM` | 主 top-1 Hierarchical MoE | 3.70M | $x_M,x_{\text{Mcc}},x_{\text{Mtail}}$ | global 看 $x_{\text{head}}$，conditional 看 $x_M$ | 1.1685 | 2.1041 | 2.1357 | 0.2960 | 0.1615 | 0.9196 |
| `A2_top1_rawexp_router_M` | 全输入 learned Hierarchical MoE | 3.70M | $x_M,x_{\text{Mcc}},x_{\text{Mtail}}$ | 所有 experts 看 $h$ | 1.1937 | 2.1553 | 2.2268 | 0.2988 | 0.1583 | 0.9067 |
| `G12_h_condct_top1_oracle_diag` | projected-input oracle 上界 | 3.70M | 真实 label/source path | $x_{\text{head}},x_{\text{Mcc}},x_{\text{Mtail}}$ | 1.1532 | 1.9982 | 2.0114 | 1.0000 | 1.0000 | 0.3674 |
| `G13_h_condct_top1_oracle_raw_all_diag` | 全输入 oracle 上界 | 3.70M | 真实 label/source path | 所有 experts 看 $h$ | 1.1562 | 1.9507 | 2.0099 | 1.0000 | 1.0000 | 0.3978 |

## 4. 指标怎么读

| 指标 | 含义 | 这次说明什么 |
|---|---|---|
| `loss` | overall next-token prediction loss，越低越好 | `B2` 比 dense、flat raw、flat middle 都略好，但还远低于 oracle 上界 |
| `fine-source loss` | 来自 fine phrase 的 token loss，越低越好 | `B2` 改善 fine token；`G13` 显示全输入 oracle 对 fine token 很强 |
| `rare-bucket loss` | 低频 token bucket 的 loss，越低越好 | `B2` 对 rare token 有收益，说明层级分支对长尾词有帮助 |
| `coarse/fine recovery` | routing 与真实 coarse/fine label 的 permutation-invariant 匹配程度 | `B2` 有部分恢复，但远没到 oracle，说明 hierarchy 只学出一部分 |
| `oracle regret` | 当前选择 path 与 counterfactual best path 的差距，越低越好 | `B2` 明显小于 flat MoE，但仍高于 oracle，瓶颈仍在 learned router/path selection |

## 5. 模型公式

### 5.1 Dense 对照：`G0_dense_matched`

没有 routing，只有一个 matched-budget dense adapter。

$$\Delta_{\text{G0}}(h)=E_{1792}(h)$$

### 5.2 普通 flat MoE：`G1_flat_raw_lb`

router 和 experts 都看完整 hidden state，并加 load-balance loss。

$$q_i(h)=\operatorname{softmax}(W_Rh)_i,\quad \Delta_{\text{G1}}(h)=\sum_{i=1}^{16}q_i(h)E_{112}^{(i)}(h)$$

### 5.3 Middle-band flat MoE：`G2_flat_middle`

router 只看 middle band，但 experts 仍看完整 hidden state。

$$q_i(h)=\operatorname{softmax}(W_Rx_M)_i,\quad \Delta_{\text{G2}}(h)=\sum_{i=1}^{16}q_i(h)E_{112}^{(i)}(h)$$

### 5.4 主 Hierarchical MoE：`B2_top1_ccM_tailM`

每个 token 总是走 global expert，再 hard-select 一个 conditional path。global expert 看 $x_{\text{head}}$，conditional experts 看完整 middle band $x_M$。

$$c^{*}=\arg\max_c\operatorname{softmax}(W_Cx_M)_c,\quad s^{*}=\arg\max_{s\in\{\text{cc},\text{tail}\}}\operatorname{softmax}(W_S^{(c^{*})}x_{\text{Mcc}})_s$$

如果选择 conditional-common path：

$$\Delta_{\text{B2}}(h)=E_{256}^{g}(x_{\text{head}})+E_{128}^{\text{cc},c^{*}}(x_M)$$

如果选择 conditional-tail path：

$$f^{*}=\arg\max_f\operatorname{softmax}(W_F^{(c^{*})}x_{\text{Mtail}})_f,\quad \Delta_{\text{B2}}(h)=E_{256}^{g}(x_{\text{head}})+E_{64}^{\text{tail},c^{*},f^{*}}(x_M)$$

### 5.5 全输入 learned Hierarchical MoE：`A2_top1_rawexp_router_M`

结构和 `B2` 一样，但所有 experts 都接收完整 hidden state $h$。这是“如果专家不受 projection 限制会怎样”的 learned-router 消融。

$$c^{*}=\arg\max_c\operatorname{softmax}(W_Cx_M)_c,\quad s^{*}=\arg\max_{s\in\{\text{cc},\text{tail}\}}\operatorname{softmax}(W_S^{(c^{*})}x_{\text{Mcc}})_s$$

如果选择 conditional-common path：

$$\Delta_{\text{A2}}(h)=E_{256}^{g}(h)+E_{128}^{\text{cc},c^{*}}(h)$$

如果选择 conditional-tail path：

$$f^{*}=\arg\max_f\operatorname{softmax}(W_F^{(c^{*})}x_{\text{Mtail}})_f,\quad \Delta_{\text{A2}}(h)=E_{256}^{g}(h)+E_{64}^{\text{tail},c^{*},f^{*}}(h)$$

### 5.6 Projected-input oracle：`G12_h_condct_top1_oracle_diag`

不用 learned router，而是直接用真实 label/source 选择 path，用来测 projected-input hierarchy 的上界。

$$c^{*}=\text{true coarse label},\quad f^{*}=\text{true fine label within }c^{*}$$

如果 token 来自 coarse phrase：

$$\Delta_{\text{G12}}(h)=E_{256}^{g}(x_{\text{head}})+E_{128}^{\text{cc},c^{*}}(x_{\text{Mcc}})$$

如果 token 来自 fine phrase：

$$\Delta_{\text{G12}}(h)=E_{256}^{g}(x_{\text{head}})+E_{64}^{\text{tail},c^{*},f^{*}}(x_{\text{Mtail}})$$

### 5.7 全输入 oracle：`G13_h_condct_top1_oracle_raw_all_diag`

也直接使用真实 label/source 选择 path，但所有 experts 都接收完整 hidden state $h$。

$$c^{*}=\text{true coarse label},\quad f^{*}=\text{true fine label within }c^{*}$$

如果 token 来自 coarse phrase：

$$\Delta_{\text{G13}}(h)=E_{256}^{g}(h)+E_{128}^{\text{cc},c^{*}}(h)$$

如果 token 来自 fine phrase：

$$\Delta_{\text{G13}}(h)=E_{256}^{g}(h)+E_{64}^{\text{tail},c^{*},f^{*}}(h)$$

## 6. 最小结论

第一，`B2_top1_ccM_tailM` 是当前最能代表我们目标的 learned top-1 sparse Hierarchical MoE。它比 matched dense、flat raw MoE、middle-band flat MoE 都略好，尤其在 fine-source token 和 rare-bucket token 上更明显。

第二，`A2_top1_rawexp_router_M` 说明“所有 experts 都看完整 hidden state”并没有让 learned Hierarchical MoE 变强，反而整体 loss 明显变差。这说明问题不只是 expert 输入信息不够；全输入会削弱层级约束，使 learned router 更难形成有效分工。

第三，`G13_h_condct_top1_oracle_raw_all_diag` 说明：如果 path 已经由真实 label/source 指定，全输入 oracle 仍然很强，尤其 fine-source loss 最好。但它的 overall loss 略差于 projected-input oracle `G12`。这支持一个更细的判断：专家可以接收更多信息，但 learned routing 阶段仍然需要结构化约束。

最短结论：

> top-1 Hierarchical MoE 已经训出部分有效层级信号，但还没有自然恢复真实 hierarchy。当前瓶颈不是单纯的专家容量，而是 learned router/path selection 与 expert specialization 的对齐。下一步应优先做 oracle-distilled router training 或 advantage-aware router training。
