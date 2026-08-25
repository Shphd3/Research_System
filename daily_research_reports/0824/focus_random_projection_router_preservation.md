---
status: E03_COMPUTATION_COMPLETE_AWAITING_HUMAN_RESULT_AND_H1_REVIEW
cycle_start: 2026-08-24
target_meeting: 2026-08-25
project: from-attention-to-search
anchor: ../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md
protocol: ../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E03_native_router_representation_controls/protocol.md
predecessor_protocol: ../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/protocol.md
approval_source: user explicitly approved the native Router-input and adjacent-layer-difference design and directly authorized execution
---

# 0824 核心任务：区分残差失败与原生 Router 表征边界

## 1. Core question

E02 已经表明新定义的更新残差 $R_U$ 含有条件新增信息，但不能单独形成跨模板正低尾间隔。现在要判断：这个负结果只属于 $R_U$ 的构造，还是连 Qwen3-30B-A3B 真正送入 MoE gate 的原生路由表征及其相邻层变化也没有稳定线性类别信息？

这里“原生路由表征”是每层 post-attention RMSNorm 后、直接送入该层 MoE `gate` 的 hidden state；“相邻层变化”是当前层原生路由表征减去上一层原生路由表征。线性可读不等于模型 gate 实际使用该类别，更不等于真实专家效用。

## 2. Experiment purpose, subquestions, and completion standard

1. 沿用 E02 已审计的 19,200 行数据、最后一个 `Answer:` token、8 个 parent labels 和冻结划分，不重新生成数据，不再次抽取模型表征。
2. 从 E02 已验证的 $(X_\ell,U_\ell)$ 构造原生路由输入 $G_\ell=X_\ell+U_\ell$，以及 $\Delta G_\ell=G_\ell-G_{\ell-1}$；分别画 TRAIN 类内/类间方差逐层曲线。
3. 对两种表征分别用 TRAIN 拟合、DEV 选层，在冻结层上给出 same-template 与 new-template TEST 的五种子线性分类准确率和置信区间。

完成标准：两个表征各有完整逐层方差表、类内/类间方差图、DEV 准确率曲线、冻结选层回执和两面板 TEST 准确率；机器守卫、`summary.md`、`detailed.md` 和两份 `docs/` 简报齐全。E02 的 $R_U$ 结果和理论文件保持不变。

## 3. Analysis method

1. 用 E02 的哈希和 identity receipt 验证 $G_\ell=X_\ell+U_\ell$ 确实对应模型原生 MoE 输入，并明确 $\Delta G_1$ 未定义。
2. 仅在 TRAIN 计算按维度归一化的类内、类间方差；用 GPU ridge probe 扫描所有合法层，并只按 DEV balanced accuracy 冻结每种表征的一个确认层。
3. 在冻结层复用五种子 L2 multinomial-logistic probe 和标签置换控制，最后读取两个 TEST 面板并输出准确率及 95% 区间。

## 4. Conclusion

### Before E03 execution: registered branches

- 若 $G$ 或 $\Delta G$ 在两个 TEST 面板都稳定高于随机水平：E02 的负结论必须限定为“$R_U$ 单独不可稳健路由”，不能扩展到模型的整个路由输入空间；下一步再决定应学习新表征还是直接利用原生状态。
- 若两种表征也不能跨模板稳定高于随机水平：当前负证据覆盖范围扩大到三个已注册线性表征，但仍不能证明 gate 没有其他任务相关信息，也不能替代专家效用检验。

### After E03 execution: human-owned result

- Direct result: `[E03 COMPUTATION COMPLETE; AWAITING HUMAN RESULT WORDING; E02 evidence remains immutable]`
- Updated judgment: `[AWAITING_HUMAN_RESULT]`
- Cannot claim: 随机投影创造语义结构；分类标签等于专家效用；probe 失败证明所有线性子空间不存在。
- Next decision: `[AWAITING_HUMAN_RESULT]`
