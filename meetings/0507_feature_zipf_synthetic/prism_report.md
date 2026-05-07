# PRISM Report - Feature-Zipf Synthetic Hierarchical MoE

## 1. Report Purpose

这份报告要裁决一个具体问题：在更合理的 feature-Zipf synthetic 数据上，Hierarchical MoE 是否真的比 flat MoE 更能形成 expert specialization。

这里的关键不是“哪个模型 loss 最低”，而是区分：

- sparse feature 是否被分给不同 experts；
- expert function 是否恢复真实输出机制；
- 哪些 claim 可以进入组会汇报。

## 2. Research Background

我们的长期目标是设计能够支持“一学就会、尽量不遗忘”的 Hierarchical MoE。这个目标要求模型把共享知识和可塑的长尾知识分开处理。

但要推进这个方向，必须先把“expert specialization”定义清楚。一个 expert 被频繁选中，或者 Leaf NMI 略高，并不等于它学到了有功能意义的机制。

因此这次实验把问题放到受控 synthetic 世界中：我们知道真实 sparse features、真实 group / unique structure 和真实输出函数，然后检查不同 MoE 是否能恢复这些结构。

## 3. Current Hypothesis

强版本假设：

如果 hidden representation 由 hierarchical sparse Zipfian features 生成，那么 Hierarchical MoE 应该同时优于 flat MoE 的 feature-level specialization 和 function-level specialization。

当前被支持的弱版本：

Hierarchical MoE 能恢复一部分分层计算机制，尤其在 function-level recovery 上有弱正信号。

当前没有被支持的部分：

Hierarchical MoE 还没有明显优于 flat middle spectral MoE 的 sparse feature division。

## 4. Modeling / Mechanism

数据构造为：

$$
h=\frac{1}{\sqrt{|S(x)|}}\sum_{j\in S(x)}a_je_j+\epsilon
$$

其中 $S(x)$ 是样本激活的 sparse feature 集合。

Zipf 不直接作用在 leaf label 上，而是作用在 sparse feature 的出现频率上：

- common feature 高频出现；
- group feature 中频出现；
- unique feature 低频出现。

variable-A 设置：

$$
y=(A_{\text{common}}+\mathbf 1[c]A_c+\mathbf 1[f]A_{c,f}^{tail})h+\eta
$$

fixed-A 设置：

$$
y=A_{\text{common}}h+\eta
$$

fixed-A 是控制组，只能说明输入 feature 是否诱导 routing 分化，不能说明 expert 学到了不同输出机制。

## 5. Empirical Evidence

### Evidence 1: Oracle 证明机制可恢复

实验观察：

- Oracle flat 和 Oracle Hier 的 Leaf NMI 都达到 1.000。
- Oracle Hier conditional_input 在 variable-A 下 function cos 达到 0.973。

支持什么：

- 这个 synthetic mechanism 本身是可恢复的；
- 指标能识别真实路径上界。

不支持什么：

- 这不代表 learned router 已经学会真实机制。

### Evidence 2: Learned routers 有弱 sparse feature signal

实验观察：

- learned models 在 variable-A 下 loss 明显优于 random flat；
- Leaf NMI 和 feature selectivity 比 random 有小幅提升。

支持什么：

- sparse features 本身能提供弱路由信号；
- learned routers 不是完全随机。

仍然存在的解释：

- 这些提升还可能来自 spectral preprocessing、common expert、load balancing 或参数结构，不一定是 hierarchy 自身造成。

### Evidence 3: Hierarchy 的 function-level 信号强于 feature-level 信号

实验观察：

- variable-A 下 Hier conditional_input 的 learned function cos 为 0.796，高于 flat learned baselines；
- 但 Leaf NMI 和 feature selectivity 没有明显超过 flat middle spectral。

支持什么：

- Hierarchical MoE 对 function-level mechanism recovery 有弱正信号。

不支持什么：

- 不能说 Hierarchical MoE 更会按 sparse features 分工。

### Evidence 4: Middle spectral routing 是当前最强 feature-division 现象

实验观察：

- Flat middle spectral + common 在 Leaf NMI 上达到 0.260，是 learned models 中最高；
- sparse dictionary diagnostics 中，它也有最高 atom diversity 和最低 top atom overlap。

支持什么：

- middle spectral routing 对 sparse feature division 有明确诊断信号。

需要解释什么：

- 为什么 $17:207$ 这个中间谱段能帮助 sparse feature 分工；
- hierarchy 如何吸收这个优势。

## 6. Current Interpretation

当前最稳的解释是：specialization 至少有两个不同层面。

第一是 feature-level specialization，即专家是否按 sparse feature 或 feature combination 分工。

第二是 function-level specialization，即专家函数是否对齐真实输出机制。

这次实验中，Hierarchical MoE 更像是改善了 function-level recovery；flat middle spectral routing 更像是改善了 feature-level division。下一步的关键不是继续堆模型，而是解释这两个信号为什么分离。

