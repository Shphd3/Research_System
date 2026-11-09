# S7 两组适配实验：开发集与可回滚更新分析

**状态：开发集与预设 rollback 已分析；CONFIRM 未解封。** 本文是可复核的阶段性读数，不是 `summary.md` / `detailed.md` 的正式确认结论，也不替研究者更新 Anchor 或 Focus 的科学判断。执行依据是 [Protocol](../../../../../experiments/A17/17_05_shared_parameter_interference/20260924/protocol.md) §§9–13、18；问题边界见 [Anchor](../../../../../problem_anchors/17_shared_and_interference_learning/17_05_shared_parameter_interference/17_05_shared_parameter_interference_anchor_cn.md)。

## 直接结论

1. **A、B 单独都能学。** 每组只训练自己的秩 16 适配器，在开发集上从同一未适配起点持续降低下一词元损失。末点 A 约降低 0.086、B 约降低 0.065 nats/词元；两个预定末端检查点和三个固定种子均改善。按 Protocol 中仍标为 AI 提案的 0.02 资格门槛，开发集 headroom 通过。此项只证明当前模型、数据、适配位置与训练预算下存在可测的泛化改善。
2. **共享秩 16 的 A 端有小幅拖累趋势，B 端差距更小。** 在相同本组 8,388,608 个有效预测词元、同一更新数和同一开发文档上，S16 相对 A-only 的末点损失高 0.00799；相对 B-only 高 0.00134 nats/词元。三个种子均为正，开发集配对区间也在零之上。A 的差距主要在中后期出现。该比较有单组全局批量减半等固有限制，且 DEV 已用于资格判断，不能代替独立确认集来定案。
3. **隔离没有解除这次可见的共享拖累。** D8 相对总参数量相同的 S16，在 A 和 B 都更差：等权平均差值 S16−D8 = −0.00900 nats/词元，三个种子同向。D8 胜过每词元活跃秩相同的 S8，也胜过等总容量、等负载的混合分组 R8；所以“按域分组在双秩 8 架构内有用”和“按域隔离胜过秩 16 共享”必须分开。本轮 DEV 只显示前者。
4. **预设早期 rollback 不支持稳定的局部跨组互损。** 从同一个 S16 step-64 状态只用 A 或只用 B 做一次虚拟更新，平均看源组变好，另一组也变好；相对于仅延续 Adam 历史动量的零新梯度分支，另一组仍平均获益。完整步长和半步长都这样。少量单批次分支确实使另一组损失上升，但没有形成跨种子、跨来源批次的总体伤害。这不能排除晚期状态或其他更新批次出现互损。

**当前能确定的范围：** 18 条正式训练轨迹和三套 rollback 已完成；上述方向是已观察到的开发集及诊断结果。**当前不能确定的事：** 独立确认集上的共享拖累是否成立、是否达到研究者认为有实际意义的幅度，以及两个 M2D2 配置之外的泛化。研究者要求数值判据保持灵活；为避免看过确认集后选判据，CONFIRM 继续封存。

## 设计与资格核对

| 项目 | 实际执行 | 对读数的影响 |
| --- | --- | --- |
| 起点 | 从第 1 次预训练更新起采用 \(\lambda_{rec}=0.1\) 的 S7，累计 21B 预训练词元；冻结主干及 SAE | 21B 指词元量，不是参数量；本轮仅最后一块 MLP 下投影的 LoRA 更新 |
| 六条件 | A-only-16、B-only-16、S16、S8、D8、R8；种子 17/29/43 | 六组均 1,024 次更新，各有 64 个 DEV/检查点网格 |
| 数据坐标 | 单组每步 8,192 本组有效词元；共享每步 A/B 各 8,192，总计 16,384 | 末点比较按各自本组曝光 8,388,608 词元，而非把共享总词元误当 A/B 曝光 |
| 硬件 | 种子 17 为四 H100 Reserved；29/43 为各四 5090 Spot | 同种子条件在同一设备上配对；种子与设备差异无法分离，不据此精确推断随机种子总体 |
| 数据含义 | M2D2 官方 Mathematics 与 Biology 两个配置，按连续空白行重建文章边界；原页面 ID 不可得，A 内容含非数学文本 | 结论仅针对这两个**配置定义的文本分布**，不能说纯数学与生物语义冲突 |
| 工程完成 | [完成审计](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/completion_audit.json)：18/18 曲线、64/64 各自网格、3/3 rollback；三个任务 `pt-x11lbx2o`、`pt-kftmbkdl`、`pt-b2b6dxgc` | 工程完整不等于科学假设已证实；CONFIRM 状态仍为 `NOT_RUN_SEALED` |

训练起点、批量、损失和检查点以 [Protocol](../../../../../experiments/A17/17_05_shared_parameter_interference/20260924/protocol.md) 及执行脚本为准。单组与 S16 使用同秩、同更新数、同本组窗口严格子序列；单组全局有效批量只有共享的一半。这种对照能量出**本配置下的共享相对落后**，不能把差值直接解释为另一组梯度的纯因果伤害。

