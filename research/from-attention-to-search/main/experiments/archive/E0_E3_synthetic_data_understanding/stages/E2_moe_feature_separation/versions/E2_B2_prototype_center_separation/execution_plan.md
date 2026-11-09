# Execution Plan: E2-B2 Prototype Center Separation

## 1. Run Goal

在 E2-B prototype router 基础上加入 center separation loss，不使用 feature label supervision，跑 3 seeds，判断无监督 center geometry pressure 是否能让 routing 更接近 one-feature-one-expert。

## 2. Router And Loss

Prototype routing:

$$
s_{t,e} = \tau \cdot \cos(z_t,c_e)
$$

Center separation:

$$
L_{\text{center-sep}}
=
\frac{1}{E(E-1)}
\sum_{e\neq e'}
\max(0, \cos(c_e,c_{e'}) - m)^2
$$

Total loss:

$$
L = L_{\text{NTP}} + \lambda L_{\text{center-sep}} + \alpha L_{\text{LB}}
$$

## 3. Variants

| variant | center sep coef | LB | seeds |
|---|---:|---:|---|
| `prototype_center_sep_0_1_no_lb` | 0.1 | 0.0 | 20260513-20260515 |
| `prototype_center_sep_1_0_no_lb` | 1.0 | 0.0 | 20260513-20260515 |
| `prototype_center_sep_1_0_lb` | 1.0 | 0.01 | 20260513-20260515 |

## 4. Run Command

```bash
python scripts/train_moe_prototype_center_gating.py \
  --run-config configs/e2_b2_prototype_center_separation_uniform_all_trigram_v1000.json
```

Plot:

```bash
python scripts/plot_router_gating_variants.py \
  --mode prototype \
  --out-dir outputs/e2_b2_prototype_center_separation \
  --fig-dir figures/e2_b2_prototype_center_separation
```

## 5. Metrics

- readback probability;
- NMI / ARI;
- best-permutation accuracy;
- fixed-label accuracy;
- expert load entropy;
- dominant expert ablation drop;
- prototype off-diagonal cosine;
- final center separation loss.

## 6. Acceptance Logic

Strong support:

```text
NMI >= 0.95 and best-perm acc >= 0.95 without feature label supervision.
```

Weak support:

```text
prototype cosine decreases and NMI improves over no-aux E2-B baseline.
```

No support:

```text
prototype centers separate, but NMI remains around ordinary no-aux prototype level.
```
