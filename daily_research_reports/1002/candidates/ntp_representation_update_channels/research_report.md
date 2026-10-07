# Natural-text responses to shared updates: a stage study in S7's representation space

**S7 shows helpful domain means with mixed individual finite-update effects, and modest response information readable from pre-update representations. A sparse autoencoder (SAE), an analysis network encoding activations into a few nonzero coordinates and reconstructing them, provides useful coordinates, but their differences do not faithfully reconstruct these small native displacements.** All measurements use previously exposed natural texts and are exploratory. Long-term net separation benefit remains unresolved.

2026-10-02. Candidate work outside the formal project. The researcher requested mechanism analysis together with exact natural texts, using S7 and its existing SAE sidecar. New design choices and the next decision are AI proposals. [中文](research_report_cn.md) · [Anchor](history/20261002_before_capacity_refinement/reading/anchor.md) · [Protocol](history/20261002_before_capacity_refinement/reading/protocol.md) · [Full derivations](mathematical_analysis.md) · [Process](research_process.md).

**Deeper update (from2026-10-02 17:30 UTC):** the previous99% mean component averages A/B batches within each domain; it is not the common response across four domains. Relative domain effects partly reproduce. Removing amplitude along the selected common parameter axis retains about69% of derivative cross-half response inner product. Yet an earlier-prefix forecast of eight future targets yields only about0.077%/0.289% incremental SAE Q, with stronger ordinary projections. Inputs annihilated in the current output still contribute to update effects; this is neither a lost-information fraction nor an identified cause of low Q. See [domain effects, continuations and visible information](domain_response_structure.md).

**Continuation update (from 2026-10-02 16:35 UTC):** frozen predictors retain about 0.48%–0.60% finite-response prediction-error improvement across two sources with disjoint records. About 99% of the current fixed-regularization own-source absolute MSE improvement comes from the within-domain A/B mean response. Within-domain A/B contrast-specific tuning yields an SAE gain of about 0.009%: very small, but not established as zero. These are two-source exploratory readings on the old panel under previously constructed features, not general source-population transfer. See the [source-transfer continuation](source_transfer_addendum.md).

## 1. Purpose: what response are we trying to explain?

The operation begins with source texts supplying mean pure next-token loss gradients and recipient texts measuring consequences. Source A and recipient B here are data roles, unlike the later A/B source banks. Change only the final attention output matrix. Send the recipient's changed activation through the unchanged residual, MLP, normalization and vocabulary head, and recompute true-next-token cross-entropy. Updated minus original loss is the finite loss change; negative means help. This comparison distinguishes apparent representation/gradient association from the measured consequence of a specified update.

The sparse autoencoder (SAE) is a separately trained, frozen analysis tool: an encoder extracts a few nonzero activation coordinates and a decoder reconstructs the activation. Coordinate prediction and endpoint differences test whether this tool explains the actual update, not whether it replaces LM training. The old INSUFFICIENT verdict means evidence did not resolve the registered effect; NON_SUPPORT means the original registered prediction lacked support. Those verdicts remain attached to their original questions.

The broader question asks which data should share parameters and when separation has net value. Human domain labels organize observations but should not supply the answer in advance.

This round asks a smaller question: **after source texts change a shared parameter matrix, how does another text's representation move, how does its true next-token loss change, and how much can its pre-update representation explain?** The object connects representation analysis to an actual learning consequence.

Prior work already includes gradient geometry, SAE activation, directional sensitivity and some finite interventions. The old natural-statistics primary result remains INSUFFICIENT: \(T=0.006637\), 95% interval \([-0.003738, 0.017012]\), unable to distinguish zero from the historical candidate 1% scale. Today's changed question/comparison cannot rewrite that verdict. [Old result](../../../../Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/summary.md).

A separate [earlier representation predictor](../../../../Projects/from-attention-to-search/main/experiments/shared_updates/natural_ntp_representation_compatibility/20260930/summary.md) produced qualified NON_SUPPORT. It predicted pairwise DCLM-event gradient inner products from matrix inputs, testing at least 5% improvement over a mean constant; measured \(Q=-0.000138\). Today's target is the response of N8 scientific texts to a fixed **aggregate source update**, with different inputs, lexical/scale baseline and exposed data. The historical 5% threshold/verdict remain attached to that experiment. The new candidate zero boundary tests the specified readout relation only; a scientifically useful scale remains Unknown. These are not success-rate comparisons for the same prediction task.

