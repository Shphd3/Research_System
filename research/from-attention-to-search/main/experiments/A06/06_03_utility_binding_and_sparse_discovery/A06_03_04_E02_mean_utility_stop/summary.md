# A06_03_04_E02 Utility-Certified Audition Stop: Summary

## What We Established

The all-position mean utility certificate is highly compute-efficient but is
not yet a valid safety certificate. It triggers in every specialist seed at
median step `220.5`, saves `63.25%` of the 600 allowed auditions, reaches
`127/128` final correction, and retains every corrected cell. However, it stops
before sustained route correction in `24/128` cells (`18.75%`), above the
preregistered 5% limit.

The failure is not explained by background positions. The oracle task-position
utility certificate has nearly identical behavior: `127/128` correction,
`17.1875%` premature stops, and `62.83%` median audition saving. Score confidence
never triggers, and interchangeable generalists never trigger the utility
certificate.

The decisive conclusion is: **mean pairwise utility detects the global phase
transition, but it is not tail-safe**. Utility averaged over an incumbent's
routed population can be dominated by already-correct examples while a minority
still routes to the wrong identity.

## Exact Setup

- A06_03_04_E01 learned specialists, useful expert installed at rank 4.
- Frozen experts and representation; router-only SGD `0.001`; full LM loss.
- Maximum 600 continuous pair auditions; total horizon 800.
- Utility EMA decay `0.9`; all 12 directed expert pairs required positive for
  nine stable updates.
- 32 seeds and four tasks; four-H100 job `pt-r30pqxpg` succeeded.

## Primary Results

| Stop rule | Correction | Retention | Premature stop | Median stop | Median audition saving |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fixed 600 | 1.0000 | 1.0000 | 0 | 600.0 | 0 |
| Oracle route | 1.0000 | 1.0000 | 0 | 242.5 | 0.5958 |
| Score only | 1.0000 | 1.0000 | 0 | censored 600 | 0 |
| Utility all-position | 0.9922 | 1.0000 | 0.1875 | 220.5 | 0.6325 |
| Utility task-oracle | 0.9922 | 1.0000 | 0.1719 | 223.0 | 0.6283 |

Generalist utility-all trigger rate is zero.

![Stopping tradeoff](figures/stopping_rule_tradeoff.png)

The left panel shows that mean utility preserves almost all eventual correction
but violates the premature-stop constraint. The right panel shows substantial
compute savings. This figure does not justify accepting the safety failure.

![Margin trajectories](figures/certified_stop_margin_trajectories.png)

Utility-stop trajectories closely track the fixed and oracle branches and end
with slightly larger median margin because top-1 reinforces the corrected route
after an earlier switch. Aggregate median trajectories hide the minority cells
responsible for premature stopping; that hidden tail is the next mechanism.

## Hypothesis Update

- H1 utility-certified stop succeeds: rejected by premature-stop rate.
- H2 score confidence is sufficient: rejected; score-only never triggers.
- H3 semantic-position credit is required: rejected; task-oracle utility does
  not materially improve the failure.
- H4 mean certificate is not identifiable as a safe stopping rule: supported.

## Next Decision

Replace mean utility with a distributionally robust certificate. The next test
must compare lower-tail utility quantiles or conditional value at risk against
the mean, and determine whether tail evidence reduces premature stops below 5%
without losing at least 30% audition saving. This is a route-population
heterogeneity problem, not an MTP source-credit problem.

## Claim Boundary

The current rule is a strong predictor and engineering candidate, not a safe
certificate. The experiment does not establish joint-training robustness,
pretrained-LLM transfer, scalable per-token statistics, or systems throughput.
