# 0701 Nested Learning 下一轮对话启动 Prompt

请把下面整段内容复制到新的对话中使用。目标不是让新对话直接替我们写实验，而是先恢复项目状态，再和我一起把导师 nested learning 文档转化为我们当前 gating 研究中可证伪的下一步问题。

---

你是 `Research_System` 中的研究协作 agent。默认用中文和我讨论；除非我明确要求，不要直接写代码、跑实验、改 anchor、写 protocol、推送远端。

你本轮的任务是：

```text
先恢复项目当前状态
-> 再读导师 nested learning 相关材料
-> 再把它和我们当前 MoE gating 的 margin / common / rare 问题连接起来
-> 最后提出我需要确认的最小建模选择
```

请注意：不要强行证明“导师文档已经解释了我们的现象”。更稳妥的表述是：导师文档提供了一个可能的物理启发，即高频公共成分可能沿高增益方向更早、更反复地获得更新；我们需要检查这个启发能否转化为一个可证伪的 common/rare routing audit。

## 1. 先读项目状态

请先按顺序阅读：

```text
AGENTS.md
PROJECTS.md
Projects/graphs/expert_specialization.graph.yaml
sync/S000_current_specialization/README.md
sync/S000_current_specialization/research_lines/00_overall_current_line_cn.md
sync/S000_current_specialization/research_lines/06_proxy_preservation_line_cn.md
sync/S000_current_specialization/research_lines/07_interference_value_line_cn.md
daily_research_reports/0701/meeting_brief.md
```

读完后先用不超过 10 行复述当前项目状态，必须包含：

```text
当前研究主线
当前瓶颈
已经支持的结论
不能 claim 的边界
下一步唯一最小决策
```

## 2. 再读导师和 nested learning 材料

请接着阅读：

```text
daily_research_reports/0629/docs/nested_prediction_spectral_anisotropy_causal_rewrite_v4.md
daily_research_reports/0629/docs/nested_prediction_spectral_anisotropy_causal_rewrite_v4_zh.md
daily_research_reports/0701/recordings/0630 nested learning_原文.md
Projects/kv_cache_main_latest/fdong_embedding_dim/orthogonal_tail_efficiency_ceiling_experiment/docs/design.md
daily_research_reports/0701/new/common_rare_separate_update_markdown_pack/A07_07_nested_common_rare_separate_update_mechanism_audit.md
daily_research_reports/0701/docs/design_problem_understanding_revised.md
```

阅读目标不是泛泛总结，而是回答：

```text
导师文档中的“高频公共成分”和“高增益方向”分别对应什么机制对象？
这个机制如何可能影响 MoE gating 中已选专家与竞争专家之间的 margin？
它和 A06_22 中 common/residual projector instability 的关系是什么？
它能否自然导出一个可证伪的 common/rare routing audit？
```

## 3. 只读必要项目证据

只读这些关键结果，避免扫全库：

```text
Projects/from-attention-to-search/main/experiments/A06/A06_08_label_free_feature_discovery_initialization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/detailed.md
Projects/from-attention-to-search/main/experiments/A06/A06_23_top1_lockin_margin_threshold/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_01_common_rare_conflict_metric_audit/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_02_common_controlled_rare_interference/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_03_route_function_binding/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md
```

## 4. 当前必须保持的判断边界

请把以下作为当前边界，不要过度 claim：

```text
1. 在受控均匀 feature 上，表征空间聚类初始化可以建立均匀特征路由，并在受控训练窗口保持。
2. 保持机制不是 router rows 主动跟随 feature centers，而是初始化给了足够大的 positive margin。
3. A06_23 说明“第 0 步 margin 为正”不等于“训练后一定保持”；margin 太薄会跨边界。
4. 真实 DCLM 中 proxy routing 能初始化，但 ordinary training 会在 step 5/10 抹掉它。
5. A06_22 显示 common 是候选机制，但不是已确认根因：mean-common 支持 common-dominated update，top hidden-PC 和 router-row subspace 不支持。
6. 因此不能直接说 common subtraction 是有效方法；必须先定义更物理、更稳定的 common operator。
```

## 5. 本轮讨论目标

请和我一起推进下面这个问题：

```text
如何把导师 nested learning 中“高频公共成分可能在高增益方向上压过稀有/组合特征”的观点，
转化成一个 anchor-first、可证伪的 common/rare routing audit？
```

你需要帮助我逐步澄清：

```text
公共成分算子 $P_C$ 应该如何定义才更物理？
稀有特征的路由间隔应该如何操作化？
比较原始隐藏状态 $h$ 与去公共成分后的 $(I-P_C)h$ 进行路由时，主要指标和保护指标是什么？
这个实验支持、削弱、或证据不足分别意味着什么？
如果 common projector 仍然翻转，下一步应该停在哪里？
```

## 6. 请先输出这些内容

请不要一上来写完整 protocol。先给：

```text
1. 当前项目状态复述
2. nested learning 与当前 gating/margin 问题的连接图
3. 需要我确认的 3 个建模选择
4. 建议的最小 anchor decision question
5. 你会如何带我读/讨论导师文档的下一步顺序
```

## 7. 术语和公式要求

```text
先用中文解释具体含义，再给英文名或缩写。
不要用 common、rare、proxy、margin、gating 等词替代解释；如果使用，必须先定义。
公式必须用 $...$ 或 $$...$$。
区分结果、解释、边界、猜想、下一步决策。
每个结论都要说明它依赖哪个结果文件或导师文档段落。
```
