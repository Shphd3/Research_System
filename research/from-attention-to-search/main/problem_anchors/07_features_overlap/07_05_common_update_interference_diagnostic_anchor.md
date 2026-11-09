# A07_05: Common-Update Interference Diagnostic

Document status: full controlled run completed on 2026-06-25. Result:
weakened / insufficient for promoting common-update interference as an A07
utility mechanism. It does not replace A06 preservation.


## 1. Problem Definition

**Parent problem:** A07 asks why a preserved partition would have functional
value.

**Sharper subproblem:** Before testing MoE utility, decide whether common-update
interference is a real rare-loss mechanism on a controlled surface.

**Decision question:** Do common-example updates causally hurt rare/conflict
loss beyond norm-matched controls?

**Not in scope:** real-DCLM functional specialization, dense-beating MoE,
semantic experts, many-expert scaling, or replacing A06 preservation. The
real-data bridge is an observational transfer guard, not a utility claim.

## 2. Physical Prior

**P1: Common patterns can create a stable update subspace.**  
Frequent parent patterns are learned earlier and repeatedly, so their update
directions may become a high-gain route for optimization.

**P2: Overlap is not enough; harm must be causal.**  
A rare update can overlap the common subspace without being harmed by common
learning. The mechanism needs a perturbation that worsens rare loss.

## 3. Falsifiable Hypothesis

**H1: Common-update interference is active.**  
Supported if common updates increase rare loss more than norm-matched random or
unrelated updates, during a window where rare updates also show elevated
\(\alpha_R^C\). Weakened if rare loss is high but common updates do not harm rare
loss after controls.

## 4. Mathematical Model

**Objects:** \(P_C\) is the common-update projector, \(u_R\) is a rare-example
update, \(\alpha_R^C\) is rare update mass in the common subspace, and
\(\Delta L_{R|C}\) is rare-loss change after a common update.

**Core model:** Estimate a common-update projector from common-example updates:

\[
P_C = U_C U_C^\top.
\]

Measure how much of a rare update lies in that common subspace:

\[
\alpha_R^C = \frac{\|P_C u_R\|^2}{\|u_R\|^2+\epsilon}.
\]

**Mechanism relation:** Test causal harm by applying a small common update and
measuring rare loss:

\[
\Delta L_{R|C}=L_R(\theta-\eta \bar u_C)-L_R(\theta).
\]

**Observable metric:** `common_to_rare_loss_effect`, guarded by
`rare_common_update_fraction`, common loss, and update norm.

**Falsifier:** \(\Delta L_{R|C}\) is not positive relative to matched controls,
even when rare loss is high.

## 5. Computational Realization

**Input objects:** controlled nested-conflict sequence task, common/rare labels,
model checkpoints, and update directions or optimizer state; optional
real-DCLM proxy/common/rare group definitions if they already exist.

**Computed variables:** \(P_C\), \(\alpha_R^C\), \(\Delta L_{R|C}\), rare loss,
common loss, and update norms.

**Algorithm stages:** train/load a small model; estimate \(P_C\) after common
warmup; compute rare projection; run one-step common-update perturbation with
norm-matched controls.

**Stage-local evidence:** projector stability, rare underlearning window,
perturbation table, loss-effect plot, and optional real-data bridge table.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`,
`tables/causal_perturbation.csv`, optional
`tables/real_data_observational_bridge.csv`, and one plot for rare loss effect.

## 6. Minimal Falsification Tests

| Test | Comparison | Primary metric | Pass / fail / insufficient | Failure means |
|---|---|---|---|---|
| Common-to-rare perturbation | common update vs norm-matched random and unrelated updates | `common_to_rare_loss_effect` | Pass if common update hurts rare loss more than controls; fail if effect is zero or control-matched; insufficient if rare validation or update reconstruction is noisy | common-update interference is not established on this surface |
| Gated real-data observational bridge | real-DCLM proxy/common/rare groups vs shuffled, frequency, or position controls | secondary bridge metrics: projection overlap, nuisance guards, optional group-loss association | Compatible if the same direction is visible above controls; incompatible if signal is absent or nuisance-driven; insufficient if no stable groups exist | controlled mechanism may not transfer to the real-DCLM surface; it does not falsify the controlled perturbation |

Guards: projector stability, rare underlearning window, \(\alpha_R^C\), common
loss, update norm, data/capacity controls, and real-data bridge only after the
controlled perturbation passes.

## 7. Current Evidence

**Observation:** A07_05 full controlled run completed with 8 seeds on a local
two-H100 setup. Common updates increased rare loss more than matched controls,
but the primary effect was small:
`common_to_rare_loss_effect = 0.00168`, below the pre-set `0.005` pass
threshold. The projector guard passed
(`rare_common_update_fraction = 0.22076`,
`projector_stability = 0.85250`), and rare update sanity passed
(`rare_update_sanity_rare_loss_delta = -0.00406`).

**Interpretation:** The direction-specific mechanism is visible but weak. The
result supports "overlap plus small causal harm" rather than a strong
common-update interference mechanism.

**Boundary:** Do not promote this to real-DCLM utility or partition value. The
real-data bridge was not run because the controlled causal perturbation did not
pass the effect threshold.

**Evidence links:**

- `Projects/from-attention-to-search/main/experiments/A07/A07_01_common_rare_conflict_metric_audit/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_02_common_controlled_rare_interference/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_03_route_function_binding/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_05_common_update_interference_diagnostic/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_05_common_update_interference_diagnostic/detailed.md`

## 8. Claim Boundary And Next Decision

**Can claim now:** common-example updates have a small, direction-specific
rare-loss harm on the tested controlled surface, and rare updates overlap a
stable common-update subspace.

**Cannot claim:** a strong common-update interference mechanism, preserved
real-DCLM expert utility, semantic experts, or that MoE partitioning is already
the right intervention.

**Next decision:** Do not write a partition-value anchor from A07_05. Keep
common-update interference as mechanism reserve. Return to A06 preservation
unless a future decision explicitly opens a checkpoint-window audit for this
mechanism.
