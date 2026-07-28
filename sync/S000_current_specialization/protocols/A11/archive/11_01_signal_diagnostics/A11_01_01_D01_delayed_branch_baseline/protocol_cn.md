# Protocol Draft: A11_01_k2_branch_delayed_next_two

状态：已批准并执行。英文 canonical `protocol.md` 已创建；本文件保留为中文 companion。

## 0. Approval Snapshot

**Approval status:** pending user review.

**Purpose:** 验证 clean K=2 branch-delayed 分布中，next-two 是否比 fixed-next-one 更直接让同一个 $h_T$ 支持 branch-specific $S_B$ 的 single-prefix prediction。

**Primary anchor:** `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_01_k2_branch_delayed_next_two_anchor_cn.md`

**Anchor decision question:** 在 $Y_1=A$ shared、$Y_2=S_B$ branch-specific 的 K=2 分布中，next-two 是否比 fixed-next-one 更强地让 $h_T$ 支持 single-prefix offset-2 prediction？

**Anchor physical prior tested:** shared $Y_1$ 不迫使 $h_T$ 区分 branch；branch-specific $Y_2$ 会通过 next-two 直接惩罚 branch-blind $h_T$。

**Anchor core model term tested:** $\lambda\mathrm{CE}(q_2(\cdot\mid h_T),S_B)$ 对 $h_T$ 的 branch-specific direct supervision。

**Anchor falsifier:** next-two 在 offset2 single-prefix accuracy、branch-swap 和 frozen probe 上不优于 capacity-matched fixed-next-one。

**Experiment role:** operationalization / proxy test. 它验证理论构造能否在最小可运行模型中显现，不是方法构造。

**Primary metric from anchor:** `offset2_single_prefix_accuracy`。

**Claim boundary from anchor:** 只能支持 controlled K=2 objective-level pressure；不能支持自然语言 MTP 优越性或 curriculum 优越性。

**Minimal setup:** clean deterministic synthetic data: `BR_b F00 ... F{L-1} U0 U1 A_SHARED S_b STOP`。

**Model architecture (fixed for this protocol):** one-layer causal Transformer (small), with separate direct projection heads for offset-1 and offset-2 under the same hidden state \(h_T\).

**Basic configuration:** `num_branches=3`，`L=8`，`shared_context_len=2`，`max_horizon=2`，`structured_probability=1.0`，`random_filler_probability=0.0`，seeds `971,972,973`。

**Conditions to run:** `direct_heads_fixed_next_one` and `direct_heads_next_two`. `standard_lm` is optional sanity check only.

**Pass:** next-two has high offset2 single-prefix accuracy, high worst-branch target probability, passes branch-swap, and has stronger frozen probe than fixed-next-one; fixed-next-one predicts $A$ but is weak/unstable on $S_B$ from $h_T$.

**Fail:** fixed-next-one matches next-two on offset2 single-prefix accuracy and frozen probe across seeds.

**Insufficient:** offset1 accuracy fails, only one seed exists, branch probabilities are highly imbalanced, or probe split is too small/overfit.

**Cannot claim:** MTP always beats NTP; NTP cannot learn long-horizon; curriculum is better than full-horizon; synthetic K=2 transfers to real LLMs.

**Approval decision:** user to approve / revise / park.

