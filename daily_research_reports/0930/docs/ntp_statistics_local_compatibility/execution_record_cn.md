# 执行记录：自然语言统计与局部更新结构

所属[Protocol](protocol_cn.md)。研究者2026-09-30授权本轮实现、Smoke及通过门槛后的完整Full。**本轮Full已成功结束**；科学判断Unknown；模型／SAE更新0。

## 资源与运行环境

默认h100-4-reserved；ACP share-space／share-cluster；一台n6ls.iu.i40.4、4工作进程／4H10080GB；Reserved／Normal。镜像shphd-lite-0911，展开为registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423。AFS01995892-d478-76d8-aec7-13fd8284477e挂载/data；GPU真实使用。运行激活脚本[runtime.sh](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runtime.sh)复用审计过的模型依赖层。训练对比契约NOT_APPLICABLE。

## 尝试、资格与真实状态

| 阶段 | 作业 | run目录 | 事实 | 资格 |
| --- | --- | --- | --- | --- |
| 严格Smoke1 | pt-wd184bbc | smoke_initial | 梯度分项精度失败 | 失败门槛记录 |
| 严格Smoke2 | pt-gqxil5g2 | smoke_precision | 原生VJP累加精度失败 | 失败门槛记录 |
| 定位诊断 | pt-xm7fqnf3 | smoke_diagnostic | 断言临时改为诊断，运行器虽写PASS | DEBUG_ONLY，不能放行 |
| 严格资格Smoke | pt-k68kogs3 | smoke_qualified | 16记录／256目标、48方向的局部KL与状态冻结通过 | PASS；保持原门槛 |
| Full | pt-z162gb1w | full_initial | 2048记录／32768测量目标、4096功能上下文／32768VJP及登记分析完成 | SUCCEEDED；主裁决INSUFFICIENT |

严格Smoke分项重组最大相对误差3.3502e−7，低于2e−5原门槛；正式Smoke34.9秒、保守Full估计927.2秒。28类估计器校准各5000重复通过；五个独立非线性尾部CPU检查验证原生前向逐位相等和反传精度，主估计器测试含共同目标抵消与整数领域ID。Full程序223.0秒，作业05:32:22UTC开始／05:36:14UTC成功结束；严格限制Full6600秒，重试与Full均在既有2小时／8GPU小时预算内。

## 精确入口与范围

通过[仓库ACP提交模板](/data/250010109/Research_System/templates/execution/acp_submit_template.sh)提交，底层为审计的sco_acp_compat.sh。DRY_RUN=0、ALLOW_SUBMIT=1、PROTOCOL_APPROVED=1；Full另SMOKE_GATE_PASSED=1。原始运行命令：

```bash
source runtime.sh
python scripts/stage.py --mode full --out runs/full_initial --smoke-root runs/smoke_qualified
```

[代码](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/scripts)；[数据清单](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/data/data_manifest.json)；[校准](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/data/calibration.json)；[资格Smoke回执](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/smoke_qualified/smoke_receipt.json)；[Full登记](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/registration.json)；[完成回执](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/completion_receipt.json)；[分析审计](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/analysis/postrun_audit.json)；[提交回执](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/acp_receipts)；[持久日志](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/acp_receipts/pod)。Full复制拥有权Protocol／Anchor及不可变源码快照，保留原始哈希；当前实现后续修复领域名称输出，并改进图例布局，不改变主值／样本／阈值。缺覆盖分支保留不足，不追加样本。

## 监测与完成核对

监测所有者为当前Codex对话主agent。已核对真实运行、分片／目标身份、F工具冻结先于R、全部登记分析、参数冻结、完整文件和终止状态。仅作业成功不等于科学支持；本轮主区间跨门槛，科学解释Unknown。历史N8语料曝光与近似文档独立性限制陈述范围，不能称全新未见语料确认。无训练、router、有限W干预、长期共享／分开比较；TensorBoard不适用。

先读[Summary](summary_cn.md)，完整来源／失败／修订见[Detailed](detailed_cn.md)。
