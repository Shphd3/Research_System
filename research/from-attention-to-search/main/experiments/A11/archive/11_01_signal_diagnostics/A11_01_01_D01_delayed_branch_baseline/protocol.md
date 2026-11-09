# Protocol: A11_01 K=2 Branch-Delayed Next-Two

## 0. Approval Snapshot

**Approval status:** approved by user and executed on 2026-07-06.

**Purpose:** Test whether next-two prediction makes the same prefix hidden state $h_T$ support branch-specific second-token prediction better than a capacity-matched fixed-next-one objective.

**Primary anchor:** `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_01_k2_branch_delayed_next_two_anchor.md`

**Anchor decision question:** In the clean K=2 branch-delayed distribution with shared $Y_1=A$ and branch-specific $Y_2=S_B$, does next-two impose a direct branch-relevant requirement on $h_T$ that next-one at $T$ does not impose?

**Anchor physical prior tested:** A shared next token does not require $h_T$ to distinguish branches; a branch-specific second token does.

**Anchor core model term tested:** $\lambda\operatorname{CE}(q_2(\cdot\mid h_T),S_B)$.

**Anchor falsifier:** Next-two does not outperform capacity-matched fixed-next-one on single-prefix offset-2 accuracy, frozen probe, and branch-swap consistency.

**Experiment role:** operationalization / proxy test.

**Primary metric from anchor:** `offset2_single_prefix_accuracy`.

**Claim boundary from anchor:** This can support only the controlled K=2 objective-level pressure claim, not a general claim that MTP always beats NTP.

**Minimal setup:** deterministic synthetic data `BR_b F00 ... F07 U00 U01 A_SHARED S_b STOP`.

**Basic configuration:** `num_branches=3`, `filler_length=8`, `shared_context_length=2`, seeds `971,972,973`, direct heads, branch embeddings initialized identically.

**Conditions to run:** `direct_heads_fixed_next_one`; `direct_heads_next_two`.

**Pass:** next-two has high offset-2 single-prefix accuracy, high worst-branch target probability, high branch-swap consistency, and high frozen-probe accuracy; fixed-next-one predicts $A$ but remains weak on $S_B$ from $h_T$.

**Fail:** fixed-next-one matches next-two on the primary metric and guards across seeds.

**Insufficient:** offset-1 learning fails, active-loss wiring is wrong, one seed only, or next-two is unstable without a clear optimization diagnosis.

**Cannot claim:** MTP always beats NTP; NTP cannot learn long-horizon dependencies; curriculum is better than full-horizon; synthetic K=2 transfers to real LLMs.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| next-one | Predict only the first future token from $h_T$ | $\operatorname{CE}(q_1(\cdot\mid h_T),A)$ | loss | Capacity-matched control without offset-2 supervision | All NTP behavior |
| next-two | Predict the first and second future tokens from the same $h_T$ | $\operatorname{CE}(q_1,A)+\lambda\operatorname{CE}(q_2,S_B)$ | loss | Tests the direct second-token term | Optimization always succeeds |
| single-prefix offset-2 accuracy | Whether $h_T$ directly predicts $S_B$ | top-1 accuracy of $q_2(\cdot\mid h_T)$ | 0 to 1 | Primary metric for the theorem's mechanism | Natural-language reasoning |
| frozen probe | Linear readout of branch from frozen $h_T$ | linear classifier $h_T\to B$ | accuracy | Tests whether $h_T$ exposes branch information | Native head usability alone |
| branch-swap consistency | Replace only `BR_b` and check whether predicted suffix switches | predicted $S_b\to S_c$ under `BR_b -> BR_c` | rate | Guards against local-context shortcuts | All memorization routes |

## 2. Anchor Alignment

**Decision question:** Does next-two make $h_T$ support branch-specific offset-2 prediction better than fixed-next-one?

**Physical prior tested:** Shared $Y_1$ gives no branch-specific loss; branch-specific $Y_2$ does.

**Core model term tested:** $\operatorname{CE}(q_2(\cdot\mid h_T),S_B)$.

**Falsifier:** no stable next-two advantage on primary and guard metrics.

**Claim boundary:** clean K=2 operationalization only.

## 3. Tested Hypothesis

In the clean K=2 distribution, next-two will make $h_T$ expose branch information, while fixed-next-one will remain branch-blind under balanced data and identical branch-token initialization.

## 4. Rival Explanations

| Rival explanation | Protocol guard |
|---|---|
| The result comes from extra heads or capacity | Both conditions use the same direct-head architecture |
| Native offset-2 success is only a trained-head artifact | Frozen probe from $h_T$ to $B$ |
| Prediction uses local context leakage | Filler and shared context are identical across branches; branch-swap test |
| Rollout success is confused with single-prefix prediction | Primary metric uses $h_T\to S_B$ directly |

