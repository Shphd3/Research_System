# Frequency-priority dispatch: tighter feature lists, concentrated actual inputs

[Detailed record](detailed.md) · [User Anchor](design/anchor_cn.md) · [Frozen Protocol](protocol.md) · [Figures and terms](figures_cn.md) · [184 text cards](text_cases_cn.md) · [Single next question](next_decision.md)

**The tested operations did not solve actual reception of low-frequency targets.** With the original scoring rule, grouping by log frequency and regrouping after excluding exactly the ten most frequent features still sent almost every input to one expert. Co-activation adjustment increased its list-level relation objective but changed no input's actual destination. The AI recommendation is to clarify what expert scores should compare before testing calibration. No new scoring rule, expert training, learning benefit, or capacity benefit was tested.

## Purpose and necessary definitions

Can changes to routing candidates and feature lists, with the original representations and activations held fixed, improve reception of the fixed low-frequency features by their assigned experts and reduce their actual within-expert frequency gap relative to accompanying head features? An assigned expert is specified by a feature list. Actual top-1 routing sends one complete representation to one expert per position. Reception rate a uses positions containing the feature as its denominator; within-expert frequency q uses all positions received by that expert. Empty experts have q=NA.

We reused the same frozen Qwen3-0.6B Base/final 14-selected-layer CrossCoder cache: 130,712 TRAIN and 65,402 EVAL positions, a reliable pool of 9,615 features, and a fixed low-frequency target set L of 964. T10 contains exactly the ten highest TRAIN-frequency features in that pool; **it is not the original top-decile list C of 962 features**. Other high-frequency candidates remain after excluding T10, and complete inputs still carry T10.

## Three findings

**1. Tighter list frequencies did not produce better reception.** O is the original eight linear equal-width groups; F uses eight log-frequency K-means groups on the full reliable pool; T excludes T10 and repeats that grouping method. F sent every EVAL position to expert 7. T sent one position to expert 0 and 65,401 to expert 7; 960 of 964 low-frequency targets still had zero assigned reception.

|EVAL strategy|Equal-feature mean low-target reception|Zero-reception low targets|B≤2 out of all 964 targets|B finite / ∞ / NA|
|---|---:|---:|---:|---|
|O: original linear groups|0%|964|0%|0 / 0 / 964|
|F: log-frequency groups|0%|964|0%|0 / 0 / 964|
|T: exclude ten and regroup|0.002307%|960|0.4149%|4 / 960 / 0|
|Tφ: relation adjustment|0.002307%|960|0.4149%|4 / 958 / 2|
|Random 11|16.6280%|31|4.5643%|933 / 31 / 0|
|Random 22|17.4438%|20|5.7054%|944 / 20 / 0|
|Random 33|17.7257%|26|4.4606%|938 / 26 / 0|

B is the average positive log10 frequency advantage of T10 over a target within its assigned expert; smaller values indicate a smaller gap. B≤2 is a predetermined descriptive threshold, not a learning qualification. T's four finite values, all B=0, come from **the same single received position**. Their finite mean does not establish broad improvement. Sources: [summary table](tables/core_summary.json), [individual low targets](tables/low_target_metrics.csv).

![Reception and actual head-frequency gap](figures/figureC2_low_target_outcomes.png)

Figure C2 separates zero reception, reception distributions, B rates using the fixed denominator of 964, and NA/infinite states. Random lists increased reception, but most targets retained a large head-frequency advantage. They cannot be declared the overall winner or evidence of better learning.

**2. A higher relation objective did not add actual dispatch value.** Tφ retained T's candidates and eight group sizes. Under a maximum 5% increase in list-frequency dispersion, 489 positive-φ-guided swaps left 175 features in different groups. Within-group normalized edge weight rose from 1098.951 to 1221.536, and dispersion increased by 4.99966%. Nevertheless, TRAIN and EVAL top-1 destinations were identical to T at every position. Two low targets moved to an empty assigned expert, changing ∞ to NA; they already had zero reception and did not lose positive reception. See [swap and provenance record](tables/relation_summary.json).

![Separate relation construction from actual dispatch](figures/figureD_relation_increment.png)

Figure D's upper panels measure list construction; its lower panels measure actual reception and frequency gaps. Improving the former did not improve the latter. This result is limited to the fixed graph, tolerance, swap heuristic, score, and window; it does not reject every relation-based organization method.

**3. A missing branch asset did not block the main comparisons.** O/F/T/Tφ and three random lists were evaluated on both splits, with 200 descriptive context-block bootstrap replicates, 19 figures, and 184 actual-hit text cards. The first-singular-direction branch P is NOT RUN: the original preprocessed 14-layer joint input H at these positions is missing. Final-layer hidden states cannot substitute for it. See the [completion matrix](detailed.md).

## Updated understanding and one next question

The intuition that frequency-near lists plus removal of a few head features might enable low-frequency specialization is now narrower: **tighter lists and more within-group co-activation do not ensure that the original mean-over-members score gives low targets routing opportunities.** The evidence favors studying what scores compare, rather than expanding the deletion count or scanning relation tolerances.

AI recommendation: retain the present candidates and lists, then preregister one TRAIN-frozen score-calibration comparison that jointly checks low-target reception, head-frequency gaps, and costs to other targets. Its formula, required reception, and budget remain for discussion; it was not executed here. EVAL had already been viewed and document independence is unknown. These are exploratory holdout checks in this window. Improved reception would not by itself establish learning or capacity benefits.
