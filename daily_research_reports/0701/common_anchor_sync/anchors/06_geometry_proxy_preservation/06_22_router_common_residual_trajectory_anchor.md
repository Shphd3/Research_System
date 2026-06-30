# A06_22: Router Common-Residual Trajectory Audit

Document status: draft anchor for review. This anchor follows A06_21 and is
intended to decide whether the next real-DCLM preservation audit should focus
on router update trajectories rather than another initialization method.

## 0. Thinking Card

**Phenomenon:** Real-DCLM proxy-center routing can be strong at step 0 but is
erased by early ordinary top-1 training. Controlled A06_21 shows that positive
margins can preserve a partition, but it does not yet explain why real-DCLM
router updates overwrite the proxy partition.

**Mechanism guess:** Router gaps may update toward a hierarchy of common modes
rather than toward feature-residual directions. A single common subtraction may
remove only the most visible common component while leaving class-, context-,
position-, or route-logit common components that still dominate router
trajectory.

**Key variables:** hidden state $h_i(t)$, fixed proxy label $y_i=f$, feature
center $\mu_f(t)$, common-mode projector $P_C$, residual center
$r_f(t)=(I-P_C)\mu_f(t)$, router row $w_e(t)$, assigned expert $a(f)$, router
gap $u_{f,e}(t)=w_{a(f)}(t)-w_e(t)$, router-gap update
$\Delta u_{f,e}(t)=u_{f,e}(t)-u_{f,e}(0)$, common margin term
$\gamma^C_{f,e}(t)$, residual margin term $\gamma^R_{f,e}(t)$, proxy-route
NMI, sign flip rate, and LM loss.

**Causal relation:** If early router-gap updates are dominated by common-mode
directions, then proxy-route NMI can fall even when residual feature
information remains present in hidden states. If updates are residual-aligned
and margins still fail, then the failure is not primarily common-mode router
trajectory.

**Observable metric:** primary metric is the common-over-residual router update
dominance ratio during the step-0 to step-5/10 window, with proxy-route NMI and
LM loss as decision guards.

**Rival Explanations:** weak step-0 residual margin; feature centers drift
across fixed router boundaries; router boundary drift unrelated to common
modes; proxy labels are unstable; expert feedback makes the proxy partition
objective-incompatible; the chosen common projector is wrong.

**Decision:** Pursue this anchor as a diagnostic if common-over-residual update
dominance predicts real-DCLM proxy-route collapse. Revise or park it if NMI
collapse occurs without common-dominated router updates or if common projector
choice determines the conclusion.

## 1. Problem Definition

**Parent problem:** A06 asks how route-relevant proxy or feature partitions can
be found and preserved for top-1 MoE gating.

**Sharper subproblem:** A06_21 explains controlled no-position bridge
preservation through positive margins. The unresolved real-DCLM question is
why ordinary training moves away from a strong step-0 proxy assignment.

**Terminology / Definitions:**

**Router gap:**  
Plain meaning: the pairwise scoring direction separating the originally
assigned expert from a competing expert.  
Concrete object:

$$
u_{f,e}(t)=w_{a(f)}(t)-w_e(t).
$$

Why it matters: router specialization is determined by which directions these
gaps read.  
Cannot prove: expert utility or semantic specialization.

**Common-mode subspace:**  
Plain meaning: a pre-specified subspace carrying shared, high-frequency, or
high-gain structure across features.  
Concrete object: an orthogonal projector $P_C$ fitted without using the test
route labels.  
Why it matters: if router gaps align to this subspace, routing may become
stable but non-discriminative.  
Cannot prove: that all large singular directions are harmful.

**Feature-residual center:**  
Plain meaning: the part of a feature center left after removing the chosen
common subspace.  
Concrete object:

$$
r_f(t)=(I-P_C)\mu_f(t).
$$

Why it matters: this is the candidate direction that should carry
feature-specific route identity.  
Cannot prove: functional expert value by itself.

**Common-over-residual update dominance:**  
Plain meaning: whether router-gap movement is more aligned with common
directions than with feature-residual directions.  
Concrete computation:

$$
\Lambda_{\mathrm{upd}}(t)
=
\operatorname{median}_{f,e}
\frac{
\left|\Delta u_{f,e}(t)^\top P_C\mu_f(0)\right|
}{
\left|\Delta u_{f,e}(t)^\top r_f(0)\right|+\varepsilon
}.
$$

