> 历史阅读副本。科学内容与原始快照相同；仅解析原上下文相对链接。当前设计另见候选目录的现行Anchor。

# 临时 Protocol：自然文本连续学习中的 common 与 specialized 计算

版本：2026-10-03 capacity-r1。[Anchor](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261003_before_routing_refinement/reading/anchor_cn.md) 拥有科学设计；[旧 Protocol 快照](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261002_before_capacity_refinement/reading/protocol_cn.md) 保留原实验约定。本轮是一组六臂实验及其检查点干预。[英文完整执行契约](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261003_before_routing_refinement/reading/protocol.md)与本文件共同使用。

## 0. 审批快照

用户在 2026-10-03 04:14:29 UTC 明确要求持续约 2.5 小时研究，可选择小模型或约 300M 八层模型，所有训练用 8×RTX5090 SPOT，反复检查推理链，保留临时目录，不再审批。[原文记录](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/receipts/user_authorization.json)。执行状态为 `APPROVED_FOR_BOUNDED_STAGED_EXPLORATION`。下述细节是授权范围内 AI 选择的探索方案，不伪称为逐块人工科学确认。问题开放，实际可接受质量阈值与科学闭环仍为 `Unknown`。

## 1. 术语与定义

C：每层始终使用的 common FFN。E_d：由已知领域 d 选择的私有 FFN。T：其他参数，包括绑定的 embedding/输出权重、领域嵌入、Attention 与归一化。领域 0/1/2/3 分别为计算机、数学、物理、生物。257 个存储 token 产生 256 个有效 NTP 目标。token 暴露包括重复遍历，不能称为新增独立数据。

## 2. Anchor 对齐

检验有限私有宽度下，共同计算与其串行组合能否改善习得和保持。旧的表征预测问题不构成前置。沿用同一问题与临时路径，不新建 Focus、不移项目、不因执行完成而宣称科学闭环。

## 3. 待检验假设

H1：parallel 相比初始函数匹配的 private_active 能提高资源效率。H2：serial 相比 parallel 改善固定预算表现。H3：在旧专家确实不变时，旧域损失变化可通过 common/主干有限回滚定位。主指标是习得、保持、终点损失及资源坐标组成的向量，不是一个方法好坏标签。

## 4. 替代解释

检查欠训练、预算差异、主干漂移、领域顺序、初始函数、深度与优化、领域标签特权、数据重叠和专家优化器漂移。没有加入深度匹配的第七臂，因此 serial 优势仍保留有效深度解释。seed 与 order 绑定，两个组合不能分别估计两者效应。

## 5. 数据构造与来源

本地 m2d2_paired_dev_v1 八个类别：cs.CL/cs.CV、math.AP/math.NT、physics.optics/physics.flu-dyn、q-bio.GN/q-bio.NC。使用官方 train.txt/valid.txt/test.txt 成员；Qwen3 tokenizer 不加特殊 token；仅选长度至少 257 的文本，取前 257 个 token。每类别 train 8192、dev/test 各128；每领域 train16384、dev/test各256。训练独立预测位置共 16,777,216，全部选中记录共 67,584。

按固定 test→dev→train 顺序做全局全文与257-token完全去重；dev/test 还排除旧0930/1002面板的全文与256-token前缀重叠。没有文章ID与近似去重保证。候选池仅按预定数量和长度扩展；在任何训练前，math.AP dev/test、math.NT test 不足，改为扫描其固定5MB完整成员。保留失败尝试和数据修订，不改配额、不按模型损失挑样本。

[数据NPZ](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/data/capacity_data.npz) SHA256：`6ed1bdb93e9734682c2c46338c06303239638eee48e53d6b310bab669c4a7331`。[manifest](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/data/manifest.json) SHA256：`ea4e6f12d6d413653006391f88bca4dc707c9956d5dde611d802d336c58cded6`。24条独立重读/分词验证通过。test仅在预定最终检查点评估，不用于调参或选择检查点。

## 6. 学习任务与允许监督

