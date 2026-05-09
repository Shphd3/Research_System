# Feature-Zipf 合成实验当前结果汇报稿

说明：本稿用于汇报 Feature-Zipf synthetic 实验。主体部分只保留结论和关键结果；更细的数据构造解释放在后面。

## 目的

构造一个可控的 hidden representation 空间，检查 Hierarchical MoE 和普通 Flat MoE 是否能：

1. 把激活不同 sparse features 的样本分给不同 expert/path；
2. 让不同 expert/path 的函数真的依赖这些 sparse features；
3. 恢复真实的分层计算机制。

## 一句话结论

当前结果说明：

> Hierarchical MoE 在恢复真实分层计算函数上略强于普通 Flat MoE；但没有证据表明它比 Flat MoE 更稳定地按 sparse features 分工。

最关键的三点：

- **路由分工**：Flat middle spectral routing 的 sparse atom 分化最强；
- **函数依赖**：只有当不同语义真的对应不同计算函数时，expert 才明显依赖 group / unique sparse atoms；
- **机制恢复**：Hierarchical conditional_input 的 Function cos 为 0.796，高于 Flat $Wh$ + common + LB 的 0.780，但低于 Oracle Hier 的 0.973。

## 数据构造

我们把一个 hidden vector 看成少量 sparse features 的叠加：

$$h=\frac{1}{\sqrt{|S(x)|}}\sum_{j\in S(x)}a_je_j+\epsilon$$

其中 $e_j$ 是真实 sparse feature 方向，$a_j$ 是该 feature 在当前样本中的强度。

真实 features 分三层：

| 层级 | 数量 | 直观含义 |
|---|---:|---|
| common | 16 | 高频通用成分，例如功能词、普通句式、通用表达 |
| group | $10\times6=60$ | 粗粒度语义成分，例如数学、法律、医学这类上下文 |
| unique | $10\times10\times1=100$ | 细粒度语义成分，例如特征值分解、合同违约、心电图 ST 段 |

样本分三类：

| 样本类型 | 概率 | 激活内容 | 例子 |
|---|---:|---|---|
| common-only | 0.40 | common | 普通日常表达，没有明确领域语义 |
| group-only | 0.35 | common + group | 有数学上下文，但没有具体到某个子概念 |
| group+unique | 0.25 | common + group + unique | 数学 + 特征值分解 |

Zipf 作用在 feature 出现频率上：有些 common / group / unique features 更常被抽到，有些更少见。这样比“直接让完整语义标签服从 Zipf”更接近自然语言里的高频通用成分和低频具体成分。

我们跑两类任务：

| 任务 | 直观含义 | 输出函数 |
|---|---|---|
| 语义相关计算任务 | 不同语义需要不同计算 | $$y=(A_{\text{common}}+\mathbf 1[c]A_c+\mathbf 1[f]A_{c,f}^{tail})h+\eta$$ |
| 共享计算对照 | 所有语义做同一种计算，只保留输入 feature 差异 | $$y=A_{\text{common}}h+\eta$$ |

共享计算对照用于回答：如果输出函数完全一样，仅靠输入 feature 不同，是否也会形成清晰 expert 分工。

## 训练设置

| 模型 | Path 数 | 参数量 | 说明 |
|---|---:|---:|---|
| Random flat | 100 | - | 随机路由下界 |
| Flat $Wh$ + common + LB | 100 | 5.427M | 普通线性 MoE |
| Flat middle spectral + common | 100 | 5.427M | router 只看 PCA middle band |
| Hier full_input | 10 coarse × 10 fine | 5.427M | 分层路由，expert 输入完整 $h$ |
| Hier conditional_input | 10 coarse × 10 fine | 5.427M | 分层路由，expert 输入对应谱投影 |
| Oracle flat | 100 | - | 使用真实 leaf path |
| Oracle Hier | 10 coarse × 10 fine | - | 使用真实 coarse/fine path |

所有 learned 模型参数量对齐，训练数据和训练配置一致：

$$d=1024,\quad \text{train}=20000,\quad \text{valid}=5000,\quad \text{test}=5000,\quad \text{seeds}=[0,1,2]$$

## 分析结果

### 1. 是否把激活不同 sparse atoms 的样本分给不同 path

做法：先用 sparse dictionary 表示 hidden：

$$h\approx Dz$$

然后统计每个 path 收到的样本主要激活哪些 atoms。

| 指标 | 含义 |
|---|---|
| Atom selectivity ↑ | 同一个 atom 是否集中进入少数 path |
| Atom diversity ↑ | 不同 path 的 atom profile 是否不同 |
| Top atom overlap ↓ | 不同 path 的 top atoms 是否重复 |

语义相关计算任务结果：

| 模型 | Atom selectivity ↑ | Atom diversity ↑ | Top atom overlap ↓ |
|---|---:|---:|---:|
| Random flat | 0.077 | 0.451 | 0.135 |
| Flat $Wh$ + common + LB | 0.085 | 0.494 | 0.116 |
| Flat middle spectral + common | **0.089** | **0.550** | **0.100** |
| Hier full_input | 0.088 | 0.492 | 0.124 |
| Hier conditional_input | 0.085 | 0.485 | 0.129 |
| Oracle Hier conditional_input | 0.617 | 0.687 | 0.074 |

