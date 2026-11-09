# Summary: Domain activation structure and local update structure

[Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_12_domain_update_geometry/17_12_domain_update_geometry_anchor.md) · [Frozen Protocol](protocol.md) · [Detailed evidence](detailed.md) · [中文](summary_cn.md)

**Final text R2, revised after the reasoning-auditor review.** Domain-mean activation profiles replicate across this panel's splits, while the current domain-mean gradient descriptor has no held-out gain. Selected common SAE output spans capture more gradient energy in the specified comparison; this does not explain most pairwise compatibility. Editorial finalization does not close the scientific question. Human judgment remains `Unknown`. [Revision audit](evidence/reasoning_audit_final.json)

## 1. Purpose

At a fixed model state, examine reproducible structure in natural domain-text update demands and its relationship with native representations and the existing SAE, to inform subsequent research on parameter sharing.

## 2. Hypothesis

The primary test asks whether empirical fit-domain mean gradients describe readout gradients more accurately than the pooled mean. It tests one mean descriptor, not all domain structure. **The strongest live rival** is that domain association exists but event variation and finite-sample high-dimensional mean error mask prototype gains; another possibility is genuinely weak population mean differences. These alternatives remain unresolved.

Activation replication, gradient spectral transfer and SAE span capture are separate questions; none substitutes for the others.

## 3. Analysis Method

- Freeze **S7, historical λ_rec=.1, exact33B training-token checkpoint**, with281,431,040 backbone parameters;33B is not a parameter count. Measure final-attention-output pure next-token gradients and the30,000-atom SAE on1,024 historical records: four domains, eight subfields,512 fit and512 readout.
- Primary \(Q_D\) is readout gradient-MSE improvement of domain over pooled prototypes. Distinguish input \(c\), native output \(a=Wc\), output loss derivative \(e\), and gradient \(G=ec^\top\). Single-target gradients are primary; the actual mean of16 gradients diagnoses scale. SVD transfers each space's own fit directions.
- Measure every atom across261,120 input positions: frequency, amplitude, position, persistence and coactivation. Fit activation alone selects common/enriched sets. Readout evaluates replication and decoder-output-span gradient coverage against matched-rank native-a PCA and three random spaces.

## 4. Conclusion

| Question | Observation | Supported reading |
| --- | --- | --- |
| Does this mean descriptor help? | \(Q_D=-0.005715\): MSE increases0.5715%; mean16 Q=−0.005060 | No gain for this split and estimator, not absence of domain–update association. [Primary](evidence/primary.json) |
| Do domain activation profiles replicate? | Four domain-mean30,000-dimensional frequency vectors: same-domain cross-split cosine0.972–0.991 versus cross-domain0.611–0.894;65/99 common atoms meet the same readout rule | Descriptive replication of domain averages, not individual-record classification or semantic causality. [Profiles](evidence/activation_pattern_distances.csv), [atoms](evidence/review.json) |
| Do fitted gradient directions transfer? | Centered last-target top64 retains39.17% fit versus3.18% readout energy; mean16 readout4.83% | Limited capture by these estimated directions, not proof of no population low-dimensional structure. [Spectrum](evidence/spectral_reading_rows.csv) |
| What do selected SAE spans capture? | Rank64 common captures8.96% pooled-readout last-target gradient energy; random6.21–6.31%; four enriched sets5.12–5.41%; native-a PCA6.74% | Higher common-set capture in this comparison; own-domain selective usefulness and mediation of interference were not tested by pooled trace. [Projection](evidence/projection_results.csv) |

### Primary evidence eligibility

The registered program's `NON_SUPPORT` field is preserved. **Negative finite-panel \(Q_D\) is verifiable; population directional inference remains insufficient.** The registered percentile interval[−0.014058,−0.009694] is materially displaced: refitting domain means adds approximately0.63964 more expected squared error than refitting the pooled mean, explaining the bootstrap-center shift. This is not a measurement-noise correction or calibrated95% population coverage. [Estimator audit](evidence/review.json)

Permutation p=.022 means the observed statistic exceeds most generated shuffled-label statistics. Combined with negative \(Q_D\), it neither establishes useful domain prototypes nor supplies general significance without label exchangeability and resolved source/record dependence. [Registered comparison](evidence/primary.json)

### Commonality and differences

![Readout records on each space's own fit axes](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/common_fit_coordinates.png)

Each panel has its own fit directions and energy denominator: two axes capture about0.1% of gradient,17.5% of native-output and20.8% of SAE-frequency readout energy. Visible activation separation is informative, but different spaces/denominators do not establish a matched-budget algorithm comparison; gradient mixing in two dimensions cannot exclude full structure. [Spectrum values](evidence/spectral_reading_rows.csv), [figure origins](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/origins.json)

Fit last-target energy is0.19% pooled mean,0.58% domain deviations and99.23% within-domain residual. A small mean does not imply absent shared directions: opposing gradients cancel in a mean. Common firing and a common mean update are different objects. [Decomposition](evidence/energy_decomposition.json)

SAE capture measures diagonal squared-gradient energy of \(K\), not signed off-diagonal compatibility. Common rank64 still leaves off-diagonal relative squared K-reconstruction error.803. A64-direction full-gradient SVD also differs from output-rank64 \(PG\), whose vectorized projection retains64×2048 directions. Comparing3.18% to8.96% does not show SAE outperforming a matched-budget gradient SVD. [Detailed explanation](detailed.md)

The e Gram aligns.903 with K; identical-target mean gradient cosine is.193 versus.00046 for different targets. These motivate investigation, but K is constructed from c/e and e jointly depends on predictions, true targets and downstream derivatives. No isolated target-causality mechanism has been established. [Alignment](evidence/kernel_alignment.csv), [target strata](evidence/review.json)

### Next step analysis

**AI-proposed next question:** how much domain-associated K structure co-varies with target composition and aggregation scale, and how much replicates under comparable target conditions? Targets belong to the learning task. Total domain association and additional association conditional on targets answer different questions; retain both rather than automatically deleting the former as confounding. Mean16 gradients averaged over64 records align.104 for true domains versus.074 for mixed groups, a descriptive clue only. [Scale](evidence/scale.json)

If this question is adopted: calibrated, independent-record conditional gains would support the bounded relation; qualified precise estimates below a prespecified effect would weaken it; sparse target overlap, uncalibrated intervals or unstable estimation would be insufficient. Failure of a conditional relation would not deny total domain association. The precise contrast and effect threshold are not a new approved design.

All registered statistics are delivered, not every higher-order activation combination or causal function. Historical exposure, unknown paper IDs, imperfect source semantics and one state/matrix bound the claims. This round did not retest representation-only K prediction or measure finite-step/long-term sharing benefits. Earlier verdicts and frozen Anchor/Protocol remain unchanged.
