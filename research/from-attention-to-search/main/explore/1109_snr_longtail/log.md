# 1109_snr_longtail：长尾为什么学得慢（信噪比视角）

活跃问题：#1 长尾学习的信噪比与信号集中　脚本：`/data/250010109/MoE_Router/experiments/20261108_snr_mig_pilot/code/stage3_probe.py`

本日志是探索车道的第一份试运行。下面第一条引用已完成的 R02（正式记录已存在，不重写），之后的迭代只在这里追加。

## 1108 21:00　一步更新的均值项与噪声项（R02，已完成）

- 假设：长尾学得慢主要因为信噪比低，而不是方向冲突。
- 先验→模型→计算：单 batch 梯度 = 平均梯度 + 零均值、方差 Σ/n 的误差，且 B 的损失局部向上弯 → E[ΔL_B] ≈ −η g_B·ḡ_A + (η²/2)tr(H_BΣ_A)/n + (η²/2)ḡᵀHḡ，交叉点 η\* = 2g_B·ḡ_A/(tr(HΣ)/n + ḡᵀHḡ) → 冻结 33B MoE，只让 block7 expert7 走一步 SGD，扫 η 与 n，比较均值分支与单 batch 分支
- 跑前预测：噪声项 ∝ η²/n 且跨组帮助在 η\* 翻转 → 进入 H2 训练比较；跨组方向项在所有 η 都伤害 → 转查方向冲突；区间盖过效应 → 加大抽样。
- 竞争解释：方向冲突（跨组一阶项为负）主导。
- 结果：噪声项 η 斜率 1.95–2.35、n 斜率约 −1；跨组一阶项 z=1.28（6 对全为帮助，3 对 z>2）；η\* 只到推导与事后估计（0.018/0.036/0.057）。原始数据：`/data/250010109/MoE_Router/experiments/20261108_snr_mig_pilot/results/`；正式记录：[R02 Summary](../../experiments/A17/17_13_ntp_statistics_local_compatibility/R02_20261108_snr_mig_pilot/summary_cn.md)
- 研究者决定：已授权 R03 教师路由信号集中训练（见 R03 protocol）；对 H1 的科学接受 Unknown。
- 链条位置：机制

今日认识更新：一步更新的后果由噪声项主导；能抬高可用学习率的是同一信号的重复次数（有效 n），不是“同一簇”本身。

## 1109 10:30　D1：$\bar M$ 随训练步数怎样变化（只读已存评估产物，探索性）

- 假设：A1 在 250–500 步领先、750 步后落后于 A0，是因为原生 router 早期还没形成集中，后来 $\bar M$ 超过 A1。
- 先验→模型→计算：可学 router 的集中度随 LM 梯度逐步形成，固定 teacher 分发的集中度只随 load bias 漂移 → 每个臂每步的 $\bar M_i=\frac1L\sum_l\sum_e\frac{c_i^{(l)}(e)}{k}\cdot\frac{c_i^{(l)}(e)\pi_i^{(l)}(e)}{p_i}$ → 读取 `eval/<arm>/stepXXXXXX.pt` 中每层集中度（训练时在 EVAL 2M token 上算好），对 A0、A1、A4、A1-deep 在 250–2000 步取全体与 bin0、bin9 中位数。
- 跑前预测（研究者预登记）：A0 的 $\bar M$ 中位数在 500–750 步之间超过 A1，与 A1−A0 符号翻转同步。成立 → “早期领先来自原生 router 尚未集中”得到时间上的相容证据，A1 的劣势是集中度不够而不是分发本身有害；不成立（A0 一开始就更集中，或交叉时间与 NLL 翻转不同步）→ 早期领先另有原因（如固定路由的优化更容易、warmup 期间学习率小），需另查。
- 竞争解释：warmup（前 1000 步线性升温）期间固定路由更易优化；NLL 翻转与集中度无关。
- 结果：**预登记预测不成立。** A0 的 $\bar M$ 中位数从第 250 步起就高于 A1（0.803 vs 0.547），之后升到 1.010；A1 稳定在 0.54–0.59。差值从 0.26（250 步）增到 0.39（750 步）后稳定在约 0.42；A1−A0 NLL 在 500→750 步由 −0.028 变 +0.045。与翻转同步的是 A0 集中度的增长（0.80→0.93），不是“A0 超过 A1”。早期领先另有原因（warmup、固定路由易优化等，未检验）。表/图：`daily_research_reports/1109/meeting_report/figures_tables/D1_Mbar_by_step.*`、`D1_Mbar_over_steps.*`；脚本 `/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/analysis/meeting_1109/build_tables.py`
- 研究者决定：Unknown
- 链条位置：机制

## 1109 10:30　D2：A1 的集中度损失在哪里（离线、只前向分数，探索性）

- 假设：A1 的 $\bar M$（0.586）远低于 A0（1.010），主要因为分发规则本身稀释了 teacher 信号。
- 先验→模型→计算：teacher 分数 $s_{t,e}=\hat a_t^\top\mu_e$ 是余弦量级的小数，而 $b_e$ 每步按 ±0.001 漂移，2000 步后可能与分数同量级甚至更大，从而让 Top-2 由负载均衡而不是 teacher 决定；Top-2 的第二选择也可能是噪声 → 在 EVAL 上用同一组 teacher 分数离线重算 $\bar M$：(a) $b=0$；(b) A1 第 2000 步实际的逐层 $b$；(c) 只取 top-1（$k=1$）；(d) 权重按相似度 softmax（硬选择的 $\bar M$ 不含权重，另报按权重加权的版本）。同时报告 A0 逐层 $\bar M$，对照 A1“8 层共用同一划分”。
- 跑前预测（AI）：(b) 相对 (a) 的下降最大 → 负载均衡偏置压过了 teacher 分数，下一步应考虑缩放分数或改负载均衡方式；若 (a)→(b) 差很小，而 top-1/top-2 差大 → 稀释来自第二选择；若都小 → A1 的低集中度来自 8 个粗簇本身（簇数与层间共享），而不是分发规则。
- 竞争解释：teacher 簇本身粗（8 簇），任何分发规则都无法提高集中度。
- 结果：(b) 复现训练评估产物（最大差 0）。Top-2 硬选择口径下，去掉 load bias 使 $\bar M$ 中位数 0.586→0.697，是所测规则中下降最大的一项；Top-1（k=1）0.510/0.442，softmax 加权 0.766（另一口径）。$|s|$ 均值 0.057、第 2/3 高分差 0.036，而 $b$ 极差 0.136。bias 对频段作用相反：bin9 0.49→0.68，bin0 0.74→0.66。A0 逐层 0.83–0.97，A1 八层完全相同（0.586）；b=0 时 0.697 仍低于 A0 任一层。按跑前分支，属“(b) 相对 (a) 下降最大”，但 b=0 后剩余差距仍大，“8 个粗簇本身”的解释也未排除。表/图：`D2_A1_concentration_variants.*`、`D2_concentration_loss.*`；脚本同目录 `d2_concentration_loss.py`（MIG 39 秒）
- 研究者决定：Unknown
- 链条位置：机制 → routing·架构含义

今日认识更新：A1 落后 A0 不是因为 A0 早期“还没集中”——A0 一开始就更集中；A1 的集中度在规则层面主要被 load bias 稀释，但即使去掉 bias，8 簇共用划分的上限仍明显低于原生 router 的每一层。

## 1109 11:00　建模链条回填：从一步噪声到分发假设（回溯整理，不是新预登记）

