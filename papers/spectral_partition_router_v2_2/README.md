# Spectral Partition Router v2.2

This folder is the revised static-dispatch version after `spectral_partition_router_v2_1`.

## Why v2.2 exists

`v2_1` correctly noticed that equal-mass dispatch is not enough for a good router, but it mixed two stages:

```text
static good feature dispatch
training-time preservation
```

For the next stage, preservation is removed from the paper scope.  The goal is to first define and solve a sharper static problem:

```text
In a spectrally isotropic route-relevant feature space, what is a good static feature dispatch,
and what additional feature assumptions make such dispatch identifiable and useful?
```

## Core correction

Recursive quantiles can equalize probability mass for many feature distributions.  Therefore spectral isotropy is **not** the causal condition for equal mass.

The revised thesis is:

```text
Spectral isotropy removes global anisotropic confounds.
Local feature structure provides recoverable feature coherence.
Optional expert alignment assigns coherent cells to expert identity.
Quantiles enforce equal mass after a split direction is chosen.
```

## Static good dispatch

V2.2 studies three static targets:

1. **Equal mass**: each expert receives probability mass `1/E`.
2. **Feature coherence**: routes preserve latent feature structure when such structure exists.
3. **Static utility / expert compatibility**: the partition helps a controlled static learning task or aligns with model-internal expert geometry.

It explicitly does **not** study training preservation, representation drift, or dynamic recalibration.

## Main middle-regime assumption

The productive regime is neither full spherical uniformity nor arbitrary covariance isotropy.  V2.2 studies:

```text
globally spectrally isotropic but locally structured route-relevant features
```

Examples:

```text
F ~ Uniform({1,...,K})
X | F=f = mu_f + epsilon
Cov(X) approximately sigma^2 I after centering / whitening
mu_f are separated enough to create local feature structure
```

Latent labels `F` are never used by the router.  They are used only for evaluation.

## Files

```text
README.md
PROBLEM_STATEMENT.md
METHOD_AND_THEORY_NOTES.md
RESEARCH_PLAN.md
exp/EXPERIMENT_PLAN.md
exp/CODEX_TASKS.md
latex/paper.tex
latex/math_commands.tex
latex/references.bib
```

## Current status

This folder is a scaffold for the static good-dispatch stage.  It should replace the preservation-heavy v2.1 storyline for the next paper iteration.  Experimental numbers should not be inserted until the v2.2 experiments are implemented and run.
