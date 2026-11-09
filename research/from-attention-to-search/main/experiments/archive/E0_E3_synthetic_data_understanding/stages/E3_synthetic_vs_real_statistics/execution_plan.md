# Execution Plan: E3 Synthetic vs Real Data Statistics

## 1. Run Goal

Audit real corpus statistics with the same conceptual columns as the synthetic audit.

## 2. Real-Data Diagnostics

On a real corpus:

- plot n-gram rank-frequency curves for multiple $n$;
- compute conditional entropy by context frequency bucket;
- identify high-confidence contexts;
- compare feature count distribution to synthetic target;
- estimate deterministic vs ambiguous contexts.

## 3. Synthetic Features To Compare

- n-gram / phrase frequency distribution。
- conditional entropy $H(x_{t+1}\mid x_{t-k:t})$。
- repetition and burstiness。
- context-dependent next-token certainty。
- hierarchical composition: subpattern and phrase co-occurrence。

## 4. Interpretation Rule

Do not ask whether the synthetic model works on real data first.

Ask which synthetic assumptions match real-data statistics.

## 5. Expected Artifact

A real-data audit table with the same columns as synthetic `data_audit.json`.