每条文本256个目标的因果NTP；按记录领域固定路由。训练允许目标与领域标签。评估不利用实际目标选择专家。无辅助损失、SAE、蒸馏、teacher、预训练权重；混合阶段后不重放旧域。

## 7. 模型、架构与冻结条件

八层，h=256，4Q/2KV head，head_dim64，上下文256，词表151936，绑定embedding/head；所有臂的token输入均加4×256的领域embedding（计入trunk，使Dense也获得相同领域信息）；RMS epsilon1e-6，RoPE theta1e6，SwiGLU，无dropout。C宽256，私有宽384，4专家。[复用记录](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/reuse_decision.json) 给出已检查的原实现与hash。

| 条件 | FFN计算 | 总宽度 | 激活宽度 |
|---|---|---:|---:|
| common_parallel | C(z)+E_d(z) | 1792 | 640 |
| common_serial | C(z)+E_d(z+C(z)) | 1792 | 640 |
| private_active | E_d(z) | 2560 | 640 |
| private_total | E_d(z) | 1792 | 448 |
| dense_active | D(z) | 640 | 640 |
| dense_total | D(z) | 1792 | 1792 |

各式外加Attention后的残差。serial关键路径更长，名义乘法量相同不代表耗时相同。完整参数统计包含大词表embedding。按参数名/形状/seed初始化，同组合所有主干完全相同；common两臂C/E相同。private_active在每个专家中拼接C及对应E的gate/up行、down列，使初始函数与parallel在浮点误差内相同。其余参照不声称初始函数匹配。

## 8. 目标与优化

有效token加权CE，单位nats；无正则项（`NOT_APPLICABLE`）。AdamW beta=(0.9,0.95)，学习率3e-4，前256更新线性warmup，再cosine到3e-5；weight_decay0.1，梯度裁剪1。BF16 autocast、FP32参数/优化器。每次32条×256=8192目标，microbatch8，累积4，每条件DP world1。CE chunk512；精确配置的显存/吞吐以Smoke测量为准，必要实现修订在正式训练前留痕。非有限更新显式失败，不静默跳过。

512次混合更新，每次各域8条；随后4个单域阶段，每阶段1024更新。每轨迹固定4608更新、37,748,736目标暴露。记录确定性排列、游标、循环次数；同组合所有臂读取相同token序列。终点固定，不挑最好loss。最早1152更新草案在训练前扩到4608，目的是降低“还没学会”混同“容量不够”的风险，不是按结果扩预算。

混合阶段已向四域各暴露4096条记录、1,048,576个目标。自身阶段的学习增益衡量已见域的额外专门学习，不是首次遇到全新领域。

## 9. 条件、seed与检查点

12条轨迹：6臂×A(seed1003，0→1→2→3)/B(seed1004，3→2→1→0)。保存初始化、混合结束、四个阶段末完整检查点；每512更新周期保存，周期件仅保留最近两个。原子保存模型、优化器、token/update、数据游标/排列/重复轮次、RNG、配置与源代码身份；每run唯一写锁。SPOT中断可同配置、同资源恢复，日志坐标不得冲突。

## 10. 主指标与分析计划

初始化、每512更新、混合结束与每阶段结束均评估四域dev。每次评估保存token总损失和目标数；回滚分析另存逐记录损失。预定比较：serial−parallel；parallel−private_active；common两臂−dense_total；另在对应预算轴报告private_total与dense_active。分别报告两个组合及描述性均值，不把两个训练重复包装成充分功效的显著性检验。

领域自身阶段的学习增益＝阶段前loss−阶段后loss。后续阶段遗忘＝当时loss−自身阶段结束loss，保留负值（改善）。展示完整领域×阶段矩阵、最终等权领域macro dev/test，以及逐域差距。没有事后“等同Dense”的数值门槛；实用等价判断仍Unknown。

## 11. 次指标与保护检查

