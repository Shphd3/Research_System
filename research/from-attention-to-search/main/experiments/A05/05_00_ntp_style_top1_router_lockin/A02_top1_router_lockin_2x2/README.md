# H0531 2x2 Top-1 Router Lock-In

Formal project record for the 2026-05-31 daily sandbox.

Main update:

```text
minimal 2-feature / 2-expert top-1 NTP-style proxy
-> failed seeds collapse from step 0
-> successful seeds split from step 0 and stay split
-> router bias worsens same-expert initialization risk
```

## Read Order

1. `protocol_for_approval.md`
2. `execution_plan.md`
3. `summary.md`
4. `detailed.md`
5. `report_card.md`
6. `../../../../problem_anchors/05_failure_mechanism/05_00_ntp_style_top1_router_lockin_anchor.md`

## Claim

```text
initial same expert -> lock-in + starvation -> collapse
initial different experts -> co-amplification -> stable route-pattern separation
router bias -> shared expert preference -> worse random-init collapse
```

## Boundary

This is a minimal NTP-style top-1 proxy. It supports route-pattern dynamics
only; it does not prove utility-aligned specialization or full LM behavior.

## Source

```text
daily_research_reports/0531/exp_2x2_understanding/
```