## 2. Hypothesis: why might representation help, and what is the strongest rival?

Candidate hypothesis: context, actual continuation and current model error jointly determine update demand. Pre-update representations may carry readable response information beyond simple lexical composition. An SAE is one tool for reading it.

Rival: apparent domain properties mostly reflect recurring tokens, local history, target identity and common update directions. SAE may recode that composition, and ordinary native projections may read it as well or better.

Four quantities must remain separate: activation, sensitivity to a direction, actual movement through the direction, and signed true-target effect. The first two cannot substitute for the last two.

## 3. Analysis method: close the chain from text to actual loss

### 3.1 Use one model state for every object

Freeze S7 at 33B training tokens; 33B is not parameter count. Study only its final attention output matrix \(W\), with 2048-dimensional input \(c\) and 1024-dimensional native output \(a=Wc\). The existing SAE observes \(a\), not \(c\).

For prefix \(x\) and true next token \(y\), let \(e\) be the native-output loss gradient. The matrix gradient is

\[
G=ec^\top.
\]

Average source gradients into \(M_A\), then apply the diagnostic matrix change \(-\eta M_A\). Another event's native displacement is exactly

\[
\Delta a_A=-\eta M_Ac.
\]

Feed this displacement into the native downstream model and measure actual next-token loss difference \(I_A\): positive is adverse, negative is helpful. No SAE reconstruction replaces the forward pass. The direction comes from pure NTP loss and is an ordinary SGD-form diagnostic, not a replay of S7's AdamW or SAE-augmented training step. There is no later cross-position attention; temporary full-matrix forwards qualified the native tail replay.

### 3.2 Separate records before constructing comparisons

The old panel contains 2048 scientific-text records, 16 targets each, for32768 events across computer science, mathematics, physics and biology. Old F and old R each contain1024 records; both were exposed by prior work.

Split old F again. Its half0 supplies512 source records, 128/domain. Its half1 supplies512 source-validation and response-fitting records. Old R supplies1024 readout records. The roles do not share rows, but old R is not new confirmation, and missing paper identity limits independent-record inference.

The F-determined step is \(\eta=0.05731845587090156\), giving a pooled-source relative RMS output displacement of 0.001. Also evaluate half-step. Use the same step for all four sources. Full-R evaluation has 16384 events under each of four sources and two step lengths. There is no new LM/SAE training or remote submission.

### 3.3 Each analysis step answers one question

The learned object in this step is a response predictor. Measured source-update responses supervise coefficients mapping pre-target features to predicted effects; a squared-coefficient penalty constrains fitting. This is ridge regression; neither the LM nor the SAE continues to learn. PCA selects linear activation-variance directions from fitting data, whereas random projection uses fixed random directions. They test whether an apparent SAE advantage is also available through ordinary projections, not the information-theoretic ordering of representations.

| Step | Operation | Question |
| --- | --- | --- |
| Actual response | Source-validation loss, all-R finite effects, derivative approximation | Does the direction help its source, and what happens to other events? |
| Pre-update readout | Common lexical/scale baseline, SAE augmentation, native controls and separate target diagnostic | What is readable before the target, and what depends on knowing it? |
| Direction fidelity | Native displacement, all-coordinate SAE difference, residual, fixed subspace/complement | Do SAE coordinates carry the movement faithfully, and how do components relate to the total? |

Ridge regularization uses F-only cross-validation. Initial models predict the derivative; without refitting, their scaled outputs are evaluated against actual finite labels. Later sensitivities add a preceding16-token bag, extend the regularization grid and swap F halves. Registrations/repairs preserve their order, but all analyses remain post-exposure exploration.

## 4. Conclusion: what can now be stated?

### 4.1 Helpful domain means coexist with many adverse events

