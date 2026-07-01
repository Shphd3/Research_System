# 会议简报：A06_22 real-DCLM proxy routing collapse 的 common/residual 机制审计

## 0. 执行摘要

**研究问题：** real-DCLM raw-center proxy routing 在 step 0 形成较强 proxy partition 后，为什么会在 step 5/10 被普通 top-1 训练迅速擦除？

**机制解释：** 当前审计将 router gap 的早期更新分解为 common-projected update 和 feature-residual update，并用 $\Lambda_{\mathrm{upd}}$ 判断 router gap 更新更接近 common 方向还是 residual feature 方向。

**主要结果：** A06_22 四卡 full run 已完成并复现 A06_12 collapse，但强版 common-dominated trajectory 假设被削弱；mean-common 坐标支持 common dominance，top hidden-PC 与 router-row subspace 坐标不支持。

**证据说明：** proxy-route NMI 表示 fixed proxy labels 与 top-1 expert route 的一致性；`raw_center` NMI 从 step 0 的 `0.7549` 降到 step 5 的 `0.0410` 和 step 10 的 `0.0131`，但 $\Lambda_{\mathrm{upd}}$ 的方向判定随 common projector 改变。

1. A06_22 full run 稳定复现了 real-DCLM proxy-route collapse。
2. common-dominated update 不是 projector-robust 机制，因此不能作为当前 gating 方法靶点。
3. residual-margin fragility 仍是活跃解释，但必须和一个更物理的 common operator 一起定义。

**结论边界：** 当前证据不能证明 common-dominated router update 是 root cause，也不能推出 common subtraction、新初始化或新 gating 结构会成功。

**执行动作：** 下一步应定义由 training objective、gradient 或 router-update geometry 约束的 common operator；完成判据是该 operator 在 step 5/10 collapse window 中给出跨 seed/layer 稳定的 $\Lambda_{\mathrm{upd}}$ 判定，并通过 NMI、LM loss、sign flip 与 margin guards。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| proxy-route NMI | fixed proxy labels 与 top-1 expert route 的一致程度 | step-0 proxy label $y_i$ 与当前 expert route $a_i(t)$ 的 normalized mutual information | 0 到 1 | 判断 proxy partition 是否被训练保持 | expert utility 或 semantic expert |
| router gap | matched expert 与 competitor expert 的成对打分方向 | $u_{f,e}(t)=w_{a(f)}(t)-w_e(t)$ | hidden 维向量 | top-1 routing boundary 由这些方向决定 | expert 是否具有功能 |
| common projector | 被定义为共同模式的子空间 | mean-common、top hidden-PC、router-row subspace 三种 $P_C$ | 正交投影 | 判断 update 是否沿 common 方向 | 所有 common 定义都等价 |
| feature-residual direction | 去掉 common projection 后的 feature center 方向 | $(I-P_C)\mu_f(0)$ | hidden 维向量 | 表示 proxy-specific contrast 是否仍被 router gap 读取 | feature 一定有语义 |
| $\Lambda_{\mathrm{upd}}$ | common update 与 residual update 的相对大小 | 见第 2 节公式 | ratio，>1 表示 common 项更大 | A06_22 的主判定指标 | 不结合 NMI/loss 时不能证明因果 |
| sign flip rate | pairwise margin 变成非正的比例 | $\gamma_{f,e}(t)\leq 0$ 的 feature/competitor pair 比例 | 0 到 1 | 表示 router boundary 是否跨过原 proxy center | collapse 的唯一原因 |

## 2. 机制解释与建模

**核心模型：**

$$
\Lambda_{\mathrm{upd}}(t)
=
\operatorname{median}_{f,e}
\frac{
\left|\Delta u_{f,e}(t)^\top P_C\mu_f(0)\right|
}{
\left|\Delta u_{f,e}(t)^\top (I-P_C)\mu_f(0)\right|+\varepsilon
}.
$$

**符号含义：**

- $u_{f,e}(t)$：proxy label $f$ 的 matched expert 与 competitor expert $e$ 之间的 router gap。
- $\Delta u_{f,e}(t)$：从 step 0 到 step $t$ 的 router gap update。
- $P_C$：common projector，即当前定义下的共同模式子空间。
- $\mu_f(0)$：step 0 的 proxy feature center。
- $(I-P_C)\mu_f(0)$：去掉 common projection 后的 residual feature direction。

**机制链条：**

1. 若 $\Delta u_{f,e}(t)$ 主要沿 $P_C\mu_f(0)$，router boundary 更可能跟随 common structure，而不是保持 proxy-specific contrast。
2. 若这种 movement 发生在 step 5/10，且 proxy-route NMI 同时下降，则支持 common-dominated trajectory。
3. 若不同 $P_C$ 给出相反结论，则当前瓶颈不是是否存在 collapse，而是 common operator 的物理定义尚未稳定。

**当前问题分解：**

- 当前实验能够检验 generic common dominance 是否稳健。
- 最危险的替代解释是 residual margin 初始已弱，或 common projector 定义错误。
- 当前实验不能直接证明 causality，也不能证明 preservation method 会成功。

## 3. 主要结果

**一句话总结：** A06_22 将 real-DCLM collapse 从单纯现象推进为可审计的机制负结果：collapse 稳定存在，但 generic common-dominated router update 不是稳健解释。

### 结果 1：real-DCLM proxy-route collapse 在 full run 中被复现。

**机制对应：** 该结果确认 A06_22 审计对象处于 A06_12 的真实失败窗口。

