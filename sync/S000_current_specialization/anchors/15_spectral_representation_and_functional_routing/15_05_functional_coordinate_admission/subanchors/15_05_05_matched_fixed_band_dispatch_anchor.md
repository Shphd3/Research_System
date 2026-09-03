---
anchor_id: 15_05_05_matched_fixed_band_dispatch
legacy_anchor_id: 15_03_matched_band_dispatch_effect
parent_anchor: 15_05_functional_coordinate_admission
status: completed_fail_distribution_only
created: 2026-07-31
canonical_language: en
chinese_companion: 15_05_05_matched_fixed_band_dispatch_anchor_cn.md
depends_on: 15_00_router_input_spectral_geometry
---

# A15_05_05 Matched 2B Band-Dispatch Ablation

## 1. Problem Definition

**Single decision question:** From one common 0.629B-token four-layer MoE
checkpoint, which frozen actual-input covariance bands change token-to-expert
dispatch by 2B tokens, and which improve or harm held-out NLL relative to
native routing and their equal-rank random controls?

## 2. Physical Priors

Band restriction first changes routing, which changes expert data, updates,
load, and representation feedback. Long-run effects can amplify, cancel, or
reverse static and one-step signals. A true band must beat an equal-rank random
projector to establish rank-specificity.

## 3. Falsifiable Hypotheses

**H1:** At least one true band causes substantial paired route divergence from
native and a different 2B matched-compute held-out NLL from its equal-rank
random control. Rivals are generic dimensionality reduction, load artifacts,
stale frozen bases, and routing change without functional benefit.

Pass requires the routing manipulation check plus lower held-out NLL than both
the relevant random arm and native. Precise non-superiority is Fail; failed
resume, compute, load, basis, or evaluation guards is Insufficient.

## 4. Mathematical Model

At the branch checkpoint estimate actual-input $\mu_\ell,U_\ell$ and freeze
$P_{\ell,a}$. Each arm uses

$$
r'_{\ell,a}=\mu_\ell+P_{\ell,a}(r_\ell-\mu_\ell),
\qquad z_{\ell,a}=W_\ell r'_{\ell,a}.
$$

An algebraically equivalent projected-weight implementation preserves the
full-shaped Gate and token-level Gate FLOPs. The primary metric is 2B held-out
NLL difference in nat/token. Route divergence is a required manipulation
check, not a substitute outcome.

## 5. Computational Realization

The approved [E01 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_05_functional_coordinate_admission/A15_05_05_E01_2b_matched_band_dispatch/protocol.md)
uses an H768 four-layer, eight-sparse-expert plus shared-expert, top-1 DCLM MoE
on one 8xRTX5090 node per arm. Nine arms are native, H64, M256, T448, N704, and
R64/R256/R448/R704. Every arm resumes identical step-800 model, optimizer,
scheduler, data cursor, and RNG state and ends at step 2544 (about 2.001B
nominal tokens).

## 6. Minimal Falsification Tests

Native no-op replay; true-versus-equal-rank-random comparisons; matched model,
data, tokens, capacity, kernel, and Gate path; fixed-token route divergence;
DCLM held-out NLL as primary outcome; WOS domain/topic routing only as an
interpretive diagnostic; and frozen/current band-overlap audit.

## 7. Current Evidence

[E01](/Projects/from-attention-to-search/main/experiments/A15/15_05_functional_coordinate_admission/A15_05_05_E01_2b_matched_band_dispatch/summary.md)
completed all nine matched arms at 2.000683B tokens. True H/M/T/N changed
frozen DCLM routes by 4.98%, 19.80%, 21.88%, and 13.26%, respectively, so the
manipulation passed. Yet every true arm had strictly higher paired held-out NLL
than native: +0.001784, +0.005600, +0.003697, and +0.003308 nat/token. Head
beat random64 but still lost to native; middle and nonhead lost to their random
controls; tail was indistinguishable from random448. Compute, load, replay,
completion, and basis guards passed.

## 8. Claim Boundary And Next Decision

The result establishes for one paired four-layer branch that fixed covariance
bands affect dispatch but do not improve 2B DCLM training. It does not rule out
additive head+residual views, learned task-conditioned coordinates, or direct
expert-update utility targets, and it is not cross-seed generality. WOS label
structure remains diagnostic rather than a language-model utility target.

**Next decision:** close fixed covariance-rank band-only dispatch and require
the next Router representation to pass an independent functional
expert-update or task-utility gate before matched large-scale training.
