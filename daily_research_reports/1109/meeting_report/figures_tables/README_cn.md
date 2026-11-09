# 1109 组会图表与两项只前向诊断

生成于 2026-11-09。所有表都同时有 CSV 和 Markdown 两份，所有图都同时有 PNG 和 PDF 两份。本轮没有训练，也没有改动正在续训的任务。科学判断：Unknown。D1、D2 与除 A1/A2 之外的逐 feature 对比都是**探索性**结果。

## 来源

- 五臂 2000 步结果包：`/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/`（下文简称“结果包”）。
- 每 250 步的评估产物：同一实验根目录下的 `eval/<臂>/stepXXXXXX.pt`，在 EVAL 的 2,097,152 个 token 上保存了逐层集中度、逐 feature NLL 和联合计数。
- A1 第 2000 步的 load bias：`runs/A1/milestones/token_000524288000/state.pt`。
- R02：`/data/250010109/MoE_Router/experiments/20261108_snr_mig_pilot/results/`。
- 代码在执行侧 `analysis/meeting_1109/`：`build_tables.py`（T1–T5、D1）、`d2_concentration_loss.py`（D2，MIG 上约 40 秒）、`figures.py`（全部图）。

## 公式

- 一步更新：

$$
\mathbb{E}[\Delta L_B]\approx-\eta\,g_B^\top\bar g_A+\tfrac{\eta^2}{2}\bar g_A^\top H_B\bar g_A+\tfrac{\eta^2}{2}\tfrac{\operatorname{tr}(H_B\Sigma_A)}{n}
$$

- 交叉步长：$\eta^\*\approx 2n\,g_B^\top\bar g_A/\operatorname{tr}(H_B\Sigma_A)$。
- 分发：$S_t=\operatorname{Top2}(s_t+b)$，$y_t=\sum_{e\in S_t}w_{t,e}E_e(h_t)$。
- 集中度：覆盖率 $c_i(e)=P(e\in S_t\mid i\in A_t)$，纯度 $\pi_i(e)=P(i\in A_t\mid e\in S_t)$，$p_i$ 是 feature $i$ 在 DEV 上的参考频率。

$$
\bar M_i=\frac1L\sum_l\sum_e\frac{c_i^{(l)}(e)}{k}\cdot\frac{c_i^{(l)}(e)\pi_i^{(l)}(e)}{p_i}
$$

  dense 为 1；随机 Top-2/8 为 $1/4$。表中的“中位数”是对 30000 个 feature 的 $\bar M_i$ 取中位数。
- 逐 feature 读数：$G_i(X,Y)=\mathrm{NLL}_i(Y)-\mathrm{NLL}_i(X)$，$\Delta_i(X,Y)=\log\bar M_i(X)-\log\bar M_i(Y)$，$\rho=\operatorname{Spearman}(G_i,\Delta_i)$。

## 表

| 文件 | 内容 | 读法 |
|---|---|---|
| `T1_R02_summary` / `T1b_R02_cross_pairs` | R02 的噪声项斜率、方向项与 z、SNR、$\eta^\*$；6 个跨簇对的方向项 | 6 个跨簇对的方向项全为正（帮助），3 个 z>2；$\eta^\*$ 为推导值（A01，事后） |
| `T2_five_arms_step2000` | 五臂总体 NLL、相对 A0、$\bar M$ 中位数、按出现次数加权的平均 $\log\bar M$、q10/q90、bin0/bin9 NLL | 中位数排序与 NLL 排序完全一致（秩相关 1.00）；按加权平均 $\log\bar M$ 排序，A0 与 A1-deep、A1 与 A4 互换（秩相关 0.80） |
| `T3_contrasts_by_step` | 250–2000 步的 A1−A2、A1−A0、A4−A0、A1-deep−A1、A1-deep−A0，每项给总体、bin0、bin9 | A1−A0 在 250、500 步为负，从 750 步起为正；A1−A2 在所有步数、所有频段都为负 |
| `T4_Mbar_median_by_bin` | 臂 × 10 个频段的 $\bar M$ 中位数 | 除 A2 外，各臂都是低频 feature 更集中；A1 在每个频段都低于 A0、A4、A1-deep |
| `T5_feature_spearman` | 5 组对比的 $\rho$，全部 feature 及 10 个频段分别计算 | A1/A2 的 $\rho=0.256$，低频段更高（bin0 为 0.34，bin9 为 0.10）；其余 4 组为探索性 |
| `D1_Mbar_by_step` | 各臂每 250 步的 $\bar M$ 中位数，以及 bin0、bin9 的中位数，附同步数 A1−A0 的 NLL 差 | 见下文 D1 |
| `D2_A1_concentration_variants`（含逐层对照，CSV 另存为 `D2_layerwise_A0_vs_A1.csv`）、`D2_checks.json` | 同一组 teacher 分数在 5 种分发规则下的 $\bar M$；A0 与 A1 的逐层 $\bar M_l$ | 见下文 D2 |

## 图

