# Protocol: A06_02_02_E01 Router Common-Residual Trajectory Audit

## 0. 审批快照

**审批状态：** 用户已明确要求写 protocol、提交四卡 full run、跑完后更新假设并完成 meeting brief，因此本协议进入执行状态。

**目的：** 判断真实 DCLM 的 proxy routing 崩塌，是否因为早期 router gap 更新主要沿着共同模式方向移动，而不是沿着 feature-residual 方向移动。

**主 anchor：** `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/subanchors/06_02_02_common_background_preservation_controls_anchor.md`

**anchor 决策问题：** 在 real-DCLM proxy-init 训练中，早期 router-gap 更新是否被 common-mode hierarchy 主导，而不是被 feature-residual 方向主导？这种主导是否解释 proxy-route collapse？

**被检验的物理先验：** top-1 routing 读的是 router gap 和 hidden state 的方向关系。如果 router gap 更新到 common 方向，即使 hidden state 里仍然保留 residual feature 信息，固定 proxy label 也会被路由抹掉。

**核心模型项：**

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

**falsifier：** proxy-route NMI 崩塌，但多个 common projector 下 router-gap update 并不 common-dominated；或者结论完全取决于某一个 common projector。

**实验角色：** 根因审计 / 机制分解。不是新 gating 方法实验。

**主指标：** step 5 和 step 10 的 common-over-residual router update dominance ratio，即 $\Lambda_{\mathrm{upd}}$。

**结论边界：** 只解释 early real-DCLM proxy-init training 轨迹。不能证明 expert utility、semantic expert identity、最终 gating 方法。

**最小设置：** 复用 A06_01_04_E03 real-DCLM 训练配置，在 checkpoint 处收集 hidden states 和 router rows，并对固定 step-0 proxy labels 计算 common/residual router-gap 分解。

**基础配置：** DCLM binary token stream，Qwen3-style top-1 MoE，6 层，8 experts，audit layers 3/4/5，model seeds 0/1/2，checkpoints 0/1/2/3/5/10/20/50。

**运行条件：** `raw_center` 是主条件；`random`、`equal_norm_random`、`residual_center` 是 A06_01_04_E03 继承下来的 guard。

**Pass：** `raw_center` step-0 proxy-route NMI 高，step 5/10 崩塌，并且稳健 common projectors 下 $\Lambda_{\mathrm{upd}}(5)$ 或 $\Lambda_{\mathrm{upd}}(10)>1$，同时 LM loss 与 random 接近。

**Fail：** `raw_center` 崩塌，但 $\Lambda_{\mathrm{upd}}(5/10)\leq 1$，或者 residual update terms 主导。

**Insufficient：** hidden states、router rows、fixed proxy labels、checkpoint coverage、projector robustness 缺失；分解项非有限；或者没有复现 A06_01_04_E03 的 step-0 high NMI 与 step-5/10 collapse。

**不能声称：** 新 gating 方法、语义专家、expert utility、common-removal 成功、长期预训练行为。

**执行决定：** smoke run 先验证代码路径、输出 schema 和分解指标有限；通过后提交四卡 full audit。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象 / 计算 | 单位或公式 | 为什么重要 | 不能证明什么 |
| --- | --- | --- | --- | --- | --- |
| 固定 proxy label | step-0 聚类得到的固定目标划分。 | $y_i=f$，来自 router 初始化前 raw hidden-state k-means。 | 离散标签 | 训练过程中保持同一个 proxy partition。 | 语义 feature identity。 |
| Router gap | 区分 matched expert 和 competing expert 的成对方向。 | $u_{f,e}(t)=w_{a(f)}(t)-w_e(t)$。 | hidden 维向量 | top-1 routing 的边界由这些方向决定。 | expert 是否有用。 |
| Common projector | 被视为共同模式或高增益结构的子空间。 | $P_C$，来自 mean direction、top hidden-state PCs 或 router-row subspace。 | 正交投影 | 检验 router update 是否被非 feature-specific 结构主导。 | 所有大方向都有害。 |
| Feature-residual center | 去掉 common projection 后的 feature center。 | $r_f(0)=(I-P_C)\mu_f(0)$。 | 向量 | 候选的 proxy-specific contrast 方向。 | functional value。 |
| Router update dominance | router-gap 更新更像 common 还是 residual。 | $\Lambda_{\mathrm{upd}}(t)$。 | ratio | H1 的主指标。 | 不结合 NMI/loss 时不能证明因果。 |
| Proxy-route NMI | fixed proxy labels 和 top-1 experts 的一致程度。 | $y_i$ 与 $a_i(t)$ 的 normalized mutual information。 | 0 到 1 | 守卫是否复现 collapse。 | expert utility。 |
| LM loss | next-token 训练损失。 | A06_01_04_E03 runner 的 cross-entropy。 | cross entropy | 防止把 optimization crash 误读成 routing mechanism。 | specialization quality。 |

