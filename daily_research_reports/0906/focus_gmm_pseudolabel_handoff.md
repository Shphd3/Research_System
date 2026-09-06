# 原伪标签专家的在线路径为什么损失收益？

```text
problem_key: A15.gmm_pseudolabel_oracle_gap
focus_role: SECONDARY
task_state: ACTIVE
cycle_start: 2026-09-06
target_meeting: NOT_SPECIFIED
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: AWAITING_HUMAN_CONFIRMATION
```

本任务续接原八任务伪标签路径交接问题。旧文件 `0903/focus_gmm_pseudolabel_oracle_gap.md` 已被逐层静态审计占用；本任务不接管该问题，不改变静态、插层或 SAE 任务归属。

## 核心问题与当前判断

固定原专家库，外部纠正粗路径能恢复多少在线部署损失，剩余差距是否仍需修复细路由？用户已认可四步顺序，并明确要求执行第一步、路径修复和架构审计。第一步已完成：外部纠正粗路径恢复大部分交接损失，原训练粗路由缺少梯度。当前局部验证节点推进为：补足粗路由监督，能否在不改变专家、细路由、标签和读取位置的情况下恢复在线收益。用户已表示理解原实验，要求构建第二步验证计划，并授权标准配额资源；第二步具体设计随后已明确确认并完成执行。

## 实验一（已完成）：粗路径干预与架构审计

### 1. 目的
在不训练参数的条件下定位粗细路径对原部署差距的贡献，决定后续只修粗路由还是完整修复粗细路由。

### 2. 假设
强制原教师粗路径、在该父组内重新预测细路径应降低损失；竞争解释是细路径也失败，或教师细专家不优于同父错误细专家。

### 3. 分析方法
1. 固定种子 17、29 的八任务硬伪标签检查点、原标签、512 条评估样本和单位专家系数，比较原在线、教师粗加预测细、完整教师、教师粗加同父错误细四条件；错误细专家全部枚举后按样本平均。
2. 检查参数冻结、父子路径合法、完整前向干预、答案掩码和原始路径重放；配对计算粗纠正、细纠正、细匹配的损失差和样本重采样区间。
3. 核对训练阶段、粗细监督梯度、检查点权重变化和实际输入读取位置；实现只修复干预入口，不在本步更新已训练专家或启动新训练。

### 4. 结论分支
- 纠正粗路径即可接近完整教师：下一步优先只训练粗路由。
- 粗纠正和细纠正均有收益：下一步完整训练粗细路由。
- 教师细专家不稳定优于同父错误细：先查标签与专家匹配。
- 两种子不一致、区间跨零或资格检查失败：保持证据不足，不扩大方法。

## 实验二（执行与审核已完成）：只补足粗路由监督

### 1. 目的
把第一步“外部给定粗路径有效”变成一次可部署路由验证，判断原监督缺失能否通过只训练粗路由修复。

### 2. 假设
用原伪标签监督粗路由，应使完全在线的答案损失低于原模型，也低于同预算打乱标签训练。竞争解释是收益仅来自类别比例调整，或只存在于训练中重复出现的题目；这些情况下不支持样本与标签对应关系带来的在线修复。

### 3. 分析方法
1. 固定原两种子检查点的专家、细路由、原标签和实际读取位置，分别只训练粗路由预测原粗标签、或预测按样本打乱但数量相同的粗标签；两组各训练相同的四遍数据，选择固定最后一步。
2. 在相同样本上比较原在线、修复后在线、打乱标签后在线，以及外部给定粗路径和完整伪路径两个参考，计算答案预测损失；同时检查粗标签预测情况，但不把分类准确率当作任务收益。
3. 保留完整评估以承接第一步，同时单列与训练记录编号不重叠的 384 条样本；只有两个种子在两种样本范围上都可靠优于原在线和打乱对照，才支持本次修复。报告剩余差距，不事后定义“已完全恢复”。

