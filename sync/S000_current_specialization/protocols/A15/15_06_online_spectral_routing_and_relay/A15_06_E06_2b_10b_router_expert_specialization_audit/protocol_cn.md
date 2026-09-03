---
experiment_id: A15_06_E06_2b_10b_router_expert_specialization_audit
anchor_id: 15_06_02_router_expert_specialization
status: approved_for_implementation_smoke_and_full_evaluation
approved_by: user
approval_date: 2026-08-10
design_revision: A15_06_E06-v1
design_frozen_at: 2026-08-10T13:00:00Z
resource_profile: 5090-8-spot
primary_metric: paired_document_difference_in_10b_counterfactual_expert_choice_regret
---

# Protocol：A15_06_E06 Router--Expert 专业化与利用审计

## 0. Approval Snapshot

**文档状态：** `APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_EVALUATION`。  
**批准状态：** 研究者于 2026-08-10 批准五臂、单 seed、2B/5B/10B 的规模与直接执行。  
**区块审计：** A--G 全部 `CONFIRMED`；跨区块一致性 `PASS`。  
**已批准执行范围：** 实现、单元测试、smoke、一次单节点 8×5090 冻结评估、聚合、制图、结果记录与所属 Anchor 证据更新；不含发布、Git commit/push、root sync 或 graph 修改。  
**目的：** 判断 covariance 排名的 H/M/T 路由是否比同维随机瓶颈形成并利用更强的 token 条件化专家专业化。  
**实验角色：** 冻结根因/指标审计；不训练模型、不构造训练方法。  
**最小设置：** 五个具有可微 LB 的 seed-17 模型，在 2B、5B、10B 上对固定 held-out 文档做八专家反事实；一次只改变一个目标 token 的一个目标层。  
**处理与对照：** Local-HMT 对 Local-Random-Matched、Relay-HMT 对 Relay-Random 检验 covariance 身份；Vanilla-Full 是完整表征参考。  
**保持不变：** 架构、seed、训练数据顺序、tokenizer、训练 token 数、可微 microbatch Switch LB、评估文档、目标位置、干预幅度、专家数与统计规则。  
**主指标：** Router 选专家遗憾，单位 nat/token，越低越好。  
**Pass：** HMT 相对匹配随机臂在 10B 同时降低遗憾、提高 Router 分数与专家效用的秩一致性，文档配对 95% 区间与 Holm 校正符号翻转检验均支持相同方向。  
**Fail：** 所有有效性护栏通过，但两个 HMT 路径都没有取得上述双指标证书。  
**Insufficient：** 任一必要 checkpoint、配对 token、no-op 重放、同输入 CKA、模型状态不可变性或主结果产物失败。  
**不能声称：** 专业化导致终点 NLL、PCGrad 对本模型有效、H/M/T 有普遍语义，或结果能跨 seed/尺度推广。

## 1. Terminology / Definitions

- **稀疏专家：** 每个 block 中由 Router 选择的八个 MLP。共享专家始终运行，不参与 Router 选择，也不与稀疏专家混合统计。
- **反事实专家效用：** 只在一个目标 token 的一个层强制使用某稀疏专家，其他 token 和层保持原生路由时得到的下一词 NLL。
- **选专家遗憾：** 原生选择的专家 NLL 减去八个强制专家中的最小 NLL。零表示 Router 选中了即时反事实最优专家；它不测长期训练价值。
- **线性 CKA：** 对相同输入上的两位专家输出做中心化核对齐，衡量样本间相似性几何是否相同。它对正交换基和整体等比例缩放不敏感，但不对任意可逆变换不敏感；单独低 CKA 不能证明有用专业化。
- **主参数子空间：** 拼接 `gate_proj` 与 `up_proj` 的前若干右奇异输入方向，或 `down_proj` 的前若干左奇异输出方向。
- **Oracle 最优专家：** 对某目标产生最低强制 NLL 的专家。其身份必须随 token 改变，替换代价才支持条件化专业化，而非一个全局最优专家。
- **PCGrad：** 训练时投影多目标冲突梯度的算法；本轮只解释，不在冻结、无 backward 审计中执行。

