# Meeting Brief

## Meeting Summary

Conclusion:

1. 没有position embedding，同时feature在sequence中移动情况下，collapse仍然存在
2. 被路由的hidden state中含有feature信息
3. 路由崩塌最主要被common logit部分决定，我们将hidden state 分割为：$h = c + r_{slot} + u_{postion} + residual_{s, p}$, 我们发现最终290/320 个 cell 是 common component 主导，并且在优化10步以后，就稳定collapse.【下一步，控制变量，查明common来源】

```text
c = mean_{s,p}(m_{s,p})
r_s = mean_p(m_{s,p}) - c
u_p = mean_s(m_{s,p}) - c
residual_{s,p} = m_{s,p} - c - r_s - u_p
```

Minimum reason:

Current interpretation:

Next decision:

1. 需要查明，这个common造成的gating logit，是一开始就很大，还是后面慢慢长出来的
2. 对于slot-init的情形，我们发现几乎所有的的seeds都产生了slot-level的specialization, 这非常令人诧异，让人感到疑惑，难道仅仅只是初始化到附近，就直接lock-in吗？common component是否长出来了呢？
3. 为什么这种均匀随机初始化，就是会对齐common component呢？

## Meeting Preparation

**Question:**

[One core question this meeting should answer.]

**Why this matters?**

[Explain why it affects the mainline judgment, claim boundary, or next experiment decision.]

**Hypothesis:**

[Falsifiable research hypothesis. State the parent problem / subproblem relation when needed.]

**Evidence:**

[Summarize the key evidence. Put the most important metric or figure first because it decides this judgment.]

1. [Evidence point: metric / figure / table / experiment condition.]
2. [Evidence point: what it cannot prove.]

**Boundaries:**

[State which conditions, data, model, training objective, initialization, or metric this conclusion covers.]

**Cannot claim yet:**

[State the stronger conclusion that cannot be claimed yet.]

**Next Decision:**

[The smallest decision after this meeting: continue, redirect, add one diagnostic, or park.]

**Next Iteration:**

[If continuing, write the minimal decisive experiment. If not, write the park or redirect condition.]