| 文件 | 读图说明 |
|---|---|
| `F1_noise_term_scaling` | R02 的噪声项随 η 的变化：几条线斜率接近 2；n 每翻一倍，整条线下移约一半。 |
| `F2_help_to_harm_crossing` | 用平均梯度走一步始终是帮助；单 batch 一步在 η 增大后由帮助转为伤害，n 越大转折越靠右（事后控制变量估计）。 |
| `F3_eval_nll_curves` | 五臂 EVAL NLL，不做平滑；右图是 1000–2000 步的放大。A2 始终最差；到 2000 步，A0 与 A1-deep 几乎重合。 |
| `F4_concentration_vs_nll` | 左：横轴是 $\bar M$ 中位数，五个臂的 NLL 随它单调下降。右：横轴改为加权平均 $\log\bar M$，A0/A1-deep、A1/A4 两组的次序互换。 |
| `F5_contrast_by_frequency` | 第 2000 步，A1 相对 A2 的优势在最低频 bin0 最大（−0.29），在 bin9 最小（−0.11）；A1 落后 A0 的幅度在各频段大致相同；A1-deep 与 A0 基本持平。 |
| `F6_Mbar_by_frequency` | 第 2000 步各频段 $\bar M$ 中位数。A0 在低频段超过 dense 参照 1；A2 贴着随机参照 1/4。 |
| `F7_contrasts_over_steps` | 同步数差值随训练步数的变化。A1−A0 在 500 与 750 步之间由负转正；A1-deep−A0 逐渐收敛到 0。 |
| `F8_train_ce` | 训练 CE：淡线是逐步原值，粗线是尾随 50 步均值；右图是 1000–2000 步的放大。次序与 EVAL 一致。 |
| `D1_Mbar_over_steps` | 三个子图分别是全部 feature、bin0、bin9 的 $\bar M$ 中位数随步数的变化；灰带标出 500–750 步。A0 从第 250 步起就高于 A1。 |
| `D2_concentration_loss` | 左：A1 的同一组分数在 5 种规则下的 $\bar M$ 中位数（点线是对应 k 的随机参照，虚线是 A0）。右：A0 的逐层 $\bar M_l$ 与 A1（8 层同一划分）的对比。 |

## D1：$\bar M$ 随训练步数的变化（探索性）

预登记的预测是：A0 的 $\bar M$ 中位数会在第 500 到 750 步之间超过 A1，并与 A1−A0 的符号翻转同步。**结果：不成立。** A0 从第 250 步起就更集中（A0 0.803，A1 0.547），之后持续上升到 1.010；A1 一直在 0.54–0.59 之间。两者的差从 250 步的 0.26 增大到 750 步的 0.39，此后稳定在约 0.42。A1−A0 的 NLL 差在 500 与 750 步之间由 −0.028 变为 +0.045。

这说明：A1 早期领先并不是因为“A0 当时还没集中”，因为 A0 当时已经更集中。早期领先另有原因，需要另外检查。可能的原因包括：前 1000 步 warmup 期间学习率小，固定路由更容易优化；或者在训练早期，集中度对学习的作用还没有显现。两者都未检验。时间上与 NLL 翻转同步的是“A0 集中度的增长”（0.80 → 0.93），而不是“A0 超过 A1”。

## D2：A1 的集中度在哪里损失（探索性）

对象是 A1 在第 2000 步的 Top-2 硬选择 $\bar M$ 中位数，实测为 0.586；用同一组 teacher 分数离线复算，(b) 与训练中保存的评估产物逐 feature 完全一致（最大差 0）。

| 情形 | $\bar M$ 中位数 |
|---|---:|
| (a) $b=0$，Top-2 | 0.697 |
| (b) 实际 $b$，Top-2（即 A1） | 0.586 |
| (c) $b=0$，只取 Top-1（$k=1$，随机参照 1/8） | 0.510 |
| (c′) 实际 $b$，只取 Top-1 | 0.442 |
| (d) 实际 $b$，Top-2，权重按 $\operatorname{softmax}(s/\tau)$（加权 $\bar M$） | 0.766 |

**结论：在可比的 Top-2 硬选择口径下，造成下降最大的一项是 load bias。** 去掉它，$\bar M$ 中位数从 0.586 回到 0.697。

补充事实：
- teacher 分数 $|s|$ 的均值是 0.057，第 2 与第 3 高分之差的均值是 0.036，而实际 $b$ 的极差是 0.136。
- load bias 的影响随频段不同：去掉它会让 bin9 从 0.49 升到 0.68，却让 bin0 从 0.74 降到 0.66。
- Top-1 与 Top-2 的随机参照不同，所以两者的绝对值不能直接比较。
- (d) 用的是按权重加权的集中度。按硬选择的定义，(d) 与 (b) 的 $\bar M$ 完全相同，因为硬选择不看权重。
- 逐层对照：A0 各层的 $\bar M_l$ 中位数是 0.83–0.97；A1 的 8 层 load bias 完全相同，所以 8 层的路由也完全相同，每层都是 0.586。即使取 $b=0$，A1 的 0.697 也低于 A0 的任何一层。