## 1. 术语解释

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| fixed-next-one | 架构有 offset 1/2 heads，但只训练 offset 1 | active loss 是 $\mathrm{CE}(q_1(\cdot|h_T),A)$ | loss condition | 控制“多了 head/capacity”解释 | 不能代表全部 NTP |
| offset-1 head | 用同一个 prefix hidden state \(h_T\) 预测 \(Y_1\) 的线性头 | \(q_1=\mathrm{softmax}(W_1h_T+b_1)\) | 概率分布 | 在共享令牌 \(A\) 上定义 next-one 的监督路径 | 不能单独说明 long-horizon 学习 |
| next-two | 同一个 $h_T$ 同时预测 offset 1/2 | active loss 是 $\mathrm{CE}(q_1(\cdot|h_T),A)+\mathrm{CE}(q_2(\cdot|h_T),S_B)$ | loss condition | 主测试条件 | 不保证优化成功 |
| offset-2 head | 用同一个 prefix hidden state \(h_T\) 预测 \(Y_2\) 的线性头 | \(q_2=\mathrm{softmax}(W_2h_T+b_2)\) | 概率分布 | 在 fixed-next-one 下不受约束，是本实验区分的关键路径 | 不能证明自然语言中一定成立 |
| offset2 single-prefix accuracy | 固定 $h_T$ 预测 $S_B$ 的 top-1 accuracy | top-1 of $q_2(\cdot|h_T)$ | 0 到 1 | primary metric | 不证明自然语言推理 |
| worst-branch probability | 最差 branch 的正确 suffix 概率 | $\min_b q_2(S_b|h_T^{(b)})$ | probability | 防止平均数遮住某个 branch 失败 | 不证明 calibration |
| branch-swap consistency | 只换 early branch token，看 suffix 预测是否切换 | `BR_b -> BR_c` then prediction should switch $S_b\to S_c$ | pass/fail or rate | 检查因果依赖早期 branch | 不排除所有 memorization |
| frozen probe | 冻结模型后从 $h_T$ 线性读出 $B$ | linear probe accuracy | 0 到 1 | 区分 head readout 和 representation 信息 | probe 成功不等于 native head 成功 |

## 2. Anchor Alignment

**Decision question:** next-two 是否比 fixed-next-one 更强地让 $h_T$ 支持 offset-2 branch-specific prediction？

**Physical prior tested:** shared $Y_1$ 不提供 branch-specific loss；branch-specific $Y_2$ 提供 direct supervision。

**Core model term tested:** offset-2 cross-entropy term $\mathrm{CE}(q_2(\cdot|h_T),S_B)$。

**Falsifier:** fixed-next-one 与 next-two 在 single-prefix offset2、branch-swap、frozen probe 上没有稳定差异。

**Claim boundary:** 只裁定 clean K=2 operationalization。

## 3. Tested Hypothesis

在 clean K=2 分布中，next-two 会比 fixed-next-one 更稳定地让 $h_T$ 暴露 branch 信息，表现为更高的 offset2 single-prefix accuracy、更高的 worst-branch probability、更好的 branch-swap consistency 和更强 frozen probe。

## 4. Rival Explanations

| Rival explanation | Protocol guard |
|---|---|
| 成功只是因为 next-two 有更多参数 | 两个条件使用同一 direct-head architecture |
| fixed-next-one 的 offset-2 head 没训练，所以 native offset2 失败不说明 representation | 使用 frozen probe $h_T\to B$ |
| rollout 成功说明已经学会 long-horizon | primary metric 使用 single-prefix offset2，不用 rollout 做主证据 |
| local context 泄露 branch | $F,U,A$ 对所有 branch 共享；做 branch-swap |
| next-two 只记住 suffix token 频率 | branch-wise probability 和 branch-swap 检查是否依赖 `BR_b` |

## 5. Data / Model / Algorithm / Objective

**Data template:**

```text
BR_b F00 F01 ... F{L-1} U0 U1 A_SHARED S_b STOP
```

**Evaluation prefix:**

```text
BR_b F00 F01 ... F{L-1} U0 U1
```

At this prefix:

```text
offset 1 target = A_SHARED
offset 2 target = S_b
```

**Model:** one-layer causal Transformer (small), with embedding + one causal self-attention block + FFN, and two direct future-prediction heads at each relevant position:

$$
q_1=\mathrm{softmax}(W_1 h_T+b_1),\quad
q_2=\mathrm{softmax}(W_2 h_T+b_2).
$$

The first approved run should use direct-head architecture only (no latent-decoder branch), with fixed-next-one and next-two differing only by active-loss terms, not by parameter count.

