# Summary: A17_01_E02 Restricted Update Smoke

[中文](summary_cn.md) · [Protocol](protocol.md) · [Detailed](detailed.md)

Engineering state: `PASS`；scientific verdict `NOT_EVALUATED`；human adoption/mechanism `Unknown`。

## 1. Purpose

Qualify direct last-projection and shared rank8 LoRA update chains before the researcher chooses a measurable learner/state.

## 2. Hypothesis

Restricted parameters may adapt FIRST/LAST and yield finite effects; rivals are insufficient location/capacity or rapid saturation. This Smoke does not adjudicate stable help or harm.

## 3. Analysis Method

- Compare same-location L/R8 at two LRs with original Base, data,20 answers/update and50-update ceiling fixed; all other parameters frozen.
- Measure capability/CE on full800 dev; finite effects on a fixed80-dev engineering panel with five balanced source batches × three SGD step sizes × BF16/FP32; report novelty panels separately and combined.
- Audit native full-vocabulary logits/CE, frozen bytes, counters/TensorBoard, saves and external-process restore/continuous next update9.

## 4. Conclusion

Repaired job pt-i3ianttt engineering PASS; independent gates 64/64 passed.

First job pt-bw3s1pxw failed at the update0 baseline-restoration guard, with zero trajectory training updates; actual initial states were saved/registered. The identified engineering bug was repaired, eight CPU tests passed, and failed outputs remain preserved. This does not refute the learner or scientific hypothesis.

| Arm | Update | Order-new | Combination-new | Combined | Combined CE | Raw record |
|---|---:|---:|---:|---:|---:|---|
| l_lr-5 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-5/capability/update_00000.json) |
| l_lr-5 | 50 | 78.00% | 77.25% | 77.62% | 0.89746392 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-5/capability/update_00050.json) |
| l_lr-4 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-4/capability/update_00000.json) |
| l_lr-4 | 50 | 80.25% | 82.50% | 81.38% | 0.64701936 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-4/capability/update_00050.json) |
| r8_lr-5 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-5/capability/update_00000.json) |
| r8_lr-5 | 50 | 73.50% | 73.00% | 73.25% | 1.02801167 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-5/capability/update_00050.json) |
| r8_lr-4 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-4/capability/update_00000.json) |
| r8_lr-4 | 50 | 73.75% | 76.00% | 74.88% | 0.96421549 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-4/capability/update_00050.json) |


Accuracy is a development observation for the fixed-format full-vocabulary next answer, with novelty relative to task training; test remained closed. LoRA and direct-matrix updates are not equivalent, and equal LRs do not match functional steps. All dual-precision probes are retained, but source gradients are recomputed in each precision, so the comparison includes update-direction and readout-pipeline changes and cannot isolate reader precision error for one fixed perturbation; scientific near-zero thresholds, source efficacy and learner adoption remain Unknown. A raw negative sign does not grant scientific eligibility.

[Raw source-window readout](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/raw_source_window_readout.json) · [Retry artifacts](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z)。

Can establish executed engineering scope and observations. Cannot claim LoRA superiority, format-only change, stable interference, functional decomposition, expert necessity or frequency effect. The researcher chooses the learner/window; no frequency/SAE/Full ran.
