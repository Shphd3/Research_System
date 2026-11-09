# S15 详细记录与复算入口

本记录支持[中文总结](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/summary_cn.md)，不改变既有Focus、Anchor或S11/S13/S14结果。问题是DEV定义的共享／偏向成员是否伴随稳定的实际expert分布。竞争解释是负载、类别、词面、模板、位置、长度与其他共激活成员；本轮是观察分析，不是功能干预。研究者已在当前对话直接批准完成现有范围，附件旧阶段A等待被覆盖。科学接纳仍为Unknown。

## 实际计算与数据

固定普通MoE 33B token、原生末层router输入SAE，评估模式下只做6912条前缀前向；没有答案补全前向或新行为任务。取两个预定位置，得到13,824条观测。张量是原生norm2后的1024维向量，不另行中心化、单位化或替换父模型。SAE本身的偏置与编码方式由原生实现持有。

模型：`/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/runs/formal/milestones/token_033000000000/state.pt`。
SAE：`/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/runs/formal/sae_full_final.pt`。
原生实现：同SAE实验的`source/moe_model.py`、`source/e16_sae_core.py`；tokenizer：`/data/share/Qwen3-0.6B-Base/tokenizer.json`。严格可读记录见[evidence/input_access.json](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/evidence/input_access.json)，新算全文件摘要见[final_model_SAE_hashes.json](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/evidence/final_model_SAE_hashes.json)。

S14的panel为S13构造英语文本：8粗类及16细类，共24标签，4表达；DEV24家族／8场景簇、2304文本，CONF48家族／16不交场景簇、4608文本。全部CONF早已被查看；当前成员只从DEV决定仍不能恢复盲确认身份。`prefix`中历史保存字面`\n`，验证时还原为实际换行；保存token_ids已为实际编码，所有6912条验证相同。读取位置按各文本实际索引，末冒号ID25，正文位置常为句号加换行token，不能混称类别词位置。

Q参考原样复用2000 Magicoder题干、2000 GSM8K问题、2000 MMLU问题；G为6000 DCLM文档。各取原始前128正文token并按原规则附加读取后缀，无答案／选项，不重采。两套均为**同MoE、同SAE、同末冒号hook**的新S14缓存。参考出现率是count/6000，不是训练曝光次数、词频或知识长尾标记。正文没有本轮原生重选或原生频率匹配确认。

本轮没有训练／验证划分用于拟合，不使用这6912条小规模构造文本做训练集。继承S14完整答案序列对数似然的二选一行为资格（每侧至少0.75），用于限制语义解释，没有把行为门槛当路由指标。原评分位于S14/results/confirmation_scores.jsonl，固定身份纳入输入清单。

## 冻结规则、估计与可交换性

完整[英文协议](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/protocol.md)、[中文协议](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/protocol_cn.md)、[config](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/config.json)、[统计计划](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/statistics_plan.json)与[差异记录](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/amendments.md)共同描述实际时序。共享是DEV同一家族两侧交集出现率至少0.75，不是同token两个feature共同激活；偏向是两侧边际出现率差至少0.25且8个开发场景至少6个同向；普遍背景是DEV全24标签出现率至少0.90。共132个逐对候选角色、53个不同字典坐标；共享角色96、偏向36，普遍背景7个与共享有重叠。共享与偏向容许重叠，本次实际为0。

评估覆盖要求每成员×类别至少12/48家族、8/16场景；组指标至少80%相关角色达到，bootstrap至少95%有效。未出现则NaN；允许计算部分有观测角色的均值，但显式报告覆盖不足。Q1使用共享两侧及偏向各自侧的去重角色，Q2同一共享成员两侧，Q3各自偏向成员的等权条件分布。零距离也可能来自完全相同的token路由，不能解释成独立feature被有意聚合。

