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
  在强全局均值遮蔽（Cone Effect）与小样本二阶噪声被显式控制的条件下，验证四路由在可证伪协议中的稳定优势区间，判断“二阶子空间路线”是否具备继续作为主线的必要性。
  在不使用强行负载均衡损失（No Load-Balancing Loss）的自然状态下，评估引入了 **$V_e$ 正交正则化** 的子空间路由，是否能在一个完美拟合“真实 LLM 谱空间特征”的受控数据集中，展现出降维隔离和任务分发优势。

- Experiment design:
  - Hypothesis:
    - H1: 若二阶结构有效，其增益应主要出现在 Type2/Type3，且在多 seed 下保持方向一致，而非单次偶然胜出。
    - H2: `hybrid_subspace_energy` 的优势应来自 “mean-aware + centered-linear + subspace-energy” 协同，而不是牺牲负载稳定性换取短期 TaskLoss。
    - H3: 若 `subspace_energy` 或 `hybrid_subspace_energy` 有效，必须在机制统计上看到稳定的子空间利用证据，而非仅最终指标波动。
  - Mathematical modeling:
    - Router logit:
      $$
      \ell_e(x) = a_e^\top x_{\parallel} + b_e^\top x_c + \|V_e x_c\|_2^2 + c_e
      $$
    - 其中：
      - $x_{\parallel}$ 负责 mean-related bias 方向；
      - $x_c$ 负责 centered first-order 残差；
      - $\|V_e x_c\|_2^2$ 负责 expert-specific subspace energy。
    - 协议要求：最终解释必须同时覆盖 “性能结果” 与 “机制统计”，二者任一缺失均不得下主线结论。
  - Experiment design (MVP first, then phase gate):
    - Common setup (固定不变):
      - Model: 两层 Transformer（Layer2 为 Top-1 MoE），`freeze_backbone=true`
      - Routers: `linear_running_center / acp_lite / hybrid_subspace_energy / subspace_energy`
      - Data: `continuous_hmm_v3`（含大范数 $\mu_{global}$；Type1/2/3 生成逻辑固定）
      - Hidden dim: `d_model in {64, 128}`（同一轮仅允许一个值）
      - LR decoupling: `router_lr > embedding_lr`，并写入每个 run 的 `config.json`
    - MVP (最小可执行版本，先拿干净证据):
      - 只跑 Type2（covariance-separable）四路由
      - 固定：`train=2500, epochs=12, batch_size in {128, 256}, seeds={20260404,20260405,20260406}`
      - 输出：3-seed 均值±标准差 + 相对 `linear_running_center` 的 Δ 表
    - Training modifications:
      - 对 `subspace` 相关的模型,要加上一组实验：Loss = TaskLoss(MSE) + $\alpha \sum_{i \neq j} \|V_i V_j^\top\|_F^2$。
    - 坚持大 Batch Size（$\ge 128$），跑 3 seeds。
    - Phase gate（仅在满足条件后扩展）:
      - Gate-A（进入 Type3）: MVP 中至少一个二阶相关路由在 `NMI` 与 `TaskLoss` 同时优于 `acp_lite`，且 `CV_load` 无明显恶化（不超过基线 20%）
      - Gate-B（进入 Type1）: Type3 结果仍支持主线，且三 seed 方差可控（关键指标 std 未出现同量级反转）
      - Gate-C（扩数据到 train=10000）: 仅当各路由排序受高方差影响无法判读时触发
  - Mandatory metrics and logs (缺一不可):
    - Final metrics（每 run 必须）:
      - `TaskLoss, NMI, ARI, CV_load, expert_counts`
    - Mechanism telemetry（epoch 级 + 关键 step 级）:
      - 几何分解统计：`||x||_2`, `u^T x`, `||x_c||_2`, `||V_e x_c||_2^2` 的均值/方差/分位数
      - 路由分配统计：expert token 占比轨迹、token->expert 转移矩阵、每专家有效样本量
      - 二阶稳定性统计：`V_eV_e^T-I` 正交约束损失、跨专家子空间重叠 proxy（如 `||V_iV_j^T||`）
      - 优化统计：router grad norm、embedding grad norm、二者比值轨迹
      - 训练可观测性：`train.log`（step loss、epoch loss、wall-clock）+ `eigen_log`
    - Aggregation format（汇总口径）:
      - 按 Type 输出：`mean ± std` 表
      - 必含列：`Δ vs linear_running_center` 与 `Δ vs acp_lite`
      - 必含图：CV_load 轨迹、top-k eigen ratio 轨迹、`||V_e x_c||^2` 分布对比
      - 必含指标（对于hybrid方法）：对于logit，二阶项、去中心化一阶项、均值分离项具体占比贡献
  - Dataset (Continuous HMM v3.1 - "Realistic LLM Spectrum"):
    - **核心修改**：根据真实 LLM 统计，设置协方差矩阵与 $\mu_{global}$，使得**第一主成分（SV1，通常与均值共线）占据约 30% 的总能量**。当执行去均值操作后，SV1 能量应下降约 50%。这是极其关键的物理锚点！
  - Compared routers:
    1. `linear_no_center` (必须加入，作为必然 collapse 的反面教材)
    2. `linear_running_center`
    3. `acp_lite`
    4. `hybrid_subspace_energy`
  - Training Rule:
    - **严禁使用 Load Balancing Loss**。纯看 Router 自身的结构偏置。
    - 提升 Batch Size (>=128) 解决二阶梯度的样本诅咒。
  - Risk / confounders（必须显式审计）:
    - C1: 小 batch 导致每专家有效样本不足，二阶梯度噪声伪造“路由优劣”
    - C2: 强 $\mu_{global}$ 设定过弱/过强，导致结论被 mean 效应主导或淹没
    - C3: 只看 TaskLoss 忽略负载均衡，得到“低损失但不可部署”的伪优势
    - C4: 单 seed 或日志缺失造成不可解释性，无法区分机制增益与随机波动
    - C5: 混入配置漂移（lr、freeze、容量）导致跨 run 不可比

