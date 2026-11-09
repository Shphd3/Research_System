# Protocol: A11_02 Two-Token Shared-Trunk Signal / Interference

状态：已批准第一轮 `decision_only` 实验；`decision_only` 已在 2026-07-07 执行。`all_positions_lm_control` 尚未执行。

## 0. Approval Snapshot

**Approval status:** approved for `decision_only`; executed on 2026-07-07.

**Purpose:** 判定 K=2 two-token loss $L_2$ 在 shared-trunk Transformer 中是 useful branch signal、redundant signal、noisy target，还是 useful-but-interfering gradient source。

**Primary anchor:** `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_02_two_token_shared_trunk_signal_interference_anchor.md`

**Anchor decision question:** 在 K=2 one-layer causal Transformer 中，$L_2$ 的 branch-relevant signal 是否能转化为可用 shared-trunk representation，并且不破坏 $L_1$ 的 next-token 学习？如果破坏，shared-attention separate-expert 是否能定位并缓解干扰？

**Anchor physical priors tested:** data-information prior；representation-usefulness prior；shared-gradient compatibility prior。

**Anchor core model terms tested:** $I(B;Y_2\mid Y_1)$, branch probe from hidden states, and parameter-group gradient metrics $c_s,r,\rho$ for $g_1=\nabla L_1$ and $g_2=\nabla L_2$.

**Anchor falsifier:** Regime A-clean and Regime C-noisy behave the same; or $L_2$ improves neither head2 branch prediction nor branch probe; or noisy control shows branch gain; or separate expert fails to reduce any measured interference when interference is present.

**Experiment role:** root-cause / metric audit. It is not method construction and not a curriculum experiment.

**Primary decision object:** `two_token_signal_class`.

**First primary metric:** `A_vs_C_branch_probe_gain_at_prediction_site`.

**Claim boundary from anchor:** Only classifies K=2 shared-trunk two-token dynamics in controlled synthetic regimes. It cannot claim MTP universally improves NTP, cannot claim K>2 behavior, and cannot claim natural-language transfer.

**Minimal setup:** one-layer causal Transformer; three data regimes; three model conditions; multiple seeds；主实验使用 `objective_scope=decision_only`；no curriculum；no K>2。

**Basic configuration to audit:** `num_branches=4`, `filler_length=16`, `shared_context_length=4`, `lambda_offset2=1.0`, seeds at least `5`, normal random branch init plus identical branch-token init。数值配置已由用户在 2026-07-07 审核支持。所有非目标变量必须在比较中统一。

**Data regimes:**

- `A_clean`: $Y_1=U$, $Y_2=S_B$.
- `B_redundant`: $Y_1=S_B$, $Y_2=R(S_B)=T_B$，其中 $R(S_b)=T_b$ 是固定的一一 local continuation map。
- `C_noisy`: $Y_1=U$, $Y_2=Z$，其中 $Z\perp B$，并且 $Z$ 从固定 noise-token distribution $P_Z$ 中按 occurrence 独立采样。

**Model conditions to run:**

- `ntp_baseline`: one head, $L_1$ only.
- `shared_trunk_two_token`: shared attention + shared MLP, two heads, $L_1+\lambda L_2$.
- `shared_attention_separate_expert`: shared attention, horizon-specific experts, two heads.

**Pass:** Regime A-clean gives branch probe/head2/swap gain over NTP, Regime C-noisy does not, and gradient metrics either show no material interference or identify useful-but-interfering behavior; if interference appears, separate-expert improves $L_1$ preservation without losing branch metrics.

**Fail:** Regime A-clean does not improve branch probe/head2/swap; or Regime C-noisy improves similarly; or gradient metrics do not explain observed $L_1$ degradation; or separate-expert does not reduce interference while conflict remains unexplained.

**Insufficient:** data audit fails, active loss/head wiring is wrong, probe split is too small, C-noisy can be memorized, gradient profiling changes training, or too few seeds finish.

**Cannot claim:** curriculum works; K>2 works; natural-language long-horizon reasoning improves; expert separation is generally useful; MTP always beats NTP.

**Approval decision:** 第一轮 `objective_scope=decision_only` 已批准并执行。下一步需要决定是否实现并运行 `all_positions_lm_control`。