- 假设：沿用 H1/H2：稀少的信息在共享参数上可能受到 minibatch 梯度噪声的限制；若分发把同一信息的有效更新集中到相同参数，并减少无关更新，可能提高学习效率。这里的“同一信息”暂用冻结 teacher SAE feature 的激活作为可计算代理，不把“同一簇”直接当成同一梯度方向。
- 先验→模型→计算：同一信息出现次数少，有限 minibatch 对其平均更新的估计可能不稳定 → 用一次更新的方向项、均值曲率项和噪声项分解 H1，再用覆盖率、纯度构造集中度代理检验 H2 → H1 沿用 R02 已完成的单 expert SGD 扰动；H2 沿用 R03 已保存的五臂训练/EVAL，不新增训练或前向。本条只把已有建模依据、运算和证据连接起来。
- 跑前预测：回溯原 R02/R03 已冻结预测，不把本次读过结果后的整理称为跑前登记。H1：噪声项按学习率平方及 batch 大小倒数变化，且帮助到伤害的交叉随 batch 增大右移；H2：A1 对 A2 的逐 feature 收益与集中度差正相关，低频收益更大。相应支持、非支持和不足分支见下一条；新增机制解释均为 AI 建议。
- 竞争解释：低频学习受有效样本不足、容量或优化条件限制；teacher 分发的收益也可能来自语义共享结构，而非梯度噪声下降。R02 的簇对不等同于低频 feature，不能仅凭 R02 排除所有长尾任务中的方向冲突。
- 结果：已读研究者新提供的[组会稿草稿](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/inputs/1109_组会稿_草稿.md)和[框架交接文档](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/inputs/1109_框架交接文档.md)，按下述条件整理。附件是本轮建模来源；其中候选解释、待做清单和讨论问题不自动变为已验证结论、研究者接受或新增运行授权。
- 研究者决定：Unknown。研究者已授权既有训练及结果整理；科学接受另行记录。
- 链条位置：机制 → 干预验证 → routing·架构含义 → loss·训练效果；各箭头目前仍有未闭合条件。

**一步模型中的对象与条件。** 固定模型状态和参数块，A 是提供更新的 token 组，B 是评估损失的 token 组；\(\bar g_A\) 是 A 的平均梯度，\(\Sigma_A\) 是单样本梯度协方差，\(g_B,H_B\) 是 B 损失的梯度与 Hessian，\(n\) 是 minibatch 有效样本数，\(\eta\) 是一步 SGD 步长。在局部二阶近似及相应抽样假设下：

\[
\mathbb E[\Delta L_B]\approx-\eta g_B^\top\bar g_A
+\frac{\eta^2}{2}\bar g_A^\top H_B\bar g_A
+\frac{\eta^2}{2n}\operatorname{tr}(H_B\Sigma_A).
\]

噪声项非负需要 \(\operatorname{tr}(H_B\Sigma_A)\ge0\)，例如相关方向上的曲率半正定；它不是任意模型状态下的普遍保证。token 相关性也会影响简单的 \(1/n\) 抽样近似。方向帮助为正、二阶分母为正时，二阶模型的交叉步长为：

\[
\eta^*\approx\frac{2g_B^\top\bar g_A}
{\bar g_A^\top H_B\bar g_A+\operatorname{tr}(H_B\Sigma_A)/n}.
\]

只有噪声项主导分母、其他条件近似不变时，才进一步得到 \(\eta^*\approx2n g_B^\top\bar g_A/\operatorname{tr}(H_B\Sigma_A)\)。所以“有效重复次数提高可用步长”是有条件的桥，不是“同簇就一定能提高学习率”。R02 主跨组方向项 z=1.28；噪声标度符合预测，但预先网格未直接分辨帮助到伤害的翻转，交叉点只到推导/事后估计。前文“噪声主导”的认识应限于该固定状态、单 expert、一步 SGD，不能扩成全部长尾训练的已证主因。详见[R02 原结果与判据](../../experiments/A17/17_13_ntp_statistics_local_compatibility/R02_20261108_snr_mig_pilot/summary_cn.md)。

**分发模型中的对象与计算。** feature \(i\) 指 teacher 第7层 norm2 输出经30000维、TopK32 SAE 得到的激活坐标；\(c_i^{(l)}(e)\) 是 feature 激活时第 \(l\) 层选中 expert \(e\) 的条件概率，\(\pi_i^{(l)}(e)\) 是选中该 expert 的 token 中携带此 feature 的比例。参考频率 \(p_i\) 来自冻结 DEV；覆盖率和纯度来自同一 EVAL 的实际路由。先对每个 feature 求各层值，再对8层算术平均：

\[
\bar M_i=\frac1L\sum_{l=1}^{L}\sum_e\frac{c_i^{(l)}(e)}k
\frac{c_i^{(l)}(e)\pi_i^{(l)}(e)}{p_i},\qquad k=2,\quad L=8.
\]

这是本轮已实施的集中度代理。把它解释为关于信息 \(i\) 的有效信噪比，需要额外限定梯度信号、噪声结构、专家输出权重和层间合成；从这些路由计数尚不能直接推出 Adam 多步 NLL。dense=1、随机 Top-2/8=1/4、理想均衡集中=4 是对应理想条件下的参照，不是实际 EVAL 在 DEV/EVAL频率偏移及任意负载下的通用上界。

源码入口：[evaluation.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/evaluation.py)、[routing.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/routing.py)、[teacher.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/teacher.py)。R03 的 teacher feature 接口与旧实验的其他 SAE 接口不同，不能混用 feature ID。

## 1109 11:00　H2：五臂统一2000步结果与原预测对照（已完成结果的回填）

- 假设：teacher feature 分发若把同一信号集中到相同专家，应比随机分发更有利于低频 feature；是否比可学习原生 router 更好，要测实际集中度和相同预算 NLL，不能预设 teacher 划分更集中。
- 先验→模型→计算：沿用上一条分发模型 → 定义逐 feature 的条件 NLL、两臂的收益与集中度差 → 读取既有2000步统一表及30000个 feature 的统计，核对总体/十频段 NLL、集中度与 Spearman 秩相关；本次只作现有 CSV 的算术复核，没有新训练、模型前向或补图。
- 跑前预测：原 R03 已登记：A1/A2 的相关为正且家族 bootstrap 区间下界大于零、低频收益最大 → 支持原集中假设；无关联 → 削弱；只有点估计而缺所需区间 → 证据不足，保留描述性事实。deep 改善高频与总体 → 与共享代价预测相容；A3复现A1 → 削弱“频率信息不足以解释”的分支；高学习率的相对低频收益扩大 → 与更大可用步长预测相容。后两项在本次2000步包中无结果，不能替它们选分支。
- 竞争解释：teacher 提供了更有利的 token 共享结构；固定0.5权重、router梯度路径和层间适应性也影响学习。A1/A2外生改变分发方案，但没有单独操纵集中度、保持其余共享结构和负载统计不变，因此尚不能识别“集中度降低噪声”这一中介机制。
- 结果：五臂同一seed17、同一随机初态、同一训练顺序及262144有效目标token/步，共2000步=524288000有效训练token；每个EVAL点2097152有效目标token，按原1000步预热后恒定调度。下表是已完成训练结果；固定路由分支无router到表征的梯度回流、选中两专家各0.5，teacher训练见过训练前缀。总体NLL按有效token平均，集中度中位数按feature等权汇总，两者不是同一个加权总体。
- 研究者决定：Unknown。当前能记录损失及关联的事实；家族区间缺失，不能把原完整支持判据标为通过，也不据中位数排序确认机制。
- 链条位置：分发干预 → loss·训练效果（当前条件下的 A1/A2 总效应）；机制中介与 routing·架构推广仍待检验。

