# Feedback Common Preservation Bridge Anchor

## 0. Thinking Card

**Phenomenon:** Real-DCLM proxy routing can be aligned at step 0, but ordinary
training erases the proxy partition by step 5/10.

**Mechanism guess:** Training introduces or amplifies a shared feedback drift
that pushes gate inputs toward a common-margin direction. This feedback common
can overwrite route-relevant residual structure even when the step-0 proxy
router is valid.

**Key variables:** Step-0 hidden state $h_0$, later hidden state $h_t$, drift
$\Delta h_t=h_t-h_0$, feedback projector $P_{\mathrm{fb}}$, proxy labels,
router logits, proxy-route NMI, common margin, and residual drift.

**Causal relation:** If feedback common is the preservation failure mechanism,
then replaying $P_{\mathrm{fb}}\Delta h$ should explain most of the step-0 to
step-5/10 proxy-route NMI collapse, while removing
$P_{\mathrm{fb}}\Delta h$ from the full drift should rescue the proxy route.

**Observable metric:** `proxy_nmi_drop_explained_by_feedback_common`, the
fraction of full proxy-route NMI drop reproduced by replaying only the
feedback-common drift.

**Rival Explanations:** Proxy labels may be invalid; collapse may be caused by
group-specific residual drift, expert feedback, optimizer geometry, route-load
imbalance, or activation nuisance rather than shared feedback drift.

**Decision:** If feedback-common replay explains the proxy-route collapse and
feedback-common removal rescues it in controlled settings, carry the bridge to
bounded real-DCLM artifacts. If the real gate-logit bridge fails, decompose the
collapse into gate-weight drift, hidden-state drift, and expert-update feedback
before proposing a method.

## 1. Problem Definition

**Parent problem:** The active preservation bottleneck is that step-0 proxy
routing is overwritten during early training.

**Sharper subproblem:** Decide whether a shared feedback drift can causally
explain and rescue proxy-route collapse.

**Decision question:** Does estimated feedback common explain step-0 to
step-5/10 proxy-route NMI collapse?

**Not in scope:** Proving hidden-state feedback causality from gate-logit
artifacts alone, proving utility, or designing the final anti-feedback method.

## 2. Physical Priors

**P1:** Preservation failure can be dynamic rather than static.

**Meaning:** Step-0 proxy geometry may be valid, but early training can add a
shared drift that changes gate margins and overwrites routing.

**Could be wrong if:** Replaying shared drift does not reproduce collapse, or
removing it does not rescue routing.

**P2:** Feedback common should be tested by causal replay/removal, not only by
subspace stability.

**Meaning:** A drift direction is relevant only if it explains proxy-route NMI
drop under intervention.

**Could be wrong if:** Subspace replay/removal effects are indistinguishable
from random drift projectors.

## 3. Falsifiable Hypotheses

**H1:** Feedback-common drift explains proxy-route collapse.

**Supported if:** $P_{\mathrm{fb}}\Delta h$ alone reproduces most of the NMI
drop caused by full drift.

**Weakened if:** The full drift collapses routing but
$P_{\mathrm{fb}}\Delta h$ does not.

**H2:** Removing feedback common rescues proxy routing.

**Supported if:** $(I-P_{\mathrm{fb}})\Delta h$ preserves substantially more
proxy-route NMI than full drift.

**Weakened if:** Removing feedback common leaves the same collapse.

## 4. Mathematical Model

**Objects:** step-0 hidden state $h_0$, drift $\Delta h$, router $W$, proxy
labels $y$, feedback projector $P_{\mathrm{fb}}$, and route assignment
$r(h)=\arg\max_e (Wh)_e$.

**Drift decomposition:**

$$
\Delta h = P_{\mathrm{fb}}\Delta h + (I-P_{\mathrm{fb}})\Delta h
$$

**Replay interventions:**

$$
h_{\mathrm{full}}=h_0+\Delta h
$$

$$
h_{\mathrm{fb}}=h_0+P_{\mathrm{fb}}\Delta h
$$

$$
h_{\mathrm{res}}=h_0+(I-P_{\mathrm{fb}})\Delta h
$$

**Primary metric:**

$$
\mathrm{drop\_explained}=
\frac{\mathrm{NMI}(r(h_0),y)-\mathrm{NMI}(r(h_{\mathrm{fb}}),y)}
{\mathrm{NMI}(r(h_0),y)-\mathrm{NMI}(r(h_{\mathrm{full}}),y)+\epsilon}
$$

**Rescue metric:**

$$
\mathrm{rescue}=
\frac{\mathrm{NMI}(r(h_{\mathrm{res}}),y)-\mathrm{NMI}(r(h_{\mathrm{full}}),y)}
{\mathrm{NMI}(r(h_0),y)-\mathrm{NMI}(r(h_{\mathrm{full}}),y)+\epsilon}
$$

