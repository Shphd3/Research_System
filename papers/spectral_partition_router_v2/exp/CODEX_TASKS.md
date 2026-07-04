# Codex Tasks for Spectral Partition Router v2

## General instructions

Implement experiments for `papers/spectral_partition_router_v2/`.

Do not edit `latex/paper.tex` with fabricated results. Only update result tables after experiments have been executed.

Use deterministic seeds and write all raw metrics to CSV.

## Task 1: Implement SPR routers

Create a reusable module, suggested path:

```text
exp/src/spr.py
```

Required classes/functions:

```python
class SPRTree:
    def fit(self, X_cal, num_experts, direction_policy, expert_weights=None, **kwargs): ...
    def predict(self, X): ...
    def leaf_centers(self, X_cal): ...
    def margins(self, X): ...
```

Direction policies:

```text
fixed
local
expert_svd
expert_mpi
```

Required helper functions:

```python
make_fixed_axes(d, seed)
fit_quantile_threshold(values, rho)
compute_load_metrics(assignments, num_experts)
compute_margin_tree(tree, X)
extract_top_svd_direction(W)
power_iteration_direction(W, steps)
make_regular_simplex(E, d)
route_linear_top1(X, router_rows)
```

## Task 2: Implement data generators

Suggested path:

```text
exp/src/data.py
```

Required generators:

```python
gaussian_features(n, d, seed)
spherical_features(n, d, seed)
axis_features(n, d, seed)
symmetric_sparse_mixture(n, d, num_atoms, seed)
latent_feature_mixture(n, d, num_features, noise, seed, whiten=True)
controlled_expert_matrices(E, d, hidden_dim, geometry, seed)
standard_expert_matrices(E, d, hidden_dim, init, seed)
```

All generators should return training/calibration/holdout splits when requested.

## Task 3: Static dispatch experiments

Create:

```text
exp/run_static_dispatch.py
```

Runs Experiments A and B.

Outputs:

```text
results/static_dispatch/metrics.csv
results/static_dispatch/summary.md
results/static_dispatch/figures/loadcv_by_method.pdf
results/static_dispatch/figures/holdout_gap.pdf
```

## Task 4: Expert-weight experiments

Create:

```text
exp/run_expert_guided.py
```

Runs Experiment C.

Outputs:

```text
results/expert_guided/metrics.csv
results/expert_guided/summary.md
results/expert_guided/figures/prototype_spread.pdf
results/expert_guided/figures/alignment_vs_loadcv.pdf
```

Acceptance checks:

- Report expert prototype pairwise cosine distribution.
- Compare expert-SVD top-1 vs SPR-Expert.
- Separate exact SVD and MPI approximation.

## Task 5: Feature partition quality

Create:

```text
exp/run_feature_partition_quality.py
```

Runs Experiment D.

Outputs:

```text
results/feature_partition/metrics.csv
results/feature_partition/summary.md
results/feature_partition/figures/nmi_purity.pdf
results/feature_partition/figures/within_cell_variance.pdf
```

Important: feature labels are evaluation-only. The router construction must not access them.

## Task 6: Training dynamics

Create:

```text
exp/run_training_dynamics.py
```

Runs Experiment E.

Minimum toy task:

```text
X sampled from latent feature mixture
Y = A_F X + noise
experts are linear maps or small MLPs
router variants compared under identical optimizer settings
```

Outputs:

```text
results/training_dynamics/metrics.csv
results/training_dynamics/summary.md
results/training_dynamics/figures/loss_curves.pdf
results/training_dynamics/figures/route_nmi.pdf
results/training_dynamics/figures/flip_rate.pdf
results/training_dynamics/figures/margin_p05.pdf
```

## Task 7: Ablations

Create:

```text
exp/run_ablations.py
```

Ablate:

```text
n_cal
E
d
non-power-of-two E
direction policy
whitening on/off
expert-weight quality
slow update frequency
feature drift strength
```

Outputs:

```text
results/ablations/metrics.csv
results/ablations/summary.md
```

## Task 8: Generate paper-ready tables

Create:

```text
exp/make_paper_tables.py
```

This script reads result CSV files and writes:

```text
latex/tables/static_dispatch.tex
latex/tables/non_spherical.tex
latex/tables/expert_guided.tex
latex/tables/feature_partition.tex
latex/tables/training_dynamics.tex
latex/tables/ablations.tex
```

Do not create result numbers by hand.

## Task 9: Update paper only after results exist

After experiments run, update `latex/paper.tex`:

- replace protocol text in Section 5 with actual result descriptions;
- include generated tables;
- cite figures generated from results;
- keep all claim boundaries.

Forbidden claims:

- SPR discovers semantic experts in general.
- Equal-mass dispatch implies downstream improvement.
- Expert weights alone guarantee uniform dispatch.
- Load-balancing loss and uniform feature dispatch are equivalent.
