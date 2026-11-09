# A14_E05 Summary: Same Tokens Do Not Support a Model-General Gold-Split Advantage

## Direct Result

**Registered verdict: insufficient.** Qwen's gold split did not beat the
same-parent, same-token alternative: relative advantage was **-0.0415**, with
sentence-cluster 95% interval **[-0.1079, 0.0213]**. The upper endpoint is
below the registered 5% effect threshold. Pythia pointed in the opposite
direction, with advantage **+0.1486** and interval **[0.1308, 0.1645]**.

No validation-eligible Qwen point combined a 5% split advantage with a
non-vacuous generic bound. Its minimum eligible bound ratio was **1.3369**.

![Same-parent split and prediction-stability results](prediction_stability_frontier.png)

## Hypothesis Updates

| Hypothesis | Direct result | Registered update |
| --- | ---: | --- |
| H1 shared-space approximation | Qwen gold error 0.5381 $<0.90$ | pass |
| H2 gold-split specificity | -0.0415, interval [-0.1079, 0.0213] | insufficient; 5% effect not supported |
| H3 ordered versus mean, secondary | +0.0698, interval [0.0339, 0.1069] | pass, but probe capacity remains a rival |
| H4 prediction--stability compatibility | 0 compatible points; minimum bound 1.3369 | fail |
| H5 Qwen learning increment | +0.0574 over initialization | numeric pass, but it cannot rescue failed H2 |

## Interpretation

The strict leaf space is descriptively strong in Qwen: 24 of 896 directions
retain 95% of centered training-leaf energy, and held-out parent variation has
only 5.82% energy outside that space. Yet the gold shared operator leaves
53.81% of centered parent energy unexplained, while an alternative split fitted
on the same parent tokens leaves only 51.67% unexplained. Shared subspace
alignment therefore does not imply the registered gold composition law.

Pythia cannot establish a general result because the control selected a
right-shifted alternative in 84.3% of cases. A post-hoc boundary audit found
Pythia advantage +19.97% for right shifts but -14.26% for left shifts. This
direction reversal motivated the pre-execution E06 two-sided protocol; the
audit only narrowed the claim and did not upgrade H2.

## Conclusion

Holding parent content fixed removes the large lexical-containment shortcut
from E03/E04. Under this cleaner control, Qwen provides no gold-split advantage,
Pythia is direction-sensitive, and the recursive norm bound remains vacuous.
E05 therefore does not support a model-general stable shared-linear
composition mechanism.

## Resolved Next Decision

Run the [two-sided direction-balanced robustness test](../../boundary/A14_E06_two_sided_split_robustness/summary.md)
before interpreting Pythia's positive aggregate.
