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
