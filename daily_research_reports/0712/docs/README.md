# 0712 Workload-Grounded MTP and Router Package

Status: daily research package for 2026-07-12.  
Role: approval-ready working draft, not canonical project sync.  
Scope: workload modeling, theory route, one paired synthetic-real protocol. No experiment has been run.

## Current Decision

Accept, revise, or reject the following workload definition:

> A minimal difficult long-context task requires retaining multiple necessary pieces of evidence under distractors, binding them correctly, composing them into an intermediate task state, and preserving that state until the answer position.

No MTP horizon sweep, MoE training, or Router method design should begin before this decision and the A11_22 paired audit.

## Reading Order

1. `01_workload_grounded_mtp_router_story_cn.md`  
   Chinese primary reading path. It starts with the five urgent questions, gives the theory route, and states the research order.

2. `01_workload_grounded_mtp_router_story.md`  
   English canonical companion with the same research question, theorem status, claim boundary, and next decision.

3. `A11_22_distributed_evidence_composition_anchor.md`  
   One adjudicable decision question and one core mathematical model.

4. `A11_22_distributed_evidence_composition_protocol.md`  
   One minimal paired synthetic-real experiment using a controlled composition task and a real 2WikiMultiHopQA/LongBench-format test.

## Five Urgent Questions

1. Which concrete long-context workload is being solved?
2. Which minimal capabilities does that workload require?
3. Which representation-space properties are necessary?
4. Under what conditions does MTP help or hurt those properties?
5. Which structural bottleneck, if any, would justify MoE and a Router?

## Minimal Experiment

Exactly three conditions:

```text
NTP
MTP-info
MTP-mask
```

Exactly one paired test:

```text
controlled operator-labeled evidence composition
+
held-out real multi-document compositional QA
```

Primary metric:

$$
T_{\mathrm{pair}}
=
\min(\Delta Q^{\mathrm{syn}},\Delta Q^{\mathrm{real}}).
$$

Synthetic-only success is not sufficient. Real-task improvement without the declared causal representation mechanism is also not sufficient.

## Theory Route

```text
workload generative model
-> task-relevant evidence equivalence class
-> representation necessity
-> intermediate composition-state formation
-> informative-horizon MTP gradient
-> capacity/conflict/catch-up scale model
-> conditional MoE/Router interference model
```

Only the first paired audit is currently active. Later layers are theory targets, not approved experiments.

## Source Context

Repository rules and state:

```text
AGENTS.md
PROJECTS.md
```

Prior A11 daily package:

```text
daily_research_reports/0710/mtp_long_horizon_semantic_efficiency_theory_closure/
```

Advisor-dialogue source:

```text
daily_research_reports/0710/0710_MTP_Router_对话校订稿.md
```

## Sync Boundary

This folder is a daily working package. It does not automatically update:

```text
PROJECTS.md
sync/
Projects/from-attention-to-search/
graph manifests
```

After approval, migrate the accepted anchor/protocol into the project-local A11 surfaces and update canonical indexes in one explicit sync task.
