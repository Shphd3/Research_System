# MoE-input 修正版结果报告

本报告替换旧版 sparse dict 分析结果。旧版分析取的是 decoder layer input，也就是 attention block 之前的输入；这不能代表 expert 实际收到的表征。

本次修正后，分析对象改为 MoE block 输入：每层 attention 之后、post-attention layernorm 之后、进入 MLP/MoE 之前的 hidden state。也就是 expert/path 真正接收的输入。

## 目的

探究 Hierarchical MoE 与普通 Flat MoE 在真实 DCLM 表征数据上训练后，是否：

1. 把激活不同 sparse atoms 的 token 分给不同 expert/path；
2. 不同 expert/path 的计算是否真的依赖自己收到的主要 atoms；
3. Hierarchical 内部是否出现 coarse 到 fine 的分层分工迹象。

## 一句话结论

修正到 MoE 输入后，当前证据仍不支持“Hierarchical 比 Flat 更会把不同 atoms 分到不同 path”。Flat raw top-1 + LB 的 path-atom 分化最强。

但可以确认两点：第一，各模型确实依赖自己 path 上的主要 atoms；第二，Hierarchical 内部存在正的 coarse block gap，说明它有可观察的层级分工迹象，但这个迹象较弱，不能直接等同于恢复真实语义层级。

## 训练与分析设置

| 模型 | 层数 | 最终 path 数 | 训练 tokens | 参数量 | 分发方式 |
|---|---:|---:|---:|---:|---|
| Flat raw top-1 + LB | 8 | 16 | 5B | 441.863M | raw hidden，top-1，带 LB |
| Flat middle spectral top-1 | 8 | 16 | 5B | 441.863M | middle spectral band，top-1，不带 LB |
| Hierarchical full_input | 8 | 16 | 5B | 441.896M | 4 coarse × 4 fine，expert 接收 full hidden |
| Hierarchical conditional_input | 8 | 16 | 5B | 441.896M | 4 coarse × 4 fine，expert 接收对应 band 输入 |

四个模型使用相同 DCLM shard、相同数据顺序、相同 batch 设置、相同训练 token 数。Flat 和 Hierarchical 参数量差约 0.007%，可以视为参数量对齐。

Sparse dict 设置：每层使用同一套 shared dictionary，`n_atoms=256`。四个模型同一层的 heatmap 使用相同 atom 列顺序和相同颜色范围。

## 结果 1：是否把不同 atoms 的 token 分给不同 path

看法：对每个 path，统计它收到的 token 平均激活哪些 sparse atoms。如果不同 path 的 atom profile 差异越大，说明分发越分化。

Layer 7 结果：

| 模型 | Atom diversity ↑ | Top atom overlap ↓ | UsageNorm |
|---|---:|---:|---:|
| Flat raw top-1 + LB | 0.229 | 0.379 | 0.999 |
| Flat middle spectral top-1 | 0.104 | 0.439 | 0.967 |
| Hierarchical full_input | 0.036 | 0.661 | 0.992 |
| Hierarchical conditional_input | 0.030 | 0.669 | 0.995 |

跨层 atom diversity：

| Layer | Flat raw + LB | Flat middle | Hier full_input | Hier conditional_input |
|---|---:|---:|---:|---:|
| 1 | 0.573 | 0.398 | 0.248 | 0.264 |
| 3 | 0.548 | 0.286 | 0.100 | 0.087 |
| 5 | 0.431 | 0.143 | 0.063 | 0.068 |
| 7 | 0.229 | 0.104 | 0.036 | 0.030 |

结论：Hierarchical 的 UsageNorm 接近 1，说明不是 path collapse；但是它的 atom diversity 明显低、top atom overlap 明显高，说明不同 path 收到的 sparse atom profile 更相似。当前结果不能支持“Hierarchical 比 Flat 更会把不同 atoms 分给不同 path”。

图 1：Layer 7 四个模型的 path-atom heatmap。

![四个模型 path-atom heatmap](figures/fig1_shared_atoms_side_by_side_layer_7_moe_input.png)

## 结果 2：expert/path 是否真的依赖自己收到的主要 atoms

看法：对每个 path 找到它平均激活最强的 atoms，把这些 atoms 从 MoE 输入中移除，再重新过完整模型。若 loss 或 MoE 输出变化明显大于随机移除 atoms，说明这些 atoms 对模型计算有实际影响。

Layer 7，移除 top 16 atoms：

| 模型 | 原始 loss | 移除 top atoms 后 loss 增量 | 随机移除后 loss 增量 | top-random loss gap | MoE 输出变化 gap |
|---|---:|---:|---:|---:|---:|
| Flat raw top-1 + LB | 4.023 | 0.522 | 0.085 | 0.437 | 0.610 |
| Flat middle spectral top-1 | 4.082 | 0.553 | 0.113 | 0.440 | 0.532 |
| Hierarchical full_input | 4.112 | 0.508 | 0.120 | 0.389 | 0.484 |
| Hierarchical conditional_input | 4.163 | 0.567 | 0.153 | 0.414 | 0.457 |

