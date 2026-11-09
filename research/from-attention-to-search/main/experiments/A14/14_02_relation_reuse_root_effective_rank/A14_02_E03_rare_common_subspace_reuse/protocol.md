---
experiment_id: A14_02_E03_rare_common_subspace_reuse
status: approved_conditional
approved_by: researcher
approved_date: 2026-07-26
execution_scope: run_only_after_e02_capability_rank_common_space_gates
chinese_companion: protocol_cn.md
---

# Protocol: A14_02_E03 Rare–Common Subspace Reuse

## 0. Approval Snapshot

**Approval status:** `PROTOCOLS_APPROVED`, conditional on E02 capability,
rank-validity, and common-space-stability gates.  
**Purpose:** determine whether one rare exposure calling a learned common
mapping creates a non-negligible, historically novel, frozen-readout
functionally necessary direction outside common and old residual spaces.  
**Primary anchor:** [A14_02_02](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_02_rare_common_subspace_reuse_anchor.md).  
**Physical prior:** most task-effective rare update reuses common/old
directions; geometric outside mass is not automatically functional.  
**Strongest rival:** rare exposure requires a new direction, or apparent
outside mass is an AdamW, space-estimation, gauge, or arbitrary-deletion
artifact.  
**Treatment/control:** one batch-size-one rare target versus a matched common
control from the same model and optimizer state.  
**Primary causal metric:** \(\Delta CE_{\mathrm{drop-new}}\).  
**Pass (reuse):** at least eight causal-valid seeds; the rare branch has a
measurable gain, but novel mass is negligible or the one-sided 95% upper bound
of drop-new CE is at most 0.02 nat, with base/random guards passing.  
**Fail (new direction required):** at least eight causal-valid seeds;
\(\rho_{\mathrm{new}}\) is stably non-negligible, the one-sided 95% lower bound
of drop-new CE exceeds 0.02 nat, damage exceeds equal-norm random deletion, and
base behavior is preserved.  
**Insufficient:** no stable measurable rare gain, fewer than eight seeds, E02
gate failure, unstable common/old spaces, or mixed functional evidence.  
**Cannot claim:** all rare facts reuse common mappings, parameter novelty is
semantic novelty, natural-language/multilayer transfer, or NTP-implied H9-F.  
**Approval decision:** `APPROVED, CONDITIONAL ON E02 GATES`.

## 1. Terminology / Definitions

### Target-attributable finite parameter effect

Rare/control begin from identical \(\theta_{\mathrm{ref}}\) and AdamW state and
take one actual step:

\[
v_r
=
\theta_T^{\mathrm{rare}}
-\theta_T^{\mathrm{ctrl}}.
\]

It is a vector in registered non-head parameter coordinates. It is not the
per-example gradient, which is recorded separately.

### Common, outside, old, and new components

\[
v_\parallel=P_cv_r,
\qquad
v_\perp=(I-P_c)v_r,
\]

\[
v_{\mathrm{old}}=P_{\mathrm{old}}v_\perp,
\qquad
v_{\mathrm{new}}=(I-P_c-P_{\mathrm{old}})v_r.
\]

\(G_c\) is fitted on 32 target-free common step contrasts and validated on 32;
\(R_{\mathrm{old}}\) is the 95%-energy basis of the last 64 E02 historical batch
updates after projection into \(G_c^\perp\).

### Geometry fractions

\[
\rho_\perp
=
\frac{\|v_\perp\|_2^2}{\max(\|v_r\|_2^2,\varepsilon)},
\]

\[
\rho_{\mathrm{new}}
=
\frac{\|v_{\mathrm{new}}\|_2^2}{\max(\|v_r\|_2^2,\varepsilon)},
\]

\[
\nu_{\mathrm{new}}
=
\frac{\|v_{\mathrm{new}}\|_2^2}{\max(\|v_\perp\|_2^2,\varepsilon)}.
\]

These are dimensionless energy fractions. Novel mass is non-negligible only if

\[
\rho_{\mathrm{new}}
\ge
\max(0.05,Q_{0.95}(\rho_{\mathrm{new}}^{\mathrm{common-null}})).
\]

They do not prove task or semantic novelty.

### Rare functional gain

\[
\Delta CE_{\mathrm{gain}}
=
CE(\theta_T^{\mathrm{ctrl}})
-CE(\theta_T^{\mathrm{rare}}).
\]