## 2. Anchor Alignment

父 A15_06 的结果没有稳定证明 covariance 身份优于随机匹配路由，也不能说明专家专业化是否介导 NLL 差异。本实验只判断这一机制条款，不改变父实验的终点 NLL 问题。主证伪条件是：专家可能在几何上不同，但 Router 不按 token 特异效用选择它们。

## 3. Tested Hypothesis

在 10B 时，Local-HMT 或 Relay-HMT 应当相对匹配随机臂同时降低即时选专家遗憾，并提高 Router logits 与强制专家效用的 token 内排序一致性。辅助证据梯应从参数空间差异，推进到同输入输出差异，再推进到具有 token 变化 oracle 身份的非零替换代价。2B→5B→10B 轨迹用于判断这一关系是否随训练形成，而非只看终点快照。

## 4. Rival Explanations

1. 任意稳定瓶颈：随机匹配路由产生同等分化和选择质量。
2. 只有参数差异：权重子空间不同，但同输入功能冗余。
3. 专家不同但 Router 不会利用：输出与替换代价不同，Router 分数却不排序效用。
4. 全局单一优势专家：几乎所有 token 的 oracle 都相同，不是条件化分工。
5. 路由幅度伪影：主干预继承原生 top-1 概率；单位幅度敏感性用于检查是否依赖该标量。

## 5. Data Construction And Provenance

冻结评估源为：
`/data/250010109/MoE_Router/experiments/20260802_a15_01_04_progressive_band_source_2b_5090/artifacts/eval_tokens.pt`。
文件 SHA-256 为
`5c8cca2b0821f25b8e7abc50d7653dfba8d71e9ccf167fee61b82624116a52e4`；
其中 `dclm` 张量形状为 `[1024,1024]`，训练 manifest 记录的 validation token SHA 为
`91acad820e5521832a4e54033fd062d4d275819856725d9803981c0c972a289c`。
不得按模型结果选文档或位置。

冻结两个嵌套样本：

1. **轨迹集：** 文档 0--63，绝对位置 `[128,310,492,674]`，共 256 个目标，用于 2B、5B、10B。
2. **10B 确认集：** 文档 0--127，位置 `[128,219,310,401,492,583,674,765]`，共 1,024 个目标。轨迹集是声明过的子集，不与确认集伪装成独立样本。

同输入专家输出集使用文档 0--63 与 128 个位置 `64+7j`，$j=0,\ldots,127$，每层共 8,192 个专家输入。统计独立单位是文档；位置、层、专家和专家对都是重复测量。

## 6. Learning Task And Permitted Supervision

本实验不拟合、不训练。对每个目标 token、层和候选专家，评估器预测原生下一 token 并记录 NLL。只允许读取 Router logits、原生专家、强制专家损失、专家输入、未乘路由权重的稀疏专家输出和专家参数。下一词标签只用于计算 NLL，不能选择文档、位置、子空间维度或 checkpoint。

## 7. Model / Architecture And Frozen Variants

每个 checkpoint 都是 E05 已验证的四层 H768 MoE：八个 top-1 稀疏专家、一个共享专家、专家宽度 1536，BF16 推理；训练时使用可微 microbatch Switch LB。

| Arm | Router 读取对象 | 证据角色 |
| --- | --- | --- |
| Vanilla-Full | 未中心化的本层完整表征 | 无限制参考 |
| Local-HMT | block 2--4 的动态本层 covariance H/M/T | 本层 covariance 处理 |
| Local-Random-Matched | 动态本层同维随机嵌套子空间 | 本层身份对照 |
| Relay-HMT | block-1 covariance H/M/T relay 到 block 2--4 | relay covariance 处理 |
| Relay-Random | 匹配随机 block-1 relay | relay 身份对照 |

共享专家、attention、residual stream、LM head 和全部参数冻结。禁止直接点乘 Router 权重与专家权重，因为 Router 输入和专家输入不是同一空间，Relay 尤其如此。

## 8. Training Objective And Optimization

没有优化。PCGrad 不运行：它需要分解 LM 与 LB 梯度并改变训练更新。评估使用 `torch.inference_mode()`，每个任务前后验证参数和持久 buffer hash 不变。

## 9. Conditions, Seeds, And Checkpoints

seed 固定为 17，五臂均评估：

| 标签 | optimizer step | 实际累计 token |
| --- | ---: | ---: |
| 2B | 2,544 | 2,000,683,008 |
| 5B | 6,358 | 5,000,134,656 |
| 10B | 12,716 | 10,000,269,312 |

15 个 checkpoint 必须位于
`/data/250010109/MoE_Router/outputs/online_spectral_router_training_lb_fixed/`
并匹配 step、模型 schema 和冻结 source manifest。本实验不使用 20B/25B/30B 状态。

## 10. Primary Metric And Frozen Analysis Plan

对文档 $d$、目标位置 $p$、层 $\ell$、原生选择 $s$ 与候选 $e$，令 $L_{d,p,\ell,e}$ 为下一词 NLL：

$$
r_{d,p,\ell}=L_{d,p,\ell,s}-\min_e L_{d,p,\ell,e}.
$$

10B 时先在每篇文档内平均位置，再等权平均四层。对两个匹配比较计算 HMT 减随机；负值表示 HMT 选得更好。第二个决策量是八个 Router logits 与 $-L_e$ 的 Spearman 秩相关文档均值差；正值表示 Router 更会按效用排序专家。

- 观测单位：目标 token × 层；独立单位：held-out 文档。
- 确认样本：10B 的 128 文档 × 8 位置；64 文档轨迹集只作描述。
- 不确定性：固定 RNG seed `20260810`，20,000 次文档配对 bootstrap，百分位 95% 区间。
- 检验：每个指标和匹配比较做 20,000 次文档配对符号翻转；每个主指标族内对两个比较做 Holm 校正。
- checkpoint：固定 10B，不做最优 checkpoint 选择。
- 缺失/离群：禁止按结果删除或 winsorize；文档失败若不能由同一冻结任务重建，则相应比较为 Insufficient。

结果类型为 `support_local`、`support_relay`、`support_both`、`mixed_not_supportive`、`no_covariance_specific_support` 或 `insufficient`。某路径通过要求：遗憾差 CI 低于零且分数—效用秩相关差 CI 高于零，并且二者 Holm 校正 $p<0.05$。次级指标不能挽救未通过的主结果。

## 11. Secondary Metrics And Guards

1. **margin—遗憾校准：** top1--top2 logit margin 是否越大、遗憾越低；只测置信度是否有意义。
2. **路由成熟度：** 同一目标在 2B→5B、5B→10B 保持专家身份的比例；只描述稳定性。
3. **参数子空间：** 对 `gate_proj+up_proj` 输入几何和 `down_proj` 输出几何，计算专家对主子空间的平均平方 canonical correlation。主 $k=\max(1,\lceil0.01\min(d_{in},d_{out})\rceil)$（约 8），并做 $k=16,32$ 敏感性与同维 Haar q95。
4. **同输入线性 CKA：** 八位专家读取完全相同的 8,192 个实际专家输入，在路由幅度和共享专家相加前比较输出。低 CKA 表示输出关系几何不同，不保证更有用。
5. **替换代价与 oracle 多样性：** 候选 NLL spread、原生到其他专家的损失增加、各专家 oracle share 与 oracle entropy。
6. **Router--Expert 经验耦合：** 在同一 token 上相关 $z_e-\bar z$ 与 $\|B_{e,k}^{\top}h\|^2/k$；$h$ 是实际专家输入，避免无效的跨空间权重点积。
7. **幅度敏感性：** 在 10B 把目标 routing amplitude 固定为 1 重跑反事实；若主比较方向反转，只能对原生幅度干预作有限解释。

E06 不测梯度冲突、PCGrad 训练干预、系统吞吐、capacity drop 或负载分析。

