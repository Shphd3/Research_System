# Frozen common-path diagnostics: authorized scope

This is a user-requested, post-hoc diagnostic of the completed T_F/T_H experiment. It does not revise the original Protocol, select a new model, train parameters, or close the scientific question. The user confirmed the bounded starting observation: T_H has no stable additional benefit over T_F; harm from a common path has not been established.

Owning sources: [original Protocol](../protocol.md), [Summary](../summary.md), and [Anchor](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/15_24_frequency_composition_common_path_anchor.md).

## Questions and distinguishing checks

1. **No useful added capability:** On the same low-feature positions, does the selected B4 expert's residual reduce target NLL relative to omitting that residual while retaining its partner?
2. **Replacement cost:** Does H replace a selected F expert rather than add a third expert? Within one frozen checkpoint, compare the original partner with the forced B4 partner at unchanged coefficient 1/2.
3. **Heterogeneous effects:** On the same positions, inspect the distribution of endpoint NLL(T_H) minus NLL(T_F), including both seeds, rather than infer utility from a spectrum or activation norm.

These explanations can coexist. B4 membership is a frequency label, not evidence that an expert implements common semantic knowledge.

## Fixed inputs and computation

- Source run: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_composition_common_path/20261019T164834Z`.
- Endpoints: T_F/T_H, steps 168, seeds 11 and 22. No checkpoint selection.
- Panel: existing DEV, 10,340 answer targets; fixed TRAIN-B1 union, 1,701 positions. DEV is already exposed. No new confirmatory dataset or tuning.
- Reuse existing cached h, target, feature IDs and routes; validate block/position/target alignment and required asset access.
- Paired endpoint analysis reuses saved per-position NLL. Structure strata are route unchanged/replaced and displaced B1/non-B1 expert; no outcome-selected subgroups.
- Frozen forward uses the original input scale, complete h, experts, final RMSNorm and LM head. Every active expert retains coefficient 1/2. No omitted residual is reassigned to its remaining partner.
- In one checkpoint, on genuine replacements write the original F pair as (a,b), the H pair as (a,c), where c is selected from B4. Compare Base, a/2, c/2, (a+b)/2 and (a+c)/2, with residuals added to h. Replicate in both trained checkpoint families when affordable.
- CPU BF16 inference must report deviations from saved GPU endpoint NLL. Effects comparable to replay error remain numerically bounded. Do not use a visible debug GPU as a reservation.
- NLL units are nats per answer position; negative differences favor the first named intervention. Dialogue bootstrap is exploratory; two seeds are descriptive, not a population-level replication claim.

## Outputs and boundaries

Execution root: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z`; disjoint `paired` and `ablation` outputs.

Save source/code identity, access receipts, numerical calibration, per-position arrays, aggregate tables and a self-contained bilingual result record. Preserve old artifacts and all failed/unsupported outcomes.

An endpoint T_H-versus-T_F difference combines changed training exposure, learned weights and routing. A within-checkpoint route exchange isolates frozen calling behavior, not an alternative training trajectory. A useful B4 residual does not prove common semantic capability. No Focus/Anchor state transition, retraining, commit, push or publication is authorized here.
