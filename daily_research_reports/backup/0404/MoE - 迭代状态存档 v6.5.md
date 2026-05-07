# MoE - 迭代状态存档 v6.5

> 这是一份持续更新的状态文档。  
> 以后默认一直更新这一份；只有当主线问题明显切换时才升版。  
> 新开对话时，优先直接上传这份文档，再补一小段本轮 focus。

---

## 0. Metadata

- Project: MoE Router for Continual Learning
- Version: v6.5
- Date: 2026-04-03
- Current Stage: 主线重塑中，准备继续与 theory agent 深入讨论

---

## 1. Executive Summary

- Current mainline:
  我们现在的主线不是“旧 diagonal quadratic 是否成立”，而是：
  **什么样的二阶结构真正与 MoE routing 相关，以及怎样把这些结构写成更合理的 hybrid router。**

- Current bottleneck:
  当前最大问题不是“有没有二阶项”，而是：
  **哪些二阶结构值得保留，哪些只是几何分离信号但不具有真正的 routing 价值；以及我们当前的 token-level 评估协议，是否足以支撑“semantic routing”这一说法。**

- Single Decision Question:
  **下一步是否应正式转向 `mean-aware + centered-linear + low-rank subspace-energy` 的 hybrid route，并停止把旧 diagonal quadratic 当成主线目标？**

- Why this matters:
  因为 0403 的聚类实验已经削弱了旧 diagonal 语义叙事，而 benchmark 又说明一阶路线依然很强；如果主线不重塑，后续训练和实验会继续发散。

---

## 2. Stable Knowledge

- `linear_running_center` 是当前干净 baseline。
- `acp_lite` 是当前最强的一阶 comparator。
- `specialization`、`low-rankness`、`variance-aware routing` 是三层不同概念，不能混用。
- token-level audit 已经证明 expert specialization 的确存在。
- clustering audit 已经削弱了“旧 diagonal 二阶项直接编码语义”的说法。
- 当前 token-level semantic evidence 仍有协议漏洞：token 标签继承自句子标签，因此它更接近“sentence-label-related routing evidence”，还不能直接等同于严格的 token-level semantic routing 证据。

---

## 3. Current Mainline

### 3.1 Hypothesis

- H1:
  并非所有二阶结构都对 routing 有意义；真正值得保留的是与 domain / semantic separation 强相关的二阶结构。

- H2:
  更合理的 variance-aware route 应保留一阶有效信息，并在其上叠加低秩子空间能量，而不是只保留纯 quadratic branch。

- H3:
  更清晰的 assignment specialization 在合适约束下会诱导更低的 expert 内部 occupancy / rank。

### 3.2 Mathematical Modeling

- Core variables:

  - Global centering:

    $$
    x_c = x - \mu_{\mathrm{global}}
    $$

  - Mean direction:

    $$
    u = \frac{\mu_{\mathrm{global}}}{\|\mu_{\mathrm{global}}\|_2}
    $$

  - Mean-direction projection:

    $$
    x_{\parallel} = (u^\top x)u
    $$

- Current revised route:

  $$
  \begin{aligned}
  \ell_e(x)
  &= a_e^\top x_{\parallel} + b_e^\top x_c \\
  &\quad + \|V_e x_c\|_2^2 + c_e
  \end{aligned}
  $$

- Structural regularization:

  $$
  \begin{aligned}
  \mathcal{L}_{\mathrm{internal}}
  &= \sum_e \|V_eV_e^\top - I_r\|_F^2 \\
  \mathcal{L}_{\mathrm{cross}}
  &= \sum_{i\neq j} \|V_iV_j^\top\|_F^2
  \end{aligned}
  $$

- Interpretation:
  - `$x_{\parallel}$`：mean-related / bias-like direction
  - `$x_c$`：centered first-order residual
  - `$\|V_e x_c\|_2^2$`：expert-specific subspace energy

- What is already clear:
  当前想推进的“方差路由”不应该再被理解成“只加一个二阶项”，而应该理解成：
  **保留有用的一阶信息，再增加低秩子空间能量项。**

### 3.3 What Is Established vs. Not

