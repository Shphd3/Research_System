# Experiment Plan 1 - Minimal Synthetic Data Sanity

## Decision Question
Is the synthetic data actually the data we think it is?

## Mainline Anchor
The current bottleneck is not model architecture. The first bottleneck is whether the corpus contains controlled sequential features with known frequency/popularity.

## Hypothesis
Specific token combinations, not individual token frequencies, define the feature. The feature popularity should be controlled at the n-gram/pattern level.

## Data Construction
Use a vocabulary of 100 tokens.

Start with three regimes:

1. **Random-only control**  
   All tokens iid random. No planted feature.

2. **One-feature corpus**  
   Insert one feature `[A,B]` with count `c`. Fill all other positions randomly.

3. **Four-feature corpus**  
   Insert four features with Zipf-like counts:
   - `[A,B]`: high frequency
   - `[C,D,E]`: medium frequency
   - `[F,G]`: low frequency
   - `[H,I]`: very low frequency

Important: log or filter background collisions.  
For bigrams, random background expected count is approximately $N/V^2$. With $N=10^6,V=100$, that is about 100 accidental occurrences. Any planted bigram with count near 50 is not clean unless collisions are filtered.

## Required Diagnostics
- Actual count per feature.
- Collision count per feature.
- Empirical $P(\text{next}\mid\text{prefix})$.
- Entropy of feature contexts vs random contexts.
- Zipf rank-frequency plot.

## Pass Criteria
The generator passes only if target counts, empirical conditional probabilities, and collision rates are all reported.

## Minimal Next Action
Implement `generate_synthetic_patterns.py` and produce `data_audit.json` plus one rank-frequency figure.
