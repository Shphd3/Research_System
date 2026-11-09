# Protocol: A13_00_03_E02 Gate-Coherent Independent Confirmation

## 0. Approval Snapshot

Approval status: approved under standing autonomous authorization.

Purpose: independently confirm the E01 relay-necessity interaction after
repairing one logical inconsistency between its capability and causal-use
guards.

Primary anchor:
[13_00_03](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_03_relay_necessity_objective_interaction_anchor.md)

E01 remains formally `insufficient`; its primary effects are not reused to
declare E02 success.

## 1. Terminology / Definitions

`Capability-eligible causal use` means that relay intervention is judged only
for trained models whose ordinary-head held-out answer accuracy is at least
the already registered per-seed capability threshold of 0.90. A model that
cannot answer the intact task has no interpretable answer-control interface.

## 2. Anchor Alignment

The decision question, task, objectives, primary metrics, effect thresholds,
and claim boundary are unchanged from E01.

## 3. Tested Hypothesis

On eight new paired seeds, mean \(U_{\mathrm{relay}}\) and mean
\(\Delta_{\mathrm{relay}}\) are each at least 0.02 nats, have positive paired
bootstrap lower bounds, and are positive in at least seven seeds.

## 4. Rival Explanations

The E01 effect was caused by its seed set, by matched-shared-aux instability,
or by including models that did not causally use the relay.

## 5. Data / Model / Algorithm / Objective

Exactly the E01 `copy_matched` data, width-64 two-layer model, sparse relay and
bypass masks, NTP/shared-aux/Next-2 objectives, optimizer, schedule, loss
weights, and 3,000-step budget.

## 6. Conditions, Seeds, And Checkpoints

New paired seeds: 1501--1508. Checkpoints and the frozen 1,000-step AULC
horizon are unchanged.

## 7. Primary Metric

Unchanged:

\[
U_{\mathrm{relay}}
=
\operatorname{AULC}_{\mathrm{SA,relay}}
-
\operatorname{AULC}_{\mathrm{MTP,relay}},
\]

\[
\Delta_{\mathrm{relay}}
=
U_{\mathrm{relay}}-U_{\mathrm{bypass}}.
\]

All original effect thresholds remain unchanged.

## 8. Guard Correction

The original capability rule passed an objective/path cell when at least seven
of eight seeds had accuracy \(\ge0.90\). Its causal-use rule then averaged donor
follow over all eight seeds, including an explicitly ineligible model. E02
uses the same thresholds but composes them coherently:

1. each objective/path cell still requires mean accuracy \(\ge0.95\) and at
   least seven of eight seeds \(\ge0.90\);
2. for each relay objective, donor follow is calculated only among those
   capability-eligible seeds;
3. at least seven eligible seeds are still required;
4. their mean different-label donor follow must still be \(\ge0.90\).

No numerical threshold is relaxed.

## 9. Secondary Metrics

Unchanged final NLL, auxiliary accuracy, NTP system contrast, initial-gradient
diagnostics, and same-label donor preservation.

## 10. Known Good / Known Bad / Known Confusing Cases

E01 had eight positive \(U_{\mathrm{relay}}\) and interaction signs, but its
registered verdict was insufficient. Seven NTP seeds were capability-eligible
and each had donor follow 1.0; the one ineligible NTP seed had clean accuracy
0.7692 and donor follow 0.0769.

This observation motivates the guard repair but cannot itself confirm E02.

## 11. Algorithm Specification

Run the same six cells with new paired seeds. Apply the corrected guard only
after all final capability values are available.

## 12. Success / Failure / Insufficient Evidence

Pass: corrected guards pass and all original primary-effect criteria pass on
the new seeds.

Fail: corrected guards pass but either effect has a non-positive upper bound.

Insufficient: any corrected guard fails or intervals straddle the decision
region.

## 13. What This Cannot Claim

Unchanged from E01: no pure-content, standard-MTP, code, language,
long-context, composition, planning, MoE, or compute-scaling claim.

## 14. Review Notes And Protocol Changes

Only two registered objects changed: fresh seeds and logical conditioning of
the causal-use gate on the pre-existing capability gate. The task, models,
objectives, horizon, metrics, and numerical thresholds did not change.
