# Minimal Anchor Handwrite Draft

Use this by hand before asking AI to polish the anchor. Write rough bullets.
The canonical anchor is written in English. If Chinese helps thinking, write a
separate `_cn.md` companion; do not mix two full versions in one file.
Exception: write the `Thinking Card` section in Chinese as the quick judgment
surface.

## AI Use Contract

This file is a thinking draft, not a final anchor. When an AI reads it, the
default task is to critique and clarify the user's logic before writing a
formal anchor.

In normal use, the user and AI first complete sections 1-4: Problem Definition,
Physical Prior, Hypothesis, and Minimal Mathematical Model. Minimal Tests are
then co-designed after those sections are clear. The AI may propose candidate
tests, tradeoffs, and questions for user approval, but should not finalize
Minimal Tests on its own.

The AI should first identify:

- which user judgments should be preserved;
- whether the user's physical priors are correct, falsifiable, and sufficient
  to support the current hypotheses;
- which objects, feature definitions, metrics, or claim boundaries are unclear;
- which hypotheses lack falsifiers;
- which claims are stronger than the available evidence or metrics;
- the smallest additions needed before this can become a formal anchor.

The AI should not silently replace the user's research question, feature key,
physical prior, or next decision. If the AI thinks a new physical prior is
needed, it should propose it as a candidate for user approval first. Do not add
that prior to the formal anchor until the user explicitly accepts it. If a
formal anchor is requested, it should improve this draft on top of the user's
logic and then state what was tightened.

Optional notes for the user:

My uncertain points:

- Expert 的“谱方向”到底取自完整局部 Jacobian，还是取自 FFN 的某个有效线性近似？
- common expert 是真实训练中的额外 expert，还是只作为初始化前的 common-subspace removal / routing oracle？
- 当前 top-1 linear router 能否表达 $\|P_{S_e}h\|^2$ 这种子空间投影分数，还是需要先做 oracle audit 再压缩成线性权重？

接下来需要讨论：expert 的谱方向到底怎么定义、common expert 是真实结构还是诊断构造、以及 top-1 linear router 能不能表达子空间投影分数。以及，除了导师这种初始化方式之外，是否存在对于初始表征空间 + 专家初始化方式相结合的初始化

Do not silently change:

- 不要把导师的 intuition 改成普通 load-balance loss、center-separation 或 supervised slot router。
- 不要把“按 expert top spectrum 分发”直接写成成功；必须保留 common feature 污染风险。
- 不要把 A06_02 的机制证据改写成“gate-only 初始化问题”；A06_02 支持 hidden drift + gate-hidden interaction。

AI should challenge:

- “专家初始化足够覆盖空间”是否是可测先验，还是只是期望？
- top 1% singular directions 是否真的对应 useful feature，而不是 common / high-energy / frequency direction？
- 如果 common expert 吃掉 common 后，剩余 residual 方向是否还有足够稳定的 expert-specific alignment？
- 如果按照表征空间的统计进行初始化，会出现什么问题？

Candidate physical priors I am not sure about:

- P-candidate: random expert FFNs have heterogeneous high-gain input subspaces at initialization.
- P-candidate: common directions should be handled by a low-rank common expert before residual feature dispatch.
- P-candidate: useful early routing should align token residuals to expert high-gain subspaces, not merely balance load.

# 06_01 Common-Filtered Expert-Spectrum Router Initialization

## 0. Thinking Card

父问题：为什么 random-init sparse top-1 MoE router 不能稳定进入 useful expert specialization？

当前子问题：能否把导师提出的 expert-spectrum routing intuition 变成可计算的 router initialization，并判断它是否真的优于 random init？

核心假设更新：expert spectrum 里有弱 residual utility signal，但把 spectrum score 压成 linear top-1 router 后，大部分 oracle assignment 结构丢失。common-filtered spectrum 只能降低 replay interaction，不能解决 step-10 common-margin 和负载集中。

已完成最小测试：4-GPU ACP full run，6 个 initialization variants，3 seeds，0--300 steps，完整 replay / utility / exact gate-input audit。

当前边界：这是 negative-but-informative result。它不否定 expert spectrum 在更强 router / oracle gate 下可能有用，但不支持当前 linear router initialization。

下一步决策：不要把 V4 common-filtered spectrum linear init 当作成功方法继续推进。若导师追问，应做 computation-vs-implementation split：residual-spectrum oracle gate 或 stronger fitted classifier bridge vs 当前 linear row-mean bridge。

## 1. Problem Definition

Parent problem:
Why do random-initialized sparse top-1 MoE routers fail to enter stable and useful expert specialization before early route concentration appears?

Sharper subproblem:
Can expert initialization and initial router-input geometry jointly provide a label-free router initialization, after common directions are removed or isolated?

Decision question:
Does a common-filtered expert-spectrum / representation initialization reduce early common-logit amplification and improve specialization or utility alignment compared with random and raw-spectrum initialization?

Not in scope:
Pretrained large MoEs, final expert utility specialization, load-balance loss as the solution, top-2 routing, and claims that expert singular vectors are true semantic features.

## 2. Physical Priors
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

## 4. Mathematical Model
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

## 8. Claim Boundary And Next Decision

Can claim now:
Expert spectrum contains a weak residual utility signal, and common filtering can reduce replay interaction. However, common-filtered expert-spectrum **linear** initialization does not reduce the primary step-10 common-margin spike or top-1 load concentration in this random-init DCLM top-1 MoE setting.

Cannot claim now:
Expert top singular directions are true features; expert initialization sufficiently covers the representation space; spectrum initialization solves collapse; expert spectrum is useless in general; or the result transfers to pretrained / large / top-2 or top-4 MoEs.

Next decision:
Do not promote V4 common-filtered expert-spectrum linear initialization as a successful method.

Decision after results:
If this direction must be pursued, run only one narrow follow-up: compare residual-spectrum oracle gate or a stronger fitted classifier bridge against the current linear row-mean bridge for steps 0--10. If the oracle/fitted bridge also fails to reduce `common_margin_delta` and `raw_max_load`, park expert-spectrum routing for this setting.
