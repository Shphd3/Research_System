# ICLR 2027 Official Review — Submission #46026

**Paper:** *Forward Similarity Does Not Guarantee Training Equivalence: Precision Placement in Differentiable Gram Solvers*  
**Document status:** **AI-assisted bilingual working draft — for the reviewer and supervising professor to revise; not submitted.**  
**Basis:** The reader's draft `iclr_2027.md`, the submitted paper, and the provided second-round reference audit `round2_audit_cn.md`. Where an argument relies on the reference audit, it should be checked against the cited original work before submission.

> **Important distinction:** Sections below labeled **Human-written assessment (to be completed by reviewer)** must contain the reviewer's actual original, independently written evaluation. The illustrative assessments at the end were generated with AI assistance and **must not** be passed off as an original human self-report. ICLR 2027 additionally requests the reviewer's inputs to the LLM across all turns when AI is used to generate or edit review text. See the [official AI policy](https://iclr.cc/Conferences/2027/AIPolicyForReviewers).

---

# Part A. English — OpenReview fields (editable draft)

## 1. AI Documentation For Reviewing — visible to AC/SAC, not authors

### A1. Human-written assessment (ORIGINAL; reviewer must fill)

**[To be inserted by the reviewer, using an unpolished self-written assessment prepared independently of AI generation. Do not paste the illustrative example in Part C into this field.]**

If your independent first assessment was written before engaging with AI, preserve that original version verbatim. The Chinese notes reproduced in Part C are genuinely user-authored text in the discussion, but they were expressed **during AI-assisted discussion**; they are not automatically interchangeable with an initial assessment written without AI.

### A2. AI usage disclosure (AI-assisted draft; reviewer to verify)

I used ChatGPT to help understand technical concepts and mathematical formulations in the paper, including Cholesky factorization, differentiable Gram solvers, Spectral Koopman Attention, and the paper's precision-route definitions. I also used it to clarify the experimental protocols, assess how the reported evidence relates to the paper's claims, and discuss possible critical strengths, weaknesses, and questions for the authors. ChatGPT additionally assisted in organizing, drafting, translating, and polishing portions of this review.

I also used AI-assisted research and checking to examine the existence and relevance of selected references and to compare the manuscript with related work. The reference audit was selective rather than exhaustive; it did not independently establish the accuracy of every citation, the originality of every experimental procedure, or the reproducibility of the reported results. No independent reproduction of the authors' experiments is claimed here.

The assessment and recommendation will be determined and verified by the human reviewer, who is responsible for the final submission. **The reviewer's original, self-written assessment and the inputs supplied to AI tools across all relevant turns must accompany this disclosure in accordance with the conference's policy.**

**Record to attach before submission:** the actual original human assessment; the prompts/inputs from the paper-reading conversations, reference-checking workflow, and iterative review drafting; and the final account of which AI tools were used. This file is a disclosure summary, **not** a complete prompt transcript.

## 2. Paper Summary

> Adapted from the reviewer's existing English draft; substantive overstatements were softened. Check against the original version in `iclr_2027.md` before copying.

This paper investigates precision placement in differentiable Gram solvers, asking whether close agreement in forward predictions guarantees agreement in gradients and optimizer updates.

The authors distinguish three solver stages—statistic construction, Cholesky factorization, and solution-side computation—and selectively assign FP32 or FP64 to each. They study a controlled Spectral Koopman Attention (SKA) model and an independent episodic ridge regression classifier. The experiments compare predictions, full-model gradients, restored optimizer updates, and the endpoints of separately trained models under a common evaluation route.

In 18 matched SKA validation comparisons from three training seeds, comparing $q_{110}$ with the higher-precision solver reference $q_{111}$ yields median relative discrepancies of 0.962% in logits, 8.61% in full-model gradients, and 9.88% in restored AdamW parameter updates, with each quantity normalized by its corresponding $q_{111}$ reference norm. Further tests examine solver-stage sensitivity, a fixed-forward alternative backward computation, and algebraically equivalent primal/dual ridge formulations. Experiments on separately trained endpoints additionally investigate how learned ridge regularization and prescribed ridge schedules affect regularized-Gram conditioning.

The results indicate that close predictions need not imply close local optimizer updates. They also show setting-dependent differences in endpoint statistics and a strong dependence of measured conditioning separation on the ridge policy in the tested classifier. A lower condition number under a prescribed ridge schedule does not establish improved or equivalent task performance. Overall, the paper provides a controlled empirical examination of the distinction between forward agreement, local learning computations, and selected post-training statistics.

## 3. Evaluation Scores — **provisional, reviewer must decide**

| Field | Working value | Reason for re-check |
|---|---:|---|
| Presentation (1–3) | **2** *(from existing draft)* | The dense experimental narrative may be difficult to follow, but this should be supported by specific presentation issues rather than the number of tables alone. |
| Informativeness (1–3) | **2** *(from existing draft)* | Some useful evidence; reviewer remains unconvinced that it provides a substantial conceptual advance. |
| Soundness (1–3) | **2 — NOT SETTLED** *(from existing draft)* | Main controlled results are not shown to be incorrect. If there is no substantive concern about support for the stated, limited claims, consider whether 3 is more consistent. A weak-reject recommendation does not require a low Soundness score. |

## 4. Critical Strengths

**S1. Carefully controlled, decision-relevant measurements of local learning computations.** The matched comparisons hold parameters, inputs, and restored optimizer state fixed while varying solver-stage precision. This permits a more targeted assessment than comparisons of prediction loss alone. The additional fixed-forward backward diagnostic (Table 5), CPU/A100 fixed-checkpoint comparison (Table 4), and shared-ridge training intervention (Section 4.6) probe alternative explanations rather than merely restating the original discrepancy. In particular, the manuscript directly measures restored optimizer updates, not only forward errors or isolated solver derivatives. These controls strengthen the empirical evidence for the paper's narrowly stated findings, even though they do not settle their generality or practical impact.

## 5. Critical Weaknesses

**W1. The significance of the incremental insight beyond prior numerical-sensitivity literature is not sufficiently established.** The broad observation that similar function values need not yield similarly accurate derivatives, and the use of different forward/backward numerical strategies for differentiable matrix operations, have substantial precedents (e.g., Hückelheim et al., 2024; Hovland & Hückelheim, 2024; Song et al., 2021). This work does add specific evidence through matched optimizer updates and ridge-schedule interventions, and those additions should be acknowledged. However, it is not yet clear what generalizable principle, diagnostic threshold, or implementation decision follows from the observed discrepancies. The primal/dual comparison (Table 7) also finds markedly smaller local discrepancies under a standard equivalent formulation, albeit at only one fixed checkpoint and five episodes. Without a clearer account of the consequences under established stable formulations, the importance of the remaining empirical increment is difficult to judge. This concern is about **significance/informativeness**, not an accusation of invalid experiments or absent novelty of every component.

**W2. The empirical findings do not yet form a sufficiently explanatory account of when local precision sensitivity matters for training.** Sections 4.2–4.3 document local gradient and update discrepancies, while Sections 4.4–4.6 separately report endpoint variation and show that training-time ridge policies can change the between-route spread of conditioning. These are meaningful, partially intervention-based observations, but they do not establish how the measured local deviations relate to the observed endpoint changes or under what conditions those deviations have important task-level consequences. In the rank-deficient episodic classifier, conditioning has an explicit algebraic dependence on ridge, $\kappa(Z_s^\top Z_s+\lambda I)=1+\sigma_{\max}(Z_s)^2/\lambda$. Thus the large reduction in conditioning spread under a shared ridge schedule (97.4%) is informative about the tested policy, but cannot on its own attribute the full training dynamics or representation changes to that mechanism. The reported P5 task comparison does not establish a performance benefit or equivalence. The paper acknowledges these limitations; the remaining concern is whether the resulting explanatory depth is sufficient for the claimed contribution.

## 6. Questions For Authors

**Q1 (incremental insight and stable formulations).** What concrete new understanding or practical decision criterion should readers take from the matched optimizer-update measurements beyond existing work on derivative sensitivity and differentiable matrix layers? Given that the equivalent dual formulation substantially reduces the measured local discrepancies in Table 7, can the authors clarify the extent to which their central conclusion remains consequential under an established, numerically preferable formulation? Any already available evidence on trained dual-form endpoints would be particularly informative; if such evidence is unavailable, please clarify the scope of the claim.

**Q2 (mechanistic interpretation of the ridge intervention).** In the P1–P2 intervention, can the authors distinguish the direct effect of prescribing $\lambda$ on the condition-number statistic from changes in the learned features or other training states? For example, could the existing results be summarized in terms of ridge values and the feature-spectrum contribution alongside conditioning, and related to the reported common-route task outcomes? This would help assess whether the intervention reveals a broader training mechanism or primarily a change in a statistic that depends explicitly on $\lambda$.

**What could change the recommendation?** A convincing distinction from the closest prior work, together with evidence or a well-supported explanation that the diagnosed update discrepancies have meaningful implications under stable implementations, would materially affect the significance assessment. Q2 can also be addressed by careful analysis of existing results rather than necessarily by a large new experimental campaign.

## 7. Flag For Ethics Review

- **Flag For Ethics Review:** No *(current working judgment; reviewer must confirm)*.
- **Details Of Ethics Concerns:** N/A.

The paper's disclosed use of ChatGPT/Codex, without additional evidence, is **not** a basis for alleging research misconduct. The accompanying selective reference audit did not establish fabricated references or experiments.

## 8. Rating and Confidence — **provisional**

- **Rating (1–4): 2 — Weak rejection** *(reviewer's tentative position, subject to revision after the author response and supervisor review)*.
- **Confidence (1–4): [REVIEWER TO SELECT]** — choose on the basis of direct expertise in this specific topic and the relevant literature, not on certainty about the recommendation.

---

# Part B. 中文 — 对照阅读与修改版本

## 1. 人工智能使用说明（对应 AI Documentation）

### B1. 原始人工判断（须本人填写，不可用以下 AI 范例替代）

**[此处粘贴审稿人实际独立撰写的、未经 AI 生成的初步评估原文。]**

你在本次讨论中自行写出的中文意见，可以作为真实的个人判断记录；但由于这些意见是在 AI 辅助讨论过程中形成的，不应直接声称它们必然属于“使用 AI 之前独立写成的初评”。若不存在这样的初评，应向负责提交的导师说明事实，不要倒填或伪造时间线。

### B2. AI 使用披露（中文版对照）

我使用 ChatGPT 辅助理解论文中的 Cholesky 分解、可微 Gram 求解器、谱 Koopman 注意力及精度路径等技术概念，并用其澄清实验协议、核对作者主张与证据的对应关系、讨论关键优点和不足以及可能向作者提出的问题。本次审稿部分英文措辞、翻译与结构组织也获得了 ChatGPT 的辅助。

此外，我使用 AI 辅助开展了有限范围的相关文献检索与真实性、相关性核查，并比较论文与部分已有工作的关系。这些检查不是穷尽性文献检索，不代表全部引用已经独立验证，也没有独立复现作者的实验。

最终判断与评分由审稿人负责并自行核验。按 ICLR 2027 要求，还须一并提供真实的初始人工评估及相关多轮模型输入记录。本说明只是使用范围摘要，**不是完整提示词记录**。

## 2. Paper Summary（中文理解版）

论文研究可微 Gram 求解器的数值精度配置，核心问题是：前向预测结果接近，是否意味着反向梯度和优化器实际更新也接近？作者将求解器划分为统计量构造、Cholesky 分解及求解端计算三个阶段，并在受控 SKA 模型和独立的任务片段岭回归分类器中分别配置 FP32/FP64。

在 18 项来自 3 个训练种子的匹配 SKA 比较中，`q110` 相对 `q111` 的 logit、全模型梯度和恢复状态后的 AdamW 更新的相对差异中位数分别为 0.962%、8.61%、9.88%。作者还研究固定前向的反向替换、原问题与对偶形式、不同训练精度下的终点差异，以及正则化参数调度对条件数的影响。

论文表明：预测接近并不足以保证局部更新接近；部分终点统计量的路径差异依赖具体设置；在所测试的分类器中，正则化策略明显影响条件数的路径间差异。但条件数改善没有确立相应的任务性能收益或等价性。其主要贡献是对这些不同层次的数值现象进行受控经验测量，而不是提出普遍误差界或新的通用求解器。

## 3. 评分（供本人定稿）

| 项目 | 暂定 | 需要进一步确认的问题 |
|---|---:|---|
| 表达清晰度（Presentation） | 2 | “实验过多”本身不等于表达不清，应指出具体困难。 |
| 信息价值（Informativeness） | 2 | 承认新增实证信息，同时说明为什么尚未形成足够深的认识更新。 |
| 可靠性（Soundness） | 原稿 2，待定 | 如果没有明确的证据不足或方法错误，不能只因倾向拒稿就下调可靠性。 |
| 录用建议（Rating） | 2（倾向拒绝） | 目前根据新增知识的重要性而非伦理或伪造疑虑作出。 |
| 专业把握度（Confidence） | 本人填写 | 以对专题与文献的熟悉度为准。 |

## 4. Critical Strengths（关键优点）

**S1. 实验控制明确，直接测量实际学习计算。** 作者在匹配比较中固定模型参数、输入和恢复的优化器状态，只改变求解器的精度阶段，使局部梯度及参数更新差异更易归因于数值实现。Table 5 的固定前向反向替换、Table 4 的固定检查点跨环境验证，以及 §4.6 的训练期正则化干预，都具有明确的验证目的。相比只报告损失或孤立的导数误差，直接测量恢复优化器状态后的实际更新是一项值得肯定的实证增量。这些控制增强了特定实验结论的可信度，但不自动证明它们具有普遍性或显著的实际训练后果。

## 5. Critical Weaknesses（关键不足）

**W1. 新增认识相对于已有数值敏感性研究的重要性，尚未充分明确。** 函数值相近并不能保证导数同样准确，以及通过不同前向／反向数值策略处理可微矩阵运算，已有相关研究先例。本文通过匹配优化器更新、训练期正则化调度等提供了新的特定实证信息，不能否定这一增量；但目前尚不清楚这些结果能否提炼出可迁移的判断原则、误差判据或对实现选择真正有用的指导。Table 7 中已知的对偶形式明显减小局部差异，但实验只覆盖单一固定检查点和五个任务片段；在更稳定的等价实现下，这项现象对真实训练仍有多重要，尚缺充分证据。该不足指向**信息价值和贡献重要性**，而不意味着现有实验计算错误。

**W2. 多组局部结果之间仍缺乏充分的解释联系。** §4.2–4.3 观察到梯度与单步更新差异，§4.4 报告训练终点的数值统计差异，§4.5–4.6 又通过正则化参数干预显示条件数路径差异对训练期策略的依赖。这些实验包含有效的局部干预，并非只描述现象；但现有证据尚未充分说明何时、通过什么过程，局部数值差异会形成具有实际意义的长期训练后果。对于本身秩亏的分类器，条件数直接满足 $\kappa=1+\sigma_{\max}(Z_s)^2/\lambda$，因此共享 $\lambda$ 后条件数离散程度显著降低，虽然不是数学上必然为零，也不能单独解释全部特征学习和任务效用。Table 8 的结果没有确立任务收益或等价性。作者承认了这些局限；审稿疑虑在于这些已有联系是否足以支撑论文所强调的整体解释价值。

## 6. Questions For Authors（作者问题）

**Q1. 本文相对已有数值敏感性研究，带来了哪项可影响实践的新增认识？** 在已知的求解器导数敏感性、矩阵层前后向数值策略以及岭回归对偶形式的基础上，本文的匹配优化器更新实验证据应如何改变读者的精度选择或诊断方式？考虑到 Table 7 中等价对偶形式显著减小了局部差异，作者能否澄清主要发现对更稳定实现的适用范围？若已有对偶形式完整训练证据，也请说明。

**Q2. 共享正则化调度的实验究竟解释了哪一部分训练差异？** P1–P2 的条件数路径间差异大幅减小，其中多少可以归结为 $\lambda$ 在条件数公式中的直接作用，多少涉及不同训练路径获得的特征谱变化？能否利用已有检查点或聚合结果补充 $\lambda$、特征谱与终点任务结果之间的联系，以支持所声称的解释范围？

**可能改变判断的作者回复：** 若作者能够明确定位与最接近前作的关键区别，并以已有或有针对性的新证据说明这些数值差异在稳定实现下依然具有值得关注的训练后果，录用倾向可以重新考虑。

## 7. 伦理审查与总体建议

- **伦理标记：** 暂定 No。论文已披露 AI 辅助，不能仅因披露或写作风格推断学术不端。
- **总体评分：** 暂定 Rating 2/4（倾向拒绝）。
- **Confidence：** 留由审稿人本人根据专题经验填写。

---

# Part C. Human-written Assessment 的界限与范例

## C1. 来自此次讨论的**真实、用户本人撰写的中文原话**（保留备查，不冒充“AI 使用前”版本）

> 回味这篇文章，我觉得比较让我印象深刻的点是，它分了不同的计算阶段，并且每个阶段都明确进行了干预，干预后确实很清晰地告诉了我发生了什么。同时，我觉得它的实验设置也算是严谨且完善的。
>
> 
> 但是，读了这些实验以后，我只看到了很多现象，根本不知道背后的原因是什么。作为一篇机制分析的实验，我觉得它不够清晰，实验的逻辑链条太浅了。同时，我认为它的文脉链条并没有衔接起来，不足以让我对这个问题有更深刻的理解。

> 我感觉还是没有，因为我对这个实验的结果是有预期的，感觉还是没有这种认识更新。

上述段落**由用户自行表达**，但形成于与 AI 的对话期间。若会议要求提交最初独立评估，应保留其真实来源与时间顺序，不能将其伪装成尚未使用 AI 时的文稿。

## C2. 中文完整评估结构范例——**AI 辅助生成，禁止作为原始人工初评提交**

以下示例仅用于展示一段判断怎样衔接“事实—证据—价值—不足—结论”；你应根据自身真实观点取舍：

> 这篇论文研究可微 Gram 求解器中的精度配置问题。作者通过固定输入、参数与优化器状态，比较不同精度路径的预测、梯度与真实参数更新，并进一步分析训练终点与正则化策略。印象最深的是对照设计较清晰：不仅观察输出差异，还使用固定前向的反向替换、统一精度终点评估等方式核查可能的解释。
>
>
> 但读完以后，我仍不认为论文充分说明了新增认识的重要性。求解器导数对数值实现敏感已有文献基础，本文的匹配更新测量值得肯定，却没有清晰提炼出何时这种差异会改变实际训练判断的可迁移规律。后半部分虽然对正则化参数进行了真正的训练期干预，但研究主要落在条件数离散程度上，与局部更新差异及任务表现之间的联系仍较弱。
>
>
> 因此，我目前认可论文对其有限实验结论的认真控制，但倾向认为对 ICLR 研究社区的知识增量尚不够有说服力，初步倾向弱拒。如果作者能够更明确地与最接近的前作区分，并解释稳定等价实现下结果的实际重要性，我愿意重新考虑这一判断。

## C3. English example — **AI-assisted illustration, NOT an original self-written assessment**

> The paper studies precision placement in differentiable Gram solvers through matched comparisons of predictions, gradients, and actual optimizer updates. I find the controlled design valuable, especially the restored-state comparisons, fixed-forward backward diagnostic, and common-route endpoint evaluation. These experiments make the reported local effects more interpretable than an unpaired comparison of losses alone.
>
>
> My main reservation concerns the significance and explanatory reach of the empirical advance. Derivative sensitivity and alternative numerical implementations of differentiable matrix layers already have strong precedents. Although the paper adds concrete update-level and ridge-policy evidence, I am not yet convinced that these results establish a sufficiently general or actionable understanding of when precision-induced discrepancies matter for training. The endpoint conditioning results are carefully delimited, but they do not fully connect the local diagnostics to task-level consequences.
>
>
> I therefore tentatively lean toward weak rejection on contribution/significance grounds rather than because of a demonstrated flaw in the core local experiments. A clearer distinction from the nearest prior work and a convincing account of the importance of the remaining discrepancies under stable formulations could change that view.

---

# Part D. Before submission: evidence and disclosure checklist

- [ ] Independently reread Table 3–8 and confirm that each English claim matches its actual measurement and experimental scope.
- [ ] Confirm the closest related-work comparisons in the primary sources rather than treating the AI-assisted literature audit as an exhaustive proof of priority.
- [ ] Decide whether Soundness should remain 2 or be revised in light of the limited, mostly well-controlled claims; ensure the score is explained consistently.
- [ ] Select Confidence based on your actual subject-matter expertise.
- [ ] Preserve the **real original human-written assessment** and the required full history of user inputs to AI tools; do not replace it with Part C's example.
- [ ] Make the disclosure accurately reflect reference verification, review drafting, translations, and other AI assistance. The current file does not contain the full prompt history.
- [ ] Ask the supervising reviewer to verify the review/delegation and submission requirements before posting in OpenReview.

## Key locations and sources

**Manuscript:** §3.1–3.4 (precision routes); §4.2–4.3 (Tables 2–5); §4.4 (Tables 6–7); §4.5–4.6 (Figure 1, Table 8); Appendix A.1/A.3/A.5 (protocols and metrics); Appendix B.3/B.12/B.13; Appendix C (algebraic relations).

**Official policies:** [ICLR 2027 Reviewer Guide](https://iclr.cc/Conferences/2027/ReviewerGuidelines) · [AI Policy for Reviewers](https://iclr.cc/Conferences/2027/AIPolicyForReviewers).

**Relevant literature (selection; comparison should be checked in the primary works):**

- Hückelheim et al., *A Taxonomy of Automatic Differentiation Pitfalls* (2024), [DOI](https://doi.org/10.1002/widm.1555).
- Hovland & Hückelheim, *Differentiating Through Linear Solvers* (2024), [arXiv](https://arxiv.org/abs/2404.17039).
- Song et al., *Why Approximate Matrix Square Root Outperforms Accurate SVD in Global Covariance Pooling?* (2021), [paper](https://openaccess.thecvf.com/content/ICCV2021/html/Song_Why_Approximate_Matrix_Square_Root_Outperforms_Accurate_SVD_in_Global_ICCV_2021_paper.html).
- Bertinetto et al., *Meta-learning with Differentiable Closed-form Solvers* (2019), [arXiv](https://arxiv.org/abs/1805.08136).
- Seeger et al., *Auto-Differentiating Linear Algebra* (2017), [arXiv](https://arxiv.org/abs/1710.08717).
- Maddox et al., *Low-precision arithmetic for fast Gaussian processes* (2022), [paper](https://proceedings.mlr.press/v180/maddox22a.html).
- Alder & Herbrich, *Energy-Efficient Gaussian Processes* (2024), [paper](https://proceedings.mlr.press/v235/alder24a.html).

**Accuracy boundary of the provided reference audit:** It reports selective checks of ten DOI-linked works, with one publisher-page verification where DOI metadata lookup was rate-limited; it does not establish that every reference, every citation-to-claim relationship, or the authors' experimental data has been independently verified. The supplemental audit references additional local JSON records that are **not attached to this Markdown draft** and should not be assumed accessible.
