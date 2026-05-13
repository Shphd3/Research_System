# 0513 Experiment Cards - Synthetic Data Understanding

## Current Mainline

Before using MoE/router claims, first prove that the synthetic data itself contains the intended language-like statistical features and that a dense next-token model can recover them.

## Card E0: Data Generator Sanity Audit

### 1. Hypothesis To Decide
H0: The synthetic corpus really contains controlled sequential features: specific token combinations appear with designed Zipf-like popularity, while the rest is random background.

### 2. Experiment Question
Does the generated corpus have the exact feature counts, conditional next-token probabilities, and background collision rates we intended?

### 3. Setup
Model: none.  
Dataset: vocabulary size $V=100$, corpus length $N=10^6$.  
Features: one or more n-gram patterns, e.g. `[A,B]`, `[C,D,E]`, `[F,G]`, `[H,I]`.  
Background: iid random tokens from vocabulary, with either collision filtering or collision logging.

### 4. Metrics
- Actual count of each feature.
- Random background collision count for each feature.
- Empirical $P(\text{next token} \mid \text{prefix})$.
- Feature frequency rank plot and fitted Zipf slope.
- Background next-token entropy.

### 5. Expected Outcomes
If generator is correct, feature counts match target and feature contexts have low next-token entropy.  
If not, later model results are uninterpretable.

### 6. What This Can Prove
It proves the data construction is controlled.

### 7. What This Cannot Prove
It does not prove any model has learned the feature.

### 8. Result
TBD.

### 9. Next Step
Run E1 only after E0 passes.

---

## Card E1: One-Feature Dense NTP Smoke Test

### 1. Hypothesis To Decide
H1: A tiny dense next-token model can recover one deterministic or high-probability sequential feature from random background.

### 2. Experiment Question
If the only planted feature is `[A,B]`, does the model output high $P(B \mid A)$ and near-random predictions elsewhere?

### 3. Setup
Model: small dense autoregressive model, preferably one-layer Transformer or even a minimal bigram baseline.  
Dataset: one planted feature `[A,B]` inserted at high frequency; all other positions random.  
Task: next-token prediction, not classification.

### 4. Baselines
- Empirical bigram table.
- Random predictor.
- Tiny dense Transformer.

### 5. Metrics
- $P_\theta(B \mid A)$.
- Accuracy / CE on feature contexts vs random contexts.
- Logit margin: $\ell_B(A)-\max_{j\ne B}\ell_j(A)$.
- Calibration against empirical $P(B\mid A)$.

### 6. Expected Outcomes
If H1 holds, model confidently predicts `B` after `A` and remains uncertain elsewhere.  
If H1 fails, either the data generator, task definition, or training setup is broken.

### 7. Claim Boundary
This only proves a model can learn one controlled sequential feature.

### 8. Result
TBD.

### 9. Next Step
Move to four-feature dense model.

---

## Card E2: Four-Feature Dense Transformer Readback

### 1. Hypothesis To Decide
H2: Dense Transformer representations/logits expose the four planted features as a small number of dominant signal directions or conditional transitions.

### 2. Experiment Question
With four planted names/patterns, can a dense model recover all four and separate them from random background?

### 3. Setup
Model: one-layer dense Transformer, no MoE, no gate.  
Dataset: four features with Zipf-like counts, e.g. `[A,B]`, `[C,D,E]`, `[F,G]`, `[H,I]`; background random.  
Task: autoregressive next-token prediction.

### 4. Metrics
- Per-feature next-token probability.
- Per-feature CE / accuracy.
- Feature-context vs background entropy.
- SVD/effective rank of hidden states, FFN activations, or logit-delta matrix.
- Confusion matrix: prefix feature $\rightarrow$ predicted next token.

### 5. Expected Outcomes
If H2 holds, each feature context has a distinct prediction signature; background remains high entropy; signal rank should roughly match the number of independent planted transitions.

### 6. What This Cannot Prove
It cannot prove MoE experts specialize; it only validates dense-model recoverability.

### 7. Result
TBD.

### 8. Next Step
Only after this passes, run MoE specialization.

---

## Card E3: Four-Expert MoE Specialization

### 1. Hypothesis To Decide
H3: In the four-feature synthetic world, a four-expert MoE can route different planted features to different experts.

### 2. Experiment Question
Does each expert specialize to one feature rather than merely balancing load or memorizing token frequency?

### 3. Setup
Model: same base as E2, replace FFN with 4-expert top-1 or top-2 MoE.  
Dataset: same four-feature corpus.  
Task: next-token prediction.

### 4. Metrics
- Expert purity by feature: $P(\text{feature}=f \mid \text{expert}=e)$.
- Feature routing concentration: $P(\text{expert}=e \mid \text{feature}=f)$.
- NMI / ARI between feature ID and expert ID.
- Per-feature next-token accuracy.
- Expert load distribution.
- Seed stability.

### 5. Expected Outcomes
Strong support: near one-to-one feature-expert mapping, high NMI, stable across seeds.  
Weak support: better-than-random but mixed routing.  
No support: routing mostly follows token frequency or load balance, not feature identity.

### 6. What This Can Prove
It can test whether MoE routing can recover known synthetic features under an easy controlled setting.

### 7. What This Cannot Prove
It cannot prove real language features are similarly separable, nor that router IDs align with attention softmax winners.

### 8. Result
TBD.

### 9. Next Step
If clean, compare with real data; if not, debug synthetic setup before scaling.

---

## Card E4: Hierarchical Phrase Extension

### 1. Hypothesis To Decide
H4: When planted features become hierarchical phrases, attention/sequence modeling becomes necessary and simple n-gram memorization is insufficient.

### 2. Experiment Question
Can a model learn both low-level features (`经 常`, `打 球`) and higher-level phrases (`A B 经 常 打 球`) with different popularity?

### 3. Setup
Dataset: controlled phrases with nested subpatterns and Zipf-like counts.  
Models: dense Transformer first, then MoE.  
Task: next-token prediction.

### 4. Metrics
- Low-level n-gram recovery.
- Higher-level phrase recovery.
- Error by hierarchy level.
- Attention pattern over earlier phrase tokens.
- Expert routing by hierarchy level, if MoE is used.

### 5. Claim Boundary
This is a second-stage experiment after E0-E3; do not use it before the one-feature and four-feature tests are clean.

### 6. Result
TBD.
