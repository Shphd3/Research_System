# Protocol 草案：A14_E08 关系复用的参数—任务状态桥接审计

## 0. 批准快照

**批准状态：**研究者于 2026-07-22 给予暂时批准并授权直接实现、冒烟检查与完整运行。数值阈值和判决规则在本轮运行前冻结；运行后审核若不通过，另行修订协议并重跑，不追溯移动本轮门槛。

**目的：**判断学长 ABCD-NTP 实验中观察到的 Q/K 功能压缩，是否同时对应一个跨 B 上下文可复用、且保留 C-token 任务效用的低维 attention-update 状态。

**主子锚点：**[A14_01 中文 anchor](../../../../../../problem_anchors/14_tree_low_rank_language_structure/14_01_relation_reuse_parameter_state_bridge/14_01_relation_reuse_parameter_state_bridge_anchor_cn.md)

**决策问题：**在 full-model 能力匹配时，`share16` 是否比 `random_unshared` 需要更少的状态方向，才能在未见 B 上保持第一个 C token 的交叉熵？

**实验角色：**参数谱现象到条件状态理论之间的最小桥接审计；不是频率因果实验，也不是 Router 实验。

**主要指标：**`random_unshared` 相对 `share16` 多需要的归一化 held-out 功能状态秩 \(C_H\)。

**主证伪条件：**来源、能力、划分和 intervention 守卫均通过，但 \(C_H\le0\)，或 `share16` 不能在预注册维度预算内保留 held-out C-token loss。

**建议审核的三个数值决定：**

1. 任务容忍度 \(\epsilon=0.02\) nat / first-C-token；
2. 非平凡低维预算 \(k_H/d\le0.25\)，即 64 维模型最多 16 维；
3. 主要统计守卫为 3/3 seeds 方向一致，且按 seed 与 B identity 分层 bootstrap 的 95% 区间下界大于 0。

**Claim Boundary：**通过只表示当前合成 NTP 条件下，参数功能压缩伴随可复用、任务充分的局部状态压缩。它不证明“频率导致低秩”、自然语言是树、概率活动树存在于真实 LLM，或该状态应被 MoE Router 使用。

## 1. 术语与定义

| 术语 | 普通含义 | 具体计算 | 单位 | 决策作用 | 不能证明 |
| --- | --- | --- | --- | --- | --- |
| share 条件 | A→C 映射跨多少 B 复用的设置 | `share16/share4/share2/random_unshared` | 类别 | 主要受控变量 | 纯频率；独立规则数量也变化 |
| 来源复现 | 确认继承的参数侧现象真实存在 | 重放 full checkpoint、matched-fit 和源删谱曲线 | pass/fail | 进入 E08 的前置守卫 | 状态桥已经成立 |
| attention update | attention 子层在 B 末端写入 residual stream 的更新 | \(g_{i,t}=h_{i,t}^{post-attn}-h_{i,t}^{pre-attn}\)，具体 hook 按实现核对 | 向量 | 状态侧主对象 | 整个 residual stream 低维 |
| held-out 功能状态秩 | 保留未见 B 任务损失所需的最小线性维数 | 校准 B 拟合 PCA；测试 B 做状态投影干预 | 维 | 主要指标基础 | 严格秩、信息熵或语义原子数 |
| 能量有效秩 | 奇异值能量等效占据的方向数 | entropy effective rank 与 95% energy rank | 维 | 几何诊断 | 投影方向对任务有用 |
| QK 功能秩 | 保留 attention-score 功能与 C-token loss 所需的最小组合算子秩 | 对 \(B_{QK}=W_Q^\top W_K\) 做 SVD 截断并在 score 处替换 | 维 | 参数侧桥接诊断 | hidden-state 功能秩 |
| 同秩随机空间 | 与学得子空间维数相同但方向随机的空间 | Haar 随机正交基 | loss 增量 | 排除任意低维投影都可用 | 学得空间具有语言语义 |

## 2. Anchor 对齐

**A14 已证明：**给定一个活动模式，根表示位于活动路径像空间之和中；若少量低维源被激活，则条件可达维数受控。

**A14 尚未证明：**NTP 会把重复关系组织为低维局部状态；这种状态能跨上下文复用；低维投影保持任务效用。

**学长实验已观察：**在 share 复合条件变化时，学习速度与 Q/K 尾部删谱鲁棒性系统变化，`share16` 最集中，`random_unshared` 最不集中。

**本实验补的唯一箭头：**

```text
QK 参数功能压缩
        ?
        ↓
跨 B 可复用、任务充分的低维 attention update
```

**本实验不补的箭头：**

```text
纯 relation frequency
→ 梯度对齐
→ QK 功能压缩
```

因为现有 share 设置把频率、复用和独立规则数量同时改变。该因果分离只能在 E08 通过后由新协议处理。

## 3. 可证伪假设