- Expected decision logic:
  - 支持主线：
    - 在 Type2（并随后 Type3）中，`hybrid` 或 `subspace` 对 `acp_lite` 的优势在 3 seeds 下方向一致；
    - 优势至少体现在 `NMI/ARI` 与 `TaskLoss` 的联合改进，且 `CV_load` 不明显恶化；
    - 机制日志同步显示子空间能量项被稳定利用（非噪声尖峰）。
  - 削弱主线：
    - 仅单指标偶发胜出，或仅单 type 胜出且方差大；
    - 最终指标与机制统计不一致（例如指标提升但子空间利用证据缺失）。
  - 否定主线（当前协议下）：
    - 多 seed 下二阶相关路由相对 `acp_lite` 无稳定优势，且伴随负载恶化或机制证据缺失；
    - 或出现“仅靠配置漂移才胜出”的不可复现模式。
  - 观察在加入正交约束且无人工负载均衡干预下，`hybrid` 是否能自然避免绝对塌缩，并在 Type 2 / Type 3 中实现最优的 NMI 对齐。

- Hard boundaries:
  1. 不扩大 benchmark；仅在 Type1/2/3 与 `d in {64,128}` 内迭代。
  2. 严格执行四路由，不回流 `old_diagonal_quadratic` 到 active 对比。
  3. 严格执行 LR 解耦与固定 backbone；禁止在同一轮混入额外超参漂移。
  4. 不把静态 proxy、单 seed 结果或 token 继承句子标签证据直接写成 CL 终局结论。

- What experiment agent must return:
  1. 修订后的实验目标（含 primary/secondary endpoint）
  2. 按 MVP -> Phase gate 的实际执行步骤与触发条件
  3. 核心指标总表（`TaskLoss/NMI/ARI/CV_load`，含 `mean±std` 与 `Δ vs baseline`）
  4. 机制日志摘要（几何分解、路由分配、二阶稳定性、优化统计）
  5. 结果模式判定（支持/削弱/否定主线）与对应证据链
  6. 假说更新与下一阶段最小动作（继续/收缩/终止二阶主线）

---

## 8. Experiment Return

> 实验结束后，把 experiment agent 的总结压回这里。

- Experiment objective:
  在满足 V4 约束（新增 `linear_no_center`、禁用 LB Loss、对子空间路由加入 `ortho_loss`）下，完成 5 路由 × 3 types × 3 seeds 的全量对比，检验二阶子空间主线在更真实谱锚点数据上的稳定性。

- Experiment steps:
  1. 生成 `continuous_hmm_v4`，并完成 Type2 光谱锚点校验：`SV1 before=0.3000, after=0.1149, drop=61.71%`。  
  2. 五路由对比：`linear_no_center / linear_running_center / acp_lite / hybrid_subspace_energy / subspace_energy`。  
  3. 训练口径：`epochs=12, batch_size=128, d_model=64, d_ff=128, n_experts=4, freeze_backbone=true, 2卡DDP`；`embedding_lr=3e-4, router_lr=3e-3, backbone_lr=2e-4`；`ortho_alpha=0.05`。  
  4. 执行 `5 routers × 3 types × 3 seeds = 45 runs`，聚合 `TaskLoss/NMI/ARI/CV_load` 的 `mean±std` 与 Δ 表。  
  5. 执行 `ortho_alpha ∈ {0.01,0.05,0.1}` 分档复跑（`type2/type3 × hybrid/subspace × 3 seeds = 36 runs`），并完成 Gate-A 复判。  
  6. 在结果报告中补齐：模型完整构造、数据制作流程与参数、各类型数据量与训练步长、过程机制分析。  
  7. 结果落盘：
     - `output/continuous_hmm_v4/r20260405_v4full_*`
     - `output/continuous_hmm_v4/r20260406_v4alpha_*`
     - `docs/summary_continuous_hmm_v4_r20260405_v4full.{json,md}`

