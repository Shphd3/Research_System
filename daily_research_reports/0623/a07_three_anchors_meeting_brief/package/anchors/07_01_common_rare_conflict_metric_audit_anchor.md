---
anchor_id: A07_01_common_rare_conflict_metric_audit
parent_node: rq.expert_specialization
status: supported_controlled_synthetic
created: 2026-06-23
canonical_language: en
source_draft: 00_handwrite_anchor.md
---

# A07_01 Common / Rare Conflict Metric Audit Anchor

## 0. Tiny Summary

父问题：expert partition 是否真的降低 feature interference，而不是只改善 load。
当前子问题：先验证 D07 数据和 `Delta_vs_best_null` 是否是合法审计面。
当前判断：D07 是可用的 controlled synthetic audit surface。
关键证据：full run 8 seeds；`Delta_vs_best_null=0.8601`；shortcut 最高 `0.5000`；hidden readout `1.0000`。
最危险边界：这是 synthetic analytic audit，不是真实神经训练或真实语料迁移。
下一步决策：使用该 surface 作为 A07_02 依赖。

Question:
Does D07, measured by `Delta_vs_best_null`, provide a valid controlled audit surface for later method-level rare-interference tests?

Physical prior:
A valid rare-interference surface must have oracle-relievable rare loss, comparable null baselines, no dominant shortcut explanation, and readable conflict signal at the routed token.

Core model:
For sample $i$, D07 exposes conflict feature $b_i$, conflict group $g_i$, rare/common class $r_i$, routed-token hidden state $h_i$, and target $y_i$.

Model term being tested:
Operational validity of D07 and its oracle-relievable rare-loss gap.

Primary metric:
`Delta_vs_best_null = min(L_rare(dense), L_rare(load_only)) - L_rare(oracle_feature_gate)`.

Falsifier:
`Delta_vs_best_null <= 0`, oracle uses forbidden information, null baselines are not comparable, shortcut-only variables explain the task, or $b_i/g_i$ is not readable from $h_i$.

Can claim:
D07 is valid enough for A07_02 method testing in the controlled synthetic audit.

Cannot claim:
`RIR_cc` works, common-control works, routing is semantic, expert utility exists, or the setup transfers beyond controlled D07.

Next decision:
Use the A07_01-supported surface as the dependency for A07_02.

## 1. Problem Definition

Parent problem: expert specialization must show reduced feature interference, not only non-collapsed load.

Sharper subproblem: validate the synthetic D07 audit surface before testing any method.

Decision question: does D07 plus `Delta_vs_best_null` create a valid method-test surface?

Not in scope: common-control, `RIR_cc`, route-function binding, expert ablation, real text, or deployable architecture.

## 2. Physical Priors

P1: Oracle-relievable rare loss is required.
Meaning: an oracle using only $b_i$ or $g_i$ should lower rare loss beyond dense and load-only nulls.
Could be wrong if: oracle gives no rare-loss advantage or needs target / split / future-token leakage.

P2: Null comparability is required.
Meaning: dense, load-only MoE, and oracle-gated MoE must use matched objective, budget, evaluation split, and comparable capacity reporting.
Could be wrong if: the oracle advantage is explained by budget, capacity, or objective mismatch.

P3: Router input must contain the conflict signal.
Meaning: later learned gating is interpretable only if $b_i/g_i$ is readable from $h_i$ at `B_CONST`.
Could be wrong if: oracle helps but a held-out readout cannot recover $b_i/g_i$ from $h_i$.

## 3. Falsifiable Hypotheses

H1: D07 has oracle-relievable rare conflict.
Supported if: `Delta_vs_best_null > 0` with common and total loss preserved.
Weakened if: oracle advantage is absent or comes from common/total regression.

H2: D07 is not shortcut-driven.
Supported if: shortcut-only variables do not predict $b_i/g_i$ or $y_i$ above threshold.
Weakened if: position, token identity, nuisance cue, or $r_i$ alone explains the task.

H3: The conflict signal is readable at the routed token.
Supported if: held-out readout from $h_i$ predicts $b_i/g_i$ above threshold and beyond shortcut controls.
Weakened if: no hidden-state readout exists or readability fails.

## 4. Mathematical Model

Objects: model $M$, rare loss $L_{\mathrm{rare}}(M)$, dense null, load-only null, and oracle feature gate.

