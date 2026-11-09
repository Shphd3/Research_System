# Reading the four figures

[中文](figures_cn.md). All figures read saved tables; no new activation extraction or training. Each has PNG, scalable SVG and PDF versions. [Payload/source manifest](payload_manifest.json).

## Figure 1: actual reception and designated-target zero reception

![Actual reception](figures/figure1_actual_reception.png)

The upper row plots expert ID against the percentage of all valid TRAIN inputs reaching it. The lower row plots the percentage of each expert's member features with no hits reaching their designated expert. “Original” is the original route. “C score terms zero” virtually removes frequent C terms from the score; input representations do not change. A/B1/B2 use their own membership/routes, and matching expert IDs do not mean matching semantics.

Look for A's concentrated load, three empty experts, and the degenerate move of all inputs to expert 0 after C removal. Nonempty/balanced allocation is not evidence of learning, and C removal is not a validated strategy. The two rows have different denominators.

Sources: execution-side `metrics/score/expert_loads_original_and_C_zero.csv` and `feature_owner_original_and_C_zero.csv`, split=TRAIN by rule/expert. N=130,712; membership pool=9,615. [Expert table](tables/expert_summary.csv).

## Figure 2: global versus designated-expert frequency

![Global versus within-owner frequency](figures/figure2_global_vs_owner_frequency.png)

“Global activation frequency p” is feature occurrence over all valid positions. “Frequency inside assigned expert q” is its occurrence among inputs reaching its designated expert. Both axes use linear percentages. “Assigned” means membership-designated, not largest actual receiver. “Low-frequency” denotes the frozen 964 targets; “Other” denotes the remaining reliable features. The q=p dashed line marks no enrichment relative to global frequency.

A has 55 defined owner q values, including 30 real zeros; the other 9,560 are NA because the owner is empty and are not fabricated as zero scatter points. B still has low/zero q for many rare targets. NA does not establish uselessness, and larger q does not establish improved prediction learning.

Source: execution-side `metrics/core/feature_owner_summary.csv`; split/rule facets, p_i versus owner_q, with owner_q_NA_reason. Every panel retains the same 9,615-feature scope; TRAIN N=130,712, EVAL N=65,402.

## Figure 3: targets and frequent companions inside actual expert inputs

![Targets and companions](figures/figure3_target_common.png)

Each row is a frozen target; U is that target and C:ID is a companion from the original high-frequency list. C is not universal semantics, a principal component or noise. Three C members per target were selected by TRAIN P(c|i). The vertical axis is EVAL within-expert frequency q (%); N_e is received positions and n_U is the target's total EVAL support.

“Assigned” means designated expert; “Most receiving” means the expert receiving the most target hits. A's left panel is empty owner 0, so all q are NA. The second panel is its main receiving expert 7, not a newly designated owner. B uses each original membership. Different expert denominators prevent interpreting bar heights directly as learning comparisons.

Read how frequent target and companions are after routing, and why an empty expert has no estimable q. Do not infer that common must be removed, equal frequency is optimal, or a few cases represent every feature.

Source: [108-row plot table](tables/case_common_plot_source.csv), fields expert_role, expert, N_expert, n_expert_i/n_expert_c and q_i/q_c; TRAIN selection record remains execution-side at `metrics/cases/case_common_plot_selection_train.json`. Target EVAL supports are 162, 145 and 111, with expert denominators shown.

## Figure 4: text positions and original scores

![Text and scoring](figures/figure4_text_and_score.png)

Each column uses the first frozen random hit for one ID. “Prefix” is a shortened display of the model-visible prefix; “Current token” is the current input token. “Next target” is the next-token label, used for interpretation only, not current routing. “Group/expert” is the original membership ID. “Original score” is decoder-norm-weighted mean activation using the original denominator, not a probability. “Assigned” marks the target's owner; “Winner” marks the highest score and actual destination.

The target is active, yet A0 scores far below A7 and the full input goes to A7. This does not imply that the model saw the next label, the target is useless, or a single word exhausts the feature's meaning.

Sources: execution-side `texts/text_cases.json`, `metrics/cases/text_case_scores.csv` and `text_sampling.json`. [All 12 cards](text_cases_cn.md) retain prefixes, source bins, positions, group scores, companions and individual-U score-removal checks.

## Consistent terms

A feature is one fixed shared CrossCoder coordinate, not certified knowledge. The designated expert comes from its membership list; the actual receiver gets the complete current input. Global p, conditional destination share a, expert load and within-expert q have different denominators. NA is undefined/missing, not zero. C is the original TRAIN high-frequency list of 962 members, not “present in every input.” U is a case target. TRAIN/EVAL are the fixed training and held-out-position sides; 1024-token contexts are not verified independent documents.
