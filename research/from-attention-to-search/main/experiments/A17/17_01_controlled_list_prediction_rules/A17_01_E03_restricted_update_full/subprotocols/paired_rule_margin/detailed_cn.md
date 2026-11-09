# 完整记录：A17 配对规则答案优势

[English](detailed.md) · [中文 Summary](summary_cn.md) · [Protocol](protocol_cn.md)

工程已完成。证据在冻结的已暴露开发集局部干预范围内合格，不是盲确认。冻结描述性判定为 `DESCRIPTIVE_HETEROGENEOUS_OR_INSUFFICIENT`；科学机制和问题关闭仍为 Unknown。以下解释为 AI 建议，待研究者裁定。

## 0. 核心结果

主要切片18/18来源更新有效，且降低接收规则 CE；接收双答案优势12/18提高、6/18下降。两种规则提示的偏好分离 S 在18/18提高，平均+0.003115。没有满足“所有主要更新均改善接收 margin”的冻结一致性标准。

## 1. 对象定义

双答案优势：同一提示下，正确规则答案 logit 减错误规则答案 logit，等于两者对数概率差。S：同列表 FIRST/LAST 两条提示的双答案优势之和。20词条件 CE：把概率限定在20个答案词后，正确答案的负对数概率。词池对数概率：20个候选词概率总和的对数。

CE 改变为负是帮助；margin 改变为正是相对优势改善。loss/margin 使用自然对数。准确率差在原始文件中为比例，乘100后为百分点。数值分辨率为1e-6，S 为2e-6；它们不是效果重要性或统计显著性标准。

## 2. Anchor 与判断位置

父问题关心共享学习的帮助或干扰；子问题只核对 loss 帮助是否到达相对答案选择。不重定义父问题，不裁定专家或 SAE 机制。子 Anchor 的问题身份保持 `list_rule_shared_update`。

## 3. 冻结、合规与偏离

| 注册项 | 预期 | 实际 | 状态 |
| --- | --- | --- | --- |
| 模型状态/Full 条件 | 7/280 | 7/280 | PASS |
| Smoke | 4进程、8条件 | 全部通过、8份终点 | PASS |
| 固定 dev 配对 | 每条件60对 | 完整60对 | PASS |
| 来源/接收内容组 | 无重合 | 重合0 | PASS |
| 空更新、恢复、冻结权重 | 精确重复与恢复 | 漂移0，所有进程冻结摘要相同 | PASS |
| 输入/产物身份 | SHA256 一致 | 330/642项均匹配 | PASS |
| 主要切片 | 第16步、.01、倍率1、b2–4、三种子双向 | 18条件 | PASS |
| 新训练/SAE/test访问 | 无 | 无 | PASS |

无修订、重试、删除条件或缺失条件。事后复算和面板均值只总结已冻结读数，不增加新的模型测量或假设检验。此前开发结果引出本轮，不能把现在的冻结称为盲预注册。入口检查器检查86项，因10条存在但未跟踪的旧入口返回1，没有报告缺失路径；新文档链接/数学源码通过，未进行渲染验证。

运行前合同见[冻结 Protocol](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/protocol.md)，其 SHA256 由[登记请求](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/registration_request.json)保存；后续执行事实追加到当前 Protocol，不改写冻结正文。

## 4. 实际设置

官方 Qwen3-0.6B Base；仅从已存 direct 检查点恢复第27层1024×2048 Attention o_proj，其余权重为同一个官方父模型。一个去重 Base，加三个种子29/43/71的第16和100步，共7状态。完整确定性 FP32 前向，FP64 对数归一化/差值；每批20个答案。

每状态40个已存真实矩阵：FIRST/LAST×来源b0–4×步长{.001,.01}×倍率{1,.5}。从同一原矩阵应用更新，检查有效增量字节一致，逐条件恢复。没有优化器、新训练步骤或续训；也没有 SAE 分析分支。

数据为 selection-v2 固定120条留出 dev/60对。名义未见顺序20对、未见组合40对。来源组与接收组独立，答案不进入输入。分词器和 input_ids 沿用既有数据；没有访问 test。

[代码](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/source/run_margin.py) · [配置](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/config.json) · [冻结清单](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/freeze.json) · [输入谱系](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/provenance/input_lineage.json) · [环境证书](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/execution_certificate.md)。

## 5. 指标与冻结判定

主指标为接收规则双答案优势改变。辅助记录 S、正确词减其他两项最大 logit、列表内/全词表准确率、CE、20词条件 CE、词池对数概率。来源有效要求独立同规则 CE 降低超过1e-6；接收帮助要求另一规则 CE 同样降低。随后 margin 大于1e-6是提高，小于−1e-6是下降，其余未分辨。

主要切片：第16步、已存步长.01、倍率1、b2/b3/b4、三种子双向，共18更新。支持一致改善要求18次全部合格并提高 margin。三种子是训练重复；种子内三个来源批次是重复读数，不能当三个独立训练。平均先批次等权、再种子等权。不报总体 p 值或总体置信区间。

## 6. 证据谱系

