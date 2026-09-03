# 真实下一词元预测中，粗—细语义路由是否有功能价值？

```text
type: meeting_cycle_core_task
status: SUPERSEDED_BY_0903_GMM_PSEUDOLABEL_FOCUS
problem_key: A15.semantic_supervision_middle_layer_separability
focus_role: SECONDARY
conversation_owner: codex-thread:01a0652d-8c53-71e0-aab2-4008063e91a3
ownership_status: RELEASED
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
cycle_start: 2026-09-01
target_meeting: 2026-09-02
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_04_m2d2_causal_lm_semantic_routing_anchor.md
core_experiment_count: 3
```

## 1. 核心问题

在真实下一词元预测中，粗—细自然语言领域是否值得被分给不同专家：它是否比随机分组和不细分得到更低的留出词元损失，并使细专家形成不可互换的功能？

## 2. 本轮实验

### 实验 1：学习得到的语义 Router 能否恢复功能收益？

#### 目的

判断语义监督是否不仅让路由看起来更像领域标签，还能让预测 Router 降低留出下一词元损失并形成有用的细专家。

#### 假设

正确细领域监督应优于完全只靠下一词元损失学习的同架构 Router；最强竞争解释是监督只提高标签一致率，不提高语言建模或专家功能。

#### 分析方法

1. 三组都先学习并冻结正确粗领域 Router，再比较不加细标签、加入正确细标签和加入均衡打乱细标签的第二阶段。
2. 首先比较确认集每个目标词元的负对数似然，再看路由和细标签的一致程度；两者必须分开解释。
3. 删除当前预测选中的细专家或换成同粗类的其他细专家，判断学习到的专家是否真的不可互换。

#### 结论

**AI 核验的直接结果，等待研究者确认表述：**正确细语义监督把细 Router 的平均 NMI 从 `0.00646` 提高到 `0.12059`，并通过删除与错误替换干预；但确认集 NLL 比 task-only 更差 `0.001054`，反方向差值的 95% 区间为 `[0.000966, 0.001142]`，两个种子和九个细领域方向都一致。注册裁决为 `FAIL_NO_LEARNED_FUNCTION`：学会了更语义化的分发和不可互换的专家，但没有得到更好的整体下一词元预测。

### 实验 2：给定正确路径时，语义分组本身是否有价值？

#### 目的

去掉 Router 预测误差，直接判断粗—细语义分组在下一词元预测中是否比随机分组和不细分更有价值。

#### 假设

若细领域对应不同续写规律，正确路径应同时优于均衡随机路径和每个粗类只有一个细专家；最强竞争解释是任何额外容量都一样有效。

#### 分析方法

1. 三组从每个种子完全相同的粗阶段终点和细专家初始化出发，只改变细专家分组规则。
2. 用确认集词元负对数似然比较正确语义、均衡随机和不细分；领域等权，两个种子分别报告。
3. 对正确语义组执行当前细专家删除和同粗类错误专家替换，直接测试细专家能否互换。

#### 结论

**AI 核验的直接结果，等待研究者确认表述：**硬语义组相对较强控制的确认集 NLL 优势为 `0.001506 [0.001396, 0.001618]` nats/目标词元，两个种子均为正。删除当前细专家使 NLL 增加 `0.004691`，换成同粗类错误专家增加 `0.005355`，两个区间均完全大于零。注册裁决为 `PASS_SEMANTIC_FUNCTIONAL_VALUE_NTP`。该收益在九个细领域中有七个为正，在 Biology 和 Physical sciences 为负，因此是平均功能价值，不是普遍收益。

### 实验 3：简单基线与末层无监督伪标签能否把语义功能推进为实用方法？

#### 目的

判断层级语义 Router 在保持下一词元预测性能的同时，是否比单一适配器和平铺专家多得到可验证的语义分发与专家功能；并判断冻结模型最后一层生成的无监督伪标签能否替代人工领域标签。

#### 假设

若层级结构有独立价值，层级金标签或聚类伪标签模型应在留出 NLL 上不弱于简单基线，并在路由语义一致性和专家删除/换错干预上显示额外作用。最强竞争解释是语义指标变好只来自分类监督，而普通单适配器或平铺专家已经得到相同或更好的语言建模性能。

#### 分析方法

1. 复用实验 1 和实验 2 的全部检查点，只补训单一秩 24 适配器、秩 24 平铺叶专家、直接九类路由的层级专家，以及末层聚类伪标签层级专家。
2. 聚类只读取冻结 Qwen 最后一层的训练窗平均输出，在训练集拟合方向与模长的三乘三层级混合模型；真实领域标签不参与拟合、重启选择或训练，只用于确认集语义审计。
3. 先比较等领域留出 NLL，再分别比较路由与标签的一致性，以及删除或换错专家造成的 NLL 增量；三类证据不互相替代。

