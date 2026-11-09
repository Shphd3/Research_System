---
experiment_id: A14_02_E02_frequency_mapping_rank_separation
status: completed
verdict: pass_noninferior
completed_date: 2026-07-26
canonical_summary: summary.md
---

# 结果摘要：E02 频次—mapping 功能秩分离

主 anchor：[A14_02_01](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_01_frequency_mapping_rank_separation_anchor_cn.md)  
Protocol：[批准版本](protocol_cn.md)

## 直接结论

**Verdict：**`pass_noninferior`。

在注册的 common-mapping NTP 任务中，把 target exact frequency 从 \(8\) 降到
\(1\)，没有迫使冻结读出 ROOT 功能秩发生有意义的上升。10/10 paired seeds 的
能力与 rank validity 全部通过；LowF–HighF 秩差均值为 \(0.2\) 个方向，单侧 95%
upper bound 为 \(0.5\)，远低于预注册的 \(2\) 方向边界。

这说明：一个 cell 可以很 rare，但如果它调用的 mapping 已由其他 surfaces
学会，其任务方向可以被复用。至少在这个受控任务中，raw frequency 不是决定
任务功能秩的充分变量。

## 主指标公式与解析

只用 calibration 拟合 ROOT 子空间：

\[
\widetilde h_\rho^{(q)}
=
\mu+U_qU_q^\top(h_\rho-\mu).
\]

冻结原输出头，rank-selection 选择：

\[
k_{\mathrm{func}}^{\mathrm{fix}}
=
\min\{q:\Delta CE_q\le0.02\ \mathrm{nat},\ \Delta Acc_q\le0.01\}.
\]

这个指标的单位是“ROOT 方向数”，表示保持原模型答案行为所需的最少线性方向；
它不是严格矩阵秩，也不是单样本属性。

paired 决策量为：

\[
D_s
=
k_{\mathrm{func},s}^{\mathrm{LowF}}
-k_{\mathrm{func},s}^{\mathrm{HighF}}.
\]

结果：

- LowF 平均 \(7.6\)，范围 \(7\)--\(8\)；
- HighF 平均 \(7.4\)，范围 \(7\)--\(8\)；
- \(D_s=[0,1,0,0,-1,1,0,0,1,0]\)；
- \(\bar D=0.2\)，单侧 95% bounds 为 \([-0.1,0.5]\)；
- 10/10 pairs 均满足 \(D_s\le2\)。

## 能力与有效性指标分析

unseen-cell accuracy 定义为：

\[
Acc_{\mathrm{unseen}}
=
\frac1{|\mathcal D_{\mathrm{unseen}}|}
\sum_{(r,a,c)}
\mathbf1\{\arg\max_y p_\theta(y\mid r,a,c)=\pi(a)\}.
\]

这些 cell 的 optimizer frequency 严格为零，但 alias 和 entity 分别在其他
cells 中出现。LowF 的 mean/min 为 \(1.000/1.000\)；HighF mean 为 \(0.9926\)，
minimum 为 \(0.96875\)，都高于研究者批准的 \(0.75\) 门。

其他有效性证据：

- LowF target/new-context accuracy：10/10 为 \(1.0\)；
- 20/20 final-rank replays 通过；
- full-rank replay 最大 CE 误差 \(6.71\times10^{-8}\) nat；
- ROOT shuffle 平均增加 CE：LowF \(14.65\) nat，HighF \(14.42\) nat；
- 640 个 matched-rank random subspaces 中 0 个通过。

因此，小功能秩不能由“模型没学会”“ROOT 不影响答案”或“任意同维子空间都行”
解释。

## 中心图

![Exact frequency 与功能秩](figures/frequency_functional_rank.png)

纵轴是保持答案任务所需的 ROOT 方向数。两组都位于 7--8 方向；正式结论来自
paired non-inferiority interval，而不是只看箱线图重叠。

## E03 门控结果

E03 不执行 full run。它要求 common-step parameter basis 的 held-out capture：

\[
C_{\mathrm{common}}
=
\frac{\|P_{G_c}V_{\mathrm{test}}\|_F^2}
{\|V_{\mathrm{test}}\|_F^2}
\ge0.80.
\]

实际范围只有 \(0.478\)--\(0.631\)，0/10 通过。因此当前不能稳定定义
“outside-common parameter direction”，不能通过事后增加 rank 强行运行 E03。

## 认识更新与边界

**更新：**“rare 必须高秩”被当前证据直接削弱。更准确的说法是：当 rare cell
可调用已经跨 surface 学会的映射时，降低该 cell 的 exact frequency 不必增加
答案任务所需的 ROOT 方向。

**同时保留：**功能方向复用不自动推出 raw parameter-update directions 跨样本
共享。E03 的门失败说明 parameter-space 机制仍未识别。

**不能声称：**frequency 在所有任务中无关；raw ROOT/完整参数低秩；自然语言
rare facts 已验证；mapping 数量是普适因果定律；H9-F 由 NTP 自动推出。
