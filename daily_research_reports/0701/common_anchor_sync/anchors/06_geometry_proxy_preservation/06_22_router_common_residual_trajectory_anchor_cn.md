# A06_22：Router Common-Residual Trajectory Audit

文档状态：待审阅 draft anchor。英文版
`06_22_router_common_residual_trajectory_anchor.md` 是 canonical source。
本锚点继承 A06_21，用来决定下一步 real-DCLM preservation 审计是否应聚焦
router 更新轨迹，而不是继续提出新的初始化方法。

## 0. Thinking Card

**现象：** real-DCLM proxy-center routing 在 step 0 可以很强，但会被早期普通
top-1 训练擦掉。受控 A06_21 说明正 margin 能保持分区，但还没有解释
real-DCLM 中 router update 为什么会覆盖 proxy partition。

**机制猜想：** router gap 的更新可能朝向一组层级化 common modes，而不是朝向
feature-residual directions。单次 common subtraction 可能只移除了最显眼的
common component，但 class、context、position 或 route-logit common 仍可能主导
router trajectory。

**关键变量：** hidden state $h_i(t)$、固定 proxy label $y_i=f$、feature center
$\mu_f(t)$、common-mode projector $P_C$、residual center
$r_f(t)=(I-P_C)\mu_f(t)$、router row $w_e(t)$、assigned expert $a(f)$、
router gap $u_{f,e}(t)=w_{a(f)}(t)-w_e(t)$、router-gap update
$\Delta u_{f,e}(t)=u_{f,e}(t)-u_{f,e}(0)$、common margin term
$\gamma^C_{f,e}(t)$、residual margin term $\gamma^R_{f,e}(t)$、
proxy-route NMI、sign flip rate、LM loss。

**因果关系：** 如果早期 router-gap updates 被 common-mode directions 主导，
那么即使 residual feature information 仍在 hidden states 中，proxy-route NMI
也可能下降。若 updates 是 residual-aligned 但 margin 仍失败，则主要失败机制
不是 common-mode router trajectory。

**可观测指标：** 主指标是 step 0 到 step 5/10 窗口中的 common-over-residual
router update dominance ratio，并以 proxy-route NMI 和 LM loss 作决策保护。

**对立解释：** step-0 residual margin 本来就弱；feature centers 跨越固定
router boundaries；router boundary drift 与 common modes 无关；proxy labels
不稳定；expert feedback 使 proxy partition 与目标不兼容；common projector
定义错误。

**决策：** 如果 common-over-residual update dominance 能预测 real-DCLM
proxy-route collapse，就推进这个 diagnostic anchor。若 NMI collapse 不伴随
common-dominated router updates，或结论完全依赖 common projector 选择，则修正
或暂停。

## 1. Problem Definition

**父问题：** A06 研究如何为 top-1 MoE gating 找到并保持 route-relevant proxy
或 feature partitions。

**更尖锐子问题：** A06_21 解释了 controlled no-position bridge 中 positive
margin preservation。real-DCLM 中尚未解决的问题是：为什么普通训练会离开一个
强 step-0 proxy assignment。

**术语解释：**

**Router gap**  
含义：原 assigned expert 与一个 competing expert 之间的成对打分方向。  
具体对象：

$$
u_{f,e}(t)=w_{a(f)}(t)-w_e(t).
$$

为什么重要：router specialization 由这些 gap 读取哪些方向决定。  
不能证明：expert utility 或 semantic specialization。

**Common-mode subspace**  
含义：承载跨特征共享、高频或高增益结构的预先指定子空间。  
具体对象：不使用测试 route labels 拟合的正交投影 $P_C$。  
为什么重要：如果 router gaps 对齐这个子空间，routing 可能稳定但不区分。  
不能证明：所有大奇异值都有害。

**Feature-residual center**  
含义：移除 common subspace 后的 feature center 部分。  
具体对象：

$$
r_f(t)=(I-P_C)\mu_f(t).
$$

为什么重要：它是候选 feature-specific route identity direction。  
不能证明：functional expert value。

**Common-over-residual update dominance**  
含义：router-gap movement 是否比 feature-residual directions 更对齐 common
directions。  
具体计算：

$$
\Lambda_{\mathrm{upd}}(t)
=
\operatorname{median}_{f,e}
\frac{
\left|\Delta u_{f,e}(t)^\top P_C\mu_f(0)\right|
}{
\left|\Delta u_{f,e}(t)^\top r_f(0)\right|+\varepsilon
}.
$$

为什么重要：它直接测试早期 router movement 是否 common dominated。  
不能证明：除非同时伴随 NMI drop 和 margin sign changes，否则不能单独证明
common dominance 导致 collapse。

