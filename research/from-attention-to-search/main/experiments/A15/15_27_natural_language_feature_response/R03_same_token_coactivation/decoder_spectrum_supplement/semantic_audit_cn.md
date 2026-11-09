# 谱段语义标签与表征配对资格审计

**问题3本轮未运行：未找到合格的“独立语义标签＋匹配raw h＋发现/留出”组合，当前前向剩余为0。** 这不是分类器实现不足，也不是语义不可分的阴性结果。路径、字段、形状与访问证据见[机器审计](semantic_audit.json)。本审计只读已有metadata、源码与train/development数组头；没有前向、PCA、分类器拟合、聚类或新统计。

| 已查对象 | 已核执行事实 | 为什么不能直接回答谱段语义可分性 |
| --- | --- | --- |
| 原phase1 `class_positions/` | 四类为A-only、B-only、both、neither；源码`inspection.py:101–115`直接由feature是否激活生成；数组存context及位置数 | 标签来自被分析的feature，不是独立语义真值 |
| A22 relation-learning `data/train.pt`、`data_eval512/eval.pt` | manifest记录train130712位置/128context，eval523136位置/512context；BF16最终block27 residual-post、final RMSNorm之前；来源是CrossCoder原TRAIN bin，不是封存TEST | 现有目标为真实下一token与R/F/N路由，没有可核查的独立语义标签。可作为匹配谱参考候选，不能硬换成语义验证 |
| 旧`report_spectrum`组条件谱与`winning_group_labels.npz` | 按原phi community、频率组、随机组winner或成员命中选择位置 | 是组/路由标签与条件选样谱，不是语义真值，也不是新C03的独立验证 |
| E18 M2D2及eight-task | 标签来源是3×3主题树/数据集身份，独立于簇编号；已有缓存只含`indices/values/window_ids` | 没有同模型、同residual-post hook的raw h。旧E16稀疏SAE坐标不能搬成A22的表征 |
| R03两份`*_A_far_hooks.npz` | 仅固定S01_A_far、R01_A_far两例；本审计未重载完整h schema | 缺配对A/B raw h、独立情境留出；两例目标词/类型不同，不能拿来做无混杂语义验证 |

E18实际数组头：M2D2 train的indices/values为`(196734,32)`，development为`(441792,32)`；task train为`(674993,32)`，development为`(83054,32)`。indices是int32、values是float16，window_ids为同等行数int32；没有raw h字段。未读取confirmation/evaluation实例或封存TEST。

## 已核路径与资产

- 原图及四激活类：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/`；资产`analysis_crosscoder_feature_relation_phase1_20261013t173130z`。
- raw h候选：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z/`；资产`representation_crosscoder_relation_learning_20261015t164000z`、`representation_crosscoder_relation_learning_eval512_20261015t164000z`。本审计读取其既有`data_eval512/cache_manifest.json`；完整h身份/访问由父任务缓存审计另核。原文档与近重复独立性Unknown，不能称新盲语义验证。
- E18稀疏缓存：`/data/250010109/MoE_Router/experiments/20260904_a15_13_e18_dataset_conditioned_sae_semantics/runs/full-20260904T042013Z/activation_cache/`；资产`representation_qwen3_0p6b_e18_semantics_042013`。
- 标签数据来源：`data_qwen3_0p6b_e18_e14_eight_task_proxy`与`data_qwen3_0p6b_e18_m2d2_seq256`，具体地址和已查字段存JSON。本审计没有解包实例标签来拟合或选样。

## 当前访问证据

2026-10-27 06:38:54 UTC（北京时间14:38:54），对原phase1、E18缓存和上述两个标签数据资产运行`tools/check_assets.py --strict`，四项均ACCESSIBLE，退出码0。**访问stdout内嵌于`semantic_audit.json`的`strict_access_evidence`，没有另造一个不存在的收据文件。** 这只证明所列地址可访问，不证明raw h、标签和留出已经配对合格。

## 若要完成，还缺哪些新增计算

需要先核定独立标签数据及发现/留出，再用固定Base在精确residual-post hook生成与标签配对的raw h。这会新增模型前向，当前1500/1500已用满，不能自动执行。随后才能在发现集固定中心化PCA基和简单分类器，在留出集比较等维头/中/尾谱段及随机子空间，并单列方差。数据范围及新增前向条数尚未授权，本审计不虚构条数，等待父任务核对并取得预算确认。

本审计没有给出语义可分性结果，也没有声称所有历史项目均无语义缓存；结论仅限上述有界搜索和本轮匹配要求。原R01/R02/R03结果不改。
