# Shared SAE Atom Reuse as a Candidate Explanation of S7's Low Effective Dimension

Problem key: `sae_shared_direction_reuse`.
Question and mechanism: HUMAN_CONFIRMED in the
[0922 Focus](../../../../focus/focus_sae_shared_direction_reuse.md).
Exact metric/panel/statistical decision: HUMAN_CONFIRMED on 2026-09-22 by
“确认，按这套判据执行”. Full frozen audit is authorized after smoke PASS under
Protocol A2. This confirms design/execution, not the future mechanism judgment.

## 1. Problem Definition

**On identical inputs, does S7's lower native attention-write effective dimension
coincide with stronger reuse of the same SAE atom identities across examples than
SALL?** This inherits the [parent's](../15_17_three_model_sae_representation_trajectory_anchor.md)
question of how a training-time sparse-autoencoder (SAE) sidecar reshapes native
representations, but adjudicates only one candidate explanation of concentration.
An atom is one decoder dictionary column; its ID is meaningful within its own
model only. Effective dimension counts equivalent variance-bearing directions,
not semantic concepts. The attention write is the vector after output projection
and before residual addition, not the SAE reconstruction.

S7 is a final-layer sidecar branch reweighted from coefficient 1 to 0.1; SALL is
the original all-eight-layer sidecar. Their histories and architectures are not
a matched coefficient experiment. Both checkpoints are at exactly 21B valid
prediction tokens. The missing link is same-panel, model-local support reuse:
support means the atom IDs selected by the native encoder for each valid token.
A positive necessary-condition test keeps the explanation viable; a resolved
negative one weakens this specific explanation; measurement or uncertainty
failure leaves it unknown. Semantics, task utility, and training causality are
outside this subanchor.

## 2. Physical Priors

HUMAN_CONFIRMED candidate: a model may accommodate sparse reconstruction pressure
by reusing a smaller shared set of dictionary atoms across examples, making low
global dimension possible. This is not a theorem about Top-K: each token can use
32 atoms while different tokens use disjoint supports. Even shared supports do
not determine covariance rank, because coefficients, decoder geometry and
reconstruction error also matter. The proposed observable tests the same-ID
version of this explanation, not every meaning of geometric direction reuse.

## 3. Falsifiable Hypotheses

H1 predicts higher cross-example same-ID reuse in S7 together with lower native
effective dimension on the same examples. Its intended causal story is sparse
reconstruction pressure → shared support reuse → reduced global direction
diversity; E01 measures an association needed by this particular story, not
those causal arrows.

H2 allows low dimension without greater same-ID reuse: different atom IDs can
have aligned decoder directions, or their coefficients can co-vary along a few
joint directions. H1 and H2 can coexist. Passing H1's necessary prediction does
not discriminate their relative contributions. A popular small set of atoms
is an instance of H1, **not** an explanation to subtract as an unwanted null.
The earlier chat's excess-overlap null is therefore not adopted.

## 4. Mathematical Model

For example \(i\), valid token \(t\), and model-local atom \(j\), let \(S_{it}\) be the
native encoder's size-\(K\) selected support, with \(K=32\). Let \(T_i\) count valid
body tokens and \(u_{ij}\) be the fraction of that example's selected slots using
atom \(j\):

\[u_{ij}=\frac{1}{T_i K}\sum_t\mathbf{1}[j\in S_{it}].\]

HUMAN_CONFIRMED definition: quantify reuse by the mean cosine of these frequency profiles,
not by treating a whole multi-token example as one Top-32 set:

\[R=\frac{2}{n(n-1)}\sum_{i<q}\frac{u_i^\top u_q}{\|u_i\|_2\|u_q\|_2},
\qquad \Delta R=R_{\mathrm{S7}}-R_{\mathrm{SALL}}.\]

\(R\) is dimensionless and compares atom frequencies, not amplitudes, meanings,
or cross-model feature identity. Similar frequency profiles may arise from
different token arrangements; this is not a tokenwise semantic-equivalence test.
Zero-valued selected slots and ties require explicit identity guards.

Let \(a_i\) be the mean native attention write over exactly those tokens, and
\(\Sigma_a\) its centered sample covariance. The aligned guard is
\(d_{\rm eff}=(\operatorname{tr}\Sigma_a)^2/\operatorname{tr}(\Sigma_a^2)\).
Lower \(d_{\rm eff}\) means concentrated variance; it is not evidence of better
or worse semantics. A sparse reconstruction is \(\hat a=Dz+b\) while the native
write is \(a=\hat a+e\); support reuse alone cannot control all three covariance
contributions from \(Dz\), residual \(e\), and their cross-covariance.

The researcher subsequently selected a within-S7 history control: exact17B fresh lambda0.1 versus reweighted1→0.1, keeping the same observation and R definitions. Define DeltaR_history=R_reweighted−R_fresh without assuming its sign. Report the paired95% interval and native dimension ordering separately; the E01 directional necessary-condition rule is not transplanted to this pair. This addresses an architecture confound, not the causal share of support reuse.

## 5. Computational Realization

Use frozen 21B S7 and SALL, layer 8, width 30,000, K=32, identical N8 tokenized
records and masks. The inherited observer panel has 192 records of 256 body
tokens each. It was historically category-stratified; E01 freezes those IDs
without accessing labels for new selection, analysis, thresholds or interpretation.
Record-level sampling does not establish independent source articles.

Adopt the verified checkpoint loader, native-write hook and mean-pooling helper
from the existing audit. Adapt extraction to call the native `sae.encode()`.
**Do not reuse cached selected IDs as if they were native Top-32 IDs:** source
inspection found that the old observer uses `topk(128)[:, :32]`, which can select
different boundary IDs under equal scores. Fresh same-pass native support and
native means avoid splicing statistics from different panels. Do not change
training code, fit an SAE/probe, align IDs across models, or subtract the earlier
chat's popularity-preserving null.

The exact engineering and future scientific scopes are owned by
[E01 Protocol](../../../../experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/protocol.md).

## 6. Minimal Falsification Tests

HUMAN_CONFIRMED scientific rule: 2,000 paired example resamples (seed 20260922)
produce a percentile 95% interval for \(\Delta R\). With identity guards and lower same-panel
S7 \(d_{\rm eff}\), an interval wholly above zero passes the necessary-condition
test; one with upper bound at or below zero fails it; overlap with zero, an
unreproduced dimension ordering, or identity failure is insufficient. Lack of
statistical significance is not equivalence. Global atom-use concentration is
descriptive and cannot rescue a failed primary test. No numerical scientific
threshold is learned from smoke outputs.

The user-authorized [E02 protocol](../../../../experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E02_s7_17b_training_history_reuse_audit/protocol.md) owns the17B control. Both checkpoints have the same recorded initial parameter hashes, current last-layer sidecar and reconstruction weight0.1. Reweighted history changes at15.465567744B; microbatch/accumulation and CE chunking differ from fresh training, so isolated history causality remains unavailable. The user explicitly waived new smoke; full embedded measurement guards remain required.

## 7. Current Evidence

VERIFIED_EVIDENCE: the [E01 summary](../../../../experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/summary.md) reports the frozen21B same-panel comparison. S7 versus SALL gives Delta R=+0.085788, paired-record95% CI[0.072687,0.098599], with native effective dimension14.486918 versus17.160447. This meets the previously approved necessary-condition rule; independent numerical/artifact verification passed. It does not determine causal contributions. The older full-panel dimension values are not substituted for this aligned result.

Native Top32 versus same-forward top128-prefix32 supports matched on all tested tokens in both conditions despite boundary ties. The hypothesized support-extraction discrepancy was not observed here. The [Detailed record](../../../../experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/detailed.md) owns full setup, qualification, failures and provenance. Researcher mechanism judgment remains AWAITING_RESEARCHER.

## 8. Claim Boundary And Next Decision

The registered necessary prediction is observed; no causal mechanism is promoted. Per-token sparsity still does not imply global low dimension. Decoder geometry, coefficient covariance and reconstruction-error contributions remain unresolved and can coexist with greater same-ID reuse. No claim follows about regularization strength alone, semantic quality, task utility, optimal K or training evolution. Record-level uncertainty does not cover training seeds or establish article independence.

The researcher's current next decision is refined by the requested E02 control: after the same-S717B comparison, decide whether the observed reuse/geometry difference remains associated with training history once sidecar topology and current coefficient match. E02 is NOT RUN at registration; a resolved interval shows a bounded checkpoint difference, an unresolved interval is not equivalence, and guard failure requires measurement repair. Resume at [E02](../../../../experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E02_s7_17b_training_history_reuse_audit/protocol.md); geometry-versus-support causality remains deferred, not approved. Human mechanism judgment awaits verified results and the researcher's interpretation.