- Established:
  - 旧 diagonal 二阶线不该再作为主线终点
  - `acp_lite` 必须被视为强 baseline
  - 未来要推进的二阶路线必须是 hybrid，而不是纯 quadratic

- Not established:
  - 当前 hybrid route 是否真的会学出更有用的 routing structure
  - 这些结构是否最终有利于 CL
  - `specialization -> low-rankness` 的桥梁在当前项目里应如何写得更强

---

## 4. New Results That Forced This Reset

### 4.1 Clustering Audit

0403 的 coarse clustering audit 表明：

- raw first-order features 仍然最对齐 coarse semantic labels
- pure energy 可以分得很开，但不等于 semantic grouping
- diagonal second-order features 没有展示稳定语义优势

这意味着：

- 不能再把旧 diagonal 二阶项当成“已经被证明有语义 routing 价值”的路线
- 未来若继续推进二阶路线，必须解释清楚“到底是哪种二阶结构值得保留”

### 4.2 Benchmark Constraint

当前 benchmark 同时说明：

- `acp_lite` 很强，不能绕开它
- 新路线如果继续推进，必须回答：
  - 为什么一阶不够
  - 为什么保留的一阶信息和新增的二阶信息能形成更合理的组合

### 4.3 Evaluation Protocol Caveat

当前还存在一个会直接影响主线叙事的评估漏洞：

- 现有 token-level 分析里，token 标签本质上继承自句子标签
- 因此我们当前测到的更准确表述是：
  `token assignment is correlated with sentence-level labels`
- 但这还不足以严格推出：
  `router has learned token-level semantic routing`

这意味着：

- 现有 token audit 仍然可以作为“expert specialization 存在”的证据
- 但它不能单独承担“semantic routing 已被证明”的角色
- 如果后续还要继续推进 semantic / variance-aware routing 这条主线，就需要一个更可控的 benchmark，把：
  1. token latent label
  2. sentence / task label
  3. domain / nuisance factor
  明确拆开

因此，这一轮 theory 讨论除了机制解释本身，还必须回答：
**什么样的 controlled experiment 才足以让我们更干净地谈 token-level routing structure。**

---

## 5. This-Round Focus

- Current mode: `Convergence`

- This-round focus:
  这轮不是继续讨论旧 diagonal quadratic。  
  这轮只推进：
  **新的 hybrid route 是否值得成为正式主线，这条路线背后的理论解释要怎么写得更严谨，以及我们应该怎样设计一个足够干净的 controlled benchmark 去验证 token-level routing structure。**

- What should not be done now:
  - 不扩大 benchmark
  - 不直接下 CL 终局结论
  - 不再回到“只要有二阶项就叫 variance routing”
  - 不再把“token 继承句子标签”的结果直接写成 token-level semantic routing 结论

---

## 6. Theory Sync Block

> 新开 theory 对话时，优先直接复制这一节。

- Mainline:
  我们现在的主线是：什么样的二阶结构真正与 MoE routing 相关，以及怎样把这些结构写成更合理的 hybrid router。

- Bottleneck:
  当前最大问题不是有没有二阶项，而是哪些二阶结构值得保留、哪些只是几何分离信号；以及当前 token-level 评估协议是否足以支撑 semantic routing 叙事。

- Single Decision Question:
  下一步是否应正式转向 `mean-aware + centered-linear + low-rank subspace-energy` 的 hybrid route，并停止把旧 diagonal quadratic 当成主线目标？

- Stable knowledge:
  1. `linear_running_center` 是 baseline  
  2. `acp_lite` 是当前最强一阶 comparator  
  3. token-level specialization 已存在  
  4. clustering audit 已削弱旧 diagonal 语义叙事  
  5. 当前 token 标签继承句子标签，因此现有 token-level semantic evidence 仍不足以构成严格的 token semantic routing 证明

- Current revised route:

  $$
  \begin{aligned}
  \ell_e(x)
  &= a_e^\top x_{\parallel} + b_e^\top x_c \\
  &\quad + \|V_e x_c\|_2^2 + c_e
  \end{aligned}
  $$

