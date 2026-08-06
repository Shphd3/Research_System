# Round B Theory Pack

## Hypothesis

### Current Problem

当前 Round B 只回答一个问题：

`在当前训练得到的 router 上，不同 domain 的 routed activations 是否表现出更清晰的分离、更低的 overlap，以及更明确的 expert geometry？`

### Target Hypotheses

- `H2-B`：如果 router 真的利用了与 domain / semantic separation 相关的结构信息，则 experts 会表现出更清晰的 assignment specialization。
- `H3`：更清晰的 assignment specialization 会诱导更低的 expert 内部占用维度。
- `H4-B`：如果当前 quadratic-family 方法真的在利用相关二阶结构，则它应在 interference / geometry 指标上显示出与 baseline 不同的结构模式。

### Why It Matters

Round B 不是纯静态表示分析，而是当前模型结构后果的检查。

它回答的是：

- 训练出来的 router 是否正在朝理论上期望的方向收敛；
- expert 是否真的更专一；
- 不同 domain 的 activation overlap 是否真的被压低。

## 4. Mathematical Model
### Core Objects

对于 expert `e` 和 domain `A / B`，定义 routed feature covariance：

$$
C_{e,A} = \mathrm{Cov}(x \mid E=e, D=A), \qquad
C_{e,B} = \mathrm{Cov}(x \mid E=e, D=B).
$$

定义 subspace interference proxy：

$$
SI_e = \frac{\mathrm{Tr}(C_{e,A} C_{e,B})}{\|C_{e,A}\|_F \, \|C_{e,B}\|_F}.
$$

定义 expert low-rankness proxy：

$$
r_{0.9}(C_e)
$$

即解释 90% 能量所需的最小有效维数。

必要时还可观察：

- covariance overlap
- per-domain expert usage
- token-level expert assignment pattern

### Mechanism Claim Being Tested

Round B 不直接证明“当前 router 已经是完整 variance routing”，而是检查它是否已经产生下列结构后果：

1. 更清晰的 expert assignment
2. 更低的跨域 overlap / interference
3. 更低的 expert 内部 occupancy

如果这些结构后果没有出现，则即便 Round A 证明二阶结构有信息，也不能说明模型已经学会了使用这些信息。

### Geometry Interpretation

Round B 的理论位置是：

- Round A 检查“信息是否存在”
- Round B 检查“模型是否学会利用这些信息”

因此 Round B 是从数据结构层走向模型结构层的关键一步。

## Experiment Design

### Minimal Experiment

Round B 是一个 interference / geometry audit。

输入：

- 当前训练得到的一个或若干 checkpoint
- routed activations / expert assignments
- domain split

输出：

- `SI_e`
- `r_{0.9}`
- overlap / covariance overlap
- per-domain expert usage
- token-level expert evidence

### Minimal Procedure

1. 从当前 checkpoint 提取 routed activations 与 expert assignments。
2. 按 domain 划分 routed activations。
3. 对每个 expert 计算 domain-conditional covariance。
4. 计算 `SI_e`、`r_{0.9}` 和 overlap。
5. 辅助检查 token-level expert usage 与 domain-level usage pattern。

### Metrics

主指标：

- `SI_e`
- `r_{0.9}`
- overlap / covariance overlap

辅助指标：

- per-domain expert usage
- token-level expert inspection
- load balancing

### Decision Rule

- 如果模型表现出更低的 `SI_e`、更低的 occupancy、并且伴随更清晰的 expert usage pattern，
  则支持“模型正在学会利用与 separation 相关的结构信息”。

- 如果几何指标没有改善，或 assignment pattern 仍不清晰，
  则说明当前模型还没有把二阶结构转化成有效 routing mechanism。

- 如果几何指标改善，但 load balance 极差或 collapse 明显，
  则结果不能被解释为健康 specialization。

## Conclusion/Update

### What This Round Can Establish

Round B 只允许建立下面这一层结论：

- 当前训练模型是否已经呈现出更清晰的 routing geometry 后果。

### What This Round Cannot Establish

Round B 不能单独建立：

- 当前模型已经完成真正的 variance routing 机制闭环
- CL 上的最终 forgetting 优势已经得到支持

### What Should Be Handed to Experiment Agent

experiment agent 应接到的任务是：

- 在新的项目文件夹里实现一个独立 `Round B`
- 只做 interference / geometry audit
- 结果必须整理成 `Result Pack`

### Theory -> Experiment Card

- Current problem:
  Does the currently trained router exhibit clearer expert geometry, lower cross-domain overlap, and more specialized assignment patterns?

- Target hypothesis:
  H2-B, H3, and H4-B

- Minimal mathematical definition:
  Use domain-conditional expert covariance, `SI_e`, and `r_{0.9}` to characterize cross-domain overlap and within-expert occupancy.

- Minimal experiment:
  Frozen-checkpoint interference / geometry audit on routed activations and expert assignments.

- Metrics:
  `SI_e`, `r_{0.9}`, covariance overlap, per-domain expert usage, token-level expert inspection, and load balance.

- Decision rule:
  If geometry becomes clearer and overlap decreases without collapse, support the claim that the router is learning useful structure. Otherwise weaken the claim.

- Implementation constraints:
  Keep this round separate from clustering experiments and from any new router training.

- Known risks:
  Geometry improvements may be confounded by load imbalance, collapse, or checkpoint instability.
