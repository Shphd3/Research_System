---
anchor_id: 15_08_04_transition_object_spectrum_sensitivity
status: EXECUTED_AWAITING_HUMAN_JUDGMENT
canonical_companion: 15_08_04_transition_object_spectrum_sensitivity_anchor.md
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor_cn.md
depends_on: 15_08_03_function_admitted_update_representation_rank_anchor_cn.md
parent_line: 15_spectral_representation_and_functional_routing
execution_authority: APPROVED_IMPLEMENTATION_SMOKE_FULL_RUN_2026-08-17
created: 2026-08-17
updated: 2026-08-17
---

# A15_08_04：层对象与 RMSNorm 定义的谱敏感性

父问题见 [A15_08](../15_08_target_conditioned_layer_innovation_anchor_cn.md)。英文正式版本见 [Canonical Anchor](15_08_04_transition_object_spectrum_sensitivity_anchor.md)。

## 1. Problem Definition

本子 Anchor 只问一个描述性决策问题：

> 在同一冻结模型与同一批 2,048 个 DCLM token 上，当对象分别是相邻 Attention write 差、四种 raw/normalized MLP 位置差、同层 \(U=Z-X\)，以及 MLP 位置的 raw/normalized 状态时，中心化协方差谱是否会产生实质变化？

当前阻塞是对象身份。相邻层、MLP 输入和同层更新的谱只有在 hook 与 RMSNorm 位置写清后才能比较。本实验只审计无标签表征几何；功能、语义、因果、总体内禀秩和 Router 效用都不在范围内。

## 2. Physical Priors

**先验：**协方差秩属于一个具名随机向量，而不属于抽象的“某层”。residual 累积、Attention 单独写入、相邻层差分和 RMSNorm 都可能改变 token 点云的谱。若所有注册 raw/RMSNorm 对照都产生近似相同的归一化谱与 \(r_{80}\)，该先验被削弱。

## 3. Falsifiable Hypotheses

**H-SENS：谱对对象定义敏感。**至少一个注册的 raw—RMSNorm 配对对照，其层间 \(r_{80}\) 占可识别秩的差值中位数至少为 0.05，且至少 70% 匹配层方向一致。

**最强竞争解释 R-ROBUST：谱对对象定义稳健。**在 token、中心化、秩上限和绘图坐标完全一致时，所有配对对照的 \(r_{80}\) 占比差值中位数均小于 0.02，且没有对照达到 70% 方向一致。

介于两者之间、身份 guard 失败、谱非有限、层不完整或 covariance trace 低于 \(10^{-12}\) 均为 `INSUFFICIENT`。这些阈值只裁定定义敏感性，不定义科学意义上的低秩。

## 4. Mathematical Model

对 block \(\ell\)，定义 Attention 前 raw residual \(h_\ell\)、raw Attention write \(a_\ell\)、Attention 后 raw residual \(r_\ell=h_\ell+a_\ell\)、归一化旧状态 \(X_\ell=N_\ell(h_\ell)\)、实际归一化 MLP 输入 \(Z_\ell=N_\ell(r_\ell)\)，以及同层更新 \(U_\ell=Z_\ell-X_\ell\)。

每个注册对象矩阵 \(M_{c,\ell}\in\mathbb R^{2048\times4096}\) 在 token 行中心化后计算

\[
G_{c,\ell}=\frac{1}{2047}\widetilde M_{c,\ell}\widetilde M_{c,\ell}^{\top}.
\]

令降序非负特征值为 \(\lambda_j\)，\(p_j=\lambda_j/\sum_k\lambda_k\)，主紧凑度量为

\[
r_{80}(c,\ell)=\min\left\{r:\sum_{j\le r}p_j\ge0.8\right\},
\]

并汇报 \(r_{80}/2047\)。effective rank 与 covariance trace 为辅助量。该谱只描述具名对象的 token 变化，不能识别目标信息。

## 5. Computational Realization

1. 本地加载 Qwen3-8B，对一段长度 2,048 的 DCLM token 序列做一次确定性 forward，不训练。
2. 捕获 36 层所有 token 的 block 输入与 raw Attention `o_proj` 输出；用每层自己的 post-Attention RMSNorm 重算 \(r,X,Z,U\)，并核对 native MLP 输入等于 \(Z\)。
3. 构造八个条件：\(\Delta a,\Delta h,\Delta X,\Delta r,\Delta Z,U,r,Z\)。相邻差有 35 条曲线；同层状态/更新有 36 条。
4. 用 float32 计算中心化 Gram 谱，只截断负数值误差并按 trace 归一化；保留统一 2,048-rank 横轴。中心化导致最后一个特征值结构性为零，只在 log 展示时设下限。
5. 每个条件输出一张全层图，再输出 2×4 同坐标总图、层中位谱叠图以及 trace、\(r_{80}\)、effective rank 数表。

## 6. Minimal Falsification Tests

主配对对照是 Attention 前 RMSNorm 效应 \((\Delta X,\Delta h)\)、Attention 后 MLP 位置 RMSNorm 效应 \((\Delta Z,\Delta r)\)，以及状态 RMSNorm 效应 \((Z,r)\)。逐对计算 \(r_{80}/2047\) 的层配对绝对差中位数和更大方向占比。

- **Pass — `DEFINITION_SENSITIVE`：**任一对照绝对差中位数至少 0.05，且方向一致率至少 0.70。
- **Fail — `DEFINITION_ROBUST_WITHIN_TOLERANCE`：**所有对照绝对差中位数均低于 0.02，且方向一致率均低于 0.70。
- **Insufficient：**其他数值结果或任何有效性 guard 失败。

其他对象和全部谱图只作描述，不能挽救或推翻配对 verdict。

## 7. Current Evidence

完整运行已覆盖 2,048 个固定 DCLM token、36 层和 283 条注册谱曲线，身份与重放 guard 均为零误差。注册结果为 `DEFINITION_SENSITIVE`：状态对照 \((Z,r)\) 的 \(r_{80}/2047\) 绝对差中位数为 0.194675、方向一致率为 0.8056；但两个相邻差分对照 \((\Delta X,\Delta h)\) 和 \((\Delta Z,\Delta r)\) 只有 0.013679/0.6286 与 0.011724/0.5714，均未达到敏感阈值。

后验尺度审计发现，raw \(r_l\) 从 block 8 起被序列首 token 的极大范数支配：block 8 最大范数 12,414、中位数 46.7，约 266 倍。因此当前 Pass 应读作“整层状态谱依赖 RMSNorm，且 raw 状态会被尺度异常扭曲”，不能读作“跨层新增信息的秩对 RMSNorm 大幅敏感”。完整来源见 [canonical Summary](../../../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_04_E01_dclm_transition_object_spectrum_comparison/summary.md)。当前解释仍为 `AI_DRAFT_AWAITING_HUMAN_JUDGMENT`。

## 8. Claim Boundary And Next Decision

当前结果最多说明：在冻结 Qwen3-8B 和这一段 DCLM token 上，表面谱紧凑性会随具名对象与 RMSNorm 实质改变；该敏感性由整层状态而非相邻层差分主导。它不能识别新增信息、语义、模型原生 feature、总体内禀秩或 Router 效用，也不能把 raw \(r_l\) 的 rank-1 外观解释成语义低秩。

**唯一下一决策：**研究者确认是否把 \(U_l=Z_l-X_l\) 冻结为后续 token-subspace 分析的主对象，并把 raw \(r_l\) 限定为尺度诊断。完成条件是明确接受或拒绝这一对象边界；恢复时先阅读 canonical Summary，再决定是否另立功能条件化的子空间实验。
