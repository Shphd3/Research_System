# Meeting Brief - Feature-Zipf Synthetic Hierarchical MoE

## One-Sentence Main Message

这次 feature-Zipf synthetic 实验支持“Hierarchy 能恢复一部分分层计算机制”，但更准确地说，Hierarchy 的优势现在主要体现在 function-level recovery，而不是 sparse feature division；feature-level 分工最强的 learned baseline 反而是 flat middle spectral routing。

## Background

我们的长期目标是做能够“一学就会、尽量不遗忘”的 Hierarchical MoE。为此需要先弄清楚：expert specialization 到底应该怎么定义。过去如果只看 routing frequency、Leaf NMI 或 loss，很容易把不同层面的现象混在一起。

这次实验把 Zipf 放在 sparse feature 的出现频率上，而不是直接让 leaf label 服从 Zipf。这样更接近语言里的 common / group / unique feature 结构。

## Hypothesis

如果 hidden representation 由 hierarchical sparse Zipfian features 生成，那么 Hierarchical MoE 应该比 flat MoE 更能：

1. 按 fine-grained sparse features 分 expert；
2. 让 expert function 对齐真实输出机制。

## Experiment

实验包含两种输出机制：

- variable-A：不同 group / unique 有不同输出函数，用来测试功能机制恢复；
- fixed-A：所有样本共享输出函数，用来测试输入 feature 本身是否诱导 routing 分化。

比较模型包括 random flat、flat $Wh$ + common + LB、flat middle spectral + common、Hier full_input、Hier conditional_input、oracle flat 和 oracle Hier。

## Results

三个最重要观察：

1. Oracle flat / Hier 都能达到 Leaf NMI 1.000，说明 synthetic mechanism 是可恢复的。
2. Learned Hierarchical 的 function cos 比 flat learned models 略高，variable-A 下 Hier conditional_input 达到 0.796，是 learned models 中最高。
3. Feature-level 指标上，Hierarchical 没有明显超过 flat middle spectral；flat middle spectral 在 Leaf NMI 和 sparse dictionary division 上是当前最强 learned baseline。

## Interpretation

当前应该把 specialization 拆开讲：

- feature-level specialization：模型是否按 sparse features 分 expert；
- function-level specialization：expert 函数是否对齐真实机制。

Hierarchy 目前更像是帮了 function-level recovery；middle spectral routing 更像是帮了 sparse feature division。二者还没有在一个 learned hierarchical architecture 里统一起来。

## Claim Boundary

可以说：

- Feature-Zipf synthetic 比 leaf-Zipf synthetic 更合理；
- oracle 证明机制可恢复；
- learned routers 有弱 sparse feature signal；
- Hierarchical MoE 有 function-level recovery 信号；
- middle spectral routing 是当前最强 feature-division 信号。

不能说：

- Hierarchical MoE 已经比 flat MoE 更会按 sparse features 分工；
- learned hierarchical router 已经恢复真实 leaf mechanism；
- synthetic 结果已经证明真实语言 hidden state 中也会成立。

## Next Step

下一步不要直接堆更复杂 hierarchy，而是先解释 middle spectral routing 为什么强，并设计实验把 feature-level specialization 和 function-level specialization 分开测。

## Backup

需要保留的表和图：

- variable-A 主结果表；
- fixed-A 控制结果表；
- sparse dictionary 诊断表；
- PCA log-y spectrum，用来解释 middle spectral router 的有效谱段。
