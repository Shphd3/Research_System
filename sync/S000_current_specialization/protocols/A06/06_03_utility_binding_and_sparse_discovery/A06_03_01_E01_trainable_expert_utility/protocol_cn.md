# 实验协议：A06_03_01_E01 上下文任务上的可训练专家功能绑定

## 0. 审核摘要

**状态：** 依据持续研究目标，于 2026-07-10 批准执行。

**目的：** 检验正确路由暴露能否在测试集上制造任务特定的 expert function，而不是只保持几何路由身份。

**主 anchor：** `../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/subanchors/06_03_01_trainable_expert_utility_binding_anchor.md`

**唯一问题：** 正确暴露是否产生超过负载匹配身份打乱控制的正反事实功能绑定差？

**主指标：** 冻结表征、只训练 expert 时，测试任务位置上的

$$
G_f^{cf}=\min_{b\ne a(f)}(L_{f,b}^{cf}-L_{f,a(f)}^{cf}).
$$

**最小设置：** 四种等频序列级变换指令；一层无位置因果 Transformer；四个相同初始化的可训练 MLP experts；暴露阶段固定 oracle route；全序列 LM loss；不同 content 顺序的测试集。

**条件：** 正确的 expert-only 暴露；负载匹配打乱的 expert-only 暴露；正确的 expert+representation 共同暴露；对应的打乱共同暴露；step-0 baseline。

**通过：** expert-only 正确暴露中至少 90% 的 feature-seed 单元 $G_f^{cf}>0$，且正确减打乱配对中位差的 seed-clustered 95% 置信区间下界大于 0；所有有效性 guard 通过。

**失败：** 任务可学习且控制有效，但正确与打乱 expert-only 暴露的测试功能差不可区分。

**证据不足：** seeds 少于 32、更新次数不匹配、train/test 重合、任务不可学、反事实状态改变或 route/full-LM guard 失败。

**不能声称：** 自然语言语义专家、无标签路由、真实下游收益、长上下文 scaling 或可部署 gating。

## 1. 术语解释

| 术语 | 具体含义 | 计算 | 为什么重要 | 不能证明什么 |
| --- | --- | --- | --- | --- |
| 上下文任务 | 序列开头的 instruction 决定后续 token 输出 | 模 4 变换 $f$ | 超越 token identity | 自然语义 |
| 任务位置 | content token 后预测 instruction-dependent output | 每序列 16 个位置 | 隔离条件算子 | 全 LM 质量 |
| 正确暴露 | 任务 $f$ 始终更新 expert $f$ | identity permutation | 形成稳定条件更新 | 可部署路由 |
| 平衡打乱 | task-expert mapping 按四个 offset 循环 | $a_t(f)=(f+t)\bmod4$ | 完全匹配 load/count | 排除所有真实混杂 |
| 反事实损失 | 固定其他组件，强制使用 expert $e$ | $L_{f,e}^{cf}$ | 直接比较 expert function | 长期稳定 |
| 功能绑定差 | 指定 expert 相对最佳竞争 expert 的 loss 优势 | $G_f^{cf}$，nats/token | 主裁定指标 | 自然语义 specialization |
| 绑定时间 | 正确减打乱的配对中位差从该 checkpoint 起持续为正 | $T_{bind}$，updates | 受控训练效率 | 系统 wall-clock 效率 |
| 路由压力 | 一步 task-loss gradient 预测的 margin movement | $-\langle g_a-g_b,\mu_f\rangle$ | utility 是否反馈到 gate | 长期收敛 |

## 2. 数据、模型与训练

- 四个 instruction tokens、四个 content tokens、四个 output tokens。
- instruction $f$ 把 content $c$ 映射为 output $(c+f)\bmod4$。
- 一个 instruction token 后接 16 组 content/output pairs；长度 33；全部 32 个 next-token positions 进入 LM loss。
- 每个 seed 有 32 条训练序列和 32 条测试序列，每项任务各 8 条，content 顺序不重合。
- 模型：hidden 64、四头一层因果 attention、residual、LayerNorm、四个 hidden width 128 的同初始化 MLP experts、固定 readout、无可学习位置嵌入。
- 在 LayerNorm 前把序列 instruction embedding 以 strength 1.0 固定广播到每个位置，作为上下文可见性的 known-good control；它不是新 gate。
- 暴露 200 步；checkpoints 为 0、10、25、50、100、200。
- expert AdamW learning rate 0.001；representation learning rate 0.0005；32 seeds。

## 3. 因果对照

| 条件 | 训练对象 | task-expert mapping | 作用 |
| --- | --- | --- | --- |
| 正确 expert-only | experts | 固定 identity | 主因果条件 |
| 打乱 expert-only | experts | 四个 offset 平衡循环 | load/count 负控制 |
| 正确 joint | experts + representation | 固定 identity | 共同训练迁移检查 |
| 打乱 joint | experts + representation | 平衡循环 | representation-only 解释控制 |
| step-0 | 无 | experts 完全相同 | 指标与初始化 guard |

## 4. 主要判定

对每个 seed、task、condition、checkpoint，固定非 expert 组件并逐个强制 expert，计算测试任务位置的 $L_{f,e}^{cf}$ 与 $G_f^{cf}$。

主判定只使用最终 expert-only 条件：

1. 正确暴露正 gap 单元比例；
2. 同 seed/task 下正确减打乱的配对 gap；
3. 按 seed 聚类 bootstrap 的配对中位差 95% 置信区间。

通过要求正 gap 比例不低于 0.90 且置信区间下界大于 0。只有正 gap、但不超过打乱控制，不能作为功能绑定证据。

## 5. 次指标与有效性

- $T_{bind}$ 与 gap trajectory 面积。
- 测试 task loss 和 all-position LM loss。
- task-by-expert 反事实 loss matrix。
- task gradient 与 full-LM gradient 的 router pressure。
- route NMI、低尾 margin、expert update-count parity。
- 表征冻结条件的 non-expert state exact equality。
- train/test sequence overlap count。

## 6. 核心图

1. **测试功能差轨迹：** 横轴 updates，纵轴 median $G_f^{cf}$；回答正确暴露是否更快形成 utility。
2. **最终反事实 loss matrix：** 行是 task，列是 forced expert；回答指定对角线是否功能更好。
3. **utility 到 router pressure：** 横轴 $G_f^{cf}$，纵轴 margin pressure；回答学到的功能差是否传递给 gate。

## 7. 结论边界与下一步

若通过，A06_03_01_E02 应在同一上下文算子任务上取消 oracle exposure，检验 learned routing、expert utility 与 route identity 是否在 full joint training 中共同稳定。若失败，先用已知可用 context-state control 区分表示不可见与 expert capacity 不足，不直接发明新 gate。

## 8. run 01 有效性失败与修订

`a06_38_full_4gpu_20260710_01` 完成了 32 seeds，但最小 native 初始 route NMI 为 0.9198，违反“给定正确可读 partition”的 guard。其 utility 结果只保留为无效运行诊断，不进入结论。run 02 只加入固定 instruction-state broadcast；问题、条件、指标、阈值、optimizer 和 seed 数不变。
