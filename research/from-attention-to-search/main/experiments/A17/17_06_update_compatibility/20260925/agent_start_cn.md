# 新实验 agent 启动对话

> **这是供研究者复制、审阅后亲自发送的启动文本，不是本文件自行授予执行权限。**研究者发送下方正文时，才表达正文中的设计选择和条件式执行授权。当前 Anchor／Protocol 仍是待审草案。若只引用本文件而没有要求执行，agent 只能按实际消息范围行动。
> 建议新任务名：`0925-更新兼容性与参数隔离验证`。本文不自动创建任务，也不将旧实验执行授权移给新任务。

---

请基于下面的 Anchor 与 Protocol，完成新的“任务对更新兼容性与参数隔离”实验。先读来源、审核实现，再按已固定条件推进；不要重新发明实验框架，也不要为了得到预期结果改数据和判据。

## 研究问题与授权

我选择检验这条有边界的假设：**两组数据即使容易区分，也未必互相拖累；训练前更新方向更相反的任务对，可能在新样本上出现更强局部互损，并获得更大隔离收益。**先在八来源做资格及筛选，正式最多一对低兼容候选＋一对高兼容参照，不做28对训练。

我采用所列 Protocol 的提案设计、阈值、停止规则和预算作为本次执行契约；数据、身份及实现仍须实际验收。将此明确决定写入该 Protocol 的批准账本，不把实测资格尚未通过的区块虚写为通过。确认稳定 problem_key 为 `task_update_compatibility`；请按仓库规范建立这一独立问题的 Focus，并在主问题归属清楚后放置单份 Anchor/Protocol，更新这些启动链接。若项目层级确实存在科学归属歧义，请先完成不依赖它的核查，再指出最小分歧，不借用其它工作的编号。

**我授权的范围是：新工作目录中的实现、必要本地检查、Protocol 范围内的冻结模型筛选、目标设备小测、资格通过后的 Solo／正式训练、回滚及独立确认分析。**每个任务使用研究者 2026-09-25 指定的 `5090-4-spot` 与资源契约当前默认镜像及其 SM120 运行层；本实验不用四卡 H100 Reserved。独立任务允许在可用配额内并行提交，任务数不另设上限，但不能跳过筛选、Solo 等依赖门或重复提交同身份轨迹。原 32 GPU 小时累计提案须由研究者在发送本启动文本时明确保留或修订；提交数不限不自动取消该预算。工程／数据／可学性门通过且仍在批准范围内可继续，不逐步重复索取同一许可。若数据不合格、没有注册的任务对对照、单任务学不动或预计超批准上限，按规则停并报告，不自行扩大范围。

我没有授权提交Git、推送、发布、外部同步、改旧实验或打开旧M2D2确认集；也没有要求从头训练主干或学习SAE／Router。

## 必须先读的材料

1. `/data/250010109/Research_System/AGENTS.md`
2. `/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_06_update_compatibility/17_06_update_compatibility_anchor_cn.md`
3. `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_06_update_compatibility/20260925/protocol.md`
4. `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/shared_updates/20260924/docs/analysis/dev_rollback_reading_cn.md`
5. `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_05_shared_parameter_interference/20260924/protocol.md` 的 §18（仅识别旧已运行范围，不继承其权限）。
6. `/data/250010109/Research_System/docs/training_reuse_index.md`、`docs/training_observability_contract.md`、`docs/execution_envelope.md`。

先用 `research-reasoning-auditor` 检查“筛选不等于验证”和代理边界，再按 `problem-anchor-writer`、`experiment-card-writer` 检查同一份设计／契约的执行资格；远程工作使用 `remote-experiment-workflow` 和 `sco-control`。只加载实际任务所需参考。

旧结果已经完成18条训练和三套早期回滚；两组各自可学，D8未胜S16，早期总体为互惠。它目前是DEV／诊断证据，不能写成正式阴性确认，不能说两组分布相同或“数据不适合所以失败”。本任务不补跑或重解释旧实验。

## 复用资产：先读源码再适配

