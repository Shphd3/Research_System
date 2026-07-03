# Implementation Tasks

## Goal

Implement and run the synthetic experiments for the paper `Uniform Feature Routing from Spectral Expert Prototypes`.

The first pass covers E1--E5 only. Training-dynamics experiments are optional after the synthetic suite is complete.

## Main runner

Use this file:

```text
papers/uniform_feature_moe_initialization/exp/run_synthetic.py
```

Smoke test:

```bash
cd papers/uniform_feature_moe_initialization/exp
python run_synthetic.py --outdir results --quick
```

Full run:

```bash
python run_synthetic.py --outdir results --full
```

## Required outputs

```text
results/results.csv
results/summary.md
results/tables/e1_uniform_sphere.md
results/tables/e2_2d_geometry_floor.md
results/tables/e3_spectral_prototypes.md
results/tables/e4_balanced_assignment.md
results/tables/e5_anisotropy_whitening.md
```

Optional:

```text
results/figures/*.png
```

## Required CSV columns

```text
experiment, setting, method, seed, n, d, e, alpha, prototype_mode, preprocess,
load_cv, load_max_min, load_kl, load_max_abs_error,
condition_number, spectral_entropy, effective_rank,
prototype_max_cos, prototype_mean_abs_cos,
alignment_lambda_mean, alignment_lambda_min,
score_mean, score_drop_vs_top1,
init_error, sampling_error, total_error, notes
```

Use `nan` for non-applicable numeric fields.

## Experiment checklist

1. E1: uniform sphere features; compare symmetric, random, clustered, and balanced prototype routing.
2. E2: two-dimensional circle; record true Voronoi mass, measured load, initialization error, sampling error, and total error.
3. E3: synthetic expert matrices; compare exact SVD prototypes, one-step MPI, five-step MPI, and random router rows.
4. E4: compare unconstrained top-1 with balanced assignment and report the score cost of balancing.
5. E5: sweep anisotropy `alpha`; compare raw, centered, normalized, whitened, and whitened-balanced routing.

## Acceptance checklist

1. `results.csv` contains rows for E1--E5.
2. E2 shows sampling error decreases with token count while initialization error remains.
3. E3 shows MPI improves alignment over random router rows.
4. E4 shows balanced assignment gives near-zero load CV.
5. E5 reports condition number and shows whitening reduces imbalance under anisotropy.
6. Summary tables are compact enough to paste into `paper.tex`.
