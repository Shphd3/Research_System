# 协议：A15_27 R02频率、距离与两线索整合

## 0. Approval Snapshot

状态`APPROVED_FOR_BOUNDED_READONLY_PENDING_SOURCE_FREEZE`。2026年10月26日用户已授权先冻结后直接有界只读执行；数值约定为`DELEGATED_BOUNDED_ANALYSIS_CHOICES`，不伪造逐块人工批准。仅在来源/计划/文本一致性PASS及首次前向哈希收据之后可执行，目前未看新响应。[Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/15_27_natural_language_feature_response_anchor_cn.md)／[Focus](../../../../focus/focus_natural_language_feature_response_cn.md)保持问题所有权；本轮为操作定义/代理检验。Q1/Q2/Q3分别支持、削弱或不足。主要竞争解释为稀疏目标支持、词面、位置及编码非线性。

只用当前已有H100MIG：`execution_surface=current_container`、`resource_profile=USER_AUTHORIZED_EXISTING_RESOURCE`；这是用户本轮覆盖默认提交配置的明确范围，不申请/购买资源。计划1024参考+120面板+4重放+4截断前缀=1152条，绝对上限1500；主面板≤120条、每条≤256token，实际112–139。无模型/字典/专家训练、干预、封存TEST、删除、提交推送或外部发布。

## 1. Terminology / Definitions

Feature是固定模型/hook/字典坐标；样本为目标token及可见前缀，早期读数只用其当时前缀解释。频率是同模型、FP32编码、Top32门控在独立参考有效位置的正激活比例，不是词频、强度、奇异值或面板命中率。关系组来自语义编辑贡献差轨迹，频率/距离/整合标签均不参与聚类。距离为最后相关线索末端到最终目标开始间的token数；短1–8、长48–64只是本轮尺度，实际按线索二计为6/7与48/49；线索一距离另列。整合指注册的两线索联合响应，不是统一语义高度。[对象对照](object_comparison_cn.md)区分旧概念。

## 2. Anchor Alignment

Q1检验独立构组后的频率关联；Q2检验近远线索效应；Q3检验联合响应超过纯位置推进。原激活cosine只描述，主要关系用配对差；差向量范数为零则cosine为NA。不推出专家划分、频率因果或学习收益。

## 3. Tested Hypotheses

P1：5个预定旧发现稳定组的log频率差小于完整保边际重构组null。P2：固定组的线索效应在近远移位下有可复现差异。P3：两线索齐备处联合响应增加、超过无关/推进对照，并符合预定候选语义。一个问题非支持或不足不替另外两个裁决。

## 4. Rival Explanations

共同目标词支持可造成组相关；补G02/G04条件支持匹配。稀疏边际可制造同频聚类；保边际并完整重跑。局部词面、中性块句序/新近性和不等阶段跨度仍为竞争解释。SAE/ReLU/TopK能产生非加性而无语义整合。不假设导师已定义cluster或旧类别树就是feature高度。

## 5. Data Construction And Provenance

R01D36决定旧组，旧D/H都已暴露；复核旧H不是新确认。保留bass是针对已知R01缺口，不称盲选目标词。新增12情境由Codex构造英文自然语言并受控编辑，6bass选择、6人物属性绑定，模板/实体/来源组与R01分开。每例四组合×近远共96条，再加12线索二中性位置控制及12无关星期编辑，共120。全文、线索span、token、检查点、候选对应与排除规则先冻结。

Bass线索一交换鱼/乐器描述顺序，线索二选第一/第二；00/11为鱼、10/01为乐器，候选为单token` swims`/` sounds`。人物线索一给二选一职业、线索二给二选一物品，从预定四名中确定一人。仅见线索一时保留两个允许候选，不能用未来线索二标签解释。目标分别bass(ID21529)与is(ID374)，不混成语义高度序列。

三个重复同token检查点在线索一、线索二及中性续写之后。四组合与中性控制的检查点绝对位置匹配；近远早期位置不同，只有最终位置/总长度匹配。阶段主分析只短版本。同距离语义编辑保持目标附近措辞；近远移动中性块也改句序/新近性及较长局部后缀，不称纯距离识别。

参考先固定：按排序前16个DCLM TRAIN bin，每bin以seed2026102602均匀选64个互不重叠256token窗，共1024；各丢前16位置，剩245760。它只估计此有限语料及窗口，不代表总体语言；不替用旧BF16频率。文本SHA256：a172212a9f7840ca63a8e84324a5ba01dde129083e80b8ddaae196713eb3e203。[精确token清单](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/panel/tokenized_sequences.jsonl)／[参考manifest](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/reference/manifest.json)。

## 6. Task And Permitted Supervision