- What I want to discuss now:
  1. 这条 hybrid route 的理论解释还缺哪些关键桥梁？
  2. `specialization -> low-rankness` 在我们当前问题里怎样才能写得更强、更严谨？
  3. 这一轮最小实验到底应该怎么设计，才能真正支持或削弱这条新主线？
  4. 如果我们要摆脱“token 继承句子标签”的协议漏洞，一个最小但足够有说服力的 controlled benchmark 应该具备什么结构？

- Request:
  请围绕这条主线，按
  `Hypothesis -> Mathematical Modeling -> Experiment Design -> Conclusion/Update`
  推进；其中 Experiment Design 部分请额外明确：
  - 如何拆开 token latent label 与 sentence/task label
  - 如何区分 mean-separable / covariance-separable / hybrid-separable 三类 setting
  - 什么结果模式才足以支持“二阶 routing 确实学到了 token-level 结构”
  讨论几轮后，如果你判断已经可以收束，请直接把新的理论认识写成一版更清晰的实验设计和结论更新建议。

---

## 7. Experiment Handoff Block

> theory 端收束后，再填这一节交给 experiment agent。

- Experiment objective:
  用一个可控的两层 Transformer MoE benchmark，替代“token 继承句子标签”的弱语义评估方式。
  核心目标是回答：在 token-level latent label 已知的前提下，不同 router 是否真的学出了更合理的 token 分发结构，以及这种结构与任务性能的关系。

- Experiment design:
  - Model:
    两层 Transformer，其中 Layer 1 为标准的 Dense FFN（特征混合），Layer 2 替换为 Top-1 MoE。
    **【关键细节】**：为了严格对比 router，Backbone（Attention 与 Layer 1）必须在所有 router 对比实验中保持完全一致（可考虑冻结 Backbone 或确保相同的随机初始化与学习率），确保唯一下游变量是 Router 结构。
  - Compared routers (参数量需严格对齐 O(Kd)):
    1. `linear_running_center`
    2. `acp_lite`
    3. `old_diagonal_quadratic`
    4. `hybrid_route` (mean-aware + centered-linear + low-rank subspace-energy)
  - Dataset principle:
    自建 Continuous HMM synthetic dataset，嵌入特征 $x_i = \mu_{global} + \mu_{local}(z_i) + \Sigma(z_i)^{1/2} \epsilon_i$。
  - Dataset split:
    1. **Mean-separable (Type 1)**: $\Sigma$ 为球形各向同性，仅存在显著的 $\mu_{local}$ 差异。
    2. **Covariance-separable (Type 2)**: 引入复杂的实际表征偏移。两个类别的 $\mu_{local}$ 存在重叠或极小的次级偏移（模拟真实语料中同领域的局部均值漂移），但核心区分度在于它们在不同的低维正交子空间上存在极大的方差拉伸。
    3. **Hybrid-separable (Type 3)**: 序列中交替混合 Type 1 和 Type 2 的 token。
  - Training mode:
    Auto-regressive Next-Token Prediction (MSE Loss)。Token-level latent labels ($z_i$) 仅用于 Evaluation。
  - Primary evaluation & Logging Details:
    1. Task Loss (MSE on test set)
    2. Routing Alignment: `NMI(E, z_token)` 与 `ARI` (必须按 Dataset Type 独立打点输出)
    3. Load balance: `CV_load`
    4. **【关键细节】**：记录每个专家的特征值谱（Eigenvalue Spectrum），以直观验证子空间能量路由是否成功捕获了低秩正交矩阵。

- Expected decision logic:
  - 若 `acp_lite` 赢下 Type 1 但在 Type 2 崩溃，且 `hybrid` 完美解决 Type 2 并赢下 Type 3，则 Hybrid 理论完备性成立。
  - 若 `old_diagonal` 在 Type 2 表现远逊于 `hybrid`，则彻底淘汰旧二阶路线。

- Hard boundaries:
  1. 不扩大 benchmark，隐藏维度控制在 $d=64$ 或 $128$ 以内保证快速迭代。
  2. Router 的学习率可以与 Backbone 解耦，防止梯度被 Backbone 淹没。
  3. 不把静态 proxy 直接写成 CL 结论。

