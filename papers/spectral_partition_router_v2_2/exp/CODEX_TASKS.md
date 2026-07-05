# Codex Tasks for V2.2 Static Good Dispatch

## Goal

Implement and run the static good-dispatch experiments for V2.2.

Do not implement training preservation, slow updates, hysteresis, or drift experiments in this version.

---

## Task 1: fork code safely

Copy the V2 experiment code into:

```text
papers/spectral_partition_router_v2_2/exp/src/
```

Do not mutate V2 or old V2.1 code.

---

## Task 2: implement corrected router names

Implement:

```text
c_spr_random_axis
c_spr_fixed_basis
c_spr_local
c_spr_expert
c_spr_expert_local
balanced_assignment_control
```

Remove from v2.2:

```text
slow_update_spr
margin_update_spr
hysteresis_spr
```

Alias only for backwards compatibility:

```text
spr_fixed -> c_spr_random_axis
lb_control -> balanced_assignment_control
```

---

## Task 3: true fixed-basis router

Add:

```python
make_fixed_basis(d: int, seed: int, kind: str) -> np.ndarray
```

Supported kinds:

```text
coordinate
orthogonal_random
hadamard_if_available
```

The tree should choose directions deterministically by depth and node id.

---

## Task 4: local-structure data generators

Add generators:

```python
sample_isotropic_null(n, d, label_mode)
sample_isotropic_local_mixture(n, d, k, separation, noise, whiten=True)
sample_anisotropic_distorted_mixture(n, d, k, separation, noise, condition_number)
sample_static_task(features, labels, task_type)
```

Rules:

- labels are returned only for evaluation;
- whitening parameters are fit on calibration data and applied to holdout;
- report pre/post covariance stats.

---

## Task 5: projective expert prototypes

Implement:

```python
svd_projectors(weights) -> np.ndarray  # [E, d, d]
projective_distance_matrix(projectors) -> np.ndarray
projective_group_split(projectors, experts, num_left)
projective_cell_alignment(routes, features, projectors)
```

Do not average raw SVD vectors unless an orientation rule is explicitly supplied.

---

## Task 6: expert alignment ladder

Implement expert weight constructors:

```python
make_aligned_experts(feature_dirs, signal, noise)
make_partially_aligned_experts(feature_dirs, alignment_strength, noise)
make_random_experts(e, d, hidden)
make_clustered_misaligned_experts(e, d, hidden)
```

Report:

```text
nearest-neighbor prototype cosine
max pairwise prototype cosine
effective prototype rank
alignment to true feature directions  # evaluation-only
```

---

## Task 7: feature-derived tie handling

Implement:

```python
lexicographic_keys(X, directions) -> np.ndarray
stable_feature_split(X_node, primary_direction, rho, tie_directions)
```

Output tie stats:

```text
tie_rate
max_atom_mass
exact_split_possible
num_tie_breaks
```

Do not break ties by sample index.

---

## Task 8: C-SPR direction objectives

Implement candidate scoring:

```python
score_local_split(X_node, q, rho)
score_expert_alignment(X_node, q, expert_groups_or_projectors)
score_margin_tail(X_node, q, rho)
```

Combined objective:

```python
score = -within_cell_variance + lambda_align * expert_alignment + eta_margin * margin_score
```

Labels must not appear in any scoring function.

---

## Task 9: experiment runners

Create runners:

```text
run_equal_mass.py
run_isotropy_null.py
run_local_structure.py
run_expert_alignment.py
run_spectral_normalization.py
run_static_utility.py
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

---

## Task 10: metrics

Implement metrics:

```python
usage_metrics
route_feature_nmi
feature_purity
within_cell_variance
between_cell_center_separation
margin_p05
covariance_stats
cell_projector_alignment
prototype_spread_metrics
static_expert_fit_loss
```

---

## Task 11: acceptance checklist

Before updating the paper with numbers, verify:

- [ ] calibration and holdout metrics are separated;
- [ ] labels are never used during router construction;
- [ ] balanced assignment is reported only as a control;
- [ ] projective prototypes remove SVD sign ambiguity;
- [ ] tie stats are reported;
- [ ] covariance stats are reported before and after normalization;
- [ ] every positive experiment has a matched null or failure case;
- [ ] no preservation claims appear in v2.2.

---

## Task 12: paper update after runs

Only after generated results exist:

- replace protocol paragraphs with result paragraphs;
- include generated tables and figures;
- keep the claim hierarchy:
  1. equal mass;
  2. feature coherence;
  3. static utility / expert compatibility.

Forbidden claims:

- spectral isotropy alone gives meaningful routing;
- equal mass implies specialization;
- expert weights always help;
- static dispatch solves training dynamics;
- current synthetic results imply real LLM utility.
