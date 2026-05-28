---
parent_node: <parent_problem>
---

# <Problem Title>

## 汇报前 Summary

这一节只写汇报前的最短 summary，不展开完整论证。目标是让合作者先知道：
我们在问什么、为什么问、当前结果/预期判断是什么、边界在哪里、下一步做什么。

父问题：

```text
这个 anchor 属于哪个更大的研究问题？
```

当前子问题：

```text
这次只隔离和判断哪个小问题？
```

为什么要问这个问题：

```text
之前哪个结果、失败模式或矛盾使这个 anchor 必要？
```

决策问题：

```text
这个 anchor 最终要帮助我们判断哪一个问题？
```

任务构造：

```text
用什么最小构造或对照暴露这个机制？
```

当前结果 / 预期结果：

```text
如果已经有结果，用一句话总结。
如果还没跑，写清什么结果支持、削弱或重定向这个假设。
```

结论边界：

```text
这个 anchor 能声称什么，不能声称什么？
```

下一步：

```text
下一个最小研究动作是什么？
```

## 1. Problem Definition

1. broader question
   $$\downarrow$$
2. sharper question
   Used to clarify which parent question this sharper question belongs to.

Key: decide what we don't need to do.

Operational definitions, only for decision-critical terms:

```text
term_1: success / failure / ambiguous or insufficient evidence
term_2: success / failure / ambiguous or insufficient evidence
term_3: success / failure / ambiguous or insufficient evidence
```

## 2. Physical Priors

- Features
  - They should have physical meaning in the real world.
  - They can be refuted.
  - They can guide mathematical modeling.
  - They should guide real implementation.

## 3. Mechanistic Motivation

Explain why these priors obey the real-world facts.

## 4. Mathematical Modeling

physical prior -> objects -> variables -> mapping/operator -> observable metric

## 5. Computational Realization

### 5.1 Workflow Interface

If the hypotheses hold, then the system should look like...
Define the input, computation, then output.

### 5.2 Minimal Computational Test

Use the smallest controlled synthetic setup where task factors are known and
expert causal utility can be measured.

## 6. Minimal Falsifiable Test

mathematical object -> implementation object -> metric

## 7. Falsifiable Outcomes

Supported if ...
Weakened if ...
Still not proven ...

## 8. Current Evidence


## 9. Claim Boundary And Next Decision