| 臂 | 分发条件 | 2000步总体NLL | 集中度中位数 | bin0低频NLL | bin9高频NLL |
|---|---|---:|---:|---:|---:|
| A0 | 原生可学习router | 4.083142 | 1.010460 | 3.794580 | 4.073950 |
| A1-deep | 前四层原生，后四层teacher固定 | 4.085093 | 0.870829 | 3.789857 | 4.076663 |
| A4 | 原生router加teacher蒸馏 | 4.129442 | 0.810892 | 3.867187 | 4.116810 |
| A1 | 全层teacher固定 | 4.157604 | 0.585752 | 3.901086 | 4.144840 |
| A2 | 全层随机固定 | 4.286028 | 0.256799 | 4.187886 | 4.256258 |

| 对比 | 检验原问题的哪一部分 | 已有读数与允许的读法 |
|---|---|---|
| A1−A2 | teacher组织共享相对随机分发是否改善学习 | 八个评估点A1都较低；2000步总体−0.128423，bin0−0.286800、bin9−0.111418；500步总体差−0.205311，之后优势收窄 |
| A1−A0 | 是否超过实际可学习基线 | 250/500步−0.092436/−0.027840，750步+0.045035，2000步+0.074463；2000步十bin全部较高，未观察到相对A0的净收益 |
| deep−A1 | 浅层保持原生路由是否有利 | 八个评估点deep总体都较低；2000步−0.072511且十bin都改善；deep−A0仅+0.001951，不能宣布等效或稳定胜出 |
| A4−A0 | teacher蒸馏能否形成有利路由 | 总体+0.046300且十bin都较高；A4中位集中度低于A0，teacher top1一致率约38%，不能说已形成目标路由后仍无收益 |
| A1/A3，参照A2 | 仅频率信息是否足以解释收益 | 本次统一包无A3结果；不据旧计划或附件“未跑”推断当前平台状态 |
| (A1-hi−A0-hi) 对 (A1−A0) | 集中后能否利用更大步长 | 本次统一包无hi结果；需相同2000步和相同频段比较，尚不能选择结果分支 |

原登记主对比 A1/A2 的 Spearman 为0.255924；附件的四个事后探索值也已按现有 CSV 复核：A1/A0为0.372391，deep/A1为0.284746，deep/A0为0.293297，A4/A0为0.163541。feature不是独立训练重复，家族映射与bootstrap区间Unknown，不能把四个事后值重新登记成主检验。A1/A2有176个feature的收益为负，不能把正关联加强为“每个feature集中度更高就必然更好”。

五臂的总体NLL排序与集中度中位数反向一致，是此端点的描述。换成按feature激活次数加权的平均log集中度，A0为−0.401735、deep为−0.360923、A1为−0.453949、A4为−0.472061，A0/deep与A1/A4两对次序互换。因此不能用挑选的一种汇总统计作为已经验证的设计筛选准则，更不能将模型端点统计解释为中介因果。

来源：[原预测及紧急修订](../../experiments/A17/17_13_ntp_statistics_local_compatibility/R03_20261109_teacher_routing_signal_concentration/protocol_cn.md)、[2000步统一分析与图表](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/README.md)、[完成回执](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/evidence/urgent_2000_completion_certificate.json)、[本次附件数字复核](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/evidence/framework_attachment_numeric_check_20261109T0259Z.json)。训练、自动恢复和分析入口由[既有脚本索引](/data/250010109/Research_System/.research/memory/conversations/1109-teacher分发训练与2000步分析/scripts_inventory.md)记录，不把完整代码搬入探索日志。

资产ID：`analysis_teacher_routing_frozen_clusters_20261109`；实际存档家族 `checkpoint_family_teacher_routing_r03_training_A0_through_002000_20261109`、`checkpoint_family_teacher_routing_r03_training_A1_through_002000_20261109`、`checkpoint_family_teacher_routing_r03_training_A2_through_002000_20261109`、`checkpoint_family_teacher_routing_r03_training_A4_through_002573_20261109`、`checkpoint_family_teacher_routing_r03_training_A1_deep_through_002573_20261109`。A4/deep仍只取2000步读数。上述六ID本轮限定strict访问通过，回执为[explore_fill_assets](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/evidence/explore_fill_assets_20261109T0258Z.json)；未加载权重，不以访问检查替代内容或科学验证。

## 1109 11:00　接收另一Agent的D1/D2：按已写分支更新解释，不重复运行

- 假设：已有D1检验“A0到500–750步才超过A1的集中度”，D2检验“A1的偏置/Top-k等规则稀释了集中度”。本条只接收上文另一Agent回填的结果及其源表，对附件的旧候选解释作范围澄清。
- 先验→模型→计算：沿用上文D1/D2 → D1看相同feature、相同汇总的集中度时间轨迹是否交叉；D2看同一teacher分数下规则改变前后的集中度 → 本轮只读已有CSV、D2检查回执及实际生产脚本，不重复前向、不生成图，也不覆盖另一Agent已写的D1/D2条目。
- 跑前预测：沿用上文已存在的D1/D2分支。D1若A0从首个已测点就更集中 → 不支持“后期才超过”解释；若交叉同步 → 仅时间相容证据，仍非因果识别。D2若去bias恢复同口径集中度 → bias是该指标变化的来源之一；若差很小 → 查其他结构；若不复现保存值或改变统计口径 → 不足。最后的复现/口径条件为本次读取时的有效性检查，不冒称旧预测的一部分。
- 竞争解释：D1早期NLL差由warmup、固定权重/梯度路径或优化历史造成；D2剩余差距来自簇划分、层间共享或不同表征适配。静态分配指标变化并不能替代新路由下的训练收益测量。
- 结果：D1的A0在250步中位集中度0.802799，已高于A1的0.546501；500/750步A0为0.913792/0.933316，A1为0.547134/0.541257，未出现所预测的500–750步交叉。D2的实际bias Top-2逐feature复现保存评估，最大差0；同一硬Top-2口径下去bias使总体中位数0.585752→0.696911。低频bin0反而0.739287→0.659596，高频bin9为0.493332→0.675454，不能说bias对所有频段都稀释信号。
- 研究者决定：Unknown。AI分支记录：D1的具体交叉预测不成立；D2显示bias影响当前集中度，且具有频段差异。“去bias会改善训练”仍未检验。
- 链条位置：机制诊断 → routing·架构候选；尚无这些诊断变体的新训练效果。

D1能排除的是“在500–750步才发生集中度高低交叉”的具体解释；没有0–249步的同口径测量，不能说A0从初始化起就更集中。集中度差随训练增大仍可作为另一个候选解释，但不能把这个事后版本称为原交叉预测得到支持。

D2还需保留两点读法边界：Top-1的硬集中度0.510275/0.441644对应不同k，随机参照也从1/4改为1/8，不能仅凭原始值降低判定“第二选择不是问题”或Top-1训练一定更差；softmax加权值0.765640使用另一统计口径，不表示原硬选择集中度提高，更不是loss改善。去bias的0.696911低于本次A0每层中位数0.83–0.97，只能说明**这一个已测的无bias划分仍较低**，不是“所有8簇设计的上限”已被证明。

