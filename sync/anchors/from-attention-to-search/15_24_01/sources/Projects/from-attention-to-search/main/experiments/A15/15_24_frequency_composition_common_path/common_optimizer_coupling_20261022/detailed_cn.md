# Detailed：common 梯度通过全局裁剪产生的耦合

[English](detailed.md) · [Summary](summary_cn.md) · [Protocol](protocol_cn.md) · [产物清单](artifact_manifest.json)

主归属：[A15_24_01](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_01_common_optimizer_coupling_anchor_cn.md)。四个计划模型全部完成，每个均为 168 次更新、85,548 个有效目标。工程资格与独立结果审计通过，证据可用于预定的**探索性**策略比较。低频宏平均变化为 -0.000332028 和 +0.000529222，未满足双种子改善规则。研究者的机制判断与科学关闭状态保持 Unknown。

## 1. 问题、对象与实际比较

父实验保留两个频率路由专家并新增 always-on common；全局裁剪更频繁，却没有稳定低频收益。本轮检查裁剪分母产生的优化耦合，与另一个对话的 feature 关系/冻结表征研究互补：这里不改变输入、feature 分组、路由或架构。

一个有效训练位置是缓存回答预测 hidden 向量及原 next-token 目标。冻结 Qwen3-0.6B block-28 hidden state 为 1,024 维 BF16。八个无 bias、宽 1,024 的 SwiGLU 专家沿用保存的 T_F top-2 路由，权重 0.5/0.5。第九个 common 始终调用，系数为 1。每个专家读取相同完整 hidden state，经原 TRAIN RMS 归一化；分支输出缩放后加回，再经过冻结最终 norm/head。仅九个模块可训练，T_F 没有可训练 router。

对照用一个全局系数裁剪所有原始梯度；处理只用路由梯度计算路由系数，common 继续使用原全局系数。架构和容量相同。完整轨迹分开后，common 的后续学习可以改变；只有固定状态影子对照把它的当步更新保持完全相同。

预期是在两个种子上都降低最终低频宏平均 NLL。最强竞争解释是 AdamW 吸收梯度缩放，或者轨迹改变并不能改善预测。本实验识别指定策略的总效应，不声称原 baseline/common 差异被裁剪完全中介。

## 2. 裁剪如何进入 AdamW

完整有效批次累积结束后，以 \(g_R\) 表示拼接的路由参数原始梯度，\(g_C\) 表示 common 原始梯度，均未裁剪。阈值为 1 时，

\[
q=\min\{1,1/(\sqrt{\lVert g_R\rVert^2+\lVert g_C\rVert^2}+10^{-6})\},\qquad
r=\min\{1,1/(\lVert g_R\rVert+10^{-6})\}.
\]

对照把 \((qg_R,qg_C)\) 交给 AdamW；处理交给 \((rg_R,qg_C)\)。修改任何梯度之前先计算全部范数。1e-6 属于裁剪稳定项，AdamW epsilon 另为 1e-8。

对一个参数坐标，以 \(g_t\) 表示原始梯度、\(c_t\) 表示裁剪系数、\(\eta_t\) 表示学习率、\(m_t,v_t\) 表示一阶/二阶矩状态、\(\lambda\) 表示权重衰减，则

\[
m_t=0.9m_{t-1}+0.1c_tg_t,\quad
v_t=0.95v_{t-1}+0.05c_t^2g_t^2,\quad
\Delta\theta_t=-\eta_t\frac{\widehat m_t}{\sqrt{\widehat v_t}+10^{-8}}-\eta_t\lambda\theta_{t-1}.
\]

帽号是通常的偏差修正。统一正标量保持当前原始梯度的方向，但经过历史矩累积及逐坐标归一化之后，不必保持更新方向。第一步矩状态为零时，自适应项化为 \(-\eta_1c_1g_1/(|c_1g_1|+10^{-8})\)，非近零坐标上的尺度大部分抵消。实际测量的参数移动还包含 weight decay 和舍入。

