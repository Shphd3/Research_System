# Source-batch transfer: the within-domain A/B mean and contrast

**Subsequent clarification:** all mean/contrast decompositions here compare A/B batches within the same domain. The99.02% result does not establish an absence of between-domain effects. See the [deeper analysis](domain_response_structure.md) for domain structure, strict prefix forecasting and input channels.

**Across two source samples with disjoint records, frozen SAE readouts retain about 0.48%–0.60% prediction-error improvement. An error decomposition of the two own-source predictions assigns most of their improvement to the mean response; additional information about the response difference is very small.** A transferable readout does not by itself establish a basis for deciding which data should share parameters. This remains exploration on the exposed natural-science text panel.

Continuation requested on 2026-10-02 for approximately 30 minutes. This file extends the daily candidate bundle without changing the formal question or scientific state. [中文](source_transfer_addendum_cn.md) · [Full stage report](research_report.md) · [Derivations §9](mathematical_analysis.md).

## 1. Purpose: close one specific gap

The earlier work established mean help alongside many adverse events, modest representation readout gains, and sensitivity to replacing source records. But each half-swap analysis refitted its predictor. It did not test an already fitted predictor on another source.

Simply swapping those halves would also overlap the new source with the old fitting records. We instead split old F-half0 into A/B within each category by identity hash: each contains 64 records per source domain. F-half1 supplies 512 fixed fitting records; old R supplies 1,024 fixed readout records. All four roles have disjoint record IDs and no cross-role exact full-token-sequence duplicates. Paper identity and near-duplicate independence remain unverified.

A/B come from the same four predefined domains. This replaces records within a source domain; it does not extrapolate to a new domain or source population.

## 2. Hypothesis: which part transfers?

One candidate explanation is that representations read a response component present under both sources. Another is that they additionally reveal different effects of the two sources, potentially helping distinguish which source benefits a particular event more. Both can partly hold.

Cross-source prediction gain alone cannot separate them. We therefore read the mean and difference of responses and compare representation augmentation with the lexical baseline. Limited readout gain does not establish absent information: finite samples, model restrictions and selected features remain alternatives.

## 3. Analysis method

We retain the S7 state, final attention-output matrix, pure-NTP ordinary-gradient diagnostic and earlier step size. A/B independently define their average source gradients. The original model tail evaluates actual finite loss differences in eight conditions, each containing all 16,384 R events. Predictors do not receive the true next token.

Features retain the strong lexical/history/position/scale baseline and SAE320, PCA320 or random320 augmentation. The main analysis freezes the earlier ridge choice, \(\lambda=10\). The main predictors fit first-order responses; finite predictions multiply their derivative predictions by the step size. A→B fits to A derivatives and freezes every prediction parameter when scoring B's finite responses; the baseline and augmented predictor transfer together. B→A reverses the roles. A→A and B→B provide corresponding references.

Vocabulary, PCA and the earlier regularization selection used complete F-half0, which equals A+B. This is transfer between two fixed samples under previously frozen settings. It is not a strict source holdout from all feature and hyperparameter construction. R is also historically exposed.

The main descriptive statistic averages four source-domain values of \(Q=1-\mathrm{SSE}_{\rm aug}/\mathrm{SSE}_{\rm base}\) equally. Intervals use 2,000 paired, category-stratified R-record bootstrap draws, fixing sources, features and fitted predictors. They exclude source-sampling and paper-cluster uncertainty. A 0.48% gain concerns prediction error, not LM loss.

After observing weak contrast readout at fixed regularization, a separately registered exploratory sensitivity selects regularization specifically for the response difference, using four record folds within F and a grid from \(10^{-4}\) to 100. R does not select parameters. All four models select 100, the grid's upper boundary. This neither creates new confirmation nor establishes optimization over the entire regularization range.

## 4. Conclusion

### 4.1 Frozen prediction retains a small incremental gain

All entries below score actual finite loss labels without refitting the main predictors to those labels.

| Fitted source → evaluated source | SAE Q | Conditional 95% interval | random320 Q |
| --- | ---: | ---: | ---: |
| A → A | 0.622% | [0.519%,0.719%] | 1.092% |
| A → B | 0.481% | [0.383%,0.574%] | 0.804% |
| B → A | 0.602% | [0.502%,0.695%] | 1.000% |
| B → B | 0.535% | [0.440%,0.631%] | 0.854% |

