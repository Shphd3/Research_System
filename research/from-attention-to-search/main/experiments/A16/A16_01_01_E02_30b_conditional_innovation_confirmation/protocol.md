---
experiment_id: A16_01_01_E02_30b_conditional_innovation_confirmation
anchor_id: 16_01_01_regret_distilled_conditional_innovation
status: approved_conditional_on_e01_pass
approved_by: user
approval_date: 2026-08-12
design_frozen_at: 2026-08-12
resource_profile: 5090-8-spot
primary_metric: document_paired_30b_endpoint_nll
---

# Protocol: A16_01_01_E02 30B Conditional-Innovation Confirmation

## 0. Approval Snapshot

**Purpose.** Test whether an E01-admitted utility-distilled conditional branch improves language modeling when jointly trained from a common Native 10B state to a 30B total-token endpoint.

**Activation condition.** This Protocol is executable only when E01 returns `PASS` with complete artifact hashes for both seeds. Smoke may be built before that verdict; long jobs may not be created before it.

**Treatment and controls.** Conditional-Utility is compared with the existing exact Native continuation, Raw-Utility, and Conditional-Haar. All start from each seed's own Native 10B checkpoint and preserve Native parameters, optimizer, scheduler, RNG, and data cursor. Existing step-0 Trainable-Innovation is an external reference only.

**Primary metric.** 30B total-token held-out NLL in nat/token on the frozen 1,024-document endpoint set; lower is better.

**Pass.** Conditional minus Native, Raw, and Haar has a paired-document 95% upper bound below zero in each seed. Missing a mechanism control narrows or rejects the corresponding claim. **Insufficient.** Any resume, data, artifact, branch, LB-gradient, checkpoint, or endpoint identity fails.

**Execution approved.** If E01 Passes, six new single-node 8×5090 jobs—Raw, Conditional, Haar for seeds 17 and 29—may be submitted without another approval. Existing Native 30B runs may be reused only after scalar, token-order, and checkpoint identity are verified.

## 1. Terminology / Definitions

- **30B endpoint:** 30,000,021,504 cumulative tokens at optimizer step 38,147; the treatment receives about 20B continuation tokens after the 10B branch point.
- **Teacher initialization:** the E01-fitted \(P,C,B_T\) installed into the dormant rank-56 branch.
- **Ramp:** branch multiplier rises linearly from 0 to 1 over the first 128 optimizer steps after 10B, about 100.7M tokens.
- **Utility preservation loss:** KL from the frozen teacher route distribution to the jointly trained route distribution; it is a regularizer, not a new forced-expert label during LM training.

## 2. Anchor Alignment

E01 establishes only frozen local expert choice. E02 addresses its strongest remaining rival: that the teacher is short-sighted or becomes obsolete when the representation, experts, and Gate jointly evolve. Endpoint NLL, rather than regret or load, decides whether the method helps training.

## 3. Tested Hypothesis

An E01-admitted Conditional-Utility branch yields lower 30B NLL than Native, Raw-Utility, and Conditional-Haar in both seeds under verified LB.

## 4. Rival Explanations

| Rival | Separator |
| --- | --- |
| Utility supervision helps but conditional residual does not | Conditional versus Raw |
| Any matched low-dimensional side path helps | Conditional versus Haar |
| Extra compute or resume state explains gain | same checkpoint/data plus measured FLOPs and exact-resume guards |
| Gain is only load redistribution | load/capacity telemetry cannot replace endpoint NLL |
| Frozen utility teacher becomes stale | regret re-audits at 20B/25B/30B and late NLL slope |

## 5. Data Construction And Provenance

Continue the verified DCLM binary stream from each seed's Native checkpoint-12716. Evaluation uses the frozen 1,024-document artifact already registered by A16_01. The E01 functional bank is disjoint and supplies only the immutable initialization artifact; it never enters LM batches or endpoint evaluation.

## 6. Learning Task And Permitted Supervision

The primary task is ordinary next-token prediction. Each online Router uses only current-layer \(x,u\) and Native logits. No online forced-expert sweep, confirmation label, taxonomy label, or future-layer state is permitted.

## 7. Model / Architecture And Frozen Variants

Every treatment retains the Native Gate and reuses its dormant rank-56 branch parameters. Raw uses \(uP\); Conditional and Haar use \(uP-xC\). \(P,C\), FIT standardizers, and a frozen copy \(B_T\) are immutable buffers reconstructed from the E01 artifact. Student branch weights \(B\) continue to train. This introduces no new trainable parameter or optimizer slot relative to the Native 10B checkpoint.

