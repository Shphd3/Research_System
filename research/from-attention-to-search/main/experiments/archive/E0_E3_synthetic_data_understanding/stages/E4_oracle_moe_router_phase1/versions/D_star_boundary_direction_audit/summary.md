# D* Router Boundary Direction Audit - Summary

## 1. 目的

D* 要回答的是：router 不是只看结果把 token 分到 expert，而是它的“分界线”到底沿着什么方向切开 `attention_output` 表征空间。

这一步是 E4 的机制诊断：如果 feature 表征已经存在，但 router 不按 feature 分 expert，我们需要知道 router 是沿 feature 方向切，还是沿 common / 高频方向、utility 方向或其它方向切。

## 2. 假设

如果 router 真正在做 feature-aligned routing，那么应该同时看到：

1. router boundary 和 feature centroid difference 有较高对齐；
2. router boundary 的谱能量不只集中在 top shared / common directions；
3. router 选中的 expert 也是 forced-routing 下对该 feature 最有用的 expert。

## 3. 结论

D* 的结论是：普通 router 的边界多数不是干净沿 feature direction 切，而更偏向 top shared / common directions；C7d/C7e 能把边界推向更 feature-related、utility-aligned 的区域，但仍不是纯 feature boundary。

所以 E4 可以说：

```text
C7 构造出了更强的 routing reference；
但 router boundary 仍是 feature direction、common geometry、expert utility 三者混合后的结果。
```

不能说：

```text
router 已经自然学到了干净的语义边界。
```

## 4. 证据

### 证据 1：普通 router 的 boundary 更偏 top shared / common directions

Uniform 中，C0/C3/C4 的 boundary energy 主要集中在 top shared band：

| variant | top | middle | tail |
|---|---:|---:|---:|
| C0 | 0.787 | 0.163 | 0.049 |
| C3 | 0.853 | 0.098 | 0.049 |
| C4 | 0.916 | 0.077 | 0.007 |

Zipf 中也类似：

| variant | top | middle | tail |
|---|---:|---:|---:|
| C0 | 0.784 | 0.169 | 0.047 |
| C3 | 0.832 | 0.123 | 0.045 |
| C4 | 0.930 | 0.053 | 0.017 |

![uniform boundary band energy](figures/uniform_boundary_band_energy.png)

### 证据 2：C7d/C7e 改善 feature alignment 和 utility，但不是纯 feature boundary

Uniform 中，C7e 的 feature-boundary alignment 为 0.413，router-selects-best 为 1.000。Zipf 中，C7e 的 feature-boundary alignment 为 0.343，router-selects-best 为 0.993。

这说明 C7e 的 expert 分配既更接近 feature-related region，也更接近 forced-routing 下的有效 expert；但 alignment 远不是 1，因此它不是干净的 feature 几何切分。

![uniform boundary feature alignment](figures/uniform_boundary_feature_alignment.png)

![zipf boundary feature alignment](figures/zipf_boundary_feature_alignment.png)

### 证据 3：NMI 不能单独证明 functional specialization

C1 是关键反例：它可以出现相对较高的 feature-expert 对齐现象，但 router-selects-best 很低。Uniform 中 C1 的 selected-best 约为 0.621，Zipf 中约为 0.304。

这说明“feature 和 expert 看起来对应”不等于“这个 expert 真的最会处理该 feature”。E4 后续报告必须同时看 feature assignment、boundary alignment、expert utility 和 readback。

![uniform boundary alignment vs utility](figures/uniform_boundary_alignment_vs_utility.png)

![zipf boundary alignment vs utility](figures/zipf_boundary_alignment_vs_utility.png)

## 5. Claim Update

可以说：

```text
D* 支持 E4 的机制解释：router failure 不是因为 feature representation 完全不存在，而是因为自然 router boundary 没有足够压力必须沿 feature direction 切。
```

还不能说：

```text
当前 C7 已经获得真实语言意义上的语义 expert，或 router boundary 等同于 semantic boundary。
```

## 6. Next Step

下一步应该继续追问：

```text
不用 feature-prefix oracle，如何自动找到值得聚类的 rule-context 表征？
```

如果后续要推进 Reverse Index，需要先保留 D* 的约束：不能只看 NMI，必须同时检查 routing boundary、forced expert utility 和 readback。
