# Advisor Questions - Feature-Zipf Synthetic

## 1. 如果 flat middle spectral 已经最好，Hierarchy 的意义在哪里？

Short answer:

Hierarchy 现在的意义不是已经赢了 feature-level 分工，而是在 function-level recovery 上有信号。当前结果说明 hierarchy 方向要收缩，不能强 claim，但也不该直接放弃。

Evidence:

- Hier conditional_input function cos = 0.796，是 learned models 中最高；
- flat middle spectral Leaf NMI = 0.260，sparse dict division 指标最好。

Better wording:

“当前 hierarchy 还没有统一 feature-level 和 function-level 两种 specialization。下一步要解释 middle spectral 的 feature-level 优势，并尝试把它并入 hierarchy。”

## 2. 为什么这个 toy model 有意义？

Short answer:

它的意义不是模拟完整自然语言，而是在机制已知的受控世界里测试架构是否能恢复 sparse hierarchical mechanisms。

Evidence:

- Oracle Leaf NMI = 1.000，说明机制可恢复；
- fixed-A / variable-A 区分了 input feature signal 和 output function mechanism。

Better wording:

“这个 toy model 是 controlled experiment，不是自然语言替代品。它帮我们判断哪些 specialization 指标有解释力。”

## 3. fixed-A 中仍有 feature selectivity，应该怎么解释？

Short answer:

fixed-A 说明输入 sparse feature 本身可以诱导弱 routing differentiation，但因为输出函数相同，它不能证明 expert 学到了不同功能。

Evidence:

- fixed-A 下 function cos 基本相同；
- Leaf NMI 和 feature selectivity 有小幅差别。

Better wording:

“fixed-A 是控制组，用来拆开 input-feature signal 和 output-function specialization。”

## 4. 下一步为什么不是直接做更复杂 Hierarchical MoE？

Short answer:

因为现在的问题不是模型不够复杂，而是 feature-level 和 function-level specialization 的来源还没分清。

Evidence:

- oracle 强，但 learned hierarchy 未追上 oracle；
- middle spectral 的 feature-level signal 强于 hierarchy。

Better wording:

“下一步最诊断的是解释 middle spectral 为什么有效，而不是先增加 hierarchy 复杂度。”
