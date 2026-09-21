# Conversation Memory: 0920-SAE表征空间审计

Conversation name: 0920-SAE表征空间审计
Processed by: Codex (harness: Codex desktop; model: unknown)
Created at: 2026-09-20T06:45:12Z
Latest update at: 2026-09-20T18:05:34Z
Continues from: `.research/memory/conversations/0914-training-scheduling/memory.md`
Environment: `repo=/data/250010109/Research_System` `exec=/data/250010109/MoE_Router`; both roots are readable.

## 2026-09-20T06:45:12Z -- 冻结检查点表征空间审计启动

- Summary: 研究者要求把当前重点从语言损失排序转向冻结检查点上的表征空间审计，同时保留语言预测代价检查；核心待检验问题是旁路稀疏自编码器是否改变可跨表达、跨语境使用的语义组织，还是主要改变尺度、类内压缩或观察方式，以及在线字典能读出什么、重构误差仍保留什么。本条只记录工作目标，不把问题写成已有结论或批准的新科学状态。
- Current work: 正在完整读取来源对话记忆、当前 Focus、E05 的 Protocol/Summary/Detailed、会议材料及真实执行包，随后做只读资产盘点和必要的小型本地检查。授权不含新主模型训练、离线字典训练、大规模提取、远程提交、科学状态变更、提交或推送。
- Next action: 先完成 E05 证据资格、Dense 10B 末词元异常标尺、P/N 面板适用性、双缓存根与可用键的核对，再形成一个未自动获批的最小分析计划；若已有缓存不足，则明确缺口并停在范围裁定，不以文件名推定数据存在。
- References: `.research/memory/conversations/0914-training-scheduling/memory.md` 提供本任务的直接续接入口；`.research/memory/conversations/0915-表征梯度测量/memory.md` 提供 E05 导航但不拥有证据；`daily_research_reports/0918/focus_meeting_sae_sidecar_regularization_0_10b_cn.md` 与 E05 的 `summary_cn.md`、`detailed.md`、`protocol.md` 是待核验的正式来源；`.research/memory/conversations/0914-training-scheduling/0920_representation_analysis_prompt_cn.md` 是本任务来源提示，不拥有科学批准。

## 2026-09-20T07:10:53Z -- 首轮证据地图、标尺审计与最小计划完成

- Summary: 已完成用户指定材料、E05 正式链、会议材料、两个候选调研、执行包代码和缓存谱系的只读审计，并在 `daily_research_reports/0920/representation_analysis_followup/` 写出三份中文产物。没有训练、远程提交、大规模提取、Focus/Anchor/Protocol/problem_key 变更或科学批准。
- Evidence update: 合格表征必须按 E05 记载使用双根；30 个表征单元的 P/N 样本顺序核对无 mismatch。M0 P 末词 10B 的 $B/W$ 下落主要来自 $W$ 暴涨且由三个 report 样本主导，单位范数化和 fit-only 共同方向移除不能修复，既有均值池化敏感性不复现该终点异常。对既有 P 做的事后跨叶领域读出中，M0/SALL 的 10B 平衡准确率为 0.90000/0.85556，差 -0.04444、family 成对 bootstrap 95% 区间为 [-0.09444, 0.00000]；该结果只作探索和停止依据，不是正式确认。严格低重叠同义句对高重叠反例的余弦间隔在所有原生模型 5B/10B 均为负，不能把现有领域读出升级为命题语义。
- Observer boundary: 现有旁路缓存有 $a$、重构和误差，但没有逐样本 $z$；三者跨叶读出呈混合结果。误差单独可读不能证明重构丢失信息，需在主干效应稳定后做固定总容量的增量读出。固定 M2D2 上三个旁路 10B 留出 NLL 均劣于 M0，继续作为不利护栏。
- Missing input: `daily_research_reports/0920/docs/atten执行资料/` 存在且为空；同日两个 survey 只作建议，未被当作缺失资料或批准。
- Artifacts: `daily_research_reports/0920/representation_analysis_followup/01_证据地图与最小分析计划_cn.md`；`02_只读资产与标尺审计_cn.md`；`03_方法原始定义学习笔记_cn.md`。
- Proposed scope: 唯一候选是领域主线下 M0 对 SALL 的 5B/10B、共同末层原生 $h$、按 family 分组的跨叶线性读出，S37 仅诊断尺度/压缩；不自动纳入 S7、M2、所有层、R 面板、$z$ 提取、离线字典、K 扫描或干预。现有 P 已看过，只能探索；若研究者仍要确认，需要另行批准小型、人工核对并冻结的新领域面板及科学最小效应阈值。
- Next action: 等待研究者裁定是否在当前负向/不足的探索结果后冻结上述唯一候选，以及科学最小效应阈值是否需要高于零；在此之前不执行新提取或训练。
- References: E05 `summary_cn.md`、`detailed.md`、`protocol.md` 是正式结果与资格来源；本条只作非规范导航，不能替代这些证据或研究者批准。

