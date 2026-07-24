# NTP 在什么条件下形成条件低功能秩的 ROOT 表示？

**今日唯一决策问题：**E02 是否已经足以让我们暂停当前 A14_02 合成表面，
转向最小 Transformer 的 Jacobian/path-image 理论；还是弱的 above-chance
信号值得再做一次能力操作化？

## 已固定的理论认识（AI 填入，研究者核对）

- 我们不证明“树、长程或 NTP 天然低秩”，而是研究：全局高容量系统在给定
  输入和任务后，是否只需少量 ROOT 方向保持 next-token 功能。
- 受控定理成立形式是：低维任务充分变量、独立 context 消噪、优化不系统
  写入 nuisance、概率稀疏活动和共享 Jacobian/path image 同时成立时，固定
  原输出头所需的 ROOT 功能秩以高概率不超过 $sr$。
- 该定理允许不同活动模式使用不同局部子空间，也允许完整模型全局高维。
- 唯一核心数学缺口是：一般 Transformer 中能否从 attention 与 NTP 更新
  推出共享 Jacobian/path image，而不是直接把它写入假设。

理论来源：[从静态树到 NTP 条件功能秩](../0724/docs/从静态树到NTP条件功能秩_概率稀疏层级计算完整理论论文.md)。

## 决定性实验结果（AI 填入，研究者核对）

- reserved 4×H100 full run `pt-zecsxjd8` 已 `SUCCEEDED`；10/10 单元、生成器
  和泄漏守卫全部通过，因此结果不是实现失败或证据不足。
- shared 与 lookup 的已见配对新 context 能力均为 5/5 通过，平均 accuracy
  为 0.9990 与 0.9949，排除了“基础任务没有学会”。
- shared 未见组件配对为 0/5 通过，平均 accuracy 0.2125，低于 0.80 门槛；
  四个 held-out pair 均低于 0.70。正式预注册裁定为 `fail`。
- shared 在每个配对 seed 中都高于 lookup，但在 0.088–0.515 间波动。这是
  弱的 partial-structure 信号，不足以证明可复用组合算法。

结果来源：[E02 中文摘要](../../Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E02_component_recombination_capability/summary_cn.md)。

## 认识更新概述

- **理论更新：**正式结论是附带条件的 ROOT 任务功能秩定理，不是 raw hidden
  state、参数矩阵或自然语言的全局低秩定理。
- **实验更新：**多样 context 足以学习已见完整映射，却没有在当前模型中产生
  可靠组件重组；因此 E02 任务不能继续承担 shared-versus-lookup 秩比较。
- **方法更新：**任何表示秩结论之前必须先通过任务能力与固定读出效用门。
- **Router 边界：**条件低功能秩只说明“少量方向可能足够”，不说明存在多个
  不同最优专家；Router 仍需独立的条件—专家反事实效用证据。
- **不能声称：**NTP 普遍不能学习组合；模型只会 lookup；高频导致低秩；
  条件功能秩定理被 E02 否定；或低秩已经推出 Router。

## 请研究者亲自填写

- **我的当前判断（暂停 / 再做一次 / Unknown）：**______
- **我这样判断的核心理由：**______
- **我认为最强的替代解释：**______
- **什么新证据会改变我的判断：**______
- **我希望导师只裁定的一个问题：**______

## AI 建议与恢复点

- **AI 建议：**暂停当前 generator；下一步只研究最小单层单头 Transformer
  能否推出或反驳共享 Jacobian/path image。该建议不是你的最终判断。
- **恢复点：**先完成上面五个空格，再从完整理论论文第 19–20 节继续。
