# 11_02 Two-Token Shared-Trunk Signal / Interference Anchor

状态：中文 companion；`decision_only` 证据已完成；`all_positions_lm_control` 尚未执行。  
父线：`11_long_horizon_mtp_objective`。  
前置证据：`11_01_k2_branch_delayed_next_two_anchor.md` 已支持 clean K=2 objective-level separation。  
源设计文档：`daily_research_reports/0707/mtp_k2/two_token_shared_trunk_theory_experiment_design.md`。

## 0. Thinking Card

**Phenomenon:** clean K=2 已经说明：当 $Y_1$ shared、$Y_2$ branch-specific 时，next-two 的 $L_2$ 可以给 $h_T$ 提供 next-one 没有的 branch-relevant supervision。但这还没有说明 $L_2$ 在真实 shared-trunk Transformer 训练中是 useful、redundant、noisy，还是 interfering。

**Mechanism guess:** $L_2$ 的作用由三个层次共同决定：数据层面 $Y_2$ 是否含有 $Y_1$ 之外的 branch 信息；表示层面 $g_2=\nabla_{\theta_s}L_2$ 是否让 $h_T$ 更可恢复 branch；优化层面 $g_2$ 是否在 shared trunk 上破坏 $g_1=\nabla_{\theta_s}L_1$ 的 next-token 更新方向。

**Key variables:** branch key $B$；prefix hidden states at multiple positions；$Y_1,Y_2$ 的信息关系；shared trunk parameters $\theta_s$；gradient pair $(g_1,g_2)$；parameter groups: embedding, shared attention, shared MLP, expert_1, expert_2, head_1, head_2。

**Causal relation:** 如果 $I(B;Y_2\mid Y_1)>0$ 且 $g_2$ 提升 branch recoverability，同时 $g_2$ 不在关键 shared parameters 上强烈反向 $g_1$，则 $L_2$ 是 useful branch signal；如果 $Y_2$ 不含新增 branch 信息或 $g_2$ 在 shared trunk 上产生强冲突，则 $L_2$ 可能 redundant、noisy 或 useful-but-interfering。

**Observable metric:** primary decision object 是 `two_token_signal_class`，由三类证据共同判定：data-regime contrast、branch representation gain、shared-gradient compatibility。第一主数值是 `A_vs_C_branch_probe_gain_at_prediction_site`。`decision_only` 结果显示这个数值必须由 `single_prefix_head2_accuracy` 和 `branch_swap_preference` guard；branch probe 不能单独作为结论。

**Rival Explanations:** $L_2$ 成功可能只是 $Y_2$ 可由 $Y_1$ 或 local context 推出；Regime C 的提升可能来自数据泄漏或 memorization；branch probe 提升可能与 usable head2 prediction 不一致；head2 成功可能牺牲 $L_1$；separate experts 若有效，可能只是参数量增加而不是减少 horizon conflict。

**Decision:** `decision_only` 当前分类为：$L_2$ 是 branch-specific useful signal，但在 shared trunk 中 branch acquisition 不稳定。这个不稳定主要表现为 $Y_2$ branch learning 不完整，不是 $L_1$ 被破坏。下一步先做 `all_positions_lm_control`，再考虑 curriculum 或 K>2。

## 1. Problem Definition

**Parent problem:** 导师要求建立 long-horizon language 与 multi-token prediction 之间的严谨联系。A11_01 已回答“是否存在 clean K=2 构造使 $L_2$ 提供 $L_1$ 没有的 branch signal”。

**Sharper subproblem:** 在最小 K=2 shared-trunk Transformer 中，判断 second-token loss $L_2$ 在不同 target-information regimes 下是 useful branch signal、redundant signal、noisy target，还是 useful but interfering gradient source。

**Decision question:** 在 K=2、one-layer causal Transformer 中，$L_2$ 的 branch-relevant signal 是否能在 shared trunk 中转化为可用表示，并且不破坏 $L_1$ 的 next-token 学习？如果发生破坏，shared-attention separate-expert 是否能定位并缓解干扰？

