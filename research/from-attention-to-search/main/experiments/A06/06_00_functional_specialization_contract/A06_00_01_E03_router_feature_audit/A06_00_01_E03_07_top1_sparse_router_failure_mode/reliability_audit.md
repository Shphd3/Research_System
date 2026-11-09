# Reliability Audit: H0526 Top-1 Sparse Router Failure Mode

## Conclusion

H0526 is valid as a sparse-router experiment. The failure signal is not caused by zero router gradients or accidental soft mixture.

## 1. Sparse Router Validity

| Check | Result |
|---|---|
| C1 router weight grad norm | 0.043496 |
| C1 router bias grad norm | 0.003369 |
| C1 router logits/probs grad | nonzero |
| C1 router weight delta after one step | 0.018101 |
| active experts per token | 1 |
| full soft mixture | false |
| selected gate renormalized to 1 | false |

## 2. Negative Control

Hard top-1 no-gate has router grad 0 and router delta 0, while still activating one expert per token. This confirms the audit distinguishes sparse dispatch from trainable router weighting.

## 3. Task Learning

Signal classes reach near-perfect accuracy, so ablation results are not from an untrained model.

## 4. Failure Mode Reliability

Observed pattern:

```text
S_AB is strong in only 1/4 seeds.
route-function mismatch appears in seed 20260524 for AB-composite.
load imbalance is moderate but not total collapse.
```

Reliability judgment:

```text
The cleanest conclusion is unstable functional specialization under no-load-balance top-1 selected-gate routing.
```
