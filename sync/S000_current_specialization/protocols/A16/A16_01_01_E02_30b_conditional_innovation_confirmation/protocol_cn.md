---
experiment_id: A16_01_01_E02_30b_conditional_innovation_confirmation
anchor_id: 16_01_01_regret_distilled_conditional_innovation
status: approved_conditional_on_e01_pass
approved_by: user
approval_date: 2026-08-12
design_frozen_at: 2026-08-12
resource_profile: 5090-8-spot
primary_metric: document_paired_30b_endpoint_nll
---

# Protocol：A16_01_01_E02 30B 条件增量确认实验

## 0. Approval Snapshot

**目的：** 检验通过 E01 的效用蒸馏条件分支，在共同 Native 10B 状态后联合训练到 30B 总 token 时，是否改善语言模型质量。

**启动条件：** E01 必须在两个 seed 返回 `PASS` 并生成完整 artifact hash。可提前实现 E02 smoke，但在该 verdict 前不得创建长任务。

**处理与对照：** Conditional-Utility 与 exact Native continuation、Raw-Utility、Conditional-Haar 比较。每个 seed 都从自己的 Native 10B checkpoint 开始，并继承 Native 参数、optimizer、scheduler、RNG 与 data cursor。原 step-0 Trainable-Innovation 只作外部参照。

**主指标：** 冻结 1,024 文档上的 30B 总 token held-out NLL，单位 nat/token，越低越好。

**Pass：** Conditional 相对 Native、Raw 和 Haar 的文档配对 95% 上界在两个 seed 都小于零。某个机制对照不通过，则相应机制结论被否定或收窄。**Insufficient：** resume、数据、artifact、分支、LB 梯度、checkpoint 或终点评估身份失败。

**执行批准：** E01 Pass 后，可无需再次审批提交六个单节点 8×5090 任务：Raw、Conditional、Haar × seed17/29。既有 Native 30B 只有在 scalar、token order 与 checkpoint 身份完全通过时才可复用。

## 1. Terminology / Definitions

- 30B endpoint：累计 30,000,021,504 token，对应 optimizer step 38,147；处理 arm 在 10B 后实际续训约 20B。
- Teacher initialization：将 E01 的 $P,C,B_T$ 安装到 dormant rank-56 分支。
- Ramp：10B 后最初 128 optimizer steps 内，分支乘数从 0 线性增加到 1，约 100.7M token。
- Utility preservation loss：冻结教师路由分布到当前路由分布的 KL；它不是在线强制八专家标签。

## 2. Anchor Alignment

E01 只建立冻结专家下的局部选 expert 效用。E02 检验最强剩余竞争解释：教师是否短视、是否在表示和 experts 共同演化时过时。最终由 NLL 而不是 regret 或负载裁定训练价值。

## 3. Tested Hypothesis

通过 E01 的 Conditional-Utility 在 verified LB 下，30B NLL 低于 Native、Raw-Utility 和 Conditional-Haar，且两个 seed 方向一致并通过区间规则。

## 4. Rival Explanations

| 竞争解释 | 区分条件 |
| --- | --- |
| 效用监督有效但残差化无价值 | Conditional vs Raw |
| 任意低维旁路都有效 | Conditional vs Haar |
| 额外计算或恢复状态造成收益 | 同 checkpoint/data、FLOPs 与 exact-resume guard |
| 只改变负载 | 负载只能解释，不能代替 NLL |
| 教师随训练过时 | 20B/25B/30B regret 重测与 late NLL slope |

## 5. Data Construction And Provenance

从每个 seed 的 Native `checkpoint-12716` 继续同一 DCLM binary stream。评估使用 A16_01 已冻结的 1,024 文档。E01 功能 bank 与二者文档隔离，只产生不可变初始化 artifact，不进入 LM batch 或 endpoint evaluation。

## 6. Learning Task And Permitted Supervision

主任务是普通下一 token 预测。在线 Router 只读取当前层 $x,u$ 与 Native logits。禁止在线遍历八个 expert、confirmation 标签、taxonomy 标签或未来层状态。

## 7. Model / Architecture And Frozen Variants

所有处理条件保留 Native Gate，并复用 checkpoint 已有的 dormant rank-56 参数。Raw 使用 $uP$；Conditional/Haar 使用 $uP-xC$。$P,C$、FIT 标准化和冻结教师 $B_T$ 从 E01 artifact 重建；student 分支 $B$ 联合训练。相对 Native 10B checkpoint 不增加可训练参数或 optimizer slot。

