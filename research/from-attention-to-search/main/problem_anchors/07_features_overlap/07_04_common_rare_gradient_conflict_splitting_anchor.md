---
anchor_id: A07_04_common_rare_gradient_conflict_splitting
parent_node: rq.expert_specialization
status: insufficient_evidence_neural_proxy
created: 2026-06-25
canonical_language: en
source_draft: ../../../../../daily_research_reports/backup/2026/06/0625/docs/07.md
placement: 07_features_overlap
depends_on:
  - A05_common_logit_collapse_line
  - A06_common_residual_control_line
  - A07_01_to_A07_03_positive_control_line
---

# A07_04 Common / Rare Gradient Conflict Splitting Anchor


## 1. Problem Definition

Parent problem: decide whether MoE expert partition has causal value for feature-level specialization.

Sharper subproblem: test whether routing separates a high-frequency feature \(C\) from a rare feature \(R\) when they create harmful gradient conflict inside shared experts.

Decision question: does routing reduce measured \(C/R\) gradient conflict alongside rare loss, and does that identify why sharing hurts?

Not in scope: early common-logit collapse as the main object, hidden-state geometry preservation as the main object, broad semantic clustering, real-corpus generalization, or deployable routing.

## 2. Physical Priors

P1: Frequency imbalance can make common updates dominate rare updates.
Meaning: if \(\pi_C\gg\pi_R\), then shared expert parameters receive much larger update pressure from \(C\) than from \(R\).
Boundary: frequency imbalance alone does not establish harm to \(R\).

P2 (`AI_PROPOSAL`, reasoning correction): negative gradient inner products can explain shared-update harm in a small-step SGD approximation.
Meaning: overlap is not itself harmful; negative cosine is not necessary for finite-step harm.
Could be wrong if: actual cross-feature loss changes disagree with the first-order prediction.

P3: Load balance is a guard, not the claim.
Meaning: a route can be balanced while still putting conflicting features into the same functional expert.
Could be wrong if: rare-loss gains vanish after matching load, capacity, and objective.

## 3. Falsifiable Hypotheses

H1: The tested setup contains measurable common/rare gradient conflict.
Supported if: at least one shared expert has \(q_{C,e}q_{R,e}>0\) and \(\cos(g_{C,e},g_{R,e})<0\).
Weakened if: common/rare gradients are non-conflicting or never share experts.

H2: Conflict-aware routing reduces routing-weighted conflict.
Supported if: \(\Delta\mathcal{C}_{C,R}>0\) against dense/shared or random top-1 baselines under matched load/capacity guards.
Weakened if: overlap or conflict does not fall, or the change is explained only by load balancing.

H3 (`AI_PROPOSAL`, bounded reading): conflict reduction accompanies rare-loss improvement.
Compatible if: \(\Delta\mathcal{C}_{C,R}>0\) and \(L_R\) improves without unacceptable \(L_C\) regression; weakened if rare loss does not improve.
Rival: changed expert allocation improves loss independently of measured conflict. Co-movement does not identify mediation.

## 4. Mathematical Model

Objects: high-frequency feature \(C\), rare feature \(R\), frequencies \(\pi_C\gg\pi_R\), expert \(e\), routing probability \(q_{f,e}\), per-expert gradient \(g_{f,e}\), and feature loss \(L_f\).

Core decomposition:
\[
O_{C,R}=\sum_e q_{C,e}q_{R,e}
\]

\[
I_{C,R,e}=[-\cos(g_{C,e},g_{R,e})]_+
\]

\[
\mathcal{C}_{C,R}=\sum_e q_{C,e}q_{R,e}[-\cos(g_{C,e},g_{R,e})]_+
\]

Mechanism relation:
\[
\Delta \theta_e=-\eta(\pi_Cq_{C,e}g_{C,e}+\pi_Rq_{R,e}g_{R,e})
\]

\[
\Delta L_R^{C\rightarrow R}\approx-\eta\pi_C\sum_e q_{R,e}q_{C,e}\langle g_{R,e},g_{C,e}\rangle
\]

Negative inner products predict harm in this first-order SGD term. Finite-step curvature and optimizer state can alter actual loss; routing benefit need not be mediated by this term.

Observable metrics: \(O_{C,R}\), \(\mathcal{C}_{C,R}\), \(\Delta\mathcal{C}_{C,R}\), \(L_R\), \(L_C\), max load, active experts, and expert utility / ablation guards.

Falsifier: the measured gradients do not conflict, routing does not reduce \(\mathcal{C}_{C,R}\), or rare loss does not improve when \(\mathcal{C}_{C,R}\) falls.

## 5. Computational Realization

Input objects: trained neural D07 or realistic common/rare proxy; feature labels used only for audit; dense/shared baseline; random top-1 MoE; candidate conflict-splitting router; optional oracle split as an upper-bound diagnostic.

Computed variables: per-feature route distribution \(q_{f,e}\), per-expert gradients \(g_{f,e}\) on matched mini-batches, expert overlap \(O_{C,R}\), routing-weighted conflict \(\mathcal{C}_{C,R}\), feature losses \(L_C,L_R\), and load guards.

