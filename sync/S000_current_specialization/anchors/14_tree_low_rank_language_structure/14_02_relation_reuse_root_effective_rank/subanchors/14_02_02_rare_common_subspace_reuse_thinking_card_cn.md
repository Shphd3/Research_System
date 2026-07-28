---
thinking_card_id: 14_02_02_rare_common_subspace_reuse
status: human_approved
approved_date: 2026-07-26
human_language: zh
formalization_authorized: true
protocol_authorized: true
full_run_authorized: conditional_on_e02_gates
---

# Rare 暴露是否新增功能上必要的方向 — Thinking Card

## Human Judgment

**具体现象：** rare 样本调用 common mapping 时，它的 gradient 或实际 optimizer
update 不必严格位于估计的 common 参数空间；但“空间外分量存在”不等于它大、
几何上新，更不等于模型在任务中使用它。

**机制猜想：** rare 暴露的大部分任务有效更新复用 common 参数和 ROOT 功能
空间。common 外分量可能幅度很小、复用历史 residual，或几何上新但只承载
nuisance/gauge。只有非小、历史上新、且删除后任务退化，才是新功能方向。

**最强替代解释：** rare 样本确实需要 common mapping 无法提供的新任务方向；
或者 outside-common 只是 common-space 估计不足、AdamW 逐坐标预条件、batch
混合、参数坐标 gauge 或非线性训练分叉的测量假象。

**最不确定之处：** 如何把一次 rare 暴露从训练轨迹中归因出来，以及如何把
参数新分量转成可审计的功能干预。

**会改变判断的证据：** rare/control 从同一 checkpoint 与 optimizer state
出发，仅相差一个注册样本；若 target-attributable effect 中存在稳定非小的
历史 residual 外分量，且精确删除该分量后 rare held-out CE 显著上升，则承认
rare 暴露新增了功能方向。

**当前唯一决策：** 用 leave-target-out common 空间、历史 residual 空间、
单步配对 AdamW 反事实和 frozen-head exact endpoint replay，判断 rare 新分量
是否功能必要。

## Human-Approved Operationalization

- 主时间尺度是一个实际 AdamW step；多步 continuation 不进入主 verdict；
- rare 与 control 使用同一 entity、同一答案、匹配 context，只改变 cell 的
  rare/common 身份；
- 输出头在两支更新与全部 replay 中冻结为同一个 reference head；
- $G_c$ 只使用 target 之前、且 leave-target-out 的 common step contrasts；
- $R_{\mathrm{old}}$ 只使用 target 之前的历史 residual updates；
- $v_r=\theta_T^{\mathrm{rare}}-\theta_T^{\mathrm{ctrl}}$ 是实际 optimizer
  有限效应，不称为 per-example gradient；
- drop-new endpoint 精确定义为
  $\theta_T^{\mathrm{drop-new}}=\theta_T^{\mathrm{rare}}-v_{\mathrm{new}}$；
- ROOT 新效应由两个 endpoint 完整前向差分定义，不使用单点 Jacobian；
- 主因果指标是 $\Delta CE_{\mathrm{drop-new}}$；$\rho_\perp$ 与
  $\rho_{\mathrm{new}}$ 是几何守卫。

## AI Audit Resolution

未定义对象已关闭：drop-new 是完整参数 endpoint 干预，直接重新运行模型；它
不假设 ROOT 对参数线性，也不恢复已被 E06 否定的 H11。参数几何仍依赖注册
坐标，因此只有 frozen-head 功能删除结果能够决定任务必要性。

AI verdict: `READY`, conditional on E02 capability, rank-validity, and
common-space stability gates.
