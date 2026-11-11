# A5续训到1B：明早速报

AI分析；研究者判断 Unknown。更新：2026-11-11 05:34 北京时间。

**这条单种子轨迹中，A5在约1B仍优于原生baseline。** A5从R04第2000步完整状态继续到baseline的1B manifest指定第3816步；新增1816步。A5实际累计1000341504有效token，baseline恰1000000000，相差0.03415%。

| 模型 | EVAL NLL（nat，越低越好） | 硬集中度中位数 |
|---|---:|---:|
| A5@3816 | 3.763121999 | 1.338417415 |
| MoE baseline@1B | 3.779426355 | 1.049242805 |
| Dense@1B | 3.871651564 | 不适用 |

| pair            | band    |   difference |   ci95_low |   ci95_high |   documents |   replicates |
|:----------------|:--------|-------------:|-----------:|------------:|------------:|-------------:|
| A5-MoE_baseline | overall |   -0.0163020 | -0.0191177 |  -0.0126727 |        1871 |         2000 |
| A5-Dense        | overall |   -0.1085270 | -0.1127165 |  -0.1035535 |        1871 |         2000 |

P10：**支持**。P12：**比较口径不足**：原生baseline正式轨迹第2000步存档未保存；R03 A0起点代理的后段Jaccard为0.281250，前段旧臂配对中位数为0.630952，按代理数值套原规则为支持，主判断不把代理当精确原轨迹。

![A5与baseline曲线](loss_comparison.png)

左图到1B，右图约0.5B以后放大；横轴实际累计有效token，曲线只连实际评估。领先量见step_lead.csv/md：在真实baseline检查点间插值，超过范围标“测不出”。

AI分析：固定teacher原子分组的早期优势延续到更长训练，当前数据削弱“2000步后立即消失”的解释；不能据此转成无teacher可部署方案。

学习／遗忘：2000步后每250步及最后3750→3816的66步区间均已统计；阈值沿用R04。掌握率沿用teacher33B可学集合及ln2／2ln2迟滞，毛流量只统计可见快照，baseline稀疏采样会漏掉中间反复。完整表、解释和数据缺口见[分析报告](README_cn.md)。

单种子；baseline来自原硬件训练；A5分发依赖teacher；提示泄露仍未排除。训练结束后分析在本次保留Reserved任务内完成，没有使用MIG，没有重复提交baseline前向。分析完成后控制器退出并释放任务，平台终态由监督回执核验。

## 实际训练与资源

主任务平台ID：`om-8dy8ynho`；worker内部ID：`om-91a0eb8b4f064e10aa637000ab5031ec`；资源：`5090-4-reserved`。结构8层hidden1024、8expert Top2、507988992主模型参数；完整复用R04 teacher33B+SAE在线编码、冻结8组与w、gate各0.5、原负载bias规则。最新研究者指令已取代一小时等待：本轮使用4卡5090Reserved，微批8×累积4及SM120运行层，仍每步262144有效token，不宣称跨硬件轨迹逐位一致。

原始prompt SHA见evidence/protocol_freeze.json。起点SHA和全部状态核对见source_checkpoint_verified.json；没有重置模型、AdamW动量、scheduler、数据游标、load bias或四卡RNG。实际10步SIGKILL恢复到20步与不中断对比见runs/smoke_summary.json，通过后仅删除本任务smoke。新的完整存档只保留最近2个及终点，BF16权重每250步及3816步保存，实际清单见saved_checkpoints.json。

训练正式墙钟（含初始化／评估／存档）2.569小时。冒烟删除20357477538字节，滚动完整状态删除30478579675字节；生成回执时挂载文件系统可用95.134TB，不是账户配额。排队不计训练GPU时，最终平台complete_time和总分配GPU小时由监督回执给出。

## 训练 loss

![训练CE对比](training_loss_comparison.png)

50步尾随均值；原始逐步读数见training_CE.csv/md。竖线后为本轮续训，原生baseline的历史里程碑部分batch差异另列。

## 学会、遗忘和掌握率

学会是某原子支撑位置平均loss显著下降，遗忘是显著上升；n≥50、BH q<.05且绝对差≥0.01nat。净遗忘相对A5所有实际可见250步之后的历史最佳，选择历史最佳先Bonferroni再BH。原子支持重叠且文档依赖保留，计数为描述性读数，不能当作独立知识题或多种子证据。

