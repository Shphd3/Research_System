---
thinking_card_id: 14_02_01_frequency_mapping_rank_separation
status: human_approved
approved_date: 2026-07-26
human_language: zh
formalization_authorized: true
protocol_authorized: true
full_run_authorized: true
---

# 低频调用 common mapping 是否额外增加 ROOT 功能秩 — Thinking Card

## Human Judgment

**具体现象：** E01 已观察到 exact duplicate 不能替代独立 context diversity；
在 capability-passing lookup 条件中，独立 mapping 数 $K=1/4/16$ 时固定读出
ROOT 功能秩均值为 $10.2/11.0/12.8$。因此，样本频次、context 多样性和独立
任务函数数量不是同一变量。

**机制猜想：** 一个 rare exact relation 若调用已经由其他 surface 学到的
common mapping，不需要为该 rare surface 单独建立新的任务功能方向。方向预算
更直接地受已学 mapping 并集控制，而不是受该 cell 的 raw frequency 控制。

**最强替代解释：** LowF 看起来秩低可能只是模型没有学会、答案头瓶颈、
nuisance 被主指标忽略，或 LowF/HighF 的总 common-function 剂量、边际与训练
预算没有真正匹配。

**最不确定之处：** 新 nuisance context 正确并不等于跨 surface 复用。最低
复用门必须是：alias $r$ 和 entity $a$ 分别在训练中出现，但精确 cell $(r,a)$
在实际 optimizer stream 中零曝光；模型仍需输出由同一 common mapping 给出的
$\pi(a)$。

**会改变判断的证据：** 在能力、匹配、重放和 test isolation 全部通过后，
Common-LowF 的固定读出功能秩稳定比 Common-HighF 高出超过两个方向；或后续
E03 表明 rare 暴露需要功能上不可删除的新方向。

**当前唯一决策：** 在总 common-function dose 和全部边际不变时，只把 target
exact frequency 从 $8$ 改为 $1$，判断固定读出 ROOT 功能秩是否非劣。

## Human-Approved Operationalization

- frequency target 与 unseen-cell 是两批互斥 cell；前者 $F=1/8$，后者 $F=0$；
- unseen-cell final accuracy 门因小样本和小模型冻结为 $0.75$；
- 主指标是 calibration 选择、final test 验证的
  $k_{\mathrm{func}}^{\mathrm{fix}}$；
- 主决策量为 paired difference
  $D_s=k_{\mathrm{LowF},s}-k_{\mathrm{HighF},s}$；
- 非劣效 margin 冻结为 $\tau=2$ 个方向；
- 参数更新空间不作为 E02 主指标，交由 E03 处理；
- 旧 E01 的 $K=1/4/16$ 趋势保留为次级历史证据，不与 frequency verdict 混写。

## AI Audit Resolution

未定义对象已关闭：unseen-cell 是训练实际流中零曝光、但 alias 与 entity 两个
组成部分分别被观察的 held-out matrix cell。主指标能够排除“低秩只是未学会”
的解释，前提是 unseen capability、完整重放、shuffle 和随机子空间守卫通过。

AI verdict: `READY`.