Ordinary projections also help. The result is not an SAE-specific advantage. A→B need not perform worse than B→B because their fitted predictors have different estimation errors; this table does not rank the sources.

![Finite response transfer and contrast readout](figures/source_transfer.png)

The left panel shows the four transfer cells; the right shows response-difference readout on a different vertical scale. All intervals condition on sources and fits. The [complete finite table](evidence/source_transfer_finite_readout.csv) includes PCA, raw MSE, pooled scoring and each source domain.

### 4.2 About 99% of the current gain concerns the mean; contrast gain is small, not established as zero

Let \(I_A,I_B\) denote finite responses and \(P_A,P_B\) their predictions. Average own-source MSE equals prediction MSE for the mean response plus one quarter of prediction MSE for their difference. This exact accounting requires no independence assumption. [Derivations §9](mathematical_analysis.md)

For the fixed-\(\lambda=10\) SAE predictor, pooled absolute MSE improvement across the two own-source predictions is \(2.106\times10^{-7}\) nat squared. **99.02% belongs to the mean component**, and about 0.98% to the difference component. This describes prediction errors for two sources and one learner; it is not 99% explanation of a semantic or causal mechanism. [Gain accounting](evidence/source_transfer_gain_accounting.csv)

For \(I_B-I_A\) alone, fixed-regularization SAE Q is **0.0261%**, with conditional interval **[−0.0124%,0.0625%]**. Contrast-specific tuning yields about **0.0092%**, interval **[0.0046%,0.0136%]**. This is a very small conditional positive reading, also found with ordinary projections. It does not justify saying that contrasts carry no information, nor that this scale suffices for a data-separation decision.

The mean derivative and fixed-regularization prediction exactly recover the earlier full-F-half0 quantities because A/B partition it equally and ridge is linear in labels. That recovery is not independent evidence. The average of two finite effects also generally differs from the finite effect of their average matrix; we keep those objects separate.

### 4.3 Individual sign sensitivity coexists with modest prediction gain

A/B finite-response correlations on R are 0.423/0.742/0.362/0.253 for computer science/mathematics/physics/biology. Among events resolved beyond \(10^{-5}\) nat in both conditions, sign agreement is 54.66%–69.79%. Each source now contains 64 records per domain, compared with 128 earlier, and the split also differs. Their difference cannot be attributed solely to sample size.

Prediction MSE, response correlation and sign agreement answer different questions. [Finite-effect table](evidence/source_transfer_finite_effects.csv)

### 4.4 Keep readout existence distinct from source discrimination

**AI suggestion:** if the aim is to inform sharing/separation, independent confirmation should observe both the mean response and source differences. Positive fixed-source Q alone does not bridge that gap. The researcher still needs to choose independent units, a useful effect scale and the most consequential source comparison.

The existing candidate Protocol retains its fixed-source new-record question and `DRAFT_NOT_EXECUTABLE` state. This continuation neither expands its primary test automatically nor modifies the formal Focus. Long-term net benefit from separate parameters remains unanswered.

## 5. Verification and execution boundaries

The first finite attempt exited with SIGSEGV during baseline-tail evaluation, before producing any condition. Its script, registration and log are retained; root cause is Unknown. Removing the newly introduced interop setting and Python signal timer, then retrying the same inputs with an external time limit, completed in 186.3 seconds. Baseline entries match old R exactly; model-state and input hashes are unchanged. Relative absolute first-order error is 0.253%–0.617%. Successful retry does not establish which configuration difference caused the crash.

Numerical error in the new MSE identities is below \(4\times10^{-18}\). Raw arrays, scripts, failed logs and registrations remain in the [execution workspace](/data/250010109/MoE_Router/experiments/20261002_s7_representation_update_channels/README.md). [Continuation receipts](evidence/source_transfer_receipts.json) and the [payload manifest](payload_manifest.json) preserve provenance. No new LM/SAE training or remote job was launched. Markdown and equations receive source checks; the figure was visually inspected. Scientific confirmation remains Unknown.
