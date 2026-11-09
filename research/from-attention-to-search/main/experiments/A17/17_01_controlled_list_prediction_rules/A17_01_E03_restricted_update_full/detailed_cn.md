# Detailed: A17_01_E03 Restricted Projection Full

[Summary](summary_cn.md) · [Protocol](protocol_cn.md)

## 0. 快速回顾

- Smoke: `pt-fleom0t0`, platform `SUCCEEDED`, engineering `PASS`, 64/64 gates; [run](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106).
- Full: `pt-ujjb8f7a`, platform `SUCCEEDED`, engineering `PASS`, 96/96 gates; [run](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z).

## 1. 问题、假设与边界

以下为实际阶段状态和逐轨迹事实，研究者机制判断Unknown。三个独立训练seed只作描述；来源批不是重复实验，局部帮助/损害不等于长期效益。

## 2. 设置与对照

Original Qwen Base; layer27 o_proj1024×2048. L2097152 trainables; R824576,alpha8/scale1,zero-output initialization. Others frozen. AdamW1e-4,betas(.9,.95),eps1e-8,decay0,clip1,constantLR; micro5×accum4,20valid answers/update. Three seeds per variant,100updates,12000totalFull answers. Same LR is not matched functional displacement. Smoke four arms17/19,10updates,no test. Four reserved H100 GPUs,default shphd-lite-0911 image,one node,independent workers,max4 concurrently.

## 3. 数据与确认边界

Registered model_qwen3_0p6b_base and data_a17_list_rules_v1; exact release train4000/dev800/test800. Train/dev hashes checked before use; source IDs frozen before model outputs. Sources train-only; recipient full dev800. Test first-model-opened at final100 under frozen rule,not for choice. Source batches may overlap; content groups and two novelty panels retained. Dev-only Smoke does not confirm mechanism.

## 4. 实现、观测与保存

Reuse E02 wrapper/LoRA/freeze/save/resume; adapt fixed perturbation and constant LR,retain old source/results. CPU8 tests PASS. Seven required TB tags and independent counters; no auxiliary training objective. Checkpoint states include trainables/AdamW/scheduler/RNG/cursor/counts; original Base separate. Digests verified; final restore NOT_CHECKED unless own receipt states otherwise. Update8 external restore and continuous next9 receive separate evidence. Every effective matrix perturbation saved with hash,source,eta/full-half. Family registration requests enumerate actual members,never planned saves; root owns shared registry writes.

## 5. 阶段结果与原始证据

| Phase | Arm | Step | Panel/reader | Order-new | Combination-new | Combined | CE | Raw |
|---|---|---:|---|---:|---:|---:|---:|---|
| Smoke | l_s17 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/l_s17/capability/update_00000.json) |
| Smoke | l_s17 | 10 | dev | 80.25% | 82.25% | 81.25% | 0.82358977 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/l_s17/capability/update_00010.json) |
| Smoke | r8_s17 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/r8_s17/capability/update_00000.json) |
| Smoke | r8_s17 | 10 | dev | 73.75% | 73.50% | 73.62% | 1.02663286 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/r8_s17/capability/update_00010.json) |
| Smoke | l_s19 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/l_s19/capability/update_00000.json) |
| Smoke | l_s19 | 10 | dev | 76.75% | 79.50% | 78.12% | 0.82121537 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/l_s19/capability/update_00010.json) |
| Smoke | r8_s19 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/r8_s19/capability/update_00000.json) |
| Smoke | r8_s19 | 10 | dev | 73.50% | 73.50% | 73.50% | 1.02643462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/r8_s19/capability/update_00010.json) |
| Full | l_s29 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s29/capability/update_00000.json) |
| Full | l_s29 | 100 | dev | 89.00% | 84.25% | 86.62% | 0.55138834 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s29/capability/update_00100.json) |
| Full | l_s29 | 100 | test_fp32 | 91.00% | 86.25% | 88.62% | 0.52499711 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s29/confirmation_test_endpoint.json) |
| Full | r8_s29 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s29/capability/update_00000.json) |
| Full | r8_s29 | 100 | dev | 76.50% | 77.00% | 76.75% | 0.84565399 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s29/capability/update_00100.json) |
| Full | r8_s29 | 100 | test_fp32 | 80.75% | 76.75% | 78.75% | 0.83281099 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s29/confirmation_test_endpoint.json) |
| Full | l_s43 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s43/capability/update_00000.json) |
| Full | l_s43 | 100 | dev | 86.75% | 87.25% | 87.00% | 0.54475833 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s43/capability/update_00100.json) |
| Full | l_s43 | 100 | test_fp32 | 90.25% | 92.50% | 91.38% | 0.51536036 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s43/confirmation_test_endpoint.json) |
| Full | r8_s43 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s43/capability/update_00000.json) |
| Full | r8_s43 | 100 | dev | 76.25% | 76.50% | 76.38% | 0.84303762 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s43/capability/update_00100.json) |
| Full | r8_s43 | 100 | test_fp32 | 82.25% | 76.50% | 79.38% | 0.82925014 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s43/confirmation_test_endpoint.json) |
| Full | l_s71 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s71/capability/update_00000.json) |
| Full | l_s71 | 100 | dev | 86.00% | 84.75% | 85.38% | 0.56136077 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s71/capability/update_00100.json) |
| Full | l_s71 | 100 | test_fp32 | 90.50% | 88.00% | 89.25% | 0.52728926 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s71/confirmation_test_endpoint.json) |
| Full | r8_s71 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s71/capability/update_00000.json) |
| Full | r8_s71 | 100 | dev | 78.50% | 77.50% | 78.00% | 0.83906893 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s71/capability/update_00100.json) |
| Full | r8_s71 | 100 | test_fp32 | 83.50% | 78.50% | 81.00% | 0.82661910 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s71/confirmation_test_endpoint.json) |


