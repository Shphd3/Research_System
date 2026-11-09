---
experiment_id: A15_01_02_E01_low_variance_functional_delay
verdict: weak_pass_delay_only_strong_fail
completed: 2026-07-31
canonical_language: en
---

# Result: Low Variance Delays Correct Stability; It Does Not Randomize Tail

## Direct Result

**Strong conjecture Fail; weak delay conjecture Pass.** Native tail was not
random-like: all 32 tail Gates became both correct and persistent by step 2,460
at the latest, and final tail accuracy was 0.953 versus 0.501 for matched
label-free random tail. Low variance nevertheless caused a large finite-time
delay that energy equalization mostly removed.

Functional stability time \(T_{FS}\) is the first optimizer step where held-out
accuracy is at least 0.90 and route flip rate is at most 0.02 for three
consecutive evaluations. It prevents a stable-wrong random Gate from being
called stable.

| Condition | Crossed / 32 | Median \(T_{FS}\) | Restricted mean \(T_{FS}\) | Final accuracy |
| --- | ---: | ---: | ---: | ---: |
| Native H | 32 | 600 | 552 | 0.973 |
| Native M | 32 | 1,080 | 912 | 0.967 |
| Native T | 32 | 2,130 | 1,938 | 0.953 |
| Equal-energy T | 32 | 660 | 615 | 0.972 |
| Random T | 0 | censored | 4,000 | 0.501 |

The paired restricted-time contrasts were H→M +360 steps
(95% interval [227,481]) and M→T +1,026 steps ([802,1,255]). Equalization
reduced tail's restricted mean time by 68.3%.

## Central Figure

![Low variance delays correct stability](figures/functional_stability.png)

The accuracy panel shows ordered H/M/T learning and the recovery of equalized
T. The flip panel shows why churn alone is misleading: random T quickly has
near-zero flips while remaining at chance accuracy. Native T eventually
crosses both functional thresholds.

## Operational Validity

- 32/32 formal seeds completed for every native, equal-energy, and random band.
- Equal-energy H/M/T crossed in 32/32 seeds; random H/M/T crossed in 0/32.
- Random final accuracies were 0.499, 0.500, and 0.501 for H/M/T.
- All numeric, pairing, initial-condition, known-good, and known-bad guards
  passed on remote job `pt-15rmvipu`.

## Knowledge Update And Boundary

The correct statement is:

> Low covariance makes a learnable routing coordinate slower to become
> functionally stable, but low variance alone does not make it equivalent to a
> random basis. Tail eventually converges to the correct persistent partition;
> equalization mainly changes when, not what, it learns.

This result is for a matched-SNR linear controlled system. It does not show
that a natural tail band is semantically useful, that real checkpoints will
recover within the same factor, or that stable routes improve expert training.
The next layerwise portrait should therefore report correctness and persistence
together, not raw flip or covariance energy alone.
