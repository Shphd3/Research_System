---
name: hypothesis-closure
description: Use when an experiment, result, meeting note, or research iteration needs to close the loop on a hypothesis by linking original purpose, mainline anchor, setup validity, result, claim update, weakest point, next decision, and advisor-facing summary.
metadata:
  short-description: Close research hypotheses
---

# Hypothesis Closure

Use this skill after an experiment or analysis has enough result evidence to update, weaken, reject, or keep open a hypothesis.

If the experiment is not finished, write only the sections that can be filled and mark the rest as `TBD`. Do not pretend the hypothesis is closed before results exist.

## Default Location

For project-specific closure documents, write under the active project's hypothesis folder. For the current primary project, use:

```text
Projects/from-attention-to-search/XingyuD/main/hypotheses/
```

Name files like:

```text
H001_router_attention_recall_closure_MMDD.md
```

## Required Output

```markdown
# Hypothesis Closure - MMDD

## 1. Original Purpose

本轮实验原本要验证什么问题？

## 2. Mainline Anchor

它对应 architecture.md / mainline.md 里的哪一句问题定义？

## 3. Hypothesis

Hx: ...

Claim strength before experiment:
- unsupported / weakly supported / unclear

## 4. Why This Setup Tests The Hypothesis

为什么这个模型、数据、指标能测试这个假设？
边界条件是什么？

## 5. Experiment Summary

- Model:
- Data:
- Baseline:
- Metric:
- Key comparison:

## 6. Result

只写关键结果，不写流水账。

## 7. Interpretation

结果说明什么？

## 8. Claim Update

- Supported:
- Weakly supported:
- Unsupported:
- Contradicted:
- Still unclear:

## 9. What Cannot Be Claimed

明确不能说什么。

## 10. Weakest Point

导师最可能攻击哪里？

## 11. Next Decision

继续 / 修改 / 停止 / 换假设。

## 12. 30s Advisor Version

一句话目的 + 结果 + 边界 + 下一步。
```

## Rules

- One closure document should close one hypothesis or one tightly scoped hypothesis family.
- Keep the result section short; do not paste full logs.
- Separate result, interpretation, claim update, and next decision.
- Do not upgrade a claim unless the setup directly tests it.
- If the setup only tests a boundary condition, say so.
- The weakest point must be concrete: missing control, ambiguous metric, weak baseline, limited dataset, layer/head specificity, or mismatch with the mainline.
- When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.