Model hyper-configuration for the first approved run:

- `n_layers = 1`  
- `d_model = 128`  
- `n_heads = 4`  
- `ffn_hidden = 512`  
- `dropout = 0.0`  
- `pre-LN`  
- learned token embedding + learned position embedding (`max_seq_len = 64`)  
- separate offset heads: `W_1, b_1` and `W_2, b_2` are independent  
- losses: `fixed-next-one: \lambda_1=1, \lambda_2=0`, `next-two: \lambda_1=1, \lambda_2=1`.

Training and optimization:

- optimizer: `AdamW`  
- learning rate: `1e-3`  
- betas: `(0.9, 0.95)`  
- weight decay: `0.0`  
- gradient clip: `1.0` (global norm)  
- train steps: `8000`  
- train batch size: `256`  
- eval batch size: `512`  
- LR schedule: constant (no scheduler in the first run)  

Data protocol (K=2 clean stage):

- train/val/test size per seed: `12,000 / 3,000 / 3,000`  
- random generation is deterministic per seed and cached  

Primary pass/fail is judged on all 3 seeds with the above fixed values.

### Post-review revision policy

If this approved protocol is not passed, we will keep the anchor and model form, but revise training/data settings in this order to improve identifiability of the mechanism:

1. If both fixed-next-one and next-two fail to learn (offset-1 and offset-2 weak), keep `num_branches=3` and double steps: `8000 -> 16000`; if still weak, increase data size to `20,000 / 4,000 / 4,000`.
2. If both conditions are strong but no stable gap on offset-2 metrics, increase delay context to `L=12` or `L=16` while keeping `max_horizon=2`, then test `lambda_2 in {1, 2}` to surface offset-2 pressure under fixed architecture.
3. If next-two improves offset-2 but branch-swap/probe are unstable, only refine evaluation protocol first: enlarge branch-swap pairs per sample and fix frozen-probe training protocol (more epochs, fixed regularization), while keeping model and loss settings unchanged.
4. If offset-2 head is still noisy, we do one stabilization step only: keep data and model, raise eval frequency and keep `train_batch` options `256` and `384` as a bounded comparison.

Revision rule: in each round we change at most one class of hyperparameters (training, data, or loss weighting).  
MoE, latent-decoder, curriculum, and longer-horizon extensions are not allowed until this K=2 clean protocol has a stable pass/fail pattern.

**Objectives:**

fixed-next-one:

$$
\mathcal L_{\mathrm{fixed1}}=\mathrm{CE}(q_1(\cdot\mid h_T),A).
$$

next-two:

$$
\mathcal L_{\mathrm{next2}}=\mathrm{CE}(q_1(\cdot\mid h_T),A)+\mathrm{CE}(q_2(\cdot\mid h_T),S_B).
$$

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
|---|---|---|---|---|---|---|---|---|
| `direct_heads_fixed_next_one` | next-one can be branch-blind at $T$ | capacity control | Same heads, no offset-2 loss | primary comparison | offset1 high, offset2/probe weak | matches next-two | offset1 fails | behavior + probe table |
| `direct_heads_next_two` | offset-2 direct supervision | $\mathrm{CE}(q_2,S_B)$ | Main condition | primary comparison | offset2/probe/swap high | no improvement | unstable across seeds | behavior + probe table |
| branch-swap eval | prediction depends on early branch | local leak / memorization | Guard | secondary | suffix switches correctly | no switch | probabilities low | branch-swap table |
| frozen probe | representation contains $B$ | head-only explanation | Guard | secondary | next-two probe higher | no probe gain | overfit or split too small | probe table |

**Seeds:** 971, 972, 973.

**Checkpoints:** final checkpoint plus optional early checkpoints if training curves are cheap to log.

## 7. Primary Metric

