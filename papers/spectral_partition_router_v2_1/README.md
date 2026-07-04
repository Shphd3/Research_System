# Spectral Partition Router v2.1

This folder contains the next iteration after `spectral_partition_router_v2`.

## Core change from V2

V2 showed that recursive quantile routing can solve equal-mass dispatch, but equal mass alone does not guarantee meaningful feature partition or training preservation.

V2.1 therefore studies:

```text
equal mass + feature coherence + margin-based preservation
```

under mild explicit assumptions:

- globally spectrally normalized features;
- optional local cluster structure;
- optional expert-weight alignment;
- low boundary mass;
- bounded feature drift during training.

## Files

```text
latex/paper.tex                  # self-contained v2.1 draft, experiment section empty
latex/references.bib
latex/math_commands.tex
exp/README.md                    # experiment overview
exp/EXPERIMENT_PLAN.md           # full experiment design
exp/CODEX_TASKS.md               # implementation tasks for Codex
exp/TABLE_TEMPLATES.md           # result table templates
```

## Current status

No experimental results are claimed in this folder yet. The paper contains theory and protocols only.
