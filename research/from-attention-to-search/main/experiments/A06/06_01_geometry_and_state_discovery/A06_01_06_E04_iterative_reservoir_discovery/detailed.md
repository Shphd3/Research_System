# Detailed: A06_01_06_E04 Iterative Reservoir Direction Discovery

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 0. Quick Recap

Purpose: test the r1 iterative reservoir loop.

Hypothesis: after freezing \(A\), the residual learns \(B\); after freezing \(A,B\),
the residual learns \(C\).

Conclusion: failed under the current operationalization.

Evidence: `tables/a08_04_aggregate.csv` and
`figures/a08_04_iterative_alignment.png`.

## 1. Protocol Compliance Audit

approved conditions match actual conditions: main protocol conditions yes.

primary metric exists: yes, next-level alignment.

central figures/tables exist: yes.

seeds/checkpoints recorded: yes, 8 seeds.

known good/bad/confusing cases reviewed: yes.

success/failure/insufficient criteria applied: yes.

protocol change: oracle residual debug conditions were added after the learned
loop failed, to localize whether failure came from learned-projector leakage or
from the residual objective itself.

## 2. Setup

Data: same nested synthetic surface.

Stage 1: train rank-one model on full input and audit A alignment.

Stage 2: remove learned stage-1 direction, train residual model, audit B
alignment.

Stage 3: remove learned stage-1 and stage-2 directions, train residual model,
audit C alignment.

Debug: repeat stage 2/3 using oracle previous directions.

## 3. Metrics

Target alignment: squared projection onto the intended next feature.

Old overlap max: largest squared projection onto already extracted directions.

Next-level alignment: target alignment minus old overlap. Positive means the
new stage is more aligned to the next feature than to old features.

## 4. Main Results

| Condition | Target alignment | Old overlap | Next-level alignment |
| --- | ---: | ---: | ---: |
| one_stage_common | `0.7819` | `0.0000` | `0.7819` |
| two_stage_A_then_B | `0.0078` | `0.2006` | `-0.1928` |
| three_stage_A_B_C | `0.0521` | `0.1544` | `-0.1023` |
| shuffled_residual_guard | `0.0061` | `0.0361` | `0.0061` |
| oracle_two_stage_A_then_B | `0.0567` | `0.0000` | `0.0567` |
| oracle_three_stage_A_B_C | `0.2601` | `0.0000` | `0.2601` |

Interpretation: learned residualization does not expose the next direction.
Oracle residualization partly helps for C after A/B removal, but does not make
B strong. The current loop lacks a stage objective that isolates child
directions.

## 5. Visualization Results

### Iterative Alignment

![Iterative alignment](figures/a08_04_iterative_alignment.png)

Purpose: show whether each stage discovers a new nested direction.

Setup: learned residual stages plus oracle residual debug stages.

How to read: positive bars indicate a new child direction; negative bars mean
old-direction overlap dominates.

Observed result: learned stage 2 and stage 3 are negative; oracle stage 3 is
positive but oracle stage 2 remains weak.

Take-home: "freeze old direction and train residual" is not enough.

Remaining uncertainty: a loss decomposition or curriculum objective may be
needed before the loop can be fairly tested.

## 6. Failure Decomposition

Falsified physical prior: not fully; nested directions exist, but the simple
loop does not reveal them.

Falsified mathematical model: partially. \(h_{k+1}=(I-P_{\le k})h\) is
insufficient without a stage-local objective.

Falsified operationalization / proxy: yes. Learned residual extraction fails.

Falsified implementation: no.

Falsified metric: no; the metric catches repeated old-direction overlap.

Remaining rival explanations: imperfect learned projector, residual target
noise, frequency imbalance, and missing stage objective.

## 7. Claim Boundary

Can claim: the first common direction is recoverable.

Cannot claim: iterative reservoir discovery, real-data hierarchy discovery, or
method readiness.

## 8. Links And Artifact Map

runner:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a08_singular_direction_preservation.py`

raw result dir:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a08_singular_direction_preservation/a08_singular_preservation_full_20260628_2`

tables: `tables/a08_04_aggregate.csv`, `tables/a08_04_iterative_metrics.csv`,
`tables/decision_metrics.json`.

figure: `figures/a08_04_iterative_alignment.png`.

job id: local CUDA run, no ACP job id.
