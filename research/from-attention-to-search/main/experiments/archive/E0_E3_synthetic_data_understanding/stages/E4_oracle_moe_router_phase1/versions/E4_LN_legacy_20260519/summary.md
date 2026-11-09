# Result Summary: E4 Oracle-MoE Router Phase 1

### Observation

本阶段完成了 1-layer Transformer + Oracle-MoE 的 C0-C4 full run，并完成 D0-D7 router behavior diagnostic 与 C-series boundary direction audit。注意：本轮 router 的原始输入是 `attention_output`，但实际 logits 前会经过 `router_ln(z_t)`；center routers 还会再做向量归一化。因此本轮 boundary 结果应标注为 `LN(attention_output)` router-space 结果，不是 raw attention-output routing。两个 ACP 任务均使用 4 卡保障资源并成功结束：

- training job: `pt-l65uzwbz`
- diagnostic job: `pt-vhg9jerf`

训练结果显示，五种 router 都能在 planted feature prefix 上保持很高 readback，但 feature-expert 对齐不稳定：

| variant | NTP loss | readback | feature-expert NMI | router selects best expert |
|---|---:|---:|---:|---:|
| C0 standard linear | 6.643 | 0.9999 | 0.462 | 0.999 |
| C1 fixed parameter center | 6.641 | 0.9998 | 0.773 | 0.295 |
| C2 trainable center + repulsion | 6.642 | 1.0000 | 0.663 | 1.000 |
| C3 inhibition margin | 6.660 | 1.0000 | 0.685 | 0.995 |
| C4 center + inhibition | 6.658 | 0.9999 | 0.364 | 0.996 |

补充 C5/C6 clean inhibition 后，inhibition 辅助项只更新 expert 参数，不更新 shared path / router / LN / LM head。本地梯度 audit 显示 `shared_grad_norm=0` 且 `expert_grad_norm>0`。LB 主实验结果如下：

| variant | NTP loss | readback | feature-expert NMI | router selects best expert | inhibition gap | violation |
|---|---:|---:|---:|---:|---:|---:|
| C5 clean linear inhibition | 6.651 | 0.9999 | 0.346 | 1.000 | 3.414 | 0.000 |
| C6 clean center inhibition | 6.652 | 0.9999 | 0.697 | 1.000 | 2.648 | 0.000 |

no-LB 消融中 C5/C6 仍能 readback，但 expert load entropy 接近 0、dead experts 平均为 3，说明 clean inhibition 不能替代 LB 来维持可用 expert allocation。

Boundary audit 显示，除 C1 外，大多数 router boundary 的能量主要落在 top shared directions，而不是 middle/tail feature-specific directions：

| variant | feature-boundary abs cosine | top shared energy | middle energy | tail energy |
|---|---:|---:|---:|---:|
| C0 | 0.312 | 0.786 | 0.169 | 0.046 |
| C1 | 0.099 | 0.289 | 0.454 | 0.257 |
| C2 | 0.334 | 0.798 | 0.167 | 0.036 |
| C3 | 0.355 | 0.885 | 0.080 | 0.034 |
| C4 | 0.278 | 0.923 | 0.072 | 0.005 |

### Interpretation

当前结果不支持直接进入 Reverse Index。理由是：readback 成功和 router-selected expert utility 成功，并不等价于 clean one-feature-one-expert specialization。

更具体地说：

- C1 的 NMI 较高，但 router 选中 best forced expert 的比例只有 0.295，说明“看起来分得开”不代表 expert 功能分化正确。
- C2/C3 的 utility 很强，但 boundary 主要依赖 top shared directions；这更像 task-utility compatible routing，不足以证明按 feature direction 路由。
- C5/C6 说明 clean inhibition 可以增强 selected expert 相对 other experts 的功能优势，但它仍没有证明 relation-level feature boundary。
- 在 `unique_uniform` 数据中，feature、target token、prefix-end token 和 attention-source token 基本一一对应，因此 MI 指标无法区分 router 到底用的是人工 feature，还是 token/target shortcut。

### Limitation

本阶段仍然只使用 `unique_uniform`。它能检查 C-series router design、utility alignment 和 boundary geometry，但不能排除 token shortcut。另一个实现边界是 router 使用 `LN(attention_output)` 计算 logits；后续需要补一个 raw-attention router 对照。后续必须用 shared-target / shared-prefix-end / crossed-factorial controls 才能回答 router 是否真正按 relation-level feature 切分。

### Key Figures

![training metrics](../../figures/fig_e4_training_metrics.png)

![router factor MI](../../figures/fig_e4_router_factor_mi.png)

![boundary feature alignment](../../figures/fig_c_variant_feature_alignment.png)

![boundary band energy](../../figures/fig_c_variant_boundary_band_energy.png)

![boundary alignment vs utility](../../figures/fig_c_boundary_alignment_vs_utility.png)

![clean inhibition main](../../figures/c5_c6_main_alignment_utility.png)

![clean inhibition no LB](../../figures/c5_c6_lb_vs_nolb_ablation.png)

### Claim Update

可以说：在 Oracle-MoE Phase 1 中，C0/C2/C3/C4 能形成对当前 NTP readback 有用的 expert selection；但是这些选择没有被证明是 clean feature-aligned functional specialization。

补充 C5/C6 后还可以说：clean inhibition 的 expert-only 梯度链路成立，并且能增强 functional exclusivity；但这仍不是 relation-level one-feature-one-expert 的证据。

不能说：C-series Oracle-MoE 已经形成了可靠的一 feature 一 expert 分工，也不能据此进入 Reverse Index claim。

### Decision

不进入 Reverse Index。下一步应做 shortcut-controlled Oracle-MoE：共享 prefix-end token、共享 target token、crossed-factorial feature relation。只有在这些控制下仍同时满足 feature assignment、boundary alignment、utility diagonality 和 readback，才推进 Reverse Index。
