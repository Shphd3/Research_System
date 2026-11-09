# Detailed Result: A05_01_uniform_feature_collapse_mechanism_audit

Anchor: `../../../problem_anchors/05_failure_mechanism/05_01_geometric_inhibition_anchor.md`

Story: checkpoint-level audit of whether uniform-feature route collapse is initialized early, amplified during early top-1 training, or appears late.

## 0. Quick Recap

Purpose: audit collapse in the original pre-relaxation uniform feature experiment before using inhibition, P1/P3 relaxation, or route-utility binding as main evidence.

Hypothesis: final collapsed runs should show an early dominant expert and growing top-1 margin if collapse is early-geometry dominated and training-amplified.

Experiment logic: use all available baseline and inhibition seeds, prioritize checkpoints 0, 10, 20, 50, 100, and final, and measure route load, feature assignment, hidden-router cosine, top-1 margin, common-direction alignment, and router geometry.

Conclusion: final judgment is **A. Early-geometry dominated collapse**, with a secondary common-direction clue. Final collapsed runs have the final dominant expert at step 0 in 9/9 runs; top-1 margins grow strongly during training.

Evidence: `tables/audit_collapse_timing_by_seed.csv`, `tables/audit_top1_margin_by_checkpoint.csv`, `tables/audit_common_direction_alignment.csv`, and the figures in `figures/`.

## 1. Anchor Link And Decision Point

Anchor: `../../../problem_anchors/05_failure_mechanism/05_01_geometric_inhibition_anchor.md`

Parent question: can inhibition stabilize useful feature-level routing, or does the current top-1 system lock into collapse before useful routing can be interpreted?

This experiment updates: the collapse mechanism boundary for 05_01. It says the next move should be anti-lock-in control, not a direct move from inhibition to utility binding.

## 2. Purpose

The audit answers three concrete questions:

1. Does collapse appear at step 0, early training, or late training?
2. Are collapsed seeds already assigned to the final dominant expert early?
3. Is the final collapse expert aligned more with a common hidden direction than with feature-specific residual directions?

## 3. Hypothesis And Rival Explanations

Hypothesis: early hidden-router geometry selects a dominant expert, and top-1 training amplifies that expert into near-single-expert routing.

Rival explanation 1: collapse is purely late training drift. This would predict balanced early routing and a dominant expert that appears only late.

Rival explanation 2: collapse is target-learning failure. This would predict low target accuracy or unstable task learning in collapsed runs.

Rival explanation 3: collapse is utility-correct specialization. This cannot be decided here because forced-routing utility was not recomputed in this audit.

## 4. Experiment Logic

Operational feature: exact feature `(slot, B_i)` when available, plus slot-aggregated views for readable heatmaps.

Route load of expert \(e\): fraction of pre-target routed tokens assigned to expert \(e\).

Collapse guard: high max-load fraction, low normalized load entropy, and low active-expert count. The report keeps raw values instead of hiding the threshold.

Common direction:

\[
c(t)=\mathrm{normalize}\left(\frac{1}{|F|}\sum_f h_f(t)\right)
\]

Feature residual:

\[
r_f(t)=h_f(t)-\frac{h_f(t)^T c(t)}{\|c(t)\|_2^2}c(t)
\]

The key mechanism check is whether the final collapse expert has high early route load, high cosine with \(c(t)\), and increasing top-1 margin.

## 5. Setup

Data: original uniform feature setting from `A05_01_true_token_conditioned_inhibition_replay`.

Conditions: `R0-dot`, `R0-cos`, `R1-dot`, `R1-cos`, `S0-dot`, `S0-cos`, `S1-dot`, `S1-cos`.

Seeds: `20260521`, `20260522`, `20260523`.

Checkpoints: step 0, 10, 20, 50, 100, 200, 800, and 1600 or final where available.

Runner: `scripts/audit_uniform_feature_collapse.py`

Result artifacts: `tables/` and `figures/` inside this experiment folder.

## 6. Primary Metric And Decision Rule

Primary metric: per-seed max-load fraction over checkpoints. This metric decides whether routing is valid before interpreting feature structure.

Decision rule:

- Early-geometry dominated collapse: final collapsed seeds already show the final dominant expert at step 0 to early checkpoints, and training increases margin/load.
- Training-amplified lock-in: early routing is not fully collapsed but load and margin concentrate during training.
- Common-direction collapse clue: final collapse expert aligns more with the common hidden direction than with residual feature directions.
- Insufficient evidence: early checkpoints or hidden/router states are missing and cannot be recovered.

## 7. Main Result

Final judgment: **A. Early-geometry dominated collapse**, with training-amplified lock-in and a common-direction clue.

Collapsed run count: 9 final-collapsed condition-seeds out of 24.

First collapsed checkpoint among final-collapsed runs:

| First collapsed step | Count |
|---:|---:|
| 10 | 4 |
| 20 | 3 |
| 100 | 2 |

Dominant expert agreement among final-collapsed runs:

| Checkpoint | Fraction matching final dominant expert |
|---|---:|
| step 0 | 1.000 |
| step 10 | 0.667 |
| step 20 | 0.222 |
| step 50 | 1.000 |
| step 100 | 1.000 |

Interpretation: the final expert is visible at initialization in all final-collapsed runs, even though some runs briefly switch at steps 10 or 20 before returning to the final expert by step 50.

## 8. Key Figures

![Collapse load timeline by seed and condition](figures/collapse_load_timeline_by_seed_condition.png)

Supports: route load must be inspected by seed and condition; averages hide transient collapse and recovery.

![Feature-to-expert assignment timeline](figures/feature_expert_assignment_timeline.png)

Supports: the same final collapse experts absorb broad feature groups rather than separating exact feature identities.

![Feature-router cosine timeline](figures/feature_router_cosine_timeline.png)

Supports: hidden-router geometry changes before and during route concentration.

![Top-1 margin dynamics](figures/top1_margin_dynamics.png)

Supports: margin growth is a training-amplification signature.

![Common-direction alignment](figures/common_direction_alignment.png)

Supports: final collapse experts increasingly align with the shared hidden direction.

![Router geometry timeline](figures/router_geometry_timeline.png)

Supports: collapse is not simply all router vectors merging into one vector.

![Seed-level load, margin, and common-direction contrast](figures/evidence_s1cos_seed_contrast_load_margin_common.png)

Supports: selected seeds show the contrast between collapse, recovery, and non-collapsed behavior.

![Cross-condition lock-in for seed 20260522](figures/evidence_seed20260522_cross_condition_lockin.png)

Supports: the same seed can repeatedly lock in across related conditions, showing that seed-level geometry matters.

## 9. Evidence Walkthrough

### 9.1 Collapse Timeline

Final-collapsed seed table:

| Condition | Seed | First collapsed step | Final expert | Step0 max | Step10 max | Step20 max | Step50 max | Step100 max | Final max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R0-dot | 20260522 | 20 | E0 | 0.694 | 0.796 | 0.992 | 0.791 | 0.955 | 1.000 |
| R1-cos | 20260521 | 100 | E3 | 0.681 | 0.503 | 0.887 | 0.848 | 1.000 | 1.000 |
| R1-cos | 20260522 | 20 | E0 | 0.685 | 0.810 | 0.993 | 0.863 | 1.000 | 1.000 |
| R1-dot | 20260521 | 100 | E3 | 0.681 | 0.599 | 0.882 | 0.925 | 1.000 | 1.000 |
| R1-dot | 20260522 | 20 | E0 | 0.694 | 0.770 | 0.992 | 0.963 | 1.000 | 1.000 |
| S0-cos | 20260522 | 10 | E3 | 0.889 | 0.968 | 0.896 | 0.911 | 0.998 | 1.000 |
| S0-dot | 20260522 | 10 | E3 | 0.889 | 0.981 | 0.990 | 0.978 | 0.987 | 0.972 |
| S1-cos | 20260522 | 10 | E3 | 0.889 | 0.976 | 0.872 | 0.992 | 1.000 | 1.000 |
| S1-dot | 20260522 | 10 | E3 | 0.889 | 0.991 | 0.999 | 1.000 | 1.000 | 1.000 |

Observation: collapsed runs start with high but not always threshold-level max-load. Training turns this into hard collapse.

Boundary: 3 non-final-collapsed runs show transient early collapse and later recovery, so an early threshold crossing alone is not sufficient for final collapse.