The four source updates reduce their separate same-source validation mean losses by approximately0.000421, 0.002099, 0.000508 and 0.000291 nat. These are locally useful directions on records not used to construct them.

On all R, each of the16 source/readout-domain mean loss changes is negative, from−0.001953 to−0.000182 nat. Fixed-source record-bootstrap intervals are negative too, but omit source resampling, refitting and paper clustering. They are not16 confirmatory discoveries.

At the \(10^{-5}\)-nat sign deadband, 43.97%–52.81% of events across those conditions have higher loss; 1.00%–3.83% are unresolved. Mean help and individual adversity coexist.

![Finite means and adverse-event fractions](figures/finite_mean_and_events.png)

Figure 1: left values are in thousandths of a nat, negative helpful; right values exceed the positive deadband. Same four sources, 1024 R records and 16 targets/record. [Complete finite table](evidence/finite_panel_summary.csv) includes conditional intervals. Full-step absolute first-order approximation errors are 0.21%–0.77%; actual finite effects were measured rather than inferred solely from gradients.

Stage conclusion: domain means do not say every text benefits, while a harmed event does not by itself establish a stable conflict worth isolating.

### 4.2 Exact natural texts make the relation concrete

The [Chinese reading companion](research_report_cn.md) displays short original prefix excerpts. The table below identifies the same four events without repeating their text. All columns in a row share one prefix, actual target and pre-update representation; only the source update changes. Values are \(10^{-3}\) nat.

| Record / zero-based position | Actual target token | CS source | Math source | Physics source | Biology source |
| --- | --- | ---: | ---: | ---: | ---: |
| cs.CL/test/9274 /206 | ` notorious` | +3.779 | +0.540 | −1.076 | +1.934 |
| math.NT/test/5479 /78 | `1` | −1.938 | −0.822 | +0.706 | +0.424 |
| physics.optics/test/223 /14 | ` the` | +0.030 | +0.045 | −0.167 | +0.205 |
| q-bio.GN/test/39 /206 | ` distributed` | +3.254 | +1.856 | −4.006 | −4.170 |

These are post-hoc illustrations. Within each domain, filter for events with both positive and negative source effects, then select the minimum identity hash. They are not chosen by semantic typicality and are not a statistical test. [Case provenance](evidence/cases.json) records IDs, positions, hashes, selection and native responses. Displayed excerpts show only the prefix tail; the model sees all preceding tokens.

The first case shows why a CS record need not benefit individually from a CS source update. The learning relation depends on text, source update and current model state, not domain name alone.

### 4.3 Pre-target readout gains are modest; target identity explains more

Define \(Q=1-\mathrm{SSE}_{\rm augmented}/\mathrm{SSE}_{\rm baseline}\). A 1.41% value is lower error when predicting responses, not a1.41% LM loss improvement. The following uses pooled SSE across sources; high-error sources carry more weight.

| Comparison | Result | Boundary |
| --- | ---: | --- |
| Initial SAE predictor → actual finite response | +1.41%, conditional 95% interval[0.71%, 2.06%] | Short lexical/scale baseline; no finite-label refit |
| Same comparison, PCA320 | +2.26% | Native projections also help |
| Same comparison, random320 | +2.53% | No SAE-exclusive advantage |
| Strong-history baseline +SAE, derivative response | +1.11%; swapped halves+1.21% | Later exploration; equal-source means about 0.76%, 0.89% |
| Strong-history baseline +actual target | +23.92%; swapped+21.03% | Available only after the target |
| Add SAE after target features | −1.76%; swapped−2.67% | No gain for this finite-sample readout, not an information-theoretic absence result |

![Representation and target-identity readouts](figures/response_readout.png)

Figure 2: paired, category-stratified record intervals condition on sources and fitted predictors. The left explicitly distinguishes finite/derivative labels and short/strong baselines; these are not one registered comparison. The right is an after-target diagnostic. [Finite readouts](evidence/finite_prediction_readout.csv), [sensitivities](evidence/robust_prediction_readout.csv). Whole-record shuffled-label controls yield about−0.57% and−0.64%, not the same positive gains.

