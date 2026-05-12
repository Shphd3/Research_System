# Consensus / Known Knowledge - 0512

## Purpose

This file records what we inherit from previous reports and what remains unproven for the current route-guided KV retrieval project.

## Known From main_cn.pdf

1. MoE inference has a memory problem: token-level routing is sparse, but a sequence can activate many experts, forcing many experts to stay in GPU memory.
2. Prior analysis suggests MoE routing is partly predictable because gate decisions are sensitive to dominant low-dimensional spike features in hidden activations.
3. The same analysis gives a mixed conclusion: routing may be predictable, but naive expert swapping is bandwidth-limited and expensive.
4. The proposed H-MoE / Common-Unique design organizes experts hierarchically with always-active common experts and conditional unique experts.
5. In the preliminary <0.5B parameter-budget setting, H-MoE training loss is close to flat MoE, with only a small gap.

## Known From Draft.docx

The draft motivation is:

- data feature activation is long-tailed;
- data feature activation is sparse;
- data features have hierarchical structure;
- the intended purpose is to test whether hierarchical MoE learns this kind of data better;
- the stated draft conclusion is that H-MoE experts are more feature-specialized and old-feature distribution is more stable after learning new data.

Reliability: weak. The draft is an early motivation document, not the final executable experiment spec.

## Known From the Continual-Learning Diagnostic Report

The executable prior experiment is not the draft global/middle/leaf design. It is an atom-rule-task synthetic continual regression benchmark.

Main result:

- Flat forgetting MSE increase: 0.0497270364.
- H-MoE forgetting MSE increase: 0.0382086334.
- Relative reduction vs flat: about 23.16%.
- H-MoE Task B final MSE is slightly worse than flat.

Reliable claim:

- Under the exact synthetic continual-regression benchmark and matched total/active parameter budget, H-MoE reduces Task A MSE forgetting relative to flat top-1 MoE.

Weak interpretation:

- H-MoE may provide a better inductive bias for separating latent rule/task updates.

Unreliable extrapolation:

- It does not prove real language-model MoE forms the same feature hierarchy.
- It does not prove inference speedup.
- It does not prove router specialization without stronger metrics.

## How We Use Prior Work

We inherit:

- H-MoE Common-Unique design.
- Flat vs H-MoE matched-budget comparison.
- Routing heatmaps and routing specialization metrics.
- Need for load-balancing loss in flat MoE.
- Claim-boundary discipline.

We do not inherit:

- continual learning as the main objective;
- CL forgetting as the primary metric;
- any claim about real inference speedup;
- any proof that learned routing is a valid KV retrieval index.

## Current Consensus

The current project should test route-guided attention retrieval, not continual learning. The first closed loop must answer whether expert/path buckets ranked by router logits can recover the tokens that matter to dense attention.
