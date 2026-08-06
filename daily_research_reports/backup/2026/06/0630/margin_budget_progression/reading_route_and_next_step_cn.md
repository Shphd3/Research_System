# 0630 Margin-Budget Progression: Reading Route And Next Decision

## 1. Direct Result

**当前推进结果：** 已经把 0630 的两个文档推进为 A06_21 full run。结论是：

> 在 controlled no-position bridge 中，feature-center 初始化能保持，不是因为 router row 跟着 center 主动移动，而是因为初始化后形成了正的 routing margin。训练会消耗一部分 margin，主要负向压力来自 feature-center drift，但没有把 margin 吃完，所以分发保持。

对应项目文件：

- [`A06_21 anchor`](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_21_margin_budget_preservation_audit_anchor.md)
- [`A06_21 protocol`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/protocol.md)
- [`A06_21 summary`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/summary.md)
- [`A06_21 detailed`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/detailed.md)

这一步没有提出新的初始化方法，而是把“好的 feature-center 初始化为什么训练后能保持，为什么有时会失效”改写成一个可计算的机制问题：

$$
\text{能否保持分发}
=
\text{初始 margin 是否足够覆盖训练造成的漂移}.
$$

这里的 **margin** 指的是：一个 feature center 被当前应属 expert 选中时，它相对于最近竞争 expert 的 logit 差距。差距越大，feature center 离决策边界越远，越不容易在训练中被改分到别的 expert。

这一步更新的认知是：

- A06_17_02 已经说明：保持不是因为 router row 主动跟着 feature center 移动。
- A06_17_03 已经说明：成功保持的 run 中，feature center 的漂移没有吃完初始边界距离。
- A06_17_04 已经说明：margin 是真实几何边界；强行跨过边界会破坏原来的分发。
- A06_17_05 已经说明：不需要精确中心，只要落在正 margin basin 内，就能保持。
- A06_20 已经说明：简单减 common 或 route-logit common estimator 不能稳定找回 feature residual structure。
- A06_21 进一步说明：controlled bridge 中，真正保持的条件同时满足正 margin、零 sign flip、正 cluster-aware margin、低 common share；NMI alone 不足够，因为 label-shuffled center 可以有中等 NMI 但没有保持原始 feature-to-expert identity。

因此，下一步不是再问“中心初始化有没有用”，而是问：

**训练中到底是哪一项在消耗 margin：router 边界漂移、feature center 漂移，还是 common direction 压过 residual feature direction？**

A06_21 的 controlled 答案是：center-init 条件中，负向消耗主要来自 feature-center drift；router drift 不是主要负向项；common share 很低，因此 common overwrite 不是 controlled center-init 保持的失败解释。

---

## 2. Reading Route

按下面顺序读，可以完整理解现在的推进流程。

### Step 0: 先读项目状态

读：

- [`PROJECTS.md`](../../../PROJECTS.md)

目的：明确当前研究处在第 3 层：**preservation**，也就是 step-0 proxy/feature 分发能否在 step 5/10 的训练窗口里保持。

读完要记住一句话：

> 当前瓶颈不是“能不能在 step 0 找到 proxy/feature 分区”，而是“训练是否会快速擦掉这个分区”。

### Step 1: 读 real-DCLM 失败背景

读：

- [`A06_12 summary`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md)

作用：说明真实 DCLM proxy-center 初始化在 step 0 有高 NMI，但 step 5/10 被普通训练擦掉。

要理解的结论：

> step-0 routing bridge 可以成立，但普通训练会覆盖它；这不是 loss 崩坏，而是 router/expert training feedback 改写了分发。

### Step 2: 读 controlled bridge 的保持机制

读：

- [`A06_17_02 summary`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md)
- [`A06_17_03 summary`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_17_03_feature_drift_margin_boundary/summary.md)
- [`A06_17_04 summary`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md)
- [`A06_17_05 summary`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_17_05_margin_basin_robust_initialization/summary.md)

这四个实验构成一条链：

| Experiment | 更新了什么 |
|---|---|
| A06_17_02 | 保持不是 active tracking；router row 没有朝 feature center 移动，但分发仍能保持。 |
| A06_17_03 | 成功保持时，feature center 漂移没有越过初始边界。 |
| A06_17_04 | margin 是真实边界；人为推过边界会破坏分发。 |
| A06_17_05 | 初始化不必精确，只要在正 margin basin 内即可。 |