结论：四个模型的 top path atoms 都不是装饰性的。移除 top atoms 后，loss 上升明显大于随机移除，说明 path 主要 atoms 对模型输出有真实影响。

但这只能说明“模型使用了这些 atoms”，不能说明“不同 path 使用了更不一样的 atoms”。结合结果 1，Hierarchical 的 path 之间 atom profile 更相似，因此不能说 Hierarchical 更会学习互异的 sparse atoms。

图 2：移除 top atoms / random atoms 后的 LM loss 增量。

![移除 path 主要 atoms 后的 loss 增量](figures/fig4_true_atom_loss_delta_layer_7_moe_input.png)

图 3：top atoms 相对 random atoms 的 loss gap。

![top-random loss gap](figures/fig5_true_atom_loss_gap_layer_7_moe_input.png)

图 4：移除 atoms 后的 MoE 输出相对变化。

![MoE 输出变化](figures/fig6_true_atom_moe_output_change_layer_7_moe_input.png)

## 结果 3：Hierarchical 是否出现层级分工迹象

Hierarchical 的最终 path 写成：

$$path=4c+f$$

因此 path 0-3 属于 coarse 0，path 4-7 属于 coarse 1，依此类推。我们按 coarse block 排列 path，并比较：

$$coarse\ block\ gap = coarse\ 间差异 - coarse\ 内差异$$

如果该值大于 0，说明不同 coarse block 之间比同一 coarse 内部更不同。

| Layer | Hier full_input | Hier conditional_input |
|---|---:|---:|
| 1 | 0.148 | 0.106 |
| 3 | 0.043 | 0.031 |
| 5 | 0.030 | 0.034 |
| 7 | 0.016 | 0.012 |

结论：coarse block gap 在所有层都是正数，说明 Hierarchical 内部确实有 coarse block 结构。但这个 gap 从浅层到深层变小，Layer 7 上已经较弱。因此更稳妥的说法是：Hierarchical 出现了分层分工迹象，但当前真实语料实验不能证明它恢复了真实语义层级。

图 5：Hierarchical full_input 的 coarse block heatmap。

![Hierarchical full_input coarse block heatmap](figures/fig2_hier_full_layer_7_coarse_block_heatmap_moe_input.png)

图 6：Hierarchical conditional_input 的 coarse block heatmap。

![Hierarchical conditional_input coarse block heatmap](figures/fig3_hier_conditional_layer_7_coarse_block_heatmap_moe_input.png)

## 对三个问题的直接回答

**问题 1：Hierarchical 是否更会把激活不同 features 的 token 分给不同 expert/path？**

不能。MoE-input 修正后，Flat raw top-1 + LB 的 atom diversity 最高，Hierarchical 的 atom diversity 最低、top atom overlap 最高。这说明 Hierarchical path 之间接收的 atom profile 更相似。

**问题 2：Hierarchical 是否让不同 expert/path 真的使用不同的表征？**

只能回答一半。四个模型都使用了自己 path 上的主要 atoms，因为移除 top atoms 后 loss 明显上升。但 Hierarchical 不一定使用了更“不同”的 atoms；它的 path profile 更相似，所以不能说它比 Flat 更会学到互异表征。

**问题 3：Hierarchical 是否恢复真实分层计算机制？**

不能直接证明。真实 DCLM 没有真实 coarse/fine 标签。我们只能说 Hierarchical 内部出现了 coarse block 结构，即不同 coarse block 的 atom profile 比 block 内更不同。

## 建议写进正文的最终结论

使用 MoE block 输入重新分析后，当前结果不支持“Hierarchical MoE 比 Flat MoE 有更强的 path-level sparse atom 分化”。Flat raw top-1 + LB 的分发更分散，Hierarchical 的不同 path 共享更多 atoms。

不过，各模型的 path 主要 atoms 对模型输出都有实际影响；移除这些 atoms 会显著提高 loss，说明 sparse dict 捕捉到的是模型实际使用的表征，而不只是可视化噪声。

Hierarchical MoE 仍然表现出弱的层级结构：按 `path=4c+f` 排列后，coarse block 间差异稳定大于 block 内差异。但由于真实语料没有真实层级标签，这只能说明模型内部有分层分工迹象，不能直接说明恢复了真实语义层级。

## 本次修正说明

旧分析对象：decoder layer input，位置在 attention block 之前。  
新分析对象：MoE block input，位置在 attention 之后、post-attention layernorm 之后、进入 MoE/MLP 之前。  

因此，本报告中的结果比旧版更贴近“expert 实际收到什么表征”。
