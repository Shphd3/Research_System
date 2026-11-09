# checkpoint、训练轨迹、数据与测试基建

六个请求点全部存在，均已实际完整SHA、原生严格加载和评分。两模型实际3,000,000,000／15,000,000,000／17,000,000,000有效训练目标token，优化步11446／57224／64854，严格对齐，无插值。冻结选择文件仍保留加载前状态；完成事实以逐模型receipt和[新清单](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/audit/checkpoint_manifest.json)为准。

| Model | Actual tokens | Optimizer step | Actual state path / SHA256 |
|---|---|---|---|
| Baseline | 3000000000 | 11446 | `/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/runs/formal/milestones/token_003000000000/state.pt`<br>`70c8b3b7239c4bbd47e2498b26d1eed55c392155b5c8657f92d15947764d5fd7` |
| Baseline | 15000000000 | 57224 | `/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/runs/formal/milestones/token_015000000000/state.pt`<br>`99354d417a8657ed4d9d427e4a068026baa903489e6495cd8e27231e709e90e4` |
| Baseline | 17000000000 | 64854 | `/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/runs/formal/milestones/token_017000000000/state.pt`<br>`26e08b8795bd96e46bacc727ce448c830f7050ba5e285864d31a82400afd3b59` |
| Dense | 3000000000 | 11446 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/milestones/token_003000000000/state.pt`<br>`a2ae7f02bf3f8eabf217cc9f780b0c87b0ce0f103d7ecc7f4652f191c3e6ff1b` |
| Dense | 15000000000 | 57224 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/continuation_checkpoints/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/target_015000000000_actual_015000000000_step_00057224/state.pt`<br>`1956120a63a6cd555bd90eca7883413367611117f0f3574079d1d1159bdc2c4f` |
| Dense | 17000000000 | 64854 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/continuation_checkpoints/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/target_017000000000_actual_017000000000_step_00064854/state.pt`<br>`890925657c576192f07c18d14c03a539ca7e8d6a15e29fb56c41ca48cabb6cb3` |

[基建标量与配置来源](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/audit/infrastructure.json)核实保存的tokens_seen、optimizer_step、配置hash和当前原生源码；[本次访问核查](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/audit/input_access.json)不替代这些加载核查。权重和MoE负载偏置均冻结，无训练优化器。

Dense总／常规激活参数281,431,040；普通MoE总507,988,992、常规激活281,496,576，8专家top2。两者均8层、隐藏1024、上下文2048。激活参数近似不等于实耗FLOP相等。[原训练来源](../R01_behavior/training_assets_cn.md)拥有AdamW、数据和完整历史，本轮核对源码hash及六实际状态，没有重跑历史训练或样本顺序审计。每种模型仅一条seed17轨迹，容量／硬件历史不同。历史数据顺序仅核实对齐至22,018,691,584token；六点均在此前，后续分歧不能直接解释这六点，但仍限制R01整条轨迹比较。

## 原R01数值复算

37个原始分数文件重新hash并重算成对成功，Dense14／Baseline23，共14208提示；当前stat／大小也核对同37个权重路径，但本轮只有六个权重重新加载。[原完整清单](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use/audit/inventory.json)保留所有缺失、归档恢复和别名，不用插值补点。[本轮复算receipt](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/audit/r01_replay.json)。

| Model | R01 gap | 60% first sampled | 80% first sampled | 90% first sampled |
|---|---|---|---|---|
| Dense | 16 | 3 B (20/24) | 3 B (20/24) | 5 B (23/24) |
| Dense | 1024 | 3 B (19/24) | 15 B (21/24) | 19 B (22/24) |
| Baseline | 16 | 3 B (24/24) | 3 B (24/24) | 3 B (24/24) |
| Baseline | 1024 | 3 B (23/24) | 3 B (23/24) | 3 B (23/24) |

Dense的80%首次采样达标为近3B、远15B；Baseline均3B。60／80／90%沿用原描述口径，没有事后更换。它们不是稳定掌握或准确出现时间，回落、门槛敏感和24旧家族限制保留。R01的p=1151，正确值末token分别e1134／894／126，对应gap16／256／1024；gap=p−e−1，首答案下标1152。

## 冻结文本、距离和标签校验

实际Qwen3 tokenizer同R01，无BOS／chat模板；tokenizer.json SHA256 c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539。[构造receipt](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/audit/construction.json)保存全部校验；[每条完整文本及token位置](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/data/panel.jsonl)，[家族定义](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/data/families.json)。24个旧主家族×2世界×2锚点距离=每状态96前缀；另六个旧工程家族，每模型24 smoke前缀。没有新家族独立确认。

真实T1_F1：A为box→key、bag→spoon；B为bag→key、box→spoon，都查box。两个世界仅两个实体token互换，值次数／顺序／位置、其他字节均一致。原生tokenizer确认实体各1token，程序解析绑定验证标签翻转；均先于模型评分。

| World | Anchor gap | Value token positions | Correct value | Correct-value gap | Block tokens | Prefix last / first prediction |
|---|---|---|---|---|---|---|
| A | 16 | {'key': [1128], 'spoon': [1134]} | key | 22 | 12 | 1151 / 1152 |
| B | 16 | {'key': [1128], 'spoon': [1134]} | spoon | 16 | 12 | 1151 / 1152 |
| A | 1024 | {'key': [120], 'spoon': [126]} | key | 1030 | 12 | 1151 / 1152 |
| B | 1024 | {'key': [120], 'spoon': [126]} | spoon | 1024 | 12 | 1151 / 1152 |

所有前缀1152token，值本身1token，完整候选为前导空格＋词＋句号、2token。关系块10–16token；固定锚点为最后列出的值B，gap16／1024，正确值另报近16–24／远1024–1032。逐行有绝对offset、值／块跨度、块末gap、查询和最终预测下标。全部含8token生成预算均不截断。近远移动关系块时有1008个填充token从前移到后，匹配总长、问题、预测位置与token多重集合，绝对位置和竞争项仍变化。

只取最近值、词频或固定候选在两个世界给同一答案，不能通过两侧同时正确；这是构造层检查，不指定模型内部算法。家族内查询实体固定，未交叉另一个查询，实体词汇先验与查询作用仍未完全拆开。没有独立新改写、多跳或低曝光验证。[四层定义](definitions_cn.md)另列实例。

## 原始输出和统计

完整候选FP32逐token条件log概率求和为主，平分失败。首词／无句号／长度平均作为敏感性；候选等长，平均不改变完整排序。生成不限制候选，greedy最多8token、首标点或EOS停止；仅判开头首个词，可略去一个开头the/a/an，OTHER全部失败且保留。先生成冠词会改变名词的条件前缀，因此生成与直接候选排序分开。

六个[逐状态原始文件](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/results/full)各含96绑定行、96旧任务FP32候选参照及新receipt；[家族表](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/tables/family_results.csv)288行保留两世界分差、Δ和两种成功；[逐样本](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/tables/sample_results.json)、[汇总](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/tables/summary.csv)、[模板／类型](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/tables/template_type.csv)、[近远配对](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/tables/near_far_paired.csv)、[同精度旧新](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/tables/R01_FP32_comparison.csv)、[两条轨迹差](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/tables/model_trajectory_difference.csv)全部可读。家族配对和六模板聚类区间均不代替训练seed不确定性。

资产ID与英文伴随页一致；[复查说明](reproduce_cn.md)、[artifact manifest](artifact_manifest.json)给出处。原始文本／权重／分数留执行侧，Git仅选主PNG及小型图数据。