The unit is nat. Causal validity requires at least 0.02 nat improvement on the
preregistered rare-cell/new-context evaluation.

### Exact endpoint drop-new

\[
\theta_T^{\mathrm{drop-new}}
=
\theta_T^{\mathrm{rare}}-v_{\mathrm{new}}
=
\theta_T^{\mathrm{ctrl}}+v_\parallel+v_{\mathrm{old}}.
\]

No further training occurs. Exact forward evaluation defines

\[
\Delta h_{\mathrm{new}}^{\mathrm{exact}}(x)
=
h_\rho(x;\theta_T^{\mathrm{rare}})
-h_\rho(x;\theta_T^{\mathrm{drop-new}}).
\]

The experiment never substitutes \(J_\rho(\theta_\star)v_{\mathrm{new}}\) for
this finite effect.

### Primary causal metric

Using one frozen reference output head,

\[
\Delta CE_{\mathrm{drop-new}}
=
CE(\theta_T^{\mathrm{drop-new}})
-CE(\theta_T^{\mathrm{rare}}).
\]

It is measured in nat; positive values mean deleting the novel component harms
the rare task. The functional margin is 0.02 nat. This metric directly tests
task use; parameter norms cannot replace it.

### Random-removal specificity and base preservation

For 16 equal-norm Haar directions \(z_j\) in the keep-space orthogonal
complement,

\[
\Delta CE_{\mathrm{random},j}
=
CE(\theta_T^{\mathrm{rare}}-z_j)-CE(\theta_T^{\mathrm{rare}}),
\]

\[
\Delta CE_{\mathrm{specific}}
=
\Delta CE_{\mathrm{drop-new}}
-Q_{0.95}(\Delta CE_{\mathrm{random}}).
\]

Necessary novelty requires \(\Delta CE_{\mathrm{specific}}>0\). Base preservation
is

\[
\Delta CE_{\mathrm{base}}
=
CE_{\mathrm{base}}(\theta_T^{\mathrm{drop-new}})
-CE_{\mathrm{base}}(\theta_T^{\mathrm{rare}}),
\]

with \(|\Delta CE_{\mathrm{base}}|\le0.02\) nat.

### Common-space, reconstruction, and auxiliary diagnostics

The prerequisite common-space statistic is

\[
C_{\mathrm{common}}
=\frac{\|P_{G_c}V_{\mathrm{test}}\|_F^2}
{\|V_{\mathrm{test}}\|_F^2}.
\]

Its unit is held-out energy fraction. At least eight E02-valid seeds must reach
\(0.80\) before any rare component may be called `outside-common`. This tests
estimator stability, not functional sufficiency.

The decomposition audit is

\[
E_{\mathrm{recon}}
=\frac{\|v_r-v_\parallel-v_{\mathrm{old}}-v_{\mathrm{new}}\|_2}
{\max(\|v_r\|_2,\varepsilon)}
\le10^{-6}.
\]

It checks numerical reconstruction only. Let \(g_r=g^{\mathrm{rare}}-g^{\mathrm{ctrl}}\)
be the registered gradient contrast. Common-space alignment is reported as

\[
c_{\mathrm{grad}}
=\frac{\|P_cg_r\|_2}{\max(\|g_r\|_2,\varepsilon)},
\qquad
c_{\mathrm{step}}
=\frac{\|P_cv_r\|_2}{\max(\|v_r\|_2,\varepsilon)}.
\]

Both are dimensionless subspace cosines. Their difference diagnoses AdamW
preconditioning; neither establishes functional use.

For the exact drop-new endpoint,

\[
\Delta Acc_{\mathrm{drop-new}}
=Acc(\theta_T^{\mathrm{rare}})-Acc(\theta_T^{\mathrm{drop-new}}).
\]

For logit margin

\[
m_\theta(x,y)=z_y(x;\theta)-\max_{y'\ne y}z_{y'}(x;\theta),
\]

the registered margin drop is

\[
\Delta m_{\mathrm{drop-new}}
=\mathbb E[m_{\theta_T^{\mathrm{rare}}}(X,Y)
-m_{\theta_T^{\mathrm{drop-new}}}(X,Y)].
\]

Accuracy drop is a fraction and margin drop is in logits. They explain the CE
effect but cannot replace the preregistered primary CE decision.

## 2. Anchor Alignment

This is a mechanism and causal-intervention audit for the H9-F/T6-F finite
endpoint story. It does not test H9-L or restore H11.

## 3. Tested Hypothesis

