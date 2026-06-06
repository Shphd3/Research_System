# 02 Experiment Plan

Status: first-round known-good plan.

Decision question:

```text
Under favorable conditions, can linear router preserve route-pattern separation?
```

## Fixed Setup

```text
2 orthogonal features
2 experts
linear router
balanced feature frequency
prediction-loss proxy
```

Known-good condition:

```text
favorable expert initialization
mild router diagonal prior
```

Do not run:

```text
full initialization grid
architecture changes
full NTP
utility-alignment claim
```

## Metrics

Primary:

```text
route-feature heatmap
```

Secondary:

```text
NMI / assignment accuracy
entropy / collapse indicator
loss sanity check
```

## Judgment

Success:

```text
diagonal or anti-diagonal heatmap persists across checkpoints;
NMI / assignment accuracy high;
no one-expert collapse.
```

Failure:

```text
mixed routing, collapse, or separation disappears.
```

Insufficient evidence:

```text
single seed only;
final checkpoint only;
metric conflict;
shortcut not ruled out.
```

## Artifact Requirements

```text
figures/heatmap_*.png
figures/trajectory_*.png
tables/metrics_by_checkpoint.csv
tables/seed_checkpoint_summary.csv
notes/run_observations.md
```

## Next Logic

```text
known-good succeeds -> remove router prior
known-good fails -> inspect expressivity / gradient / expert imbalance / implementation
insufficient evidence -> add seed/checkpoint, not broad grid
```

