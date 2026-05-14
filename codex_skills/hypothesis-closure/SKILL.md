---
name: hypothesis-closure
description: Use when an experiment, result, meeting note, or research iteration needs to close the loop on a hypothesis in Chinese by linking original purpose, mainline anchor, setup validity, result, claim update, weakest point, next decision, and advisor-facing summary.
metadata:
  short-description: Close research hypotheses
---

# Hypothesis Closure

Use this skill after an experiment or analysis has enough result evidence to
update, weaken, reject, or keep open a hypothesis.

Default language is Chinese. Use English only for code identifiers, metric
names, file paths, or when the user explicitly asks for English.

If the experiment is not finished, write only the sections that can be filled
and mark the rest as `TBD`. Do not pretend the hypothesis is closed before
results exist.

## Location Rule

Every completed experiment or recursive stage must first have a local closure
inside its experiment summary:

```text
Projects/<project>/main/experiments/<experiment_id>/summary.md
Projects/<project>/main/experiments/<experiment_project_id>/stages/<stage_id>/summary.md
```

Use local `summary.md` to close the experiment's immediate hypothesis.

Use the active project's `hypotheses/` folder for advisor-facing big closure
documents that synthesize one experiment line or one tightly scoped hypothesis
family. Each big closure should be a subfolder with its own figures:

```text
Projects/from-attention-to-search/XingyuD/main/hypotheses/<closure_id>/
  hypothesis_closure.md
  figures/
```

Name big closure files like:

```text
H001_router_attention_recall_closure_MMDD/hypothesis_closure.md
```

Big closure documents may link back to local experiment `summary.md` files, but
they must be self-contained: a reader should understand the purpose, setup,
result, claim boundary, and next decision without reading previous experiments
or chat context.

## Required Output

```markdown
# 假设闭环：<name> - MMDD

## 1. 原始目的

本轮实验原本要验证什么问题？

## 2. 主线锚点与待判定假设

它对应 architecture.md / mainline.md 里的哪一句问题定义？

Hx: ...

实验前证据强度：
- 未支持 / 弱支持 / 不清楚

## 3. 直接结果

只写关键结果，不写流水账。

## 4. 关键图片

- Figure:
- Path:
- Supports:

## 5. 解释

结果说明什么？

## 6. Claim 边界

- 支持：
- 弱支持：
- 不支持：
- 被反驳：
- 仍不清楚：

明确不能说什么。

## 7. 最弱点与下一步

导师最可能攻击哪里？
继续 / 修改 / 停止 / 换假设。

## 8. 30 秒汇报版本

一句话目的 + 结果 + 边界 + 下一步。
```

## Rules

- One closure document should close one hypothesis or one tightly scoped hypothesis family.
- Write closure documents in Chinese by default.
- Local experiment closure belongs in `experiments/.../summary.md`.
- Advisor-facing big closure belongs in `main/hypotheses/`.
- Big closure should be self-contained. Do not assume the reader knows previous
  failed runs, chat history, or why a design changed. Mention prior context only
  if it is essential to the current claim.
- Big closure may reference the local summary files it synthesizes, but should
  not depend on them for basic comprehension.
- Keep the result section short; do not paste full logs.
- Put setup details, metric details, and long tables in the corresponding experiment `summary.md` / `detailed.md`, not in the big closure.
- Copy report-ready figures into the closure folder's `figures/` directory and
  embed them with Markdown image links when figures exist.
- Merge mainline anchor with hypothesis, merge claim update with cannot-claim boundaries, and merge weakest point with next decision.
- Do not upgrade a claim unless the setup directly tests it.
- If the setup only tests a boundary condition, say so.
- After a closure is complete, state whether `consensus.md` should be updated and which specific item changes.
- The weakest point must be concrete: missing control, ambiguous metric, weak baseline, limited dataset, layer/head specificity, or mismatch with the mainline.
- When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.
