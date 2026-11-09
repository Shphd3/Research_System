# 0915 三模型表征审计：完整远程提交一次性审批包

> **2026-09-16 最新覆盖：**`h100-2-spot` 作业 `pt-20q3i7pd` 在 S2 因 AFS advisory lock 失败，未完成任何资格单元。研究者现已明确授权单节点 `h100-4-reserved` 立即全量重提；四个独立 worker 按 5/5/4/4 分配。现行任务仍是完整 S2--S6，不以 ETA 缩减范围。

> **中间状态（已被上一条覆盖）：**研究者曾选择一个单节点 `5090-4-spot`；该尝试未获主机即被停止。现行合同见 [A15_17_E01 Protocol](../../../../experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E01_three_model_sae_representation_audit/protocol.md)。

日期：2026-09-15。处理者：Codex。状态：`AWAITING_RESEARCHER_BUNDLE_APPROVAL`。

本文只汇总会改变科学归属、分析范围、结论边界、资源、成本、失败行为或提交后监督方式的裁定。研究者可一次批准整包；在此之前不创建正式执行授权、不提交 ACP 任务。

## 1. 当前判断与状态

| 层级 | 当前状态 | 判断 |
|---|---|---|
| 科学范围 | 已有详细日期计划；无本实验确认 Focus/Anchor/Protocol | 计划不能冒充正式问题归属或执行批准 |
| S0 来源审计 | `PASS` | 三模型、六共同点、P/N、18任务和候选旧缓存身份没有阻断矛盾 |
| S1 数学契约 | `PASS` | 9项 CPU 测试再次通过 |
| S2 资格入口 | `PARTIAL_IMPLEMENTATION` | 严格加载/hook/一批梯度框架存在，但计时、5B桥接、显存、probe计时不完整 |
| S3--S6 | `NOT_IMPLEMENTED_AS_ONE_DRIVER` | 采集、A/B分析、统计、绘图、恢复和汇总尚未形成可提交闭环 |
| 资源 | `h100-2-spot` 已在 execution envelope 为本范围登记 | 当前队列证据不支持改成 5090；H100 更适合内存和 CPU 尾部 |
| 远程 | `NOT SUBMITTED` | `job_submitted=false`；没有远程模型前向、反向或结果 |

**AI 判断：现在不能直接提交。** 一次性批准后，应先在同一冻结范围内补齐实现、创建并确认正式 Focus/Anchor/Protocol、通过本地回归和最终 dry-run，然后无需再次询问即可提交完整 S2→S6 单节点任务。任何本地门失败、resolved tuple 漂移或新 ETA 超过获批门槛都必须停下，不能用本审批绕过。

## 2. 请一次审核的十项裁定

### A1. 正式问题归属与唯一下一决策

**AI 建议批准：**把本审计激活为 A15 的独立子问题，避免借用 teacher、hierarchy 或 flat-router 的既有 Anchor。

- `problem_key`: `three_model_sae_representation_audit`
- Focus: `Projects/from-attention-to-search/main/focus/legacy/0915_focus_three_model_sae_representation_audit.md`
- Anchor: `Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_12_three_model_sae_representation_audit_anchor.md`
- Experiment: `Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E22_three_model_sae_representation_audit/`
- 核心问题：在相同累计训练 token 下，Dense、detach-SAE 和 live+AuxK-SAE 的最后层领域信息线性可读性、实际 MLP 输入和稀疏接口是否呈现有界差异；这些差异是否依赖均值/第一高能方向？
- 唯一下一决策：**是否有一个当前 SAE 配置值得进入单独设计、单独批准的因果功能干预；若没有稳定表征证据，则停止把本配置作为已成立机制依据。**

批准 A1 只激活本 checkpoint 审计问题，不批准新训练、Router/LoRA、模型修改或后续因果实验。

### A2. 冻结输入和对照

**AI 建议原样批准：**

- 模型：M0 Dense；M1 最后层串联 SAE、重构输入 detach、无 AuxK；M2 live 重构输入、SAE-only AuxK。
- checkpoint：每模型 0/0.5/1/3/5/10B，共 18 个。
- 数据：冻结 P 360 句；学术 M2D2 N 1200 行，仅作开发复核；两者不合并标签或冒充未触碰确认集。
- 表征：最后块 `norm2` 后 raw-\(h\)；实际 MLP 输入 \(\hat h\)；M1/M2 的 SAE Top-k 稀疏码。
- M2−M1 只解释为 live+AuxK 组合差，不解释为纯 detach 或纯 AuxK 因果效应。
- 不追加种子、checkpoint、数据、模型或新训练。

### A3. 完整分析链路

**AI 建议全部批准，不能挑有利分支替代：**

