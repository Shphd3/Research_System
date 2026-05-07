请使用pytorch，在本地环境中完成实验：

---

# 📌 Experiment Handoff: MoE 长尾特征的梯度饥饿与动力学验证

**To: Execution Agent**
**From: Theory AI (Checkpoint Workflow)**

## 一、 实验背景与核心目标 (Background & Objective)

[cite_start]本实验旨在验证大语言模型 MoE 架构中长尾信息（Tail Features）丢失的物理机制。现有的主线理论表明：MoE 的核心不仅仅是路由分配，更重要的是表征解耦与正则化生存条件的解耦 [cite: 74]。

[cite_start]在主流的分布式训练框架中，统一的 Weight Decay 会与微弱的长尾数据驱动力产生竞争。当专家的占用率 $p_e$ 和特征方差 $\lambda_i$ 极小时，长尾信号会被系统性压制 [cite: 75]。这种压制在工程实现上表现为两种死亡方式：
1.  [cite_start]**Global WD（全局衰减）：** 未激活专家的梯度被置为 0 但仍执行 Weight Decay [cite: 126]。长尾特征死于“稳态天花板极低”，最终参数趋近于 0。
2.  [cite_start]**Lazy WD（仅激活衰减）：** 未激活专家的梯度为 None，跳过 Weight Decay [cite: 124][cite_start]。长尾特征死于“收敛速度被 $p_e$ 严重拖慢”，在有限的预训练 Epoch 内来不及长大 [cite: 118, 125]。

[cite_start]**实验目标：** 通过最小受控的合成实验（Toy Experiment），分别利用**严格的数学闭式解**与**带时间轴 $t$ 的动力学仿真**，复现并验证上述两种死亡机制，并证明“分支解耦正则化（Hierarchical/Dynamic WD）”是唯一解 [cite: 121]。

---

## 二、 全局变量与数学定义 (Mathematical Setup)

* **输入表征 $x$：** 维度 $d = 8$。前 4 维为 Head 特征（高方差），后 4 维为 Tail 特征（低方差）。
    * $\lambda_{head} = [100, 50, 20, 10]$
    * $\lambda_{tail} = [1, 0.5, 0.2, 0.1]$
    * 生成方式：$x_i \sim \mathcal N(0, \lambda_i)$
* [cite_start]**Teacher 目标参数 $\beta$：** 设定 $\beta_i = 1/\sqrt{\lambda_i}$。这保证了所有特征方向对最终输出结果（Loss）的理论贡献绝对相等，排除“Tail 本身不重要”的干扰 [cite: 78, 79]。
* **目标标签 $y$：** $y = \beta^\top x + \epsilon$，其中 $\epsilon \sim \mathcal N(0, 0.1^2)$。
* [cite_start]**核心评估指标：** 信号存活率 (Signal Survival Rate) $S_{sig}$ [cite: 77]。
    $$S_{sig} = \frac{\sum_{i \in Group} \lambda_i a_i^2}{\sum_{i \in Group} \lambda_i \beta_i^2}$$
    （分别计算 $Group = Head$ 和 $Group = Tail$ 的存活率）。

---

## 三、 实验 1：稳态闭式解实验 (Steady-State Closed-Form Validation)

[cite_start]**目的：** 验证在 Global WD 设定下，统一 Weight Decay 会导致 Tail 特征的稳态天花板彻底坍塌，而解耦正则化可以挽救这一问题 [cite: 78, 126]。

**执行细节：**
1.  **数据生成：** 采样 $N = 500,000$ 个样本构建矩阵 $X \in \mathbb R^{N \times 8}$ 和向量 $y \in \mathbb R^{N \times 1}$。
2.  [cite_start]**求解方式：** 不使用 SGD，直接使用正则化最小二乘法的严格闭式解 [cite: 79]：
    $$w^* = (\frac{X^\top X}{N} + \Gamma)^{-1}(\frac{X^\top y}{N})$$
3.  **对比组设置 (调节矩阵 $\Gamma$)：**
    * *Baseline (统一正则):* $\Gamma = \gamma I$，其中 $\gamma = 10$。
    * [cite_start]*Ours (分支解耦正则):* $\Gamma = \operatorname{diag}(\gamma_h, \gamma_h, \gamma_h, \gamma_h, \gamma_t, \gamma_t, \gamma_t, \gamma_t)$，其中 $\gamma_h = 10, \gamma_t = 0.1$ [cite: 78]。
4.  **输出要求：** 打印出两种设置下的 Head $S_{sig}$ 和 Tail $S_{sig}$ 百分比表格。

---

## 四、 实验 2：带时间轴 $t$ 的动力学实验 (Kinetic Learning Curve)

[cite_start]**目的：** 验证在有限训练步数内，不同 Expert 占用率 $p_e$ 和不同的 WD 底层实现（Global vs. Lazy）是如何在时间轴上拖慢或压死 Tail 特征的 [cite: 118, 120]。

**执行细节：**
1.  **超参数设定：** * 学习率 $lr = 0.01$。
    * 总训练步数 $T = 20,000$ 步。
    * [cite_start]设定两种专家：Frequent Expert ($p_e = 0.5$) 和 Rare Expert ($p_e = 0.05$) [cite: 120]。
    * 设定统一 Weight Decay 系数 $\gamma = 0.1$。
2.  **模拟 SGD 迭代 (关键逻辑)：** 初始化权重 $w = \mathbf{0}$。在每一个 Step $t$ 中：
    * 生成一个 Batch ($B=32$) 的数据 $X_b, y_b$。
    * 通过均匀分布随机采样决定当前专家是否被激活（命中率 $= p_e$）。
    * **如果命中 (Activated):** 计算梯度 $g = \frac{1}{B} X_b^\top (X_b w - y_b)$。
        权重更新：$w \leftarrow w - lr \cdot g - lr \cdot \gamma \cdot w$。
    * **如果没有命中 (Not Activated):**
        * [cite_start]**对于 Global WD 模拟：** $g = 0$。依然执行衰减：$w \leftarrow w - lr \cdot \gamma \cdot w$ [cite: 126]。
        * [cite_start]**对于 Lazy WD 模拟：** $g = None$。直接 `continue`，**完全不更新 $w$** [cite: 124]。
3.  **动态 WD 救援测试 (Ours):**
    在 Lazy WD 的代码逻辑基础上，将衰减系数改为与 $p_e$ 绑定：$\gamma_{dynamic} = \gamma \cdot p_e$。
4.  **记录与绘图要求：**
    * 每 100 步记录一次 Rare Expert 和 Frequent Expert 的 Tail 信号存活率 $S_{sig}(t)$。
    * **绘制三张折线图 (X轴为 Step $t$，Y轴为 Tail $S_{sig}$)：**
        1. Global WD 下，Frequent vs. Rare 的曲线对比（预期 Rare 极低且平缓）。
        2. [cite_start]Lazy WD 下，Frequent vs. Rare 的曲线对比（预期 Rare 最终能上去，但极慢，在 20000 步时远低于 Frequent） [cite: 121]。
        3. Dynamic WD 下，Frequent vs. Rare 的曲线对比（预期两者的学习效率和轨迹被拉齐）。

---
**End of Handoff Document**
