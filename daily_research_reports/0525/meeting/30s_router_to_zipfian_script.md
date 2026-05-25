# 组会发言稿 - 从 Router Initialization 到 Zipfian

参考材料：

```text
Projects/from-attention-to-search/XingyuD/sync/0524_router_feature_specialization/report.md
Projects/from-attention-to-search/XingyuD/sync/0525_zipfian_hierarchical/report.md
```

## 30s 版本

**目的**：我这部分主要想检查一个问题：稀疏 MoE 里面的 router 把 token 分给不同 expert，这个分工到底是不是真的有功能意义。这里的功能意义不是看 routing 图上分得好不好看，而是把某个 expert 拿掉以后，某一类样本的 loss 会不会真的明显变差。

**假设**：我们一开始沿着 initialization 这条线做。直觉是：如果模型内部的 hidden state 已经有语义边界，那我用语义信息初始化 router，应该能帮助 router 最后形成稳定的语义专家分工。比如同一个 B token，在单独出现、A 上下文、C 上下文里，应该被分给不同功能的 expert。

**结论**：0524 的 uniform AB/CB 结果说明，这个假设不成立。语义初始化确实能让训练一开始的 routing 更像语义分组，但训练后这个结构会衰减；即使用训练后的 hidden state 重新构造一个语义 router，任务 loss 可以恢复，但 expert 的功能分工仍然不稳定。所以现在的结论是：**初始化能提供一个语义起点，但普通训练目标不会自动把这个语义分组保持成真正有功能的 expert 分工。**

**证据**：有三点。第一，semantic initialization 只提高最开始的 B-context routing，训练后优势消失。第二，训练后的 hidden state 里仍然能恢复 B-context 边界，但 learned router 不会自然使用它。第三，把 router 重新 refresh 成语义方向后，loss 能恢复，可是语义 routing 继续衰减，ablation 指标也没有稳定提升。这里 ablation 的意思是拿掉某个 expert，看某类样本 loss 是否特别受影响；它比 routing 图更能说明 expert 有没有真正功能。

**下一步**：所以我不再继续只调 initialization。下一步转到 Zipfian 数据，是为了问一个更接近语言分布的问题：真实语言里 token 频率很不均匀，这种频率差异会不会让 flat router 更容易按 token 本身、常见程度或者普通词义分，而不是按上下文里的具体含义分。

## 1 分钟版本

**目的**：我这部分想回答的是，稀疏 MoE 的 router 学到的 expert 分工到底有没有功能意义。我的判断标准不是 routing heatmap，而是功能性指标：如果拿掉某个 expert，某一类样本的 loss 是否会明显变差。

**假设**：0524 这条线主要围绕 initialization。我们的初始假设是，如果 hidden state 里本来就有语义边界，那么用语义信息初始化 router，应该能帮助最终形成稳定的语义 expert 分工。也就是说，同一个 B token 在不同上下文里，router 应该能分到不同 expert，并且这些 expert 对对应上下文真的有预测贡献。

**结论**：结果是否定的。semantic initialization 只改变训练一开始的 routing，训练后这个语义结构会衰减。更进一步，训练后的 hidden state 里其实仍然有可恢复的 B-context 语义边界，但 learned router 不会自然使用它。即使我们在当前 hidden state 上重新构造 semantic router，任务 loss 可以恢复，专家的功能分工还是不稳定。所以我现在的结论是：**问题不只是初始化不好，而是 router 的分发目标、expert 的实际功能、普通 next-token prediction 训练目标没有自动对齐。**

**证据**：第一，semantic initialization 提高了 step-0 的 B-context 分组，但 final routing 不保持。第二，post-hoc 换成语义 router 会明显伤任务 loss，说明“语义上可分”的 route 不等于当前 trained experts 可用的 route。第三，semantic refresh 后 loss 能恢复，但 B-context routing 继续衰减，功能性 ablation 指标没有稳定提升。也就是说，图上看起来更语义，不等于 expert 真的有对应功能。

**下一步为什么是 Zipfian**：基于这个结果，我下一步不是继续调 initialization，而是换到 Zipfian hierarchical-sense 数据。这个转向不是随便换数据，而是因为 uniform 数据太理想化；真实语言里 token 频率高度不均匀。Zipfian 实验要测试的是：频率不均衡会不会让 flat router 更偏向 token identity、常见词、普通含义这些 shortcut，而不是上下文里的具体含义。