## 12. Known Good / Known Bad / Known Confusing Cases

- 已知正确：相同矩阵/子空间 overlap 和 CKA 为 1；正交换基保持 CKA；完全一致排序 Spearman 为 1；强制原生 expert 是 no-op。
- 已知错误：独立打乱样本破坏 same-input CKA；正交子空间 overlap 接近 0；倒序得 Spearman -1；一个 replica 改多个目标会污染因果干预。
- 易混淆：低参数 overlap 但 CKA≈1 是参数冗余；低 CKA 但 swap cost≈0 是无决策意义的输出差异；高 swap cost 但 oracle 只有一个专家是全局优势；遗憾更好但完整排序不更好可能只是 winner 校准。

## 13. Scientific Procedure And Stage Contracts

| 阶段 | 目标 | 输入/方法 | 输出 | 门与失败 | 产物 |
| --- | --- | --- | --- | --- | --- |
| S0 | 固化 provenance | 核对 15 checkpoint、数据、schema、step、模型状态 | 不可变 manifest | 任一不一致：Insufficient | `raw/provenance.json` |
| S1 | 验证数学实现 | 合成 known-good/bad 单测 CKA、秩、子空间、bootstrap | 测试报告 | 任一恒等式失败阻断 smoke | `tests/` 报告 |
| S2 | 真实 no-op smoke | Vanilla 2B、2 文档、2 位置、64 CKA 输入 | smoke verdict | NLL 误差 >2e-5 或状态变化阻断 full | `smoke_verdict.json` |
| S3 | 全量冻结审计 | 15 个任务分配到 8 GPU；每 replica 只干预一个目标 | raw arrays/summary | 缺任务使相应比较 Insufficient | worker `raw/` |
| S4 | 配对推断 | 冻结脚本做 bootstrap、sign-flip、matched contrasts | typed verdict/table | 配对失败：Insufficient | project `tables/` |
| S5 | 图和证据审计 | 按 plot contract 绘图并逐张打开 | audited figures | 图契约不符则不能最终化 | project `figures/` |

S0--S2 通过后才能扩展。NaN/Inf、OOM、checkpoint 损坏、分布式任务丢失、no-op 失败或模型状态变化停止受影响任务；科学结果差不得早停。

## 14. Algorithm, Output, And Provenance Contract

每个目标干预使用单独因果 replica，只改变一个目标层的一个目标 token，其他路由原样保留，并读取该位置预测下一 token 的 logits。主分析对八个候选专家使用相同的原生 top-1 概率；敏感性只把目标幅度改成 1，不改其他 token。

代码冻结在
`/data/250010109/MoE_Router/experiments/20260810_router_expert_specialization_e06_frozen_v1`；
raw 输出写入
`/data/250010109/MoE_Router/outputs/online_spectral_router_training_lb_fixed/e06_router_expert_specialization/`。
Research_System 只接收 Protocol、run receipt、紧凑表、图、`summary.md` 与 `detailed.md`；checkpoint 与 raw arrays 留在 worker。代码 manifest、环境、ACP job ID、命令及 raw-to-table 变换写入 `detailed.md`。

## 15. Success / Failure / Insufficient Evidence

- **Pass_Local / Pass_Relay / Pass_Both：** 相应匹配路径通过两个主量；专业化证据梯再区分“利用不可互换专家”还是只有功能选择信号。
- **Fail：** 护栏通过，但两个 HMT 路径均未通过双指标，否定注册尺度上的 covariance 特异冻结功能证书；不证明专家相同。
- **Mixed：** 单指标或未校正比较有利，但完整证书不通过，按“不支持”报告。
- **Insufficient：** provenance、no-op、目标隔离、状态不变、同输入条件、checkpoint 完整或主聚合失败。

## 16. What This Cannot Claim

