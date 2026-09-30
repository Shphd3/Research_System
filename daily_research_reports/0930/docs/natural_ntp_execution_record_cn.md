# 自然 NTP 更新相容性：执行记录

[Protocol](protocol_cn.md) · [English](natural_ntp_execution_record.md)

截至 2026-09-29 18:00 UTC：工程 Smoke 已通过；Full 已提交且观察到运行。科学结果与 Focus 判断仍为 **Unknown**。

| 尝试 | 任务 ID | 已核事实 | 持久证据 |
|---|---|---|---|
| Smoke 1 | `pt-5k6mv35t` | 四个测量 worker 通过后，预测器恢复检查因 CPU 随机数状态被加载到 CUDA 而失败；未打开确认数据。 | `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/smoke_20260929T173730Z/result/failure.json` |
| Smoke 2 | `pt-1lqply7o` | 通过；64 个 OPS 事件、32 个数据对的梯度、临时更新及预测器下一步恢复检查均通过。 | `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/smoke_20260929T174308Z/result/smoke_receipt.json` |
| Full | `pt-dgpld36j` | 2026-09-29 17:59:39 UTC 提交，18:00:04 UTC 观察到 `RUNNING`；尚无科学结果。 | `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/submit/` 与 `pod/` |

三次提交均使用执行信封中的 `h100-4-reserved` 与 `shphd-lite-0911`。第二次 Smoke 实测用时 50.57 秒；其以 1.5 系数估算的 Full **事件采集部分**为 0.53 GPU 小时，并非整个 Full 的实测耗时。Full 保留 Protocol 的总计 24 GPU 小时和 50 GiB 产物上限，运行命令有时限，失败门槛不放宽。

数据准备已核对指定分片及分词器哈希：59,812 条来源记录中有 47,760 条合格，按哈希选取的 20,000 条候选去重后有 19,997 个文档组，足够完成预定四组划分。未按结果筛选。[数据清单](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/data_v1/data_manifest.json)保留计数和来源。

Full 应在 `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/` 留下采集、拟合、注册、确认预测封存、分析及验证收据。提交成功或平台显示 `SUCCEEDED` 均不足以判定科学结果，须按 Protocol 核对持久证据。本记录未提交 Git、推送或作科学裁决。

2026-09-29 18:01 UTC 启动核查：预定的 7,232 个事件已采集；OPS 数值分辨率阶段报告 PASS（`delta_l=6.69e-6`、`delta_k=1.82e-6`）；多个几何预测器拟合已到第 10 轮。平台仍为 `RUNNING`。这些只是阶段进度，尚无确认结果；仅凭早期几何拟合不足以估计整个 Full 的完成时间。

## 终态补记 — 2026-09-29

上文的 `RUNNING` 和“尚无结果”是带时间的启动历史。ACP 任务 `pt-dgpld36j` 随后到达 `SUCCEEDED`；持久 pod log 与 [Full 验证收据](</data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/verification.json>) 共同确认 `COMPLETE_OPERATIONAL`，实测 210.54 秒、产物 4,699,652,035 字节，原检查点未变。四组共 7,232 个事件、34,336 个数据对和 24 次预测器拟合全部完成。封存的 CONFIRM 主结果已合格，类型为 **`NON_SUPPORT`**，不再是“结果 Unknown”：DEV 选中的完整表征读出器 \(Q=-0.000138\)，95% 区间 \([-0.002768,0.002294]\)，注册支持门槛为 0.05。有限步确认因 DEV 作用分辨率门槛失败而 `NOT_RUN_BY_BRIDGE`；14 个结构读出均 `NOT_RUN_BY_GATE`。研究者解释和 Focus 转移仍为 `Unknown`。

结果请先读[中文摘要](summary_cn.md)，再读[完整中文证据记录](detailed_cn.md)；[理论审计交接索引](../reviews/natural_ntp_audit_handoff.md)列出各结果与证据优先级。本补记不改冻结 Protocol，也不授权下一次实验。
