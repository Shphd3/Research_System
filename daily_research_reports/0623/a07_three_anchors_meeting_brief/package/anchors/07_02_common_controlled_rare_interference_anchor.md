---
anchor_id: A07_02_common_controlled_rare_interference
parent_node: rq.expert_specialization
status: supported_controlled_synthetic
created: 2026-06-23
canonical_language: en
depends_on: A07_01_common_rare_conflict_metric_audit
source_draft: 00_handwrite_anchor.md
---

# A07_02 Common-Controlled Rare Interference Anchor

## 0. Thinking Card

父问题：common-control 是否从 anti-collapse 推进到 rare-feature interference reduction。
当前子问题：在 A07_01 合法 D07 上，common-control 是否比 matched balance-only 降低 rare loss。
当前判断：common-control 在 controlled D07 上支持 rare-interference reduction。
关键证据：8 seeds；`RIR_cc=0.9502`；load 完全匹配；conflict signal 无下降。
最危险边界：这是 synthetic analytic method test，不是真实训练 checkpoint 证据。
下一步决策：用 route assignments 进入 A07_03 utility audit。

Question:
On A07_01-valid D07, does label-free common-control reduce rare-feature interference beyond load-matched balance-only MoE?

Physical prior:
If common-logit bias hides the conflict feature, label-free common-control should reduce rare loss beyond matched load balance while preserving conflict signal.

Core model:
Raw score $z_{i,e}=w_e^Th_i$; common-controlled score $z'_{i,e}=w_e^T\phi(h_i)$, where $\phi$ is label-free common control.

Model term being tested:
Method-level effect of common control on rare loss.

Primary metric:
`RIR_cc = L_rare(balance_only) - L_rare(common_control)`.

Falsifier:
`RIR_cc <= 0`, the gain disappears under matched-load comparison, $\phi(h_i)$ removes conflict signal, or common-control uses forbidden labels.

Can claim:
Common-control reduces rare-feature interference beyond matched balance-only MoE in controlled synthetic D07.

Cannot claim:
Expert causal specialization, semantic routing, route-function binding, real-language transfer, or deployable architecture.

Next decision:
Use A07_02 route assignments and expert IDs for A07_03.

## 1. Problem Definition

Parent problem: after D07 validity, test whether common-control gives functional benefit beyond load balancing.

Sharper subproblem: isolate rare-loss improvement from load-only improvement.

Decision question: does label-free common-control beat load-matched balance-only MoE on rare loss?

Not in scope: D07 validity, oracle data sanity, expert utility, expert ablation, real text, or broad method search.

## 2. Physical Priors

P1: Common-logit bias can block conflict-conditioned routing.
Meaning: $w_e^Tc$ can dominate assignment before $q_{b_i}$ matters.
Could be wrong if: common-control changes load but not rare loss.

P2: Matched load is the null.
Meaning: common-control must beat balance-only MoE matched on max load, active experts, entropy, load objective, budget, and split.
Could be wrong if: the rare-loss gain disappears under matched-load comparison.

P3: Common-control must preserve conflict signal.
Meaning: $\phi(h_i)$ should reduce common dominance without erasing $q_{b_i}$.
Could be wrong if: conflict readability or margin collapses after $\phi$.

## 3. Falsifiable Hypotheses

H1: Common-control reduces rare interference.
Supported if: `RIR_cc > 0` with common and total loss guards passing.
Weakened if: rare loss does not improve over matched balance-only MoE.

H2: The gain is not just better load.
Supported if: load metrics are matched within tolerance while `RIR_cc` remains positive.
Weakened if: common-control only wins by having better load balance.

H3: The transform preserves conflict signal.
Supported if: conflict readability / margin before and after $\phi$ are preserved.
Weakened if: $\phi$ removes conflict signal.

## 4. Mathematical Model

Objects: rare loss, common-control transform $\phi$, load-matched balance-only baseline, A07_01 oracle gap.

Primary metric:
$$
\mathrm{RIR}_{cc}=L_{\mathrm{rare}}(\mathrm{balance\ only})-L_{\mathrm{rare}}(\mathrm{common\ control})
$$

Fraction of oracle gap:
$$
\mathrm{FoO}_{cc}=\frac{\mathrm{RIR}_{cc}}{\Delta_{\mathrm{best\ null}}}
$$

