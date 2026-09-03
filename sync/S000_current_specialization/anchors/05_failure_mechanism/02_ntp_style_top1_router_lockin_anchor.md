---
parent_node: problem.moe_expert_specialization
status: promoted_project_evidence
source_sandbox: daily_research_reports/backup/2026/05/0531/exp_2x2_understanding/
---

# 2x2 Top-1 Router Lock-In Anchor


## Problem

Broader question:

```text
Why does ordinary top-1 MoE gating fail to produce stable, interpretable
feature-level expert specialization?
```

Minimal sandbox question:

```text
In a 2-feature / 2-expert top-1 NTP-style setting, does route collapse come
from early top-1 lock-in, and can better initial router geometry preserve
route-pattern separation?
```

## 2. Physical Priors
1. Top-1 routing converts a small logit difference into a discrete training
   path.
2. The unselected expert receives no token update, so early imbalance can
   become starvation.
3. Router bias can create a shared expert preference across tokens.

For $h_A=e_1,h_B=e_2$:

$$
z(h)=W_rh+b,\qquad p(e|h)=\operatorname{softmax}(z(h)).
$$

Define:

$$
\delta_A=z_{A,E1}-z_{A,E0},\qquad
\delta_B=z_{B,E1}-z_{B,E0}.
$$

If $\delta_A$ and $\delta_B$ have the same sign, A/B select the same expert. If
they have opposite signs, A/B split across experts.

## Hypothesis / Conjecture

```text
Top-1 route-pattern specialization is path dependent.
Initial same-expert assignment causes lock-in and expert starvation.
Initial split assignment is amplified into stable routing and expert advantage.
```

## Minimal Decisive Test

Use only the NTP-style top-1 proxy:

```text
features: h_A=e1, h_B=e2
targets: A_next, B_next
router: linear top-1 selected-gate router
experts: two linear experts
objective: next-token CE
checkpoints: 0, 10, 50, 100, 200, 300
```

Primary evidence:

```text
NMI trajectory
selected gate trajectory
expert usage / update norm
counterfactual CE per forced expert
initial router delta signs
```

## Current Evidence

Early lock-in audit:

```text
Failed seeds are already collapsed at step 0.
Selected gate rises quickly by step 10 and reaches about 0.985 by step 300.
Unselected expert has zero usage for these tokens.
Counterfactual CE shows the selected expert learns both A/B targets.
```

Success dynamics audit:

```text
Successful seeds start with A/B split at step 0.
The split stays stable through step 300.
Selected logit margin rises from near 0 to about 2.
Selected expert becomes much better than unselected expert for its token.
```

No-router-bias audit:

```text
with bias:  random-router split 3/10 -> final split 3/10
no bias:    random-router split 6/10 -> final split 6/10
router prior: known-good split 10/10 -> final split 10/10
```

Main evidence files:

```text
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/summary.md
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/detailed.md
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/report_card.md
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/figures/ntp_style_lockin_audit.png
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/figures/ntp_style_success_dynamics_audit.png
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/figures/ntp_style_no_router_bias/summary_by_seed.png
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/tables/ntp_style_lockin_audit.csv
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/tables/ntp_style_success_dynamics_audit.csv
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/tables/ntp_style_router_bias_comparison.csv
```

## Claim Boundary And Next Decision

Safest current claim:

```text
In this minimal top-1 NTP-style proxy, route collapse is mainly explained by
early top-1 lock-in and expert starvation. Initial split can be amplified into
stable route-pattern separation. Router bias worsens collapse by adding shared
expert preference, but removing bias only partially improves split rate.
```

What cannot be claimed:

```text
This proves utility-aligned specialization.
This directly transfers to full LM or attention settings.
This fully explains ABC synthetic failure.
```

Next smallest decision:

```text
Test one anti-lock-in mechanism:
structured router initialization / exploration noise / load-balancing.
```
