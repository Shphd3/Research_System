# Daily Research Report - 0507

## Today's Goal

把 feature-Zipf synthetic 实验从“结果简报”整理成可以更新主线、进入 claim board、并用于组会汇报的科研判断。

## What I Did

- 阅读并整理 `feature_zipf_synthetic_brief_report_0505.md`。
- 将实验抽象为 `E001 Feature-Zipf Synthetic Hierarchical MoE` experiment card。
- 更新主线判断和 claim board。
- 准备 0507 组会汇报材料。

## Key Results

Feature-Zipf 数据构造比直接让 leaf label 服从 Zipf 更合理，因为它把 Zipf 放在 sparse feature 出现频率上，更接近 common / group / unique feature 的语言结构。

实验结果显示：

- oracle 证明该 synthetic mechanism 是可恢复的；
- learned routers 比 random 有弱但稳定的 feature signal；
- Hierarchical MoE 在 function cos 上有优势信号；
- 但 Hierarchical MoE 没有明显超过 flat middle spectral MoE 的 Leaf NMI 和 sparse dictionary feature division 指标。

## Interpretation

当前最重要的更新是：specialization 不能再只当成一个概念。它至少要拆成两个层面：

1. feature-level specialization：专家是否按 sparse feature 分工；
2. function-level specialization：专家函数是否对齐真实输出机制。

这次实验中，Hierarchy 更像是在 function-level recovery 上给出弱正信号，而 flat middle spectral routing 反而是 feature-level division 的最强 learned baseline。

## Problems / Blockers

当前不能强讲：

- Hierarchical MoE 已经比 flat MoE 更会按 sparse features 分工；
- learned hierarchy 已经恢复真实 leaf mechanism；
- synthetic 结果已经能直接迁移到真实语言 hidden states。

真正卡住的问题是：为什么 middle spectral routing 对 sparse feature division 最强，以及怎样让 hierarchy 在 learned router 下也获得这个 feature-level 优势。

## Tomorrow's Plan

下一步优先设计一个更诊断性的实验，把 feature-level specialization 和 function-level specialization 分开测：

- 按 frequency band 看 routing entropy 和 expert utilization；
- 对比 function-level alignment 与 feature-level selectivity 是否由不同结构驱动；
- 解释 middle spectral routing 的有效谱段为什么对应 sparse feature division。

## Questions For Advisor

1. 当前是否应该把主张降级为“Hierarchy 有 function-level recovery 信号，但 feature-level division 还不强”？
2. middle spectral routing 的优势应作为下一步机制解释重点，还是先尝试更强 hierarchy 结构？
3. 真实 hidden state 迁移前，synthetic 里还缺哪一个关键诊断？