读完要形成的理解：

> 好初始化的作用不是保证 router 永远跟着 feature center，而是在训练开始时给出一个足够宽的决策缓冲区。

### Step 3: 读失败的方法约束

读：

- [`A06_18 summary`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_18_label_free_route_relevant_state_selector/summary.md)
- [`A06_19 summary`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_19_minimal_prior_margin_aware_center_search/summary.md)
- [`A06_20 summary`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/summary.md)

作用：防止错误推进。

要理解的结论：

> 所有 hidden states 一起聚类、SAE/code 聚类、简单 route-logit common subtraction，都不能稳定给出 route-relevant feature center。feature geometry 存在，但必须用和 route-position / route-margin 更贴近的标准去选。

### Step 4: 最后读 0630 两个文档

读：

- [`A06 preservation margin-budget mini anchor`](../docs/A06_preservation_margin_budget_mini_anchor.md)
- [`Margin-budget math model derivation`](../docs/margin_budget_math_model_derivation.md)

这两个文档负责把上面的实验链收束成一个数学问题。

先读 mini anchor，抓住问题和判定：

> 能否把 early preservation failure 解释为 initial margin 被 training drift 消耗完？

再读 math derivation，抓住核心分解：

$$
\gamma_{f,e}(t)
=
\gamma_{f,e}(0)
+
\Delta u_{f,e}(t)^\top \mu_f(0)
+
u_{f,e}(0)^\top \Delta \mu_f(t)
+
\Delta u_{f,e}(t)^\top \Delta \mu_f(t).
$$

其中：

- $\gamma_{f,e}(0)$：初始 margin。
- $\Delta u_{f,e}(t)^\top \mu_f(0)$：router 边界自己移动造成的 margin 变化。
- $u_{f,e}(0)^\top \Delta \mu_f(t)$：feature center 移动造成的 margin 变化。
- $\Delta u_{f,e}(t)^\top \Delta \mu_f(t)$：router 和 feature 同时移动造成的交互项。

读完要得到的判断：

> 后续实验不应该只看 NMI 是否下降，而要把 NMI 下降对应到 margin 被哪一项消耗。

### Step 5: 读 A06_21 full run

读：

- [`A06_21 summary`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/summary.md)
- [`A06_21 detailed`](../../../Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/detailed.md)

读完要记住：

| Condition | Step 10 NMI | Step 10 min margin | Step 10 sign flip | 解释 |
|---|---:|---:|---:|---|
| pseudo-center | 1.000 | 5.688 | 0.000 | 正 margin 保持分发 |
| oracle-center | 1.000 | 5.771 | 0.000 | 正 margin 保持分发 |
| random | 0.823 | -1.394 | 0.229 | 没有稳定正 margin |
| equal-norm random | 0.827 | -1.420 | 0.229 | 等范数不能解决分区 |
| label-shuffled center | 0.869 | -0.685 | 0.286 | NMI 中等，但不是原始匹配保持 |

核心理解：

> margin / sign flip / preserve fraction 比 NMI 更接近“是否真的保持了原来的 feature-to-expert 分发”。

---

## 3. Current Mechanism Map

当前主线可以压成这条链：

```text
普通 top-1 routing 容易坍缩
-> feature/proxy center 可以在 step 0 构造干净分发
-> 普通训练可能擦掉这个分发
-> controlled bridge 中，好的初始化能保持
-> 保持不是因为 router 跟着 center 走
-> 保持更像是初始 margin buffer 足够大
-> margin 是真实几何边界
-> A06_21 full run 支持 controlled bridge 的 margin-budget 解释
-> 下一步把同样的分解带到 real-DCLM proxy-init 失败上
```

---

## 4. Next Decision

**下一步最自然的判定：** 把 A06_21 的 margin-budget audit 搬到 real-DCLM A06_12 proxy-init training 上。

### Decision Question

real-DCLM 中，proxy-center 初始化为什么 step 0 有效、step 5/10 被擦掉？

需要区分三种可能：

1. step 0 residual margin 本来就弱；
2. step 0 margin 足够，但 early training 把它吃完；
3. common direction 增长，压过 residual feature term。

在 controlled bridge 中，可以先用下面这个量理解 preservation / collapse：

$$
R(t)=\frac{\text{drift budget}(t)}{\Gamma(0)}.
$$

