# A06_03_02_E02 Semantic-Credit Source Decomposition: Summary

## What We Established

The learned-specialist wrong-route basin has two causal components. Background
positions reverse the initial useful-expert margin pressure, but removing them
does not make selected-only top-1 feedback sufficient. At useful rank 2,
task-only top-1 correction rises from `0/128` to `42/128` (`32.8125%`), whereas
task-only soft routing corrects `128/128`. At rank 4, task-only top-1 remains
`0/128`, while task-only soft again corrects `128/128`.

The supported verdict is **dual bottleneck**: semantic credit is assigned to the
wrong positions under full LM loss, and the selected-only path still lacks
enough information about an unselected useful expert.

## Exact Setup

- Data: four equally frequent instruction-defined transformations; sequence
  length 33; 16 instruction-dependent and 16 background next-token targets.
- Model: one causal-attention layer, residual and LayerNorm, no learned position
  embedding, and four trainable MLP experts.
- Specialist state: 200 expert-only exposure updates; held-out median useful
  expert advantage `8.8947` loss units.
- Intervention: clone identical useful-rank-2/rank-4 routers; freeze experts and
  representation; train the router for 300 SGD updates at learning rate `0.001`.
- Conditions: full, task-only, background-only, half-scaled task-only top-1, and
  task-only soft mixture.
- Replication: 32 seeds and four tasks per seed, or 128 paired cells per
  condition. Remote four-GPU job `pt-t897a1ag` succeeded.

## Primary Evidence

| Initial useful rank | Full top-1 | Task top-1 | Half-task top-1 | Background top-1 | Task soft |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 0.0% | 32.8125% | 14.8438% | 0.0% | 100.0% |
| 4 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |

At rank 2, median initial source pressure is `+2.6106` for task positions,
`-9.0820` for background positions, and `-3.3286` for their full-loss mixture.
Background pressure is negative in `128/128` cells; task pressure is positive
in `107/128`. The exact gradient decomposition has maximum relative error
`3.30e-7`, and the half-task scale identity has zero measured error.

![Initial source pressure](figures/initial_source_pressure.png)

The figure tests the sign of each loss source's first-order effect on the
useful-versus-selected margin. Positive values favor the useful expert. It
shows that task positions are usually corrective, but background positions are
larger and uniformly anti-corrective, making the full gradient anti-corrective.
It does not show that positive initial pressure guarantees a finite-time route
crossing.

![Source-branch trajectories](figures/source_branch_trajectories.png)

The figure compares rank-2 trajectories from identical initial tensors. Task
masking raises useful-expert probability only modestly and leaves median regret
near one; all-expert soft utility coverage drives probability above one half
and removes almost all routing excess. Background-only training moves in the
wrong direction. The plot establishes causal branch behavior in this
controlled task, not a deployable position selector.

## Hypothesis Update

- H1, background override alone: weakened. Background override is real, but
  task-only top-1 does not reach the preregistered 90% correction rate.
- H2, selected-only blindness alone: weakened. Task masking produces a real
  rank-2 improvement, so background is not irrelevant.
- H3, dual bottleneck: supported. Removing background improves rank-2
  correction but remains far below soft utility coverage; rank 4 remains fully
  trapped without utility coverage.
- H4, no source bottleneck: rejected.

## Decision And Boundary

The next router candidate must jointly control **where route credit is taken
from** and **which candidate experts expose utility-bearing outputs**. A loss
mask alone is incomplete; always-soft routing is a mechanism control with four
activated experts, not a production design.

This experiment does not provide a label-free semantic-position estimator,
prove MTP supplies beneficial routing credit in language, define natural
semantic experts, or establish a compute-efficient sparse router.

## Next Decision

Test whether a bounded two-expert candidate set plus task-credit weighting can
recover the useful expert with near-top-1 activated compute, and whether either
component alone is insufficient. MTP enters only as a candidate non-oracle
credit estimator after this joint sufficiency test.
