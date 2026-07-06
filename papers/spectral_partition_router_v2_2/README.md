# Spectral Partition Router v2.2

This folder contains the static-dispatch stage of the spectral routing project.

The scope is intentionally narrow:

```text
Goal: define and test static feature-family dispatch under globally
      spectrally isotropic and frequency-uniform feature distributions.

Out of scope: representation drift, dynamic router updates,
              route preservation during training, full learned-router MoE dynamics,
              and downstream task utility.
```

## Core question

We study a controlled clean case:

> If route-relevant feature families occur with uniform frequency and their aggregate representation is globally spectrally isotropic, can a label-free, batch-independent static router assign feature families to experts in a balanced and specialization-preserving way?

Here, "good dispatch" is not equal token counts.  A good static dispatch should balance expert usage while keeping each feature family intact.

## Difference from V1

V1 studied a strong spherical prototype case:

```text
spherical feature directions + equal-measure prototype cells
-> uniform top-1 expert usage
```

V2.2 studies a constructive feature-family problem:

```text
globally isotropic aggregate representation
+ uniformly frequent, locally recoverable feature families
-> balanced feature-family-to-expert dispatch
```

Thus V2.2 does not claim that spectral isotropy alone gives useful routing.  It identifies the additional condition required in the clean case: local feature-family recoverability.

## Main method: BFSR

The primary method is **BFSR: Balanced Feature-Specializing Routing**.

BFSR uses the clean-case assumptions directly:

```text
1. Fit a spectral normalizer on calibration features.
2. Recover feature families from calibration features without labels.
3. Assign recovered families to experts under a balanced constraint.
4. Route each future example by recovered family identity.
```

The mass mechanism is family-level frequency balance:

```text
uniform feature-family frequencies
+ equal number / equal estimated mass of families per expert
-> equal expected expert usage
```

Projection-quantile routing is retained as a baseline.  It can balance mass, but it is not the main mechanism for feature-family dispatch because it may split one coherent family across experts.

## Why spectral isotropy matters

Spectral isotropy is not the source of feature identity.  Its role is metric control:

```text
remove global anisotropic directions
make local feature recovery comparable across directions
separate global spectrum uniformity from local feature structure
```

A null isotropic Gaussian with labels independent of the representation should not yield feature-family dispatch for any label-free router.

## Static good dispatch

A static dispatch is evaluated by:

1. **Mass balance**: each expert receives approximately equal probability mass.
2. **Family consistency**: each feature family is routed mostly to one expert.
3. **Low split rate**: coherent feature families are not cut apart by the router.
4. **Information fraction**: expert identity carries information about feature-family identity.

For `K > E`, one expert necessarily receives multiple feature families.  Therefore the main metric is not ordinary route-to-feature purity.  Use family consistency, feature split rate, and `I(G;F)/H(G)` as primary indicators.

## Current executed result

The E1--E5 suite has been implemented and run.

Full-run setup:

```text
seeds: 0,1,2,3,4
d: 16
K: 32
E: 4
calibration examples: 8000
holdout examples: 16000
```

Main results:

```text
E1 clean case: BFSR-Cluster LoadCV 0.003, family consistency 0.990, cluster accuracy 0.986.
E2 isotropy null: admissible label-free methods expert information fraction about 0.002.
E3 recoverability: cluster accuracy rises 0.063 -> 0.942; family consistency rises 0.294 -> 0.956.
E4 whitening: structured distorted cluster accuracy rises 0.250 -> 0.958; null information remains about 0.002.
E5 frequency imbalance: equal-number BFSR LoadCV 0.149; mass-aware BFSR LoadCV 0.029.
```

## Files

```text
README.md                         # overview
PROBLEM_STATEMENT.md              # scope and definitions
METHOD_AND_THEORY_NOTES.md         # BFSR method and theorem sketches
RESEARCH_PLAN.md                   # falsifiable hypotheses and research anchors
AUDIT_2026_07_06.md                # claim and experiment audit
READING_GUIDE_2026_07_06.md        # guided reading path
MEETING_BRIEF_2026_07_06.md        # short Chinese meeting brief
exp/EXPERIMENT_PLAN.md             # experiment/result map
exp/CODEX_TASKS.md                 # implementation status and parked tasks
exp/run_static_dispatch_suite.py   # experiment runner
exp/src/static_bfsr_suite.py       # source utilities and routers
exp/results/                       # raw/aggregate results and summary
latex/paper.tex                    # polished paper draft
latex/tables/                      # generated paper tables
latex/figures/                     # generated paper figures
```

## Stage closure criterion

The current results support this narrow statement:

```text
Under globally spectrally isotropic, frequency-uniform, and locally recoverable
feature-family distributions, BFSR achieves balanced static feature-family
dispatch by recovering families and assigning them to experts under a balanced
constraint.
```

The current results do not support claims about downstream learning utility, real language-model hidden states, learned-router dynamics, automatic K selection, or training-time preservation.