**Not in scope:** 重新证明 A11_01 的 objective-level separation；K>2；curriculum；MoE routing complexity；真实 LLM 长程推理；自然语言迁移；证明 MTP 普遍优于 NTP。

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
|---|---|---|---|---|---|
| 多词元预测（MTP） | 一个 prefix state 预测多个未来 token | 当前只看 $h_T\to Y_1,Y_2$ | objective family | 父问题对象 | 普遍优于 NTP |
| 下一词元预测（NTP） | 一个 prefix state 只预测下一个 token | $h_T\to Y_1$ | objective family | baseline | 不能学习 long horizon |
| shared trunk | 多个 horizon loss 共用的 causal representation path | embedding + shared attention + shared MLP 或其子集 | 参数集合 | $L_1,L_2$ 可能在这里协同或冲突 | 所有模型结构 |
| Regime A-clean | $Y_1$ shared，$Y_2$ branch-specific | $Y_1=U,\;Y_2=S_B$ | data regime | 测试 useful branch signal | shared-trunk 是否无干扰 |
| Regime B-redundant | $Y_2$ 不提供 $Y_1$ 之外的 branch 信息 | 例：$Y_1=S_B,\;Y_2=R(Y_1)$ | data regime | 测试 $L_2$ 是否只是重复 $L_1$ 信息 | $L_2$ 无优化影响 |
| Regime C-noisy | $Y_2$ 与 branch 无关或随机 | $Y_2=Z,\;Z\perp B$，train/eval 重采样 | data regime | noisy control | 所有噪声形式 |
| branch recoverability | $h$ 中 branch label 是否可读出 | frozen linear probe $h\to B$ | accuracy / CE | 表示是否保留 early branch | native head 可用 |
| branch-swap preference | 只换 early branch 后预测是否切换 | `BR_b -> BR_c` 后 $Y_2$ preference 应切到 $S_c$ | rate / logit margin | 因果 guard | 排除所有 memorization |
| gradient compatibility | $L_1,L_2$ 在同一参数组上是否协同 | $c_s,r,\rho$ | scalar | 判断 useful signal 是否伤害 shared training | 长期训练结果 |
| two_token_signal_class | 本 anchor 的分类结论 | useful / redundant / noisy / useful-but-interfering / attention-bottleneck | categorical | 总结当前实验决策 | 定理证明 |

## 2. Physical Priors

**P1: Data-information prior.**  
Meaning: $L_2$ 只有在 $Y_2$ 含有 $Y_1$ 之外的 branch 信息时，才有 principled reason 改善 long-horizon branch representation。  
Observable condition:

$$
I(B;Y_2\mid Y_1)>0.
$$

Could be wrong if: data construction leaks branch through local context, or Regime B/C 不干净。

**P2: Representation-usefulness prior.**  
Meaning: 有 branch information 的 $Y_2$ 不自动保证模型使用它；只有当 $L_2$ 的学习方向降低 branch-probe loss，才算 useful representation signal。  
Observable condition:

$$
\langle \nabla_{\theta_s}R_\phi,g_2\rangle>0,
$$

where $R_\phi=\operatorname{CE}(S_\phi(h),B)$ is branch-probe loss.

Could be wrong if: probe 训练不可靠、样本太少，或 branch information 非线性但线性 probe 看不到。

**P3: Shared-gradient compatibility prior.**  
Meaning: useful $L_2$ 仍可能伤害 $L_1$，因为 both losses update shared trunk.  
Observable condition:

$$
c_s=\frac{\langle g_1,g_2\rangle}{\|g_1\|\|g_2\|},\qquad
\rho=\frac{\langle g_1+\lambda g_2,g_1\rangle}{\|g_1\|^2}.
$$

Could be wrong if: short-run gradient conflict does not predict training degradation, or conflict is dominated by harmless head parameters.

## 3. Falsifiable Hypotheses

**H1: Useful branch-signal hypothesis.**  
Regime A-clean 中，shared-trunk two-token 应比 NTP baseline 有更高 `branch_probe_accuracy_prediction_site`、更高 `single_prefix_head2_accuracy`、更强 `branch_swap_preference`；Regime C-noisy 不应出现同样提升。  
Supported if: `A_vs_C_branch_probe_gain_at_prediction_site > 0` 且 A-clean head2/swap 高、C-noisy 接近 chance。  
Weakened if: Regime A 和 Regime C 表现相同，或 C-noisy 也产生 branch gain。

**H2: Redundancy hypothesis.**  
Regime B-redundant 中，$Y_2$ 不应提供明显超过 $Y_1$ 的新增 branch representation gain；head2 可以好，但 branch gain 不应显著超过 NTP 的 $Y_1$ branch signal。  
Supported if: B 中 `branch_probe_gain` 小于 A，且 `single_prefix_head2_accuracy` 的提升主要伴随 head1/local prediction。  
Weakened if: B 与 A 一样提升 branch representation，说明 Regime B 构造不够 redundant，或 $L_2$ 有非预期优化效应。