## 2. Anchor 对齐

**决策问题：** early real-DCLM router-gap updates 是否 common-dominated，并且是否与 proxy-route collapse 对齐？

**被检验的物理先验：** 如果 router gap 继续读 residual feature directions，partition 更可能保留；如果 router gap 移向 common directions，proxy labels 会被抹掉。

**核心模型项：** $\Delta u_{f,e}(t)^\top P_C\mu_f(0)$ 对比 $\Delta u_{f,e}(t)^\top r_f(0)$。

**falsifier：** 多个 common projectors 下，collapse 不伴随 common-dominated update terms。

**结论边界：** early real-DCLM training window 的机制审计。

## 3. 被检验假设

**H1 common-trajectory：** `raw_center` 条件下，早期 router-gap updates 被 common-mode directions 主导。

**H2 residual-margin insufficiency：** step-0 raw-center routing 脆弱，是因为 residual margin 弱，即使 total proxy-route NMI 高。

**H3 common-projector robustness：** 结论不是某一个 common 定义造成的 artifact。

## 4. 竞争解释

- residual margin 弱；
- feature-center drift 跨过固定 router boundary；
- router-boundary drift 存在但与 common 无关；
- fixed proxy labels 本身不稳定；
- next-token objective 奖励另一个 routing partition；
- common projector 定义造成 artifact。

## 5. 数据 / 模型 / 算法 / 目标

**数据：** A06_01_04_E03 使用的 DCLM binary token stream：`/data/share/109_cache_dir/hf_data/dclm_bin`。

**模型：** A06_01_04_E03 同款 Qwen3-style real-DCLM top-1 MoE，6 层，hidden size 512，8 experts，每个 token 选 1 个 expert，router input 是 raw hidden states。

**训练目标：** 标准 next-token cross-entropy。这个 audit 不改变训练目标。

**proxy 构造：** 对每个 seed/layer，在 step 0 router init 前用 calibration split 的 raw hidden-state k-means 得到 proxy centers，然后固定 eval proxy labels。

**router 初始化：** 复用 A06_01_04_E03 variants。主条件是 `raw_center`。

**审计 population：** 每个 checkpoint 都用相同 held-out eval tokens。主层是 3、4、5。

## 6. 条件、seeds、checkpoints

Seeds: `0, 1, 2`。

Layers: `3, 4, 5`。

Checkpoints: `0, 1, 2, 3, 5, 10, 20, 50`。

Variants: `raw_center` 主条件；`random`、`equal_norm_random`、`residual_center` 为 guard。

Common projectors:

- mean common projector；
- top hidden-PC projector；
- router-row projector。

## 7. 主指标

主指标是：

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

它直接回答：router-gap movement 更像 common 还是 residual。主要看 step 5 和 step 10，因为 A06_01_04_E03 的 collapse 就发生在这个窗口。

## 8. 次级指标

- proxy-route NMI；
- matched preserve fraction；
- LM loss；
- max route load 和 active experts；
- total current margin；
- common margin；
- residual margin；
- residual margin share；
- sign flip rate；
- feature-center drift term；
- router update common/residual terms；
- projector agreement rate。

## 9. 已知 good / bad / confusing cases

**Known good：** A06_01_04_E03 中 raw-center step-0 proxy-route NMI 应该高。