种子2026110815，1000次全局、1000次条件置换，共享2000次场景簇bootstrap。每簇3家族、24标签、4表达的相关结构保留。全局共同打乱标签角色；条件固定标签角色、表达与位置。条件长度分层退化为单层的实际记录见[exchangeability.json](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/evidence/exchangeability.json)。这些置换只在假设的场景可交换性下提供探索性参照，不能消除未测混杂。

主结果报每问题八类别Holm8及三问题合并Holm24。逐成员Q1给全部成员×类别校正、逐对校正；expert差值另给八expert最大偏差同时bootstrap带。TV主区间是原始统计量的百分位区间，不是相对null的效应区间；未运行等价性检验。5个百分点只是事先展示筛选线，不是效用阈值。权重为事先指定次要分析；完整权重重采样代码在点估计可见后完成，另补全192次要比较校正，因此不作为新的事先主检验。

频率匹配不放宽门槛：同时匹配Q、G和DEV汇总出现率，各绝对差≤0.10，DEV至少0.125，最近32候选，按坐标稳定打破距离并列，抽1000个不重复成员集合。空池留缺项。充分参照至少800有效组；低于门槛保留所有数值但为不足。正文复用冒号匹配池，只作位置敏感性。

## 三条核查路径

| 路径 | 实际证据 | 结果与边界 |
| --- | --- | --- |
| 行为与控制 | 继承完整答案评分；类别负载；两种块置换；匹配池及有效数；改写／属性／情境／正文分表 | 主显式除家具外行为合格；主选择关联未决；长度未充分控制，大部分随机成员组不足，不能声称已排除所有竞争解释 |
| 表示 | DEV冻结成员；Q/G原生频率；同位置Top32与完整hidden；样本共有/仅一侧集合；feature×类别×expert、expert内部组成 | 新旧Top32全集一致；共享和偏向是统计角色，不是独立语义因子；多个成员不是独立样本 |
| 功能与质量 | 重建相对平方误差、冻结router对重建向量的离线敏感性、原生路由复算、行为资格 | 能检查工具接线和部分信息保真；未进行expert消融、替换、功能任务或训练，专家效用与学习收益Unknown |

主结果、缺项和一项AI建议由[summary_cn.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/summary_cn.md)完整持有。全部192个主表行保留；正文餐具等大距离但覆盖不足，属性／情境行为失败，均不转成主结果支持。无新独立确认，`NOT_RUN_NOT_APPROVED`。没有自动升级到功能或训练对照。

## 原始数据字典

| 文件／字段 | 结构、单位与含义 |
| --- | --- |
| data/token_records.jsonl | 6912行；row为张量第0轴；原文、prefix、token_ids、family、cluster、split、wording、label、target_index、body_index。索引均零起算 |
| data/observations.npz | 原始完整采集，含hidden；第1轴固定colon/body，不能按全局同绝对索引解释 |
| h | [6912,2,1024]，实际router输入FP32 |
| logits / probability | 各[6912,2,8]，原8维logits及softmax；probability尚未加bias |
| selected / weight | 各[6912,2,2]，实际专家ID及所选原概率归一化权重；weight每位置之和1 |
| indices / values | 各[6912,2,32]，同一向量的SAE正Top32坐标和值。所有保存值均>0；未入选的0不是preactivation=0 |
| load_bias | [8]，保存的负载偏置；以probability+bias作选择；共同偏移不影响排序 |
| metrics | [6912,2,6]，列为平方误差/输入平方和、输入L2范数、z的L2、重建Top2槽位重合比例、重建原softmax的L1变化、最大logit变化 |
| data/token_routes_without_hidden.npz | 与完整观测相同但省h；原始h仍保存在observations；不声称小包独立含有模型权重 |
| results/token_routes.csv | 13,824行，展开上述每位置观测；8维和32维字段以分号保存。与token_records按row连接 |
| feature_groups.csv | 132行逐对成员；DEV两侧频率／场景支持、Q/G频率、组标记、CONF覆盖；跨对同坐标可能重复 |
| feature_expert_statistics.csv | 16,896行；两个位置×4表达×成员类别×8expert；入选概率、r/2质量、类别基线、差值、区间、原始／校正p、gate与幅值敏感性 |
| results/primary_questions.csv | 192行，两个位置×4表达×8类别对×3问题；原TV、区间、两个null均值／差值／p及Holm8/24、资格 |
| results/gate_weighted_resampling.csv | 192行权重次要比较；同样重采样区间、p、Holm8及补充全192校正 |
| results/expert_internal_feature_composition.csv | 16,896行，expert入选时的feature出现率、联合／边际计数；分母为0留NaN。成员可重叠，不形成总和1的语义模块 |
| results/sample_set_changes.csv | 3072行，48家族×8对×4表达×2位置，逐对交集／仅一侧ID、Jaccard、完整expert对；描述样本集合更替，不重新挑候选 |
| results/frequency_matched_reference.csv | 实际有效抽样、控制均值／范围及不足；body另标同位置参考=false |
| data/resampling_indices.npz | 全部固定2000bootstrap权重及1000+1000完整行映射，可按exchangeability.json还原场景、家族、标签轴 |
| data/frozen_random_member_sets.npz | 冻结随机成员抽样，-1表示某位置未能抽出，不是feature编号 |
| results/case_rows.csv | 10个案例行，连回原始row和文本ID；不是10个独立试验 |