## 1. 术语解释

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| `two_token_signal_class` | 本实验最终分类 | useful / redundant / noisy / useful-but-interfering / attention-bottleneck / invalid | categorical | 决定下一步研究路线 | 定理证明 |
| `A_vs_C_branch_probe_gain_at_prediction_site` | A-clean 相对 C-noisy 的 branch probe 特异提升 | $\Delta_{\mathrm{probe}}(A,T)-\Delta_{\mathrm{probe}}(C,T)$ | accuracy delta | 判断 $L_2$ 是否是 branch-specific useful signal | head2 是否可用 |
| `single_prefix_head2_accuracy` | 从同一 $h_T$ 用 head2 预测 $Y_2$ | top-1 accuracy | 0 到 1 | 测试 $L_2$ 目标是否可用 | representation 必然含 branch |
| `branch_swap_preference` | 只换 early branch 后 head2 是否偏向新 suffix | swap success / logit margin | 0 到 1 or margin | 因果 guard | 排除所有记忆 |
| `branch_probe_accuracy` | 从 frozen hidden state 线性读出 branch | linear probe accuracy | 0 到 1 | 判断 branch 是否保留在 hidden state | native head 可用 |
| `branch_probe_cross_entropy` | branch probe 的 CE | $\operatorname{CE}(S_\phi(h),B)$ | loss | 比 accuracy 更敏感 | 非线性可读性 |
| $c_s$ | $L_1,L_2$ 梯度 cosine | $\langle g_1,g_2\rangle/(\|g_1\|\|g_2\|)$ | -1 到 1 | 判断 shared parameter conflict | 训练结果因果充分性 |
| $r$ | $L_2$ 梯度相对 $L_1$ 的 norm | $\|g_2\|/\|g_1\|$ | ratio | 判断 $L_2$ 是否主导更新 | 梯度方向是否有用 |
| $\rho$ | combined update 保留 $L_1$ 方向程度 | $\langle g_1+\lambda g_2,g_1\rangle/\|g_1\|^2$ | scalar | 判断 $L_2$ 是否削弱 next-token update | 长期泛化 |
| `init_mode=random` | 标准随机初始化 | branch-token embeddings 独立初始化 | condition label | 测试现象是否在普通初始化下存在 | clean objective-only mechanism |
| `init_mode=identical_branch` | 对称控制初始化 | 所有 `BR_b` token embeddings 初始相同，但训练中仍可更新 | condition label | 防止 fixed-next-one 利用随机 branch identity leakage | 随机初始化鲁棒性 |
| `loss_site=prediction_site` | 唯一产生训练 loss 的位置 | $Y_1$ 之前的最终 prefix hidden state | position label | 保持目标和理论一致 | 全 token LM 训练 |
| `objective_scope=decision_only` | 只在 decision prefix 上产生训练 loss | loss 只在 `prediction_site` 计算 | condition label | 直接测试 $h_T\to(Y_1,Y_2)$ | 标准 LM 训练行为 |
| `objective_scope=all_positions_lm_control` | 所有合法位置都产生 LM-style loss | 对合法 token positions 求平均 loss | optional condition | 测试结论是否能承受 background LM loss | 干净理论隔离 |
| parameter unification | 所有非目标因素固定 | 同一比较内 data/model/optimizer/seeds/eval contract 一致 | implementation rule | 防止隐藏混杂因素 | 所有实现漂移 |
| `fully_separated_control` | 两个 horizon 没有共享表示路径 | horizon-1 和 horizon-2 各自独立 trunk | optional condition | 判断完全移除共享干扰时的上界 | 公平容量匹配方法比较 |

## 2. Anchor Alignment

**Decision question:** $L_2$ 在 K=2 shared trunk 中是 useful、redundant、noisy，还是 interfering？

**Physical priors tested:** data-level branch information; representation gain; shared-gradient compatibility.

**Core model terms tested:** $I(B;Y_2\mid Y_1)$, branch probe loss, $c_s,r,\rho$.

**Falsifier:** A-clean and C-noisy are indistinguishable, or C-noisy shows branch gain, or gradient diagnostics do not explain observed interference.

**Claim boundary:** K=2 synthetic shared-trunk dynamics only.

## 3. Tested Hypotheses

**H1:** A-clean two-token improves branch representation and head2 prediction; C-noisy does not.  
**H2:** B-redundant does not add branch gain beyond what $Y_1$ already supplies.  
**H3:** If A-clean $L_2$ improves branch metrics but hurts $L_1$, negative $c_s$ or low $\rho$ should identify the shared parameter group causing interference.  
**H4:** If interference is mainly in MLP/expert parameters, shared-attention separate-expert should preserve $L_1$ while retaining head2/probe gains.  
**H5:** C-noisy should remain chance on branch-specific metrics; otherwise the setup is invalid.

