# A14 状态—参数验证与实验路径 TODO

> 日记录用途：帮助审核执行顺序，不替代 canonical anchor 或 protocol。  
> Current primary anchor：[A14_02 共享规则与语义条件根表示有效秩](../../../../../../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor_cn.md)
> Current experiment：[A14_02_E01 中文 protocol 草案](../../../../../../Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/protocol_cn.md)
> Blocked follow-up anchor：[A14_03 状态功能秩与参数方向需求](../../../../../../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_03_state_parameter_functional_rank_demand/14_03_state_parameter_functional_rank_demand_anchor_cn.md)

## 1. 归属与编号

```text
A14：条件低维层级计算
├─ A14_01：参数—状态桥
│  └─ E08：关系复用状态桥独立重建（已完成；有边界证据）
├─ A14_02：共享规则是否额外降低任务根表示秩
│  └─ A14_02_E01：共享规则 vs 匹配 lookup（当前待审核实验）
└─ A14_03：更高状态功能秩是否要求更多参数功能方向
   └─ 候选 anchor；依赖 A14_02；没有 protocol，不授权执行
```

`A14_02_E01` 只分离 exact frequency、规则复用和 lookup 基数。路径深度四格是可能的后续 `A14_02_E02`，不并入当前实验。

A14_03 不重复 E08。E08 只观察参数侧与状态侧的复合差异；A14_03 要做的是因果干预：先建立真实的状态功能秩差异，再用共同参数秩上限检验高状态秩条件是否承受额外效用损失，以及更多参数方向能否选择性恢复。

## 2. 当前唯一验证目标

> 在匹配 exact relation frequency、独立规则数量、上下文多样性、输出分布和 held-out task utility 后，共享可组合规则是否比独立随机 lookup 产生更低的语义条件根残差 effective rank？

A14_03 的问题今天只审核、不执行：

> 如果 A14_02 证明一个条件确实需要更高的任务状态功能秩，那么保持该条件的 held-out utility 是否也需要更多已注册参数算子的功能方向？

## 3. 物理先验

1. 不同具体关系若调用同一个组合规则，模型可能复用相同的根状态形成机制。
2. 低 exact frequency 主要减少学习机会，不必决定条件表示维数。
3. 少量答案类别和较少 lookup 表都能制造平凡低秩，必须显式控制。

## 4. 假设、rival 与可证伪

**主假设：**低频 shared-rule 条件在通过未见组合 utility 门后，比频率、规则数量和答案分布匹配的 lookup 条件具有更低根残差 effective rank。

**最强 rival：**低秩完全由 lookup 函数基数较小、答案类别有限或模型欠训练造成，共享组合结构没有额外作用。

**主 falsifier：**所有能力与匹配守卫通过后，shared 与 lookup 的根残差 effective rank 无稳定差异，或差异可被 lookup-$K$ 曲线完全解释。

**证据不足：**任一主要条件没有学会、结果依赖单 seed／单阈值、答案或样本数不匹配、或者中心化实现不稳定。

## 5. 实验路径

### P0：复用既有已完成证据

- A14_E07 作为数学核算与实现 known-good，不重新编号运行。
- A14_01/E08 作为参数—状态桥的有边界起点；它不能支持纯频率结论。

### P1：当前实验 A14_02_E01

决定性四条件：

| 条件 | 规则类型 | exact relation exposure | 作用 |
|---|---|---:|---|
| S-U | shared | 低 | 低频共享规则关键反例 |
| L-U | independent lookup | 低 | matched rival |
| S-R | shared | 高 | 高频 shared 守卫 |
| L-R | independent lookup | 高 | 高频 lookup 守卫 |

主指标：

- 语义条件根残差 effective rank 的 matched shared advantage。

必要能力门：

- held-out answer accuracy / CE；
- 未见组合泛化；
- semantic consistency；
- 等答案、等样本和固定 checkpoint 选择。

辅助证据：

- lookup-$K$ 曲线；
- repeat-diverse vs repeat-duplicate；
- 梯度对齐；
- task-preserving projection；
- 参数秩只作桥接诊断。

### P2：候选后继 A14_03

只有 A14_02_E01 建立稳定、任务充分的状态功能秩差异后，才允许为 A14_03 编写 protocol。候选主判据是：

1. 用低状态秩条件校准参数功能秩上限；
2. 将同一上限施加到高、低状态秩条件；
3. 检验高状态秩条件是否承受额外 held-out utility 损失；
4. 增加参数保留方向后，检验该损失能否被选择性恢复。

若没有选择性损失或恢复，则状态几何不能解释参数方向需求。

### P3：条件式后续 A14_02_E02

仅当 E01 表明规则复用具有额外作用后，再审核：

> 在固定共享规则与活动源数量时，路径深度 × 精确路径激活频率是否改变条件功能秩，还是只改变学习速度和 pooled spectrum 权重？

该实验尚无正式 anchor clause 或 protocol，不授权实现。

### P4：真实任务迁移

只有受控实验形成稳定结论后：

1. ProofWriter：标准化多步规则推理验证；
2. MuSiQue：真实文本多证据组合验证。

不提前为迁移实验分配编号；CLUTRR、RepoBench 和 Router 实验继续 `park`。

## 6. E01 判决

| 结果 | 更新 |
|---|---|
| 低频 shared 通过泛化门且 rank 低于 matched lookup | 支持规则复用提供额外状态压缩 |
| 高频 lookup 同样低秩，但低频 shared 无优势 | 增强频率或函数基数解释 |
| matched 后无差异 | 削弱 A14_02 主假设 |
| 低频条件未学会或控制失败 | 证据不足，不解释秩 |

## 7. Claim boundary

即使 E01 通过，也只能说明受控 NTP 任务中存在任务充分的条件表示压缩；不能推出自然语言整体是树、NTP 普遍低秩、参数秩等于状态秩，或 Router 已有功能价值。

## 8. 当前 TODO

- [ ] 审核 A14_02_E01 的 generator。
- [ ] 审核 `ROOT` 位置和答案条件中心化。
- [ ] 审核 capability / generalization gates。
- [ ] 审核最小 rank effect 与 seed 规则。
- [ ] 对 A14_02_E01 给出 `批准 / 修改 / 拒绝`；批准前不运行。
- [ ] 审核 A14_03 Thinking Card 的现象、机制、rival 和改变判断的证据。
- [ ] 对 A14_03 anchor 给出 `提升 / 修改 / park`；A14_02 出结果前不创建 protocol。

**唯一下一决策：**批准、修改或拒绝 A14_02_E01 中文 protocol。