## 逐文档开发集证据

下表中损失差用 nats/词元。DEV 每域 128 个独立派生文档窗口；在文档层保持条件和三个固定种子配对，重采样 2,000 次，RNG=20260924。区间只表示这些固定训练种子下的开发文档抽样变化；DEV 参与了资格判断，所以下表中的共享/隔离区间是**探索性区间**。

| 问题与差值定义 | 三种子均值 | 95% 配对区间 | 三种子方向 | 读法 |
| --- | ---: | ---: | --- | --- |
| A 单组可学：未适配 − A-only，step 1008 | +0.08681 | [0.07414, 0.10065] | 全正 | A 的独立改善明显 |
| A 单组可学：未适配 − A-only，step 1024 | +0.08606 | [0.07327, 0.09903] | 全正 | 末点仍保有改善 |
| B 单组可学：未适配 − B-only，step 1008 | +0.06472 | [0.06046, 0.06915] | 全正 | B 的独立改善明显 |
| B 单组可学：未适配 − B-only，step 1024 | +0.06484 | [0.06040, 0.06904] | 全正 | 末点仍保有改善 |
| A 共享拖累：S16 − A-only，step 1024 | +0.00799 | [0.00372, 0.01251] | +0.00579 / +0.00832 / +0.00987 | 正值即共享在 A 更差；幅度小于原提案的 0.01 点值 |
| B 共享拖累：S16 − B-only，step 1024 | +0.00134 | [0.00014, 0.00255] | +0.00154 / +0.00193 / +0.00054 | 同方向但更小 |
| 隔离主比较：S16 − D8，A | −0.01087 | [−0.01267, −0.00900] | 全负 | D8 在 A 更差 |
| 隔离主比较：S16 − D8，B | −0.00713 | [−0.00847, −0.00591] | 全负 | D8 在 B 更差 |
| 隔离主比较：S16 − D8，A/B 等权 | −0.00900 | [−0.01012, −0.00787] | 全负 | 固定总参数预算下 S16 更好 |
| 分组对照：R8 − D8，A/B 等权 | +0.00681 | [+0.00521, +0.00844] | 全正 | 按域分组优于本次固定混合分组 |
| 活跃秩参照：S8 − D8，A/B 等权 | +0.00376 | [+0.00236, +0.00526] | 全正 | 同为每词元秩 8 时，D8 更好 |

每个共享/隔离差值来自 [DEV 逐文档配对表](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/analysis/dev_terminal_analysis.json)；可学性读数来自 [预确认分析表](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/analysis/preconfirm_analysis.json)。图中的横轴是**每组自己看过的有效预测词元**，不是共享训练的两组总和；线是三个固定种子的均值，淡色范围是种子最小至最大值，不是置信区间。

逐文档损失在本地 H100 MIG 上重新计算；种子 29/43 的原训练工作节点为 5090。重算均值与工作节点 DEV 汇总的最大差异约 0.00023 nats/词元。A 的共享差和 S16−D8 方向远大于这一差异；B 的共享差较小，尤其区间下界只有 0.00014，因此应视为很弱的 DEV 趋势，不能依它单独作最终判断。

![六条件开发集曲线](../../../../../../../../daily_research_reports/backup/2026/09/0924/figures/dev_curves.png)

曲线显示 A-only 与 S16 在早期近似、S16 曾短暂较好，随后 A-only 持续略好；B-only 与 S16 基本贴近。D8 优于 S8/R8，却在多数训练过程中落后 S16。这种次序限制了“隔离解除拖累”的说法；D8 减少每词元活跃秩也是不可消去的竞争解释。

## 预设 rollback：实际损失而非梯度角度

来源状态是各种子 S16 更新 64 次、总新增 1,048,576 有效词元的检查点。每个种子有 A 来源 32 组、B 来源 32 组，完整与半步长各一次，共 128 个独立回滚分支；另有两种步长的零新梯度但保留 Adam 动量对照。每个分支在独立 A/B 诊断文档各 128 个上读损失，之后恢复原参数和优化器状态。下表为三固定种子均值；区间对来源批组和目标文档两层配对重采样 2,000 次，双侧 97.5%。负值表示读出损失下降。

| 来源更新 | 步长 | 来源组相对原状态 | 目标组相对原状态 | 目标组相对零新梯度对照 |
| --- | ---: | ---: | ---: | ---: |
| A→B | 1.0 | −0.000532 [−0.000670, −0.000399] | −0.000346 [−0.000471, −0.000227] | −0.000405 [−0.000543, −0.000263] |
| A→B | 0.5 | −0.000319 [−0.000424, −0.000209] | −0.000269 [−0.000366, −0.000171] | −0.000181 [−0.000274, −0.000092] |
| B→A | 1.0 | −0.000375 [−0.000506, −0.000240] | −0.000488 [−0.000619, −0.000350] | −0.000472 [−0.000597, −0.000347] |
| B→A | 0.5 | −0.000284 [−0.000382, −0.000193] | −0.000301 [−0.000417, −0.000187] | −0.000215 [−0.000321, −0.000101] |

