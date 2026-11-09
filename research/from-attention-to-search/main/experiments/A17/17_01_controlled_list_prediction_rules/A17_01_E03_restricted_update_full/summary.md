# Summary: A17_01_E03 Restricted Projection Full

[中文](summary_cn.md) · [Protocol](protocol.md) · [Detailed](detailed.md)

## 1. Purpose

Establish how useful FIRST learning changes LAST prediction and vice versa,providing native loss evidence before frequency and SAE explanation. Direct last Attention o_proj is primary; LoRA is a capacity/parameterization control.

## 2. Hypothesis

Shared updates may help or harm the other rule; the main rival is joint improvement,with answer-vocabulary/format adaptation,ineffective source,numerics and step size distinguished. Local effects do not directly identify common functions or expert necessity.

## 3. Analysis Method

Original Base,L/R8×independent seeds29/43/71,20answers/update equally split rules,constantLR1e-4 and100updates. Full dev at0/16/100,five answer-balanced20-source batches,eta0.001/0.01 full/half; compute FP32 source gradients once and read the same actual perturbation in both precisions,with restore/no-op guards. Endpoint test is read after choices freeze. Three seeds are descriptive; source batches/panels do not inflate independent experiment count.

## 4. Conclusion

The main native observation for direct matrices is cross-rule help: at states0/16 and eta0.01 full step,both directions,all three seeds and five sources pass source/numeric guards and lower recipient loss. Effects shrink after learning; current evidence does not establish stable net interference. All three LOCAL_HARM readouts among4320 cells trace to one L43/state100/LAST sourcebatch0 at full/half scale and different panels,not three independent discoveries. Researcher mechanism judgment remains Unknown.

Full pt-ujjb8f7a is platformSUCCEEDED and independent96/96engineeringPASS,six100-step trajectories and12000 training answers. Preceding Smoke pt-fleom0t0 passed64/64. All42actual milestone members and six endpoint families are registered; source/terminal/resume/numeric evidence is in Detailed.

The table reports registered directional recipient changes in nats/answer. Average five sources within each seed,then report three-seed mean/range; retain all five including insufficient cells and list qualification separately. Ranges are not CIs. Negative means help,positive harm.

| Update | Eta | Step | FIRST→LAST mean [seed range] | LAST→FIRST mean [seed range] | Qualified batches F→L / L→F |
|---:|---:|---|---:|---:|---|
| 0 | 0.001 | full | -0.0010532 [-0.0010753, -0.0010264] | -0.0010252 [-0.0010535, -0.0010044] | 13/15 / 8/15 |
| 0 | 0.001 | half | -0.0005269 [-0.0005379, -0.0005134] | -0.0005133 [-0.0005273, -0.0005030] | 0/15 / 7/15 |
| 0 | 0.01 | full | -0.0103950 [-0.0106056, -0.0101353] | -0.0101551 [-0.0104346, -0.0099487] | 15/15 / 15/15 |
| 0 | 0.01 | half | -0.0052358 [-0.0053439, -0.0051036] | -0.0051044 [-0.0052448, -0.0050004] | 15/15 / 15/15 |
| 16 | 0.001 | full | -0.0002456 [-0.0002896, -0.0002210] | -0.0002324 [-0.0002404, -0.0002216] | 6/15 / 8/15 |
| 16 | 0.001 | half | -0.0001229 [-0.0001450, -0.0001105] | -0.0001162 [-0.0001202, -0.0001109] | 8/15 / 8/15 |
| 16 | 0.01 | full | -0.0024139 [-0.0028382, -0.0021751] | -0.0022827 [-0.0023655, -0.0021800] | 15/15 / 15/15 |
| 16 | 0.01 | half | -0.0012184 [-0.0014345, -0.0010972] | -0.0011518 [-0.0011925, -0.0011005] | 13/15 / 13/15 |
| 100 | 0.001 | full | -0.0000958 [-0.0001256, -0.0000683] | -0.0000779 [-0.0001336, -0.0000445] | 5/15 / 4/15 |
| 100 | 0.001 | half | -0.0000480 [-0.0000629, -0.0000346] | -0.0000392 [-0.0000670, -0.0000224] | 6/15 / 4/15 |
| 100 | 0.01 | full | -0.0008959 [-0.0011788, -0.0006258] | -0.0007198 [-0.0012602, -0.0004009] | 12/15 / 10/15 |
| 100 | 0.01 | half | -0.0004653 [-0.0006113, -0.0003287] | -0.0003757 [-0.0006504, -0.0002122] | 9/15 / 9/15 |


![Direct native cross-rule effects](figures/cross_rule_effects.png)

Colors show directions and styles show seeds; zero separates help/harm. Filled points have all five sources qualified; hollow points retain insufficient evidence. All registered scales are shown without selection. Negative late means do not erase a harmed source or precision insufficiency. [Complete seed/source table](figures/cross_rule_effects.csv) and origins are in the figure folder.

Endpoint FP32 test three-seed means follow. L/R8 use the same LR but actual ΔW norms are about2.74/0.624 and ranks1024/8; differences cannot be attributed to pure capacity because parameterization and functional displacement also differ.

| Variant | Order-new* | Combination-new* | Combined | Combined CE | Seed combined accuracy range |
|---|---:|---:|---:|---:|---|
| L | 90.58% | 88.92% | 89.75% | 0.522549 | 88.62%–91.38% |
| R8 | 82.17% | 77.25% | 79.71% | 0.829560 | 78.75%–81.00% |


*Registered nominal panels are retained: of400nominal order_new endpoint records,seeds29/43/71 have392/390/388actual seen-group records; the remainder belongs to actual unseen-group. State0 has no task-training exposure,so order_new is design-relative. An append-only actual-exposure audit reaggregates both true novelty types and combined at0/16/100 without changing the full800primary. [Exposure audit](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/actual_exposure_panel_qualification.json).

This establishes the entry from measured shared-update effects to later SAE explanation without requiring net harm first. It does not establish basic-module/unique-expert structure,natural-pretraining mechanism,long-term utility or population significance from three seeds. SAE must account for actual displacement/residual and survive finite interventions; frequency has its independent Anchor.


### All authorized SAE substages completed after numerical finalization recovery

The existing E03 scope is now engineering-complete: all nine Qwen states and the S7 list state are saved and qualified under their recorded readers, totaling760 matrix settings/9,120 interventions. The matching Qwen raw-output SAE completed1,000,002,960 valid prediction positions; S7 reuses its embedded SAE and was not retrained. S7 native-DCLM qualification covers all64 conditions/16 actual matrices and four passing source-gradient checks. [Complete stage audit](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/completion_audit_20261010T1048Z.json) and [SAE Detailed record](detailed.md) own the evidence.

GPU job `pt-f9dhsb6w` remains FAILED because two saved-summary means disagreed with NumPy reductions. A separate [CPU finalization recovery](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/summary.json) recomputed array-backed means in float64 and passed all320 exact summary checks without changing measurement bytes or native error caps. All required outputs are registered. Eight Qwen states retain20-row tail qualification; Qwen71/update100 uses native120-recipient qualification. Engineering completion does not turn these into uniform reader evidence or establish functional decomposition. Overall scientific synthesis awaits researcher discussion; mechanism judgment remains Unknown. Earlier pending/NOT_RUN statements below this stage's preparation history are historical, not the current execution state.
