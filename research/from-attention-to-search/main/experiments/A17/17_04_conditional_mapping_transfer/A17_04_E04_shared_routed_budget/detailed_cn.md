# Detailed: A17_04_E04 有界资格测试

Primary Anchor: [A17_04_02](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_02_shared_routed_budget_anchor_cn.md).
Frozen Protocol: [registered copy](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/registered_protocol.md), SHA256 `ecdc6ef8fc04c7332198569ac58204f178bf2da86858594f7546ba696da9810b`.
Summary: [summary_cn.md](summary_cn.md).
Eligibility: 工程合格；单种子获取结果有界；正式收益NOT_RUN。

## 0. 快速认识

目的：核验实现及两映射学习资格。工程PASS，五组学习资格均NOT_PASSED，不推断分开收益。下一项决定：选择哪项有界资格修复。

## 1. 对象定义

| Object | Meaning / computation | Boundary |
|---|---|---|
| Shared base | Exact Base plus E03 acquired-old q/k/v/o; all frozen | Same in all arms |
| Shared increment | Factors active in both modes | Sharing permissions, not identified common semantics |
| Private increment | Factors active for one visible input mode | Known-mode allocation, not learned routing |
| Rule margin | log p(correct) − log p(opposite endpoint), nat | Mean can hide weak conditions |
| Qmin | Minimum accuracy of8 cells, each200 DEV answers | Qualification threshold95% |
| Candidate choice CE | −log[p(correct)/candidate mass] | Separates access from selection |

## 2. Anchor与决定

本前置检查避免把没学会解释成结构收益。父共享／分开问题的科学接受仍Unknown。

## 3. 契约核验及偏离

| Contract | Actual | Status / scope |
|---|---|---|
| Three main plus2 rank controls |5 arms, seed29 |PASS for pilot;3-seed formal NOT_RUN |
| Main parameter counts |163,840 each |PASS |
| Active counts S/U/H |163,840/81,920/122,880 |PASS; deliberately unequal |
| Data exposure |Each pilot1200×20, old/new12,000 each |PASS |
| Compute |Main relative spread2.7229207703621487e-7 |PASS matrix FLOPs; no wall-time equality claim |
| Original freeze |Same original-parameter digest before/after every case |PASS, source byte hash and per-step versions |
| Resume |5 independent Smoke step1→2 replays |PASS; pilot240 continuation restores actual state, no uninterrupted241 reference |
| Backend |FP32 eager; parent used SDPA |Clarified before freeze, common new-arm setting |
| Pilot stopping |All fail240; all continue1200 |Matches bounded authorization |
| Mixed GPU check |5 synthetic nonzero-bank cases, zero optimizer steps |Supplemental engineering check, recorded separately; max difference5.43594e-5≤1e-4 |
| Formal utility/local interventions |Not submitted/not run |NOT_RUN, not silently replaced by pilot |

没有调秩／学习率、重提、替换种子、排除异常值或评估TEST。补充只读检查通过ACP exec在同一reserved节点运行，没有改变训练或保存状态。

## 4. 实际设置

冻结已学会旧规则的Qwen3-0.6B，最后一层增量库，其他原参数全部冻结。
Joint view:4800 TRAIN/1600 exposed DEV; mode partitions2400/800 each. Source labels: mode1甲FIRST乙LAST, mode2甲LAST乙FIRST. Both mode prefixes visible, target not supplied. Sampler: five lists × two commands × two modes; microbatch5, accumulation4, DP1; CE sum/20.
AdamW1e-4, betas(.9,.999), eps1e-8, decay0, global clip1, constant schedule, zero-B initialization/gain1. Same paired seed/order; rank masks S16all, U8old0–7/new8–15, H8shared0–7/old8–11/new12–15, controls real rank8/12 padded to16.
Milestones0/1/16/50/120/240/600/1200. Smoke8/arm. Pilot1200/arm. Source/config/view identities in [freeze.json](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/freeze.json), with exact old1200 member. Runtime: four H10080GB, PyTorch2.3.0a0+6ddf5cf85e.nv24.04/CUDA12.4, independent GPU lanes, TF32off, dropoutoff.

