# 会议简报：V2.2 静态特征家族分发

## 0. 执行摘要

**研究问题：** 在特征家族频率均匀、整体表示谱近似各向同性的受控分布中，是否可以用无标签校准特征构造一个静态路由器，使专家负载均衡并保持特征家族不被切碎。

**机制解释：** 谱各向同性提供干净距离度量，频率均匀提供负载均衡条件，局部可恢复性提供特征家族身份；三者同时成立时，静态特征家族分发才可构造。

**主要结果：** V2.2 支持一个受控静态结论：构造的聚类方法 BFSR 可以在上述三条件同时成立时构造平衡且保持特征家族的静态分发；谱各向同性单独不够。

**证据说明：** E1--E5 共同验证该结论：正例中 BFSR-Cluster 达到 LoadCV 0.003、family consistency 0.990、cluster accuracy 0.986；各向同性空白对照的信息量约为 0.002；可恢复性、白化和频率消融分别验证三个条件的作用。

1. 谱各向同性单独不能恢复特征家族分发。
2. 局部可恢复性提高时，静态专门化质量同步提高。
3. 频率不均匀时，按 family 数量均分不再保证负载均衡，需要 mass-aware assignment。

**结论边界：** 当前证据只支持受控合成分布中的静态分发结论，不能推出真实语言模型 hidden states、训练保持、专家效用、learned router 动态或自动选择特征家族数量。

**执行动作：** 组会前汇报只关闭 V2.2 静态 clean case；组会后选择一个下一阶段问题：static utility、real hidden-state audit、training preservation 或 automatic K selection。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| BFSR | 平衡特征专门化路由 | normalize -> cluster -> assign -> route | 静态路由流程 | 当前构造方法 | 训练收益 |
| 特征家族 | 应稳定进入同一专家的潜在特征类别 | 合成数据中的 latent family $F$ | $F\in\{1,\ldots,K\}$ | 判断 family 是否被保持 | 真实语义专家 |
| LoadCV | 专家负载变异系数 | expert mass 的标准差除以均值 | 越低越均衡 | 判断负载均衡 | family 是否完整 |
| Family consistency | 每个 family 是否主要进入同一专家 | 每个 $F=k$ 内最大 expert 概率再平均 | $0$ 到 $1$ | 判断 family 是否被切碎 | 专家功能价值 |
| Expert information fraction | expert id 携带多少 family 信息 | $I(G;F)/H(G)$ | $0$ 到 $1$ | 区分负载均衡和特征分发 | downstream utility |

## 2. 机制解释与建模

**核心模型：**

$$
F\sim\mathrm{Unif}(\{1,\ldots,K\}),\qquad
X\mid F=k=\mu_k+\epsilon,\qquad
\operatorname{Cov}(\widetilde X)\approx I_d.
$$

**符号含义：**

- $F$：潜在特征家族。
- $X$：路由器读取的表示向量。
- $G=g(X)$：静态路由器输出的专家编号。

**机制链条：**

1. 谱各向同性控制 metric。
2. 局部可恢复性使无标签聚类能恢复 family identity。
3. 频率均匀使 recovered families 均分给 experts 后得到近似负载均衡。

**当前问题分解：**

- 需要判断：三条件是否足以构造平衡且保持 family 的静态分发。
- 替代解释：仅靠负载均衡或谱各向同性也许已经足够。
- 当前实验区分：谱控制、局部可恢复性、频率均匀分别承担什么作用。

## 3. 主要结果

**一句话总结：** V2.2 完成受控静态 clean case 的闭环：BFSR 在三条件同时成立时有效，关键条件移除时出现可预测失败。

### 结果 1：静态特征家族分发需要谱控制、局部可恢复性和频率均匀三个条件同时成立。

**机制对应：** 该结果对应第 2 节的三段机制链条。

**指标或条件定义：** LoadCV 判断负载均衡；family consistency 判断 family 是否完整；cluster accuracy 判断无标签 family recovery；expert information fraction 判断 expert id 是否携带 family 信息。

**证据：** E1 中 BFSR-Cluster 达到 LoadCV 0.003、family consistency 0.990、cluster accuracy 0.986。E2 中各向同性空白对照的信息量约为 0.002。E3 中分离度提高使 cluster accuracy 从 0.063 到 0.942、family consistency 从 0.294 到 0.956。E5 中频率不均匀时，mass-aware BFSR 将 LoadCV 从 0.149 降至 0.029。

**解释：** E2 排除“谱各向同性单独足够”；E3 说明 family 可恢复性决定专门化质量；E5 说明频率均匀是 equal-number assignment 产生 mass balance 的条件。

**边界：** 该证据不支持真实语言模型 hidden states、训练保持、专家效用、learned router 动态或自动选择 $K$。

**来源：** `papers/spectral_partition_router_v2_2/exp/results/summary.md`；`papers/spectral_partition_router_v2_2/AUDIT_2026_07_06.md`；`papers/spectral_partition_router_v2_2/latex/paper.tex`。

## 4. 执行动作

**下一步动作：** 组会汇报先关闭 V2.2 静态 clean case，不扩展新的实验主张。

**目的：** 明确当前结论、产出和边界，并决定下一阶段只进入一个问题。

**完成判据：** 组会后选定一个方向：static utility、real hidden-state audit、training preservation 或 automatic K selection。

## 5. 证据索引

| 结果 | 证据 | 主要指标或图 | 支持什么 | 不能证明什么 | 来源 |
|---|---|---|---|---|---|
| 结果 1 | E1 clean case | LoadCV 0.003；family consistency 0.990；cluster accuracy 0.986 | BFSR 在 clean case 有效 | 真实训练收益 | `exp/results/summary.md` |
| 结果 1 | E2 isotropy-only null | information fraction 约 0.002 | 谱各向同性单独不够 | 所有谱方法失败 | `exp/results/summary.md` |
| 结果 1 | E3/E5 消融 | recoverability sweep；frequency ablation | 可恢复性和频率均匀分别必要 | learned router 或真实 hidden states | `AUDIT_2026_07_06.md` |

## 6. 来源索引

**Anchor：** 当前 V2.2 是 paper workspace 内的静态 clean-case 闭环，不替代主线 anchor。

**Protocol：** `papers/spectral_partition_router_v2_2/exp/EXPERIMENT_PLAN.md`

**Summary：** `papers/spectral_partition_router_v2_2/exp/results/summary.md`

**Detailed：** `papers/spectral_partition_router_v2_2/AUDIT_2026_07_06.md`

**Figures：** `papers/spectral_partition_router_v2_2/latex/figures/`

## 7. 补充材料

产出文件：

- `papers/spectral_partition_router_v2_2/PROBLEM_STATEMENT.md`
- `papers/spectral_partition_router_v2_2/METHOD_AND_THEORY_NOTES.md`
- `papers/spectral_partition_router_v2_2/RESEARCH_PLAN.md`
- `papers/spectral_partition_router_v2_2/AUDIT_2026_07_06.md`
- `papers/spectral_partition_router_v2_2/latex/paper.tex`
- `papers/spectral_partition_router_v2_2/latex/paper.pdf`
- `papers/spectral_partition_router_v2_2/exp/results/summary.md`