Stage conclusion: there is a small repeated exploratory readout gain and a strong target-composition rival. This motivates independent-record testing, not a pure semantic mechanism or ready-to-use Router.

### 4.4 Accurate static SAE reconstruction does not guarantee displacement fidelity

On a metadata-selected64-record R panel with 1024 events, mean static relative squared reconstruction error is 6.51%. Comparing complete 30000-coordinate sparse endpoints gives:

- With unchanged support, dynamic residual energy is about 0.979–1.000 times true displacement energy.
- Full-step support changes occur for7.6%–11.8% of events. Including them raises aggregate dynamic residual ratios to about 48–82; halving the step does not cure the problem and increases the aggregate ratio.

![Static and dynamic SAE fidelity](figures/sae_static_and_dynamic.png)

Figure 3: static error divides by native-state energy; dynamic error divides by true-displacement energy, so denominators differ. The dynamic axis is logarithmic. [Endpoint table](evidence/endpoint_summary.csv). Because the map is not an orthogonal projection, one minus this ratio is not automatically explained variance.

With frozen SAE \(a=b+D\alpha+\varepsilon\),

\[
\Delta a=D\Delta\alpha+\Delta\varepsilon.
\]

Residual change cannot be dropped. With unchanged positive support, the code difference transmits \(D_SE_S\Delta a\), of rank at most32 and not necessarily close to the identity. A support switch can jump the reconstruction while residual compensates for the continuous native state.

S7 endpoint checks agree with this local formula to within 0.20% relative error on stable support. Every event satisfying the sufficient TopK-margin certificate remains stable. [Local map audit](evidence/local_map.csv). A mathematical counterexample gives arbitrarily low static error with arbitrarily high dynamic error; see [§6 of the derivations](mathematical_analysis.md).

Stage conclusion: the SAE remains useful for activation patterns, candidate directions and readable coordinates. Update mechanism analysis must retain native movement and residual. This limitation for the tested small displacements is not a claim that SAE is generally useless.

### 4.5 Measure adverse components and helpful totals together

Take the first32 left singular directions of decoder columns for64 old-F-selected common atoms. This is a rank32 subspace, not32 independent semantic atoms. Evaluate full update, only this component and its removal, with a random rank32 control.

On the64-record R panel, the symmetric two-component finite allocation is helpful on average, yet about 14%–17% of events have an adverse common component and a helpful total. Random subspaces also show this, so it is not an SAE-exclusive mechanism. The allocation explicitly averages adding each component first and last; it is not unique atom causation. [Two-component finite table](evidence/finite_two_component_attribution.csv).

Stage conclusion: locating an adverse channel is different from establishing net benefit from removal. Even a beneficial one-step removal would not establish long-term separation value.

### 4.6 Changing source halves preserves average help but flips some individual effects

Fixed-source intervals omit whether a different same-domain source set helps/hurts the same events. We first compared source matrices and derivatives across F halves, then directly evaluated the F-half1 source updates on all R. This finite check completed in 112.4 seconds, with exactly matching baseline and unchanged model-state hash.

| Source domain | Source-matrix cosine | Centered finite-response correlation | Same-sign finite responses | Mean R effects for the two halves, \(10^{-3}\) nat |
| --- | ---: | ---: | ---: | ---: |
| Computer science | 0.137 | 0.469 | 63.91% | −0.313 / −0.290 |
| Mathematics | 0.422 | 0.890 | 79.13% | −0.808 / −0.810 |
| Physics | 0.154 | 0.641 | 66.38% | −0.356 / −0.511 |
| Biology | 0.100 | 0.554 | 63.64% | −0.334 / −0.366 |

The same-sign denominator includes events outside the \(10^{-5}\)-nat deadband under both updates, 95.3%–97.2% of all events. Among them, 20.87%–36.36% reverse sign; the all-event reversal fractions are 20.28%–35.08%. All16 domain means for the second source half are also helpful. Two observed source sets do not estimate stability across the full source population. [Source matrices](evidence/source_matrix_repeatability.csv), [actual finite repeatability](evidence/finite_source_repeatability.csv).

