# Experiment Plan 2 - Dense Model Before MoE

## Decision Question
Can a simple dense autoregressive model recover the planted sequential features?

## Mainline Anchor
Do not discuss MoE specialization until a dense model can read back the planted features.

## Hypothesis
If the data contains strong controlled patterns, a small dense next-token model should learn high-confidence next-token predictions at feature prefixes and high-entropy predictions elsewhere.

## Model Setup
- Model: one-layer Transformer, no MoE, no gate.
- Task: next-token prediction.
- Dataset: first one-feature corpus, then four-feature corpus.
- Baseline: empirical bigram/n-gram table.

## Measurements
For each feature prefix:
- $P_\theta(\text{correct next token}\mid\text{prefix})$
- logit margin
- feature-context CE
- background-context CE
- confusion matrix over predicted next token

Representation diagnostics:
- SVD/effective rank of hidden states at feature contexts.
- SVD/effective rank of FFN activations or logit-delta matrix.
- Compare feature-context rank to background rank.

## Expected Outcomes and Claim Updates
If dense model learns one-feature and four-feature corpora:
- Claim: synthetic data is learnable and readback works.
- Strength: supported for the synthetic setup only.

If dense model fails:
- Claim: no MoE conclusion is meaningful.
- Next action: debug data generation, training objective, or evaluation.

## Minimal Next Action
Train the one-feature dense model and produce a table: prefix, target next token, empirical probability, model probability, CE, logit margin.
