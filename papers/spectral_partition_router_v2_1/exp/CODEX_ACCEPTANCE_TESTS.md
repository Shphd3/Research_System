# Codex Acceptance Tests

## Unit tests

- `test_recursive_leaf_mass_on_continuous_data`
- `test_no_holdout_recalibration`
- `test_non_power_of_two_expert_split`
- `test_projective_svd_sign_invariance`
- `test_lexicographic_tie_handling`
- `test_atom_impossibility_reported`
- `test_margin_preservation_bound`

## Smoke runs

```bash
python exp/run_equal_mass.py --quick
python exp/run_assumption_ladder.py --quick
python exp/run_expert_guided.py --quick
python exp/run_margin_update.py --quick
python exp/run_controlled_training.py --quick
python exp/run_failures.py --quick
```

## Required generated outputs

Each quick run must generate:

```text
metrics.csv
summary.md
at least one figure
```

No quick run should modify `latex/paper.tex`.
