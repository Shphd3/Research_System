# R04 Detailed：实际执行、偏差与证据

[Summary](summary_cn.md)；[冻结Protocol](protocol_cn.md)；[实施补充](implementation_amendment_20261110_cn.md)。状态：七臂已纳入；研究者科学判断Unknown。

## 问题、模型与结果读法

原子是冻结SAE的激活坐标，不预设等同人类概念。位置$x$ 的次token损失为$\ell_x(t)$ ；原子$j$ 的支撑集为$A_j=\{x:z_{x,j}>0\}$ ，出现次数为$n_j$ 。原子条件NLL是这些位置损失的平均，不等于已证明模型学会了该语义。

专家数$E=8$ ，每个位置选择$k=2$ 个专家。对原子$j$ 、层$l$ 、专家$e$ ，覆盖$c_j^{(l)}(e)=P(e\in S\mid j\text{激活})$ ，纯度$\pi_j^{(l)}(e)=P(j\text{激活}\mid e\in S)$ ，参考频率$p_j$ 在DEV冻结：

$$
\bar M_j=\frac1L\sum_l\sum_e\frac{c_j^{(l)}(e)}k\frac{c_j^{(l)}(e)\pi_j^{(l)}(e)}{p_j},\qquad L=8.
$$

它是无量纲富集读数，允许大于1；负载均衡且EVAL与DEV频率相同时，随机Top2参照为k/E=0.25。它不单独测量梯度是否兼容。频段NLL按bin内原子激活次数加权，同一位置可进入多个原子，不是互斥token分桶。

A6保留原生路由，只向router权重加入集中正则的梯度。令$\operatorname{sg}$ 截断隐藏状态$h$ 的梯度，$\tilde P=\operatorname{softmax}(W_r\operatorname{sg}(h))$ ，用正激活幅值加权形成$q_j$ ，再最小化三阶Rényi熵：

$$
q_j(e)=\frac{\sum_xz_{x,j}\tilde P_x(e)}{\sum_xz_{x,j}},\qquad H_3(q_j)=-\frac12\log\sum_eq_j(e)^3.
$$

各层、micro-batch内出现至少2次的原子按冻结$w_j$ 加权，再加到语言模型CE；λ按50步router梯度范数规则冻结。A5在DEV共激活图中把原子划为8组，以组内$w_jz_j$ 之和形成固定score，8层相同、gate各0.5。两者均保留动态load bias。训练q按激活幅值和soft概率加权，评估M按二元激活和硬Top2计数；H3下降并不由定义保证硬M上升。统一的末层teacher原子也未必能被学生早层隐藏状态识别，截断表征梯度的辅助项只能使用该层已有可读信息；按层诊断可定位这一接口，不能直接证明不可读。A6在推理时只需原生学生router；A5仍需要teacher/SAE与原子分组生成外部分数。

候选机制是同一重复信号的更新被分散到不同参数，集中或能降低有效更新波动；最强竞争解释是集中只是学习结果，或正则/gate/负载本身起作用。另一个可区分的接口解释是：soft H3下降而动态bias补偿硬负载，实际硬M不随之提高；通过既定H3、原始概率、熵、load/bias与硬M联合诊断，避免把操纵不足误写成学习机制失败。A6−A0检验集中正则的联合学习效果；A5−A1检验原子划分相对token划分。它们都没有单独替换或识别梯度噪声中介。

其中$\mathcal J$ 为本micro-batch出现至少两次的原子集合，冻结$w_j=\min(\log(1/p_j)/\operatorname{median}_j\log(1/p_j),3)$ ，实际目标为

$$
\mathcal L_{\rm total}=\mathcal L_{\rm CE}+\lambda\frac1L\sum_l\frac{\sum_{j\in\mathcal J}w_jH_3(q_j^{(l)})}{\sum_{j\in\mathcal J}w_j}.
$$



终点AI分析：A5比A1同时提高硬集中度并降低NLL，支持当前固定分发条件下原子分组路线的联合价值；分组身份、score尺度、bias和gate的作用尚未隔离。A6的H3下降而硬M低于A0，说明soft训练目标没有实现预期的硬集中操纵，不能把它当作集中机制已被充分检验。其NLL方向较差，但按原检查点变化规则保留不足。终点8层中6层平均raw概率有超过99.5%落到单个专家，边际熵仅0.007–0.037nat，与全局soft偏置及bias补偿的解释相容；其余2层并无同等坍缩，且这些诊断未独立识别NLL变化的原因。原始值见D13_A6_raw_probability_marginals.csv。下一步优先考虑A0/A1/A5配对复现及分发尺度控制，尚未授权新训练。

## 实际设置与比较

