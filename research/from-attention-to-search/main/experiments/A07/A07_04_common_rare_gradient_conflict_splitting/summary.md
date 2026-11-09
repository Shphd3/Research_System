# Summary: A07_04 Common / Rare Gradient Conflict Splitting

Primary anchor: `../../../problem_anchors/07_features_overlap/07_04_common_rare_gradient_conflict_splitting_anchor.md`

Protocol: `protocol.md`

## Purpose

Test whether a neural MoE reduces measured high-frequency / rare feature gradient conflict, not just load imbalance.

## Exact Setup

Run: `a07_04_grad_conflict_full_20260624_1`

Seeds: `20260624-20260631`, 8 seeds.

Conditions: `dense_shared`, `random_top1_moe`, `centered_unsup_split_moe`, `oracle_split_moe`.

Data: controlled neural synthetic common/rare binary task. Train is imbalanced; evaluation is balanced. Expert utility is not hand-coded.

Execution: local full run with 4 logical shards on GPU, after a CPU full attempt was interrupted for slowness before producing full shard outputs. ACP 4-card script was dry-run only.

## Primary Metric

Primary metric: \(\Delta\mathcal{C}_{C,R}\), the reduction in routing-weighted negative gradient conflict versus `random_top1_moe`.

Required guard: rare loss must improve without common loss regression.

## Result

Judgment: insufficient evidence for the full A07_04 claim.

What passed: real neural gradient conflict was measurable, and `centered_unsup_split_moe` reduced conflict versus `random_top1_moe`.

What did not close: the rare-loss improvement was small and noisy, rare accuracy stayed low, and dense shared training had lower rare loss than the centered MoE.

Key numbers:

| Condition | Weighted conflict | Rare loss | Rare acc | Max load |
| --- | ---: | ---: | ---: | ---: |
| dense_shared | `0.9982` | `1.7321` | `0.1301` | `1.0000` |
| random_top1_moe | `0.2641` | `1.8827` | `0.1449` | `0.3630` |
| centered_unsup_split_moe | `0.2370` | `1.8195` | `0.1373` | `0.3239` |
| oracle_split_moe | `0.0000` | `0.0004` | `1.0000` | `0.5000` |

Against `random_top1_moe`, centered split has:

| Metric | Value |
| --- | ---: |
| \(\Delta\mathcal{C}_{C,R}\) | `0.0271 +/- 0.0398` |
| rare loss improvement | `0.0632 +/- 0.0617` |
| common loss regression | `-0.0046 +/- 0.0054` |

## Key Figures

### Figure: Conflict Versus Rare Loss

![Conflict versus rare loss](figures/conflict_vs_rare_loss.png)

What this tests: whether lower measured gradient conflict corresponds to lower rare loss.

Anchor question: does routing reduce common/rare gradient interference enough to improve rare learning?

Protocol question: does `centered_unsup_split_moe` reduce \(\mathcal{C}_{C,R}\) and \(L_R\) versus `random_top1_moe`?

Metric shown: routing-weighted gradient conflict and rare loss.

Metric definition: \(\mathcal{C}_{C,R}=\sum_e q_{C,e}q_{R,e}[-\cos(g_{C,e},g_{R,e})]_+\).

Data source: full run aggregate over 8 seeds.

How to read: lower-left is better. A useful split should move down and left against random top-1.

What this figure decides: whether the mechanism and rare-loss guard move together.

Observed result: centered split moves slightly left/down versus random top-1, but dense has higher conflict and lower rare loss.

Allowed claim: this run measured neural conflict and found weak partial movement in the expected direction versus random top-1.

What this does not prove: MoE partition beats dense or solves rare-feature interference.

Anchor update implication: update A07_04 as insufficient evidence, not supported.

## Claim Boundary

Can claim: the protocol can measure real neural \(C/R\) gradient conflict; centered unsupervised routing weakly reduces conflict and rare loss versus random top-1 in this proxy.

Cannot claim: functional expert specialization, dense-beating MoE benefit, real-corpus transfer, or robust rare-feature recovery.

## Next Decision

Revise the neural proxy or candidate router before using A07_04 as evidence for expert specialization.
