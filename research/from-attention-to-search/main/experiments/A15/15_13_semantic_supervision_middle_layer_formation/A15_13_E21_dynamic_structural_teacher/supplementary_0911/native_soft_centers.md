# Common input empirical centers: native membership addendum

Status: POSTHOC_BOUNDED; interpretation is AI_DRAFT_AWAITING_HUMAN_CONFIRMATION. User-requested plotting correction, 2026-09-11. No main-model or SAE training. This does not close E21 or change its registered verdict.

## Purpose
Compare K-Means, GMM and SAE groups in a common input coordinate system, separating representation motion from reassignment.

## Hypothesis
The descriptive question is whether initially grouped inputs tighten and their centers separate. Overlapping soft membership is a rival explanation for nearby projected SAE centers; nearby centers alone do not establish poor semantic groups.

## Analysis method
The same dynamic_sae_b_u trajectory, seeds 17/29/43, six updates 0/32/64/128/256/512 and 1247 answer-prediction positions are used. Existing source/record/position-balanced weights are normalized to sum to one. Let \(u_i(t)=h_i(t)/\|h_i(t)\|\). Each method defines initial memberships \(q_{ig}(0)\): K-Means one-hot labels; diagonal GMM posterior probabilities; SAE normalized feature-group activation mass. Freeze these memberships for every subsequent checkpoint.

\[m_g=\sum_iw_iq_{ig}(0),\qquad \mu_g(t)=\frac{\sum_iw_iq_{ig}(0)u_i(t)}{m_g}.\]

\[W(t)=\sum_{ig}w_iq_{ig}(0)\|u_i(t)-\mu_g(t)\|^2,\qquad B(t)=\sum_gm_g\|\mu_g(t)-\bar u(t)\|^2.\]

These are empirical input centers, not SAE decoder directions or GMM parameter means. Soft W includes overlap across groups. W+B equals total scatter; neither statistic establishes natural class count. Different partition objectives prevent interpreting absolute W/B as a fair ranking of semantic quality.

GMM is refitted on initial unit inputs with the previous unweighted diagonal recipe (K=8, n_init=1, max_iter=200, reg_covar=1e-6, random_state=20260910); hard-label equality to prior fits is verified in all three seeds. K-Means reuses the previous labels. SAE uses saved initial ordinary-node group distributions. All eight groups have positive weighted mass for each method/seed.

The figure uses seed17 and the same fixed initial PCA projection as the previous figures (34.4% initial variance retained), with common axis limits. Grey points are the same terminal inputs; circles/stars are initial/terminal centers. Colors and group numbers do not match between methods. The full-dimensional statistics are seed-wise relative changes averaged over three training seeds; bands show min/max, not confidence intervals.

## Conclusion

| Method | W change at 512 | B change at 512 | B/W change |
|---|---:|---:|---:|
| gmm | -0.99% | -4.80% | -3.84% |
| kmeans | -0.90% | -4.71% | -3.84% |
| sae | -3.38% | +14.46% | +18.46% |

Direct observation: fixed initial SAE soft groups exhibit decreasing W and increasing B, while both W and B decrease for the two geometric partitions. This is a description of one model trajectory through different grouping rules, not a comparison of three trained models or evidence of SAE-caused improvement.

![Common centers](figures/0911_common_centers.png)

Read: compare circle-to-star motion on identical coordinates. SAE now has eight valid empirical centers; overlapping positions are retained faithfully.

![Full-dimensional scatter](figures/0911_common_variance.png)

Read: W below zero means tightening under the specified initial membership; B above zero means greater dispersion of its centers. The result is specific to this answer-position panel and unit-normalized inputs. It does not contradict earlier results using different panels, hard labels, or changing assignments by itself.

Evidence: [108 measurement rows](tables/native_soft/geometry.csv), [hashes, fit parity and identity checks](tables/native_soft/receipt.json). Source inputs, producer SHA and output hashes are in the receipt; raw membership/center arrays remain in the execution workspace under `meeting_v2/variance_trajectory/native_soft/weights_centers.npz`. Producer: sibling `native_soft.py`. Maximum W+B identity residual: 4.440892098500626e-16.

AI suggested next decision: inspect representative texts and the activation features shared across SAE groups to determine whether close centers reflect interpretable cross-cutting features or non-discriminative group mass. Redirect from semantic naming if representative content does not support it. Neither the projected centers nor W/B alone resolves teacher learnability, expert utility, router imitation, or end-task gains.

This addendum supersedes the earlier all-hard-label figures only for the requested native-soft comparison. Earlier hard-label figures remain distinct diagnostics; the trained/changing-SAE grid continues to involve both membership and input changes and must not be read as this fixed-membership trajectory.