没有模型学习。保存原z、原始贡献c=z×实际decoder列范数、c/hook范数、重构、候选log概率和支持。偏置/均值分开，贡献幅度不是加性解释方差。Bass候选仅语义兼容，不是唯一正确自然续写；人物标签是受控绑定读数。各检查点只按可见线索定义允许候选。

## 7. Frozen Assets And Interface

主输入为model_qwen3_0p6b_base_official_a5、tokenizer_qwen3_0p6b_base_official_a5、sae_qwen3_0p6b_e16_layer27_final_1b、dclm_pair_v1及已存R01表征/分析；当前严格访问及新算哈希绑定身份。模型SHA256`cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`；SAE`e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`。模型BF16eval/no_grad/SDPA/use_cacheFalse；SAE原生FP32ReLUTop32。hook为零起始27MLP输入（post-attention norm之后），1024→30000。不单位归一化输入或预减decoder偏置。

CrossCoder只复用暴露VAL行0–7：F16384共享z、14层residual-post、保存TRAIN中心/RMS及严格阈值。各层贡献不是独立激活，不对齐E16ID，不为Q1–Q3新增CrossCoder前向。[资产审计](asset_audit_cn.md)。

## 8. Objective And Optimization

无可训练模型/字典/专家参数、optimizer、更新、训练检查点或干预。发现侧OLS及离线分组只是统计，不是模型/字典训练。旧资产不变。

## 9. Conditions,Seeds And Frozen Candidates

分析seed20261026。旧固定64候选、83发现资格池由旧candidate_freeze与机器计划绑定；七组身份保留。Q1主组G01/G02/G04/G06/G07只按旧D共簇率≥0.70预定，G03/G05保留失败，不替补。Q2主G02/G04×bass，其余关系/组与feature次要。复用spectral-hier Python、已有Transformers4.53.3依赖路径与Torch2.5.1；不安装或比较模型/环境。

## 10. Primary Metrics And Frozen Analysis

**旧组资格。** 先复现旧G02/G04，以旧暴露H组内受控响应相关对比1000随机组，池为83旧D资格feature、排除本组。六目标的激活计数与六目标原始响应计数各维差≤1案例，log旧D贡献RMS差≤1池SD；按标准化13维平方距离取最近20。须≥800有限draw且≥20独特无序随机组。不放宽caliper/扩池、不匹配频率（频率本身是待解释量）；仍是暴露数据诊断。

**Q1。** p=n/N，每feature≥20命中、≥8命中窗。保存原计数、零/NA、token级Wilson95%描述区间和主2000参考窗block-bootstrap95%区间。仅bootstrap取log时用Jeffreys(count+.5)/(N+1)，原始频率点估不替换。组离散度为全部无序成员对abs(logp_f−logp_g)均值；主量是5个预定组等权平均，任一必要成员/组不可估则整体不足，不能删组救结论。

