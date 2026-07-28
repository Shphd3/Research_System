# Protocol: A13_00_04_E01 Relay-Target Localization

## 0. Approval Snapshot

Approval status: approved under standing autonomous authorization.

Purpose: isolate the local answer-aligned relay target from the other
all-position Next-2 target changes.

## 1. Terminology / Definitions

`Background-MTP` predicts the usual Next-2 targets at auxiliary positions
0--3 and predicts fixed `[ANSWER]` at the relay position 4. `Full-MTP` differs
only by predicting answer value $A$ at position 4.

## 2. Anchor Alignment

Primary anchor:
[13_00_04](/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_04_relay_target_localization_anchor.md)

Single question: is the relay-position answer target the local cause of the
candidate utility interaction?

## 3. Tested Hypothesis

Both $D_{\mathrm{relay}}$ and
$\Delta_D=D_{\mathrm{relay}}-D_{\mathrm{bypass}}$ are positive under all
registered effect criteria.

## 4. Rival Explanations

The benefit comes from background Next-2 labels, seed selection, direct-path
regularization, or an invalid carrier.

## 5. Data / Model / Algorithm / Objective

Freeze the validated `copy_matched` data hash, two-layer width-64 model,
attention masks, AdamW cosine schedule, equal standard/auxiliary loss weights,
and all-position target count.

Only one auxiliary label differs between arms:

```text
background: [x2 x3 x4 x5 x5]
full MTP:   [x2 x3 x4 x5 x6]
```

At the final auxiliary position, $x_5=[ANSWER]$ and $x_6=A$.

## 6. Conditions, Seeds, And Checkpoints

Paths: relay and bypass. Objectives: background-MTP and full-MTP. Fresh paired
seeds: 1601--1608. Train 3,000 steps and freeze AULC at 0--1,000.

## 7. Primary Metric

$$
D_r
=
\operatorname{AULC}_{\mathrm{background},r}
-
\operatorname{AULC}_{\mathrm{full},r}.
$$

Pass: bootstrap lower bounds for mean $D_{\mathrm{relay}}$ and mean
$\Delta_D$ are positive; both means are at least 0.02 nats; at least seven of
eight paired seeds have each positive sign.

## 8. Guard Logic

Carrier validity is a pre-treatment fact established by
`A13_00_02_E02`. Objective-arm capability is reported as an outcome and is not
used to discard paired effect observations.

Relay donor use is tested among capability-eligible models at the unchanged
0.90 threshold. Failure to obtain seven eligible models limits causal-interface
interpretation for that arm but does not invalidate the pre-treatment carrier
or erase an objective performance effect.

## 9. Secondary Metrics

Final arm capability, relay auxiliary accuracy, initial gradient diagnostics,
same-label preservation, and comparison of $D$ with the earlier full-objective
$U$ magnitude.

## 10. Known Good / Known Bad / Known Confusing Cases

Known good: the NTP-only carrier passed all structural and intervention gates.

Known confusing: requiring every treatment arm to pass capability is
post-treatment selection and can condition away the effect being measured.

## 11. Algorithm Specification

Replay paired initialization and mini-batch streams for both arms within each
path. Evaluate only the ordinary next-token head.

## 12. Success / Failure / Insufficient Evidence

Pass/fail follows the primary effect criteria with the pre-treatment carrier
gate. Causal-interface evidence is separately sufficient or insufficient; it
does not redefine arm performance.

## 13. What This Cannot Claim

No generic MTP, all-position necessity, code, language, long-context,
composition, planning, MoE, or compute-scaling conclusion.

## 14. Review Notes And Protocol Changes

Relative to prior comparisons, this protocol changes the causal estimand,
uses fresh seeds, and removes post-treatment capability as a performance
inclusion rule. It does not relax any effect threshold or alter the carrier.
