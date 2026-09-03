---
anchor_id: 15_06_01_local_random_identity_control
parent_anchor: 15_06_online_spectral_routing_and_relay
status: completed_control_recorded
canonical_language: en
updated: 2026-08-08
---

# A15_06_01 Local Random Identity Control


This subanchor was migrated from the temporary `A15_01` identifier; raw
worker artifacts retain that historical identity.

## 1. Problem Definition

This subanchor inherits A15_06 and adjudicates one unresolved clause: whether
the weak Local-HMT endpoint advantage is specific to covariance-ranked H/M/T,
or is reproduced by an arbitrary smooth dynamic local partition.  The primary
metric is the 10B paired held-out NLL contrast between the completed Local-HMT
run and a new motion-matched Local-Random run, in nat/token; lower is better.

## 2. Physical Priors

A random control is causally useful only if its dimensions and temporal target
motion match the H/M/T treatment.  A fixed ambient orthogonal rotation of the
current nested H/M/T flag preserves all principal angles between successive
targets while removing covariance-rank identity.

## 3. Falsifiable Hypotheses

- **H1, covariance identity:** Local-HMT beats Local-Random-Matched in both
  seeds with paired-document confidence intervals below zero.
- **R1, generic dynamic constraint:** Local-Random-Matched matches or beats
  Local-HMT, or the two seeds disagree.
- **R2, tracking mismatch:** apparent HMT superiority is accompanied by a
  materially worse realized tracker in the random arm; this is insufficient
  for covariance attribution.

## 4. Mathematical Model

For layer $\ell$ and refresh $k$, let the covariance target be the nested flag
$F_{\ell,k}=(U_{64},U_{320})$.  Draw one deterministic seed- and layer-specific
Haar matrix $O_{s,\ell}\in\mathbb R^{768\times768}$ and define

$$
F^{rand}_{\ell,k}=(O_{s,\ell}U_{64},O_{s,\ell}U_{320}).
$$

Because $O_{s,\ell}$ is orthogonal, nesting, ranks, and every principal angle
between $F_{\ell,k}$ and $F_{\ell,k+1}$ are preserved exactly.  The deployed
flag then uses the same EMA, Procrustes/Grassmann candidates, and route
continuity guard as Local-HMT.

## 5. Computational Realization

The new arm changes only the target flag used by blocks 2--4.  Block 1 remains
Centered-Full; each later Router uses its own layer-local source and the same
H/M/T dimensional schedule (64/256/448).  Experts still receive full local
states.  Model, seed-specific step-0 parameters, DCLM stream, optimizer,
schedule, load loss, statistics/guard text, milestones, evaluation documents,
and 10B budget match the completed experiment.

## 6. Minimal Falsification Tests

Run seed 17 and 29 only.  Before full submission, unit and distributed smoke
must establish exact target-motion isometry, nested projector validity,
step-0 identity, paired token hashes, exact resume, and complete telemetry.
The decisive endpoint comparison reuses the completed Local-HMT and
Centered-Full per-document NLL values.

## 7. Current Evidence

Both E02 jobs completed 10B. Local-Random-Matched endpoint NLL was
3.60411/3.60076 (seed 17/29). The paired Local-HMT-minus-Random contrasts were
$-0.005370$ [$-0.006858,-0.003969$] and
$+0.001272$ [$-0.000265,+0.002925$]. Seed 17 clearly favored HMT, while seed 29
reversed in point estimate and crossed zero.

The fixed rotation preserved target principal-angle motion with maximum error
$1.23\times10^{-14}$ radians, and the random deployed-target overlap was higher
than HMT. All tracking-comparability guards passed. The typed verdict is
`fail_no_stable_covariance_identity_advantage`, not tracking insufficient.

Protocol: [A15_06_E02](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E02_local_random_identity_control/protocol.md)

Result: [Summary](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E02_local_random_identity_control/summary.md)

## 8. Claim Boundary And Next Decision

The registered four-layer, two-seed, 10B setting does not support attributing
the Local effect to covariance-rank identity. This does not establish universal
H/M/T semantics or rule out loss-aligned discriminative coordinates. The one
next decision is a held-out functional admission test: whether an
expert-utility discriminative side incrementally predicts expert regret or
cross-update compatibility beyond native scores and matched random controls.