独立重算：每条pilot处理489,600个非padding前缀词元、500,410个包含padding的计算位置，另有规范计数的24,000个答案目标。五组的这些数目及完整record顺序相同。前缀／padding用于计算量解释，不加入答案监督的规范曝光轴。

## 5. 指标与规则

测全词表准确率、答案CE、正确／相反答案优势、候选概率和候选内选择CE。学习资格为八项最低≥95%；正式收益还要求三种子及独立的提升／保持条件，本轮NOT_EVALUATED。

## 6. 证据链

| Question | Criterion | Raw / independent evidence | Observation | Eligibility |
|---|---|---|---|---|
| Engineering |Budget/mask/freeze/exposure/replay |[Smoke verdict](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/smoke_verdict.json); per-case scope/guards/TB verification |5 PASS |ELIGIBLE engineering |
| Both rules learned |All8 cells≥95% |[Raw-record audit](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/independent_results.json) from40 pilot evaluations |Qmin45.5%–78.5% at1200 |BOUNDED acquisition |
| Identical exposure/order |20 targets/update,10 each |Independent metrics+record lookup |5 same1200-window orders and prefix/padding totals |ELIGIBLE matching |
| Actual saves |Saved weights/optimizer/counters |[Tensor audit](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/independent_tensor_audit.json) after registration |55 states PASS |ELIGIBLE saves, not learning |
| Allocation utility |Qualified3-seed comparisons |No formal run |NOT_RUN |Cannot adjudicate |

## 7. 完整读数

### 240 updates /4800 targets

| 设置 | 旧准确率 | 新准确率 | 旧CE | 新CE | 旧规则优势 | 新规则优势 | 最弱分项 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 完全共享16槽 | 89.625% | 45.375% | 0.339318 | 1.788583 | 2.524 | -0.637 | 1.00% |
| 分开8／8槽 | 100.000% | 50.000% | 0.000702 | 1.765268 | 17.768 | -0.042 | 1.50% |
| 共享8＋专属4／4槽 | 100.000% | 49.875% | 0.007010 | 1.620648 | 8.467 | -0.044 | 1.50% |
| 全共享8槽对照 | 90.375% | 42.500% | 0.355196 | 2.374215 | 2.982 | -1.172 | 0.00% |
| 全共享12槽对照 | 88.250% | 45.250% | 0.374472 | 1.958276 | 2.480 | -0.769 | 1.00% |


### 1200 updates /24000 targets

| 设置 | 旧准确率 | 新准确率 | 旧CE | 新CE | 旧规则优势 | 新规则优势 | 最弱分项 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 完全共享16槽 | 99.750% | 87.500% | 0.011851 | 0.332006 | 11.581 | 5.929 | 75.00% |
| 分开8／8槽 | 100.000% | 84.375% | 0.000054 | 0.411580 | 21.647 | 2.918 | 71.50% |
| 共享8＋专属4／4槽 | 100.000% | 89.750% | 0.000852 | 0.275144 | 15.131 | 5.006 | 78.50% |
| 全共享8槽对照 | 99.125% | 72.750% | 0.033712 | 0.649917 | 9.342 | 3.236 | 45.50% |
| 全共享12槽对照 | 99.500% | 84.375% | 0.017920 | 0.416978 | 11.091 | 4.732 | 69.00% |


### 1200步两类未见分别汇报

