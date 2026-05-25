# 组会 30s 发言稿 - 从 Uniform Router 到 Zipfian

参考材料：

```text
Projects/from-attention-to-search/XingyuD/sync/0524_router_feature_specialization/report.md
Projects/from-attention-to-search/XingyuD/sync/0525_zipfian_hierarchical/report.md
```

## 30s 版本

**目的**：我这部分想回答一个问题：稀疏 MoE 里的 router 把 token 分给不同 expert 时，这个分工到底有没有功能意义。也就是说，不只是“看起来分到不同 expert”，而是某个 expert 被拿掉以后，某一类样本的 loss 会不会真的明显变差。

**假设**：一开始我们的假设是，如果 hidden state 里已经有语义边界，或者我们用语义信息初始化 router，那么 router 最后应该能形成比较稳定的语义专家分工。比如同一个 B token 在不同上下文里，应该能被分到有不同功能的 expert。

**结论**：0524 的 uniform AB/CB 实验说明，这个假设不成立。语义初始化确实能让一开始的 routing 更像语义分组，但训练之后这个结构会衰减；即使我们在训练后的 hidden state 上重新构造一个语义 router，任务 loss 可以恢复，但专家的功能分工仍然不稳定。所以现在最安全的结论是：**hidden state 可分，不等于 expert 有功能分工；routing 图上看起来有语义结构，也不能直接当作证据。**

**证据**：主要证据有三点。第一，semantic initialization 只提高 step-0 的语义 routing，final routing 仍然退化。第二，训练后的 hidden state 里确实还能恢复 B-context 的边界，但直接换成这个 semantic router 会明显伤任务 loss，说明它和已经训练出来的 expert 功能不匹配。第三，重新 refresh semantic router 后，loss 能恢复，但语义 routing 继续衰减，ablation 指标也没有稳定提升。这里的 ablation 指标意思是：拿掉某个 expert，看某类样本的 loss 是否特别受影响，用它判断 expert 是否真的有功能。

**下一步为什么做 Zipfian**：uniform 实验已经说明“语义可分”本身不够。真实语言里 token 频率不是均匀的，有些词非常常见，有些很少见，所以我下一步转到 Zipfian 数据，不是随便换数据集，而是想测试：这种频率不均衡会不会让 flat router 更倾向于按 token 本身、常见程度、common meaning 分，而不是按上下文里的具体含义分。

## Zipfian 实验目的

**H0529a 的目的**：先只看 flat router。构造一个更像词义歧义的 synthetic setup：同一个 token $b_i$ 有一个普通含义 `r b_i`，也有两个上下文含义 `A b_i` 和 `C b_i`。训练时让 token 频率服从 Zipfian 分布，但每个 token 内部的上下文比例保持均衡。这样可以单独测试：**token 频率不均衡会不会削弱低频 token 的上下文功能分工。**

**H0530a 的目的**：如果频率确实造成问题，再比较一个两层结构：第一层处理 common meaning，第二层处理 context-conditioned sense。也就是看显式拆开“普通词义”和“上下文词义”能不能改善 expert 的功能分工。

**关键判断指标**：我不再把 routing heatmap 当主证据，而是看两个指标：

- `S_sense`：某个 expert 是否对某个上下文含义有特别大的功能贡献；
- route-function alignment：router 最常分到的 expert，是否真的是 ablation 后最重要的 expert。

## 当前 Zipfian 结果一句话

H0529a 结果是：Zipfian 改变了 expert 的负载分布，但没有削弱低频 token 的功能分工，所以“token 频率不均衡本身就是主要失败原因”这个强假设被削弱。

H0530a 结果是：当前这个简单 hierarchy 没有改善功能分工；它让 routing 更像 token/family 分组，但低频部分的 route-function alignment 反而变差。这进一步说明：**让 routing 看起来更有结构，不等于 expert 真正有功能。**

## 可直接读的 1 分钟版本

我这部分主要想回答：稀疏 MoE 里的 router 有没有学出真正有功能意义的 expert 分工。这里的“有功能意义”不是看 heatmap 上 token 分到哪里，而是把某个 expert 拿掉以后，某一类样本的 loss 会不会真的明显变差。

在 0524 的 uniform AB/CB 实验里，我们先测试了一个比较自然的假设：如果 hidden state 里已经有语义边界，或者我们用语义信息初始化 router，那么最终应该能形成比较稳定的语义 expert 分工。但结果是否定的。semantic initialization 只影响训练一开始；训练后 routing 会退化。训练后的 hidden state 里其实还能恢复 B-context 的边界，但 learned router 不会自然使用它。更关键的是，即使用当前 hidden state 重新构造 semantic router，任务 loss 可以恢复，专家的功能分工仍然不稳定。

所以这一步的结论是：hidden state 语义上可分，不等于 expert 有功能分工；routing 图上看起来有语义结构，也不能直接作为 expert specialization 的证据。

基于这个结论，我下一步转到 Zipfian synthetic setup。原因是 uniform 数据太理想化，而真实语言里 token 频率高度不均匀。所以 Zipfian 实验不是无端换数据，而是为了测试频率不均衡会不会把 flat router 拉向 token 本身、常见程度或者 common meaning，而不是上下文里的具体含义。H0529a 先比较 uniform flat 和 Zipfian flat；H0530a 再比较 flat Zipfian 和一个 common/sense 两层 MoE。主指标仍然是 ablation-based 功能指标，而不是 routing heatmap。

## 文件链接

H0529a Zipfian frequency shortcut:

```text
Purpose card:
Projects/from-attention-to-search/main/hypotheses/H0529a_zipfian_frequency_shortcut/purpose_card.md

Closure:
Projects/from-attention-to-search/main/hypotheses/H0529a_zipfian_frequency_shortcut/hypothesis_closure.md

Summary:
Projects/from-attention-to-search/main/experiments/H0529a_zipfian_frequency_shortcut/summary.md
```

H0530a Hierarchical common/sense MoE:

```text
Purpose card:
Projects/from-attention-to-search/main/hypotheses/H0530a_hierarchical_common_sense_moe/purpose_card.md

Closure:
Projects/from-attention-to-search/main/hypotheses/H0530a_hierarchical_common_sense_moe/hypothesis_closure.md

Summary:
Projects/from-attention-to-search/main/experiments/H0530a_hierarchical_common_sense_moe/summary.md
```

## 不要这样说

不要说：

```text
Zipfian 更真实，所以一定更好。
Hierarchy 已经是修复方向。
routing heatmap 有结构，所以 expert 已经 specialization。
```

更安全的说法：

```text
Zipfian 是为了测试频率不均衡是否放大 route 和 expert function 的不匹配。
Hierarchy 是一个机制对照，不是已经确认的解决方案。
最终判断要看 ablation 后的功能贡献，而不是只看 routing 图。
```
