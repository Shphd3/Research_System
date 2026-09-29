# Anchor: Can natural NTP representations predict local update compatibility?

Status: **DESIGN_ADOPTED_FOR_EXECUTION / RESULT_UNKNOWN**. On 2026-09-29 the researcher explicitly directed Smoke submission and supervision followed by Full submission if it passes, adopting the companion Protocol's exact proposal for execution. Technical gates are not thereby passed; scientific result and next judgment remain Unknown. Problem key: `natural_ntp_representation_compatibility`. [中文](anchor_natural_ntp_representation_compatibility_cn.md) · [Protocol](protocol.md) · [Protocol 中文](protocol_cn.md).

## 1. Problem Definition

At the fixed S7 reconstruction-weight-0.1 checkpoint trained for 33B tokens, can complete input representations of natural next-token events predict continuous gradient compatibility at the last attention output matrix on independent documents, reducing mean squared error by at least 5% relative to a constant predictor?

The parent purpose is to inform sharing/separation decisions. The immediate uncertainty is whether representations contain extractable local-update information worth locating in a compact representation. Use natural prefixes, genuine next tokens and native forward activations; do not inject synthetic vectors or flip labels. All effects may be helpful: differences in benefit remain informative.

One experiment measures compatibility, evaluates representation-only prediction and checks finite one-step meaning. Support motivates structural comparisons; non-support weakens this operationalization; insufficient evidence identifies measurement, sampling or precision limitations. This does not decide long-term isolation benefit, multi-billion-parameter generality or causal feature use.

## 2. Physical Priors

**Empirical prior:** natural NTP contexts and continuations share a data-generating distribution; historical training shapes representations that may carry statistical information about downstream error signals. The current loss does not change the already-computed representation in the same forward pass, and the representation need not uniquely determine the target.

Input coupling and predictable error-signal relations may jointly produce predictable compatibility. Failure to reach the held-out threshold weakens this premise within the specified operationalization, not the gradient identity itself.

## 3. Falsifiable Hypotheses

**H1:** information in complete pre-update representations permits at least 5% held-out compatibility-MSE reduction over the training-mean prediction.

**R1:** target and downstream-sensitivity variation remaining after conditioning on the representations leaves extractable gains below that threshold; apparent success may reflect memorized documents or the overall mean. Deduplication, document-first splitting and sealed confirmation distinguish these explanations.

Simple geometry is also representation information. Its success supports H1; improvement beyond geometry is a separate secondary question. Failure of the specified estimators does not prove that every function must fail.

## 4. Mathematical Model

Freeze the original model and temporarily change only the last attention output matrix. One event uses 256 original tokens as prefix and original token 257 as target. At the final prefix position observe full input vector, output vector and the event's own residual input. The input has 2048 coordinates; the output has 1024. Full-vocabulary cross-entropy is in nats per target:

\[
a_i=W_0c_i,\qquad \ell_i=-\log p_{\theta_0}(y_i\mid x_i),\qquad e_i=\partial\ell_i/\partial a_i,\qquad G_i=e_ic_i^\top.
\]

The downstream path receives both output and sample-specific residual. Only positionwise operations follow the last attention projection, so a single target is expected to contribute at one position. Verify against full-forward autograd. If this fails, stop and revise the observation unit; do not silently call one vector a complete representation of a multi-position gradient.

The parameter-to-representation relation is exact; loss consequences are local:

\[
K_{ij}=\langle G_i,G_j\rangle_F=(c_i^\top c_j)(e_i^\top e_j),\quad
\Delta W_i=-\eta G_i,\quad\Delta a_j=\Delta W_i c_j,\quad
I_{i\to j}=-\eta K_{ij}+R_{i\to j}.
\]

Positive compatibility means first-order help; negative actual loss change means help. Use a common scalar SGD rate, no momentum or per-source normalization, and restore the same initial state for every update. Historical SAE auxiliary losses do not enter these gradients.

The statistical target is the conditional mean, with remaining conditional variation:

\[
\mu(c_i,c_j)=\mathbb E[K_{ij}\mid c_i,c_j],\qquad
\sigma^2(c_i,c_j)=\operatorname{Var}(K_{ij}\mid c_i,c_j).
\]

Squared-error fitting estimates the mean using training-pair gradient labels. Test inputs contain representations only, excluding targets, loss, gradients, domain labels and post-update quantities. Residuals combine conditional variation, estimation error and function-class limits; this experiment does not identify irreducible conditional variance.

