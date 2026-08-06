# 10_01 公共投影 SGD 学习率 Anchor

Thinking Card source: [10_01_common_projected_sgd_lr_thinking_card_cn.md](10_01_common_projected_sgd_lr_thinking_card_cn.md)

## 1. Problem Definition

**Parent problem:** seminar optimizer 支线要判断 Adam / Nesterov 等方法为何允许更大的有效学习率，以及这种优势是否与 common / high-gain 方向有关。

**Sharper subproblem:** 先在最小可控 output-head 设置中测试：公共梯度是否会限制 SGD 的临界学习率。

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| 公共方向 (common direction) | batch 中许多样本共享的 hidden 方向 | $u=\mathrm{mean}(h_i)/\|\mathrm{mean}(h_i)\|$ | unit vector | 定义要投掉的输入侧方向 | 不证明它是真实 LLM 的唯一 common |
| 公共梯度 (common gradient) | 输出梯度中沿公共方向的部分 | $G_c=uu^\top G$ | gradient matrix | 候选 loud-direction bottleneck | 不证明所有不稳定来自它 |
| 公共投影梯度 (common-projected gradient) | 去掉公共方向后的梯度 | $G_r=(I-uu^\top)G$ | gradient matrix | 测试投掉公共方向是否提高稳定 LR | 不等于最终 optimizer |
| 临界学习率 (critical learning rate) | 固定窗口内仍稳定下降的最大学习率 | $\eta_{\mathrm{crit}}$ | scalar | 当前决策的主指标 | 不证明最终泛化好 |
| rare-token loss | 低频 token 类上的交叉熵 | eval rare subset CE | loss | 检查投影没有牺牲 rare 学习 | 不证明语义稀有特征 |

**Decision question:** 在合成 output-head 任务中，去掉 batch 公共梯度是否能显著提高 SGD 的临界学习率，并且不恶化 rare-token learning？

**Not in scope:** 不证明 Adam 全部优势；不比较所有 optimizer；不证明 Nesterov 有效；不直接接 MoE routing preservation claim。

## 2. Physical Priors

**P1:** 输出层梯度可以分解为公共方向和 token-specific 方向。  
**Meaning:** 频繁 token 的梯度会反复写入共享方向，使该方向成为 loud update direction。  
**Could be wrong if:** 公共方向不稳定，或梯度能量与 token frequency 无关。

**P2:** 大学习率 SGD 的第一个失败点可能是 loud direction，而不是全部方向同时失败。  
**Meaning:** 一个全局学习率必须同时满足最大方向的稳定性，因此公共强方向会压低可用学习率。  
**Could be wrong if:** 不稳定主要来自 Hessian curvature、batch noise、normalization layer 或 attention dynamics。

**P3:** 投掉公共梯度不应自动改善 rare 学习，必须用 rare loss guard 检查。  
**Meaning:** 如果公共方向对 rare token 也必要，投影会提高稳定性但损害学习。  
**Could be wrong if:** rare token 的有效学习也主要依赖公共方向。

## 3. Falsifiable Hypotheses

**H1:** 公共投影 SGD 提高临界学习率。  
**Supported if:** $\eta_{\mathrm{crit}}(\mathrm{projected}) / \eta_{\mathrm{crit}}(\mathrm{vanilla}) \ge 3$，且 norm-matched control 不能解释。  
**Weakened if:** 提升小于 1.5x，或 norm-matched / random projection 也同样提升。

**H2:** 公共投影不牺牲 rare-token learning。  
**Supported if:** 在各自临界学习率附近，projected SGD 的 rare-token eval loss 不高于 vanilla SGD，且 rare update share 不下降。  
**Weakened if:** 稳定性提高但 rare loss 明显变差。

## 4. Mathematical Model

**Objects:** 固定 hidden states $h_i\in\mathbb{R}^d$，输出层梯度 $G\in\mathbb{R}^{d\times V}$，目标 token $y_i$，预测误差向量 $e_i=p_i-\mathrm{onehot}(y_i)$。

**Core decomposition:**

$$
G=\frac{1}{B}\sum_i h_i e_i^\top
$$

