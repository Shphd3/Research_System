# MoE Continual Learning 项目故事线

这个项目想回答一个问题：为什么 MoE 在持续学习里会忘记旧任务，以及什么样的 MoE 结构更适合不稳定、长尾、组合式的数据。

最开始的直觉是：真实数据不是均匀、独立、密集的。一个样本通常只激活少数 latent feature；有些 feature 很常见，有些很稀有；feature 之间还有层级、共现、互斥和组合关系。因此，普通 MoE 如果只靠线性 router 分专家，可能无法把这些 feature 清楚分开，导致不同知识被塞进同一批专家，后续训练就会覆盖旧知识。

项目第一阶段先把“数据性质”说清楚，而不是直接发明模型。核心性质包括：稀疏激活、长尾频率、feature 依赖、层级结构、组合低秩，以及新旧任务之间的函数冲突。随后构造了一个可控 synthetic 数据世界：样本由 global、middle、leaf 三层 feature 组成。global 覆盖所有样本，middle 覆盖子树，leaf 覆盖细类，所以 long-tail 不是类别采样不均，而是 feature coverage 不同。

早期实验发现一个反直觉现象：普通 MoE 的专家确实没有干净地按 feature 分工，很多专家混合接收大量 feature；但只要新旧任务共享同一个输入输出规则，遗忘并不明显，甚至可能因为第二阶段训练而变好。这说明“feature 混合”本身不足以解释遗忘。

于是项目引入了更关键的概念：rule。rule 表示同一批 feature 应该如何被解释成输出。真正危险的情况不是两个任务共享 feature，而是共享 feature 却需要不同 mapping。比如同一个颜色特征，在不同对象上可能代表完全不同含义。此时如果 router 把这些冲突 rule 送进同一个专家，第二阶段更新就会覆盖第一阶段学到的解释。

因此当前结论是：MoE 遗忘来自“feature overlap + rule conflict + routing specialization 不足”。新的 MoE 思路不是简单增加专家，而是让结构更符合数据性质：common feature 可以共享，rare 或冲突 rule 需要专门保护；global/middle/leaf 层级结构适合 hierarchical routing；专家不仅要按 feature 分工，也要按 rule-conditioned mapping 分工。

和普通 MoE 相比，这个方向的 MoE 更强调三点：第一，router 不能只被高方差 common feature 主导；第二，需要 shared expert 处理通用结构，同时用 specialized expert 保护细粒度和冲突结构；第三，评估模型不能只看 loss，还要看 expert purity、feature overlap、routing stability、旧数据分发漂移和 rare feature retention。

当前项目还不能 claim 已经提出了最终最优 MoE。更稳妥的说法是：项目已经把 MoE 遗忘问题从“专家是否分 feature”推进到“专家是否分 feature 与 rule mapping”，并给出了一个更可诊断的数据模型和实验解释框架。它对现在的帮助是：后续设计 MoE 时，可以先问数据有什么结构、冲突在哪里、哪些知识该共享、哪些知识必须隔离，而不是盲目调整专家数或 router 形式。
