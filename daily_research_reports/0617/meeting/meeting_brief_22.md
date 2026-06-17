# Meeting Brief: A06_E01 2x2 Expert-Geometry Metric Audit

Use this as a short group-meeting reading surface. It is not a replacement for
`summary.md` or `detailed.md`.

## Question

Core question:

theory_proof\theoretical_analysis.md中给出了关于2维情形下，使用m个随机中心根据余弦相似度分发，为什么不能够形成均匀分发。
我们探索的问题在于：在两个 $2\times2$ experts 和二维均匀输入中，哪一种由 expert 初始化矩阵诱导的路由分数 $q_e(x)$ 可以作为下一步路由器初始化构造的核心几何对象？

Why it matters to the mainline:

如果先不确定 $q_e(x)$，后续路由器的训练、近似和负载控制都没有清楚目标。这个实验先审计“直接用分数最高者分配”的理想静态规则，而不是证明训练一定会学到它。

Current subproblem:

我们使用以下几种分数进行实验：
M1 signed prototype: $q_e(x)=x^\top m_e$。  
M2 unsigned prototype: $q_e(x)=(x^\top m_e)^2$。  
M3 top-1 projection: $q_e(x)=\|V_{e,1}^\top x\|^2$。  
M3 full-span control: $q_e(x)=\|V_{e,1:2}^\top x\|^2$。  
M4 matrix response: $q_e(x)=x^\top A_e^\top A_ex=\|A_ex\|^2$。

比较 M1/M2/M3/M4 在最小二维设置下是否能同时支持两个目标：第一，均匀分布的 feature 能被均匀分到两个 experts；第二，分配不是随机凑均匀，而是被选中的 expert 对该 feature 的分数更高，并且分数优势足够清楚。后文把第二点简称为“由分数定义的专家偏好”。

## Conclusion

One-sentence summary:

二维情形下，M3-top1形式（也就是专家输入侧第一奇异向量） 是高维低秩近似初始化的首选，M4 的“完整专家矩阵响应能量”是当前最能够反映专家矩阵结构的核心分发分数定义；

但在后续外推到高维情形时，我们发现专家输入侧第一奇异向量并不能将均匀空间完成均匀分划，因此应该同步微调专家网络的初始化方式，让专家top-1的输入侧向量均匀分划整个d维空间。

更新：

1. 2*2情形下，所有方法都能均匀分发，需要考虑的是分发的分数是否与专家矩阵结构相关。
2. M3-top1 在 uniform disk 上也能接近 50/50，因此它是合理的低秩近似候选。
3. M4 的优势是保留完整专家矩阵响应；在二维实验里，它给出的分发 margin 明显大于 M3-top1。
4. 在 uniform disk 上，trace-centered M4，也就是 $x^\top(G_e-\mathrm{tr}(G_e)I/2)x$，仍然能接近 50/50 分发；但因为圆盘里有小模长点，分数优势会变小。

## Setup

Only include setup details needed to judge the evidence.

Data / task:

二维输入从 uniform disk 采样：

$$
x\sim\mathrm{Unif}(\{x:\|x\|\le 1\}).
$$

这是“二维空间中均匀分布的表征”的最小版本。实验中使用两个 $2\times2$ expert matrices，并在多个随机 expert pairs 上统计平均结果。今天汇报只展开 uniform disk，不展开其它二维区域或条件编号。

Model / router（模型 / 路由规则）:

两个 $2\times2$ expert matrices $A_1,A_2$。路由规则是理想静态规则：$g(x)=\arg\max_e q_e(x)$，也就是把 $x$ 分给分数最高的 expert；这里没有训练。

Comparison:

M1 signed prototype: $q_e(x)=x^\top m_e$。  
M2 unsigned prototype: $q_e(x)=(x^\top m_e)^2$。  
M3 top-1 projection: $q_e(x)=\|V_{e,1}^\top x\|^2$。  
M3 full-span control: $q_e(x)=\|V_{e,1:2}^\top x\|^2$。  
M4 matrix response: $q_e(x)=x^\top A_e^\top A_ex=\|A_ex\|^2$。

A06_E02 中额外区分三个 M4：

raw M4: $x^\top G_ex$。  
trace-centered M4: $x^\top(G_e-\mathrm{tr}(G_e)I/2)x$，这是二维证明要用的对象。  
distribution-centered M4: $x^\top G_ex-\mathbb{E}_{x\sim P}[x^\top G_ex]$，这是一个容易混淆的对照；半径变化时它不等价于 trace-centered M4。

Primary metric:

`metric_validity` 是主判据；审核时必须同时读自然负载误差、平均分数优势、退化比例和符号敏感性。最重要的是平均分数优势，因为它回答“分发是否带有可分辨的 expert 偏好”，而不是只回答“数量是否 50/50”。

Important omission:

本实验不包含可训练路由器、不包含真实 MoE、不包含语义特化、不包含高维公共成分移除，也不证明真实训练会学到 M4 的理想分配规则。

## Key Evidence

1. **M4 是更合适的核心分数定义**
   Evidence:
   在非退化 expert pairs 上比较 prototype、top-1 projection 和完整矩阵响应。
   Result:
   在单位圆实验中，M4 的平均分数优势最大；在 uniform disk 实验中，trace-centered M4 仍然保持接近 50/50 分发。
   Interpretation:
   M4 不只是构造一个均匀分割；它使用的是完整 expert 矩阵响应，因此比只取一个 prototype 或一个 top singular direction 更接近我们想要的 expert-aware routing。

2. **其他方法也能分开 feature，但证据更弱**
   Evidence:
   M1/M2/M3-top1 在对称分布下也可以得到接近均匀负载。
   Result:
   在 uniform disk 上，M3-top1 的负载误差 = 0.0030，平均分数优势 = 0.2587；trace-centered M4 的负载误差同样 = 0.0030，但平均分数优势 = 0.9702。也就是说，M3-top1 能均分，但分数优势明显小于 M4。
   Interpretation:
   这些方法不是失败方法，但更适合作为 baseline 或低秩近似候选；它们不能替代 M4 作为完整 expert 几何对象。

3. **只看负载均匀不够**
   Evidence:
   线性分割、prototype 分割、top-1 projection 分割都可能在对称分布上得到均匀负载。
   Result:
   均匀负载本身只能说明“数量分开了”，不能说明“expert 矩阵真的更适合处理被分到的 feature”。
   Interpretation:
   审核时必须同时看 load 和 margin；margin 才回答分配是否有清楚的 expert 偏好。

4. **Uniform disk 支持二维证明不是单位圆 artifact**
   Evidence:
   A06_E02 在同样的 $2\times2$ experts 上，把输入从单位圆改成 uniform disk，也就是圆盘内均匀填点。
   Result:
   对非退化 expert pairs 取平均，trace-centered M4 在 uniform disk 上的负载误差 = 0.0030，平均分数优势 = 0.9702。对比单位圆，负载仍接近 50/50，但分数优势约变成原来的一半。
   Interpretation:
   半径变化本身不会破坏分发，因为 trace-centered M4 的分数差会乘上 $r^2$，符号不变；但小模长点会让 margin 变小。所以 uniform disk 的结论是：能均分，但 confidence 比单位圆弱。

5. **trace-centered M4 和 distribution-centered M4 不能混用**
   Evidence:
   在随机 expert pairs 中，uniform disk 上 raw M4 会偏向平均响应能量更大的 expert；trace-centered M4 明显改善负载。
   Interpretation:
   二维证明要写的是 $x^\top(G_e-\mathrm{tr}(G_e)I/2)x$。如果只减整个分布上的均值，半径变化时可能引入新的阈值效应，不能作为同一个证明对象。

## Boundary

This conclusion does not cover:

- 不证明可训练路由器能自动学到 M4。
- 不证明真实 MoE collapse 已解决。
- 不证明语义 feature 特化，也不证明 feature 被分到某个 expert 后一定带来真实任务收益。
- 不证明高维低秩近似和 common removal 已经成立。
- 不证明 `metric_validity` 这种有效/无效二值判据在近似相同 experts 上足够严格。
- 本次汇报不展开其他二维区域实验；这里只用 uniform disk 说明“空间中均匀分布”的 2D 版本仍支持 trace-centered M4。

## Next Step

Next decision:

是否把 trace-centered M4 写成二维证明对象，并把 M4 的矩阵响应能量作为下一轮路由器构造目标，同时把 M3-top1 当作低维近似候选？

Next minimal experiment or action:

先完成二维证明：对单位圆和 uniform disk 说明为什么 trace-centered M4 能 50/50，以及为什么 uniform disk 的 margin 约减半。高维今天不展开；目前直接把二维二次 metric 外推到高维线性 gating 还没有形成清楚可用的结果。下一步需要同时考虑两件事：一是是否要修改 expert 初始化，让专家几何更容易被 router 读出；二是如何把 M4/M3 这类二次 metric 映射成高维线性 gating 可以初始化的形式。
