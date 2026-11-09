# Detailed: A13_00_01_E03 Schedule-Only Carrier Audit

Primary anchor:
[13_00_01](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Protocol: [protocol.md](protocol.md)

Summary: [summary.md](summary.md)

## 0. Quick Recap

Purpose: isolate persistent update-size noise.

Hypothesis: cosine decay makes the width-64 carrier pass.

Conclusion: strongly improved but formally failed.

Evidence: relay mean `0.9437`, donor-follow `0.9845`, all relay seeds capable at
some checkpoint, but final multi-seed stability below threshold.

## 1. Terminology / Definitions

The setup uses the definitions in [summary.md](summary.md) and
[protocol.md](protocol.md). `Best checkpoint` is debug evidence only; the
registered verdict uses the final checkpoint.

## 2. Anchor Link And Decision Point

E03 remains an NTP-only carrier audit. No objective result exists.

## 3. Protocol Compliance Audit

Only the learning-rate schedule changed: yes.

Primary metric and original thresholds retained: yes.

All seeds/conditions/checkpoints recorded: yes.

Known cases reviewed: yes.

Verdict applied without threshold relaxation: yes.

## 4. Setup

Data, masks, model depth, width 64, optimizer family, batch order, seeds, and
3,000-step budget match E02. Learning rate follows the registered cosine
formula. Runtime was `142.55` seconds on one H100.

## 5. Metrics And Decision Rules

Unchanged carrier gates. Selector-conditional accuracy is debug-only.

## 6. Main Results

| Seed | relay final | relay best | selector A final | selector B final | bypass final |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1301 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1302 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1303 | 0.9223 | 1.0000 | 0.8462 | 1.0000 | 1.0000 |
| 1304 | 0.8252 | 1.0000 | 0.8269 | 0.8235 | 1.0000 |
| 1305 | 0.9709 | 0.9806 | 1.0000 | 0.9412 | 0.8350 |

The failures are not a universal selector branch: seed 1303 is weak on A,
seed 1305 is weak on B, and seed 1304 degrades on both. This weakens a simple
single-branch data bug.

## 7. Visualization Results

![Cosine schedule carrier trajectories](figures/carrier_trajectory.png)

Purpose: compare stable acquisition across structural controls.

Metric: fraction correct on 103 held-out triples.

Expected: relay 2L and bypass 1L stabilize above `0.95`.

Observed: all relay seeds cross or approach mastery, but two do not retain it;
one bypass seed remains below.

Take-home: optimization scale mattered, but width-64 robustness remains below
the registered standard.

Remaining uncertainty: shared representational capacity versus initialization.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| structural | relay 1L `0.0583` | pass | none | bypass leak |
| interface | bypass mean `0.9670` | pass | none | general output failure |
| reachability | every relay seed best \(\ge0.9806\) | pass as debug | none | architecture impossibility |
| final capability | mean `0.9437` | fail | seed-specific retention | stable width-64 eligibility |
| counterfactual | both gates pass | pass | none | selector/value independence |
| donor content | different-label follow `0.9845` | pass | none | non-specific patch damage |
| donor preservation | `0.9495` | fail by `0.0005` | clean accuracy ceiling | full carrier conjunction |

Falsified operationalization: width-64 final-state eligibility under the tested
schedule.

Remaining rival: representational/optimization capacity shared across
irreducible all-position losses and relay binding.

## 9. Full Experiment Record

Raw result:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/a13_00_01_e03_cosine_schedule_20260716`

## 10. Interpretation

The correct update is two-part. First, a diminishing learning rate repairs most
of the instability, so E02 was not merely a hard task. Second, crossing a
threshold once is not enough: carrier validation needs a stable multi-seed
surface, because the later objective comparison will otherwise inherit seed
selection bias.

## 11. Claim Boundary

No objective or workload-type claim is supported.

## 12. Next Decision

Test width 128 once under the same schedule; stop carrier repair if it fails.

## 13. Links And Artifact Map

runner:
`active/synthetic_data_understanding/scripts/run_a13_query_conditioned_relay.py`

config:
`active/synthetic_data_understanding/configs/a13_00_01_e03_cosine_schedule.json`

tables:
[final metrics](tables/final_metrics.csv),
[counterfactual](tables/counterfactual_audit.csv),
[patch](tables/relay_patch_audit.csv).

figure: [trajectory](figures/carrier_trajectory.png).
