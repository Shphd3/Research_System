# Decision 1: Test Whether Common-Aligned Router Winners Are Amplified By Early Top-1 Training

## Thinking Card

当前事实：第 0 步负载最高的 expert，也是 router 向量与 common direction 余弦最对齐、且 $w_e^\top c$ 最大的 expert。

当前疑问：这个初始 common-aligned winner 是否会在 Top-1 MoE 早期训练中被 router 更新进一步放大，从而扩大它的路由区域？

下一步决策：值得推进一个小型更新方向审计。它直接连接 06_01 的初始化偏置和 06_02 的早期 common-logit 放大，是当前主线中最紧的 causal bridge。

## Question

Does the early Top-1 MoE training process amplify the router vector that is initially most aligned with the common router-input direction?

More concretely:

```text
At step 0:
load winner = argmax_e count(argmax_j w_j^T h_i = e)
             = argmax_e w_e^T c
             = argmax_e cos(w_e, c)

During early training:
does this winner's common-direction projection increase relative to other experts?
```

## Why This Matters

This is the missing link between two existing results:

1. A05/A06 initialization audit:
   random Top-1 routers already have a load-favored expert at step 0, and this expert is the one most aligned with the common hidden-state direction.

2. A06_02 early-training audit:
   common-margin and raw route concentration spike quickly by step 10, but the spike is not explained by gate-only replay alone.

If the initially common-aligned router row receives reinforcing updates, then the story becomes:

```text
random geometric advantage
-> higher initial top-1 load
-> biased early router / hidden feedback
-> expanded route region
-> severe early load concentration
```

If not, then the step-10 concentration is more likely caused by hidden-state drift, position structure, expert-output feedback, or gate-hidden interaction rather than simple router self-reinforcement.

## Current Evidence

Step-0 common alignment audit:

```text
projection winner == cosine winner: 18 / 18
projection winner == raw load winner: 18 / 18
mean cos(w_e, c) of winner: ~0.068
range: ~0.026 to ~0.112
mean gate-vector norm CV: ~0.030
max gate-vector norm CV: ~0.053
```

Interpretation:
The winner is not mainly winning because its router-vector norm is larger. Router row norms are close, and the load winner is consistently the most angle-aligned row with the common direction.

Existing route-load evidence:

```text
step0 raw_max_load:      0.2781
step0 centered_max_load: 0.1561
uniform baseline:        0.1250
```

Interpretation:
The common component is not the dominant single-token margin source, but it is a measurable load-bias source.

Existing early-training evidence:

```text
step0 raw_max_load: 0.2781
step10 raw_max_load: 0.8507
```

Interpretation:
Early training strongly amplifies route concentration, but the exact update path still needs to be decomposed.

## Hypothesis

H1:
The initially common-aligned router winner receives a positive common-direction update during early training.

Operational form:

$$
\Delta w_{winner}^{(t)} \cdot c_t > 0
$$

and the winner's projection margin increases:

$$
\max_e w_e^{(t)\top}c_t - \mathrm{secondmax}_e w_e^{(t)\top}c_t
$$

H2:
Non-winner router rows are not equally reinforced along the common direction, so the winner-vs-others common projection gap expands.

H3:
If this mechanism is real, the load winner, common-projection winner, and cosine-alignment winner should remain coupled during the first few steps, especially before the step-10 spike.

## Main Vulnerability

This hypothesis can be wrong because early concentration does not have to come from router rows alone.

Rival explanations:

```text
1. hidden-state common direction rotates or grows;
2. residual hidden geometry becomes more anisotropic;
3. position-specific structure concentrates routes;
4. expert outputs reshape downstream router inputs;
5. gate-hidden interaction dominates over direct router self-reinforcement.
```

Therefore, this decision should not claim that router update is already the cause. It should only test whether the direct router-update channel exists and how large it is.

## Minimal Test

Use existing checkpoints from the early-training run if available. Otherwise run a short 0--10 step trajectory with the same DCLM audit batch.

For each seed, layer, and checkpoint $t \in \{0,1,2,3,5,10\}$:

```text
c_t = mean router input on fixed audit tokens
s_e(t) = w_e(t)^T c_t
a_e(t) = cos(w_e(t), c_t)
load_e(t) = fraction of tokens routed to expert e
```

Track:

```text
load_winner(t)
projection_winner(t)
cosine_winner(t)
winner_projection_margin(t)
winner_cosine_margin(t)
raw_max_load(t)
centered_max_load(t)
```

Then decompose router updates:

```text
delta_w_e(t) = w_e(t+1) - w_e(t)
common_update_e(t) = delta_w_e(t)^T c_t
common_update_cos_e(t) = cos(delta_w_e(t), c_t)
```

Primary metric:

```text
winner common projection margin from step 0 to step 10
```

Secondary metric:

```text
whether the initial load winner has larger common_update_e than the expert average
```

## Decision Rule

Support router self-reinforcement if:

```text
1. initial load winner remains projection/cosine winner through early steps;
2. winner_projection_margin increases before or by step 10;
3. delta_w_winner^T c_t is positive and larger than the expert mean;
4. the increase correlates with raw_max_load growth.
```

Weaken router self-reinforcement if:

```text
1. projection/cosine winner changes frequently;
2. winner_projection_margin does not increase;
3. delta_w_winner^T c_t is not positive or not larger than others;
4. raw_max_load grows while router common projection stays flat.
```

If weakened, shift focus to:

```text
hidden-state drift,
residual anisotropy,
position structure,
or expert-output forward feedback.
```

## Claim Boundary

Can claim after this test:

```text
whether early router row updates directly amplify the initially common-aligned winner in this small random-init DCLM Top-1 MoE setting.
```

Cannot claim from this test alone:

```text
that router self-reinforcement is the only cause of step-10 concentration;
that the mechanism transfers to pretrained MoE, Top-2/Top-4 routing, load-balanced training, or shared-expert models;
that common alignment alone explains useful expert specialization.
```

## Recommended Next Action

Run a focused posthoc audit first:

```text
input: existing checkpoints from A06_02 / A05 phase3 if available
output: router_common_alignment_trajectory.csv
scope: seeds 0--2, layers 0--5, steps 0/1/2/3/5/10
```

Only run a new experiment if the existing checkpoints do not contain enough router weights and exact audit-batch hidden states.
