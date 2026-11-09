# Detailed: A07_05 Common-Update Interference Diagnostic

## Conclusion

The full run weakens A07_05 as a mainline utility mechanism. It finds a
direction-specific rare-loss effect from common updates, but the effect is
below the pre-set pass threshold. Projection and sanity guards pass, so the
mechanism is not falsified outright; it is not strong enough to promote.

## Protocol Compliance Audit

Approved protocol: `protocol.md`.

Actual full run: `a07_05_common_update_full_local_2gpu_20260625_1`.

Seeds matched protocol: yes, `20260623-20260630`.

Primary metric exists: yes, `tables/decision_summary.csv` and
`tables/stage_summary.csv`.

Norm-matched controls exist: yes, `random_update` and `unrelated_update` in
`tables/perturbation_summary.csv`.

Rare update sanity exists: yes, `rare_update_sanity` in
`tables/perturbation_summary.csv`.

Projection guard exists: yes, `tables/projection_summary.csv`.

Central figures exist: yes, `figures/rare_loss_effect.png` and
`figures/projection_fraction.png`.

Real-data bridge: not run. The controlled causal perturbation did not pass the
effect threshold, so the protocol gate for a real-data observational bridge did
not open.

Deviation: the implemented model is a small MLP classifier rather than a small
transformer. This is within the protocol's "matched small model with
reconstructable update directions" clause and keeps the mechanism isolated.

## Setup

Runner:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a07_05_common_update_interference_diagnostic.py`

Config:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a07_05_common_update_interference_diagnostic.json`

