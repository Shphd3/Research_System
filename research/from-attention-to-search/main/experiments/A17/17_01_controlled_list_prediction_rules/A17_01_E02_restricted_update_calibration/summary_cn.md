# Summary: A17_01_E02 Restricted Update Smoke

[English](summary.md) · [Protocol](protocol_cn.md) · [Detailed](detailed_cn.md)

工程状态: `PASS`；scientific verdict `NOT_EVALUATED`；human adoption/mechanism `Unknown`。

## 1. 目的

核验同一末层投影直接更新与共享rank8 LoRA的工程链，为研究者选择可测学习状态提供事实。

## 2. 假设

受限参数能够适配首项/末项并输出有限变化；竞争是位置/容量不足或仍迅速饱和。本Smoke不裁决稳定共享或干扰。

## 3. 分析方法

- 同位置L/R8各两档LR，原始Base、数据、每步20答案、50步上限保持一致；其他参数冻结。
- 完整800条dev测能力/CE；固定80条工程子面板测5批均衡来源×3SGD步长×BF16/FP32，各未见分别与合并汇报。
- 核验原生全词表logits/CE、冻结字节、计数/TensorBoard、保存及8步外进程恢复/连续第9步。

## 4. 结论

修复后作业pt-i3ianttt工程PASS；独立64/64门槛通过。

首个job pt-bw3s1pxw在update0探针基线恢复守卫失败，正式训练0步；实际初始状态已保存/登记。确定的工程错误已修复，8项CPU测试PASS。失败产物保留，不能解释为学习器或科学假设失败。

| 条件 | 更新数 | 顺序未见 | 组合未见 | 合并 | 合并CE | 原始记录 |
|---|---:|---:|---:|---:|---:|---|
| l_lr-5 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-5/capability/update_00000.json) |
| l_lr-5 | 50 | 78.00% | 77.25% | 77.62% | 0.89746392 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-5/capability/update_00050.json) |
| l_lr-4 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-4/capability/update_00000.json) |
| l_lr-4 | 50 | 80.25% | 82.50% | 81.38% | 0.64701936 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-4/capability/update_00050.json) |
| r8_lr-5 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-5/capability/update_00000.json) |
| r8_lr-5 | 50 | 73.50% | 73.00% | 73.25% | 1.02801167 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-5/capability/update_00050.json) |
| r8_lr-4 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-4/capability/update_00000.json) |
| r8_lr-4 | 50 | 73.75% | 76.00% | 74.88% | 0.96421549 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-4/capability/update_00050.json) |


准确率是固定格式全词表下一答案的开发集观测，未见仅相对本轮训练；test未打开。LoRA与直接矩阵不等价，同LR不等于同功能步幅。双精度探针全部保留，但各精度分别重新计算来源梯度，比较同时包含更新方向和读出管线差异，不能称为同一扰动的纯reader精度误差；科学近零阈值、来源有效性、学习器采纳仍Unknown，原始负号不自动获得资格。

[原始来源窗口读出](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/raw_source_window_readout.json) · [重试产物](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z)。

可以确认已执行的工程范围及观测；不能声称LoRA更优、只改格式、稳定干扰、功能分解、专家必要性或频率效应。后续学习器/窗口选择由研究者评判，本轮未执行频率/SAE/Full。
