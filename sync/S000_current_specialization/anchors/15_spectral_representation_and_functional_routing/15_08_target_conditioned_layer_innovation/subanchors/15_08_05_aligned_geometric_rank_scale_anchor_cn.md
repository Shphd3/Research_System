---
anchor_id: 15_08_05_aligned_geometric_rank_scale
status: EXECUTED_AWAITING_HUMAN_JUDGMENT
canonical_companion: 15_08_05_aligned_geometric_rank_scale_anchor.md
thinking_card: 15_08_05_aligned_geometric_rank_scale_thinking_card_cn.md
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor_cn.md
depends_on: 15_08_04_transition_object_spectrum_sensitivity_anchor_cn.md
created: 2026-08-18
updated: 2026-08-18
---

# A15_08_05：对齐模型、token 与指标后，秩差异是否仍存在？

## 1. Problem Definition

A15_08_04 在 Qwen3-8B、2,048 token 下比较八类对象，主要使用 $r_{80}$；组会中的 ZX/CAR 使用 Qwen3-0.6B、约百万 token 和 $r_{90}$。因此当前唯一问题是：

> 在同一 Qwen3-0.6B、同一批评价 token 和同一个中心化协方差 $r_{90}$ 估计器下，CAR 的完整 block 相邻差、ZX 的500维 Attention 相邻差与我们的 $R_U$ 是否仍呈现材料性的秩差异？

这是尺度与对象口径审计，不做聚类，不检验语义、因果使用或 Router 收益。

## 2. Physical Prior

协方差秩属于一个具名对象和样本总体。token 数增加会解除样本秩上限；投影、差分、归一化和线性去旧都会改变谱。如果三种对象在对齐后具有近似相同的归一化 $r_{90}$，则“对象定义解释冲突”的判断被削弱。

## 3. Falsifiable Hypotheses

**H-OBJECT：**token 数收敛后，CAR 和 ZX 相对匹配目标层 $R_U$ 的层中位归一化 $r_{90}$ 都至少相差 0.10；差异方向由数据决定。

**R-NO-GAP：**两组绝对差都小于 0.03。其他结果或不收敛记为 `MIXED_OR_INSUFFICIENT`。

所有对象来自同一个 Qwen3-0.6B forward，因此模型大小解释在本实验内部被固定，而不是被额外估计。

## 4. Mathematical Model

对 block $l$，令 $h_l$ 为 raw 输入 residual，$a_l$ 为 Attention `o_proj` write，$N_l$ 为 post-Attention RMSNorm，$H_l$ 为完整 block 输出：

$$X_l=N_l(h_l),\qquad U_l=N_l(h_l+a_l)-N_l(h_l).$$

只用 TRAIN 拟合仿射岭回归，只用 DEVELOPMENT 选择无量纲正则强度：

$$R_{U,l}=U_l-\widehat{\mathbb E}_{lin}[U_l\mid X_l].$$

三个评价对象为

$$D^{CAR}_l=H_{l+1}-H_l,$$

$$D^{ZX}_l=Q_{500}^{\top}(a_{l+1}-a_l),$$

以及 $R_{U,l}$。$Q_{500}$ 是 TRAIN 最后 block 状态 PCA 的前500个方向，对应会议记录中的 ZX 最后层参考基；评价 token 不参与构基。

对任一对象中心化协方差的降序能量占比 $p_j$：

$$r_{90}=\min\{r:\sum_{j\le r}p_j\ge0.9\}.$$

主比较量为 $r_{90}/d_{object}$，同时保留绝对 $r_{90}$ 与完整累计谱。

## 5. Computational Realization

使用本地 Qwen3-0.6B 和不重叠 DCLM token 分区，序列长度固定为2,048。TRAIN、DEVELOPMENT 各131,072 token；EVALUATION 为1,048,576 token。全量激活不落盘，使用按 batch 中心化的稳定流式 covariance/cross-covariance 统计。评价在2,048、8,192、32,768、131,072、524,288和1,048,576 token 处保存嵌套快照。

## 6. Minimal Falsification Test

三种对象共享模型、评价 token、hook、中心化、特征分解和 $r_{90}$ 规则。CAR/ZX 的目标 blocks 2--28 与相同 blocks 的 $R_U$ 配对。如果完整运行与524,288-token 快照的层中位 $r_{90}/d$ 相差不超过0.02，则该方法记为收敛。只有全部方法收敛，且身份、有限性、层覆盖和 token 计数 guard 全部通过，才能裁定 H-OBJECT 或 R-NO-GAP。

## 7. Current Evidence

对齐实验已经在 Qwen3-0.6B 的1,048,576个 EVALUATION token 上完成，三个方法从524,288到1,048,576 token 的层中位 $r_{90}/d$ 变化分别为0.00488、0.00400和0.00244，均通过0.02收敛阈值。全量结果为：

- CAR 完整 block 相邻差：层中位 $r_{90}=576/1024=56.25\%$；
- ZX 的500维 Attention 相邻差：层中位 $r_{90}=297/500=59.40\%$；
- $R_U$：层中位 $r_{90}=445.5/1024=43.51\%$。

配对层上，CAR-$R_U$ 的中位差为+0.1377，ZX-$R_U$ 为+0.1498，达到注册的 `METHOD_OBJECT_GAP` 判据。也就是说，同一模型与同一批 token 上，CAR/ZX 的层间差确实呈宽谱高秩，而线性去旧后的 $R_U$ 更集中，但仍需要数百个方向，不能称为一个极小的全局低秩空间。

CAR 的目标 block 3 是局部异常：$r_{90}=1$，第一方向占99.88%方差。去除每段序列的 position 0 后仍为 $r_{90}=1$、第一方向占90.95%，说明边界 token 会放大但不能完全解释该奇异性。它更像少量大幅、同向或离群更新支配 covariance，不能被解释成语义功能秩一。去除边界前后的 CAR 层中位 $r_{90}$ 为576与575，因此总体高秩结论不依赖该边界效应。

## 8. Claim Boundary And Next Decision

合格结果只能说明几何秩冲突是否在对齐后仍存在，以及差异由哪个具名对象产生。不能把协方差方向称为语义新增信息，不能证明功能充分性、非线性新颖性或 Router 价值。

当前证据支持“对象构造与样本规模足以解释低秩/高秩叙述的显著部分”：2,048-token 小样本明显低估了收敛后的 $r_{90}$，而 CAR/ZX 比 $R_U$ 宽约14--15个百分点。下一决策应由研究者闭卷判断：后续是否冻结 $R_U$ 作为“去掉旧状态线性可预测部分”的候选对象，并另外用任务收益检验它的功能秩。几何高秩本身不能决定 Router 输入，也不能回答哪些方向有用。
