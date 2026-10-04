# Deeper structure: domain effects, realized continuations, and information available beforehand

**Updates from different domains have partially reproducible relative effects on the same text. These effects are not entirely explained by amplitude along the selected common parameter direction. Yet reproducibility after observing a realized next token is different from prediction using an earlier prefix. The current output representation also does not retain every input component that the matrix update may use.** These distinctions let structured effects, weak prospective readout, and poor SAE displacement reconstruction coexist.

Continuation beginning2026-10-02 17:30 UTC. This is exploratory work in the day's candidate directory, using the old panel and existing sources. No new LM/SAE training or remote run was performed. Scientific judgment and promotion remain researcher-owned. [中文](domain_response_structure_cn.md) · [Stage report](research_report.md) · [Derivations§10–11](mathematical_analysis.md) · [Process](research_process.md).

## 1. Purpose: correct the object that was easy to confuse

The previous statement that99.02% of improvement came from the mean referred to averaging responses from **two source batches A/B within each domain**. It did not average away the computer-science, mathematics, physics, and biology source domains. Consequently, the tiny previous A/B contrast readout cannot establish an absence of between-domain response structure.

We now separate changing the sampled records within one domain from comparing different source domains on the same recipient text and asking whether that comparison survives replacement of source records. The former includes source-sampling variation; the latter is closer to the data relationship of interest.

The [formal0930 natural-statistics study](../../../../Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/summary.md) already examined domain mean updates and sampling variation. This continuation adds their functional effects on recipient texts. Parameter distances and response distances use different metrics and cannot be exchanged directly. Earlier results and verdicts remain unchanged.

## 2. Hypothesis and rivals

The candidate explanation is that between-domain update differences interact systematically with recipient inputs and actual continuation demands, producing relative responses that partly reproduce across source batches and can partly be read from prefixes.

Three rivals require distinct checks: apparent domain differences are amplitudes along a common parameter direction; reproducibility depends on knowing the realized target and may be difficult to predict beforehand; and the observed SAE output omits input variables used by the update. The third is presently a computational-channel explanation, not an identified cause of weak readout. Ordinary projections remain controls; SAE superiority is not required.

## 3. Analysis method

Reuse S7 at33B cumulative training tokens, the final attention output matrix, and pure-NTP ordinary-gradient diagnostics. The matrix input is2048-dimensional \(c\), and its current output is1024-dimensional \(a=Wc\). Source matrix \(M_{s,d}\) averages gradients for source half \(s\in\{A,B\}\) and domain \(d\). Finite effect \(I_{s,d}\) is the realized next-token loss change after \(-\eta M_{s,d}\): positive is adverse, negative helpful.

A/B are complementary category/hash partitions of old F-half0, each with64 records per domain. Old F-half1 supplies512 fit records; old R supplies1024 readout records with16 targets each. The four roles have disjoint record identities, but this is not new independent-paper confirmation: R was exposed and earlier feature construction used A+B. The complementary halves are dependent conditional on their fixed finite pool.

For each event, center across the four source domains: \(V_{s,d}=I_{s,d}-\frac14\sum_e I_{s,e}\). This preserves relative effects with rank three; the six pairwise contrasts are not six independent repetitions. We score pooled squared error over four outputs, \(Q=1-\mathrm{SSE}_{\rm aug}/\mathrm{SSE}_{\rm base}\), which differs from the previous average of per-source-domain Q values.

The four ordinary frozen transfer predictors retain frozen strong lexical/history/position/scale features and SAE320, PCA320, or random320 enhancements, with ridge regularization10. They fit derivatives and scale predictions by the original step size when scoring actual finite labels. A→B freezes a predictor fitted to A responses and evaluates B; no finite-label refit occurs. The separate post-target composition diagnostic retains its earlier F selection, with regularization0.1 for target and target+SAE fits; prefix forecasting selects its own models. Intervals use2000 stratified paired R-record bootstrap draws, holding sources, fitting and selection fixed. They exclude source-population, paper-cluster and exploratory-selection uncertainty.

## 4. Conclusion: relative domain effects partly reproduce

A/B correlations of actual finite pairwise effects are0.586 for CS–math,0.251 for CS–physics,0.060 for CS–biology,0.461 for math–physics,0.479 for math–biology, and0.032 for physics–biology. Structure is concentrated in comparisons involving mathematics; this is not universal stable separation of four domains. [Correlations](evidence/domain_response_repeatability.csv)

Averaged over all events and four source coordinates, the cross-half inner product of centered finite responses is \(5.147\times10^{-6}\) nat squared, compared with average squared response \(1.257\times10^{-5}\), a ratio of40.93%. This is algebraic accounting for fixed A/B, not an estimated41% population signal fraction. After removing each source's mean R response, the ratio remains40.75%, so overall source helpfulness alone does not account for the description. [Energy accounting](evidence/domain_response_energy.csv)

