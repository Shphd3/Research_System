---
anchor_id: 15_00_02_gate_common_residual_preference
parent_anchor: 15_00_router_input_spectral_geometry
status: completed_pass_pooled_alignment_with_native_use
canonical_language: en
companion_language: zh
thinking_card: 15_00_02_gate_common_residual_preference_thinking_card_cn.md
updated: 2026-07-31
---

# A15_00_02 Gate Preference For Pooled Common Versus Local Residual Modes

Thinking Card source:
[15_00_02_gate_common_residual_preference_thinking_card_cn.md](15_00_02_gate_common_residual_preference_thinking_card_cn.md).

## 1. Problem Definition

A15_00 establishes strong equal-energy Gate alignment with a pooled covariance
head but does not determine whether that head is a cross-data common component
or an accidental calibration direction.

**Decision question:**

> At equal input energy, does the decommon Gate produce greater expert-relative
> logit gain and native route dependence for an independently pooled
> centered-common candidate than for equal-dimensional shard-local residuals,
> and how does this preference change across 30k/40k/80k?

This subanchor directly adjudicates pooled-versus-local preference. The joint
phrase “preference for stable common” is licensed only if A15_00_01
independently establishes the stability labels.

The primary metric is

$$
B_{\ell,P:L}
=\log\frac{G_{\ell,P}+\epsilon}
{\operatorname{median}_sG_{\ell,L_s}+\epsilon},
$$

a log equal-energy gain ratio. It measures Gate geometry, not utility.

## 2. Physical Priors

1. A fixed linear Gate can accumulate a coherent weight on directions that
   recur across data groups; rotating shard-local directions can cancel.
2. Pooled top directions have greater raw energy, so only eigenvalue-free
   equal-energy gain $G$ can adjudicate selection.
3. Endpoint alignment reflects both $W$ and representation-basis motion;
   checkpoint crossings are needed to separate them.

## 3. Falsifiable Hypotheses

**H1:** At decommon 80k, $B_{P:L}>0$ beyond a singular-value-preserving
orientation null, with directional replication at 40k. Removing the pooled
candidate also removes more native-winner margin support than removing an
equal-dimensional local residual; route flip is supporting evidence. LB
determines lineage sharing.

**Strongest rival R0:** Only raw input energy favors the pooled candidate;
$G$ and $B_{P:L}$ do not.

**R1:** Any pooled direction, wrong-layer basis, or matched orientation null
produces the same result.

**R2:** Endpoint change is representation drift; fixed-basis
$W_{30/40/80}$ comparisons do not reproduce it.

**R3:** Stable shared directions are functionally useful. This experiment
cannot label a real pooled preference as beneficial or harmful.

**Pass:** Both equal-energy gain and native-margin-support comparisons support
H1 at the decommon primary endpoint, replicate directionally at 40k, and pass
null and wrong-layer guards.

**Fail:** A valid precise result supports R0/R1, or native route dependence on
local residuals is not weaker.

**Insufficient:** A15_00_01 may independently be insufficient while this
anchor still decides pooled-versus-local preference, but the stability
interpretation remains unavailable. Failure of actual-input, basis, route
replay, checkpoint crossing, or precision guards makes this anchor itself
insufficient.

## 4. Mathematical Model

Let $\bar W_\ell=C_EW_\ell$, with
$C_E=I-\mathbf1\mathbf1^\top/E$. Fit a pooled 64-dimensional candidate
$U_{\ell,P}$. For shard $s$, fit a local residual basis after removing it:

$$
Y_{\ell,s}=X_{\ell,s}(I-U_{\ell,P}U_{\ell,P}^{\top}),
\qquad
U_{\ell,L_s}=\operatorname{TopSV}_{64}(Y_{\ell,s}).
$$

For any 64-dimensional basis $U$,

$$
G_\ell(W,U)=\frac1{64}\|\bar W_\ell U\|_F^2.
$$

$B_{\ell,P:L}$ compares pooled gain with the median local-residual gain.
Equal-rank ablation uses native-winner margin support as the route-use metric;
top-1 flip is supporting evidence.
Full $W_a\times U_b$ crossings for
$a,b\in\{30k,40k,80k\}$ separate saved-weight and basis effects but do not
identify per-step gradient causality.

## 5. Computational Realization

The [approved canonical E01 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_02_E01_gate_common_residual_preference/protocol.md)
reuses A15_00_01 frozen actual-input caches, document splits, and 64-dimensional
bases while independently computing Gate gain, route effect, orientation null,
and checkpoint crossings.

Existing 12-layer H768 decommon and LB 30k/40k/80k checkpoints are used. The
80k endpoint is primary, 40k is replication, and 30k is macro-trajectory
support. All 12 layers are reported.

The two E01 analyses share S0 provenance and activation extraction and can
execute in parallel. Neither result may alter the other's estimator, data, or
metric post hoc.

## 6. Minimal Falsification Tests

1. Apply one implementation of $G$, flip, and margin to pooled, each local
   residual, and full/complement Haar-64 bases.
2. Use 256 singular-value-preserving Gate-orientation nulls and wrong-layer
   pooled bases.
3. Compare equal-rank ablations on identical held-out documents.
4. Use the full $3\times3$ checkpoint crossing to separate $W$ and basis
   motion.
5. Adjudicate LB and decommon separately; they are not a single-variable
   center/LB causal pair.

## 7. Current Evidence

The approved [E01 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_02_E01_gate_common_residual_preference/protocol.md)
completed with verdict `pass_pooled_alignment_with_native_use`; see the
[summary](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_02_E01_gate_common_residual_preference/summary.md)
and [detailed evidence ledger](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_02_E01_gate_common_residual_preference/detailed.md).

At 40k/80k, pooled/local equal-energy Gate-gain ratios are 2.83/3.08 for
decommon and 3.94/4.55 for LB. The corresponding pooled-minus-local
native-winner margin support is 1.998/2.061 and 1.873/1.953 logit/token. All
model-level intervals lie above zero and all observed $B$ values exceed the
singular-value-preserving orientation-null q95 near 0.06.

LB passes the layerwise gain test in 12/12 layers. Decommon passes in 11/12;
layer 12 is a registered local exception, so the gain claim is model-level.
Margin support is positive in 12/12 layers for all four endpoints. Actual-input
replay, matched rank, SVD, wrong-layer, route replay, and numerical guards pass.

Combined with A15_00_01, the joint verdict is
`joint_pass_gate_prefers_transferable_centered_common`: the Gate preferentially
uses a more cross-document-transferable centered component over a less
transferable local residual at the retained endpoints. Per researcher
amendment, 30k is excluded.

## 8. Claim Boundary And Next Decision

A15_00_02 establishes current equal-energy Gate geometry and native-route
dependence. The joint result does not establish semantics, expert
compatibility, validation benefit, or a causal explanation of decommon
performance. LB/decommon differences are descriptive because centering,
load-balancing, and their training paths differ.

**Exactly one next decision:** decide whether to formalize the matched
stable-versus-local residual training intervention opened by the joint Pass,
with expert-update conflict and held-out loss/FLOP as decision outcomes.
