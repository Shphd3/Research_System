# 组会 30s 发言稿 - 从语义初始化到 Zipfian

参考材料：

```text
Projects/from-attention-to-search/XingyuD/sync/0524_router_feature_specialization/report.md
Projects/from-attention-to-search/XingyuD/sync/0525_zipfian_hierarchical/report.md
```

## 30s 白话版

**目的**：我这部分想回答一个很具体的问题：MoE 里的 router 把 token 分给不同 expert，这个分工到底有没有真正的功能意义。我的判断标准不是路由图看起来分得好不好，而是把某个 expert 拿掉以后，某一类样本的 loss 会不会真的明显变差。

**假设**：这条线一开始是沿着“初始化”来做的。我们的直觉是，如果模型的 hidden state 里本来就有语义边界，那我把 router 一开始就初始化到这个语义方向，它最后应该更容易形成稳定的语义专家分工。比如同一个 B token，在单独出现、A 上下文、C 上下文里，应该被分给不同 expert，而且这些 expert 应该真的对对应上下文有预测贡献。

**结论**：结果说明，初始化不是决定性原因。语义初始化确实能让训练刚开始的 routing 更像我们想要的语义分组，但训练之后这个结构会衰减；训练后的 hidden state 里仍然能恢复出语义边界，可 learned router 不会自然使用它。即使用训练后的 hidden state 重新构造一个语义 router，loss 可以恢复，但 expert 的功能分工仍然不稳定。所以现在更安全的结论是：问题不是“router 一开始没放对位置”，而是普通 next-token prediction 训练目标没有自动把“语义分组”和“expert 的真实功能”对齐。

**证据**：第一，语义初始化把 step-0 的 B-context routing NMI 从接近随机提高到 `0.3124`，说明初始化本身是有效干预。第二，训练到最后后，这个 B-context routing NMI 掉到 `0.0468`，接近随机初始化的水平。第三，功能性指标没有稳定提升，`S_AB` 仍然只有 `1/4` seed 出现正向结构。这里的功能性指标是指：拿掉某个 expert 后，特定样本的 loss 是否特别变差，这比 routing heatmap 更能说明 expert 有没有实际功能。

**下一步为什么转 Zipfian**：既然 uniform 实验已经说明“语义初始化不够”，下一步不是继续调初始化，而是问一个更接近语言分布的问题：真实语言里 token 频率很不均匀，这种频率差异会不会让 flat router 更容易按 token 本身、常见程度或者普通词义分，而不是按上下文里的具体含义分。所以我设计了 Zipfian hierarchical-sense 数据来测试这个问题。

## 1 分钟版

**目的**：我想检查 sparse MoE 的 router 分工是不是有功能意义。这里“功能意义”不是指路由图看起来有结构，而是指某个 expert 对某一类样本的预测真的有因果贡献。具体说，就是 ablation：把一个 expert 拿掉，看哪一类样本的 loss 增加最多。

**假设**：0524 这一轮主要沿着 initialization 这条线。假设是：如果 hidden state 里已经有语义边界，那么语义初始化应该能帮助 router 最终形成稳定的语义专家分工。比如 B token 在三种上下文里出现：`B_only`、`AB`、`CB`。如果初始化有效，router 应该能从一开始就更倾向于区分这三种 B 的上下文角色，并且训练后这个分工应该变成真正有用的 expert 功能。

**语义初始化怎么做**：我们不是随便指定 expert，也不是直接看标签硬分。具体做法是：

1. 先用模型收集 router 看到的 hidden state。
2. 只看 B token 在三种上下文里的表示：`B_in_B_only`、`B_in_AB`、`B_in_CB`。
3. 分别算这三类 hidden state 的中心点。
4. 再用整体协方差做一个白化处理，让方向更像“能区分这三类上下文”的方向，而不是只看原始均值大小。
5. 最后把前三个 expert 的 router weight 初始化成这三个方向，第四个 expert 先不给语义角色。

用公式简写就是：对每个上下文角色 $k$，先算中心点 $\mu_k$，再减掉全局中心 $\mu$，然后用协方差矩阵 $\Sigma$ 做校正：

$$
d_k = \mathrm{normalize}\left((\Sigma+\lambda I)^{-1}(\mu_k-\mu)\right)
$$

router 的第 $k$ 行初始化为：

$$
w_k = \alpha d_k
$$

直观理解：我把 router 的初始分界线放到“最能区分 B 的三种上下文”的方向上。

**结论**：这个初始化确实改变了起点，但没有改变终点。它能让 step-0 的 B-context routing 更语义，但训练以后 router 会离开这个语义分组，最后的 expert 功能分工仍然不稳定。所以 initialization 不是主要瓶颈。

**证据**：

