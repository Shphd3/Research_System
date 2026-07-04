# Parameter Sweeps

## Equal mass

```text
d in {32, 64, 128}
E in {4, 8, 12}
n_cal in {2048, 8192, 32768}
n_holdout = 32768
seeds = 5
```

## Assumption ladder

```text
separation in {1.0, 1.5, 2.0, 3.0}
noise in {0.4, 0.7, 1.0}
expert_alignment in {none, noisy, aligned}
```

## Margin update

```text
flip_budget beta in {0.01, 0.03, 0.05}
hysteresis_width in {0.0, 0.01, 0.03}
drift_strength in {0.0, 0.05, 0.15, 0.30}
```