Mechanism relation: if $\phi$ removes common bias without erasing $q_{b_i}$, rare loss should improve beyond matched load-only routing.

Observable metrics: `RIR_cc`, `FoO_cc`, rare/common/total loss, matched-load table, conflict readability / margin before and after $\phi$, and label-free audit.

Falsifier: no positive `RIR_cc`, unfair load comparison, conflict signal removal, or label leakage.

## 5. Computational Realization

Input objects: A07_01-valid D07, `Delta_vs_best_null`, matched balance-only MoE, and one or two label-free common-control candidates.

Computed variables: `RIR_cc`, `FoO_cc`, loss guards, load-match metrics, conflict-signal preservation, and checkpoint / route-assignment manifest for A07_03.

Algorithm stages: reuse A07_01 data; run matched balance-only and common-control; compute method benefit; audit load match, label-free validity, and conflict-signal preservation; save required checkpoints.

Stage-local evidence: rare-loss table, matched-load table, conflict-signal table, label-free audit, checkpoint manifest.

Expected artifacts: `protocol.md`, `summary.md`, `detailed.md`, `tables/common_control_rir.csv`, `tables/matched_load_guard.csv`, `tables/conflict_signal_preservation.csv`, `tables/checkpoint_assignment_manifest.csv`.

## 6. Minimal Falsification Tests

Test: common-control rare-loss effect.
Question: does common-control lower rare loss beyond matched balance-only MoE?
Intervention / comparison: matched balance-only versus common-control.
Primary metric: `RIR_cc`.
Supports: positive `RIR_cc` with common/total guards passing.
Weakens: nonpositive `RIR_cc` or common/total regression.
Insufficient evidence: A07_01 not passed or matched-load comparison missing.

Test: load and signal guards.
Question: is the effect common-control-specific and signal-preserving?
Intervention / comparison: matched-load audit plus pre/post-$\phi$ conflict readout.
Guard metric: matched-load table, `FoO_cc`, and conflict-signal preservation.
Supports: load is matched and conflict signal remains available.
Weakens: gain is load-only or $\phi$ removes conflict signal.
Insufficient evidence: missing load table, hidden readout, or label-free audit.

## 7. Current Evidence

Observation: A07 shared full run completed on 2026-06-23 with 8 seeds.
Interpretation: common-control beats matched load-only on rare loss: `RIR_cc = 0.9502 +/- 0.0006`; `FoO_cc = 1.1049`.
Boundary: this is a controlled synthetic method test, not a trained-checkpoint or real-corpus result.
Evidence links: `../../experiments/A07/A07_02_common_controlled_rare_interference/summary.md`, `../../experiments/A07/A07_02_common_controlled_rare_interference/detailed.md`.

Observation: Load and signal guards passed.
Interpretation: load-only and common-control both have max load `0.2500`, active experts `4.0000`, and load entropy `1.0000`; raw and post-control conflict readout are both `1.0000`.
Boundary: this rules out load-only and signal-erasure rivals within this synthetic setup only.
Evidence links: `../../experiments/A07/A07_02_common_controlled_rare_interference/tables/matched_load_guard.csv`, `../../experiments/A07/A07_02_common_controlled_rare_interference/tables/conflict_signal_preservation.csv`.

Observation: A05_03 supports common offset as an early collapse mechanism.
Interpretation: common-control is plausible as an entry-condition method.
Boundary: A05_03 does not show rare-interference reduction.
Evidence links: `../05_failure_mechanism/05_03_uniform_collapse_common_offset_anchor.md`.

Observation: A06_07 weakens simple common/residual controls as standalone specialization evidence.
Interpretation: A07_02 must use rare loss and matched-load comparison.
Boundary: A06_07 did not test D07 or `RIR_cc`.
Evidence links: `../06_geometry_proxy_preservation/06_07_label_free_common_residual_control_router_anchor.md`.

## 8. Claim Boundary And Next Decision

Can claim:
Label-free common-control reduces rare-feature interference beyond matched balance-only MoE in controlled D07.

Cannot claim:
Expert utility, semantic routing, real-language transfer, or deployable architecture.

Next decision:
Use A07_02 outputs for A07_03 route-function binding; do not generalize beyond controlled D07.
