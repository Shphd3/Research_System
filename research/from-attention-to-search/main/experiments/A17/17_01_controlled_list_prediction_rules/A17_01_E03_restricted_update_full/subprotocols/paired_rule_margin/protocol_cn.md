# A17_01 E03 补充 Protocol：配对规则答案优势

[English](protocol.md)

状态：`APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_ANALYSIS`。父问题 `list_rule_shared_update`；E03 补充分析、子 Anchor A17_01_01，不增加第四个核心实验，不训练模型或 SAE。

## 授权与审计账本

2026-10-10研究者授权：“没问题，那就执行吧。完成 sub anchor 和 sub protocol 的书写，然后进行执行。现在开始，可以使用4卡H100 reserved计算资源”。该回复接受已讨论的配对 margin 检查，并授权正式写入与执行。以下重放/读数设置是委托落实的操作选择，不是研究者已经裁定的科学发现。科学解释和问题关闭仍为 Unknown；未授权 Git 或发布。

| 块 | 状态 | 依据 |
| --- | --- | --- |
| A 问题与边界 | CONFIRMED | 同列表、两种规则，局部相对选择 |
| B 数据与来源 | CONFIRMED | 已登记 selection-v2 留出 dev，来源内容组独立，不读 test |
| C 任务与监督 | CONFIRMED | 规则可见、预测单词元答案，无新监督 |
| D 架构 | CONFIRMED | 已采用的 Qwen 末层 o_proj，完整 FP32 前向 |
| E 优化 | CONFIRMED | 不训练，重放已存真实更新并精确恢复 |
| F 比较与证据 | CONFIRMED | 更新/不更新配对 margin、CE、来源有效性、竞争解释检查 |
| G 执行 | CONFIRMED | 4卡 H100 reserved，四进程 Smoke 全通过才运行 Full |

跨块一致性 PASS：同一固定列表和更新直接测量指定疑问，无 test 真值或 SAE 代理。数值阈值仅属工程。这是已接触开发集的补充分析，不是盲确认。

## A. 问题、假设与允许结论

来源学习改善另一规则答案 loss 时，正确答案相对错误规则答案的优势是否提高？H1 预测提高。R1 为候选词总概率适应但相对选择不改善。R2 为两种提示共有的位置偏置，S 检查其中相同加性情形。R3 为两词优势提高但仍不能胜过中间词/全词表其他词。只允许指定真实矩阵干预的局部预测结论，不支持内部规则算法、普遍迁移、SAE 机制或专家必要性。

## B. 输入与独立性

严格资产访问快照见执行目录 provenance/input_access.json、partial_input_access.json；逐文件哈希见 required_input_hashes.json。输入为官方 Qwen Base/分词器、list_rules_v1、selection_v2、三个种子的 E03 direct 检查点、Qwen29/43 分析矩阵、Qwen71 初始/16步和100步 partial-recovery 矩阵资产。100步 partial 只提供已存更新字节，不使用旧的不完整干预结果作证据；本轮独立完整前向。

固定 selection-v2 的120条留出 dev，即60对。每规则5个来源批次、每批20条，20个答案词均衡。来源与接收无序内容组不重合。批次2–4是此前留出来源，0–1是此前发现来源；目前均已暴露，不称盲集。冻结全部 ID、数据/选择器/检查点/manifest 和280个矩阵的 SHA256。不读取 test.jsonl。

每对是同一有序列表的 FIRST/LAST 两条前文。检查三个词互异、两条列表一致、正确答案 ID、完整配对、内容组独立。按每检查点训练步数和实际 batch_record_ids 重算是否见过内容组，与旧审计交叉检查。分别汇报名义 order_new/combination_new、实际见组未见顺序/本轮未见组，以及合并。列出对数和组数；不能把列表对当独立训练种子。

## C. 预测任务

输入止于答案标记，不含已完成答案。预测单位是一个词元。FIRST 答案为第1项，LAST 为第3项。沿用 Qwen 分词器与已存 input_ids，不重新分词。规则和列表候选词是合法输入。沿用数据准入检查，并核查答案映射和配对；异常即停止，不偷偷删除样本。

## D. 模型、状态与干预

核对官方 Qwen3-0.6B Base 磁盘身份。FP32、eval、SDPA、不采样、无 dropout、关闭 TF32、确定性算法和 CUBLAS 配置。使用完整模型前向的答案 logits，不使用 SAE 重构或仅末段重放。

仅恢复第27层 Attention 的 o_proj.weight（1024×2048），其余权重保持官方父模型。状态为去重 Base，以及29/43/71三个种子各第16和100步，共7个。每状态 FIRST/LAST ×b0–b4×步长{0.001,0.01}×倍率{1,0.5}，40个 strict 实际 FP32 更新，总280条件。要求 `(W0+delta)-W0 == delta`，检查有限值/形状/类型/来源、矩阵恢复和冻结权重摘要。每条件从原矩阵独立出发。

## E. 目标与优化

无优化器、新梯度、训练轨迹或检查点选择。步长与倍率是已存更新标签，不重新算更新。各终点与同一初始无更新预测配对。每前向批20条；四进程分配不同状态，不使用 DDP。FP32 logits，FP64 logsumexp/差值。CE 单位为 nat/答案，按记录等权；S 按列表对等权。候选池恒等式来自同一组 logits。