这里 $R(t)$ 是 **margin consumption ratio**，即训练漂移消耗了多少初始 margin。

### Primary Metric

主指标仍然是：

$$
\text{proxy/feature-route NMI at step 5/10}.
$$

原因：NMI 直接回答“原来的 feature/proxy 分区是否还被 expert 分开”。

### Mechanism Metrics

需要同时计算：

| Metric | 作用 |
|---|---|
| initial min margin $\Gamma(0)$ | 初始分发缓冲有多大。 |
| drift budget $B(t)$ | 训练造成的最坏 margin 消耗上界。 |
| consumption ratio $R(t)$ | margin 是否被吃完。 |
| sign flip rate | 哪些 feature-expert pair 已经跨边界。 |
| router drift term | 是否主要是 router 边界移动。 |
| feature drift term | 是否主要是 feature center 移动。 |
| common term $u^\top c$ | 是否 common direction 主导 routing。 |
| residual term $u^\top r_f$ | feature-specific residual 是否仍然支撑分发。 |

### Pass / Fail / Insufficient

| Outcome | 判断 | 下一步 |
|---|---|---|
| real-DCLM step 0 margin 已经弱 | 失败主要是初始化表面好、真实 buffer 小 | 回到 proxy/center selection，要求 residual margin guard。 |
| real-DCLM step 0 margin 强，但 step 5/10 被吃完 | 失败主要是 early training drift | 研究 router LR、expert feedback、anti-drift window。 |
| common term 增长压过 residual term | 失败主要是 common overwrite | 连接 spectral/common-band 机制，设计 common-band guard。 |
| router drift term 主导 margin 消耗 | router-side early lock-in supported | 研究早期 router 更新、common alignment、load feedback。 |
| feature drift term 主导 margin 消耗 | feature-center drift supported | 研究 hidden-state 表征漂移，以及 center tracking / representation stabilization。 |
| NMI 掉但 $R(t)\ll 1$ 且无 sign flip | margin model insufficient | 转向 expert feedback、token-level spread、metric mismatch 或 objective conflict。 |
| $R(t)>1$ 但 NMI 仍高 | norm-bound budget 太松或 NMI 不够严格 | 改用 token-level cluster-aware margin 和 preserve fraction。 |

---

## 5. What This Does Not Claim

现在还不能声称：

- margin-budget 已经解释了 real-DCLM preservation failure；
- 去 common 就一定能恢复 feature specialization；
- feature-center 初始化一定能长期保持；
- NMI 高就说明 expert 有功能价值；
- controlled synthetic 结果可以直接推出真实语义 feature。

现在可以更稳地声称：

> controlled bridge 中，center initialization 的保持是正 margin buffer 的结果；下一步需要把 real-DCLM failure 分解到 step-0 residual margin、early drift、common overwrite、token spread 这些具体项上。

---

## 6. Suggested Immediate Artifact Path

这条路线已经正式化并完成 full run：

```text
Anchor:
  Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_21_margin_budget_preservation_audit_anchor.md

Protocol / results:
  Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/

Full-run result:
  controlled bridge supported; real-DCLM audit is next
```

是否需要新训练：

```text
First pass for real-DCLM:
  no new training if A06_12 saved hidden states and router rows.

Second pass:
  rerun minimal A06_12 snapshot collection only if needed.
```

---

## 7. One-Minute Explanation

这条线现在不是在证明某个初始化方法一定有效，而是在理解为什么有些初始化能保持、有些会被训练擦掉。

目前 controlled bridge 的结果说明：好的 center 初始化并不是因为 router row 一直追着 feature center 走，而是因为一开始 feature 到 expert 的 logit gap 足够大。训练会移动 router，也会移动 hidden-state feature center；在这次 A06_21 full run 中，负向消耗主要来自 feature-center drift，但它没有吃完初始 margin，所以分发保持。一旦 margin 被吃完，feature 就会跨过 expert 决策边界，NMI 或 matched preserve fraction 就下降。

因此下一步要做的不是再换一个聚类方法，而是把 real-DCLM 的 step-0 到 step-5/10 failure 拆成三项：router 边界动了多少，feature center 动了多少，common direction 是否压过了 residual feature direction。这样才能知道真实瓶颈是初始化 residual margin 不够、router 早期锁死、表征漂移，还是 common-band overwrite。