Frozen SAE predictors improve prediction of these **relative finite domain effects** by **0.493% [0.349%,0.639%]** for A→B and **0.757% [0.609%,0.899%]** for B→A. random320 gives1.051% and1.352%; there is no SAE-exclusive advantage. Intervals cross zero for some weak domain pairs; a pooled positive result does not establish every pair. [Finite readout](evidence/domain_prediction_readout.csv)

### 4.1 Are these merely different amplitudes along a common direction?

Within each source half define \(\bar M_s=\frac14\sum_dM_{s,d}\), then project using the parameter Euclidean inner product:

\[
\alpha_{s,d}=\frac{\langle M_{s,d},\bar M_s\rangle_F}{\|\bar M_s\|_F^2},
\qquad M^\perp_{s,d}=M_{s,d}-\alpha_{s,d}\bar M_s.
\]

Residual matrices are orthogonal to that half's common axis and average to zero across domains. Applying the exact corresponding transform to derivative responses retains **68.53%** of the event-level cross-half inner product, or68.74% after recipient-mean removal. Correlation falls from0.411 to0.328. Residual SAE readout Q remains **0.407% [0.282%,0.540%]** for A→B and **0.577% [0.453%,0.702%]** for B→A. [Geometry](evidence/common_direction_geometry.json) · [Replication](evidence/common_direction_replication.csv) · [Readout](evidence/common_direction_readout.csv)

Pure amplitude along the selected common parameter direction therefore does not explain all observed replication. This uses step-scaled derivatives, not new finite interventions. Truth, baseline and augmented predictions use the same known evaluation-source coefficients; R fits no coefficients. The A/B common axes themselves have cosine0.258. This is a descriptive sensitivity analysis using source-defined axes, not a unique mechanism decomposition or exclusion of all scale, lexical and target-composition rivals. Parameter orthogonality does not imply response orthogonality; the retained inner-product ratio is not a mechanism-explanation fraction.

## 5. Why can an effect reproduce yet remain hard to forecast?

Let \(x\) denote a prefix, \(p_x\) the model next-token distribution, and \(q_x\) the unknown natural continuation distribution. Write the difference between two source-domain logit directions as \(\tau_s(x)\). Hold sources fixed and assume their conditional independence from the readout continuation given the prefix. For realized target \(y\), the first-order unit-step contrast is

\[
C_s(x,y)=\tau_s(x)_y-p_x^\top\tau_s(x).
\]

Hold the prefix and sources fixed, evaluate A/B using a shared random continuation \(Y\sim q_x\), and average over Y. The conditional response product contains both the product of prefix-conditional means and a covariance from sharing the same realized target. Even in the idealized case \(q_x=p_x\), the mean term vanishes while the covariance can stay positive. **Agreement about the same realized continuation need not require that its effect sign was predictable from the prefix.** This is a conditional derivation, not evidence that the current model is calibrated; zero first-order mean does not imply zero finite-effect mean. Actual targets belong to the learning task, so this covariance is not automatically a spurious relationship. [Derivation§10.4](mathematical_analysis.md)

A post-target composition diagnostic is compatible with this distinction: for centered derivatives from the original full F-half0 sources, adding actual target identity yields19.55% event-level Q; adding SAE after that gives−1.57%. These are finite-model prediction results, not a19.55% mechanism fraction or proof of no SAE information. [Composition](evidence/domain_target_composition.csv)

### 5.1 Record aggregation and genuinely earlier prediction have different information boundaries

Averaging the16 true effects and their16 predictions separately before scoring raises cross-half SAE Q to3.58%/4.21%. Later event prefixes contain earlier targets, however. This aggregates sequential local readouts and is not a forecast of the record made at its beginning. The gain cannot be attributed solely to noise removal.

A bounded prefix forecast therefore uses only averaged features from the first eight positions14…126 to predict average response at the later eight positions142…254, whose targets are143…255. Inputs stop at126; later-position features, actual targets and gradients never enter predictors. Record-level four-fold F validation selects ridge or a constant, then freezes fitting. Derivatives train the predictors and actual finite effects score them. Causality was audited in the actual cache and attention source code; no new truncated forward was run. [Time-boundary audit](evidence/prefix_forecast_causal_audit.json)

| Information and evaluation time | SAE A→B Q | SAE B→A Q | random320 A→B / B→A |
| --- | ---: | ---: | ---: |
| Event prefix predicts that event | 0.493% | 0.757% | 1.051% /1.352% |
|16 sequential predictions, then record averaging |3.584% |4.208% | See full scale table |
| Earlier prefix predicts future-eight mean |0.0766% |0.2892% |1.2253% /0.9875% |

The last row's SAE intervals are[0.0511%,0.1013%] and[0.0905%,0.4889%]. For A fitting, the history baseline selects a constant and SAE/PCA select the regularization-grid upper boundary1000; B fits select100. Thus not every enhancement beats an effective nonconstant lexical model, and complete regularization optimization is not established. [Scales](evidence/domain_response_scales.csv) · [Prefix forecast](evidence/prefix_forecast.csv)

![Domain-pair replication and three information horizons](figures/domain_response_structure.png)

Figure: left, finite-effect correlation for domain pairs sharing realized targets; right, SAE incremental Q and conditional intervals at different information horizons and scales. Columns also change target windows or fitting rules, so their differences are not causal estimates of leakage.

## 6. Inputs invisible in the current output can still affect its update

The1024×2048 final matrix has measured rank1024 and an input nullspace of dimension1024. Decompose \(c=c_R+c_N\) into row-space and nullspace components. The current output obeys \(a=Wc_R\), \(Wc_N=0\), whereas a source update produces

\[
\Delta a=-\eta Mc_R-\eta Mc_N.
\]

An input component annihilated by the current matrix need not be annihilated by the update matrix. Even the full current output, residual and actual target need not determine every update response on arbitrary inputs; fixed-event ambiguity additionally requires \(P_NM^\top e\ne0\). This is algebra for variable inputs. It does not establish matched examples on the natural data manifold or statistical unpredictability of nullspace inputs from outputs. [Derivation§11](mathematical_analysis.md)

On current R, nullspace input contributes29.49% of squared input energy; its derivative response RMS across eight source matrices is18.12%–20.55% of total response RMS. These channels are nonzero in actual cached events. The relative norm \(\|Wc_N\|_F/\|Wc\|_F\) is about \(5.4\times10^{-16}\), and row plus null responses close against old total labels. [Input geometry](evidence/input_nullspace_geometry.csv) · [Response components](evidence/input_nullspace_response.csv)

Scalar row and null responses are highly correlated, so cross terms must be retained. For centered domain responses, row-square, null-square and twice-cross fractions are65.54%,3.82%,30.64% in A and64.62%,4.01%,31.37% in B. Neither20% RMS nor4% squared response is a fraction of information lost by SAE or independently explained variance. [Within-half energy accounting](evidence/input_nullspace_centered_energy.csv); also [A/B four-term cross-source decomposition](evidence/input_nullspace_cross_moment.csv)

This distinguishes two limitations: current outputs may omit update inputs, and the earlier study showed that SAE encoding differences may poorly reconstruct actual output displacement. Neither makes SAE useless or independently identifies the cause of prediction error.

## 7. Exact texts: which relationship survives?

Keep the four previously illustrated records and targets unchanged; select no new examples. The table reports actual finite \(I_{\rm math}-I_{\rm physics}\), in millinats.

| Original record / actual target | Half A | Half B |
| --- | ---: | ---: |
| cs.CL/test/9274, ` notorious` |+0.570 |+2.647 |
| math.NT/test/5479, `1` |−1.536 |−1.517 |
| physics.optics/test/223, ` the` |+0.498 |−0.071 |
| q-bio.GN/test/39, ` distributed` |+14.580 |−2.854 |

The first two preserve relative ordering across halves; the latter two reverse. A negative contrast only says mathematics is relatively more favorable: both updates may help or both may harm. These tracked exploratory examples estimate neither prevalence nor permanent task conflict and do not name SAE atoms. [Prefixes, positions, all eight effects and identities](evidence/domain_case_followup.json)

## 8. What changes in the next research question?

The completed connection is source-matrix direction, input-dependent native movement, and signed effect through a text's realized continuation demand. Domain-relative effects partly reproduce beyond the tested common-axis amplitude. Realized continuations still induce substantial event variation, available prefix readouts capture little, and current output is not a generally complete update state.

A more precise candidate than intrinsic domain conflict is: **given a fixed prefix-information boundary and future horizon, can relative update benefits be predicted across source batches with information beyond lexical and common-axis amplitude explanations, while comparing what SAE and ordinary projections can each read?** This is an AI suggestion, not a replacement for the candidate Protocol primary test. Practical effect thresholds, independent-source/paper sampling, and whether to enter routing or separation interventions remain researcher decisions.

Persistence on new independent samples, survival of these controls, and reduced loss in an actual selection intervention would provide evidence of decision value. Strong explanation only after observing targets would support a retrospective analysis role. Weak earlier-prefix readout still requires distinguishing feature limits, estimation limits and small conditional means; it does not establish an absence of natural regularities. Net benefit from long-term separate training needs its own comparison.

Seven added local runs, including algebra checks, have code, input provenance and receipts. Old evidence and formal project records were preserved. [Run receipts](evidence/domain_response_receipts.json) · [Common-direction receipt](evidence/common_direction_receipt.json) · [Payload provenance](payload_manifest.json).