| Arm | Mode | Panel | Accuracy | CE | Rule margin | Candidate mass | Candidate choice CE |
|---|---|---|---:|---:|---:|---:|---:|
| 完全共享16槽 | old | order_new | 99.500% | 0.013964 | 11.703 | 99.977% | 0.013739 |
| 完全共享16槽 | old | combination_new | 100.000% | 0.009738 | 11.458 | 99.976% | 0.009492 |
| 完全共享16槽 | reversed | order_new | 86.500% | 0.319916 | 6.082 | 98.674% | 0.305415 |
| 完全共享16槽 | reversed | combination_new | 88.500% | 0.344096 | 5.775 | 99.248% | 0.336273 |
| 分开8／8槽 | old | order_new | 100.000% | 0.000095 | 21.920 | 100.000% | 0.000095 |
| 分开8／8槽 | old | combination_new | 100.000% | 0.000013 | 21.374 | 100.000% | 0.000012 |
| 分开8／8槽 | reversed | order_new | 85.250% | 0.369947 | 2.979 | 97.219% | 0.339399 |
| 分开8／8槽 | reversed | combination_new | 83.500% | 0.453213 | 2.857 | 97.446% | 0.426046 |
| 共享8＋专属4／4槽 | old | order_new | 100.000% | 0.001088 | 15.371 | 99.998% | 0.001067 |
| 共享8＋专属4／4槽 | old | combination_new | 100.000% | 0.000616 | 14.891 | 99.990% | 0.000516 |
| 共享8＋专属4／4槽 | reversed | order_new | 92.250% | 0.225965 | 5.156 | 98.445% | 0.208485 |
| 共享8＋专属4／4槽 | reversed | combination_new | 87.250% | 0.324322 | 4.855 | 98.817% | 0.311723 |
| 全共享8槽对照 | old | order_new | 98.500% | 0.040934 | 9.231 | 99.923% | 0.040156 |
| 全共享8槽对照 | old | combination_new | 99.750% | 0.026490 | 9.454 | 99.883% | 0.025278 |
| 全共享8槽对照 | reversed | order_new | 70.500% | 0.674809 | 3.323 | 94.483% | 0.612300 |
| 全共享8槽对照 | reversed | combination_new | 75.000% | 0.625024 | 3.150 | 95.116% | 0.571464 |
| 全共享12槽对照 | old | order_new | 99.250% | 0.022083 | 11.155 | 99.943% | 0.021512 |
| 全共享12槽对照 | old | combination_new | 99.750% | 0.013757 | 11.027 | 99.953% | 0.013281 |
| 全共享12槽对照 | reversed | order_new | 83.250% | 0.409357 | 4.873 | 98.191% | 0.389933 |
| 全共享12槽对照 | reversed | combination_new | 85.500% | 0.424600 | 4.591 | 98.654% | 0.410415 |

### Eight qualification cells at1200

| Arm | Cell | Accuracy |
|---|---|---:|
| S16 | old/甲/order_new | 99.50% |
| S16 | old/甲/combination_new | 100.00% |
| S16 | old/乙/order_new | 99.50% |
| S16 | old/乙/combination_new | 100.00% |
| S16 | reversed/甲/order_new | 98.00% |
| S16 | reversed/甲/combination_new | 98.50% |
| S16 | reversed/乙/order_new | 75.00% |
| S16 | reversed/乙/combination_new | 78.50% |
| U8 | old/甲/order_new | 100.00% |
| U8 | old/甲/combination_new | 100.00% |
| U8 | old/乙/order_new | 100.00% |
| U8 | old/乙/combination_new | 100.00% |
| U8 | reversed/甲/order_new | 94.00% |
| U8 | reversed/甲/combination_new | 95.50% |
| U8 | reversed/乙/order_new | 76.50% |
| U8 | reversed/乙/combination_new | 71.50% |
| H8 | old/甲/order_new | 100.00% |
| H8 | old/甲/combination_new | 100.00% |
| H8 | old/乙/order_new | 100.00% |
| H8 | old/乙/combination_new | 100.00% |
| H8 | reversed/甲/order_new | 96.50% |
| H8 | reversed/甲/combination_new | 96.00% |
| H8 | reversed/乙/order_new | 88.00% |
| H8 | reversed/乙/combination_new | 78.50% |
| S8 | old/甲/order_new | 97.50% |
| S8 | old/甲/combination_new | 100.00% |
| S8 | old/乙/order_new | 99.50% |
| S8 | old/乙/combination_new | 99.50% |
| S8 | reversed/甲/order_new | 95.50% |
| S8 | reversed/甲/combination_new | 97.00% |
| S8 | reversed/乙/order_new | 45.50% |
| S8 | reversed/乙/combination_new | 53.00% |
| S12 | old/甲/order_new | 99.50% |
| S12 | old/甲/combination_new | 100.00% |
| S12 | old/乙/order_new | 99.00% |
| S12 | old/乙/combination_new | 99.50% |
| S12 | reversed/甲/order_new | 97.50% |
| S12 | reversed/甲/combination_new | 98.50% |
| S12 | reversed/乙/order_new | 69.00% |
| S12 | reversed/乙/combination_new | 72.50% |

