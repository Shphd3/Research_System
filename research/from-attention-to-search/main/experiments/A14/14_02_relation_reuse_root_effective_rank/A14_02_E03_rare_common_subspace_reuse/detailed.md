---
experiment_id: A14_02_E03_rare_common_subspace_reuse
status: parked_before_full_run
verdict: parked_e02_common_space_gate_failed
---

# Detailed: A14_02_E03 Rare–Common Subspace Reuse

Primary anchor: [A14_02_02](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_02_rare_common_subspace_reuse_anchor.md)  
Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** test whether one rare exposure adds a historically novel and
functionally necessary direction outside common/old spaces.  
**Gate logic:** execute only if E02 capability, rank validity, and common-space
stability pass.  
**Direct result:** capability and rank validity passed, common-space stability
failed 0/10.  
**Conclusion:** E03 full treatment was correctly parked.  
**Evidence:** mean held-out common capture 0.5717 versus the 0.80 gate.

## 1. Terminology / Definitions

### Common-space capture

\[
C_{\mathrm{common}}
=
\frac{\|P_{G_c}V_{test}\|_F^2}{\|V_{test}\|_F^2}.
\]

**Plain meaning:** fraction of new common-step energy represented by a space
fitted on other common steps.  
**Unit:** energy fraction.  
**Decision role:** prerequisite for calling any rare component outside common.  
**Cannot prove:** a unique, coordinate-free, or functionally sufficient
mechanism.

### Planned finite effect

\[
v_r=\theta_T^{rare}-\theta_T^{ctrl}.
\]

It is the actual one-step AdamW endpoint contrast, not a gradient.

### Planned geometry

\[
v_\parallel=P_cv_r,
\qquad
v_\perp=(I-P_c)v_r,
\]

\[
v_{old}=P_{old}v_\perp,
\qquad
v_{new}=(I-P_c-P_{old})v_r.
\]

\[
\rho_\perp=\frac{\|v_\perp\|_2^2}{\|v_r\|_2^2},
\qquad
\rho_{new}=\frac{\|v_{new}\|_2^2}{\|v_r\|_2^2}.
\]

These are dimensionless geometry diagnostics. Because \(P_c\) failed stability,
they were not interpreted in a full run.

### Planned exact endpoint metric

\[
\theta_T^{drop-new}
=\theta_T^{rare}-v_{new},
\]

\[
\Delta CE_{drop-new}
=CE(\theta_T^{drop-new})-CE(\theta_T^{rare}).
\]

This is an exact forward intervention, not a point-Jacobian approximation. It
was not measured in confirmation because \(v_{new}\) was invalidly identified.

### Planned causal and guard metrics

The rare functional gain was registered as

\[
\Delta CE_{\mathrm{gain}}
=CE(\theta_T^{\mathrm{ctrl}})-CE(\theta_T^{\mathrm{rare}}).
\]

Its unit is nat and its causal-valid gate was \(0.02\) nat. It would establish
that the rare branch improved the rare slice before asking which component was
necessary. It was not measured in full confirmation because the common-space
prerequisite had already failed.

For equal-norm random removals \(z_j\), specificity and base preservation were

\[
\Delta CE_{\mathrm{specific}}
=\Delta CE_{\mathrm{drop-new}}
-Q_{0.95}\!\left(
CE(\theta_T^{\mathrm{rare}}-z_j)-CE(\theta_T^{\mathrm{rare}})
\right),
\]

\[
\Delta CE_{\mathrm{base}}
=CE_{\mathrm{base}}(\theta_T^{\mathrm{drop-new}})
-CE_{\mathrm{base}}(\theta_T^{\mathrm{rare}}).
\]

Both are in nat. Specificity would separate targeted novel-component use from
generic parameter damage; \(|\Delta CE_{\mathrm{base}}|\le0.02\) would guard the
old/common task. Neither was measured in full confirmation.

The numerical reconstruction guard was

\[
E_{\mathrm{recon}}
=\frac{\|v_r-v_\parallel-v_{\mathrm{old}}-v_{\mathrm{new}}\|_2}
{\max(\|v_r\|_2,\varepsilon)}.
\]

The gradient and actual-step common-space cosines were

\[
c_{\mathrm{grad}}
=\frac{\|P_cg_r\|_2}{\max(\|g_r\|_2,\varepsilon)},
\qquad
c_{\mathrm{step}}
=\frac{\|P_cv_r\|_2}{\max(\|v_r\|_2,\varepsilon)}.
\]

