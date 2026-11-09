# Result Summary: E2-H H-MoE Hierarchical Routing Side Branch

## Observation

本实验目的：验证 two-level synthetic corpus 中，H-MoE 是否比 Flat-MoE 更稳定地把高层 event family 和低层 phrase/role 分开，并保持 readback 能力。

数据审计通过。L1 phrase 几乎无背景碰撞；L2 event 背景碰撞很低，例如最高频 `F1_E1_A1_O1` planted count 为 `35174`，actual count 为 `35181`，背景碰撞为 `7`。

三类模型都能稳定 read back：

| model | L1 prob | L2 prob | L1 acc | L2 acc |
|---|---:|---:|---:|---:|
| Dense | 0.9989 | 0.9919 | 1.00 | 1.00 |
| Flat-MoE | 0.9994 | 0.9912 | 1.00 | 1.00 |
| H-MoE | 0.9995 | 0.9906 | 1.00 | 1.00 |

Routing 没有支持“当前 H-MoE 自然更稳定地形成层级分工”：

| metric | mean NMI |
|---|---:|
| Flat expert vs L2 family | 0.457 |
| H-MoE root vs L2 family | 0.381 |
| H-MoE path vs L2 family | 0.464 |
| Flat expert vs L1 phrase | 0.596 |
| H-MoE path vs L1 phrase | 0.564 |

H-MoE root 在 event 内部也不稳定：平均 root majority fraction 为 `0.566`，all-same-root 比例约 `0.007`。

## Interpretation

这说明 synthetic hierarchy 是干净且可学的；dense、Flat-MoE、H-MoE 都能读回 L1/L2 结构。但当前训练目标下，H-MoE 没有自然把 root router 稳定变成 L2 family router，也没有让 leaf/path 明显优于 Flat expert 的 L1/L2 对齐。

这与 E2 主线现象一致：`可读回结构` 不等于 `router 自然按我们定义的结构切分 expert`。

## Limitation

这不是 H-MoE 的最终否定。当前实验只测试了 1-layer tiny Transformer、top-1 routing、固定 load-balance 系数和一个 exact-triple 层级语料。更强的层级压力、不同容量约束或更深层模型可能改变结果。

## Key Figures

![Data frequency rank curves](figures/frequency_rank_curves.png)

![Dense Flat HMoE readback](figures/dense_flat_hmoe_l1_l2_readback.png)

![Routing alignment NMI](figures/routing_alignment_nmi.png)

![Flat expert by L2 family](figures/flat_expert_by_l2_family.png)

![HMoE root by L2 family](figures/hmoe_root_by_l2_family.png)

![HMoE path by L1 phrase](figures/hmoe_path_by_l1_phrase.png)

![HMoE event root consistency](figures/hmoe_event_root_consistency.png)

## Claim Update

可以 claim：

```text
在当前 controlled hierarchical synthetic NTP 设置中，H-MoE 保持了与 dense/Flat-MoE 相当的 L1/L2 readback，但没有比 Flat-MoE 更稳定地产生与人工层级标签一致的 routing。
```

不能 claim：

```text
H-MoE 一定不能形成层级专家；也不能 claim 真实语言中的 H-MoE 没有层级语义分工。
```

## Decision

本支线暂时作为架构负结果/边界结果关闭。下一步若继续追 H-MoE，不应只增加训练步数，而应增加真正的 specialization pressure：例如让 L2 target 依赖共享 phrase 的不同组合，使单一 phrase shortcut 不足以完成 readback。

