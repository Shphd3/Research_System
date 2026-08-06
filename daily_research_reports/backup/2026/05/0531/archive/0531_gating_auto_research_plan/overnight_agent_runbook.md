# Overnight Agent Runbook: 0531 Gating Auto Research

## 0. Hard Rule

Do not start from scripts. Start from the anchor and decision question.

Required read order:

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
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/stable_route_function_binding_anchor.md
```

If a listed project path is missing locally, use the root `sync/` copy and this 0531 plan folder, then record the missing path in `detailed.md`.

## 1. Goal For This Auto-Research Session

Goal:

```text
Find or eliminate the first plausible mechanism for stable feature-level routing under synthetic NTP.
```

The session should not try to solve real-corpus routing. It should produce a clean decision:

```text
representation decomposition / residual router
or explicit route-function binding regularizer
or expert write-in pressure
or nonlinear/prior router
or metric/data construction repair
```

## 2. Work Surface

Research-process repository:

```text
Research_System
```

Experiment code workspace from previous runs:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
```

Experiment docs to write:

```text
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/summary.md
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/detailed.md
```

Root anchor copy after update:

```text
sync/S000_current_specialization/anchors/expert_specialization/stable_route_function_binding_anchor.md
```

Daily package:

```text
daily_research_reports/0531/gating_auto_research_plan/report.md
```

## 3. Preflight

Run from the experiment workspace:

```bash
hostname
pwd
git status --short --branch
python --version
nvidia-smi || true
```

Check previous runner exists:

```bash
ls scripts/run_hierarchical_route_utility_binding.py
ls configs/hierarchical_route_utility_binding.json
```

If previous runner exists, reuse its data/model code for H0531a. Do not reimplement synthetic data from scratch unless necessary.

## 4. Execution Tree

### Step A: Implement H0531a only

Create:

```text
scripts/run_router_factor_attribution.py
configs/router_factor_attribution_0531.json
```

Minimum implementation:

```text
1. train or load flat_top1/common_flat checkpoints;
2. log h_B, router logits, routes, expert outputs;
3. compute probes for slot/B/frequency;
4. compute router factor sensitivity under component edits;
5. compute forced expert CE matrix;
6. compute decision metrics;
7. save tables and figures.
```

Do not implement H0531b/c/d before H0531a produces at least smoke evidence.

### Step B: Smoke H0531a

Run one condition, one seed, short steps.

Smoke pass requires:

```text
training completes;
target CE/acc logs exist;
hidden states/logits/routes are saved;
probe table exists;
forced expert loss table exists;
at least one figure is generated;
summary smoke note is written in detailed.md or logs.
```

If smoke fails:

```text
stop broad experiments;
write failure reason;
fix only the failed stage;
rerun smoke.
```

### Step C: Full H0531a

Run:

```text
multi_b_64_A_long
multi_b_64_B_long
multi_b_256_B_long
flat_top1
common_flat
4 seeds
```

If compute is limited, prioritize:

```text
multi_b_64_B_long and multi_b_256_B_long
flat_top1 and common_flat
```

### Step D: Analyze H0531a before choosing next experiment

Write a decision table:

```text
Dominant router factor
Expert utility structure
Failure diagnosis
Next intervention
```

Decision gate:

| H0531a finding | Next action |
|---|---|
| common/B or head-frequency dominates route logits | run H0531b true_common_residual + learned residual smoke |
| expert utility is diagonal but router does not select it | run H0531c utility-binding KL smoke |
| expert utility is collapsed or tail/slot not written | run write-in pressure / reweight variant before router architecture |
| metrics disagree or probes/oracle fail | repair data/metric; do not run architecture sweep |

### Step E: Conditional H0531b or H0531c

Run only the branch justified by H0531a.

Minimum conditional run:

```text
one diagnostic condition
one seed smoke
then two-seed short full if smoke passes
```

Do not run H0531d unless:

```text
H0531b and H0531c are both insufficient or negative, and the failure suggests router capacity/interaction is the bottleneck.
```

## 5. Documentation During Run

Append to `detailed.md` after each stage:

```text
stage
command
input files
output files
passed / failed / unclear
failure reason
what this rules out
```

Never leave only raw logs. Every result needs interpretation.

## 6. Required End State

At the end of the session, produce:

```text
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/summary.md
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/detailed.md
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/tables/
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/figures/
updated stable_route_function_binding_anchor.md
root sync anchor copy
```

If only partial runs finished, `summary.md` still must state:

```text
what was tested
where evidence is
what passed
what failed
why it failed if known
what next concrete decision is
```

## 7. End-of-Session Report Card

Use this exact structure:

```markdown
# 0531 Gating Auto Research Report Card

## 0. Decision

## 1. What Was Tested

## 2. Strongest Evidence

## 3. What Passed

## 4. What Failed Or Stayed Ambiguous

## 5. Claim Boundary

## 6. Next Run

## 7. Artifact / Repro Map

code workspace:
runner:
config:
result dir:
figure dir:
tables:
logs:
repro command:
job id:
```

## 8. Stop Rules

Stop and write a failure note if:

```text
oracle slot router fails;
forced expert loss cannot be computed;
target CE/accuracy is not comparable to previous baseline;
component attribution edits are not shape-correct or not interpretable;
all metrics are aggregate-only with no heatmap/trajectory evidence;
summary.md and detailed.md cannot be updated before ending.
```

## 9. What Not To Do

```text
Do not claim specialization from CE/accuracy alone.
Do not claim specialization from route heatmap alone.
Do not claim H-MoE works from common path improvement alone.
Do not run broad architecture sweeps before H0531a diagnosis.
Do not commit raw checkpoints, full logs, or unfiltered outputs.
Do not edit graph.yaml unless the research-state change is explicitly confirmed.
```