## 2026-09-20T14:16:51Z -- v2 分析计划已读并压缩为实现前检查点

- Summary: 研究者指定 `daily_research_reports/0920/docs/0920_SAE_表征空间分析计划_v2_资料包/0920_SAE_表征空间分析计划_v2_CKA与数据构造.md` 为当前分析计划。其核心问题是：在推理主路径不使用旁路重构的条件下，SAE 旁路正则是否改变投影后、残差相加前的注意力写入 $a$，这种变化是否提高指定语义因素在未见表达中的简单可读性，并能否进一步与模型行为联系。结构变化、语义可读、模型使用和任务收益保持四层分离；本计划是实现工作规格，不是已执行结果、正式 Protocol 或训练/远程执行授权。
- Supersedes: 上一检查点中“5B/10B 末层原生 $h$、M0/SALL 主比较、S37 诊断”的 AI 候选范围，不再作为即将实现的工作规格；其已完成 E05 审计和负向/不足探索仍保留为历史证据。v2 的当前主范围改为 Dense 与原版 SALL 在 15B/21B 的四个端点、八层轻量扫描及第4/8层重点分析，主对象改为注意力原始写入 $a$。早期 0--10B 点只有在四端点完成后、且真实共同 checkpoint 通过核验才可条件性加入。
- Fixed scope: 主确认比较是 21B 原版 SALL 对 21B Dense，第4/8层分别报告；15B检查持续性。八层扫描使用同次前向的小型拟合/开发面板，开发集最多选择一个额外层，规则固定为除4/8层外 P 四家族平均线性准确率的 `|SALL-Dense|` 最大层。M2-15B只作为主路径使用重构的次级能力候选；S7 原版15B与重加权21B只作分叉次级条件；S37与新版SALL系数0.8目前无合格端点，不为补表自动重训或混名。
- Data contract: `P_rel_v1` 为200实体组、四关系家族、八模板、双方向共12,800句，120/40/40实体组与4/2/2模板独立划分，`test_joint` 640句为主确认；首轮使用 fit/dev_joint/test_joint 共5,120句。`N8_v1` 为八个M2D2学术细类，每类300/100/200、256正文词元，共4,800条。`PAWS_wiki_final` 目标8,000/2,000/2,000句对并按来源连通组隔离。所有面板必须先完成来源分组、查重/冲突、实际分词器检查、捷径基线和人工语义审核再冻结；探针划分独立不等于主干预训练未见。
- Measurement contract: 唯一主取点是各层注意力输出投影后、残差相加前的 $a$，不是旧 E05 的末层 `norm2` 原生 $h$。P主汇聚为最后有效正文词元，N8/PAWS为正文均值，二者均保留对照；排除填充和自动特殊标记。重点层保存 `attn_raw`、`sae_recon`、逐词元 `sae_code`、`sae_error` 与真实 `effective_write`，并先通过残差恒等式、旁路观察不改输出、左右填充一致、因果前缀不变、整段与增量缓存相容等取点验收。M2必须区分重构前注意力与实际写入。
- Analysis contract: 数据冻结后，无标签结构指标（范数、频谱、类间/类内分解、标准及有限样本修正线性CKA）与标签/反例指标（线性读出、跨模板/实体双留出、PAWS、距离间隔）并行，不把CKA当放行门或优劣分。主指标是 P `test_joint` 四家族等权线性准确率差；配对来源组自助法2,000次、种子20260920，两主层若作显著性主张用配对交换检验加Holm校正。CKA须用 `sample_id + input_ids_sha256` 对齐、双精度、标准/U修正两版、100次组约束置换、第一主成分诊断和样本量敏感性；普通CKA可能在小样本高维下虚高。
- Stage gates: 顺序固定为 0模型/谱系登记 -> 1数据冻结 -> 2提取位置与128条成本验收 -> 3四端点八层概览 -> 4第4/8层完整主分析且先看原始 $a$ -> 5条件性早期轨迹和在线字典读法 -> 6接入既有能力结果。先缓存八层池化 $a$，逐词元只限固定小诊断集；不把所有方法乘满所有 checkpoint。只有原始 $a$ 出现跨表达候选后才解释 SAE 读法或行为联系；离线公平字典、定向干预、续训和非稀疏辅助对照均需另行授权。
- Existing behavior boundary: v2复用但未重算0919下游报告。15B M2是常规任务正面候选但改变主路径；21B SALL与Dense没有可靠整体胜者；纯旁路SAE正则尚未建立稳定广泛的能力收益。2K训练条件下4K/8K长上下文只作分布外压力诊断，15B SALL高点未在21B持续。
- Assets and verification: 资料包包含 `config.yaml`、`build_p_rel.py`、`pool_attention.py`、`cka_reference.py`、`cka_self_test.json` 与 `verification_status.json`，本轮逐文件读取并核对 SHA-256，均与状态文件一致。CKA合成单元检查、汇聚合成检查和关系生成器语法检查已有 PASS；关系生成器本轮未运行，新同后缀/自然姓名诊断未实现，P 未经人工/分词器验收，N8/PAWS未下载清洗，真实模型取点、checkpoint和缓存均未验收。合成自测不构成语言模型结果。
- Current work: v2主文档1018行及全部随包文件已完整读取；本次只更新非规范 memory，没有开始代码实现、生成数据、加载 checkpoint、提取表征、训练字典/主干、提交远程任务或修改科学状态。当前 memory 通过新增这一压缩检查点保留旧负结果和未解决边界，没有删除历史条目。
- Next action: 开始实现前，先重新核对 `docs/training_reuse_index.md` 与 `/data/250010109/MoE_Router` 的真实源文件，确定不落入活跃训练目录的实现位置；完成阶段0的真实 `model_manifest.json` 与 `blocked_items.md`，解析 Dense/SALL 15B/21B 的 checkpoint路径、状态哈希、初始化/父运行、真实参数/上下文、分词器版本、模块路径和旁路主路径。随后先实现/测试 `verify_sites.py`、数据清单与捷径审计接口；身份或取点未通过时阻止模型提取，但可继续不依赖它的数据和单元测试工作。
- References: v2主计划拥有当前工作规格；同资料包 `README.md`、`config.yaml`、`verification_status.json` 及三个辅助程序拥有现有资产和未完成项；`daily_research_reports/0920/representation_analysis_followup/02_只读资产与标尺审计_cn.md` 与 E05 `summary_cn.md`/`detailed.md`/`protocol.md` 只拥有既有0--10B证据和边界，不能替代v2的15B/21B真实身份核验。