- What experiment agent must return:
  1. 实验目标与生成的合成数据可视化特征（PCA/t-SNE 验证生成是否符合预期）
  2. 实验具体步骤
  3. 核心指标对比表（Task Loss, NMI, CV_load）
  4. 实验结果分析
  5. 更新了什么假说

---

## 8. Experiment Return

> 实验结束后，把 experiment agent 的总结压回这里。

- Experiment objective:
  在可控 synthetic（Type1/2/3）上比较 5 种 router 的 token 分发结构与任务损失关系，验证哪些二阶结构对 routing 真正有增益。

- Experiment steps:
  1. 使用 `continuous_hmm_v2` 三类数据（Type1/2/3），固定两层 Transformer + Layer2 Top-1 MoE。  
  2. 五路由全量对比：`linear_running_center / acp_lite / old_diagonal_quadratic / hybrid_subspace_energy / subspace_energy`。  
  3. 统一训练口径：`epochs=6, d_model=64, d_ff=128, n_experts=4, freeze_backbone=true, 4卡DDP`。  
  4. 每个 run 记录 `TaskLoss/NMI/ARI/CV_load` 与 `eigen_log`，结果落盘到 `output/continuous_hmm_v2/r20260404_full_type*_*`。

- Experiment results:
  - Type1:
    - `acp_lite` 在对齐指标最优（`NMI=0.1618, ARI=0.1369`）
    - `linear_running_center` 在负载均衡最优（`CV=0.1574`）
    - `old_diagonal_quadratic` 在 TaskLoss 略低（`0.4639`）但对齐较弱
  - Type2:
    - `subspace_energy` 对齐最优（`NMI=0.0276, ARI=0.0283`）
    - `hybrid_subspace_energy` TaskLoss 最低（`2.2319`）
    - `linear_running_center` 负载均衡最优（`CV=0.1103`）
  - Type3:
    - `acp_lite` 对齐最优（`NMI=0.0386, ARI=0.0309`）
    - `old_diagonal_quadratic` TaskLoss 最低（`1.3099`）但 `CV=0.9497` 失衡明显
    - `linear_running_center` 负载均衡最优（`CV=0.1156`）
  - 完整结果表见：`/data/250010109/spectral_router/exp_synthetic_data/docs/experiment_result_r20260404_full_sweep.md`

- Result analysis:
  - 结果未支持“hybrid 在 Type2/Type3 全面胜出”的强叙事。  
  - 一阶路由 `acp_lite` 仍是强 comparator（Type1/Type3 对齐表现稳健）。  
  - 纯 `subspace_energy` 在 Type2 对齐最优，提示协方差分离场景中二阶子空间信息有效。  
  - `old_diagonal_quadratic` 在 Type2/Type3 出现高 `CV_load`，稳定性与可解释性均偏弱，不宜继续作为主线目标。  
  - `TaskLoss` 与 `NMI/ARI` 并不总是同向提升，后续必须继续采用多指标联合判读。

- Hypothesis update:
  - 保留：`acp_lite` 作为强基线的地位。  
  - 更新：二阶结构里“子空间能量”比“旧 diagonal”更值得保留与深入。  
  - 暂缓：hybrid 已经全面优于一阶的结论。  
  - 下一步：固定当前口径做多 seed（≥3）与小范围超参扫描，验证 `hybrid` 是否存在稳定优势区间。

---

## 9. Report Sync

- What can enter report now:
  - specialization ↔ low-rankness link
  - clustering audit weakened old diagonal story
  - `acp_lite` remains strong
  - hybrid route is the active revised direction

- What must stay tentative:
  - hybrid route 是否最终更优
  - CL 层面的最终收益
  - 任何基于“token 继承句子标签”协议直接推出的 token-level semantic routing 结论

- One-line report framing:
  - 我们已经从“为旧 diagonal quadratic 辩护”切换到“围绕 hybrid route 重新定义什么样的二阶结构才值得用于 routing”

---

## 10. Version Rule

- Continue updating this version when:
  - 只是新增结果
  - 只是修正定义
  - 还是同一条主线

- Upgrade when:
  - 主线问题变了
  - 机制解释变了
  - 阶段切换了
  - 准备正式汇报
