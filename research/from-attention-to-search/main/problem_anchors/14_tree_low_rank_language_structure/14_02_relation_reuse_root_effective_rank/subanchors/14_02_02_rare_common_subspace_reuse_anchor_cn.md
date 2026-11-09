---
anchor_id: 14_02_02_rare_common_subspace_reuse
status: parked_common_space_gate_failed
canonical_language: en
canonical_file: 14_02_02_rare_common_subspace_reuse_anchor.md
parent_anchor: 14_02_relation_reuse_root_effective_rank
experiment_id: A14_02_E03_rare_common_subspace_reuse
---

# A14_02_02 Rare–common 子空间复用


## 1. Problem Definition

唯一问题：一个调用已学 common mapping 的 rare 暴露，是否会在 leave-target-out
common update 空间之外产生幅度非小、历史上新、且冻结读出任务功能上必要的
方向？参数空间中非零不等于任务功能方向。

## 2. Physical Priors

1. common mapping 复用预言大部分任务有效 rare update 复用 common 或旧 residual；
2. AdamW 与参数 gauge 会产生几何 outside 分量，所以 gradient、实际 step 和
   function effect 必须分开；
3. 功能必要性必须用 exact endpoint 干预，不用单点 Jacobian 翻译有限分量。

## 3. Falsifiable Hypotheses

rare/control 从同一 reference 与 optimizer state 各走一个 AdamW step：

\[
v_r=\theta_T^{\mathrm{rare}}-\theta_T^{\mathrm{ctrl}}.
\]

只有 rare branch 先产生可测功能增益，才能继续判断新方向是否必要。若新分量
可忽略或删除后功能保持，支持复用；若新分量稳定非小且精确删除造成特异任务
损害，则否定复用充分性。

## 4. Mathematical Model

\[
v_\parallel=P_cv_r,
\qquad
v_\perp=(I-P_c)v_r,
\]

\[
v_{\mathrm{old}}=P_{\mathrm{old}}v_\perp,
\qquad
v_{\mathrm{new}}=(I-P_c-P_{\mathrm{old}})v_r.
\]

\[
\rho_\perp=\frac{\|v_\perp\|_2^2}{\|v_r\|_2^2},
\qquad
\rho_{\mathrm{new}}=\frac{\|v_{\mathrm{new}}\|_2^2}{\|v_r\|_2^2}.
\]

精确删除终点：

\[
\theta_T^{\mathrm{drop-new}}
=\theta_T^{\mathrm{rare}}-v_{\mathrm{new}}
=\theta_T^{\mathrm{ctrl}}+v_\parallel+v_{\mathrm{old}}.
\]

冻结同一个 reference output head，主因果量为：

\[
\Delta CE_{\mathrm{drop-new}}
=CE(\theta_T^{\mathrm{drop-new}})-CE(\theta_T^{\mathrm{rare}}).
\]

这是完整模型前向的 exact endpoint intervention，不使用 H11。

## 5. Computational Realization

复用 E02 中有效的 Common-LowF checkpoints 与 optimizer states。rare cell 在
E02 中从未进入 optimizer；matched control 具有相同 entity、答案和 exposure
context，但属于历史高频 cell。两支只改变该样本身份。\(G_c\) 与
\(R_{\mathrm{old}}\) 都严格早于 target 且 leave-target-out；output head 在两支
更新前冻结。

## 6. Minimal Falsification Tests

1. E02 capability、rank-validity 和 common-space stability 全过；
2. rare/control 起点的模型与 optimizer state 完全相同；
3. rare full branch 先有 \(\Delta CE_{\mathrm{gain}}\ge0.02\) nat，否则功能必要性
   为 insufficient；
4. 新几何需要 \(\rho_{\mathrm{new}}\ge0.05\) 且超过 common-common null；
5. 新方向功能必要需要 \(\Delta CE_{\mathrm{drop-new}}>0.02\) nat、超过等范数
   random deletion，并保持 base/common CE 在 0.02 nat 内。

## 7. Current Evidence

E04 支持局部共享 Jacobian image；E05/E06 表明实际 optimizer displacement 与
exact ROOT secant 有效低维，但 endpoint/reference 单点 Jacobian 不能表示有限
效应。因此 E03 直接使用 exact endpoints，并把参数几何降为功能 verdict 的
必要守卫。

在 rare treatment 前，common-step parameter space 前置门失败：held-out capture
为 0.478--0.631（均值 0.5717），0/10 seeds 达到 0.80。因此 E03 full
intervention 没有执行；这是 operationalization failure，不是 rare 功能新颖性的
正负证据。

结果：[中文摘要](../../../../experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E03_rare_common_subspace_reuse/summary_cn.md) · [完整记录](../../../../experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E03_rare_common_subspace_reuse/detailed.md)。

## 8. Claim Boundary And Next Decision

通过最多说明注册 checkpoint 与单步尺度下，可测 rare effect 不需要新的冻结
读出任务方向；否定最多说明这一受控 rare 暴露需要注册新方向。均不能推广到
所有 rare facts、完整参数低秩、自然语言或 NTP 自动推出 H9-F。

唯一下一决策：重试前用 fresh probes 预注册并验证 leave-target-out common
ROOT-functional/secant space。