## 5. Computational Realization

**Fixed carrier proposal:** `token_033000000000`, state SHA256 `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`; `model.blocks[7].attn.o.weight`, shape 1024 by 2048. The backbone has 281,431,040 parameters; with SAE, 342,902,064. 33B counts training tokens. [Configuration](</data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/resolved_config.json>) and [manifest](</data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000/manifest.json>) establish recorded identity. Files are visible; runtime loading and qualification have not run.

**Data:** one raw JSONL shard from DCLM global shard 02, file-level heldout relative to global-shard-01 training; exact path and freshly checked hash are in Protocol §5. One 256-to-1 event per document. After duplicate grouping, allocate 64 engineering, 4096 training, 1024 development and 2048 confirmation documents. No claim of universal natural-language sampling or complete pretraining/historical-evaluation novelty is made.

**Comparison:** constant training-mean predictor; geometry predictor using norms, inner product and cosine; nonlinear full predictor using all 2048 standardized coordinates, a shared two-layer encoder and symmetric pair head. Use common training pairs, squared error and development selection. Development selects one primary predictor from geometry/full before confirmation opens. A simpler successful representation predictor must not be classified as absence of information.

**Structural analysis:** after primary support, run the prespecified secondary PCA/random-rank curves and full-output versus frozen-SAE-output comparison. Readout limitations remain explicit. SAE does not replace the original forward path and is not retrained. Predictive readout is not the actual update path. Non-support/insufficiency does not automatically trigger this stage; structural results cannot rescue the primary outcome or authorize Router training.

## 6. Minimal Falsification Tests

The single primary statistic is relative held-out MSE reduction over the training-mean constant:

\[
Q=1-\frac{\operatorname{MSE}_{\rm confirm}(q_*)}{\operatorname{MSE}_{\rm confirm}(q_0)},\qquad q_0=\operatorname{mean}_{\rm train}K.
\]

Confirmation has 1024 prespecified pairs without shared documents, equally weighted. Use 2000 paired bootstrap draws and a two-sided 95% interval, conditional on fitted predictors and corpus. **The AI-proposed practical threshold is 0.05**, a continuation threshold for structural analysis rather than a routing-benefit threshold.

- **Support:** qualification passes and the lower bound exceeds 0.05. Geometry selection is valid support; report the full-versus-geometry increment separately.
- **Non-support:** qualification passes and the upper bound is below 0.05. A small positive gain can be reported without meeting the continuation threshold.
- **Insufficient:** the interval includes 0.05, target variation is below measurement resolution, split/seal failures occur or fitting fails. A single sign is not insufficiency.

Finite-step qualification is separate: choose predicted high/middle/low groups without confirmation truth, use a development-selected common rate and half rate, and measure both directions, source-event loss and remainder. Only a successful bridge extends the result to actual one-step loss prediction. Its failure does not erase a qualified compatibility result. Source-event improvement is not held-out source-task generalization.

## 7. Current Evidence

The [0926 natural-text result](../../0926/docs/structure_update/summary_cn.md) found domain separability together with average help in all 12 cross-domain directions at a 21B-token checkpoint and the last MLP down projection. This challenges separation-by-domain alone, but is not validation at the current 33B attention matrix.

The [0927 controlled result](../../0927/docs/shared_update_research_pack/summary_cn.md) uses the present 33B checkpoint and attention matrix and retains `MODULATION_WITHOUT_NET_HARM`. [0928 localization](../../0928/docs/shared_update_signal_localization/summary_cn.md) found a small adverse component offset by larger help; static PCA/SAE readouts did not locate most dynamic action. Target-derivative diagnostics are not representation-only prediction.

Natural-NTP prediction, finite checks and structural comparisons are all **NOT RUN**. This revision replaces the candidate criteria at the same Anchor path; the earlier two-round report remains discussion provenance rather than an execution contract. The prior Focus's pending human judgment remains unchanged.

## 8. Claim Boundary And Next Decision

Maximum claim: representations contain generalizable continuous local-update information within this model, matrix, corpus and estimator scope. Do not infer identified irreducible variance, causal SAE atoms, cross-model universality, long-term separation gains or multi-billion-parameter representativeness.

**Execution decision made:** complete the Protocol's Smoke qualification and, only if it passes, submit Full. The researcher has not yet confirmed the scientific interpretation, Focus conclusion or next scientific decision after results; all remain Unknown. Operational success does not supply those judgments.