1. S2：三个来源严格加载；hook 读点；0B/5B 旧缓存桥接；0B/10B 小前向；10B FP32 分目标梯度；显存与 probe 实测计时。
2. S3：18 点 P/N 前向、raw-\(h\)、\(\hat h\)、SAE Top-k、健康指标和每点 4×8 行梯度。
3. S4 Part A：原空间领域 probe、固定 \(h\rightarrow\hat h\) 迁移、余弦关系、Fisher、稀疏读出/重合、词面参照。
4. S5 Part B：中心化、未中心化矩阵去第一奇异方向、中心化后去第一奇异方向；A 与 B 独立保留。
5. S6：逐样本预测、三模型配对差、5000 次分层配对 bootstrap、A/B 图表、完整性校验、执行回执和证据包。

PCA/UMAP/t-SNE 只作描述性图，不参与主要结论。梯度只解释固定样本的局部 wiring，不解释历史优化因果。

### A4. 结果分类和结论边界

**AI 建议批准以下非挑选规则：**

- 不产生一个“模型表征总分”或自动总体冠军。
- 对每个预注册的模型差、checkpoint、面板、目标、表示和变换，统一分类：95% 配对区间全大于 0 为 `POSITIVE`，全小于 0 为 `NEGATIVE`，跨 0 为 `UNRESOLVED`；区间只反映当前家庭/行抽样，不包括训练种子不确定性。
- 对应的 P/N 量在同一点同号且区间均不跨 0，才标记 `CROSS_PANEL_CONSISTENT`；否则分别报告，不能用其中一个替代另一个。
- B2/B3 后差异保留、减弱或反转只说明共同方向敏感性，不说明被删方向无用或原优势虚假。
- probe 只支持线性可访问性；SAE feature ID 不跨模型/时期认作同一语义原子；表征证据不证明模型在下游任务中使用该信息。
- 任何 identity、hook、数值、收敛、完成标记或来源缺口，对应对象记 `INSUFFICIENT/INELIGIBLE`，不得补值或删样本。
- 明早由研究者确认最终解释和下一决策；今夜机器链只生成直接结果、资格分类和边界，不替研究者更新最终科学判断。

### A5. 提交前允许完成的本地实现

**AI 建议批准在冻结范围内完成以下工程闭环；这些是实施合同，不改变科学设计：**

- 接通 `scripts/run_full_remote_audit.sh`，使 S2 通过后自动进入 S3--S6。
- CUDA 前向/反向计时增加同步，并拆分 checkpoint load、state hash、模型前向、额外 Top-k encode、反向和 CPU 分析时间。
- 增加 0B/5B 四句旧缓存桥接；失败则重提受影响 P，不混用旧新缓存。
- 实现 `[0.001,0.01,0.1,1]` 的 fit/tune 选择、同分取小 C、收敛资格、稀疏 CSR、逐样本预测。
- 完成梯度 RMS、raw/weighted norm、范数比、完整 cosine、四批汇总和 N/A 规则。
- 记录 GPU peak allocated/reserved、run-id/source/code hash、原子完成标记和 Spot 恢复单位；拒绝旧输出污染。
- 完成关系配对、Fisher 充分统计 bootstrap、A/B 独立表图及输出覆盖检查。
- 本地预计 2--4 小时；必须重跑全部测试、审计和 submission dry-run。

若实现发现需要改变模型/数据/主要指标/资源/预算，必须重新请示；不能算作本项已批准。

### A6. 资源、镜像与拓扑

**AI 建议批准：**

- execution surface：ACP。
- profile：`h100-2-spot`。
- exact spec：单节点 `n6ls.iu.i40.2`，2×H100 80GB、44 CPU、480GiB 主存；两个独立 worker，各 9 个 checkpoint 任务，无 DDP。
- image：`shphd-lite-0911`；使用登记的 Python 3.10 / torch 2.3 / CUDA 12.4 路径和只读运行层。
- 提交入口：`templates/execution/acp_submit_template.sh`，由 execution envelope 解析 tuple；禁止手写 ACP create。
- 工作目录：`/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit`。
- 远程入口：`bash scripts/run_full_remote_audit.sh`。
- job name：`three-model-rep-audit-0915-full-v1`。
- 不 fallback 到 5090、reserved、多节点、本地 MIG 或不同镜像。

### A7. 计费预算：需要你明确选一个

修订估计：远程 S2--S6 为 **2.5--5.5 小时，中值约 4 小时**；不含排队和 Spot 抢占空窗。

**AI 推荐方案 R：**

- S2 后保守完整 ETA 必须不超过 6 小时，才进入 S3。
- S3 一旦开始，允许当前/恢复任务把完整 S3--S6 做完，但累计计算绝对上限为 **8 小时，即 16 H100·小时**。
- 理由：6 小时仍是放大门，额外 2 小时只保护 CPU solver、bootstrap、绘图和回执尾部，避免已采集数据后留下半套链路。

