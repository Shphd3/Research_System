# R05 公平性与数值审计

证据快照：2026-10-22T17:46:07.547181+00:00。状态：`COMPLETE`。

队列定义的89个正式实验中，89个已有完成证据。本审计核对曝光、容量、实际保存状态和数值记录，不裁定科研假设。

完整逐项证据见[fairness_checks.json](/data/250010109/MoE_Router/experiments/20261023_autonomous_retention/analysis/fairness_checks.json)。仍在运行和缺失的项目保留在下表。

## 曝光是否匹配

审计按同一阶段、同一seed比较完整的冻结record ID顺序，并核对每个实际20目标窗口。A/C每步只看20个新模式答案；B/D/E每步看10个旧模式和10个新模式答案。F预测自然文本的下一token。A与B的训练分布不同，不能直接把跨阶段原始分数差解释为方法效应。seed29/43/71改变续训顺序和已登记随机性，但共用一个已学旧任务父模型，不是三次独立的旧能力获取。

| 阶段 | Seed | 已完成臂 | 未完成或缺失 | 顺序检查 |
|---|---:|---|---|---|
| R1/A | 29 | U, TS, UL, US, TC, RS, LS | none | PASS |
| R1/A | 43 | U, TS, UL, US, TC, RS, LS | none | PASS |
| R1/A | 71 | U, TS, UL, US, TC, RS, LS | none | PASS |
| R1/B | 29 | Full, SN, SP, DN, DP, SRN, RN, SRP, RP | none | PASS |
| R1/B | 43 | Full, SN, SP, DN, DP, SRN, RN, SRP, RP | none | PASS |
| R1/B | 71 | Full, SN, SP, DN, DP, SRN, RN, SRP, RP | none | PASS |
| R1/C | 29 | fixed, sham, dynamic | none | PASS |
| R1/D | 29 | multi_normal, ordinary, single_normal, single_protected, multi_protected | none | PASS |
| R2_full_native_SwiGLU/D | 29 | multi_normal, ordinary, single_normal, single_protected, multi_protected | none | PASS |
| R1/F | 29 | dense_normal, dense_protected, ordinary2, shared2_protected | none | PASS |
| R2_full_native_SwiGLU/F | 29 | dense_normal, dense_protected, ordinary2, shared2_protected | none | PASS |
| R1/E/fixed | 29 | full, summary, random_summary, oracle, random | none | PASS |
| R1/E/joint | 29 | full, summary, random_summary, oracle, random | none | PASS |
| R2_full_native_SwiGLU/E/fixed | 29 | full, summary, random_summary, oracle, random | none | PASS |
| R2_full_native_SwiGLU/E/joint | 29 | full, summary, random_summary, oracle, random | none | PASS |

## B：总容量与单模式容量

有效自由度指能独立改变有效矩阵的坐标数。优化器保存的张量还含有不影响有效矩阵的冗余坐标。Full是普通全矩阵Adam。SN/SP共用完整补空间；DN/DP复制补空间，每个模式可用的空间保持相同，但总容量增加。SRN/SRP与RN/RP匹配总有效自由度，同时改变每个模式能调用的空间。

| 臂 | Seed | 状态 | 总有效自由度 | 每模式可用自由度 | 保存的可训练坐标数 |
|---|---:|---|---:|---:|---:|
| Full | 29 | COMPLETE | 6,291,456 | 6,291,456 | 6291456 |
| SN | 29 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| SP | 29 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| DN | 29 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| DP | 29 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| SRN | 29 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RN | 29 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |
| SRP | 29 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RP | 29 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |
| Full | 43 | COMPLETE | 6,291,456 | 6,291,456 | 6291456 |
| SN | 43 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| SP | 43 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| DN | 43 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| DP | 43 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| SRN | 43 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RN | 43 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |
| SRP | 43 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RP | 43 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |
| Full | 71 | COMPLETE | 6,291,456 | 6,291,456 | 6291456 |
| SN | 71 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| SP | 71 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| DN | 71 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| DP | 71 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| SRN | 71 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RN | 71 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |
| SRP | 71 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RP | 71 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |

行空间对照在每半行内对受限候选原子计算Gram矩阵逆，再去掉候选分量。实现没有假定“行掩码”与“完整空间投影”可以交换。B在候选系数和补空间坐标上使用Adam，与Full的全矩阵Adam不同；Full负责普通容量和可学性参照，B内部四臂比较保留自己的优化坐标。

## D/E：真实计算与路由监督

R1只训练原生最后一层SwiGLU的down projection，gate/up冻结。R2是独立登记的资格修订轮，训练完整原生gate/up/down三矩阵；各投影先合成有效共享权重，再执行原生SiLU与逐元素乘法。两轮结果分别记案。已知模式路由、随机路由和推理只执行选中的专家；可学习路由的直通估计训练为了计算替代梯度，会求出两个专家的输出。因此top-1推理预算不代表训练FLOPs相同。已声明的投影/head估算未计反向、归一化、参数合成和前缀缓存获取。

| 实验 | 状态 | 专家有效自由度 | 每token活跃自由度 | Router参数 | 训练专家矩阵乘 | 推理矩阵乘 |
|---|---|---:|---:|---:|---:|---:|
| R1/D/multi_normal/main/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R1/D/ordinary/main/seed29 | COMPLETE | 6291456 | 3145728 | 0 | 1 | 1 |
| R1/D/single_normal/main/seed29 | COMPLETE | 3145728 | 3145728 | 0 | 1 | 1 |
| R1/D/single_protected/main/seed29 | COMPLETE | 3145728 | 3145728 | 0 | 1 | 1 |
| R1/D/multi_protected/main/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R1/E/full/fixed/seed29 | COMPLETE | 6291440 | 3145728 | 6146 | 2 | 1 |
| R1/E/full/joint/seed29 | COMPLETE | 6291440 | 3145728 | 6146 | 2 | 1 |
| R1/E/summary/fixed/seed29 | COMPLETE | 6291440 | 3145728 | 34 | 2 | 1 |
| R1/E/summary/joint/seed29 | COMPLETE | 6291440 | 3145728 | 34 | 2 | 1 |
| R1/E/random_summary/fixed/seed29 | COMPLETE | 6291440 | 3145728 | 34 | 2 | 1 |
| R1/E/random_summary/joint/seed29 | COMPLETE | 6291440 | 3145728 | 34 | 2 | 1 |
| R1/E/oracle/fixed/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R1/E/oracle/joint/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R1/E/random/fixed/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R1/E/random/joint/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/D/multi_normal/main/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/D/ordinary/main/seed29 | COMPLETE | 18874368 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/D/single_normal/main/seed29 | COMPLETE | 9437184 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/D/single_protected/main/seed29 | COMPLETE | 9437184 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/D/multi_protected/main/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/E/full/fixed/seed29 | COMPLETE | 18874320 | 9437184 | 65730 | 2 | 1 |
| R2_full_native_SwiGLU/E/full/joint/seed29 | COMPLETE | 18874320 | 9437184 | 65730 | 2 | 1 |
| R2_full_native_SwiGLU/E/summary/fixed/seed29 | COMPLETE | 18874320 | 9437184 | 1218 | 2 | 1 |
| R2_full_native_SwiGLU/E/summary/joint/seed29 | COMPLETE | 18874320 | 9437184 | 1218 | 2 | 1 |
| R2_full_native_SwiGLU/E/random_summary/fixed/seed29 | COMPLETE | 18874320 | 9437184 | 1218 | 2 | 1 |
| R2_full_native_SwiGLU/E/random_summary/joint/seed29 | COMPLETE | 18874320 | 9437184 | 1218 | 2 | 1 |
| R2_full_native_SwiGLU/E/oracle/fixed/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/E/oracle/joint/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/E/random/fixed/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/E/random/joint/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |

固定专家阶段对预定D来源的bank字节比较：R1/full/seed29=PASS, R1/summary/seed29=PASS, R1/random_summary/seed29=PASS, R1/oracle/seed29=PASS, R1/random/seed29=PASS, R2_full_native_SwiGLU/full/seed29=PASS, R2_full_native_SwiGLU/summary/seed29=PASS, R2_full_native_SwiGLU/random_summary/seed29=PASS, R2_full_native_SwiGLU/oracle/seed29=PASS, R2_full_native_SwiGLU/random/seed29=PASS。联合训练单独记案，只要求初始bank等于固定阶段来源。可学习router接收答案CE和负载损失；已知模式参照额外接收真实模式。全表征router的参数数多于16维摘要，随机摘要只匹配摘要维度。“oracle regret”是相对同一组专家的已知模式分配的CE差，允许为负；该分配不是逐样本最优专家下界。


D专家学习资格与上述工程检查分开。已完成D实验中，未通过或证据不完整的资格项：R1/multi_normal/seed29=FAIL、R1/ordinary/seed29=FAIL、R1/single_normal/seed29=FAIL、R1/single_protected/seed29=FAIL、R1/multi_protected/seed29=FAIL、R2_full_native_SwiGLU/multi_normal/seed29=FAIL、R2_full_native_SwiGLU/ordinary/seed29=FAIL、R2_full_native_SwiGLU/single_normal/seed29=FAIL、R2_full_native_SwiGLU/single_protected/seed29=FAIL、R2_full_native_SwiGLU/multi_protected/seed29=FAIL。E关于功能选择的解释受其精确D来源的学习资格约束，R2不能追认R1专家已合格。

## F：自然文本分母与解释范围

划分审计：`PASS`。训练文档128篇，验证文档64篇；每篇127个预测目标，验证共8128个目标。审计检查了训练与验证的文本哈希和token窗口哈希不相交。预训练曝光仍为Unknown。列表任务95%准确率资格线不能变成自然文本CE的资格门槛。

F的四臂比较整个配置包，路由、容量、共享和保护会一起变化，因而不能独立识别共享或保护效应。另做的A终点自然文本读数通过完整Qwen执行已改变的attention，完成状态单列在JSON。

## 数值与源码版本证据

每个已完成实验都核对实际batch ID和计数、必需TensorBoard坐标及实际保存状态。已被独立完整复核过的payload哈希会标明来源后复用；只对首次遇到的保存状态重新做完整SHA256和CPU张量检查。E专家bank的字节摘要另按不可变payload哈希缓存。

每个实验的磁盘文件哈希来自原队列或v2队列的冻结记录，审计没有假定所有实验使用同一SHA，也不把磁盘哈希当作已载入Python字节码的摘要。已记录的retention engineering-v2只增加B原始投影的逐步version检查和结束字节检查；保存的差异文件没有改变模型计算、指标或RNG操作。历史v1 Smoke保留当时的检查范围。无法识别的执行版与当前版差异会在JSON中保留为待复核项。


R2另有已记录的评估器修复：只有存在两个专家时，自然文本读出才计算双专家混合。保存源码的AST比较确认evaluate_natural之外的代码全部一致。五个正式实验的队列冻结早于修复，其中四个环境记录的磁盘哈希与旧版一致；F/dense_protected跨过修补时间窗口，其实际载入源码的精确字节仍为Unknown。两个可能版本的训练代码相同，该dense实验也不进入改变的oracle读出分支。完整时间和版本对账保留在JSON。

## 缺失和运行中的证据

本快照中队列定义的正式实验均已有完成记录。


已完成但审计证据仍受限的实验：

- D_multi_normal_29：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- D_ordinary_29：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- D_single_normal_29：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- D_single_protected_29：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- D_multi_protected_29：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- E_full_fixed：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- E_full_joint：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- E_summary_fixed：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- E_summary_joint：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- E_random_summary_fixed：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- E_random_summary_joint：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- E_oracle_fixed：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- E_oracle_joint：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- E_random_fixed：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- E_random_joint：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- F_dense_normal：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- F_dense_protected：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- F_ordinary2：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。
- F_shared2_protected：BOUNDED_MISSING_EVIDENCE；MISSING=['case-level environment version/precision receipt']；错误项=[]。