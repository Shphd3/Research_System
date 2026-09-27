# 语义伪标签监督为何在两个种子上产生相反的在线任务收益？

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: A15.gmm_pseudolabel_oracle_gap
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: AWAITING_HUMAN_CONFIRMATION
result_state: HUMAN_CONFIRMED
cycle_start: 2026-09-06
target_meeting: Unknown
active_project: Projects/from-attention-to-search
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/protocol.md
summary: Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/summary.md
detailed: Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/detailed.md
source_meeting: daily_research_reports/0906/plans/sol_training_comparison_handoff_cn.md
core_experiment_count: 1
```

P1/P2 已定位并修复旧模型缺少父路由监督的问题。P3 从共同冻结基座重新训练完整对照，
现在已经完成并得到研究者确认的 `INSUFFICIENT` 判定。本 Focus 不再把 Astra 交接稿当作
结果记录；正式证据入口是 P3 `summary.md` 和 `detailed.md`。

## 1. 核心问题

固定 Qwen3-0.6B-Base、block 14 层级结构、干净数据划分、训练集拟合教师、512 更新和
load-off 后，为什么真实伪标签监督相对同架构纯任务训练在种子 17 上有益、在种子 29 上
有害？下一步只检查一个尚未分离的不确定性：当前父、子各 0.5 的语义辅助监督是否过强。

## 2. 已完成实验：P3 训练充分性与同架构语义增量比较

### 目的

在排除直接集合重叠、旧检查点复用、训练预算不一致和登记的专家饥饿触发后，判断真实
伪标签监督是否同时优于同架构纯任务与固定打乱标签监督。

### 假设

若样本与伪标签的真实对应提供稳定任务信息，则 H-sem 应在种子 17、29 上都比 H-task
与 H-shuf 具有更低的在线参考答案 NLL。最强竞争解释是收益来自辅助优化、标签频率、
路由负载或随机初始化，而非样本—标签对应关系。

### 分析方法

完成 D/F/SF/H-task/H-sem/H-shuf × 两种子的 12 个条件；开发集先冻结共同 512 更新、
load-off 政策，测试集随后只按登记的逐记录、来源分层 bootstrap 规则计算四个必要比较。
正式判定后，再只读检查 H-task/H-sem 在开发集 128/256/384/512 步的反转、来源贡献、
负载、分类损失、梯度与专家更新。后验诊断不进入正式判定。

### 结论

- **直接结果：**12/12 条件均合格。测试集 H-task−H-sem 在种子 17 为
  +0.010320 [0.009795, 0.010890]，在种子 29 为 -0.002078
  [-0.002469, -0.001680]；H-shuf−H-sem 在两个种子均为正。
- **正式判定：**`INSUFFICIENT`。真实标签优于打乱标签不能补足相对纯任务训练的种子
  反转；也不满足“同一必要比较在两个种子都反向”的局部不支持规则。
- **反转审计：**两个种子从开发集 128 步起方向相反并持续到 512，八个 checkpoint
  区间均不跨零。512 步的来源符号混合，80% 绝对贡献集中于种子 17 的两个来源和种子
  29 的三个来源，但任意删除一个来源都不改变最终汇总方向。
- **运行边界：**连续历史、同种子 H 初始张量、冻结与有限值检查、评估身份/词元数以及
  57 项 artifact hash 均通过；没有发现登记范围内的实现、恢复或评估异常。H-sem 的负载
  更均衡、辅助损失下降且父/子专家更新更大，这些只是候选原因，不能证明机制。

## 3. 当前认识与不能声称的内容

- **认识更新：**当前 0.5/0.5 语义监督在本设置下没有得到可复现的纯任务增量；反转并非
  只在最终 checkpoint 出现，也不是 512 步时由单一来源独自决定。
- **仍不能说：**不能说语义监督一般有效或无效，不能说监督过强已经被证明，不能把更
  均衡的负载当成任务收益，也不能证明教师标签是真实语义、层级结构必要、专家具有不可
  互换功能，或 NLL 结果能外推到自由生成与无污染公开基准。
- **未运行记账：**正式 H-hard/H-oracle 为 `NOT_RUN_NOT_TRIGGERED`。两步 H-hard smoke
  只验证代码路径，权重已丢弃，不是结果。

## 4. 唯一下一实验：语义监督强度配对定位

### 目的

只检验当前辅助监督权重是否过强，不同时引入额外种子、层位、教师、hard/oracle 或其他
机制。

### 假设

若种子反转主要来自 0.5/0.5 辅助目标压过任务优化，则较弱的 0.25/0.25 应在两个种子上
都比当前权重具有更低的 512 步开发集答案 NLL；纯任务臂用于判断减弱后是否仍保留任务
价值。竞争结果是减弱权重不能同时改善两个种子，说明“监督过强”不足以解释反转。

### 分析方法

在同一 H 架构、冻结教师、512 更新、load-off、种子 17/29、共同初始状态与数据顺序下，
配对运行三臂：H-task \((\lambda_p=\lambda_c=0)\)、H-sem-weak \((0.25,0.25)\)、当前 H-sem
\((0.5,0.5)\)。执行前须把 128/256/384/512 开发轨迹、512 步主比较和配对区间规则写入
新 Protocol。P3 测试集已经打开，只能作为旧结果，不能成为这次权重选择的新确认面。

### 结论分支

- **若 weak 在两个种子上都可靠优于 current：**保留“当前权重过强”为局部支持；再由
  H-task 比较判断较弱监督是否还具有任务增量，但不回写 P3 为成功。
- **若 weak 不能在两个种子上都优于 current：**停止“当前权重过强”解释，不持续增加
  权重档位或种子直到结果变正。
- **若实现或资格检查失败：**只修复并重跑受影响条件，不把缺失证据判成科学失败。

该分支已经由研究者给定的审计规则选中；上面的 0.25/0.25 精确实现与判据仍是 AI
形成的候选设计，尚未获得新 Protocol 的执行批准。本任务不启动后继训练。

## 5. 路径

- [P3 结果摘要](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/summary.md)
- [P3 完整证据](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/detailed.md)
- [P3 冻结协议](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/protocol.md)
- [Primary Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md)
- [P1 路径干预结果](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P1_coarse_path_intervention/summary.md)
- [P2 父路由修复结果](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P2_parent_router_supervision_repair/summary.md)

## 6. 唯一下一决策

确认或修改上述 0.25/0.25 三臂、两种子、开发集定位 Protocol；获得明确执行批准后才运行。
当前不追加种子，不开放 H-hard/H-oracle，不并行提出第二个机制实验。