1. 起点有效：语义初始化把 step-0 B-context routing NMI 从 `0.0045` 提高到 `0.3124`。
2. 训练会抹掉：训练后 B-context routing NMI 从 `0.2469` 掉到 `0.0468`，接近随机初始化。
3. 功能没稳定：最终 `S_AB` 没有跨 seed 稳定增强，semantic init 仍然只有 `1/4` seed 有正向结构。
4. 后续 refresh 也补了一个漏洞：即使用训练后的 hidden state 重新构造语义 router，loss 可以恢复，但语义 routing 继续衰减，功能性 expert 仍然不稳定。

**所以为什么要做 Zipfian**：uniform 数据太干净，各类 token 出现频率差不多。真实语言不是这样，真实语言里少数词很常见，大量词很少见。于是下一步要问：如果 token 频率变成 Zipfian，flat router 会不会更倾向于按 token 频率、普通词义、常见模式来分，而不是按上下文里的具体含义来分。

## Zipfian 实验怎么接上来

从 0524 到 0525 的逻辑是：

```text
0524: 语义初始化不够。
原因不是 hidden state 完全没有语义边界，
而是训练不会自动把语义边界变成 expert 的功能分工。

所以 0525: 换一个更接近语言分布的压力测试。
真实语言里 token 频率不均匀，
Zipfian setup 用来检查这种频率压力会不会放大 route 和 expert function 的不匹配。
```

Zipfian 数据的直观含义：

```text
r b_i: token b_i 的普通 / 默认含义
A b_i: token b_i 在 A 上下文里的含义
C b_i: token b_i 在 C 上下文里的含义
```

也就是说，同一个 token 在不同上下文里有不同意思。这个实验不是为了模拟完整语言，而是为了控制住一个问题：

```text
router 到底按 token 的普通含义 / 频率来分，
还是按上下文里的具体含义来分？
```

## H0529a：Zipfian Frequency Shortcut

**目的**：测试 token 频率不均匀时，flat router 是否更难形成低频 token 的上下文功能分工。

**假设**：如果频率是主要问题，那么 Zipfian 训练下，低频 token 的上下文功能分工应该比 uniform 更差。

**结论**：这个强假设被削弱。Zipfian 确实让 expert 负载更集中，但没有降低低频 token 的功能分工指标。

**证据**：

```text
flat_uniform tail S_sense: 0.0451
flat_zipfian tail S_sense: 0.0612

flat_uniform tail alignment: 0.7777
flat_zipfian tail alignment: 0.7930

flat_uniform load entropy: 0.8143
flat_zipfian load entropy: 0.5218
```

解释：Zipfian 让 expert 用得更不均匀，但没有证明“频率不均匀本身会让低频上下文功能分工变差”。

链接：

```text
Purpose card:
Projects/from-attention-to-search/main/hypotheses/H0529a_zipfian_frequency_shortcut/purpose_card.md

Closure:
Projects/from-attention-to-search/main/hypotheses/H0529a_zipfian_frequency_shortcut/hypothesis_closure.md

Summary:
Projects/from-attention-to-search/main/experiments/H0529a_zipfian_frequency_shortcut/summary.md
```

## H0530a：Hierarchical Common/Sense MoE

**目的**：测试两层结构能不能改善 Zipfian setup 下的 expert 功能分工。第一层处理普通含义，第二层处理上下文含义。

**假设**：如果把普通含义和上下文含义分开处理有帮助，那么 hierarchy 应该提高低频上下文功能分工。

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

解释：hierarchy 让 routing 更像 token / family 分组，但没有让 expert 的实际功能更好。这再次说明，routing 看起来更有结构，不等于 expert 真的有功能。

链接：

```text
Purpose card:
Projects/from-attention-to-search/main/hypotheses/H0530a_hierarchical_common_sense_moe/purpose_card.md

Closure:
Projects/from-attention-to-search/main/hypotheses/H0530a_hierarchical_common_sense_moe/hypothesis_closure.md

Summary:
Projects/from-attention-to-search/main/experiments/H0530a_hierarchical_common_sense_moe/summary.md
```

## 最后一句

所以这条线现在给我的结论是：问题不是简单地初始化得不够语义，也不是简单换成 Zipfian 或 hierarchy 就能解决。真正需要解决的是，router 把样本分给 expert 的规则，和这个 expert 对 loss 的真实贡献之间怎么对齐。

## 不能这么说

不要说：

```text
语义初始化完全没用。
Zipfian 更真实，所以一定更好。
Hierarchy 已经是修复方向。
routing heatmap 有结构，所以 expert 已经 specialization。
```

更安全的说法：

```text
语义初始化能改变起点，但普通训练不会自动保留成有功能的 expert 分工。
Zipfian 是为了测试频率不均衡是否放大 route 和 expert function 的不匹配。
Hierarchy 是一个机制对照，不是已经确认的解决方案。
最终判断要看拿掉 expert 后的功能贡献，而不是只看 routing 图。
```