### H1：held-out 状态功能秩差

在 matched-fit checkpoint 上：

\[
k_H(\texttt{share16};0.02)
<
k_H(\texttt{random\_unshared};0.02).
\]

### H2：非平凡预算

`share16` 满足：

\[
k_H(\texttt{share16};0.02)/64\le0.25.
\]

### H3：方向特异性

在与 \(k_H(\texttt{share16};0.02)\) 相同的维数下，校准数据学到的 PCA 空间比同秩随机空间更能保留 held-out C-token loss。

### H4：参数—状态排序一致性（次要）

四个 share 条件的 \(k_{QK}\) 与 \(k_H\) 应具有相同的大体次序。该项只诊断桥接完整性，不覆盖 H1–H3 的主判决。

## 4. 最强替代解释

1. **规则数量解释：**`share16` 只有更少 lookup 表，所以任何记忆实现都更简单；不是跨上下文复用产生了共同机制。
2. **参数化解释：**单独 \(W_Q/W_K\) 谱集中，但决定 score 的组合算子或状态并不集中。
3. **训练集 PCA 解释：**低维只在拟合子空间的数据上成立，未见 B 不迁移。
4. **能量而非效用解释：**少数方向解释大量范数，却不保留预测 C 所需的信息。
5. **欠训练解释：**低 share checkpoint 能力较差，因此看似需要更多方向。
6. **任意投影解释：**模型对状态干预普遍鲁棒，PCA 方向并不特殊。

本协议分别通过 claim boundary、组合 QK 对象、B-disjoint 划分、功能投影、matched fit 与随机空间对照处理这些解释。第一项不会由 E08 消除；它只决定后续是否值得做正交因果实验。

## 5. 数据、模型与来源守卫

### 5.1 来源恢复（S0，硬门）

执行前必须定位并冻结：

- ABCD 数据生成器及 commit / 文件哈希；
- `share16/share4/share2/random_unshared` 的精确定义与每个 B 的映射表；
- 64 维、单层、单头 causal attention 模型配置；
- 训练数据、held-out 数据、3 个 seed、optimizer 与 checkpoint；
- matched-fit 判据；
- 源实验 \(W_Q/W_K/W_V/W_O\) 删谱实现与逐 rank 指标。

若现有 checkpoint 不可恢复，只能在完全复现生成器与配置后重新训练；任何未确认的口头设定不得静默补齐。

### 5.2 主设置

- 模型宽度：64；128 维异常运行不进入主结论。
- 种子：源实验的 3 个 seed。
- 条件：四个 share 设置全部保留；主要比较只使用 `share16` 与 `random_unshared`。
- 目标位置：B 结束位置产生的 logits 所预测的第一个 C token。
- 能力条件：沿用源实验 matched-fit 规则；未达到者标记 insufficient，不用后期训练步替代。

### 5.3 校准 / 测试划分

按 B identity 划分，而不是随机划分样本：

- `share16`：16 个 B 中 8 个 calibration、8 个 test；
- `share4`：每个 4-B 映射族内 2/2；
- `share2`：每个 2-B 映射族内 1/1；
- `random_unshared`：按 B identity 平衡划分 8/8；其 test 映射在定义上不与 calibration 复用，这是 no-reuse 边界的一部分。

每个 seed 使用冻结的确定性 split；交换 calibration/test 两半作为 split-swap 稳健性诊断。样本数量在条件间匹配。

## 6. 状态提取与 intervention

### 6.1 主状态

对每个目标位置记录：

\[
g_{i,t}=h_{i,t}^{post-attn}-h_{i,t}^{pre-attn}.
\]

若实现使用 pre-LN、post-LN 或不同 residual API，详细记录 hook 两端张量，并用“重放原 update 等于原 logits”的守卫确定对象。raw residual state 同时保存，但不参与主判决。

### 6.2 仿射子空间

只用 calibration B 的 \(g_{i,t}\) 拟合均值 \(\mu_s\) 和完整 PCA 基。对所有 \(k=0,1,\ldots,64\)，test 状态替换为：

\[
\Pi_{s,k}(g)=\mu_s+U_{s,k}U_{s,k}^{\top}(g-\mu_s).
\]

替换后运行剩余计算，测第一个 C token 的 teacher-forced cross entropy。

### 6.3 功能状态秩

\[
k_H(s;0.02)
=
\min\{k:L_s^{(k)}-L_s^{full}\le0.02\}.
\]

若曲线非单调，使用“从该 \(k\) 到 64 的所有更高秩均满足容忍度”的最小 \(k\)，防止偶然点通过。

### 6.4 随机与泄漏对照

- 每个主 rank、条件和 seed 使用 32 个 Haar 同秩随机空间；
- shuffled-state control 在相同 B split 内打乱状态与样本配对；
- test-fitted PCA 只作为乐观泄漏上界，明确不进入证据；
- \(k=64\) 的 full-basis replay 必须复现原始 loss。

