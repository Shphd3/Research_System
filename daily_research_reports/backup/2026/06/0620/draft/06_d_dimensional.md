# Minimal Anchor Handwrite Draft

This is rough thinking for AI audit. It is not a final anchor.

## User Control

Preserve:

Do not silently change:

Unclear / risky:

Candidate priors:

## 0. researcher judgment record

总目标：是否存在一种gating 初始化的方式，能够使得gating初始化的时候让hidden states 均匀分发到不同的experts上，从而缓解早期的负载不均导致的路由坍缩。

父问题：是否存在一种高维的Gating初始化方式，能够使得feature均匀分布的时候，能够均匀将feature分到不同的experts上面？

当前子问题：高维情形下，load balance来自于 token的取样方差、gauss初始化的prototype位置方差，还是中心向量的norm方差？

当前判断：

二维情形下：token sampling样本方差随着采样趋近于零，负载不均衡的来源更多来自于有限个gating中心的不均匀分布。
高维情形下：高维向量都近似正交，但是线性router一般 gating 初始模长会有区别。

关键证据：

最危险边界：

下一步决策：

### researcher judgment record Audit

Question: 

Physical prior:

Core model:

Model term being tested:

Primary metric:

Falsifier:

Can claim:

Cannot claim:

Next decision:

## 1. Problem Definition

Parent problem:

Sharper subproblem:

Decision question:

Not in scope:

## 2. Physical Priors

P1:

Meaning:

Could be wrong if:

## 3. Falsifiable Hypotheses

H1:

Supported if:

Weakened if:

## 4. Mathematical Model

Objects:

Core decomposition:

Mechanism relation:

Observable metrics:

Falsifier:

## 5. Computational Realization

Input objects:

Computed variables:

Algorithm stages:

Stage-local evidence:

Expected artifacts:

## 6. Minimal Falsification Tests

Test:

Question:

Intervention / comparison:

Primary metric:

Supports:

Weakens:

Insufficient evidence:

## 7. Current Evidence

Observation:

Interpretation:

Boundary:

Evidence links:

## 8. Claim Boundary And Next Decision

Can claim:

Cannot claim:

Next decision:
