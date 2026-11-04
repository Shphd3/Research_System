# 数据与复算 / Reproduction

全部384条文本、标签、家族、模板、划分、token及位置：data/panel.jsonl。全部四候选逐token分数：data/behavior_all.jsonl。两套SAE所有384×30000激活坐标（零值隐式完整保存）：data/*_all_z_csr.npz。非零逐值表active_values.csv；全部支持交并／事件overlaps.csv；冻结候选selection.json；每候选z/pre/u/q/cutoff在candidate_values.csv。两域选中成员对所有384样本的完整预激活在data/*_selected_pre.npz。未选中feature的完整预激活和h留在下列大缓存，不谎称包内含全部pre。

主统计的离线复算只需Python/numpy/scipy：

```bash
python code/reproduce_portable.py .
```

原生重新推理需要外部冻结模型和SAE，路径/sha/native loader见frozen_plan.json，依赖目录/data/250010109/dependency_packages/hf_transformers_qwen3。原脚本为prepare.py、run.py discovery、select.py、run.py remaining、analyze.py、figures.py、report.py、verify.py；脚本拒绝覆盖既有结果。要完全重跑，复制源码到新执行目录，并先保留原协议及显式改动记录，不在原完成目录重跑。

实际大缓存：/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/cache/discovery.npz 和 remaining.npz。每个包含行IDs、h、完整30000维z/pre、Top32索引/门槛、重构相对误差及decoder范数；确切大小和SHA由large_files_index.json登记。完整模型／字典权重不在包内。脚本和配置版本、哈希、软件／时间／CPU记录在evidence/*_complete.json及output_manifest.json。

当前报告是本轮观察和AI有限判定，科学接受Unknown；本地阅读副本不代表GitHub发布。没有commit/push/外部发送。
