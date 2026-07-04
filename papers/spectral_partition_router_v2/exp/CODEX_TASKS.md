# Codex Status for Spectral Partition Router v2

## Current state

The V2 experiment suite has been implemented and executed as a full run for
E1--E6.  The paper now uses generated metrics, tables, and figures rather than
pre-result design notes.

Canonical mapping:

```text
exp/EXPERIMENT_REGISTRY.md
exp/src/registry.py
```

Implemented runners:

```text
exp/run_static_dispatch.py          # E1, E2
exp/run_expert_guided.py            # E3
exp/run_feature_partition_quality.py # E4
exp/run_training_dynamics.py        # E5
exp/run_ablations.py                # E6
exp/make_paper_tables.py            # paper tables
```

Shared implementation:

```text
exp/src/synthetic_suite.py
```

## Full-run outputs

Every metrics file contains `run_mode=full`.

```text
exp/results/e1_static_dispatch/metrics.csv
exp/results/e2_non_spherical/metrics.csv
exp/results/e3_expert_guided/metrics.csv
exp/results/e4_feature_partition/metrics.csv
exp/results/e5_training_dynamics/metrics.csv
exp/results/e6_ablations/metrics.csv
```

Paper artifacts:

```text
latex/figures/
latex/tables/
```

## Current claim boundary

Supported:

- Recursive quantile splitting gives calibration-balanced expert cells.
- Held-out usage balance improves over random linear routing in the tested
  Gaussian, spherical, and most non-spherical synthetic settings.
- Expert spectral prototypes are useful as geometry priors when they align with
  the latent feature geometry.
- Count balance alone does not imply feature partition quality.

Not supported:

- SPR discovers semantic experts in general.
- Equal-mass dispatch implies downstream utility.
- Expert weights alone guarantee uniform dispatch.
- Slow recalibration is automatically stable under representation drift.

## Next audit tasks

1. Check whether the theory section should add a finite-sample tree-level bound
   beyond the scalar DKW discussion.
2. Decide whether the paired-direction E2 boundary case should be moved to the
   main text, appendix, or limitation paragraph.
3. Audit whether E5 should be framed as hard-routing controlled training rather
   than general MoE training.