**Definition:** `offset2_single_prefix_accuracy` is the top-1 accuracy of $q_2(\cdot\mid h_T)$ on $S_B$ when the prefix stops before `A_SHARED`.

**Why it decides:** It directly tests whether the same decision hidden state $h_T$ supports the delayed branch-specific target. This is exactly the model term that next-two supervises and next-one at $T$ does not.

**False positive risk:** native offset-2 head may learn a readout without broad representation separation; frozen probe guards this.

**False negative risk:** fixed-next-one may also encode $B$ through architecture or other losses; that weakens this operationalization, not the mathematical lower-bound theorem.

## 8. Secondary Metrics

- `offset1_accuracy`: both conditions should predict shared $A$.
- `offset2_target_probability`: confidence on the correct $S_B$.
- `worst_branch_offset2_probability`: detects branch-specific brittleness.
- `branch_swap_consistency`: checks causal dependence on early branch token.
- `frozen_probe_accuracy`: checks whether $h_T$ linearly exposes $B$.
- Optional gradient variation:

$$
V_j=\mathbb E_B\left\|G_j(B)-\mathbb E_{B'}G_j(B')\right\|^2.
$$

Expected pattern: $V_2>V_1$.

## 9. Known Good / Known Bad / Known Confusing Cases

**Known good:** next-two should pass clean K=2 if implementation, head indexing, and prefix extraction are correct.

**Known bad:** if $Y_2$ is shared across branches, next-two should not improve branch probe or branch-swap.

**Known confusing:** fixed-next-one may show high frozen probe because Transformer states can retain early tokens without being forced by the local next-one objective.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
|---|---|---|---|---|---|
| data audit | Is $Y_1$ shared and $Y_2$ branch-specific? | generated samples | pass if no local leak | sample table | detailed.md |
| loss/head audit | Are offset heads and active losses correct? | training logs | pass if fixed trains only offset1 and next-two trains both | loss table | detailed.md |
| primary eval | Does $h_T$ predict $S_B$? | offset2 metrics | apply pass/fail criteria | behavior table | summary.md |
| guard eval | Is success representation/branch dependent? | probe and swap | pass if both support next-two | guard tables | summary.md |

## 11. Algorithm Specification

input: branch count, filler length, shared context tokens, suffix tokens, seeds.  
parameters: `m=3`, `L=8`, `shared_context_len=2`, `max_horizon=2`.  
intermediate variables: prefix index $T$, $h_T$, $q_1$, $q_2$, branch id $B$.  
steps: generate data, train two conditions, evaluate single-prefix metrics, fit frozen probe, run branch-swap.  
outputs: behavior table, probe table, branch-swap table, optional gradient table.  
debug artifacts: sample dump, active-loss audit, prefix-index audit.  
pass conditions: next-two passes primary and guards; fixed-next-one remains weak/unstable on delayed branch prediction.  
fail conditions: fixed-next-one matches next-two across primary and guard metrics.  
failure reasons: data leak, wrong prefix index, inactive offset-2 loss, architecture already preserving branch, or theorem operationalization too easy.

## 12. Success / Failure / Insufficient Evidence

**Success:** next-two high on offset2 single-prefix accuracy and branch-swap, with stronger frozen probe than fixed-next-one across 3 seeds.

**Failure:** fixed-next-one matches next-two on primary and guard metrics across 3 seeds.

**Insufficient:** missing seeds, failed offset1 learning, inconsistent branch-wise results, or unverified active-loss wiring.

## 13. What This Cannot Claim

- MTP always outperforms NTP.
- NTP cannot learn long-horizon dependencies.
- Curriculum is better than full-horizon.
- Synthetic K=2 proves real LLM long-range reasoning.
- Offset-2 gradient path guarantees optimization success.
- Any MoE expert specialization claim.

## 14. Review Notes And Protocol Changes

- Pending user review.
- Do not add noisy filler, longer horizon, latent decoder, curriculum, or spectral diagnostics before the clean K=2 protocol is approved and interpreted.
