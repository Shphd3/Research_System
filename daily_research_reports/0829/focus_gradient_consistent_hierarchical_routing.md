# 共同成分之后的效用残差，能否被 1→2→4 MoE 更高效地路由？

```text
type: meeting_cycle_core_task
status: HUMAN_RESULT_CONFIRMED
problem_key: A15.counterfactual_utility_residual_expert_growth
focus_role: SECONDARY
conversation_owner: UNCLAIMED
ownership_status: RELEASED
core_question: AI_FORMALIZATION_AUTHORIZED_BY_HUMAN_SCOPE
plain_language_design: AI_FORMALIZATION_AUTHORIZED_BY_HUMAN_SCOPE
cycle_start: 2026-08-29
target_meeting: 2026-08-30
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01_qwen_native_router_access_gap/protocol.md; Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03_counterfactual_utility_residual_tree/protocol.md
resource_profile: one SPOT worker with exactly 8xRTX5090; H100 is prohibited
h100_sensitivity: accepted as collision-isolated non-owning evidence under the current Focus; not an execution of the 8xRTX5090 contract
superseded_protocol: Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E02_synthetic_parent_first_moe/protocol.md
source_meeting: daily_research_reports/0825/docs/0824_gating_会议记录_逐句校订与证明任务.md; daily_research_reports/0828/docs/0828组会_逐句校订与下一步研究方向.md
core_experiment_count: 2
```

## 1. 核心问题

“语义可分”是预先给定标签能否被读出；“效用可分”是同一个样本交给不同等算力专家时，哪位专家真正降低任务损失的排序能否被读出；“Router 使用”是原生 Gate 是否据此选择；“功能收益”是模型是否以更少样本或相同预算得到更低测试误差。这四层不能互换。

本轮唯一问题是：**先学习并冻结一个共同的 rank-1 函数，再只对它未解释的功能残差进行 $1\rightarrow2\rightarrow4$ 递归专家训练，是否仅在给定父类分组与反事实专家效用分组一致时，才把全局非线性的效用决策变成分支内的线性决策并提高训练效率；直接用反事实专家效用监督 Router，能否在相同结构和计算下提供额外收益？**

## 2. 实验目的

本轮依赖顺序上的四个子问题是：

1. 固定线性映射、可学习非线性映射、余弦 Router 和 common 残差化分别能与不能改变哪一种可分性？
2. 在冻结 Qwen3-30B-A3B 中，八类父语义从真实 MoE 输入 $H$ 到 128 维原生 Gate logits $Z$、再到 top-8 稀疏路由 $Q$ 时，跨模板线性访问性在哪里损失？
3. 在四叶合成任务中，导师提出的“一个 common、冻结、两个 specialized、冻结、四个 leaves、始终在函数/梯度残差上学习”能否实现其可证明的 work 情形，并在等价重配的 fail 情形出现可证明的 rank-1 容量下界？
4. 在相同 7 个专家、初始化、样本流、阶段预算、Gate 参数和全候选前向计算下，效用监督相对 task-only 的收益、条件树相对 flat nonlinear 的收益，是否能分别成立？

完成标准是：理论给出可复核命题与反例；Qwen 的五个确认层、C4/C5、A/B 双向模板划分产生合格结果；合成实验的八个配对种子全部完成，解析 oracle、rank/freeze/mask/计算护栏通过，并分别给出机制、效用监督和层级收益裁定。

**本轮不回答：**真实 Qwen 专家效用、Qwen 预训练的梯度历史、自然语义树能否无监督发现、真实语言模型重训 NLL、或任意任务都适合删除 common 参数方向。

## 3. 分析方法

1. 先证明三条边界：线性映射不能创造线性可分性；X-MoE 式余弦 top-$k$ 的选择边界仍是线性的；语义可分不推出反事实专家效用可分。再证明错误父类树为何必须把两个正交 rank-1 残差塞进一个 rank-1 叶专家，从而产生 $1/3$ 归一化误差下界。
2. 冻结 Qwen，只比较同一隐藏状态沿原生 $H\rightarrow Z\rightarrow Q$ 链的八类父语义跨模板读出、校准、保留率和匹配标签置换空参照；不把结果称为专家效用。
3. 合成任务用同一组四个教师函数的 work/fail 双射重配，并运行“条件树/平坦非线性”乘以“任务损失/反事实效用”的 $2\times2$。以测试误差学习曲线面积、固定预算误差、效用遗憾和归一化低尾 margin 分别裁定训练效率、功能、路由与表征。

## 4. 结论

### 执行前：两种预期结果