来源：[D1数据](/data/250010109/Research_System/daily_research_reports/1109/meeting_report/figures_tables/D1_Mbar_by_step.csv)、[D2变体表](/data/250010109/Research_System/daily_research_reports/1109/meeting_report/figures_tables/D2_A1_concentration_variants.csv)、[D2复现回执](/data/250010109/Research_System/daily_research_reports/1109/meeting_report/figures_tables/D2_checks.json)、[逐层对照](/data/250010109/Research_System/daily_research_reports/1109/meeting_report/figures_tables/D2_layerwise_A0_vs_A1.csv)。生产脚本为执行侧 [build_tables.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/analysis/meeting_1109/build_tables.py) 与 [d2_concentration_loss.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/analysis/meeting_1109/d2_concentration_loss.py)，均由另一Agent运行，本次未重跑。其表和图继续由该Agent维护。

## 1109 11:00　下一步推演：先闭合哪条桥（AI建议，未新增运行）

- 假设：若集中度能成为“何时共享、何时分开”的设计依据，应在明确梯度/优化器条件下预测改变分发后的学习差异，而非只解释已经训练好的模型端点排序。
- 先验→模型→计算：共享/分开的价值要同时计入有效信号重复、梯度噪声、参数复用及遗忘 → 在H1一步模型与H2路由计数之间建立条件化桥，并把Adam预条件及多步状态写清 → 本轮仅整理附件的七个开放问题；没有新增求解、拟合、训练或诊断运行。
- 跑前预测：AI建议，尚未运行：若同一统计定义在保留关键控制的分发改变上能预先给出正确方向，才逐步把集中度升级为设计依据；若方向不稳，或不同合理加权导致预测翻转 → 修正信号单位/目标而非事后选择指标；若缺少可识别的中介或足够复验 → 保留为描述性代理。
- 竞争解释：集中度是学习或负载均衡的结果；teacher坐标、输出权重、Adam状态、共享复用和保持过程本身决定学习，而单一集中度不足以概括。
- 结果：开放问题已归到同一活跃问题的以下三条桥，均未解决，不新建活跃问题。附件里“有效步长正比于SNR平方根”仅是简化Adam模型的候选近似；需要说明信号/噪声定义、动量和二阶矩状态，不能当成真实AdamW训练已验证的定律。
- 研究者决定：Unknown。下一科学优先级由研究者选择；本条不授权新实验。A3/hi只保留原有授权与“本次结果包无结果”的事实，不恢复训练监督。
- 链条位置：机制 → 干预验证 → routing·架构含义 → loss·训练效果；待闭合。

| 待闭合的桥 | 对应附件开放问题 | AI建议的推进含义 |
|---|---|---|
| 从路由计数到更新信噪比 | Adam多步定量关系；集中度定义；同簇信号与噪声一起变大 | 明确信号单位、协方差与优化器假设，先说明集中度能预测什么，再讨论门控目标 |
| 从关联到可操纵的因果预测 | 集中是因还是果；门控需要哪些性质 | D1的具体交叉解释已被削弱，D2仅测规则对指标；需要能区分“计数中介”与“teacher共享结构”的预测，不能只凭时间先后或相关下结论 |
| 从局部收益到共享/分开的总目标 | 共性复用代价；两次出现之间的保持/遗忘 | 同时计入学一条信息的收益、重复学习共性的成本和中间更新的保持；现有单个指标不能自动给出最优划分 |

今日认识更新：R02把注意力从该固定状态下不显著的跨组方向冲突转向可测的噪声项，但局部SGD到Adam多步的桥仍未闭合。R03中teacher分发优于随机、未优于原生；集中度和收益存在正关联，尚未成为已验证的因果筛选准则。新D1否定500–750步集中度交叉的解释；D2显示bias的影响有频段差异，去bias能提高总体集中度但不等于改善低频或训练。下一步是把信号单位、优化器和共享代价写清，再决定哪种分发值得训练；研究者判断Unknown。


## 1109 13:17　R03低频feature末层路由蒸馏：研究者明确授权，跑前冻结

- 假设：同一teacher含有可用低频feature结构，针对目标feature构造末层监督可能比完整token聚类更有效；提高集中度不预设必然带来NLL收益。
- 先验→模型→计算：稀少信号可能因分发被分散，但旧完整表征聚类不一定保留它 → 用feature条件覆盖/纯度定义第7层硬Top-2集中度M7，以DEV上的A0接收专家构造固定q_f并融合为q_t → DEV诊断后从同一A0@2000模型/优化器/RNG/数据游标，比较C0原生、C1真实q_t、C2同监督token内置换q_t的三组续训。
- 跑前预测：M7不增→干预未成功；M7增但目标NLL未改善→集中不足以保证收益；真实胜随机但不胜C0→无原生改善；真实M7增且目标NLL优于两对照→支持此条件的局部价值，仍不单独确认中介因果。统计不足或资产/接口不合格时不冒充完成。
- 竞争解释：teacher结构可用但固定簇映射未利用；或当前目标构造仍无效。C1/C2保持监督位置、目标熵/专家质量及系数相同，不能只重命名feature。feature条件NLL是激活位置的读数，不等于feature已被学生学会。
- 结果：NOT RUN。输入限定strict已通过；详细筛选/一次DEV修正规则、共同预算与停止条件先写入[执行计划](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/configs/preregistered_plan.json)。低频为正文代理位置的Top32激活率最低20%，至少128位置、8独立文档，最多64个；不按EVAL收益选feature。准备复用原trainer/模型/数据流/同步存档/A4 stop-gradient KL，改为只有末层有辅助项；旧实现和结果均不改。
- 研究者决定：已在本对话明确授权资产检查、构造、三组公平续训及交付；科学判断Unknown。无需再次确认继续；不取消其他任务，不静默替代模型或SAE。
- 链条位置：分发映射诊断 → 末层router干预 → 留出loss变化；单种子局部续训，不外推完整噪声机制。

今日认识更新：本轮直接检验低频feature定向末层监督能否利用同一teacher结构，保持真实与置换对照可比；还没有诊断或训练结果。


## 1109 13:48　R03低频末层蒸馏：DEV可行性通过，ACP等待节点

- 假设：沿用本轮跑前假设；同一teacher的低频feature可形成比旧完整表征聚类更集中的分配，但实际router能否跟随及NLL能否改善仍待三组续训。
- 先验→模型→计算：沿用前条 → 在同一DEV正文参考位置按相同硬Top-2计算M7、覆盖/富集与负载，构造真实q与同监督集合置换q → 已完成DEV诊断、实际模型aux-only反传、DEV校准和输入内容校验；未使用EVAL收益调参。
- 跑前预测：沿用四类预写分支。DEV硬目标改善只放行干预实现，不等于实际学生集中度或训练收益；若实际M7未改善，按干预失败处理，不判teacher太弱。
- 竞争解释：目标代理存在结构但线性router/弱KL未实现，或代理不反映有利的语言建模共享。原生与随机两对照均保留，不能以oracle目标M7代替它们。
- 结果：DEV参考1578146位置/1316文档，校准432677位置/330文档。64目标均满足至少128激活、8文档；全部合格低频4642个。M7中位数：原生0.867730、旧b=0映射0.623552、旧A1@2000实际bias映射0.647315、定向目标3.726510、匹配随机0.698978；定向与随机的总专家负载相同。监督覆盖0.5209%，37种q分布，跨锚点冲突0.7178%。校准系数0.0005687732，参考梯度比5%，不更新参数；aux-only实际反传只有末层router权重非零。A0完整状态、33B teacher、SAE和缓存SHA，以及tokenizer/原始文本对齐已PASS。share新任务pt-5hk74r96，四H100 Reserved16c256g，当前STARTING/worker Pending；尚未完成20步实测，不虚报训练已开始。详见[DEV诊断](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/evidence/DEV_diagnostic.json)、[实际bias对照](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/evidence/DEV_original_actual_bias.json)、[内容校验](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/evidence/model_content_identity.json)。
- 研究者决定：当前任务执行已授权，科学判断Unknown。继续监督同一任务，不重复提交或取消其他任务；三组完成后才交付训练比较。
- 链条位置：分发映射可行性诊断已完成 → 实际router干预与loss验证待运行。

