# Direct A-to-C and B-to-C parameter comparison

[中文](comparison_to_c_cn.md) · [Canonical Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R04_o_spectral_geometry/comparison_to_c/summary.md) · [Detailed evidence](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R04_o_spectral_geometry/comparison_to_c/detailed.md)

## Purpose

A/B/C differ measurably. B is closer to C than A is, for full O and leading16 full-weight operators. This parameter-only supplement tests that ordering, without gradients, as part of the shared-versus-conditional-learning question.

## Model

A continues consistent new rules; B reversed new rules only; C mixes old and reversed-new supervision from the same acquired-old state. Existing old/new accuracy is A100%/100%, B0%/99.25%, C99.83%/99.67%. Wc=Σσ_i u_i(v_iᵀc) gives large singular channels exact linear processing meaning; actual input alignment determines their use.

Compare T_AC=C-A and T_BC=C-B by SVD, and separately compare each full weight's leading16 reconstructed operator. Leading16 of a difference differs from difference of leading16 operators. Neither endpoint contrast is an executed training path.

## Hypothesis

Candidate: old-compatible A/C might be closer. Rival: B/C share reversed-new requirements but differ in retained old supervision, new exposure and Q/K/V; proximity may reflect new demands rather than old retention.

## Conclusion

1200 equal continuation-order means:

| Metric | A to C | B to C |
| --- | ---: | ---: |
| Full-O difference Frobenius norm | 3.7996 | 2.9888 |
| Difference / full C norm | 8.876% | 6.982% |
| Maximum difference singular value | 1.2233 | 1.0479 |
| Difference first16 energy | 79.621% | 78.237% |
| Full leading16 operator distance / C leading16 norm | 38.697% | 30.316% |
| Signed leading16 operator cosine | 0.9222 | 0.9526 |

Full and leading16 distances favor B/C proximity in all three orders. Fixed rank8/16/32 means preserve ordering, with one individual rank8 exception.

![Leading operator differences](/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry/runs/to_c_20261012_v1/figures/02_to_c_truncated_operator_distance.png)

X is retained rank; Y is operator difference / C truncated norm. Whiskers are three-order ranges, not confidence intervals or task effects.

## Analysis

Approximately80% difference energy lies in its own leading16, while88.58% A/C and85.88% B/C lies outside both full-C leading input/output coordinates. Learned-difference directions and dominant inherited matrix directions are different objects; full C leading16 explains only approximately5.5% matrix energy.

Relative to C's continuation displacement D_C, both-leading energy is65.11% A/C versus34.55% B/C; leading-output/other-input energy12.59% versus38.38%. B/C differences more often connect dominant C-displacement outputs to other inputs. This locates linear parameter differences, not causal old-rule protection.

![Reference blocks](/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry/runs/to_c_20261012_v1/figures/03_to_c_four_block_energy.png)

X is endpoint contrast; Y is squared difference energy. Upper/lower rows use full C versus its acquired-old displacement. Energy is not prediction contribution.

Common reversed-new requirements are an AI candidate explanation of B/C proximity, while extra old supervision helps explain why C can retain old rules. These factors were not independently isolated. Strong directions do change; the unsupported inference is that old-compatible endpoints must be geometrically closer. Shared compatibility needs a conditional computational explanation, not distance alone.

AI suggestion, not executed: insert leading16 T_BC or its residual with all other parameters fixed and evaluate both tasks, without gradients. This supplement does not identify task causality or separate-module utility.12 CPU SVDs,12 numerical tests and independent checks passed, maximum discrepancy7.54e-15. [Figure provenance](/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry/runs/to_c_20261012_v1/figures/figure_manifest.json). Actual output asset registered; mechanism acceptance/closure Unknown. No commit/push; figures remain execution-side.
