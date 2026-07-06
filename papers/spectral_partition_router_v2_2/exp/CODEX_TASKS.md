# Codex Tasks for V2.2 Static Feature-Family Dispatch

## Current Status

The current stage has been executed for E1--E5.  Do not add training
preservation, learned-router dynamics, expert alignment, or static utility runs
to the main result path unless the research scope is explicitly reopened.

## Implemented Runner

```text
papers/spectral_partition_router_v2_2/exp/run_static_dispatch_suite.py
```

This runner produces:

```text
exp/results/*_raw.csv
exp/results/*_aggregate.csv
exp/results/summary.md
latex/tables/*.tex
latex/figures/*.png
```

## Implemented Source Package

```text
papers/spectral_partition_router_v2_2/exp/src/static_bfsr_suite.py
```

It contains:

```text
isotropic null generator
isotropic feature-family mixture generator
anisotropic distortion generator
frequency-imbalance generator
spectral normalizer
k-means feature recovery
BFSR-Cluster
OracleFeature non-admissible upper bound
Quantile-SPR mass-only baseline
Random linear top-1 baseline
mass, family-consistency, split-rate, information-fraction metrics
LaTeX table and figure writers
```

## Executed Experiments

```text
E1 clean mass and specialization sanity
E2 isotropy-alone null
E3 feature recoverability sweep
E4 spectral normalization ablation
E5 frequency-uniformity ablation
```

Full-run configuration:

```text
seeds: 0,1,2,3,4
d: 16
K: 32
E: 4
calibration examples: 8000
holdout examples: 16000
```

## Current Acceptance Checks

The current result is acceptable for the narrow static claim only if:

```text
E1: BFSR-Cluster approaches OracleFeature on LoadCV and family consistency.
E2: admissible label-free methods have near-zero expert information fraction.
E3: family consistency tracks cluster recovery as separation increases.
E4: whitening repairs structured anisotropic distortion but does not create null-data information.
E5: equal-number assignment fails under frequency imbalance, and mass-aware assignment repairs LoadCV.
```

These checks pass in the current full run.  See:

```text
papers/spectral_partition_router_v2_2/exp/results/summary.md
```

## Parked Tasks

The following are intentionally parked:

```text
expert alignment ladder
static utility audit
training-time preservation
learned-router dynamics
automatic K selection
real hidden-state feature audit
```
