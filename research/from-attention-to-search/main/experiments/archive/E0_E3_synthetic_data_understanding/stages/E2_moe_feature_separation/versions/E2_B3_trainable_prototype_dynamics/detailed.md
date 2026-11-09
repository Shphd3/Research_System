# Detailed Notes: E2-B3 Trainable Prototype Dynamics

## Code Correction

旧 prototype top-1 forward:

$$
e^*=\arg\max_e p_{t,e},
\quad
y_t=\mathrm{Expert}_{e^*}(h_t)
$$

问题：$e^*$ 来自不可导 `argmax`，且 $y_t$ 不含 $p_{t,e^*}$，所以自然 $L_{\text{NTP}}$ 不会训练 router/prototype。

修正后：

$$
y_t=p_{t,e^*}\mathrm{Expert}_{e^*}(h_t)
$$

因此 $L_{\text{NTP}}$ 可以通过 $p_{t,e^*}$ 更新 prototype centers。

## Runtime Files

Config:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/e2_b3_trainable_prototype_dynamics_uniform_all_trigram_v1000.json
```

Outputs:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/e2_b3_trainable_prototype_dynamics/
```

Figures:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/e2_b3_trainable_prototype_dynamics/
```

## Aggregated Tables

Corrected summary:

```text
outputs/e2_b3_trainable_prototype_dynamics/trainable_center_dynamics_summary_corrected.csv
```

Training dynamics:

```text
outputs/e2_b3_trainable_prototype_dynamics/prototype_training_dynamics_table.csv
```

## Figure Interpretation

- `prototype_grad_norm_over_steps.png`: 证明修正后 natural NTP 也能给 prototype centers 非零梯度。
- `prototype_delta_from_init_over_steps.png`: 证明 centers 在训练中确实移动。
- `routing_matrix_by_variant.png`: 显示 natural / center-sep 都没有 clean one-feature-one-expert，supervised CE clean。
- `prototype_cosine_heatmap.png`: 显示 center separation 和 supervised CE 都让 centers 分开。
- `feature_centroid_to_prototype_heatmap.png`: 显示只有 supervised CE 把每个 feature centroid 对齐到指定 prototype。

## Important Boundary

旧 E2-B / E2-B2 仍可作为结构和监督上界参考，但不能再作为“自然 NTP 训练 prototype centers”的强证据。E2-B3 是修正后的可信版本。
