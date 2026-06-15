# 06_01 Common-Filtered Expert-Spectrum Router Initialization

## 0. Tiny Summary

父问题：为什么 random-init sparse top-1 MoE router 不能稳定进入 useful expert specialization？

当前子问题：能否把导师提出的 expert-spectrum routing intuition 变成可计算的 router initialization，并判断它是否真的优于 random init？

核心假设更新：expert spectrum 里有弱 residual utility signal，但把 spectrum score 压成 linear top-1 router 后，大部分 oracle assignment 结构丢失。common-filtered spectrum 只能降低 replay interaction，不能解决 step-10 common-margin 和负载集中。

已完成最小测试：4-GPU ACP full run，6 个 initialization variants，3 seeds，0--300 steps，完整 replay / utility / exact gate-input audit。

新增审计：step-0 token-frequency routing audit 已完成；去掉 top 1% / top 5% 高频 token id 后，初始化之间的 route-load 结论基本不变。

关键细化：去掉 top 1% 高频 token id 后，V4 step-0 rank-1 expert 只有 13.97%，比 random 的 19.98% 更均匀；但 step-10 V4 rank-1 expert 升到 93.51%，比 random 的 83.16% 更严重。

当前边界：这是 negative-but-informative result。它不否定 expert spectrum 在更强 router / oracle gate 下可能有用，但不支持当前 linear router initialization。

下一步决策：不要把 V4 common-filtered spectrum linear init 当作成功方法继续推进。下一步，应做 computation-vs-implementation split：residual-spectrum oracle gate 或 stronger fitted classifier bridge vs 当前 linear row-mean bridge。

## 1. Problem Definition

Parent problem:
Why do random-initialized sparse top-1 MoE routers fail to enter stable and useful expert specialization before early route concentration appears?

Sharper subproblem:
Can expert initialization and initial router-input geometry jointly provide a label-free router initialization, after common directions are removed or isolated?

Decision question:
Does a common-filtered expert-spectrum / representation initialization reduce early common-logit amplification and improve specialization or utility alignment compared with random and raw-spectrum initialization?

Not in scope:
Pretrained large MoEs, final expert utility specialization, load-balance loss as the solution, top-2 routing, and claims that expert singular vectors are true semantic features.

## 2. Physical Prior

P1:
Randomly initialized experts are not functionally identical because their input-side high-gain subspaces differ.

Meaning:
Even with Gaussian initialization, each expert may respond more strongly to some input directions than others.

Could be wrong if:
Expert high-gain subspaces are indistinguishable, unstable, or unrelated to forced-routing utility.

P2:
Raw top-spectrum directions are vulnerable to common-feature capture.

Meaning:
The largest expert-sensitive directions may align with common, position, frequency, or high-energy directions rather than useful residual differences.

Could be wrong if:
Top-spectrum directions have low overlap with common subspaces and raw-spectrum routing does not increase common-margin or route concentration.

P3:
Useful early routing should align residual token representations with compatible expert high-gain directions, not merely balance load.

Meaning:
A good initialization should reduce common-driven early amplification while preserving loss and improving feature / utility alignment.

Could be wrong if:
Common filtering destroys useful routing signal, worsens loss, or only improves load balance without improving specialization or utility correlation.

## 3. Hypothesis

H1:
Expert high-gain input subspaces contain non-random routing information at initialization.

Supported if:
Expert spectrum scores predict forced-routing utility or produce non-random residual assignment better than random routing.

Weakened if:
Spectrum scores are uncorrelated with forced-routing utility and do not improve early specialization or stability metrics.

H2:
Raw expert-spectrum routing is vulnerable to common-direction capture.

Supported if:
Raw top-spectrum directions overlap strongly with common subspaces and raw-spectrum initialization increases `common_margin`, `raw_max_load`, or `A_interaction`.

Weakened if:
Raw-spectrum initialization has low common overlap and reduces early common-logit amplification without filtering.

H3:
Common-filtered spectrum / representation initialization is the more plausible method.

Supported if:
Common-filtered initialization lowers step-10 `common_margin_delta` and `A_interaction` while preserving LM loss, effective experts, and specialization / utility signal.

Weakened if:
Filtered initialization only improves load balance, fails utility correlation, or reproduces the same early amplification as random init.

## 4. Minimal Mathematical Model

Objects:
For expert $e$, let $E_e(h)$ be the expert FFN function. Let $J_e(h_\*)=\partial E_e(h)/\partial h|_{h_\*}$ be its input-side local linearization. Let $S_e=\mathrm{span}(V_{e,1:k})$ be the top-$k$ right singular subspace of $J_e(h_\*)\approx U_e\Sigma_e V_e^\top$. Let $C$ be the common subspace estimated from initial router inputs $H_0$.

Core decomposition:
For token input $h_i$,

