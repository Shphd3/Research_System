# Protocol：A15_08_07_E04 完整表征与候选新增更新的层级几何对比

## 0. 审批快照

- **文档状态：**`APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN`。
- **人类已确认的问题：**比较完整层表征 \(Z_l\) 与候选新增更新 \(R_{U,l}\)，判断不同语义粗类用于细分类的方向是否彼此不同，以及合并多个粗类后维度是否增长。
- **Anchor 对齐：**`HUMAN_CONFIRMED_BOUNDED_EXTENSION`。研究者明确批准把完整表征 \(Z_l\) 的层级几何作为 A15_08_07 的有界描述性扩展；它不改变既有“新增可访问性”结论，也不准入 Router。
- **执行范围：**已批准实现、smoke、在单节点 8×5090 SPOT 上正式运行、结果分析和项目内生图；未批准打开 CONFIRMATION-v3、Anchor 修改、commit、push 或 sync。
- **实验角色：**描述性几何对照与机制定位，不承担新增信息准入或 Router 功能证明。
- **白话联合解释：**把模型真正看到的完整状态 \(Z_l\) 和本层剩下的候选新变化 \(R_U\) 放在同一把尺子上，看“领域方向本来就在完整表征里，还是本层更新又把它们分开了”。
- **主数据：**沿用 E03 的 8 个粗类 × 每粗类 8 个细类，TRAIN/DEVELOPMENT 各 640 条；不打开 CONFIRMATION-v3。
- **主层：**Block 24、28；层趋势固定为 2、6、10、14、18、22、24、28、32、36。
- **主对象：**parent-centered \(Z_l=N_l(h_l+a_l)\)。\(R_{U,l}=U_l-\widehat{\mathbb E}_{lin}[U_l\mid X_l]\) 只作补充机制定位，其中 \(U_l=Z_l-X_l\)。
- **主比较：**同一粗类内 8 个细类 versus 8 个粗类各取一个细类；类别数、每类样本数、文本、模型、token、层和分析代码保持一致。
- **主判定：**只有“同粗类谱更窄、同一粗类方向可复现且不同粗类方向不同、多个粗类方向合并后维数增长”三项在 Block 24 和 28 同时成立，才支持实验一；任一主条件不能由补充分析补救。
- **输出：**三张实验一主图和一张 B24/B28 的 \(Z_l\)–\(R_U\) 补充配对数值表。
- **不能 claim：**不能称为语义内禀秩、因果新增知识、模型原生使用、expert utility、Router 收益或遗忘结果。

## 1. 术语与分析对象

- **完整表征 \(Z_l\)：**当前 block 的 Attention 写入后、实际送给 MLP/候选 Router 的归一化状态。
- **候选新增更新 \(R_U\)：**本层精确更新 \(U_l\) 中不能被旧状态 \(X_l\) 线性预测的残余；它不排除 \(X_l\) 的非线性重编码。
- **谱宽：**归一化协方差能量下降较慢，达到 90% 能量需要更多 PCA 方向；单位为方向数或 \(r_{90}/79\)。
- **局部判别子空间：**在一个粗类内部，用 8 个细类标签学习的 rank-7 判别方向；rank 7 来自 8 类中心化均值最多 7 个独立对比，不是表征秩。
- **方向重合：**对两个正交基 \(P,Q\)，\(O(P,Q)=\|P^TQ\|_F^2/7\)；0 表示正交，1 表示同一子空间。
- **并集有效维数：**把多个粗类的 rank-7 基拼接后，对其奇异值平方计算熵有效秩；它表示方向库扩张，不等于完整表征的内禀秩。

## 2. 问题与假设

### H1：跨粗类谱宽化

在同样 8 类×10 条的条件下，parent-centered \(Z_l\) 的跨粗类任务归一化 \(r_{90}\) 高于同一粗类内部任务。\(R_U\) 同口径结果仅作补充；H1 必须与 H2、H3 合取才能支持实验一。