完整Full效应数据: [descriptive_effect_cells.json](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/descriptive_effect_cells.json)

## 6. 偏差、失败与资格

截至本记录，按现有产物保留工程状态；失败不静默删除。precision floor为工程分辨护栏，非科学收益阈值。有效来源、接收符号与双reader一致性分别报告；来源不有效或精度矛盾为不足。R8半因子步不等于半矩阵位移。任何后续修复必须附加Protocol记录并保存旧源/hash/失败产物。

## 7. 洞见、边界与下一决定

Researcher scientific interpretation Unknown. Native exact update identity and finite loss are measured before SAE. Three seeds provide descriptive repetition,not population inference. Later SAE must qualify rawhook,parent,displacement/loss-weighted reconstruction residual and finite controls; failed proxy does not overturn native evidence. Frequency is independently owned and follows root GPU-slot handoff. No architecture-utility conclusion.

## 8. 完整来源路径

- [Execution source](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/source/runner.py), [Full config](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/configs/full.json), [Smoke config](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/configs/smoke.json).
- [Managed supervisor](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/supervise.py); monitor owner /root/stage1_full;60second polling,state-change logs only.
- [Supervision ledger](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/supervision.jsonl); each run frozen_sources.json/config_frozen.json/protocol_frozen.md, submission receipts,latest_platform.json, durable pod+arm logs,terminal_verification.json and actual registration_request.json.

## 9. Final factual synthesis / 最终事实归纳


直接矩阵的主要原生观测是跨规则帮助：在state0/16、eta0.01全步，两个方向、三个seed、各五批来源均通过来源/数值护栏并降低接收损失。训练后作用变小；当前结果没有稳定的净干扰证据。全量4320格中的3个LOCAL_HARM读出都来自同一个L43/state100/LAST来源batch0的全/半步与不同面板，不是三次独立发现。研究者机制判断仍Unknown。

Platform `SUCCEEDED`,terminal96/96PASS,six arms12000answers,42actual saved members. [Platform receipt](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/platform_terminal.json),[terminal audit](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/terminal_verification.json),[registered outputs](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/registered_outputs.json),[source means](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/native_cross_rule_seed_summary.json). The same L43/state100/LASTbatch0 has combined FIRST delta+0.000471232 ateta.01full,combination panel+0.000792480full and+0.000378446half; own-rule delta−0.000620750full/−0.000329380half. These overlapping readouts are one source/state case,not independent replications. All registered means remain negative but some individual sources/readers are insufficient. Gradient tensors and direct gradient-inner-product arrays were NOT_SAVED; gradient norms/effective matrices are actual saved evidence. Additional native/SAE replays may compute them under a separate declared stage; do not relabel ΔW/eta as exact original G.

## 10. 真实曝光面板资格（附加后处理）

Root authorized this audit after all learning choices were frozen. Original nominal split labels,full800primary,training,test access and native effects remain untouched. For eachstate0/16/100,only completed trajectory presentation records define seen unordered groups; virtual source probes never count. Dev/test orders have no training-order overlap. Group/record counts,per-rule cells and all source/readers are reaggregated in [actual_exposure_panel_qualification.json](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/actual_exposure_panel_qualification.json):24capability records and1440probe-reader records. L/R8 use exactly identical100-step presentation IDs per seed. Finaldev nominal-order seen records are394/386/392 of400,and finaltest392/390/388 of400 for29/43/71. Nominalcombination false-seen=0. This is a qualification sensitivity,not a newly preregistered primary result or a retraining trigger. State0 has no task exposure,so all actual groups are unseen then.

## 11. 静态图与完整地图

