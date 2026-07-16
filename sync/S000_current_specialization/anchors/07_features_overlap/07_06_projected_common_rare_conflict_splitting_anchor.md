---
anchor_id: A07_06_projected_common_rare_conflict_splitting
parent_node: rq.expert_specialization
status: insufficient_evidence_mechanism_positive_rare_loss
created: 2026-06-28
canonical_language: en
placement: 07_features_overlap
depends_on:
  - A06_proxy_initialization_and_preservation_line
  - A07_04_common_rare_gradient_conflict_splitting
  - A07_05_common_update_interference_diagnostic
source_notes:
  - ../../../../../daily_research_reports/0625/docs/c3s_adamw_merged_rigorous_proof_with_negative_results.md
  - ../../../../../daily_research_reports/0625/docs/two_phase_singular_mode_learning_proof_and_test.md
---

# A07_06 Projected Common / Rare Conflict Splitting Anchor

Thinking Card source: [07_06_projected_common_rare_conflict_splitting_thinking_card.md](07_06_projected_common_rare_conflict_splitting_thinking_card.md)

## 1. Problem Definition

**Parent problem:** A07 asks whether expert partition has functional value, not
just balanced load or route-label purity.

**Sharper subproblem:** Decide whether common-subspace projection is a valid
mechanism-aware intervention for common/rare gradient conflict.

**Decision question:** Does freezing the harmful common/rare conflict subspace
and suppressing it in the routing / selected update path reduce
routing-weighted conflict enough to beat dense shared rare loss?

**Not in scope:** general semantic experts, real-corpus utility, many-expert
scaling, or claiming that high route NMI proves expert value. This anchor also
does not replace A06 preservation; it is a candidate A07 intervention after a
non-collapsed or controlled partition surface exists.

## 2. Physical Priors

**P1: Frequent common updates can dilute rare conflict gradients.**  
Frequent common patterns can create stable high-gain singular or update
directions. Reuse is efficient when the rare pattern shares the same function,
but harmful when repeated common updates overwrite the rare correction before
rare examples accumulate enough update mass.

**P2: Routing overlap is harmful only when overlap carries conflicting update
pressure.**  
Putting $C$ and $R$ in the same expert is not automatically bad. It becomes a
mechanism only when shared experts carry negative gradient cosine or when rare
updates are absorbed by a common projector that common updates keep reinforcing.

**P3: Projection must be judged against dense.**  
Removing a common component can improve a geometry metric while hurting the
model. The intervention is only useful if rare loss improves, common loss is
preserved, and the strong claim beats or closes the dense-shared rare-loss
boundary.

## 3. Falsifiable Hypotheses

**H1: Stable conflict-subspace absorption exists.**  
Supported if frozen raw-gradient and AdamW-update conflict projectors are
stable over the audit window and rare updates have higher conflict-subspace
mass than shuffled, random, or nuisance controls. Weakened if the projectors
drift, rare updates do not project into them, or the signal is explained by
update norm / frequency / load.

**H2: Projected routing reduces common/rare conflict.**  
Supported if a router using $(I-P_C)h$ reduces
$\mathcal{C}_{C,R}$ against random top-1 and centered-unsupervised MoE under
matched load and capacity guards. Weakened if the reduction is absent or only
explained by load balance.

**H3: Conflict update suppression is needed for dense-beating gain.**  
Supported if router-only projection is insufficient but adding selected
preconditioned-update suppression plus common confidence gating improves $L_R$
to beat or close the dense boundary without unacceptable $L_C$ regression.
Weakened if projected updates do not reduce conflict mass or rare loss does not
beat dense.

## 4. Mathematical Model

**Objects:** feature labels $f\in\{C,R\}$, expert $e$, route probability
$q_{f,e}$, per-expert gradient $g_{f,e}$, frozen common projector $P_C$, AdamW
preconditioned update $u_t$, conflict projector $P_{\mathrm{conflict},e}$,
and projection strength $\rho_t$.

**Conflict metric inherited from A07_04:**

$$
\mathcal{C}_{C,R}=\sum_e q_{C,e}q_{R,e}[-\cos(g_{C,e},g_{R,e})]_+.
$$