即使 Pass，也不能证明专业化导致终点 held-out NLL，不能建立 covariance 频带的普遍语义、跨尺度/深度 Relay 规律、跨 seed 复现，或 PCGrad 应被采用。CKA 与参数 overlap 是描述性表征指标；遗憾是一 token 的冻结干预，不是联合训练反事实。

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | 状态 | 依据 |
| --- | --- | --- |
| A 问题与边界 | CONFIRMED | 研究者批准 Router 功能与专家专业化范围 |
| B 数据与 provenance | CONFIRMED | 研究者批准规模；held-out artifact 已核验 |
| C 任务与监督 | CONFIRMED | 冻结下一词反事实效用 |
| D 架构 | CONFIRMED | 五个 valid-LB E05 arm、seed17、共享专家单列 |
| E 目标/优化 | CONFIRMED | 不训练/不 backward；PCGrad 不执行 |
| F 比较/证据 | CONFIRMED | regret、分数—效用、CKA、专业化证据梯 |
| G 执行 | CONFIRMED | 实现、smoke、8×5090 full 与记录均获授权 |

跨区块一致性在实现前通过。科学合同以 `A15_06_E06-v1` 于 front matter 时间冻结。执行开始后，只能追加状态、结果链接或说明 eligibility 的 amendment；观察结果不得回写并改变注册设计。

### E06-AM01 — 数值精确的目标 token 局部反事实实现

- **修订时间：** 2026-08-10T13:45:00Z。
- **修订前：** 第一次 smoke 通过模型的 batchwise forced-assignment hook 改目标专家，并与不同 prefix/batch 形状的原生 forward 比较。
- **修订前已见结果：** 尚未看到任何科学 arm 比较；smoke 的原生专家重放最大相差 0.0533 nat/token。定点诊断表明，同一执行形状内相同路由的 logit 误差精确为零，差异来自 BF16 kernel 随序列长度和专家分组 batch 形状变化。
- **修订后：** 八个候选、Router logits 与 no-op 参考使用完全相同的 prefix 和 replica 形状。在目标 MLP 输出处，原生幅度干预加入 $w(e_{candidate}(h)-e_{selected}(h))$；单位幅度敏感性加入 $e_{candidate}(h)-w e_{selected}(h)$。所有非目标 token 与原生共享专家输出保持 bitwise native。
- **原因：** 消除执行形状数值噪声，同时保持注册对象不变：一个目标 token、一个目标层、一个候选稀疏专家，其余计算原生。
- **受影响区块：** 仅科学过程和实现身份；问题、数据、checkpoint、指标、聚合、裁定和结论边界均不变。
- **批准依据：** 该实现修复属于用户已批准范围，不改变科学问题或五臂合同。
- **证据资格：** 修订前失败 smoke 不可用；重复 smoke 可用：原生专家 no-op 误差 0、完整序列与 prefix 专家身份 mismatch 0、Router replay 1.0、模型状态 hash 不变。

### E06-AM02 — 同一次前向内的原生控制 replica

- **修订时间：** 2026-08-10T13:27:00Z。
- **触发条件：** 第一次 full 尝试 `om-h9f7rog8` 在产生科学结果前，八个首批任务全部失败。尽管被选专家候选的干预增量在代数上严格为零，它与单独 native forward 的 NLL 仍相差 0.0176--0.0931 nat/token。
- **根因：** 八个候选 replica 共享一次 forward；另外七个反事实改变了下游 MoE 的专家分组大小，BF16 grouped-GEMM 的 kernel 选择随之变化，数值上扰动了本应原生的 replica。目标干预本身没有越界，问题在于 no-op 参考没有共享同一个下游 batch 环境。
- **修复：** 每篇文档在同一次 forward 中使用九个 replica：八个专家候选，加一个显式原生控制。被选专家候选与原生控制都获得严格为零的增量，并共享完全相同的下游分组影响；八个科学候选本身不变，候选 NLL 改为相对该同 forward 控制解释。
- **受影响区块：** 只有数值控制实现与 worker source identity；问题、checkpoint、目标位置、规模、指标、统计推断、裁定和结论边界均不变。
- **证据资格：** `om-h9f7rog8` 是不可用的工程尝试。新的 full 必须重新通过单元测试与真实 checkpoint no-op smoke。