### 9.2 Feature-To-Expert Assignment Timeline

Heatmaps are slot-aggregated for readability; exact `(slot, B_i)` tables are preserved in `tables/audit_slot_assignment_by_checkpoint.csv` and `tables/audit_slot_main_expert_feature_fraction.csv`.

Interpretation: final collapsed runs route broad feature sets to one expert. This invalidates same-feature consistency as a positive metric unless load is also valid.

### 9.3 Feature-Centroid And Router-Vector Cosine

Cosine tables are stored in `tables/audit_slot_router_cosine_by_checkpoint.csv`.

Observation: final collapsed runs show early cosine preference for the final expert, followed by stronger alignment during training.

Interpretation: the final selected expert is not chosen late from an initially balanced geometry.

### 9.4 Top-1 Margin Dynamics

Average top-1 margin and final-dominant agreement:

| Final collapsed | Step | Mean top1 margin | Fraction top1 equals final expert |
|---:|---:|---:|---:|
| 0 | 0 | 0.061 | 0.435 |
| 0 | 50 | 0.139 | 0.560 |
| 0 | 100 | 0.297 | 0.612 |
| 0 | 1600 | 0.545 | 0.592 |
| 1 | 0 | 0.078 | 0.776 |
| 1 | 50 | 0.187 | 0.922 |
| 1 | 100 | 0.462 | 0.992 |
| 1 | 1600 | 0.797 | 0.997 |

Interpretation: collapsed runs already have higher final-expert agreement at step 0, and training turns this into near-universal final-expert assignment.

### 9.5 Common-Direction Alignment

Final-expert alignment averages:

| Group | Step | Common-direction cosine | Residual absolute cosine mean |
|---|---:|---:|---:|
| Final collapsed | 0 | 0.148 | 0.063 |
| Final collapsed | 50 | 0.308 | 0.070 |
| Final collapsed | 100 | 0.609 | 0.052 |
| Final collapsed | 1600 | 0.873 | 0.029 |
| Not final collapsed | 0 | 0.092 | 0.063 |
| Not final collapsed | 50 | 0.192 | 0.115 |
| Not final collapsed | 100 | 0.360 | 0.136 |
| Not final collapsed | 1600 | 0.553 | 0.236 |

Interpretation: in collapsed runs, the final expert increasingly aligns with the shared hidden direction while residual-feature alignment stays small. This supports the common-direction clue but not a complete causal proof.

### 9.6 Router Vector Geometry

Router geometry tables are stored in `tables/audit_router_vector_geometry.csv` and `tables/audit_router_pairwise_cosine.csv`.

Observation: collapse is not best described as all router vectors merging. The selected expert vector moves and aligns with the common hidden direction; unselected experts do not all become identical.

Interpretation: the safer phrase is not "all router vectors collapse together." It is: the final selected expert becomes an attractor for the shared hidden direction.

### 9.7 Forced-Routing Utility

Forced-routing utility was intentionally not recomputed in this A05_01 audit.

Boundary: do not claim the selected expert is utility-wrong from this report. That question is addressed later in A05_03 P7 after intervention runs.

## 10. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / Failed / Unclear | Failure Reason | What This Rules Out |
|---|---|---|---|---|
| Checkpoint availability | Existing checkpoints plus same-config replay for missing early states | Partial | original step 10/20/50 model states were missing | rules out treating early replay as byte-identical original evidence |
| Route load timeline | `audit_load_by_checkpoint.csv` and load figure | Passed | none | rules out late-only collapse |
| Assignment heatmaps | slot-level and exact-feature tables | Passed | exact feature heatmap too large for one figure | rules out judging by averages only |
| Hidden-router cosine | cosine tables and heatmaps | Passed | cosine is correlational | supports early-geometry mechanism but not causality |
| Common direction | common-direction and residual tables | Passed | no intervention here | supports common-direction clue but not sufficiency |
| Forced utility | not run | Unclear | outside scope | utility mismatch remains unclaimed |

Falsified physical prior: "uniform feature frequency alone prevents route collapse" is weakened.

Falsified operationalization / proxy: same-feature consistency is not a valid specialization proxy without load and composition guards.

Remaining rival explanations: common direction may be causal, but utility co-adaptation or gradient dynamics may also participate.