**Conflict-subspace absorption gate:**

$$
\alpha_R^{\mathrm{conflict}}=
\frac{\|P_{\mathrm{conflict}}u_R\|^2}{\|u_R\|^2+\epsilon}.
$$

**Projected router input:**

$$
h_\perp=(I-P_{\mathrm{conflict}})h.
$$

**Selected update-space suppression:**

$$
\tilde u_t=r_t(I-\rho_tP_{\mathrm{conflict},e})u_t.
$$

Here $r_t$ is a residual learning gate. In the first implementation it is a
group/confidence gate that suppresses already-learned common examples more than
active rare examples, directly targeting the frequency imbalance that dilutes
rare conflict gradients.

**Mechanism relation:** If rare loss is harmed because frequent common updates
dilute the rare conflict gradient, then reducing $q_{C,e}q_{R,e}$ for
conflicting experts and reducing $P_{\mathrm{conflict}}u_R$ should reduce
$\mathcal{C}_{C,R}$ and lower $L_R$ enough to beat dense shared.

**Falsifier:** The diagnostic gate fails, or projection reduces a geometry
metric but does not reduce $\mathcal{C}_{C,R}$ and $L_R$ under matched guards.

## 5. Computational Realization

**Input objects:** the controlled neural common/rare surface used by A07_04 or
a direct successor with matched dense, random top-1, centered split, and oracle
guards; common/rare labels for audit only; reconstructable update directions or
optimizer state.

**Computed variables:** $P_C$, projector drift, $\alpha_R^C$, route
distributions $q_{f,e}$, per-expert gradients $g_{f,e}$,
$\mathcal{C}_{C,R}$, $L_R$, $L_C$, max load, active experts, and selected-block
update projection fractions.

**Algorithm stages:** run A07_06a diagnostic first; if it passes or the user
waives the gate, run A07_06b projected MoE with common-projection, conflict
router, and conflict-router-plus-update conditions; compare against dense,
random top-1, centered split, and oracle controls.

