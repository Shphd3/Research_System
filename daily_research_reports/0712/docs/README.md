# 0712 Workload-Grounded MTP Package

Status: daily research package for 2026-07-12.  
Role: approval-ready working draft, not canonical project sync.  
Scope: MTP workload definition, long-range semantics, capacity, gradient conflict, curriculum learning, and one rapid diagnostic route. MoE and Router are currently removed from the active question. No experiment has been run.

## Current Primary Decision

Approve, revise, or reject the Phase A audit:

> On matched synthetic and real two-hop examples, can gradient interference, task-effective rank, safe future-update directions, and cross-position semantic preservation predict the actual one-step NTP effect of adding a Next2 objective?

Do not start full MTP, curriculum, MoE, or Router training before this audit.

## Reading Order

1. `02_mtp_long_range_semantics_capacity_curriculum_story_cn.md`  
   Current Chinese primary synthesis. It defines long-range semantics and composition, derives the small-model conflict and capacity hypotheses, explains curriculum learning, and gives the rapid experiment and 30-second meeting script.

2. `02_mtp_long_range_semantics_capacity_curriculum_story.md`  
   English canonical companion with the same questions, theory status, experiment order, claim boundary, and next decision.

3. `01_workload_grounded_mtp_router_story_cn.md`  
   Earlier workload-first synthesis. Its MoE/Router material is background only; the active story now isolates MTP.

4. `01_workload_grounded_mtp_router_story.md`  
   English companion to the earlier workload story.

5. `A11_22_distributed_evidence_composition_anchor.md` and `A11_22_distributed_evidence_composition_protocol.md`  
   Broader paired synthetic-real downstream design. This design is parked until the faster MTP capacity/conflict audit establishes that the proposed observables predict an actual update.

## Four Active Questions

1. What statistical structure defines the target long-range compositional workload?
2. Why can Next2 encode more future information while hurting main-head NTP?
3. Why can larger models benefit more, and what observable structural quantity should replace raw parameter count as “capacity”?
4. Why can an NTP-to-MTP curriculum repair low-capacity failure?

## Active Mathematical Objects

Task coordinates:

$$
\omega=(D,L_w,\Sigma_m,d_{\mathcal G},\tau).
$$

Model mechanism coordinates:

$$
(c_{12},r_{\mathrm{NTK}},r_{\mathrm{rep}},S_{\mathrm{safe}},R_Z,\kappa_Z).
$$

Primary first-order law:

$$
L_1(\theta-\eta(g_1+\lambda g_2))
-
L_1(\theta-\eta g_1)
=
-\eta\lambda\langle g_1,g_2\rangle+O(\eta^2).
$$

## Minimal Experiment Order

### Phase A — active

Frozen/one-step audit on one small and one larger pretrained dense model using:

```text
256 exact synthetic two-hop examples
128 real two-hop relation-composition examples
```

Measure:

```text
gradient conflict
joint NTK effective rank
safe future-update fraction
current-state task recovery
cross-position task preservation
observed one-step NTP change
```

### Phase B — conditional

Only if Phase A passes, compare:

```text
NTP
static Next2
forward-curriculum Next2
```

under explicit low-rank and high-rank bottlenecks.

### Phase C — conditional

Return the same comparison to a held-out real two-hop task. Synthetic-only success is not sufficient.

## Source Context

Repository rules and state:

```text
AGENTS.md
PROJECTS.md
```

Advisor-dialogue source:

```text
daily_research_reports/0710/0710_MTP_Router_对话校订稿.md
```

Prior A11 theory package:

```text
daily_research_reports/0710/mtp_long_horizon_semantic_efficiency_theory_closure/
```

## Sync Boundary

This folder remains a daily working package. It does not automatically update:

```text
PROJECTS.md
sync/
Projects/from-attention-to-search/
graph manifests
```

After approval, migrate the accepted story and experiment design into the project-local A11 surfaces in one explicit sync task.