**决策问题：** 在 real-DCLM proxy-init training 中，早期 router-gap updates
是否被 common-mode hierarchy 主导，而不是被 feature-residual directions 主导；
这种主导是否解释 proxy-route collapse？

**不在范围：** 构造新 gating 方法、证明 semantic experts、证明 utility、替代
A06_21 margin-budget model。

## 2. Physical Priors

**P1：Top-1 gating 读取方向，不读取标签。**  
含义：route assignment 由 router rows 和 hidden states 的 dot product 控制。
如果 router gaps 对齐 common directions，即使 residual feature information
存在，labels 也可能丢失。  
可能错误：route collapse 发生时，router gaps 仍 residual aligned 且 common
terms 很小。

**P2：Common structure 可能是层级化的。**  
含义：移除单一 global mean 或 top common direction 可能仍留下 class、context、
position 或 route-logit common components。  
可能错误：一次明确定义的 common removal 后，router update dominance 稳定转向
residual feature directions。

**P3：Preservation 需要 residual-discriminative margin，而不只是 positive
margin。**  
含义：positive margin 可以保持 stable assignment，但 feature-level
specialization 要求 margin 来自 residual feature contrast，而不是 common-mode
score。  
可能错误：common-dominated margins 仍能预测 feature identity 和后续 expert
utility。

## 3. Falsifiable Hypotheses

**H1 common-trajectory hypothesis：** real-DCLM 早期 router-gap updates 被
common-mode directions 主导。  
支持条件：$\Lambda_{\mathrm{upd}}(5)$ 或 $\Lambda_{\mathrm{upd}}(10)$ 在
seeds/conditions 中大于 1，且 common update terms 与 proxy-route NMI 下降同步。  
削弱条件：router-gap updates 是 residual-aligned，但 NMI 仍下降。

**H2 residual-margin insufficiency hypothesis：** step-0 proxy routing 脆弱，
因为 residual margin 弱，即使 total margin 或 NMI 看起来强。  
支持条件：高 step-0 proxy-route NMI 下，大量 pair 的 $\gamma^R_{f,e}(0)$
仍小或为负。  
削弱条件：step 0 residual margins 强，且只在 training drift 后被消耗。

**H3 common-projector robustness hypothesis：** 结论不是某一个 common 定义的
artifact。  
支持条件：mean-common、top-band common、route-logit common projectors 得到相同
定性的 common-over-residual trajectory 结果。  
削弱条件：换 common projector 后结论翻转。

## 4. Mathematical Model

**对象：** fixed proxy labels $y_i=f$，feature centers $\mu_f(t)$，common
projector $P_C$，residual centers $r_f(t)=(I-P_C)\mu_f(t)$，router rows
$w_e(t)$，assigned expert $a(f)$，router gaps $u_{f,e}(t)$，router-gap
updates $\Delta u_{f,e}(t)$。

**核心分解：** 将 pairwise margin 拆成 common 和 residual 两项：

$$
\gamma_{f,e}(t)
=
u_{f,e}(t)^\top \mu_f(t)
=
\underbrace{u_{f,e}(t)^\top P_C\mu_f(t)}_{\gamma^C_{f,e}(t)}
+
\underbrace{u_{f,e}(t)^\top r_f(t)}_{\gamma^R_{f,e}(t)}.
$$

用同一几何分解 router-side margin update：

$$
\Delta \gamma^{\mathrm{router}}_{f,e}(t)
=
\Delta u_{f,e}(t)^\top \mu_f(0)
=
\Delta u_{f,e}(t)^\top P_C\mu_f(0)
+
\Delta u_{f,e}(t)^\top r_f(0).
$$

定义 common-over-residual update dominance ratio：

$$
\Lambda_{\mathrm{upd}}(t)
=
\operatorname{median}_{f,e}
\frac{
\left|\Delta u_{f,e}(t)^\top P_C\mu_f(0)\right|
}{
\left|\Delta u_{f,e}(t)^\top r_f(0)\right|+\varepsilon
}.
$$

**机制关系：** 如果 $\Lambda_{\mathrm{upd}}(t)>1$，同时 proxy-route NMI 下降且
residual margins 缩小或没有增长，那么支持 common-dominated router trajectory。
如果 $\Lambda_{\mathrm{upd}}(t)<1$，或 residual terms 主导而 NMI 仍下降，则
common-mode trajectory 不是主要解释。

**可观测指标：** step 5/10 proxy-route NMI、LM loss、load concentration、
sign flip rate、$\gamma^C$、$\gamma^R$、$\Lambda_{\mathrm{upd}}$、residual
margin share、common-projector robustness。

