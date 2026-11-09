# Protocol: A07_04 Common / Rare Gradient Conflict Splitting

## 0. Approval Snapshot

Approval status: Approved by user execution request on 2026-06-24; full run completed.

Purpose: test whether a neural MoE can reduce measured high-frequency / rare feature gradient conflict, rather than only improving load or route purity.

Primary anchor: `../../../problem_anchors/07_features_overlap/07_04_common_rare_gradient_conflict_splitting_anchor.md`

Anchor decision question: when a high-frequency feature \(C\) and a rare feature \(R\) have conflicting gradients inside shared experts, does top-1 MoE routing reduce their expert overlap enough to reduce rare-feature loss?

Anchor physical prior tested: if \(C\) is much more frequent than \(R\) and their per-expert gradients conflict, updates dominated by \(C\) can raise \(L_R\) unless routing separates them.

Anchor core model term tested: routing-weighted gradient conflict \(\mathcal{C}_{C,R}\).

Anchor falsifier: no negative \(C/R\) gradient conflict, no shared expert overlap, nonpositive \(\Delta\mathcal{C}_{C,R}\), or positive conflict reduction without rare-loss improvement.

Experiment role: root-cause / mechanism audit.

Primary metric from anchor: \(\Delta\mathcal{C}_{C,R}\) against the random top-1 MoE baseline, with \(L_R\) improvement as a required guard.

Claim boundary from anchor: neural controlled common/rare proxy only.

Minimal setup: train small neural dense and MoE classifiers on an imbalanced synthetic common/rare feature task; compute per-expert gradients on matched evaluation batches.

Basic configuration: 8 seeds, two features \(C/R\), four experts, dense baseline, random top-1 MoE, label-free centered unsupervised split MoE, and oracle split upper bound.

Conditions to run: `dense_shared`, `random_top1_moe`, `centered_unsup_split_moe`, `oracle_split_moe`.

Pass: measurable baseline conflict exists; centered split reduces \(\mathcal{C}_{C,R}\) versus random top-1; rare loss improves; common loss and load guards stay interpretable.

Fail: conflict is absent, conflict does not fall, rare loss does not improve, or gain is explained only by load/capacity mismatch.

Insufficient: gradients are not measured on expert parameters, routing or load tables are missing, or training/evaluation conditions are not matched.

Cannot claim: real-corpus specialization, natural-language feature discovery, or general semantic expert specialization.

Approval decision: user requested protocol plus 4-card execution in the same turn.

## 1. Anchor Alignment

Decision question: does routing reduce measured \(C/R\) gradient conflict and improve rare loss?

Physical prior tested: high-frequency common updates can hurt rare learning when gradients conflict in shared experts.

Core model term tested: \(\mathcal{C}_{C,R}=\sum_e q_{C,e}q_{R,e}[-\cos(g_{C,e},g_{R,e})]_+\).

Falsifier: no conflict, no conflict reduction, or no rare-loss improvement.

Claim boundary: controlled neural synthetic proxy only.

## 2. Tested Hypothesis

Label-free centered routing should reduce common/rare expert overlap in the presence of negative per-expert gradient cosine, lowering routing-weighted conflict and rare loss relative to random top-1 MoE.

## 3. Rival Explanations

No real conflict: \(C/R\) gradients do not conflict, so rare loss cannot be interpreted as interference.

Load-only gain: the candidate wins only because it uses experts more evenly.

Capacity mismatch: the candidate has more effective parameters or a different objective.

Hand-coded utility: the result is written into the loss or ablation rule rather than learned by neural training.

Rare impossibility: rare loss is high because the rare feature is not learnable, not because of conflict.

## 4. Data / Model / Algorithm / Objective

Data: synthetic neural common/rare classification proxy. Train split is imbalanced with \(\pi_C\gg\pi_R\); evaluation is balanced by feature. Each sample contains a strong shared component, a weak rare-disambiguating component, nuisance noise, and a binary target.

Models: dense logistic classifier; top-1 MoE with four neural experts; fixed oracle split MoE as an upper bound.

Algorithm: train each condition with the same optimizer, steps, batch size, and objective. For the centered condition, estimate a label-free train-set mean and unsupervised centers from inputs; routing uses centered inputs but experts receive full inputs.