资产：`analysis_r03_lowfreq_lastlayer_targets_20261109`、`analysis_r03_lowfreq_lastlayer_dev_diagnostic_20261109`；目标冻结后的[640对DEV共激活统计](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/targets/coactivation_top10.csv)仅作补充，不能由绝对低频或共激活直接命名composite–constituent，更不声称复现HiFER。

今日认识更新：同一teacher下可构造负载可接受的低频集中目标，旧映射不是这个代理的上限；是否能够通过弱末层监督转化为真实路由及留出NLL改进，仍等待受控续训。


## 1109 14:28　R03资源检查：share继续排队，P12协作提交受配额限制

- 假设：沿用本轮假设，资源调度不改变科学比较。
- 先验→模型→计算：沿用前条 → 三组同起点/数据/目标/预算，仅允许不同已授权四H100 worker领取不同臂 → 使用AFS原子目录独占领取缓存生成与各臂，旧控制器schema不匹配时拒绝运行；尚未发生训练更新。
- 跑前预测：沿用四类结果分支；排队和CREATE_FAILED均不构成干预结果，不改变目标集合或辅助系数。
- 竞争解释：执行未开始与干预无效必须分开；资源不足不能解释为teacher结构无效。
- 结果：share pt-5hk74r96仍STARTING，worker Pending、无节点地址。P12尝试同样四H10080GB Reserved16c256g，平台返回429 MEMBER_QUOTA_EXCEEDED（仅余2卡，申请4卡）；没有创建P12任务，不占用/取消其他任务。[拒绝回执](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/acp_receipts/submit-r03-lowfreq-last7-p12-20261109-20261109T061826Z.json)与[调度记录](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/evidence/operator_state.json)已保留。继续监督share原任务，不重复提交同一臂。统一300步仍为待20步实测后锁定的候选，当前各臂实测更新数为0。
- 研究者决定：执行授权沿用；科学判断Unknown。P12受配额阻碍的新增worker暂不能启动，share工作继续。
- 链条位置：DEV可行性通过 → 训练资源排队，实际router操纵与留出收益未检验。

今日认识更新：本轮尚无训练结论；已有DEV结构可行性与资源拒绝证据，需等待真实三组训练后再解释集中度和学习效果。


## 1109 14:50　R03四卡节点已分配，缓存完成交接

- 假设：沿用本轮低频feature末层监督假设；当前仍属实现与数据准备。
- 先验→模型→计算：沿用前条 → 同一冻结FP32 teacher/SAE、相同四条逻辑数据流与全局目标行置换 → 排队期间先用空闲本地MIG生成前120个更新，再于完整更新边界正常退出；核实PID终止后归档本地领取记录，由share四卡worker独占接管余下180个更新。
- 跑前预测：沿用四类预写分支；缓存可生成不构成学生路由改变或NLL收益。
- 竞争解释：teacher目标可分配不保证早期学生表征中的线性router可实现，也不保证NTP受益；需要C0/C1/C2实际续训。
- 结果：share `pt-5hk74r96`已RUNNING，四rank均为完整NVIDIA H10080GB、CUDA12.4/Torch2.3，设备证据在执行根`evidence/device_rank*.json`。本地生成范围2000–2119，共480分片；交接[核实记录](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/evidence/local_cache_handoff_verified.json)PASS。前54个完整更新的[q置换审计](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/evidence/cache_audit_prefix_054.json)显示目标行直方图、熵与专家总质量精确匹配，同位置q仍相同约12.09%，随机置换期望12.28%；没有按EVAL调整。四卡接管后的缓存耗时约每全局更新2–3秒。此刻还无C0/C1/C2参数更新；最新状态见[持续记录](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/evidence/live_status.json)。
- 研究者决定：执行授权沿用；科学判断Unknown。待完整缓存登记/strict通过后直接测C0前20步，并锁定三组统一预算，不再请求继续确认。
- 链条位置：DEV可构造性 → 缓存与实现验证 → 实际末层router操纵待运行。

今日认识更新：已获得正式四卡资源并完成安全缓存交接；接下来需要实际训练读数，而非用DEV目标集中度替代学生结果。


## 1109 15:17　R03统一预算锁定、C0完成；C1训练中，P12协作重新提交

- 假设：沿用本轮预写假设；不预设M7提高即带来条件NLL收益。
- 先验→模型→计算：沿用前条 → 仅末层router接受stop-gradient弱KL，四rank原生LM照常训练 → 1200分片/2400 micro输入哈希已齐全，C2置换审计PASS；C0前20步实测后统一锁定每臂+300步/78643200有效token，不按中间结果改预算。
- 跑前预测：沿用四类分支；C1/C2全程同系数0.0005687732，实际梯度比与负载变化另测，不能假定一直5%。
- 竞争解释：定向目标可分配但早期学生router不一定实现；实现集中仍可能无NTP收益。正文边界过滤只是代理，DEV上下文存在普通叙述、对话、日期、导航与网页模板并存，不能把全部目标称为稀有语义概念，也不能称纯正文验证完成。
- 结果：C0已完成300额外更新并存档至2300步/602931200有效token；实际保存的266项AdamW状态step全为2300，数据游标2300。C0目标等权NLL从3.649238→3.531095，总体4.083136→4.002434，M7中位数0.927982→0.971219，仅是原生续训对照。C1已开始正式训练，实际aux/LM末层router梯度比部分更新约8%–13%；固定系数不调整。首个+50评估C1目标NLL3.626577、M7=0.927460；同步C0为3.626540、0.896635，还不能据此下最终结论。share任务`pt-5hk74r96`继续运行。原P12任务正常结束后，于15:10重提同规格协作worker `pt-yaewtmkm`，当前STARTING/Pending，将独占领取未开始的C2；不取消其他任务。最初P12429拒绝及新提交回执均保留。
- 研究者决定：执行授权沿用，科学判断Unknown。继续监督C1/C2至同预算完整存档后评估与交付，不停止在“任务已提交”。
- 链条位置：DEV分配可行性通过 → 实际router干预/条件NLL对照进行中；纯正文与语义feature获得的强结论仍未验证。

证据：[全缓存审计](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/evidence/cache_audit_complete.json)、[预算锁定](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/configs/uniform_budget.json)、[DEV上下文审计](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/evidence/DEV_context_audit.json)与[192条上下文](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/targets/DEV_target_contexts.csv)、[C0完成](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/runs/C0/stage_complete.json)、[最新双worker状态](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/evidence/live_status.json)。

今日认识更新：原生续训本身在300步内已有明显loss改善，必须比较C1/C2相对这个新C0的额外变化；当前只知道DEV目标可构造，不能用它替代实际集中与学习收益。目标样例也提醒本轮低频单位混合了内容与格式结构，纯正文/语义概念结论不成立。


## 2026-11-09 16:02 CST｜R03低频feature末层蒸馏完成与对比