Reuse predicts that a causal-valid rare effect lies mainly in common/old space
or that deleting novel mass preserves function. The necessary-new rival
predicts stable novel mass and specific rare-task loss under exact deletion.

## 4. Rival Explanations

Gradient/update mismatch is measured directly; 32/32 common capture audits
space estimation; \(R_{\mathrm{old}}\) separates historical residual reuse;
equal-norm random removal separates arbitrary damage; base replay separates
general model damage; the one-step horizon prevents multistep bifurcation from
entering the primary effect.

## 5. Data / Model / Algorithm / Objective

Only E02-valid Common-LowF checkpoints and optimizer states are eligible. The
rare cell had zero E02 optimizer exposure; its E03 evaluation contexts are
disjoint from E02 confirmation contexts. The matched control has the same
entity, answer \(\pi(a)\), and exposure context but a historically high-frequency
donor alias. Each branch takes one batch-size-one full-position NTP AdamW step.
The language head is frozen before the step and reused for every endpoint.
Registered coordinates include all trainable non-head parameters. At least
eight inherited paired seeds are required.

## 6. Conditions, Seeds, And Checkpoints

| Item | Changed | Held fixed | Role |
|---|---|---|---|
| rare branch | rare cell | reference, optimizer, entity, answer, context | treatment |
| control branch | common donor cell | same | counterfactual |
| drop-new endpoint | remove \(v_{\mathrm{new}}\) | base and frozen head | primary intervention |
| random drop | equal-norm random direction | norm, head, eval | damage guard |

## 7. Primary Metric

\(\Delta CE_{\mathrm{drop-new}}\) decides functional necessity only after the
\(\Delta CE_{\mathrm{gain}}\), \(\rho_{\mathrm{new}}\), specificity, and base
guards are applied.

## 8. Secondary Metrics

\(\rho_\perp\), \(\rho_{\mathrm{new}}\), \(\nu_{\mathrm{new}}\), common null,
gradient cosine, actual-step cosine, accuracy and logit-margin drops,
\(\Delta CE_{\mathrm{specific}}\), and \(\Delta CE_{\mathrm{base}}\).

## 9. Known Good / Known Bad / Known Confusing Cases

Numerical decomposition must reconstruct \(v_r\) to relative error \(\le10^{-6}\).
Deleting all \(v_r\) must recover the control endpoint. A near-one conditional
novelty \(\nu_{\mathrm{new}}\) with tiny \(\rho_\perp\) is not meaningful novelty.

## 10. Stage-Level Profiling Plan

| Stage | Question | Pass | Artifact |
|---|---|---|---|
| E02 gate | may E03 run? | all three gates | e02_gate.json |
| branch audit | identical start, one variable? | hashes/counts exact | branch_audit.json |
| spaces | common/old stable? | capture/null gates | subspace_metrics.csv |
| endpoint | exact decomposition? | relative error \(\le10^{-6}\) | endpoint_audit.json |
| function | is novel mass necessary? | frozen CE rules | seed_summary.csv |

## 11. Algorithm Specification

1. Load the E02 model/optimizer state and freeze the output head.
2. Build \(G_c\) from target-free common counterfactual steps and
   \(R_{\mathrm{old}}\) from the last 64 historical E02 updates.
3. Execute rare/control one-step branches from the same state; record
   per-example gradients and actual AdamW endpoints.
4. Decompose \(v_r\) and construct exact drop-new and 16 random-drop endpoints.
5. Run full forward evaluation with one frozen head on rare and base slices.
6. Merge with frozen thresholds and without confirmation-guided changes.

## 12. Success / Failure / Insufficient Evidence

The Approval Snapshot rules are binding. If at least eight E02-valid seeds
exist but fewer than eight have \(\Delta CE_{\mathrm{gain}}\ge0.02\), record
`no_stable_measurable_rare_gain` and an insufficient functional-necessity
verdict. This is evidence that the registered one-step rare exposure has no
stable measurable gain, not proof of common-only sufficiency.

## 13. What This Cannot Claim

The parameter decomposition is coordinate-registered. Exact endpoint
intervention gives the causal effect of that intervention but not a unique
nonlinear attribution, a complete training-path result, or natural-language
generality.

## 14. Review Notes And Protocol Changes

- 2026-07-26: the researcher approved exact endpoint drop-new, a one-AdamW-step
  primary horizon, one frozen reference head, leave-target-out spaces, and
  conditional execution after E02 gates.
