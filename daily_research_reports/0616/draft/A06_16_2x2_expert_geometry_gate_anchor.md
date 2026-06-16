---
anchor_id: A06_16_2x2_expert_geometry_gate
parent_node: rq.expert_specialization
status: active_reviewed_anchor
created: 2026-06-16
canonical_language: en
---

# A06_16 2x2 Expert-Geometry Gate Anchor

## 0. Tiny Summary

- 父问题：Switch-style MoE 的 router 如何与 expert 结构发生联系，而不是作为与 expert 无关的随机分类器。
- 当前子问题：在两个 expert、二维输入的最小情形下，expert 初始化几何能否诱导一个合理的 routing rule。
- 决策问题：是否存在一个 2D expert-aware gate，同时满足均匀分发与基于度量的 specialization。
- 最小构造：四个二维单位向量，两两组成两个 expert；输入从单位圆均匀采样。
- 核心模型：由 expert 向量构造 prototype，用 \(q_e(x)=x^\top m_e\) 定义 input-expert compatibility。
- 预期判断：若非退化，prototype gate 应给出 50/50 load，并使被选 expert 的 compatibility 最大。
- 边界：这不证明真实 MoE、有语义 feature、训练稳定性、高维可扩展性或 common removal。
- 下一步：先证明并实现 static 2D oracle gate，再进入高维低秩 approximation。

## 1. Problem Definition

Broader question:

```text
How should Switch-style routing be linked to expert structure instead of being learned as an expert-agnostic random classifier?
```

Sharper subproblem:

```text
In the minimal two-expert, two-dimensional setting, can expert initialization geometry define a routing metric that induces both balanced load and metric-defined specialization under uniform input?
```

Decision question:

```text
Does a simple expert-aware 2D oracle gate exist, and can it be implemented as a linear router initialized from expert geometry?
```

Not in scope:

```text
real text;
transformer hidden states;
common component removal;
high-dimensional approximation;
training dynamics;
semantic feature labels;
causal expert utility.
```

Operational definitions:

```text
expert geometry:
the input-side directions represented by an expert's initialized 2x2 matrix.

compatibility:
a scalar score q_e(x) measuring how well input x matches expert e's geometry.

uniformity:
expected routing load is 1/2 for each expert under uniform input.

metric-defined specialization:
an input assigned to expert e has higher compatibility with expert e than with the other expert.
```

## 2. Physical Priors

P1. Expert-aware routing needs expert-side structure.

```text
Meaning:
If experts are expected to specialize, the router should not be independent of expert initialization.

Could be wrong if:
expert initialization has no stable, distinguishable input-side geometry, or the extracted geometry is too degenerate to define a useful metric.
```

P2. Expert initialization directions can induce a spatial partition.

```text
Meaning:
Two experts with different initialized directions can define two different geometric prototypes or metrics, which then divide input space.

Could be wrong if:
the prototypes are identical, ill-defined, or the metric collapses to the same score for both experts.
```

P3. Uniform input should require both load balance and specialization, not load balance alone.

```text
Meaning:
A useful gate must assign roughly equal measure to both experts and must assign inputs by a meaningful compatibility metric. Maybe the partition shoud be aligned with the function or the geometric of the corresponding experts.

Could be wrong if:
the rule gives 50/50 load only by arbitrary splitting, or gives compatibility alignment while producing strong load imbalance.
```

## 3. Falsifiable Hypotheses

H1. A prototype gate induced by expert geometry gives balanced load under uniform 2D input.

```text
Supported if:
for non-degenerate prototypes and x sampled uniformly from S^1, load_1 and load_2 are approximately 0.5 in simulation and exactly 0.5 by the geometric proof.

Weakened if:
the load is systematically imbalanced under uniform input despite a non-degenerate decision boundary through the origin.

Insufficient evidence if:
only a plot is shown without load statistics or proof.
```

H2. The same prototype gate gives metric-defined specialization.

```text
Supported if:
the selected expert has non-negative compatibility margin for every non-boundary input, and the mean margin is positive.

Weakened if:
load is balanced but the selected expert does not have higher compatibility than the other expert.

Insufficient evidence if:
specialization is claimed without defining q_e(x) or a margin.
```

H3. The oracle gate can be implemented as a linear Switch-style router initialization.

```text
Supported if:
setting router rows w_1=m_1 and w_2=m_2 reproduces the oracle assignments.

Weakened if:
the initialized linear router disagrees with the oracle despite using the same score.

Insufficient evidence if:
the oracle rule is analyzed but no router-weight implementation is checked.
```

## 4. Mathematical Model

Objects:

```math
a_1,a_2,a_3,a_4 \in S^1 \subset \mathbb{R}^2
```

```math
A_1=[a_1,a_2], \qquad A_2=[a_3,a_4]
```

Input distribution:

```math
x \sim \mathrm{Unif}(S^1)
```

Expert prototypes:

```math
m_1=\frac{a_1+a_2}{\|a_1+a_2\|}, \qquad
m_2=\frac{a_3+a_4}{\|a_3+a_4\|}
```

The model excludes cases where \(a_1+a_2=0\) or \(a_3+a_4=0\), because the prototype is undefined.

Compatibility score:

```math
q_e(x)=x^\top m_e
```

Oracle gate:

```math
g(x)=\arg\max_{e\in\{1,2\}} q_e(x)
```

Specialization margin:

```math
\Delta(x)=q_{g(x)}(x)-q_{\text{other}}(x)
```

Core mechanism relation:

```math
g(x)=1
\iff
x^\top m_1 \ge x^\top m_2
\iff
x^\top(m_1-m_2)\ge 0
```

The decision boundary is:

```math
x^\top(m_1-m_2)=0
```

For \(m_1\neq m_2\), this boundary is a line through the origin. Therefore, under uniform input on the unit circle or unit disk, it partitions the input measure into two equal halves.

Observable metrics:

```text
load_error = |load_1 - 0.5|
mean_margin = mean_x Delta(x)
min_margin_off_boundary = minimum margin after excluding boundary-near points
router_oracle_agreement = P[g_router(x)=g_oracle(x)]
prototype_angle = angle(m_1,m_2)
```

Falsifier:

```text
A non-degenerate prototype pair produces systematic load imbalance under uniform input, or produces balanced load without positive compatibility margin.
```

## 5. Computational Realization

Input objects:

```text
number of expert seeds;
number of sampled inputs per seed;
four unit vectors per seed;
uniform input points on S^1.
```

Computed variables:

```text
A_1, A_2;
m_1, m_2;
q_1(x), q_2(x);
oracle assignment g(x);
linear-router assignment with w_e=m_e;
load ratio;
specialization margin.
```

Algorithm stages:

```text
1. Generate four unit vectors.
2. Pair them into two 2x2 experts.
3. Compute one prototype per expert.
4. Sample uniform input directions.
5. Assign each input by prototype compatibility.
6. Compute load and margin.
7. Check equivalence to a linear router initialized from prototypes.
8. Run degenerate controls.
```

Expected artifacts:

```text
tables/metrics_by_seed.csv
tables/aggregate_metrics.csv
figures/partition_seed_<id>.png
figures/margin_hist_seed_<id>.png
figures/degen_cases.png
```

## 6. Minimal Falsification Tests

Test 1: Static expert-geometry oracle.

```text
Question:
Can expert prototypes induce a balanced and specialized partition?

Intervention / comparison:
Use q_e(x)=x^T m_e to route uniform x.

Primary metric:
joint_partition_validity = load_error <= epsilon_load and mean_margin > epsilon_margin.

Supports:
near-zero load error and positive margin across non-degenerate random expert seeds.

Weakens:
load balance without positive margin, or positive margin with strong load imbalance.

Insufficient evidence:
only a visual partition without load and margin.
```

Test 2: Linear-router implementation equivalence.

```text
Question:
Can the oracle be implemented as a Switch-style linear router initialization?

Intervention / comparison:
Set router weights w_1=m_1 and w_2=m_2.

Primary metric:
router_oracle_agreement.

Supports:
agreement equals 1.0 up to tie/boundary numerical tolerance.

Weakens:
systematic disagreement away from boundary.

Insufficient evidence:
oracle is defined but no router-weight implementation is checked.
```

Test 3: Degenerate and rival rules.

```text
Question:
Do predicted failure cases fail for the right reason?

Intervention / comparison:
m_1≈m_2;
a_1+a_2≈0;
distance to full span(A_e);
random 50/50 routing.

Primary metric:
failure_reason classification.

Supports:
degenerate prototypes show small/undefined margin;
full-span distance is uninformative;
random split can balance load but fails metric-defined specialization.

Weakens:
failure modes do not match the mathematical diagnosis.

Insufficient evidence:
failure cases are not tested.
```

## 7. Current Evidence

```text
No new 2x2 oracle-gate result exists yet.
This anchor is motivated by the mentor's request to solve the two-expert 2x2 case before high-dimensional approximation and common removal.
Previous collapse audits motivate why expert-aware routing matters, but they are not evidence for this anchor's mathematical claim.
```

## 8. Claim Boundary And Next Decision

Can claim if supported:

```text
A minimal expert-aware oracle gate exists in 2D.
The gate can jointly satisfy balanced load and metric-defined specialization under uniform input.
The gate can be implemented as a linear Switch-style router initialized from expert prototypes.
```

Cannot claim:

```text
This solves real MoE collapse.
This proves semantic feature specialization.
This proves high-dimensional scalability.
This proves training preserves the partition.
This proves common removal is sufficient.
This proves expert functional utility alignment.
```

Next decision:

```text
If the 2D oracle gate is proved and implemented, test whether the same expert-geometry principle can be approximated in high dimension using low-rank expert structure.
```