|   from_step |   to_step |   delta_steps | band    |   atoms |   learned |   forgotten |   net_forgotten |
|------------:|----------:|--------------:|:--------|--------:|----------:|------------:|----------------:|
|        2000 |      2250 |           250 | overall |   29995 |     19234 |         230 |             470 |
|        2250 |      2500 |           250 | overall |   29995 |     18100 |         315 |             418 |
|        2500 |      2750 |           250 | overall |   29995 |     10771 |         343 |             411 |
|        2750 |      3000 |           250 | overall |   29995 |     25285 |          74 |              50 |
|        3000 |      3250 |           250 | overall |   29995 |      7991 |         550 |             241 |
|        3250 |      3500 |           250 | overall |   29995 |      2684 |         570 |             415 |
|        3500 |      3750 |           250 | overall |   29995 |      2323 |        1334 |            1246 |
|        3750 |      3816 |            66 | overall |   29995 |       256 |        1616 |            2458 |

![学习／遗忘](learning_forgetting.png)

每点对应表中的真实区间；末点只有66步，不把它当250步计数排名。

| reference                | stratum            | model   |   checkpoints |   first_tokens |   last_tokens |   K_initial |   K_final |   acquired_after_initial |   forgotten_after_initial |
|:-------------------------|:-------------------|:--------|--------------:|---------------:|--------------:|------------:|----------:|-------------------------:|--------------------------:|
| MoE33B                   | overall            | A5      |            16 |       65536000 |    1000341504 |   0.0941427 | 0.7353999 |                0.7859665 |                 0.1447093 |
| MoE33B                   | rare_high          | A5      |            16 |       65536000 |    1000341504 |   0.0672764 | 0.7156755 |                0.8217438 |                 0.1733447 |
| MoE33B                   | rare_low           | A5      |            16 |       65536000 |    1000341504 |   0.1245333 | 0.7505517 |                0.7401588 |                 0.1141404 |
| MoE33B                   | bigram_recognition | A5      |            16 |       65536000 |    1000341504 |   0.6803357 | 0.9686248 |                0.3925234 |                 0.1042342 |
| MoE33B                   | needs_context      | A5      |            16 |       65536000 |    1000341504 |   0.0565283 | 0.7204345 |                0.8112126 |                 0.1473065 |
| MoE33B                   | overall            | MoE     |             3 |              0 |    1000000000 |   0.0000000 | 0.6697444 |                0.6750021 |                 0.0052577 |
| MoE33B                   | rare_high          | MoE     |             3 |              0 |    1000000000 |   0.0000000 | 0.6619316 |                0.6675242 |                 0.0055927 |
| MoE33B                   | rare_low           | MoE     |             3 |              0 |    1000000000 |   0.0000000 | 0.6691171 |                0.6737764 |                 0.0046593 |
| MoE33B                   | bigram_recognition | MoE     |             3 |              0 |    1000000000 |   0.0000000 | 0.9506326 |                0.9525399 |                 0.0019073 |
| MoE33B                   | needs_context      | MoE     |             3 |              0 |    1000000000 |   0.0000000 | 0.6517206 |                0.6571933 |                 0.0054727 |
| MoE33B                   | overall            | Dense   |             3 |              0 |    1000000000 |   0.0000000 | 0.6335651 |                0.6391871 |                 0.0056219 |
| MoE33B                   | rare_high          | Dense   |             3 |              0 |    1000000000 |   0.0000000 | 0.6241409 |                0.6301275 |                 0.0059866 |
| MoE33B                   | rare_low           | Dense   |             3 |              0 |    1000000000 |   0.0000000 | 0.6339004 |                0.6387409 |                 0.0048405 |
| MoE33B                   | bigram_recognition | Dense   |             3 |              0 |    1000000000 |   0.0000000 | 0.9540657 |                0.9564499 |                 0.0023841 |
| MoE33B                   | needs_context      | Dense   |             3 |              0 |    1000000000 |   0.0000000 | 0.6129995 |                0.6188292 |                 0.0058297 |
| Dense_latest_34076363264 | overall            | A5      |            16 |       65536000 |    1000341504 |   0.1016237 | 0.7888925 |                0.8246687 |                 0.1373998 |
| Dense_latest_34076363264 | rare_high          | A5      |            16 |       65536000 |    1000341504 |   0.0741113 | 0.7861094 |                0.8771395 |                 0.1651415 |
| Dense_latest_34076363264 | rare_low           | A5      |            16 |       65536000 |    1000341504 |   0.1319414 | 0.7887902 |                0.7655226 |                 0.1086739 |
| Dense_latest_34076363264 | bigram_recognition | A5      |            16 |       65536000 |    1000341504 |   0.6935969 | 0.9864750 |                0.3604051 |                 0.0675270 |
| Dense_latest_34076363264 | needs_context      | A5      |            16 |       65536000 |    1000341504 |   0.0611543 | 0.7753851 |                0.8564074 |                 0.1421766 |
| Dense_latest_34076363264 | overall            | MoE     |             3 |              0 |    1000000000 |   0.0000000 | 0.7241321 |                0.7293812 |                 0.0052492 |
| Dense_latest_34076363264 | rare_high          | MoE     |             3 |              0 |    1000000000 |   0.0000000 | 0.7327159 |                0.7386051 |                 0.0058892 |
| Dense_latest_34076363264 | rare_low           | MoE     |             3 |              0 |    1000000000 |   0.0000000 | 0.7087485 |                0.7130844 |                 0.0043359 |
| Dense_latest_34076363264 | bigram_recognition | MoE     |             3 |              0 |    1000000000 |   0.0000000 | 0.9742568 |                0.9757269 |                 0.0014701 |
| Dense_latest_34076363264 | needs_context      | MoE     |             3 |              0 |    1000000000 |   0.0000000 | 0.7070327 |                0.7125402 |                 0.0055075 |
| Dense_latest_34076363264 | overall            | Dense   |             3 |              0 |    1000000000 |   0.0000000 | 0.6864557 |                0.6922630 |                 0.0058073 |
| Dense_latest_34076363264 | rare_high          | Dense   |             3 |              0 |    1000000000 |   0.0000000 | 0.6923091 |                0.6984831 |                 0.0061740 |
| Dense_latest_34076363264 | rare_low           | Dense   |             3 |              0 |    1000000000 |   0.0000000 | 0.6731291 |                0.6780726 |                 0.0049435 |
| Dense_latest_34076363264 | bigram_recognition | Dense   |             3 |              0 |    1000000000 |   0.0000000 | 0.9747468 |                0.9765109 |                 0.0017641 |
| Dense_latest_34076363264 | needs_context      | Dense   |             3 |              0 |    1000000000 |   0.0000000 | 0.6667471 |                0.6728308 |                 0.0060837 |

