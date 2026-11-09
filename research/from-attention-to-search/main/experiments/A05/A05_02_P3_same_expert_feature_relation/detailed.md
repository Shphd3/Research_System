# Detailed Result: A05_02_P3_same_expert_feature_relation

Anchor: `../../../problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

Story: P3 tests whether same-expert features share family structure under a controlled many-feature setup.

## 0. Quick Recap

Purpose: test whether many-to-one expert assignment is structured rather than arbitrary.

Hypothesis: P3a positive would mean input family alone can induce grouping. P3b stronger than P3a would mean shared family-level target utility helps induce grouping.

Experiment logic: use \(G=4\) families, \(K=4\) features per family, \(F=16\) total features, and \(E=4\) experts. Compare actual family purity against a load-matched random baseline.

Conclusion: P3a/P3b are not positive. Shared family target utility does not reliably increase grouping.

Evidence: all condition groups reach target accuracy 1.000, but mean family-purity deltas are only 0.047 to 0.090 and are seed-unstable.

## 1. Anchor Link And Decision Point

Anchor: `../../../problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

Parent question: when multiple features share experts, is the grouping meaningful?

This experiment updates: the same-expert relation branch of 05_02. It weakens ordinary top-1 family grouping.

## 2. Purpose

P3 asks whether same-expert features are related, not merely whether each feature has a consistent route.

## 3. Hypothesis And Rival Explanations

Hypothesis: same-family features should share experts more than a load-matched random grouping, especially when they also share the same target.

Rival explanation 1: same-expert features are arbitrary early-locked buckets.

Rival explanation 2: apparent family purity comes from load concentration or one lucky seed.

Rival explanation 3: target accuracy is solved without family-structured routing.

## 4. Experiment Logic

Data:

\[
g \in \{1,\ldots,4\}, \quad k \in \{1,\ldots,4\}, \quad f=(g,k)
\]

P3a sequence:

\[
x=[r_{\mathrm{start}},G_{g1},G_{g2},G_{g3},F_{gk1},F_{gk2},F_{gk3},Y_{gk},r_{\mathrm{end}}]
\]

P3a target: feature-level \(Y_{gk}\).

P3b sequence:

\[
x=[r_{\mathrm{start}},G_{g1},G_{g2},G_{g3},F_{gk1},F_{gk2},F_{gk3},Y_g,r_{\mathrm{end}}]
\]

P3b target: family-level \(Y_g\) shared by all features in family \(g\).

Route position: the last \(F_{gk}\) token, immediately before the target.

## 5. Setup

Code workspace: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

Runner: `active/synthetic_data_understanding/scripts/run_h0605bc_feature_assumption_relaxation.py`

Config: `active/synthetic_data_understanding/configs/h0605c_same_expert_feature_relation.json`

Training: standard full-sequence next-token prediction, 1200 steps, batch size 384, learning rate 0.0008, weight decay 0.01.

Model: tiny Transformer with one top-1 selected-gate MoE FFN, 4 experts, \(d_{\mathrm{model}}=128\), FFN dimension 256.

Seeds: `20260521`, `20260522`, `20260523`.

Conditions: B0 no inhibition; I1 true token-conditioned inhibition comparison.

Actual hardware: 2 visible H100 GPUs; no ACP/SCO job id.

## 6. Primary Metric And Decision Rule

Primary metric:

\[
\Delta_{\mathrm{family}}=\mathrm{Purity}_{actual}-\mathrm{Purity}_{load\ matched\ random}
\]

Success: P3a has seed-stable positive \(\Delta_{\mathrm{family}}\), and P3b is stronger than P3a under non-collapse.

Failure: deltas are small, within random variation, driven by one seed, or collapse-contaminated.

Insufficient evidence: target accuracy fails or route load is too collapsed to interpret.

## 7. Main Result

Condition-level result:

| Case | Cond. | Acc. | Entropy | Max load | Active | NMI family | NMI feature | Actual purity | Random mean | Delta |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P3a | B0 | 1.000 | 0.666 | 0.563 | 3.00 | 0.282 | 0.569 | 0.479 | 0.424 | 0.055 |
| P3a | I1 | 1.000 | 0.611 | 0.646 | 3.00 | 0.286 | 0.543 | 0.458 | 0.411 | 0.047 |
| P3b | B0 | 1.000 | 0.446 | 0.729 | 2.67 | 0.319 | 0.379 | 0.458 | 0.372 | 0.087 |
| P3b | I1 | 1.000 | 0.301 | 0.792 | 2.00 | 0.237 | 0.224 | 0.417 | 0.327 | 0.090 |

Interpretation: P3b has a slightly larger mean delta, but it also has stronger concentration and does not produce seed-stable grouping. This is not positive evidence.

## 8. Key Figures

![Family purity vs load-matched random](figures/family_purity_vs_load_matched_random.png)

Supports: the main metric is small and unstable.

![P3a expert x feature heatmap](figures/P3a_expert_feature_heatmap.png)

Supports: P3a input-family structure alone is not enough.

![P3b expert x feature heatmap](figures/P3b_expert_feature_heatmap.png)

Supports: P3b does not reliably translate shared target into family grouping.

![P3a expert x family composition heatmap](figures/P3a_expert_family_composition_heatmap.png)

Supports: P3a family composition is mixed.

![P3b expert x family composition heatmap](figures/P3b_expert_family_composition_heatmap.png)

Supports: P3b apparent grouping is not stable enough to claim.

![Expert load histogram](figures/expert_load_histogram.png)

Supports: load concentration remains a validity concern.

![Target accuracy table](figures/target_accuracy_table.png)

Supports: negative grouping is not a target-learning failure.

## 9. Evidence Walkthrough

### 9.1 Condition-Level Evidence

All condition groups have target accuracy 1.000. The result is therefore a routing-structure failure, not a task-learning failure.

The mean family-purity delta is small:

- P3a-B0: 0.055.
- P3a-I1: 0.047.
- P3b-B0: 0.087.
- P3b-I1: 0.090.

### 9.2 Seed-Level Family Relation

| Case | Cond. | Seed | Actual purity | Random mean | Delta | Random 2.5% | Random 97.5% |
|---|---|---:|---:|---:|---:|---:|---:|
| P3a | B0 | 20260521 | 0.500 | 0.413 | 0.087 | 0.312 | 0.500 |
| P3a | B0 | 20260522 | 0.625 | 0.485 | 0.140 | 0.375 | 0.625 |
| P3a | B0 | 20260523 | 0.312 | 0.375 | -0.062 | 0.312 | 0.438 |
| P3a | I1 | 20260521 | 0.562 | 0.402 | 0.160 | 0.312 | 0.500 |
| P3a | I1 | 20260522 | 0.500 | 0.483 | 0.017 | 0.375 | 0.625 |
| P3a | I1 | 20260523 | 0.312 | 0.350 | -0.037 | 0.312 | 0.438 |
| P3b | B0 | 20260521 | 0.250 | 0.250 | 0.000 | 0.250 | 0.250 |
| P3b | B0 | 20260522 | 0.750 | 0.479 | 0.271 | 0.375 | 0.625 |
| P3b | B0 | 20260523 | 0.375 | 0.387 | -0.012 | 0.375 | 0.438 |
| P3b | I1 | 20260521 | 0.250 | 0.250 | 0.000 | 0.250 | 0.250 |
| P3b | I1 | 20260522 | 0.750 | 0.481 | 0.269 | 0.375 | 0.625 |
| P3b | I1 | 20260523 | 0.250 | 0.250 | 0.000 | 0.250 | 0.250 |

Interpretation: the positive-looking P3b mean is mainly seed `20260522`; other seeds are zero, near zero, or negative. This is not seed-stable evidence.

