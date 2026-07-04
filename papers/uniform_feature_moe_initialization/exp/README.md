# Experiments for Uniform Feature Routing from Spectral Expert Prototypes

This folder contains the execution plan for the paper:

`papers/uniform_feature_moe_initialization/latex/paper.tex`

The experiments are deliberately static before training dynamics. They test the exact claims in the paper:

1. uniform feature geometry + symmetric prototypes gives uniform expected expert load;
2. random prototype imbalance is a geometry floor, not finite-token noise;
3. expert principal singular directions can serve as router centers;
4. covariance isotropy alone is not directional uniformity;
5. nonuniform feature spectra in the elliptical toy setting can be repaired by whitening;
6. strict finite-token uniformity can be forced by balanced assignment, but that is only a control.

## Minimal tonight target

Run E1--E6 with synthetic features only. Do not train a language model for this paper.

Expected outputs:

```text
papers/uniform_feature_moe_initialization/exp/results/results.csv
papers/uniform_feature_moe_initialization/exp/results/summary.md
papers/uniform_feature_moe_initialization/exp/results/tables/*.md
```

## File guide

- `EXPERIMENT_PLAN.md`: full scientific protocol.
- `EXPERIMENT_REGISTRY.md`: mapping from E1--E6 to scripts, tables, figures, and paper labels.
- `CODEX_TASKS.md`: step-by-step implementation contract for Codex.
- `run_synthetic.py`: full-suite executable script for E1--E6.
- `run_e*.py`: per-experiment wrappers writing to `results/by_experiment/`.
- `TABLE_TEMPLATES.md`: current table index.

## Main command

```bash
cd papers/uniform_feature_moe_initialization/exp
python run_synthetic.py --outdir results --quick
```

For the full run:

```bash
python run_synthetic.py --outdir results --full
```

Run one experiment by ID:

```bash
python run_synthetic.py --experiments E4 --outdir results/by_experiment/e4_covariance_counterexample --full
```

## Claim boundary

The synthetic results can support the controlled routing theorem. They cannot support claims about real semantic experts, real language training, residual-induced anisotropy in trained Transformers, or long-term expert specialization preservation.
