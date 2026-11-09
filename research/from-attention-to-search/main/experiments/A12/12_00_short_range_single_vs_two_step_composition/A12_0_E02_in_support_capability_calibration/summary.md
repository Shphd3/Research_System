# Summary: A12_0_E02 In-Support Capability Calibration

Primary anchor: [12_0 short-range single-step versus two-step composition](../../../../problem_anchors/12_structured_compositional_mtp_workload/12_00_short_range_single_vs_two_step_composition/12_00_short_range_single_vs_two_step_composition_anchor.md)
Protocol: [protocol.md](protocol.md)

## Result Snapshot

**Verdict:** capability supported; the NTP/MTP mechanism comparison remains unconfirmed.

**What we established:** after training and evaluation shared all 64 ordered rule pairs, every 1-, 2-, and 4-layer condition reached exact full-support standard-head answer accuracy `1.0`. The two formal scales, 2 and 4 layers, maintained `1.0` at every evaluation from step 19,000 through 20,000 under both tasks, both objectives, and both seeds.

**What the experiment shows:** E01's main blocker was unseen rule-pair composition generalization, not inability to fit the supported finite function. It also shows that this E02 carrier permits one-layer exact fitting, so behavioral success need not imply factorized intermediate-state computation.

**What we do next:** the user must fix the confirmation accuracy threshold before untouched seeds 1301--1305 can run. Calibration reveals that this choice changes the scientific claim: thresholds through `0.99` show no stable composition-specific MTP speed gain, while exact `1.0` shows a positive last-mile interaction at both formal scales.

## Purpose

E02 changes only the ordered-rule-pair support contract from E01. It asks whether the short single-step/two-step comparison becomes behaviorally learnable when pair generalization is removed.

## Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| full-support accuracy | correctness on every supported rule-pair/state input | 64 ordered rule pairs × 32 states = 2,048 inputs per task | fraction correct | exact `1.0` means the finite function is fully fitted | unseen-pair generalization |
| standard head | common next-token output surface | \(q_1(h_{\mathrm{SHARED}})\) predicts `ANSWER_Y` | accuracy | fair NTP/MTP outcome | internal causal path |
| MTP speed gain | NTP steps minus MTP steps at the same threshold | \(G_c(\tau)=T_{c,\mathrm{NTP}}-T_{c,\mathrm{MTP}}\) | optimizer steps | positive means MTP reaches the threshold sooner | composition specificity alone |
| composition interaction | difference between two-step and single-step MTP gains | \(\Gamma(\tau)=G_2(\tau)-G_1(\tau)\) | optimizer steps | positive means MTP's speed gain is larger for two-step | use of intermediate state \(B\) |

## Exact Setup

- Data: fixed nine-token sequences, 32 states, eight fixed bijective rules, all 64 ordered rule pairs shared across training and evaluation.
- Tasks: \(Y=r_1(A)\) for single-step; \(B=r_1(A)\) and \(Y=r_2(B)\) for two-step.
- Models: decoder-only Transformers with 1, 2, or 4 layers; width 128; four heads; FFN width 512.
- Objectives: NTP versus standard two-head MTP with \(K=2\) and second-head loss weight 1.
- Training: AdamW, batch 512, 20,000 steps, evaluation every 100 steps, seeds 1201 and 1202.
- Full run: ACP job `pt-s9fu4zsd`, four N6LS-80G GPUs, 24/24 conditions complete.
- Known limitation: evaluation is in-support and may reward finite-table memorization.

## Primary Metric

The anchor-primary metric remains the first step at which the standard head reaches a user-fixed accuracy threshold \(\tau\). It is not assigned in E02. For the capability stage, exact full-support stability is decisive because `1.0` means all 2,048 supported inputs are correct.

False positive cost: calling a partially or transiently learned task eligible would manufacture an objective comparison. False negative cost: requiring exact fit may emphasize the last few errors rather than broad convergence.

## Result

Final full-support standard-head answer accuracy was `1.0` for all 24 runs. The exact-stability capability rule passed at both formal scales:

| Formal scale | Single NTP/MTP, both seeds | Two-step NTP/MTP, both seeds | Steps 19,000--20,000 | Capability |
|---:|---:|---:|---:|---|
| 2 layers | 1.0 | 1.0 | every evaluation 1.0 | pass |
| 4 layers | 1.0 | 1.0 | every evaluation 1.0 | pass |

The 1-layer diagnostic also satisfied exact stability. This strengthens the learnability result but weakens any claim that task success itself forces an explicit multi-stage internal algorithm.

## Key Figures

### Figure 1: In-support learning curves

![In-support learning curves](figures/e02_in_support_learning_curves.png)

**What this tests:** whether each objective learns both finite target functions at each depth.
**How to read:** rows are model depth; columns are task structure; solid lines are the two-seed mean and bands span the seeds.
**Observed result:** every panel reaches and sustains exact accuracy. Two-step learning is slower than single-step, but no condition remains at a capability floor.
**Take-home:** the in-support surface is eligible for a later speed comparison.
**Does not prove:** unseen-pair composition, intermediate-state use, or MTP advantage.

### Figure 2: Threshold sensitivity of the composition interaction

![Threshold sensitivity](figures/e02_threshold_interaction.png)

**What this tests:** whether the sign and size of \(\Gamma(\tau)\) are stable to the still-undecided threshold.
**How to read:** positive values mean MTP's speed gain is larger for two-step than single-step; each line is the two-seed mean and each band spans both seeds.
**Observed result:** from accuracy `0.50` through `0.99`, the interaction is near zero or negative and is not seed-stable. At exact `1.0`, it becomes positive for both seeds at 2 and 4 layers.
**Take-home:** calibration suggests a narrow last-mile exact-fitting effect, not a general learning-speed advantage.
**Does not prove:** that the exact-fit effect will replicate on untouched seeds or comes from earlier supervision of \(B\).

Selected calibration values:

| Threshold | 2-layer \(\Gamma\), seeds 1201/1202 | 4-layer \(\Gamma\), seeds 1201/1202 | Reading |
|---:|---:|---:|---|
| 0.95 | 0 / -100 | 100 / -100 | no stable advantage |
| 0.99 | -100 / -100 | 200 / -400 | no stable advantage |
| 1.00 | 1,300 / 200 | 1,300 / 100 | positive exact-fit tail in calibration |

## Claim Boundary

**Can claim:** the fixed-length in-support carrier is learnable under both objectives at the two formal scales; E01 failure primarily localizes to unseen pair generalization; the calibration interaction is threshold-sensitive.

**Cannot claim:** MTP generally learns two-step composition faster; MTP uses the intermediate state; one-layer or larger models learned a compositional algorithm rather than a finite table; the exact-fit interaction replicates on new seeds.

## Next Decision

Fix the meaning of “the task has been learned” before confirmation:

- choose \(\tau=1.0\) if the scientific object is exact satisfaction of every supported deterministic case;
- choose a lower mastery threshold if the object is broad convergence, accepting that current calibration does not show a composition-specific MTP advantage there.

This semantic decision must be made before confirmation results are visible.