## 2026-09-20T17:39:00Z -- 21B 本地 Smoke 通过并提交正式任务，压缩至下一波入口

- Summary: 本对话当前仍属 A15_17；21B 的三模型 Dense、原版 SALL、重加权 S7 与 P_rel_v2/N8_v1/PAWS 三面板、双汇聚的冻结审计已写入 E06 Protocol。三次早期远程 Smoke 均未产生模型输出；研究者随后指定本地单 H100 40GB MIG Smoke 与一份 4×5090 Spot full。经审计脚本标量取样和源码不支持左填充的工程修复，本地生产右填充路径三模型 Smoke 有完整 PASS；左填充仍为明确限制，Smoke 不构成科学结果。正式作业 `pt-pqqnvoy6` 在 2026-09-20 17:37:21 UTC 提交；首次仅见 `STARTING`/Pending，尚无完整结果。研究者随后要求不再监督启动；不得将提交当作结果或自动重投。
- Current work: 正按研究者新增顺序准备下一波：先精确 15B 模型的本地 Smoke，再真实共同 0–10B checkpoint 的本地 Smoke；两者都通过后才分别提交 4×5090 Spot 正式任务，提交即停止监督。此新增范围和资源由本对话研究者明确授权，但仍需在各自 owning Protocol/执行凭据中固定真实模型集合、checkpoint、面板与失败闸门；不能从本记忆直接推定科学结论或把 21B 作业结果当已存在。不得训练主干或离线字典、改活跃训练目录、提交或推送。
- Next action: 核对 15B 与 0–10B 的真实 checkpoint/源代码/谱系及 v2 计划的适用范围，写独立冻结执行合同；先做 15B 本地小型 Smoke，之后做 0–10B 本地小型 Smoke。任何身份/取点/输入不合格都阻止对应 full，不用改名凑齐；两个 PASS 后各提交唯一一份 4×5090 Spot full，不观察是否进入运行中。
- References: `daily_research_reports/0920/focus_three_model_sae_representation_audit.md` 与 A15_17 Anchor 拥有当前问题边界；`Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E06_21b_sidecar_representation_audit/protocol.md` 拥有 21B 执行合同；`/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit/runs/smoke_local_h100mig_relrms_20260920T1725Z/stages/SMOKE_PASS.json` 与 `runs/full_4x5090_20260920T1736Z/execution_certificate_cn.md` 分别拥有本地工程 PASS 与正式提交/初次状态；v2 主计划用于下一波范围核对，但不是 15B/0–10B 的模型身份或作业批准来源。