Stage conclusion: in these two source sets, average help is more stable than identifying a specific event as harmed. Fixed-source prediction improvement is not automatically a stable data property. The candidate Protocol deliberately tests fixed-source information; source-transferable learning relations require an additional new-source test, not merely a tighter target-readout interval.

Parameter angle alone also cannot characterize functional stability. The math source has matrix cosine 0.422 but finite-response correlation 0.890. Readout texts do not weight every parameter direction equally: first-order response correlation is weighted by their true-gradient covariance. This exact linear identity appears in §5 of the derivations; that covariance cannot be silently replaced by model Fisher. The [finite correlation addendum](evidence/finite_response_correlation.csv) was computed after seeing sign results and is explicitly descriptive, without changing the primary interpretation.

## 5. What mechanism bridge was added, and what remains open?

Let \(p_x\) be model prediction, \(q_x\) the unknown natural continuation distribution, and \(J_x\) the native-output-to-logit Jacobian. For fixed source define \(t_A=J_xM_Ac_x\). Then

\[
h_A(x,y)=t_A(x)_y-p_x^\top t_A(x),\qquad
\mathbb E[h_A\mid x,M_A]=t_A(x)^\top(q_x-p_x).
\]

Identical prefixes can have opposite realized effects for different next tokens. Mean response also depends on model/data mismatch. One realized continuation per prefix does not identify \(q_x\), and S7 calibration has not been established.

Under the additional theoretical condition \(p_x=q_x\), the first-order conditional mean is zero while variance can remain positive and equals the model-Fisher quadratic form along the movement. The expected loss of a fixed finite perturbation is then nonnegative KL. Sensitivity, single-event adversity and stable mean conflict are therefore distinct. The mathematical companion derives the second-order curvature/source-noise relation and a counterexample in which sharing averages noise down.

These are conditional derivations, numerically checked with identity errors below \(10^{-14}\), not new natural laws. [Identity checks](evidence/derived_identities.json). The remaining bridge is whether the local relation repeats for new independent records and new sources, and whether separation preserves useful sharing while improving long-term outcomes.

## 6. One next decision

AI proposal: confirm whether representation adds finite-response information for new natural texts under fixed sources. Keep a strong lexical/scale baseline, SAE primary arm and native controls. Aggregate equally across sources to prevent large math-source errors from dominating. Select only on fitting records, then read new confirmation once. The complete candidate Protocol remains `DRAFT_NOT_EXECUTABLE`.

The researcher must settle the independent unit/population and the increment needed to justify a later design. Current exploration cannot promote itself. SAE does not need to win to remain useful; actual source/readout responses and dynamic fidelity must stay in the comparison.

## 7. Evidence, execution boundary and relation to prior work

Code, raw arrays, registrations, failures and receipts live in the [execution workspace](/data/250010109/MoE_Router/experiments/20261002_s7_representation_update_channels/README.md). This folder holds selected tables/figures and a [payload manifest](payload_manifest.json). [Collected receipts](evidence/execution_receipts.json) preserve source locations and hashes.

Full-R replay exactly matches overlapping small-panel results and preserves the model-state hash. Initial finalization failed because a probe loop label shadowed the model variable; the first repair missed a per-source branch. Both logs remain, and the same conditions were rerun successfully. No unfavorable condition was dropped. Source/math checks do not establish every Markdown rendering.

No broad novelty claim is made. Relevant primary work includes [TracIn](https://arxiv.org/abs/2002.08484) for gradient effects; [Kunstner et al.](https://arxiv.org/abs/1905.12558) for empirical/model Fisher distinctions; [Task2Vec](https://arxiv.org/abs/1902.03545) and [NTK overlap](https://arxiv.org/abs/2010.04003) for task geometry; [GradSAE](https://aclanthology.org/2025.emnlp-main.87/) for output-related directions beyond reconstruction; [Attribution Graphs methods](https://transformer-circuits.pub/2025/attribution-graphs/methods.html) for residuals and intervention checks; and [Integrated Gradients](https://proceedings.mlr.press/v70/sundararajan17a.html) for path attribution. We use our native model and frozen SAE, without training those methods or claiming priority from this bounded search.