## 7. Claims To Downgrade

不要说：

- Hierarchical MoE 已经证明比 flat MoE 更适合 sparse feature specialization；
- learned hierarchy 已经恢复真实 leaf routing；
- synthetic 结果已经证明真实语言 hidden state 中存在同样结构；
- fixed-A 结果证明 expert 有功能性 specialization。

可以说：

- Feature-Zipf 是更合理的 synthetic diagnostic；
- oracle 证明 mechanism recoverable；
- learned routing 有弱 sparse feature signal；
- Hierarchical 有 function-level recovery 信号；
- middle spectral routing 是当前最值得解释的 feature-level 现象。

## 8. Next Iteration

下一轮最小推进问题：

> 为什么 middle spectral routing 对 sparse feature division 最强，而 Hierarchical MoE 只在 function-level recovery 上更强？

建议实验：

1. 按 common / group / unique 或 frequency band 统计 routing entropy 和 expert utilization；
2. 分开报告 feature-level metrics 与 function-level metrics；
3. 对 middle spectral router 的谱段做 ablation；
4. 把 middle spectral preprocessing 加入 hierarchical router，判断 hierarchy 是否能继承 feature-level 优势。

## 9. Meeting Version

### 30 秒版本

我这次汇报的是 feature-Zipf synthetic 实验。相比之前直接让 leaf label 服从 Zipf，这次把 Zipf 放在 sparse feature 出现频率上，更接近语言里的 common、group、unique feature 结构。核心结论是：这个机制在 oracle 下是可恢复的，learned routers 也确实有弱的 sparse feature signal；但 Hierarchical MoE 目前没有明显超过 flat middle spectral MoE 的 sparse feature 分工。更准确地说，Hierarchy 的优势现在主要体现在 function cos，也就是函数机制恢复；而 middle spectral routing 是当前最强的 feature-level 分工信号。下一步我想重点解释为什么 middle spectral 有效，并把 feature-level 和 function-level specialization 分开诊断。

### 1 分钟版本

我这次想回答的问题是：如果语言中的长尾不是 label 本身长尾，而是 sparse feature 的出现频率长尾，那么 Hierarchical MoE 是否更容易恢复真实机制。为此我构造了 feature-Zipf synthetic 数据：common feature 高频，group feature 中频，unique feature 低频，label 由激活到的 features 决定。实验分 variable-A 和 fixed-A，前者测试不同输出机制，后者只测试输入 feature 是否能诱导路由分化。

结果是，oracle flat 和 oracle hierarchical 都能达到 Leaf NMI 1，说明机制本身可恢复。learned models 比 random 强，说明 sparse feature 确实有路由信号。但最关键的是，Hierarchical MoE 在 function cos 上有优势信号，却没有在 Leaf NMI 和 sparse dictionary 指标上明显超过 flat middle spectral MoE。因此我现在会把 claim 降级：Hierarchy 能恢复一部分分层计算机制，特别是 function-level recovery；但 feature-level sparse division 目前最强的是 middle spectral routing。下一步应该解释 middle spectral 为什么有效，并设计实验把 feature-level 和 function-level specialization 分开。

## 10. Likely Questions

### Question 1: 既然 Hierarchical 没有赢 flat middle spectral，为什么还要做 hierarchy？

Short answer:

因为 hierarchy 仍然在 function-level recovery 上有信号，但它还没有解决 feature-level division。现在不是放弃 hierarchy，而是要找出如何让 hierarchy 继承 middle spectral 的 feature 分工优势。

Evidence:

Hier conditional_input 在 learned models 中 function cos 最高；但 flat middle spectral 在 Leaf NMI 和 sparse dict 指标上最好。

How to redirect back to the mainline:

这说明 specialization 要拆成 feature 和 function 两层，下一步的主线就是把这两层统一起来。

### Question 2: synthetic 结果和真实语言有什么关系？

Short answer:

这次 synthetic 不是模拟完整自然语言，而是在机制已知的受控世界里测试可恢复性和诊断指标。

Evidence:

Zipf 作用在 sparse feature 上，而不是 label 上；common/group/unique 的设计对应语言中的高频通用结构、粗粒度上下文和细粒度语义。

How to redirect back to the mainline:

如果 synthetic 中都不能分清 feature-level 和 function-level specialization，就不应该直接在真实 hidden state 上讲强 claim。

### Question 3: 为什么 fixed-A 还有 feature selectivity？

Short answer:

fixed-A 中输出函数相同，所以它不能证明 functional specialization；它只能说明输入 sparse feature 本身会诱导弱路由分化。

Evidence:

fixed-A 下 function cos 基本一样，但 Leaf NMI / feature selectivity 仍有小幅差异。

How to redirect back to the mainline:

这正好说明我们需要把 input-feature routing signal 和 output-function specialization 分开。
