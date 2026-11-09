# A13_00_03_E02 Summary

## Direct Result

**Formal verdict: insufficient again, for a different reason.** On eight fresh
paired seeds, the candidate effects independently repeated and were positive
in 8/8 seeds:

\[
\bar U_{\mathrm{relay}}=1.4703\ \text{nats},
\qquad
95\%\ \text{bootstrap interval }[0.9957,2.0099],
\]

\[
\bar\Delta_{\mathrm{relay}}=1.3901\ \text{nats},
\qquad
95\%\ \text{bootstrap interval }[0.8996,1.9553].
\]

But relay shared-aux final capability passed in only 5/8 seeds, below the
registered 7/8 requirement. Therefore E02 does not promote the parent anchor
to pass.

![Independent-confirmation learning curves](figures/objective_learning_curves.png)

![Independent-confirmation paired effects](figures/relay_interaction.png)

## Gate Reading

- NTP: 7/8 capability-eligible relay seeds; donor follow was 1.0 among all
  seven.
- shared-aux: only 5/8 capability-eligible relay seeds; donor follow was 1.0
  among all five.
- informative Next-2: 8/8 capability-eligible relay seeds; donor follow was
  1.0 among all eight.
- Every bypass condition reached 1.0 mean accuracy.

The failed shared-aux arm is not evidence that the NTP carrier is invalid. It
is a result after the auxiliary treatment was applied.

## Recognition Update

Across E01 and E02, the full-objective utility and relay interaction have the
expected sign in 16/16 paired seeds, while Next-2 relay capability is 16/16.
The matched shared-aux target is substantially less stable.

This reveals a design error in the original Stage-1 gate: requiring every
treatment arm to be capable conditions the analysis on a post-treatment
outcome and can remove the very objective harm/benefit being measured.

## Next Decision

Keep both original verdicts as insufficient. On new seeds, change only the
relay-position auxiliary label while fixing the other four Next-2 targets;
treat arm capability as an outcome and directly localize whether the
answer-aligned relay target causes the performance interaction.