### 9.3 Load Boundary

P3b has higher max-load than P3a:

- P3a-B0 max-load: 0.563.
- P3a-I1 max-load: 0.646.
- P3b-B0 max-load: 0.729.
- P3b-I1 max-load: 0.792.

Interpretation: P3b's small mean delta comes with stronger concentration, so it should not be upgraded to a structural grouping claim.

## 10. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / Failed / Unclear | Failure Reason | What This Rules Out |
|---|---|---|---|---|
| Target learning | acc. 1.000 in all groups | Passed | none | target failure |
| Input-family-only grouping | P3a small deltas and one negative seed | Failed | not seed-stable | input family alone is insufficient here |
| Shared family target | P3b small mean gain driven by one seed | Failed | seed instability and concentration | shared target utility alone is insufficient here |
| Inhibition comparison | I1 does not improve structure | Failed | load concentration remains | I1 as repair |
| Random baseline | load-matched comparison included | Passed | none | raw purity inflation by load alone |

Falsified physical prior: shared family target utility is not sufficient to induce reliable ordinary top-1 family grouping.

Remaining rival explanations: a stronger anti-collapse or utility-binding intervention may still create grouping.

## 11. Goal / Metric Audit

Trigger: same-feature consistency cannot answer whether same-expert features are related.

Old metric risk: consistency ignores what else enters the same expert.

Revised metric: compare actual same-expert family composition with a load-matched random baseline, by seed and condition.

## 12. Full Experiment Record

Command:

```bash
python active/synthetic_data_understanding/scripts/run_h0605bc_feature_assumption_relaxation.py \
  --experiment p3 \
  --config active/synthetic_data_understanding/configs/h0605c_same_expert_feature_relation.json \
  --run-name h0605c_same_expert_feature_relation_full_20260604 \
  --run-stage full \
  --max-parallel 2
```

Full tables:

- `tables/summary_by_condition.csv`
- `tables/summary_by_seed.csv`
- `tables/family_relation_by_condition.csv`
- `tables/family_relation_by_seed.csv`
- `tables/route_matrix_by_seed.csv`
- `tables/expert_load_by_seed.csv`

Figures:

- `figures/family_purity_vs_load_matched_random.png`
- `figures/P3a_expert_feature_heatmap.png`
- `figures/P3b_expert_feature_heatmap.png`
- `figures/P3a_expert_family_composition_heatmap.png`
- `figures/P3b_expert_family_composition_heatmap.png`
- `figures/expert_load_histogram.png`
- `figures/target_accuracy_table.png`

## 13. Interpretation

P3 is a negative result for ordinary top-1 same-expert family grouping. The router can learn the target while assigning features to experts in a way that is only weakly above load-matched random and not stable across seeds.

## 14. Claim Boundary

Can claim:

- The P3 tasks are learnable.
- Ordinary top-1 does not reliably group same-family features in this setup.
- P3b shared target utility does not reliably strengthen family grouping over P3a.

Cannot claim:

- No architecture can learn family grouping.
- Family grouping is impossible under a load-balanced or utility-bound router.
- This is expert utility specialization evidence.

## 15. Next Decision

Treat ordinary top-1 same-expert assignment as arbitrary or early-locked until a stronger intervention changes P3b under seed-stable non-collapse.

## 16. Links And Artifact Map

anchor: `../../../problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

summary: `summary.md`

code workspace: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

runner: `active/synthetic_data_understanding/scripts/run_h0605bc_feature_assumption_relaxation.py`

config: `active/synthetic_data_understanding/configs/h0605c_same_expert_feature_relation.json`

result dir: `.../results/h0605c_same_expert_feature_relation/h0605c_same_expert_feature_relation_full_20260604/`

figure dir: `figures/`

key tables: all `tables/*.csv`

logs / checkpoints: local full run; no ACP/SCO job id.