- `/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/scripts/smoke.py`：fresh-S7精确21B的加载与冻结核验。
- 同目录 `lora.py`：固定外部分组的增量参数化。核验并显式实现共享r16前八行与r8嵌套初始化，不能仅凭同seed假定相同；新增D16两个独立r16分支，共131,072可训练参数，每分支复制S16的A16初值并保持独立Adam状态。
- 同目录 `train_formal.py`：训练、状态保存和观测框架；原DATA／513-token窗口／每条512目标／1024步等假设全部按新契约改写。
- 同目录 `rollback_formal.py`：保存／恢复、零新梯度动量分支、半步对照；改为实际答案掩码、目标计数及注册早晚两状态。
- `/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/data.py`：八来源字段映射、原题身份与答案位置经验；不复制旧截断方式、旧缓存或28层模型。
- 同旧后训练目录 `runs/full-20260908T111248Z/data/audit.json` 和 `generation_records.pt`：来源版本／题族与历史使用核查。

所有旧路径只读，新实现放 `/data/250010109/MoE_Router/experiments/20260925_task_update_compatibility/`。先检查是否已有同身份任务或结果；如果有就核对并恢复原任务，不能再次提交。raw输出／权重不放研究仓库。不得自动调用子agent；本启动文本没有要求并行agent工作。

## 按此顺序推进

1. **核身份和边界。**读取fresh-S7而非重加权S7；核state哈希、实际配置、tokenizer与最后下投影。将本次批准、协议版本和科学正文哈希写入账本。确认旧结果保持不动。
2. **核数据与掩码。**恢复原题和答案，按题族去重，分离SCREEN／TRAIN／DEV／DIAG／CONFIRM。明确历史使用边界，拒绝标签歧义与整题被截断；按真实答案目标计算库存，不用样本数或输入长度替代。
3. **按注册规则筛选。**筛选模型读数前冻结D/C定义、门槛和选对算法。D只表示来源可分，C是虚拟全秩增量梯度的代理。没有合格的两对组合就交付完整筛选结果并停止，不强行选MMLU–MBPP或改门槛。
4. **验证新训练器。**目标设备小测答案位置、首末目标、全局分母、绑定退化、初始化、冻结、TensorBoard、独立进程恢复以及回滚。任何工程失败先修复并留痕；旧Smoke不能替代新目标掩码资格。七条件均小测，并验证D16参数量、状态隔离与绑定后退化为S16；重新估算包含D16的运行开销，32 GPU小时上限不变。
5. **先Solo后混学。**只有参与来源按Protocol都可学，才执行两对五个共享／隔离条件（S16、S8、D8、R8、D16）；连同每对两个 Solo，共最多42条逻辑轨迹，允许按Protocol复用完全同身份的Solo。使用同一冻结目标流，按真实答案目标计数，无重复epoch。保存预定状态，不看曲线挑最冲突节点。
6. **冻结分析再解封。**完成全部轨迹与诊断收据后冻结分析代码，按Protocol一次解封新CONFIRM。正确处理跨对共享来源的统计相关，不把筛选数据混进确认。
7. **按结果分型交付。**分别报告Γ、P−自身隔离收益、混合分组对照、主要早期互损／参照差和晚期边界；按§11.4另报D16容量诊断Q/E。D16胜S16不能排除总容量翻倍的解释，也不能挽救固定预算Γ的失败。功能正而机制不支持要分开说，不用漂亮的某一图补足缺失环节。

若科研设置需改，先列影响和已见数据，按追加变更规则处理；不要静默覆盖注册正文。常规工程修复可在不改变科学契约的前提下继续，并记录差异。

## 完成与汇报

交付可追溯的来源／选对／训练／分析清单，及与实际证据一致的 `summary.md`、`summary_cn.md`、`detailed.md`。机械判定可以按注册规则给出；最终机制解释、Focus判断和下一科学决策由我确认。不得因没出现预期效果而写“实验失败”或继续换数据。

若是长任务，先确认首个资格和进度门，报告作业ID、输出路径和证据化ETA，随后保持远程任务运行；无需长期占住对话轮询。后续检查同一任务，不重提。遇停止规则则报告精确状态、已有可用证据和最小缺口；不要把范围缩减后仍标为完整验证。

给我的回复先链接结果阅读入口，再用简短中文说：假设哪一环获得支持、哪一环不支持／未知，以及当前不能声称什么。