**H3: Shared-trunk acquisition-interference hypothesis.**  
在 Regime A-clean 中，$L_2$ 可以是 useful branch signal，但 shared parameters 未必能稳定获得这个 signal。失败可以表现为 $L_1$ 变差，也可以表现为 $L_1$ 已经解了但 $Y_2$ branch learning 长期停在 partial partition。  
Supported if: branch metrics across seeds 不稳定或 partial，同时 critical shared groups show $c_s<0$ or $\rho<1$.  
Weakened if: branch metrics 稳定高、$L_1$ 不下降，并且没有 destructive shared-gradient evidence。

**H4: Expert-separation localization hypothesis.**  
H4 不是第一步判断 next-two 是否造成 shared-trunk gradient interference；这个由 H3 判断。H4 的问题是：如果 H3 显示存在 useful-but-interfering 的 $L_2$，那么 shared-attention separate-expert 是否能定位并缓解 MLP/expert 子空间中的有害干扰。  
Supported if: separate-expert improves `L1_structured_loss` relative to shared-trunk two-token without reducing `single_prefix_head2_accuracy`, and expert parameter conflict disappears by construction.  
Weakened if: separate-expert 与 shared-trunk 同样伤害 $L_1$，且 conflict 仍集中在 shared attention / embedding。

**H5: Diagnostic validity hypothesis.**  
Regime C-noisy 应主要通过 head2 判断为 useless/noisy：head2 accuracy 应接近 noise chance，并且 branch-swap 不适用。branch probe 是表示诊断，不是充分 validity test。  
Supported if: C-noisy head2 仍接近 chance，且无法通过 swap。  
Weakened if: C-noisy head2 学到 branch-specific target，说明数据泄漏、memorization 或构造失效。

## 4. Mathematical Model

### 4.1 Sequence regimes

Let $B\sim\operatorname{Unif}\{1,\ldots,M\}$ and let the prediction prefix end at $T$:

$$
h_T=f_{\theta_s}(X_{\le T}).
$$

All regimes share an early branch token and shared local context:

$$
X_{\le T}=(\operatorname{BR}_B,F_1,\ldots,F_L,U_1,\ldots,U_s).
$$

**Regime A-clean: useful second-token branch signal**

$$
Y_1=U,\qquad Y_2=S_B,\qquad I(B;Y_2\mid Y_1)=H(B).
$$

Purpose: reproduce the clean K=2 data condition, but now measure shared-trunk diagnostics.

**Regime B-redundant: second token adds little branch information beyond $Y_1$**

$$
Y_1=S_B,\qquad Y_2=R(S_B),\qquad I(B;Y_2\mid Y_1)=0.
$$

Here $R$ is a deterministic one-to-one or many-to-one local continuation rule from $Y_1$ to $Y_2$. Purpose: $Y_2$ may be predictable, but it should not add new branch information beyond $Y_1$.

**Regime C-noisy: second token is branch-independent**

$$
Y_1=U,\qquad Y_2=Z,\qquad Z\perp B.
$$

For implementation, $Z$ must be sampled with train/eval separation so that the model cannot solve C by memorizing fixed branch-noise pairs.

### 4.2 Objectives

NTP baseline:

$$
L_{\mathrm{NTP}}=L_1=\operatorname{CE}(p^{(1)}_\theta(Y_1\mid h_T),Y_1).
$$

Shared-trunk two-token:

$$
L_{\mathrm{2tok}}=L_1+\lambda L_2
=\operatorname{CE}(p^{(1)}_\theta(Y_1\mid h_T),Y_1)
+\lambda\operatorname{CE}(p^{(2)}_\theta(Y_2\mid h_T),Y_2).
$$

Shared-attention separate-expert:

$$
a_T=f_{\theta_{\mathrm{attn}}}(X_{\le T}),
$$

$$
h_T^{(1)}=e_1(a_T),\qquad h_T^{(2)}=e_2(a_T),
$$

$$
L_{\mathrm{sep}}=
\operatorname{CE}(p^{(1)}_\theta(Y_1\mid h_T^{(1)}),Y_1)
+\lambda\operatorname{CE}(p^{(2)}_\theta(Y_2\mid h_T^{(2)}),Y_2).
$$

### 4.3 Gradient diagnostics

For shared parameters $\theta_s$:

$$
g_1=\nabla_{\theta_s}L_1,\qquad g_2=\nabla_{\theta_s}L_2.
$$

For each parameter group $G$:

$$
c_s(G)=\frac{\langle g_1^G,g_2^G\rangle}{\|g_1^G\|\|g_2^G\|},
$$

$$
r(G)=\frac{\|g_2^G\|}{\|g_1^G\|},
$$

