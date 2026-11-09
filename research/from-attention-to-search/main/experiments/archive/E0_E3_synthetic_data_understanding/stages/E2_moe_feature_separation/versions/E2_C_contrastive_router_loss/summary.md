# Result Summary: E2-C Contrastive Router Loss

### Observation

本实验的目的：不固定 feature 到 expert 的编号，只让同一 feature 的 router representation 更近、不同 feature 更远，检验“表示聚类压力”是否足以诱导 clean feature-expert routing。

核心假设：如果 router representation $r_t=\mathrm{normalize}(W_ph_t)$ 中 ABC/DEF/GHI/JKL 被拉成清楚的 feature clusters，那么 router 可能自然把这些 clusters 分给不同 experts。

Full run 使用 5 个 seeds，每个 variant 训练 10000 steps。结果：

| variant | readback | NMI | best-perm acc | fixed-label acc | load entropy | ablation drop |
|---|---:|---:|---:|---:|---:|---:|
| contrastive_no_aux_no_lb | 0.9944 | 0.4382 | 0.5073 | 0.3132 | 0.8807 | 0.5755 |
| contrastive_no_aux_lb | 0.9954 | 0.1363 | 0.3132 | 0.2146 | 1.3855 | 0.4472 |
| contrastive_aux_0_1_no_lb | 0.9960 | 0.5294 | 0.5002 | 0.1401 | 0.7750 | 0.6982 |
| contrastive_aux_1_0_no_lb | 0.9956 | 0.6920 | 0.6189 | 0.1009 | 0.7913 | 0.7091 |
| contrastive_aux_1_0_lb | 0.9954 | 0.4192 | 0.4498 | 0.2498 | 1.3856 | 0.6173 |

所有 variants 的 router representation probe accuracy 都是 1.0，说明 feature label 可以从 $r_t$ 线性读出。

### Interpretation

E2-C 的关键结果是：feature representation 已经可线性读出，但 expert routing 仍没有 clean one-to-one。最强的 `contrastive_aux_1_0_no_lb` 只达到 NMI 0.692、best-permutation accuracy 0.619。

这说明 contrastive representation clustering 不自动等于 expert assignment。换句话说，router representation 中“有 feature 信息”和 router 最终“按 feature 分 expert”之间仍有断裂。

LB 在这里主要改善负载均衡，但没有改善 feature routing；`contrastive_aux_1_0_lb` 的 load entropy 接近 $\log 4$，但 NMI 下降到 0.419。

### Limitation

当前 supervised contrastive loss 在训练日志中很快进入平台期，约为 3.434；这可能表示 batch contrastive 目标存在退化解或压力不足。因此 E2-C 不能证明“所有 contrastive router 都无效”，只能说明当前这版 contrastive representation pressure 不足以恢复 clean expert specialization。

### Key Figures

![routing matrix](figures/routing_matrix_by_variant.png)

![best permutation](figures/best_permutation_accuracy_by_variant.png)

![router representation PCA](figures/router_representation_pca_by_feature_and_expert.png)

![contrastive loss](figures/contrastive_loss_curve.png)

### Claim Update

E2-C 强化了 E2.1 的主线判断：representation separability 不等于 router specialization。即使 feature label 可从 router representation 中读出，top-1 expert boundary 也不会自动变成 feature boundary。

### Decision

下一步不应只继续“让表示更可分”，而要直接研究 cluster-to-expert boundary：为什么 router logits 没有把可分 representation 映射成一对一 expert 分配，以及是否需要显式边界约束、prototype CE 或 assignment-level objective。
