# Result Summary: E0 Data Sanity

## Observation

E0 first generated the original `V=100,N=10^6` corpus and found that low-frequency
bigram features were too close to background collision. We then regenerated the
clean testbed as all-trigram context relations with `V=1000,N=10^6`.

Final all-trigram audit:

| Feature | Pattern | Target count | Actual | Collision | Empirical prob |
|---|---|---:|---:|---:|---:|
| ABC | `[1,2] -> 22` | 10000 | 10000 | 0 | 1.000 |
| DEF | `[3,4] -> 23` | 5000 | 5000 | 0 | 1.000 |
| GHI | `[6,7] -> 20` | 500 | 500 | 0 | 1.000 |
| JKL | `[8,9] -> 21` | 100 | 100 | 0 | 0.971 |

## Interpretation

The all-trigram version solves the key E0 risk: low-frequency features are no
longer drowned by accidental bigram collision. The final corpus is clean enough
to test dense readback and then MoE feature separation.

## Limitation

This is still synthetic discrete-token data. It proves data controllability, not
real-language transfer or MoE specialization.

## Key Figures

![Rank frequency](figures/rank_frequency.png)

`figures/rank_frequency.png` supports the dataset-construction claim that
planted features follow the intended long-tail frequency order.

## Claim Update

- Supported: all-trigram synthetic features are clean enough for E1 dense
  readback.
- Supported: low-frequency feature probes can be separated from background by
  using longer context relations and larger vocabulary.
- Still unclear: whether MoE experts will separate these feature relations.

## Decision

Use the all-trigram clean long-tail corpus for E1 dense readback and E2 MoE
feature separation.
