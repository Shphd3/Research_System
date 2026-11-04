# Three common-path diagnostics: paired outcomes and attribution limits

**All three checks were executed. The intervention replaces a partner, while position-level gains and losses cancel without an identified stable beneficiary group. Local frozen inference suggests that a B4 residual can help alone without providing a stable additional benefit alongside its partner. However, replay qualification against the original GPU record failed, so these observations do not identify the original negative result's mechanism.**

This is a post-hoc supplement to the [original Summary](../summary.md), under the [diagnostic scope](analysis_contract.md). It changes no original primary metric, model, route, training data, trained weights or scientific state. No retraining was performed.

## Panel and metric

Use the original step168 T_F/T_H endpoints, seeds11/22, and original TRAIN-defined B1 features. DEV has10,340 answer-prediction positions in128 dialogues. The B1 union has1,701 positions in124 dialogues, each position counted once. DEV is already exposed.

NLL is the negative log probability of the correct next answer token, in nats; lower is better. The diagnostic difference is NLL(T_H) minus NLL(T_F), negative favoring H. Position-union means differ from the original feature-equal macro primary; they do not replace it.

## Actual intervention

F selects the two highest calibrated bands. H selects B4 plus the highest non-B4 band, with the same within-band winner. If F already includes B4, the pair is unchanged. Otherwise H retains F's first winner and replaces its second with the B4 expert. Both residual coefficients remain1/2, on complete original h. A B1 expert need not survive.

| DEV panel | Positions | Same pair | Replaced pair | Dropped B1 / B2 / B3 |
|---|---:|---:|---:|---:|
| All | 10,340 | 7,694 | 2,646 | 132 / 965 / 1,549 |
| B1 union | 1,701 | 686 (40.33%) | 1,015 (59.67%) | 132 / 507 / 376 |

Dropping B1 occurs at7.76% of B1 positions, or13.00% of genuine replacements. This establishes an opportunity-cost structure, not that the displaced computation was more useful.

## Paired same-position outcomes

Average per-position differences over the two fixed seeds, then equally over positions. Intervals use1,000 whole-dialogue joint bootstrap draws and are exploratory conditional on these seeds.

| B1 structure stratum | Positions | Mean H−F NLL | Exploratory95% interval |
|---|---:|---:|---|
| All B1 | 1,701 | +0.000871 | [−0.002642, +0.004259] |
| Same route | 686 | +0.003501 | [+0.000373, +0.006784] |
| Actual replacement | 1,015 | −0.000906 | [−0.006140, +0.004017] |

The actual replacement stratum does not show stable deterioration. Same-route positions also differ between endpoints. Separately trained weights therefore prevent attributing the full endpoint difference to an immediate partner exchange.

At tolerance1e−6 nats, the seed-mean difference improves781 positions(45.91%), worsens879(51.68%), and is near-zero at41(2.41%). Only443 positions(26.04%) improve under both seeds;511(30.04%) worsen under both;673(39.56%) reverse direction. The median difference is+0.00000459 nats;10th/90th percentiles are−0.05966/+0.06135.

Using all1,701 positions as denominator, beneficial positions contribute−0.018718 nats and detrimental positions+0.019589, yielding+0.000871 overall. Heterogeneity is observed; a stable, prospectively identifiable beneficiary group is unknown. No outcome-selected subgroup search was performed.

Position-union means for seeds11/22 are+0.000736/+0.001007. Original feature-macro differences were−0.000152/+0.002131. Different aggregation units explain this distinction; the original primary is unchanged.

## Frozen residual comparison: local observations and numerical limits

Within one checkpoint, write the genuine replacement as original pair(a,b) versus H pair(a,c), c selected from B4. Evaluate Base, a/2, c/2, (a+b)/2 and (a+c)/2 as residuals added to h. Omitting an expert never reallocates its coefficient to another expert.

The B4 marginal compares(a+c)/2 against a/2; partner replacement compares(a+c)/2 against(a+b)/2. An additional NLL interaction contrast compares combined benefit with the sum of individual benefits; it is not evidence of vector or gradient cancellation.

CPU BF16 evaluation first completed but lacked replay precision. At the user's request, four checkpoints were then evaluated sequentially on the local H10040GB MIG slice in24.27 seconds, with approximately0.61GB peak allocated GPU memory and no parameter updates. See the [execution amendment](execution_amendment_local.md).

The following results hold **one trained T_H checkpoint fixed, under local GPU arithmetic, on the1,015 genuine replacement positions**, averaged equally over two seeds. Intervals use500 whole-original-DEV-dialogue draws conditional on these seeds and local arithmetic; they exclude replay uncertainty.

