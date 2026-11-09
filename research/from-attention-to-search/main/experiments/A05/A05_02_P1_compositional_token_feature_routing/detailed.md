# Detailed Result: A05_02_P1_compositional_token_feature_routing

Anchor: `../../../problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

Story: P1 tests whether route axis follows target rule under compositional tokens.

## 0. Quick Recap

Purpose: relax the single-feature-token assumption.

Hypothesis: C1 routes by \(S1\), C2 routes by \(S2\), and C3 routes by \((S1,S2)\) if ordinary top-1 follows the target-relevant feature.

Experiment logic: use the same input format while changing only the target rule; record routing at the \(B_i\) position, immediately before target prediction.

Conclusion: P1 is negative or bounded. All targets are learned, but C1/C2 mostly collapse. C3-B0 is the only interpretable positive clue.

Evidence: `tables/summary_by_condition.csv`, `tables/summary_by_seed.csv`, route matrices, load tables, collapse timing tables, and figures in `figures/`.

## 1. Anchor Link And Decision Point

Anchor: `../../../problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

Parent question: does route consistency remain meaningful after relaxing the minimal baseline assumptions?

This experiment updates: the compositional-token branch of 05_02. It weakens robust target-rule-dependent routing under ordinary top-1.

## 2. Purpose

P1 asks whether a router can select the target-relevant feature when one routed context contains multiple candidate features.

## 3. Hypothesis And Rival Explanations

Hypothesis: the dominant route axis follows the target rule.

Rival explanation 1: the router follows a fixed surface axis or nuisance token.

Rival explanation 2: route consistency is produced by collapse, not feature selection.

Rival explanation 3: target learning is solved by shared model components while MoE routing remains arbitrary.

## 4. Experiment Logic

Input format:

\[
x=[r_{\mathrm{start}},S1,S1,S1,S2,S2,S2,B_i,Y,r_{\mathrm{end}}]
\]

Cases:

- C1: target depends on \(S1\).
- C2: target depends on \(S2\).
- C3: target depends on \((S1,S2)\).

Conditions:

- B0: no inhibition.
- I1: true token-conditioned inhibition comparison.

Primary route-axis metric: normalized mutual information between route and \(S1\), \(S2\), \(B_i\), and \((S1,S2)\).

Validity guard: target accuracy must be high and route load must not collapse.

## 5. Setup

Code workspace: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

Runner: `active/synthetic_data_understanding/scripts/run_h0605bc_feature_assumption_relaxation.py`

Config: `active/synthetic_data_understanding/configs/h0605b_compositional_token_feature_routing.json`

Training: standard full-sequence next-token prediction, 1200 steps, batch size 384, learning rate 0.0008, weight decay 0.01.

Model: tiny Transformer with one top-1 selected-gate MoE FFN, 4 experts, \(d_{\mathrm{model}}=128\), FFN dimension 256.

Seeds: `20260521`, `20260522`, `20260523`.

Actual hardware: 2 visible H100 GPUs; no ACP/SCO job id.

## 6. Primary Metric And Decision Rule

Primary metric: route-axis NMI after passing load and accuracy guards.

Success: C1 highest valid NMI with \(S1\), C2 with \(S2\), and C3 with \((S1,S2)\) across seeds.

Failure: target accuracy is high but route load collapses, or routing does not follow the target rule.

Insufficient evidence: target accuracy fails or only collapsed conditions show route-axis alignment.

## 7. Main Result

Condition-level table:

| Case | Cond. | Acc. | Entropy | Max load | Active | NMI S1 | NMI S2 | NMI B | NMI S1S2 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C1 | B0 | 1.000 | 0.135 | 0.917 | 1.33 | 0.212 | 0.000 | 0.000 | 0.150 |
| C1 | I1 | 1.000 | 0.135 | 0.917 | 1.33 | 0.212 | 0.000 | 0.000 | 0.150 |
| C2 | B0 | 1.000 | 0.135 | 0.917 | 1.33 | 0.000 | 0.212 | 0.000 | 0.150 |
| C2 | I1 | 1.000 | 0.000 | 1.000 | 1.00 | 0.000 | 0.000 | 0.000 | 0.000 |
| C3 | B0 | 1.000 | 0.574 | 0.686 | 3.00 | 0.430 | 0.183 | 0.000 | 0.528 |
| C3 | I1 | 1.000 | 0.102 | 0.964 | 1.67 | 0.099 | 0.099 | 0.005 | 0.168 |

