# Larger-sample and cross-layer review: association without a reliable token label

[中文](summary_cn.md) · [Detailed evidence](detailed.md) · [Protocol](protocol.md)

**The DCLM evidence supports a narrower description: rarer features tend to hit positions whose current tokens are rarer on average. It does not establish that rare tokens reliably activate the lowest-frequency feature pool.** For that position-level profile, DCLM does not reproduce Tulu's approximately 0.259 association magnitude: position-weighted rho is 0.00619 and token-ID-weighted rho is −0.11904. All 14 layers agree in these directions but share the same activation z; they are not 14 independent validations. Factual recording is complete; the researcher's scientific judgment and question closure remain Unknown.

## Purpose and actual model

The earlier result suggested that rarer current tokens might have higher decoded-amplitude shares from rare features. This review tests sensitivity to sample, layer and weighting. The strongest rivals are token identity/format/position composition, tail support and the share denominator, rather than a universal rare-token/rare-feature correspondence.

We froze Qwen3-0.6B Base and the 14-layer joint CrossCoder, reusing 10,485,760 DCLM cached positions: D=5,238,097 to estimate frequencies and V=5,247,663 for review. The original Tulu TRAIN85,548/EVAL22,446 positions supply a cross-layer supplement, not a larger SFT sample. No training or new neural inference occurred. The current token is already read at t, not the next target.

Each corpus defines feature frequency p and token frequency f on its own reference side. Four equal-width positive-log-p bands yield a lowest band of 314 DCLM features versus 1694 Tulu features. Position-level R1 sums shared z times layer decoder norms over that band and divides by the corresponding full 16,384-feature sum. It is an amplitude share, not hit probability, information or net vector contribution.

## Three units answer different questions

| Question / weighting unit | DCLM | Tulu SFT |
|---|---:|---:|
| Position: current-token rarity versus final-layer R1 | 0.006191 | 0.259051 |
| Token ID: rarity versus the ID's mean R1 | −0.119041 | 0.124371 |
| Feature: feature rarity versus mean current-token rarity on its hits | 0.336019 (15,928 features) | 0.374516 (14,610) |
| Previous row restricted to ≥20 known-token review hits | 0.339147 (15,749) | 0.119556 (10,220) |

The first two rows use the local low-frequency pool in [layer metrics](tables/layer_metrics.csv). The last two use all eligible features in the [feature-level summary](tables/feature_correspondence_summary.csv), not just the lowest band. Their units and weights differ; they neither contradict nor replace each other. The DCLM feature-level direction survives the fixed ≥20-hit sensitivity check; Tulu's is more tail-sensitive. **Corpus, reference window and rare-feature membership change together; the DCLM–Tulu difference cannot be attributed to sample expansion alone.** Overall rho has a point estimate only; no overall-rho confidence interval was computed. [Figure 4](figures/figure4_feature_level_correspondence.png) shows the trend across sufficiently supported features. Only 34/314 DCLM lowest-band features and 2/1694 Tulu lowest-band features reach ≥20 eligible review hits, so Figure 4 cannot substitute for the lowest-band primary test; see [support qualification](tables/feature_level_support.csv).

## What agrees across layers

DCLM position rho is approximately 0.00619 throughout layers 2–28 and ID-weighted rho approximately −0.11904. Tulu ranges are 0.25650–0.25905 and 0.11643–0.12437. [Figure 1](figures/figure1_layer_correlations.png) shows these two overall weighting schemes above and equal-block/conversation means with descriptive intervals below. The lower intervals are not confidence intervals for the upper overall rho.

At DCLM layer 28, 37/41 V blocks have positive rho; the equal-block mean is 0.007474 with a 1000-resample 95% descriptive interval [0.004663, 0.010108]. This is a consistent but tiny within-bin direction, not independent-document confirmation. Tulu has 227 estimable conversations, 212 positive, and 29 NA out of 256; its layer-28 equal-conversation mean is 0.255918 [0.231404, 0.280123]. See [block correlations](tables/block_correlations.csv) and [stability](tables/block_stability.csv).

## Why this is not a reliable label

DCLM's local lowest-frequency pool hits only 0.05294% of all V positions; R1 is zero at 99.94706%. Tulu's hit incidence is 16.31471%. Even among DCLM's rarest current-token group (reference count 1–3), only 0.19305% of positions hit the pool and mean R28 is 0.002643%; the most frequent group (≥37) has 0.04674% and 0.000634%. The endpoint direction exists, but nearly all rare-token positions still fail to hit, and intermediate groups are not strictly monotone. [Binary metrics](tables/binary_metrics.csv) and [all groups](tables/groups.csv) preserve denominators and NA. Classification accuracy and knowledge identification were not tested.

At layer 28, rarity versus M_low has rho 0.006191 in DCLM and 0.260185 in Tulu, close to the R results; total-amplitude rho is 0.325661 and 0.194053. The direction cannot simply be attributed entirely to the denominator, but identity, format and context remain causally unresolved. [Figure 2](figures/figure2_r28_token_band.png) retains all four shares; [Figure 3](figures/figure3_binary_contribution.png) separates hits, amplitude and denominator.

Only 25 of the fixed old Tulu 1694 features remain in DCLM's local 314-feature lowest band; 11 become D-zero-frequency. The old pool's DCLM layer-28 position rho is 0.157293, with ID-weighted rho −0.218740. This is fixed-membership migration, not replication for locally rare DCLM features. See [migration](tables/migration.csv) and [layer metrics](tables/layer_metrics.csv).

## Completion and boundary

Core CPU statistics completed in 314.8 seconds with recorded peak process RSS4.16GiB, producing 10 core tables and three derived/definition/qualification tables (13 total). Old Tulu layer-28 profiles reproduced position-wise and all 16,384 DCLM V marginal counts matched. Independent identity/table auditing is PASS_WITH_LIMITATIONS. Engineering completion does not promote scientific confirmation. DCLM remains within-bin with original-document independence UNKNOWN; Tulu EVAL is exposed and all layers share z. No causality, rare-knowledge identification, routing utility, learning gain or question closure follows.

**One AI-suggested question: does the feature-level association persist with original-document-separated data after accounting for format, source and position?** This is a researcher's choice, not an automatically authorized next run.

Similar association coefficients do not mean equal contribution shares. Across all Tulu review positions, mean low-band share is about 0.6274% at layer2 versus 0.1079% at layer28. This is a decoder-amplitude profile, not low-frequency knowledge quantity.
