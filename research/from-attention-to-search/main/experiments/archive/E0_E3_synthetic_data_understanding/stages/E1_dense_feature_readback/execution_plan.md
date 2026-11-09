# Execution Plan: E1 Dense Transformer Feature Readback

## 1. Run Goal

Train a small dense autoregressive Transformer and test whether it recovers planted sequential features.

## 2. Setup

- Model: one-layer dense Transformer, no MoE, no gate.
- Dataset: all-trigram clean long-tail corpus plus controls.
- Task: next-token prediction.
- Baselines:
  - random-only control;
  - shuffled unigram control that preserves token frequencies but destroys sequence order;
  - empirical n-gram table.

## 3. Measurements

For each feature prefix:

- $P_\theta(\text{correct next token}\mid\text{prefix})$。
- logit margin。
- feature-context CE。
- background-context CE。
- confusion matrix over predicted next token。

Representation diagnostics:

- SVD / effective rank of hidden states at feature contexts。
- SVD / effective rank of FFN activations or logit-delta matrix。
- feature-context rank vs background rank。
- fc1 / fc2 SVD top-k energy and stable rank。
- feature representation vs FFN singular-vector alignment。
- top singular direction probe against feature-token and background-token embedding means。

## 4. Pass / Fail Criteria

Pass if feature prefixes show high-confidence target prediction and background remains high entropy.

Fail if training loss decreases but planted next tokens are not recovered at feature prefixes.

## 5. Expected Artifact

A table with: prefix, target next token, empirical probability, model probability, CE, logit margin.

Additional artifacts:

- `*_transition_readback_table.csv`
- `*_context_loss_table.csv`
- `*_weight_svd_summary.csv`
- `*_svd_alignment_table.csv`
- `*_top_singular_direction_probe.csv`
- loss, context-loss, transition-readback, SVD-energy, and SVD-alignment figures.