- 假设：同一teacher的低频feature定向末层监督，能否比原生及同监督位置置换q的随机指导更集中并改善留出NLL？沿用跑前分支，不预设集中必有学习收益。
- 先验→模型→计算：沿用本轮跑前条 → 层7硬Top2 M7为操纵指标，64目标feature条件NLL等权均值为主读数 → 三组从同一A0@2000模型/266项AdamW/scheduler/四rank RNG/数据游标各续训300步，每臂78643200有效token；仅层7router有stop-gradient辅助项，0–6层正常LM训练；同一EVAL每50步评估。
- 跑前预测：按预写分支的点估计方向，C1的M7提高且主均值微弱低于两对照，属于局部价值预测相容分支；但科学稳定性需量级与不确定性检查，不能据此自动接受机制或延长优势组。
- 竞争解释：真实与随机辅助均可能通过router正则化、gate重权或其他优化轨迹改变NLL，而不是经由真实feature集中这一中介；目前未被单独识别。
- 结果：三组均完整保存到2300步/602931200有效token，266项优化器state step全为2300。C0/C1/C2目标等权NLL为3.531094819/3.529205532/3.529247998，M7为0.971218572/1.035971525/0.954566046，总体NLL为4.002433651/4.001488064/4.001167544。C1相对C0目标主均值−0.001889287，相对C2仅−0.000042466；激活次数加权、目标位置并集和总体NLL则C2更低。C1目标M7较C0约+6.67%、较C2约+8.53%，操纵成功，但不能把极小主均值领先升级为明确对应收益。C1在36/64目标胜C0，32/64胜C2，22/64同时胜二者；每feature EVAL覆盖92–554位置、29–156文档。次要目标并集文档bootstrap（1561篇）C1−C0区间[−0.003737,+0.000847]，C1−C2[−0.001646,+0.002164]均跨0，不是主均值/种子区间。
- 研究者决定：Unknown。AI认识更新：集中可被操纵，同一teacher存在可分配结构；真实feature对应相对匹配随机的额外学习收益尚未确立。没有断言teacher弱或集中永远无效。下一预算与接受判断仍由研究者决定，未追加训练。
- 链条位置：分发映射诊断 → 末层router干预已执行 → 留出读数比较完成；噪声中介及语义feature获得尚未验证。

边界/未完成：一个种子、300步局部续训；正文为非特殊token/边界过滤代理，实际DEV样例含网页模板等，纯正文验证未完成。上条“纯正文/语义概念结论不成立”意为本轮证据不足以建立该强结论，并非证明语义结构不存在。SAE原训练context1024，本轮编码2048；层接口相同但未独立验证语义稳定性。条件NLL不是feature被学会。没有验证HiFER composite–constituent身份，也未测固定token/参数块梯度噪声协方差。

执行：三组实际均为share四H10080GB Reserved16c256g任务pt-5hk74r96，平台SUCCEEDED，训练于15:42完成。P12首申429配额不足；重申pt-yaewtmkm约17分钟仍Pending，未领取任何臂后撤回，仅本任务空闲申请，平台SUSPENDED，没有停止其他任务。预算固定后无按结果调整，无训练失败重试或数据跳过。

交付：[完整中文报告](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/deliverables/verified_from_frozen_zip/R03_lowfreq_last7_300/summary_cn.md)；[冻结ZIP](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/deliverables/R03_lowfreq_last7_300.zip)，SHA256 `89190ab09ae75bee4b99b525abe1ef3c7c0849767d61d5637c5a3021e3928ade`。CRC、154包内文件哈希、20条相对链接、1200缓存内容哈希通过；原归档字节保留，校验解压副本与归档一致。11项本轮实际资产已登记/strict。模型及优化器权重留在各臂checkpoints/step_00002300，未塞入ZIP。新增图表、原始表、配置、源码、日志及目标清单均在包内。

今日认识更新：真实指导显著改变了分发计数，但学习读数与随机指导接近且对聚合敏感；本轮闭合了“可操纵集中”的工程环节，没有闭合“真实feature集中带来稳定学习收益”的科学环节。


## 2026-11-09 17:35:30 CST｜按研究者要求核查P12并汇报已保存结果

- 假设：沿用本轮研究假设；本次是任务清理与状态核验，不新增科学干预。
- 先验→模型→计算：沿用前条；任务状态可能滞后于实际执行 → 平台归属及非终止状态判定 → 对P12用户名250010109查询全部8条记录，并核对旧P12 pod日志、各臂latest_checkpoint与EVAL JSONL。
- 跑前预测：发现本人活动任务则按本次明确授权停止并核验；无活动任务则不执行stop、不影响其他人的工作。
- 结果：本人RUNNING/排队任务0。pt-kw43x8ls已于15:07:35 CST自然成功结束；其A1达2573，A1-hi/A0-hi/A3达2000。R03辅助申请pt-yaewtmkm早已SUSPENDED且从未启动。无任务需要停止，本次无资源变更。旧manifest残留RUNNING不是当前状态。同2000步NLL：A0=4.083142，A1=4.157604，A2=4.286028，A4=4.129442，A1-deep=4.085093，A1-hi=4.004250，A0-hi=3.922043，A3=4.153230。新C0/C1/C2均在share完成，沿用既有报告。
- 研究者决定：本次明确授权停止P12本人活动训练；实际无活动任务。科学判断Unknown，未追加训练或改写冻结结果。
- 链条位置：执行状态核验；不产生新的机制或训练收益证据。

证据：[现场核查](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/evidence/p12_status_20261109T093414Z/status_cn.md)；[原始平台回执](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/evidence/p12_status_20261109T093414Z/jobs_user_filtered.json)；[实际存档与同2000步结果表](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/evidence/p12_status_20261109T093414Z/verified_training_results.csv)。

今日认识更新：P12本人训练均已结束或暂停；teacher固定分发优于随机但在相同学习率下仍落后原生，高学习率成对对照亦未反转。此为已有单次结果的核对，不是新增复验。


## 2026-11-09 17:42 CST｜C0/C1/C2 loss与同期baseline重绘

- 假设：沿用R03；本次按用户要求展示训练及留出loss，不新增实验。
- 先验→模型→计算：续训的共同改善可能掩盖干预的微小增量 → 相同更新数下以C0为baseline计算C1/C2−C0 → 复用冻结train_curves.csv及evaluation_curves.csv，逐字节核对ZIP后重绘语言模型CE和总体/64目标留出NLL。
- 跑前预测：绝对曲线重合则用差值图呈现量级；如真实与随机读数接近，不将共同下降算成真实feature对应的额外收益。
- 结果：C0/C1/C2总体终点4.002434/4.001488/4.001168；目标等权终点3.531095/3.529206/3.529248。训练CE几乎重合。C1−C0目标差−0.001889，C1−C2仅−0.000042；总体C2低于C1。新图同时显示原值、同步差值、共同A0@2000水平线。训练仅20步尾随展示平滑；EVAL未平滑。
- 研究者决定：Unknown；本次只重绘，不追加训练、不覆盖冻结数据。
- 链条位置：已有训练收益读数可视化；不新增因果机制证据。

资产：`analysis_r03_loss_vs_native_baseline_20261109`，输入`analysis_r03_lowfreq_lastlayer_results_20261109`。图及表见[说明](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/deliverables/loss_vs_baseline_20261109T0943Z/README_cn.md)，复现脚本[plot_loss_vs_baseline.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_distill_20261109/code/plot_loss_vs_baseline.py)。

今日认识更新：三组共同续训下降占主导，真实/随机相对C0的额外loss变化很小；保留此前真实对应收益尚未确立的边界。


