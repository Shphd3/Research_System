# Meeting Brief

## Meeting Summary

Conclusion:

> 真实 DCLM 文本上的 full run 没有复现 toy setting 中“step 0 common-logit 已经主导”的强结论；step 0 的主要 logit margin 来自 token residual，而不是 common component。
> 但 common component 仍然是一个真实的 route-concentration bias：去掉 common 后 max load 明显下降，并且训练前 10 步会快速把 common-logit 放大，所以主线应从“纯初始化几何导致 collapse”修正为“早期训练反馈放大 common bias”。

Minimum reason:

0. Full run 已完成：4-GPU ACP job `pt-mrx0wq1v` 成功结束，run stage 是 `full`；Phase 1/2/3/4 行数分别是 `18 / 20736 / 108 / 432`，不是 smoke run，也不是 r2 fallback。
1. 初始化主导性被削弱。主判据是 `dominance_ratio = common_margin / residual_margin`，它衡量 common logit gap 是否大于 token residual logit gap。step 0 均值是 `common_margin=0.1237`、`residual_margin=0.2364`、`dominance_ratio=0.5251`；18 个 layer/seed 里只有 1 个 `dominance_ratio > 1`。
2. common component 仍然影响路由负载。对 exact gate input 做 centering 后，`raw_max_load=0.2781` 降到 `centered_max_load=0.1561`，差值 `0.1220`。这说明 common 不是最大 margin 来源，但确实把更多 token 推向少数 expert。
3. 训练动态支持“早期放大”解释。actual $E=8$ 时，step 10 变成 `common_margin=0.7427`、`residual_margin=0.0707`、`dominance_ratio=21.7874`、`raw_max_load=0.8507`。这不是 step 0 静态几何能单独解释的现象。
4. 大 expert 数的 underuse 风险出现在训练后，而不是 step 0。step 300 时 raw active-expert ratio 在 $E=16$ 为 `0.9792`，在 $E=32$ 为 `0.9149`；但 step 0 所有实际 $E=4,8,16,32$ 都使用了全部 expert。

Current interpretation:

Observation:
真实文本中确实存在 common component，而且它会增加 top-1 routing 的负载集中；但在随机初始化 step 0，router 的最大 logit gap 主要不是由 common component 决定，而是由 token-specific residual differences 决定。

Interpretation:
toy experiment 的 common-logit story 不能原样外推成“真实文本 step 0 必然 common-dominant”。更稳妥的说法是：common component 是一个可测量的负载偏置源；sparse top-1 训练很早就会把这个偏置放大，随后形成 route concentration / expert underuse 风险。

Claim boundary:
这个结论只覆盖小型随机初始化 Qwen-style top-1 MoE、DCLM packed text、no shared expert、no load-balance loss、300-step early training。它还不能说明 pretrained MoE、最终 feature specialization、或者可部署的 anti-common router 方法。

Next decision:
下一轮不要先做新的 anti-common 方法；先做 early-training causal split。最小实验是分别 freeze gate weights、freeze hidden-state producer、freeze expert-output feedback，看 step 10 的 `dominance_ratio` 和 `raw_max_load` 到底是哪一路更新放大的。

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