Interpretation: C1/C2 are invalidated by collapse. C3-B0 remains a narrow positive clue because it has multi-expert load and highest NMI with the compositional axis.

## 8. Key Figures

![B0 target-rule route-axis NMI](figures/B0_target_rule_route_axis_nmi.png)

Supports: B0 has a readable C3 compositional signal, but C1/C2 are collapse-contaminated.

![I1 target-rule route-axis NMI](figures/I1_target_rule_route_axis_nmi.png)

Supports: I1 does not provide a valid repair.

![C1 target-relevant feature x expert heatmap](figures/C1_target_relevant_feature_expert_heatmap.png)

Supports: C1 alignment is seed-local and mostly collapse-contaminated.

![C2 target-relevant feature x expert heatmap](figures/C2_target_relevant_feature_expert_heatmap.png)

Supports: C2 mirrors the C1 failure.

![C3 target-relevant feature x expert heatmap](figures/C3_target_relevant_feature_expert_heatmap.png)

Supports: C3-B0 is the only route-axis clue worth preserving.

![Expert load histogram](figures/expert_load_histogram.png)

Supports: load guard is the deciding validity metric.

![C1/C2 route load over checkpoints](figures/collapse_route_load_over_checkpoints_C1_C2.png)

Supports: C1/C2 collapse is established by step 200 in final-collapsed runs.

## 9. Evidence Walkthrough

### 9.1 Condition-Level Evidence

All six condition groups reach target accuracy 1.000. Therefore the negative result is a routing-validity failure, not a task-learning failure.

C1 and C2 have mean max-load 0.917 or 1.000 and active experts 1.33 or 1.00. Their route-axis NMI cannot be promoted to evidence of target-rule routing.

C3-B0 has mean active experts 3.00 and mean max-load 0.686. Its NMI with \((S1,S2)\) is 0.528, higher than with \(S1\) at 0.430, \(S2\) at 0.183, and \(B_i\) at 0.000.

### 9.2 Seed-Level Evidence

Seed-level records are stored in `tables/summary_by_seed.csv`.

Important pattern: C1/C2 have one non-collapsed-ish seed (`20260523`) that aligns with the target axis, but two seeds collapse. This is not seed-stable positive evidence.

C3-B0 seed summary:

| Seed | Acc. | Entropy | Max load | Active | NMI S1 | NMI S2 | NMI B | NMI S1S2 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20260521 | 1.000 | 0.712 | 0.625 | 4 | 0.603 | 0.187 | 0.000 | 0.597 |
| 20260522 | 1.000 | 0.409 | 0.745 | 2 | 0.317 | 0.122 | 0.000 | 0.439 |
| 20260523 | 1.000 | 0.600 | 0.688 | 3 | 0.371 | 0.240 | 0.000 | 0.548 |

Interpretation: C3-B0 is not perfect, but it is the only condition where a route-axis claim can be read.

### 9.3 Collapse Timing Diagnostic

Collapse definition: eval route max-load fraction \(\ge 0.95\) at the \(B_i\) route position.

Timing result for C1/C2:

- 12 C1/C2 runs total.
- 9 of 12 are final collapsed.
- 0 of 12 are collapsed at step 0.
- 9 of 9 final-collapsed runs first cross the collapse threshold by step 200.
- 9 of 9 final-collapsed runs have the same dominant expert at step 200 and final.
- Only 3 of 9 final-collapsed runs have the same dominant expert at step 0 and final.

Interpretation: P1 C1/C2 collapse is early-training lock-in, not initialization hard collapse and not late-stage drift.

