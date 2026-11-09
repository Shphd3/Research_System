# Detailed: A07_02 Common-Controlled Rare Interference

## Conclusion

Common-control is supported on controlled D07. The rare-loss improvement is not explained by better load balance and does not erase the conflict signal.

## Setup

Run name: `a07_common_rare_conflict_full_20260623_1`

Run date: 2026-06-23.

Seeds: `20260623` to `20260630`.

Runner: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a07_common_rare_conflict.py`

Config: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a07_common_rare_conflict_full.json`

Execution type: local full synthetic audit, 4 logical shards. ACP four-card script was dry-run only.

## Method

Common-control subtracts an unlabeled train-set mean from routed-token hidden states, then performs unsupervised k-means routing on \(\phi(h_i)\). This tests whether removing common bias exposes conflict group structure.

The comparison is load-only routing with the same expert count, objective, evaluation split, and total budget.

## Primary Metric

`RIR_cc = L_rare(balance_only) - L_rare(common_control)`.

Observed: `0.9502 +/- 0.0006`.

`FoO_cc = 1.1049 +/- 0.0012`, using the A07_01 oracle gap denominator.

## Evidence Ledger

| Metric | Result |
| --- | ---: |
| load-only rare loss | `1.5300` |
| common-control rare loss | `0.5798` |
| `RIR_cc` | `0.9502` |
| `FoO_cc` | `1.1049` |

Load guard:

| Condition | Max load | Active experts | Load entropy |
| --- | ---: | ---: | ---: |
| load-only | `0.2500` | `4.0000` | `1.0000` |
| common-control | `0.2500` | `4.0000` | `1.0000` |
| oracle | `0.2500` | `4.0000` | `1.0000` |

Signal guard:

| Readout | Accuracy |
| --- | ---: |
| raw hidden to conflict group | `1.0000` |
| common-control phi to conflict group | `1.0000` |
| accuracy drop | `0.0000` |

## Visualization Results

![A07_02 common-control rare interference](figures/rare_interference_common_control.png)

Purpose: show rare-interference relief by common-control.

How to read: `RIR_cc` is the rare-loss gain over load-only; `FoO_cc` is the fraction of the oracle gap recovered.

Observed result: both are positive and large.

Take-home: common-control has a controlled method benefit beyond matched load.

What it does not prove: real trained-checkpoint robustness, semantic experts, or real-data transfer.

## Artifact Map

Raw result dir: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a07_common_rare_conflict/a07_common_rare_conflict_full_20260623_1`

Curated tables:

- `tables/common_control_rir.csv`
- `tables/matched_load_guard.csv`
- `tables/conflict_signal_preservation.csv`
- `tables/checkpoint_assignment_manifest.csv`

Curated figure: `figures/rare_interference_common_control.png`

Repro command:

```bash
python scripts/run_a07_common_rare_conflict.py --config configs/a07_common_rare_conflict_full.json --run-name a07_common_rare_conflict_full_20260623_1 --run-stage full --seeds 20260623,20260624,20260625,20260626,20260627,20260628,20260629,20260630 --aggregate-only --device cpu
```

## Boundary

This is a controlled synthetic method test. It is not a real neural checkpoint training result.