**证伪条件：** proxy-route collapse 在多个 common definitions 下都不随 common
update dominance、residual margin loss 或任何 common/residual decomposition
变化。

## 5. Computational Realization

**输入对象：** real-DCLM A06_12-style proxy-init checkpoints，包括 routed
position hidden states、fixed proxy labels、router rows、route assignments、
LM loss 和 expert load。

**计算变量：** feature centers、多个 common projectors、residual centers、initial
feature-to-expert matching、router gaps、router-gap updates、common/residual
margin terms、update dominance ratios、sign flips、NMI、loss/load guards。

**算法阶段：** 收集 checkpoints；在不泄漏测试标签的前提下拟合 common
projectors；计算 center 和 residual terms；分解 step 0 到 step 5/10 的
router-gap updates；与 proxy-route NMI collapse 和 LM loss 对照；检查不同
common definitions 的鲁棒性。

**阶段证据：** per-pair common/residual margin table、per-step trajectory
summary、common-projector comparison table、NMI/loss/load guard table、
common-vs-residual update plot。

**预期 artifacts：** `protocol.md`、`summary.md`、`detailed.md`、
`tables/common_residual_margin_by_pair.csv`、
`tables/router_update_trajectory.csv`、
`tables/common_projector_robustness.csv`，以及 NMI vs update dominance、
common/residual margin trajectories、router-gap alignment figures。

## 6. Minimal Falsification Tests

| Test | Question | Primary metric | Pass / fail / insufficient | Failure means |
|---|---|---|---|---|
| Router trajectory audit | 早期 router gaps 是否更多沿 common modes 而不是 residual feature directions 移动？ | $\Lambda_{\mathrm{upd}}@5/10$ plus proxy-route NMI | 若 common dominance 与 NMI collapse 同步则 pass；若 residual updates 主导或无关系则 fail；若 checkpoints/router rows 缺失则 insufficient。 | 削弱 H1，或说明 collapse 不是 router-trajectory common dominance。 |
| Residual margin audit | step-0 proxy partition 是否一开始就 residual-fragile？ | $\gamma^R_{f,e}(0)$ and residual margin share | 若高 NMI 伴随弱 residual margin 则 pass；若 residual margins 强且只是 later consumed 则 fail。 | 把 H2 修正为 training drift 而不是 weak initialization。 |
| Common-definition robustness | common-dominance 结果是否跨 common definitions 稳定？ | mean、top-band、route-logit projectors 的一致性 | 若定性一致则 pass；若结论翻转则 fail。 | 削弱 H3，并把 common definition 变成瓶颈。 |

## 7. Current Evidence

**Observation:** A06_12 显示 real-DCLM raw-center proxy routing 在 step 0 很强，
但普通训练到 step 5/10 会 collapse，同时 LM loss 仍可接受。

**Observation:** A06_20 显示简单 route-logit common estimator 会改变 load，但不比
controls 更好地恢复 feature residual geometry。这削弱单步 common subtraction
方法，但不证伪 hierarchical 或 dynamic common-mode trajectory 解释。

**Observation:** A06_21 显示在 controlled no-position bridge 中，center-init
preservation 由 positive margins surviving training drift 解释；preserved
center-init conditions 的 common share 很低。这支持把 common/residual margin
terms 用作 guard，但还没有解释 real-DCLM collapse。

**Interpretation:** 当前不确定性不是 controlled bridge 中 margin 是否重要，而是
real-DCLM router updates 是否通过对齐 common-mode hierarchy 来擦掉 proxy
routing，而不是保留 residual feature contrast。

**Boundary:** 现有证据只支持提出这个 diagnostic anchor，不能支持新 gating 方法，
也不能说 common dominance 已经导致 real-DCLM collapse。

**Evidence links:**

- `../../experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md`
- `../../experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/summary.md`
- `../../experiments/A06/A06_21_margin_budget_preservation_audit/summary.md`

## 8. Claim Boundary And Next Decision

**Can claim if supported:** real-DCLM proxy routing collapse 与 step 0 到 step
5/10 窗口中 common-dominated 而非 residual-feature-aligned 的 router-gap updates
有关。

**Cannot claim:** common-dominated trajectory alone 不能证明 expert utility 缺失，
不能证明 common removal 会解决 preservation，不能证明 long-tail residuals 无意义，
也不能验证新 gating architecture。

**Next decision:** 写一个最小 protocol，将这个 common/residual router-trajectory
audit 应用于 A06_12-style real-DCLM proxy-init checkpoints。