额外小表的字段名与计算见[code/analyze_routes.py](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/code/analyze_routes.py)；全部文件摘要与字节数见[artifact_manifest.json](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/artifact_manifest.json)。原始数据在执行侧，项目内仅放说明与核查入口。

## 复算、预算与失败

本机已存在H100 MIG 3g40GB，未申请或提交作业。FP32、TF32关闭、batch16；前向24.579秒，峰值2.194GiB，低于12GiB／1800秒边界。统计主脚本16.54秒，权重5秒量级；独立主复算27.00秒、次要18.89秒，均CPU。版本见[evidence/runtime.json](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/evidence/runtime.json)。

两次独立复算分别在[verify_independent.py](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/code/verify_independent.py)和[verify_secondary.py](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/code/verify_secondary.py)，使用原始行、显式重算路径及已保存重采样索引，不用已汇总表代替原始数据。全部route logits CPU最大差2.15e−6、权重最大差9.66e−8；32个SAE位置最大差4.58e−5（均在1e−4内），集合严格一致。全部384点估计误差0，主条件硬／权重各24区间与48p完全复现。源码冻结摘要保持不变。输入模型、SAE最终全文件摘要与S14相同；参数版本、requires_grad和bias检查均保持冻结。

首次采集因默认路径无tokenizers在观测前失败；复用已有`/data/250010109/dependency_packages/hf_transformers_qwen3`后成功。案例脚本首次重复解压缓存过慢，停止本轮自身进程后改为一次读入，数值未改；图三补空心不足标记。保留首次日志、旧案例代码及修复说明。描述表在主检验后导出，不新增假设检验；主输出不改。所有失败、时序与事后性质见[amendments.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/amendments.md)。

可从当前执行目录进行CPU复算：

```bash
python code/verify_independent.py
python code/verify_secondary.py
```

验证需要原始输入权重和已有依赖可见。不要把`analyze_routes.py`当只读验证运行，它会重写本轮派生结果与冻结记录；已保存的原始输出和摘要应先保留。config.json固定原始权重及参考源地址，S14是必要的相邻目录，压缩包是阅读和原始表交付包，不是携带全部权重的自包含执行环境。必要GPU采集命令与当时日志在collect_routes_retry.log；不建议为阅读结果重复前向。

## 状态与材料入口

[task_coverage.csv](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/task_coverage.csv)逐项区分完成、尝试后证据不足和未获准新确认；[evidence/](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/evidence)持有接线、冻结、完成、匹配可交换性和复算记录；[sources/](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/sources)保留上传协议和旧案例实现。结果图的源表、单位、抽样与解释边界见[figure_lineage.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/figure_lineage.md)。没有训练配置改动或权重输出，没有commit／push／发布；当前科学验收Unknown。