## 7. 参数侧桥接诊断

### 7.1 组合 QK 功能秩

按实现方向确认 attention score 的组合算子 \(B_{QK}\)。对其 SVD 截断后，在 score 计算点直接使用 \(B_{QK,k}\)，其余权重不变。定义：

\[
k_{QK}(s;0.02)
=
\min\{k:L_{s,QK}^{(k)}-L_s^{full}\le0.02\}.
\]

### 7.2 来源曲线复现

原始单独 \(W_Q/W_K\) 尾部删除曲线必须复现到源记录的数值容忍度内；\(W_V/W_O\) 保留为机制定位对照。它们不替代组合 QK 与状态功能秩。

### 7.3 梯度诊断

若现有代码能无额外训练稳定提取，则报告 relation-conditioned 梯度余弦与 gradient effective rank。该项是候选机制诊断，不属于 E08 pass/fail，也不能在运行时升级为主结论。

## 8. 主要指标与统计规则

### 8.1 主要指标

\[
C_H
=
\frac{k_H(\texttt{random\_unshared};0.02)
-k_H(\texttt{share16};0.02)}{64}.
\]

**单位：**环境维度比例。

**具体解释：**正值表示 no-reuse/高规则数量复合条件需要更多任务状态方向；它不把差异归因于频率。

### 8.2 统计聚合

- 首先逐 seed 报告 \(k_H\) 与 \(C_H\)；
- 主方向守卫要求 3/3 seed 的 \(C_H>0\)；
- 使用分层配对 bootstrap：外层按 seed，内层按 test B identity 重采样；
- 主要置信区间为 \(C_H\) 的 95% percentile interval；下界必须大于 0。

仅 3 个 seed 使 seed-level 不确定性较粗；必须同时展示所有 seed，不以大量 token 伪造独立样本数。

### 8.3 非平凡预算

\[
k_H(\texttt{share16};0.02)\le16.
\]

该 25% 预算沿用 A14 对“远小于环境维度”的保守操作化。研究者可在批准前修改；运行后不得移动。

## 9. 次要指标

1. 四个 share 条件的 \(k_H\)、\(k_{QK}\) 与完整 loss-rank 曲线；
2. energy effective rank、95% energy rank 和 held-out 投影误差；
3. PCA 对同秩随机空间的 C-token loss 优势；
4. raw residual 与 attention update 的结果差异；
5. split-swap 稳健性；
6. \(k_H\) 与 \(k_{QK}\) 的 seed-level / condition-level 秩相关；
7. 若可用，relation-conditioned gradient alignment。

这些指标解释主结果，不覆盖主要指标与预算。

## 10. 已知正确、已知错误与易混淆案例

### 已知正确案例

1. \(k=64\) 的完整 PCA 基应复现原始 attention update 与 loss。
2. 重放原始 update 应与未 hook 的 forward 一致。
3. synthetic rank-\(r\) state injection 守卫应恢复已知 \(r\)，并在 \(k<r\) 时损害注册 target。

### 已知错误案例

1. 在 test B 上拟合 PCA 再测 test：存在泄漏，不得作为证据。
2. 只报告 95% energy rank：不能说明任务效用保留。
3. 只删除 \(W_Q\) 或 \(W_K\)：不能唯一表征 score 算子的功能秩。

### 易混淆案例

1. `share16` energy rank 低，但 \(k_H\) 高：说明几何集中不等于任务充分。
2. `share16` 的 \(k_H\) 低，但随机同秩空间也一样好：说明模型只是普遍容忍投影。
3. QK 功能秩低，但状态功能秩无差异：参数—状态桥失败。
4. 状态桥通过，但中间 share 条件不单调：保留主要复合对照，不能声称简单频率定律。
5. 状态桥通过，但规则数量正交实验后只随规则数量变化：机制应改写为函数复杂度，而非频率。

## 11. 分阶段证据计划

| 阶段 | 局部问题 | Pass | Fail | Insufficient | 输出 |
| --- | --- | --- | --- | --- | --- |
| S0 来源恢复 | 源实验是否可追溯 | generator/checkpoint/metric 全冻结 | — | 任一核心 artifact 缺失 | provenance manifest |
| S1 来源重放 | Q/K 现象是否复现 | matched fit 与删谱曲线复现 | 明确不复现 | 代码语义仍不确定 | replay table |
| S2 hook 守卫 | 状态对象与 replay 是否正确 | full replay/no-op 通过 | 数值不一致 | hook 不可定位 | intervention audit |
| S3 held-out 几何 | calibration 子空间能否跨 B | 完整曲线生成 | — | split/sample 守卫失败 | spectrum/projection tables |
| S4 功能干预 | 低维状态是否保留 C loss | \(k_H\) 可稳定计算 | 主假设不满足 | 曲线或数值不稳定 | functional-rank table |
| S5 随机对照 | 方向是否特异 | PCA 优于随机 | 无优势 | 随机运行不完整 | random-control table |
| S6 联合判决 | 是否建立状态侧桥 | Success 条款全满足 | Failure 条款触发 | 任一硬门失败 | summary/detailed/figures |