Why it matters: it directly tests whether early router movement is common
dominated.  
Cannot prove: that common dominance causes collapse unless paired with NMI
drop and margin sign changes.

**Decision question:** In real-DCLM proxy-init training, are early router-gap
updates dominated by common-mode hierarchy rather than feature-residual
directions, and does that dominance explain proxy-route collapse?

**Not in scope:** constructing a new gating method, proving semantic experts,
claiming utility, or replacing the A06_21 margin-budget model.

## 2. Physical Priors

**P1: Top-1 gating reads directions, not labels.**  
Meaning: route assignment is controlled by dot products between router rows
and hidden states. If router gaps align with common directions, labels can be
lost even when residual feature information exists.  
Could be wrong if: route collapse occurs while router gaps remain residual
aligned and common terms stay small.

**P2: Common structure can be hierarchical.**  
Meaning: removing a single global mean or top common direction may leave
class-, context-, position-, or route-logit common components that still guide
router updates.  
Could be wrong if: after one well-defined common removal, router update
dominance reliably shifts to residual feature directions.

**P3: Preservation requires residual-discriminative margin, not just positive
margin.**  
Meaning: a positive margin can preserve a stable assignment, but for
feature-level specialization the margin should come from residual feature
contrast rather than common-mode score.  
Could be wrong if: common-dominated margins still predict feature identity and
later expert utility.

## 3. Falsifiable Hypotheses

**H1 common-trajectory hypothesis:** Early real-DCLM router-gap updates are
dominated by common-mode directions.  
Supported if: $\Lambda_{\mathrm{upd}}(5)$ or $\Lambda_{\mathrm{upd}}(10)$ is
greater than 1 across seeds and conditions, and common update terms coincide
with falling proxy-route NMI.  
Weakened if: router-gap updates are residual-aligned while NMI still falls.

**H2 residual-margin insufficiency hypothesis:** Step-0 proxy routing is
fragile because residual margin is weak even when total margin or NMI looks
strong.  
Supported if: $\gamma^R_{f,e}(0)$ is small or negative for many pairs despite
high step-0 proxy-route NMI.  
Weakened if: residual margins are strong at step 0 and are consumed only after
training drift.

**H3 common-projector robustness hypothesis:** The conclusion is not an
artifact of one common definition.  
Supported if: mean-common, top-band common, and route-logit common projectors
produce the same qualitative common-over-residual trajectory result.  
Weakened if: the result flips depending on the chosen common projector.

## 4. Mathematical Model

**Objects:** fixed proxy labels $y_i=f$, feature centers $\mu_f(t)$, common
projector $P_C$, residual centers $r_f(t)=(I-P_C)\mu_f(t)$, router rows
$w_e(t)$, assigned expert $a(f)$, router gaps $u_{f,e}(t)$, and router-gap
updates $\Delta u_{f,e}(t)$.

**Core decomposition:** split the pairwise margin into common and residual
terms:

$$
\gamma_{f,e}(t)
=
u_{f,e}(t)^\top \mu_f(t)
=
\underbrace{u_{f,e}(t)^\top P_C\mu_f(t)}_{\gamma^C_{f,e}(t)}
+
\underbrace{u_{f,e}(t)^\top r_f(t)}_{\gamma^R_{f,e}(t)}.
$$

Split the router-side margin update using the same geometry:

$$
\Delta \gamma^{\mathrm{router}}_{f,e}(t)
=
\Delta u_{f,e}(t)^\top \mu_f(0)
=
\Delta u_{f,e}(t)^\top P_C\mu_f(0)
+
\Delta u_{f,e}(t)^\top r_f(0).
$$

Define the common-over-residual update dominance ratio:

$$
\Lambda_{\mathrm{upd}}(t)
=
\operatorname{median}_{f,e}
\frac{
\left|\Delta u_{f,e}(t)^\top P_C\mu_f(0)\right|
}{
\left|\Delta u_{f,e}(t)^\top r_f(0)\right|+\varepsilon
}.
$$

**Mechanism relation:** if $\Lambda_{\mathrm{upd}}(t)>1$ while proxy-route NMI
falls and residual margins shrink or fail to grow, then the data support a
common-dominated router trajectory. If $\Lambda_{\mathrm{upd}}(t)<1$ or
residual terms dominate while NMI still falls, then common-mode trajectory is
not the main explanation.

