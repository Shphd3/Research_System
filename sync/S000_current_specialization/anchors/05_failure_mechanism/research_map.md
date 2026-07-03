# A05 Failure-Mechanism Research Map

This is a mutable research map for the A05 line. The canonical A05 anchors live
in this folder.

## Parent Question

Why does ordinary top-1 MoE routing fail to form stable feature-level expert
specialization, even in controlled synthetic settings?

## Current Judgment

A05 does not provide a final method. It provides the failure mechanism priors
used by the later A06 pipeline:

```text
ordinary top-1 is early-lock-in prone;
load balance is not specialization;
common / shared hidden directions can create expert-specific routing advantage;
inhibition or center separation alone can amplify collapse instead of solving it.
```

## Decision Flow

```text
Does minimal top-1 routing lock in the initial route assignment?
-> A02: failed seeds collapse at step 0, while split seeds preserve; this is
   the early-lock-in precursor inherited by A05.

Can geometric inhibition fix collapse?
-> A05_01: center separation is insufficient; token-conditioned inhibition is lock-in prone.

Can relaxed feature assumptions make ordinary top-1 acceptable?
-> A05_02: target learning can happen, but routing structure is not reliable specialization.

Does a shared component explain uniform collapse?
-> A05_03: common offset becomes a serious mechanism candidate.

After removing obvious position shortcuts, does feature routing appear?
-> A05_04_01: positive controls help, but ordinary routing still needs mechanism separation.

Is common-logit causally involved?
-> A05_04_02: common-logit timing/cancellation supports the common-feedback mechanism.

Does this matter in real text?
-> A05_04_03: real-text common-logit risk motivates the A06 real-DCLM proxy line.
```

## Anchor Index

| Anchor | Role | Main update | Feeds into |
|---|---|---|---|
| [`02_ntp_style_top1_router_lockin_anchor.md`](02_ntp_style_top1_router_lockin_anchor.md) | Minimal top-1 lock-in precursor | Failed seeds are already collapsed at step 0; split seeds preserve and gain utility advantage. | A05 common / feedback diagnosis and A06 preservation |
| [`05_01_geometric_inhibition_anchor.md`](05_01_geometric_inhibition_anchor.md) | Inhibition / center-separation audit | Geometry-only fixes are not robust; inhibition can harden early lock-in. | Common / feedback diagnosis |
| [`05_02_feature_assumption_relaxation_anchor.md`](05_02_feature_assumption_relaxation_anchor.md) | Relaxed feature audit | Loss or weak route consistency does not prove specialization. | Metric boundary |
| [`05_03_uniform_collapse_common_offset_anchor.md`](05_03_uniform_collapse_common_offset_anchor.md) | Common-offset audit | Uniform data can still collapse through shared hidden offsets. | Common-logit causality |
| [`05_04_01_uniform_feature_specialization_after_position_removal_anchor.md`](05_04_01_uniform_feature_specialization_after_position_removal_anchor.md) | No-position positive-control line | Removing position shortcut is not enough by itself. | Residual/common split |
| [`05_04_02_dotproduct_common_logit_causality_anchor.md`](05_04_02_dotproduct_common_logit_causality_anchor.md) | Common-logit causality | Dot-product common terms are plausible early concentration drivers. | Anti-common prior |
| [`05_04_03_real_text_common_logit_initialization_anchor.md`](05_04_03_real_text_common_logit_initialization_anchor.md) | Real-text common-logit bridge | The common-feedback risk carries into real DCLM settings. | A06 real-DCLM geometry/proxy line |

## Open Questions

1. Which anti-feedback intervention can reduce common/lock-in without turning
   into a supervised feature router?
2. Which metric should decide success when route consistency and non-collapse
   disagree?
3. Which A05 mechanism should become the first A06 preservation intervention:
   mean-subtracted router input, router freeze, delayed router updates, lower
   router LR, or a preservation auxiliary loss?

## Maintenance Notes

Update this map when an A05 result changes:

- the failure mechanism;
- the claim boundary inherited by A06;
- the next preservation / anti-feedback decision.
