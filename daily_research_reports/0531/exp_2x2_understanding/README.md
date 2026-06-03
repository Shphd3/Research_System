# exp_2x2_understanding

Daily sandbox promoted into a compact evidence package. Main result: minimal
top-1 NTP-style routing is path dependent.

## Read Order

1. `00_handwrite_anchor.md` - user rough judgment.
2. `02_ntp_style_top1_router_lockin_anchor.md` - current research state.
3. `01_protocol_for_approval.md` - approved audit protocol.
4. `02_execution_plan.md` - execution contract.
5. `03_summary.md` - first result reading path.
6. `04_detailed.md` - full evidence ledger.
7. `report_card.md` - meeting-facing card.

## Main Claim

```text
initial same expert -> lock-in + starvation -> collapse
initial different experts -> co-amplification -> stable route-pattern separation
router bias -> shared expert preference -> worse random-init collapse
```

## Main Artifacts

```text
figures/ntp_style_lockin_audit.png
figures/ntp_style_success_dynamics_audit.png
figures/ntp_style_no_router_bias/summary_by_seed.png
tables/ntp_style_lockin_audit.csv
tables/ntp_style_success_dynamics_audit.csv
tables/ntp_style_initial_router_audit.csv
tables/ntp_style_router_bias_comparison.csv
```

## Boundary

Only claim route-pattern dynamics in this minimal top-1 NTP-style proxy. Do not
claim full LM behavior, attention behavior, or utility-aligned specialization.

## Archive

Older soft-routing and non-NTP proxy probes are kept under `archive/` for
traceability. They are not part of the main read path.
