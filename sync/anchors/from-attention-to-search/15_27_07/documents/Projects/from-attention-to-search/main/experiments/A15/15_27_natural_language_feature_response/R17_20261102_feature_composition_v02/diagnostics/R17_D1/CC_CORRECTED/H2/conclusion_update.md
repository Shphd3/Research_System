派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/CC_CORRECTED/H2/conclusion_update.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/CC_CORRECTED/H2/conclusion_update.md)；研究修改仍回到原件。

---

# CC_CORRECTED / H2: conclusion update

## Purpose

Retest the original H2 without rewriting a failed positive hypothesis into a supported diagnostic statement. These are AI evidence assessments; researcher acceptance and next scientific decision remain Unknown.

## Hypothesis

Relative strength within the same candidates is not a stable refinement readout here; conditioning on membership and magnitude does not remove cue/context dependence. The original hypothesis and computation remain in [Protocol](protocol.md). C contains up to8 common candidates; F up to8 fine candidates; A=F minus C. A coordinate is an observation proxy, not a proven unique semantic atom. Dictionary identities are independent.

## Experiment

Own encoder and frequency statistics; old discovery selection and development regularization; fresh24families/12theorems/two paraphrases/answer-cue present or absent. Each cue condition has96 fine rows. The before-input diagnostic fixes corrected-discovery candidate IDs, uses original inputs and mixed/mixed selection. Corrected old48 and fresh192 are separate. Their difference is not a causal allocation to an individual correction.

| arm   | version                                       | cue         |   N |       LL |   correct |
|:------|:----------------------------------------------|:------------|----:|---------:|----------:|
| b_r   | Original inputs / mixed selection / old48     | explicit    |  24 | 0.561331 |        18 |
| b_r   | Original inputs / mixed selection / old48     | description |  24 | 0.722317 |        12 |
| b_r   | Corrected inputs / repaired selection / old48 | explicit    |  24 | 0.691670 |        12 |
| b_r   | Corrected inputs / repaired selection / old48 | description |  24 | 0.679459 |        14 |
| b_r   | Locked fresh /192 total,96 per cue condition  | explicit    |  96 | 0.702481 |        46 |
| b_r   | Locked fresh /192 total,96 per cue condition  | description |  96 | 0.703962 |        47 |
| q_b_r | Original inputs / mixed selection / old48     | explicit    |  24 | 0.413483 |        18 |
| q_b_r | Original inputs / mixed selection / old48     | description |  24 | 0.783321 |        15 |
| q_b_r | Corrected inputs / repaired selection / old48 | explicit    |  24 | 0.609627 |        24 |
| q_b_r | Corrected inputs / repaired selection / old48 | description |  24 | 0.671545 |        14 |
| q_b_r | Locked fresh /192 total,96 per cue condition  | explicit    |  96 | 0.632002 |        66 |
| q_b_r | Locked fresh /192 total,96 per cue condition  | description |  96 | 0.720911 |        51 |

## Analysis

No-answer loss gains, with theorem-group2000-bootstrap simultaneous95% intervals within each declared comparison family:

- identity_amplitude_minus_relative: -0.016950 [-0.027485, -0.008516]


Resolved rivals: unbound n, cue/frame confounding, incorrect SAE hook identity, shared dictionary frequencies, mixed dtype and missing equal-budget baselines. Remaining: cue-biased candidate selection, theorem/paraphrase transfer, linear-model calibration, task-signal retention by each dictionary, and limited independent groups. Membership/magnitude are adjusted covariates with a same-support subset, not exact interventions. See [Detailed](../../detailed.md), [cases](../../casebook.md) and [corrections](../../corrections.md).

## Conclusion

**ATTN opposes a positive pooled increment; MLPIN has a small pooled gain but a negative no-answer gain, so the stable claim is not supported.** Relative strength within the same candidates is not a stable refinement readout here; conditioning on membership and magnitude does not remove cue/context dependence. Scope is this model/dictionary/panel/readout. No claim of absent nonlinear information, causal use, training benefit, or architecture ranking follows. H4 failure of target coverage is not negative mechanism evidence.

Knowledge update: Relative strength within the same candidates is not a stable refinement readout here; conditioning on membership and magnitude does not remove cue/context dependence.

AI revision direction: require stability across cue, paraphrase and theorem changes; preserve H3's dual budget-matched comparison and H4's content and rarity gates. One suggested next decision, owned by the researcher: prioritize the observed gap between readable no-answer question-prefix representations and weak current dictionary/small-set readouts. No new experiment is launched.

[Raw outputs](../../../../../../../../../../../../UNAVAILABLE.md) · [per-item predictions](../../../../../../../../../../../../UNAVAILABLE.md) · [coefficients/scalers](../../../../../../../../../../../../UNAVAILABLE.md)

## Fixed text and route predictions

Old original (same old ID before and after repair):

```text
Let A be a real array with 22 rows and 22 columns. For this array, zero is not an eigenvalue.
Summarize the mathematical object and its stated properties.
Summary:
```

Corrected old:

```text
Consider a real square matrix A with n = 22. It satisfies the following condition: zero is not an eigenvalue. This is the full description for this exercise.
Summarize the mathematical object and its stated properties.
Summary:
```

Locked fresh instance (related spectral certificate, different n and expression, not an old/new identical-input contrast):

```text
Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is nonzero. This is the full description for this exercise.
Summarize the mathematical object and its stated properties.
Summary:
```

| id                                      | arm   |   p_invertible |     loss |   correct |
|:----------------------------------------|:------|---------------:|---------:|----------:|
| M05_0_invertible_description            | b_r   |       0.494947 | 0.703305 |         0 |
| D1_M05_0_invertible_description_p0_main | b_r   |       0.493179 | 0.706883 |         0 |
| M05_0_invertible_description            | q_b_r |       0.479594 | 0.734815 |         0 |
| D1_M05_0_invertible_description_p0_main | q_b_r |       0.509712 | 0.673910 |         1 |
