# Detailed：CC_FEATURE_RELATION_PHASE1

[中文总结](summary_cn.md) · [English Summary](summary.md) · [冻结Protocol A1](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/frozen_protocol.md) · [当前Protocol](protocol.md)

## 0. 结果与资格

阶段一材料完整交付。发现原始边214,711，复核通过206,136，约简后146,947；候选4对。当前实测支持“存在可复核且可定位的统计对象”，没有证明主题一致、因果关系或学习收益。高J共有8项中的7项是Top10背景；机制与未来训练判断留待研究者。task_state=COMPLETE；question_state=OPEN；design_state=APPROVED_FOR_PHASE1_FULL_ANALYSIS；result_state=MEASURED_AWAITING_HUMAN_REVIEW。正式Focus未绑定；依本对话显式选定Protocol执行，未创建或修改Focus／Anchor科学状态。

## 1. 对象、判据与对齐

特征是最终联合CrossCoder编号0–16383；激活由14层共同编码。每个位置共享同一z，各层解码向量不同。组成列表是传递约简后的直接出邻居；箭头A→u表示A出现时u常出现且u更常见。固定支持nA≥200、nu≥200、nAu≥20；精确整数判据5nAu≥4nA、2nAu≤nu、nu≥2nA；先复核发现原始边，再约简。频率沿箭头至少翻倍，故无环是定义推论，不是实测发现。J=交集／并集；空并集NA，单方空列表J=0但仅作诊断。正式候选四个D/V列表均非空，A/B在两侧都支持≥200。

## 2. 冻结与修订

用户2026-10-14北京时间一次性确认设计、实现和启动。A1将正式主动上限从120改为220分钟；固定128完整上下文块、种子20261014；Top10仅追踪固定候选，从删除节点后的原始图正确重算；完整缓存只生成一次；无候选诊断规则保留。性能smoke豁免，不写PASS。科研问题与固定门槛未改变。冻结Protocol SHA256：`16dd4dd46fd3c301a8a39919da7680bf97f1e787d6f4cb9b1b5772d7acb403dd`；Anchor SHA256：`efedd70106a143475ce3de597ba7193acccb4c749520ab9b58117c08736712b1`。

A1-E1：首次任务pt-io5c5h2p在生成激活前因整数接口要求矩阵M>16失败。逻辑16特征人工矩阵补零至32、小候选池同样对齐；计数定义不变。41.221134秒计入总预算。接续任务pt-zwh6g95p完成。冻结代码版本A1_IMPL_2；原始代码快照、失败日志均保存。A1-E2：交付核对补齐全节点D/V列表比较、空列表J=0诊断表、机器图侧文件相对地址、文本可用数提示；仅使用已保存结果，没有重新推理或全池排名，没有改变候选。

## 3. 实际设置