**Known bad：** A06_01_04_E03 中 raw-center NMI 应该在 step 5/10 崩塌，但 loss 与 random 接近。

**Known confusing：** random/equal-norm random 可能 load concentration 很强，但它们 step-0 proxy NMI 低，所以不能解释 proxy preservation。

**Known confusing：** projector 可能因为捕获了大部分 norm 而制造高 common dominance；因此需要 projector robustness 和 residual margin share。

## 10. Stage-level profiling

| Stage | 局部问题 | 输入证据 | 通过 / 失败 / 不清楚规则 | debug artifact | handoff |
| --- | --- | --- | --- | --- | --- |
| Snapshot audit | 每个 checkpoint 是否有 hidden states、logits、routes、labels、router rows？ | run inventory | 全覆盖通过 | `snapshot_inventory.csv` | detailed.md |
| Reproduction audit | 是否复现 A06_01_04_E03 collapse？ | `proxy_route_nmi` trajectory | raw-center high at step 0 and collapse by step 5/10 | `router_update_trajectory.csv` | summary.md |
| Projector audit | projector bases 是否有限且非退化？ | basis rank/norm | zero rank 或 NaN 失败 | `common_projector_robustness.csv` | detailed.md |
| Pair decomposition audit | pair-level terms 是否完整有限？ | pair table | 缺失或 NaN 失败 | `common_residual_margin_by_pair.csv` | detailed.md |
| Decision audit | $\Lambda_{\mathrm{upd}}$ 是否与 NMI collapse 对齐？ | aggregate table / figures | 按第 12 节判定 | figures | summary.md |

## 11. 算法规格

输入：

- A06_01_04_E03 training code 和 DCLM binary data；
- step-0 calibration hidden states；
- checkpoint held-out eval hidden states、router logits、router rows；
- step-0 raw hidden k-means 的 fixed proxy labels；
- training LM loss。

参数：

- seeds: `0,1,2`；
- variants: `random`, `equal_norm_random`, `raw_center`, `residual_center`；
- layers: `3,4,5`；
- checkpoints: `0,1,2,3,5,10,20,50`；
- common rank: `4`；
- epsilon: `1e-8`。

步骤：

1. 按 A06_01_04_E03 初始化模型和 fixed proxy labels。
2. 应用 router initialization variant。
3. 每个 checkpoint 收集 hidden states、router logits、route assignments、router rows。
4. 用 step-0 majority route 定义 $a(f)$。
5. 从 step-0 数据拟合 common projectors。
6. 计算 pairwise common/residual margin 和 router-update terms。
7. 聚合到 seed/variant/layer/checkpoint/projector。
8. 生成决策图和 summary。

## 12. Success / Failure / Insufficient Evidence

**支持 H1：** `raw_center` 复现 A06_01_04_E03 collapse，并且 mean、top-hidden-PC、router-row projectors 下 $\Lambda_{\mathrm{upd}}(5)$ 或 $\Lambda_{\mathrm{upd}}(10)>1$，common update terms 大于 residual update terms，LM loss 与 random 接近。

**削弱 H1：** `raw_center` collapse 发生，但 $\Lambda_{\mathrm{upd}}(5/10)\leq 1$，或 residual update terms 主导。

**支持 H2：** step-0 residual margins 小或 sign-fragile，尽管 step-0 proxy-route NMI 高。

**削弱 H2：** step-0 residual margins 强，collapse 主要来自 later update 或 center drift。

**支持 H3：** 多个 projector 给出同质结论。

**削弱 H3：** 结论随 projector 翻转。

**Insufficient：** 没有复现 A06_01_04_E03，缺 checkpoint rows，分解项非有限，或只有一个 common projector 有效。

## 13. 不能声称

这个 audit 不能单独证明 common-mode update 因果导致 collapse，只能支持 measured trajectory 内的关联。不能声称 common subtraction 会修复训练、long-tail residual directions 没意义、真实语义 experts 存在，或新 gating architecture 已验证。

## 14. Review Notes

2026-06-30：根据 A06_02_02_E01 anchor 和用户明确执行请求创建 protocol。