**具体实验目的**：H0529a 先只比较 uniform flat 和 Zipfian flat，看 Zipfian 频率是否削弱低频 token 的上下文功能分工。H0530a 再比较 flat Zipfian 和两层 common/sense MoE，看显式拆开“普通词义”和“上下文词义”是否能改善 expert 的功能分工。主指标仍然是 ablation-based 功能指标和 route-function alignment，而不是 routing heatmap。

## Zipfian 实验怎么接上来

**从 0524 到 0525 的逻辑**：

```text
0524: semantic initialization 不够。
原因不是 hidden state 完全没有语义边界，而是训练不会自动把语义边界变成 expert 的功能分工。

所以 0525: 测试更接近语言的数据压力。
真实语言里 token 频率不均匀，Zipfian setup 用来检查 frequency pressure 会不会进一步放大这个 route-function mismatch。
```

**Zipfian 数据的直观含义**：

```text
r b_i: token b_i 的普通 / 默认含义
A b_i: token b_i 在 A 上下文里的含义
C b_i: token b_i 在 C 上下文里的含义
```

可以类比成一个词在不同上下文里有不同意思。这个实验不是为了模拟完整语言，而是为了控制住一个问题：同一个 token 的普通含义和上下文含义，router 到底会按哪个来分。

## H0529a：Zipfian Frequency Shortcut

**目的**：测试 token 频率不均匀时，flat router 是否更难形成低频 token 的上下文功能分工。

**假设**：如果频率是主要问题，那么 Zipfian 训练下，低频 token 的上下文功能分工应该比 uniform 更差。

**结论**：这个强假设被削弱。Zipfian 确实改变了 expert 的负载分布，但没有降低低频 token 的功能分工指标。

**证据**：

```text
flat_uniform tail S_sense: 0.0451
flat_zipfian tail S_sense: 0.0612

flat_uniform tail alignment: 0.7777
flat_zipfian tail alignment: 0.7930

flat_uniform load entropy: 0.8143
flat_zipfian load entropy: 0.5218
```

解释：Zipfian 让专家负载更集中，但没有证明“频率不均匀本身会让低频上下文功能分工变差”。

链接：

```text
Projects/from-attention-to-search/main/hypotheses/H0529a_zipfian_frequency_shortcut/purpose_card.md
Projects/from-attention-to-search/main/hypotheses/H0529a_zipfian_frequency_shortcut/hypothesis_closure.md
Projects/from-attention-to-search/main/experiments/H0529a_zipfian_frequency_shortcut/summary.md
```

## H0530a：Hierarchical Common/Sense MoE

**目的**：测试两层结构能不能改善 Zipfian setup 下的 expert 功能分工。第一层处理普通含义，第二层处理上下文含义。

**假设**：如果 common meaning 和 context sense 分开处理有帮助，那么 hierarchy 应该提高低频上下文功能分工。

**结论**：当前这个简单 hierarchy 没有改善，反而让低频部分的 route-function alignment 明显变差。

**证据**：

```text
flat_zipfian tail S_sense: 0.0612
hierarchical_zipfian tail S_sense: 0.0465

flat_zipfian tail alignment: 0.7930
hierarchical_zipfian tail alignment: -0.0693

flat_zipfian tail CE: 0.0055
hierarchical_zipfian tail CE: 0.0920
```

解释：hierarchy 让 routing 更像 token/family 分组，但没有让 expert 的实际功能更好。这再次说明，routing 看起来更有结构，不等于 expert 真正有功能。

链接：

```text
Projects/from-attention-to-search/main/hypotheses/H0530a_hierarchical_common_sense_moe/purpose_card.md
Projects/from-attention-to-search/main/hypotheses/H0530a_hierarchical_common_sense_moe/hypothesis_closure.md
Projects/from-attention-to-search/main/experiments/H0530a_hierarchical_common_sense_moe/summary.md
```

## 最后一句可以这样收

所以这条线现在给我的结论是：**问题不是简单地初始化得不够语义，也不是简单换成 Zipfian 或 hierarchy 就能解决；真正需要解决的是 router 把样本分给 expert 的规则，和这个 expert 对 loss 的实际贡献之间怎么对齐。**

## 避免这样说

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
最终判断要看拿掉 expert 后的功能贡献，而不是只看 routing 图。
```
