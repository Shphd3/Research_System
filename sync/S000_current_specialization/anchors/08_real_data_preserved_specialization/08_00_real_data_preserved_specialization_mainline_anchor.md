---
anchor_id: A08_00_real_data_preserved_specialization_mainline
parent_node: rq.expert_specialization
status: first_batch_closed
created: 2026-06-28
canonical_language: en
source_docs:
  - ../../../../../daily_research_reports/0625/docs/two_phase_singular_mode_learning_proof_and_test.md
  - ../../../../../daily_research_reports/0625/docs/c3s_adamw_merged_rigorous_proof_with_negative_results.md
  - ../../../../../daily_research_reports/0626/recordings/r1.md
---

# A08_00 Real-Data Preserved Specialization Mainline Anchor

## 0. Thinking Card

**Phenomenon:** Real DCLM proxy routing can be initialized at step 0, but ordinary early training erases it by step 5/10.

**Mechanism guess:** Once a useful singular direction is stable, its forward gating role can be treated as fixed; cross-entropy can still increase its gain and overwrite later routing unless gate/training updates suppress the already-converged common direction.

**Key variables:** singular-direction drift, singular gain, gate-forward assignment, proxy-route NMI, LM loss, common-subspace update fraction, route-function utility.

**Causal relation:** converged direction -> stable gate-forward partition -> early CE feedback/gain growth -> partition overwrite unless updates are constrained -> preserved specialization can later be tested for utility.

**Observable metric:** `proxy_route_NMI@step5/10` with LM loss guard, plus direction drift and update-subspace guards.

**Alternative explanation:** proxy clusters may not be functional, preservation may only protect labels, or loss changes may come from regularization rather than specialization.

**Decision:** pursue A08 if a singular-convergence-aware router preserves real-DCLM proxy routing through early training without LM loss regression.

## 1. Problem Definition

**Parent problem:** Build a MoE training method that initializes specialization on real data and preserves it through early training.

**Sharper subproblem:** Define specialization as preserved, converged-direction-based routing with later causal utility, not as load balance or semantic naming.

**Decision question:** Can stable singular directions become real-data gate-forward anchors that survive early training and later show utility?

**Not in scope:** final pretrained MoE claims, broad scaling, or semantic expert names before preservation and utility evidence.

## 2. Physical Priors

**P1: Converged directions can define forward routing.**
If a singular direction no longer rotates materially, its gating role is stable enough to become a router row.

**P2: CE still amplifies gain after direction convergence.**
The stable direction can keep growing in gain and dominate updates unless controlled.

**P3: Preserved specialization needs both routing and utility.**
Initialization specialization means route identity survives early training; functional specialization additionally requires interference reduction or causal ablation value.

## 3. Falsifiable Hypotheses

**H1:** stable singular directions exist in controlled and real surfaces.
**H2:** those directions can initialize gate-forward partitions.
**H3:** anti-feedback training preserves the partition through step 5/10.
**H4:** preserved partitions reduce update-space interference or have causal expert utility.

## 4. Mathematical Model

**Objects:** selected matrix $W(t)=\sum_i\sigma_i(t)u_i(t)v_i(t)^\top$, direction projector $P_i(t)=v_i(t)v_i(t)^\top$, router row $g_i\propto v_i$, and update $u_t$.

**Core decomposition:**
$$
\text{specialization} =
\text{direction stability}
+\text{route preservation}
+\text{functional utility}.
$$

**Observable metrics:** $\|P_i(t)-P_i(t-\Delta)\|$, $\Delta\sigma_i$, `proxy_route_NMI@step5/10`, LM loss, $\alpha_{\mathrm{tail}}$, fixed-route ablation selectivity.

**Falsifier:** direction stability exists but route preservation fails without explanation, or preservation succeeds but no utility metric moves.

## 5. Computational Realization

**Input objects:** 05 common-logit audits, 06 real-DCLM proxy initialization/preservation, 07 nested update-space utility, mentor notes, r1 recording.

**Computed variables:** convergence thresholds, gate-forward rows, preservation trajectories, update-subspace diagnostics, utility reads.

**Algorithm stages:** reproduce mechanism -> synthetic method loop -> real-DCLM convergence audit -> real preservation method -> utility closure.

**Expected artifacts:** A08_01 to A08_10 anchors, first four protocols, synthetic/real summaries, and two meeting briefs.

## 6. Minimal Falsification Tests

**Test:** ten-step iteration chain.
**Primary metric:** each card has one primary metric; the whole series is decided first by `proxy_route_NMI@step5/10` with LM loss guard.
**Pass / fail / insufficient:** pass only if preservation and utility close in order; fail if route preservation cannot be maintained; insufficient if synthetic-only evidence is used for real claims.
**Failure means:** method construction is premature or the gating definition is wrong.

## 7. Current Evidence

**Observation:** A06_11 supports real-DCLM step-0 proxy-center initialization, while A06_12 shows ordinary training erases it by step 5/10.
**Interpretation:** preservation, not discovery, is the current real-data bottleneck.
**Boundary:** proxy-route NMI is not utility.

**Observation:** A07_01/A07_02 nested runs support common-backbone formation and update-space control on a controlled rank-one surface.
**Interpretation:** update-space control is a plausible preservation guard.
**Boundary:** this is not real-DCLM evidence.

**Observation:** r1 states that once singular direction is stable, gate-forward assignment can be treated as fixed, but convergence must be defined.
**Interpretation:** A08 begins with convergence operationalization.

**Observation:** A08_01/A08_02 full synthetic run
`a08_singular_preservation_full_20260628_2` supports the first two bridge
steps: rank-one direction convergence and direction-to-gate conversion.
**Interpretation:** the mentor/r1 direction-forward part is operational on a
controlled rank-one surface.
**Boundary:** wide robustness and real-data convergence are not established.

**Observation:** A08_03/A08_04 weaken the first proposed method loop:
common/residual split improves tail loss but loses to a capacity-matched random
split, and iterative residual discovery fails.
**Interpretation:** direction-based routing is plausible, but the current
split/reservoir method should not be promoted to real-DCLM preservation.
**Boundary:** method construction must return to preservation failure
decomposition before A08_08/A08_09.

## 8. Claim Boundary And Next Decision

**Can claim:** A08 has closed its first synthetic batch: convergence and
direction-to-gate conversion are supported on a controlled rank-one surface.

**Cannot claim:** common/residual split is the mechanism, iterative residual
discovery works, the method works on real data, real semantic experts exist, or
preserved routes are useful.

**Next decision:** run A08_05 real-DCLM singular/gate-input convergence audit,
while keeping A08_03/A08_04 method claims parked.
