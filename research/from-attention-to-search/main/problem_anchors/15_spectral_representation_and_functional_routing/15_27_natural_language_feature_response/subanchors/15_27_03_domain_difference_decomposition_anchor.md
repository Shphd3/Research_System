# A15_27_03: CrossCoder decomposition of a fixed-target domain mean difference

## 1. Problem Definition

Can the average mathematical-versus-biological representation difference at a fixed final target token be described by reproducible changes in native CrossCoder member use, and which reference-frequency groups and spectral ranges contribute? The parent line asks whether a fixed target responds to its context. R07 found a reproducible mean association; R08 separated center differences from within-domain variation. Neither result identifies the dictionary members composing that difference.

This subanchor explains one frozen representation difference. It preserves both fixed endings separately, all 384 texts, 48 families and the original 24/12/12 family split. The researcher additionally requests domain-versus-family and short-versus-long-context descriptions. Here “individual” means a topic or text family within a domain, not a person, word type or neuron. A concentration result would support a compact description of this difference; distributed or residual-dominated results would restrict that description; unstable estimates would leave the question unresolved. No training, routing or functional intervention belongs to this question.

## 2. Physical Priors

Three assumptions delimit the analysis. First, the frozen A22 decoder is a linear map from one jointly encoded activation vector to each layer's reconstructed representation, in a verified training-normalization scale. Second, related wordings and endings within a family are dependent; the family is the resampling unit. Third, reference occurrence rate, domain-associated activation differences and distance response are different measurements. None defines semantic exclusivity.

## 3. Falsifiable Hypotheses

The researcher supplied four live explanations: A, a small set consistently carries much of the difference; B, many members contribute with reinforcement or cancellation; C, apparent candidates depend on an ending or wording; D, important difference remains in reconstruction residuals. Fixed discovery rankings evaluated on original heldout families distinguish concentration from discovery-only selection. Separate endings, wordings and ending contrasts examine C. Whole-vector residuals examine D even when directional alignment is high. Family variance and controlled distance responses characterize these same objects; neither may rescue poor reconstruction.

## 4. Mathematical Model

An observation is a text's final target representation, \(h\in\mathbb R^{1024}\), and its native shared activation, \(z\in\mathbb R^{16384}\). For one ending, let \(\delta=\mu_{\mathrm{math}}-\mu_{\mathrm{bio}}\), with equal family and wording weights. Let \(d_j\) be member \(j\)'s block27 decoder vector and \(s\) its training-normalization restoration scale. The decomposition is

\[
c_j=s\,d_j\,\Delta z_j,\qquad
\widehat\delta=\sum_j c_j,\qquad
r=\delta-\widehat\delta.
\]

Fixed centering and decoder bias cancel between the two means. A contribution is a vector, not a member error. Sum vectors before computing any length or spectral energy. The signed amount along the true difference is

\[
a_j=\frac{c_j^\top\delta}{\|\delta\|^2},\qquad
a_r=\frac{r^\top\delta}{\|\delta\|^2},\qquad
\sum_j a_j+a_r=1.
\]

Negative values oppose the true difference; totals may exceed one. Whole-vector relative residual \(\|r\|/\|\delta\|\), cosine and original lengths remain necessary because directional shares do not measure perpendicular reconstruction error. Near-zero denominators yield raw values and an explicit undefined ratio.

To describe activation variation rather than reconstruction, each member also has a separate nested variance decomposition at fixed ending: between-domain \(B=\Delta z^2/4\), within-domain between-family \(F=E_{d,f}(\mu_{df}-\mu_d)^2\), and within-family wording \(W=E(z-\mu_{df})^2\). Balanced sampling gives \(T=B+F+W\). These quantities cannot be substituted for the signed vector contributions above.

## 5. Computational Realization

Use frozen Qwen3-0.6B Base block27 residual-post, before final normalization, and A22's native fourteen odd-block joint input, original normalization and gate. Reuse R08's actual vectors and shared activations. Validate the dictionary identity and scale against its training source and saved tensors. This makes the sum a decomposition of the same measured interface.

Analyze all 16,384 members before selecting any candidates. For each ending, rank positive discovery contributions and freeze the top32 list and union; evaluate fixed nested subsets on original heldout families. A separate discovery-fixed list of up to64 candidates per preferred domain answers the researcher's request for more members; its exact rule is owned by the Protocol and cannot replace the all-member analysis. Preference follows the sign of activation difference, not the sign of contribution.