Raw result dir:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a07_05_common_update_interference_diagnostic/a07_05_common_update_full_local_2gpu_20260625_1`

Curated experiment dir:
`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A07/A07_05_common_update_interference_diagnostic`

External job id: none. This was a local two-H100 run.

## Data And Model

Data: controlled four-group nested-conflict classification surface.

| Group | Role | Parent |
| --- | --- | --- |
| `0` | common | `0` |
| `1` | rare exception | `0` |
| `2` | common | `1` |
| `3` | rare exception | `1` |

The rare groups share parent features with common groups but require different
labels. Training uses common-only warmup before the update perturbation audit.
Evaluation is balanced across all four groups.

Model: two-layer MLP classifier with hidden size `64`, trained with AdamW.

Full configuration:

| Item | Value |
| --- | ---: |
| input dimension | `32` |
| train common per group | `4096` |
| train rare per group | `768` |
| eval per group | `1536` |
| warmup steps | `80` |
| learning rate | `0.014` |
| perturbation step scale | `2.0` |
| seeds | `8` |

## Algorithm

1. Train the MLP on common groups only.
2. Freeze the checkpoint.
3. Compute negative-gradient update directions for common, rare, unrelated,
   and random controls.
4. Norm-match all directions to the common-update norm.
5. Apply one perturbation from the same checkpoint for each direction.
6. Measure rare/common loss deltas.
7. Estimate the common-update projector from group-specific common updates.
8. Measure rare update mass in that projector and split-half projector
   stability.

## Evidence Ledger

Decision table:

| Metric | Mean |
| --- | ---: |
| `common_to_rare_loss_effect` | `0.00168` |
| `common_update_rare_loss_delta` | `0.00168` |
| `rare_update_sanity_rare_loss_delta` | `-0.00406` |
| `rare_common_update_fraction` | `0.22076` |
| `projector_stability` | `0.85250` |
| `baseline_rare_common_loss_gap` | `13.06880` |
| anchor decision | `weakened_or_insufficient` |

Perturbation table:

| Perturbation | Rare loss delta | Common loss delta | Direction norm applied |
| --- | ---: | ---: | ---: |
| `common_update` | `0.00168 +/- 0.00053` | `-0.00000020 +/- 0.00000014` | `0.00032 +/- 0.00011` |
| `random_update` | `0.00000 +/- 0.00006` | `0.00000000 +/- 0.00000001` | `0.00032 +/- 0.00011` |
| `unrelated_update` | `-0.00278 +/- 0.00089` | `0.00000015 +/- 0.00000012` | `0.00032 +/- 0.00011` |
| `rare_update_sanity` | `-0.00406 +/- 0.00140` | `0.00000009 +/- 0.00000006` | `0.00032 +/- 0.00011` |

Projection table:

| Row | Value |
| --- | ---: |
| rare group `1` projection fraction | `0.21022 +/- 0.02474` |
| rare group `3` projection fraction | `0.23131 +/- 0.04924` |
| projector stability | `0.85250 +/- 0.04114` |
| projector rank | `2` |

Stage table:

| Metric | Value |
| --- | ---: |
| baseline common loss | `0.000083 +/- 0.000045` |
| baseline rare loss | `13.06889 +/- 0.42271` |
| baseline common acc | `1.00000` |
| baseline rare acc | `0.00000` |
| common update norm | `0.000316 +/- 0.000109` |
| rare update norm | `6.42186 +/- 0.10011` |

Interpretation: rare examples are strongly underlearned, and the common
projector is stable. However, the common-update norm at this warmup checkpoint
is very small, so even the direction-specific rare harm remains small.

## Visualization Results

### Rare-Loss Effect

![Rare-loss effect](figures/rare_loss_effect.png)

Purpose: test whether a common-example update causes rare loss to increase
beyond matched controls.

Setup: full aggregate across 8 seeds; all directions are norm-matched to the
common-update norm.

How to read: a positive bar means rare loss increased after the perturbation.
The anchor would pass only if `common_update` clearly exceeds the controls.

Observed result: `common_update` is positive, `random_update` is approximately
zero, `unrelated_update` is negative, and `rare_update_sanity` is negative.

Take-home: the direction is specific, but the effect is too small for the pass
criterion.

Remaining uncertainty: an earlier or less saturated common-update checkpoint
might produce a larger effect, but that would require a separate
checkpoint-window audit.

### Rare Update Projection

![Rare update projection](figures/projection_fraction.png)

Purpose: test whether rare updates share mass with the common-update subspace.

Setup: common projector is estimated from group-specific common updates; rare
projection is measured for rare groups `1` and `3`.

How to read: higher fraction means more rare update energy lies inside the
common-update projector.

Observed result: both rare groups have nonzero projection, and split-half
projector stability is high.

Take-home: overlap exists, but overlap alone did not create a strong enough
rare-loss harm.

Remaining uncertainty: projection may be a necessary diagnostic but not a
sufficient utility mechanism.

## Failure Interpretation

The physical prior is partially visible: rare updates overlap the common-update
subspace, and common updates hurt rare loss more than random controls.

The causal effect is too weak: `common_to_rare_loss_effect = 0.00168`, below
the threshold `0.005`.

The rare surface is valid but harsh: rare loss is high and rare update sanity
reduces rare loss, but rare accuracy remains zero for the norm-matched
one-step perturbation.

The common-update checkpoint is close to common saturation: common loss is
near zero and common update norm is small. This limits effect size and prevents
promotion to a utility claim.

## Artifact Map

Curated tables:

- `tables/decision_summary.csv`
- `tables/stage_summary.csv`
- `tables/stage_by_seed.csv`
- `tables/perturbation_summary.csv`
- `tables/perturbation_by_seed.csv`
- `tables/projection_summary.csv`
- `tables/projection_by_seed.csv`
- `tables/group_loss_delta_summary.csv`
- `tables/group_loss_by_seed.csv`

Curated figures:

- `figures/rare_loss_effect.png`
- `figures/projection_fraction.png`

Curated scripts:

- `scripts/run_a07_05_common_update_interference_diagnostic.py`
- `scripts/a07_05_common_update_interference_diagnostic.json`

Manifest:

- `run_manifest.json`

Repro commands:

```bash
CUDA_VISIBLE_DEVICES=0 python active/synthetic_data_understanding/scripts/run_a07_05_common_update_interference_diagnostic.py \
  --config active/synthetic_data_understanding/configs/a07_05_common_update_interference_diagnostic.json \
  --run-name a07_05_common_update_full_local_2gpu_20260625_1 \
  --run-stage full \
  --num-shards 2 \
  --shard-index 0 \
  --device cuda:0
```

```bash
CUDA_VISIBLE_DEVICES=1 python active/synthetic_data_understanding/scripts/run_a07_05_common_update_interference_diagnostic.py \
  --config active/synthetic_data_understanding/configs/a07_05_common_update_interference_diagnostic.json \
  --run-name a07_05_common_update_full_local_2gpu_20260625_1 \
  --run-stage full \
  --num-shards 2 \
  --shard-index 1 \
  --device cuda:0
```

```bash
python active/synthetic_data_understanding/scripts/run_a07_05_common_update_interference_diagnostic.py \
  --config active/synthetic_data_understanding/configs/a07_05_common_update_interference_diagnostic.json \
  --run-name a07_05_common_update_full_local_2gpu_20260625_1 \
  --run-stage full \
  --aggregate-only
```

## Claim Boundary

Can claim: common-update direction has a small, direction-specific rare-loss
harm on this controlled surface; rare updates overlap a stable common-update
subspace.

Cannot claim: common-update interference is a sufficient utility mechanism,
MoE partitioning improves rare learning, real-DCLM transfer, semantic experts,
or scaling.

## Next Decision

Do not use A07_05 as positive evidence for a partition-value anchor. Keep it
as mechanism reserve. The mainline should continue through A06 preservation
unless a future decision explicitly opens a checkpoint-window audit for the
common-update mechanism.