$$
h_i = c_i + r_i,\qquad
c_i = P_C h_i,\qquad
r_i = (I - P_C)h_i.
$$

Candidate spectrum scores:

$$
s_e^{raw}(h_i)=\|P_{S_e}h_i\|^2
$$

$$
s_e^{res}(h_i)=\|P_{S_e}(I-P_C)h_i\|^2
$$

Implementation bridge:
Use the oracle score $s_e^{res}$ to assign audit tokens to experts, then compress that assignment into linear router rows:

$$
A_e=\{i:e=\arg\max_j s_j^{res}(h_i)\}
$$

$$
w_e^{init}\propto \mathrm{mean}_{i\in A_e}r_i
$$

or fit a small ridge / linear classifier from $r_i$ to the oracle assignment.

Mechanism relation:
If $S_e$ mainly overlaps with $C$, raw spectrum routing amplifies common directions. If $S_e$ captures residual directions after common removal, linearized residual-spectrum initialization may reduce early common amplification.

Observable metrics:
`overlap(S_e, C)`, inter-expert subspace diversity, oracle spectral load, forced-routing utility correlation, `common_margin_delta`, `raw_max_load`, `effective_experts`, LM loss, `slot_NMI`, and `A_interaction`.

Falsifier:
If raw and filtered spectrum scores neither predict utility nor change step-10 common-margin / `A_interaction` relative to random init, expert-spectrum initialization is not supported in this setting.

## 5. Minimal Tests

Experiment 1:
Expert-spectrum / common-overlap / utility audit.

Question:
Do expert top high-gain directions differ across experts, and do they align more with common directions, residual directions, or forced-routing utility?

Intervention:
Compute top-$k$ input-side expert subspaces $S_e$; compare $S_e$ with common subspace $C$ and residual activations $R=(I-P_C)H_0$. Also measure forced-routing utility on a fixed audit batch.

Primary metric:
`overlap(S_e, C)`, inter-expert subspace diversity, activation $\|P_{S_e}r_i\|^2$, and correlation between $s_e^{res}$ and forced-routing utility.

Supports:
Expert spectrum contains distinct residual / utility signal.

Weakens:
Top spectrum is common-dominated, indistinguishable across experts, or unrelated to utility.

Experiment 2:
Initialization implementation comparison.

Question:
Can we turn expert-spectrum and initial representation geometry into a valid linear router initialization?

Intervention:
Construct these initializations on the same model and audit batch:
1. random_init;
2. representation_residual_init;
3. raw_spectrum_init;
4. common_filtered_spectrum_init;
5. hybrid_spectrum_to_linear_init.

Primary metric:
step-0 raw_max_load, centered_max_load, common_margin, empty expert count, oracle-to-linear agreement, and initialization reconstruction / classifier accuracy.

Supports:
A method produces sane step-0 routing without common dominance or empty-expert failure.

Weakens:
A method collapses at step 0, cannot be represented by a linear router, or only changes load through common bias.

Experiment 3:
Early-training comparison.

Question:
Does the initialization change the early training path, especially the step-10 common amplification and gate-hidden interaction?

Intervention:
Train selected initialization variants for 0--300 steps under the same top-1 MoE setup, with exact gate-input audit and cross-checkpoint replay.

Primary metric:
For synthetic: `slot_NMI`, per-slot purity, accuracy, `common_margin`, `slot_margin`.
For real DCLM: `common_margin_delta`, `raw_max_load_delta`, `effective_experts`, LM loss, and `A_interaction`.

Supports:
Common-filtered or hybrid initialization lowers step-10 common amplification / `A_interaction` while preserving loss and improving specialization or utility alignment.

Weakens:
It only improves load balance, worsens loss, or follows the same early amplification path as random init.

## 6. Falsifiable Outcomes

Supported:
Expert high-gain subspaces are distinct; common-filtered spectrum scores predict forced-routing utility; and common-filtered / hybrid initialization reduces early common amplification or improves slot specialization without hurting loss.

Weakened:
Top spectrum is mostly common, raw and filtered initialization do not improve utility alignment, or all initialized variants reproduce the same step-10 amplification as random init.

Insufficient evidence:
Only load balance is reported; no common-overlap audit exists; forced-routing utility is not measured; exact gate input is not audited; or only one seed / layer is tested.

## 7. Current Evidence

Observation:
The advisor proposed that router initialization should use the large singular directions of initialized experts, because an ideal router should dispatch inputs according to their compatibility with expert high-gain directions.

Interpretation:
This motivates expert-spectrum-conditioned initialization, but it does not by itself prove that top singular directions are useful features.

Boundary:
The advisor's idea is a computation target, not yet experimental evidence.

Observation:
In the minimal synthetic setting, slot information exists and slot-specialization is reachable, but random routing collapses. Common-logit cancellation raises slot_NMI from 0.080 to 0.896 / 0.963 while preserving accuracy.

