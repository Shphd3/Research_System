# Default Configurations

These are starting points only.

## Static experiments

```text
seeds = 5
d in {32, 64, 128}
E in {4, 8, 12}
n_cal in {2048, 8192, 32768}
n_holdout = 32768
```

## Training experiments

```text
seeds = 5
d = 32 or 64
E = 8
n_train = 8192
n_val = 4096
epochs = 80
```

## Margin-aware update

```text
beta_flip_budget in {0.01, 0.03, 0.05}
gamma_margin_min in {0.01, 0.02, 0.05}
hysteresis_width in {0.0, 0.01, 0.03}
```