## 8. Training Objective And Optimization

$$L=L_{LM}+0.01\sum_{\ell=1}^{4}L_{SwitchLB,\ell}+0.1L_{preserve}.$$

Native 的 $L_{preserve}=0$。处理 arm 的 $L_{preserve}=KL(q_T\|p)$；$q_T$ 由 detach 的当前 Native logits 加冻结 E01 教师分支在同一 ramp 下构成，$p$ 为当前总 Router 分布。0.1 系数、128-step ramp、AdamW 状态、学习率与 A16 公共配置在执行前冻结。LM+LB 可更新 backbone、experts、Native Gate 与 student branch；preservation loss 只更新 student branch。

## 9. Conditions, Seeds, And Checkpoints

新增 Raw-Utility、Conditional-Utility、Conditional-Haar × seed17/29 六个任务。均从各自 Native-LB `checkpoint-12716` 精确恢复。必须保存/评估 10B branch、15B、20B、25B、30B。只有新 source 对 Native logits/loss scalar hash、token hash 复现且 10B checkpoint 身份一致，才复用既有 Native endpoint。

## 10. Primary Metric And Frozen Analysis Plan

在 30B 对同一 1,024 文档计算 per-document NLL。每 seed 内配对，做 2,000 次 bootstrap，报告处理减对照均值与双侧 95% 区间。只有三个比较的点估计与上界在两个 seed 均小于零，才支持完整方法。不能把两个 seed 的文档池化成独立复制。

## 11. Secondary Metrics And Guards

报告 NLL 轨迹、25B→30B slope、token/FLOPs/wall-clock、LB loss 与 Gate 梯度、expert share/entropy/capacity drop、branch/native logit RMS、ramp 中 route flip/margin、teacher KL、20B/25B/30B frozen regret、expert update conflict、checkpoint/recovery 身份。它们不能挽救 endpoint Fail。

## 12. Known Good / Known Bad / Known Confusing Cases

alpha=0 必须 bitwise replay Native；artifact 篡改、跨 seed checkpoint 或重置 inherited optimizer 必须 fail closed；负载或 regret 改善而 NLL 不变不构成性能 Pass。

## 13. Scientific Procedure And Stage Contracts

| 阶段 | 目标 | 操作 | 放大条件 | 产物 |
| --- | --- | --- | --- | --- |
| S0 | E01 eligibility | 读取 typed verdict/hash | 仅 Pass | gate receipt |
| S1 | continuation | 单卡安装/ramp/保存恢复 | 全 guard 通过 | local smoke |
| S2 | distributed state | 一个全 arm 8×5090 smoke | rank/LB/data/resume 一致 | receipt |
| S3 | 提交 | 六个 5090-8-spot jobs | S0-S2 通过 | job ledger |
| S4 | 轨迹 | 15/20/25/30B 评估 | 不因性能停臂 | milestones |
| S5 | 终点 | sealed paired analysis | typed verdict | arrays/tables/figures |

## 14. Algorithm, Output, And Provenance Contract

每个任务记录 source/config/artifact/checkpoint hash、恢复步数/token、token-order hash、ramp state、student/teacher branch、LB gradient、TensorBoard、milestones 与 exact recovery。使用新输出根，禁止覆盖 A16_01。

## 15. Success / Failure / Insufficient Evidence

- Full Pass：Conditional 在两个 seed 上同时优于 Native、Raw、Haar。
- 仅效用监督支持：Conditional 与 Raw 优于 Native，但 Conditional 不优于 Raw。
- 无条件方向身份：Conditional 不优于 Haar。
- Fail：合格 endpoint 不支持注册正结论。
- Insufficient：有效性 guard 或必要 endpoint 失败。

## 16. What This Cannot Claim

即使 Full Pass，也不能证明跨尺度普遍性、语义层级、公共谱基，或专家专业化是 NLL 改善的唯一中介。

## 17. Block Confirmation, Freeze, And Amendment Ledger

A-G 已确认，跨块一致性 PASS。用户批准 smoke 通过后按方案自动提交，但 E01 Pass 仍是 fail-closed 条件。启动后若改变目标权重、ramp、特征、checkpoint、数据、seed、主指标或 verdict，必须追加 amendment。commit、push、sync、graph 与 publication 未授权。