任何阶段失败不得通过增加 seed、改变阈值或改用 raw residual 静默救援；这些变化需要新协议修订。

## 12. Success / Failure / Insufficient

### Success

同时满足：

1. S0–S2 全部通过；
2. 3/3 seed 的 \(C_H>0\)，且其分层 bootstrap 95% 区间下界大于 0；
3. `share16` 的 \(k_H\le16\)；
4. 在该 rank 上，PCA 子空间保留 \(\Delta CE\le0.02\)，而 32 个同秩随机空间的中位数不满足该容忍度；
5. split-swap 不反转 `share16` 对 `random_unshared` 的方向。

### Failure

来源、能力、hook 与统计守卫通过，但出现任一情况：

- 主差值不为正或 seed 方向不稳定；
- `share16` 超过 16 维预算；
- PCA 只解释能量但不能保持 loss；
- 同秩随机空间与 PCA 无实质差异。

### Insufficient evidence

- 源 artifact 或生成器语义无法恢复；
- 源 Q/K 现象不能可靠复现；
- matched-fit checkpoint 缺失；
- B-disjoint 划分不可构造；
- no-op/full-rank replay 不通过；
- 运行不完整或 rank 曲线数值不稳定。

## 13. 中心图合同

### 图 1：状态功能秩曲线

- **问题：**不同 share 复合条件需要多少状态方向才能保留未见 B 的 C-token loss？
- **横轴：**保留状态秩 \(k\)；**纵轴：**相对完整模型的 \(\Delta CE\)（nat / first-C-token）。
- **线与误差：**四个 share 条件；按 seed 与 B 的区间。画出 \(\epsilon=0.02\) 横线。
- **允许结论：**`share16` 与 `random_unshared` 的 held-out 功能状态秩是否不同。
- **不能证明：**频率是原因、梯度对齐或自然语言外推。

### 图 2：参数功能秩与状态功能秩

- **问题：**QK 参数压缩与状态任务压缩是否在同一运行中共同出现？
- **横轴：**归一化 \(k_{QK}\)；**纵轴：**归一化 \(k_H\)；颜色为 share 条件，点为 seed。
- **允许结论：**两类功能秩的经验对应关系。
- **不能证明：**QK 压缩因果地产生状态压缩；相关仅作桥接诊断。

随机空间结果使用表格与图 1 的阴影带呈现，不新建第三个中心叙事。

## 14. 本协议不能回答的内容

1. exact relation frequency 与独立规则数量谁是因果因素；
2. 梯度对齐是否是训练机制；
3. 长程、层级深度或树结构本身是否降低秩；
4. 自然语言 hidden state 是否存在同样条件空间；
5. 多个局部空间是否需要多个专家；
6. Router 是否应读取该 attention update；
7. 负载均衡、z-loss 或 expert capacity 应如何设置；
8. 该几何是否带来真实 workload 的稳定 expert utility headroom。

## 15. 协议通过后的唯一分支

- **若 Success：**下一项独立研究问题 正交操纵 exact relation repetition 与 independent-rule complexity，裁决“复用/频率”与“函数复杂度”解释；不能直接进入 Router。
- **若 Failure：**关闭“现有 QK 结果支持概率树低维局部状态”的桥接主张；保留参数侧现象，不再用它支持状态理论。
- **若 Insufficient：**只补齐缺失来源或实现守卫，不改变假设、阈值和主指标。

## 16. 审阅记录

- 2026-07-22：依据研究者对 share 混杂、状态秩对象、downstream utility 标准、lookup-rule rival 和 Router 边界的明确判断起草。
- 2026-07-22：研究者暂时批准直接执行。冻结状态对象为 attention residual update，\(\epsilon=0.02\)，16/64 非平凡预算，3/3 seed 与分层 bootstrap 规则，以及“先桥接、后正交分离”的执行顺序。
- 运行后重点复核：来源重建是否足够忠实；状态 hook 是否恰好位于 B 末端 attention update；B-disjoint 划分是否无泄漏；\(k_H\) 的持续容忍定义是否正确；随机同秩对照是否排除一般投影鲁棒性；结论是否保持复合条件边界。
- 2026-07-22：full run 完成。由于公开来源缺少生成器、训练代码和 checkpoint，S0 来源硬门失败，正式判定为 `insufficient evidence`；独立重建的其余操作守卫全部通过。结果见 [summary_cn.md](summary_cn.md)，该记录不追溯修改冻结阈值。
