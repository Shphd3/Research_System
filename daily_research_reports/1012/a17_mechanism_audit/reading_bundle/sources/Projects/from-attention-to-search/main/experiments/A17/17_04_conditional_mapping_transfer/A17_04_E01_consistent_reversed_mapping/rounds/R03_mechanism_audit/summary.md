# Summary: A17_04_E01 R03 finite mechanism audit of reversed transfer

[中文](summary_cn.md) · [Protocol](protocol.md) · [Detailed](detailed.md) · [Manifest](artifact_manifest.json) · [Independent audit](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/independent_audit/finite_outputs_audit.json)

## 1. Purpose

The parent question asks when different prediction requirements benefit from shared learning and when processing should depend on the input condition. This round asks which actual final-attention matrix changes participate in R02's reversal of both modes, and whether simply reducing the existing displacement can preserve both mappings.

## 2. Model

The acquired Qwen3-0.6B maps command Jia/Yi to the first/last list item in old mode1. Reversed mode2 swaps those two answers. The mode is visible, so both mappings can be satisfied. R03 reads R02's three continuation orders and saved steps240/1200; it performs zero training updates. Only the four last-layer Q/K/V/O matrices differ across the source states.

Q/K/V produce the contextual reading vector c; O maps it to the raw attention output. Each counterfactual restores the complete specified state before replacing one matrix with its old value, or inserting one reversed matrix into the old state. Accuracy uses the full-vocabulary argmax. CE is negative correct-answer log probability. Endpoint margin is the correct endpoint logit minus the other endpoint logit, in natural-log units.

Let j index the command and \(s_{m,j}\) be last-minus-first endpoint logit and \(a_m=(s_{m,Yi}-s_{m,Jia})/2\). Positive values denote the original mapping; negative values denote reversal. With equal command weights the old correct margin equals \(a_1\), and the reversed-new correct margin equals \(-a_2\). These identities do not supply independent evidence.

## 3. Hypothesis

The candidate mechanism is that new-only reversed learning changes reading and output computations used by both modes without confining their effects to the new mode. Single-matrix counterfactuals test actual prediction effects; the four O-by-QKV states test whether O's finite effect depends on the current reading computation.

The strongest remaining explanation concerns training objectives and initial difficulty. Reversed-new accuracy starts at0%, whereas consistent-new starts at99.875%; new-only training provides no old labels, while joint training adds old labels and halves new exposure. The present intervention can locate finite effects of existing changes, but cannot identify why optimization chose that trajectory. Five fixed interpolation points additionally test a limited displacement-scale repair, not smaller-learning-rate retraining.

## 4. Conclusion

1. **The damage involves coupled matrix changes rather than an isolated reversal matrix.** At step1200, complete reversed weights give old/new accuracy0%/99.25%. Rolling back only Q gives48.54%/57.04%; rolling back only O gives32.67%/68.71%. All24 rollback comparisons (three orders×two states×four matrices) increase old accuracy and decrease new accuracy. Inserting only reversed O into the old model gives98.71%/1.29%. These actual finite counterfactuals establish participation conditional on the other weights, not a unique, generally necessary or separable task module. Two-/three-matrix combinations were not exhausted, so all four matrices cannot be called necessary. [All matrices, states and panels](detailed.md#51-actual-one-matrix-counterfactuals).

2. **O's predictive effect depends on its reading input; matrix effects are not simply additive.** On the preregistered80-record DEV panel, old correct margins for old-O/old-QKV, new-O/old-QKV, old-O/new-QKV and new-O/new-QKV are+15.8824,+12.4139,−3.1091 and−14.9432. The four-state interaction is−8.3657 for the old correct margin and+8.3695 for the reversed-new correct margin. This is a signed prediction interaction from one order and endpoint, not unique mediation or discovery of a shared subspace. [Representation bridge](detailed.md#53-representation-to-prediction-bridge).

3. **None of the tested scalar reductions preserves both tasks.** Across three orders, two endpoints and five alpha values,0/30 sampled states meet≥80% accuracy in all eight task-by-command-by-panel cells. The best weakest-cell accuracy is13.5%. This weakens the simple scale-repair explanation at these sampled points; it excludes neither unsampled alpha values nor other paths or actual smaller-LR training. [Complete interpolation tables](detailed.md#52-five-point-interpolation).

## 5. Analysis

R02 already showed that the same shared parameter budget can satisfy both mappings under joint supervision. Opposing answers therefore do not imply that parameter separation is required. R03 adds actual parameter participation and a conditional computation bridge: reading/output edits alter both task predictions, and O's effect depends on the current reading vector. The explanation is more specific, while the reason new-only optimization did not confine the change remains unresolved.

Displacement norms describe how far weights moved. Representation norms describe how much internal vectors changed. Neither directly establishes functional harm. Actual counterfactual CE, full-vocabulary accuracy and signed endpoint margins supply that link. Every Q/K/V/O rollback and insertion, both saved states and both DEV panels remain in the [300-row native table](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1/full_parameter_rollback.csv), with separate-panel and equal-weight combined results.

For the four actual O-by-QKV states, let \(c_0\) be the old reading vector and \(\Delta c\), \(\Delta W\) their changes. The exact linear relation is

\[
\Delta h_{\mathrm{attn}}=\Delta Wc_0+W_0\Delta c+\Delta W\Delta c.
\]

Its relative numerical residual is \(5.3885\times10^{-7}\). The frozen output-head bridge from final normalized hidden states to endpoint logits has maximum error \(8.1065\times10^{-5}\) nat. Verifying these identities is implementation evidence; the new functional evidence is the signed four-state prediction interaction. Averaging raw last-minus-first effects across opposite commands nearly cancels the effect: raw interaction mean−0.3194 versus old-rule signed interaction−8.3657. [Independent signed table](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/independent_audit/representation_signed_response.csv).

CPU audits cover9600 source records,72 states and72 cached readouts. Same-profile Smoke and Full pass. Full saved88 native readouts/140800 record appearances,300 condition-panel rows and30 interpolation decisions. Independent auditing isVALID with0 errors; original-state replay errors are0, saved no-op/restoration records are exactly equal and frozen bytes remain unchanged. [Actual output registration](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1/full_registration_receipt.json) covers native analysis and four-state representations; no new training checkpoint was created. Repeated record appearances and the80-record representation panel are not independent model replications. All three orders share one old trained state; all evidence is exposed-DEV diagnosis with no TEST or fresh confirmation.

Researcher mechanism acceptance, closure and the next decision remainUnknown. AI suggestion: test which learning constraint confines the reversed change to the new mode while holding new learning and exposure accountable. This round does not compare budget-matched shared and independent parameters.