## 2026-09-20T18:05:34Z -- 15B 与 0–10B 顺序 Smoke 完成、双四卡正式任务已提交

- Summary: 研究者明确要求不观察进入运行中，先完成 15B 本地 Smoke，再完成 0–10B 本地 Smoke，之后各提交一项单节点 4×5090 Spot 正式只读任务，提交即结束。两组均按顺序完成，本对话没有查询新正式作业或 21B 作业的后续状态，也没有自动重提。当前 A15_17 的 E06 21B 仍是主确认；新增 E07 15B 仅查持续性，E08 早期仅查时间轨迹，不改变科学结论或 Focus 的下一决策。
- Scope: E07 为精确 15B Dense 与原版 SALL 两模型，P_rel_v2/N8_v1/PAWS 三面板、双汇聚；E08 为 Dense/SALL 在真实共同 0/0.5/1/3/5/10B 十二 checkpoint，P/N8 双汇聚、八层轻扫和第4/8层重点读出，PAWS 不乘满早期点。SALL 在 9,174,381,056 词元由八卡续接四卡，10B 与15B须标记该分叉。M2/S7/S37 未混入主旁路对照。
- Engineering: E07 本地 H100 40GB MIG Smoke 2/2 PASS，模型加载时间合计 118.50 秒；E08 12/12 PASS，合计 635.44 秒；两组峰值预留 3,944,742,912 B（3.67 GiB）。两份真实模型清单、冻结 E06 数据哈希、Python/Bash 静态检查、配对统计小单元及 22 项 SHA-256 代码/协议快照检查通过；两份正式命令干运行及只读双 Smoke 预检均通过。本地 Smoke 不证明 RTX5090 运行、完整分析或语义结果；目标作业自己有四卡/SM120/显存/身份/结果闸门。正式耗时仅宽范围外推，排队未知。
- Submissions: E07 15B `pt-anbugr1c`，2026-09-20 18:03:43 UTC；E08 0–10B `pt-8hs32e5w`，18:03:51 UTC。均为 `5090-4-spot`、`shphd-lite-0911`，平台返回 `SUBMITTED`，不是 `RUNNING` 或完成。各作业运行根为执行包 `runs/full_15b_4x5090_20260920_wave1/` 与 `runs/full_early_4x5090_20260920_wave1/`，其中有提交 JSON/TXT 和 `execution_certificate_cn.md`；未监控任务启动。禁止仅凭本记忆判定作业状态或自动重投。
- Canonical/artifact map: E07/E08 Protocol 与 `detailed.md` 位于 `Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/` 对应实验目录；Focus 已加入两项补充实验但保留 21B 主问题。执行包 `/data/250010109/MoE_Router/experiments/20260920_sae_representation_15b_early_audit/` 的 `preflight_cn.md`、`manifests/model_manifest_{15b,early}.json`、`manifests/full_freeze_sha256.txt`、两本地 Smoke 的 `stages/SMOKE_PASS.json` 和正式提交回执拥有工程证据。无 Summary，因为正式结果尚未存在。
- Next action: 仅在研究者后续请求状态或结果时，检查上述既有作业 ID 和各运行根的目标 GPU 预检、`terminal_receipt.json`、`COLLECTION_PASS.json`、`ANALYSIS_PASS.json`、逐点 P/N8/CKA/在线 SAE/NLL 输出；失败或排队不等于需要重投。正式结果合格后再写 Summary/详细结果并请研究者确认机制边界。
