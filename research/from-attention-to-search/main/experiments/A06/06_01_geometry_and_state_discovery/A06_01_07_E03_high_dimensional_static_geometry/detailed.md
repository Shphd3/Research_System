# Detailed: A06_01_07_E03_high_dimensional_static_geometry

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
Protocol: `protocol.md`
Summary: `summary.md`

## 0. Quick Recap

Purpose:
Test whether centered/calibrated M4 can generalize the 2D uniform-load result to high-dimensional uniform features.

Hypothesis:
Centered M4 should improve load over raw M4; high-dimensional balance should depend on spectral spread; calibration should enforce load only if margin survives.

Experiment logic:
Sample \(x\sim\mathrm{Unif}(S^{d-1})\), compute raw/centered/calibrated M4 score differences from the eigen-spectrum of the score-difference matrix, and compare load, margin, degeneracy, and spectral-spread diagnostics across dimensions and expert conditions.

Conclusion:
Centered M4 is supported as the right high-dimensional static target, but not as an unconditional exact 50/50 rule. Calibration is needed for robust load control, and low-rank proxies require enough rank to preserve full centered-M4 decisions.

Evidence:
At \(d=512\), raw M4 load error is 0.4644 in the Gaussian-like random spectrum proxy and 0.4556 in random anisotropic spectra. Centered M4 reduces these to 0.0358 and 0.0574. Calibrated M4 reduces them to 0.0070 and 0.0065. The spiked traceless counterexample remains imbalanced under centered M4 with load error 0.1824.

## 1. Anchor Link And Decision Point

Anchor decision question:
Should the next theoretical and experimental target be raw M4, centered M4, calibrated M4, or a low-rank approximation of M4?

Decision after this experiment:
Use centered/calibrated M4 as the high-dimensional static target. Treat weighted top-r as an approximation family, not a replacement. Move to text-facing static transfer only after preserving load, margin, and oracle agreement.

## 2. Protocol Compliance Audit

approved conditions match actual conditions:
Partially. All named condition families were included, but `random_gaussian` was implemented as a fast Gaussian-like positive-spectrum proxy rather than exact dense Gaussian matrices. This is a runtime-driven implementation caveat and must be treated as spectrum-model evidence.

primary metric exists:
Yes. `load_error`, `mean_margin`, `low_margin_fraction`, `degeneracy_rate`, `r3`, and `operator_to_frobenius` are recorded in `tables/high_dim_metric_summary.csv`.

central figures/tables exist:
Yes. Central tables and figures are listed in the artifact map.

seeds/checkpoints recorded:
Yes. 100 seeds per dimension and condition. No checkpoints because this is a static audit.

known good/bad/confusing cases reviewed:
Yes. Equal isotropic and unequal isotropic controls are degenerate or non-directional; spiked traceless is the predicted high-dimensional failure case; balanced spectrum and separated low-rank are positive controls.

success/failure/insufficient-evidence criteria applied:
Yes. The result supports centered/calibrated M4, weakens raw M4, and gives partial support to top-r proxies only at sufficient rank.

## 3. Setup

Code:
`run_high_dim_uniform_centered_m4.py`

Command:

```bash
python run_high_dim_uniform_centered_m4.py
```

Dimensions:
`2, 4, 8, 16, 32, 64, 128, 256, 512`

Seeds:
100 per dimension and condition.

Samples:

- evaluation: 20,000 sphere samples per seed;
- calibration: 5,000 sphere samples per seed.

Conditions:

- `random_gaussian`: Gaussian-like positive-spectrum proxy;
- `equal_isotropic`;
- `unequal_isotropic`;
- `random_anisotropic`;
- `separated_low_rank`;
- `near_identical`;
- `spiked_traceless_counterexample`;
- `balanced_spectrum_control`.

Implementation note:
The first execution attempted exact repeated dense eigendecompositions for the random Gaussian condition and was interrupted because it was too slow. The final script replaces that condition with a spectrum proxy and records the proxy mode in the low-rank table.

## 4. Metrics And Decision Rules

Primary metrics:

