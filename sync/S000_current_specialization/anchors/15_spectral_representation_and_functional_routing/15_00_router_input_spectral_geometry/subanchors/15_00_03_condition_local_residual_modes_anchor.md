---
anchor_id: 15_00_03_condition_local_residual_modes
parent_anchor: 15_00_router_input_spectral_geometry
status: complete_pass_conditional_modes_shared_envelope
created: 2026-07-31
canonical_language: en
chinese_companion: 15_00_03_condition_local_residual_modes_anchor_cn.md
---

# A15_00_03 Condition-Stratified Residual Modes

## 1. Problem Definition

Random document shards showed high overlap for both centered top-64 and the
residual top-64 after removing it. This does not distinguish a truly global
residual projector from condition-varying modes averaged inside mixed shards.

**Single decision question:** Under real Web of Science domain/topic labels,
is same-condition residual-64 overlap higher than cross-condition overlap while
cross-condition bases still capture residual energy above a matched random
null?

## 2. Physical Priors

Repeated variation within a condition can produce a reproducible low-rank
projector. Projectors may rotate across conditions while remaining inside a
shared residual envelope. Low cross overlap alone is not sufficient because
estimation noise also lowers within-condition overlap.

## 3. Falsifiable Hypotheses

**H1:** within-condition overlap exceeds cross-condition overlap, while
cross-capture remains above complement-Haar q95; domain and nested-topic
analyses agree in direction.

**R0:** residual geometry is global, so within and cross overlap are similarly
high. **R1:** estimates are unstable, so both overlaps and cross-capture are
low. **R2:** label imbalance or text length creates the gap, so label
permutation and matched random groups reproduce it.

Pass requires a positive paired-bootstrap lower bound for
$\Delta O=O_{within}-O_{cross}$ and positive cross-capture margin above Haar
q95 in the domain primary analysis, with topic directional replication. A
precise R0/R2 pattern is Fail; failed reliability or object guards is
Insufficient.

## 4. Mathematical Model

Estimate pooled top-64 $U_P$ on an independent domain-balanced training pool.
For disjoint within-condition training halves $A/B$, fit residual top-64 bases
$U_c^A,U_c^B$ after removing $U_P$:

$$
O(c,d)=\frac{\|U_c^{A\top}U_d^B\|_F^2}{64},\qquad
\Delta O=\operatorname{median}_cO(c,c)-
\operatorname{median}_{c\ne d}O(c,d).
$$

Cross-capture applies source basis $U_c^A$ to target $d$'s independently
centered test residual covariance and subtracts target-specific
complement-Haar q95. Overlap tests identical directions; capture tests a
transferable envelope.

## 5. Computational Realization

The approved [E01 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_03_E01_condition_local_residual_modes/protocol.md)
uses the actual Gate input of LB/decommon 40k/80k checkpoints at all 12 layers.
Only abstracts enter the model. Seven domains form the primary analysis; the
top four sufficiently populated areas per domain form 28 nested topic checks.

## 6. Minimal Falsification Tests

Disjoint A/B training documents, validation means, and test capture targets;
real versus permuted labels and equal-size random groups; centered-top versus
residual comparison; complement-Haar q95; separate lineage/checkpoint reports;
and actual-input/native-logit replay guards.

## 7. Current Evidence

The completed [condition-stratified experiment](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_03_E01_condition_local_residual_modes/summary.md)
passes H1 in a bounded form. Across LB/decommon 40k/80k, domain-level residual
within overlap is 0.754--0.777 and cross overlap 0.698--0.725. The basis-refit
document/basis-refit interval for within-minus-cross is 0.032--0.044 and the
2,000-draw domain-block interval remains positive at 0.019--0.069, versus
matched random-group q95 0.0012--0.0015. Nested topics replicate the direction.

Cross-condition bases nevertheless retain 95.1--96.4% of within-domain
capture and 92.2--93.8% at topic level. Centered top-64 is more stable in
absolute overlap but also condition-dependent. The evidence therefore supports
condition-specific rotations inside a strongly shared envelope, not isolated
or uniquely residual condition spaces.

The approved document-level follow-up refines this result. Residual rank-64
overlap falls to 0.301--0.308 for same-domain document pairs and 0.295--0.302
cross-domain, versus Haar q95 0.0939. Cross-domain capture is 97.8--98.1% of
same-domain capture but only 32.7--34.1% of the target document's own rank-64
optimum. A disjoint-token rank-32 guard gives 0.516--0.534 overlap within one
document, 0.173--0.181 across same-domain documents, and 0.168--0.177 across
domains. Thus exact local modes vary beyond estimator noise, while coarse
domain identity explains only a modest share and the broad envelope remains
shared.

## 8. Claim Boundary And Next Decision

This anchor establishes condition-stratified geometry only. It does not make
semantic, causal, or training-benefit claims and does not authorize labels as
Router inputs. The result rejects the strong explanation that decommon fails
because each condition exposes an incompatible residual space.

The separate matched 2B band-dispatch experiment has now shown that fixed bands
change routes but do not improve NLL over native.

**Next decision:** close fixed residual-band dispatch and require a future
Router representation to pass a direct expert-update or task-utility gate.
