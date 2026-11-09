# 运行前审计：科学识别、数据统计与数值实现

审计阶段仅为来源／构造及平台接受提交。此记录尚未核验作业`pt-ds9bdaxb`进入GPU。这些检查保障可解释性，不确认研究假设。

## 1. 科学识别

设计／核算范围PASS：主变化是专家跨深度分配，专家／router总参数精确匹配，hidden、专家宽度、top-2、attention与绑定词表接口不变。H1看终点低频token NLL，同时保留整体／高频代价。这是频率代理，不是语义长尾表征。导师直觉、既往口头报告与本轮假设已在[来源审查](source_review_cn.md)分开。

仍有单对初始化敏感性、小前缀重复曝光、优化／负载控制交互及实际dispatch／计算差异。router／接收量改变是架构行为观察，不能据此识别负载因果中介。变宽草图仅公式，不属于A／B。

## 2. 数据统计

精确文档切分／来源构造PASS：先按token字节全局去重，再分开发／测试／训练。完整冻结dev／test保留整体损失。实际循环监督目标计数决定整数类型三分位桶，未见独立；共同预算固定计数，最终模型指标不能改规则。已按要求看测试metadata／样例，未用模型测试表现选配置。

LIMITED：只扫描确定性67,108,864token前缀，未查近重复。恢复文档用于成对bootstrap，但packed上下文可能跨文档，仍有残余相关。确切类型数／阈值／覆盖待正式冻结。无独立可信出现次数与切分合同，事实／实体评估NOT RUN。2,000次成对文档重采样只描述采样，不替代多训练种子。

## 3. 实现与数值

CPU参数清点／共同起点PASS：两组均507,988,992，64专家完整计入，绑定头只计一次，242共有张量与42共有router行相等。见[真实账本](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/parameter_ledger.json)及[初值哈希](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/initial_parameter_hashes.json)。

GPU证据PENDING：前反向与梯度有限性、assignment恒等／无drop、真实吞吐／显存、保存重载、跨进程重放及评估复算。提交回执不等于短测通过。完整阶段资格需共同关卡与不可变冻结。理论激活参数／FLOPs是核算，未实际测量不能称硬件指令FLOPs已测。保留失败／重试，不能单减一组预算强行完成。

## 完成后的三部分审计更新

科学识别：同量／同曝光比较已完成，本轮低频与整体B更差；不解释为SNR原因，不关闭问题。数据统计：30项raw值与独立2000次文档区间复核PASS，low仅246／544文档有1481目标；单种子／packed依赖仍保留。实现数值：A/B各874步有限／计数／drop0／TensorBoard审计PASS，数据hash全一致；8冻结代码、5旧复用源及11项分析来源SHA未变；正式seed20261106初态在双家族strict后实际读取比较PASS。正式A/B与分析资产strict登记PASS。所有PASS仅确认对应工程／统计事实，科学接受Unknown。

## 最终关卡更新

上述GPU PENDING为注册前快照。实际两组短测、精确外部恢复／DEV复算、874步共同数据与计数、全部正式评估、独立区间复算、正式初态、冻结／旧源哈希和实际资产严格检查现已通过；证据见[Detailed](detailed_cn.md)与[交付检查](delivery_completion_checks.json)。科学接受仍Unknown；完整硬件FLOPs未测，保留矩阵算子计数与有假设的全图估计。
