# Experiment Plan 4 - Synthetic vs Real Data Comparison

## Decision Question
Which statistical features of the synthetic corpus are actually present in real data?

## Mainline Anchor
Synthetic data is useful only as a controlled mirror of a hypothesized real-data property. After synthetic validation, compare properties, not model performance first.

## Hypothesis
Real language should contain repeated sequential patterns with heavy-tailed popularity, but its hierarchy, ambiguity, and context dependence will differ from the toy corpus.

## Synthetic Features To Compare
- n-gram / phrase frequency distribution.
- Conditional entropy $H(x_{t+1}\mid x_{t-k:t})$.
- Repetition and burstiness.
- Context-dependent next-token certainty.
- Hierarchical composition: subpattern and phrase co-occurrence.

## Real-Data Diagnostics
On a real corpus:
- plot n-gram rank-frequency curves for multiple $n$;
- compute conditional entropy by context frequency bucket;
- identify high-confidence contexts;
- compare feature count distribution to synthetic target;
- estimate how many contexts are deterministic vs ambiguous.

## Interpretation Rule
Do not ask “does synthetic model work on real data?” first.  
Ask “which synthetic assumptions match real-data statistics?”

## What This Can Claim
It can claim whether the synthetic generator captures selected real-data statistical properties.

## What This Cannot Claim
It cannot claim MoE expert specialization in real LLMs unless real model routing and attention diagnostics are measured.

## Minimal Next Action
Create a real-data audit table with the same columns as synthetic `data_audit.json`.