[Figure](figures/cross_rule_effects.png),[PDF](figures/cross_rule_effects.pdf),[complete72-pointCSV](figures/cross_rule_effects.csv),[origins](figures/SOURCES.md),[small curated payload manifest](figures/payload_manifest.json). Figure uses all registereddirectseed/state/eta/fullhalf combinations,five-source means,zero line,qualified markers,noCI/no bestscale. Complete4320source×rule×novelty×state/scale cells stay in [native map](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/descriptive_effect_cells.json); they are dependent cells. Failed source/numeric eligibility remains visible and cannot be rescued by average signs.


## 已授权SAE执行及最终验收完成：北京时间2026-10-10

**目的与假设。** 补齐既有分析范围，核验最后S7失败是否来自均值求和实现不一致，而非原生测量缺失。此处只做工程资格，不引入新科学假设、feature选择或因果解释。

**设置与对照。** 原GPU64条件的矩阵、梯度、SAE编码、原生端点及所有失败job保留。端点/梯度2e-5、差值4e-5门槛不变。A06记录看到结果后的数值修复：独立CPU恢复从已保存逐位置数组统一以NumPy float64求均值，最终验收要求精确相等，不增加容差。四项回归测试覆盖抵消、错误汇总、篡改数组及非有限/非法输入；43项源码/配置/Protocol绑定通过。原275个导出成员在修复前后SHA一致；恢复导出共276个成员，增加明确来源记录。

**数据与评估划分。** 无新增训练数据、模型训练或SAE训练。保留列表discovery120/heldout120、完整dev800及全部固定DCLM窗口。Qwen九状态为29/43/71三seed×0/16/100步；八个原状态与S7列表沿用20条原生对tail资格，Qwen71/update100直接核验全部120条heldout原生终点。两种reader分开保留，不宣称统一原生三seed复验；原Qwen71 tail失败及一个S7 chunk失败仍为失败诊断。

| 阶段 | 实际完成范围 | 当前工程证据 |
|---|---|---|
| 主实验E03 |6轨迹、42个保存checkpoint、96/96门|原Full不变|
| 频率训练 |126轨迹、504个保存checkpoint、1,520/1,520门|原Full不变|
| 匹配Qwen SAE |244,380步、1,000,002,960个有效预测位置、15门|原Full不变|
| Qwen列表SAE分析 |9状态，各80矩阵/960干预|八个原reader状态加一个已登记原生恢复|
| S7列表SAE分析 |1状态、40矩阵/480干预|原完整分支；S7 SAE未重训|
| S7自然文本资格 |64条件、16矩阵、四来源梯度|原GPU测量加CPU验收；320个均值精确通过|
| 频率终点SAE描述 |36对、28,800条记录|原完整已登记产物|

**结果与证据。** [完整核验](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/completion_audit_20261010T1048Z.json)当前重读4,549个唯一文件SHA，并对142个登记输出ID做strict访问检查；逐项核对矩阵/干预全组合唯一覆盖、recipient身份、带符号及绝对端点SAE数组、有限值、no-op/恢复及相应原生误差门槛。[前置Smoke与保存数量核验](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/prerequisite_and_save_counts_20261010T1051Z.json)记录主Smoke64/64、频率Smoke56/56、修复SAE Smoke21/21。已授权范围不存在尚缺的实验条件或必需保存成员。

旧job `pt-8bnbcqqj`、`pt-azc2zkl5`、`pt-czzk7rb3`、`pt-f9dhsb6w`保留原状态，复合恢复结果不把任何失败平台job改成SUCCEEDED。原S7两个线性项在GPU/NumPy float32求和下相差3.4106e-12与5.4570e-12；统一float64重算全部数组均值后，最大记录变化7.8528e-11。[恢复来源记录](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/payloads/s7_native_dclm/summary_recovery_lineage.json)列明每项变化，原测量数组字节不变。登记后完整验证再次通过。登记辅助文件移至payload外，保留[字节不变迁移凭证](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/registration_bookkeeping_relocation.json)。

**产物清单。** 新S7资产`representation_a17_raw_sae_s7_summary_recovery_20261010t104246z_s7_native_dclm`及[登记回执](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/registration/registration_request_registered_outputs.json)。[当前选定输出访问快照](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/completion_audit_20261010T1048Z_access.json)只覆盖本次核验输出，不是全库复查。[恢复资格](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/summary.json)、[冻结来源](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/freeze_manifest.json)、[postflight](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/postflight.json)及[原GPU失败日志](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_fullseq_recovery_20261010T100922Z/podlogs/a17-s7-native-recovery-20261010t100922z-20261010T101533Z.log)保留实际来源，不新增GPU提交。

**边界与下一决定。** 当前已授权执行、工程修复和产物恢复全部完成。重构、回放资格与数值记账不证明共同/独特功能、atom因果作用或专家收益。机制判断及问题关闭仍Unknown；总体解释待研究者讨论，此处不指定新实验。