Core quantities:
$$
\Delta_{\mathrm{dense}}=L_{\mathrm{rare}}(\mathrm{dense})-L_{\mathrm{rare}}(\mathrm{oracle})
$$
$$
\Delta_{\mathrm{load}}=L_{\mathrm{rare}}(\mathrm{load\ only})-L_{\mathrm{rare}}(\mathrm{oracle})
$$
$$
\Delta_{\mathrm{best\ null}}=\min\{L_{\mathrm{rare}}(\mathrm{dense}),L_{\mathrm{rare}}(\mathrm{load\ only})\}-L_{\mathrm{rare}}(\mathrm{oracle})
$$

Mechanism relation: oracle versus dense tests partition value; oracle versus load-only tests feature-aware routing beyond load balance.

Observable metrics: oracle gaps, common/total loss guards, null comparability, shortcut audit, and router-input readability.

Falsifier: the primary gap fails, or any validity guard makes the gap uninterpretable.

## 5. Computational Realization

Input objects: D07 manifest; dense, load-only MoE, and oracle-gated MoE; routed-token hidden states.

Computed variables: oracle gaps, loss guards, shortcut-only predictor scores, null-comparability table, and $h_i\rightarrow b_i/g_i$ readability.

Algorithm stages: construct D07; run null/oracle comparisons; audit oracle variables; audit shortcuts; audit routed-token readability.

Stage-local evidence: data manifest, oracle-gap table, null-comparability table, shortcut audit, readability table.

Expected artifacts: `protocol.md`, `summary.md`, `detailed.md`, `tables/d07_metric_audit.csv`, `tables/null_comparability.csv`, `tables/router_input_readability.csv`, `figures/oracle_rare_gap.png`.

## 6. Minimal Falsification Tests

Test: oracle-relievable gap.
Question: does oracle routing lower rare loss beyond the best null?
Intervention / comparison: dense, load-only MoE, oracle feature gate.
Primary metric: `Delta_vs_best_null`.
Supports: positive gap with common/total guards passing.
Weakens: no gap or gap caused by common/total regression.
Insufficient evidence: oracle variables or null comparability cannot be audited.

Test: shortcut and readability guards.
Question: is the gap about the intended conflict feature?
Intervention / comparison: shortcut-only predictors and held-out $h_i\rightarrow b_i/g_i$ readout.
Guard metric: shortcut score and routed-token readability.
Supports: shortcuts fail and conflict signal is readable.
Weakens: shortcuts explain the task or readability fails.
Insufficient evidence: missing manifest or hidden-state artifact.

## 7. Current Evidence

Observation: A07 shared full run completed on 2026-06-23 with 8 seeds.
Interpretation: D07 has oracle-relievable rare conflict: `Delta_vs_best_null = 0.8601 +/- 0.0008`; dense rare loss is `1.4399`, load-only rare loss is `1.5300`, and oracle rare loss is `0.5798`.
Boundary: this is a controlled synthetic hidden-state audit, not a neural end-to-end training result.
Evidence links: `../../experiments/A07_01_common_rare_conflict_metric_audit/summary.md`, `../../experiments/A07_01_common_rare_conflict_metric_audit/detailed.md`.

Observation: Validity guards passed in the same run.
Interpretation: conflict signal is readable from raw hidden and common-controlled hidden states (`1.0000` each), shortcut-only predictors stay at or below `0.5000`, and oracle forbidden-variable use is `0`.
Boundary: this validates the synthetic audit surface, not real-language transfer.
Evidence links: `../../experiments/A07_01_common_rare_conflict_metric_audit/tables/router_input_readability.csv`, `../../experiments/A07_01_common_rare_conflict_metric_audit/tables/shortcut_audit.csv`.

Observation: A05/A06 show load, entropy, and route_NMI can be misleading.
Interpretation: A07 needs a loss-based audit surface before method testing.
Boundary: this does not prove D07 is valid.
Evidence links: `../05_failure_mechanism/05_03_uniform_collapse_common_offset_anchor.md`, `../06_geometry_proxy_preservation/06_07_label_free_common_residual_control_router_anchor.md`.

Observation: A06_14 separates assignment from utility.
Interpretation: route-function binding belongs after metric and method tests.
Boundary: A07_01 does not test utility.
Evidence links: `../06_geometry_proxy_preservation/06_14_real_dclm_proxy_expert_utility_binding_anchor.md`.

## 8. Claim Boundary And Next Decision

Can claim:
D07 is valid enough for A07_02 common-control testing in controlled synthetic audit.

Cannot claim:
Common-control benefit, expert specialization, real-data transfer, or utility binding.

Next decision:
Use this surface for A07_02; do not generalize beyond controlled synthetic D07.
