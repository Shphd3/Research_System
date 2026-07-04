# Table Templates for Spectral Partition Router v2

These tables are templates only. Fill them after running the experiments.

## Table 1: Static equal-mass dispatch

| Data | Method | Cal LoadCV ↓ | Holdout LoadCV ↓ | Max Abs Error ↓ | Margin p05 ↑ |
|---|---|---:|---:|---:|---:|
| Gaussian | Vanilla linear |  |  |  |  |
| Gaussian | Simplex prototype |  |  |  |  |
| Gaussian | SPR-Fixed |  |  |  |  |
| Gaussian | SPR-Local |  |  |  |  |
| Gaussian | SPR-Expert |  |  |  |  |
| Gaussian | Balanced assignment control |  |  |  |  |

## Table 2: Spectrally flat but non-spherical features

| Data | Cov Condition ↓ | Effective Rank ↑ | Method | Holdout LoadCV ↓ | Max Abs Error ↓ |
|---|---:|---:|---|---:|---:|
| Axis |  |  | Vanilla linear |  |  |
| Axis |  |  | Simplex prototype |  |  |
| Axis |  |  | SPR-Fixed |  |  |
| Axis |  |  | SPR-Local |  |  |

## Table 3: Expert-weight-guided partitioning

| Expert Init | Prototype Source | Router | Proto Spread ↑ | Alignment ↑ | Holdout LoadCV ↓ | Margin p05 ↑ |
|---|---|---|---:|---:|---:|---:|
| Xavier | SVD | SVD top-1 |  |  |  |  |
| Xavier | SVD | SPR-Expert |  |  |  |  |
| Controlled symmetric | SVD | SVD top-1 |  |  |  |  |
| Controlled symmetric | SVD | SPR-Expert |  |  |  |  |
| Controlled clustered | SVD | SVD top-1 |  |  |  |  |
| Controlled clustered | SVD | SPR-Expert |  |  |  |  |

## Table 4: Feature partition quality

| Method | LoadCV ↓ | Route-Feature NMI ↑ | Feature Purity ↑ | Within-Cell Var ↓ | Margin p05 ↑ |
|---|---:|---:|---:|---:|---:|
| Vanilla linear |  |  |  |  |  |
| Simplex prototype |  |  |  |  |  |
| SPR-Fixed |  |  |  |  |  |
| SPR-Local |  |  |  |  |  |
| SPR-Expert |  |  |  |  |  |

## Table 5: Controlled MoE training dynamics

| Router | Val Loss ↓ | LoadCV ↓ | Route-Feature NMI ↑ | Flip Rate ↓ | Margin p05 ↑ | Specialization ↑ |
|---|---:|---:|---:|---:|---:|---:|
| Vanilla linear |  |  |  |  |  |  |
| Linear + load-balance loss |  |  |  |  |  |  |
| Simplex init |  |  |  |  |  |  |
| Frozen-SPR |  |  |  |  |  |  |
| SPR-init-linear |  |  |  |  |  |  |
| SlowUpdate-SPR |  |  |  |  |  |  |
| SPR-Expert |  |  |  |  |  |  |

## Table 6: Ablations

| Ablation | Setting | LoadCV ↓ | NMI ↑ | Margin p05 ↑ | Val Loss ↓ |
|---|---|---:|---:|---:|---:|
| Calibration size |  |  |  |  |  |
| Expert count |  |  |  |  |  |
| Dimension |  |  |  |  |  |
| Direction policy |  |  |  |  |  |
| Whitening |  |  |  |  |  |
| Expert weight quality |  |  |  |  |  |
| Slow update frequency |  |  |  |  |  |