## 5. Data / Model / Algorithm / Objective

Data template:

```text
BR_b F00 F01 F02 F03 F04 F05 F06 F07 U00 U01 A_SHARED S_b STOP
```

Evaluation prefix:

```text
BR_b F00 F01 F02 F03 F04 F05 F06 F07 U00 U01
```

Model: one-layer causal Transformer with two direct heads $q_1$ and $q_2$ from the final prefix state $h_T$. Branch-token embeddings are initialized identically so that fixed-next-one has no branch-specific symmetry-breaking signal.

Objectives:

$$
\mathcal L_{\mathrm{fixed1}}=\operatorname{CE}(q_1(\cdot\mid h_T),A).
$$

$$
\mathcal L_{\mathrm{next2}}=\operatorname{CE}(q_1(\cdot\mid h_T),A)+\operatorname{CE}(q_2(\cdot\mid h_T),S_B).
$$

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Evidence role | Pass | Fail | Table |
|---|---|---|---|---|---|---|
| `direct_heads_fixed_next_one` | next-one can be satisfied by branch-blind $h_T$ | capacity control | primary comparison | offset1 high, offset2/probe/swap weak | matches next-two | `per_seed_metrics.csv` |
| `direct_heads_next_two` | second-token supervision distinguishes branches | $\operatorname{CE}(q_2,S_B)$ | primary comparison | offset2/probe/swap high | no improvement | `per_seed_metrics.csv` |
| frozen probe | representation contains branch information | head-only explanation | guard | next-two probe high | no probe gain | `per_seed_metrics.csv` |
| branch-swap | prediction depends on early branch key | local leak / shortcut | guard | suffix switches with branch token | no switch | `branch_swap.csv` |

Seeds: `971,972,973`. Final run steps: `4000`.

## 7. Primary Metric

`offset2_single_prefix_accuracy` is the top-1 accuracy of $q_2(\cdot\mid h_T)$ on $S_B$ when the prefix stops before `A_SHARED`.

It decides the judgment because it directly tests whether the same hidden state $h_T$ can predict the delayed branch-specific target.

## 8. Secondary Metrics

- `offset1_accuracy`: both conditions must predict shared $A$.
- `worst_branch_offset2_probability`: detects a failed branch hidden by the mean.
- `branch_swap_consistency`: checks causal dependence on the early branch token.
- `frozen_probe_accuracy`: checks whether $h_T$ exposes branch information.
- `hidden_pairwise_distance_min`: checks whether branch states are actually separated.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: next-two should separate branches if the offset-2 loss is active and training converges.

Known bad: fixed-next-one should stay branch-blind under balanced data and identical branch initialization.

Known confusing: short training may show partial next-two separation; this is insufficient until convergence is checked.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Evidence | Pass / fail / unclear rule | Handoff |
|---|---|---|---|---|
| data audit | Is $Y_1$ shared and $Y_2$ branch-specific? | `sample_table.csv` | pass if only suffix differs by branch | `detailed.md` |
| loss/head audit | Are the active losses different? | condition objectives and history | pass if fixed trains only offset 1 and next-two trains both | `detailed.md` |
| primary eval | Does $h_T$ predict $S_B$? | `per_seed_metrics.csv` | apply pass/fail criteria | `summary.md` |
| guard eval | Is success representation/branch dependent? | probe and swap tables | pass if both support next-two | `summary.md` |

## 11. Algorithm Specification

Input: branch count, filler length, shared context length, seeds.

Steps: build deterministic sequences; train both direct-head conditions; evaluate $q_1$, $q_2$, frozen probe, branch-swap; write tables.

Outputs: `condition_summary.csv`, `per_seed_metrics.csv`, `branch_probabilities.csv`, `branch_swap.csv`, `training_history.csv`, `sample_table.csv`, `run_manifest.json`.

## 12. Success / Failure / Insufficient Evidence

Success: next-two passes primary and guard metrics across all three seeds, while fixed-next-one remains branch-blind.

Failure: fixed-next-one matches next-two after verified loss wiring and convergence.

Insufficient: one seed only, broken offset-1 learning, or unstable next-two convergence without diagnosis.

## 13. What This Cannot Claim

This protocol cannot claim that MTP always improves language modeling, that NTP cannot learn long-horizon dependencies, that curriculum is superior, or that this synthetic mechanism transfers to real LLMs.

## 14. Review Notes And Protocol Changes

The Chinese draft `protocol_cn.md` was approved by the user. The final executed configuration used 4000 training steps after an initial 1200-step run showed partial next-two convergence on one seed.