## 4. Rival Explanations

| Rival explanation | Protocol guard |
|---|---|
| $L_2$ success is local/redundant, not branch-specific | Regime B-redundant |
| $L_2$ success is arbitrary auxiliary loss | Regime C-noisy |
| branch metric improvement is probe-only artifact | require head2 accuracy and branch-swap preference |
| head2 success hurts $L_1$ | track `L1_structured_loss_delta` and $\rho$ |
| separate experts help only by extra parameters | compare to shared-trunk and inspect where gradient conflict disappears |
| noisy target is memorized | train/eval resampling for C-noisy and held-out probe/eval split |

## 5. Data / Model / Objective

**Shared prefix:**

```text
BR_b F_1 ... F_L U_1 U_2 U_3 U_4
```

**Regime A-clean:**

$$
Y_1=U,\qquad Y_2=S_B.
$$

**Regime B-redundant:**

$$
Y_1=S_B,\qquad Y_2=R(S_B)=T_B,\qquad R(S_b)=T_b.
$$

这里 $S_b$ 和 $T_b$ 是两组 branch-indexed unique tokens。$Y_2$ 单独看可以是 branch-specific，但在 $Y_1$ 已知之后不再增加关于 $B$ 的信息：

$$
I(B;Y_2\mid Y_1)=0.
$$

**Regime C-noisy:**

$$
Y_1=U,\qquad Y_2=Z,\qquad Z\sim P_Z,\qquad Z\perp B.
$$

$P_Z$ 在 train/eval 中固定，但每个 occurrence 都重新独立采样 $Z$。不要创建固定 branch-to-noise 或 prefix-to-noise table。

**Objectives:**

NTP:

$$
L_{\mathrm{NTP}}=L_1.
$$

Shared-trunk two-token:

$$
L_{\mathrm{2tok}}=L_1+\lambda L_2.
$$

Separate-expert:

$$
L_{\mathrm{sep}}=\operatorname{CE}(p^{(1)}(Y_1\mid h_T^{(1)}),Y_1)+\lambda\operatorname{CE}(p^{(2)}(Y_2\mid h_T^{(2)}),Y_2).
$$

### 5.1 Loss Sites And Optimization Targets

主实验使用 `objective_scope=decision_only`：训练 loss 只在最终 prefix state，即 `prediction_site` 上计算；这个位置紧挨着 $Y_1$ 之前。`after_branch_token`、`middle_filler`、`shared_local_context` 只是诊断位置，不产生 main-model training loss。

对 `ntp_baseline`：

$$
L_{\mathrm{active}}=L_1=\operatorname{CE}(p^{(1)}(Y_1\mid h_T),Y_1).
$$

没有 $L_2$ 梯度参与优化。实现上优先使用真正 one-head model；如果为了代码对齐保留 second head，则 second-head loss weight 为 0，不参与优化。

对 `shared_trunk_two_token`：

$$
L_{\mathrm{active}}=L_1+\lambda L_2,
$$

其中

$$
L_2=\operatorname{CE}(p^{(2)}(Y_2\mid h_T),Y_2).
$$

两个 heads 读取同一个 $h_T$。$L_1$ 和 $L_2$ 都更新 embedding、shared attention、shared MLP；每个 loss 还更新自己的 head。

对 `shared_attention_separate_expert`：

$$
L_{\mathrm{active}}=L_1+\lambda L_2.
$$

$L_1$ 更新 embedding、shared attention、expert_1、head_1。$L_2$ 更新 embedding、shared attention、expert_2、head_2。因此这个条件可以减少 MLP/expert 干扰，但不能移除 embedding 或 shared-attention 干扰。

branch-probe loss 只在 frozen hidden states 上训练 probe，不更新主模型。gradient profiling 只为测量分别计算 $g_1$ 和 $g_2$，随后清空梯度，再执行正常 training update。

可选 LM-style robustness control：

给定完整序列 $x_0,\ldots,x_{N-1}$，定义合法位置集合 $\mathcal P_1=\{t:t+1<N\}$ 和 $\mathcal P_2=\{t:t+2<N\}$。则：

$$
L_{\mathrm{allpos}}^{(1)}=\frac{1}{|\mathcal P_1|}\sum_{t\in\mathcal P_1}
\operatorname{CE}(p^{(1)}(x_{t+1}\mid h_t),x_{t+1}),
$$

$$
L_{\mathrm{allpos}}^{(2)}=\frac{1}{|\mathcal P_2|}\sum_{t\in\mathcal P_2}
\operatorname{CE}(p^{(2)}(x_{t+2}\mid h_t),x_{t+2}).
$$

