# Experiment Card: E2.3 Router Behavior Decomposition

## 1. Purpose / Main Reason

E2.3 的目的不是继续证明 feature 被学到，而是解释 learned router 到底按什么变量划分。E2.1 已经显示 feature identity 在 router input hidden space 中可分，但 router boundary 没有强烈对齐 feature-difference directions；E2.2 又显示 readback 可保持很高而 dominant expert ablation effect 变弱。因此下一步要把 expert choice 本身作为被解释变量。

## 2. Known Narrative / Premise

已知前提：

- controlled all-trigram MoE 能读回 planted trigram features；
- shuffled unigram control 不能读回这些 feature；
- feature identity 在 router input hidden states 中仍可分；
- learned router boundary 与 feature-difference direction alignment 低；
- 多个 experts 能支持同一 feature prediction；
- 增加 feature count 或降低 expert capacity 没有强制 clean one-feature-one-expert。

## 3. Hypothesis To Decide

H2.3a: router choice mainly follows feature identity.

H2.3b: router choice mainly follows shortcut or nuisance variables: prefix-end token, target token, hidden norm, activation scale, frequency, CE difficulty, or target confidence.

H2.3c: router choice follows low-variance but router/logit-relevant hidden directions rather than human-defined feature centroid directions.

H2.3d: feature readback is mostly supported by shared attention/residual/LM head or shared expert competence, so NTP loss does not require feature-aligned partition.

## 4. Experiment Question

Given router input hidden state $h_t$ at feature prefix-end positions and matched background positions, which variables best predict the learned top-1 expert id, and does feature identity remain explanatory after conditioning on token/norm/difficulty/router-logit variables?

## 5. Data And Task Construction

Use the existing E2 checkpoints and all-trigram data.

Samples:

- feature prefix-end positions `[A,B] -> C`;
- matched non-feature background positions;
- optional hard negatives with same B token if available;
- for next data run, add crossed-feature controls where the same B token appears in multiple rules.

Recorded fields:

- `feature_id`, `A_token`, `B_token`, `target_token`, `feature_frequency`;
- router input hidden state `h`;
- hidden norm and selected activation statistics;
- router logits, margin, entropy, selected expert id;
- LM target logit, CE loss, target probability;
- PCA coordinates and router-weight projections.

## 6. Setup

Model: E2 trained 4-expert top-1 MoE checkpoint.

Dataset: four_feature_all_trigram_v1000, plus optional crossed-feature control for shortcut test.

Layer: MoE router input at prefix-end token.

Signal source: learned router top-1 expert id and router logits.

Candidate explanatory variables:

- feature identity;
- prefix-end token identity;
- target token identity;
- hidden norm / activation scale;
- CE loss / target confidence / logit margin;
- frequency bucket;
- PCA top-k coordinates;
- router boundary projections $W_{router}h$;
- low-variance PLS/CCA directions selected to predict router logits.

## 7. Baselines

- Random expert predictor matched to global load.
- Majority expert predictor.
- Feature-only predictor.
- B-token-only predictor.
- Norm/difficulty-only predictor.
- PCA-only predictor.
- Full hidden linear probe.
- Router-logit projection predictor.

## 8. Metrics

- expert-id prediction accuracy;
- expert-id NLL;
- McFadden pseudo-$R^2$;
- mutual information with expert id;
- conditional permutation importance;
- within-B-token feature effect;
- within-norm/CE bucket feature effect;
- assignment stability under feature-subspace and router-subspace projection.

## 9. Expected Outcomes

If H2.3a holds:

- feature-only or A+B relation predictor explains expert id best;
- feature_id retains high conditional importance after controlling B token, norm, frequency, and CE;
- projecting feature subspace changes expert assignment.

If H2.3b holds:

- B token, norm, CE/margin, or frequency explains expert id better than feature_id;
- feature_id loses conditional importance after controlling shortcut variables;
- crossed-feature shared-B design breaks or changes routing.

If H2.3c holds:

- PCA/centroid separability remains high but router assignment is explained by router-weight projections or PLS/CCA directions;
- low-variance router-relevant directions change routing more than feature centroid directions.

If H2.3d holds:

- random/oracle routing changes expert id but barely changes readback/CE;
- zero or mean-replaced MoE output still preserves feature prediction;
- feature-oracle routing improves partition cleanliness without improving NTP loss much.

## 10. What This Can Prove

It can decide whether the learned router is using feature identity or an alternative loss-compatible variable in this toy setting.

It can support the claim that representation separability does not imply router specialization, if feature_id is recoverable from hidden states but not used to explain learned expert choice.

## 11. What This Cannot Prove

It cannot prove real LLM experts do or do not specialize semantically.

It cannot prove MoE routers are useless as KV indices.

It cannot prove a universal theory of routing; it only diagnoses this controlled trigram NTP setup.

## 12. Result

TBD.

## 13. Conclusion

TBD.

## 14. Next Step

If E2.3 shows shortcut/norm/difficulty dominates, run crossed-feature data control. If it shows shared-path bypass dominates, run shared-path bottleneck or expert-path necessity intervention.
