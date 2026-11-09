> 2026-10-12 A03：下文保留原8192维历史工程证据。当前32768维配置与H100试跑启动见[更新后的操作计划](validation_plan_cn.md)及执行侧 `runs/pilot_32768_20261012/execution_certificate.json`；不把历史结果改写为新配置的验证。

# 冻结 Qwen3 全层 CrossCoder：本地工程报告

[English](engineering_report.md) · [验证计划](validation_plan_cn.md) ·
[实现入口](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/README.md)

**本地实现检查通过；pilot 没有训练。测量质量未评估，科学问题没有得到回答。**
这是研究者所需工具的事实工程记录，不是科学 Summary，也不是正式运行授权。
来源于 2026-10-12 当前检查。

## 后续时长修改 A01

下文的一小时/4GPU 小时是最初提案的历史记录。研究者随后取消该限制；
当前草案为 12 小时/48GPU 小时。原曝光预算未变，没有提交或新增训练。
当前运行合同见[验证计划](validation_plan_cn.md)。

## Purpose：目的

检查冻结 Qwen3-0.6B Base 能否向指定全层 CrossCoder 提供正确配对的 block
输出，以及架构、损失、尺度、梯度、日志与精确恢复是否一致。此工具供以后
测量特征结构、出现频率和共同学习。工程检查通过不证明这些科学性质。

## Model：实际对象

当前模型路径为 `/data/share/Qwen3-0.6B-Base`，revision 为
`da87bfb608c14b7cf20ba1ce41287e8de496c0cd`。完整权重 SHA-256 为
`cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`。
已核对模型卡、配置、来源 metadata 和完整 hash；模型是 Base/Pretraining，
28 层、hidden1024。没有用 Instruct、添加 router、训练 Base、下载模型，
也没有另存 Base 副本。

CrossCoder 的独立参数为 encoder[28,1024,8192]、decoder[28,8192,1024]、
共享偏置[8192]和 decoder 偏置[28,1024]，共 469798912。FP32 损失对位置取
均值，对层和隐藏维求和。L1 使用各层 decoder 向量范数之和。TRAIN-only
每坐标 RMS=1 采用未中心化固定尺度，可逆。初始化适配作者固定 commit
`d1fd6f3fea41fc1123699cc09f4cdad47ca35160` 的 L1 norm0.05；初值转置复制，
参数存储不绑定。

DCLM 视图的 TRAIN 有 2000000 个唯一配对位置、1935 个文档；VAL 有 32768 个
位置、41 个文档。扫描 20000 条来源记录，在选择之前处理 22669105 个原文
token；排除 12 条非法文本，发现 3 条精确重复和 2 条近重复链接。一个文档的
全部片段属于同一划分，不产生 padding。来源 fastText 标签标为英语，不等于
独立语言审计。整个原始文件有 59812 条记录。上游精确 revision 为 Unknown，
完整本地 SHA256 固定实际 payload。历史暴露和有限近重复检索边界仍保留。

## Hypothesis：检查预期

正确实现应与手算一致，在相同位置采集全部 block 各一次，保持 Base 权重不变，
能逆变换尺度，使梯度只流入 CrossCoder，并在恢复 RNG 与数据 cursor 后复现
下一次优化器更新。hook 索引、配对、reduction、权重绑定或校准污染都是可信
工程失败解释。这些检查只区分工程错误。

## Conclusion：已验证事实与边界

| 检查 | 实际证据与范围 |
| --- | --- |
| 单元/融合/运行合同 |42 项 CPU 测试通过，耗时 29.07 秒；包含真实 tiny-Qwen 的 28 层融合与两 rank CPU DDP |
| 完整指定架构 |实际分配 469798912 参数；2 个位置上的完整 FP32 CPU 前向/反向有限，没有优化器更新 |
| 真实预训练 Base hook |28 个 hook 各调用一次；前 27 层精确对应 hidden_states，最后一层精确对应最终 norm 输入 |
| Base 不变 |FP32 内存状态前后 hash 一致，BF16 状态也一致；全部参数冻结，无 Base 梯度 |
| 无操作 next-token 对照 |真实 Base 的 8-token CPU 面板，全层替回原激活，变化为 0.0 nats/有效预测 |
| 损失/尺度/配对 |平方误差与 sum-of-norms 手算、mask 配对、独立权重和逆归一化均通过 |
| 恢复 |小张量 FP32 Adam/RNG/归一化/文档内 cursor 恢复后，下一次参数和 moments 逐位一致 |
| 并行目标 |两 rank gloo/no_sync 累积后的梯度、loss、Adam 更新与串行配对 batch 一致；4-H100 路径未运行 |
| 来源门槛 |当前模型/tokenizer/原始数据 strict 检查、派生数据与配置绑定、23 文件源码冻结和提交 dry-run 均通过 |

