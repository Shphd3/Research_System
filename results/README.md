# Results

Use this folder for curated, valuable stage-level research outcomes.

This is not a dump for raw experiment outputs. A result belongs here only when
it is stable enough to be reused in mainline files, hypothesis closures, meeting
briefs, PRISM reports, or future project framing.

## Folder Contract

Each curated result is a folder:

```text
results/R001_short_name/
  README.md
  figures/
  tables/
  source_notes/
```

Only `README.md` is required. Add `figures/`, `tables/`, or `source_notes/`
when the result needs reusable evidence.

## README Shape

```markdown
# R001 Short Name

## Result

## Why It Matters

## Evidence

## Claim Boundary

## Reuse Links
```

## Add A Result Only When

- it changes a claim boundary, bottleneck, or next decision;
- it will likely be cited across meetings, reports, or project mainlines;
- the daily or experiment source material is too noisy to reread every time.

## Current Curated Results

- `R001_dclm_moe_input_sparse_atom/`: real DCLM MoE-input sparse-atom summary.
- `R002_correlation_aware_feature_zipf/`: negative result for explicit
  correlation-aware Feature-Zipf routing.