执行根[/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer)。共同初始资产checkpoint_moe_baseline_dense_aligned_initial_20261030；数据dclm_pair_v1；训练至330亿token的MoE teacher与sae_moe_baseline33b_gate_input_formal_1b_20261104的blocks.7.norm2输出；DEV/EVAL资产dataset_teacher_routing_dev_eval_20261109和representation_teacher_routing_sparse_codes_20261109；原子分组analysis_r04_atom_groups_frozen_20261109。模型507,988,992参数、8层1024、16Q头/8KV头/head128、8专家Top2/expert1536、vocab151936/tied embedding。seed17、seq2048、4rank×micro16×累积2，每步262144有效token。AdamW β=.9/.95、ε=1e-8、wd=.1、lr3e-4、warmup1000后恒定、clip1、bf16/TF32关闭。负载bias每步0.001 sign更新，无均衡辅助损失。

## Protocol符合性与数值边界

| 项目         | 预期                             | 实际                                                              | 影响                                  |
|:-------------|:---------------------------------|:------------------------------------------------------------------|:--------------------------------------|
| 资源         | share 4H100 Reserved             | pt-lcxcxgyw；原pt-nmcuobkl冒烟后控制器失败，正式更新0，修复后续提 | 排队不代表更新；无P12                 |
| 输入/配置    | 复用A0与冻结teacher/SAE/DEV/EVAL | 输入strict与冻结分组已登记                                        | 访问不替代数值/训练完成               |
| 旧checkpoint | 每250步位置数据                  | A0四点；A4/A1-deep各两点；A1/A2各八点                             | 250步账本缺失；共同1000→2000补充      |
| NLL复现      | 逐位一致                         | 见position_consistency.csv，存在微小非零差                        | BOUNDED，未放宽训练冒烟门             |
| 新臂位置数据 | 由bf16快照复算                   | 同一次FP32训练评估直接捕获                                        | 避免快照舍入偏差；快照照存            |
| 恢复冒烟     | 真实中断恢复                     | step10完整存档后外部SIGKILL，再续至20                             | PASS须看真实smoke_summary，不提前宣称 |
| teacher精度  | 沿用A1记录                       | bf16；Top32索引一致率0.98962                                      | 与EVAL FP32编码存在接口差异           |
| P4固定路由   | χ约0                             | 按实测硬Top2；动态bias未冻结                                      | 不得人为零填充或作纯因果结论          |

单种子seed17；仅2000步/每臂524,288,000有效训练token；teacher训练时见过这些训练token；可学习路由的集中可能是学得好的结果；A6用同一SAE字典优化和测量，存在循环风险；teacher bf16的Top32单索引一致率98.962%，沿用原A1选择；旧臂缺失部分checkpoint，账本区间不一；位置SE未消除文档内相关；总体复算与原四卡评估并非全部逐位一致；fp16存储差另报。

## 结果与证据链

| arm     |     总体NLL |     M中位数 |   频次加权logM |        bin0 |        bin1 |        bin2 |
|:--------|------------:|------------:|---------------:|------------:|------------:|------------:|
| A5      | 4.039118998 | 1.344967711 |   -0.080334963 | 3.720251498 | 3.872186784 | 3.865717683 |
| A0      | 4.083141622 | 1.010460056 |   -0.401735217 | 3.794580477 | 3.942305977 | 3.929827148 |
| A1-deep | 4.085093112 | 0.870828768 |   -0.360922850 | 3.789857108 | 3.930946271 | 3.917200750 |
| A4      | 4.129441802 | 0.810891851 |   -0.472061195 | 3.867186691 | 4.009898194 | 3.986286052 |
| A1      | 4.157604347 | 0.585752336 |   -0.453948743 | 3.901086299 | 4.028563391 | 3.998681224 |
| A6      | 4.174997252 | 0.924780174 |   -0.284026317 | 3.985564060 | 4.104733180 | 4.059321536 |
| A2      | 4.286027700 | 0.256798644 |   -1.345580429 | 4.187885924 | 4.277627418 | 4.202913688 |

|读数|直接来源|计算|允许解释|
|---|---|---|---|
|总体与十bin NLL|[/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/A1_eval_nll_by_step.csv](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/A1_eval_nll_by_step.csv)|原训练时同一2M位置评估|单种子条件下实际学习读数|
|逐原子M及各层|[B3](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/B3_Mbar_distribution.csv)与[per_atom](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/per_atom)|覆盖/纯度/DEV频率公式|几何/分发统计，非训练收益|
|D1/D2|[D1检查](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/B4_D1_checks.json)/[D2来源](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/D2_source_manifest.json)|前者逐checkpoint；后者复用冻结只前向诊断|D1原跨越预测不成立；D2不是独立训练干预|
|收益–集中相关|[B6](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/B6_gain_vs_concentration_spearman.csv)|全体有覆盖原子与n≥50补充，10bin|描述相关，不识别中介|
|账本δ、SE、q、χ|[C8](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/C8_learn_forget_ledger.csv)/[共同区间](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/C8_matched_1000_2000.csv)|固定支撑位置配对差，BH及阈值；真实硬Top2集合翻转|位置变化与路由变化的关联|
|t50|[C9](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/C9_t50.csv)|从250步起净改善达到末端一半|离散、受正改善选择约束|
|例子|[C12](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/C12_examples_decoded.md)|首/末相邻区间显著原子；Top3激活上下文±20，限制在同序列|可读实例，不重新定义原子语义|
|正则诊断|[/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/D13_A6_regularizer.csv](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/D13_A6_regularizer.csv)|每50步H3/覆盖/CE与reg梯度/熵/负载bias|只有A6实际训练后可读；未生成则BLOCKED|