### H2：用于细分类的领域方向不同

同一粗类在 TRAIN 与 DEVELOPMENT 的 parent-centered \(Z_l\) 上学到的局部判别子空间重合度，高于不同粗类之间的重合度。主读数为对角线中位数减非对角线中位数。

### H3：多个领域方向合并后维度增长

随着加入的粗类数 \(k=1,\ldots,8\) 增加，parent-centered \(Z_l\) 局部判别子空间并集有效秩增长，并在 \(k=8\) 超过“同一粗类重复重采样 \(k\) 次”的 q95。

### H4：\(Z_l\)–\(R_U\) 机制定位

在 Block 24、28，用完全相同的数据、中心化和三个指标比较 \(Z_l\) 与 \(R_U\)：

- \(Z_l\) 明显、\(R_U\) 弱：领域几何主要已存在于完整状态，不是本层候选新增更新独有；
- 两者都明显：本层更新继续表达或强化完整状态中的领域分化；
- \(R_U\) 明显、\(Z_l\) 弱：本层更新包含局部重组，但它尚未主导完整状态几何；
- 两者都弱：当前数据不支持“领域方向分离并合并增秩”的解释。

## 3. 数据、中心化与保持不变项

- 沿用 E03 已审计数据、prompt、decision token、Qwen3-8B 权重和粗类—细类标签；不重新生成文本。
- TRAIN 只用于计算均值、拟合 residualizer 和生成主方向；DEVELOPMENT 用于跨表达复现，不参与阈值或层选择。
- 对 \(Z_l\) 画两种视图：
  1. **global-centered \(Z_l\)：**只减 TRAIN 全局均值，展示领域均值位置与局部变化共同形成的总几何；
  2. **parent-centered \(Z_l\)：**减各粗类 TRAIN 均值，只检验局部子空间形状。
- \(R_U\) 主图使用 parent-centered native \(R_U\)，与 E03 几何口径一致。
- 谱均按各任务总能量归一化，不做逐特征方差标准化；因此比较的是原生协方差方向，整体尺度不会影响 \(r_{90}\)。
- 只有模型、数据、prompt、token、hook 和 activation hash 全部一致时才复用 E03 的 \(X_l,U_l\)；否则执行前硬停止，而不是混用快照。

## 4. 三张主图与一张补充配对表

### 图 1：粗细粒度与深度的能量谱

- **主布局：**列分别为 parent-centered \(Z_l\) 的同粗类 8-way 与跨粗类 8-way，两格共享纵轴；\(R_U\) 同口径曲线放在补充行，不参与主判定。
- **曲线：**2、6、10、14、18、22、24、28、32、36 层，明确高亮 24、28。
- **横轴：**PCA 方向编号 1–79；**纵轴：**每个方向占总方差的比例，对数坐标。
- **附表：**每层报告同粗类与跨粗类 \(r_{90}\) 中位数、差值及粗类分层 bootstrap 95% 区间；B24/B28 单列突出。
- **白话结论模板：**“跨粗类曲线如果更平、\(r_{90}\) 更大，说明把不同领域放在一起后需要更多方向；但这还没说明这些方向真的属于不同领域。”

### 图 2：加入更多粗类后的并集维度增长

- **横轴：**加入的粗类数 \(k=1,\ldots,8\)；**纵轴：**rank-7 局部基并集的熵有效秩。
- **主线：**\(Z_l\)；阴影为同一粗类重复重采样的 5%–95% null。\(R_U\) 作为补充虚线。
- **数值：**报告 \(k=8\) 的实际有效秩、null q95、二者差值；B24/B28 分开。
- **白话结论模板：**“每加一个新领域，方向库都继续变大并超过重复同一领域的上限，才说明不同领域确实带来了新的判别方向。”

### 图 3：局部子空间重合矩阵