完整 384 个单批次分支中有 14 个使目标组的 128 文档平均损失上升，均在种子 43；其中 9 个同时改善来源组。这说明个别更新可能互损，但 Protocol 的**预定总体方向判据未满足**。平均读数甚至指向正向迁移。它只覆盖 step-64 的局部状态、所选来源批组和学习率，不能宣称不存在任何晚期或稀有的有害更新。原始逐分支数据见三个任务各自的 `formal/diagnostics_seed*/branches.jsonl`，完整聚合见 [预确认分析表](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/analysis/preconfirm_analysis.json)。

## 冻结 SAE 面板归档（辅助，不参与干扰判定）

已按 Protocol §11.4 在未适配 S7 起点处理预先指定的 DIAG_READOUT A/B 各 128 个窗口，每窗 512 个位置。归档含输入词元序列 SHA-256、位置、原生注意力输出 \(a\) 的逐记录均值与均方根、每位置 SAE Top-32 索引/系数及相对重构误差。A/B 的平均相对重构误差分别为 0.0621/0.0589；这只是该固定面板的重构描述，不证明 SAE 特征具有领域语义，也不证明其预测共享拖累。完整文件及 SHA 见 [SAE 归档收据](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/analysis/sae_diag/sae_diag_receipt.json)；读出代码 SHA-256 为 `c0cfdacc92e3fdffd5904a15ccf22061b4216fd2e5771f1406ac6b497537ff21`。

## 证据边界与下一步

- **直接观察：**两组单学有效；末点 S16 对单组尤其 A 有小幅落后；D8 优于 S8/R8 但输给 S16；预定早期 rollback 的总体跨组效应是改善而非伤害。
- **允许的解释：**本配置下共享相对单组有 A 向的小幅代价，同时完整共享秩 16 对两个双专家秩 8 的最终效果更好；这与活跃容量及正向迁移共同存在相容。
- **尚不能声称：**确认过的共享干扰、隔离缓解、A/B 纯数学/生物语义冲突、损失差的纯梯度因果机制、晚期完全无互损、自动路由能力。固定 A/B 外部标签和配置噪声也限制推广。
- **已冻结但未启用：**[确认分析代码与末点身份清单](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/analysis/preconfirm_freeze.json) 已生成，CONFIRM 文件仍未用于损失读出。原 Protocol 的 0.01 最小关注差异和相关区间仍标为 `AI_PROPOSAL`；研究者本轮要求先看趋势并保留数值灵活性，因此未将这套门槛升级成正式判据。
- **仍待完成：**正式 `summary.md` / `detailed.md` 和 Anchor 结果更新需独立确认读数与研究者的初始科学判断。SAE 固定面板现已归档，但没有任何针对其预测能力的独立检验。

## 溯源

| 证据 | 位置与身份 |
| --- | --- |
| 数据身份 | [manifest](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/data_v1/data_manifest.json)，SHA-256 `9b62a1ee3c424e00a30387d08bba7c6b536ab2fb11fc1eff5545be210fa3e1f9`；[数据审计](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/data_v1/data_audit.json) |
| 运行完成 | [completion_audit.json](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/completion_audit.json)，SHA-256 `824d5237598c46599ed441be782ed8207e8966dd18ea7b7d1c785adf6559dc38` |
| 开发集可学性与 rollback | [preconfirm_analysis.json](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/analysis/preconfirm_analysis.json)，SHA-256 `f4cde6a6a0328a425c87177bd8b9a66f1350438695668c6f4e5e9504f6d20167` |
| 六条件末点配对 | [dev_terminal_analysis.json](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/analysis/dev_terminal_analysis.json)，SHA-256 `658661c202025377ae6a797a5ddd18e256a0fd1e51de6f5e674ec4c7565d2ef1` |
| 阅读图 | 本日期 `figures/dev_curves.png`，来源为执行目录同名图，双方 SHA-256 `9b6505ea6f787ddec15fd518131e7b5650985e79aa65814b43285ba9ef907b79` |
| 冻结清单 | [preconfirm_freeze.json](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/analysis/preconfirm_freeze.json)，SHA-256 `31c4b5700f15ae3a3ec6bef31ae6c5946d733714b27700cbbc69748f7c0e5978`；包含 18 个末点检查点和分析代码 SHA-256 |
| SAE 辅助面板 | [sae_diag_receipt.json](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/analysis/sae_diag/sae_diag_receipt.json)，SHA-256 `056daa4568673cf7912b65e500e8e02e750ce5cfa665bcfd39f51c8932453a77`；A/B 原始压缩归档及输入哈希在收据中 |

上述数值在 2026-09-24 的本次读数上成立；如果之后更改判据、数据或代码，应以新修订与新产物单独登记，不反写本次观察。