- `load_error = |load_1 - 0.5|`;
- `mean_margin = E[|score_1-score_2|]` after the relevant centering or calibration;
- `low_margin_fraction = P(|score_1-score_2| < 1e-4)`;
- `degeneracy_rate = P(|score_1-score_2| < 1e-10)`;
- `r3 = sum |lambda|^3 / (sum lambda^2)^(3/2)`;
- `operator_to_frobenius = ||H0||op / ||H0||F`;
- `agreement_with_centered_m4` for top-r proxies.

Decision rules:

- Raw M4 is weakened if it is consistently load-imbalanced.
- Centered M4 is supported if it reduces load error while keeping positive margin.
- The spectral-spread hypothesis is supported if higher \(r_3\) tracks higher centered-M4 load error.
- Calibration is accepted only if load improves without margin collapse.
- Top-r proxies are useful only if agreement and margin retention improve with rank.

## 5. Main Results

### M4 Results At d=512

| Condition | Method | Load error | Mean margin | Low-margin fraction | \(r_3\) |
| --- | --- | ---: | ---: | ---: | ---: |
| random Gaussian spectrum proxy | raw M4 | 0.4644 | 0.0287 | 0.0030 | 0.2690 |
| random Gaussian spectrum proxy | centered M4 | 0.0358 | 0.0029 | 0.0254 | 0.2690 |
| random Gaussian spectrum proxy | calibrated M4 | 0.0070 | 0.0029 | 0.0259 | 0.2690 |
| random anisotropic | raw M4 | 0.4556 | 0.0560 | 0.0012 | 0.3884 |
| random anisotropic | centered M4 | 0.0574 | 0.0094 | 0.0087 | 0.3884 |
| random anisotropic | calibrated M4 | 0.0065 | 0.0092 | 0.0091 | 0.3884 |
| near-identical | centered M4 | 0.0027 | 0.0005 | 0.1276 | 0.0705 |
| spiked traceless | centered M4 | 0.1824 | 0.9659 | 0.0000 | 0.9971 |
| balanced spectrum | centered M4 | 0.0029 | 0.0543 | 0.0012 | 0.0505 |
| separated low-rank | centered M4 | 0.0028 | 0.0368 | 0.0018 | 0.1768 |

Interpretation:
Raw M4 fails the high-dimensional load target in random spectrum settings. Centering largely removes average-energy bias but still depends on spectral shape. Calibration enforces load in non-degenerate cases.

### Spectral Spread

Across non-isotropic conditions:

- Pearson correlation between \(r_3\) and centered load error: 0.7263.
- Spearman correlation between \(r_3\) and centered load error: 0.5650.

Condition-level examples:

- spiked traceless: Pearson 0.8766, Spearman 0.9256;
- random anisotropic: Pearson 0.5217, Spearman 0.4122;
- random Gaussian spectrum proxy: Pearson 0.4570, Spearman 0.3067.

Interpretation:
Spectral spread is not the only factor, but the direction is strongly aligned with the proof document's prediction.

### Low-Rank Proxy Evidence At d=512

Weighted top-r agreement with full centered M4:

| Condition | r=8 | r=32 | r=128 |
| --- | ---: | ---: | ---: |
| random Gaussian spectrum proxy | 0.7438 | 0.8161 | 0.8697 |
| random anisotropic | 0.8004 | 0.8715 | 0.9322 |
| separated low-rank | 0.6684 | 1.0000 | 1.0000 |

Interpretation:
Top-r proxies are promising only when rank is high enough or the true response difference is low-rank. Tiny-rank projections can be balanced yet disagree with full centered M4.

## 6. Visualization Results

### Load Error Versus Dimension

![Load error versus dimension](figures/load_error_vs_dimension.png)

Purpose:
Compare raw, centered, and calibrated M4 across dimension.

Setup:
Aggregated over 100 seeds per dimension and condition.

How to read:
Lower y-axis is closer to 50/50 load. Lines show method-condition pairs.

Observed result:
Raw M4 is highly imbalanced in random spectrum conditions. Centered M4 reduces load error. Calibrated M4 stays near balanced. Spiked centered M4 remains imbalanced.