## 10. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / Failed / Unclear | Failure Reason | What This Rules Out |
|---|---|---|---|---|
| Target learning | all condition groups acc. 1.000 | Passed | none | task failure is not the explanation |
| Load validity | C1/C2 max-load 0.917 to 1.000 | Failed for C1/C2 | route collapse | C1/C2 NMI cannot be interpreted positively |
| C3-B0 route axis | NMI S1S2 highest with multi-expert load | Partial pass | still moderately concentrated | keeps only a weak compositional clue |
| I1 comparison | I1 collapses C2 and near-collapses C3 | Failed | concentration increases | I1 is not a P1 repair |
| Timing diagnostic | collapse by step 200 | Passed | none | rules out late-only collapse |

Falsified physical prior: target-relevant routing is not guaranteed by target learnability.

Remaining rival explanations: C3-B0 may be a real compositional signal, but it needs anti-lock-in replication.

## 11. Goal / Metric Audit

Trigger: C1/C2 show perfect target accuracy but invalid routing.

Old metric risk: route NMI can look meaningful even when one expert dominates.

Revised metric order: target accuracy first as a validity guard, then max-load/entropy/active experts, then route-axis NMI.

## 12. Full Experiment Record

Command:

```bash
python active/synthetic_data_understanding/scripts/run_h0605bc_feature_assumption_relaxation.py \
  --experiment p1 \
  --config active/synthetic_data_understanding/configs/h0605b_compositional_token_feature_routing.json \
  --run-name h0605b_compositional_token_feature_routing_full_20260604 \
  --run-stage full \
  --max-parallel 2
```

Full tables:

- `tables/summary_by_condition.csv`
- `tables/summary_by_seed.csv`
- `tables/route_matrix_by_seed.csv`
- `tables/expert_load_by_seed.csv`
- `tables/collapse_route_load_trajectory.csv`
- `tables/collapse_timing_by_seed.csv`

Figures:

- `figures/B0_target_rule_route_axis_nmi.png`
- `figures/I1_target_rule_route_axis_nmi.png`
- `figures/C1_target_relevant_feature_expert_heatmap.png`
- `figures/C2_target_relevant_feature_expert_heatmap.png`
- `figures/C3_target_relevant_feature_expert_heatmap.png`
- `figures/expert_load_histogram.png`
- `figures/collapse_route_load_over_checkpoints_C1_C2.png`

## 13. Interpretation

P1 should be reported as a negative or bounded result. The key comparison is not "accuracy succeeds" but "routing remains valid enough to interpret." C1/C2 fail that guard. C3-B0 remains useful only as a clue that compositional utility can sometimes align route axis when load does not collapse.

## 14. Claim Boundary

Can claim:

- P1 target tasks are learnable.
- Ordinary top-1 does not robustly follow the target-relevant feature under P1.
- C3-B0 provides a weak, non-collapsed-ish compositional route-axis clue.
- C1/C2 collapse occurs during early training by step 200.

Cannot claim:

- Ordinary top-1 gives robust compositional feature routing.
- I1 is a successful repair.
- C3-B0 is expert utility specialization.
- The timing diagnostic identifies the exact gradient-level cause.

## 15. Next Decision

Park P1 as bounded evidence unless the next test directly targets early lock-in. A future P1 rerun must include a load guard and report seed-level trajectories before route-axis NMI is interpreted.

## 16. Links And Artifact Map

anchor: `../../../problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

summary: `summary.md`

code workspace: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

runner: `active/synthetic_data_understanding/scripts/run_h0605bc_feature_assumption_relaxation.py`

config: `active/synthetic_data_understanding/configs/h0605b_compositional_token_feature_routing.json`

result dir: `.../results/h0605b_compositional_token_feature_routing/h0605b_compositional_token_feature_routing_full_20260604/`

figure dir: `figures/`

key tables: all `tables/*.csv`

logs / checkpoints: local full run; no ACP/SCO job id.
