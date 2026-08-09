# Can MTP's Additional Learning Signal Be Used by the Standard Predictor?

## 0. Executive Summary

**Research question:** What does multi-token prediction (MTP) learn beyond next-token prediction (NTP), and can the shared standard next-token head use that information on an evidence-composition task?

**Update:** The research is separated into two layers: first identify MTP's objective-specific direct signal, then test whether that signal becomes functional on a task that requires an intermediate result.

**Current conclusion:**

1. An informative future token adds a direct current-state update unavailable to NTP at that position. Information inclusion and update-direction alignment matter more than horizon length alone.
2. The signal can form at the current state and reach shared parameters, but it need not remain useful to the standard head one position later.
3. Missing representation directions can make MTP improve the future target while harming the standard target. Curriculum cannot create the missing direction.

**Boundary:** Real long-context benefit and a general model-scale law are unproved. The current from-scratch small model also failed to learn the new composition task.

**Action:** First require one pretrained small model to pass the shared capability gate. Stop on failure; compare NTP and MTP from the same checkpoint only after a pass.

## 1. Questions

1. Why does the constructed task isolate the target capability?
2. What has MTP been shown to add, and is it used by the standard head?
3. Why can MTP harm the standard objective, and can curriculum repair it?

### Definitions

| Term | Plain meaning | Concrete object | Cannot prove |
|---|---|---|---|
| Standard head | The normal next-token predictor used for autoregressive output | Shared answer interface in all conditions | Auxiliary-head success is standard-generation success |
| Intermediate state | First result needed by the second computation | Entity $B$ returned by the first table | Probe recovery means functional use |
| Functional use | Intervening on the intermediate state changes the standard-head answer by the task rule | Counterfactual intervention on $B$ | Real-task improvement |

## 2. Minimal Model and Exact Data

Let two complete random one-to-one maps act on the same entity set. The query gives start entity $A$:

$$
B=\pi_1(A),\qquad Y=\pi_2(B).
$$

One table alone is insufficient: the first does not specify the second mapping, and the second does not specify which row to use. Together they model the controlled skeleton of multi-document hops, graph queries, and code-dependency tracing.

```text
Table 1: v0→v2, v1→v0, v2→v3, v3→v1
Table 2: v0→v1, v1→v3, v2→v0, v3→v2
Query: start from v1; apply Table 1 and then Table 2.
Intermediate state: v0; answer: v1
Output: <DECIDE> <FMT_0> <ANS_v1>
```

**Training and evaluation:** NTP predicts the format token at the decision state and the answer with the standard head one position later. MTP keeps those losses and additionally predicts the answer directly from the decision state. Final comparison always uses the shared standard answer head.

## 3. Current Answers

### Question 1: Is the task valid?

**Answer:** The construction strictly requires ordered composition, but the current small model did not learn it.

**Decisive evidence:** A two-layer width-64 model trained for 3,000 steps reached answer accuracy `0.1274–0.1353` across five seeds, near eight-class chance `0.125`, while format accuracy was `1.0`.

**Boundary:** This disqualifies the checkpoint for objective comparison; it does not show that a pretrained model cannot learn the task.

**Source:** [Capability summary](../../../../../../Projects/from-attention-to-search/main/experiments/A12/12_01_compositional_workload_capability_gate/A12_01_01_E02_explicit_binding_calibration/summary.md)

### Question 2: Is the MTP information used?

**Answer:** Direct formation is supported; cross-position standard-head use is not.

**Decisive evidence:** The direct update turns on at the first informative future position, and parameter transmission is positive in `5/5` seeds. Standard-head usefulness is positive at the current state in `5/5` seeds and one position later in `0/5`.

**Boundary:** This supports “formation does not imply use” only in the controlled setting.

**Source:** [Information inclusion](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_01_informative_horizon_supervision/A11_01_01_E01_next_k_inclusion_law/summary.md) · [Parameter transmission](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E01_semantic_tangent_transmission/summary.md) · [Cross-position use](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E01_head_position_cross_kernel/summary.md)

### Question 3: What do capacity and curriculum explain?

**Answer:** Missing independent representation directions are sufficient to create an MTP/NTP tradeoff, and curriculum cannot repair this structural deficit.

**Decisive evidence:** At rank one, the MTP standard-loss penalty is `0.9084–1.0218` while future-factor error improves in `5/5` seeds; at rank two the penalty is numerically zero. Dose-matched curriculum passes in `0/5` rank-one seeds.

**Boundary:** This is a controlled linear mechanism, not a Transformer scale law. Curriculum may still help an optimization-path problem when capacity is sufficient.

**Source:** [Rank summary](../../../../../../Projects/from-attention-to-search/main/experiments/A12/12_02_interference_capacity_curriculum_boundary/A12_02_01_E01_task_rank_competition/summary.md) · [Curriculum boundary](../../../../../../Projects/from-attention-to-search/main/experiments/A12/12_02_interference_capacity_curriculum_boundary/A12_02_01_E02_curriculum_rank_boundary/summary.md)

## 4. One Next Decision

**Action:** Calibrate one pretrained small model on the same task.

**Pass:** Full-answer accuracy at least `0.70`, format accuracy at least `0.99`, single-table accuracy at most `0.20`, and evidence-swap consistency at least `0.90`.

**Stop:** If any gate fails, do not compare objectives or run representation interventions. After a pass, clone NTP and MTP from the same checkpoint and intervene on intermediate state $B$. [Draft protocol](../../../../../../Projects/from-attention-to-search/main/experiments/A12/12_03_standard_head_causal_use/A12_03_E01_standard_head_causal_use/protocol.md)

## 5. Source Index

- [A11 current boundary](../../../../../../Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/README.md)
- [A12 current boundary](../../../../../../Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/README.md)
- [Next protocol](../../../../../../Projects/from-attention-to-search/main/experiments/A12/12_03_standard_head_causal_use/A12_03_E01_standard_head_causal_use/protocol.md)
