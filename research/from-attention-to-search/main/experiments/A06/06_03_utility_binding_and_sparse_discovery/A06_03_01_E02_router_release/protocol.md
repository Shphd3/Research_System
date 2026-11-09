# Protocol: A06_03_01_E02 Specialist-Generalist Router Release

## 0. Approval Snapshot

**Approval status:** Approved for execution under the persistent research goal on 2026-07-10.

**Purpose:** Determine whether expert specialization value changes multi-step native weighted-top-1 router dynamics in a task-beneficial way when representation and router start identically.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`

**Decision question:** Does replacing generalists with specialists produce larger assigned-margin growth after router release while retaining lower native task loss?

**Physical prior tested:** A value-aligned gate should convert relative expert utility into task-beneficial route dynamics rather than merely respond to residual-error magnitude.

**Core model term:** \(D_m(T)=\operatorname{median}_{f,seed}[\Delta m_f^{spec}(T)-\Delta m_f^{gen}(T)]\).

**Falsifier:** Specialists retain lower native task loss but have no larger margin growth than generalists from the identical router state.

**Experiment role:** Root-cause audit, not method construction.

**Primary metric:** Specialist-minus-generalist paired cumulative matched-margin growth at router-only SGD horizon 50.

**Minimal setup:** Deterministically rebuild A06_03_01_E01 specialist/generalist expert-only checkpoints; verify exact non-expert state identity and utility reproduction; freeze experts and representation; release only the router under native full-sequence weighted-top-1 LM loss.

**Conditions:** specialist/generalist router-only SGD; specialist/generalist router-only AdamW; specialist/generalist joint AdamW transfer.

**Pass for value-aligned transmission:** \(D_m(50)>0\) with seed-clustered 95% CI lower bound above zero, specialist native task loss remains lower, and validity guards pass.

**Support for transmission misalignment:** specialist native task-loss advantage has CI lower bound above zero while \(D_m(50)\) has CI upper bound below or equal to zero.

**Insufficient:** exposure reproduction fails; non-expert state mismatch; initial route mismatch; utility floors are not finite; fewer than 32 seeds; or route loss diverges.

**Cannot claim:** Natural-language semantic routing, from-scratch task discovery, real downstream benefit, or that a new gate is already necessary or optimal.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Specialist start | Experts trained only on their assigned context task | A06_03_01_E01 correct expert-only checkpoint | model state | positive utility start | natural semantics |
| Generalist start | Experts trained equally on all tasks | A06_03_01_E01 shuffled expert-only checkpoint | model state | load-matched control | useless experts |
| Router release | Stop forcing expert identity and train the native weighted-top-1 router | router optimizer steps | updates | tests utility-to-route handoff | from-scratch discovery |
| Margin growth | Change in assigned expert's minimum score lead | \(m_f(t)-m_f(0)\) | logit margin | route-strength trajectory | task value |
| Margin-growth contrast | Specialist minus generalist margin growth | \(D_m(T)\) | logit margin | primary causal metric | system efficiency |
| Forced floor | Loss when the assigned expert is forced with probability one | \(L_{f,f}^{cf}\) | nats/task-token | expert-function lower bound | native route quality |
| Routing excess loss | Native loss above the forced floor | \(E_f(t)=L_f^{native}(t)-L_{f,f}^{cf}(t)\) | nats/task-token | isolates routing inefficiency | total task difficulty |
| Normalized excess | Fraction of initial routing excess remaining | \(R_f(t)=E_f(t)/E_f(0)\) | ratio | update-efficiency comparison | wall-clock efficiency |

## 2. Anchor Alignment

**Decision question:** Whether learned expert function changes multi-step router dynamics from an identical non-expert state.

**Physical prior:** Relative utility should affect a value-aligned route trajectory; selected-benefit magnitude alone is insufficient.

**Falsifier:** Lower specialist task loss with nonpositive specialist-minus-generalist margin-growth contrast.

**Claim boundary:** Controlled context task and staged release only.

## 3. Tested Hypotheses

- **H1 task value:** Specialist-start native task loss remains below generalist-start loss at horizon 50, with positive paired generalist-minus-specialist loss CI.
- **H2 route transmission:** Router-only SGD \(D_m(50)>0\) with positive clustered-CI lower bound.
- **H3 trajectory misalignment:** H1 passes while \(D_m(50)\le0\) with nonpositive CI upper bound.
- **H4 optimizer transfer:** The sign of \(D_m(50)\) is unchanged under router-only AdamW.
- **H5 joint transfer:** The qualitative route/task relation survives joint AdamW release.

## 4. Rival Explanations

1. The one-step pressure reversal is transient. Multi-step release directly tests it.
2. Different representations or routers create the contrast. Exact non-expert state identity is required before release.
3. Specialist/generalist checkpoints are not reproduced. Counterfactual utility matrices and native losses are checked before release.
4. Absolute loss floors create a false efficiency gap. Normalized routing excess uses each condition's own forced floor.
5. SGD-specific scaling creates the result. Router-only AdamW checks sign transfer without changing the primary causal surface.
6. Frozen experts are unrealistic. Joint AdamW is secondary transfer evidence only.

## 5. Data / Model / Objective

Reuse A06_03_01_E01 exactly:

- four equally frequent sequence-level modular transformation tasks;
- one instruction plus sixteen content/output pairs, length 33;
- 32 train and 32 disjoint held-out sequences per seed;
- all 32 next-token positions in the LM objective;
- one causal attention layer, fixed instruction-state visibility control, residual plus LayerNorm, no learned positional embedding;
- four MLP experts, fixed readout, weighted top-1 router.

Exposure reconstruction uses 200 expert-only updates with A06_03_01_E01 optimizer and balanced controls. Release uses native routing; forced assignments are disabled.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Rival explanation | Why needed | Evidence role | Pass | Fail | Insufficient | Artifact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Specialist router-only SGD | H1/H2/H3 | one-step artifact | primary treatment | primary | task value + positive \(D_m\) | task value + nonpositive \(D_m\) | state mismatch | margin/loss curves |
| Generalist router-only SGD | H1/H2/H3 | residual-error route growth | primary paired control | primary | paired comparison valid | -- | utility not reproduced | margin/loss curves |
| Specialist/generalist router-only AdamW | H4 | SGD-only effect | optimizer transfer | secondary | same sign relation | sign reversal | numerical failure | optimizer table |
| Specialist/generalist joint AdamW | H5 | frozen-path artifact | native-training transfer | secondary | same qualitative relation | transfer fails | utility destroyed at start | joint curves |

Seeds: 0--31. Exposure steps: 200. Release steps: 50. Release checkpoints: 0, 1, 2, 5, 10, 20, 50. Smoke: two seeds, exposure 20, release 10.

Primary SGD router learning rate: \(10^{-4}\). Router-only AdamW learning rate: 0.001. Joint AdamW uses router 0.001, experts 0.001, and representation 0.0005.

## 7. Primary Metric

For task \(f\) and start type \(z\in\{spec,gen\}\):

\[
\Delta m_f^z(T)=m_f^z(T)-m_f^z(0).
\]

The primary paired metric is

\[
D_m(T)
=
\operatorname{median}_{f,seed}
\left[\Delta m_f^{spec}(T)-\Delta m_f^{gen}(T)\right].
\]

Use a seed-clustered bootstrap 95% CI. Positive \(D_m\) supports value-aligned transmission. Nonpositive upper CI with preserved specialist task value supports misalignment. An interval crossing zero is inconclusive.

## 8. Training-Efficiency And Secondary Metrics

For each task, use its own forced assigned-expert floor:

\[
R_f(t)
=
\frac{L_f^{native}(t)-L_{f,f}^{cf}(t)}
{L_f^{native}(0)-L_{f,f}^{cf}(0)}.
\]

Report median \(R_f(t)\), area under the normalized-excess curve, and first checkpoint with \(R_f\le0.1\). This measures router optimization efficiency without treating different expert floors as routing effects.

Other metrics:

- paired native task-loss advantage \(L^{gen}-L^{spec}\);
- route NMI, route accuracy, and p05 margin;
- counterfactual utility gap retention;
- selected-benefit pressure and actual router update projection;
- finite-step margin closure;
- joint representation/expert drift.

## 9. Known Good / Bad / Confusing Cases

- Known good: exposure reconstruction should reproduce specialist gap above 5, generalist absolute gap below 0.5, native route NMI 1, and exact non-expert identity.
- Known bad: any pre-release router or representation difference invalidates causal attribution.
- Known confusing: both specialists and generalists may receive positive margin growth. The decision is their paired difference plus task value, not absolute sign.
- Known confusing: smaller specialist raw gradient can still be sufficient for stable routing. Negative \(D_m\) means lack of value calibration, not collapse.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Pass / fail / unclear | Debug artifact | Handoff |
| --- | --- | --- | --- | --- |
| Rebuild exposure | Are A06_03_01_E01 utility matrices reproduced? | specialist >5; generalist absolute <0.5 | pre-release utility table | validity |
| State identity | Are non-expert states identical? | max error \(\le10^{-7}\) | state audit | validity |
| Release step 0 | Are route NMI and margins matched? | exact paired agreement | initial audit | validity |
| Early release | Does one-step pressure ordering reproduce? | record, not pass/fail | pressure table | mechanism |
| Horizon 50 | What are \(D_m\), task loss, and normalized excess? | preregistered CI rules | central figures | decision |
| Transfer | Does sign survive AdamW/joint release? | qualitative sign table | transfer figures | next anchor |

## 11. Plot Contracts

### Figure 1: Paired Margin-Growth Contrast

- Question: Does specialist utility create stronger multi-step route growth?
- Metric: median paired \(\Delta m^{spec}-\Delta m^{gen}\).
- X-axis: release step; Y-axis: logit-margin contrast.
- Positive supports value-aligned transmission; nonpositive with specialist task value supports misalignment.
- Limitation: controlled context task only.

### Figure 2: Native Task Loss And Routing Excess

- Question: Do specialists keep task value, and how efficiently does the router approach each expert floor?
- Metrics: native task loss and normalized routing excess \(R_f(t)\).
- Limitation: activated compute is identical and system cost is not measured.

### Figure 3: Utility, Pressure, And Actual Margin Movement

- Question: Does the A06_03_01_E01 one-step mismatch persist in actual updates?
- Metrics: counterfactual utility gap, selected-benefit pressure, actual margin change.
- Limitation: does not identify an optimal alternative gate.

## 12. Success / Failure / Insufficient Evidence

**Value-aligned transmission:** H1 and H2 pass with all guards.

**Transmission misalignment:** H1 passes and H3 passes; specialists provide task value but receive no stronger route growth.

**No task-value retention:** H1 fails; do not interpret \(D_m\) as specialization alignment.

**Insufficient:** Any state, reproduction, coverage, finite-value, or closure guard fails.

## 13. What This Cannot Claim

No natural-language semantic specialization, no from-scratch routing discovery, no real benchmark gain, no compute-efficiency scaling, and no proof that a relative-utility gate is necessary or optimal.

## 14. Review Notes

- Router-only SGD is primary because it preserves the A06_03_01_E01 local pressure equation.
- Router-only AdamW checks optimizer transfer.
- Joint AdamW is a secondary realism bridge and cannot rewrite the primary causal result.
- All release optimizers start with empty optimizer state; exposure-stage AdamW moments are not transferred.
- The experiment advances the specialization definition from utility formation to utility-to-routing handoff.
