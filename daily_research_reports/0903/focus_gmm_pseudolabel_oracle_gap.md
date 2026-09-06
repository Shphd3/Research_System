# 真实粗细语义分别从哪一层开始稳定可读？

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: A15.gold_label_layerwise_static_audit
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: AWAITING_HUMAN_CONFIRMATION
cycle_start: 2026-09-03
target_meeting: 2026-09-04
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_07_true_label_layerwise_static_audit_anchor.md
core_experiment_count: 1
```

## 1. 核心问题

在冻结的 Qwen3-0.6B-Base 中，M2D2 的真实粗领域和已知真实父领域后的细领域分别从哪一层开始，能够被相同容量、与部署形式相符的分类器稳定读取？

本轮只审核表示中有没有可读信息。它不证明模型原生使用该信息，不证明在线路由已经可用，也不证明在候选层加入专家会提高下一词元任务。

## 2. 本轮实验

### 实验 1：真实粗细标签的逐层静态审计

#### 1. 目的

使用最稳固的真实粗细语义标签，找到粗语义和细语义首次稳定成为路由器可读信息的层，为后续粗细 Oracle LoRA 专家插层实验提供候选位置。

#### 2. 假设

粗领域信息应当比父类内部的细领域信息更早达到稳定可读，因此应得到粗候选层早于细候选层。最强竞争解释是二者同时出现、只有非线性分类器能读取、候选依赖大量样本或特定词元位置、粗类只是记住已见子类，或所有层都没有稳定线性结果。

#### 3. 分析方法

1. 冻结与 E14 完全相同的 Qwen3-0.6B-Base 和 M2D2 `3×3` 数据，在全部 28 个 Transformer 块只读取未来 LoRA Router 真正接收的当前词元 MLP 调用前表示；不分析其他表征，不更新基座、语言头或加入 LoRA。
2. 每层以同容量线性分类器为主判据，并在同一输入上增加固定小型非线性分类器、分层嵌套样本效率曲线、Fisher 判别强度和粗细判别子空间夹角，从而区分线性可路由、非线性折叠、样本难学和粗细方向关系。
3. 在真实父类条件下做细分类，并增加三个词元位置区间、粗类留一子类泛化、窗口级标签打乱和 2,000 次分层窗口重采样；开发集冻结候选规则后，确认集只评估一次。

#### 4. 结论

1. **直接结果：**开发集与确认集的线性粗、细首次稳定层均为 `(9,9)`；2,000 次窗口重采样的层差区间均为 `[0,0]`，细层至少晚两层的概率均为 `0.0%`。未经资格门否定时，这不支持错层插入。
2. **稳健性：**三个词元位置区间全部仍选第 9 层；粗分类需要 25% 训练窗口、细分类需要 50%；粗分类在三个留一子类折中都没有稳定层。因此细分类样本脆弱，粗分类依赖已见子类身份。
3. **正式裁决：**`UNQUALIFIED_SHUFFLE_CONTROL`。确认集条件细分类的打乱标签中位交叉熵为 `1.148744`，比预注册上界 `1.148612` 高 `0.000132`；准确率接近随机且没有稳定层，但硬资格门仍失败。第 9 层只能登记为描述性的同层候选，不能送入 LoRA 验证。
4. **不能声称：**本实验只观察表示可读性；没有验证在线路由、专家功能或下一词元收益。

## 3. 前置证据与冻结边界

- E14 的历史结果保持不变：正确真实路径在受控八任务答案损失上优于同拓扑 task-only，但当前伪标签与因果 Router 没有缩小 Oracle 差距。E15 不覆盖、重算或加强该结论。
- E15 不训练稀疏自编码器，不生成伪标签，不更新基座或语言头，不训练 LoRA 专家，也不测量下一词元任务收益。
- 2026-09-03 的旧作业 `om-kpp7frgn` 在 0 副本、未执行代码时停止；没有通过的冒烟、checkpoint、开发集或确认集结果。
- 修订方法已由研究者确认。新的冒烟与全量计算只使用单节点 `1×H100 SPOT`；不得回退到保留资源、5090 或其他 GPU 数量。
- 开发集负责选择层；规则冻结后，确认集只读取一次。不得依据中间结果删层、改阈值、改主指标或选择更好看的种子。
- 本实验只审核未来 LoRA Router 的当前词元 MLP 调用前输入；其他表征对象不进入本轮结果。

## 4. 唯一下一决策

请研究者决定：是否授权用一个全新种子原样复现本静态审计，以裁定 `0.000132` nat 的空对照越界。复现通过并重现 `(9,9)` 前，不进入匹配预算的 Oracle LoRA 验证。

## 5. 路径

- [E15 Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_07_true_label_layerwise_static_audit_anchor.md)
- [E15 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E15_true_label_layerwise_static_audit/protocol.md)
- [E15 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E15_true_label_layerwise_static_audit/summary.md)
- [E15 Detailed evidence](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E15_true_label_layerwise_static_audit/detailed.md)
- [E14 preserved predecessor](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_gmm_pseudolabel_oracle_gap/summary.md)
