# E14-P1: Supplying the teacher parent recovers most of the deployment gap

Execution: COMPLETE; eligible frozen evaluation. Registered verdict: `COARSE_CORRECTION_SUPPORTED`.
Knowledge wording: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.
[Protocol](protocol.md) · [Detailed evidence](detailed.md)

Supplying the original pseudo-teacher parent while reselecting the predicted child inside that parent recovers **98.24% and 93.96%** of the online-to-full-pseudo-teacher loss gap in seeds 17 and 29. The primary parent-correction contrast is positive with positive 95% interval lower endpoints in both seeds. No parameter was trained or updated. This is an externally supplied path intervention, not a repaired deployable Router.

## Conditions and direct result

NLL means summed answer-target negative log probability divided by answer-token count, in nats per answer token; lower is better. Each seed uses the same 512 examples and 30,442 answer tokens. “Teacher” means the original offline pseudo assignment, not ground-truth semantic labels or the historical gold Oracle model.

- A: original predicted parent and predicted child; online baseline.
- B: teacher parent and a newly selected predicted child constrained to that parent.
- C: original teacher parent and teacher child; privileged reference.
- D: teacher parent and each wrong same-parent child; average alternative losses within each example before token aggregation. Parent sizes are 3, 3, 2.

| Seed | Condition | NLL (nats/token) |
|---|---|---:|
| 17 | A | 0.845991414 |
| 17 | B | 0.806372044 |
| 17 | C | 0.805663412 |
| 17 | D | 0.824458165 |
| 29 | A | 0.827523137 |
| 29 | B | 0.805791562 |
| 29 | C | 0.804393423 |
| 29 | D | 0.824043854 |
| mean | A | 0.836757276 |
| mean | B | 0.806081803 |
| mean | C | 0.805028417 |
| mean | D | 0.824251009 |

| Seed | Contrast | Difference (nats/token) | Paired-example 95% interval |
|---|---|---:|---|
| 17 | A − B | 0.039619370 | [0.033635655, 0.046319138] |
| 17 | B − C | 0.000708633 | [0.000067915, 0.001358270] |
| 17 | D − C | 0.018794753 | [0.016071291, 0.021893043] |
| 17 | A − C | 0.040328002 | [0.034252845, 0.047382719] |
| 29 | A − B | 0.021731576 | [0.017851930, 0.026396028] |
| 29 | B − C | 0.001398138 | [0.000649159, 0.002148447] |
| 29 | D − C | 0.019650431 | [0.016726572, 0.022948563] |
| 29 | A − C | 0.023129714 | [0.019036444, 0.028061890] |

A−B measures parent correction, B−C the residual child correction, and D−C the matched-child advantage. The recovery fraction is (A−B)/(A−C), not an order-independent causal attribution. Intervals use 2,000 paired-example resamples separately for each fixed checkpoint; auxiliary intervals are descriptive.

![Frozen path intervention](figures/path_intervention.png)
How to read: the large A-to-B loss reduction appears in both seeds; the positive D-minus-C contrast shows a cost to selecting the wrong child even with the parent supplied. Fine correction remains positive, so B and C have not been established equivalent.

## Architecture finding

The historical eight-task hard-pseudo branch runs only stage 2, where auxiliary supervision reaches the child Router only. Hard forced indices and unit expert coefficients eliminate the task-loss route to parent logits. A small backward check finds no parent gradient. All seven stored snapshots, updates 1 through 128, have exactly unchanged parent weights and biases in both seeds. Child weights change by maximum absolute values 0.032013 and 0.032875.

![Historical Router parameter change](figures/architecture_weight_audit.png)
How to read: parent weight and bias changes are exactly zero; this figure describes historical parameter updates, not the performance of a newly trained Router.

This is a concrete supervision defect that must be controlled before attributing the large handoff failure to final-layer teacher semantics or inaccessible early representations. It does not establish that online parent training will recover the privileged intervention benefit. The independently staged M2D2 branch is outside this defect's audited scope.

## Eligibility and boundary

ACP job `pt-5xgwtcam` succeeded on one reserved H100. All three regression tests and the two-seed smoke passed. Full A/C per-example losses and paths exactly replay the historical arrays. Every path legality, sample identity, finiteness and frozen-parameter guard passed; optimizer updates: **0**. Earlier failed smoke runs are excluded.

The teacher uses full-sequence final-layer means and therefore privileged later context. Results concern previously examined internal eight-task answer losses, not uncontaminated benchmark generalization. The deployed Router's block input and the earlier static audit's post-attention MLP input are different objects. No layer/context intervention, new labels, gold-Oracle comparison, or deployment training was run here.

## One next decision

Choose whether step 2 should first train only the parent Router with experts and child Router frozen. AI recommendation: prioritize this minimal repair because parent correction removes most of the observed gap; retain the measured residual child gap as a later target. This training choice and its protocol remain unconfirmed; step 1 execution approval does not launch step 2.