**更严格方案 S：**

- 全部提交累计绝对上限仍为 **6 小时，即 12 H100·小时**。
- 代价：在真实尾部接近估计上界时，可能只能交付 `PARTIAL`，与“确保完整链路”的要求存在张力。

本审批包默认请求 **方案 R**。排队不计费；所有已实际运行的 Spot 时间计入累计上限。

### A8. 提交次数、Spot 恢复与失败停止

**AI 建议批准：**

- 首次正式提交 1 次；最多允许 1 次相同 tuple、相同 protocol、相同 run root 的 Spot 恢复提交。
- 恢复只读取通过 hash 验证的完成标记，继续缺失单元；不得覆盖合格缓存或扩大范围。
- S2 的模型身份、hook、有限值、state/buffer 不变、显存或梯度资格任一失败：保存证据并停止，不进入 S3。
- S2 保守 ETA 超过 A7 门槛：保存资格结果并停止，不删模型/点/数据/Part B 来凑预算。
- S3 后单个分析对象失败：保留其他合格对象并将该对象标记 `PARTIAL/INELIGIBLE`；系统性失败则停止。
- 不自动停止、修改或占用任何既有任务。

### A9. 提交后监督方式

**AI 建议批准，符合“提交后即可结束，明天看结果”：**

- 提交后只观察短启动窗口：任务被平台接受、workerspec/image/mount 正确、两个 GPU worker 可见、pod 持久日志开始写入、没有立即失败。
- 不在当前对话持续轮询到 S2 或全链完成；确认启动健康后报告 job ID、最后状态、日志/结果位置和 ETA，然后结束。
- S2 通过后作业内自动继续 S3--S6，不需要新的人工确认。
- 若在当前对话结束后发生 Spot 抢占，恢复不会凭空发生；明早状态检查再依据 A8 的授权执行唯一一次恢复。若平台自身恢复同一 job，则由完成标记续跑。

### A10. 今夜交付和明确排除项

**AI 建议批准：**

远程 run root 至少生成：

- S2 资格与实测 ETA；18 点 task/completion manifests；P/N 表征缓存；完整梯度表；
- `A_raw/` 与 `B_common_direction/` 的 tables、predictions、figures；
- bootstrap 区间、分析覆盖矩阵、失败/缺失表；
- execution receipt/certificate、持久 pod log、直接结果报告和 artifact map。

今夜不做：新训练、optimizer update、checkpoint/buffer 改写、结果驱动加样本/点/C、自动因果结论、最终 Anchor/Focus 结果更新、commit、push、root sync 或外部发布。明早结果存在后，再由研究者完成科学解释；canonical `summary.md/summary_cn.md/detailed.md` 按证据与研究者判断写入。

## 3. 一次批准后我将执行的顺序

```text
研究者批准 A1--A10
-> 创建并自检 Focus/Anchor/Protocol（DRAFT -> confirmed design -> execution-approved scope）
-> 补齐 A5 实现
-> 本地审计 + 全测试 + 全链 dry-run
-> resolved tuple 与 A6 逐字段一致
-> 正式提交一个 H100-2-Spot full job
-> 短窗口确认调度/运行层/双 worker/持久日志健康
-> 报告 job ID、最后验证状态、ETA 与结果位置
-> 结束本次对话，作业自行运行，明早读取结果
```

任何箭头未通过，都不执行下一步；特别是不会把“提交成功”写成“S2 通过”或“分析完成”。

## 4. 可直接回复的整包批准文本

若以上均同意，请回复：

> **全部批准，按 0915 完整远程提交审批包执行；确认 A1 的 problem_key 与唯一下一决策，确认 A2--A6、A8--A10，并采用 A7 推荐方案 R（S2 放大门 6 小时、累计绝对上限 8 小时/16 H100·小时）。完成本地门后可直接提交一次 H100-2-Spot full job；允许一次同范围 Spot 恢复。**

若只想维持 6 小时硬上限，请把“方案 R”改为“方案 S”。其他任何修改请直接指出对应编号；未修改项视为按本文精确值批准。

## 5. 证据入口

- 分析链路与二次实现审计：`0915_three_model_analysis_chain_review_cn.md`
- 完整执行计划：`0915_SAE_three_model_execution_plan_cn.md`
- 本地审计：`/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/audit/LOCAL_AUDIT_REPORT_CN.md`
- 当前 S2 卡：`/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/qualification/S2_EXECUTION_CARD_CN.md`
- 脱敏队列快照：`/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/audit/hardware_queue_snapshot.json`
- 资源/镜像/提交入口：`docs/execution_envelope.md`