每个单域阶段前后，对所有未选专家的参数与优化器状态同时hash，要求完全相同；其grad必须为None，AdamW不得做衰减或动量更新。C/T允许更新。未选领域embedding行仍可能受AdamW动量或衰减影响，这归入T；旧专家冻结不等于旧域所有参数冻结。记录实际token数、loss、LR、梯度范数、显存、墙钟、有效token/s，以及观测契约要求的全部TensorBoard坐标。token轴是累计有效目标，update轴是优化器步数。

对后续阶段中已完成自身单域阶段的旧域，在固定dev记录和未改变专家上回滚C/T四格，保存L00/L10/L01/L11、交互、phi_C/phi_T、加和误差。private-only仅做trunk变化参照；Dense没有固定旧专家，不套用该机制条件。混合阶段不算旧任务遗忘。有限混合检查点不是可达训练轨迹。

## 12. 已知好、坏与混淆情形

实现正控：parallel/private_active初始函数一致；非选专家参数/优化器不变；连续2步与1步后恢复到2步一致；8192目标计数；有限loss/梯度；TensorBoard文件及tags真实存在。坏情形：上述失败、源代码/配置/数据身份不符、OOM或非有限loss。混淆情形：均值改善但某旧域受损；C有益但T伤害更大；Dense差距仅靠额外计算缩小。必须分别报告。

## 13. 科学流程与阶段约定

先冻结数据/代码/配置，做本地tiny实现检查。随后提交一台8×RTX5090 SPOT，保持指定镜像，激活挂载的SM120兼容Torch2.8/cu128层。验证八卡与BF16；对六臂精确shape做Smoke，检查目标数、loss、TB、保存与恢复。程序只有全部门槛通过才开始正式轨迹；Smoke不是科学支持。

12条轨迹在8GPU上排队。每轨迹墙钟上限5400秒；未达终点必须标未完成并从完整状态恢复，不能把不同终点混为最终比较，也不能暗减慢臂预算。用户约2.5小时研究窗口至06:44 UTC左右；若作业仍运行，如实报告状态。最后验证终点和guard，做回滚与再次推理审计，更新事实记录。

## 14. 算法、输出与来源契约

[执行根目录](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity) 保存选择清单、冻结hash、提交回执、持久日志、硬件与Smoke记录、条件配置、JSONL、TensorBoard、评估、guard、检查点与最终状态。选入临时研究目录的小型证据需记录来源/hash。原始数据和检查点不进入Research_System。不commit/push，不发布，不搬入正式项目。

## 15. 支持、不支持与不足分支

探索性支持：预定比较在两个组合中改善对应loss/保持且guard完整；仍需列出逐域与资源权衡。不支持：没有对应收益、反向，或收益以假设原本想避免的保持损失换取。不足：guard失败、终点不齐、组合不一致、强替代解释未排除，或更强容量主张缺少阈值/饱和定义。这些是解释分支，不伪装成人工确认的数值阈值。解释Unknown时仍完成事实记录。

## 16. 本轮不能声称什么

不能声称普遍共同知识、最大容量、槽位耗尽、一般学习路由优势、长期连续学习收益、排除深度后的串行机制、文章级独立泛化或约300M缩放结果。数据含重复暴露；领域标签提供路由特权。若用最终test结果再调参，必须标记其转为开发数据并修订契约。

## 17. 逐块确认、冻结与修订记录

A–G实质选择由AI在明确授权下完成，不伪称逐块研究者确认。训练前修订：三份不足评估成员扩大扫描；预算1152→4608；parallel/private_active匹配初始化；所有臂增加同样的领域嵌入，修正Dense缺少领域信息的问题，结构性专家路由仍是处理变量。后续Smoke代码或运行时修订，须在正式轨迹前记录hash。见结果后的修订必须明确标为事后，不追溯预注册。


### 2026-10-03 05:15 UTC：第二项有界机制诊断（训练结果出现前）

在用户的持续自主研究授权内，加入同前向的单层梯度通道诊断；不改变六臂训练、数据、优化器或固定终点。源自第三轮reasoning审计，属于第二项实验而不是第七条训练架构。此登记时pt-uasnh61d worker仍Pending，无新模型loss已读。

