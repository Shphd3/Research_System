---
anchor_id: A07_02_common_controlled_rare_interference
current_short_name: nested_tail_common_subspace_control
parent_node: rq.expert_specialization
status: supported_controlled_rank1_surface
created: 2026-06-23
retargeted: 2026-06-28
canonical_language: en
depends_on: A07_01_common_rare_conflict_metric_audit
thinking_card_source: 07_02_common_controlled_rare_interference_thinking_card.md
---

# A07_02 Nested Tail Common-Subspace Control Anchor

Thinking Card source: [07_02_common_controlled_rare_interference_thinking_card.md](07_02_common_controlled_rare_interference_thinking_card.md)

## 1. Problem Definition

**Parent problem:** A07_01 tests whether the common high-gain backbone exists.

**Sharper subproblem:** Test whether controlling the common-subspace component of tail updates improves rare nested learning.

**Decision question:** Conditional on A07_01 passing, does common-subspace update control reduce nested tail loss while preserving common accuracy?

**Not in scope:** proving the full C3S optimizer, selecting the best optimizer, MoE causal utility, or real-language claims.

## 2. Physical Priors

**P1: Tail interference is update-space concentration.**  
Meaning: the key object is not route load or hidden norm, but the fraction of the actual update direction inside $P_C$.  
Could be wrong if: $\alpha_{\mathrm{tail}}$ is low while tail loss remains bad.

**P2: Useful common knowledge should be preserved.**  
Meaning: suppressing tail updates inside $P_C$ should not erase the already-learned $A$ feature.  
Could be wrong if: common loss regresses when tail improves.

**P3: Confidence capping alone is a rival.**  
Meaning: reducing gradients on already-solved common examples may help without subspace suppression.  
Could be wrong if: confidence capping explains all improvement.

## 3. Falsifiable Hypotheses

**H1: Tail updates overuse $P_C$.**  
Supported if: CE baseline has high $\alpha_{\mathrm{tail}}$ after $T_0$.  
Weakened if: tail updates already live outside $P_C$.

**H2: Subspace control reduces tail loss.**  
Supported if: controlled updates lower $L_{\mathrm{tail}}$ versus CE under matched budget.  
Weakened if: tail loss does not improve.

**H3: The effect is specifically subspace-related.**  
Supported if: $\alpha_{\mathrm{tail}}$ decreases when tail loss improves, and confidence-capping-only does not explain the full effect.  
Weakened if: loss improves with no reduction in $\alpha_{\mathrm{tail}}$.

## 4. Mathematical Model

**Objects:** frozen common projector $P_C$, AdamW preconditioned update $u_t$, tail update $u_{\mathrm{tail}}$, common and tail losses.

**Core decomposition:**
$$
u_t=P_Cu_t+P_{\perp C}u_t,
$$
$$
\tilde u_t=(I-\rho P_C)u_t.
$$

**Mechanism relation:** if harmful absorption is real, reducing $P_Cu_{\mathrm{tail}}$ should reduce tail loss while preserving the already-learned common feature.

**Observable metrics:**
$$
\alpha_{\mathrm{tail}}(t)=\frac{\|P_Cu_{\mathrm{tail}}(t)\|^2}{\|u_{\mathrm{tail}}(t)\|^2+\epsilon},
$$
$$
\Delta L_{\mathrm{tail}}=L_{\mathrm{tail}}(\mathrm{CE})-L_{\mathrm{tail}}(\mathrm{control}).
$$

**Falsifier:** no tail loss improvement, common loss regression, or no reduction in $\alpha_{\mathrm{tail}}$.

## 5. Computational Realization

**Input objects:** A07_01-passing nested data, frozen $P_C$, matched CE baseline, confidence-capped baseline, subspace-suppressed update condition.

**Computed variables:** per-level loss, common retention, $\alpha_{\mathrm{tail}}$, effective rank, top-$k$ tail feature mass.

**Algorithm stages:** freeze $P_C$ at $T_0$; continue CE baseline; run confidence-capping-only guard; run subspace-suppressed control; compare tail loss and update projection.

