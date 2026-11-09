# Execution Plan: E2-B3 Trainable Prototype Dynamics

## Model Fix

旧版本：

$$
y_t=\mathrm{Expert}_{\arg\max_e p_{t,e}}(h_t)
$$

这个形式中，`argmax` 不可导，且 expert output 没有乘以 gate probability，因此 NTP loss 不能训练 router/prototype。

修正版：

$$
y_t=p_{t,e^*}\mathrm{Expert}_{e^*}(h_t),
\quad
e^*=\arg\max_e p_{t,e}
$$

这样被选中的 gate value $p_{t,e^*}$ 会收到 NTP 梯度。

## Config

Runtime config:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/e2_b3_trainable_prototype_dynamics_uniform_all_trigram_v1000.json
```

Runtime output:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/e2_b3_trainable_prototype_dynamics/
```

## Variants

| variant | loss | purpose |
|---|---|---|
| `trainable_center_natural_no_lb` | $L_{\text{NTP}}$ | 测自然 NTP 梯度下 centers 是否自发对齐 feature |
| `trainable_center_sep_1_0_no_lb` | $L_{\text{NTP}} + L_{\text{center-sep}}$ | 测无监督 center separation 是否足够 |
| `trainable_center_supervised_ce_1_0_no_lb` | $L_{\text{NTP}} + L_{\text{router-feature}}$ | supervised upper bound |

Center separation:

$$
L_{\text{center-sep}}
=
\frac{1}{E(E-1)}
\sum_{e \neq e'}
\max(0,\cos(c_e,c_{e'}) - 0)^2
$$

Supervised feature CE:

$$
L_{\text{router-feature}}
=
\mathrm{CE}(\text{router logits at prefix-end position}, \text{feature id})
$$

## Run Setup

```text
seeds = [20260513, 20260514, 20260515]
steps = 10000
batch_size = 128
seq_len = 32
d_model = 64
n_heads = 4
ffn_dim = 128
num_experts = 4
lr = 0.0006
```

## Gradient Audit

Training logs must include:

- `prototype_grad_norm`
- `prototype_grad_abs_max`
- `prototype_delta_from_init_norm`
- `prototype_offdiag_cosine_mean/max/min`
- `center_sep_loss`

Pass condition for the code fix:

```text
natural NTP variant must have non-zero prototype_grad_norm.
```

## Main Metrics

- readback probability
- NMI / ARI
- best-permutation accuracy
- fixed-label accuracy
- expert load entropy
- ablation drop
- prototype off-diagonal cosine
- feature centroid to prototype cosine
