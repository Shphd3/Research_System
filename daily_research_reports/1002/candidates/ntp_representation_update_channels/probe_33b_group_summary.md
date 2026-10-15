# Frozen 33B policies retain within-group matching, while fixed common remains better

2026-10-04. [中文](probe_33b_group_summary_cn.md) · [Detailed record](probe_33b_group_detailed.md). Owner: [Anchor](anchor.md). Contract: [frozen Protocol, 16:43 UTC addendum](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/second_window_20261004/group_decomposition_protocol.md). Execution is complete. This is post-hoc analysis on previously exposed DEV; researcher scientific judgment, practical thresholds and the next decision remain `Unknown`.

## 1. Purpose

The original policy chooses measured matrix increments. Its frozen candidate library contains four domain directions and the pooled raw-gradient common direction, with a separate set allowing zero update. FIT-fixed selection uses one candidate everywhere on DEV, here common. Globally usage-matched random allocation retains total candidate proportions but removes input correspondence. This note asks whether gain remains when domain/category-specific proportions are also retained.

Determine whether the original policies' gains over globally usage-matched random allocation remain after preserving action frequencies within receiving domains or categories.

## 2. Hypothesis

The policies may match actions to individual events beyond those coarse groups. The rival is that their global-random gain is explained entirely by different action frequencies between groups. Neither explanation implies that the policy beats the strong fixed common action.

## 3. Analysis Method

Here an action remains a measured, scaled matrix increment: four domain directions and one pooled raw-gradient direction, with a separate set permitting zero update. Candidates and predictors are frozen; each DEV position chooses one increment and reads its previously measured finite CE. No new experts are trained. FIT chooses a single candidate for all positions, here the common update. A/B identify source banks; FIT/DEV identify fitting/evaluation roles.

Why add a within-group control? Global random allocation preserves total candidate frequencies but destroys domain–choice association. Reallocate choices only within the same recipient domain or category to retain that association and each group's counts, removing only within-group input–choice matching. If the residual vanishes, coarse composition remains credible; a strictly positive residual interval shows that these labels do not exhaust matching. Either outcome still needs the FIT-fixed comparison to assess adoption utility.

- Retain all original Dense, fresh-S7 and SALL policies at 33 billion cumulative training tokens: 92 frozen policies, each evaluated on both source banks, for 184 pooled conditions. Preserve all feature families, same-source and cross-source directions, and both action sets. No model is fit or run again.
- Read the original finite action costs on 1,024 DEV records, with 16 events per record. The domain control randomly reallocates the policy's own choices within four receiving domains; the category control does so within eight categories. Their expected costs are calculated exactly. These explanatory labels are not a tested deployment-time routing input.
- Global-random gain equals the global-to-group control difference plus the residual gain over within-group random allocation. Positive residual means lower policy cost than that control. Gains use micro-nats per event. Reuse the original 2,000 category-stratified paired whole-record bootstrap samples; recompute group frequencies and action means inside each sample. Conditional 95% intervals neither include refitting nor correct for multiple comparisons.

## 4. Conclusion

1. **The global-random gain is not exhausted by these four domains or eight categories on this panel.** All 184 domain-residual intervals and all 184 category-residual intervals are positive, including all 92 cross-source conditions. The table retains every model; values are ranges of condition-level point estimates, not pooled intervals.

| Model | Cross-source conditions | Within-domain gain | Within-category gain | Gain over fixed common |
|---|---:|---:|---:|---:|
| Dense | 28 | +95.12 to +332.59 | +93.34 to +332.36 | -504.84 to -198.21 |
| fresh S7 | 32 | +186.84 to +667.78 | +186.51 to +670.21 | -807.31 to -345.56 |
| SALL | 32 | +124.60 to +387.50 | +124.05 to +391.36 | -514.85 to -191.92 |

   The within-group columns average over groups within each condition; they do not assert a positive result in every individual group. Every displayed residual's corresponding condition-level interval is positive, while every fixed-common interval is negative. [Complete 184 × 13 matrix](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/probe_33b_group_decomposition_20261004/summary.csv)

2. **Finer labels add no consistently resolved control difference here.** The global-to-domain component has 184 positive intervals; the global-to-category component has 183 positive intervals and one interval spanning zero. The domain-to-category component spans zero in all 184 conditions. This last result is not evidence of equivalence, and it does not mean the positive within-category residual is zero. A negative residual would indicate worse selection than its group control; no such interval occurs in this matrix.

3. **AI interpretation (`AI_PROPOSAL`): these policies use matching information beyond the named coarse labels, but that information still does not justify replacing fixed common.** All 184 fixed-common gain intervals remain negative. Group controls preserve each policy's action mixture, whose mean cost can already exceed common. Numerical decomposition does not identify a unique representation mechanism, show semantic dispatch, or test a deployable label-aware router.

Independent raw-array recomputation checked every mean, interval endpoint, bootstrap value and per-record value without importing the producer or helper. The largest interval-endpoint discrepancy was 8.67 × 10⁻¹⁹ nats. [Independent audit](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/group_decomposition_independent_audit.md)

The conditions share models, records, fits and source banks. They are not independent replications; old cached-panel outcomes must not be substituted for this 33B panel. This post-hoc analysis does not test joint router/expert training, future learning or retention. [Full lineage and boundaries](probe_33b_group_detailed.md)
