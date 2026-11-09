---
anchor_id: 15_05_01_shallow_feature_guidance
legacy_anchor_id: 15_01_shallow_head_guided_deep_routing
parent_anchor: 15_05_functional_coordinate_admission
status: layer_band_profile_pass_compatibility_pending
canonical_language: en
companion_language: zh
depends_on: 15_00_router_input_spectral_geometry
updated: 2026-07-31
---

# A15_05_01 Shallow Feature Guidance


## 1. Problem Definition

This sibling parent asks a functional question that A15_00 explicitly does not
answer:

> After controlling the native deep Router score, load, capacity, parameters,
> token count, and compute, do token-specific shallow-head coordinates add
> held-out information about which tokens are compatible for training in the
> same deeper expert?

For layer \(k<\ell\), shallow-head coordinates mean

\[
c_{k,H}(x)=U_{k,H}^\top(g_k(x)-\mu_k).
\]

They are carried from the same token. Applying \(U_{k,H}\) directly to \(g_\ell\)
is invalid without a registered cross-layer transport map.

The parent primary metric is the held-out incremental prediction of one-step
cross-update compatibility beyond the native deep Router score and registered
nuisance controls. It decides functional admission, not end-to-end benefit.

## 2. Physical Priors

1. A shallow high-variance factor may provide a stable, low-noise coarse cohort
   before deeper representations and experts differentiate.
2. High variance is not equivalent to useful compatibility; common, position,
   length, or source-frequency factors can dominate the head.
3. Reusing one coarse partition at multiple depths can reduce churn but can
   also cause premature lock-in and repeated expert functions.

## 3. Falsifiable Hypotheses

**H1:** On independent tokens, \(c_{k,H}\) predicts deeper one-step compatibility
beyond the native deep score and beats same-dimensional random and
token-shuffled controls. Conditional on that gate, shallow-head guidance
improves matched-compute early training.

**Strongest rival:** Any gain is caused by extra parameters, marginal feature
scale, altered load, or token identity rather than the spectral and
token-specific shallow signal.

**Pass:** The compatibility admission gate and matched-compute training test
both pass with load/capacity guards.

**Fail:** The model is capable, but shallow head does not beat the compatibility
controls, or its training gain does not beat the native and matched side-channel
controls after compute/load matching.

**Insufficient:** The registered variable is not stably present in the shallow
head, the base model is incapable, compatibility is underpowered, or routing
guards fail.

## 4. Mathematical Model

The proposed deep score is

\[
z_\ell(x)
=W_\ell g_\ell(x)+A_\ell c_{k,H}(x),
\qquad \ell>k.
\]

\(A_\ell\) is a trainable auxiliary readout. The native path remains reachable
when \(A_\ell=0\). Random and shuffled conditions use the same tensor shapes and
operations.

Let \(Y_{ij}^{(\ell)}\) be an independently measured one-step cross-update
compatibility target for token groups \(i,j\). The admission quantity is the
held-out residual gain

\[
\Delta_{\rm comp}
=\operatorname{Perf}(Y\mid s_{\rm native},c_{k,H},q)
-\operatorname{Perf}(Y\mid s_{\rm native},q),
\]

where \(q\) contains registered load, norm, position, length, and outlier
controls. The exact performance score is frozen in the Protocol.

## 5. Computational Realization

The first subanchor uses a controlled four-layer MoE. Layers 1--2 first form a
stable representation; the layer-2 head basis is frozen. A genuine native
four-layer arm is compared with layers 3--4 receiving layer-2 head,
same-dimensional random, or token-shuffled head coordinates. The three
side-channel arms use identical auxiliary readouts. All arms use no
load-balance loss and share a non-gradient expert-score-bias rule. Informative
and nuisance tasks distinguish useful shallow structure from variance alone.

## 6. Minimal Falsification Tests

1. Verify that the registered controlled variable is captured by layer-2 head
   above random and is absent as a functional predictor in the nuisance task.
2. On independent token groups, require head compatibility gain beyond native,
   norm/outlier, random, and shuffled controls before joint training.
3. At matched cumulative FLOPs, compare head against a genuine native model
   and against random/shuffled arms with identical auxiliary parameters, load
   targets, capacity, data, and seeds.
4. Audit route margin, flips, load, expert-update conflict, and expert-function
   repetition to localize any loss difference.

## 7. Current Evidence

A15_00 establishes that trained Gates can strongly access their own-layer
covariance head. It does not establish shallow semantics or deep compatibility.
The old wrong-layer-basis control weakens direct basis transplantation but does
not test carrying the same token's shallow coordinates forward.

A15_05_02 stopped at Stage A because head and equal-dimensional random views
both achieved saturated accuracy, so it could not adjudicate guidance.
A15_02_01 then used a recombination-capable, low-sample task with random-
direction q95 controls. Composition training reproducibly made F1/head at
layers 3--4 specific to the one-step intermediate state and F2 specific to the
coarse condition in seeds 17 and 29. The composed result formed in the deeper
full state but was not specifically localized to any fixed H/M/T or fine band.

Gate ablation further showed that the native Router still relied primarily on
F1/head and scarcely used F2 despite its coarse readability. This supplies
candidate layer-specific coordinates but no co-training compatibility or
training-benefit certificate. See the [A15_02_01 result](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_01_E01_controlled_layer_information_profile/summary.md).

A15_05_03 then trained local HMT and block-1-relay HMT explicitly. Local HMT
ended worse than native. Relay ended slightly better in both paired
continuations, but both treatments had worse NLL AUC; relay showed consistent
route-regret improvement without coherent utility-dispersion, redundancy, and
conflict improvements. Fixed band scheduling therefore changes the learning
path but has no training-efficiency certificate. See the
[A15_05_03 result](../../../../experiments/A15/15_05_functional_coordinate_admission/A15_05_03_E01_progressive_band_source_routing_2b/summary.md).

## 8. Claim Boundary And Next Decision

This parent can establish controlled incremental compatibility and a
matched-compute pilot effect. It cannot establish natural-language universality,
large-scale efficiency, or that covariance head represents domain semantics.
The completed subanchors establish that band meaning can reorganize with
depth and that explicit band scheduling can alter expert function, but they
still provide no compatibility admission or full-trajectory efficiency gain.
In particular, F1=intermediate and F2=coarse cannot be generalized to natural
language, and readability cannot authorize expert dispatch.

**Exactly one next decision:** distill the replicated A15_02_01 functional
coordinates into fixed low-rank readouts and test whether they predict deeper
one-step co-training compatibility beyond the native score. Matched cross-layer
guidance remains blocked until they beat equal-dimensional random,
token-shuffled, and wrong-layer controls.
