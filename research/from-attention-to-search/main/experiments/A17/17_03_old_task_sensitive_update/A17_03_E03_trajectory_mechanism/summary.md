# A17_03_E03: Intermediate update effects on old-error repair

[中文](summary_cn.md) · [Detailed](detailed.md) · [Protocol](protocol.md)

Completed: Smoke12/12, independent replay4/4, Full108/108 and independent recomputation. Jobs pt-c1i5f9pl and pt-8aoyrzuw on h100-4-reserved. Mechanism/closure Unknown.

## 1. Purpose

Test whether the immediate component operator at intermediate states can reduce improvement of initially incorrect old predictions, bridging the existing100-step repair disparity with bounded local effects.

## 2. Model

Restore registered Qwen3 Base last-o_proj states at new steps1/16/50, ordinary/protected histories. Keep original rank16 Q, same next20 source batch and ordinary external next-step norm within each paired history. Compare full, out, out_norm independently;36 state/history cases and108 cells, no cumulative retraining. Initially wrong/correct old subsets are fixed from the old endpoint. Paired output coordinates m_new=b+h,m_old=b-h are identities, not internal modules. Exposed dev400 pairs; separate equal panels and full-vocabulary readouts; test closed.

## 3. Hypothesis

Immediate deletion/amplification may reduce old-error selection improvement. Rivals are accumulated state, generic candidate adaptation and other competitors. Within-state contrasts identify the operator; across-history contrasts still jointly include gradient and downstream-state changes.

## 4. Conclusion

The repair gap is already substantial at saved step16:27 ordinary versus6 restricted; at50 it is55 versus18; at100 it is72 versus36. Initially wrong old pair-margin changes at16 are+0.011005 versus−0.010085, and at100+0.021118 versus−0.069114. Across36 state/history cases, out_norm-full initially-wrong mean pair-margin contrasts are negative in24/36. These finite effects do not establish complete trajectory mediation. [Trajectory](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/trajectory/aggregate.json) · [Case contrasts](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/full/case_contrasts.json)

| Saved step | Ordinary repairs | Restricted repairs | Ordinary losses | Restricted losses |
|---|---:|---:|---:|---:|
| 1 | 3 | 2 | 10 | 6 |
| 16 | 27 | 6 | 29 | 23 |
| 50 | 55 | 18 | 49 | 47 |
| 100 | 72 | 36 | 80 | 75 |

| Step | Restored history | Initial-old-error pair-margin contrast | Full-competitor-margin contrast | Net repair-count contrast, case mean |
|---|---|---:|---:|---:|
| 1 | ordinary | -0.000850 | -0.000851 | -1.333 |
| 1 | protected | -0.000885 | -0.000865 | -0.667 |
| 16 | ordinary | -0.000183 | -0.000218 | -0.167 |
| 16 | protected | -0.000441 | -0.000698 | -0.500 |
| 50 | ordinary | -0.001535 | -0.001228 | +0.333 |
| 50 | protected | -0.002458 | -0.001982 | -0.667 |



**Order/state heterogeneity is material.** Equal-history averages of out_norm−full initially-wrong pair-margin contrast:

| Saved step | FIRST→LAST | LAST→FIRST |
|---|---:|---:|
| 1 | +0.000686 | -0.002421 |
| 16 | +0.001492 | -0.002116 |
| 50 | -0.004601 | +0.000608 |

Negative means less pair-margin improvement under restriction, positive means more. Signs differ by order and step. This is not stable bidirectional harm. At step50 ordinary history, out_norm has two more net repairs across cases despite lower mean margins. No complete100-step mediation is established.

## 5. Analysis

The finite table compares each operator from the identical state. Norm matching removes simple step-size difference between full and out_norm; out separately retains deletion cost. Full/out_norm source CE improves in36/36 and36/36 states. Different steps use different source batches; histories at the same step use the same source. Separate orders/panels and all records are in metric_changes.json. Only three independent training seeds; repeated states/lists are not independent replicates. No new significance or blind-confirmation claim.

At100, initially wrong restricted old CE changes+0.005964 versus ordinary−0.055532 in equal-case means, while the old overall CE still improves. Restricted pair-access changes−0.052768 and pair-selection+0.058732: probability mass can improve while within-pair choice worsens. This is output accounting, not causal module partition. Full trajectory mediation, rule algorithms, expert benefit and natural-task generalization remain unestablished. Round-two tasks were not executed.


A measured illustrative counterfactual: seed29 FIRST→LAST, ordinary saved step16, old FIRST list [红,鱼,虎]. Before update the prediction is鱼; full repairs it to红; out_norm remains鱼. Correct probabilities are0.428907/0.432827/0.429462 and competing middle-word probabilities0.433871/0.431740/0.433798. Both improve correct CE but only full changes argmax. The competitor is the middle word, showing the limit of endpoint-pair margins. [Native records](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/full/example_lost_repair.json). Selected after results for illustration, not new independent evidence.
