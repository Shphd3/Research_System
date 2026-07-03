# Experiments for Uniform Feature Routing from Spectral Expert Prototypes

This folder contains the execution plan for the paper:

`papers/uniform_feature_moe_initialization/latex/paper.tex`

The experiments are deliberately static before training dynamics. They test the exact claims in the paper:

1. uniform feature geometry + symmetric prototypes gives uniform expected expert load;
2. random prototype imbalance is a geometry floor, not finite-token noise;
3. expert principal singular directions can serve as router centers;
4. strict finite-token uniformity requires balanced assignment;
5. nonuniform feature spectra break the raw theorem assumptions and require whitening or explicit balancing;
6. training preservation is a separate margin question and should not block this paper.

## Minimal tonight target

Run E1--E5 with synthetic features only. Do not train a language model tonight.

Expected outputs:

```text
papers/uniform_feature_moe_initialization/exp/results/results.csv
papers/uniform_feature_moe_initialization/exp/results/summary.md
papers/uniform_feature_moe_initialization/exp/results/tables/*.md
```

## File guide

- `EXPERIMENT_PLAN.md`: full scientific protocol.
- `CODEX_TASKS.md`: step-by-step implementation contract for Codex.
- `run_synthetic.py`: starter executable script for E1--E5.
- `TABLE_TEMPLATES.md`: result tables to paste into the paper after runs.

## Main command

```bash
cd papers/uniform_feature_moe_initialization/exp
python run_synthetic.py --outdir results --quick
```

For the full run:

```bash
python run_synthetic.py --outdir results --full
```

## Claim boundary

The synthetic results can support the controlled routing theorem. They cannot support claims about real semantic experts, real language training, residual-induced anisotropy in trained Transformers, or long-term expert specialization preservation.