真实 Base 与完整 CrossCoder 的本地检查耗时 29.81 秒。8-token CPU 面板中，
BF16 相对 FP32 的各层激活 RMS 差异范围为 0.001361–0.057669。这是实测差异，
不是目标 GPU 数值等价结论，也没有被当作合格阈值。真实 GPU 精度验证仍待
获批 pilot。

没有完整规模的优化器更新、已训练 checkpoint、GPU pilot、集群 job ID、训练
测量曲线或已训练重构的 next-token 结果。真实训练曝光为 0。随机初态 loss
只检查有限性，不作为测量质量。研究者尚未判断操作点，也未回答科学问题。

## Analysis：证据、资源与下一步

实现适配了已审阅的 CrossCoder 架构/初始化、已有自然文档数据流程以及
checkpoint、DDP 和日志模式。tokenizer 指纹模块从干净训练框架原样复用。
没有继承旧 MoE/TopK 架构、缺文档边界的 bin、随机激活行划分或不相容的
损失 reduction。代码、token、原始日志与运行证据都留在执行侧。

证据根路径为 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/`。
主要记录是 `docs/local_qualification_20261012.json`、`docs/tests_20261012.txt`、
`docs/input_inventory.json`、`docs/reference_audit.json`、当前资产访问检查、
`docs/data_release.json`、`docs/source_manifest.json`、
`docs/preflight_with_data.json` 和 `docs/submission_dry_run.txt`。
数据由 `data/pilot_v1/data_manifest.json` 管理，事件文件有 hash、文档/位置/
分片 ID。本任务没有覆盖已有研究记录、sealed 划分或资产 catalog。默认导航
检查发现一项既有未跟踪文献路径；`--working-tree` 检查为 0 问题，并保留
“尚未跟踪”的事实边界。

数据文件共 29770578 bytes；token 临时文件峰值 102958014 bytes。没有保存
全量激活。FP32 参数、梯度、Adam 状态显存下界为 7.00GiB/rank，不含 Base、
DDP 与工作区。完整恢复状态约 5.25GiB；checkpoint 总 payload 上限 14GB。
目标 GPU 显存峰值、激活生成吞吐、训练吞吐、完成 ETA 与货币成本都为
Unknown。CPU 检查耗时不能替代 GPU ETA。

pilot 拟为 488 次更新、1998848 次曝光，资源为 4 个完整 H100 Reserved，
到一小时预算停止，预留收尾与保存时间。拟定成本上限 4GPU 小时，一小时包括至多 60 秒外层终止宽限；必须记录实际占用。当前 40GB MIG 与默认资源规范
不证明真实容量或预约。可审阅请求 `docs/authorization_request_pilot.json`
绑定源码、配置、数据与上限，`researcher_approved=false`，不会启动训练。
正式计划为 24414 次更新、99999744 次曝光，仍需 pilot 质量和资源/预算确认，
不会自动开始；当前 2M TRAIN 池会被重复访问。

替换评估有 28 个单层条件与同时全层条件，并保留无操作对照。固定原始来源的
绝对 residual 覆盖使最高被替换层决定结果；全层条件等价于最后一层条件，
不能作为独立累积误差证据。特征频率指 token 出现比例，失活只指固定 32768
位置窗口内零命中。41 个 VAL 文档和英语来源不建立广泛多语言测量质量。

`AI 建议`：审阅冻结配置、数据与拟定 4GPU 小时上限后，批准这个具体 pilot。
此处需批准的原因是用户明确要求“任何新集群提交……先取得相应批准”。
批准不包含正式训练、自动 L1 校准或重提。真实训练保存后需完成资产生命周期；
当前没有已训练保存可注册。工程实现通过本地检查；测量质量为
`NOT_EVALUATED`；科学答案为 `Unknown`。
