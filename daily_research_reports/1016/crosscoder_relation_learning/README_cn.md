# 1016 · CrossCoder 关系分组到学习验证

全部计算已完成。共同出现组织获得有界统计支持，但当前关系分配没有转化为学习收益。局部更新及响应控制进一步缩小了原因；完整训练根因仍未识别，科学批准与问题关闭保持Unknown。

先读[一页中文摘要](summary_cn.md)，再读[完整中文报告](report_cn.md)及[Detailed](detailed_cn.md)。[English report](report.md)提供伴随版本。

- [执行Protocol](protocol_cn.md)及[英文版](protocol.md)：问题、竞争解释、精确控制、指标和边界。
- [连续reasoning audit](reasoning_audit_cn.md)：自我反驳和修复。
- [执行修订](execution_amendments_cn.md)：保留旧版和新增分析的身份。
- [原始Anchor](sources/02_ANCHOR_关系分组到学习验证.md)、[组会稿](sources/01_组会报告修订稿.md)、[执行要求](sources/03_PROMPT_交给现有Agent自主执行.txt)。

执行根：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z`。唯一四卡作业：`pt-szeffn72`。研究记录不授予科学关闭状态。

## 图与原始CSV

[五种主图](figures/)均有PNG/PDF/SVG；补图标为supplement。报告逐图解释，不依赖网页。

- [逐节点学习](evidence/analysis_outputs/learning_metrics.csv)、[配对终点与近似区间](evidence/analysis_outputs/paired_endpoints.csv)、[零适配器参考](evidence/analysis_outputs/zero_reference_changes.csv)。
- [局部更新原始数据](evidence/analysis_outputs/intervention_all_effects.csv)、[配对汇总](evidence/analysis_outputs/intervention_paired_effects.csv)、[响应反事实](evidence/analysis_outputs/response_decomposition_effects.csv)、[专家损害分解](evidence/analysis_outputs/expert_loss_changes.csv)。
- [186组完整对照](evidence/structure/full_group_controls.csv)、[B99修复版](evidence/structure/triple_counting_repair/null_results.json)、[首方向及均值控制](evidence/data/first_direction/)。

## 绘图与复现

[code/replot.py](code/replot.py)只读取随包小型CSV/JSON/选定NPZ，不需要GPU、模型或完整缓存。依赖Python、NumPy和Matplotlib；运行 `python code/replot.py --output-dir /tmp/crosscoder_replot`。[实际复现检查](replot_verification.json)保留验证结果。

下列地址均相对上面的执行根：

| 对象 | 地址／身份 |
| --- | --- |
| 冻结配置 |`config/formal_R1_8.json`；6120updates/1566720targets每run，3conditions×3seeds |
| 缓存 |`data_eval512/train.pt`、`eval.pt`；130712/523136positions |
| 正式状态 |`learning/seed_<seed>/<arm>/checkpoints/update_<step>.pt`；step0/510/1530/3060/4590/6120 |
| 实际清单 |`checkpoint_manifest.json`；54正式状态、9final，fresh字节哈希核验 |
| 训练日志／TensorBoard |`logs/train_<seed>_<arm>.log`；各run的`metrics.jsonl`、`stage_timings.jsonl`、`tensorboard/initial/` |
| 干预与响应控制 |`intervention/seed_<seed>/<arm>/`、`response_decomposition/seed_<seed>/<arm>/` |

四卡worker于UTC17:39:48退出，未新增额度。输入、缓存两个版本、正式状态和Smoke均已登记并严格检查；[访问与资源证据](provenance/)保留回执。存有优化器/RNG/顺序/计数状态，序列化下一步复现通过；外部进程恢复资格明确未检查。

[证据来源清单](evidence_origin_manifest.json)、[产物清单](artifact_manifest.json)及[变更清单](change_manifest.json)记录哈希和写入范围。选定NPZ仅为绘图/审计证据例外。原始文本、全激活缓存、矩阵、权重与日志不进入讨论包，地址保留上表。原strict样本NA与旧失败保留执行侧，不回写成通过。本任务未修改skills、训练base/CrossCoder、commit/push、外发或改变Focus科学状态。
