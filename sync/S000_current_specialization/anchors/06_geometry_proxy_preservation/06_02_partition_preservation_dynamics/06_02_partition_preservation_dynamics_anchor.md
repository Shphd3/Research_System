# A06_02 Partition-Preservation Dynamics

Status: completed parent mechanism anchor.

Thinking Card source: [06_02_partition_preservation_dynamics_thinking_card.md](06_02_partition_preservation_dynamics_thinking_card.md)

## 1. Complete Problem

**Decision question:** Which signed training dynamics determine whether a
supplied feature-expert partition survives, crosses, or recovers?

### Terminology / Definitions

| Term | Plain meaning | Computation | Cannot prove |
|---|---|---|---|
| Route margin | Assigned expert's score lead | $(w_a-w_b)^\top\mu_f$ | Expert utility |
| First crossing | First update at which a relevant margin becomes nonpositive | $T_{cross}$ | Irreversible failure |
| Expert advantage | First-order loss reduction from increasing an expert's contribution | $A_e$ below | Long-run preservation |
| Boundary pressure | Source update projected on the relevant margin gradient | signed inner product | General optimizer optimality |

## 2. Physical Priors

1. Weak tail examples fail before a positive feature mean.
2. Margin is bilinear in Router and representation geometry.
3. Gradient source count and norm matter only after projection onto a relevant
   boundary.
4. Optimizer attribution requires actual-update controls, not nominal learning
   rates alone.

## 3. Falsifiable Hypotheses

**H1: any-positive-margin safety.** Every positive initialization is
preserved. Rejected by small-positive-margin crossings.

**H2: background-count mechanism.** More background positions predict failure
without considering geometry. Rejected by signed source controls.

**H3: representation-only failure.** Hidden-state drift is necessary for first
crossing. Rejected when Router-only training reproduces crossing.

**H4: AdamW-history necessity.** Coordinate-wise AdamW history uniquely causes
crossing. Weakened by direction and norm-matched interventions.

## 4. Core Mathematical Model

For feature $f$, assigned expert $a$, and competitor $b$,

$$
m_{f,a,b}(t)=(w_a(t)-w_b(t))^\top\mu_f(t).
$$

The exact finite-step identity is

$$
\Delta m
=(\Delta w_a-\Delta w_b)^\top\mu_f
+(w_a-w_b)^\top\Delta\mu_f
+(\Delta w_a-\Delta w_b)^\top\Delta\mu_f.
$$

For a soft mixture with frozen states,

$$
\Delta w_e=\frac{\eta}{\tau}p_eA_eh,
\qquad
A_e=-\langle\nabla_{\hat y}\ell,E_e(h)-\hat y\rangle.
$$

For source $s$, the relevant pressure is

$$
B_s^{a,b}=-\langle g_s,\nabla_\theta m_{f,a,b}\rangle.
$$

## 5. Evidence Chain

1. Small positive margins can cross, while larger margins more often remain in
   the same basin. Exact center equality is unnecessary.
2. A no-background full-slot control preserves the ideal partition for 2000
   updates, making mixed/background positions a necessary controlled candidate,
   not a universal sole cause.
3. Matched utility produces positive local pressure; identical experts produce
   zero pressure; utility permutation redirects the pressure.
4. Background count alone does not predict harm; signed boundary projection
   does.
5. Freeze interventions localize early crossing on the tested AdamW surface to
   Router-row motion. Representation motion supplies much of ordinary recovery.
6. Optimizer decomposition weakens an AdamW-specific directional explanation;
   actual Router update scale is the stronger localized variable.
7. Explicit post-cross recovery adds little beyond ordinary joint dynamics in
   the fixed-utility bridge.

### Subanchor Registry

| Subanchor | Local decision | Experiment group |
|---|---|---|
| [`A06_02_01`](subanchors/06_02_01_finite_margin_basin_anchor.md) | Preservation occupies a finite low-tail margin basin. | [`E01`--`E08`](/Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics) |
| [`A06_02_02`](subanchors/06_02_02_common_background_preservation_controls_anchor.md) | Common/background controls can slow drift but do not solve binding. | [`E01`--`E04`](/Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics) |
| [`A06_02_03`](subanchors/06_02_03_utility_signed_local_dynamics_anchor.md) | Expert advantage and signed background pressure determine local margin direction. | [`E01`--`E03`](/Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics) |
| [`A06_02_04`](subanchors/06_02_04_representation_router_optimizer_codynamics_anchor.md) | Router, representation, and optimizer-transmitted updates jointly determine crossing and recovery. | [`E01`--`E04`](/Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics) |

## 6. Minimal Adjudication Contract

Preservation experiments must report low-tail margin, first crossing, re-entry,
Router and representation freeze interventions, source-conditioned boundary
pressure, actual parameter updates, and a no-background or solved-background
guard. Mean center distance or gradient norm alone cannot decide the claim.

## 7. Current Verdict

**Supported:** finite low-tail margin is the local preservation state; expert
utility and signed boundary projection determine local direction; Router,
representation, and optimizer scale jointly determine realized events.

**Rejected as general solutions:** common subtraction, Router-row projection,
Router learning-rate reduction, early freeze, and the tested denoising rules.

## 8. Claim Boundary And Next Decision

**Cannot claim:** a universal safe margin, natural-language transfer, a new
optimizer theorem, or functional specialization with trainable experts.

**Next decision:** replace assumed expert utility with trainable expert-function
formation and test discovery under sparse feedback (`A06_03`).
