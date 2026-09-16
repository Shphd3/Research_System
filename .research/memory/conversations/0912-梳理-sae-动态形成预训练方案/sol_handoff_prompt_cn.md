# 给 Sol 的续接 prompt

以下文本由研究者转发给 Sol 后，作为接收任务的工程工作指令。它不是正式训练批准，也不替代项目记录。

---

请接手 Dense LM + 最后层 SAE 的代码审计与后续工程修复。先读取资料和实际源码，再完成最小修复及本地 CPU 测试，不要停在审计建议。

本轮允许：读取、代码审计、局部工程修复、小规模 CPU 测试、更新工作记录和你自己的 memory/continuation。
本轮不允许：提交任何 GPU 任务、正式预训练、大规模实验、改变科学假设或语义标签、增加复杂 loss/router/MoE/额外模块、commit/push/外部同步。之前的一次四卡 Smoke 批准不延续为新任务的 GPU 批准。

工作根目录：
- 研究记录：`/data/250010109/Research_System`
- 执行代码：`/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining`
- 源任务记录：`/data/250010109/Research_System/.research/memory/conversations/0912-梳理-sae-动态形成预训练方案`

先按顺序读：
1. Research_System 的 `AGENTS.md`、`docs/training_reuse_index.md`，以及执行路径上存在的 AGENTS.md。
2. 源任务的 `continuation.md` 和完整 `memory.md`。记忆只提供工作上下文，不提供科学判断或新批准。
3. `/data/250010109/Research_System/daily_research_reports/0912/docs/dense_sae_30k_smoke/` 下的 `execution_scope.md`、`execution_record.md`、`code_handoff.md`。
4. 执行目录的 `README.md`、`docs/reuse_sources.json`、`configs/smoke_4h100_sae30k.json`、`handoff/baseline_manifest.json`，然后阅读与你要修改的内容对应的真实源码和测试。先说明复用、适配、不复用的部分。

当前基线：随机初始化的 312,892,928 参数 Dense LM，隐藏维度 1024；SAE 字典宽度 30000、k=32，61,471,024 参数，合计 374,363,952。SAE 读取最后层 RMSNorm 后的 `h.detach()`，仅训练自己的重构分支；LM/SAE 参数组、计数归一化和梯度裁剪分开。模型不是预训练 Qwen 权重加载器。

工程证据：`runs/smoke_4h100_sae30k_fix_20260912080957/` 对应 `pt-ro6ijc54`，100 次逻辑更新，含一次额外恢复重放。以 smoke、terminal、artifact_verification 和平台记录核实结果，不依赖本 prompt 的概述。17 项本地测试和早先两进程 Gloo 检查已通过。首次任务 `pt-i9ohovsb` 在第一个更新前发生状态探针浮点索引越界，已改为整数索引；失败记录必须保留。

优先审计和处理六点（细节、代码位置及验收见 code_handoff.md）：
1. **独立进程恢复，最高优先级。** 外部 `--resume` 会重设初始 SAE/验证/面板；在重放边界及其之后恢复时，重放状态缺失；日志、物理更新次数和端到端计时不能完整描述原运行。还需统一恢复路径解析。保留真正的 step-zero 基准、精确数据游标和日志唯一性。
2. **梯度与优化器隔离。** 核查 detach、参数唯一归属、共享 embedding、独立裁剪，以及各卡/各微批不等样本数的全局归一化；匹配初始化和数据，比较 none/observer 的 LM 梯度和更新。
3. **数据与预测位置。** 只 shift 一次；保持固定数据顺序、rank 切分、因果位置和恢复后的下一批/SAE 掩码；不把源文件隔离当作文档去污染。
4. **检查点与异常退出。** 覆盖 model/optimizer/scheduler、各 rank RNG、独立 Generator、计数和游标、损坏/未完成 manifest、安全停止。现有 GPU probe 只抽查模型状态，不是完整优化器等价证明。
5. **分析接口。** 固定 sample_id/顺序/position/checkpoint；`raw_h` 是归一化前表示，`h` 是归一化后表示，`indices/values` 是稀疏激活。验证推理不会改变后续训练状态，明确跨时间使用哪个 h/SAE。16 条无标签面板不是语义基准。
6. **配置、边界和计时。** 100 步 Smoke 尚在 LM warmup；检查 LR 步号、未使用字段、更新计数和时间/存储上限。训练步骤吞吐不含前置取数，端到端包含 I/O；没有测量 no-SAE GPU 开销。不得靠删除 Smoke 上限来启动正式训练。

先修复可复现的独立进程恢复问题，再处理其余审计中发现的最小缺陷。使用同一训练契约，在 tiny CPU 数据上比较连续运行与停止、退出、新 Python 进程恢复；覆盖重放边界之前、当步和之后，比较完整模型/优化器/调度器、下一批/掩码、RNG/计数、原始面板身份和最终记录。不要只增加一个同进程 load_state_dict 测试，也不要修改 max_steps 来绕过契约不匹配。

执行目录没有 Git：先核对冻结快照和文件哈希，保留现有源码差异，不要覆盖解压或修改旧 run 结果。源码改变后的测试写到新目录，旧 GPU PASS 只证明旧版本。不要禁用源/config/拓扑校验来恢复修改前的检查点。

本地测试先在执行目录 `source scripts/runtime.sh`，使用 `CUDA_VISIBLE_DEVICES=''` 运行必要的 pytest / 两进程 CPU Gloo。该脚本复用已挂载依赖并设置 protobuf 兼容；不要往基础环境安装依赖。文件不可见时报告具体路径，不要猜测或重新生成旧证据。

最终交付：实际修改文件及职责；按优先级列出已确认缺陷、已修复项和仍待验证项；给出测试命令、退出状态和证据路径；更新工程记录。按 research-memory 规则读取你自己的任务名称，创建新的 memory，`Continues from` 指向源任务 memory；不要覆写源任务日志。接管时维护该工作流唯一 CURRENT continuation。

完成局部修复后停止，不提交 GPU。正式训练预算、长期调度/保存策略、语义分析标准以及任何新 GPU 验证，整理为等待研究者决定的事项。不要把 Smoke 通过或更宽 SAE 解释成语义结构形成的结论。