Objective: binary cross entropy plus the same load-balance regularizer where a trainable router is used. No label is used for centered unsupervised routing.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dense shared | conflict existence | shared update conflict | establishes worst shared baseline | conflict/loss tables | negative cosine and high \(L_R\) | no conflict | gradients missing | `common_rare_gradient_conflict.csv` |
| Random top-1 MoE | baseline MoE | random routing may not split conflict | primary baseline | conflict/loss/load tables | conflict measurable | no valid baseline | load missing | `common_rare_gradient_conflict.csv` |
| Centered unsup split | H2/H3 | conflict-aware routing | main candidate | \(\Delta\mathcal{C}_{C,R}\) and \(L_R\) | conflict and rare loss improve | no improvement | load/capacity mismatch | `conflict_vs_rare_loss.png` |
| Oracle split | upper bound | rare impossible | checks learnability under correct split | loss table | rare learnable | oracle fails | forbidden if used as candidate | `common_rare_loss_guard.csv` |
| Load guard | load-only rival | load-only gain | protects interpretation | max load/entropy | matched/interpretable | gain load-only | missing | `load_guard.csv` |
| Gradient audit | core model | no real conflict | direct mechanism evidence | per-expert cosine | negative shared cosine | no negative cosine | wrong parameters | `gradient_cosine_by_expert.csv` |

Seeds: `20260624` to `20260631` for full run; two-seed smoke before full.

Checkpoints: final checkpoint only for the first run; step-wise conflict may be added only after this decision is closed.

## 6. Primary Metric

Primary metric:
\[
\Delta\mathcal{C}_{C,R}=\mathcal{C}_{C,R}^{\mathrm{random\ top1}}-\mathcal{C}_{C,R}^{\mathrm{centered\ split}}
\]

This metric decides whether routing actually reduces the measured overlap-weighted negative gradient conflict. Rare loss is a required guard: conflict reduction without \(L_R\) improvement is not support.

False positive cost: claiming expert specialization from load or routing structure alone. False negative cost: missing a real mechanism because the proxy is too small or too noisy.

## 7. Secondary Metrics

\(O_{C,R}\) expert overlap, per-expert gradient cosine, \(L_R\), \(L_C\), total loss, common/rare accuracy, max load, active experts, load entropy, oracle rare loss, and conflict-versus-rare-loss correlation across conditions.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: oracle split learns rare feature with low \(L_R\); centered split lowers \(\mathcal{C}_{C,R}\) and \(L_R\).

Known bad: dense/shared shows no negative gradient cosine; then the task does not instantiate the anchor prior.

Known confusing: \(\mathcal{C}_{C,R}\) falls but \(L_R\) does not; this supports route separation but not functional rare learning.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Smoke | Does the runner train and emit all tables? | smoke artifacts | all required tables exist | smoke result dir | detailed |
| Conflict existence | Is the anchor prior present? | gradient cosine table | pass if baseline conflict > 0 | `gradient_cosine_by_expert.csv` | summary |
| Split effect | Does candidate reduce conflict? | conflict table | pass if \(\Delta\mathcal{C}_{C,R}>0\) | `common_rare_gradient_conflict.csv` | summary |
| Rare guard | Does rare loss improve? | loss table | pass if \(L_R\) improves | `common_rare_loss_guard.csv` | summary |
| Load guard | Is result load-only? | load table | fail if load/capacity mismatch explains gain | `load_guard.csv` | detailed |

## 10. Algorithm Specification, If Nontrivial

input: config, seeds, synthetic common/rare generator, model condition.

parameters: feature frequencies, input dimension, expert count, train steps, learning rate, load-balance weight, conflict thresholds.

intermediate variables: route assignments, \(q_{f,e}\), per-expert gradients, cosine matrix, \(O_{C,R}\), \(\mathcal{C}_{C,R}\), losses.

steps: generate train/eval data; train matched models; evaluate feature losses; compute route distributions; compute per-expert gradients on matched feature batches; aggregate metrics; write tables and figures.

outputs: protocol-aligned tables, central figures, summary, detailed record, anchor update.

debug artifacts: seed-level CSVs, run manifest, ACP dry-run log.

pass conditions: conflict exists, candidate reduces conflict, rare loss improves, and guards are interpretable.

fail conditions: no conflict, no conflict reduction, no rare improvement, or load/capacity mismatch.

failure reasons: invalid proxy, ineffective routing, rare impossibility, insufficient seeds, or flawed gradient measurement.

## 11. Success / Failure / Insufficient Evidence

Success: A07_04 supports that routing can reduce measured common/rare gradient interference in a controlled neural proxy.

Failure: this setup does not support conflict splitting as the mechanism.

Insufficient evidence: missing gradient audit, missing route/load tables, or mismatch between trained objects and measured gradients.

## 12. What This Cannot Claim

No real-corpus transfer, no natural-language feature discovery, no general semantic expert theorem, no deployable router, and no claim that balanced load or high NMI is enough.

## 13. Review Notes And Protocol Changes

2026-06-24: initial protocol. User requested protocol and immediate 4-card execution in the same turn.

2026-06-24: full run `a07_04_grad_conflict_full_20260624_1` completed locally over 8 seeds and 4 logical shards. ACP four-card script dry-run was recorded; no external ACP job id was created.