### 4. 结论分支
- 满足全部损失比较：支持有限预算下的粗路由在线修复，保留其为后续基线，再判断残余差距是否需要改变标签或细路由。
- 至少一个必要比较在两个种子上都可靠不支持：指出具体失败环节；若分类改善而任务不改善，不能宣布路由成功。
- 种子不一致或区间跨零：证据不足；依据预先记录的训练与评估诊断定位下一检查，不同时展开所有候选。
- 实现、数据或冻结检查失败：结果不具科学判定资格，先处理执行问题。

## 四步关系
1. 已完成：冻结路径干预和架构审计，定位粗路径与监督缺失。
2. **当前位置：粗路由监督修复验证已完成并通过预定判据。**只训练了粗路由；专家、细路由、标签和读取位置均保持不变。
3. 第二步仍有断点时：拆分教师层位、上下文范围及读出能力；按结果选择一个诊断。不得预先把第二步失败归因为末层标签错误。
4. 候选交接机制成立后：再做路由与专家的功能训练，并验证真正分阶段训练或联合训练的收益。

本轮未创建新工作流或重置问题。资源偏好已确认：标准配额；不再请求配额选择。第二步监督、打乱对照、数据资格检查和训练预算均已由用户确认，执行与分析现已完成。

执行状态：第一步已完成。标准配额单张 H100 作业 `pt-5xgwtcam` 成功；三个回归测试、两种子小样本及完整原路径重放、路径合法和参数冻结检查全部通过。优化器更新次数为零。

AI 核验结果（`AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`，不代填人工认识）：外部纠正粗路径恢复种子 17、29 的原交接差距 98.24% 和 93.96%；粗纠正损失收益分别为 0.039619370 和 0.021731576 nat/答案词元，两种子的配对 95% 区间下界均大于零。正式判定为支持粗路径纠正；细路由残余差距仍为 0.000708633 和 0.001398138，不能宣布两条路径等效。原八任务硬伪路径训练没有粗路由梯度，七个保存点粗路由参数均未变化。

AI 建议：第二步先冻结专家和细路由，只训练粗路由，以验证补足监督能否带来在线收益。现已据此形成第二步候选设计；本次外部供给路径没有修好可部署 Router，也没有验证末层标签优劣。人工结果、不能声称的内容和下一决策尚待研究者填写或确认。

## 证据入口
- [原问题 Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md)
- [本步协议](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/protocol.md)

- [本步结果](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/summary.md)
- [完整证据](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/detailed.md)

- [第二步完整协议草案](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/protocol.md)

## 唯一下一决策
将本次修复检查点作为后续诊断的候选固定在线基线，确认其结果与不能声称的边界；第三步须以修复后的模型为比较起点。人工认识表述仍待研究者确认，不能把实验执行授权当成结果判断。


执行授权：用户明确确认第二步完整方案，并要求完成实验与四段式分析审核；标准配额单张 H100。全部设计、实现、小样本与完整运行、结果审核已授权，继续执行不再重复询问。


## 第二步完成记录（AI 核验，不代填人工判断）

作业 `pt-diap9xc9` 已成功。四个正式训练条件各 128 次更新，十组完整评估完成。正式判定：支持粗路由在线修复；两种子在完整与不重叠记录上，对原在线与打乱标签对照的八个区间下界全部大于零。完整评估平均答案损失由 0.836757 降至 0.804183。专家、细路由、底座冻结，标签和读取位置未变；原路径精确重放，所有资格检查通过。首个作业的检查代码失败保留且排除。

AI 解释：原来的大交接差距不应继续被当作“末层标签无法监督当前输入”的证据。修复只证实本内部任务上的粗路由监督有效；不证明标签最优、真实语义或干净公开基准收益。此处属于 `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`，研究者结果与认识表述仍待确认。

- [第二步结果摘要](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/summary.md)
- [中文四段式审核](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/summary_cn.md)
- [完整实验账目](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/detailed.md)
