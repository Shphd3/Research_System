# Protocol: A11_14b Decision-Weighted Semantic Efficiency

## 0. Approval Snapshot

**Purpose:** repair the answer-signal dilution identified by A11_14 without changing the task, K, architecture, or common downstream metric.  
**Decision question:** does MTP's earlier H2 decision loss improve common-H1 learning efficiency once both methods receive the same explicit H1 decision loss?  
**Primary metric:** evaluation $T_{0.9}$ and token-AUC for the unchanged $Q_{downstream}$.  
**Conditions:** decision-weighted NTP and decision-weighted K=2 MTP only.  
**Seeds:** `971-975`.  
**Execution:** remote four-H100 full run after paired CPU/GPU smoke.  
**Cannot claim:** pure all-position pretraining efficiency or pretrained-LLM benefit.

## 1. Fixed Contract

Everything below remains identical to A11_14:

- A11_13 `horizon_target=256` task;
- train paraphrase IDs `0,1`, evaluation IDs `2,3`;
- 160 train and 160 evaluation examples per seed;
- word/punctuation vocabulary and sequence rendering;
- two-layer causal Transformer and copied H1/H2 initialization;
- AdamW `3e-4`, weight decay `0.01`, batch size `16`, gradient clip `1.0`;
- paired sample, vocabulary, initialization, batch, token, and update hashes;
- full-vocabulary H1 argmax in the common downstream score.

## 2. Objective Change

Only the decision terms change:

$$
L_I=\frac1B\sum_i\operatorname{CE}(U_1h_{i,T+1},Y_i),
$$

$$
L_D=\frac1B\sum_i\operatorname{CE}(U_2h_{i,T},Y_i).
$$

With $\lambda=1$:

$$
L_{NTP}^{dw}=L_1^{all}+\lambda L_I,
$$

$$
L_{MTP}^{dw}=L_1^{all}+L_2^{all}+\lambda(L_I+L_D).
$$

This preserves ordinary all-position training and gives the behaviorally decisive answer an order-one contribution, as in supervised task adaptation. It does not represent pure next-token pretraining.

## 3. Training And Evaluation

- 2,000 updates;
- checkpoints `0,10,20,50,100,200,500,1000,1500,2000`;
- evaluate both train and held-out splits at each checkpoint;
- record H1/H2 decision losses in addition to all A11_14 metrics;
- ten tasks sharded over four GPUs.

Train and evaluation scores use the same definitions, with a split prefix:

$$
Q_{split}=\min\{A_{H1}^{split},C_{para}^{split},S_{cf}^{split}\}.
$$

## 4. Decision Rules

**Valid:** all A11_14 paired guards pass; train/eval metrics are complete and finite.

**Adjudicable:** at least one condition reaches evaluation $Q\ge0.9$ for three consecutive evaluations in at least 4/5 seeds.

**Supported:** MTP has smaller evaluation $T_{0.9}$ and larger evaluation token-AUC in at least 4/5 seeds; final evaluation $Q$ is not lower in at least 4/5; every local H1 guard passes.

**Weakened:** adjudicable, but speed/AUC or local guards fail.

**Insufficient:** neither condition is evaluation-adjudicable. Use train $Q$ to report whether the bottleneck is fitting or held-out paraphrase transfer.

**Falsified:** both are adjudicable and MTP is slower in at least 4/5 seeds.

## 5. Required Evidence

- evaluation and train curve tables;
- paired threshold/AUC table;
- H1/H2 decision-loss table;
- all pairing and coverage guards;
- central figure separating train fit, evaluation transfer, H1/H2, and local H1 cost;
- `summary.md`, `detailed.md`, anchor update, and story update.