**Stage-local evidence:** projector stability table, rare update absorption
table, route/conflict table, loss guard table, load guard table, and
projection-fraction table.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`,
`tables/projector_diagnostic.csv`, `tables/common_rare_gradient_conflict.csv`,
`tables/common_rare_loss_guard.csv`, `tables/load_guard.csv`,
`figures/conflict_vs_rare_loss.png`, and
`figures/update_projection_fraction.png`.

## 6. Minimal Falsification Tests

**Test 1: conflict-subspace absorption diagnostic.**  
Question: do rare updates actually reuse a stable harmful common/rare conflict
subspace?  
Primary metric: $\alpha_R^{\mathrm{conflict}}$ above shuffled and nuisance
controls, measured for both raw gradients and AdamW-update directions, with
projector stability as a required guard.  
Supports: $P_{\mathrm{conflict}}$ is stable and rare conflict mass is
materially above controls.  
Weakens: $P_{\mathrm{conflict}}$ drifts, rare updates do not project into it, or the signal is
explained by update norm, frequency, position, or load.  
Failure meaning: projected MoE would be premature; return to proxy/router
definition rather than method construction.

**Test 2: projected-router conflict split.**  
Question: does routing on $h_\perp=(I-P_{\mathrm{conflict}})h$ reduce measured common/rare
gradient conflict?  
Primary metric: $\Delta\mathcal{C}_{C,R}$ versus random top-1 and
centered-unsupervised split.  
Supports: conflict falls under matched load/capacity guards.  
Weakens: conflict does not fall or the improvement is load-only.  
Failure meaning: common projection may not define the relevant routing axis.

**Test 3: projected-update rare-loss guard.**  
Question: does adding selected update-space suppression improve rare loss while
preserving common loss?  
Primary guard: $L_R$ improves versus random top-1 and centered split, with
$L_C$ stable. Strong support requires rare loss to beat dense shared or close
the dense gap within the pre-registered tolerance.  
Weakens: projection lowers conflict but $L_R$ does not improve, or $L_C$
regresses enough to show transferred harm.  
Failure meaning: the intervention changes geometry but not functional expert
utility.

## 7. Current Evidence

**Observation:** A07_06 full 4GPU audit completed on 2026-06-28 as ACP job
`pt-gwnh6l71`. The full method `conflict_projected_router_update_moe` improved
rare loss versus random top-1 by `0.2848`, versus centered split by `0.2155`,
and beat dense shared rare loss by `0.1538`, while common-loss regression
versus random was `0.0292`.
**Interpretation:** the method has a controlled-surface rare-loss positive
signal.
**Boundary:** rare accuracy did not improve, so this is not a rare-feature
recovery closure.
**Evidence links:** `../../experiments/A07/A07_06b_projected_moe_conflict_splitting/summary.md`,
`../../experiments/A07/A07_06b_projected_moe_conflict_splitting/detailed.md`.

**Observation:** Route-level conflict reduction was tiny:
`delta_conflict_vs_random_top1 = 0.0036` and
`delta_conflict_vs_centered = 0.0010`.
**Interpretation:** the run does not show that routing-weighted conflict
splitting explains the rare-loss improvement.
**Boundary:** this weakens the anchor's intended mechanism, even though the
loss guard moved in the desired direction.

**Observation:** The raw conflict projector captured high rare mass
(`0.7934`, `7.85x` random control) but had low stability (`0.3309`). The
AdamW-like projector was more stable (`0.7327`) but captured lower rare mass
(`0.1690`).
**Interpretation:** there is a projection signal, but the frozen object is not
yet cleanly identified.
**Boundary:** do not claim stable conflict-subspace isolation from this run.

**Observation:** A07_04 measured real neural common/rare gradient conflict.
Centered unsupervised split weakly reduced conflict versus random top-1, but
rare-loss improvement was small and dense shared training had lower rare loss.
**Interpretation:** common/rare conflict is measurable, but the current router
is not sufficient evidence for MoE utility.

**Observation:** A07_05 found rare updates overlap a stable common-update
subspace and common updates cause a small direction-specific rare-loss harm,
but the primary effect was below the pass threshold.  
**Interpretation:** common-update interference is a mechanism reserve, not a
supported strong mechanism.

**Observation:** The 2026-06-25 C3S and two-phase singular-mode notes argue
that common high-gain directions can continue to grow after direction discovery
and that update-space suppression gives a geometric guarantee.  
**Interpretation:** this is a plausible intervention principle, but it is not
yet project evidence that projected MoE improves rare loss.

**Observation:** A07_01/A07_02 nested retarget run `a07_nested_full_20260628_2`
now reproduces a controlled rank-one common-backbone surface and shows that
combined confidence gating plus common-subspace suppression improves tail loss
by `0.1075` while reducing $\alpha_{\mathrm{tail}}$ by `0.1204`.
**Interpretation:** this supports the update-space target that A07_06 tried to
approximate, but it also sharpens the A07_06 failure: the reliable mechanism
metric is tail update concentration in a frozen common subspace, not
route-level conflict reduction alone.
**Boundary:** the new nested result does not validate A07_06 projected MoE or
its dense-beating route-utility claim.
**Evidence links:** `../../experiments/A07/A07_01_nested_common_backbone_reproduction/summary.md`,
`../../experiments/A07/A07_02_nested_tail_common_subspace_control/summary.md`.

**Observation:** A06 real-DCLM proxy routing exists at step 0 but ordinary
training overwrites it by step 5/10.  
**Interpretation:** anti-feedback or preservation remains upstream of broad
real-DCLM utility claims. A07_06 should first be tested on a controlled or
checkpoint-window surface.

## 8. Claim Boundary And Next Decision

**Can claim now:** on the controlled A07 surface, conflict-projected update
suppression with a common confidence gate improved rare loss and beat dense
shared rare loss under the loss metric.

**Cannot claim now:** projected MoE works, dense-beating MoE utility,
real-DCLM expert specialization, semantic experts, rare-feature recovery, or
that routing-weighted conflict reduction caused the gain.

**Next decision:** Run a mechanism separation follow-up: confidence-gate-only,
update-projection-only, AdamW-projector variant, and rare loss / rare accuracy
calibration audit.
