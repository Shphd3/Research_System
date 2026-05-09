# Slide Outline - Feature-Zipf Synthetic Hierarchical MoE

## Slide 1: Main Message

Title: Feature-Zipf Synthetic 实验给出的当前 claim boundary

Message:

Hierarchical MoE 有 function-level recovery 信号，但还没有证明比 flat middle spectral 更会做 sparse feature division。

Show:

- One-sentence takeaway
- Claim boundary: can say / cannot say

## Slide 2: Why Feature-Zipf

Message:

这次 synthetic 的关键改动是：Zipf 作用在 sparse feature 出现频率上，而不是直接作用在 leaf label 上。

Show:

- common / group / unique feature table
- formula for $h$
- why this is closer to language

## Slide 3: Experiment Setup

Message:

variable-A 测 function recovery，fixed-A 测 input feature 是否诱导 routing differentiation。

Show:

- variable-A formula
- fixed-A formula
- model list: random, flat, middle spectral, hier, oracle
- metrics: loss, Leaf NMI, feature selectivity, function cos, sparse dict metrics

## Slide 4: Main Results

Message:

Oracle proves recoverability; learned models beat random; hierarchy helps function cos but not Leaf NMI.

Show:

- compact table with variable-A highlights
- highlight function cos for Hier conditional_input
- highlight Leaf NMI for flat middle spectral

## Slide 5: Sparse Dictionary Diagnosis

Message:

Sparse dict 诊断说明 middle spectral 是当前最强 feature-division signal。

Show:

- atom selectivity / diversity / overlap table
- oracle as upper bound
- statement: Hier > random, but not > flat middle spectral

## Slide 6: Interpretation And Next Step

Message:

Specialization must be split into feature-level and function-level. Next step is to explain middle spectral and unify it with hierarchy.

Show:

- two-axis specialization diagram:
  - feature-level
  - function-level
- next experiments:
  - frequency-band routing entropy
  - spectral range ablation
  - middle spectral + hierarchy combination

## Backup Tables

- full variable-A result table
- fixed-A result table
- sparse dictionary stability table
- PCA log-y spectrum figure