- **布局：**B24、B28 的 \(Z_l\) 为主热力图；\(R_U\) 两图作为补充对照。
- **行：**TRAIN 学到的粗类子空间；**列：**DEVELOPMENT 学到的粗类子空间。
- **单元格：**方向重合度 \(O(P,Q)\)；对角线是同一粗类跨 split 复现，非对角线是不同粗类重合。
- **主数值：**对角线中位数、非对角线中位数及差值；用 label-permutation 和同秩 Haar 作为参考。
- **白话结论模板：**“对角线明显更亮，说明同一领域换一批表达还能找回相似方向；非对角线较暗，说明不同领域用于细分的方向不同。”

### 补充表 4：Block 24、28 的 \(Z_l\)–\(R_U\) 配对解释

每层一行，列出两种对象的：跨减同 \(r_{90}\)、对角减非对角重合、\(k=8\) union−null q95。只报告同口径差值，不比较原始方差绝对大小。

## 5. 分析与不确定性

- 单位独立性以 8 个粗类为主，不把 64 个跨粗类组合当作 64 个独立重复。
- 谱宽使用粗类分层 bootstrap；方向差使用跨 split 的 8 个对角与 56 个有向非对角配对，并同时报告逐粗类值；并集 null 使用至少 1,000 个冻结重采样 seed。
- 三个结果先分别报告 `SUPPORTED / NOT_SUPPORTED / INSUFFICIENT`，再按注册的三项合取给出实验一总 verdict。
- **H1 supported：**跨减同 \(r_{90}\) 的同时 95% LCB > 0。
- **H2 supported：**对角减非对角方向重合的同时 95% LCB > 0，且 label-permutation/Haar 不产生相同差值。
- **H3 supported：**TRAIN 和 DEVELOPMENT 中均满足 \(k=8\) 实际 union effective rank > 同粗类重复 null q95，且 \(k=8\) 大于 \(k=1\)。
- **单项 not supported：**在有效 guard 下，该项的 95% UCB \(\le 0\)（H1/H2），或 \(k=8\) 不超过同粗类 null 中位数或不高于 \(k=1\)（H3）。其余边界情形为 `INSUFFICIENT`。
- **实验一总 `SUPPORTED`：**Block 24、28 的 H1、H2、H3 六个单项全部 `SUPPORTED`。
- **实验一总 `NOT_SUPPORTED`：**任一注册层的任一单项为 `NOT_SUPPORTED`；这否定“该三条件在两层一致成立”的命题，但不否定其他层或其他数据存在局部子空间。
- **实验一总 `INSUFFICIENT`：**没有单项 `NOT_SUPPORTED`，但至少一项为 `INSUFFICIENT`。若只在一层三项全成立，另报 `LAYER_SPECIFIC_ONLY`，不能升级为总 `SUPPORTED`。
- 数据身份、trace 分解、方向正交性或 split 守卫失败记为 `INSUFFICIENT`，不得解释科学结果。

## 6. 科学阶段

| 阶段 | 输入 | 操作 | 输出 | 停止条件 |
| --- | --- | --- | --- | --- |
| S0 身份审计 | E03 数据与 activation 快照 | 核对模型、文本、token、hook、层和 hash | 可复用清单 | 任一身份不一致即停 |
| S1 构造对象 | TRAIN/DEV 的 \(X_l,U_l\) | 计算 \(Z_l=X_l+U_l\)；按 E03 重新拟合各层 \(R_U\) | 10 层的 \(Z_l,R_U\) | trace/shape/finite guard 失败即停 |
| S2 谱分析 | 三种中心化对象 | 同粗类/跨粗类能量谱与 \(r_{90}\) | 图 1 与数值表 | 样本数不匹配即停 |
| S3 局部方向 | TRAIN/DEV 细类标签 | 学 rank-7 判别基并计算跨 split overlap | 图 3 | 任一粗类缺类或秩不足即停 |
| S4 并集增长 | 8 个局部基 | \(k=1\ldots8\) 加入粗类并与同粗类 null 比较 | 图 2 | null seed/覆盖不足即停 |
| S5 配对解释 | B24/B28 三类指标 | 同层、同指标比较 \(Z_l\) 与 \(R_U\) | 表 4 | 禁止跨对象比较原始尺度 |

## 7. 复现边界与待确认项

- **建议资源：**若 E03 activation 快照身份通过，只需在现有 8×5090 worker 上重算 10 层 residualizer 与几何；若快照不完整，才重新抽取。
- **预期产物：**`summary.md`、`detailed.md`、三张 PNG、四张机器表、identity/trace/seed receipts。
- **已授权：**实现、smoke、单节点 8×5090 SPOT 正式运行、项目内结果分析与生图。
- **仍未授权：**打开 CONFIRMATION-v3、Anchor 修改、commit、push、sync。
- **冻结执行配置：**`execution_surface=ACP`，`workspace=share-space`，`aec2=computing-cluster-5090-01g`，`worker_spec=n12lp.nn.i10a.8`，`worker_nodes=1`，`quota_type=spot`，`GPU/process_count=8`。

## 8. A–G 审计

| Block | 状态 | 说明 |
| --- | --- | --- |
| A 问题与边界 | `CONFIRMED` | 实验一只裁定完整表征的三项层级几何合取；不裁定新增信息或 Router |
| B 数据与来源 | `CONFIRMED` | 沿用 E03 已审计 TRAIN/DEV，不打开 confirmation |
| C 任务与监督 | `CONFIRMED` | 标签只用于局部判别基；谱不使用标签 |
| D 模型与对象 | `CONFIRMED` | 冻结 Qwen3-8B；parent-centered \(Z_l\) 为主，\(R_U\) 为补充 |
| E 目标与拟合 | `CONFIRMED` | 无模型训练；只重拟合 residualizer 和 rank-7 几何基 |
| F 比较与证据 | `CONFIRMED` | 三张主图、三项逐项 verdict 与两层合取总 verdict |
| G 执行与复现 | `CONFIRMED` | 实现、smoke 和单节点 8×5090 SPOT 正式运行已获批准 |

跨块一致性：`PASS`。主对象、数据、监督、指标、判定与资源边界一致。

设计冻结时间：`2026-08-19T00:00:00Z`（本次用户批准消息所在日期；精确执行时间写入 receipt）。注册修订：`E04-zru-geometry-v1`。科学正文在首次执行后不得静默改写；任何材料变更必须追加 amendment 并声明证据资格影响。

审批记录：研究者于 2026-08-19 明确要求“完成绘图实验，确切完成并回答实验1”，并明确其余更新不作为主结论。该表述确认 A–G、三项合取主判定以及实现、smoke、正式运行和项目内生图；不授权 publication/Git/sync。

## 9. 执行回执（不属于注册科学正文）

- ACP job：`pt-1qp1h2z0`；状态：`SUCCEEDED`；运行时间：2026-08-19 07:17:39Z 至 07:20:32Z。
- 资源实况：单节点 `n12lp.nn.i10a.8`，8×5090 32GB，`computing-cluster-5090-01g`，SPOT。
- source snapshot：`/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e04_z_ru_hierarchical_geometry/source-snapshots/formal-20260819T_e04_zru_geometry_r1`；manifest SHA256 `0d99d9c8b838eaae499fc6a6e8c6d3cfd35c54347f56951b0016ccdef52a3ecd`。
- raw result：`/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e04_z_ru_hierarchical_geometry/runs/formal-20260819T_e04_zru_geometry_r1`；analysis manifest SHA256 `95e3d5ae3972fbcaa1c56cc0660ed18fc4f8a3caa4abdb305f4214a1bf9d2af3`。
- 容器内新增核心测试：5/5 passed；完整 worker 测试在提交前为 90/90 passed。
- 结果记录：[summary.md](summary.md)、[detailed.md](detailed.md)。