每个分项200答案；每种模式每面板400，合并为两面板等权。全部为未平滑的单种子原始观察。

## 9. 阶段失败定位

工程通过，操作层面的学习资格失败。未发现模型加载、明显掩码／冻结错误或曝光不等。秩容量、因子化优化／更新尺度、泛化问题仍未区分。当前训练loss只是各批次读数，没有额外完整已见TRAIN准确率评估，不能确认只是记忆或只是泛化失败。

## 10. 本轮记录

1. Question: five-arm implementation and two-rule qualification.
2. Setup: same frozen old state, masks/rank allocation only, fixed optimizer.
3. TRAIN: joint view and exact equivalent mode partitions.
4. DEV: unseen order/combination exposed panels; no TEST truth.
5. Result: engineering PASS, acquisition NOT_PASSED; registered actual assets.
6. Boundary/next: no formal utility verdict; choose one bounded qualification repair.

## 11. 解释

专属路由保护参数访问，但保护本身不会自动解决新规则学习。混合组的新平均准确率本次最高，但仍未合格。受限因子结构是一个新学习配置，父实验完整矩阵联合成功不能替它通过资格。

## 12. 结论边界

可报告实现、预算、匹配监督、旧规则基本保持、新规则部分学习及95%门槛失败。不能宣称分开收益、语义共同／独特expert、学习路由成功、低秩不可能或自然任务泛化。

## 13. 下一项决定

研究者下一项决定：采用哪项有界资格修复。AI建议保留数据／实现，分别检查更新尺度和秩。正式仍暂缓，没有提交修复训练。

## 14. 资产与产物清单

[Machine-readable artifact manifest](artifact_manifest.json) binds sources, freeze, raw records, independent audits and actual registration. Two data-view IDs;10 output families containing55 real checkpoint members. [Strict actual output access](../../../../../../../assets/checks/2026-10-12_a17_e04_actual_checkpoints.json).
Saved states: `<run>/smoke/seed_29/<arm>/checkpoints/` and `<run>/pilot/seed_29/<arm>/checkpoints/`. Smoke saves0/1/8 (15 states); pilot saves0/1/16/50/120/240/600/1200 (40 states). External reference step2 files are replay artifacts, not extra checkpoint members. Five source-profile backward computations and one rolled-back isolation step are engineering overhead, excluded from pilot update exposure and separately bounded.

## 15. 执行入口与来源

Job `pt-1rb3s2t0`, completed successfully2026-10-12T05:53:32Z. [Certificate](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/execution_certificate.md).
Runner: `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/source/orchestrate.py`.
Worker: `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/source/run_bank.py`; bank: `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/source/bank.py`.
Config: [/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/config.json](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/config.json).
Registered body: [/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/registered_protocol.md](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/registered_protocol.md).
Dataset: [/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/data/mapping_view_v1/manifest.json](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/data/mapping_view_v1/manifest.json).
Raw evals: `<run>/pilot/seed_29/<arm>/eval_<step>.json`; metrics: `metrics.jsonl`.
Independent record/profile verification: [independent_results.json](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/independent_results.json).
Additional mixed checks: [additional_mixed_gpu_checks.json](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/additional_mixed_gpu_checks.json), producer `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/source/additional_mixed_checks.py`, independent of training source freeze.
Reproduce only under new authorization: source runtime then `python source/orchestrate.py --config <frozen_config> --run <NEW_ROOT>`; do not overwrite this completed run or treat this text as run approval.
