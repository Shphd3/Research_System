# High-Dimensional Random Gate Load Imbalance Experiment

## Minimal question

For uniform high-dimensional tokens and a pure top-1 random gate, is observed load imbalance mainly finite-token sampling noise or true decision-cell imbalance from one finite random gate initialization?

## Model

$$\hat p_e-\frac{1}{m}=(p_e-\frac{1}{m})+(\hat p_e-p_e)$$

- `p_e`: true decision-cell probability estimated by large Monte Carlo.
- `hat p_e`: measured finite-token load.
- normalized error: `m * max_e |error_e|`.

## Main findings

1. Increasing token count reduces sampling error but observed load approaches a fixed floor for a fixed gate initialization.
2. Increasing dimension reduces the true cell imbalance, especially for normalized gate directions.
3. Standard Gaussian-scaled gate rows retain extra imbalance from row-norm variation; this is much larger when m is high and d is moderate.
4. Therefore uniform tokens alone do not guarantee balanced load for one finite random gate. But in high dimension with normalized directions, the floor can become small.

## Key summary: true cell imbalance, m=8

|   d |   gaussian_scaled |   normalized |
|----:|------------------:|-------------:|
|   2 |            1.609  |       0.8656 |
|   8 |            0.6421 |       0.3889 |
|  32 |            0.3703 |       0.2044 |
| 128 |            0.2089 |       0.089  |
| 512 |            0.079  |       0.0566 |

## Key summary: true cell imbalance, m=32

|   d |   gaussian_scaled |   normalized |
|----:|------------------:|-------------:|
|   2 |            6.8622 |       1.8017 |
|   8 |            2.4481 |       0.5924 |
|  32 |            1.1551 |       0.2539 |
| 128 |            0.5432 |       0.126  |
| 512 |            0.3035 |       0.077  |

## Refined selected large-MC checks

|                              |   mean_true |   std_true |   mean_row_norm_cv |   mean_max_corr |
|:-----------------------------|------------:|-----------:|-------------------:|----------------:|
| ('gaussian_scaled', 32, 32)  |      1.2154 |     0.2313 |             0.1286 |          0.5224 |
| ('gaussian_scaled', 512, 32) |      0.2557 |     0.0398 |             0.0315 |          0.1545 |
| ('normalized', 2, 8)         |      1.0675 |     0.1985 |             0      |          0.9992 |
| ('normalized', 512, 8)       |      0.0528 |     0.0184 |             0      |          0.1007 |
| ('normalized', 512, 32)      |      0.0638 |     0.0071 |             0      |          0.1429 |
