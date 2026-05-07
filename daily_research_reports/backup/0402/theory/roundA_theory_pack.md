# Round A Theory Pack

## Hypothesis

### Current Problem

当前 Round A 只回答一个问题：

`如果显式构造一阶特征与二阶特征表示，二阶表示是否比一阶表示更能揭示 domain / semantic structure？`

### Target Hypotheses

- `H1`：某些二阶统计量确实编码了 domain / semantic separation 的结构信息，而不仅仅是噪声尺度。
- `H2-A`：如果这种二阶结构真实存在，则基于二阶表示做 clustering / grouping 时，应当比一阶表示得到更清晰的 separation。

### Why It Matters

这轮不是要证明当前 router 已经学会按方差分发，而是先证明：

- 二阶结构里确实有与分发相关的可用信息；
- 这条线不是纯口头直觉。

如果这一步不成立，那么后面关于 variance-aware routing 的机制叙述会非常虚。

## Mathematical Modeling

### Core Objects

给定中心化特征：

$$
x_c = x - \mu_t.
$$

定义一阶表示：

$$
z^{(1)} = x_c.
$$

定义当前最简单的二阶表示：

$$
z^{(2)} = x_c \odot x_c
$$

或去偏版本：

$$
z^{(2)}_{\text{deb}} = x_c \odot x_c - \lambda_t.
$$

如果需要进一步做更稳定的结构分析，也可以使用：

$$
\phi^{(2)}(x) = P z^{(2)} \quad \text{or} \quad P z^{(2)}_{\text{deb}}
$$

其中 `P` 是 PCA / SVD 投影矩阵。

### Mechanism Claim Being Tested

Round A 不测试“router 是否已学会使用二阶项”，而测试更基础的一层：

`数据表征中的二阶结构本身，是否比一阶结构更能揭示 domain / semantic grouping。`

如果二阶表示在 clustering / grouping 上显著优于一阶表示，则说明：

- 二阶结构中包含与 separation 相关的信息；
- variance-aware routing 至少具有数据层面的候选合法性。

### What Counts As “Variance-Relevant Structure”

本轮不把“按方差分发”定义成完整 router 结论，而只给出最小数据层定义：

`某类二阶表示若能把不同 domain / semantic groups 分得更清楚，则可视为捕获了与 routing 可能相关的 variance-relevant structure。`

### Key Quantities

可比较的对象包括：

- 一阶表示的 clustering quality
- 二阶表示的 clustering quality
- 一阶表示的 group separability
- 二阶表示的 group separability

这里的“更清楚”不是一句空话，而应落在可计算指标上。

## Experiment Design

### Minimal Experiment

Round A 是一个静态 clustering / separation audit。

输入：

- 固定 checkpoint 的 hidden features
- 明确的数据子集
- 一阶表示与二阶表示

比较：

1. `z^{(1)} = x_c`
2. `z^{(2)} = x_c \odot x_c`
3. 如有必要，再比较去偏版本 `z^{(2)}_{\text{deb}}`

### Minimal Procedure

1. 从固定 checkpoint 抽取一批 token-level hidden features。
2. 构造一阶与二阶表示。
3. 必要时做 PCA / SVD 降维，保持比较公平。
4. 对这些表示分别做 clustering / grouping / separation analysis。
5. 报告哪种表示更能把 domain / semantic groups 分开。

### Metrics

主指标建议：

- clustering quality
- separation quality
- 如有标签，可加入 group purity / cluster purity / adjusted score

辅助输出建议：

- 可视化
- cluster centroid inspection
- 每簇的 domain composition

### Decision Rule

- 如果二阶表示并没有比一阶表示更清楚地揭示 structure，
  则当前“variance-aware”叙述必须降级。

- 如果二阶表示稳定地比一阶表示更能揭示 domain / semantic grouping，
  则支持继续推进 variance-aware routing 主线。

- 如果结果高度依赖某个降维或聚类细节，
  则结论只能记为 `tentative evidence`。

## Conclusion/Update

### What This Round Can Establish

Round A 只允许建立下面这一层结论：

- 二阶结构中是否存在与 separation 相关的信息。

### What This Round Cannot Establish

Round A 不能直接建立：

- 当前 router 已经在按方差分发
- 二阶机制已经主导路由决策
- 低 forgetting 已经得到支持

### What Should Be Handed to Experiment Agent

experiment agent 应接到的任务是：

- 在新的项目文件夹里实现一个独立 `Round A`
- 只做 clustering / separation audit
- 结果必须整理成 `Result Pack`

### Theory -> Experiment Card

- Current problem:
  Does second-order representation reveal domain / semantic structure more clearly than first-order representation?

- Target hypothesis:
  H1 and H2-A

- Minimal mathematical definition:
  Compare `x_c` against `x_c \odot x_c` or its debiased version as alternative representations for clustering / separation.

- Minimal experiment:
  Frozen-feature clustering / separation audit on the same checkpoint and the same sampled tokens.

- Metrics:
  Clustering quality, separation quality, group purity, and supporting visualizations.

- Decision rule:
  If second-order representation consistently reveals clearer grouping than first-order representation, support the data-level legitimacy of variance-aware routing. Otherwise downgrade the claim.

- Implementation constraints:
  Keep checkpoint fixed, keep sample source fixed, and do not mix this round with training-progress or interference analysis.

- Known risks:
  Results may depend on clustering method, dimensionality reduction choice, and label granularity.