Take-home:
Raw M4 should not be the high-dimensional load target.

Remaining uncertainty:
The random Gaussian condition is spectrum-proxy evidence, not exact dense Gaussian evidence.

### Load Error Versus Spectral Spread

![Load error versus spectral spread](figures/load_error_vs_spectral_spread.png)

Purpose:
Check whether \(r_3\) predicts centered-M4 load error.

Setup:
Each point is a condition-dimension-seed case.

How to read:
Higher \(r_3\) means a more spiky spectrum. Higher y means worse centered-M4 load balance.

Observed result:
Higher \(r_3\) generally corresponds to larger load error.

Take-home:
High-dimensional centered M4 needs spectral-spread or calibration assumptions.

Remaining uncertainty:
The relation is not a complete predictor of load in every condition.

### Agreement Versus Rank

![Agreement versus rank](figures/agreement_vs_rank.png)

Purpose:
Test whether weighted top-r proxies approach full centered M4.

Setup:
Rank sweep over selected dimensions and conditions.

How to read:
Higher agreement means the proxy matches full centered-M4 assignments more often.

Observed result:
Agreement increases with rank. Separated low-rank reaches exact agreement at the rank that covers the constructed subspaces.

Take-home:
Top-r is an approximation family; rank choice is a real decision.

Remaining uncertainty:
This is a spectral proxy, not a trained router implementation.

### Spiked Counterexample Histogram

![Spiked counterexample histogram](figures/spiked_counterexample_hist.png)

Purpose:
Show why zero-mean centered score does not guarantee 50/50 load.

Setup:
Spiked traceless counterexample at \(d=128\), seed 0.

How to read:
The zero line is the routing threshold. Unequal sign mass means load imbalance.

Observed result:
The distribution has zero mean but asymmetric sign mass.

Take-home:
The high-dimensional proof must use spectral spread or calibration, not centering alone.

Remaining uncertainty:
This is a constructed failure case, not a typicality claim.

## 7. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| Raw-vs-centered split | raw load error 0.46 vs centered 0.036 in d=512 random spectrum proxy | Passed | n/a | Rules out raw M4 as uniform-load target. |
| Degenerate controls | equal/unequal isotropic have zero centered margin and degeneracy | Passed | Expected no direction preference | Rules out mistaking trace-only difference for expert preference. |
| Spiked control | centered load error 0.1824 at d=512 | Passed | Spectrum dominated by one eigen-direction | Rules out unconditional high-dimensional 50/50 from centering. |
| Spectral diagnostic | Pearson r=0.7263 between \(r_3\) and load error | Passed with caveat | Correlational, not complete predictor | Supports spectral-spread hypothesis. |
| Calibration | d=512 random spectrum proxy calibrated load error 0.0070 | Passed | n/a | Shows load can be enforced when margin survives. |
| Near-identical guard | d=512 mean margin 0.0005, low-margin fraction 0.1276 | Passed | Expert responses too similar | Rules out using load alone as confidence. |
| Low-rank proxy | d=512 random anisotropic r=128 agreement 0.9322 | Passed with caveat | Requires substantial rank | Rules out tiny-rank proxy as generally sufficient. |

Falsified physical prior:
None. Expert geometry remains useful as a static scoring object.

Falsified mathematical model:
Unconditional high-dimensional exact 50/50 from centered M4 is falsified by the spiked traceless control.

Falsified operationalization / proxy:
Tiny-rank top-r proxy as a general replacement for full M4 is weakened.

Falsified implementation:
Exact dense random Gaussian eigendecomposition at the requested scale was too slow for this local run; it was replaced by a spectrum proxy.

Falsified metric:
Load alone is insufficient; near-identical cases can be balanced with tiny margin.

Remaining rival explanations:
Exact dense Gaussian experts may differ from the spectrum proxy; real text hidden states may be non-uniform and common-direction dominated; a trainable router may fail to approximate the static score.

## 8. Full Experiment Record

Run command:

```bash
python run_high_dim_uniform_centered_m4.py
```

