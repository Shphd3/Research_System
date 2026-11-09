# Epoch-one experts: training evidence, principal components and parameter spectra

The audit covers20 epoch-one models and160 experts. **130 pass the exposure floor;49 also pass this analysis's heldout-benefit rule. Neither label guarantees convergence. Beneficial experts have different output principal subspaces, but the spectra do not support a general improvement in isotropy after training.** This is exploratory analysis of previously inspected EVAL. It preserves the original negative epoch-three endpoint and does not close the research question.

## Purpose, model and competing explanations

We distinguish actual supervision, natural-region loss benefit and geometric differences. Updating weights or obtaining a broad spectrum alone does not establish successful learning. Eligibility was fixed before spectra; all130 exposure-qualified experts, including negative learning results, were decomposed. The49 benefit experts are reported separately.

Qwen3-0.6B Base, the14-layer/F16384 CrossCoder and original final RMSNorm/vocabulary head remain frozen. Eight bias-free SwiGLU residual experts sit after the complete28th block and before final RMSNorm. Each gate/up/down matrix is1024×1024; the internal gate matrix differs from the router multiplier. Experts receive the full final hidden vector. CrossCoder features determine fixed dispatch only. Epoch one contains168 optimizer updates and85,548 answer/EOS target exposures per model; TRAIN has1,024 dialogues and EVAL256.

The analysis expectation is that sufficiently exposed experts with heldout benefit can have different principal response subspaces on identical inputs. Random initialization, shared input structure and unequal exposure are credible competing explanations for geometric differences. Initialization and full-weight/increment comparisons constrain these explanations but do not identify semantic specialization or effective capacity.

## Which experts have learning evidence?

The exposure floor requires at least2,048 actual unique TRAIN prediction positions,20 distinct dialogues,20 expert update steps and nonzero down-weight change. Fixed dispatch is reconstructed exactly. Learned routers lack per-position training histories, so dialogue diversity uses a conservative capacity lower bound rather than endpoint routes. This diagnostic floor is not a maturity theorem.

130 experts pass;26 receive zero TRAIN positions and4 fail another exposure/diversity requirement. The additional benefit rule requires at least200 natural EVAL positions across20 dialogues, negative endpoint natural-region TRAIN loss change, and negative EVAL change with a1,000-dialogue-bootstrap descriptive95% interval entirely below zero.49 pass. The other81 exposed experts have no established benefit under this complete rule; that does not imply they are all harmful.

|Condition|seed|Exposure-qualified|Benefit IDs|Zero-exposure IDs|
|---|---|---|---|---|
|T_S0|11|1|7|0,1,2,3,4,5,6|
|T_S0|22|1|7|0,1,2,3,4,5,6|
|T_S1|11|8|0,1,3|none|
|T_S1|22|8|1,3|none|
|T_S2|11|1|7|0,1,2,3,4,5|
|T_S2|22|1|7|0,1,2,3,4,5|
|T_S3|11|8|1,3|none|
|T_S3|22|8|1,3|none|
|R11_S0|11|8|0,4,6|none|
|R11_S0|22|8|0,4,6|none|
|R11_S1|11|8|0,4,6|none|
|R11_S1|22|8|4,6|none|
|R11_S2|11|8|0,1,4|none|
|R11_S2|22|8|0,1,4,6|none|
|R11_S3|11|8|4|none|
|R11_S3|22|8|0|none|
|Learned|11|8|1,3|none|
|Learned|22|6|2,4,6|none|
|LearnedLB|11|8|0,1,3,7|none|
|LearnedLB|22|8|1,2,3,4,5,6,7|none|

IDs are zero-based within each model, not functional identities across conditions. T_S1 experts1 and3 pass in both seeds; expert0 additionally passes in seed11. T_S2 expert6 receives too few positions in both seeds. Learned seed22 expert3 has3,209 positions but only13 guaranteed dialogues; excluding it conservatively does not mean its actual diversity is13. See [all counts, intervals and labels](tables/expert_training_evidence.csv).

## Principal-subspace similarity

Every qualified expert receives the same1,024 EVAL prediction positions, four per dialogue. PCA uses column-centered residual corrections, excluding both the shared Base hidden vector and the router multiplier. Overlap is the squared Frobenius norm of the cross-product between two orthonormal rank16 bases, divided by16; zero means orthogonal and one identical subspaces.

|Condition|seed|Benefit pairs|Benefit PCA median|All-qualified PCA median|
|---|---|---|---|---|
|T_S1|11|3|0.07737|0.07213|
|T_S1|22|1|0.06865|0.06898|
|R11_S1|11|3|0.08240|0.07599|
|R11_S1|22|1|0.09725|0.07690|

![Beneficial experts: output PCA overlap](figures/figure10_benefit_subset_PCA.png)

Off-diagonal cells compare experts; gray means excluded/undefined, not zero. Beneficial T_S1 pairs have median overlap0.07737/0.06865. These directions differ substantially but retain more overlap than the independent random-subspace geometric reference16/1024=0.015625. This reference is not a significance test. R11_S1 has a similar scale, so geometric differentiation is not unique to frequency grouping. Only3 or1 benefit pairs contribute per model and pairs share experts.

Parameter and response directions differ. For all eight T_S1 seed11 experts, median gate-input overlap changes from0.01557 initially to0.03646 at epoch one, while its increment overlap is0.16253. Up changes0.01608→0.02066, with increment0.14811. Down output directions overlap0.14838, whereas nonlinear response PCA overlaps0.07213. Shared update directions coexist with different responses. [Pair data](tables/within_model_similarity.csv) and [summaries](tables/similarity_summary.csv) retain all conditions.

