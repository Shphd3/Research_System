### Layer 1: Main Response

完全同意你的判断。这不是方向崩塌，而是典型的**“对照组升维导致主张门槛被动提高”**。`acp_lite` 用极小的代价（$2Kd$ 参数）打出了极高的收益，这证明我们之前对 `acp_on` 复杂度的剥离是绝对正确的。现在，我们必须用更严苛的眼光审视 Quadratic。

以下是基于当前实验结果的理论回写与状态更新。

---

### 1. Hypothesis Update

当前结果对我们的核心假说产生了明确的推拉效应：

- **支持 H3（比较口径更新）：** 强烈支持。`acp_lite` 在没有 $O(d^2)$ 参数膨胀的情况下，在 Round0 (Avg: 0.4497) 拿到了全场最高分。这证明“显式分离均值方向”本身就是一个极为有效的归纳偏置（Inductive Bias），而不是纯靠参数量堆出来的假象。它完全确立了自己作为“最强公平对照组”的地位。
- **削弱 H4（Quadratic 的机制必要性）：** 当前结果**削弱**了 H4 在“任务表现（Task Performance）”层面的必要性主张，但**尚未完全证伪**其在“几何结构（Geometric Structure）”层面的独特性。

  - 从端到端任务来看（Round0），二阶方差路由（`quadratic_nosvd` / `quadratic_debias`）并没有展现出碾压 `acp_lite` 的能力。
  - 因此，我们不能再说“必须有二阶信息才能做好 CL/任务”。但 H4 目前处于“未被证明（Unproven）”而非“绝对证伪”状态，因为端到端训练的梯度动态可能掩盖了特征空间的真实可分性。
- **削弱“方向敏感性决定论”：** Round4 的 DSI 极小（$10^{-4}$ 级别），这表明即使路由器显式利用了均值方向（如 `acp_lite`），它对该方向的局部扰动也并不极其敏感。方向特征是有用的，但“方向敏感性差异”不是解释各模型表现差距的主导机制。

---

### 2. Mathematical Interpretation

基于 Round0-4 的全量数据，这些结果在数学和机制上更支持以下解释：

- **“Mean-direction 已经足够强” (Primary Driver):**
在当前的表征空间（`ckpt40000`）中，不同 Domain 或 Expert 真正需要的低维子空间，极大程度上与运行中心（Running Center）的投影方向共线或高度相关。`acp_lite` 显式地给这个方向分配了独立权重矩阵 $A$，使得一阶线性分类器足以拉开足够的 Logit 差距。
- **“Quadratic 主要提供鲁棒性” (Secondary Effect):**
在 Round2 中，`quadratic_nosvd` 在极高噪声 $\sigma=0.5$ 下保持了全场最高的一致性（CR 0.9651，排除已塌缩的 baseline）。这在数学上非常合理：二阶项 $x_c \odot x_c$ 会放大高振幅特征、压制低振幅噪声，本质上自带一种非线性的特征硬截断（thresholding）效应，从而提高了抗噪鲁棒性。**但鲁棒性好 = 分发更准**。
- **目前不能从结果中推出什么：**

  - 不能推出“Quadratic 的二阶方差提取能力在任务中发挥了决定性作用”。
  - 不能推出“`acp_lite` 的 Margin 机制失效”（Round3 中 `acp_lite` Margin 均值为 0 极大概率是 logging/实现 bug，因为其 Round0 任务最高且 Round1 熵正常，不可能没有真实的 Logit Margin）。

---

### 3. Conclusion / Update

**现在可以冻结成稳定结论的内容（Write to Report）：**

1. **Baseline 塌缩定理：** 缺少运行中心化（`linear_no_center`）会导致极端的路由塌缩（低条件熵、高负载离散、高 SI 干扰），并直接拖累综合任务表现（Round0 垫底）。
2. **acp_lite 的标杆地位：** 在严格控制 $O(Kd)$ 路由参数复杂度的前提下，显式的一阶均值方向分离（`acp_lite`）能提供当前最优的综合任务收益。
3. **多指标非支配（Multi-objective 解耦）：** 极端的鲁棒性（CR=1.0）或极低的 ED 往往伴随塌缩，健康的分发必须在熵、均衡度、SI 和下游任务之间寻找平衡。

**只能保留为 Tentative Evidence 的内容：**

- Quadratic 的抗高噪优势（需要在更多 ckpt 上确认是否普遍存在）。

**Round4 应该如何进入主线叙事：**

- **降级处理。** Round4 只能作为 **Null / Weak Evidence**。在 Report 中，它不应作为单独的 Section 大书特书，而应放在 Appendix 或 Ablation 中，用一句话带过：“我们排除了方向扰动敏感性（DSI）作为核心驱动机制的假设，其效应量在 $10^{-4}$ 级别。”

---

### 4. Next Iteration Decision

**决定：先补一个最小分析（Follow-up），暂不开启全新的训练迭代。**

我们现在不能带着“Quadratic 到底赢在哪”的模糊疑问进入下一代设计。端到端训练（Round0-4）已经给出了结论：如果在训练动态中跑，`acp_lite` 就够了。
要彻底完结对 Quadratic 的考察，我们必须回到上一份文档 (`draft.md`) 中定义的**冰冻特征鉴别实验（Frozen-Feature Discriminative Audit）**。只有切断了反向传播，纯看特征的几何静态属性，我们才能最终宣判二阶信息的死刑或缓刑。

**最小子问题收缩：**
剥离训练动态后，`ckpt40000` 的静态特征中，到底存不存在只有 $x_c \odot x_c$ 能分开、而 $x_{\parallel}$ 分不开的 Domain Pair？

---

### Minimal Theory -> Next-Step Card

```plaintext
## Minimal Theory -> Next-Step Card

- Current best explanation: 
  The feature geometry at `ckpt40000` is sufficiently separable using explicit first-order mean-direction projections (`acp_lite`). The variance-routing capability of Quadratic models primarily provides non-linear noise thresholding (robustness) rather than strictly necessary boundary separation.

- What remains unresolved: 
  Is Quadratic losing in end-to-end tasks because the structural variance information genuinely doesn't exist, or because the standard training loop fails to optimize the quadratic parameters effectively compared to linear ones?

- Minimal next question: 
  In a purely static, frozen-feature setting (Step-0 audit), does the quadratic feature space $(x_c, q_{deb})$ yield a higher theoretical clustering purity (SVM Purity) on hard Domain Pairs compared to the `acp_lite` feature space $(x_\parallel, x_c)$?

- Why this question is the bottleneck: 
  It cleanly decouples "structural necessity" from "optimization difficulty". If `acp_lite` SVM Purity matches Quadratic SVM Purity on frozen features, we can officially declare Quadratic structurally redundant for CL routing and close the H4 chapter.

- What evidence would resolve it:
  Run a linear SVM on the frozen `ckpt40000` outputs using the three explicit router input formations (`linear_centered`, `acp_lite`, `debiased_quadratic`). Compare the raw classification Margin and Purity scores.

- (Engineering Note): 
  We must also immediately inspect why `acp_lite` logged a Mean Margin of 0.00 in Round3 summary, as this is mathematically contradictory to its high task performance and normal entropy.

```

---

### Layer 2: Reasoning Monitor

- **Current problem:** Adapting to `acp_lite`'s unexpected dominance and cleanly resolving the fate of the quadratic router without getting lost in training artifacts.
- **Established:** `linear_no_center` is dead (collapses). `acp_lite` is the current SOTA baseline. DSI (Round 4) is a dead end.
- **Working hypotheses:** Quadratic routing's main practical benefit is high-noise thresholding (robustness), not necessary geometric separation for tasks.
- **Definition gaps:** Need to define what constitutes a "hard domain pair" for the SVM purity test.
- **Main bottleneck:** Conflation of structural feature geometry with end-to-end gradient optimization dynamics.
- **Risks detected:** Proceeding to complex Continual Learning tasks before definitively knowing if the router *needs* quadratic inputs. Also, trusting the Round3 Margin logging for `acp_lite` which is clearly bugged.
- **Best next step:** Execute the Frozen-Feature SVM Purity test from the previous handoff.
- **What to avoid right now:** Do not train new router architectures. Do not expand the direction-sensitivity (Round 4) narrative.

---

Given that the frozen-feature SVM purity test is the definitive lock-and-key to resolving the quadratic question, are we aligned to have the Experiment AI prioritize this exact audit, along with investigating the `acp_lite` Round3 margin bug, before we design any further routing mechanisms?