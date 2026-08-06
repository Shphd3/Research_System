# 今晚的候选最小问题与决策门

日期：2026-07-16

状态：候选计划；在人类判断和正式 Protocol 获批前，不执行实验。

英文主文档：
[02_minimal_question_and_evening_gate.md](02_minimal_question_and_evening_gate.md)

> 本计划已在 19:00 被研究者的“共享子空间冲突”定义替代。当前问题与时间表见
> [理论澄清与明日汇报锚点](05_theory_clarification_and_meeting_anchor_cn.md)。

## 建议今晚只回答这一个问题

> **标准 MTP 是否会自动提高 rare 模式相对 common 模式的学习速度？如果不会，
> “未来 horizon 相对富集 rare 信息”是否是必要条件？**

这比“为什么 MTP 有用”“为什么代码需要 MTP”小得多，但它能给明天组会增加一个
确切认识：

> MTP 不是天然 long-tail 方法；它的效果取决于未来监督改变了哪一种模式的
> 有效信息比例。

## 今晚可以正式完成的决定性步骤

在已经写明的两模式二次模型中，证明并审计：

$$
\rho_M
=
\frac{\sum_k\lambda_kq_{k,r}}
{\sum_k\lambda_kq_{k,c}},
\qquad
\rho_N=\frac{q_{1,r}}{q_{1,c}}.
$$

必须覆盖三个世界：

1. **零效应世界**：每个 horizon 的 rare/common 比相同，MTP 不改变相对速度；
2. **正效应世界**：未来 horizon 相对 rare-enriched，MTP 帮助 rare；
3. **负效应世界**：未来 horizon 相对 common-enriched，MTP 加剧失衡。

只要这三个情况在同一个形式化里闭合，我们今晚就已经完成一个 decisive 的理论
回答，而不是再产生一个宽泛假设。

## 若要做最小数值检查，必须有的对照

1. **NTP**：只有 next-token 目标。
2. **shared-aux**：头数和名义 loss scale 匹配，但 auxiliary 仍复制
   next-token 信息。
3. **informative-MTP / ratio-preserving**：增加未来信息，但 rare/common
   曲率比不变。
4. **informative-MTP / rare-enriched**：未来 horizon 提高 rare/common
   曲率比。
5. **informative-MTP / common-enriched**：必须能产生反方向结果的负对照。

候选主指标：

$$
D_{\mathrm{rel}}
=
\log\frac{\widehat Q_{M,r}}{\widehat Q_{M,c}}
-
\log\frac{\widehat Q_{N,r}}{\widehat Q_{N,c}}.
$$

其中 $\widehat Q_{j}$ 由训练早期
$-\frac{d}{dt}\log|e_j(t)|$ 的斜率估计。

这个指标只决定“相对模式学习率是否改变”，不能证明：

- 真实 long-tail accuracy；
- 普通主头因果使用；
- 代码/规划收益；
- Router 效用。

## 按 16:00 开始的 16:00–22:00 路径

| 时间 | 具体产物 | 决策门 |
| --- | --- | --- |
| 16:00–16:30 | 你闭卷填写 Thinking Card | 只冻结一个机制猜测和一个最强 rival |
| 16:30–17:15 | 共同固定 MTP 版本、common/rare 对象、效率单位、主头利用定义 | 任一对象仍混合，就不进入实验 |
| 17:15–18:30 | 逐行审计两模式命题与证明 | 明确假设，并验证零/正/负三个符号情况 |
| 18:30–19:00 | 写出反例与 cannot-claim boundary | 判断它是否构成明天的新认识 |
| 19:00–19:30 | 仅在你批准后建立正式 anchor 与 Protocol | 未批准则停止，不实现 |
| 19:30–21:00 | 只在 worker surface 运行注册后的最小数值 sanity check | 它只是实现核验，不是真实任务证据 |
| 21:00–21:30 | 用冻结指标比较解析预测与实测斜率 | 判定 pass / fail / insufficient |
| 21:30–22:00 | 你闭卷写结果；我只做证据和边界审计 | 冻结明天唯一下一决定 |

## 明天下午 13:00 前的组会答案

建议只汇报：

> **标准 MTP 并不会自动缓解 common/long-tail 失衡。它只有在新增 horizon
> 相对富集欠学习模式的有效信息时，才改变两类模式的相对收敛速度。这个条件已经
> 在最小模型中形式化；真实任务相关性和普通主头使用仍待验证。**

组会材料只需要：

- 一个定理；
- 一个零效应反例；
- 若获批并运行，则加入最小数值检查结果；
- 一条 claim boundary；
- 一个下一决定。

不要在明天同时声称代码/规划 causal effect，也不要同时提出新 Router 方法。

## 当前必须停住的位置

在你完成 Thinking Card 并批准/修改最小问题以前：

- 不建立正式 anchor；
- 不冻结 Protocol；
- 不写实验实现；
- 不更新项目对外 sync；
- 不 commit 或 push。
