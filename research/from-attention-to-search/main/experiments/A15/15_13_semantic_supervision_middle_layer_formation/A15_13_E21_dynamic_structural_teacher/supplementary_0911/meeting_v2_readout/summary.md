# Meeting v2 readout: SAE classification geometry and evolution

Status: **COMPUTED / POST-HOC / BOUNDED**. Interpretation: **AI_DRAFT_AWAITING_HUMAN_CONFIRMATION**. Processing agent: Codex. This is the researcher-requested visualization follow-up, not a new training experiment or a closure of parent E21. [Detailed](detailed.md); [prior supplement](../summary.md).

## Purpose

Make the distinction between model-geometry evolution and SAE-induced reclassification visible, including ordinary-node and historical high-node readouts and the already-trained changing SAE.

## Hypothesis

The researcher's latest clarification fixes the input-point positions in the hypothesis illustration: initially mixed assignments should become organized and meaningful over training. Geometric tightening is not required by this clarified intuition; the geometry curve remains a separate diagnostic. The rival is that changing encoders, grouping or coverage changes the observed classes without establishing useful semantic structure.

## Analysis method

- Read existing unified held-out replays and sparse codes for the same dynamic-SAE model trajectory, three training seeds and six times. Compute original ordinary-node targets and existing high28 targets with the fixed encoder; use saved refreshed ordinary-node targets for the adaptive readout.
- Freeze t0 hard teacher labels and covered cohorts, then measure full-dimensional unit-h within/between dispersion. Separately display current hard classifications in one t0-fitted projection and track label retention with group-name alignment.
- Replot prior cross-record relation-drift and reconstruction metrics; show the historical four SAE refresh points. No new main-model training, SAE training, graph fitting or semantic annotation.

## Conclusion

1. **The fixed ordinary-SAE classification has increased relative geometric separation on this trajectory.** Mean seed-wise t0→512 changes: within dispersion **−3.604%**, between dispersion **+20.939%**, between/within ratio **+25.468%**. This updates any blanket description that all within-class dispersion increased. Earlier K-means/GMM numbers used another arm, position panel and label definition, and remain distinct observations; their difference cannot be attributed solely to clustering algorithm. [Source table](tables/readout_metrics.csv).
2. **Fixed and refreshed readouts give visibly different classification trajectories on identical h.** At512, weighted label retention after alignment is **95.997% fixed** (95.863–96.185%) versus **59.020% refreshed** (58.102–60.807%). These are descriptive, class-imbalance-sensitive values, not semantic accuracies. The relation-drift readout remains **0.0534 vs0.3527** and reconstruction residual/current-h variance remains **0.3374 vs0.1078**, as recorded in the [prior supplement](../summary.md).
3. **The high28 readout is a narrow-coverage comparison.** At t0 it covers **82/1247 positions**, weighted **4.865%**, and its covered-cohort between/within ratio changes **−2.390%** by512. It cannot be ranked against the all-covered ordinary readout as if the cohorts were identical. Ordinary grouping is not leaf-only; high28 selects historical depth≥2 atoms and is not an established semantic-parent classifier. No refreshed high28 hierarchy was trained or reconstructed here.

4. **Matched readouts of the same trajectory give different geometry trends.** A subsequently requested common-panel comparison fits K-Means and diagonal GMM at t0 on the SAME1247unit-h positions used by the SAE readout, then fixes each method's initial memberships. Mean seed-wise final W/B changes are **−0.899%/−4.710% K-Means**, **−0.994%/−4.796% GMM**, and **−3.604%/+20.939% SAE**. This isolates the descriptive effect of choosing these labelings on the same states, not semantic superiority or an intervention on training. [Matched table](tables/variance_trajectory/geometry.csv), [setup and validation](detailed.md#8-matched-k-means-gmm-sae-variance-and-centroid-follow-up).

![Matched within and between variance](figures/0911_v2_variance_comparison.png)

Left is W, right B; each is percent change from that method's initial value. Same states/panel/weights for all methods; fixed memberships over time. Small shaded ranges are training-seed min–max, not solver-repeat uncertainty. Stars and trajectories are available in the revised meeting report; each center is a weighted membership centroid, not a GMM parameter mean.

![SAE trajectories](figures/0911_v2_fig2a_curves.png)

Read A as fixed-membership geometry, B as changing pairwise classification relationships, and C as reconstruction adaptation. Shading is min–max of three training seeds, not a confidence interval. All comparisons in this figure use the same dynamic-model trajectory per seed; the two A curves have different covered cohorts.

![Classification evolution](figures/0911_v2_fig2b_clusters.png)

Read across time, then across readouts. Positions are identical across rows at each time; current class colors differ. Gray positions are unclassified by high28. Projection explains34.37% of t0 variance and is illustrative; it cannot adjudicate full-dimensional semantic separation.

**Boundary:** this establishes readout behavior, not useful semantic classes, expert utility, task gain or necessity of adaptation. Historical dynamic-source and t0-extraction limitations in the parent supplement remain. Fixed K8 does not reveal natural class birth. The refreshed ordinary SAE is the existing four-refresh training output; it is not a new online high-node hierarchy.

**AI proposed next decision:** under a common co-occurrence rule, track one independently interpretable operation relation with fixed versus refreshed readouts, including ordinary unsupervised routing as a reference. Close this comparison by deciding whether refresh restores that relation, fixed readout already retains it, or both chiefly follow format. No new training scope is authorized by this proposal.
