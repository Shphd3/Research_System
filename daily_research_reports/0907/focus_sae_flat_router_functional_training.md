# 最后一层 SAE 扁平分组能否带来可验证的专家功能收益？

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: A15.sae_hierarchical_teacher_construction
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: AWAITING_HUMAN_CONFIRMATION
cycle_start: 2026-09-07
target_meeting: 2026-09-08
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_10_sae_flat_router_functional_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/protocol.md
source_meeting: USER_CONFIRMATION_2026-09-07
core_experiment_count: 1
```

## 1. 核心问题

冻结的最后一层 SAE 在八任务训练数据上形成八组共激活特征后，这个固定扁平路由是否能让低秩专家获得随机特征分组和纯任务路由不能稳定复现的答案预测收益？本轮只回答一个最后层、八专家设置中的功能问题，不选择最优层或专家数。

## 2. 本轮实验

**本轮不回答：**这些分组是否是真实语义类别、内部留出分数是否是官方基准成绩，以及更深、更浅或更多专家是否更好。

### 实验 1：五条件配对的最后层扁平专家训练

#### 目的

把 SAE 可读结构推进到功能检验：确认其冻结路由能否降低答案词元损失，并用随机 SAE 分组、提示状态 GMM、纯任务路由和秩16稠密适配器排除分组偶然性、旧离线聚类族、一般路由能力和参数量解释。

#### 假设

若共激活 SAE 分组提供任务相关结构，SAE 条件应在三个种子中稳定优于频率匹配随机分组，并进一步优于纯任务路由。最强竞争解释是分组虽稳定但没有功能价值；此时 SAE 不会稳定胜过随机分组，或任何变化都可由共享适配器和一般训练解释。

#### 分析方法

1. 先审计八任务数据身份、题目级与截断后泄漏，再只用训练记录的互斥两半完成 SAE/GMM 分组和离线路由；验证集只选择路由正则，内部测试在模型冻结后才打开。
2. 对 SAE、随机特征、GMM、纯任务路由和稠密秩16五个条件使用种子17/29/43及完全配对的512次更新，比较更新0/128/256/384/512的答案损失和固定更新512的逐任务结果。
3. 以每种子、逐记录配对的答案词元损失为主证据，并用 SAE/GMM 专家选择置乱和专家更新矩阵诊断区分路由依赖、任务收益与参数几何；后两者不能替代任务收益。

#### 结论

**直接结果：**工程资格在 prompt-only 层次 GMM 处失败。父组收敛为
`[5724, 13697, 363]`，前两个父组的三个子组均非空，最小父组要求的
两个子组却为 `[363, 0]`；固定 GMM 对照只有七个占用叶组，不能构造
批准的八专家条件。

**有界结论：**流程按预注册规则停止；没有拟合离线路由，没有完成
五条件单步 smoke，也没有提交正式训练。因此这不是 SAE 功能成败结果，
不能比较 SAE、随机分组、GMM 或 task-only，更没有八任务内部成绩。

**对 Focus 的影响：**原“完整结果是否支持 SAE 功能收益”的决策尚未被
回答。研究者已澄清 GMM 不应有父层，并批准修订为 PCA-64 后直接拟合一个
八成分对角 GMM；其余条件、随机种子、指标与判定规则不变。已通过的数据
与激活缓存只可在精确哈希复验后复用，旧层次 GMM 及其下游均不可复用。

## 3. 核心任务卡总结论

- **我的认识更新：**首次数据与缓存资格通过，但旧层次 GMM 的最小父组子模型塌缩为 `[363, 0]`；研究者随后确认应使用无父层、直接八组的平坦 GMM，正式训练仍未启动。
- **仍不能说：**尚不能声称 SAE 路由有任务收益或专家功能。
- **唯一下一决策：**完成修订后的全套资格检查；仅在八组 GMM、分组审计、九个离线路由器和五条件真实 GPU smoke 全部通过时提交已批准的完整训练，任一门失败即停止且不再自动改设计。

## 路径

- **实验协议：**[E20 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/protocol.md)
- **结果摘要：**[E20 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/summary.md)
- **完整证据：**[E20 Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/detailed.md)
- **每日研究报告：**NOT_YET_WRITTEN
- **待研究问题清单：**[Parking Lot](../../Projects/from-attention-to-search/main/parking_lot/README.md)
