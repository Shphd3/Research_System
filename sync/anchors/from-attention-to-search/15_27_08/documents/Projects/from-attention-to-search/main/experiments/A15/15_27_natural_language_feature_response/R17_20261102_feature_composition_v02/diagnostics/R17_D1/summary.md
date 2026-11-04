派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary.md)；研究修改仍回到原件。

---

# R17_D1: feature composition and language relations, two native SAEs

[中文](summary_cn.md) · [Detailed](detailed.md) · [Cases](casebook.md) · [Verification](verification.md)

Read along three analysis paths: (1) behavior and factor controls, (2) representations and location-specific organization, (3) functional interventions and quality. No causal intervention was run; path3 covers frozen-execution, precision and annotation quality.

## Purpose

Test whether refinement uses extra members, relative strengths, frequency complementarity or rare configurations. Both native SAE sites completed H1–H4; A22 is a separate reference. **Shared coarse response recurs, but it does not establish stable fine-concept organization across cue and readout contexts.**

## Hypotheses

H1 requires actual recruitment and incremental information beyond common and count-matched random members. H2 conditions on member identity and total magnitude. H3 requires equal-budget mixed members to beat both high-only and middle/low-only sets. H4 separately requires rarity, clear content correspondence and cross-context replication; an additional discrimination claim requires comparison to an additive model of the same members.

ATTN_SAE observes block27 attention o_proj output before residual addition. MLPIN_SAE observes actual MLP input after residual addition and RMSNorm. Each has its own30000-member Top32 dictionary. A22 jointly encodes14 residual-post blocks into16384 shared members and reconstructs block27. No atom IDs are aligned, and these observations cannot identify a pure location causal effect.

## Experiment

Old384 rows support discovery, development and error diagnosis. Freeze own frequencies/candidates/optional gates before evaluating locked288main rows,192fine, plus48one-factor controls. Fine rows span24families,12theorems,two paraphrases,cue present/absent;96 rows per cue condition. Natural frequencies use matching600documents/76800positions; boundaries fit300discovery documents/38400positions. Primary FP32 was chosen before fresh evaluation; precision check uses24old cases.

One2x5090spot job pt-viic7g4p completed2026-11-03 02:30:02UTC. No LM or dictionary updates. Only CPU L2 logistic probes fit. All original R17 hashes remain unchanged. Before old48, corrected old48 and new192 are separate comparisons, not a causal decomposition of repairs.

## Analysis

C denotes8common candidates; C_union_F is their16-member union with8fine candidates. b_r uses support identity and total magnitude; q_b_r adds relative strength. H/M/J are high-only, middle/low-only and mixed16-member groups, selected independently within each dictionary.

No-answer fresh results (lower logloss is better; uniform baseline0.693147):

| site         | H   | arm       |       LL | correct   |
|:-------------|:----|:----------|---------:|:----------|
| ATTN_SAE     | H1  | C         | 0.706420 | 44/96     |
| ATTN_SAE     | H1  | C_union_F | 0.706364 | 42/96     |
| ATTN_SAE     | H2  | b_r       | 0.925955 | 45/96     |
| ATTN_SAE     | H2  | q_b_r     | 1.210693 | 45/96     |
| ATTN_SAE     | H3  | H         | 0.733004 | 48/96     |
| ATTN_SAE     | H3  | M         | 0.984849 | 49/96     |
| ATTN_SAE     | H3  | J         | 0.734410 | 46/96     |
| MLPIN_SAE    | H1  | C         | 0.695204 | 50/96     |
| MLPIN_SAE    | H1  | C_union_F | 0.703452 | 56/96     |
| MLPIN_SAE    | H2  | b_r       | 0.693579 | 50/96     |
| MLPIN_SAE    | H2  | q_b_r     | 0.705954 | 49/96     |
| MLPIN_SAE    | H3  | H         | 0.757480 | 52/96     |
| MLPIN_SAE    | H3  | M         | 0.710831 | 57/96     |
| MLPIN_SAE    | H3  | J         | 0.709414 | 54/96     |
| CC_CORRECTED | H1  | C         | 0.719244 | 49/96     |
| CC_CORRECTED | H1  | C_union_F | 1.638051 | 73/96     |
| CC_CORRECTED | H2  | b_r       | 0.703962 | 47/96     |
| CC_CORRECTED | H2  | q_b_r     | 0.720911 | 51/96     |
| CC_CORRECTED | H3  | H         | 1.562467 | 66/96     |
| CC_CORRECTED | H3  | M         | 0.698096 | 51/96     |
| CC_CORRECTED | H3  | J         | 0.569979 | 75/96     |

H1 pooled gains are0.07205/0.14041 for ATTN/MLPIN, but no-answer gains are0.00006/−0.00825. Both beat matched-random additions, yet neither establishes the required advantage over the common set. Real transitions separate recruitment from amplitude: among768no-answer extra-member comparisons, ATTN has67off→on and19on→on; MLPIN42off→on and286on→on.

H2 no-answer gains are−0.28474/−0.01238; MLPIN theorem interval[−0.01792,−0.00609]. Same-support29/31pairs also yield negative gains. A small pooled MLPIN gain does not establish a cue-stable strength code. Controls are statistical covariates/same-support subsets, not exact interventions.

H3 neither SAE meets both budget-matched advantages. ATTN's pooled mixed set is worse than high-only by0.03819. MLPIN's high-minus-mixed interval crosseszero despite a middle/low advantage. Corrected CC has pooled dual gains but not robust no-answer dual gains; it cannot substitute for either SAE.

H4 ATTN validation support11positions/6documents fails30/10; MLPIN has75/37 but rarity upper bound0.005156 exceeds0.005. Additive/configuration fits ran; all20matched-configuration attempts/site failed frozen-pool eligibility. Original CC10configurations/208pairs stay unchanged; corrected FP32 CC has10/228. Controls improve9/20→20/20 after actual text-rule repair, not a natural-recall estimate. Agent reviews49old,6ATTN and40MLPIN prefixes found no determinate fine positives. Full600sources match600SHA hashes; automatic full-document detection has no fine positive. Bounded100000-line enrichment yields48prefixes but only2invertible/0singular, below10/class. Unknowns are not negatives; content correspondence and replication remain unidentified.

Native full-candidate continuation scores classify73/96no-answer rows; fixed question format50/96 and it fails the direct invertible-answer control. This is evidence of output-format sensitivity, not absent knowledge. At the fixed question-prefix observation, old-only fit gives original hook logloss~0.51/0.52 and79/76correct; own reconstructions and fixed small sets are weaker:

| site         | representation   |   N |       LL |   correct |
|:-------------|:-----------------|----:|---------:|----------:|
| ATTN_SAE     | h                |  96 | 0.507074 |        79 |
| ATTN_SAE     | reconstruction   |  96 | 0.654091 |        60 |
| ATTN_SAE     | residual         |  96 | 0.501927 |        73 |
| ATTN_SAE     | selected_union   |  96 | 0.746670 |        48 |
| CC_CORRECTED | h                |  96 | 0.504878 |        76 |
| CC_CORRECTED | reconstruction   |  96 | 0.511335 |        70 |
| CC_CORRECTED | residual         |  96 | 0.850660 |        75 |
| CC_CORRECTED | selected_union   |  96 | 0.489588 |        74 |
| MLPIN_SAE    | h                |  96 | 0.520332 |        76 |
| MLPIN_SAE    | reconstruction   |  96 | 0.744264 |        59 |
| MLPIN_SAE    | residual         |  96 | 0.732017 |        73 |
| MLPIN_SAE    | selected_union   |  96 | 0.679760 |        54 |

Context and observation position move together here. This weakens the wholly absent-signal account and favors readout context, dictionary retention and selection as live bottlenecks, without identifying their unique mechanism. Optional description-specific K16/32/64 runs were enabled from old data and completed, without reversing the main findings.

Direct between-site comparisons use the same bootstrap indices. No-answer H2 gain difference0.27236,[−0.13304,0.60590] does not establish a difference; H3 middle/low-minus-mixed difference−0.24902,[−0.40718,−0.10161] is a scheme effect with dictionary/hook confounds, not pure position causality.

## Conclusion

- H1: insufficient for full extra-member claim; coarse response and actual support changes remain.
- H2: ATTN pooled positive increment opposed; MLPIN small pooled gain reverses without cues, so stable claim not supported.
- H3: neither SAE supports dual equal-budget superiority.
- H4: insufficient support/rarity confidence and target coverage; no negative mechanism conclusion.

Knowledge update: coarse-candidate reuse is better established than stable fine-member organization. Relative strength, frequency mixing and rare states cannot yet be promoted to general concept-refinement rules.

AI revision direction: require cue-free, paraphrase- and theorem-stable incremental evidence while retaining both H3 controls and H4 gates. One researcher-owned next decision: prioritize the gap between readable question-prefix representations and current dictionary/small-set readouts. No follow-up experiment is started. Scientific acceptance and closure remain Unknown. [Corrections](corrections.md) records applied T1/S1/P1/R1/L1 and exact recomputations.


### Final localization: configuration response, valid controls and visible context

MLPIN primary H4 configuration11234strong+47strong never occurs in any old-discovery/development/diagnostic or fresh fine-label row. All20candidate controls have exactly the same semantic-panel indicator and fail IDENTICAL_INDICATOR_FAILED. ATTN has no admissible distance-matched pool (20MATCH_FAILED); its no-answer primary event occurs in2/48invertible and2/48singular rows. Thus current-configuration response, distinguishable controls and natural target coverage are separate measured bottlenecks. A zero gain is not evidence of no interaction mechanism, and configurations are not reselected.

Description-selection is not uniformly unchanged: ATTN K16/32/64 no-answer LL=.6840/.6716/.6854; K32 improves over original union.7064 and classifies58/96, but matched-random gain.02203 has theorem simultaneous interval[−.00539,.04949]. ATTN K64 matching succeeds0/20, so no matched gain is estimated; K16/32 each20/20. MLPIN each20/20 has LL=.8213/.8245/.7433, not better than original union.7034. These do not establish stable or monotonic organization.

“No-answer” in the question-position diagnostic refers to the body withholding the correct answer. The appended question contains both option words but does not reveal the correct class. This is not a replication in a prefix entirely without option words.

[H4event counts](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/tables/H4_semantic_panel_event_counts.csv) · [Kmatching status](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/tables/optional_K_matching_status.csv) · [Kconditional effects](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/tables/optional_K_conditioned_effects.csv). Read-only frozen-output diagnostics; no forward, reselection, fit or search.