- Experiment results:
  - Type1:
    - 对齐最优：`acp_lite`（`NMI=0.134674±0.011529`）
    - ARI 最优：`linear_running_center`（`ARI=0.111708±0.011831`）
    - TaskLoss 最低：`linear_no_center`（`0.476830±0.003592`）
    - 负载最稳：`linear_running_center`（`CV=0.174181±0.010432`）
  - Type2:
    - 对齐最优：`subspace_energy`（`NMI=0.024238±0.012672`, `ARI=0.020527±0.010309`）
    - TaskLoss 最低：`linear_no_center`（`2.096917±0.017947`）
    - 负载最稳：`linear_running_center`（`CV=0.233325±0.136416`），`subspace_energy` 次优（`0.260662±0.106425`）
  - Type3:
    - 对齐最优：`hybrid_subspace_energy`（`NMI=0.030606±0.008937`, `ARI=0.026305±0.006725`）
    - TaskLoss 最低：`linear_no_center`（`1.162066±0.004297`）
    - 负载最稳：`linear_running_center`（`CV=0.134801±0.071646`）
  - 完整结果表见：`/data/250010109/spectral_router/exp_synthetic_data/docs/summary_continuous_hmm_v4_r20260405_v4full.md`

- Result analysis:
  - V4 全量 45 runs 已完成且可复核。  
  - 正交扫描 36 runs 已完成；`ortho_alpha=0.01/0.05/0.1` 下主指标变化极小，未出现稳定拐点。  
  - Type2 中 `subspace_energy` 在 NMI/ARI 上保持显著领先，说明二阶子空间结构在协方差分离场景仍有效。  
  - `hybrid_subspace_energy` 在 Type3 的 NMI/ARI 最优，但 TaskLoss 未形成相对 `acp_lite` 的同步优势。  
  - `linear_no_center` 在 Type2/Type3 的 `CV_load` 明显恶化（高于中心化线性），符合“反面教材”预期。  
  - Gate-A（NMI+TaskLoss 同时优于 acp_lite，且 CV 不恶化）在本轮未满足，当前证据不足以宣告二阶主线进入“稳定优势”状态。

- Hypothesis update:
  - 保留：二阶结构中“纯子空间能量”在 Type2 的结构对齐优势仍成立。  
  - 更新：`hybrid` 的收益更依赖数据类型（Type3 更明显），尚未形成跨 Type 的一致压制。  
  - 暂缓：`hybrid/subspace` 对 `acp_lite` 的“TaskLoss+NMI 联合稳定优势”结论。  
  - 下一步：在保持同口径前提下，优先探索更大正交强度区间或结构约束改写，以解决 Type2 下 TaskLoss 瓶颈。

### 下一步深入建议与实验修正 (Action Items for Round 2)
1. **扩正交区间**：将 `ortho_alpha` 扩到更高区间（如 `0.2/0.5/1.0`），验证是否存在 TaskLoss-CV 折中点。  
2. **结构正则改写**：尝试联合 `cross + internal` 约束，而非仅 cross-overlap，观察是否能改善 Type2 TaskLoss。  
3. **机制对齐检查**：继续跟踪 `||V_e x_c||^2`、子空间重叠 proxy、router/embedding 梯度比，验证“机制改善是否先于指标改善”。  
4. **严格控变量**：继续固定 batch/LR/freeze/backbone，仅变更单一实验因子避免配置漂移。

### Round 3 执行回填（30% Energy Law）

- Round 3 额外要求执行状态：
  1. 显式均值能量约束 `||mu||^2 / (||mu||^2 + Tr(Sigma)) ≈ 0.30`：**已实现并记录**  
  2. 不引入特征归一化 patch（ACP/Hybrid 保持原实现）：**已遵守**  
  3. 输出 hybrid 三项 logit 贡献（mean 项 / centered 一阶项 / 二阶项）：**已统计并汇总**

