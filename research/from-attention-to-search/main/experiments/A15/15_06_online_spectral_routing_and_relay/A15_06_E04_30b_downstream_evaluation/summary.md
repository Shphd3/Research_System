---
experiment_id: A15_06_E04_30b_downstream_evaluation
status: complete
scientific_verdict: fail_broad_transfer_with_task_specific_local_hmt_gains
last_updated: 2026-08-09
---

# Final result summary

## Direct conclusion

No 30B arm obtained the registered broad-transfer certificate over
Centered-Full.  Local-HMT had the highest navigation-only eight-task macro
accuracy (37.84% versus 37.33% for Centered-Full) and was higher on six tasks,
but only ARC-Easy (+1.98 points) and LAMBADA (+1.30 points) had paired 95%
intervals above zero.  Its covariance-ranked identity was not certified:
Local-HMT did not differ reliably from the motion-matched Local-Random control
on any task.

The shallow Relay also lacked downstream support.  Relay-HMT was reliably
worse than Local-HMT on ARC-Easy (-3.20 points) and LAMBADA (-1.55 points),
with no reliable positive task.  Relay-HMT did not reliably beat Relay-Random
on any task and was worse on ARC-Easy.  The evidence is therefore mixed and
task-specific, not a universal downstream winner.

## Decisive evidence

Accuracy is the fraction of benchmark examples answered correctly; higher is
better.  Each cell below is percentage accuracy.  The macro column is the
unweighted mean of eight heterogeneous tasks and is navigation only.

| Arm | ARC-C | ARC-E | HellaSwag | LAMBADA | PIQA | RACE | SIQA | WinoGrande | Macro |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Vanilla-Full | 22.70 | 39.23 | 28.79 | 24.68 | 61.04 | 25.45 | 36.23 | 51.38 | 36.19 |
| Centered-Full | 22.87 | 40.32 | 30.29 | 26.33 | **64.09** | 26.70 | 36.69 | 51.38 | 37.33 |
| Local-HMT | 22.87 | **42.30** | **30.49** | **27.63** | 62.84 | 27.27 | 36.85 | **52.49** | **37.84** |
| Local-Random | 22.95 | 41.04 | 29.98 | 26.70 | 63.98 | 26.89 | 36.23 | 49.96 | 37.22 |
| Relay-HMT | 23.98 | 39.10 | 30.01 | 26.08 | 63.22 | **28.04** | **36.90** | 50.36 | 37.21 |
| Relay-Random | **24.15** | 40.66 | 29.94 | 25.91 | 63.22 | 27.46 | 36.18 | 47.99 | 36.94 |

![Task accuracy heatmap](figures/figure1_task_accuracy_heatmap.png)

The paired item-level contrast below uses the identical benchmark items for
each arm.  A star means the 10,000-draw paired 95% interval excludes zero.

![Architecture contrasts](figures/figure4_mechanism_contrasts.png)

Centering itself has the clearest task-level evidence relative to Vanilla:
HellaSwag +1.50, LAMBADA +1.65, and PIQA +3.05 points, all with paired intervals
above zero.  This agrees qualitatively with the 30B held-out DCLM ordering, but
does not prove a shared mechanism.

## Evaluation validity and boundary

All six immutable step-38,147 checkpoints passed evaluation-mode Router guards:
native logit replay error was zero, winner agreement was 1.0, saved Router
buffers were unchanged, Local/Relay projections were active, nested bases met
the registered numerical tolerance, and Relay blocks used the saved block-1
source exactly.  Thus the negative Relay and covariance-identity readings are
not explained by silently disabling the specialized Router at evaluation.

The result is one seed, one four-layer H768 model family, eight zero-shot task
versions, and 30B training tokens.  It cannot establish universal transfer or
why a task improved.  A separate audit also established that the source runs
logged `lambda_LB=0.01` but their re-entrant checkpoint path detached the LB
auxiliary tensor from backward.  The six-model comparison remains valid, but
none of its differences may be attributed to effective LB regularization.

## Next decision

Do not extend Relay-HMT on downstream accuracy alone.  The next A15 decision is
whether a loss-aligned, expert-utility coordinate can beat both native Router
scores and matched random coordinates before any further matched training.