$$
u=\frac{\mathrm{mean}_i(h_i)}{\|\mathrm{mean}_i(h_i)\|}
$$

$$
G_c=uu^\top G,\qquad G_r=(I-uu^\top)G
$$

**Mechanism relation:** 若公共方向是限制大 LR 的主因，则移除 $G_c$ 后，稳定学习率上界应提高；若提升只来自范数缩小，则 norm-matched SGD 会给出同样提升。

**Observable metrics:** $\eta_{\mathrm{crit}}$ ratio，rare-token loss，rare-token update share，$\|G_c\|_F/\|G\|_F$，top singular energy。

**Falsifier:** 公共投影 SGD 在 norm-matched control 下不能提高 $\eta_{\mathrm{crit}}$，或提高稳定性但 rare loss 明显恶化。

## 5. Computational Realization

**Input objects:** 合成 hidden-token 数据；固定输出头训练；vanilla SGD、common-projected SGD、norm-matched SGD、random-projected SGD。

**Computed variables:** $G_c$、$G_r$、临界学习率、frequent/rare loss、per-token update norm、common energy ratio。

**Algorithm stages:** 构造带公共方向的 hidden 数据；只训练输出头；扫学习率；判定稳定窗口；比较 projected 与 controls。

**Stage-local evidence:** LR stability curve；rare-vs-frequent loss curve；common/residual energy trajectory；control comparison table。

**Expected artifacts:** `protocol_cn.md` approval draft，approved `protocol.md`，`summary.md`，`detailed.md`，一张 LR stability figure，一张 rare-loss figure，一张主结果表。

## 6. Minimal Falsification Test

**Test:** 合成 output-head common-projected SGD 临界学习率审计。

**Question:** 公共梯度本身是否足以压低 SGD 的临界学习率？

**Intervention / comparison:** 在 $h=\alpha_c c+\alpha_y z_y+\epsilon$ 的合成数据上比较 vanilla SGD、common-projected SGD、norm-matched SGD、random-projected SGD。

**Primary metric:** $\eta_{\mathrm{crit}}(\mathrm{common\text{-}projected})/\eta_{\mathrm{crit}}(\mathrm{vanilla})$。

**Pass / fail / insufficient:** Pass if ratio $\ge 3$ and controls do not explain it. Fail if ratio $\le 1.5$ or norm/random controls match it. Insufficient if projected SGD is stable but rare loss collapses, or the synthetic common direction is not actually present.

**Why it decides:** 它先裁定“公共梯度限制 LR”这个最小机制是否存在；只有通过后，才值得接 small-real LM、Adam/Nesterov 诊断。

**Failure means:** 可能 falsify 当前 common-gradient operationalization；不直接 falsify Adam/Nesterov 或 MoE 主线。

## 7. Current Evidence

**Observation:** seminar prompt 记录了：Adam effective LR 远大于 SGD；大 LR SGD 的失败与 layer-wise spikes、output-layer per-token-class imbalance、frequent-token gradient dominance 有关。

**Interpretation:** 这些现象支持“公共/高频 loud direction 可能限制 SGD LR”的候选机制，但还没有证明公共投影能提升临界 LR。

**Boundary:** 当前 anchor 是 seminar optimizer 支线，不更新 feature-level MoE specialization 主线 claim。

**Evidence links:** `daily_research_reports/backup/2026/07/0701/prompts/0701_seminar_questions_next_conversation_prompt_cn.md`; `daily_research_reports/backup/2026/07/0701/docs/design_problem_understanding_revised.md`; seminar screenshots noted there.

## 8. Claim Boundary And Next Decision

**Can claim:** 该 anchor 测试公共梯度投影是否提高合成 output-head 中 SGD 的稳定学习率。

**Cannot claim:** 不能 claim common projection 解释 Adam 全部优势；不能 claim Nesterov 有效；不能 claim real LM 或 MoE routing preservation 已被解释。

**Next decision:** 审批并运行 synthetic protocol；只有 synthetic pass 后，再设计 small-real LM / Adam / Nesterov follow-up。
