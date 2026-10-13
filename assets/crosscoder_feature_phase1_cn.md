# CrossCoder特征关系：阶段一实存资产

[English](crosscoder_feature_phase1.md)。保存日期：2026-10-14，北京时间。

- 完整稀疏激活：`representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z`；入口 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/feature_cache/manifest.json`。完整10,485,760位置、16384特征、2,669,034,642非零值；平均激活数254.538978767395。16384个边缘命中次数与原有最终验证逐项完全一致。
- 分析交付：`analysis_crosscoder_feature_relation_phase1_20261013t173130z`；入口 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z`。发现原始边214,711、复核通过206,136、复核约简边146,947、固定候选4对；完整机器图、文本、解码贡献、Top10敏感性和逐块证据已保存。
- 固定父对象：最终14选定层／16384特征CrossCoder；不是0.5B状态或28层／32768任务。完整TRAIN阈值、归一化及原始推理绑定见input_identity.json、cache_binding.json。
- 生产任务pt-zwh6g95p；首次接口错误任务pt-io5c5h2p已退出并保留，合并计入220分钟主动计算上限。
- [本次输出访问检查](checks/2026-10-14_crosscoder_feature_phase1_outputs_20261013T173130Z.json)仅覆盖所列新资产，不代表全库重新核验。

边界：同bin复核；原文档和近重复独立性未知。高J共同组成项中87.5%为Top10节点；逐个删除不能排除共同背景支配。登记不证明因果、主题相似或专家学习收益，不启动MoE或CrossCoder训练。both=0或稀少按实交付。
