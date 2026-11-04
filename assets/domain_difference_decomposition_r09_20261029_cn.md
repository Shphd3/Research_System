# R09 领域均值差分解：实际产物

[English](domain_difference_decomposition_r09_20261029.md) · [正式结果概述](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/summary_cn.md) · [登记索引](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/asset_registration.json) · [当前严格访问检查](checks/20261029T152118Z_r09_actual_outputs.json)

本轮在完成后登记六类实际产物。2026-10-29 15:21 UTC 的严格访问检查全部通过。检查确认登记文件和探针可访问；科学解释仍属探索性，研究者接受状态为 Unknown。本轮没有训练模型或 CrossCoder 检查点。

| 资产 ID | 实际保存对象与产生脚本 |
| --- | --- |
| `analysis_a15_27_03_r09_domain_difference_decomposition_20261029` | 原 384 条输入上的全部 16,384 名成员；9 个条件、147,456 行成员统计；真实差异、重建与残差向量，还原后的 decoder、冻结候选、符号贡献、Top-k 和谱表。脚本：`main/analyze.py`。 |
| `analysis_a15_27_03_r09_frequency_family_20261029` | 独立 DCLM 65,536 个位置的发生率、三种冻结分组、98,304 行逐成员方差、家族重采样索引与候选关联表。脚本：`frequency_family/analyze.py`。 |
| `data_a15_27_03_r09_controlled_distance_20261029` | 3,840 条派生文本：384 条原输入 × 5 个距离 × 2 种星期词。每条 240 token，目标位置为 239。脚本：`distance/prepare.py`。 |
| `representation_a15_27_03_r09_distance_native_jointz_20261029` | 十份真实 14 层残差向量和原生 A22 共享激活分片，另有归一化、精确重放记录。共 3,840 次分析前向与 2 次原生重放。脚本：`distance/acquire.py`。 |
| `analysis_a15_27_03_r09_distance_response_20261029` | 全成员带符号响应、日期编辑对照、家族区间、冻结远距比较与分母和支持限制。脚本：`distance/analyze.py`。 |
| `analysis_a15_27_03_r09_supplement_abcd_20261029` | A：全部 141 名固定候选及原始激活差。B：原全成员频率贡献。C：单位 decoder 几何及字典、匹配背景。D：含残差的频率 × 谱段可加贡献。没有新增前向或模型拟合。 |

完整载荷保留在[执行目录](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029)。[总清单](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/artifact_manifest.json)记录 67 份主分析或补充文件，并链接各分支清单。catalog 的摘要字段区分既有清单提供的哈希与本次新计算的本地哈希。[精选阅读载荷](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/payload_manifest.json)只是派生交付选择，不是另一套执行缓存。

输入保持冻结的 Qwen3-0.6B Base、A22 检查点、R08 原 384 行联合缓存、R04 的 DCLM 发生率参照，以及 R07 使用的独立自然文本基底。真实目标向量是零起算 block 27 的 residual-post，位于最终归一化前。A22 联合编码十四个奇数层，得到一份 16,384 维共享激活；它不提供各层独立的激活。decoder 还原使用训练时冻结的 RMS，block 27 为 374.3495121024576。精确父资产 ID、哈希、层列表、门控和加载脚本均在 catalog 中。

主分解通过 1,166 项独立数值检查；距离数据与统计通过 16,239 项；C/D 复算通过 2,141 项；背景比较通过 26 项。C 的每行和为 1。D 的行和等于 B 的有符号组贡献，列和等于真实差异的分段谱能量，含残差的全部格子和为 1；残差存在于各谱段。这些恒等关系验证计算，不证明语义专有性或因果重要性。

原留出家族已在 R07/R08 暴露。距离操作也改变填充次序与框架；整个领域核心的编辑幅度与单 token 的星期词对照不同。原发现集 RMS 为零的成员，其归一化距离量保持 NA。频率发生、激活使用复现、重建贡献、decoder 朝向和距离响应分别保留。完整定义、真实文本与边界见 [Detailed](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/detailed_cn.md)和[独立 A–D 补充](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/supplement_ABCD_cn.md)。