Interrupted attempt:
The first run attempted repeated exact dense eigendecompositions for the random Gaussian condition and was interrupted. The final run uses a Gaussian-like positive-spectrum proxy for that condition and completed successfully.

Rows:

- `high_dim_metric_per_seed.csv`: 21,600 rows.
- `low_rank_approximation_per_seed.csv`: rank/method rows for all conditions, dimensions, and seeds.
- `spectral_spread_per_seed.csv`: one row per condition, dimension, and seed.

Central output files:

- `tables/high_dim_metric_summary.csv`
- `tables/spectral_spread_summary.csv`
- `tables/low_rank_approximation_summary.csv`
- `tables/calibration_summary.csv`
- `figures/load_error_vs_dimension.png`
- `figures/load_error_vs_spectral_spread.png`
- `figures/agreement_vs_rank.png`
- `figures/spiked_counterexample_hist.png`

## 9. Interpretation

Observation:
Raw M4 is heavily imbalanced in random spectrum and anisotropic conditions.

Interpretation:
Average expert energy remains a real source of routing bias in high dimension.

Claim:
Raw M4 should not be used as the high-dimensional uniform-load target.

Boundary:
This does not say raw M4 has no useful preference signal; it says the load objective needs centering or calibration.

Observation:
Centered M4 improves load but fails in the spiked traceless counterexample.

Interpretation:
Centering removes mean energy bias, but high-dimensional sign mass depends on the spectrum of \(H_0\).

Claim:
Centered M4 is useful only with a spectral-spread condition or follow-up calibration.

Boundary:
The observed relationship is empirical in this run.

Observation:
Calibration enforces load while preserving margin in non-degenerate cases.

Interpretation:
Calibration is a load-control mechanism, not a specialization proof.

Claim:
Calibrated M4 is the practical static target for the next bridge experiment.

Boundary:
Near-identical experts still have tiny margins.

Observation:
Weighted top-r agreement improves with rank but may require high rank.

Interpretation:
M3/top-r is a scalable approximation family, not a guaranteed low-rank replacement.

Claim:
The next experiment should test weighted low-rank M4 with rank selection rather than assume top-1 or tiny-r is enough.

Boundary:
The current low-rank audit uses spectrum proxies, not an actual trainable router.

## 10. Claim Boundary

Can claim:

- Centered/calibrated M4 is the best current high-dimensional static expert-geometry target.
- Raw M4 is weakened as a load-balanced target.
- Spectral spread is a useful diagnostic for when centered M4 is near-balanced.
- Calibration can enforce load without necessarily destroying margin.
- Weighted top-r approximation quality improves with rank.

Cannot claim:

- Centered M4 gives exact 50/50 for all high-dimensional expert pairs.
- Exact Gaussian matrix initialization has been fully audited at dense-matrix level.
- Text hidden-state routing will behave like uniform sphere routing.
- A trainable router can learn centered/calibrated M4.
- Load balance proves semantic expert specialization or task utility.

## 11. Next Decision

Run A06_01_07_E04 as a static text-facing transfer audit. The leading candidate should be empirical-centered or calibrated weighted low-rank M4. The next experiment must report load, margin, agreement with full centered M4, common-direction sensitivity, and rank needed for stable agreement.

## 12. Links And Artifact Map

anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

protocol:
`protocol.md`

summary:
`summary.md`

code workspace:
`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_07_E03_high_dimensional_static_geometry/`

runner:
`run_high_dim_uniform_centered_m4.py`

config:
embedded constants in `run_high_dim_uniform_centered_m4.py`

key code files:
`run_high_dim_uniform_centered_m4.py`

data / manifest:
synthetic spectra and uniform-sphere samples generated in the runner

result dir:
current experiment directory

figure dir:
`figures/`

key tables:
`tables/high_dim_metric_summary.csv`, `tables/spectral_spread_summary.csv`, `tables/low_rank_approximation_summary.csv`, `tables/calibration_summary.csv`

logs / checkpoints:
No checkpoints. No training.

repro command:
`python run_high_dim_uniform_centered_m4.py`

job id:
Local run, no scheduler job id.
