# A13_00_02_E02 Summary

## Direct Result

**Pass:** the entropy-matched single-value serialization passed all six carrier
gates. Two-layer NTP relay mean held-out accuracy was 0.9846, one-layer bypass
was 1.0000, and the structurally disconnected one-layer relay remained at
0.0577, near chance.

![Entropy-matched carrier trajectories](figures/carrier_trajectory.png)

## Causal-Use Checks

- Changing early answer variable \(A\) made the ordinary head follow the new
  correct answer in 0.9769 of cases.
- Changing nuisance variable \(B\) preserved the original prediction in 0.9808
  of cases.
- Replacing the relay with an in-distribution state carrying a different
  answer made the ordinary head follow the donor label in 1.0000 of cases.
- A same-label donor preserved the answer in 0.9962 of cases.

## Recognition Update

NTP can learn this minimal relay, so later standard-head credit is a real
baseline rather than an impossible learner. The carrier also removes the
query-binding bottleneck and matches the Bayes-entropy sum of the shared-aux
and Next-2 auxiliary label sets.

This does not guarantee equal realized gradient norms or learning difficulty;
those remain diagnostics in the objective comparison.

## Next Decision

Freeze this data/model surface and test exactly one interaction: whether
relay necessity increases Next-2 standard-head utility relative to matched
shared-aux.