| 判断 | 原始/派生来源 | 计算 | 观察 | 边界 |
| --- | --- | --- | --- | --- |
| 工程完成 | [核验](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/completion_verification.json) | 字节哈希、计数、进程收据 | 7状态、280终点、8 Smoke | 平台成功不足以单独证明完成 |
| loss与margin | [逐条件表](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/primary_conditions.csv) | 固定主要切片 | 18 loss帮助，12/6 margin符号 | 暴露dev、局部更新 |
| 两提示分离 | [复算](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/readout_audit.json) | 同列表两优势相加 | 18/18正 ΔS | 来源改善可压过接收下降 |
| 未见分别/合并 | [面板表](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/primary_panels.csv) | 保留名义和实际分类 | 下表 | 实际子组大小依种子变化 |
| CE分解 | 已存终点数组 | 条件20CE−词池对数概率 | 两项均值均改善 | 记账恒等式，非因果中介 |

## 7. 主要结果

| 来源→接收 | 平均ΔCE | 平均Δmargin | 提高/下降次数 | 准确率改变（百分点） |
| --- | ---: | ---: | --- | ---: |
| 首项→末项 | −0.002282 | +0.000545 | 4/9、5/9 | −0.370 |
| 末项→首项 | −0.002436 | +0.000940 | 8/9、1/9 | +0.556 |

六个种子×方向单元的平均 margin 都为正：种子29为+.000161542/+.001525413，43为+.000421863/+.000874774，71为+.001050864/+.000418801（依次首→末、末→首）。但只有2/6单元的三个来源全部提高，因此冻结判定仍为异质/不足。S 在18/18提高，范围.002667014–.003472678。条件20 CE 为17/18改善，词池概率18/18提高。首→末准确率2/9下降、7/9不变；反向3/9提高、6/9不变。

| 来源→接收 | 名义面板 | 每状态配对数 | ΔCE | Δmargin | 准确率改变（百分点） |
| --- | --- | ---: | ---: | ---: | ---: |
| 首项→末项 | 未见组合 | 40 | -0.002349 | -0.000043 | +0.000 |
| 首项→末项 | 未见顺序 | 20 | -0.002149 | 0.001721 | -1.111 |
| 末项→首项 | 未见组合 | 40 | -0.002938 | 0.001969 | -0.278 |
| 末项→首项 | 未见顺序 | 20 | -0.001433 | -0.001119 | +2.222 |

| 来源→接收 | 实际曝光面板 | 每状态配对数 | ΔCE | Δmargin | 准确率改变（百分点） |
| --- | --- | ---: | ---: | ---: | ---: |
| 首项→末项 | 实际见组未见顺序 | 6,8,10 | -0.001220 | 0.001370 | +0.000 |
| 首项→末项 | 实际本轮未见组 | 50,52,54 | -0.002387 | 0.000360 | -0.412 |
| 末项→首项 | 实际见组未见顺序 | 6,8,10 | -0.001598 | -0.000752 | +0.000 |
| 末项→首项 | 实际本轮未见组 | 50,52,54 | -0.002522 | 0.001138 | +0.634 |

面板平均先批次等权再种子等权，不把不同大小的实际子组直接池化。合并用每条件全部60对；名义20/40，实际见组按种子29/43/71分别8/10/6，未见组52/50/54。实际见组太小，不能据此推广哪种泛化更好。

## 8. 可视证据

以上表格呈现关键符号和计数，无另生成科学图。逐配对数据由原始 payload manifest 链接。

## 9. 阶段证据与失败分解

7项本地检查通过；Smoke8条件、Full280条件通过；330输入/642产物哈希通过；独立复算280终点和7基线，最大差异1.4210854715202004e-14。无运行恢复。6个接收 margin 下降使科学一致性标准未满足；这是实测现象，不是工程失败，也不证明不存在共享功能。数值分辨率不等于统计不确定性。

## 10. 完整轮次与执行历史

2026-10-10轮次：检验配对相对选择假设；7个已存原生 Qwen 状态与各自空更新比较；没有新训练数据，来源批次固定；60对dev，不开test；结果18个CE帮助、margin为12正6负；AI认识为loss帮助不稳定蕴含相对选择迁移。作业 pt-hz9kc697 使用4卡 H100 reserved并成功。上轮首进展后停止轮询，本轮收到结果请求后检查同一已完成任务，没有重复提交。

<details><summary>Historical startup notes (preserved; not current status)</summary>

# A17 E03 配对答案优势：执行记录

## 问题与假设

有效的跨规则更新是否同时改善 loss 和正确答案相对错误规则答案的优势？与候选词总概率适应、共有位置偏置比较。科学解释 Unknown。

## 设置与对照

7个已存 Qwen direct-o_proj 状态、280个独立真实矩阵、固定120条 dev/60对；不训练模型/SAE、不访问 test。4卡 H100 reserved，四独立进程，内部 Smoke→Full。[Protocol](protocol_cn.md)；[环境证书](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/execution_certificate.md)。

## 数据与来源

