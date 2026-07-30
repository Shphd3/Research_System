# Agent Runbook: 0531_auto_route_function_binding

## 0. Operating Rule

Do not optimize for running many jobs. Optimize for reducing one uncertainty:

```text
Can we make route assignment bind to target-deciding feature and expert causal utility under NTP?
```

Every stage must end with:

```text
observation / interpretation / claim boundary / next decision
```

## 1. Startup Checklist

Read:

```text
AGENTS.md
PROJECTS.md
.agents/skills/research-progress-core/SKILL.md
.agents/skills/problem-anchor-writer/SKILL.md
.agents/skills/experiment-card-writer/SKILL.md
.agents/skills/remote-experiment-workflow/SKILL.md
sync/S000_current_specialization/README.md
sync/S000_current_specialization/anchors/expert_specialization/slot_context_dominance_router_specialization_anchor.md
sync/S000_current_specialization/anchors/expert_specialization/hierarchical_route_utility_binding_anchor.md
daily_research_reports/0529/meeting/group_meeting_thought_update.md
```

Confirm active route:

```text
feature-level expert specialization
-> baseline gating failure
-> route-function binding
-> downstream effects only after specialization
```

## 2. Work Boundary

Research_System owns:

```text
anchor, execution plan, summary.md, detailed.md, handoff report, graph proposal, claim boundary, next decision.
```

Remote experiment codebase owns:

```text
code edits, debug runs, full runs, raw outputs, checkpoints, figures, tables, logs.
```

Do not commit raw logs/checkpoints unless explicitly curated.

## 3. Half-Night Schedule

### Phase A: Preflight and Smoke, 0-60 min

1. Verify repo state and code workspace.
2. Implement or locate route-binding runner.
3. Run T0 2x2 smoke.
4. Generate first table:

```text
case | expected | observed route | loss | pass/fail
```

Stop if T0 fails. Debug objective before proceeding.

### Phase B: Baseline and Attribution, 60-180 min

1. Run T2 multi-B uniform baseline for 2 seeds.
2. Confirm slot probe/oracle if available.
3. Save hidden states, logits, routes.
4. Run factor attribution:

```text
R2(logit, common/B/slot/head factors)
route changes under component swap
route NMI by feature vs B identity
```

Decision:

```text
If router controlled by wrong factor -> test C1.
If utility missing -> test C6.
If utility exists but gate mismatch -> test C2.
If linear boundary fails under distributed code -> test C4.
```

### Phase C: Candidate Smoke, 180-300 min

Run 2 seeds each for selected candidates only. Default shortlist:

```text
C1_residual_linear
C2_utility_binding
C5_residual_plus_binding
C4_nonlinear_gate only if C1/C2 insufficient or factor boundary nonlinear
C6_tail_writein_pressure only if forced utility is missing
```

Minimal table:

```text
model | CE | route_feature_NMI | route_B_NMI | assignment_utility | forced_diag_margin | BindingPass | failure
```

Pick at most 2 candidates for full run.

### Phase D: Selective Full Run, 300-420 min

For top 1-2 candidates:

```text
5-10 seeds on T2/T3 uniform
heldout B test
checkpoint stability
noise perturbation
```

Only add Zipf T4 if uniform binding passes.

### Phase E: Documentation, 420-480 min

Write:

```text
summary.md
detailed.md
anchor update section
artifact map
graph_update_proposal if needed
```

Must include:

```text
central tables
central figures embedded
failed/ambiguous runs
claim boundary
next smallest decision
```

## 4. Autonomous Decision Rules

### Rule 1: Do Not Trust A Single Metric

Reject if:

```text
CE improves but BindingPassRate does not.
route_feature_NMI improves but forced_loss_diag_margin does not.
assignment_utility improves but route_feature_NMI collapses.
```

### Rule 2: Stage-Gated Expansion

Do not add Zipf until uniform passes.
Do not add real-corpus proxy until synthetic route-function binding passes.
Do not add hierarchy depth unless factor attribution says root/leaf factor split is the bottleneck.

### Rule 3: Negative Result Is Progress

If candidate fails, write which level failed:

```text
physical prior / mathematical model / operationalization / implementation / metric
```

### Rule 4: Keep Methods Comparable

For every candidate, record:

```text
active compute
number of experts
router parameters
expert parameters
training steps
total tokens/samples
seeds
init type
load balance coefficient
```

## 5. Minimal Figures

Generate at least:

```text
figures/route_heatmap_baseline_vs_best.png
figures/forced_loss_heatmap_baseline_vs_best.png
figures/checkpoint_binding_trajectory.png
figures/factor_attribution_router_logits.png
```

Each figure needs one sentence:

```text
Supports: <claim it supports>
Cannot prove: <claim it cannot prove>
```

## 6. End State

At the end, there must be one of these decisions:

```text
A. residualized representation is the next mainline;
B. explicit utility-binding regularizer is the next mainline;
C. nonlinear gate is necessary and worth isolating;
D. linear gate + prior/margin works only diagnostically and needs real-plausible proxy;
E. router-only fixes fail because feature write-in is missing;
F. evidence is insufficient because implementation/metric failed.
```

No other ending is acceptable.
