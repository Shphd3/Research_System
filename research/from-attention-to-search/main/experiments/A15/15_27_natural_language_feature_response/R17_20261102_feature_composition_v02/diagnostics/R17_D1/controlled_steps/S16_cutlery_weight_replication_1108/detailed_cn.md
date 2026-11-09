# S16 详细证据与复算

[中文总结](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/summary_cn.md)拥有完整图片说明、主要数值与资格边界；[英文协议](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/protocol.md)和[预响应冻结](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S16_cutlery_weight_replication_1108/evidence/freeze.json)持有准确口径。本轮为R17_D1/S15的支持性复核，不把历史Focus R10状态或Qwen字典当作本MoE实验授权。

## 输入、原生实现与授权

config.json给出模型/SAE/tokenizer/source绝对路径；当前strict结果evidence/input_access.json、new_dataset_access.json。固定父模型为普通8层MoE token_033000000000；33B是训练token数。父模型/SAE与S15完全相同；不是官方Qwen3SAE，featureID不跨字典对齐。evidence/final_input_hashes.json新算全文件摘要对照S15，仍相同。evidence/freeze.json固定全部输入文本、成员、方向、配置、协议及infer/analyze/verify/common/stimuli/prepare源码。源码都早于新模型结果；后写翻译、图、报告未冒充预冻结。

数据由code/stimuli.py持有24个物理场景、每场景2事件家族，每个事件两种表达，各自spoon/fork配对。data/panel.jsonl为192原始输入，data/scene_templates.csv可人工审读，length_pairs.csv有96个精确同长度配对。old_overlap_check.csv与data_preflight.json记录旧面板重叠；最大词4-gramJaccard=.05，0精确重复。只证明文本层面新增，不排除共同作者、后缀和语义领域，不作自然总体抽样的声明。

code/infer.py明确复用并适配S15原生route观察与S14完整答案评分。它把两候选附在同一前缀之后，观测答案之前的末冒号；因果掩码校准prefix-only与延长前缀隐藏差≤4.77e−6，原始路由集合相同。批单误差≤4.05e−6，候选反序评分差1.24e−5，均在1e−4内；校准说明见evidence/calibration.json。没有用答案位置替代前答位置。所选成员只从旧S15读取，不根据新行为或路由筛选。

## 张量与原始表

data/token_records.jsonl与panel.jsonl按row和observations第0轴连接，均192行。data/observations.npz的h[192,1024]为实际router输入；logits/probability[192,8]；selected/weight[192,2]；indices/values[192,32]；load_bias[8]；metrics[192,6]依次为相对平方重建误差、输入L2、zL2、重建Top2槽重合率、概率L1变化、最大logit变化。原生route选择softmax概率+bias的前2，再对所选原概率归一化，故weight和为1。保存SAE值全部正，0仅指该坐标没入选Top32。

results/token_routes.csv为192条逐位置展开记录；behavior_scores.jsonl保存每个候选的两个token概率、总分、选择与正误。results/member_expert.csv为两表达×8固定成员×2类别×8expert=256行，保留目标侧与交叉侧、包括低覆盖。group_profiles.csv为32行，category_loads.csv为32行，replication.csv为2个预定条件，pair_counts.csv为各条件全部expert组合。resampling_indices.npz保存9999+9999行映射、2000bootstrap权重与长度层；statistic_draws.npz保存各次统计和方向，不填0补缺失。

注意：member_expert的交叉侧用于保留信息，Q3仍只用A偏向在spoon、B偏向在fork；不因交叉侧更好而更换。固定平均使仅出现一次的#23973仍占A组三分之一，故覆盖门槛至关重要。部分bootstrap副本成员缺失时按预冻结的有效成员均值；全部有限2000次并不保证整个固定组支持充分。主要结论先由覆盖/行为判不足，不借描述性区间下界>0恢复确认资格。

## 统计、核查与例外

code/analyze.py从原始数据算逐成员条件均值、等权Q3、类别基准、旧方向对齐及覆盖。精确A/B长度之外，条件场景长度两层实际14/10簇；通过整场景映射与共同两家族槽位保留类别负载、配对和表达依赖，不逐token或逐feature独立重抽。旧频率匹配池因空池/不足没有恢复，不另采可用成员。所有192文本保留，没有失败样本删除、扩样、重选阈值/成员或改主指标。

主判断不足：显式A/B组0/3与1/5合格，改写1/3与1/5；fork两表达34/48。条件p=.4859/.0946只作描述；改写以及全局参照不是替代主成功。signed方向均正不等于足够强或可靠。新旧场景分布改变，不能把两点差作为受控因果效应。

code/verify.py不导入生产统计实现，显式循环重建所有192router logits/softmax+bias选择/权重、全192SAE正Top32、两表达D/方向、95%区间与9999全局/条件置换p。evidence/verification.json为PASS，最大router差8.34e−7、权重差7.12e−8、SAE差1.43e−5；全部冻结文件摘要一致。CPU复算约9.2秒。行为分数由原生完整前向及候选顺序/前答因果/批单校准保护，本轮没有另以CPU重跑整个LM的192条行为评分。

原生测量在已有H100MIG3g40GB，FP32/TF32关闭/batch16，正式384候选序列及校准，9.85秒、峰值2.207GiB。inference_complete.json有参数版本、bias不变、无训练/提交记录。本轮无运行失败；图二、四初稿脚注与横轴挤压，图三共享轴反复反向使顺序倒置，已只修改布局/顺序再实际查看，不改任何数值。观测后未修改被冻结的科学代码或协议。

CPU复算入口（原权重/依赖需仍可见，会在本轮evidence更新复算时间，不建议仅为阅读反复运行）：

```bash
python code/verify.py
```

模型测量原命令记录在evidence/execution_commands.txt，inference.log为完整逐批进度。没有新训练配置或checkpoint输出。原始权重不放交付包，包内含所有本轮192hidden及路由，原始文本、候选评分、抽样索引、图表、协议、源码和日志。

## 状态与责任

任务覆盖见task_coverage.csv；三次比例适当的识别/统计/实现审计在evidence/audit_1.json至audit_3.json；图的读法和数据来源见figure_lineage.md。项目内保存本轮说明及摘要，执行侧保存原始payload；asset registry只登记实际已保存资产。没有改Focus/Anchor科学状态或旧S15结果，未commit/push或外部发布。新场景测量完成，复现成立仍不足；学习价值与下一研究判断Unknown。

报告阶段的成员出现率方向补表由code/export_presence.py从已有member_expert表派生，明确事后描述；无新模型前向、检验或成员选取。
