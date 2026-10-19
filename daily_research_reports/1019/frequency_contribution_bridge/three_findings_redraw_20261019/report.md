# Three findings: list size, relation groups and regional learning benefit

The redrawn evidence answers three questions. List size does not represent input contribution. Additional co-occurrence in some frequency bands has not yielded two stable substantial groups. The receiving regions of old T_S1 do not all benefit.

Figures 1 and 2 are NEW dispatch analysis (20261019T025630Z), with no training. Figure 3 uses OLD T_S1 epoch-one checkpoints, seeds 11/22, 168 updates and 85,548 answer-target exposures. The old expert IDs are not the new bands or subgroups. EVAL contains 256 previously inspected dialogues and 22,446 answer predictions. Claims remain exploratory.

## Figure 1: does list size represent input contribution?

![Aligned count and contribution panels](figures/figure1_feature_count_vs_contribution.png)

Observation: bands 1–4 contain 1,694 / 5,673 / 7,013 / 1,097 features, whereas their mean EVAL contribution shares are 0.108% / 2.198% / 31.275% / 66.419%. The 907 TRAIN-zero features remain separate; their 0.001185% EVAL share stays in the denominator. The top and bottom panels share the band axis and have separate labeled y axes; there is no dual axis.

Allowed conclusion: membership counts do not represent the contribution scalar on these inputs. Contribution equals activation times final-layer decoder-vector norm, summed within band and divided by the total across all 16,384 features at each position, then averaged across EVAL positions. This is not information, knowledge, gradient interference, learning value or capacity; it does not measure vector cancellation or reconstruction residual.

Design implication (AI suggestion): report list counts and actual contribution separately, and state whether dispatch uses total contribution, group means or TRAIN-baseline calibration. Equal membership alone does not establish balanced contribution.

Source: [figure data](tables/figure1_feature_counts_contribution.csv). Means use EVAL, not the TRAIN means in the membership source table. No uncomputed uncertainty is displayed.

## Figure 2: is extra relation enough for stable grouping?

![Heldout within-group phi](figures/figure2a_heldout_phi_vs_matched_random.png)

Observation: relation-group heldout signed phi exceeds all 20 frequency-matched random results in bands 1 and 3. Band 3 is 0.00511779 versus random mean 0.00240052. Gray segments show the min–max range over seeds 11–30, not confidence intervals. Random lists preserve subgroup sizes within ten finer frequency strata per band. Values aggregate estimable unordered within-subgroup feature pairs; constant-feature pairs are excluded with their counts retained. The singleton in band 4 has phi=NA, not zero; its band aggregate comes only from the large subgroup. The right column reports relation minus random mean so small differences remain visible.

Allowed conclusion for Figure 2a: some within-band relations exceed matched frequency statistics. Bands 2/4 allow only 18.97%/1.09% exchangeable members, limiting random-control discrimination. Mean phi alone cannot establish membership stability, update compatibility, learning value or capacity.

Design implication for Figure 2a (AI suggestion): retain relation and matched random comparisons and check membership stability separately before selecting expert lists.

## Figure 2b: are members stable?

![Membership stability](figures/figure2b_membership_stability.png)

Observation: band 3 full-TRAIN sizes 1,861/5,152 change to 7,010/3 and 4,587/2,426 in the two dialogue-hash halves; half-to-half mean matched Jaccard is 0.327. Band 1 full-to-half values are about 0.385. Band 2 has full sizes 5,670/3; band 4 stays at 1,096/1 with Jaccard 1. Rows label full-TRAIN subgroup sizes; cells compare full/halves after choosing the better subgroup-label permutation. The frequency bands remain fixed, so this is conditional membership stability. Half samples contain 45,637/39,911 positions.

Allowed conclusion: membership evidence does not establish two stable substantial groups. Average co-occurrence and membership stability answer different questions. Missing values remain NA; actual zero Jaccard remains zero. Jaccard and group sizes do not measure gradient compatibility, learning value or capacity.

Design implication (AI suggestion): retain this split as candidate organization and inspect band competition, relation and membership stability separately. A forced two-way split does not itself supply two qualified experts. Keep matched random controls; this redraw does not freeze new training lists.

Sources: [phi](tables/figure2a_heldout_phi.csv), [stability and subgroup sizes](tables/figure2b_membership_stability.csv).

## Figure 3: do all receiving regions benefit?

![Old T_S1 regional losses](figures/figure3_old_T_S1_epoch1_expert_DeltaNLL.png)

Observation: only old T_S1 is shown. For experts 1/3 both seeds' intervals are below zero. Expert 0 has an entirely negative interval only in seed 11. Expert 7 worsens in both seeds: +0.01309 [0.00338, 0.02235] and +0.01128 [0.00128, 0.02086]. Several other intervals cross zero. Points and intervals directly reuse the existing 1,000-dialogue-bootstrap 95% descriptive results; no losses or intervals were recomputed.

Allowed conclusion: receiving regions do not all benefit at these old epoch-one checkpoints on this exposed EVAL. Delta NLL is branch-enabled minus branch-disabled NLL, averaged over each expert's natural receiving answer positions, in nats per position. Fixed routes define the same region across seeds; experts/pairs are not independent experimental replicates. Intervals crossing zero leave the direction uncertain. This cannot explain which feature caused the differences or evaluate training of the new dispatch/groups.

Design implication (AI suggestion): future dispatch/training comparisons should retain regional losses and uncertainty and evaluate the new method's own trained states. More reception, co-occurrence or active features cannot substitute for learning evidence or identify gradient interference.

Source: [all 16 plotted rows](tables/figure3_old_T_S1_epoch1_DeltaNLL.csv). Epoch one was selected post hoc and EVAL previously inspected; intervals provide neither independent confirmation nor multiplicity-controlled error guarantees. Original epoch-three results retain their original identity.

## Provenance

The [artifact manifest](artifact_manifest.json) binds exact source tables, code, hashes, checkpoint identities and allowed claims. PNG/PDF/SVG versions share names. This is a presentation redraw using saved statistics; no new training, inference, activation extraction or resampling occurred.
