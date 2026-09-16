# 转交执行 AI 的 prompt

任务根 `/data/250010109/Research_System`。先读AGENTS.md、`docs/training_reuse_index.md`、`docs/training_observability_contract.md`，以及 `daily_research_reports/0914/sae_research_decision_materials/02_next_step_plan_cn.md` 和决策AI形成的最终决策卡/Protocol及研究者批准范围。**本prompt自身不包含GPU执行批准**；若已收到覆盖对应阶段的明确批准，验收通过即继续该阶段，不重复申请相同权限。没有批准时完成可审阅准备，不提交训练。

复用 `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining` 的README、源码身份、真实resolved_config、数据/DDP/AdamW/checkpoint/运行时，不从0912平铺草稿重写。代码只在新隔离目录，旧SAE和baseline训练、日志及checkpoint保持原状。readout可参考 `20260914_semantic_feature_reuse_analysis`，但锁定新实验自己的model导出接口。

若决策卡采用当前建议，做两份相同随机初始化的串联SAE：C辅助输入detach，T输入live；主路径一样，目标/分母均detach，λ相同。30k、k32、8层1024维，其余配置按冻结卡。先打通配置对λ的校验、engine传参和weighted日志，测试λ=0/.1/1梯度比例；不要机械删所有detach，不引入AuxK/router/MoE。

先交付源文件复用表与最小diff，然后完成小CPU梯度与恢复验收。必须验证同权重前向一致、C辅助不进主干而T进、两组LM梯度都正常；按模块图识别上游，注意输入输出共享权重；LM/SAE独立裁剪、全局有效目标/采样分母、数据和采样RNG逐步配对、恢复下一步重放、训练/离线post-norm2取点一致。失败保留回执，修复后复测相应项。

数据先冻结小型自然领域fit/dev面板；旧360句只做debug，勿当新确认。源码、运行配置、输入数据、导出位置都写哈希。自然语料抽样活动计数与固定panel覆盖分开；未满窗口不要判死。完整字典统计与精选图分开。

GPU执行前从 `docs/execution_envelope.md` 解析当前四H100 profile/image/入口，不复制旧jobID或假设卡空闲。只运行已批准的100步Smoke与/或分阶段开发预算；拟议1024/4096步均是每组累计上限，阶段可续训但不能换λ/日程后拼成同一实验。旧50B launcher不能指向新目录充当小试。三种子正式预算另外审定。

输出：`audit/source_identity.json`、配置diff、`checks/gradient_contract.json`、`checks/resume_replay.json`、训练/SAE raw与weighted标量及TensorBoard、双计数、恢复点、`metrics/representation.csv`、`metrics/sae_quality.csv`、固定面板manifest、终止/完成回执。原始h读出是主结果；LM代价、SAE重构/活跃/选择性是分开的解释。报告实际tokens与端到端吞吐、显存、额外物理重放步。仅工程PASS不能写成科学假设成立。

启动只监督到健康/首个有界进度门，除非我另要持续监控；交付jobID、真实进度、实测ETA、结果位置后结束轮询，让作业继续。不要因监督结束重提任务。完成授权阶段后按自己task身份写memory/continuation；对机制和下一预算等待我的判断。
