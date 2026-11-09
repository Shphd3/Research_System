# Summary: A01_04 Feedback Common Preservation Bridge Controlled Full Run

## Conclusion

The controlled feedback bridge supports the feedback-common mechanism. In the
two main feedback regimes, replaying only \(P_{\mathrm{fb}}\Delta h\) reproduces
the proxy-route NMI collapse, and removing \(P_{\mathrm{fb}}\Delta h\) rescues
the proxy route.

Primary result:

```text
n_passed_main_feedback_regimes = 2 / 2
controls_ok = true
pass = true
```

This supports feedback-common replay/removal as a valid controlled mechanism
for preservation failure. It does not prove real-DCLM feedback causality
because the local A06 artifacts contain trajectory metrics but not
hidden/checkpoint drift tensors for real replay/removal.

## Primary Metric

`proxy_nmi_drop_explained_by_feedback_common` is:

\[
\frac{\mathrm{NMI}_0-\mathrm{NMI}_{\mathrm{feedback\ only}}}
{\mathrm{NMI}_0-\mathrm{NMI}_{\mathrm{full}}+\epsilon}
\]

It measures how much of the full-drift proxy-route NMI drop is reproduced by
feedback-common drift alone.

Pass rule: both main feedback regimes must have explanation and rescue
fractions at least 0.75, beat random controls by more than 0.25, and negative
controls must not show false feedback explanation.

## Setup

Step-0 hidden states are generated so a linear router recovers proxy groups.
The router has a common-margin direction for one expert. Feedback drift moves
hidden states along that common-margin direction; residual drift moves
group-specific components.

Interventions:

- `step0`: original valid proxy route.
- `full_drift`: \(h_0+\Delta h\).
- `feedback_only`: \(h_0+P_{\mathrm{fb}}\Delta h\).
- `residual_only`: \(h_0+(I-P_{\mathrm{fb}})\Delta h\).
- random projector controls.

Configuration: hidden dimension 32, eight groups/experts, 600 samples per
group, twenty seeds, five regimes.

## Main Results

| Regime | Step0 NMI | Full NMI | Feedback-only NMI | Residual-only NMI | Explain | Rescue | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| common_feedback | 1.0000 | 0.0205 | 0.0205 | 1.0000 | 1.0000 | 1.0000 | pass |
| mixed_feedback_residual | 1.0000 | 0.1440 | 0.1028 | 1.0000 | 1.0509 | 1.0000 | pass |
| residual_drift_control | 1.0000 | 0.9996 | 1.0000 | 0.9998 | 0.0000 | 0.0002 | control ok |
| nuisance_drift_control | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | control ok |
| weak_feedback | 1.0000 | 0.9602 | 0.9650 | 1.0000 | 0.1074 | 0.1343 | denominator small; sensitivity only |

In `mixed_feedback_residual`, explanation fraction is slightly above 1 because
residual drift partly counteracts the collapse, so feedback-only replay drops
NMI slightly more than full drift.

## Central Figures

![Proxy-route NMI by condition](figures/feedback_bridge_nmi_by_condition.png)

This figure tests causal replay/removal. In feedback regimes, full drift and
feedback-only drift collapse proxy NMI, while residual-only drift rescues it.
Residual and nuisance controls do not collapse.

![Feedback explanation and rescue](figures/feedback_explain_rescue_by_regime.png)

This figure tests the primary metric and rescue metric. Feedback regimes pass
the 0.75 threshold; controls do not show false explanation. `weak_feedback` is
treated as a sensitivity case because the full NMI drop is small.

![Route max load by condition](figures/feedback_bridge_max_load_by_condition.png)

This figure checks the routing mechanism. Full and feedback-only drift create a
high max-load collapse in feedback regimes, while residual-only drift restores
balanced routing.

## Real-DCLM Artifact Boundary

Local `A06_01_04_E03/E04` artifacts include trajectory metrics, summaries, figures,
logs, and partial JSONL records. They do not include the hidden-state drift
tensors needed to compute:

\[
\Delta h_t=h_t-h_0
\]

or to replay/remove:

\[
P_{\mathrm{fb}}\Delta h_t
\]

Therefore this run can validate the controlled bridge mechanism, but the
real-DCLM feedback-common claim remains untested until those artifacts are
recovered or regenerated.

## Claim Boundary

This run supports: feedback-common replay/removal is a valid controlled
mechanism for proxy-route collapse.

This run does not support: real-DCLM feedback causality, real preservation
rescue, layerwise feedback common, residualized MoE improvement, or expert
utility.

## Next Decision

Before method construction, recover or regenerate real-DCLM hidden/checkpoint
drift artifacts for step 0, step 5, and step 10. Then run the same
feedback-common replay/removal test on real proxy labels and real hidden
drifts.
