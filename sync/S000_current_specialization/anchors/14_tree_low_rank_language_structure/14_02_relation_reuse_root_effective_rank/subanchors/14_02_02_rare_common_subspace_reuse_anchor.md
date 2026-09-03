---
anchor_id: 14_02_02_rare_common_subspace_reuse
status: parked_common_space_gate_failed
canonical_language: en
companion_cn: 14_02_02_rare_common_subspace_reuse_anchor_cn.md
parent_anchor: 14_02_relation_reuse_root_effective_rank
experiment_id: A14_02_E03_rare_common_subspace_reuse
---

# A14_02_02 Rare–Common Subspace Reuse


## 1. Problem Definition

Decision question: does one rare exposure that calls an already learned common
mapping produce a non-negligible, historically novel, and frozen-readout
functionally necessary direction outside the leave-target-out common update
space?

The experiment separates outside-common magnitude, reuse of old residual
directions, geometric novelty, and task necessity. A parameter-space direction
is not called functional merely because it is nonzero.

## 2. Physical Priors

**P1. Common mapping reuse predicts update reuse.** Most task-effective rare
update should lie in the common or old residual space.

**P2. AdamW and parameter gauge can create geometric outside components.** The
actual optimizer step, per-example gradient, and function effect are therefore
reported separately.

**P3. Function necessity requires an exact intervention.** A single-point
Jacobian is not used to translate a finite parameter component into ROOT; the
registered endpoint is reconstructed and run exactly.

## 3. Falsifiable Hypotheses

From the same reference parameters and optimizer state, rare and matched
control branches take one AdamW step. Define

$$
v_r=\theta_T^{\mathrm{rare}}-\theta_T^{\mathrm{ctrl}}.
$$

The reuse hypothesis is supported only when the rare branch has a measurable
functional gain and either the novel component is negligible or deleting it
does not cause a registered functional loss. It is refuted when a stable,
non-negligible novel component exists and exact deletion produces a specific
rare-task loss larger than the random-removal guard.

## 4. Mathematical Model

Let $P_c$ project onto the leave-target-out common AdamW-step contrast space,
and $P_{\mathrm{old}}$ onto the orthogonal historical residual space:

$$
v_\parallel=P_cv_r,
\qquad
v_\perp=(I-P_c)v_r,
$$

$$
v_{\mathrm{old}}=P_{\mathrm{old}}v_\perp,
\qquad
v_{\mathrm{new}}=(I-P_c-P_{\mathrm{old}})v_r.
$$

The geometry diagnostics are

$$
\rho_\perp=\frac{\|v_\perp\|_2^2}{\|v_r\|_2^2},
\qquad
\rho_{\mathrm{new}}=\frac{\|v_{\mathrm{new}}\|_2^2}{\|v_r\|_2^2}.
$$

The exact drop-new endpoint is

$$
\theta_T^{\mathrm{drop-new}}
=\theta_T^{\mathrm{rare}}-v_{\mathrm{new}}
=\theta_T^{\mathrm{ctrl}}+v_\parallel+v_{\mathrm{old}}.
$$

With one reference output head frozen for every branch,

$$
\Delta CE_{\mathrm{drop-new}}
=CE(\theta_T^{\mathrm{drop-new}})-CE(\theta_T^{\mathrm{rare}}).
$$

This is an exact endpoint intervention and does not invoke H11.

## 5. Computational Realization

E03 reuses valid Common-LowF E02 checkpoints and optimizer states. The rare
cell was never optimized in E02; the matched control has the same entity,
answer, and exposure context but a historically common alias--entity cell.
Only that sample identity changes. Common-space probes and historical updates
are strictly earlier than the rare step and leave the target out. The output
head is frozen before both one-step branches.

## 6. Minimal Falsification Tests

1. E02 capability, rank-validity, and common-space stability gates pass.
2. Rare/control begin from byte-identical model and optimizer states; all
   non-target fields are matched.
3. The rare full branch has measurable held-out gain
   $\Delta CE_{\mathrm{gain}}\ge0.02$ nat; otherwise functional necessity is
   insufficient rather than forced to pass.
4. Novel geometry is non-negligible only when $\rho_{\mathrm{new}}\ge0.05$ and
   exceeds the registered common-common null.
5. A necessary novel direction requires
   $\Delta CE_{\mathrm{drop-new}}>0.02$ nat, damage above equal-norm random
   deletion, and base/common CE preservation within 0.02 nat.

## 7. Current Evidence

E04 supported a shared local Jacobian image. E05/E06 showed that the actual
optimizer displacement and exact ROOT secant were effectively low-dimensional,
while one endpoint/reference Jacobian failed to represent the finite effect.
E03 therefore uses exact finite endpoints and treats parameter geometry as a
guard rather than the functional verdict.

The prerequisite common-step parameter space failed before the rare treatment:
held-out capture was 0.478--0.631 (mean 0.5717), and 0/10 seeds passed the 0.80
gate. The full E03 intervention was therefore not run. This is an
operationalization failure, not evidence for or against rare functional
novelty.

Result: [summary](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E03_rare_common_subspace_reuse/summary.md) · [detailed](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E03_rare_common_subspace_reuse/detailed.md).

## 8. Claim Boundary And Next Decision

A pass can establish only that, at the registered checkpoint and one-step
scale, a measurable rare effect did not require a novel frozen-readout task
direction. A fail can establish that this controlled rare exposure required a
registered new direction. Neither result proves a universal statement about
rare facts, full parameter rank, natural language, or NTP-implied H9-F.

Exactly one next decision: before retrying, preregister a leave-target-out
common ROOT-functional/secant space and validate it on fresh probes.
