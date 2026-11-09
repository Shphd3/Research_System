# Summary: A12_0_E04 Balanced Per-Sample Dual-Map Carrier — Stage A

Primary anchor: [12_0 short-range single-step versus two-step composition](../../../../problem_anchors/12_structured_compositional_mtp_workload/12_00_short_range_single_vs_two_step_composition/12_00_short_range_single_vs_two_step_composition_anchor.md)
Protocol: [protocol.md](protocol.md)
Detailed record: [detailed.md](detailed.md)

## Result Snapshot

**Verdict: Stage A is blocked. Do not run MTP.**

**What we established:** all 12 approved NTP trajectories completed, but neither the 2-layer nor the 4-layer scale stably learned both task depths across all three seeds. No model scale is eligible and no mastery threshold is frozen.

**What the experiment shows:** 4-layer one-step learning is possible but seed-unstable: two seeds finished near `0.999`, while one finished at `0.838`. All 4-layer two-step seeds instead converged near `0.329`. The 2-layer two-step seeds converged near `0.250`. These are capability-floor results, not evidence for or against MTP.

**What the audit corrected:** the proposed row-removal guard is invalid for bijections. Removing one of five rows does not make the mapping unidentifiable because the missing output is the only active alias unused by the other four rows. The original automatic aggregate incorrectly marked this guard as passed; the post-run audit corrected it to failed.

**What we do next:** decide whether to close E04 as an ineligible carrier under the frozen 2/4-layer, 20,000-step contract or reopen carrier design under a new capability-only Protocol. Stage B remains blocked in either case until a valid NTP capability gate passes.

## Purpose

Stage A asked only whether the paired 31-token carrier is structurally valid, learnable under NTP at at least one formal scale, not immediately saturated, and capable of freezing a standard-head accuracy threshold before any MTP result exists.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| standard-head answer accuracy | fraction of held-out calibration examples whose final answer is predicted by the ordinary next-token head | top-1 prediction from `SHARED` equals the final alias | fraction in \([0,1]\) | primary task-capability measurement | internal representation or causal use of \(B\) |
| final-window minimum | worst answer accuracy from steps 19,000 through 20,000 | minimum over 11 evaluations spaced by 100 steps | fraction | prevents one transient high checkpoint from passing capability | why a run is stable or unstable |
| eligible scale | one layer count for which both task depths and all three seeds pass the final-window and non-saturation rules | all six trajectories at that layer count satisfy the Protocol | Boolean | decides whether a later objective comparison is admissible | MTP benefit |
| query-hidden predictor | generator-aware answer guess after hiding query \(A\) | enumerate admissible query roles under the observed maps and choose the modal answer | accuracy | measures leakage from rejection rules | that a trained model uses this shortcut |
| first-hop output | the two-step model outputs \(B=pi_1(A)\) instead of final \(Y\) | top-1 rate and probability assigned to \(B\) at `SHARED` | fraction / probability | distinguishes first-lookup-only behavior from other failure | an internal \(B\) state |

## Exact Setup

- **Data:** fresh five-node active set, two per-sample bijections, shuffled rows and table order, paired one-step and two-step examples, fixed length 31, only the final alias emitted.
- **Model:** decoder-only pre-LN Transformer, width 128, 4 attention heads, FFN width 512, 2 or 4 layers; identical standard and second-head parameterization in every run.
- **Objective:** NTP only, using full-position next-token cross-entropy. The second head was instantiated but never included in the loss.
- **Training:** AdamW, batch 512, 20,000 optimizer steps, evaluation every 100 steps, three seeds `1201`--`1203`, FP32.
- **Calibration:** 8,192 fixed balanced examples. The 8,192-example future confirmation set received structural generation checks only; no model was evaluated on it.
- **Changed variables:** task depth, Transformer layer count, random seed.
- **Held fixed:** sequence length, facts, vocabulary, answer position, serialization, objective, optimizer, training budget, and paired base-instance stream within a scale and seed.
- **Remote job:** `pt-9863fywz`, four reserved H100 80GB GPUs, state `SUCCEEDED`.
- **Known limitation:** the row-removal necessity guard was found logically invalid after the run; the trajectories remain descriptive capability evidence but E04 is not a protocol-valid carrier.

## Primary Metric And Decision Rule

