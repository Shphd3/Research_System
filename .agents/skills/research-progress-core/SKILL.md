---
name: research-progress-core
description: "Maintain question-level research judgment, discover or refine a question, choose a minimal falsifier, or interpret results and failures. Not remote operations, publication or final-report ownership."
---

# Research Progress Core

Reduce one consequential uncertainty with the smallest test that can change a
judgment. The researcher owns scientific choices; AI proposes labeled
alternatives (`AI 建议`). `Unknown` is valid.

## Exploration lane output (default)

Write or append one entry in `main/explore/MMDD_<slug>/log.md`
(`templates/explore_log_cn.md`): 假设, 先验→模型→计算, 跑前预测 (A/B/不足 branches), 竞争解释,
结果 with raw numbers, 研究者决定, 链条位置. Before running, the prediction and
branches must exist. After results, decide by the pre-written branch first, then
interpret. End the day with `今日认识更新`. Check the project's active-question
budget (≤3, `PROJECTS.md`) before opening a new question.

## How to think

- 形成结论时先写一句“这次观察让我们对哪项科研选择改变了看法”，再写一句最能区分两种解释的比较。把实验覆盖和操作细节放在证据记录。评价理想假设时，指出它对哪个预测足够准确、在哪里需要用实测量替换，以及替换后会改变哪一步推导。向导师汇报时收敛为一个可讨论的取舍。

- For ongoing work, anchor interpretation to the sourced original question and
  pre-result hypotheses before choosing an explanation; apply the kernel's
  [Question And Structure](../../../docs/methodology/research_exploration_kernel.md#1-question-and-structure)
  rule. A useful new phenomenon does not replace the question being answered.
- In follow-ups, use [Multi-Turn Continuity](../../../docs/methodology/research_exploration_kernel.md#multi-turn-continuity)
  to advance the missing explanatory link without restarting settled discussion;
  the existing reasoning and evidence checks still apply.
- Start from structure, not a metric: state the falsifiable prior, derive the
  mathematical quantity or objective it implies, then the computation that
  measures it. If a proposed step cannot be traced this way, say so and repair
  the chain before running.

- Work backward from the desired outcome. Identify the decision that depends
  on this measurement and the assumption it can change. Put forward your best
  mechanism conjecture, even if the researcher did not supply it. Explain which
  observation would favor its strongest rival and how that would change the action.
- Keep observation, readout, intervention and training benefit apart; a local
  effect is not a design decision.
- Prioritize the comparison that resolves that choice. For `纯理解`, say which
  relation in the explanation or derivation becomes clearer.

## References (read only when needed)

New question: [discovery](references/problem_discovery.md) ·
child question: [refinement](references/question_refinement.md) ·
result or failure: [interpretation](references/result_interpretation.md),
[failure decomposition](references/failure_decomposition.md) ·
repeated failure: [goal audit](references/goal_audit.md) ·
fragile algorithm: [specification](references/algorithm_specification.md).

Do not create Focus files (retired), execute, publish or change scientific state
beyond scope. Formal records keep their own owners (`docs/formal_lane.md`).
