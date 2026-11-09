# Detailed Notes: E2-H H-MoE Hierarchical Routing Side Branch

## Run

Runnable workspace:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

Script:

```text
scripts/run_hmoe_hierarchical_side_branch.py
```

Config:

```text
configs/e2_h_hmoe_hierarchical_side_branch.json
```

Full output:

```text
outputs/e2_h_hmoe_hierarchical_side_branch/
figures/e2_h_hmoe_hierarchical_side_branch/
```

## Data Audit

L1 phrases were exact 2-token units. Actual count matched planted count with zero background collision for all L1 phrases.

L2 events were exact 6-token event units. Background collisions were low:

| event | planted | actual | collision |
|---|---:|---:|---:|
| F1_E1_A1_O1 | 35174 | 35181 | 7 |
| F1_E2_A1_O2 | 17473 | 17475 | 2 |
| F2_E1_A2_O3 | 14285 | 14287 | 2 |
| F2_E3_A2_O4 | 6955 | 6955 | 0 |
| F3_E2_A3_O1 | 5779 | 5779 | 0 |
| F3_E4_A3_O3 | 2810 | 2810 | 0 |
| F4_E3_A4_O2 | 2131 | 2132 | 1 |
| F4_E4_A4_O4 | 1073 | 1073 | 0 |

Conditional probability for L1 prefix was exactly 1.0 in the generated stream. L2 prefix target probability stayed around 0.988-0.999, meaning the event prefix was highly predictive but still had small accidental/context effects.

## Readback Table

| variant | level | mean probability | std | mean margin | top1 acc |
|---|---|---:|---:|---:|---:|
| dense | L1 | 0.998908 | 0.001872 | 9.549 | 1.00 |
| dense | L2 | 0.991892 | 0.004257 | 6.543 | 1.00 |
| flat8_lb | L1 | 0.999392 | 0.000676 | 9.725 | 1.00 |
| flat8_lb | L2 | 0.991176 | 0.004775 | 6.620 | 1.00 |
| hmoe4x2_lb | L1 | 0.999544 | 0.000548 | 9.997 | 1.00 |
| hmoe4x2_lb | L2 | 0.990607 | 0.004500 | 6.452 | 1.00 |

## Routing Summary

| metric | NMI mean | NMI std | purity mean |
|---|---:|---:|---:|
| flat expert vs L1 phrase | 0.596 | 0.080 | 0.397 |
| flat expert vs L1 role | 0.278 | 0.063 | 0.631 |
| flat expert vs L2 family | 0.457 | 0.179 | 0.607 |
| hmoe root vs L2 family | 0.381 | 0.312 | 0.504 |
| hmoe root vs L1 phrase | 0.459 | 0.112 | 0.229 |
| hmoe leaf vs L1 phrase | 0.331 | 0.028 | 0.167 |
| hmoe path vs L1 phrase | 0.564 | 0.063 | 0.340 |
| hmoe path vs L2 family | 0.464 | 0.293 | 0.584 |

Interpretation: H-MoE path-level alignment is comparable to Flat expert alignment, but root-level alignment with L2 family is not stronger and has high seed variance.

## Event Root Consistency

| seed | mean root majority fraction | all-same-root rate |
|---|---:|---:|
| 20260513 | 0.628 | 0.008 |
| 20260514 | 0.548 | 0.000 |
| 20260515 | 0.640 | 0.000 |
| 20260516 | 0.569 | 0.028 |
| 20260517 | 0.445 | 0.000 |

Across seeds, mean root majority fraction was `0.566 +/- 0.078`; all-same-root rate was about `0.007`. This means an event's six tokens usually did not remain under one stable root.

## Figure Paths

- `figures/frequency_rank_curves.png`: data frequency design.
- `figures/dense_flat_hmoe_l1_l2_readback.png`: readback comparison.
- `figures/routing_alignment_nmi.png`: routing-label alignment.
- `figures/flat_expert_by_l2_family.png`: flat expert vs high-level family.
- `figures/hmoe_root_by_l2_family.png`: H-MoE root vs high-level family.
- `figures/hmoe_path_by_l1_phrase.png`: H-MoE path vs low-level phrase.
- `figures/hmoe_event_root_consistency.png`: event internal root consistency.

