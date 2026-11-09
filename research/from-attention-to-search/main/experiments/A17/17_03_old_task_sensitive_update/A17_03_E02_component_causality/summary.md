# A17_03_E02: Causal contrasts for deleting and amplifying update components

[中文](summary_cn.md) · [Detailed evidence](detailed.md) · [Protocol](protocol.md)

All 630 Full interventions, 140 Smoke cells and four independent-process replays completed. Independent engineering audit passed. The interpretation below is **AI_PROPOSAL**; researcher mechanism judgment and question closure remain Unknown.

## 1. Purpose

The earlier restricted strategy removed 16 estimated old-CE-sensitive directions and amplified the remainder, yielding larger final new-task CE gains. Did deleting a harmful component cause that advantage, or did redistributing update length do so? This determines whether old sensitivity can be interpreted as an obstacle to new learning and informs the parent question about useful shared updates.

## 2. Model

Restore six Qwen3-0.6B Base states after learning the old FIRST/LAST rule. Perturb only the final Attention o_proj. At each state, fix three new-rule source batches and independently apply the full update, its sensitive component, its unamplified complement, and its complement amplified to the full update norm. Every intervention starts from the same saved state. The primary scale is one original SGD step. Evaluation uses 400 exposed development lists, each paired across the two rules.

New-CE deletion gain is full-update loss minus unamplified-complement loss; amplification gain is unamplified minus amplified-complement loss. Positive values lower new CE. Old margin compares the correct answer against the opposite-rule answer; full-vocabulary accuracy is separate. CE exactly splits into probability assigned to the answer pair and selection within it, without implying separate parameter functions.

## 3. Hypotheses

H1 proposes that deletion itself benefits new development CE, with amplification adding benefit. The strongest rival is that deletion first removes useful learning and amplification then compensates. Holding the state, source gradient and unamplified remainder fixed distinguishes these accounts. H2 proposes that increased rule-prompt response can be outweighed by a larger shift toward the new answer, harming some old selections; this requires per-list evidence.

## 4. Conclusion

**The immediate advantage does not support deleting a component harmful to new CE.** After averaging three source batches within each case, deletion gains are negative in all six cases and amplification gains positive in all six. Equal-weight pooled gains are −0.000353638 for deletion, +0.000589189 for amplification and +0.000235550 nat/answer overall. Deletion sacrifices useful new learning; amplifying the remainder compensates and on average exceeds that sacrifice. [Primary comparison table](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/primary_order_effects.csv)

| Order / 顺序 | New CE deletion gain | Amplification gain | Total gain | Old accuracy out_norm−full (pp) |
| --- | --- | --- | --- | --- |
| FIRST_to_LAST | -0.000262227 | +0.000457506 | +0.000195279 | +0.055556 |
| LAST_to_FIRST | -0.000445049 | +0.000720871 | +0.000275821 | +0.138889 |

Total gain is positive in four cases and negative in two; one negative value is only −0.000002300, close to cancellation. The strategy is not uniformly better. Across 18 fixed source batches, deletion has 2 positive/16 negative gains, amplification 18 positive gains, and total gain 12 positive/6 negative. Six cases do not constitute six independent seeds.

**The immediate new-CE advantage does not reproduce the additional long-run old-accuracy cost.** Here amplified-complement old accuracy exceeds full-update accuracy by 0.097222 percentage points, averaging both orders, whereas the original 100-step restricted strategy had lower old accuracy. These measurements identify initial-state deletion/amplification effects but do not explain the entire accuracy trajectory. [Case results](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/primary_case_effects.csv)

## 5. Analysis

The sensitive component alone lowers old CE by 0.000234727 and new CE by 0.000370856 on average. It is therefore not an identified conflict function. Redistributing a fixed update norm changes development outcomes; the complement remains sensitive to the old task, and neither subspace has been identified as a shared or unique module. [Seven-direction readouts](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/metric_changes.csv)

Source fit and development outcomes differ: full updates reduce their source-20 CE by 0.013797487, versus 0.009466609 for amplified complements; new-dev reductions are respectively 0.001678487 and 0.001914037. The ordinary gradient's maximal first-order source descent remains valid. Better development CE is not faster source fitting. [Source derivatives and finite effects](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/source_analytic_first_order.csv)

Mean margin does not determine mean selection loss. Amplified complements have higher old mean margin than full updates, yet old pair-selection CE is worse by 0.000027736 and 0.000146847 in the two orders. Selection loss is nonlinear in margin. Across 7,200 repeated list/update instances, 6,812 show increased rule response but only 1,037 improve both margins; full updates improve both in 371 instances. In 3,117 amplified-complement instances, increased rule response is outweighed by a larger new-answer shift. These are 18 updates evaluated on 400 lists, not independent samples. [Per-list coordinates](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/paired_coordinates.csv)

At the primary scale, median source-CE first-order remainder/effect ratios are about 1.00% for full and 0.44% for amplified-complement updates. Development central-difference extrapolation has a median 16.66% and maximum 80.86% error relative to the smaller total-advantage contrast. An approximation accurate for a large loss change need not explain a smaller contrast. [Remainder details](detailed.md)

The first source batch is linked numerically to E01's actual first step: across 12 conditions, the largest common-readout difference is 1.14e−5, with no accuracy disagreements. Later saved checkpoints provide post-hoc trajectory context, not a decomposition of later states and gradients. The bounded update is that **old sensitivity does not mean harmful new learning; deletion and amplification require separate tests, and help depends on the predictive requirement measured**. The remaining researcher decision is whether to focus next on why old-error repair declines over the trajectory; local CE gains do not settle that question.