Interpretation:
Common control is not optional. Any spectrum-based routing must be tested against common-direction capture.

Boundary:
This evidence is from controlled synthetic data and does not directly prove real-text behavior.

Observation:
In real DCLM early training, step-10 late-layer concentration is not gate-only. Layer-5 $A_{actual}=1.2760$, $A_{gate}=-0.0137$, $A_{hidden}=0.4858$, and $A_{interaction}=0.8038$. Freeze split shows expert updates amplify common-margin, while raw load can survive without expert updates.

Interpretation:
Anchor1 should evaluate whether initialization changes early hidden-gate interaction, not only step-0 load.

Boundary:
This does not prove expert-spectrum initialization works; it tells us which early metrics to inspect.

Observation:
A06_01 full 4-GPU ACP run completed successfully with 18 training runs, 13068 replay rows, 72 forced-utility rows, and exact gate reconstruction error 0.0. In late layers 3--5, V4 common-filtered spectrum reduced `A_interaction` to 0.1543 compared with V0 random at 0.2795, but worsened the primary early-training metrics: `common_margin_delta=0.5203` versus 0.3878, step-10 `raw_max_load=0.9374` versus 0.8344, and effective experts 1.2177 versus 1.5636.

Interpretation:
Common filtering changes the replay interaction mechanism but does not prevent early top-1 route concentration. The direct linear initialization is therefore not a successful method in this setting.

Boundary:
The residual-spectrum oracle assignment is balanced, but residual-oracle-to-linear agreement remains low: V3 0.2038, V4 0.2157, V5 0.2465. This points to the linear-router implementation bridge as a likely bottleneck. The minimal MoE source also still includes a shared expert path even though the protocol intended `use_shared_expert=false`.

Observation:
A post-hoc step-0 token-frequency routing audit was run on the completed A06_01 checkpoints. High-frequency tokens were defined from the init split. The top 1% observed token types contain 508 token ids and 61.45% of init-token mass. In late layers 3--5, removing these high-frequency ids barely changes initial `max_load`: V0 all/high/without-high = 0.2010/0.2018/0.1998, V3 = 0.1681/0.1687/0.1673, V4 = 0.1393/0.1406/0.1397, and V5 = 0.1622/0.1628/0.1617.

Interpretation:
The step-0 route distribution differences across initialization variants are not driven by a small high-frequency-token subset. Top frequent tokens are slightly more route-concentrated than all tokens, but no top-64 frequent token is single-expert collapsed at step 0.

Boundary:
This only rules out a step-0 token-id-frequency explanation. It does not prove high-frequency tokens are irrelevant after training begins, because hidden-state drift can move the same token id into different representation regions.

Observation:
A sorted route-rank audit was then run at steps 0 and 10. After removing the top 1% high-frequency token ids, late-layer step-0 rank-1 expert load is V0 19.98%, V1 13.92%, V2 14.40%, V3 16.73%, V4 13.97%, and V5 16.17%. At step 10, rank-1 load becomes V0 83.16%, V1 96.23%, V2 91.27%, V3 91.33%, V4 93.51%, and V5 88.64%.

Interpretation:
Common-filtered initialization does reduce initial sorted-load imbalance after high-frequency tokens are removed. The failure is therefore not that V4 starts collapsed. The failure is that early training amplifies a dominant route even from an initially balanced distribution; V4 is more balanced than random at step 0 but more collapsed than random by step 10.

Boundary:
This supports a training-dynamics explanation over a pure initial-token-frequency explanation. It still does not identify whether the step-10 amplification is driven more by hidden-state drift, router-gradient geometry, expert-output feedback, or their interaction.

## 8. Claim Boundary And Next Decision

Can claim now:
Expert spectrum contains a weak residual utility signal, and common filtering can reduce replay interaction and step-0 route imbalance. However, common-filtered expert-spectrum **linear** initialization does not reduce the primary step-10 common-margin spike or top-1 load concentration in this random-init DCLM top-1 MoE setting. The negative initialization result is not explained by step-0 high-frequency-token routing alone.

Cannot claim now:
Expert top singular directions are true features; expert initialization sufficiently covers the representation space; spectrum initialization solves collapse; expert spectrum is useless in general; high-frequency tokens are irrelevant during training; or the result transfers to pretrained / large / top-2 or top-4 MoEs.

Next decision:
Do not promote V4 common-filtered expert-spectrum linear initialization as a successful method.

Decision after results:
If this direction must be pursued, run only one narrow follow-up: compare residual-spectrum oracle gate or a stronger fitted classifier bridge against the current linear row-mean bridge for steps 0--10. If the oracle/fitted bridge also fails to reduce `common_margin_delta` and `raw_max_load`, park expert-spectrum routing for this setting.
