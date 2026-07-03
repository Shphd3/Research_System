# Group Meeting Report Logic Template

## 0. Core Rule

Do not report the work as a list of anchors or methods.
Report it as one decision chain:

```text
uniform feature does not guarantee feature specialization;
we decomposed why initialized top-1 routing fails;
we found which controls are load-only and which controls can actually reach feature partition;
now the next decision is feature discovery before routing and training-basin preservation.
```

## 1. One-Minute Opening

Use this exact structure:

```text
这轮我想回答一个问题：
在 uniform feature distribution 下，初始化 top-1 MoE 能不能形成 feature-level specialization？

我现在的结论不是“已经有最终 gating 方法”。
我的结论是：
1. 目标 partition 在 oracle 条件下可达；
2. simple global common/residual controls 只能改善 load，不能恢复 feature_NMI；
3. 所以下一步必须做 label-free feature discovery，再测试 training 是否保持这个 partition。
```

## 2. Main Story Line

Do not say first: “I did A06_03, A06_04, ...”

Say first:

```text
我把初始化路由失败拆成五个问题。
```

Then use this map:

| Step | Question | Update |
|---|---|---|
| Gate-only geometry | random Gaussian gate 在 uniform sphere 上为什么 load 不均？ | row norm 是 gate-only 额外 fixed floor |
| Hidden-state audit | uniform symbolic features 进入 initialized hidden states 后，还是 norm 主导吗？ | common component 是主导 tested source |
| Residual diagnostic | common-centering 后剩余 load 是什么？ | residual covariance / structured geometry 仍存在 |
| Oracle positive control | feature-level partition 是否可达？ | oracle centroid 可达，NMI=1, L=0 |
| Label-free global control | global centering / whitening 能否近似 oracle？ | 不能，load 改善但 NMI 不改善 |

## 3. Slide-Level Template

Each slide must have only one scientific claim.

Use this format:

```text
Question:
What I tested:
Observation:
Interpretation:
Boundary:
Next decision:
```

Never show a figure without saying:

```text
This figure answers which question.
The y-axis means what.
Which direction supports the claim.
What it cannot prove.
```

## 4. Latest Result Should Be Framed Like This

```text
A06_06 和 A06_07 合起来给了一个关键判断：
feature partition 不是不可达；oracle centroid 能做到。
但 simple label-free global controls 找不到它。
所以问题不是“继续调 centering / whitening”，而是：
hidden state 里是否有可 label-free 发现的 pseudo-feature centers？
```

## 5. Next Decision Request To Advisor

End with a clear ask:

```text
我现在计划做两步：
1. A06_08：在 routed-position 和 all-hidden 两个 scope 上做 label-free feature discovery，测试 pseudo centers 能不能接近 oracle partition；
2. A06_09：如果 pseudo/oracle init 能产生 step-0 partition，测试训练是否保持，还是需要 anti-lockin。

我想请您判断：
这个顺序是否合理？
还是我应该先做 training-basin preservation，再回头做 feature discovery？
```

## 6. What Not To Say

Avoid:

```text
我想设计一个更好的 gating。
我试了很多方法。
这个方法 load 更均匀，所以可能更好。
```

Use:

```text
这个方法测试的是哪个机制项？
它是否提高 feature_NMI？
它是否改变 claim boundary？
```

## 7. Five-Sentence Backup Summary

If the advisor interrupts, use this compressed version:

```text
我现在把问题从方法搜索改成机制裁定。
06_03--06_05 说明初始化 load imbalance 可以来自 row norm、hidden common 和 residual geometry。
06_06 说明 feature-level partition 在 oracle centroid 下可达。
06_07 说明 simple label-free global controls 只是 load-only，不能恢复 specialization。
所以我下一步想测 label-free feature discovery 是否能找到 pseudo centers，以及这种初始化在训练中是否保持。
```