在第 1/42/84/126/168 次更新前，实现复制参数、Adam 状态与原始累积梯度，无额外 backward 地计算两策略；真实更新仍使用该 run 指定策略。记录每种更新范数、差向量范数除以 global 更新范数、余弦以及 common 更新相等性。影子计算不额外增加目标计数。

**实际例子：种子 11 的 global 轨迹第 42 步。**原系数为 0.774878294，独立路由系数为 1。两策略的路由更新范数分别为 0.354099235 和 0.364755159，范数增加 3.0093%；差向量范数为 0.035335699，占 global 更新的 9.9790%；余弦为 0.995605965，夹角为 5.3731 度。common 更新完全相同。这几个百分比回答不同问题，不能互换。[原始步骤记录](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/training/global/seed11/steps.jsonl)

## 3. 登记设置与工程资格

| 项目 | 实际设置及证据 |
|---|---|
| 冻结 | 2026-10-22 上海时间 23:35:06（UTC 15:35:06）；[冻结哈希](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/provenance/design_freeze.json) |
| 授权范围 | 用户授权自主完成不同的机制分析；四个本地 T_F plus-common 模型；没有远端提交 |
| 数据 | Tulu revision 6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752；TRAIN 1,024 对话/85,548 目标，EVAL 256/22,446，DEV 128/10,340 |
| 标签 | 只包含回答 next-token 和 EOS；prompt/padding 目标为零；归一化 prompt 重合为零；近重复/Base 预训练独立性 Unknown |
| Feature | 同一 14 层、16,384 feature CrossCoder；阈值 0.051281172782182693；原冻结频段/路由 |
| 模型 | 九个宽 1,024 的 SwiGLU，共 28,311,552 个可训练参数；Base/字典/head 冻结；没有 router、辅助 loss 或 dropping |
| 目标 | 有效 target 交叉熵，微批次求和后除以实际有效批次 target 数 |
| 优化 | AdamW 3e-4，betas .9/.95，eps 1e-8，weight decay .01；原 9 步 warmup 与 cosine 末比例 .1 |
| 曝光 | 微批次 128、有效批次 512、尾批次 44；每模型 168 步、85,548 目标 |
| 条件 | global/route_isolated，各种子 11/22；原共享初始化和顺序 |
| 保存 | 初始完整状态及 1/42/84/126/168 步完整状态；final_resumable.pt 硬链接 step168；不选最佳点 |
| 评价 | TRAIN/EVAL 在 0/42/84/126/168；四终点完成后才评价 DEV；固定 final168 |
| 设备 | 现有本地 NVIDIA H100 80GB HBM3 MIG 3g.40gb；torch 2.3.0a0+6ddf5cf85e.nv24.04；两个 CPU 线程 |
| 资源 | 进程活跃时间合计 307.246 秒，上限 1,200 秒；没有失败调用；单模型训练过程约 65.6–66.3 秒 |

[数据说明](dataset_guide_cn.md)绑定各 split JSON、目标构造、标签支持与源身份。必需输入 ID 记录在[config](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/config/frozen.json)，加载前完成[本轮访问检查](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/provenance/inputs_access.json)。代码、config、Protocol 哈希固定。复用原冻结缓存模型、评价器和 schedule；调整裁剪、完整里程碑保存及影子测量。

[工程检查](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/qualification/receipt.json)通过：global 更新与原实现一致、无 common 时两策略相等、common 影子更新相等、标签正确、两策略恢复后下一步模型/优化器/指标精确相等、必需 TensorBoard 标签有限、目标计数 512/1024 正确。影子测量不替代终点检验。

## 4. 协议符合性、偏差与证据资格

