# A15_17_02: Native SAE Representation Concentration and N8 Domain Separability

## 1. Problem Definition

The decision question is whether representation concentration observed under a
training-time sparse-autoencoder (SAE) sidecar is accompanied by greater linear
separability of eight academic-source domains in the backbone's native layer-8
attention write at the same 17B valid-token coordinate. Domain separability here
means held-out N8 source-category accuracy of a fixed linear reader; it excludes
all-language semantics, model use, downstream utility and training efficiency.

The parent line established that native geometry and SAE atom use can change,
but those observations do not establish semantic improvement. The smallest
direction-changing uncertainty is therefore the missing same-model, same-panel
link between concentration and domain readout. Pass keeps a bounded readability
explanation viable; Fail stops using concentration as support for that explanation;
identity, data or measurement failure leaves it Unknown.

## 2. Physical Priors

HUMAN_CONFIRMED candidate prior: repeated domain-associated distinctions may
become easier for a simple reader if sparse reconstruction pressure organizes
them more consistently. The observable exposing this prior is held-out domain
accuracy on the native write. The prior is false for the tested setting if a
more concentrated condition has a resolved lower accuracy; it remains
unestablished if the contrast is unresolved. Sparse reconstruction has no domain
labels and may instead concentrate shared, scale-related or cross-domain
directions, which is the strongest live rival.

## 3. Falsifiable Hypotheses

H1 predicts that the exact-17B from-scratch coefficient-0.1 S7 condition is more
linearly readable than exact-17B Dense on the same N8 mean-pooled native writes.
It also permits the reweighted 1→0.1 S7 history to differ from fresh 0.1, without
assuming a monotonic coefficient effect.

H2 predicts that SAE history changes covariance concentration or observer use
without improving native domain distinctions. H1 and H2 separate on the
pre-registered held-out accuracy contrast. Clustering and between/within scatter
test the stronger claim that categories form clearer distance-based groups; they
cannot rescue a non-positive primary contrast. Training histories include known
microbatch, cross-entropy chunking and stochastic differences, so no contrast is
an isolated coefficient intervention.

## 4. Mathematical Model

For record \(i\) and its 256 valid body positions, let \(a_{it}\) be the layer-8
attention output after output projection and before residual addition. The
primary representation is

\[
a_i^{\mathrm{mean}}=\frac{1}{256}\sum_t a_{it}.
\]

For each frozen model \(m\), fit an L2-regularized multiclass linear reader on N8
fit records, select its regularization on development accuracy, and evaluate
test accuracy \(A_m\). In full mode the primary contrast is

\[
\Delta A_{0.1}=A_{\mathrm{S7\ fresh\ }0.1}-A_{\mathrm{Dense}}.
\]

The secondary history contrast is
\(\Delta A_{\mathrm{hist}}=A_{\mathrm{S7\ }1\rightarrow0.1}-A_{\mathrm{S7\ fresh\ }0.1}\).
Accuracy is a test-record proportion; it does not show that the language model
uses the distinction. Effective dimension
\(d_{\rm eff}=(\operatorname{tr}C)^2/\operatorname{tr}(C^2)\) and between/within
scatter \(B/W\) describe covariance concentration and centroid separation on the
same test matrix, not semantic quality by themselves.

## 5. Computational Realization

Use the frozen `N8_v1` panel: eight named M2D2 academic-source categories with
2,400 fit, 800 development and 1,600 test records, each represented by the
already frozen 256 input tokens and body mask. Preserve sample IDs, label names,
splits, token order and hashes. If those assets fail identity or leakage checks,
do not silently rebuild them under the same version.

Resolve three exact-17B checkpoints from their manifests: Dense, final-layer
S7 trained throughout with coefficient 0.1, and final-layer S7 reweighted from
1 to 0.1 near 15.47B. Use the verified checkpoint loader and native-write hook
from the completed representation audits. Adopt their production model sources,
checkpoint verification and pooling semantics; adapt extraction to save only
layer-8 mean and last-position native writes plus available S7 reconstruction
means; reject the older 192-record observer cache as a substitute for N8's 4,800
records. No model or SAE parameter is fitted or updated.

The reader uses fit-only centering and one global scale, a frozen L2 logistic
reader family, and development-only selection. K-means is fitted without labels
on fit vectors and scored by adjusted Rand index on test assignments. Exact
run settings and lineage are frozen in the E01 Protocol.

## 6. Minimal Falsification Tests

The decisive test is \(\Delta A_{0.1}\) on native layer-8 mean-pooled test writes.
In full mode, two pre-registered accuracy contrasts each receive a 97.5%
paired-bootstrap interval for directional declarations; in pair-only mode the
single history contrast receives a 95% interval. An interval wholly above zero
supports a positive difference, wholly below zero supports a negative difference,
and overlap with zero is insufficient, not equivalence. Resampling is stratified
by class at the record level unless verified source-document groups exist.

Necessary guards are exact checkpoint/token identity, identical N8 inputs and
masks, verified hook and pooling, no test access during preprocessing or model
selection, finite outputs, unchanged parameters, and deterministic repeat
forward. Smoke validates these engineering gates on a preselected subset plus
synthetic analysis invariants; it cannot set a threshold or support H1.

## 7. Current Evidence

VERIFIED_EVIDENCE from prior completed audits: on a separate 192-record panel,
fresh 0.1 S7 and reweighted 1→0.1 S7 had native effective dimensions 19.98208
and 8.41849, while their model-local atom-use similarities were 0.40498 and
0.62530. This establishes a history-associated geometry and observer difference,
not N8 separability. Historical 21B N8 measurements were mixed and cannot be
spliced into the 17B comparison. E01's bounded engineering Smoke passed on all
three exact-17B roles: each process read 16 frozen N8 development records and
4,096 body tokens, state remained unchanged, and same-process plus independent
fresh-S7 replay relative RMS were `0.0`. This qualifies the measurement path
only. E01's 17B N8 scientific result is NOT RUN; the complete conformance and
artifact map are in the [Detailed record](../../../../experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E01_n8_17b_separability_audit/detailed.md).

## 8. Claim Boundary And Next Decision

Supported now: the exact comparison, primary observable, live rival and
eligibility gates are fixed, and exact-17B assets are available for all three
roles. Unresolved: the primary and history accuracy contrasts, whether any
linear advantage is accompanied by distance-based grouping, and whether the
effect generalizes beyond these checkpoints and N8 source categories.

The study cannot establish that concentration causes readability, that SAE
improves semantics generally, that the model uses readable information, or that
training efficiency or language-model quality improves. Exactly one next
decision follows eligible full evidence: continue to retain the explanation
that SAE strengthens N8 domain separability, or stop using geometric
concentration as support for it. Completion requires the frozen full-panel
contrast and boundary; after Smoke alone, resume at full-run authorization and
leave the scientific decision unresolved.
