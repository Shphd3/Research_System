# 0602 Conversation Handoff

## Current Conclusion

本轮对话已经把 2x2 top-1 router lock-in 这条机制审计整理成正式研究流程：

```text
daily sandbox -> formal project experiment -> project-local sync -> daily meeting package
```

核心机制判断：

```text
minimal 2-feature / 2-expert NTP-style top-1 proxy 中，
route collapse 更像 early top-1 lock-in + expert starvation，
不是 late optimization drift。
```

但当前结论边界必须保留：

```text
只 claim minimal route-pattern dynamics；
不 claim full LM；
不 claim attention setting；
不 claim utility-aligned specialization。
```

下一轮研究方向：

```text
不要优先做 structured / semantic / slot-centroid initialization 修补。
回到 multi-B / slot-context synthetic，
测试 explicit route-function binding signal。
```

## What Was Completed

### 1. Research-system rules were simplified

当前默认流程：

```text
anchor -> protocol / execution plan -> summary.md -> detailed.md -> anchor update
```

只有显式要求时才做：

```text
root sync
project / collaborator sync
handoff package
graph update
commit / push
```

Graph 仍然是用户研究中心判断层；不要自动改 `graph.yaml`。

### 2. Report-card rule was standardized

Daily / sync 包中的导师汇报卡统一命名为：

```text
05_report_card.md
```

固定结构：

```text
Source Files
Executive Summary
Research Process Update
Terms Used Here
Key Figures
Current Claim
Claim Boundary
Next Step
```

它是给导师直接看的 self-contained evidence card，不是私人讲稿，不放私人问题，不写成长报告。

### 3. 0531 daily sandbox was cleaned and promoted

Daily sandbox:

```text
daily_research_reports/0531/exp_2x2_understanding/
```

主读路径：

```text
02_ntp_style_top1_router_lockin_anchor.md
01_protocol_for_approval.md
02_execution_plan.md
03_summary.md
04_detailed.md
report_card.md
figures/
tables/
```

旧 soft-routing / non-NTP proxy 内容被降级到 archive，不作为当前主读路径。

### 4. from-attention project received the formal record

Formal anchor:

```text
Projects/from-attention-to-search/main/problem_anchors/01_gated_main_causes/02_ntp_style_top1_router_lockin_anchor.md
```

Formal experiment:

```text
Projects/from-attention-to-search/main/experiments/H0531_2x2_top1_router_lockin/
```

Included:

```text
README.md
protocol_for_approval.md
execution_plan.md
summary.md
detailed.md
report_card.md
figures/
tables/
```

This was committed and pushed to:

```text
repo: Projects/from-attention-to-search
branch: Xingyu
commit: 6e12941 二维audit
```

### 5. from-attention project-local sync was added

Project sync package:

```text
Projects/from-attention-to-search/XingyuD/sync/0531_2x2_top1_router_lockin/
```

Included:

```text
README.md
report_card.md
02_ntp_style_top1_router_lockin_anchor.md
summary.md
detailed.md
protocol_for_approval.md
execution_plan.md
figures/
tables/
```

Sync principle now:

```text
sync does not create new conclusions;
sync copies current research state:
anchor + summary + detailed + 05_report_card + referenced figures/tables + README.
```

### 6. 0601 meeting-facing daily package was created

Daily package:

```text
daily_research_reports/0601/2x2_top1_router_lockin/
```

Current contents:

```text
05_report_card.md
README.md
figures/
tables/curated_evidence_table.md
```

The user decided `meeting/meeting_brief.md` is unnecessary because:

```text
daily_research_reports/0601/meeting/meeting_core.md
```

is already enough as private meeting preparation.

## Key Scientific Content

### Tested question

In a 2-feature / 2-expert NTP-style top-1 proxy:

```text
Does route collapse happen because training gradually drifts into collapse,
or because top-1 assignment is already locked at step 0 / early steps?
```

### Falsifiable hypothesis

```text
Linear router can express A/B split for two orthogonal feature states.
Failure is not mainly linear expressivity failure.
Failure comes from NTP objective + top-1 update path not requiring stable
route-pattern separation.
```

This can be weakened if:

```text
initial split later collapses;
linear router cannot express the split;
or route-pattern split appears without addressing expert utility.
```

### Main evidence

```text
failed seeds:
  step 0 A/B same expert -> selected gate confidence rises -> unselected expert starvation -> final NMI 0

successful seeds:
  step 0 A/B split -> split stays stable -> NMI 1

no-router-bias diagnostic:
  removing router bias improves random-init split from 3/10 to 6/10,
  but does not guarantee separation.
```

### Important interpretation

```text
task learning != route-pattern specialization
route-pattern specialization != utility-aligned specialization
```

Token accuracy / CE can be good while routing NMI is 0.

## Next Research Step

Do not broaden into a large ablation grid.

Do not make structured initialization the main next step, because prior multi-B
semantic / slot-centroid initialization was not sufficient.

Next minimal direction:

```text
explicit route-function binding signal
```

Decision question:

```text
In multi-B / slot-context synthetic,
if slot information is visible and oracle routing is feasible,
can an explicit route-function binding signal make route assignment align with
expert causal utility?
```

Primary evidence should jointly inspect:

```text
route-slot NMI
forced expert loss diagonal
assignment-utility agreement
```

## Suggested Read Order For Next Conversation

1. `AGENTS.md`
2. `PROJECTS.md`
3. `daily_research_reports/0602/README.md`
4. `daily_research_reports/0601/2x2_top1_router_lockin/05_report_card.md`
5. `daily_research_reports/0601/meeting/meeting_core.md`
6. `Projects/from-attention-to-search/main/problem_anchors/01_gated_main_causes/02_ntp_style_top1_router_lockin_anchor.md`
7. `Projects/from-attention-to-search/main/experiments/H0531_2x2_top1_router_lockin/summary.md`
8. `Projects/from-attention-to-search/main/experiments/H0531_2x2_top1_router_lockin/detailed.md`

## Current Workspace Notes

At the time this handoff was written:

```text
Root Research_System has uncommitted changes in 0601 daily/report-card related files.
Projects/from-attention-to-search has pushed commit 6e12941 on branch Xingyu.
Projects/from-attention-to-search currently has an untracked detailed.pdf under
main/experiments/slot_context_dominance_router_specialization/.
```

Do not commit, push, update graph, or sync root unless the user explicitly asks.
