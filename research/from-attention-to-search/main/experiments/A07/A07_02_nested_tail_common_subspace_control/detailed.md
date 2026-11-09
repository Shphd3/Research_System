# Detailed: A07_02 Nested Tail Common-Subspace Control

Primary anchor:
`../../../problem_anchors/07_features_overlap/07_02_common_controlled_rare_interference_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 0. Quick Recap

Purpose: test whether active update control away from \(P_C\) improves rare
nested tail learning.

Hypothesis: if tail updates overuse the common subspace, suppressing that
component should reduce tail loss while preserving \(A\).

Experiment logic: freeze \(P_C\) after A07_01 warmup, then compare CE, confidence
gate only, subspace suppression only, and combined control.

Conclusion: supported on the controlled rank-one surface.

Evidence: `tables/a07_02_aggregate.csv`,
`figures/a07_02_control_results.png`.

## 1. Anchor Link And Decision Point

This tests the method-facing A07_02 gate. It does not prove real optimizer or
MoE utility.

## 2. Protocol Compliance Audit

approved conditions match actual conditions: yes.

primary metric exists: yes, \(\Delta L_{\mathrm{tail}}\).

central figures/tables exist: yes.

seeds/checkpoints recorded: yes, 8 seeds.

known good/bad/confusing cases reviewed: yes, especially the A07_06-style
metric mismatch risk.

success/failure/insufficient-evidence criteria applied: yes.

## 3. Setup

Code workspace:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

Runner:
`active/synthetic_data_understanding/scripts/run_a07_nested_singular_interference.py`

Config:
`active/synthetic_data_understanding/configs/a07_nested_singular_interference.json`

Run name: `a07_nested_full_20260628_2`

Curated dir:
`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A07/A07_02_nested_tail_common_subspace_control`

Job id: local CUDA run, no ACP job.

## 4. Metrics And Decision Rules

Primary metric:

\[
\Delta L_{\mathrm{tail}}=
L_{\mathrm{tail}}(\mathrm{CE})-
L_{\mathrm{tail}}(\mathrm{combined}).
\]

Mechanism guard:

\[
\alpha_{\mathrm{tail}}=
\frac{\|P_Cu_{\mathrm{tail}}\|^2}{\|u_{\mathrm{tail}}\|^2+\epsilon}.
\]

Pass requires tail loss improvement, common loss within guard, and lower
\(\alpha_{\mathrm{tail}}\).

## 5. Main Results

Decision evidence:

| Condition | Tail loss | Tail acc | A loss | Tail improvement vs CE | Common regression | Alpha reduction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CE/AdamW | `0.3947` | `0.8806` | `0.0325` | `0.0000` | `0.0000` | `0.0000` |
| confidence gate only | `0.3242` | `0.8829` | `0.0600` | `0.0705` | `0.0275` | `-0.0171` |
| subspace suppression only | `0.3196` | `0.8896` | `0.0325` | `0.0751` | `0.0000` | `0.1153` |
| combined control | `0.2872` | `0.8933` | `0.0590` | `0.1075` | `0.0265` | `0.1204` |

Interpretation: confidence gating improves tail loss but does not reduce the
tail update fraction. Subspace suppression reduces the tail update fraction and
also improves tail loss. The combined condition gives the strongest tail loss
result.

## 6. Visualization Results

### Tail Control Results

![Tail control results](figures/a07_02_control_results.png)

Purpose: show whether functional tail loss and update-space mechanism guard
move together.

Setup: aggregate 8 seeds across the four post-warmup conditions.

How to read: lower tail loss and lower \(\alpha_{\mathrm{tail}}\) are better.

Observed result: combined control has lowest tail loss and lowest measured
tail update fraction.

Take-home: the common-subspace control target is meaningful on this controlled
surface.

Remaining uncertainty: the implementation is a minimal selected-block control,
not the full rigorous C3S-AdamW optimizer across transformer blocks.

What this figure does not prove: real-DCLM transfer, route utility, or semantic
experts.

Anchor update implication: A07_02 can be marked supported-controlled.

## 7. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| A07_01 import | pass rate `1.0` | passed | none | missing projector rival weakened |
| Tail loss | improvement `0.1075` | passed | none | no-functional-effect rival weakened |
| Common guard | regression `0.0265` | passed | none | common-erasure rival weakened |
| Update guard | alpha reduction `0.1204` | passed | none | pure-confidence-only explanation weakened |

Falsified physical prior: none on this surface.

Falsified mathematical model: none.

Falsified operationalization / proxy: none for selected-block update fraction.

Falsified implementation: none found.

Falsified metric: none.

Remaining rival explanations: result may depend on rank-one hidden model and
may not transfer to wide transformer blocks.

## 8. Full Experiment Record

Seeds: `20260628-20260635`.

Conditions: CE/AdamW, confidence gate only, subspace suppression only,
combined gate and suppression.

Warmup: `240` steps.

Post-warmup: `420` steps.

Suppression strength: `0.7`.

Confidence threshold: `0.9`.

Common cap weight: `0.05`.

## 9. Interpretation

This result explains what A07_06 could not cleanly separate. In A07_06, rare
loss improved but routing-weighted conflict barely moved. Here, the mechanism
guard is update-space concentration itself: \(\alpha_{\mathrm{tail}}\) falls when
tail loss improves. Therefore the new mainline should treat update-space
common-subspace control as the cleaner mechanism target, while routing remains
a later utility question.

## 10. Claim Boundary

Can claim: common-subspace update control reduces tail loss on the controlled
rank-one nested surface.

Cannot claim: full C3S, wide-transformer behavior, real-DCLM transfer, or MoE
utility.

## 11. Next Decision

Use the result to motivate a 06-preservation-compatible control target: preserve
route partitions first, then test whether the preserved partition reduces
update-space tail absorption.

## 12. Links And Artifact Map

anchor:
`../../../problem_anchors/07_features_overlap/07_02_common_controlled_rare_interference_anchor.md`

protocol: `protocol.md`

summary: `summary.md`

code workspace:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

runner:
`active/synthetic_data_understanding/scripts/run_a07_nested_singular_interference.py`

config:
`active/synthetic_data_understanding/configs/a07_nested_singular_interference.json`

data / manifest:
generated in-memory from config.

result dir:
`active/synthetic_data_understanding/results/a07_nested_singular_interference/a07_nested_full_20260628_2`

figure dir: `figures/`

key tables:
`tables/a07_02_aggregate.csv`, `tables/a07_02_summary.csv`

logs / checkpoints: no persistent checkpoints.

repro command: see A07_01 detailed setup.

job id: local run.