## 2026-11-09 17:57 CST｜R03低频末层指导：研究者授权share四H100等预算延长，跑前冻结

- 假设：同一teacher低频feature对应关系带来的末层集中，能否在更长等预算续训中改善目标相关位置NLL，优于原生及匹配随机？原问题保持不变；这次延长是在查看300步结果后提出，不能称独立确认性复验。
- 先验→模型→计算：稀少信号若能被固定feature对应集中到专家，可能改变专家接收的更新分布；集中不预设等于有用更新 → 保持原64feature/q、KL系数、8层/8E/Top2及末层aux输入detach → 从各自C0/C1/C2@2300完整状态继续到3500，每臂新增1200更新/314572800有效token，沿用同一数据顺序和warmup-only LR0.0003；不冻结前层。
- 跑前预测：C1的M7提高且目标等权NLL相对两对照形成可信改善→局部支持但不中介归因；M7提高而NLL不胜两对照→集中未证明有学习收益；M7未动、覆盖不足或差异极小/聚合敏感→不足，定位失败，不断言teacher弱。
- 竞争解释：C1/C2共有router正则化或gate重权可解释loss变化；只有真实对应关系增益相对随机可区分一部分解释。实际辅助梯度/负载仍需报告，未宣称完全相同。
- 结果：RUN_NOT_YET_SUBMITTED。三个父存档266项AdamW均step2300，scheduler/cursor已核验，全部manifest文件内容SHA刚重新PASS；模型/common与EVAL原实现字节不变。输入strict PASS。运行于独立目录；一个share4H100 Reserved16c256g作业含三个逻辑训练任务，先补50更新缓存并执行C1这50更新（计入固定预算），再补余缓存及三组；脚本异常等待30秒最多3次恢复。新任务不使用P12，P12本人8记录现场无活动项，未停止其他用户。
- 研究者决定：本条训练已由当前对话明确授权；具体等预算延长由AI在本条预先固定，科学判断Unknown。跨层无监督feature的方案讨论不授权额外跨层模型训练。
- 链条位置：低频feature定向分发→末层集中干预→长期一些的同种子学习读数；梯度噪声中介和语义feature学会仍未闭合。

资产：输入为三条`checkpoint_family_r03_lowfreq_lastlayer_C*_through_002300_20261109`及原目标/teacher/SAE/DCLM/EVAL资产；新计划`analysis_r03_lowfreq_long_plan_20261109`。执行计划[/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_long_20261109/configs/plan.json](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_long_20261109/configs/plan.json)；[源复用声明](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_long_20261109/evidence/source_reuse.json)；[三级跑前审计](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_long_20261109/evidence/prelaunch_audits.json)；[父内容校验](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_long_20261109/evidence/parent_content_identity.json)。

今日认识更新：本轮检验更长轨迹是否让真实对应关系的额外价值显现；不改变已有300步的微小且不确定结论，不根据新中间结果调整三组预算。


## 2026-11-09 18:04 CST｜share长续训提交及跨层讨论

- 假设：沿用本轮冻结假设；原问题仍是低频学习收益，不替换为可操纵集中。
- 先验→模型→计算：沿用前条；执行检查对应平台→四rank缓存→C1实测更新→三组固定预算完成。
- 跑前预测：沿用三分支；启动错误只判断工程环节，不构成科学非支持。
- 竞争解释：沿用router正则化/gate重权；跨层读出尚未执行。
- 结果：原share尝试pt-9k4mvtp4获节点后因torchrun把--start识别为自身--start-method缩写而退出，0缓存/0模型更新；已停止并核实SUSPENDED。缓存参数改为--cache-begin/end，launcher加显式--，本地CPU真实torchrun传参probe PASS；原日志保留。相同profile/image/科学设置的新任务pt-l0wd83dn已SUBMITTED，当前QUEUEING，尚未验证GPU运行。P12重复现场核查本人8条均非活动任务。
- 研究者决定：当前三组share续训已授权；跨层检测器或Crosscoder只讨论，不启动额外训练；科学判断Unknown。
- 链条位置：末层路由干预→更长同种子训练等待调度；跨层feature发现为后续候选路径。

[任务计划](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_long_20261109/configs/plan.json)；[当前执行证据](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_long_20261109/evidence/execution_certificate.json)；[跨层讨论稿](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_long_20261109/discussion_crosslayer_cn.md)。

今日认识更新：已有feature识别、teacher伪标签蒸馏和无监督发现新字典是三件事；无需预设每层独立SAE，但必须检查层间可读性、专家局部身份和在线可用信息。


## 2026-11-09 18:14 CST｜share已完成首50实际更新并接管长续训

- 假设：沿用本轮低频指导的训练收益问题，不用集中度或启动成功代替学习收益。
- 先验→模型→计算：沿用跑前冻结；当前核验实际四rank设备、完整恢复、真实数据输入哈希、有效token计数、TB有限值及首2350存档。
- 跑前预测：沿用支持/非支持/不足分支；三组须到同步步数后比较，禁止用C1@2350对C0/C2@2300宣称收益。
- 竞争解释：沿用；此刻没有新同步对照结果。
- 结果：share pt-l0wd83dn RUNNING，四张实际H10080GB（每卡85017624576 bytes），C1实际新增50到2350，262144有效token/update，中位计算耗时2.011秒/update；全局token616038400。完整存档266个AdamW状态均2350，RNG/数据游标/调度恢复通过。2,097,152留出token评估完成。首50共200缓存/400 micro哈希审计PASS，C1/C2目标行直方图/专家总质量精确相同。已自动进入余1150更新缓存生成；C0/C2尚未开始此次延长。P12最后现场查询本人活动0。
- 研究者决定：执行沿用授权，科学判断Unknown；脚本继续固定阶段。
- 链条位置：末层路由干预→同种子长训练已实际开始；同步学习收益与跨层发现仍未完成。

实际新资产：`checkpoint_family_r03_lowfreq_long_C1_through_002350_20261109`、`representation_r03_lowfreq_long_targets_2300_2349_20261109`、`analysis_r03_lowfreq_long_eval_states_0001_20261109`，均已登记/strict。证据[执行说明](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_long_20261109/README_cn.md)和[首50资格](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_long_20261109/evidence/startup_qualification.json)。

今日认识更新：部署已到真实更新、评估与完整存档，当前新训练科学判断仍须等同步C0/C2；跨层优先检验学生层状态能否读出共同feature，再决定共享字典路线，而非默认每层独立SAE。


## 2026-11-09 19:17 CST｜当前算法复核与teacher-free低频分发候选（未运行）

- 假设：原问题仍为低频学习的计算性价比。AI候选先验：学生表征中存在跨文档重复的稀疏低频信号，其条件更新有足够兼容性但被分发稀释；此先验尚未验证。
- 先验→模型→计算：稀有重复方向而非整token簇→小型学生稀疏字典与feature条件专家分布→提议在冻结字典上最小化条件专家熵减feature平衡边际熵，保留Top2及实际负载约束；本条只读prepare_dev/calibrate/common/model.route源码并推导，NOT RUN。
- 跑前预测：未来真实feature正则相对原生/匹配置换在同总成本改善NLL→局部支持；只集中无NLL收益→当前代理不足；统计不稳/硬路由不变/差异不明→不足，先定位。新候选配置和预算未冻结，不执行。
- 竞争解释：几何feature可能只是格式结构；同feature不一定对应兼容梯度；正则化/gate变化可解释局部NLL差，不能把计数集中直接解释成噪声机制。
- 结果：当前实际算法为DEV底20%频率+覆盖筛64→A0学生末层最常接收的专家对q_f→多feature等权融合q_t→目标位置弱KL、只直接更新末层router。没有逆频率加权，也未固定实际gate为0.5。候选teacher-free算法去掉外部teacher和预设q，以自监督字典定义可复现feature、以结构约束学习专家分工。32例的assignment计数只是示意推导，不是新增实验或4倍有效batch结论。
- 研究者决定：Unknown。按用户请求讨论与解释；没有改动运行中的share长续训代码/配置，也未提交新的字典/跨层训练。
- 链条位置：表征结构先验→分发机制候选→最小干预比较待设计；最终仍需学习效果与总成本。