结论：

> learned routing 确实能分开一部分 sparse atom profile，但 Hierarchical 没有超过 Flat MoE。当前最强的是 Flat middle spectral routing。

### 2. expert/path 是否真的依赖 sparse atoms

做法：把 sparse dictionary 中的 group + unique atoms 从 hidden 中移除，保持原路由路径不变，再看 loss 上升多少。loss 上升越多，说明模型越依赖这些 sparse atoms。

| 模型 | 语义相关计算：移除 group+unique 后 loss 增量 ↑ | 共享计算对照：移除 group+unique 后 loss 增量 |
|---|---:|---:|
| Random flat | 0.000032 | 0.000032 |
| Flat $Wh$ + common + LB | 0.000186 | 0.000031 |
| Flat middle spectral + common | 0.000185 | 0.000031 |
| Hier full_input | 0.000186 | 0.000031 |
| Hier conditional_input | 0.000186 | 0.000031 |
| Oracle Hier conditional_input | 0.000215 | 0.000031 |

结论：

> 当不同语义对应不同计算函数时，learned models 会明显依赖 group / unique sparse atoms；当所有语义共享同一个输出函数时，这种依赖基本消失。

这说明 expert 的功能分工不是单靠输入 feature 不同自动形成的，而是由“不同 feature 需要不同计算”推动的。

但 Flat 和 Hierarchical 的 loss 增量几乎一样，因此不能说 Hierarchical 更会使用 sparse atoms。

### 3. 是否恢复真实分层计算机制

这里直接比较 learned function 和真实生成函数的 cosine。Function cos 越高，说明越接近真实机制。

语义相关计算任务结果：

| 模型 | Loss ↓ | Leaf NMI ↑ | Group+Unique feature selectivity ↑ | Function cos ↑ |
|---|---:|---:|---:|---:|
| Random flat | 0.000403 | 0.226 | 0.264 | 0.715 |
| Flat $Wh$ + common + LB | 0.000160 | 0.235 | 0.270 | 0.780 |
| Flat middle spectral + common | 0.000161 | **0.260** | 0.279 | 0.775 |
| Hier full_input | 0.000163 | 0.234 | **0.290** | 0.786 |
| Hier conditional_input | **0.000160** | 0.235 | 0.279 | **0.796** |
| Oracle flat | **0.000105** | 1.000 | 0.776 | 0.825 |
| Oracle Hier conditional_input | 0.000116 | 1.000 | 0.776 | 0.973 |

结论：

> Hierarchical conditional_input 的 Function cos 最高，为 0.796，高于普通 Flat $Wh$ + common + LB 的 0.780。说明 Hierarchical 更贴近真实分层函数，但优势不大。

Oracle flat 的 loss 最低，但 Function cos 低于 Oracle Hier。这说明 Flat MoE 拿到真实 path 后也能很好预测；而 Hierarchical 的函数分解形式更贴近真实分层机制。

## 总体解释

1. **Hierarchical 不是更强的 sparse feature router。**  
   Sparse dictionary 结果显示，Flat middle spectral 的 atom diversity 最高，top atom overlap 最低。

2. **expert 会不会使用 group / unique features，取决于这些 features 是否真的对应不同计算。**  
   在语义相关计算任务中，移除 group / unique atoms 后 loss 明显上升；在共享计算对照中，这个上升消失。

3. **Hierarchical 的优势主要体现在函数结构上。**  
   它的 Function cos 略高，说明它更接近真实分层计算机制，但还远没有达到 oracle。

## 最终可汇报结论

Feature-Zipf synthetic 实验说明：当 hidden representations 由 common / group / unique sparse features 组成时，MoE 能在一定程度上利用这些 feature。若不同语义对应不同计算函数，expert 会明显依赖 group / unique features；若所有语义共享同一输出函数，这种依赖基本消失。

不过，当前实验不支持“Hierarchical MoE 比普通 MoE 更会按 sparse features 分工”。Hierarchical 的主要优势是函数形式更贴近真实分层机制，而不是路由出更清晰的 sparse atom 分工。

## 附：数据构造的直观解释

### 为什么 Zipf 放在 feature 上

自然语言里，高频的通常不是完整语义标签，而是基础成分。例如：

- 通用表达经常出现；
- 某些领域上下文偶尔出现；
- 很具体的概念更少出现。

因此我们让 feature 的出现频率服从 Zipf，而不是让完整 leaf label 服从 Zipf。一个样本可以只包含 common，也可以包含 common + group，也可以进一步包含 common + group + unique。

### 为什么需要共享计算对照

如果只做语义相关计算任务，我们看到 expert 分工后，还不知道它来自哪里：

- 是因为输入 feature 不同；
- 还是因为不同 feature 真的需要不同计算。

共享计算对照把输出函数固定成同一个。结果显示：固定后，移除 group / unique atoms 的影响接近 random。这说明清晰的 expert 函数依赖主要来自“不同语义需要不同计算”，不是输入 feature 差异本身自动造成的。