500次null：独立为30000feature各自将完整四版本激活tuple在同目标词的旧D案例间置换，保留逐feature/版本边际与目标支持。重算支持、RMS、排名/64上限、总贡献共同幅度协变量、OLS、响应、Pearson距离1−r/average-linkage/cut.5/min3及相同200案例bootstrap≥.70稳定筛选。频率不入聚类。Null量为所有生成的稳定、频率合格组的等权离散度；空或无资格为NA。须≥400有效null，报告组数分布。下尾p=(1+#null≤观测)/(1+#有效)，观测更小且p≤.05支持P1；主资格充分但非显著则削弱依据；频率/null不足则未决。按组大小匹配的5组BH次要结果不能救主失败。

**Q2。** 仅在新最终位置测旧身份。Bass S=(c10+c01−c00−c11)/2为乐器减鱼；人物保留四编辑边10−00、11−01、01−00、11−10，不压成任意姓名轴。组幅度为按旧Dscale归一化后成员RMS（人物还跨四边RMS），案例效应远减近。主G02/G04×bass采用双侧精确案例符号翻转，BH2；须每成员≥4/6案例活跃、组响应≥4、≥3模板、95%案例CI不含0、有效方向一致≥2/3。其余5组×bass及7组×people是一个12比较次要family；feature64×2另为次要。保存原/比例差、方向cosine、组一致性与候选偏好，相关编辑需超过同位无关编辑守门；零/支持不足不叫无距离效应。支持仅称移位敏感，不称纯距离或长程专属。

Q2另要求“短距离语义组RMS减同位置星期编辑RMS”的95%案例区间下界为正，其单侧精确p与距离双侧p取较大值后作BH2。若要说两组依赖范围不同，还须在相同6个bass案例直接比较G02与G04的远减近效应差：两组均通过上下文资格，精确p≤0.05且95%区间不跨0；不能用一组显著另一组不显著替代。

**Q3。** 每检查点I=c11−c10−c01+c00；bass I=−2S恒等，非独立证据。线索二前的对应前缀不随未见设置改变，禁止用未来语义。采用旧Dscale后组RMS（单feature绝对值）定义阶段增益norm(I2)−norm(I1)−norm(Ifinal−I2)；末项是中性推进，不声称已完美识别位置因果。同最终位置J=norm(c11−线索二中性)，U=norm(c11−星期编辑)，须J−U正。增益及J−U各单侧精确符号翻转，max(两p)作交并检验p，BH跨7组×2关系；64×2feature另为次要。

支持还需两95%案例bootstrap下界正、≥4/6有效案例、≥3模板，最终候选语义margin的95%CI正，且≥4/6案例的≥3/4组合偏好预定兼容候选；可见性/对齐/控制均通过。不同关系候选不同，早期只按可见允许集合解释。非加性或未经约束的位置推进不能支持语义高度；若仍不能分开信息与位置，普遍“后位更高级”保持不足，即使操作联合响应通过。

所有主区间用2000基础情境重采样，全部版本同块；参考区间整窗抽样。≤14案例符号翻转枚举全符号，保留零及有效数。缺失相似度NA不补0。不按新响应重挑组、换算法或调阈值。

## 11. Secondary Metrics And Measurement Guards

参考/面板测量位置须全有限，平均NMSE≤.15、p90≤.30，稀疏decoder求和加偏置相对误差≤1e−5。4同条件重放z最大差≤1e−5+1e−4maxabs(z)；4独立截断前缀检查h相对误差≤.01且z最大差≤.001+.01maxabs(z)。它们是工程一致性，不是语义整合或未来可见证据。保存数值差，失败停止相关解释，不放宽容差或换对象。

## 12. Known Good,Bad And Confusing Cases

未见线索二时配对前缀恒等是已知因果一致性检查；歧义或事后定义样本在响应前排除。大联合项却无兼容输出是语义解释的非支持案例。Bass代数项不能重复算发现。成功展示按G02后G04的固定顺序取完整通过者，否则首个固定通过feature；若无资格成功如实写无。反例取首个未过新资格/判据的预定组，显示其最大旧D对比与真实新反响应；全部通过则不虚构失败。

## 13. Stage Contract

| 阶段 | 目的与操作 | 输出/门槛 |
| --- | --- | --- |
| 来源/文本 | 查旧定义，固定文本/参考/身份，不看新响应 | 对象表、资产、分词资格；失败停止相关阶段 |
| 冻结 | 绑定Protocol/plan/code/text/reference哈希 | 首次前向收据前不调用模型 |
| 参考 |1024已有资源只读前向，精度匹配计数 | 命中/窗支持/区间与本地重构资格 |
| 面板 |120前向读三个同token位置，加4复放/4截断 | 原数组、logp、账本、资格，不引未来标签 |
| 离线 | 旧组复核、Q1全流程null、Q2/Q3独立 | 支持/失败/NA表及三图 |
| 交付 | 本科生可懂的观察、竞争解释与边界 | 仅两更新、一个后续建议，不自动延伸 |

## 14. Provenance,Outputs And Algorithms

执行owner为`/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/`；前向run_forward.py；精确统计offline/statistical_plan.json；文本权威panel/qualified_cases.jsonl及tokenized_sequences.jsonl；参考另有manifest。首次前向前冻结全部来源哈希，脏工作区以实际源码身份记录，不假称已提交。保存阶段收据/所有尝试账本、参考及窗计数、原z/c/h/重构/logp、旧候选scale身份、Q1null诊断、Q2/Q3支持/失败表、图契约及完整manifest。原payload留执行侧；小型记录和精选证据保留来源。

## 15. Success,Weakened And Insufficient

Q1需要全部5组和频率/全流程null合格；Q2/Q3需完整支持、区间、多重比较及控制。稀疏频率、匹配不足、有效null不足、重构失败、资源不可用或控制缺口均不足，不否定机制。次要结果不救主判据失败；新面板不保证有关系组复现。线索有效可与距离不稳并存，非加性不单独证实层级。

## 16. Cannot Claim

不推出频率导致聚类、已验证专家/知识模块、学习收益、统一语义高度、纯距离因果、层间信息诞生或跨字典ID对应。旧类别标签或树状高度不能定义本轮整合结果。旧R01和CrossCoder暴露样本不是新TEST。

## 17. Authorization,Freeze And Amendment Ledger

A–G内容有原始来源或本轮明确委托，不声称逐块人工确认。R01Protocol/Summary不变；当前Anchor/Focus修订前原字节已存执行侧provenance/r01_source_snapshots及hash，这是同problem_key的用户授权延伸，不重解冻R01。首次前向后本正文保留，实质修订须追加old/new、理由、已见数据、范围及资格影响。已授权的有界工作不重复逐项请示；研究对象/预算变化才停止报告。机制接受和关闭Unknown。