$$
\rho(G)=\frac{\langle g_1^G+\lambda g_2^G,g_1^G\rangle}{\|g_1^G\|^2}.
$$

Interpretation:

- $c_s(G)<0$ means local gradient conflict in group $G$.
- $r(G)\gg 1$ means second-token gradient may dominate the update.
- $\rho(G)<1$ means $L_2$ weakens the $L_1$ direction; $\rho(G)<0$ means it reverses it.

### 4.4 Primary decision object

Define:

$$
\Delta_{\mathrm{probe}}(R,C)
=\operatorname{ProbeAcc}_{R,C}^{\mathrm{2tok}}-\operatorname{ProbeAcc}_{R,C}^{\mathrm{NTP}},
$$

where $R$ is regime and $C$ is position.

The first primary score is:

$$
\operatorname{A\_vs\_C\_branch\_probe\_gain}
=\Delta_{\mathrm{probe}}(\mathrm{A},\mathrm{prediction\_site})
-\Delta_{\mathrm{probe}}(\mathrm{C},\mathrm{prediction\_site}).
$$

This score tests whether $L_2$ produces branch gain specifically when $Y_2$ carries branch information, rather than merely adding arbitrary auxiliary loss.

The final categorical result is `two_token_signal_class`:

| Class | Meaning |
|---|---|
| useful | A-clean improves branch metrics; C-noisy does not; no material $L_1$ harm |
| useful-but-acquisition-unstable | A-clean 的 $L_2$ 是真实 branch signal，但 shared trunk branch acquisition seed-unstable 或 partial，同时 $L_1$ 已解 |
| useful-but-interfering | A-clean improves branch metrics but harms $L_1$ with negative shared-gradient evidence |
| redundant | B-redundant behaves like A or accounts for gains through $Y_1$ / local predictability |
| noisy | C-noisy produces no branch gain and may show unstable or high-norm $g_2$ |
| attention-bottleneck | separate-expert does not help and conflict remains in shared attention / embedding |
| invalid | C-noisy or branch-swap reveals leakage / memorization |

## 5. Computational Realization

**Experiment role:** root-cause / metric audit for two-token training dynamics after A11_01 closed the clean objective-level separation.

**Code boundary:** create a new runner; do not overwrite A11_01.