training_updates=0，因此训练遥测/续训条款不适用。分析保存20候选词 logits、全词表对数归一化与 top1、指标、条件计数、耗时、来源/配置/输入清单；不声称新训练检查点。

## F. 测量与分支

m_FIRST=z(首项|FIRST)-z(末项|FIRST)；m_LAST=z(末项|LAST)-z(首项|LAST)；S=m_FIRST+m_LAST。全部报告更新前/后/差值。还报告正确词减其他两项最大 logit、列表内准确率、全词表准确率、CE、20词条件 CE 和20词总概率对数。保存逐条/逐对结果及分别/合并面板。

主要描述性切片：第16步、步长0.01、倍率1、b2/b3/b4、两个方向、三个种子。共六个种子×方向单元，每单元三个来源。列全部值与均值，不作总体 p 值或总体置信区间。敏感性切片为 b0/b1、初始/100步、较小步长和半倍率；全部保留，不挑有利条件。

基线重复两次；任何非零漂移停止。各指标 eps=max(1e-6,10×重复漂移)，S 阈值为 margin 的两倍。阈值只表示数值分辨率。来源有效：独立同规则平均 CE 改变<-eps_loss；接收帮助：另一规则 CE 改变<-eps_loss。随后 margin 改变>eps 为提高、<-eps 为下降，其余未分辨。来源无效/接收帮助未分辨单独标记，不能叫冲突。

六个主要单元中的全部来源均有效、帮助接收且 margin 提高，才给出“一致的描述性局部两词优势支持”；否则保持异质/不足，列明异常单元。loss 降而 margin 不升反驳“所有 loss 帮助都改善这个相对选择”的泛化，不证明候选池解释是唯一解释。S 提高不能掩盖接收受损，两词优势提高不等于 top1 提高。机制判断 Unknown。

本地七检查：候选词统一提高、两提示同样位置偏置、loss 降但 margin 更差、两词胜出但输给中间词、缺配对拒绝、CE 分解恒等式、非有限值拒绝。只是实现验证。

## G. 执行、门槛与产物

资源 profile 为 h100-4-reserved；镜像 key 为 shphd-lite-0911。通过根目录规范模板解析 execution_envelope，不另抄资源元组。沿用已检查的挂载 Transformers 环境和 runtime，加 CUBLAS 确定性设置，不安装环境。单节点四独立 GPU 进程，最多2小时，不换资源、不并行重复提交。启动前检查代码/配置/Protocol/输入哈希；独立 UTC run 目录和写锁防覆盖。

内部 Smoke：四进程分别加载一个检查点，两个名义面板各选四对，共8对/16条；重放 FIRST/LAST 的 b2、步长0.01、倍率1，各进程两条件，总8条件。要求4张 H100、完整有限前向、精确空更新/恢复、来源身份、更新字节、冻结权重和完整配对指标。四份 PASS 后才启动 Full：7状态、每状态120条、280条件。Smoke 仅证明工程。

缺输入、哈希错误、组重合、非有限值、非确定性空更新、设备不符、更新/恢复/冻结检查失败、进程错误或超时，均停止并保留失败证据。先检查已有作业再重试；新恢复目录保留谱系，重大改动追加修订。不偷换输入、不把失败当科学非支持。

产物包括 freeze/config、环境执行证书、四份 Smoke/四份 Full worker 结果、门槛结果、七状态汇总、初始/终点 NPZ、逐条件配对 JSONL、results.json、payload_manifest.json、completion.json 和启动检查。执行根为 /data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin，runs/ 下使用 UTC 标识。复用原 raw-projection 分析的 Qwen 加载/恢复/collate，删除无用 S7/SAE/末段方法；runtime 复用 projection_full。新计算与重放先过七项本地检查，再过四卡 Smoke。

/root 做有界启动/首进展检查，有实测吞吐后给 ETA，然后停止轮询，除非用户另有要求。平台成功不足以宣告完成；须检查条件覆盖、收据、终点计数/哈希、恢复/冻结检查和 manifest，再登记实际分析产物，并写中英补充 Summary/Detailed。科学判断由研究者负责。不提交 Git、不发布。

## 运行冻结与后续记录

启动前保存本科学正文快照与 SHA256。执行事实在 Detailed 或此处追加，不改写运行前合同。实质变动需附修订与证据资格影响。

### Execution receipt (2026-10-10T14:12:45.060800+00:00)

Job `pt-hz9kc697`; platform `QUEUEING`. Runtime gates pending. [Detailed](detailed_cn.md) records mutable execution observations; the run-local pre-start Protocol snapshot remains frozen.

### Bounded startup outcome (2026-10-10T14:13:43Z)

Four Smoke workers PASS; Full auto-started;50/280 completed at the last observation. Runtime H100/profile/image verified. Monitoring stopped after first progress. Full completion remains unverified; no design amendment.

### Verified completion (2026-10-10T14:45:45.395007+00:00)

Job pt-hz9kc697 SUCCEEDED;Smoke8/8 and Full280/280 PASS;7 states;330 frozen input and642 payload hashes matched. Registered output `representation_a17_paired_rule_margin_20261010t141041z`. [Summary](summary_cn.md) records the unchanged frozen descriptive verdict; human mechanism/closure Unknown. No amendment/retry.
