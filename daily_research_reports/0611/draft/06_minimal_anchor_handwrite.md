# Minimal Anchor Handwrite Draft

## 0. Tiny Summary

父问题：sparse top-1 MoE router 为什么在早期进入 route collapse / expert underuse？

当前子问题：DCLM real-text 上，random-initialized sparse top-1 dot-product MoE 在 step 0 / early steps 是否已有 common-logit-driven route concentration？

核心假设：h_i 可分解为 c + r_i，random router rows 对 c 的不同投影形成 expert-specific common bias。

最小测试：冻结 hidden states + 随机 top-1 router + expert-count sweep + common removal control。

当前边界：只审计 initialization geometry，不测试完整 MoE 训练，不声称新初始化方法有效。

下一步决策：若支持，再进入 label-free common-aware initialization / router-input control。

## 1. Problem Definition

Parent problem:
Why do sparse dot-product top-1 MoE routers enter early route collapse or expert underuse?

Sharper subproblem:
Do random-initialized real-text MoE hidden states contain a common component that becomes an expert-specific router offset at step 0 / early training?

Decision question:
On DCLM real-text data, does a random-initialized sparse top-1 dot-product MoE produce route concentration because w_e^T c dominates w_e^T r_i, and does this dominance worsen with expert count?

Not in scope:

- Not training a full MoE LM.
- Not proposing a deployable initialization method.
- Not claiming functional expert specialization.

## 2. Physical Prior

P1: Frozen real/semi-real hidden states contain a stable shared component or low-dimensional common subspace.

Meaning:
Token identity, prompt template, position, domain/task context, or normalization structure may create directions shared across many samples.

Could be wrong if:
The estimated common component is weak, unstable across batches/layers, or mostly noise.

P2: Random dot-product router rows project the common component differently across experts.

Meaning:
a_e = w_e^T c acts as a feature-independent but expert-specific logit offset.

Could be wrong if:
The spread of a_e is small relative to residual/feature logits.

P3: Increasing expert count increases the chance of an extreme common-projection winner.

Meaning:
With more random rows, max_e w_e^T c can become more extreme, increasing expert underuse risk.

Could be wrong if:
Router normalization, hidden-state geometry, or residual margins dominate this extreme-value effect.

## 3. Hypothesis

H1: Random-initialized real-text router-input hidden states contain a nontrivial common component c.
common_ratio and cross-split common direction stability are high, and residuals still preserve feature/residual structure.

Weakened if:
estimated common direction is unstable or common removal destroys all residual structure.

H2: The common projection w_e^T c creates an expert-specific logit gap larger than the residual projection w_e^T r_i.

common_margin > residual/feature_margin, and argmax_e w_e^T c predicts many token route winners.

Weakened if:
route winners are mainly explained by residual/feature logits, not common logits.

H3: Increasing expert count increases common-winner dominance and expert underuse.
Supported if:
max_load, entropy drop, active-expert drop, or common-winner dominance worsen as E increases.

Weakened if:
Experts-scaling looks like matched random routing or remains balanced.

## 4. Minimal Mathematical Model

Objects:
h_i: hidden state of sample/token i.
c: estimated common component or common subspace.
r_i: residual / feature-carrying component after removing common.
w_e: random router row for expert e.
z_{i,e}: router logit.

Core model:
h_i = c + r_i
z_{i,e} = w_e^T h_i = w_e^T c + w_e^T r_i

Mechanism relation:
If max_e w_e^T c has a large gap, the common term acts as an expert-specific offset shared across tokens and can dominate top-1 routing.

Observable metrics:
common_margin, residual/feature_margin, common-winner agreement, max_load, entropy, active experts, feature_NMI / cluster_NMI.

Falsifier:
If common_margin is not large and common removal does not reduce route concentration, common-logit bias is not the main explanation for real hidden-state initialization collapse.

## 5. Minimal Tests

Test 1: Step-0 common-logit audit.
Question:
At random initialization on DCLM real text, does common_margin exceed residual_margin and predict dominant routing?

Test 2: Virtual expert-count scaling.
Question:
For the same hidden states, does increasing virtual E increase common_margin, dominance_ratio, and expert underuse?

Test 3: Early-training / actual E validation.
Question:
Does early training preserve or amplify the same common-winner bias, and does actual E scaling worsen early underuse?

## 6. Falsifiable Outcomes

Supported if:

- random router on real hidden states shows high route concentration;
- common-winner agreement is high;
- common removal lowers route concentration;
- expert-count scaling worsens concentration.

Weakened if:

- random routing is close to matched random baseline;
- common margin is not larger than residual/feature margin;
- common removal does not change route concentration.

Insufficient evidence if:

- load becomes balanced but feature/residual alignment is not measured;
- only one model, one layer, one dataset, or one seed is tested;
- common removal changes everything, including useful residual structure.

## 7. Current Evidence

Observation:
In the controlled toy setting, common-logit dominates early routing and common-logit cancellation improves slot-level specialization.

Interpretation:
This suggests common-logit bias is an intervention-relevant causal factor in the controlled setting.

Boundary:
Real/semi-real hidden-state evidence is not established yet; this anchor tests whether the same geometry exists beyond toy data.

## 8. Claim Boundary And Next Decision

Can claim if supported:
Initialization-time common-logit geometry is visible in real/semi-real representation spaces.

Cannot claim:

- common-aware initialization is already deployable;
- full MoE training collapse is solved;
- load balance equals feature specialization;
- functional expert specialization is proven.

Next decision:
If supported, proceed to label-free common-aware router initialization or router-input common control.
If weakened, return to representation-source audit or training-dynamics explanation.