![掌握率与毛流量](mastery_flows.png)

用相同teacher33B逐位置loss≤ln2定义可学位置；当前loss≤ln2置“会”，≥2ln2置“不会”，中间保留上状态，首次中间区间初始化为不会。新学会和遗忘贡献的差严格等于掌握率变化。A5有更密的快照，baseline只在里程碑观察，粗网格会漏掉来回变化；不按毛流量大小直接判路由更好。十频段表mastery_flows.csv/md给按原子出现次数加权的读数，频段位置可重叠。

P12原始问题关注相同训练区间内忘掉的原子是否不同。当前正式baseline@2000缺失，R03 A0@2000沿用完整batch，而正式baseline此前有500M部分batch，二者不严格属于同一轨迹；后段1816步与前段1000步长度也不同。因此forgetting_overlap.csv/md保留全部21个旧臂对和后段代理比较，数值套用与主结论资格分开。

## 集中度与训练进度

| arm          | band    |   median_M |   median_M_EVAL |
|:-------------|:--------|-----------:|----------------:|
| A5           | overall |  1.3384174 |       1.3571807 |
| MoE_baseline | overall |  1.0492428 |       1.0667805 |

M由同一teacher原子在实际硬Top2名额上的分布、全局expert负载及DEV/EVAL频率口径构成；主版沿用DEV分母，EVAL分母版并列。先逐原子平均8层，再跨原子中位；M不含gate幅值，不能直接当训练收益。

| band    |   A5_step |   A5_NLL |   baseline_first_step |   step_lead | status                                |
|:--------|----------:|---------:|----------------------:|------------:|:--------------------------------------|
| overall |      3816 |  3.76312 |            4139.00228 |   323.00228 | interpolated_between_real_checkpoints |
| bin0    |      3816 |  3.24580 |            4125.73048 |   309.73048 | interpolated_between_real_checkpoints |
| bin1    |      3816 |  3.44032 |            4073.59132 |   257.59132 | interpolated_between_real_checkpoints |
| bin2    |      3816 |  3.47991 |            4181.49931 |   365.49931 | interpolated_between_real_checkpoints |
| bin3    |      3816 |  3.56393 |            4168.00702 |   352.00702 | interpolated_between_real_checkpoints |
| bin4    |      3816 |  3.54273 |            4120.60144 |   304.60144 | interpolated_between_real_checkpoints |
| bin5    |      3816 |  3.65492 |            4169.21311 |   353.21311 | interpolated_between_real_checkpoints |
| bin6    |      3816 |  3.74195 |            4153.83262 |   337.83262 | interpolated_between_real_checkpoints |
| bin7    |      3816 |  3.81436 |            4158.41108 |   342.41108 | interpolated_between_real_checkpoints |
| bin8    |      3816 |  3.89580 |            4140.91550 |   324.91550 | interpolated_between_real_checkpoints |
| bin9    |      3816 |  3.78552 |            4127.34433 |   311.34433 | interpolated_between_real_checkpoints |

