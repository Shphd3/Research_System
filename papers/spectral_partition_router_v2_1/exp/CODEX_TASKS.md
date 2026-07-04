# Codex Tasks for V2.1

## Goal

Implement and test Geometry-Aware Spectral Partition Routing (GA-SPR), moving beyond equal-mass dispatch toward geometry-aware and margin-preserved dispatch.

## Task 1: Fork V2 implementation safely

Copy V2 shared code into:

```text
papers/spectral_partition_router_v2_1/exp/src/
```

Do not modify V2 scripts in-place.

## Task 2: Implement corrected router names

Implement the following methods:

```text
spr_random_axis
spr_fixed_basis
ga_spr_local
ga_spr_expert
ga_spr_expert_local
ga_spr_margin_update
balanced_assignment_control
```

Retire or alias ambiguous names:

```text
spr_fixed -> spr_random_axis unless true basis exists
lb_control -> balanced_assignment_control unless auxiliary loss is implemented
slow_update_spr -> naive_slow_update_spr
```

## Task 3: Implement fixed basis directions

Add:

```python
make_fixed_basis(d: int, seed: int, kind: str) -> np.ndarray
```

Supported kinds:

```text
orthogonal_random
hadamard_if_available
coordinate
```

The tree should choose fixed directions deterministically by depth/node id.

## Task 4: Implement sign-invariant expert prototypes

Add:

```python
svd_projectors(weights) -> np.ndarray  # [E, d, d]
projective_distance_matrix(projectors) -> np.ndarray
projective_group_split(projectors, experts, num_left) -> left, right
projective_candidate_direction(projectors, left, right, X_node=None) -> q
```

Do not average raw SVD signs without an orientation rule.

If oriented MPI/router rows are available, store and report orientation source.

## Task 5: Implement feature-derived tie handling

Add lexicographic split utilities:

```python
lexicographic_keys(X, directions) -> np.ndarray
stable_feature_split(X_node, primary_direction, rho, tie_directions) -> mask, threshold, tie_stats
```

Rules:

- Do not break ties by sample index.
- If identical feature atoms prevent exact split, report `exact_split_possible=False`.
- Record `tie_rate` and `max_atom_mass`.

## Task 6: Implement margin-aware update

Add a training router wrapper:

```python
class MarginAwareSPRUpdater:
    fit_initial(X_cal, ...)
    propose_update(X_window, ...)
    accept_update_if(route_flip_rate <= beta and margin_p05 >= gamma and loadcv <= tol)
    predict(X)
```

Also implement a naive slow-update baseline for comparison.

## Task 7: Implement true learnable-router baseline

Add controlled training baseline:

```text
trainable linear top-1 router
trainable linear top-1 + load-balancing auxiliary loss
GA-SPR-init-linear + route-preservation regularizer
```

If straight-through top-1 is difficult, document the approximation used.

## Task 8: Run experiments

Create runners:

```text
run_equal_mass.py
run_assumption_ladder.py
run_expert_guided.py
run_margin_update.py
run_controlled_training.py
run_failures.py
```

Each runner writes:

```text
exp/results/<id>/metrics.csv
exp/results/<id>/summary.md
latex/tables/<id>.tex
latex/figures/<id>_*.pdf
latex/figures/<id>_*.png
```

## Task 9: Acceptance checklist

Before updating the paper with results, verify:

- calibration and holdout metrics are separated;
- labels are never used during router construction;
- expert weights are used only as model-internal geometry;
- balanced assignment is only a control;
- sign ambiguity is handled;
- tie statistics are reported;
- route flip and margin are reported for training;
- failure cases are explicitly tied to violated assumptions.

## Task 10: Update paper after experiments

Only after successful runs:

- replace protocol paragraphs with result paragraphs;
- include generated tables and figures;
- keep the claim hierarchy:
  1. equal mass;
  2. feature coherence;
  3. training preservation.

Forbidden claims:

- isotropy alone gives meaningful feature dispatch;
- equal mass implies feature specialization;
- expert weights always help;
- margin-aware update solves arbitrary drift;
- current synthetic results imply real language-model utility.