Frequency is measured on the independent DCLM reference with the matched native gate. Main groups divide log occurrence into three equal widths; original equal-count and linear equal-width groups are sensitivity views. Reference support below20/65536 and missing values remain explicit. Use R07's independent natural-text PCA, not R08's refitted mixed basis. The distance extension changes separation between context and target with matched controls; actual token positions, filler and control changes are recorded. It is a context-response measurement, not an Attention measurement.

## 6. Minimal Falsification Tests

First verify the representation interface, decoder-scale reconstruction, \(\delta=\widehat\delta+r\), and signed-sum identity. Failed identity or asset checks invalidate their dependent results. At fixed candidate counts1/4/8/16/32, compare original-heldout vector error with all-member reconstruction and equal-size random subsets. Retain every count and both endings; do not choose the most favorable one. Cross-wording or cross-ending changes restrict candidates to their observed conditions. Large residuals leave explanation D active even when selected members look coherent.

Frequency-group totals use all members and show group size, active count, positive sum, negative sum and net contribution. Family-level intervals accompany continuous summaries. No data-selected cutoff declares a member domain-exclusive, a space semantic, or a distance intrinsically long. Missing support, unidentifiable controls and near-zero denominators remain insufficient evidence. Exact operational settings are fixed before the corresponding readout in the [Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/protocol.md).

## 7. Current Evidence

R07's paired mean association generalizes within its constructed panel, while its fixed zero-threshold classifier scored60.42%; direction, threshold and fitted readability are different. [R07 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R07_fixed_target_domain_spectrum_20261029/summary.md).

R08's block27 mixed top16 space covers99.89% of the discovery mean-difference squared length, while between-domain variance is9.08% of retained total variance. Fixed endings increase that share to36.28% and19.93%. These values motivate ending-conditioned decomposition; they do not identify particular CrossCoder members. [R08 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R08_within_mixed_subspaces_20261029/summary.md).

R09 cached decomposition is complete with zero new forwards and zero parameter updates. In each ending, original heldout contains12 families and48 rows. For example/explanation, true mean-difference lengths are103.515/52.972, reconstruction lengths89.285/38.538, and residual lengths55.565/38.215. Relative residuals are0.536779 [0.521219,0.579592] and0.721408 [0.684047,0.765007], with cosines0.843928/0.693352. Intervals are pointwise95% paired-family bootstrap summaries. Whole-dictionary signed contributions along the true difference are0.727910/0.504418; directional residual shares are0.272090/0.495582. These directional shares do not replace whole-vector error.

Discovery-fixed Top32 heldout relative errors are0.719568/0.828926, versus0.536779/0.721408 for all members. The expanded discovery lists contain64 math-preferring and64 biology-preferring candidates. Sixteen math and20 biology candidates retain activation-difference signs in all four original-heldout wording/ending cells and exclude zero in both ending-specific activation-difference intervals. Call these **recurring use-preference candidates**, not stable contribution or semantic members: signed vector contribution also depends on the decoder and true-difference direction. This pointwise exploratory tag does not establish exclusivity.

Across all members in the main log-frequency groups, heldout low/middle/high net directional shares are0.003137/0.448360/0.276413 for example, and0.001675/0.245089/0.257676 for explanation. The insufficient-support/unknown category contributes−0.0000216 in explanation and remains explicit. Group size, cancellation and whole residual must accompany these shares. Main results are retained in the [completion receipt](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/main_completed.json) and [complete numerical tables](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables); distance extraction completed3,842/3,842forwards with unchanged parameters and exact native replays. At distance144, E exceeds the date-control reference after BH for83/72candidate-ending cases; requiring both wordings to preserve the original domain direction leaves37/26 and14in both endings. Of the original36use-preference candidates,7pass both far-ending checks;3also retain direction at both new near endings. Only9of36retain both new-near directions, so loss under the changed240-token framing cannot all be assigned to distance. Low-frequency support is insufficient for a group-wide range claim. [Complete R09 evidence](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/detailed.md). Researcher acceptance and closure remain Unknown.

## 8. Claim Boundary And Next Decision

The result may describe how this fixed dictionary reconstructs this panel's average domain difference, how that contribution varies across families/endings, and how measured context response changes with tested distances. It cannot establish domain-exclusive knowledge, causal importance, expert-separation benefit or global knowledge rank. Original heldout data are exposed exploratory reuse. The next decision is for the researcher to judge whether a reproducible member description, a distributed description or a residual/condition limitation best answers the question after the complete report. Deliver the registered comparisons and stop; no automatic expansion.