Expected path:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_02_two_token_shared_trunk_signal_interference.py
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_02_two_token_shared_trunk_signal_interference.json
Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/
```

**Data variables to review before protocol:**

| Variable | Proposed value / rule | Why it matters |
|---|---|---|
| `num_branches` | 3 to 8; first run 4 or 6 | enough chance baseline without expensive runs |
| `filler_length` | 16 to 64; first run 16 | tests branch retention across delay |
| `shared_context_length` | 4 | forces ambiguous local context |
| Regime A-clean | $Y_1=U$, $Y_2=S_B$ | clean useful signal |
| Regime B-redundant | $Y_1=S_B$, $Y_2=R(S_B)$ | $Y_2$ adds no branch info beyond $Y_1$ |
| Regime C-noisy | $Y_1=U$, $Y_2=Z\perp B$ | noisy control |
| branch init | first protocol should allow normal random init and optional tied-branch control | separates natural identity leakage from objective pressure |
| train/eval split | required, especially for C-noisy and probe | prevents memorization |

**Model conditions:**

| Condition | Required in first protocol | Purpose |
|---|---|---|
| `ntp_baseline` | yes | true one-head $L_1$ baseline |
| `shared_trunk_two_token` | yes | ordinary two-token shared-trunk interaction |
| `shared_attention_separate_expert` | yes | localize MLP/expert interference |
| `fully_separated_control` | optional / park unless needed | upper bound on separation benefit |

**Representation probe positions:**

| Position name | Concrete position |
|---|---|
| `after_branch_token` | immediately after `BR_b` |
| `middle_filler` | halfway through filler |
| `shared_local_context` | after shared context but before decision endpoint |
| `prediction_site` | prefix endpoint before $Y_1$ |

**Gradient parameter groups:**

```text
embedding
shared_attention
shared_mlp
expert_1
expert_2
head_1
head_2
```

For `ntp_baseline`, groups without $L_2$ are logged as not applicable. For `shared_trunk_two_token`, `expert_1/expert_2` are not applicable. For `shared_attention_separate_expert`, shared attention and embeddings remain shared; expert groups are horizon-specific.

**Expected artifacts:**

```text
protocol.md
summary.md
detailed.md
tables/per_seed_metrics.csv
tables/regime_condition_summary.csv
tables/probe_by_position.csv
tables/gradient_profile.csv
tables/branch_swap.csv
tables/refinement_metrics.csv
figures/optional_decision_panel.png
```

## 6. Minimal Falsification Tests

| Test | Question | Intervention / comparison | Primary metric | Pass | Fail | Failure meaning |
|---|---|---|---|---|---|---|
| Data-regime specificity | Is $L_2$ useful only when $Y_2$ carries branch information? | A-clean vs C-noisy under shared-trunk two-token and NTP | `A_vs_C_branch_probe_gain_at_prediction_site` | A improves, C does not | A and C same | $L_2$ branch usefulness not established or data leaks |
| Redundancy control | Does $Y_2$ add branch information beyond $Y_1$? | B-redundant vs A-clean | B branch gain lower than A; B explained by $Y_1$ | B behaves like redundant control | B equals A without explanation | Regime B not clean or $L_2$ has extra effect |
| Interference audit | Does useful $L_2$ harm $L_1$ in shared trunk? | shared-trunk two-token vs NTP in A-clean | `L1_structured_loss_delta`, $c_s$, $\rho$ | branch gain without $L_1$ harm, or measurable useful-but-interfering class | no branch gain or unexplained $L_1$ harm | shared-trunk interaction unresolved |
| Expert localization | Does separate expert reduce MLP/expert conflict? | separate-expert vs shared-trunk two-token | $L_1$ preservation + head2/probe retention | separate-expert preserves $L_1$ and branch metrics | no improvement; attention conflict persists | bottleneck likely shared attention / embedding |
| Diagnostic validity | Does noisy control stay noisy? | C-noisy branch metrics and swap | head2/probe/swap near chance | C remains chance | C branch gain high | leakage, memorization, or invalid metric |

## 7. Current Evidence

**A11_01 baseline evidence:** clean A-style K=2 with tied branch initialization supports objective-level mechanism。Fixed-next-one solved $A$ but stayed branch-blind；next-two predicted $S_B$ and passed prediction-site probe/swap。

**A11_02 `decision_only` evidence:** 第一版 A11_02 已运行 A/B/C regimes、三种 model conditions、两种 branch-init modes、5 个 seeds。当前分类：

```text
two_token_signal_class = useful branch signal with shared-trunk acquisition instability
```

关键事实：

| Observation | Evidence | Meaning |
|---|---|---|
| `A_vs_C_branch_probe_gain_at_prediction_site` 为正 | identical init `0.25`; random init `0.50` | A-clean 有超过 noisy auxiliary loss 的 branch signal |
| A-clean shared trunk 不稳定 | identical init head2/probe/swap mean `0.65`; random init `0.90` | $L_2$ useful 但 shared trunk acquisition 不可靠 |
| 12000 步诊断仍失败 | identical seeds 973/975 仍 `0.25`; random seed 973 仍 `0.50` | 不是简单 4000 步训练不够 |
| A-clean $L_1$ 已解 | $Y_1$ accuracy `1.00`; $L_1$ near zero | 不能说本轮中 $L_2$ 伤害了 $L_1$ |
| separate expert 修复 constrained A-clean | identical init mean 从 `0.65` 到 `1.00` | MLP/expert sharing 是 plausible bottleneck |
| C-noisy head2 仍 chance | head2 about `0.066-0.071`, chance about `0.0625` | noisy target 没被学会 |
| C-noisy probe 可高 | separate-expert probe `0.80/0.95` while head2 chance | branch probe alone 不是充分 metric |

Evidence links:

- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/tables/`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_01_k2_branch_delayed_next_two_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`
- `daily_research_reports/0707/mtp_k2/two_token_shared_trunk_theory_experiment_design.md`

## 8. Claim Boundary And Next Decision

**Can claim now:** A11_01 supports clean K=2 objective-level mechanism。A11_02 `decision_only` 进一步说明：在 controlled shared-trunk Transformer 中，A-clean 的 $L_2$ 是 branch-specific useful signal，但 shared trunk 不稳定地获得这个 signal；separate expert 将 constrained-init failure 的主要部分定位到 MLP/expert sharing。

**Cannot claim now:** 本轮不能声称 $L_2$ 伤害 $L_1$；不能声称 all-position LM-style training 同样成立；不能推出 K>2 / curriculum；不能推出自然语言 long-horizon reasoning 改善；不能声称 expert separation 是一般方法优势；不能完全判定 shared attention 是否 bottleneck。

**Next decision:** 实现并运行 `all_positions_lm_control`，保持同一 A/B/C regimes、model conditions、seeds 和 parameter-unification contract。关闭 objective-scope boundary 前，不进入 curriculum 或 K>2。