## 8. Training Objective And Optimization

All arms optimize

\[
L=L_{LM}+0.01\sum_{\ell=1}^{4}L_{SwitchLB,\ell}+0.1L_{preserve}.
\]

Native has \(L_{preserve}=0\). For treatment arms, \(L_{preserve}=KL(q_T\|p)\), where \(q_T\) is computed from the detached current Native logits plus the frozen E01 teacher branch under the same ramp, and \(p\) is the current total Router distribution. The 0.1 coefficient, 128-step ramp, AdamW state, learning-rate schedule, and all original A16 training values are frozen before execution. Backbone, experts, Native Gate, and student branch remain jointly trainable under LM+LB; the preservation loss reaches only the student branch.

## 9. Conditions, Seeds, And Checkpoints

New jobs: Raw-Utility, Conditional-Utility, and Conditional-Haar for seeds 17 and 29. Each resumes its own Native-LB `checkpoint-12716`. Checkpoints/evaluations are required at 10B branch, 15B, 20B, 25B, and 30B. Existing Native endpoints may replace new Native jobs only if the new source reproduces Native logits/loss scalar hashes and token hashes and their 10B checkpoint identities match exactly.

## 10. Primary Metric And Frozen Analysis Plan

At 30B, compute per-document NLL on the same 1,024 documents. Within each seed, pair documents and bootstrap 2,000 times. Report treatment-minus-control mean and two-sided 95% interval. Conditional supports the full method only when all three comparisons have negative estimates and upper bounds below zero in both seeds. Seeds are not pooled as independent documents.

## 11. Secondary Metrics And Guards

Report NLL trajectories; 25B-to-30B slope; tokens/FLOPs/wall-clock; LB loss and its Gate gradient; expert shares, entropy and capacity drop; branch/native logit RMS; route flips and margins during ramp; teacher KL; frozen regret at 20B/25B/30B; expert update conflict; and checkpoint/recovery identities. These metrics explain mechanisms but cannot rescue endpoint Fail.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: alpha zero must replay Native bitwise before the first continuation update.
- Known bad: artifact tampering, cross-seed checkpoint use, or resetting inherited optimizer state must fail closed.
- Known confusing: better load or regret with unchanged NLL is not a performance Pass.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Operation | Scale-up rule | Artifact |
| --- | --- | --- | --- | --- |
| S0 | verify E01 eligibility | read typed E01 verdict and hashes | Pass only | gate receipt |
| S1 | validate continuation | single-GPU install/ramp/save/resume | all guards pass | local smoke |
| S2 | validate distributed state | one 8×5090 all-arm smoke | rank, LB, data, resume agree | distributed receipt |
| S3 | submit long runs | six 5090-8-spot jobs | S0-S2 pass | job ledger |
| S4 | preserve trajectory | 15/20/25/30B evaluation and telemetry | no performance stopping | milestone artifacts |
| S5 | endpoint decision | sealed paired analysis | typed verdict | arrays, tables, figures |

## 14. Algorithm, Output, And Provenance Contract

Each job records source/config/artifact/checkpoint hashes, exact resumed optimizer step and token count, token-order hash, ramp state, student and teacher branch states, LB gradients, TensorBoard, milestones, and exact recovery. Outputs use a new root and cannot overwrite A16_01.

## 15. Success / Failure / Insufficient Evidence

- **Full Pass:** Conditional beats Native, Raw, and Haar in both seeds under the registered interval rule.
- **Narrow utility-supervision support:** Conditional and Raw beat Native but Conditional does not beat Raw.
- **No conditional-direction identity:** Conditional does not beat Haar.
- **Fail:** eligible endpoint evidence does not support a registered positive outcome.
- **Insufficient:** any validity guard or required endpoint fails.

## 16. What This Cannot Claim

Even a Full Pass cannot establish universal scale transfer, semantic hierarchy, a public spectral basis, or that expert specialization is the unique mediator of NLL.

## 17. Block Confirmation, Freeze, And Amendment Ledger

Blocks A-G are `CONFIRMED`; cross-block consistency is `PASS`. The user approved automatic long submission after smoke under the proposed gate. E02 remains fail-closed until E01 Pass. Any post-start change to objective weights, ramp, branch features, checkpoint, data, seed, metric, or verdict requires an append-only amendment. Commit, push, sync, graph edits, and publication remain unauthorized.

