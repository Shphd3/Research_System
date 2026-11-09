---
anchor_id: 14_02_01_frequency_mapping_rank_separation
status: completed_pass_noninferior
canonical_language: en
canonical_file: 14_02_01_frequency_mapping_rank_separation_anchor.md
parent_anchor: 14_02_relation_reuse_root_effective_rank
experiment_id: A14_02_E02_frequency_mapping_rank_separation
---

# A14_02_01 频次—mapping 功能秩分离


## 1. Problem Definition

唯一问题：在 common mapping 已经跨 surface 学会后，把 target cell 的实际
optimizer 呈现次数从 \(F=8\) 降到 \(F=1\)，是否会使冻结读出 ROOT 功能秩增加
超过两个方向？frequency target 的 \(F=1/8\)；unseen-cell 是另一批 \(F=0\)、但
alias 与 entity 分别在训练中出现的 cell。ROOT 是 final norm 后、冻结输出头前
的状态。

## 2. Physical Priors

1. 其他 aliases 已经提供同一 \(y=\pi(a)\)，所以 rare cell 不必建立独立方向。
2. 模型必须先通过新 context 与严格 unseen-cell 能力门；否则小秩只是没学会。
3. \(F\) 必须靠重新分配 exposure 改变；总 function dose、全部边际和训练预算固定。

## 3. Falsifiable Hypotheses

\[
D_s
=
k_{\mathrm{func},s}^{\mathrm{LowF}}
-k_{\mathrm{func},s}^{\mathrm{HighF}},
\qquad
\mathbb E[D_s]\le2.
\]

至少八个有效 paired seeds，单侧 95% upper bound 不超过两个方向则支持；单侧
95% lower bound 大于两个方向则否定；区间跨界或任一 hard gate 失败为证据不足。

## 4. Mathematical Model

\[
p(y\mid r,a,c)=\mathbf1\{y=\pi(a)\}.
\]

只用 calibration 拟合 \(\mu,U\)：

\[
\widetilde h_\rho^{(q)}
=
\mu+U_qU_q^\top(h_\rho-\mu).
\]

冻结原输出头，定义：

\[
k_{\mathrm{func}}^{\mathrm{fix}}
=
\min\{q:\Delta CE_q\le0.02\ \mathrm{nat},\ \Delta Acc_q\le0.01\}.
\]

rank 在 calibration-selection 选择，并且 final test 只验证、不重新选 rank。

## 5. Computational Realization

16 个 aliases、17 个 entities 共用一个固定随机 bijection \(\pi\)。每个 seed 中，
每个 alias 有四个 frequency targets、八个 unseen calibration/test cells 和五个
高剂量 donor cells。整数 transportation table 把每个 target 的七次 exposure
在 target 与 donor 之间移动，严格保持逐 alias/entity/answer/context 边际。
模型为两层、单头、width 64 causal Transformer，目标为 full-position NTP CE。

## 6. Minimal Falsification Tests

1. materialized count 与实际 optimizer count 完全一致；
2. target-new-context accuracy \(\ge0.95\)、unseen-cell final accuracy
   \(\ge0.75\)、target full-state CE \(\le0.10\) nat；
3. final test 在冻结 rank 下仍满足 0.02 nat / 0.01 accuracy 容忍度；
4. full-rank replay、shuffle 与 matched-rank random-subspace 守卫通过；
5. leave-target-out common-update basis 对 held-out common step contrasts 的
   capture \(\ge0.80\)，否则不执行 E03。

## 7. Current Evidence

E01 已分开 duplicate 与 context diversity，并在 capability-passing lookup
\(K=1/4/16\) 得到均值 \(10.2/11.0/12.8\)。归档 E02-v1 在已见 pair 新 context
通过，但强 unseen component recombination 为 0/5。二者都没有裁定已学 common
mapping 内的 exact frequency 效应。

批准的 full run 得到 10/10 有效 pairs。LowF/HighF 平均功能秩为 7.6/7.4，
paired mean difference 为 0.2，单侧 95% upper bound 为 0.5，因此通过两方向
非劣效门。LowF unseen-cell accuracy 在 10/10 seeds 为 1.0；replay、shuffle 与
random-subspace 守卫全部通过。

结果：[中文摘要](../../../../experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E02_frequency_mapping_rank_separation/summary_cn.md) · [完整记录](../../../../experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E02_frequency_mapping_rank_separation/detailed.md)。

## 8. Claim Boundary And Next Decision

即使通过，也只说明注册受控 NTP 任务中，降低 exact-cell frequency 没有迫使
答案任务 ROOT 功能秩上升；不能推广为 frequency 永远无关、raw ROOT/完整参数
低秩或自然语言定律。

唯一下一决策：E03 因 common-step parameter-space capture 只有 0.478--0.631 而
parked；下一版必须用 fresh probes 定义 common functional/secant space。
