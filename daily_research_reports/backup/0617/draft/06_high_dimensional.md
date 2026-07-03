# Minimal Anchor Handwrite Draft

Use this by hand before asking AI to critique or polish the anchor. Write rough
bullets. This file is a thinking draft, not a final anchor.

Default workflow:

```text
minimal hand-written anchor
-> AI critique and clarification
-> formal anchor
-> user review
-> protocol.md
-> implementation / run
```

The formal anchor is the project-local equivalent of
`docs/design.md` in the research-exploration workflow. It should explain the
research design, not only summarize a result.

Use `Thinking Card` as a short anchor replay: it should let you recover the
current question, judgment, evidence, boundary, and next decision before
reading the full anchor. The rest of the anchor is the auditable design layer
for AI critique, replay, and boundary checks.

## AI Use Contract

When an AI reads this draft, its first job is to audit the user's logic before
writing a formal anchor. It should identify:

- which user judgments should be preserved;
- which object, feature definition, metric, scope, or causal claim is unclear;
- whether the physical priors are falsifiable and sufficient;
- which hypotheses lack falsifiers;
- whether the mathematical model maps to measurable variables;
- whether the computational realization prevents math/code drift;
- which minimal tests still need user approval.

The AI should not silently replace the user's research question, feature key,
physical prior, or next decision. Candidate new priors must be proposed for
user approval before entering the formal anchor.

## User Notes

My uncertain points:

Do not silently change:

AI should challenge:

Candidate physical priors I am not sure about:

## 0. Thinking Card

父问题：如何做一个更好的expert-aware 同时屏蔽common的 router 初始化？

当前子问题：在 features 均匀分布的高维空间中，如何做一个将features均匀分发到各个expert上的初始化？

当前判断：对于不同的专家，具有不同的初始化，我们需要根据这种不同的初始化来划分完整的均匀分布的表征空间，从而让表征均匀分布和专家均匀分布对齐。

关键证据：

最危险边界：

下一步决策：

## 1. Problem Definition

Parent problem: 

Sharper subproblem: 如何做一个更好的expert-aware 同时屏蔽common的 router 初始化？避免MoE早期训练的坍缩。

Decision question: 在 features 均匀分布的高维空间中，如何做一个将features均匀分发到各个expert上的初始化？

Not in scope:

## 2. Physical Priors

P1:

Meaning:

Could be wrong if:

## 3. Falsifiable Hypotheses

H1:

Supported if:

Weakened if:

## 4. Mathematical Model

Objects:

Core decomposition:

Mechanism relation:

Observable metrics:

Falsifier:

## 5. Computational Realization

Purpose: prevent the mathematical object and implemented object from drifting
apart.

Input objects:

Computed variables:

Algorithm stages:

Stage-local evidence:

Expected artifacts:

## 6. Minimal Falsification Tests

Test:

Question:

Intervention / comparison:

Primary metric:

Supports:

Weakens:

Insufficient evidence:

## 7. Current Evidence

Observation:

Interpretation:

Boundary:

Evidence links:

## 8. Claim Boundary And Next Decision

Can claim:

Cannot claim:

Next decision:
