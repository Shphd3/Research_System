# A13_00_04_E01 Summary

## Direct Result

**Pass:** changing only the relay-position auxiliary target from fixed
`[ANSWER]` to answer value \(A\) improved the ordinary head, and the benefit was
substantially larger when the relay was structurally necessary.

\[
\bar D_{\mathrm{relay}}=1.0343\ \text{nats},
\qquad
95\%\ \text{bootstrap interval }[0.4052,2.0866],
\]

\[
\bar\Delta_D=0.8747\ \text{nats},
\qquad
95\%\ \text{bootstrap interval }[0.2309,1.8964].
\]

\(D_{\mathrm{relay}}\) was positive in 8/8 seeds and the interaction was
positive in 7/8, meeting every registered primary criterion.

![One-label localization learning curves](figures/objective_learning_curves.png)

![One-label localization effects](figures/relay_interaction.png)

## Intuitive Reading

On the relay path, answer-aligned supervision reached 90% held-out accuracy at
a median 90 steps; the fixed-marker control required a median 340 steps among
seeds that crossed the threshold. On the bypass path the medians were 70 and
130 steps.

Thus most of the difference is localized to whether the state that must carry
\(A\) is directly trained toward \(A\), not to the other four all-position
Next-2 targets.

## Capability And Use

Answer-aligned MTP reached final 1.0 accuracy and donor follow 1.0 in all eight
relay seeds. The fixed-marker control reached the 0.90 capability threshold in
6/8 seeds; every eligible control model also had donor follow 1.0.

Arm instability is reported as an objective outcome and was not used to remove
paired observations.

## Remaining Confound

Fixed `[ANSWER]` and variable \(A\) differ in marginal target diversity. The
pass localizes the effect to one relay label but does not yet prove that
downstream answer relevance, rather than any variable-valued target, is the
cause.

## Next Decision

Replace the fixed control with same-vocabulary, same-frequency, equally
predictable nuisance value \(B\) and test \(B\) versus answer value \(A\) on new
paired seeds.