- Round 3 数据与训练：
  - 数据集：`continuous_hmm_v5_30law`
  - 关键数据统计：`mu_energy_ratio_actual=0.3000`（target=0.3000）
  - 谱统计：`SV1 before=0.3803, after=0.1149, drop=69.80%`
  - 训练矩阵：`5 routers × 3 types × 3 seeds = 45 runs`
  - 输出目录：`output/continuous_hmm_v5_30law/r20260406_r3full_*`

- Round 3 结果要点：
  - Type2：`subspace_energy` 仍保持 NMI/ARI 最优（`NMI=0.025686±0.014657`），但 TaskLoss 不优于 `acp_lite`
  - Type3：`hybrid_subspace_energy` 在 NMI/ARI 领先（`NMI=0.025010±0.012378`），但 CV 与 TaskLoss 仍未形成联合优势
  - Gate-A（Type2）复判：**未通过**

- Hybrid logit 贡献分解（mean±std）：
  - Type1：mean `0.4346±0.0675`，centered `0.3088±0.0595`，subspace `0.2566±0.0115`
  - Type2：mean `0.2244±0.0582`，centered `0.3231±0.0374`，subspace `0.4525±0.0250`
  - Type3：mean `0.3124±0.0633`，centered `0.3155±0.0466`，subspace `0.3721±0.0179`

- Round 3 结论：
  - 30% 能量定律约束已落实，且避免了额外归一化 patch 与辅助负载损失。
  - 机制上，hybrid 的二阶项在 Type2/Type3 已成为主导贡献，但最终 `TaskLoss + CV_load` 协同仍是 Gate-A 未通过的核心障碍。
  - 当前主线状态为"机制证据增强，但性能闭环未完成"。

### Round 4 执行回填（H(E|C) 与 SI 指标）

- Round 4 额外要求执行状态：
  1. 新增 **H(E|C)** 指标（条件熵）以衡量 expert-class 相关性：**已实现并记录**
  2. 新增 **SI (Subspace Interference)** 指标以衡量专家跨域协方差重叠：**已实现并正确计算**
  3. 删除"负载最稳"描述，改为"CV_load（不坍缩即可）"：**已更新**

- Round 4 数据与训练：
  - 数据集：`continuous_hmm_v5_30law`
  - 训练矩阵：`5 routers × 3 types × 3 seeds = 45 runs`
  - 输出目录：`output/continuous_hmm_v5_30law/full_type*` (归档：`archive_r20260406_r3full/`)
  - 完整报告：`docs/summary_continuous_hmm_v5_30law_r20260407_v5full.md`

- Round 4 结果要点（新增 H(E|C) + SI 指标）：
  - Type1：
    - `linear_running_center` NMI/ARI 最优（NMI=0.126, ARI=0.123）
    - `linear_no_center` H(E|C) 最低（0.035），但 NMI/ARI 也最低——说明低条件熵≠高专一性
    - `linear_no_center` SI 最低（7.48），但分发最差
  - Type2：
    - `subspace_energy` NMI/ARI 最优（NMI=0.026, ARI=0.022）
    - `acp_lite` SI 最低（10.83），但 NMI 不高
  - Type3：
    - `hybrid_subspace_energy` NMI/ARI 最优（NMI=0.025, ARI=0.020）
    - `acp_lite` SI 最低（11.01），但 NMI 仅中等

- H(E|C) 指标分析：
  - **低 H(E|C) ≠ 高专一性**：`linear_no_center` 的 H(E|C) 最低，但分发最差
  - **随机均匀分配会产生低条件熵**，但不一定是好的 specialization
  - 需要结合 NMI/ARI 或 purity 来解释 H(E|C)

- SI 指标分析（修复后）：
  - SI 现在正确计算，不再全为 0
  - **SI 与 NMI 无明显负相关**：SI 最低不代表 NMI 最高
  - `acp_lite` 在所有 type 中 SI 都较低（~10-11），但 NMI 不是最优
  - `linear_running_center` 在 Type1 中 NMI 最高，但 SI 也最高（~20）
  - **可能原因**：SI 衡量协方差重叠，NMI 衡量类别对齐——两者不是同一件事

- Gate-A（Type2）复判：**仍未通过**（TaskLoss 未优于 acp_lite）

- Round 4 结论：
  - H(E|C) 和 SI 指标已成功计算
  - SI 与 NMI 无明显相关性，需要重新思考 SI 的含义或改进定义
  - 二阶路由在 Type2/3 仍保持 NMI/ARI 优势，但 TaskLoss 闭环未完成

---

## 9. Report Sync

- What can enter report now:
  - specialization ↔ low-rankness link
  - clustering audit weakened old diagonal story
  - `subspace_energy` 在 Type2（协方差主分离）表现稳定
  - `acp_lite` 在 v3 强均值遮蔽下出现负载塌缩风险
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
