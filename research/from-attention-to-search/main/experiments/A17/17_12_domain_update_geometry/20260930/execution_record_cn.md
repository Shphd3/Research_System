# 执行记录：domain_update_geometry

[Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_12_domain_update_geometry/17_12_domain_update_geometry_anchor_cn.md) · [Protocol](protocol_cn.md) · [English](execution_record.md)

## 2026-09-29T19:38:37Z — 已授权分阶段任务提交

提交状态：**SUBMITTED / STARTING；数值Smoke与科学结果NOT RUN**。任务`pt-t33awf9u`，名称`domain-geometry-analysis-0929-1938`。研究者明确授权完成所认可的领域共同/特殊分析及必要四卡H100 Reserved实验，不需新一轮批准。先完成文档，再实现检查后提交；同allocation内必须Smoke通过后才能全量采集，不是免Smoke。

已完成独立Focus、双语八节Anchor和十八节Protocol；本地链接、数学源码检查通过，不冒称渲染验证。数据预检核对1024条、每类别数量及原面板哈希；无跨split精确重复或5-token shingle Jaccard≥0.80近重复，论文ID仍缺。13项本地合同测试通过：原型评分、均值分解、Gram/聚合/投影恒等式、秩、激活幅度/零值、持续性边界及失败处理；Python编译通过。这些不构成自然语言结果。

资源已由提交模板解析、平台description核对：`h100-4-reserved`、ACP、share-space/share-cluster、`n6ls.iu.i40.4`、单节点4×H10080GB、RESERVED/NORMAL；镜像键`shphd-lite-0911`，展开URL为`registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423`；挂载`01995892-d478-76d8-aec7-13fd8284477e:/data`。GPU实际运行资格待测；retry0。训练/TensorBoard训练合同NOT_APPLICABLE，LM和SAE更新数0，使用测量计数/收据。

实际入口为仓库`templates/execution/acp_submit_template.sh`，已先dry run；DRY_RUN=0、ALLOW_SUBMIT=1、PROTOCOL_APPROVED=1反映已有用户授权。该`*-analysis`的run.py内部强制Smoke护栏，未伪造全量前Smoke PASS。完整tuple和payload由[英文执行证书](execution_record.md)及[提交收据](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/runs/20260929T193805Z/submit-domain-geometry-analysis-0929-1938-20260929T193835Z.json)持有。

执行根：[/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry)。[数据预检](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/data/data_manifest.json)、[本地测试](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/local_test_receipt.json)、[run root](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/runs/20260929T193805Z)。runtime复用已有offline依赖。持久pod日志在run的`pod`，运行注册/测量/分析将写`result`，预算24GPU小时/6小时/50GiB，无自动资源替换或重复full。

监控责任：Codex、本对话`01a0ed8f-85e1-7153-a531-af2fbf8288ee`；仅有界启动/即时失败核对，无自动化监控任务。当前无新实证结论；旧冻结裁决保持，后续运行事实追加，工程状态与科学裁决分开。

## 2026-09-29T19:57:08Z — 全量及结果审计完成

平台最终SUCCEEDED（update_time 19:46:35.241512Z）；runner COMPLETE_OPERATIONAL，耗时230.05秒、产物18627473471 bytes，1024记录/16384目标/261120激活位置；LM/SAE更新0，checkpoint前后hash一致。四个Smoke worker均实际NVIDIA H10080GB；没有重试或剔除。来源/数值护栏和所有必需阶段通过。

[Summary](summary_cn.md)和[Detailed](detailed_cn.md)持有结果；主程序NON_SUPPORT原值保持，人类科学判断Unknown。结果审计发现高维原型重采样偏差，明确限定percentile区间资格；九图已检查，原Q图的端点展示问题在独立审计目录修正，原图和原指标未改。补充只读描述汇总、复制小证据/图并建立来源hash；没有新模型拟合或重新采集。

[最终核验](evidence/verification.json)、[统计审计](evidence/review.json)、[平台状态](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/reviews/20260929_result_audit/platform_status.json)。本轮授权工作完成，不开启额外监控或下一实验；冻结设计正文及旧裁决保持。

## 2026-09-29T20:16:28Z — 用户请求的推理审计与终版文本

依据research-reasoning-auditor及experiment-card-writer完成R2结果文本。双语Summary/Detailed修正原型效果与结构存在性、bootstrap证据资格、两种投影秩、能量与相容性、领域平均与单记录能力、目标条件化的研究对象等12项推断。仅从既有Gram核对MSE差=B_F−2H_FR，无新实验、统计检验重跑或阈值修订。

[修订审计](evidence/reasoning_audit_final.json)保存修订前文件hash与算术核对；前版文档留于执行根reviews/20260929_reasoning_audit_final/before。原始结果、注册代码及Anchor/Protocol保持；R2是结果文本终版，不产生研究者科学确认或问题关闭。当前阅读入口为[Summary](summary_cn.md)与[Detailed](detailed_cn.md)。

## 2026-09-29T20:30:53Z — 补录明确批准，完成全部任务验收

研究者明确要求完成批准、执行分析并监督全部任务结束，长耗时任务拉长轮询。本次批准记录对应当前domain_update_geometry Protocol及R2终版交付，属于执行与交付授权，不代替总体科学结论或问题关闭。该Protocol唯一allocation此前已经成功，因此本轮核验终态与产物，没有重复提交。

实时平台查询确认pt-t33awf9u为SUCCEEDED。四个采集worker及全部分析收据完成：1,024记录、16,384目标、261,120激活位置；30,000个SAE atoms、300,000行激活统计和240,000行atom梯度统计。15项必需产物齐全。核对20个注册源hash、本次追加前12份R2文档hash、6个关键原始结果hash、10份精选证据和checkpoint hash；谱阅读表按已注明的行子集核对，未误作原表字节副本。无缺失阶段或失败分片。

[最终验收收据](evidence/completion_receipt.json)持有逐项检查，[本轮平台状态](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/reviews/20260929_approval_completion/platform_status.json)持有终态。当前授权任务均已结束，无需等待或继续轮询。本轮没有新allocation、采集、统计重跑或参数更新；冻结Protocol和实测结果保持，R2的总体推断资格限制仍有效。

Summary提出的“目标条件关系”是独立的后续比较，不是该Protocol尚未完成的阶段，本收据不自动注册或执行它。本次用户指令未给出科学解释，研究者科学判断仍Unknown。