**指标或条件定义：** `raw_center` 表示用 step-0 raw proxy centers 初始化 router rows；proxy-route NMI 越高，表示 route 越保留 fixed proxy labels。

**证据：** `raw_center` proxy-route NMI 从 step 0 的 `0.7549` 降到 step 5 的 `0.0410`、step 10 的 `0.0131`；matched preserve min 从 `0.6754` 降到 `0.0037` 和 `0.0002`；max route load 到 step 10 达到 `0.9645`。

**解释：** 该结果说明 failure 不是 proxy 不存在，也不是 step-0 linear bridge 不成立，而是 ordinary training 快速覆盖了初始 proxy partition。

**边界：** NMI collapse 不能单独说明 collapse 来自 common update。

**来源：** `summary.md`，`tables/full01_key_decision_metrics.csv`，`figures/full01_proxy_route_nmi_reproduction.png`。

![Proxy-route NMI reproduction](../../../Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/figures/full01_proxy_route_nmi_reproduction.png)

### 结果 2：common-dominated update 只在 mean-common 坐标中成立，不是 projector-robust 机制。

**机制对应：** 该结果直接检验 $\Lambda_{\mathrm{upd}}$ 是否跨 common definitions 稳定。

**指标或条件定义：** $\Lambda_{\mathrm{upd}}>1$ 表示 common update term 大于 residual update term；projector robustness 要求 mean-common、top hidden-PC 和 router-row subspace 给出同质结论。

**证据：** mean-common 下 $\Lambda_{\mathrm{upd}}@5=2.1507$、$\Lambda_{\mathrm{upd}}@10=1.9856$；top hidden-PC 下是 `0.7089/0.6666`；router-row subspace 下是 `0.4611/0.4332`。

**解释：** 同一个 collapse window 中，global mean 方向支持 common dominance，但 high-variance hidden subspace 与 router-relative subspace 都显示 residual-dominated update。因此强版 H1 没有通过 robustness rule。

**边界：** 该结果不证明 common 完全无关；它证明当前 common 定义不够稳定，不能作为方法靶点。

**来源：** `summary.md`，`detailed.md`，`figures/full01_projector_lambda_step5_step10.png`。

![Projector lambda step 5 and 10](../../../Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/figures/full01_projector_lambda_step5_step10.png)

### 结果 3：residual-margin fragility 仍是活跃解释，但必须和 common operator 一起定义。

**机制对应：** 该结果对应 H2：step-0 proxy routing 可能表现出高 NMI，但 residual margin 已经脆弱。

**指标或条件定义：** step-0 residual margin min 是在某个 projector 下，matched router gap 对 residual feature center 的最小 margin；sign flip rate 表示 pairwise margin 变成非正的比例。

**证据：** step-0 residual margin min 在 mean-common 下为 `0.6493`，在 top hidden-PC 下为 `0.0324`，在 router-row subspace 下为 `-0.1839`；sign flip rate 到 step 5 为 `0.4147`，到 step 10 为 `0.4782`。

**解释：** 高 NMI 不代表每个 residual-coordinate margin 都强。尤其在 high-gain 或 router-relative 坐标中，step-0 residual margin 已经接近 0 或为负，因此 residual fragility 仍然需要进入下一层建模。

**边界：** 由于 residual margin 也随 projector 改变，当前结果不能支持 operator-independent 的 H2 结论。

**来源：** `detailed.md`，`tables/full01_common_projector_robustness.csv`，`tables/full01_common_residual_margin_by_pair.csv`。

![Raw-center lambda trajectory](../../../Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/figures/full01_raw_center_lambda_trajectory.png)

## 4. 执行动作

**下一步动作：** 制定一个新的最小 protocol，定义 objective/gradient/router-update 约束下的 common operator，并用 A06_22 的同一分解框架复审。

**目的：** 区分 generic projector artifact 与真实训练目标驱动的 common operator。

**完成判据：** 新 operator 在 step 5/10 collapse window 中给出跨 seed、layer、projector guard 稳定的 $\Lambda_{\mathrm{upd}}$ 判定，并且通过 proxy-route NMI、LM loss、sign flip 与 margin guards。

## 5. 证据索引

| 结果 | 证据 | 主要指标或图 | 支持什么 | 不能证明什么 | 来源 |
|---|---|---|---|---|---|
| 结果 1 | raw-center NMI collapse | `full01_proxy_route_nmi_reproduction.png` | full run 复现 A06_12 failure | collapse root cause | A06_22 summary |
| 结果 2 | projector lambda flip | `full01_projector_lambda_step5_step10.png` | H1 强版本被削弱 | common 完全无关 | A06_22 summary/detailed |
| 结果 3 | residual margin and sign flips | `full01_common_projector_robustness.csv` | residual fragility 仍活跃 | H2 operator-independent | A06_22 detailed |

## 6. 来源索引

**Anchor：**

`Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_22_router_common_residual_trajectory_anchor.md`

**Protocol：**

`Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/protocol.md`

**Summary：**

`Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/summary.md`

**Detailed：**

`Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/detailed.md`

**Figures：**

`Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/figures/`

**Tables：**

`Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/tables/`

## 7. 补充材料

四卡 ACP job id：`pt-i3bkewya`。run name：
`a06_22_router_common_residual_trajectory_4gpu_20260630_full01`。full run 覆盖
864 trajectory rows、48,384 pair rows、288 snapshot rows；decomposition identity
最大误差为 `8.37e-7`。job 最终状态为 `SUCCEEDED`。
