派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/MLPIN_SAE/H4/conclusion_update.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/MLPIN_SAE/H4/conclusion_update.md)；研究修改仍回到原件。

---

# MLPIN_SAE / H4: conclusion update

## Purpose

Retest the original H4 without rewriting a failed positive hypothesis into a supported diagnostic statement. These are AI evidence assessments; researcher acceptance and next scientific decision remain Unknown.

## Hypothesis

Finite search finds low-frequency state combinations of common members, but this study cannot identify them as rare fine-grained concepts. The original hypothesis and computation remain in [Protocol](protocol.md). C contains up to8 common candidates; F up to8 fine candidates; A=F minus C. A coordinate is an observation proxy, not a proven unique semantic atom. Dictionary identities are independent.

## Experiment

Own encoder and frequency statistics; old discovery selection and development regularization; fresh24families/12theorems/two paraphrases/answer-cue present or absent. Each cue condition has96 fine rows. The before-input diagnostic fixes corrected-discovery candidate IDs, uses original inputs and mixed/mixed selection. Corrected old48 and fresh192 are separate. Their difference is not a causal allocation to an individual correction.

| arm                         | version                                       | cue         |   N |       LL |   correct |
|:----------------------------|:----------------------------------------------|:------------|----:|---------:|----------:|
| 11234_2__47_2_additive      | Original inputs / mixed selection / old48     | explicit    |  24 | 0.652927 |        19 |
| 11234_2__47_2_additive      | Original inputs / mixed selection / old48     | description |  24 | 0.687880 |        12 |
| 11234_2__47_2_additive      | Corrected inputs / repaired selection / old48 | explicit    |  24 | 0.641110 |        16 |
| 11234_2__47_2_additive      | Corrected inputs / repaired selection / old48 | description |  24 | 0.679771 |        13 |
| 11234_2__47_2_additive      | Locked fresh /192 total,96 per cue condition  | explicit    |  96 | 0.675147 |        59 |
| 11234_2__47_2_additive      | Locked fresh /192 total,96 per cue condition  | description |  96 | 0.703198 |        49 |
| 11234_2__47_2_configuration | Original inputs / mixed selection / old48     | explicit    |  24 | 0.652927 |        19 |
| 11234_2__47_2_configuration | Original inputs / mixed selection / old48     | description |  24 | 0.687880 |        12 |
| 11234_2__47_2_configuration | Corrected inputs / repaired selection / old48 | explicit    |  24 | 0.641110 |        16 |
| 11234_2__47_2_configuration | Corrected inputs / repaired selection / old48 | description |  24 | 0.679771 |        13 |
| 11234_2__47_2_configuration | Locked fresh /192 total,96 per cue condition  | explicit    |  96 | 0.675147 |        59 |
| 11234_2__47_2_configuration | Locked fresh /192 total,96 per cue condition  | description |  96 | 0.703198 |        49 |

## Analysis

No-answer loss gains, with theorem-group2000-bootstrap simultaneous95% intervals within each declared comparison family:

- additive_minus_configuration: -0.000000 [-0.000000, 0.000000]
- matched_minus_configuration: unavailable: no valid matched control


Natural validation: 19200 positions /150 documents.

| config        |   joint_count |   joint_documents |   joint_frequency |   simultaneous_upper |   joint_to_product | formal_rarity_supported   |
|:--------------|--------------:|------------------:|------------------:|---------------------:|-------------------:|:--------------------------|
| 11234_2__47_2 |            75 |                37 |          0.003906 |             0.005156 |           0.486815 | False                     |

Both SAE matched-configuration pools failed all20 attempts; this is a measured eligibility failure, not an omitted search. Additive/configuration fits ran. Original CC10/208pairs remain unchanged; corrected FP32 CC has its own10/228pairs. No determinate fine label was found in natural blind prefixes. Enrichment has only2 invertible/0 singular documents, below10/class; unknown labels are not negatives.

Resolved rivals: unbound n, cue/frame confounding, incorrect SAE hook identity, shared dictionary frequencies, mixed dtype and missing equal-budget baselines. Remaining: cue-biased candidate selection, theorem/paraphrase transfer, linear-model calibration, task-signal retention by each dictionary, and limited independent groups. Membership/magnitude are adjusted covariates with a same-support subset, not exact interventions. See [Detailed](../../detailed.md), [cases](../../casebook.md) and [corrections](../../corrections.md).

## Conclusion

**Insufficient: measured support/rarity-bound, content-coverage and matched-configuration limitations.** Finite search finds low-frequency state combinations of common members, but this study cannot identify them as rare fine-grained concepts. Scope is this model/dictionary/panel/readout. No claim of absent nonlinear information, causal use, training benefit, or architecture ranking follows. H4 failure of target coverage is not negative mechanism evidence.

Knowledge update: Finite search finds low-frequency state combinations of common members, but this study cannot identify them as rare fine-grained concepts.

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

| id                                      | arm                         |   p_invertible |     loss |   correct |
|:----------------------------------------|:----------------------------|---------------:|---------:|----------:|
| M05_0_invertible_description            | 11234_2__47_2_additive      |       0.499700 | 0.693747 |         0 |
| D1_M05_0_invertible_description_p0_main | 11234_2__47_2_additive      |       0.436535 | 0.828887 |         0 |
| M05_0_invertible_description            | 11234_2__47_2_configuration |       0.499700 | 0.693747 |         0 |
| D1_M05_0_invertible_description_p0_main | 11234_2__47_2_configuration |       0.436535 | 0.828887 |         0 |

Own primary configuration: `{"config": "11234_2__47_2", "atom_a": 11234, "state_a": 2, "atom_b": 47, "state_b": 2, "discovery_positions": 126, "discovery_documents": 61, "discovery_frequency": 0.00328125, "state_a_frequency": 0.059557291666666665, "state_b_frequency": 0.13361979166666665, "panel_discovery_difference": 0.0, "panel_discovery_hits": 0, "target": "invertible", "eligible": true, "reasons": ""}`. State cuts remain frozen. Raw member values and enriched event flags are in results/H4_enrichment_sensitivity.csv, not inferred from these predictions.

## Final localization receipt

[Current read-only failure localization](../../summary.md): actual H4event counts, admissible matching attempts, and Kconditional uncertainty are stated separately. In particular MLPIN H4event is identically0 on all fine rows; ATTN K64 has0/20successful matched sets. No parameter or candidate was changed.
