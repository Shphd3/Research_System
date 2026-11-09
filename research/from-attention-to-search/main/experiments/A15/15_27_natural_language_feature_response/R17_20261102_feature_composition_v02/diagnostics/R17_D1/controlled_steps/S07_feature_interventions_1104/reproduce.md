# S07 数据、运行和离线复算

- data/panel.jsonl：96条原始主留出文本／token，不另造更容易的prompt。
- data/selection.json：发现固定ID、典型强弱、计数／幅度范围及匹配细节。完整发现逐值仍在主包main/data的全稀疏z。
- results/conditions.jsonl：14976条件全部旧新坐标、实际有效数、构造范数、4完整候选分数、4全词表rank／概率、p4、熵/KL／top20质量。
- results/top20.jsonl：每条件实际top20词语字符串、ID、排名和概率；完整4候选分布都在conditions。没有保存／冒称包含完整151936项概率向量。
- results/actual_injection_norms.csv：实际FP32注入范数与构造范数舍入核对。
- data/key_injected_deltas.npz：固定F09部分实际1024维注入向量；所有条件向量较大，留在执行侧cache/all_injected_deltas.npz，路径及大小见large_files_index.json。
- cache/baseline_tail.npz：96条原末层input／attention／MLPinput／finalhidden／period项，体量小，可用于完整可信资产下重算末层。无模型／SAE权重。

离线小包复算：

```bash
python code/reproduce_portable.py .
```

合并包则在interventions目录运行，或传入该目录。主包仍可单独复算，原包hash保持。要重新执行全部推理需要冻结模型和两字典，其路径/sha/native loaders与依赖目录见frozen_plan.json；run.py拒绝覆盖已完成记录。CPU2threads；没有训练／GPU／云job。原始源脚本、协议freeze、校准、候选、数据和所有汇总均包含。S06文件和输入权重逐项hash通过，无永久写checkpoint。

完整执行目录：/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S07_feature_interventions_1104。主执行目录：/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104。所有大文件精确bytes/SHA在large_files_index.json；未包含文件绝不称已进包。研究者科学接受/关闭Unknown；无commit/push/外部发布。