For matched conditions, measure routes, gradients, losses, and load/capacity guards. Expert-utility or fixed-route ablation remains a secondary guard.

The existing Protocol and result records retain the registered metrics and guards; the reasoning corrections do not retrospectively change their contract.

## 6. Minimal Falsification Tests

Test: conflict existence audit.
Question: do \(C\) and \(R\) actually conflict inside shared experts?
Intervention / comparison: measure \(q_{C,e}q_{R,e}\) and \(\cos(g_{C,e},g_{R,e})\) in dense/shared or random top-1 MoE.
Primary metric: \(\mathcal{C}_{C,R}\).
Supports: positive routing-weighted conflict.
Weakens: no overlap, no negative cosine, or conflict only appears in an artificial oracle setting.
Insufficient evidence: gradients are not measured on matched batches or expert paths.

Test: conflict splitting audit.
Question: does candidate routing reduce measured common/rare conflict?
Intervention / comparison: dense/shared or random top-1 versus candidate conflict-splitting router under matched load/capacity/objective.
Primary metric: \(\Delta\mathcal{C}_{C,R}\).
Supports: positive conflict reduction with load guards passing.
Weakens: conflict does not fall or the reduction is load-only.
Insufficient evidence: load, capacity, or objective is unmatched.

Test: rare-loss guard.
Question: does rare loss improve alongside reduced conflict?
Intervention / comparison: same matched conditions as the conflict audit.
Primary metric: required guard on \(L_R\) after \(\Delta\mathcal{C}_{C,R}>0\).
Compatible: \(L_R\) improves while \(L_C\) is stable within tolerance; this alone does not identify the cause.
Weakens: \(L_R\) does not improve or \(L_C\) regresses enough to show conflict transfer.
Insufficient evidence: rare examples are too few, noisy, or not evaluated on a balanced split.

## 7. Current Evidence

Observation: A07_04 full neural run completed on 2026-06-24 over 8 seeds.
Interpretation: the anchor prior is present: dense shared training has strong negative common/rare gradient cosine and high routing-weighted conflict (`0.9982`); random top-1 has measurable conflict (`0.2641`).
Boundary: measuring conflict does not prove routing solves it.
Evidence links: `../../experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md`, `../../experiments/A07/A07_04_common_rare_gradient_conflict_splitting/detailed.md`.

Observation: centered unsupervised split weakly reduces conflict and rare loss versus random top-1.
Interpretation: \(\Delta\mathcal{C}_{C,R}=0.0271 \pm 0.0398\); rare loss improvement is `0.0632 +/- 0.0617`; common loss does not regress.
Boundary: the effect is small and noisy.
Evidence links: `../../experiments/A07/A07_04_common_rare_gradient_conflict_splitting/tables/common_rare_gradient_conflict.csv`, `../../experiments/A07/A07_04_common_rare_gradient_conflict_splitting/tables/common_rare_loss_guard.csv`.

Observation: dense shared training has lower rare loss than centered MoE, and rare accuracy remains low for non-oracle conditions.
Interpretation: the current run is insufficient evidence for functional MoE specialization.
Boundary: oracle split succeeds, so rare learning is possible under the right split; the current candidate split is too weak or the proxy is not yet well isolated.
Evidence links: `../../experiments/A07/A07_04_common_rare_gradient_conflict_splitting/figures/conflict_vs_rare_loss.png`.

Prior A05/A06 boundary: load, route entropy, and purity do not establish functional interference or expert specialization.
Evidence links: `../05_failure_mechanism/05_03_uniform_collapse_common_offset_anchor.md`, `../06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`.

Observation: A07_01 to A07_03 produced a synthetic positive-control chain, but its conflict and expert utility were largely constructed.
Interpretation: those experiments validate the audit machinery, not the real mechanism.
Boundary: they should not be used as primary evidence for natural expert specialization.
Evidence links: `07_01_common_rare_conflict_metric_audit_anchor.md`, `07_02_common_controlled_rare_interference_anchor.md`, `07_03_route_function_binding_anchor.md`.

Historical framing: the 2026-06-25 draft proposed high-frequency / rare conflict as a candidate explanation of feature interference; it is not proof of that explanation.
Historical source (unavailable locally): `../../../../../daily_research_reports/backup/2026/06/0625/docs/07.md`.

## 8. Claim Boundary And Next Decision

Can claim:
The current neural proxy measured common/rare gradient conflict and found weak partial movement in the expected direction versus random top-1.

Cannot claim:
Functional expert specialization, dense-beating MoE value, general semantic specialization, real-corpus robustness, natural-language feature discovery, or that balanced load / high route purity is sufficient.

Previous agenda: revise the proxy/router to beat dense/shared rare loss.

Next decision (`AI_PROPOSAL`, researcher confirmation pending): determine whether this carrier's conflict proxy predicts independent rare-loss change under a specified common-feature update from the same parameter and optimizer state. Completion requires a contrast separating the directional account from finite-step or allocation effects; further execution needs its own approved contract.