| 登记项目 | 实际检查 | 状态与影响 |
|---|---|---|
| 四次同环境训练 | 全部完成，绑定固定 config/代码哈希 | PASS；本轮策略比较有效 |
| 相同预算/路由 | 全部 168 步/85,548 目标，配对逐步路由曝光相等 | PASS；没有曝光混淆 |
| 标签/冻结对象 | 来源、标签和冻结检查通过 | PASS |
| 二十次固定状态比较 | 四 run × 五步，common 更新完全相同，额外 backward 为零 | PASS；当步优化器比较有效 |
| 终点聚合 | 独立审计不导入训练器，从 DEV NLL 数组和原 feature CSR 重算，与配对 CSV 误差为零 | PASS |
| 历史重放 | 初始 TRAIN/EVAL 数组相同，训练后旧/新 global 不同 | 历史比较 BOUNDED，不混合旧新 |
| 保存契约 | 中期保存完整状态，并增加 step1，而非只有权重 | 启动前已声明；增强恢复能力、不改变学习 |
| 冻结正文草稿措辞 | 最后追加 freeze receipt 覆盖早先 pending 描述；独立 qualification receipt 记录后续 PASS | 保留行政时间边界，不事后改写 |
| 失败、重试、排除 | 工程检查、四 worker、最终评价共六次调用全部完成 | 本轮无遗漏种子或结果选择 checkpoint |

DEV 已暴露、仅两个种子、没有低频 feature 达到 20 个 DEV 命中。数值比较合格也不能消除这些抽样限制；没有独立确认集。完整性与指标资格来自独立审计，而非任务状态标签。[审计记录](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/independent_audit/audit.json)

## 5. 指标、终点与学习轨迹

低频 feature 宏平均先平均每个有支持 feature 的激活位置 NLL，再对 838 个有支持 B1 feature 等权平均。原池 1,694 个，856 个无支持。整体 NLL 平均全部 10,340 个 DEV 位置；低频并集平均 1,701 个不重复位置。feature 事件重叠；两个种子是训练重复单位。不作显著性或把 feature 当独立样本的推断。

最终 DEV 前固定的主符号规则是：两种子 isolated 减 global 均为负才探索性支持；方向混合不符合稳定改善；均非负不支持；缺失/无效为证据不足。实际结果是**方向混合**，不是执行失败。

| 策略 | 种子 | DEV 整体 | DEV 低频宏平均 | DEV 低频并集 | DEV 高频宏平均 |
|---|---:|---:|---:|---:|---:|
| Global | 11 | 1.226603156 | 1.056352688 | 1.063884757 | 1.192203082 |
| Isolated | 11 | 1.226504336 | 1.056020660 | 1.064022403 | 1.192145080 |
| Global | 22 | 1.227334069 | 1.057152509 | 1.063403929 | 1.192921787 |
| Isolated | 22 | 1.227341095 | 1.057681732 | 1.063815882 | 1.192944507 |

| 种子 | 整体差值 | 低频宏平均差值 | 低频并集差值 |
|---|---:|---:|---:|
| 11 | -0.000098819364 | -0.000332028097 | +0.000137646481 |
| 22 | +0.000007025948 | +0.000529222412 | +0.000411952484 |
| 均值 | -0.000045896708 | +0.000098597157 | +0.000274799482 |

决定性来源是[条件结果](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/analysis/condition_results.csv)和[配对比较](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/analysis/paired_comparisons.csv)。种子 11 的 DEV 改善/变差/相等位置数为 5,027/4,934/379，种子 22 为 4,830/5,109/401。这些计数描述异质性，不是独立试验或新的成功判据。

| 策略 | 种子 | 最终 TRAIN 整体 | 最终 EVAL 整体 | 路由裁剪步数 | 路由累计路径 |
|---|---:|---:|---:|---:|---:|
| Global | 11 | 0.897871470 | 1.221650079 | 161 | 37.528428 |
| Isolated | 11 | 0.900642155 | 1.221437095 | 21 | 36.521194 |
| Global | 22 | 0.900176130 | 1.220305537 | 160 | 37.460139 |
| Isolated | 22 | 0.902447295 | 1.220278808 | 18 | 36.499159 |