最终checkpoint：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt`。累计999,997,440训练位置、244,140更新；本次训练更新为0。Base `/data/share/Qwen3-0.6B-Base`，revision da87bfb608c14b7cf20ba1ce41287e8de496c0cd。选择零基层1,3,...27，即一基2,4,...28；hook是block residual-post、最终全局norm之前。16384共享特征，完整FP32主状态；BF16 Base/GEMM、FP32分数与严格冻结阈值0.051281172782182693。固定TRAIN均值中心化与向量RMS归一化不重估。推理保持16个1024-token完整上下文/Base forward、1024合格位置/coder batch、原4个rank区间，SDPA设在模型及backbone配置。

数据：既定单bin完整VAL10,485,760合格位置，10,249上下文；81块，发现5,238,097、复核5,247,663。尾块保留，固定种子置乱后按合格位置数贪心平衡，平局由种子决定；未根据激活或文本切分。原文档和近重复独立性UNKNOWN，VAL曾暴露于训练评估。

缓存CSR：uint64 rowptr、uint16特征ID、FP32正激活；2,669,034,642非零值。唯一行键为固定VAL合格位置编号，可通过index_val records/prefix、排除ID映射到源SHA、绝对偏移及原始上下文；没有原文档ID。统计INT8矩阵输入、INT32分块输出、INT64累计；未缩窗、截断对象或仅统计高频特征。完整共同计数D/V及120,380,886个合格配对的交并集机器表已保存。

## 4. 正确性与失败拆解

方向与阈值人工例通过；30个DAG及90次删除与独立NetworkX约简一致。GPU人工4095+14=4109；真实256位置全16384特征与朴素枚举逐项一致；编码后门控与原始完整forward一致；查验小片段两种batch切法无差异；Base保持冻结，coder buffers不变。所有16384命中次数与原最终验证完全一致。完成核对：全部214,711原始边逐块D/V加总一致，4对J／资格和118条文本z／类别一致。图已实际查看：16面板联系表、密集面板原图及热图，标签可读、无裁切；来源数值与CSV/计数表一致。源码数学检查不等于图渲染或科研真值。

首次失败是实现接口约束；没有否定数学模型或科研机制。所有后续阶段完成，缺项列表为空。both=0属于实测空类别，不是未执行；1/17的both只有2位置按实交付。

## 5. 证据链

| 事实／计算 | 来源 | 口径与限制 |
|---|---|---|
|214,711发现原始边；206,136复核通过|[逐边计数](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/raw_edges.npz)、[失败原因](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/edge_review_summary.json)|复核仅检查发现边；非独立重新发现V图|
|146,947复核约简边；组成列表与深度|[D图](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/reduced_D.json)、[V图](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/reduced_V.json)|完整16384节点；边方向是统计包含，深度不是模型层|
|4对候选，J=1、1、0、0|[候选完整指标](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/pair_metrics.json)、[全池机器表](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/pairs)、[候选表](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/candidate_metrics.csv)|只搜索一次；非空列表及节点支持资格固定；并列组不按ID拆成高低；两对各共享一个锚点|
|高J共同8项中的7项为Top10|[背景计数](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/pair_metrics.json)、[10个删除版本](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/sensitivity.json)|删除从原始图重新约简相关可达子图；只追踪固定候选；不排除多个背景共同支配|
|全214,711条发现边的81块计数|[逐块数组](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/block_edges)、[分位数](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/edge_block_summary.npz)|每条边分块D/V加总与完整计数逐项一致；分位数不是独立抽样置信区间|
|118条文本；both缺项或稀少|[可读文本](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/pair_examples_cn.md)、[JSON](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/pair_examples.json)|复核侧随机与高激活；类别以目标位置为准；重合保留双标签；零样本不补造|
|14层解码贡献与原始数值|[逐层CSV](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/layer_contribution.csv)、[解码几何](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/decoder_geometry.npz)、[图册](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/figures_cn.md)|同一z共享跨层；幅度占比等于范数占比；不是因果贡献|
|全部16384个特征命中次数原验证一致|[复现核对](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/original_validation_replay_check.json)、[缓存](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/feature_cache/manifest.json)|完整窗口、冻结阈值与原始推理，不改变统计对象|
|空列表J=0诊断及各节点D/V列表J|[空列表诊断](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/empty_list_J0_diagnostics.csv)、[节点列表复核](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/node_composition_stability.csv)|20个支持充分但空列表节点，与固定非空参考配对；不进入正式池，不重复全池排名|

## 6. 竞争解释与允许结论

候选主题、词汇、格式与上下文解释尚未被独立干预。高J两对的共同项87.5%来自Top10；逐个移除J不变不能排除共同背景。两对高J同样不意味着频繁直接共现：1/17复核共同支持仅2、lift=0.028515。0/3共同支持0不证明本体上不存在关联。候选频率未匹配，四对共享两个锚点，不是独立重复。文本只作可读材料，不自动认证单义语义。14层幅度占比恒等于解码范数占比；第28层重构FVE86.4722%、替换CE+0.305962nats保留为工具限制。没有检验共享／分离学习H1，未开展难学内容测试。

## 7. 运行记录与资源

主任务pt-zwh6g95p平台SUCCEEDED与持久终端COMPLETE一致；首次pt-io5c5h2p失败已归档。4 H100 Reserved、实际88 CPU时间核/960GiB，CPU最多10个独立敏感性进程，图D/V并行2进程，每进程BLAS1线程。正式主动计算及交付计数核验合计10.51分钟（含首次失败41.22秒），上限220分钟。记录的新增磁盘峰值43.05GiB，CPU RSS峰值11.41GiB。特征阶段单卡allocated记录峰值4.83GiB；其他阶段不补造未持久记录的全程GPU峰值，代码分块界限及64GiB守卫保留。无资源扩展。

| 阶段 | 工程状态 | 本次秒数 |
|---|---|---:|
| 01_sparse_features | COMPLETE | 127.07 |
| 02_exact_counts | COMPLETE | 87.48 |
| 03_merge | COMPLETE | 121.11 |
| 04_raw_edges | COMPLETE | 2.37 |
| 05_reduce | COMPLETE | 2.44 |
| 06_pairs | COMPLETE | 39.41 |
| 07_sensitivity | COMPLETE | 2.91 |
| 08_block_counts | COMPLETE | 29.13 |
| 09_block_summary | COMPLETE | 12.56 |
| 10_inspection | COMPLETE | 134.12 |
| 11_delivery | COMPLETE | 25.86 |

本轮：问题是联合特征关系能否复核并得到可读候选；设置与固定项如上；无训练数据或优化，分析使用完整既有VAL；发现／复核同bin块切分；结果与证据链如上；认识变化是已有可读统计对象，但背景解释仍强，未来学习收益未知。研究者下一步决定仍Unknown。AI建议共同检查文本及背景代理适用性；交付后停止，不自动下一阶段。

## 8. 复现与资产入口

- [运行清单](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/run_manifest.json)、[执行证书](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/execution_certificate.md)、[精确输入](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/input_identity.json)、[设计快照](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/design_snapshot.json)。
- [冻结实现](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/code_snapshot_manifest_v2.json)、[原训练代码复用核验](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/source_manifest.json)、[完成核对脚本](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/completion_audit.json)。
- 缓存资产：`representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z`；分析资产：`analysis_crosscoder_feature_relation_phase1_20261013t173130z`；[本次访问检查](../../../../../../assets/checks/2026-10-14_crosscoder_feature_phase1_outputs_20261013T173130Z.json)。
- [完整文件清单](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/output_manifest.json)、[交付终端](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/delivery_receipt.json)。缓存及大数组保留执行侧，不提交Git。

原始复现命令绑定执行包中的code_snapshot_v2/launch.sh及本run_root；已完成阶段通过receipt复用，运行或扩展另需明确授权，本交付不自动再次启动。