## P1–P4、解释与下一判断

| prediction   | AI_analysis                                                                                                                                                                                                                                     | researcher_judgment   |
|:-------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------|
| P1           | 综合AI判定：NOT_SUPPORTED_OR_MIXED；方向非支持；A6−A0的M中位数=-0.085679882，低频幅度见原表。；所列逐指标差异均超过各自相邻checkpoint变化参照。                                                                                                 | Unknown               |
| P2           | 综合AI判定：INSUFFICIENT；方向非支持；总体差=+0.091855630，bin0–2差=[0.19098358296192108, 0.1624272028831233, 0.12949438803992175]；不足（小于预设相邻checkpoint参照）。；逐指标不足：eval_nll,bin0,bin1,bin2的差异小于各自相邻checkpoint参照。 | Unknown               |
| P3           | 综合AI判定：DIRECTIONALLY_SUPPORTED；方向支持；A5−A1的M中位数=+0.759215375，NLL=-0.118485348；超过总体相邻checkpoint变化参照。；所列逐指标差异均超过各自相邻checkpoint变化参照。                                                                | Unknown               |
| P4           | 非支持当前简单预测：A1在共同1000→2000区间的实际位置翻转率为0.198141，固定score不等于固定映射；A4与A1-deep的高翻转四分位也未呈最高遗忘率；对翻转的因果归因仍不足，按分位原表报告。                                                               | Unknown               |

冒烟后、正式前的[机制解释分支](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/interpretation_plan_after_smoke_cn.md)不改原目标或P1–P4。最强竞争解释与当前AI分析见[汇报稿](/data/250010109/Research_System/daily_research_reports/1111/meeting_report/atom_concentration/report_cn.md)。未隔离梯度噪声中介；下一科学决定Unknown。

## 执行与产物地图

训练入口[scripts/r04.sh](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/scripts/r04.sh)→[runner.py](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/runner.py)→[train.py](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/moe_baseline/train.py)；[A6配置](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/arms/A6.yaml)/[A5配置](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/arms/A5.yaml)。原代码快照code_origin与实际run resolved_config分开保留；接管改动见[evidence/codex_takeover_audit.json](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/evidence/codex_takeover_audit.json)。

当前任务ID pt-lcxcxgyw；冒烟资格来源任务pt-nmcuobkl已因摘要变量错误终止，修复与恢复提交见[evidence/controller_repair_receipt.json](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/evidence/controller_repair_receipt.json)。运行事件[evidence/runner_events.jsonl](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/evidence/runner_events.jsonl)、[pod持久日志](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/acp_receipts/pod)。冒烟摘要[runs/smoke_summary.json](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/runs/smoke_summary.json)、λ冻结[evidence/lambda_frozen.json](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/evidence/lambda_frozen.json)、[外部kill](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/evidence/external_kill_smoke.json)、[完整恢复状态比较](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/evidence/full_resume_comparison.json)、[删除回执](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/evidence/smoke_deletion_receipt.json)只在实际生成时成立。

完整存档：每臂runs/A*/checkpoints保留最近2份、milestones保留2000步终点，均含model/AdamW/scheduler/RNG/游标/bias；每250步weights/存bf16快照。删除清单、字节数和新存档哈希在每臂deletion_receipts.jsonl和manifest.json。smoke产物按授权删除，其摘要与删除回执保留；没有保存的早期完整状态不能宣称可恢复。

输入访问[evidence/input_access_codex_20261110.json](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/evidence/input_access_codex_20261110.json)；资产登记由[register_outputs.py](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/register_outputs.py)产生evidence/asset_registration_*.json、output_access_*.json和saved_artifacts_A*.json，只有实际存在的产物才登记。分析来源由[evidence/analysis_manifest_seven.json](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/evidence/analysis_manifest_seven.json)与position_manifest记录。

完整[覆盖账本](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/coverage.md)列出DONE、BLOCKED和缺失依赖。复现：在执行根运行python analysis/forward_positions.py（只读已有模型），再python analysis/finalize.py和python analysis/write_records.py；CUBLAS_WORKSPACE_CONFIG=:4096:8。所有表CSV/MD，图PNG/PDF；[图表注释](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/figure_table_notes.json)。三项复核在evidence/audit_1_identification_cn.md、audit_2_statistics_cn.md、audit_3_implementation_cn.md。没有commit/push。