输入检查 PASS：检查点 manifest、280矩阵形状/类型/有限值/哈希、来源与接收内容组独立、完整配对、20答案词映射、实际训练曝光账本核对。[冻结清单](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/freeze.json)；[输入谱系](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/provenance/input_lineage.json)。已暴露 dev，不是盲确认。七项本地实现检查通过；检查数学源码与本地链接，未声称渲染验证。

## 执行状态与偏离

作业 pt-hz9kc697 于 2026-10-10T14:11:19Z 通过规范模板提交；2026-10-10T14:12:45.060800+00:00 平台状态 QUEUEING。Smoke、Full 均尚未验证，科学终点尚未测得。无科学输入偏离。不因提交就宣告完成。

[提交收据](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/acp_receipts/submit-a17-margin-analysis-20261010t141041z-20261010T141117Z.json)；[启动状态](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/acp_receipts/describe_startup.json)。复用已检查 Qwen 加载/恢复/collate 和挂载 runtime，删除未用 S7/SAE/末段函数，加 CUBLAS 确定性设置。

## 结果

NOT_RUN，无 margin/CE 结论。预期7份状态汇总、280条件终点与配对记录、分别/合并未见面板、四份 Smoke/Full 结果、results、manifest、completion。仅在验证后登记实际产物。

## 认识、边界与下一判断

已授权执行，机制/关闭由研究者判断。完成后合看两个方向 margin、S、CE、准确率和词池概率；混合/未分辨值保留。目前只做有界启动/首进展检查，不重复提交排队/运行任务。

## 最近一次有界检查：2026-10-10T14:13:43Z

四进程 H100 运行环境核实；四份 Smoke PASS，8个更新条件完成。Full 已自动启动，快照确认50/280条件完成，尚无检查错误。按首批吞吐剩余计算约1–3分钟，不含最终验证/登记。停止轮询，不创建自动监控。完整工程完成与科学结论尚未验证。[启动证据](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/startup_verification.json)。入口检查器因10条已存在但未跟踪入口返回1，未报告缺失路径；新文档链接/数学源码检查通过。


</details>

## 11. 解释与推理审定

以下为 AI 提出的限定解释，非研究者已确认机制。CE下降提高正确词概率，但不说明它与指定错误词的比值。6个直接反例排除“所有loss帮助都改善双答案优势”的泛化。S在18/18提高，排除单纯统一抬高候选词、或两提示完全相同的加性位置偏置作为唯一解释；不证明内部形成了规则算法。S提高可以来自来源改善超过接收下降。20词条件CE涉及其他18个词，不能替代首末项之间的优势。来源批次、状态和方向差异仍是活跃解释。均值提高不等于每个更新稳定迁移，也不证明架构收益。

敏感性：初始Base、b2–4、.01、倍率1为6/6合格且margin提高；第100步为7提高、5下降、4接收帮助未分辨、2来源无效，共18。它们不能补救主要第16步判定；状态依赖训练历史，未识别普遍的状态机制。

## 12. 结论边界

可说：指定已存干预在固定状态和独立列表上造成局部预测变化；loss帮助与双答案优势符号可以不同；本主要集合的条件偏好分离提高。不可说：稳定普遍规则迁移、自然文本预训练收益、功能模块分解、SAE特征机制、专家必要性或架构优越性。仅三个种子、已暴露dev、效果小、无盲重复。机制/关闭 Unknown。

## 13. 下一判断

由研究者裁定 Summary 的限定解释。完成标准：研究者明确可接受答案及边界。接续方式：复核18个来源更新，尤其6个loss帮助但margin下降的情形。本报告不提交或授权下一实验。

## 14. 产物清单

| 产物 | 用途 | 身份/完成情况 |
| --- | --- | --- |
| [冻结Protocol](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/protocol.md) | 运行前合同 | SHA256见登记请求，完整 |
| [冻结清单](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/freeze.json) | 代码/配置/数据/更新身份 | 330项验证 |
| [原产物manifest](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/payload_manifest.json) | 原始终点/配对/汇总 | 642项验证，完整 |
| [结果](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/results.json) | 冻结判定及280条件 | 完整 |
| [独立复算](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/readout_audit.json) | 算术与面板派生表 | 完整 |
| [完成核验](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/completion_verification.json) | 平台、字节、计数 | 工程通过 |
| [登记收据](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/registration_request_registered_outputs.json) | 实际可复用输出身份 | representation_a17_paired_rule_margin_20261010t141041z |
| [当前访问检查](/data/250010109/Research_System/assets/checks/2026-10-10_a17_outputs_20261010T144031Z.json) | 选定产物访问 | PASS，不是全库重查 |
| [原任务状态](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/runs/analysis_20261010T141041Z/acp_receipts/describe_results.json) | 同一任务 | pt-hz9kc697 SUCCEEDED |

没有新模型或SAE检查点，续训能力不适用。原训练/数据父资产在登记请求和freeze中。新审计保留执行侧，不追加入旧payload manifest来改写历史。

## 15. 链接

[Summary](summary_cn.md) · [Protocol](protocol_cn.md) · [执行根目录](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin)
