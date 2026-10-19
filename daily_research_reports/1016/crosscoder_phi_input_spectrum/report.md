# Raw representation spectra of inputs selected by the frozen φ groups

This supplement reuses the original 186 φ groups and the original learning R/F/N winner rules. It reads genuine cached block-28 hidden, before final RMSNorm. No decoder contribution, training, new forward, regrouping, or graph changes are involved.

Within the common supported population of 145 group IDs, R has a lower mean original leading variance share and a lower mean residual leading share than F and N. The distributions overlap and the ordering is heterogeneous across group sizes. This is a descriptive property of the selected input sets, not a causal φ effect, capacity estimate, or learning benefit.

| Condition | Original leading share | Residual leading share | Mean residual trace |
| --- | --- | --- | --- |
| R | 12.5324% | 8.5749% | 116139.87 |
| F | 13.1439% | 9.0896% | 124375.38 |
| N | 14.0502% | 9.3402% | 127005.78 |

The columns above respectively mean original leading share, residual leading share after each group's own centered PC1 is removed, and mean remaining total variance. Values are group-equal. Original and residual shares have different denominators, so their difference is not an explained-effect fraction.

## Selection and population

R is the original φ partition. F sorts the same 13,807 features by discovery frequency and fills R's group-size sequence. N permutes R labels within ten discovery-frequency bins, exactly preserving per-group bin counts and sizes. All conditions contain 186 groups, sizes 2–735. These are not the later fixed-size-14 same/mixed-frequency groups.

The original score standardizes each group's binary active-member fraction using saved D mean and standard deviation. Only hit groups compete; a negative maximum still wins. Saved member-hash order breaks ties. No-hit positions receive no group, regardless of the downstream four-expert fallback. Reconstructed expert routes match every cached position; 33 actual positions across three conditions also pass 99 independent row-wise group-winner checks. Spectra use the 186-way group winners, not four experts and not any-member hits.

All conditions use the same EVAL512 source, 523,136 eligible positions and 512 contexts. The file is from original CrossCoder TRAIN provenance, not structural validation V or a new independent-document confirmation. Each supported group samples exactly 128 winning positions without replacement using frozen deterministic priorities independent of hidden and spectra.

R/F/N support respectively 176/168/171 groups; 10/18/15 groups remain explicitly insufficient. The primary common 145 group IDs preserve the same group-size sequence and cover 8,814/13,807 members (63.84%). The R/N supplement includes 161 groups but only 64.07% of members. Missing support in N is concentrated in large groups. No estimable group has zero original or residual variance.

## Figures

All four figures use block 28, N=128 per group, and 145 groups per condition.

![Original normalized spectrum](figures/figure7_phi_raw_spectrum.png)

Object: covariance of genuine hidden at group-winning positions. Computation: center across positions, normalize each group's eigenvalues by its own trace, then average groups equally. Observation: first shares are R12.53%, F13.14%, N14.05%; curves are close and not uniformly ordered. Boundary: input-set variance organization, not frequency causation or capacity. The displayed 127 directions are a sample-rank limit.

![Original leading share distribution](figures/figure8_phi_raw_first_share.png)

Object: per-group original leading share. Computation: all points are shown; boxes are IQR, black lines medians, whiskers span points within 1.5 IQR, and diamonds equal-group means. Observation: R is lower than N in 85/145 groups and lower than F in 78/145, with broad overlap. Boundary: an average ordering is neither universal advantage nor independent-document statistical significance.

![Residual normalized spectrum](figures/figure9_phi_residual_spectrum.png)

Object: hidden variation outside each group's own first centered principal direction. Computation: remove the full rank-one SVD component and renormalize λ₂,λ₃,… by remaining variance. Observation: residual first shares are R8.57%, F9.09%, N9.34%. Boundary: this is not removal of one global uncentered direction, nor identification of a common feature; at most 126 sample directions remain.

![Residual leading share distribution](figures/figure10_phi_residual_first_share.png)

Object: group-wise residual leading shares. Computation: λ₂ divided by remaining trace, using unchanged positions and group IDs. Observation: R is lower than N in 90/145 groups, but 55 go the other way; R/F counts are 74/71. Boundary: residual concentration does not measure semantic diversity, capacity, or learning compatibility; renormalization need not lower every group's ratio.

## Heterogeneity and source limitations

| Group size | Groups | Roriginal / residual | Foriginal / residual | Noriginal / residual |
| --- | --- | --- | --- | --- |
| Small: 2–3 | 69 | 11.34%／8.39% | 14.87%／10.14% | 13.25%／8.90% |
| Medium: 4–19 | 22 | 13.95%／9.05% | 9.18%／6.93% | 12.99%／9.15% |
| Large: 20+ | 54 | 13.48%／8.62% | 12.55%／8.63% | 15.50%／9.98% |

Rows are small (2–3), medium (4–19), and large (20+) groups; each condition cell gives original/residual shares. Medium groups reverse the original R/N average ordering, and R is more concentrated than F in both states. Large-group residual R/F means are nearly equal. A universal group-size claim is unsupported.

Mean member log10 D frequency, averaged equally across the main groups, is R−2.2048, F−1.1732, N−2.2253. F differs materially in group-average frequency; N's bin matching does not exactly match continuous frequency. Median selected-context counts are 106/105/103; maximum single-context shares are 32.03%/7.81%/14.06%. Same-condition selected positions are disjoint, but contexts and cross-condition positions can overlap.

A clearly post-outcome descriptive check retains 136 common group IDs whose maximum single-context share is at most 10% in every condition, without changing any samples. Original shares are R12.55%/F13.17%/N14.03%; residual shares are R8.55%/F9.11%/N9.23%. The average ordering persists outside the nine excluded groups; text-composition and document-repetition explanations remain unresolved.

The R/N intersection of 161 groups also yields original means 12.29%/14.25% and residual means 8.54%/9.43%. All-supported condition-specific results are retained separately, without substituting differently covered populations for the main comparison.

See [methods](methods.md), [complete metrics and missingness](data/per_group_input_hidden_metrics.csv), [population tables](data/population_summary.csv), [paired size strata](data/paired_group_contrasts.csv), [frozen configuration](provenance/frozen_config.json), and [independent audit](provenance/audit_result_audit.json). Four PNGs were viewed and independently replotted byte-identically; PDFs were generated but not independently rendered. Researcher-owned mechanism judgment and question closure remain Unknown.
