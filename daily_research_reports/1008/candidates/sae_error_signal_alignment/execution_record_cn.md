# H2 候选诊断：执行记录

**最终任务 `pt-c33caya0` 已 SUCCEEDED，两模型全部测量、注册分析和三组正式图表完成。** 实际四卡均为 NVIDIA H100 80GB HBM3。研究者科学判断仍为 Unknown；主统计分支与竞争对照见[候选结果](summary_cn.md)。

Owner：[Protocol](protocol_cn.md)。原始设计和阈值保持；两次数值实现修复见[Amendment 01](amendment_01_cn.md)、[Amendment 02](amendment_02_cn.md)。原22项、v2的26项冻源均保存逐项hash快照；最终30项见[v3登记](evidence/registration_v3.json)。

| 任务 | 提交 UTC | 终态 UTC | 执行状态与测量 |
|---|---|---|---|
| `pt-hsy9grzm` | 08:32:35 | 08:40:51 | FAILED；S7完成，Qwen hidden重放检查失败 |
| `pt-ahl6i4wr` | 08:49:02 | 08:56:13 | FAILED；S7完成，Qwen单目标梯度比较失败 |
| `pt-c33caya0` | 09:02:41 | 09:06:00 | SUCCEEDED；两模型16,384位置全部完成 |

三个任务依次执行，前一任务终态后才提交修正任务。[首次收据](evidence/execution_receipt.json)、[v2收据](evidence/execution_receipt_v2.json)、[最终收据](evidence/execution_receipt_v3.json)保留实际来源。最终runtime从09:03:30到09:05:37 UTC，共127.18秒；包括注册分析、图表和资产复核。按各任务提交至终态全时长乘四卡计算，保守合计约1.25 GPU小时，低于原16 GPU小时计划上限。

| 资源字段 | 已核对值 |
|---|---|
| profile / surface | `h100-4-reserved` / ACP |
| workspace / AEC2 | `share-space` / `share-cluster` |
| worker spec / 节点 / 进程 | `n6ls.iu.i40.4` / 1 / 4 |
| quota / priority | reserved / normal |
| 请求 / 实际 GPU | 四卡H100 80GB SXM5 / 四卡NVIDIA H100 80GB HBM3 |
| image key | `shphd-lite-0911` |
| image URL | `registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423` |
| mount | `01995892-d478-76d8-aec7-13fd8284477e:/data` |
| 实际 runtime | torch `2.3.0a0+6ddf5cf85e.nv24.04` / CUDA 12.4 |
| 数值资格 | 8个worker/model收据均PASS，未放宽任何阈值 |
| 更新与冻结 | LM/SAE均0更新；参数版本、原始资产文件身份未变 |

每模型1024条文本×16位置=16,384事件；fit/readout各512条，readout 8,192事件全部有效。Qwen各原生梯度/参数外积/其他位置/重放误差均为0；S7原生δ相对误差最大5.05e-6，CE重放最大绝对误差1.79e-5，均低于原阈值。重复测量完全一致。12项CPU检查通过；上述GPU收据独立核对真实实现。

提交经 `templates/execution/acp_submit_template.sh` 与既有 `sco_acp_compat.sh`，以 `DRY_RUN=0`、`ALLOW_SUBMIT=1`、`PROTOCOL_APPROVED=1` 兑现研究者直接执行授权，不代表科学审批；没有虚构外部Smoke通过。`run.sh` 复用已检查S7 runtime与挂载HF4.53.3依赖。

最终精确入口：

```bash
timeout --signal=TERM --kill-after=30s 12600s env H2_CONFIG_PATH=/data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment/configs/h2_v3.json bash /data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment/scripts/run.sh /data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment/runs/diagnostic_v3_20261008T090146Z
```

执行根目录：`/data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment`；最终run root：`/data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment/runs/diagnostic_v3_20261008T090146Z`。持久日志在 `logs/worker_*.log`、`logs/analysis_*.log` 和 `pod/`。原始数组在 `collection/shard_*/{s7,qwen}/features.npz`；完整 event/record/domain表和统计在 `analysis/{s7,qwen}/`；正式图表在 `analysis/figures/`。

[完成收据](evidence/completion.json)、[preflight](evidence/preflight.json)、8份测量收据、两模型小统计/领域表、PNG/SVG及[结果来源清单](evidence/result_manifest.json)已复制到候选目录。原始数组、模型、checkpoint、依赖和完整日志仍属执行仓库。训练比较contract与TensorBoard为NOT_APPLICABLE；不训练Router、LoRA、Expert或SAE。

本轮monitor owner为当前线程 `01a10a2a-b783-7752-9149-ed2ffd48a40a/root`。最终平台终态、首批进展和即时错误均已核验，不再轮询或追加提交。两次失败未作为科学负结果，也未用来调整数据、阈值或主指标。 registered `SUPPORT_BOUNDED_H2` 仅表示弱平均关联；原生近邻更好、不同真实下一词优势转负的边界必须同时报告。没有提交、推送或发布。