## 11. Goal / Metric Audit

Trigger: collapse made route consistency uninterpretable in A05_01 and A05_02.

Old goal / metric: high same-feature consistency.

Repeated failure pattern: consistency can be perfect under one-expert collapse.

Downstream decision: future experiments must treat final max-load, active experts, load entropy, and seed-level timelines as validity guards before interpreting NMI or purity.

Revised goal / metric: first prevent or explain collapse; only then interpret feature structure or utility binding.

Errors now acceptable: a method can reduce consistency if it prevents collapse and preserves target accuracy.

Errors still harmful: high accuracy with one expert absorbing all features remains invalid for specialization.

## 12. Full Experiment Record

Full tables:

- `tables/audit_collapse_timing_by_seed.csv`
- `tables/audit_load_by_checkpoint.csv`
- `tables/audit_slot_assignment_by_checkpoint.csv`
- `tables/audit_slot_main_expert_feature_fraction.csv`
- `tables/audit_slot_router_cosine_by_checkpoint.csv`
- `tables/audit_top1_margin_by_checkpoint.csv`
- `tables/audit_common_direction_alignment.csv`
- `tables/audit_slot_residual_alignment.csv`
- `tables/audit_router_vector_geometry.csv`
- `tables/audit_router_pairwise_cosine.csv`
- `tables/existing_checkpoint_coverage.csv`

Figures:

- `figures/collapse_load_timeline_by_seed_condition.png`
- `figures/feature_expert_assignment_timeline.png`
- `figures/feature_router_cosine_timeline.png`
- `figures/top1_margin_dynamics.png`
- `figures/common_direction_alignment.png`
- `figures/router_geometry_timeline.png`
- `figures/evidence_s1cos_seed_contrast_load_margin_common.png`
- `figures/evidence_seed20260522_cross_condition_lockin.png`
- `figures/evidence_s1cos_assignment_cosine_contrast.png`
- `figures/evidence_s1cos_router_geometry_contrast.png`
- `figures/router_pairwise_cosine_key_conditions.png`

## 13. Interpretation

Question 1 answer: collapse is early-training lock-in seeded by initialization geometry. It is not purely step-0 hard collapse, and it is not late drift.

Question 2 answer: the final dominant expert is already visible at step 0 in all final-collapsed runs, but training amplifies the margin and makes the assignment nearly deterministic.

Question 3 answer: the common hidden direction is a plausible mechanism clue because the final expert aligns with it more strongly over training, while residual alignment stays smaller in collapsed runs.

Question 4 answer: router vectors do not simply merge. The selected expert becomes more aligned with the common direction; this is a selected-vector attraction pattern, not an all-vector merge pattern.

## 14. Claim Boundary

Can claim:

- Final collapsed runs in this audit are early-geometry dominated.
- Top-1 training amplifies early expert preference into high margin and near-single-expert load.
- Common-direction alignment is a strong mechanism clue.
- Collapse is not explained by target-learning failure.

Cannot claim:

- The common direction is the only cause.
- Collapse is solved.
- The selected expert is utility-wrong.
- The replayed early checkpoints are byte-identical to the original missing checkpoints.
- Feature-level specialization exists in collapsed runs.

## 15. Next Decision

Run a minimal anti-lock-in intervention on the original uniform setting. The decision metric should be final max-load and collapse rate under high target accuracy, with seed-level timelines retained.

## 16. Links And Artifact Map

anchor: `../../../problem_anchors/05_failure_mechanism/05_01_geometric_inhibition_anchor.md`

summary: `summary.md`

code workspace: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

runner: `scripts/audit_uniform_feature_collapse.py`

config: original `A05_01_true_token_conditioned_inhibition_replay` configs and same-config diagnostic replay.

key code files: `scripts/audit_uniform_feature_collapse.py`

data / manifest: existing checkpoint coverage in `tables/existing_checkpoint_coverage.csv`

result dir: this experiment folder.

figure dir: `figures/`

key tables: all `tables/audit_*.csv`

logs / checkpoints: original early checkpoints were incomplete; missing early states were reconstructed by same-config diagnostic replay where required.

repro command:

```bash
python main/experiments/A05/A05_01_uniform_feature_collapse_mechanism_audit/scripts/audit_uniform_feature_collapse.py
```