## 5. Computational Realization

**Input objects:** Controlled hidden states with valid step-0 proxy routing,
known feedback-common drift, residual drift, nuisance drift, and router common
margin.

**Computed variables:** Estimated feedback projector from drift second moment,
random-control projector, route NMI under full replay, feedback-only replay,
residual-only replay, and random-projector replay/removal.

**Algorithm stages:** Generate step-0 proxy geometry; add feedback drift; replay
drift components; compute NMI and load guards; aggregate over seeds.

**Stage-local evidence:** Drop-explained and rescue-fraction tables, plus NMI
trajectory figures.

**Expected artifacts:** controlled `summary.md` / `detailed.md`, real-DCLM
gate-logit bridge `summary.md` / `detailed.md`, bridge tables, and central
NMI / explanation / rescue figures.

## 6. Minimal Falsification Tests

**Test:** Controlled feedback-drift preservation bridge.

**Question:** Can estimated feedback common reproduce and rescue proxy-route
collapse under causal replay/removal?

**Intervention / comparison:** full drift, feedback-only drift, residual-only
drift, and random-projector controls.

**Primary metric:** `proxy_nmi_drop_explained_by_feedback_common`.

**Pass / fail / insufficient:** Pass if feedback-common replay explains most
of the full NMI drop and feedback-common removal rescues most of it in feedback
regimes. Fail if full drift collapses routing but feedback replay/removal does
not explain it. Insufficient if step-0 routing is invalid or random controls
match feedback common.

**Why it decides:** This is the bridge from static common estimation to the
active preservation bottleneck.

**Failure means:** Preservation failure may come from residual drift, expert
feedback, optimizer geometry, or invalid proxy labels rather than feedback
common.

## 7. Current Evidence

**Observation:** `A06_01_04_E03` shows real-DCLM raw-center proxy routing drops sharply
from step 0 to step 5/10. A bounded rerun recovered gate-logit artifacts for
seeds 0/1/2, layers 3/4/5, and checkpoints 0/5/10.

**Observation:** A01_03 supports gradient common as the optimization-common
estimator in controlled mismatch regimes.

**Controlled bridge result:** A01_04 controlled full run passes:
`n_passed_main_feedback_regimes = 2 / 2`, `controls_ok = true`. In
`common_feedback`, step0 NMI is 1.0000, full-drift NMI is 0.0205,
feedback-only NMI is 0.0205, and residual-only NMI is 1.0000. In
`mixed_feedback_residual`, step0 NMI is 1.0000, full-drift NMI is 0.1440,
feedback-only NMI is 0.1028, and residual-only NMI is 1.0000.

**Real-DCLM gate-logit bridge result:** The bounded real run reproduces the
collapse surface, with mean proxy-route NMI dropping from 0.7549 at step 0 to
0.0410 at step 5 and 0.0131 at step 10. But the low-rank feedback-logit bridge
does not pass: `pass=false`, rank-1 `mean_explain_valid=0.4230`, rank-1
`mean_rescue_valid=0.1625`, and random controls are too close
(`mean_random_explain_valid=0.3355`, `mean_random_rescue_valid=0.1177`).

**Interpretation:** Feedback-common replay/removal is a valid controlled
mechanism for proxy-route collapse and rescue. In real DCLM, however, a simple
low-rank gate-logit common drift is not enough to explain or rescue the A06
collapse.

**Boundary:** Gate-logit drift is now tested and weakens the simple low-rank
logit-common explanation. Hidden-state feedback common, separate gate-weight
drift, and expert-update feedback remain unresolved.

**Evidence links:** See
`../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/summary.md`
and
`../../experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/summary.md`
and
`../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/summary.md`
and
`../../experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E03_real_proxy_training_overwrite/summary.md`.

## 8. Claim Boundary And Next Decision

**Can claim:** Feedback-common replay/removal is a valid controlled mechanism
for proxy-route collapse; real gate-logit artifacts reproduce the A06 collapse;
low-rank gate-logit common is insufficient as the main real-DCLM explanation.

**Cannot claim:** Hidden-state feedback common is false, gate-weight drift and
hidden-state drift have been separated, preservation rescue exists in real
DCLM, or method utility follows from the current bridge.

**Next decision:** Decompose the real logit collapse
$z_t-z_0=W_t h_t-W_0 h_0$ into $(W_t-W_0)h_0$, $W_0(h_t-h_0)$, and
$(W_t-W_0)(h_t-h_0)$ before making the real feedback claim or designing an
anti-feedback method.
