# Detailed: A06_01_06_E01 Singular Direction Convergence Metric

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 0. Quick Recap

Purpose: operationalize "direction convergence".

Hypothesis: a known common feature direction can show low projector drift while
its singular value still grows.

Conclusion: supported on the rank-one nested surface; wide robustness remains
unclear.

Evidence: `tables/a08_01_aggregate.csv` and
`figures/a08_01_convergence_curves.png`.

## 1. Protocol Compliance Audit

approved conditions match actual conditions: yes.

primary metric exists: yes, \(K_i\), \(G_i\), and feature alignment.

central figures/tables exist: yes.

seeds/checkpoints recorded: yes, 8 seeds and checkpoint trace.

known good/bad/confusing cases reviewed: yes.

success/failure/insufficient criteria applied: yes.

## 2. Setup

Data: synthetic nested directions `A -> AB -> ABC -> ABCD` in 32 dimensions.
Training is skewed toward common `A`; evaluation is balanced by level.

Model: rank-one MLP for the main test and hidden-dimension-4 MLP for the wide
guard.

Training: AdamW, 720 steps, checkpoint interval 40, batch size 256.

## 3. Metrics

\(K_i\): spectral norm distance between adjacent rank-one right-singular
projectors.

\(G_i\): change in top singular value between adjacent checkpoints.

Feature alignment: squared projection of the learned direction onto known
synthetic feature directions.

Convergence pass: at least three stable post-warmup checkpoints with low \(K_i\),
positive \(G_i\), small alignment drift, and sufficient feature alignment.

## 4. Main Results

| Condition | Pass rate | Final \(K\) | Final \(G\) | Main alignment |
| --- | ---: | ---: | ---: | ---: |
| rank1_nested | `1.0000` | `0.0316` | `0.0301` | `0.7865` |
| wide_nested | `0.5000` | `0.0554` | `0.0588` | `0.3322` |
| balanced_guard | `0.0000` | `0.0526` | `-0.0070` | `0.2072` |
| shuffled_feature_guard | `0.0000` | `0.0250` | `0.0221` | `0.0218` |

Interpretation: the rank-one common direction behaves like the mentor/r1 prior:
direction stabilizes while gain can still increase. The wider model does not
give a clean single-direction read, so robustness is not established.

## 5. Visualization Results

### Convergence Curves

![Convergence curves](figures/a08_01_convergence_curves.png)

Purpose: show whether the rank-one common direction has a stable window.

Setup: average checkpoint curves over 8 full-run seeds.

How to read: lower drift and higher alignment are better; singular value can
continue to rise after drift becomes small.

Observed result: drift is low after warmup, A alignment is high, and singular
value continues to grow.

Take-home: the convergence metric is usable for the next synthetic card.

Remaining uncertainty: wide/multi-direction settings need a better direction
matching rule.

## 6. Failure Decomposition

Falsified physical prior: no.

Falsified mathematical model: no for rank-one; incomplete for wide models.

Falsified operationalization / proxy: no for rank-one.

Falsified implementation: no.

Falsified metric: no, but the metric is currently rank-local.

Remaining rival explanations: wide-model direction rotation and multiple
equivalent directions.

## 7. Claim Boundary

Can claim: rank-one nested common directions can satisfy a concrete convergence
criterion.

Cannot claim: real-DCLM convergence, semantic directions, or wide-model
robustness.

## 8. Links And Artifact Map

runner:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a08_singular_direction_preservation.py`

config:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a08_singular_direction_preservation.json`

raw result dir:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a08_singular_direction_preservation/a08_singular_preservation_full_20260628_2`

tables: `tables/a08_01_aggregate.csv`, `tables/a08_01_checkpoint_trace.csv`,
`tables/decision_metrics.json`.

figure: `figures/a08_01_convergence_curves.png`.

repro command:

```bash
python scripts/run_a08_singular_direction_preservation.py \
  --config configs/a08_singular_direction_preservation.json \
  --run-name a08_singular_preservation_full_20260628_2 \
  --run-stage full \
  --seeds 20260628,20260629,20260630,20260631,20260632,20260633,20260634,20260635 \
  --device cuda
```

job id: local CUDA run, no ACP job id.
