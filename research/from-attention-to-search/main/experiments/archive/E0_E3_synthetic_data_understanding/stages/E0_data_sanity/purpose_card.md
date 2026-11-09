# Experiment Card: E0 Synthetic Data Sanity

## 1. Purpose / Main Reason

Before testing dense next-token models, MoE routing, or router-guided KV retrieval, verify that the synthetic corpus itself contains the intended controlled sequential features.

The purpose is to answer: is the data actually the data we think it is?

## 2. Known Narrative / Premise

Language is a sequence, and meaning depends on context. Therefore, the synthetic feature should be a repeated context relation rather than a single token identity.

Examples:

```text
[A] -> [B]
[C,D] -> [E]
```

If the corpus does not contain clean controlled context relations, downstream dense FFN, MoE specialization, or router-retrieval analysis will be uninterpretable.

## 3. Hypothesis To Decide

H0: The synthetic corpus contains controlled sequential features at the pattern level. Planted token combinations appear with designed Zipf-like popularity, while non-feature positions behave like random background.

## 4. Experiment Question

Does the generated corpus have the intended feature counts, conditional next-token probabilities, background collision rates, entropy gap, and rank-frequency behavior?

## 5. Data And Task Construction

Vocabulary size: $V=100$.
Corpus length: default $N=10^6$.
Random seed: `20260513`.

Regime 1: random-only control.
- All tokens sampled iid from vocabulary.
- No planted feature.
- Purpose: estimate accidental background n-gram collision.

Regime 2: one-feature corpus.
- Plant `[A,B]` with target count `10000`.
- Fill all other positions with iid random tokens.
- Log accidental `[A,B]` occurrences from background.

Regime 3: four-feature corpus.
- `[A,B]`: count `10000`
- `[C,D,E]`: count `5000`
- `[F,G]`: count `500`
- `[H,I]`: count `100`
- Fill remaining positions with iid random tokens.
- Log or filter background collisions for each planted pattern.

No model is trained in E0. The task is dataset audit.

## 6. Setup

Model: none.
Dataset: synthetic token sequence.
Signal source: planted pattern metadata plus observed corpus statistics.
Candidate construction: not applicable.

## 7. Baselines

- Random-only corpus.
- Expected random bigram collision rate, approximately $N/V^2$ for bigrams.

## 8. Metrics

- Actual count per feature.
- Target count vs actual count.
- Background collision count per feature.
- Empirical $P(\text{next token} \mid \text{prefix})$.
- Feature-context entropy.
- Background-context entropy.
- Rank-frequency plot and fitted Zipf slope.

## 9. Expected Outcomes

If E0 passes, target counts, collision counts, empirical conditional probabilities, entropy, and long-tail frequency order are all reported and consistent with the intended construction.

If low-frequency planted counts are close to accidental collision counts, the dataset is not clean enough for E1.

## 10. What This Can Prove

It can prove the synthetic data construction is controlled enough for downstream model experiments.

## 11. What This Cannot Prove

It cannot prove a dense model learned the features.
It cannot prove MoE experts specialize.
It cannot prove router buckets align with dense-attention contributors.
It cannot prove transfer to real language data.

## 12. Result

TBD.

## 13. Conclusion

TBD.

## 14. Next Step

Run E1 dense next-token smoke test only if E0 passes.