- **若支持：**解析 oracle 与所有实现护栏先通过；导师树在 work 收敛而在 fail 保留理论误差地板；效用监督相对同架构 task-only 降低学习曲线面积；且只有在 `H_util` 胜过同效用监督的 `F_util` 时，才增加“层级归纳偏置有额外训练效率”这一结论。Qwen 审计只报告语义访问接口，不参与合成因果结论。
- **若不支持或证据不足：**若 `F_util` 追平或胜过 `H_util`，则结论收缩为“效用监督或通用非线性已经充分”；若 work 树也学不出来，则由 oracle、效用遗憾、负载、rank 与 freeze 记录定位为 Router 优化、专家估计或实现失败；若 fail 树突破 $1/3$ 理论地板，则判定 mask/rank/freeze 泄漏，整个合成证据无效，而不是把它当成方法成功。

### 执行后：研究者已确认

- **直接结果：**8×RTX5090 的完整证据链通过。Qwen 审计表明，父类标签从隐藏输入到 128 维原生 Gate 投影基本保留，但在 top-8 稀疏选择处损失 0.434--0.567 的平衡准确率；稀疏路由仍高于匹配标签置换的关联空参照。合成实验中，task-only 条件树在 work 的八种子中位终点 NMSE 为 $2.30\times10^{-5}$，在 fail 为 0.33698，并保留解析 $1/3$ 下界；同一树加入逐样本瞬时反事实效用监督后，work 中位终点变为 0.41693，7/8 种子未到近零解。平坦非线性对照在 work/fail 均能到近零。研究者同时接纳 4×H100 的 E01H/E03H 为碰撞隔离敏感性证据：它复现同一质性边界，但不是本 Focus 的 H100 执行，也不产生第二个下一决策。
- **我的结论：**正确层级提供了可解释、可证明的条件函数分解；本轮证据不支持把“可分解”升级为相对通用非线性模型的训练效率优势，也不支持当前逐样本在线反事实效用监督。
- **仍不能说：**不能据此声称 Qwen 原生 Router 因果使用父类语义、所选专家具有反事实效用、真实语言模型损失会改善、自然语义具有该四叶树、模型会自动发现该树，或其他稳定化效用目标必然失败。
- **唯一下一决策：**停止推广当前残差树与在线效用目标；下一周期只裁定“父类相关预测事件频率是否足够，还是必须同时有跨细类不抵消的梯度一致性，才形成未见模板上的父类判别方向”。完成标准是冻结一个频率（高/低）乘以跨细类梯度一致性（高/低）的 $2\times2$ 下一词元预测设计，并让四格在总 token、总目标位置、父细类样本数、词表、模板和标签熵上匹配；返回梯度一致性、父类类间能量、5% 低尾归一化间隔和判别子空间谱位置。该判断只授权 Anchor/Protocol 设计，不授权实现或运行。

## 路径

- **Thinking Card：**[15_11_gradient_consistent_hierarchical_routing_thinking_card_cn.md](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_thinking_card_cn.md)
- **Anchor：**[15_11_gradient_consistent_hierarchical_routing_anchor.md](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md)
- **Qwen Protocol：**[A15_11_E01 protocol.md](../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01_qwen_native_router_access_gap/protocol.md)
- **Synthetic Protocol：**[A15_11_E03 protocol.md](../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03_counterfactual_utility_residual_tree/protocol.md)
- **Superseded E02：**[historical protocol.md](../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E02_synthetic_parent_first_moe/protocol.md)
- **Qwen Summary / Detailed：**[Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01_qwen_native_router_access_gap/summary.md) / [Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01_qwen_native_router_access_gap/detailed.md)
- **Synthetic Summary / Detailed：**[Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03_counterfactual_utility_residual_tree/summary.md) / [Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03_counterfactual_utility_residual_tree/detailed.md)
- **H100 sensitivity Qwen Summary / Detailed：**[Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01H_qwen_native_router_access_gap_h100/summary.md) / [Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01H_qwen_native_router_access_gap_h100/detailed.md)
- **H100 sensitivity Synthetic Summary / Detailed：**[Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/summary.md) / [Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/detailed.md)
- **Daily Report：**[H100 sensitivity daily report](docs/gradient_consistent_hierarchical_routing_h100/daily_report_gradient_consistent_hierarchical_routing_h100.md)，状态为 `HUMAN_CONFIRMED`
- **H100 研究材料包：**[README](docs/gradient_consistent_hierarchical_routing_h100/README.md)
- **当前唯一汇报版本：**[focus_meeting_gradient_consistent_hierarchical_routing_h100.md](docs/gradient_consistent_hierarchical_routing_h100/focus_meeting_gradient_consistent_hierarchical_routing_h100.md)，研究结果与日报均已确认
- **被取代的组会草稿：**[superseded_focus_meeting_pre_h100.md](docs/gradient_consistent_hierarchical_routing_h100/superseded_focus_meeting_pre_h100.md)，仅保留历史决策轨迹