#### 结论

**AI 核验的直接结果，等待研究者确认表述：**两种子 full run 完整通过。末层方向加模长伪标签层级模型的确认集 NLL 为 `2.881270`，相对最强的新简单基线——平铺 task-only 模型——改善 `0.001841 [0.001684,0.002003]`，两个种子均为正；伪标签 Router 的细领域 NMI 为 `0.237`、匹配宏 F1 为 `0.336`，删除和换错当前细专家分别使 NLL 增加 `0.000932` 与 `0.000485`。注册裁决为 `PASS_PSEUDO_METHOD`。但它仍比复用的同类分阶段 task-only 层级模型差 `0.000903`，因此能说“无监督语义路由在保持简单基线性能的同时形成了额外语义和专家功能”，不能说“伪标签监督本身已经带来同架构 NLL 增益”。末层对角高斯聚类的确认集 NMI `0.524` 高于本次实际训练所用方向加模长聚类的 `0.444`，是否把更好的离线标签转成更好的因果路由仍需下一轮训练验证。详见 [Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E09_m2d2_baselines_last_layer_pseudolabel/summary.md) 和 [Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E09_m2d2_baselines_last_layer_pseudolabel/detailed.md)。

## 3. 数据、训练和边界

- 数据是 M2D2-Wikipedia 平衡 `3×3` 子集；输入不写粗类或细类名称。
- 每条序列 256 个词元；前 64 个只提供上下文，后 192 个计算标准下一词元交叉熵。
- Qwen3-0.6B-Base 和原语言头冻结；只训练 block 14 新增的 Router、共享/粗/细 LoRA 专家。
- Router 在每个预测位置只读取当前及以前的中间状态。未中心化输入是主设置。
- 即使路由语义指标为正，也不能代替留出词元损失和专家干预；即使 Oracle 通过，也不能声称学习 Router 已经可部署。

## 4. 路径

- [Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_04_m2d2_causal_lm_semantic_routing_anchor.md)
- [学习 Router 协议](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E07_m2d2_learned_semantic_router_ntp/protocol.md)
- [强制 Oracle 协议](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E08_m2d2_hard_semantic_route_ntp/protocol.md)
- [学习 Router 结果](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E07_m2d2_learned_semantic_router_ntp/summary.md)
- [硬 Oracle 结果](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E08_m2d2_hard_semantic_route_ntp/summary.md)
- [基线与末层聚类伪标签协议](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E09_m2d2_baselines_last_layer_pseudolabel/protocol.md)

## 5. 核心任务卡总结论

- **我的认识更新：**等待研究者确认：M2D2 的粗—细语义分组在给定正确路径时具有小而稳定的平均下一词元功能价值；当前学习 Router 虽然学到了语义分发和专家功能，却没有恢复这部分任务收益。
- **仍不能说：**不能说语义分组对所有领域都好，不能把学习失败只归因于路由准确率，也不能说冻结 Base 的原生表征被重塑。
- **唯一下一决策：**不重新训练，先把预测/正确专家索引与概率/单位专家系数做 `2×2` 交叉评估，定位 Oracle 收益丢在选错专家、概率衰减，还是训练责任分配。

### 冻结后续诊断：学习 Router 的 Oracle 收益丢在哪里？

#### 目的

不重新训练，只用 E07 两个学习语义检查点，区分收益损失来自专家选择、概率缩放，还是已训练专家本身。

#### 假设

如果错误主要来自路由决策，改用正确专家索引或把专家系数固定为一应恢复大部分 NLL；最强竞争解释是即使正确索引与单位系数同时使用，学习专家仍达不到 task-only 或硬 Oracle。

#### 分析方法

1. 交叉评估预测/正确专家索引与学习概率/单位系数四个前向单元，所有模型参数、确认数据和检查点完全不变。
2. 用配对确认集 NLL 将总恢复量精确分给索引和系数，并报告两者交互；再与既有 task-only 和硬 Oracle 比较剩余差距。
3. 在四个单元重复删除与同父类换错细专家，确认前向修复没有把专家功能证据变成纯路由标签效果。

#### 结论

执行前分支已由研究者确认：索引贡献更大则下一轮优先修复选路；系数贡献更大则优先取消概率缩放；两者同时不足以达到 task-only 或硬 Oracle，则下一轮必须改专家责任分配或训练目标，而不能只改 Router 推理。
