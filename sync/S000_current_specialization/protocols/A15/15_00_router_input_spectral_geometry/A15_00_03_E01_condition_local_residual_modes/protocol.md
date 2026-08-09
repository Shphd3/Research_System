---
experiment_id: A15_00_03_E01_condition_local_residual_modes
status: completed_pass_conditional_modes_shared_envelope
created: 2026-07-31
approval_date: 2026-07-31
primary_anchor: 15_00_03_condition_local_residual_modes
chinese_companion: protocol_cn.md
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
resource_profile: local-2xh100
result: summary.md
---

# Protocol: Condition-Stratified Residual Projectors

## 0. Approval Snapshot

**Execution outcome (2026-07-31):** Pass for condition-specific residual
rotations inside a strongly shared envelope. Domain $\Delta O$ intervals are
positive and far above random grouping, while cross-condition capture retains
more than 95% of within-domain capture. See [summary.md](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_03_E01_condition_local_residual_modes/summary.md).

The approved document-level follow-up further found residual rank-64 overlap
near 0.30 across documents versus Haar q95 0.094. Same-document disjoint-token
rank-32 overlap exceeds 0.51, so exact local-mode variation is not primarily
estimator noise. Same-domain exceeds cross-domain only modestly, while
cross-domain capture remains about 98% of same-domain capture.

The researcher authorized implementation and full execution. The single
question is whether real domain/topic conditions produce higher same-condition
projector overlap but lower cross-condition overlap while retaining
above-random cross-capture. This is geometry evidence, not training utility.

## 1. Terminology / Definitions

Within overlap is $\|U_c^{A\top}U_c^B\|_F^2/64$ from disjoint halves of one
condition. Cross overlap replaces $c$ by $d\ne c$. Cross-capture is the
fraction of target residual covariance captured by a source-condition basis;
its decision value is the margin over target-specific complement-Haar q95.

## 2. Anchor Alignment

The primary metric is $\Delta O=\mathrm{median}(O_{within})-
\mathrm{median}(O_{cross})$. Cross-capture margin is required for the shared
envelope interpretation. Neither overlap nor energy alone is sufficient.

## 3. Tested Hypothesis

H1 predicts positive domain-level $\Delta O$ and positive cross-capture margin,
with directional nested-topic replication. R0 predicts similarly high within
and cross overlap. R1 predicts low within, cross, and capture.

## 4. Rival Explanations

Label permutations and equal-size random groups test sample/length artifacts;
centered top-64 tests residual specificity; complement-Haar q95 tests generic
energy capture.

## 5. Data / Model / Algorithm / Objective

Use only `abstract` from the local Web of Science Arrow train/validation/test
splits. Select stable-hash-ordered documents with at least 128 tokens and use
exactly 128 tokens. Seven domains are primary: 64 training documents per
domain for pooled-common fit, 64+64 for condition A/B, 64 validation documents
for target means, and 64 test documents for capture. Select the top four areas
per domain by minimum eligible count across splits (28 topics), using 32 A,
32 B, 32 validation, and 32 test documents per topic.

Run LB/decommon 40k/80k at all 12 layers on the actual Gate input. Estimate
pooled top-64 from the independent domain-balanced pool and fit every
condition residual basis only after removing it.

## 6. Conditions, Seeds, And Checkpoints

Seven domains, 28 nested topics, 256 label permutations, 64 matched random
groupings, 256 complement-Haar draws, and centered-top-64 comparison. Seed is
20260731. Layers/checkpoints/pairs are not independent seeds.

## 7. Primary Metric

$$
O(c,d)=\frac{\|U_c^{A\top}U_d^B\|_F^2}{64},\qquad
\Delta O=\operatorname{median}_cO(c,c)-
\operatorname{median}_{c\ne d}O(c,d).
$$

Use 200 document/basis bootstrap refits followed by 2,000 domain-block
bootstrap summaries. A positive domain model-level lower
bound above permutation q95 establishes condition-varying projectors but not a
shared envelope; positive cross-capture margin is additionally required.

## 8. Secondary Metrics

Within/cross capture and their ratio, centered-top overlap, layer profiles,
40k/80k change, descriptive LB/decommon differences, and within-domain versus
cross-domain topic decomposition.

### 8.1 Approved document-level mechanism follow-up

On 2026-07-31 the researcher explicitly approved a stricter follow-up using
the already captured activations. For every `domain_a` and `domain_b` document,
subtract its own token mean, remove the independently fitted pooled top-64,
and fit a rank-64 residual projector from that document alone. Compare equally
many same-domain and cross-domain document pairs with

$$
O_{s,t}=\frac{\|U_s^\top U_t\|_F^2}{64}.
$$

For the same pairs, report the fraction of target residual variance captured
by the source-document basis, both absolutely and relative to the target's own
rank-64 optimum. Repeat the calculation for per-document centered top-64 as a
comparator. This follow-up distinguishes stable exact directions from changing
directions inside a shared variance envelope. It is a mechanism refinement,
not a replacement for the registered condition-level primary metric.

## 9. Known Good / Known Bad / Known Confusing Cases

Self-overlap is one; independent Haar-64 q95 should match the known near-0.09
scale. High within/lower cross with null-level capture means isolated modes,
not an envelope. Similarly high within/cross supports global sharing. Labels
must not be interpreted as a causal semantic representation.

## 10. Stage-Level Profiling Plan

S0 manifest; S1 actual-input/no-op smoke; S2 four endpoint captures; S3 domain
analysis; S4 topic/null analyses; S5 bootstrap, figures, and verdict.

## 11. Runtime And Resource Contract

Run LB on local H100:0 and decommon on H100:1. Raw activation caches remain on
the worker surface. Only curated tables, figures, and evidence records enter
the research mainline.

## 12. Pass / Fail / Insufficient

Pass conditional modes requires positive domain $\Delta O$ lower bound above
permutation q95, positive cross-capture-margin lower bound, and topic
directional replication. Precise high within≈cross is Fail/global-shared;
failure to beat permutation is Fail/label-specificity. Failed reliability,
replay, sample, or precision guards is Insufficient.

## 13. Output Contract

Domain/topic pair tables, model summaries, null tables, one overlap/capture
two-panel figure, summary/detailed records, and an experiment-named Chinese
five-section knowledge update; no new daily `focus.md`.

## 14. Claim Boundary And Next Decision

This experiment answers condition-stratified geometry only. Geometry can
interpret routing trajectories but cannot guarantee training benefit. The
separate matched 2B experiment found distribution changes without NLL gain.
