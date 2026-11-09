# Result Summary: E2-B Prototype / Center Gating

### Observation

本实验的目的：在均匀 all-trigram synthetic feature 数据上，把普通线性 router 改成 prototype / center gating，检验“专家中心 + 余弦相似度路由”是否更容易形成 one-to-one feature-expert specialization。

核心假设：如果 expert 被表示为可学习中心 $c_e$，router 用 $\cos(h_t,c_e)$ 选 expert，那么这种聚类式归纳偏置可能比普通 linear router 更自然地把 ABC/DEF/GHI/JKL 分到不同 experts。

Full run 使用 5 个 seeds，每个 variant 训练 10000 steps。结果：

| variant | readback | NMI | best-perm acc | fixed-label acc | load entropy | ablation drop |
|---|---:|---:|---:|---:|---:|---:|
| prototype_no_aux_no_lb | 0.9953 | 0.5249 | 0.5289 | 0.1474 | 1.1468 | 0.3804 |
| prototype_no_aux_lb | 0.9951 | 0.4673 | 0.5082 | 0.2044 | 1.3862 | 0.3595 |
| prototype_aux_0_1_no_lb | 0.9961 | 1.0000 | 1.0000 | 1.0000 | 1.1564 | 0.9494 |
| prototype_aux_1_0_no_lb | 0.9967 | 1.0000 | 1.0000 | 1.0000 | 1.2136 | 0.9493 |
| prototype_aux_1_0_lb | 0.9966 | 1.0000 | 1.0000 | 1.0000 | 1.3862 | 0.9657 |

### Interpretation

只把 router 换成 prototype / center gating，并不会自然产生 clean one-feature-one-expert routing。无辅助监督时，readback 很高，但 routing NMI 只有约 0.47-0.52。

加入 feature-to-prototype 监督后，prototype router 可以稳定形成固定对角映射：ABC/DEF/GHI/JKL 分别进入 expert 0/1/2/3。readback 没有下降，dominant expert ablation drop 从约 0.36-0.38 升到约 0.95-0.97。

这说明：center gating 架构本身可承载 clean specialization，但自然 NTP loss 仍不足以把 feature identity 变成 one-to-one expert assignment。

### Limitation

`prototype_aux_*` 使用真实 synthetic feature label，因此它是机制诊断，不是自然语言可用方法。它只能说明“给足 feature 信号时，prototype router 可以干净分开”，不能说明真实数据中可以自动获得这种监督。

### Key Figures

![routing matrix](figures/routing_matrix_by_variant.png)

![best permutation](figures/best_permutation_accuracy_by_variant.png)

![ablation delta](figures/ablation_delta_by_variant.png)

![prototype-feature cosine](figures/feature_centroid_to_prototype_heatmap.png)

### Claim Update

E2-B 支持一个更清楚的判断：当前失败点不是 MoE/expert 不能 specialize，而是自然 NTP objective 对 feature-aligned routing 的压力不够。Prototype router 提供了可监督成 clean specialization 的几何形式，但不自动解决自然路由问题。

### Decision

继续追问 router 为什么不用 feature identity。下一步应比较“固定 feature CE”“prototype CE”“contrastive grouping”三种压力的差别：哪一种真正把 representation cluster 转成 expert boundary。
