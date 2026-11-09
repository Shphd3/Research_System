# Detailed: A11_14b Decision-Weighted Semantic Efficiency

Primary anchor: [11_14b_decision_weighted_semantic_efficiency_anchor.md](../../../problem_anchors/11_informative_future_branch_mechanism/11_14b_decision_weighted_semantic_efficiency_anchor.md)
Protocol: [protocol.md](protocol.md)
Summary: [summary.md](summary.md)

## 0. Decision

The valid run is **insufficient** for evaluation efficiency. Decision weighting makes the training task fit, but neither method transfers reliably to held-out cue paraphrases.

## 1. Protocol Compliance

- remote job: `pt-05fu573c`, status succeeded;
- 10/10 tasks, 10/10 checkpoints each;
- seeds `971-975`;
- 160 train and 160 held-out examples per seed;
- all shared initialization, H2 initialization, vocabulary, data, batch, token, answer-leak, finite-value, and coverage guards pass;
- decision weight fixed at `1.0` before the full run;
- no task, K, architecture, split, primary metric, or decision threshold changed.

## 2. Train Versus Evaluation

At 2,000 updates, train H1 answer accuracy is `0.90-1.00` for NTP and `0.95-1.00` for MTP. Train counterfactual/paraphrase guards yield train $Q$ of `0.80-1.00` and `0.90-1.00`, respectively.

Held-out H1 answer accuracy remains `0.519-0.625` for NTP and `0.556-0.706` for MTP. Counterfactual sensitivity remains the limiting component, with evaluation values `0.30-0.35` for NTP and `0.2375-0.4375` for MTP.

This separates the failure:

```text
task labels and pairs valid
-> explicit decision signal enables fitting
-> random small model memorizes/combines seen cue forms
-> unseen paraphrase state equivalence does not transfer reliably.
```

## 3. Paired Method Result

| Decision item | Count |
|---|---:|
| NTP evaluation threshold reached | 0/5 |
| MTP evaluation threshold reached | 0/5 |
| MTP evaluation AUC higher | 2/5 |
| MTP final evaluation $Q$ not lower | 2/5 |
| local guard pass | 5/5 |

MTP's H1/H2 answer contrast cosine stays near `0.99`, unlike unweighted A11_14 where it drifted much more. The direct and standard heads remain geometrically aligned, and MTP train H2 accuracy reaches `0.95-1.00`. Yet held-out H2 accuracy is only `0.575-0.688`. Thus private-head absorption is not the sole explanation; semantic generalization itself is weak.

## 4. Visualization Results

### Plot Contract

**Question:** after answer dilution is removed, does MTP improve common-H1 held-out semantic learning?
**Metrics:** train and evaluation $Q$, full-vocabulary H1/H2 answer accuracy, right-censored threshold budget, and non-answer H1 CE.
**Allowed conclusion:** distinguish fit, transfer, and local-cost failure.
**Limitation:** no pretrained semantic representation is used.

![A11_14b decision-weighted learning curves](figures/a11_14b_decision_weighted_learning_efficiency.png)

Dashed train curves cross or approach 0.9; solid evaluation curves remain around 0.3. This is the central evidence that the next step requires pretrained semantic geometry rather than another loss-weight adjustment.

## 5. Hypothesis Decisions

| Hypothesis | Result | Decision |
|---|---|---|
| H1 solvability repair | train yes, evaluation 0/5 | insufficient for evaluation |
| H2 earlier-credit efficiency | AUC/final wins 2/5 | not supported |
| H3 shared-head transmission | train H1 improves; eval inconsistent | partial only |
| H4 local guard | 5/5 | supported |

## 6. Artifact Map

Raw result:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
results/a11_14b_decision_weighted_semantic_efficiency/
a11_14b_decision_weighted_semantic_efficiency_4gpu_20260710_174822
```

Logs:

```text
.../logs/acp/a11_14b_decision_weighted_semantic_efficiency_4gpu_20260710_174822
```

Code:

```text
configs/a11_14b_decision_weighted_semantic_efficiency.json
scripts/run_a11_14_natural_language_semantic_learning_efficiency.py
scripts/analyze_a11_14_natural_language_semantic_learning_efficiency.py
scripts/submit_a11_14b_decision_weighted_semantic_efficiency_4gpu.sh
```

Canonical evidence:

- [paired efficiency](tables/paired_efficiency.csv)
- [trajectory summary](tables/trajectory_summary.csv)
- [decision](hypothesis_decision.json)
- [central figure](figures/a11_14b_decision_weighted_learning_efficiency.png)

## 7. Next Decision

Create A11_15 as a pretrained small-LM transfer audit on the same task and split. The first question is not yet efficiency: verify that a pretrained backbone makes held-out paraphrases solvable through the common H1 answer head. Only if both or at least one method becomes evaluation-adjudicable should threshold/AUC ordering be interpreted.