A trajectory's final capability condition is that every evaluation from step 19,000 through 20,000 has standard-head answer accuracy at least `0.95`. A scale qualifies only if both task depths and all three seeds pass. At least one scale must qualify before a threshold can be frozen.

This strict rule prevents a successful seed or task from being averaged with an unlearned one. Its false-positive cost is admitting a floor-limited comparison; its false-negative cost is rejecting a real but seed-unstable learner.

## Main Results

| Layers | Task | Seed 1201 final | Seed 1202 final | Seed 1203 final | Mean final | All seeds pass final window? | Scale eligible? |
|---:|---|---:|---:|---:|---:|---|---|
| 2 | one-step | 0.6187 | 0.3727 | 0.8716 | 0.6210 | no | no |
| 2 | two-step | 0.2504 | 0.2485 | 0.2499 | 0.2496 | no | no |
| 4 | one-step | 0.9993 | 0.8375 | 0.9983 | 0.9450 | no | no |
| 4 | two-step | 0.3281 | 0.3268 | 0.3308 | 0.3286 | no | no |

The group mean is descriptive only. Eligibility is decided by every seed and every final-window checkpoint, so the 4-layer one-step mean of `0.9450` cannot be rounded into a pass.

### Generator and shortcut audit

| Check | Result | Meaning |
|---|---:|---|
| calibration/confirmation fingerprint overlap | 0 | no repeated base instance across fixed splits |
| answer balance for both tasks and fixed splits | exact | alias frequency cannot predict above the balanced marginal |
| paired common tokens | exact match | task pairs differ only at `DEPTH` and final `ANSWER` |
| query-hidden predictor | 0.5668 | rejection rules leak substantial answer information, but below every candidate threshold in `0.80`--`0.99` |
| frequency-only predictor | 0.2009 / 0.2031 | near five-candidate chance for one-step / two-step |
| first-row-value predictor | 0.2024 / 0.2004 | row position does not expose the answer |
| swapped relation order | 0.2146 / 0.0000 | reverse composition is excluded for two-step |
| remove required row | **still identifiable** | failed guard: bijection completion recovers the missing output |

## Key Figure

### NTP answer-learning trajectories

![NTP answer-learning trajectories](figures/stage_a_learning_curves.png)

**What this tests:** whether at least one formal model scale learns both task depths across seeds without an immediate ceiling.

**Metric:** calibration-set standard-head final-answer accuracy, averaged across three seeds; shading is the seed minimum-to-maximum range. The horizontal dashed line is `0.95`; the vertical dotted line is step 2,000.

**How to read:** a qualifying scale needs both its one-step and two-step panels to lie above `0.95` throughout the final window for every seed. The mean curve alone cannot qualify a scale.

**Observed result:** 4-layer one-step runs show late learning and large seed spread, while both two-step groups plateau far below capability. No group reaches exact accuracy early.

**Allowed claim:** the approved 2/4-layer, 20,000-step NTP setup does not provide a shared learnable carrier.

**What this does not prove:** that the two-step task is impossible, that MTP would fail, that the model lacks an intermediate representation, or that more capacity or another valid carrier would not learn.

## Per-Condition Meaning

- **2-layer one-step:** partial and strongly seed-dependent learning (`0.373`--`0.872` final); the scale lacks robust one-step capability.
- **2-layer two-step:** all seeds converge near `0.250`; the result is reproducible failure, not seed noise.
- **4-layer one-step:** two seeds learn almost exactly, but one remains at `0.838`; capacity is sufficient for some initializations but not stable under the Protocol.
- **4-layer two-step:** all seeds converge near `0.329`; extra depth improves the plateau over 2 layers but remains far from task mastery.
- **Two-step first-hop error:** 4-layer models output \(B\) only about `0.132` of the time with about `0.122` probability mass, so the failure is not simply “the model learned the first lookup and stopped.”

## Claim Boundary

**Can claim:** E04 Stage A completed without infrastructure failure; its 2/4-layer NTP carrier fails the shared capability gate, and its row-removal necessity guard is invalid under bijective maps.

**Cannot claim:** whether NTP or MTP is faster, whether MTP has a composition-depth interaction, whether the model forms or causally uses \(B\), whether the task would pass with a larger learner, or whether the behavior transfers beyond this synthetic setup.

## Next Decision

Choose whether to close E04 as an ineligible carrier under the approved contract or reopen the carrier/capability design in a new Protocol. Do not run Stage B or any MTP condition from E04 as currently specified.