全部五个里程碑轨迹保存在各条件的 `metrics_step*.json`、`train_step*.npz`、`eval_step*.npz`。累计路由路径对每步八个专家联合参数更新范数求和，排除 common 和 router，不是净位移。处理的路径下降 2.6839%/2.5653%，虽然裁剪减少。当步影子与完整轨迹条件于不同历史，因此两者并不矛盾。

## 6. 固定状态更新与历史证据

表中分别为每条实际轨迹上的影子 isolated/global 更新范数比、相对向量差与夹角。范数比接近 1 不意味着向量相同。所有行的 common 更新完全相同。

| 实际策略 | 种子 | 步数 | 更新范数比 | 相对向量差 | 夹角／度 |
|---|---:|---:|---:|---:|---:|
| Global | 11 | 1 | 1.000362 | 0.002778 | 0.158 |
| Global | 11 | 42 | 1.030093 | 0.099790 | 5.373 |
| Global | 11 | 84 | 1.013573 | 0.042859 | 2.314 |
| Global | 11 | 126 | 1.000000 | 0.000000 | 0.000 |
| Global | 11 | 168 | 1.045434 | 0.156135 | 8.378 |
| Global | 22 | 1 | 1.000320 | 0.002466 | 0.140 |
| Global | 22 | 42 | 1.028893 | 0.097240 | 5.246 |
| Global | 22 | 84 | 1.012151 | 0.037086 | 1.996 |
| Global | 22 | 126 | 1.010867 | 0.030312 | 1.613 |
| Global | 22 | 168 | 1.051217 | 0.157107 | 8.307 |
| Isolated | 11 | 1 | 1.000362 | 0.002778 | 0.158 |
| Isolated | 11 | 42 | 1.022951 | 0.087289 | 4.772 |
| Isolated | 11 | 84 | 1.011998 | 0.040574 | 2.208 |
| Isolated | 11 | 126 | 1.000000 | 0.000000 | 0.000 |
| Isolated | 11 | 168 | 1.042663 | 0.151151 | 8.143 |
| Isolated | 22 | 1 | 1.000320 | 0.002466 | 0.140 |
| Isolated | 22 | 42 | 1.022927 | 0.086841 | 4.746 |
| Isolated | 22 | 84 | 1.011336 | 0.035623 | 1.924 |
| Isolated | 22 | 126 | 1.010515 | 0.030095 | 1.607 |
| Isolated | 22 | 168 | 1.047938 | 0.152017 | 8.081 |

第 168 步的尾批次只有 44 个目标而非 512，其较大差异不能解释成干净的时间增长趋势。这五批次是固定诊断点，不是所有更新效应分布的估计。独立审计保留精确值与源哈希。

历史观察在干预登记前已知。旧 MoE/T_F × 种子 11/22 中，新增 common 后路由路径分别增加 1.9560%、1.9162%、2.3090%、2.1547%。首步裁剪系数比为 0.576727/0.602401/0.562662/0.598823，实际更新范数比为 0.999579/0.999589/0.999639/0.999680。日志只保存原始梯度范数，没有原始向量。这反对总体移动量减少的简单描述，未排除所有优化机制。[历史来源审计](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/observational/saved_step_analysis.json)

新 global 减旧 global 的 DEV 低频宏平均约为 -0.0005581/-0.0006180，与本轮干预效应同量级，因此不能用历史对照替代本轮本地重跑对照。跨环境数值分歧的精确原因不由本实验识别。

## 7. 三项紧凑审计与证据链

**研究识别审计——限定范围内 PASS。**架构、容量、频率分组、顺序和曝光固定。影子对照只改变路由系数，common 更新保持相同；完整重训测量之后状态反馈。可识别当前设置中的策略效应；完全中介、feature 语义和 Rank-one 声明不在此比较范围。

