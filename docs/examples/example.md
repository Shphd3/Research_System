---
parent_node: <parent_problem>
---

# <Problem Title>

## 汇报前 Summary

这一节只写导师汇报用的最短 summary，不展开完整论证。目标是让导师在
60 秒内明白：我在问什么、我的假设是什么、我用什么证据让问题变清楚、
当前判断是什么、边界在哪里、下一步做什么。

问题：

```text
我现在要解决哪个具体问题？它为什么属于当前主线？
```

假设：

```text
我认为哪个机制/先验可能成立？
```

证据入口：

```text
放一张关键图，或用 2-3 句话说明最小实验怎么暴露这个机制。
导师应该能从这里立刻知道我到底在做什么。
```

当前判断：

```text
已有结果说明什么？如果还没跑，什么结果会支持/削弱/重定向这个假设？
```

结论边界：

```text
现在能说什么，不能说什么？
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

Each physical prior must satisfy four requirements:

1. Real-world meaning: it says something concrete about the task, data,
   system, environment, representation, mechanism, intervention, or objective.
2. Refutability: it can be wrong, and the anchor names what evidence would
   weaken or redirect it.
3. Mathematical constraint: it maps to objects, variables, relations, or
   observables in the model.
4. Implementation constraint: it determines what data, intervention, metric,
   artifact, or control the experiment must use.

## 3. Mechanistic Motivation

Explain why these priors obey the real-world facts.

## 4. Mathematical Modeling

physical prior -> objects -> variables -> mapping/operator -> observable metric

## 5. Computational Realization

### 5.1 Workflow Interface

If the hypotheses hold, then the system should look like...
Define the input, computation, then output.

### 5.2 Minimal Computational Test

Use the smallest controlled setup where the relevant factors are known and the
claimed mechanism can be measured, intervened on, or clearly falsified.

## 6. Minimal Falsifiable Test

mathematical object -> implementation object -> metric

## 7. Falsifiable Outcomes

Supported if ...
Weakened if ...
Still not proven ...

## 8. Current Evidence


## 9. Claim Boundary And Next Decision