**Observable metrics:** proxy-route NMI at steps 5/10, LM loss, load
concentration, sign flip rate, $\gamma^C$, $\gamma^R$,
$\Lambda_{\mathrm{upd}}$, residual margin share, and common-projector
robustness.

**Falsifier:** proxy-route collapse does not track common update dominance,
residual margin loss, or any common/residual decomposition under multiple
common definitions.

## 5. Computational Realization

**Input objects:** real-DCLM A06_12-style proxy-init checkpoints with hidden
states at the routed position, fixed proxy labels, router rows, route
assignments, LM loss, and expert load.

**Computed variables:** feature centers, multiple common projectors, residual
centers, initial feature-to-expert matching, router gaps, router-gap updates,
common/residual margin terms, update dominance ratios, sign flips, NMI, and
loss/load guards.

**Algorithm stages:** collect checkpoints; fit common projectors without test
label leakage; compute center and residual terms; decompose router-gap updates
from step 0 to steps 5/10; compare against proxy-route NMI collapse and LM
loss; check robustness across common definitions.

**Stage-local evidence:** per-pair common/residual margin table, per-step
trajectory summary, common-projector comparison table, NMI/loss/load guard
table, and common-vs-residual update plot.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`,
`tables/common_residual_margin_by_pair.csv`,
`tables/router_update_trajectory.csv`,
`tables/common_projector_robustness.csv`, and figures for NMI vs update
dominance, common/residual margin trajectories, and router-gap alignment.

## 6. Minimal Falsification Tests

| Test | Question | Primary metric | Pass / fail / insufficient | Failure means |
|---|---|---|---|---|
| Router trajectory audit | Do early router gaps move more along common modes than residual feature directions? | $\Lambda_{\mathrm{upd}}@5/10$ plus proxy-route NMI | Pass if common dominance coincides with NMI collapse; fail if residual updates dominate or no relation exists; insufficient if checkpoints or router rows are missing. | Weakens H1 or exposes that collapse is not router-trajectory common dominance. |
| Residual margin audit | Was the step-0 proxy partition already residual-fragile? | $\gamma^R_{f,e}(0)$ and residual margin share | Pass if high NMI coexists with weak residual margin; fail if residual margins are strong and only later consumed. | Revises H2 toward training drift rather than weak initialization. |
| Common-definition robustness | Is the common-dominance result stable across common definitions? | agreement across mean, top-band, and route-logit projectors | Pass if all give the same qualitative dominance result; fail if the conclusion flips. | Weakens H3 and makes the common definition the bottleneck. |

## 7. Current Evidence

**Observation:** A06_12 shows real-DCLM raw-center proxy routing is strong at
step 0 but collapses by step 5/10 under ordinary training while LM loss remains
acceptable.

**Observation:** A06_20 shows a simple route-logit common estimator changes
load but does not recover feature residual geometry better than controls. This
weakens a single-step common subtraction method but does not falsify a
hierarchical or dynamic common-mode trajectory explanation.

**Observation:** A06_21 shows that in the controlled no-position bridge,
center-init preservation is explained by positive margins surviving training
drift; common share remains low in preserved center-init conditions. This
supports using common/residual margin terms as guards but does not yet explain
real-DCLM collapse.

**Interpretation:** The active uncertainty is not whether margins matter in
the controlled bridge. It is whether real-DCLM router updates erase proxy
routing by aligning to common-mode hierarchy rather than residual feature
contrast.

**Boundary:** Current evidence motivates this diagnostic anchor. It does not
yet support a new gating method or a claim that common dominance causes
real-DCLM collapse.

**Evidence links:**

- `../../experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md`
- `../../experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/summary.md`
- `../../experiments/A06/A06_21_margin_budget_preservation_audit/summary.md`

## 8. Claim Boundary And Next Decision

**Can claim if supported:** real-DCLM proxy routing collapse is associated with
router-gap updates that are common-dominated rather than residual-feature
aligned during the step-0 to step-5/10 window.

**Cannot claim:** common-dominated trajectory alone proves lack of expert
utility, common removal will solve preservation, long-tail residuals are
meaningless, or a new gating architecture is validated.

**Next decision:** write a minimal protocol to apply this common/residual
router-trajectory audit to A06_12-style real-DCLM proxy-init checkpoints.