**Stage-local evidence:** tail loss table, common retention table, update-projection table, singular/effective-rank diagnostics.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`, `tables/a07_02_aggregate.csv`, `figures/a07_02_control_results.png`.

## 6. Minimal Falsification Tests

**Test: tail common-subspace control.**  
Question: does suppressing $P_Cu_{\mathrm{tail}}$ improve rare nested learning?  
Intervention / comparison: CE baseline versus subspace-suppressed control, with confidence-capping-only as a rival guard.  
Primary metric: $\Delta L_{\mathrm{tail}}=L_{\mathrm{tail}}(\mathrm{CE})-L_{\mathrm{tail}}(\mathrm{control})$.  
Pass / fail / insufficient: pass if $\Delta L_{\mathrm{tail}}>0$, common loss is preserved, and $\alpha_{\mathrm{tail}}$ decreases; fail if tail loss or common retention fails; insufficient if A07_01 did not establish stable $P_C$.  
Why it decides: it tests whether the common backbone is a controllable source of tail interference.  
Failure means: either the interference prior is wrong, the control target is wrong, or the implementation does not affect the actual update direction.

## 7. Current Evidence

**Observation:** A07_02 nested full run `a07_nested_full_20260628_2` completed with 8 seeds. Combined confidence gating plus subspace suppression improved tail loss by `0.1075`, reduced $\alpha_{\mathrm{tail}}$ by `0.1204`, and kept common loss regression within guard (`0.0265 < 0.05`).
**Interpretation:** on this controlled rank-one nested surface, the common-subspace update-control target is functional, not only geometric.
**Boundary:** this is not full C3S-AdamW and not a wide-transformer result.
**Evidence links:** `../../experiments/A07/A07_02_nested_tail_common_subspace_control/summary.md`, `../../experiments/A07/A07_02_nested_tail_common_subspace_control/detailed.md`.

**Observation:** confidence gating alone improved tail loss (`0.0705`) but did not reduce $\alpha_{\mathrm{tail}}$; subspace suppression alone reduced $\alpha_{\mathrm{tail}}$ (`0.1153`) and improved tail loss (`0.0751`).
**Interpretation:** the result separates two effects: stopping solved common examples helps, and update-space common-subspace suppression contributes its own mechanism signal.
**Boundary:** the two effects are not yet separated in real-DCLM or MoE training.
**Evidence links:** `../../experiments/A07/A07_02_nested_tail_common_subspace_control/tables/a07_02_aggregate.csv`.

**Observation:** A07_06 improved rare loss while route-level conflict barely moved.
**Interpretation:** A07_02 should be read as a cleaner update-space mechanism target than routing-weighted conflict alone.
**Boundary:** this does not rescue A07_06's route-conflict mechanism claim.
**Evidence links:** `../../experiments/A07/A07_06b_projected_moe_conflict_splitting/summary.md`.

**Observation:** The mentor C3S note defines the relevant control target as the common-subspace component of the actual preconditioned update.  
**Interpretation:** A07_02 should measure update-space suppression, not just route load or hidden norm.  
**Boundary:** The proof does not guarantee tail loss improvement outside this controlled surface.  
**Evidence links:** `../../../../../daily_research_reports/0625/docs/c3s_adamw_merged_rigorous_proof_with_negative_results.md`.

**Observation:** Prior A07_02 showed common-control improved D07 rare loss under matched load.  
**Interpretation:** This remains a useful controlled precedent, but it does not test nested $P_C$ suppression.  
**Boundary:** Old `RIR_cc` should not be promoted as evidence for this new anchor.  
**Evidence links:** `../../experiments/A07/A07_02_common_controlled_rare_interference/summary.md`.

## 8. Claim Boundary And Next Decision

**Can claim:** common-subspace update control reduces tail loss and tail update concentration on the controlled rank-one nested surface.

**Cannot claim:** full C3S validity, MoE specialization, semantic experts, or real-language transfer.

**Next decision:** do not jump to real utility; connect the control target back to A06 preservation and test it only on a preserved route/proxy partition.
