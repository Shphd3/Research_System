# Minimal Anchor Handwrite Draft

## 0. Tiny Summary

父问题：为什么 sparse top-1 MoE router 在早期进入 route concentration / expert underuse？

当前子问题：真实 DCLM top-1 MoE 中，为什么 step 0 common dominance 不强，但 step 10 common-logit 和 route concentration 快速放大？

核心假设：early top-1 training 形成 selected-path feedback；common component 先作为 load-bias source，再被 gate / hidden / expert feedback 放大。

最小测试：保存 0--300 step 的 W_t 和 H_t，做 W_a H_b cross-checkpoint replay；再用 freeze gate / freeze experts / freeze hidden producer 做 causal split。

当前边界：只解释 small random-initialized Qwen-style top-1 MoE on DCLM early training；不解释 pretrained large MoE 或最终 expert specialization。

下一步决策：判断 amplification 主要来自 gate、hidden、expert feedback，还是交互。

## 1. Problem Definition

Parent problem: 
Why do sparse dot-product top-1 MoE routers enter early route collapse or expert underuse?

Sharper subproblem:
Why does real-text sparse top-1 routing rapidly amplify route and common-logit concentration during the first 300 optimizer steps, with the strongest early spike around step 10?

Decision question:
In real DCLM top-1 MoE, is early common-logit amplification mainly caused by gate update, hidden-state producer drift, expert-output feedback, or their interaction?

Not in scope:

1. deployable mitigation method;
2. pretrained or large-scale MoE behavior;
3. final expert utility specialization;
4. mentor-style expert-spectrum initialization.

## 2. Physical Prior

P1:
The router-input common component is stable across early batches and checkpoints.

Meaning:
If the common direction is batch-stable, repeated LM gradients can accumulate coherent gate updates along this shared direction.

Could be wrong if:
The estimated common directions have low cross-batch cosine similarity, low subspace overlap, or no stable common-winner persistence.

P2:
Sparse top-1 routing creates selected-path feedback and gradient starvation.

Meaning:
The selected expert receives token traffic, task gradient, and output feedback; under-selected experts receive weaker corrective signal.

Could be wrong if:
Early route interventions or gate freezing do not change later route concentration, or non-selected experts receive sufficient corrective gradient to recover balanced routing.

P3:
Expert-output feedback can reshape future router inputs and reinforce early route choices.

Meaning:
Selected experts are not passive receivers. Their outputs can change downstream hidden states and later router inputs, making an early common-logit winner more persistent.

Could be wrong if:
Blocking expert-output feedback preserves the same step-10 common-logit amplification.

## 3. Hypothesis

H1:
The early common component is stable across batches and checkpoints within the same layer.

Supported if:
cos(c_t, c_0), top-k subspace overlap, and common-winner persistence remain high from step 0 to step 10/300.

Weakened if:
common directions rotate strongly while route concentration still appears.

H2:
Gate update alone can reproduce most of the early common-logit amplification.

Supported if:
W_10 H_0 reproduces most of the increase from W_0 H_0 to W_10 H_10, and freeze_gate suppresses the spike.

Weakened if:
W_10 H_0 stays close to W_0 H_0, or freeze_gate does not suppress concentration.

H3:
Hidden-state producer drift or expert-output feedback is necessary for the early amplification.

Supported if:
W_0 H_10 explains a large fraction of the spike, or freeze_experts / block expert feedback suppresses step-10 concentration.

Weakened if:
W_10 H_0 already reproduces the spike and expert-feedback interventions have little effect.

## 4. Minimal Mathematical Model

Objects:

$$
h_{t,i}=c_t+r_{t,i},\quad
W_t=W_0+\Delta W_t,\quad
z_{t,i,e}=w_{t,e}^{\top}h_{t,i}
$$

Core decomposition:

$$
z_{t,i,e}
=
w_{0,e}^{\top}c_0
+
w_{0,e}^{\top}r_{0,i}
+
\Delta w_{t,e}^{\top}c_0
+
w_{0,e}^{\top}\Delta c_t
+
\Delta w_{t,e}^{\top}r_{0,i}
+
w_{0,e}^{\top}\Delta r_{t,i}
+
\text{higher-order terms}.
$$
Mechanism relation:

W_t H_0 -> gate update
W_0 H_t -> hidden drift
W_t H_t -> actual
freeze experts -> expert feedback

Observable metrics:

common_margin_t
residual_margin_t
dominance_ratio_t
raw_max_load_t
centered_max_load_t
delta_max_load_t
routing_entropy_t
dominant_expert_persistence_t

Falsifier:
If neither W_t H_0, W_0 H_t, W_t H_t, nor common-centering changes explain the step-10 spike, then the current common-logit amplification model is insufficient.

## 5. Minimal Tests

Test 1: Normal 300-step trajectory
Question: Does step-10 amplification reproduce and how does it evolve by step 300?
Primary metric: common_margin, dominance_ratio, raw_max_load, centered_max_load.

Test 2: Cross-checkpoint replay
Question: Does amplification live in W, H, or their interaction?
Intervention: compute W_a H_b for checkpoints 0, 1, 2, 3, 5, 10, 20, 50, 100, 300.
Primary metric: fraction of common_margin amplification explained by W_10 H_0 and W_0 H_10.

Test 3: Freeze split
Question: Which causal path is necessary?
Intervention: normal / freeze_gate / freeze_experts / freeze_hidden_producer.
Primary metric: suppression of step-10 dominance_ratio and raw_max_load.

## 6. Falsifiable Outcomes

Supported:
One causal path or interaction explains most of the W_10 H_10 amplification and is confirmed by a matching freeze intervention.

Weakened:
Replay shows no clear W/H/interaction source, or freeze interventions do not change the spike.

Insufficient evidence:
Only max_load is reported; exact gate input is not audited; audit batch changes across checkpoints; shared expert or load-balance loss contaminates interpretation.

## 7. Current Evidence

Observation:
At step 0, common_margin=0.1237, residual_margin=0.2364, dominance_ratio=0.5251. This weakens pure step-0 common dominance.

Observation:
At step 0, raw_max_load=0.2781 and centered_max_load=0.1561. This supports common as a load-bias source.

Observation:
At step 10, common_margin=0.7427, residual_margin=0.0707, dominance_ratio=21.7874, raw_max_load=0.8507. This supports early-training amplification as the next mechanism to explain.

## 8. Claim Boundary And Next Decision

Can claim:
For this small random-initialized Qwen-style top-1 MoE on DCLM, common component is a real load-bias source and is strongly amplified during early training.

Cannot claim:
We know whether gate update, hidden drift, or expert-output feedback causes the step-10 spike.
We explain final expert specialization.
We solve MoE collapse.
This applies to pretrained large MoE.

Next decision:
Run cross-checkpoint replay plus freeze split to identify the dominant causal path of early common-logit amplification.