These dimensionless diagnostics would check decomposition correctness and
AdamW-induced gradient/update mismatch. They cannot establish functional use
and were not interpreted after the gate failure.

Finally,

\[
\Delta Acc_{\mathrm{drop-new}}
=Acc(\theta_T^{\mathrm{rare}})-Acc(\theta_T^{\mathrm{drop-new}}),
\]

\[
m_\theta(x,y)=z_y(x;\theta)-\max_{y'\ne y}z_{y'}(x;\theta),
\]

\[
\Delta m_{\mathrm{drop-new}}
=\mathbb E[m_{\theta_T^{\mathrm{rare}}}(X,Y)
-m_{\theta_T^{\mathrm{drop-new}}}(X,Y)].
\]

Accuracy drop is a fraction and margin drop is in logits. They were planned to
explain the primary CE effect, not replace it; because full treatment was not
authorized, their confirmation status is `not measured`.

## 2. Protocol Compliance Audit

| Item | Evidence | Status |
|---|---|---|
| E02 generator | all exact | pass |
| E02 capability | 20/20 condition-seeds | pass |
| E02 rank validity | 20/20 | pass |
| common-space capture | 0/10 at or above 0.80 | fail |
| E03 full treatment | prohibited after gate failure | not run |
| post-result threshold change | none | pass |

## 3. Common-Space Result

| Seed | Capture |
|---:|---:|
| 0 | 0.6117 |
| 1 | 0.5582 |
| 2 | 0.5611 |
| 3 | 0.4780 |
| 4 | 0.6216 |
| 5 | 0.5504 |
| 6 | 0.6314 |
| 7 | 0.6116 |
| 8 | 0.5803 |
| 9 | 0.5129 |

Mean was 0.5717. The fitted 95%-energy ranks were 24--26 out of a maximum 32
fit contrasts. The failure is therefore not a numerical rank-zero case: even a
fairly broad fitted space did not transfer to held-out common cells.

## 4. Visualization Result

![Common-space capture gate](figures/common_space_gate.png)

**Purpose:** decide E03 eligibility.  
**Metric/unit:** held-out common-step energy capture/fraction.  
**Expected if valid:** at least eight bars at or above 0.80.  
**Observed:** zero.  
**Take-home:** raw common AdamW step contrasts are not stably low-dimensional
under the registered estimator.  
**Limitation:** this is parameter geometry, not ROOT functional geometry.

## 5. Failure Decomposition

| Candidate failure | Status | Reason |
|---|---|---|
| common mapping not learned | ruled out | unseen accuracy 0.969--1.0 |
| ROOT functional metric invalid | ruled out | identity/shuffle/random guards pass |
| E03 implementation broken | not supported | smoke generated every endpoint metric |
| raw common update proxy unstable | supported | capture 0.478--0.631 |
| rare requires new direction | unresolved | treatment not run |

The failed object is the parameter-space operationalization, not the E02
physical prior and not the exact endpoint formula.

## 6. Interpretation

One learned common input--answer function can be realized through parameter
updates that still depend strongly on alias, entity, nuisance context, and
AdamW coordinate preconditioning. Consequently, state-functional reuse does
not entail that raw single-example update contrasts share one low-dimensional
linear span.

This result sharpens the theory boundary: H9-F concerns the finite ROOT effect,
not raw parameter-vector alignment. A future mechanism experiment should
measure a common functional/secant image directly or prove why a registered
parameter metric is appropriate.

## 7. Claim Boundary

Can claim a failed common-space estimator and a correctly parked experiment.
Cannot claim rare reuse, rare novelty, functional necessity, or a negative
result for the exact drop-new intervention.

## 8. Next Decision

If reopened, write a new protocol with fresh probes. Candidate A is a larger or
whitened raw-update space with independent confirmation; candidate B, preferred,
is a leave-target-out ROOT-functional common secant space aligned with the E02
observable. Do not reuse the current held-out captures to select the repair.

## 9. Artifact Map

- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- gate table: [tables/common_space_gate.csv](tables/common_space_gate.csv)
- gate figure: [figures/common_space_gate.png](figures/common_space_gate.png)
- E02 raw source: `active/tree_low_rank/results/a14_02_e02_frequency_mapping_rank_separation/full_v1`
- E03 smoke only: `active/tree_low_rank/results/a14_02_e03_rare_common_subspace_reuse/smoke_v1`
- E03 runner: `active/tree_low_rank/scripts/run_rare_common_subspace_reuse.py`
- E03 config: `active/tree_low_rank/configs/a14_02_e03_rare_common_subspace_reuse.yaml`
