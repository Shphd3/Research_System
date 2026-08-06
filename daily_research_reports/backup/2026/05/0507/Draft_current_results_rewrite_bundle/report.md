# Draft 当前结果改写稿

说明：本稿用于替换 `Draft.docx` 中的旧数字和旧图。当前可直接汇报的是 `checkpoint-final / 5 epochs / 16 paths` 的分析结果。

## 目的

探究 Hierarchical MoE 与普通 Flat MoE 在真实 DCLM 表征数据上训练后，是否：

1. 把激活不同 sparse atoms 的 token 分给不同 expert/path；
2. 让不同 expert/path 的计算真的依赖自己收到的主要 atoms；
3. 在 Hierarchical MoE 内部出现 coarse 到 fine 的分层分工迹象。

## 一句话结论

当前结果不支持“Hierarchical 比 Flat 更会把不同 atoms 分到不同路径”。相反，Flat 的 path-atom profile 更分散。  
但当前结果支持两点：第一，各模型的 path 确实依赖自己收到的主要 atoms；第二，Hierarchical 内部存在 coarse block 结构，说明它出现了分层分工迹象。

## 训练设置

| 模型 | 层数 | 最终 path 数 | 训练 tokens | 参数量 | 分发方式 |
|---|---:|---:|---:|---:|---|
| Flat raw top-1 + LB | 8 | 16 | 5B | 441.863M | raw hidden, linear router, 加 LB |
| Flat middle spectral top-1 | 8 | 16 | 5B | 441.863M | middle spectral band, linear router, 不加 LB |
| Hierarchical full_input | 8 | 16 | 5B | 441.896M | 4 coarse × 4 fine，spectral router，不加 LB |
| Hierarchical conditional_input | 8 | 16 | 5B | 441.896M | 4 coarse × 4 fine，spectral router，不加 LB |

四个模型使用相同 DCLM shard、相同数据顺序、相同 batch 设置、相同训练 token 数。Flat 和 Hierarchical 参数量差约 0.007%，可以视为参数量对齐。

## 分析结果

### 1. 是否把激活不同 atoms 的 token 分给不同 path

看每个 path 收到的 token 平均激活哪些 sparse atoms。  
如果不同 path 的亮区差异越大，说明分发越分化。

Layer 7 结果：

| 模型 | Atom diversity ↑ | Top atom overlap ↓ | UsageNorm |
|---|---:|---:|---:|
| Flat raw top-1 + LB | 0.348 | 0.312 | 0.999 |
| Flat middle spectral top-1 | 0.183 | 0.384 | 0.967 |
| Hierarchical full_input | 0.076 | 0.534 | 0.992 |
| Hierarchical conditional_input | 0.064 | 0.560 | 0.995 |

结论：Flat raw top-1 + LB 的 path-atom profile 最分散；Hierarchical 两个模型的 path 之间共享 atoms 更多。因此当前结果不能说 Hierarchical 比 Flat 更会把不同 atoms 分给不同 path。

图 1：四个模型在同一组 sparse atoms 上的 path-atom heatmap。

![四个模型 path-atom heatmap](figures/fig1_shared_atoms_side_by_side_layer_7.png)

### 2. 不同 path 是否真的依赖自己收到的主要 atoms

做法：对每个 path 找到它平均激活最强的 atoms，然后把这些 atoms 从 hidden 中移除，再重新过模型。  
如果 loss 或 MoE 输出变化明显大于随机移除 atoms，说明这些 atoms 对该 path 的计算有实际影响。

Layer 7，移除 top 16 atoms：

| 模型 | 移除 top atoms 后 loss 增量 | 随机移除 atoms 后 loss 增量 | MoE 输出相对变化 |
|---|---:|---:|---:|
| Flat raw top-1 + LB |  5.273 | 0.097 | 0.919 |
| Flat middle spectral top-1 |  5.695 | 0.111 | 0.906 |
| Hierarchical full_input |  6.647 | 0.202 | 0.946 |
| Hierarchical conditional_input |  7.778 | 0.247 | 0.957 |

结论：四个模型都确实依赖自己 path 上的主要 atoms；Hierarchical 在 top-atom 移除后 loss 上升更大，说明它的计算对这些主要 atoms 更敏感。但这不等于 Hierarchical 的不同 path 使用了更不一样的 atoms，因为第一个实验显示 Hierarchical path 之间的 atom profile 反而更相似。

图 2：移除 path 主要 atoms 后的 LM loss 增量。

![移除 path 主要 atoms 后的 loss 增量](figures/fig2_true_atom_loss_delta_layer_7.png)

图 3：移除 path 主要 atoms 后的 MoE 输出相对变化。

![移除 path 主要 atoms 后的 MoE 输出变化](figures/fig3_true_atom_moe_output_change_layer_7.png)

### 3. Hierarchical 是否出现 coarse 到 fine 的分层分工迹象

Hierarchical 的最终 path 写成：

$$path=4c+f$$

因此 path 0-3 属于 coarse 0，path 4-7 属于 coarse 1，依此类推。热力图每 4 行是一组 coarse block。

如果不同 coarse block 之间的 atom profile 差异大于同一 coarse 内部差异，说明模型内部存在 coarse 层级结构。

Coarse block gap：

| Layer | Hier full_input | Hier conditional_input |
|---|---:|---:|
| 1 | 0.177 | 0.120 |
| 3 | 0.094 | 0.072 |
| 5 | 0.097 | 0.094 |
| 7 | 0.027 | 0.029 |

结论：Hierarchical 的 coarse block gap 在所有层都是正数，说明不同 coarse block 之间确实比同一 coarse 内部更不同。也就是说，Hierarchical 内部出现了 coarse 到 fine 的分层分工迹象。  
需要注意：真实 DCLM 没有人工标注的 coarse/fine 标签，因此这里不能说“恢复了真实语义层级”，只能说“模型内部形成了可观察的层级分工结构”。

图 4：Hierarchical full_input 的 coarse block heatmap。

![Hierarchical full_input coarse block heatmap](figures/fig4_hier_full_layer_7_coarse_block_heatmap.png)

图 5：Hierarchical conditional_input 的 coarse block heatmap。

![Hierarchical conditional_input coarse block heatmap](figures/fig5_hier_conditional_layer_7_coarse_block_heatmap.png)

## 建议替换 Draft 中的旧表述

### 原结论 1 建议改成

相比 Flat MoE，Hierarchical 没有表现出更强的 path 间 atom 分化。Layer 7 上，Flat raw top-1 + LB 的 atom diversity 为 0.348，而 Hierarchical full_input / conditional_input 分别为 0.076 / 0.064；同时 Hierarchical 的 top atom overlap 更高，说明不同 path 共享更多 atoms。

### 原结论 2 建议改成

四个模型都依赖自己 path 上的主要 atoms。移除 top atoms 后，loss 上升远高于随机移除 atoms。Hierarchical 的 loss 上升更大，说明它对 path 主要 atoms 更敏感；但结合 atom diversity 看，这不能说明它使用了更互异的 atoms。

### 原结论 3 建议改成

Hierarchical 内部出现了 coarse block 结构。按 `path=4c+f` 排列后，不同 coarse block 之间的 atom profile 差异稳定大于同一 coarse 内部差异。该结果说明 Hierarchical 有分层分工迹象，但不能直接等同于恢复真实语义层级。

## 备注

当前这版报告只应引用 `checkpoint-final / 5ep / 16p`。旧的 checkpoint-1000 / checkpoint-2000 图和旧 100-path 结论不要再放进正文。
