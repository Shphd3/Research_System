# Detailed: A07_01 Nested Common Backbone Reproduction

Primary anchor:
`../../../problem_anchors/07_features_overlap/07_01_common_rare_conflict_metric_audit_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 0. Quick Recap

Purpose: reproduce the mentor's nested common-backbone mechanism on a controlled
surface.

Hypothesis: high-frequency \(A\) creates a stable common projector \(P_C\), while
common projected energy \(S_C\) keeps growing after warmup.

Experiment logic: train CE/AdamW on a frequency-skewed nested chain and compare
against a balanced-frequency guard.

Conclusion: supported for the controlled rank-one hidden model.

Evidence: `tables/a07_01_aggregate.csv`,
`figures/a07_01_backbone_curves.png`.

## 1. Anchor Link And Decision Point

This closes the A07_01 reproduction gate. It does not close A07_02 or A07_03.

## 2. Protocol Compliance Audit

approved conditions match actual conditions: yes.

primary metric exists: yes, stable-late-gain signature.

central figures/tables exist: yes.

seeds/checkpoints recorded: yes, 8 seeds and checkpoint trace.

known good/bad/confusing cases reviewed: yes; child-only shortcut and balanced
frequency guard were included.

success/failure/insufficient-evidence criteria applied: yes.

## 3. Setup

Code workspace:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

Runner:
`active/synthetic_data_understanding/scripts/run_a07_nested_singular_interference.py`

Config:
`active/synthetic_data_understanding/configs/a07_nested_singular_interference.json`

Run name: `a07_nested_full_20260628_2`

Result dir:
`active/synthetic_data_understanding/results/a07_nested_singular_interference/a07_nested_full_20260628_2`

Curated dir:
`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A07/A07_01_nested_common_backbone_reproduction`

Job id: local CUDA run, no ACP job.

Repro command:

```bash
python active/synthetic_data_understanding/scripts/run_a07_nested_singular_interference.py \
  --config active/synthetic_data_understanding/configs/a07_nested_singular_interference.json \
  --run-name a07_nested_full_20260628_2 \
  --run-stage full \
  --device cuda
```

## 4. Metrics And Decision Rules

Primary metric:

\[
\delta_C(t)=\|P_C(t)-P_C(T_0)\|_2,\qquad
S_C(t)=\|W_1(t)P_C\|_F^2.
\]

Pass: low post-warmup \(\delta_C\), positive late gain, and child-only shortcut
below the guard threshold.

## 5. Main Results

Decision evidence:

| Metric | Nested skewed | Balanced guard |
| --- | ---: | ---: |
| pass rate | `1.0000` | `0.3750` |
| post max \(\delta_C\) | `0.1373` | `0.4513` |
| late gain | `1.5115` | `1.5653` |
| final \(A\) accuracy | `1.0000` | `0.9955` |
| final \(ABCD\) accuracy | `0.8768` | `0.9331` |
| true-\(A\) alignment | `0.7932` | `0.2121` |

Interpretation: frequency skew makes the learned top common direction align
with \(A\) and remain stable. Balanced training can learn the task, but it does
not produce the same \(A\)-aligned common backbone.

## 6. Visualization Results

### Common Backbone Curves

![Common backbone curves](figures/a07_01_backbone_curves.png)

Purpose: show the learning order, projector drift, and common energy growth.

Setup: average checkpoint traces over 8 seeds.

How to read: stable common backbone requires saturated \(A\), low \(\delta_C\), and
continued \(S_C\) growth.

Observed result: \(A\) is saturated, \(\delta_C\) remains low after warmup, and
\(S_C\) grows.

Take-home: the nested surface reproduces the mentor mechanism at the controlled
rank-one level.

Remaining uncertainty: the wide-MLP smoke run before this final config showed
subspace drift, so this reproduction is intentionally a minimal mechanism
surface, not a capacity model.

What this figure does not prove: harmful tail interference or method utility.

Anchor update implication: A07_01 should be marked supported-controlled.

## 7. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| Data validity | child-only tail accuracy `0.6187` | passed | none | independent child marker is not sufficient |
| Common backbone | post max \(\delta_C\) is `0.1373` | passed | none | unstable projector rival weakened |
| Late gain | \(S_C\) gain `1.5115` | passed | none | no-gain rival weakened |
| Balanced guard | true-\(A\) alignment `0.2121` | passed as contrast | none | frequency-free explanation weakened |

Falsified physical prior: none.

Falsified mathematical model: none for the controlled rank-one surface.

Falsified operationalization / proxy: not applicable.

Falsified implementation: none found.

Falsified metric: none.

Remaining rival explanations: this still may not transfer to wide transformers
or real language.

## 8. Full Experiment Record

Seeds: `20260628-20260635`.

Train counts: `[4096, 1024, 256, 64]`.

Balanced guard count: `768` per level.

Evaluation: `1024` per level.

Model: input dimension `32`, hidden dimension `1`.

Training: `720` steps, batch size `256`, learning rate `0.006`, weight decay
`0.0001`.

## 9. Interpretation

The result supports the first mentor-chain clause: a frequency-skewed nested
surface can produce a stable common direction with continued gain growth. This
is the right surface for asking whether tail updates are absorbed by that
common subspace.

## 10. Claim Boundary

Can claim: controlled reproduction of the common-backbone / late-gain geometry.

Cannot claim: tail harm, C3S benefit, MoE utility, real-DCLM transfer, or
semantic feature specialization.

## 11. Next Decision

Proceed to A07_02 on the same surface.

## 12. Links And Artifact Map

anchor:
`../../../problem_anchors/07_features_overlap/07_01_common_rare_conflict_metric_audit_anchor.md`

protocol: `protocol.md`

summary: `summary.md`

code workspace:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

runner:
`active/synthetic_data_understanding/scripts/run_a07_nested_singular_interference.py`

config:
`active/synthetic_data_understanding/configs/a07_nested_singular_interference.json`

key code files:
runner and config above.

data / manifest:
generated in-memory from config.

result dir:
`active/synthetic_data_understanding/results/a07_nested_singular_interference/a07_nested_full_20260628_2`

figure dir: `figures/`

key tables:
`tables/a07_01_aggregate.csv`, `tables/a07_01_summary.csv`,
`tables/a07_01_checkpoint_trace.csv`

logs / checkpoints: no persistent checkpoints.

repro command: see Setup.

job id: local run.