仅使用两条common_serial轨迹的第一个单域阶段结束检查点（global1536）。固定第4层（index3），只允许该层C做一次诊断位移。下一个领域order[1]为源，固定train索引0:32和32:64两份源面板；dev不参与构造方向。其他全部权重及优化器状态保持原样，原检查点只读。

比较普通梯度和仅在该层E输入中使用z+stopgrad(C(z))的梯度。外侧C(z)仍可微，两者初始前向/损失相同。将各自负梯度缩放到同一参数位移范数：原C参数范数的0.001/0.003/0.01；全部尺度和两份源结果均报告，不选最好值。零梯度记录退化。该一次SGD方向诊断不复现AdamW历史，不称为训练轨迹或长期方法评价。

每个扰动在固定四域dev各256条记录及对应源面板上测有限loss，保存逐记录差、源拟合变化、梯度范数/cosine、实际位移范数和非目标参数hash。重复baseline核验数值稳定，并保留BF16实际前向的有限效果。两个seed绑定不同顺序，检查点、源域与旧域也不同；分别报告，不当独立同任务重复。

它比较给定状态、给定层中包含或截断“专家传回C”路径后，分别归一化所得更新方向的有限跨域效果。归一化也重缩放直接梯度，因此不是该通道的独立加性贡献。对产生梯度的同一源面板，完整梯度在理想可微模型的一阶等范数比较中天然最陡下降；源面板优势本身不是跨域复用发现，旧域有限读数才检验未由该恒等关系预定的影响。它不隔离所有串行深度，不证明通用语义，不自动推出长期训练或容量收益。支持/不支持/不足分支沿第三轮审计，以逐域和源代价为依据；没有自动科学关闭。精确实现、hash与状态由[预登记](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/coupling_probe_registration.json)和执行收据持有。仅当同一8×RTX5090 SPOT allocation有可用GPU与所需检查点时执行；否则明确NOT RUN，不为填补结果更换资源。


### 2026-10-03 05:38 UTC：第三项有限评价——领域与专家的匹配

在任何新训练结果出现前，登记最后一项诊断，直接检查“按领域训练”是否对应“在该领域更合适”的功能性分工。它不新增训练条件，只读取8条含专家轨迹（parallel、serial、private_active、private_total×两个组合）的固定最终4608检查点。

对真实领域d，输入领域embedding仍用d；只将每一层FFN使用的专家强制指定为e，遍历e=0,1,2,3。C/T及所有权重保持不变。固定dev每域256记录，保存4×4损失矩阵L[d,e]及逐记录值。对角线e=d必须在1e-4内重现训练最终dev，整体参数hash不变；不读取test。跨层专家bank作为整体干预，不能将其解释为某一层或某一个语义特征。

主描述量S为非对角loss均值减对角loss均值，正值表示指定域—专家匹配在平均意义上更好。同时保存逐域own-versus-other均值、最优expert，以及双中心化交互I=L−行均值−列均值+总均值。四域均衡设计中，S=−4/3×对角I均值；加性的领域难度与通用expert质量项抵消。逐域最佳专家与margin仍可能受这些因素影响，不能单独当专门化证据。

本诊断只测该检查点共享计算背景下的领域—expertbank功能匹配，可能包括共同适配、阶段学习率与顺序效应。它不识别独立语义、最大容量或唯一的训练原因。S及逐域结果连续报告，无事后阈值；seed/order组合分别报告。精确实现见[预登记](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/expert_swap_registration.json)。

上述三项有界工作（六臂训练与C/T回滚、同前向梯度路径、专家交换评价）覆盖当前问题，暂不继续添加实验。分析入口将在首次执行前单独冻结为同一GPU的顺序分析链：C/T回滚→专家交换→仅serial运行梯度路径诊断。训练源代码/配置/预算/初始freeze保持不变。此时worker仍Pending，无新loss；原分析源码、冻结快照及修订理由均保留。