`objective_scope=all_positions_lm_control` 对 NTP 使用 $L_{\mathrm{active}}=L_{\mathrm{allpos}}^{(1)}$，对 two-token models 使用 $L_{\mathrm{active}}=L_{\mathrm{allpos}}^{(1)}+\lambda L_{\mathrm{allpos}}^{(2)}$。这是 secondary robustness control。primary evaluation 仍然看 `prediction_site` 的 branch metrics。

如果 all-position control 改变定性结论，则允许 claim 必须收窄为：$L_2$ 在 decision-site objective 下有用/干扰，而不能推广到 LM-style background training。

### 5.2 Parameter Unification Contract

所有实验只能改变命名变量。固定变量：

```text
num_branches = 4
filler_length = 16
shared_context_length = 4
lambda_offset2 = 1.0
seeds = every compared condition uses the same 5 seeds
model depth / width / attention heads / dropout = same across matched conditions
optimizer / learning rate / weight decay / training steps = same across matched conditions
probe training config = same across matched conditions
gradient profiling interval = same across matched conditions
train/eval split and data generator seed policy = same across matched conditions
```

允许改变的变量：

```text
data_regime: A_clean / B_redundant / C_noisy
model_condition: ntp_baseline / shared_trunk_two_token / shared_attention_separate_expert
init_mode: random / identical_branch
objective_scope: decision_only / all_positions_lm_control
```

Loss scale control：如果运行 `all_positions_lm_control`，每个 horizon loss 必须先对 active positions 求平均，再乘 $\lambda$。否则改变的是 gradient scale，不只是 objective scope。

Capacity caveat：`shared_attention_separate_expert` 有额外 horizon-specific parameters。它是 localization diagnostic，不是公平方法性能比较。`fully_separated_control` 容量差异更大，因此继续暂缓。

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Rival explanation | Evidence role | Pass | Fail | Insufficient | Table |
|---|---|---|---|---|---|---|---|
| `A_clean x ntp_baseline` | baseline branch retention | NTP may already encode branch | primary baseline | solves $Y_1$ | fails $Y_1$ | unstable | `per_seed_metrics.csv` |
| `A_clean x shared_trunk_two_token` | useful $L_2$ signal | no branch signal | primary | head2/probe/swap high | no gain | partial seeds | `regime_condition_summary.csv` |
| `A_clean x shared_attention_separate_expert` | interference localization | expert separation useless | secondary/conditional | preserves $L_1$ and branch metrics | no improvement | no interference to localize | `regime_condition_summary.csv` |
| `B_redundant x all conditions` | redundancy control | $L_2$ is deterministic after $Y_1$ | guard | branch gain explained by $Y_1$ | acts like A without explanation | B invalid | `regime_condition_summary.csv` |
| `C_noisy x all conditions` | noisy control | leakage / arbitrary auxiliary gain | guard | branch metrics near chance | branch gain high | memorization risk | `regime_condition_summary.csv` |
| gradient profiling | shared conflict | hidden interference | diagnostic | $c_s,r,\rho$ explain $L_1$ delta | no relation | profiling alters training | `gradient_profile.csv` |
| `all_positions_lm_control` | objective-scope robustness | prefix-only objective may be artificial | secondary/conditional | same qualitative class as decision-only | class changes | too expensive / unstable | `objective_scope_summary.csv` |

Seeds: proposed `5` seeds.  
Checkpoints: final plus profiling every fixed interval, e.g. every `200` steps.

## 7. Primary Metric

The first primary metric is `A_vs_C_branch_probe_gain_at_prediction_site`:

$$
\Delta_{\mathrm{probe}}(A,T)-\Delta_{\mathrm{probe}}(C,T).
$$

It decides whether $L_2$ improves branch representation specifically when $Y_2$ carries branch information. It is primary because it separates useful branch signal from arbitrary auxiliary loss.

False positive risk: probe-only improvement without usable prediction. Guard: `single_prefix_head2_accuracy` and `branch_swap_preference`.

False negative risk: NTP already encodes branch under random initialization. Guard: identical branch-token initialization and multi-position probes.

## 8. Secondary Metrics

- `single_prefix_head2_accuracy`
- `single_prefix_joint_two_token_accuracy`
- `branch_swap_preference`
- `branch_probe_accuracy_by_position`
- `branch_probe_cross_entropy_by_position`
- `L1_structured_loss`
- `L2_structured_loss`
- `L1_global_loss`
- `L2_global_loss`
- `gradient_cosine_c_s_by_group`
- `gradient_norm_ratio_r_by_group`
- `rho_update_preservation_by_group`

