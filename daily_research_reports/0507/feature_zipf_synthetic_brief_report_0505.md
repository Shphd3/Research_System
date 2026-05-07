# Feature-Zipf Synthetic Hierarchical MoE 简报

## 目的

构造一个更贴近自然语言的合成 hidden representation，检查 Hierarchical MoE 是否比普通 MoE 更能：

1. 把激活不同 sparse features 的样本分给不同 expert；
2. 让 expert 函数恢复真实分层机制；
3. 在 sparse dictionary 诊断中呈现更清晰的 feature 分工。

## 为什么这样构造数据

旧构造是直接让 leaf label 服从 Zipf。这个设定更像“语义类别频率服从 Zipf”，但不太像自然语言。

新构造改成：Zipf 作用在 sparse feature 的出现频率上。也就是高频的是通用 feature，中频的是 group feature，低频的是 unique feature。粗粒度/细粒度 label 不是直接采样出来的，而是由激活到的 feature 决定。

类比自然语言：

| feature 类型 | 例子 | 含义 |
|---|---|---|
| common | the, is, 标点, 常见句法 | 很多样本都会出现 |
| group | 数学、代码、医学 | 表示粗粒度上下文 |
| unique | 线性代数、排序算法、心电图 | 表示细粒度语义 |

数据形式：

$$h=\frac{1}{\sqrt{|S(x)|}}\sum_{j\in S(x)}a_je_j+\epsilon$$

其中 $S(x)$ 是样本激活的 sparse feature 集合。

样本分三类：

| 类型 | 概率 | 激活内容 | 是否进入 router NMI |
|---|---:|---|---|
| common-only | 0.40 | common | 否 |
| group-only | 0.35 | common + group | 是 |
| group+unique | 0.25 | common + group + unique | 是 |

变输出机制：

$$y=(A_{\text{common}}+\mathbf 1[c]A_c+\mathbf 1[f]A_{c,f}^{tail})h+\eta$$

固定输出机制：

$$y=A_{\text{common}}h+\eta$$

固定输出实验只回答：输入 feature 本身是否能产生路由分化。它不用于证明 expert 学到了不同输出机制。

## 训练设置

本地 2 卡完成。变输出机制跑在 GPU 0，固定输出机制跑在 GPU 1。

统一设置：

$$d=1024,\quad C=10,\quad F=10,\quad \text{leaf paths}=100$$

$$\text{train}=20000,\quad \text{valid}=5000,\quad \text{test}=5000$$

$$\text{epochs}=30,\quad \text{batch}=256,\quad \text{lr}=0.003$$

seeds 为 $[0,1,2]$。

普通 MoE 和 Hierarchical MoE 的 learned 主模型参数量一致：

$$5,427,200$$

普通 MoE 也加了 always-on common expert；这个 common expert 不参与 router NMI。

## 主结果：变输出机制

| 模型 | Loss ↓ | Leaf NMI ↑ | Feature selectivity ↑ | Function cos ↑ |
|---|---:|---:|---:|---:|
| Random flat | 0.000403 | 0.226 | 0.264 | 0.715 |
| Flat $Wh$ + common + LB | 0.000160 | 0.235 | 0.270 | 0.780 |
| Flat middle spectral + common | 0.000161 | 0.260 | 0.279 | 0.775 |
| Hier full_input | 0.000163 | 0.234 | 0.290 | 0.786 |
| Hier conditional_input | 0.000160 | 0.235 | 0.279 | 0.796 |
| Oracle flat | 0.000105 | 1.000 | 0.776 | 0.825 |
| Oracle Hier conditional_input | 0.000116 | 1.000 | 0.776 | 0.973 |

简短结论：

- Oracle 证明这个数据中的机制是可恢复的。
- Learned 模型都明显强于 random flat loss。
- Hierarchical 的 function cos 略高于普通 MoE，说明它更贴近分层输出机制。
- 但 Leaf NMI 和 feature selectivity 上，Hierarchical 没有明显压过 flat middle spectral。也就是说：目前不能强 claim “Hierarchical 更会按 sparse feature 分工”。

## 主结果：固定输出机制

| 模型 | Loss ↓ | Leaf NMI ↑ | Feature selectivity ↑ | Function cos |
|---|---:|---:|---:|---:|
| Random flat | 0.000100 | 0.226 | 0.264 | 0.715 |
| Flat $Wh$ + common + LB | 0.000104 | 0.236 | 0.270 | 0.716 |
| Flat middle spectral + common | 0.000104 | 0.259 | 0.278 | 0.716 |
| Hier full_input | 0.000109 | 0.235 | 0.280 | 0.716 |
| Hier conditional_input | 0.000106 | 0.246 | 0.280 | 0.716 |
| Oracle flat | 0.000100 | 1.000 | 0.776 | 0.716 |

简短结论：

- 固定 $A$ 后，学习式路由仍比 random 有一点 feature selectivity 提升。
- 但所有模型的 function cos 基本一样，因为输出函数已经没有 group/unique 差异。
- 这说明输入 sparse feature 本身能提供弱路由信号；但清晰的 expert 专业化仍主要需要不同输出机制推动。

## Sparse Dict 诊断

主字典设置：

$$K_{\text{dict}}=256,\quad \text{sparsity}=8$$

稳定性检查：

$$K=128,\quad \text{sparsity}=5$$

$$K=512,\quad \text{sparsity}=10$$

变输出机制下的 hard routing 结果：

| 模型 | Atom selectivity ↑ | Atom diversity ↑ | Top atom overlap ↓ |
|---|---:|---:|---:|
| Random flat | 0.077 | 0.451 | 0.135 |
| Flat $Wh$ + common + LB | 0.085 | 0.494 | 0.116 |
| Flat middle spectral + common | 0.089 | 0.550 | 0.100 |
| Hier full_input | 0.088 | 0.492 | 0.124 |
| Hier conditional_input | 0.085 | 0.485 | 0.129 |
| Oracle flat | 0.617 | 0.687 | 0.074 |

稳定性结论：

- $K=128,256,512$ 下趋势一致。
- Flat middle spectral 的 sparse dict 分工指标最强。
- Hierarchical 高于 random，但没有稳定高于 flat MoE。
- Oracle 明显更高，说明 sparse dict 指标能识别真实路径上界。

## 谱图

已生成 log y-axis PCA 谱图：

`results/figures/feature_zipf_spectral_distribution/`

包括：

- `feature_zipf_variable_A/seed_mean_spectrum_logy.png`
- `feature_zipf_fixed_A/seed_mean_spectrum_logy.png`

这些图用于检查 feature-Zipf 数据是否形成谱各向异性，以及 middle spectral router 的 $17:207$ 区间是否落在有效谱段。

## 总结

这版数据构造更合理：Zipf 作用在 sparse feature 上，而不是直接作用在语义 label 上。

目前结果支持三点：

1. 输入 sparse feature 本身可以带来弱路由分化；
2. 变输出机制会明显加强 expert 专业化；
3. Hierarchical MoE 在函数恢复上略优于普通 MoE，但在 sparse feature 分工上还没有明显优于 flat middle spectral MoE。

因此当前最稳的说法是：

> 在 feature-Zipf synthetic 数据上，Hierarchical MoE 能恢复一部分分层计算机制；但“Hierarchical 比普通 MoE 更会按 sparse features 分工”这个 claim 还不够强。当前更强的现象是 middle spectral routing 对 sparse feature 分工更有帮助。