**数据统计审计——探索指标 PASS。**原 split/标签与 target 数核实。独立地用原 NLL 与 feature CSR 重算，配对差值完全吻合。无支持 feature 保持无支持，重复 feature 事件不视作独立。DEV 暴露、支持稀疏及双种子限制推广。没有按结果删样本、分箱或选择 checkpoint。

**实现数值审计——PASS。**global 原行为和无 common 等价性通过；两策略恢复后模型/优化器/指标相等、head 冻结、计数器、有限 TensorBoard 标签和二十次 common 更新相等均通过。四份完成记录绑定冻结 worker/config。训练后旧新逐点相等失败，是保留的跨环境限制，不影响本轮同环境策略配对。[独立审计](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/independent_audit/audit.json)

| 声明 | 原证据及计算 | 观察 | 资格／边界 |
|---|---|---|---|
| 稳定低频收益 | 四个 DEV `.npz` 与原 CSR；worker metric_bundle 及独立 bincount 审计 | -0.000332028 / +0.000529222 | 探索性 ELIGIBLE；方向混合 |
| 分母改变 Adam | 四份 steps.jsonl 的固定状态影子 | 种子 11 第 42 步相对向量差 9.979%；common 相同 | 当步优化器效应 ELIGIBLE |
| 少裁剪不必移动更多 | 168 步 route_update_norm 求和 | 路径下降 2.6839%/2.5653% | 轨迹描述 ELIGIBLE；移动不是效用 |
| 原简单缩步解释 | 原八模型完整日志独立聚合 | 四组 common 路径均更长 | 观察性 BOUNDED；轨迹不同 |
| 完整性/工程 | qualification、四份 complete.json、终点评价、独立审计 | 条件与计数全部齐全 | 工程 PASS，不是科学关闭 |

实际输出登记为七项资产：两个工程检查状态、四个完整 checkpoint family、一项分析资产。七项本轮严格访问检查全部通过，四个最终模型/Adam 张量摘要均经独立 CPU 核验通过。执行目录含 26 个独立 checkpoint 文件，注册时共 7.433 GiB，final/step168 硬链接只计一次。完整登记身份及本轮访问证据见[注册记录](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/asset_registration/registration_complete_20261022T154307Z.json)及产物清单。可访问、精确恢复资格与科学效用分别成立。

## 8. 解释、覆盖与下一决策

直接观察建立了真实的裁剪到 Adam 影响，但预测后果混合。**AI 解释：**common 减少总体 Adam 移动、进而压制路由学习的简单解释被削弱；去掉其分母贡献在本实验不是稳定补救。函数共享、表征组织、特定坐标学习及其他优化交互仍未解决，也不能据此判定导师的 Rank-one intuition 或普通 MoE 行为。

| 请求工作 | 状态 | 证据 |
|---|---|---|
| 独立机制子问题 | DONE_EXPLORATORY | A15_24_01 与冻结策略比较 |
| 历史观察审计 | DONE_VALID | 原八日志与 saved_step_analysis.json |
| 四次完整训练 | DONE_VALID | 四份 complete.json，各 168 步 |
| 二十次固定状态比较 | DONE_VALID | 1/42/84/126/168 步；common 相等 20/20 |
| 终点预测比较 | DONE_EXPLORATORY | 双种子差值、原数组、独立审计 |
| 科学机制判断／关闭 | Unknown | 研究者审阅，不从执行推定 |

研究者拥有的唯一下一决策为 **Unknown**：混合结果是否值得继续这条裁剪策略。不会自动追加训练。仍未建立的具体联系是：局部优化器影响能否产生可复现预测收益。输入资产、实际输出注册状态、源/config 哈希、日志、checkpoint、分析版本及其用途见 [artifact_manifest.json](artifact_manifest.json)。本结果无需新图即可理解；来源表格承载决定性比较。
