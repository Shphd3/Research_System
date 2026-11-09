# Summary: E14-P2 parent-only supervision restores online task performance

Primary Anchor: [handoff question](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md). [Frozen Protocol](protocol.md) · [Detailed record](detailed.md) · [Chinese four-part analysis](summary_cn.md).
Execution: COMPLETE / ELIGIBLE. Typed verdict: `ONLINE_PARENT_REPAIR_SUPPORTED`.
Interpretation status: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`; measured results and registered verdict are audited, researcher-owned knowledge wording remains pending.

## Result Snapshot

Training only the existing 3,075-parameter parent classifier on original pseudo-parent labels lowers fully online answer NLL in both frozen expert checkpoints. Every required comparison passes: repaired routing outperforms original routing and frequency-matched shuffled supervision on both full evaluation and the record-disjoint subset, separately for both seeds. All eight paired 95% lower endpoints are positive.

Mean full-evaluation NLL decreases from **0.836757276 to 0.804182618**, a reduction of **0.032574658 nats/answer token**. Only the coarse Router changes; all expert banks and the child Router remain fixed. This repairs an operational handoff failure in this workload, not evidence of universal semantic routing or unpolluted benchmark generalization.

## Decision-Bearing Setup

O = original online routing; R = parent-only real-pseudo-label repair; S = identical parent-only training with shuffled labels; B = supplied pseudo parent plus original predicted child; C = supplied complete pseudo path. Teacher means the original pseudo assignment, not a gold Oracle. In O/R/S evaluation no teacher path is supplied. NLL is total reference-answer negative log probability divided by answer-token count; lower is better. It uses reference previous answer tokens, not free generation.

Full evaluation has 512 records/30,442 answer tokens. The 384-record, 27,133-token disjoint subset removes all training-ID overlap and excludes GPQA and HumanEval; it is a six-source safeguard, not decontamination proof.

| Condition | Mean full-evaluation NLL |
|---|---:|
| O | 0.836757276 |
| R | 0.804182618 |
| S | 0.839262231 |
| B | 0.806081803 |
| C | 0.805028417 |

Source: [conditions](tables/conditions.csv). Both external teacher references have slightly higher point-estimate loss than R. They are privileged references, not guaranteed lower-loss bounds. No equivalence claim or superiority over a separate gold-trained model follows.

## Verdict Basis

| Seed | Population | Comparison | NLL reduction | Paired-record 95% interval |
|---|---|---|---:|---|
| 17 | full | O − R | 0.041751086 | [0.035440500, 0.048617485] |
| 17 | full | S − R | 0.035151401 | [0.029974241, 0.040884740] |
| 17 | disjoint | O − R | 0.037414844 | [0.031418940, 0.044384431] |
| 17 | disjoint | S − R | 0.032856327 | [0.027605232, 0.039045552] |
| 29 | full | O − R | 0.023398230 | [0.019733886, 0.027877898] |
| 29 | full | S − R | 0.035007825 | [0.029936917, 0.040916958] |
| 29 | disjoint | O − R | 0.018619633 | [0.014763391, 0.022976717] |
| 29 | disjoint | S − R | 0.030829598 | [0.025683539, 0.036935689] |

Source: [registered contrasts](tables/contrasts.csv), [machine-readable result](tables/results.json). The rule requires every lower endpoint above zero. Frozen analysis: 2,000 paired-record bootstrap draws, seed 20260906; no seed pooling, checkpoint selection, outlier removal or post-hoc threshold. Records are paired across conditions, not independent treatment samples.

![Online parent repair](figures/online_parent_repair.png)
How to read: left panels compare five paths; right panels show both necessary improvements above zero for both seeds, including the record-disjoint subset.

## Readout Evidence And Claim Boundary

Full-evaluation pseudo-parent agreement rises from 24.08% to 87.47% in seed 17 and from 31.66% to 86.53% in seed 29. Shuffled-supervision models reach only 38.54% and 34.58%. These are agreement with pseudo labels, not ground-truth semantic accuracy. The task-loss comparison, not agreement alone, establishes the registered success.

![Readout and task evidence](figures/parent_readout_and_task.png)
How to read: real-label supervision raises development agreement and improves evaluation task loss; the shuffled control does not reproduce that combination. This descriptive plot is not an estimated causal relationship between accuracy and loss. Source: [classification history](tables/classification_history.json) and [conditions](tables/conditions.csv).

The original large handoff failure cannot be used as evidence that final-layer labels necessarily mislead earlier routing: keeping those labels and the input hook fixed while supplying missing supervision suffices for a task-loss repair here. The labels remain full-sequence, privileged training targets; optimal teacher layer, fine semantics, free-generation accuracy, and generalization to clean public tasks remain untested. Class-count matching is at the example level; one fixed shuffled assignment is not a distribution over all possible null partitions.

## Next Decision

Use the repaired checkpoints as the candidate fixed online baseline for subsequent teacher/readout diagnosis, subject to the researcher's knowledge confirmation. Completion criterion: preserve the verified checkpoint identities and audited loss boundary; do not start a third-step label change solely to explain the now-repaired original gap. No further experiment was launched.