完整定义、信息量采样口径、坍缩/跨层边界与三组最小比较：[讨论稿](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/followups/lowfreq_lastlayer_long_20261109/discussion_teacherfree_routing_v1_cn.md)。当前源码依据为原prepare_dev.py/calibrate.py及长续训code/common.py，native route在BASE/moe_baseline/model.py:211。

今日认识更新：不依赖teacher的关键是从学生空间获得稳定、学习相关的信号单位，并让其共同决定分发，而不是用稀有性本身代替有用性；集中是候选组织方式，成本匹配NLL收益仍是原问题。


## 2026-11-10 CST｜R04接管：集中是否改善学习与学会/遗忘账本（跑前）

- 假设：沿用R04 P1–P4；原子集中能否改善低频学习，不能由五臂相关排序直接推出。
- 先验→模型→计算：可重复原子的位置更新被分散，可能提高波动→以H3约束router并比较同预算NLL；账本以固定原子支撑集上的逐位置损失差及配对SE、BH-FDR与硬Top2集合翻转衡量→先用现有五臂可用存档前向，不重训缺失存档；A6/A5后补。沿用R04 protocol。
- 跑前预测：A6集中且低频NLL改善、总体不差>0.01→局部支持；集中提高而NLL无收益→削弱集中足够的解释；差异小于预设相邻检查点波动或缺存档→不足。P4在同区间内比较χ四分位与遗忘，并另做共同1000→2000区间，避免把区间长度差当臂效应。
- 竞争解释：集中是训练变好的结果；辅助正则或固定分发差异改变了gate/优化而非噪声中介。固定分数仍有变化的load bias，χ不应被人为设成0。
- 结果：待运行；输入资产strict访问通过（evidence/input_access_codex_20261110.json）；share pt-nmcuobkl仍STARTING，未实际训练。修复逐位置A2随机分数路径后启动现有臂前向；详见执行根evidence/codex_takeover_audit.json。
- 研究者决定：执行沿用本次明确授权；科学判断Unknown。
- 链条位置：路由干预→学习效果；账本为机制线索，未识别因果中介。

今日认识更新：先把原子集中、路由变化和条件NLL置于同一可复现比较，固定分发是否固定必须由实际Top2集合检验。


## 2026-11-09T16:35:49.926052+00:00｜R04 现有五臂分析已完成；A6/A5待训练完成

- 假设：沿用R04集中是否改善学习及P1–P4；原问题不替换为仅能改变路由。
- 先验→模型→计算：沿用跑前条目→原子条件分发及同预算NLL→实际位置账本、M、相关和t50，脚本/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/ledger.py。
- 跑前预测：沿用Protocol支持/非支持/不足分支；差异小于checkpoint变化参照判不足。
- 竞争解释：集中是结果或辅助正则/gate/负载改变；位置翻转相关不识别因果。
- 结果：现有五臂中，teacher固定分数路由A1相对随机A2的总体NLL低0.128423，相对原生A0高0.074463。完整数值及覆盖见/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out_existing/coverage.md、/data/250010109/Research_System/daily_research_reports/1111/meeting_report/atom_concentration/report_cn.md，位置误差见position_consistency.csv。
- 研究者决定：Unknown；AI分析见报告，不改变Anchor判断。
- 链条位置：路由干预→学习效果；账本提供机制线索。

今日认识更新：现有五臂中，teacher固定分数路由A1相对随机A2的总体NLL低0.128423，相对原生A0高0.074463。


## 2026-11-10 01:04 CST｜参考频率恒等式诊断与完整GPU冒烟

- 假设：原问题沿用；同臂高M组遗忘更多，含随机A2，不直接推出集中致遗忘。
- 先验→模型→计算：DEV频率分母与EVAL计数可能不同→M=k(r/p)Σu³/α，均衡负载仍含r/p→只读5臂2000步joint/expert/count，检验恒等式及更换EVAL分母的事后敏感性；跑前记录在analysis/metric_reference_audit_plan_cn.md，未改原M。
- 跑前预测：A2原M随r/p，换EVAL分母后接近0.25；同原子跨臂ΔlogM不变。支持→限定M解释；非支持→查负载/有限计数；不足→保留输入问题。
- 竞争解释：遗忘率随M变化还可由出现次数/检验功效、难度或真实分发差异产生，当前不识别中介。
- 结果：恒等式最大误差≤1.43e-14；A2 rho(M,r/p)=0.994165，q10–q90从0.189536–0.324290缩到0.250370–0.259861；跨臂ΔlogM变动≤1.23e-15。GPU冒烟λ0的50步对A0差全0；真实SIGKILL恢复1100张量全同，λ=0.014186772834701426。摘要变量错误已修复且0次正式更新，当前share恢复作业pt-lcxcxgyw排队，smoke已授权删除30,558,237,742字节。
- 研究者决定：Unknown；AI分析见1111稿，不更新Anchor科学状态。
- 链条位置：表征现象→机制指标校验；实际新臂学习效果待训练。
- 资产引用：analysis_r04_atom_groups_frozen_20261109、representation_r04_positions_existing_five_20261109、analysis_r04_atom_ledger_existing_five_20261109、analysis_r04_atom_contexts_existing_five_20261110、analysis_r04_metric_reference_sensitivity_20261110；输入dataset_teacher_routing_dev_eval_20261109、representation_teacher_routing_sparse_codes_20261109。均已作用域strict检查；完整来源见执行根evidence/asset_registration_*与output_access_*。

今日认识更新：原M的参考频率成分能够被精确分离，跨臂同原子ΔlogM仍保留；固定score的动态bias与频率/检验功效应共同限制遗忘机制解释。


## 2026-11-10T02:29:43.702909+00:00｜R04 七臂已纳入

- 假设：沿用R04集中是否改善学习及P1–P4；原问题不替换为仅能改变路由。
- 先验→模型→计算：沿用跑前条目→原子条件分发及同预算NLL→实际位置账本、M、相关和t50，脚本/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/ledger.py。
- 跑前预测：沿用Protocol支持/非支持/不足分支；差异小于checkpoint变化参照判不足。
- 竞争解释：集中是结果或辅助正则/gate/负载改变；位置翻转相关不识别因果。
- 结果：A6相对A0的总体NLL差为+0.091856，A5相对A1为-0.118485，学习收益需同时结合低频结果与预设波动规则。完整数值及覆盖见/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/coverage.md、/data/250010109/Research_System/daily_research_reports/1111/meeting_report/atom_concentration/report_cn.md，位置误差见position_consistency.csv。
- 研究者决定：Unknown；AI分析见报告，不改变Anchor判断。
- 链条位置：路由干预→学习效果；账本提供机制线索。

今日认识更新：A6相对A0的总体NLL差为+0.091856，A5相对A1为-0.118485，学习收益需同时结合低频结果与预设波动规则。