![NLL与lnM](NLL_lnM.png)

三个面板为总体、bin0、bin9；只用旧A2/A1/A5三点拟合直线。星号是更长训练后的新点，曝光变化与结构变化不能混为一谈。原表NLL_lnM.csv/md保留竖直残差。

## 集中度拆解

![集中度拆解](concentration_decomposition.png)

沿用R05的对称替换方法，将逐原子平均M增量拆成分发条件分布q与全局负载分母u两项，DEV／EVAL频率比逐原子固定。合格n≥50；表concentration_decomposition.csv/md还给出配对提高的原子比例。两项份额只分摊可加的均值增量，不能套用到中位数变化，也不是因果贡献。实际q仍包含bias参与选择后的分布，M不包含gate幅值。

## 学会的内容与router

![内容与集中度](content_router_deciles.png)

复用监控对话任务A的定义，对A5与原生MoE／Dense在约1B的逐原子掌握率差，检查它与A5硬集中度的关系。主版用EVAL频率分母；总体、十频段、控制频率和对照模型自身掌握率的偏相关见content_router_correlations.csv/md；十分位和判读见content_router_deciles、content_router_rules。单种子、支撑重叠及快照密度差异保留；相关不等于集中导致学会。

| reference    | pair     |   median_within_bin_rho | low_monotonic   | high_monotonic   | result                             | researcher_judgment   |
|:-------------|:---------|------------------------:|:----------------|:-----------------|:-----------------------------------|:----------------------|
| MoE33B       | A5-MoE   |              -0.1166767 | False           | False            | 中间或单调条件未满足，如实报告     | Unknown               |
| MoE33B       | A5-Dense |              -0.0079347 | False           | False            | 未见主要集中相关（预写小效应阈值） | Unknown               |
| Dense_latest | A5-MoE   |              -0.1066503 | False           | False            | 中间或单调条件未满足，如实报告     | Unknown               |
| Dense_latest | A5-Dense |               0.0063558 | False           | False            | 未见主要集中相关（预写小效应阈值） | Unknown               |

## 判据、完整性和下一步

| prediction   | result                                                                      |      value |    ci95_low |   ci95_high | proxy_rule_result   | researcher_judgment   |
|:-------------|:----------------------------------------------------------------------------|-----------:|------------:|------------:|:--------------------|:----------------------|
| P10          | 支持                                                                        | -0.0163020 |  -0.0191177 |  -0.0126727 | nan                 | Unknown               |
| P12          | 不足：原生baseline@2000存档缺失，采用R03 A0起点代理；不同长区间跨度仍有影响 |  0.2812500 | nan         | nan         | 支持                | Unknown               |

最强竞争解释是早期优势来自进度差；P10和真实baseline领先量检查它是否仍在，而非证明其因果机制。P12起点代理不足以独立证明遗忘对象机制。需要研究者先讨论结果，再决定后续模型；本轮没有追加别的主臂或新的架构训练。AI分析与研究者接受分开，科学判断Unknown。

边界：同一seed17；EVAL文档2000次重抽样只反映评估抽样、不反映种子方差；FP32权重配合bf16 autocast，逐位置loss存FP16。teacher分发依赖外部33B-token存档，历史bf16／fp32原子一致率及提示泄露边界沿用R04/R05，不用单种子或泄露阴性探针作无风险证明。同token对比没有匹配teacher此前33B token训练和本轮在线前向成本，本轮不把同token优势称为同算力性价比收益。A5与原生路由还同时包含分数来源、固定gate及bias行为差异；P10检查整套A5方案，不能单独把收益归因于集中度。

产物链：NLL_by_step、endpoint_CI、step_lead、concentration、learning_forgetting、mastery_flows、forgetting_overlap、NLL_lnM和predictions；代码在code，原始数据和权重不入ZIP，实际路径及SHA在evidence。完整状态资产checkpoint_family_r06_A5_to1B_20261111；逐位置产物representation_r06_A5_native_evaluations_20261111；复用原生1B缓存representation_r06_reused_baseline_1b_20261111。所有旧R03/R04/R05/baseline文件保持只读。