## Does anisotropy improve?

SVD supplies each matrix's singular directions and strengths. Define q as each squared singular value divided by the total over all1,024 values. Larger q1 or top16 energy means greater concentration. Effective rank is the exponential entropy of q; larger values indicate more dispersed energy. These are geometric descriptors, not task-quality measures.

![Beneficial49 experts: first16 normalized spectral energies](figures/figure11_benefit_subset_top16_energy.png)

Left panels show full epoch-one weights and right panels increments from initialization. Every rank uses the full1,024-value denominator. Experts are averaged within each seed, followed by equal seed weighting; legend counts give seed11/22 support. Down starts at zero, so its full weight equals its increment and both columns correctly coincide. Its initial normalized spectrum is undefined.

**Gate/up do not flatten.** Across all130 qualified experts, top16 energy increases and effective rank decreases for both matrices; median rank changes are−1.176/−0.762. This also holds for the49 benefit subset. Full-weight effective ranks remain near620 and retain strong initial structure: median relative Frobenius changes are0.120/0.114 and overlap with each expert's own initial top16 directions is about0.875. In T_S1 seed11, gate full/increment effective-rank medians are619.64/129.78; up medians are619.84/185.74. Broad full-weight spectra do not imply broad learned increments. See [paired changes](tables/paired_initial_changes.csv) and [spectral metrics](tables/parameter_spectral_metrics.csv).

**Down has no normalized before/after baseline.** Its initial matrix is zero. The following table describes post-training means across all exposure-qualified experts within each seed; it is not an average over the benefit subset. The [benefit-only table](tables/benefit_subset_matrix_summary.csv) reports that subset separately.

|Condition|seed|Experts|Mean q1|Mean top16 energy|Mean effective rank|
|---|---|---|---|---|---|
|T_S0|11|1|0.03335|0.17115|422.54|
|T_S0|22|1|0.03417|0.17173|421.61|
|T_S1|11|8|0.03193|0.20485|344.85|
|T_S1|22|8|0.03170|0.20518|345.00|
|R11_S1|11|8|0.03290|0.19497|353.96|
|R11_S1|22|8|0.03253|0.19508|354.37|
|Learned|11|8|0.06274|0.26284|274.89|
|Learned|22|6|0.06409|0.26257|276.63|
|LearnedLB|11|8|0.07023|0.26385|277.89|
|LearnedLB|22|8|0.06953|0.26562|275.85|

T_S1 has slightly lower q1 than T_S0, but higher top16 energy and lower effective rank. The metrics do not jointly support improved isotropy. T_S0 trains only one expert adequately and has different exposure; this comparison cannot causally rank routing strategies.

Within T_S1 seed11, loss change is in nats per answer position and negative is beneficial:

|expert|TRAIN positions|EVAL ΔNLL|Benefit rule|down top16 energy|down effective rank|
|---|---|---|---|---|---|
|0|17492|-0.009229|yes|0.1869|374.2|
|1|14460|-0.057513|yes|0.2153|347.5|
|2|9767|+0.002459|no|0.1838|357.3|
|3|6704|-0.041455|yes|0.1877|355.9|
|4|8402|+0.007388|no|0.1569|407.0|
|5|8295|-0.008451|no|0.2143|324.2|
|6|11882|+0.004443|no|0.2831|255.5|
|7|8546|+0.013086|no|0.2107|337.2|

Expert4 has a more dispersed down spectrum than expert1, with effective rank407.0 versus347.5, but its EVAL change is+0.00739 and it fails the benefit rule; expert1 changes−0.05751 and passes. Expert5's negative point estimate has an interval crossing zero and therefore does not pass. These eight dependent observations do not establish a universal inverse relation; they do refute using flatness as this analysis's success certificate.

![T_S1 seed11 individual spectra](figures/figure7_seed11_individual_expert_spectra.png)

Stars mark benefit-qualified experts. Full1,024-value normalized spectra and absolute top16 singular values are separated. [Seed22](figures/figure7_seed22_individual_expert_spectra.png), [all-qualified full spectra](figures/figure5_full_normalized_energy_spectra.png) and [curve data](tables/spectral_curve_source.csv.gz) preserve the negative cases.

## Boundaries and next uncertainty

Epoch one was selected post hoc and EVAL was previously inspected. The49 labels and bootstrap intervals are descriptive, with no independent-confirmation or multiple-comparison error guarantee. Claims cover this Tulu subset, frozen-Base final residual branch and answer NLL, not free generation, broad capability, long-term capacity or feature semantics. The original epoch-three deterioration remains unchanged.

Full-EVAL source summaries reuse original GPU natural-route NLL. For T_S1 seed11, token-weighted changes are−0.10702 on CoT,−0.04518 on CodeAlpaca,−0.07985 on FLAN and+0.00754 on ShareGPT. Sources denote dataset origins, not pure semantic domains. An auxiliary cached-output CPU expert-replacement check fails the predeclared0.01 natural-NLL agreement threshold in13/20 models, with maximum error0.12491. It is BOUNDED and cannot adjudicate small differences or specialization. The primary130 geometry analyses and49 benefit labels use original GPU evidence and are unaffected. See [source results](tables/epoch1_source_learning.csv) and [numerical checks](evidence/probe_loss_checks.json).

Researcher mechanism judgment and next decision remain Unknown. **AI suggestion:** test whether different directions correspond to useful content specialization using same-input expert replacement on one uniform GPU arithmetic path, first qualifying natural-route replay. This new experiment was not started.

[Detailed](detailed.md) · [Frozen Protocol](protocol.md) · [Manifest](artifact_manifest.json)
