# Minimal Anchor Handwrite Draft

Use this by hand before asking AI to polish the anchor. Write rough bullets.
The canonical anchor is written in English. If Chinese helps thinking, write a
separate `_cn.md` companion; do not mix two full versions in one file.
Exception: write the `Tiny Summary` section in Chinese as the quick judgment
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
- 当前 top-1 linear router 能否表达 $||P_{S_e}h||^2$ 这种子空间投影分数，还是需要先做 oracle audit 再压缩成线性权重？

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

## 0. Tiny Summary

父问题：为什么 random-init sparse top-1 MoE router 不能稳定进入 useful expert specialization？

当前子问题：导师提出 router 初始化应利用 expert 初始化的高奇异值方向；补充说明要求先处理 common feature，再用长尾 residual feature 做 expert 分发。

核心假设：expert 初始谱含有可用的 label-free routing prior，但 raw top-spectrum 会被 common direction 污染；common-filtered residual-spectrum routing 才可能减少早期 common amplification。

最小测试：先做 expert-spectrum / common-overlap audit，再比较 random、raw-spectrum、common-filtered spectrum 初始化在 step 0--10 的 common-margin、load、replay interaction 和 utility correlation。

当前边界：这是 computation + implementation 构造草稿，不是已批准实验协议；只针对 small random-init top-1 MoE early training。

下一步决策：先确定可实现的 expert-spectrum score：oracle 子空间投影，还是可写入 linear router 的初始化权重。

## 1. Problem Definition

Parent problem:
Why does random-initialized sparse top-1 MoE fail to enter stable, useful expert specialization before early route concentration appears?

Sharper subproblem:
Can expert initialization provide a label-free routing prior if common features are removed or isolated before residual expert-spectrum dispatch?

Decision question:
Does a common-filtered expert-spectrum routing initialization reduce early common-logit amplification compared with random and raw-spectrum initialization, while preserving loss and showing expert-specific utility signal?

Not in scope:
Pretrained large MoEs, final expert utility specialization, top-2 routing, load-balance loss as the solution, and claims that expert singular vectors are true semantic features.

## 2. Physical Prior

P1:
Randomly initialized experts are not functionally identical because their input-side high-gain subspaces differ.

Meaning:
Even under Gaussian initialization, each expert may have a small set of singular directions where input perturbations produce larger output changes.

Could be wrong if:
Expert high-gain subspaces are statistically indistinguishable, unstable, or do not predict forced-routing utility.

P2:
Raw top singular directions are vulnerable to common-feature capture.

Meaning:
The largest-energy directions may align with batch-common, position-common, or frequency-common components instead of residual feature differences.

Could be wrong if:
Top expert-spectrum directions have low overlap with common subspaces and raw-spectrum routing does not increase common-margin or route concentration.

P3:
Useful spectrum-based routing should first isolate common components, then dispatch residual token features to compatible expert high-gain subspaces.

Meaning:
A common expert or common-subspace removal handles shared directions; the remaining residual is routed by expert-specific spectrum alignment.

Could be wrong if:
Common filtering destroys the routing signal, worsens loss, or fails to reduce A06_02-style common-logit amplification.

## 3. Hypothesis

H1:
Expert high-gain input subspaces contain non-random routing information at initialization.

Supported if:
Spectrum scores predict forced-routing utility or reduce loss/gradient mismatch relative to random assignment.

Weakened if:
Spectrum scores are uncorrelated with forced-routing utility and do not improve any early specialization or stability metric.

H2:
Raw expert-spectrum routing is vulnerable to common-direction capture.

Supported if:
Raw top-spectrum directions overlap strongly with common subspaces and raw-spectrum routing increases common_margin, raw_max_load, or A_interaction.

Weakened if:
Raw-spectrum routing has low common overlap and reduces early common-logit amplification without extra filtering.

H3:
Common-filtered expert-spectrum routing is the more plausible initialization method.

Supported if:
Filtering or a low-rank common expert lowers step-10 common_margin_delta and gate-hidden interaction while preserving LM loss and effective experts.

Weakened if:
Filtered routing only improves load balance, fails utility correlation, or has the same A06_02 common amplification as random routing.

## 4. Minimal Mathematical Model

Objects:
For expert $e$, let $E_e(h)$ be its FFN function and $J_e(h_0)=\partial E_e(h)/\partial h|_{h_0}$ its input-side local linearization. Let $S_e=\mathrm{span}(V_{e,1:k})$ be the top-$k$ right singular subspace of $J_e(h_0)\approx U_e\Sigma_eV_e^\top$. Let $C$ be the common subspace estimated from router inputs.

Core decomposition:
Token input is split as $h=c+r$, where $c=P_C h$ is common and $r=(I-P_C)h$ is residual. Candidate scores are:

$$
s_e^{raw}(h)=||P_{S_e}h||^2,\qquad
s_e^{res}(h)=||P_{S_e}(I-P_C)h||^2.
$$

Mechanism relation:
If $S_e$ overlaps mainly with $C$, raw spectrum routing amplifies common-score spread. If $S_e$ captures residual directions after $P_C$ removal, routing can reduce common-logit amplification and improve expert-specific assignment.

Observable metrics:
`overlap(S_e,C)`, `spectral_score`, forced-routing utility correlation, `common_margin_delta`, `raw_max_load`, `centered_max_load`, `effective_experts`, LM loss, and A06_02 replay terms `A_gate`, `A_hidden`, `A_interaction`.

Falsifier:
If raw and filtered spectrum scores do not predict utility and do not change step-10 common-margin or replay interaction relative to random init, expert-spectrum initialization is not a supported mechanism in this setting.

## 5. Minimal Tests

Experiment:
Spectral overlap and implementability audit.

Question:
Are expert top singular subspaces distinct, and do they overlap more with common or residual directions?

Intervention:
Compute top-$k$ input-side singular subspaces for each expert; compare them to common subspaces from router inputs, with $k$ around the proposed top 1% direction budget.

Primary metric:
`overlap(S_e,C)` and inter-expert subspace diversity.

Supports:
Experts have distinct high-gain subspaces and common-filtering changes the usable residual alignment.

Weakens:
Subspaces are indistinguishable, dominated by common directions, or too expensive/ambiguous to compute reproducibly.

Experiment:
Router initialization comparison.

Question:
Does common-filtered spectrum initialization change the A06_02 early amplification path?

Intervention:
Compare random init, raw-spectrum init, and common-filtered spectrum init or common-expert-plus-residual-spectrum routing on the same DCLM path-check setup.

Primary metric:
Layer 3--5 step0->10 `common_margin_delta` and replay `A_interaction`.

Supports:
Common-filtered spectrum init lowers common-margin amplification and A_interaction without worsening LM loss.

Weakens:
It only changes raw load, worsens loss, or reproduces the same common-margin spike as random init.

Experiment:
Forced-routing utility correlation.

Question:
Does the spectrum score predict whether a token benefits from expert $e$?

Intervention:
For a fixed audit batch, force candidate tokens through each expert or compare output/loss deltas under controlled routing.

Primary metric:
Correlation between `s_e^{raw}` / `s_e^{res}` and forced-routing utility.

Supports:
Filtered spectrum score predicts utility better than raw score and random assignment.

Weakens:
Neither score predicts utility, or raw/common score dominates the apparent benefit.

## 6. Falsifiable Outcomes

Supported:
Expert spectrum is distinct, common-filtered spectrum reduces step-10 common amplification and A_interaction, and filtered spectrum score predicts forced-routing utility.

Weakened:
Top spectrum is mostly common, filtered routing fails to reduce A06_02-style amplification, or spectrum score has no utility correlation.

Insufficient evidence:
Only load balance is reported; expert spectrum is approximated without a checked implementation contract; no common-overlap audit exists; no replay decomposition is run; or only one seed/layer is inspected.

## 7. Current Evidence

Observation:
Advisor explicitly proposed that router initialization should use expert initialization's large singular directions, with a later clarification that common feature directions should be removed or handled by a common expert before residual dispatch.

Interpretation:
The method is not merely random router replacement; it is a computation/implementation construction: common handling plus residual expert-spectrum alignment.

Boundary:
This is an advisor intuition and construction target, not yet experimental evidence that the method works.

Observation:
A06_02 shows the real DCLM step-10 spike is not gate-only. In layer 5, normal `common_margin_delta=1.2760`, `A_gate=-0.0137`, `A_hidden=0.4858`, and `A_interaction=0.8038`.

Interpretation:
The new initialization should be judged by whether it changes hidden/gate interaction and common amplification, not merely by initial load balance.

Boundary:
A06_02 does not test expert-spectrum initialization, common expert routing, or forced-routing utility.

Observation:
A06_02 freeze split shows raw load concentration can survive fixed gate and frozen experts, while full common-margin amplification needs hidden-producing path and gate-hidden interaction.

Interpretation:
Common-filtered spectrum routing may help only if it changes the early residual path that feeds gate-hidden interaction.

Boundary:
It cannot yet claim to solve all raw route concentration, residual anisotropy, position structure, or forward expert-output feedback.

## 8. Claim Boundary And Next Decision

Can claim:
The current method idea is a concrete label-free routing-construction hypothesis: isolate common directions, then route residual token features by expert high-gain input subspace alignment.

Cannot claim:
We cannot yet claim that expert top singular directions are useful features, that common filtering is sufficient, or that this solves MoE collapse.

Next decision:
Decide the first implementable score: run an oracle subspace-score audit first, or immediately compress expert subspaces into linear router initialization weights.
