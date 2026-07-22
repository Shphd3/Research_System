# A07: Common-Update Interference Diagnostic

Document status: compressed mechanism-reserve draft. This is not an approved
protocol and does not replace A06 preservation.

## 0. Thinking Card

**Phenomenon:** Rare or conflict examples may stay hard after common patterns
are learned. One possible reason is that rare updates reuse directions already
dominated by common examples.

**Mechanism guess:** Common examples create a stable update subspace. Rare
examples then project into that subspace, and common updates can push parameters
in a direction that hurts rare loss.

**Key variables:** common examples, rare/conflict examples, common-update
projector $P_C$, rare update $u_R$, rare common-update fraction
$\alpha_R^C$, common-to-rare loss effect $\Delta L_{R|C}$.

**Causal relation:** If common-update interference is real, rare updates should
have elevated projection into the common subspace, and applying a common update
should increase rare loss more than matched controls.

**Observable metric:** primary metric is
`common_to_rare_loss_effect`; `rare_common_update_fraction` and a gated
real-data observational bridge are diagnostic guards.

**Alternative explanation:** Rare failure may come from data scarcity, capacity,
label noise, unstable routing, or a bad rare validation surface rather than
common-update interference.

**Decision:** Pursue A07 utility only if common updates causally damage rare
loss on a controlled nested-conflict surface. After that pass, run a small
real-data observational bridge before promoting a partition-value anchor. Revise
if overlap is high but not harmful. Park if rare failure is explained by data,
capacity, or measurement noise.

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
$\alpha_R^C$. Weakened if rare loss is high but common updates do not harm rare
loss after controls.

## 4. Mathematical Model

**Objects:** $P_C$ is the common-update projector, $u_R$ is a rare-example
update, $\alpha_R^C$ is rare update mass in the common subspace, and
$\Delta L_{R|C}$ is rare-loss change after a common update.

**Core model:** Estimate a common-update projector from common-example updates:

$$
P_C = U_C U_C^\top.
$$

Measure how much of a rare update lies in that common subspace:

$$
\alpha_R^C = \frac{\|P_C u_R\|^2}{\|u_R\|^2+\epsilon}.
$$

**Mechanism relation:** Test causal harm by applying a small common update and
measuring rare loss:

$$
\Delta L_{R|C}=L_R(\theta-\eta \bar u_C)-L_R(\theta).
$$

**Observable metric:** `common_to_rare_loss_effect`, guarded by
`rare_common_update_fraction`, common loss, and update norm.

**Falsifier:** $\Delta L_{R|C}$ is not positive relative to matched controls,
even when rare loss is high.

## 5. Computational Realization

**Input objects:** controlled nested-conflict sequence task, common/rare labels,
model checkpoints, and update directions or optimizer state; optional
real-DCLM proxy/common/rare group definitions if they already exist.

**Computed variables:** $P_C$, $\alpha_R^C$, $\Delta L_{R|C}$, rare loss,
common loss, and update norms.

**Algorithm stages:** train/load a small model; estimate $P_C$ after common
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

Guards: projector stability, rare underlearning window, $\alpha_R^C$, common
loss, update norm, data/capacity controls, and real-data bridge only after the
controlled perturbation passes.

## 7. Current Evidence

**Observation:** Controlled A07 experiments already support a value chain where
common-control can improve rare loss beyond load-only baselines and route
function binding can be measured. A07_04 is insufficient evidence for the full
neural proxy conflict-splitting claim.

**Interpretation:** This draft asks for a cleaner mechanism audit: is the value
actually tied to common-update interference, and is that mechanism worth
porting toward the real-DCLM proxy surface?

**Boundary:** This is a mechanism reserve. It should not be promoted to real-DCLM
utility until A06 preservation is solved or a controlled utility surface is
explicitly chosen.

**Evidence links:**

- `Projects/from-attention-to-search/main/experiments/A07/A07_01_common_rare_conflict_metric_audit/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_02_common_controlled_rare_interference/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_03_route_function_binding/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md`

## 8. Claim Boundary And Next Decision

**Can claim if passed:** common-example updates causally interfere with rare
loss on the tested controlled surface. If the real-data bridge is compatible,
the mechanism is worth testing in a partition-value anchor.

**Cannot claim:** preserved real-DCLM expert utility, semantic experts, or that
MoE partitioning is already the right intervention.

**Next decision:** If the perturbation test passes and the real-data bridge is
compatible, write a separate partition-value anchor asking whether common/rare
routing reduces both interference and rare loss under load/capacity guards. If
the perturbation fails, park common-update interference. If perturbation passes
but the bridge fails, keep A07 as controlled mechanism reserve and revise the
real-data group definition.