## 9. Known Good / Known Bad / Known Confusing Cases

**Known good:** A-clean should reproduce the A11_01 direction in the shared-trunk two-token condition.

**Known bad:** C-noisy should not improve branch metrics; if it does, the experiment is invalid or leaking branch information.

**Known confusing:** B-redundant can have high head2 accuracy because $Y_2$ is predictable from $Y_1$ or branch-labeled $Y_1$; this should not be interpreted as new branch information from $L_2$.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
|---|---|---|---|---|---|
| data audit | Are A/B/C regimes correct? | sample table + mutual-information contract | fail if C leaks branch or B adds branch info | `sample_table.csv` | `detailed.md` |
| loss/head audit | Are active objectives correct? | active loss table | fail if NTP has head2 loss or two-token lacks L2 | `training_history.csv` | `detailed.md` |
| primary eval | Is A gain specific vs C? | probe/head2/swap | pass if A improves and C does not | result tables | `summary.md` |
| gradient eval | Is interference measured by group? | $c_s,r,\rho$ | pass if metrics explain $L_1$ delta | `gradient_profile.csv` | `detailed.md` |
| expert eval | Does separate expert localize conflict? | condition comparison | pass if $L_1$ preserved and branch metrics retained | summary table | `summary.md` |

## 11. Algorithm Specification

Input: regimes, branches, filler length, shared context length, model condition, seed, $\lambda$.

Intermediate variables: $h$ at four probe positions; $L_1,L_2$; $g_1,g_2$ by parameter group; branch probe logits; head1/head2 logits.

Steps:

1. Generate train/eval data for A/B/C.
2. Train NTP, shared-trunk two-token, and shared-attention separate-expert conditions.
3. At profiling intervals, compute $L_1$ and $L_2$ gradients separately without changing training.
4. Evaluate head metrics, branch-swap, branch probes at four positions, and gradient metrics.
5. Aggregate per seed and classify `two_token_signal_class`.

Outputs:

```text
tables/per_seed_metrics.csv
tables/regime_condition_summary.csv
tables/probe_by_position.csv
tables/gradient_profile.csv
tables/branch_swap.csv
tables/refinement_metrics.csv
run_manifest.json
```

## 12. Success / Failure / Insufficient Evidence

**Success for useful signal:** A-clean improves branch probe/head2/swap over NTP and C-noisy does not.

**Success for useful-but-interfering:** A-clean improves branch metrics but increases $L_1$ loss, with negative $c_s$ or low $\rho$ in shared groups.

**Success for expert localization:** separate-expert improves $L_1$ preservation relative to shared-trunk two-token while keeping branch metrics.

**Failure:** A-clean does not improve branch metrics, C-noisy improves similarly, or all gradient diagnostics fail to explain observed degradation.

**Insufficient:** data leakage, broken loss wiring, probe split invalid, too few seeds, or gradient profiling changes training.

## 13. What This Cannot Claim

- It cannot claim curriculum works.
- It cannot claim K>2 works.
- It cannot claim natural-language transfer.
- It cannot claim all MTP objectives are useful.
- It cannot claim expert separation is generally better.
- It cannot replace the A11_01 proof; it builds on it.

## 14. Review Notes, Execution Notes, And Required User Decisions

用户审核已确定：

1. Regime B 固定为 $Y_1=S_B,\;Y_2=R(S_B)=T_B$，其中 $R(S_b)=T_b$。
2. Regime C 使用固定分布 $P_Z$ 下的 per-occurrence iid noise，不使用 branch-to-noise table。
3. 第一轮包含 `init_mode=random` 和 `init_mode=identical_branch`。
4. `num_branches=4`, `filler_length=16`, `shared_context_length=4`, and `5` seeds 固定。
5. `fully_separated_control` 暂缓。
6. `all_positions_lm_control` 保留为 `decision_only` 后的第二阶段 objective-scope 鲁棒性控制。

执行记录：

1. 主实验：`a11_02_decision_only_local2gpu_20260707_0411`。
2. 12000 步收敛诊断：`a11_02_decision_only_completion_a_clean_shared_trunk_12000_20260707_0545`。
3. 远程 ACP 任务 `pt-tydhqbgx` 已提交，但在聚合前失败；存在部分 shard 日志，本轮完整证据来自本地 2 卡运行。
4. 结果报告位于本实验文件夹的 `summary.md` 和 `detailed.md`。