| Frozen contrast | Mean NLL difference | Reading |
|---|---:|---|
| B4 residual c/2 alone versus Base | −0.002105 | Beneficial standalone point estimate |
| Add c/2 while retaining a/2 | +0.001284 | No stable additional gain; interval[−0.004840,+0.006405] |
| Replace original partner b with c | −0.000614 | Not stable deterioration; seeds+0.001455/−0.002683 |
| NLL nonadditivity relative to individual gains | +0.003390 | Combined gain below the sum of standalone gains; interval[+0.001487,+0.005576] |

These local observations weaken the strong account that the B4 expert has no useful output at all. A useful standalone contribution need not add benefit alongside the current partner. This does not distinguish vector cancellation, gradient conflict, overcorrection or common semantic computation. Restoring the original partner is not stably better.

An auxiliary check with trained T_F weights on the same replacement positions gives B4 marginal+0.000016 and NLL interaction+0.002474, with intervals[−0.005466,+0.004822] and[+0.000212,+0.004858]. This is another trained weight family, not an independent dataset or new training experiment.

**Eligibility: BOUNDED; attribution of the original result remains Unknown.** Local evaluation uses full original DEV order, batch128 and native actual dispatch shapes. A literal call to the original evaluate function matches the new cached implementation's actual-route NLL exactly. All four weight hashes and code identities match. Base NLL matches all10,340 original values exactly. Nevertheless, T_H seeds11/22 have B1 mean absolute replay errors0.000253/0.000557 and maxima0.06658/0.12167 nats, failing the previously fixed gate. T_F errors are smaller but also fail its maximum-error requirement. Checks exclude the new cache implementation and inference_mode as causes; the discrepancy between saved T_H NLL and current same-source native inference remains unresolved.

The table therefore describes the current local frozen function and cannot establish the original GPU negative result's mechanism. Failed CPU/GPU qualification remains recorded; thresholds were not relaxed and execution surfaces were not pooled.

## Execution ordering and ordinary-MoE restoration

The first remote creation failed with `429 MEMBER_QUOTA_EXCEEDED` and produced no job. The user then selected diagnostic priority followed by ordinary-MoE resubmission. Ordinary-MoE job `pt-50sa30mo` was stopped only after verifying STARTING/zero replicas/no runtime progress. Diagnostic `pt-t9lutqt0` was accepted, then stopped before runtime when the user switched to local inference, preventing duplicate diagnostic execution.

Local inference is complete. Ordinary MoE was resubmitted unchanged as **`pt-0hi8ldns`**, still single-node four-H100 Reserved. At05:02:08 UTC it was STARTING with zero replicas, no observed training progress and no ETA. Historical receipts and cancellation reasons are retained; unstarted jobs are not training evidence.

## Answers and remaining boundary

| Hypothesis | Current answer | Boundary |
|---|---|---|
| No useful additional capability in the B4 expert | No stable local incremental gain; original attribution Unknown | Standalone point estimate helps, while adding to the partner does not stably help; this is not total absence of capability |
| Combination/replacement offsets the gain | Replacement established; local nonadditivity observed | Replacement does not stably worsen; structural cost or local nonadditivity does not identify the original negative mechanism |
| Average masks gains at some positions | Descriptive heterogeneity observed | Only26.04% improve under both seeds; no stable beneficiary group identified |

Base computation remains present throughout; this experiment never removes all common computation from low-frequency inputs. B4 is a frequency label, not a verified common semantic module. These diagnostics establish neither general harm from a common path nor one definitive explanation of the original negative result.

## Evidence and reproducibility

Execution root: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z`.

- [Paired facts](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z/paired/facts_cn.md), [full statistics](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z/paired/results.json), [source table](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z/paired/panel_summary.csv).
- [Input identity and recomputation audit](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z/paired/manifest.json): exact target/position/route alignment and all original feature-NLL/support recomputations pass; original artifacts read-only.
- [CPU forward receipt](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z/ablation/receipt.json), [numerical calibration](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z/ablation/provenance/calibration.json).
- [Local GPU execution and failed gate](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z/ablation/local_gpu/receipt.json), [contrasts and intervals](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z/ablation/local_gpu/tables/true_replacement_reading.md).
- [Literal source-evaluate check](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z/ablation/local_gpu/provenance/literal_source_evaluate.json): new implementation matches current original implementation; disagreement with the old record remains unresolved.

This record completes factual evidence and boundaries. Researcher-owned mechanism judgment and the next scientific decision remain Unknown. No Focus/Anchor transition, commit, push or publication.

Registered diagnostic asset: `analysis_crosscoder_common_path_hypothesis_checks_20261021t045000z`; [current strict access](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/common_path_hypothesis_checks/20261021T045000Z/provenance/registered_access.json) passes. Registration explicitly retains `BOUNDED_REPLAY_GATE_FAILED` and confirms accessible artifacts only.
