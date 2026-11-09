# Detailed: A12_0_E02 In-Support Capability Calibration

Primary anchor: [12_0](../../../../problem_anchors/12_structured_compositional_mtp_workload/12_00_short_range_single_vs_two_step_composition/12_00_short_range_single_vs_two_step_composition_anchor.md)
Protocol: [protocol.md](protocol.md)
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** remove unseen ordered-rule-pair generalization from the E01 capability gate without changing the short single-step/two-step structure.

**Hypothesis:** at least one formal model scale can stably learn both tasks under NTP and MTP when training and evaluation share rule-pair support.

**Experiment logic:** keep E01 fixed except for pair support, run 24 full trajectories, require exact finite-function stability, and audit how the still-pending threshold changes the composition interaction.

**Conclusion:** capability passes at 2 and 4 layers, and also at the diagnostic 1-layer scale. The remaining calibration pattern is not a general MTP speed advantage: positive two-step interaction appears only at exact accuracy `1.0`.

**Evidence:** job `pt-s9fu4zsd` succeeded; all 24 final standard-head accuracies equal `1.0`; both formal scales maintain exact accuracy through the final 1,000 steps; threshold-surface analysis shows a sign/size change between `0.99` and `1.0`.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| in-support | rule-pair identities seen during training are also evaluated | all 64 ordered rule pairs in train, validation, and test labels | support set | isolates fitting capability from pair generalization | new-pair transfer |
| exact stability | every supported answer remains correct at the end | all test \(q_1\) accuracies from steps 19,000--20,000 equal 1 | Boolean | stage pass criterion | mechanism |
| \(T_{c,o}(\tau)\) | first recorded step reaching accuracy threshold | minimum 100-step checkpoint with accuracy at least \(\tau\) | steps | primary future metric | threshold-independent speed |
| \(G_c(\tau)\) | MTP speed gain for task \(c\) | \(T_{c,\mathrm{NTP}}-T_{c,\mathrm{MTP}}\) | steps | positive favors MTP | composition specificity |
| \(\Gamma(\tau)\) | extra MTP gain for two-step over single-step | \(G_2-G_1\) | steps | anchor interaction | causal use of \(B\) |

## 2. Anchor Link and Decision Point

E01 mixed two uncertainties: learning the ordered two-step finite function and generalizing to held-out rule pairs. It failed the capability gate. E02 changes only the support contract. A pass reopens threshold selection but does not resolve the anchor's objective interaction.

## 3. Protocol Compliance Audit

| Audit item | Result | Evidence |
|---|---|---|
| approved conditions match actual conditions | pass | config snapshot and 24 unique run IDs |
| only pair-support contract changed from E01 | pass | same rule seed, layout, model, objective, optimizer, seeds, and budget |
| primary stage metric exists | pass | complete full-support \(q_1\) trajectories |
| central figures and tables exist | pass | learning curves, threshold interaction, final metrics, threshold table |
| seeds/checkpoints recorded | pass | seeds 1201/1202; every 100 steps through 20,000 |
| known good/bad/confusing reviewed | pass | single-step, E01 failures, one-seed E01 4-layer success |
| confirmation seeds protected | pass | no run ID uses 1301--1305 |
| mechanism verdict avoided | pass | aggregate summary has `mechanism_verdict: null` |

## 4. Setup

### Data construction

```text
[BOS, DEPTH_1|DEPTH_2, STATE_A, RULE_r1, RULE_r2,
 DECIDE, SHARED, ANSWER_Y, EOS]
```

- 32 state symbols.
- Eight fixed random bijections, data seed 1200.
- 64 ordered rule pairs, all shared across train/validation/test support labels.
- 2,048 enumerated inputs per task for validation and test labels; these two labels refer to identical support audits, not independent generalization sets.
- Single-step: \(Y=r_1(A)\).
- Two-step: \(B=r_1(A)\) and \(Y=r_2(B)\).
- Manifest SHA-256: `5beb206fa1b05264448643a32c0749ad4345f80a699fe16de110fd75e1b5dc42`.

### Models and objectives

| Layers | Parameters | Role |
|---:|---:|---|
| 1 | 211,456 | diagnostic capacity floor |
| 2 | 409,728 | formal small scale |
| 4 | 806,272 | formal large scale |

All use width 128, four attention heads, FFN width 512, pre-LN, GELU, learned position embeddings, and dropout 0.

Both objectives instantiate the common \(q_1\) and second \(q_2\) heads:

\[
L_{\mathrm{NTP}}=\operatorname{CE}(q_1(h_t),x_{t+1}),
\]

\[
L_{\mathrm{MTP}}=L_{\mathrm{NTP}}+\operatorname{CE}(q_2(h_t),x_{t+2}).
\]

MTP second-head weight is 1. Parameters and forward computation are matched; backward gradient dose is not.

### Optimization and execution

| Setting | Value |
|---|---:|
| optimizer | AdamW |
| learning rate | \(10^{-3}\) to \(10^{-4}\) cosine |
| warmup | 200 steps |
| betas | \((0.9,0.95)\) |
| weight decay | 0.01 |
| gradient clip | 1.0 |
| batch size | 512 |
| precision | FP32 |
| steps | 20,000 |
| evaluation | every 100 steps |
| seeds | 1201, 1202 |

ACP execution used one reserved `n6ls.iu.i40.4` worker with four N6LS-80G GPUs. Four shards each completed six runs. Job `pt-s9fu4zsd` finished `SUCCEEDED`.

## 5. Metrics and Decision Rules

The capability pass requires at least one formal scale where every task/objective/seed trajectory is exactly correct at every evaluation from step 19,000 through 20,000. This is an exact finite-function criterion, not the future confirmation threshold.

The anchor interaction remains:

\[
\Gamma_d(\tau)=
\left[T_{d,2,\mathrm{NTP}}(\tau)-T_{d,2,\mathrm{MTP}}(\tau)\right]
-
\left[T_{d,1,\mathrm{NTP}}(\tau)-T_{d,1,\mathrm{MTP}}(\tau)\right].
\]

Positive \(\Gamma_d\) means MTP's speed gain is larger for the two-step task. It does not identify why.

## 6. Main Results

### Decision evidence

- All 24 final standard-head answer accuracies are `1.0`.
- All 1-, 2-, and 4-layer task/objective/seed trajectories remain exactly `1.0` from steps 19,000--20,000.
- The aggregate capability gate records formal passing layers `[2, 4]`.
- Complete per-run final metrics: [e02_final_metrics.csv](tables/e02_final_metrics.csv).

### Threshold interaction evidence

| Threshold | Layers | Seed 1201 \(\Gamma\) | Seed 1202 \(\Gamma\) | Mean | Judgment |
|---:|---:|---:|---:|---:|---|
| 0.95 | 2 | 0 | -100 | -50 | no stable positive interaction |
| 0.95 | 4 | 100 | -100 | 0 | no stable positive interaction |
| 0.99 | 2 | -100 | -100 | -100 | MTP not faster in the interaction |
| 0.99 | 4 | 200 | -400 | -100 | seed disagreement |
| 1.00 | 2 | 1,300 | 200 | 750 | positive in both calibration seeds |
| 1.00 | 4 | 1,300 | 100 | 700 | positive in both calibration seeds |

At exact fit, 2-layer two-step NTP/MTP first-hit steps were `2300/1100` and `1300/1100`; 4-layer values were `2700/1400` and `1700/1600`. Single-step exact-fit differences were no larger than 100 steps. Full selected-threshold records: [e02_threshold_selected_checkpoints.csv](tables/e02_threshold_selected_checkpoints.csv).

### Secondary formation evidence

- MTP \(q_2\) final answer accuracy is `1.0` in every task and scale, as expected from direct supervision.
- Two-step MTP probe accuracy for \(B\) is about `0.97--1.00` at 2 and 4 layers.
- Two-step NTP shared-position probe accuracy is about `0.79--0.97`, while decision-position values vary more.
- Because probe train and evaluation share the finite support, these are formation diagnostics only and may include memorization.

## 7. Visualization Results

### In-support learning curves

![In-support learning curves](figures/e02_in_support_learning_curves.png)

- **Purpose:** verify that no task/objective condition remains at a capability floor.
- **Metric/unit:** complete-support standard-head answer accuracy, fraction correct.
- **Aggregation:** two-seed mean with min--max band.
- **Observed:** all conditions converge to and sustain exact accuracy; two-step curves rise later than single-step curves.
- **Take-home:** the behavioral capability prerequisite passes.
- **Remaining uncertainty:** exact fitting may be finite-table memorization.
- **Does not prove:** factorized composition or causal \(B\) use.

### Threshold sensitivity

![Threshold sensitivity](figures/e02_threshold_interaction.png)

- **Purpose:** audit whether the proposed interaction is robust to the undecided threshold.
- **Metric/unit:** \(\Gamma_d(\tau)\) in optimizer steps; positive favors a larger two-step MTP speed gain.
- **Aggregation:** two-seed mean and seed range for each depth.
- **Observed:** mean interactions are near zero or negative through `0.99`, then jump positive at exact `1.0` for formal scales.
- **Take-home:** the candidate effect is localized to exact-fit completion, not broad convergence.
- **Remaining uncertainty:** whether untouched seeds replicate the exact-fit tail and whether the tail uses \(B\).
- **Does not prove:** general MTP superiority or a composition mechanism.

Both figures were rendered and audited for readable titles, axes, legend, units, and visible seed variation. No confirmation threshold is drawn as if approved.

## 8. Stage Evidence and Failure Decomposition

| Stage | Evidence | Status | Interpretation |
|---|---|---|---|
| data-support repair | all 64 pairs overlap train/eval | pass | pair generalization removed as designed |
| single-step known good | all runs exact | pass | implementation and standard-head position valid |
| two-step capability | all runs exact and stable | pass | supported finite function is learnable |
| E01 versus E02 localization | held-out-pair failure becomes in-support success | pass | E01 bottleneck primarily pair composition generalization |
| threshold robustness | interaction changes at exact `1.0` | fail for broad claim | no general training-speed advantage established |
| causal intermediate-state use | probes only, no intervention | not tested | remains owned by `12_03` |

The result falsifies the E01 operationalization as a clean capability gate for the narrow speed question. It does not falsify the physical prior that earlier supervision may help intermediate-state computation. It weakens the assumption that the E02 behavioral task itself enforces such computation.

## 9. Full Experiment Record

- Expected/completed runs: 24/24.
- Curve rows: 9,648 aggregate rows, covering validation/test labels every 100 steps.
- Confirmation threshold: `null`.
- Confirmation seeds used: none.
- Mechanism verdict: `null`.
- Capability gate: passed at 2 and 4 layers.
- Job state: `SUCCEEDED`.

## 10. Interpretation

E01 and E02 together separate two notions that were previously mixed:

1. **fitting the supported deterministic map**, which E02 shows is easy enough even for one layer;
2. **generalizing composition to unseen rule pairs**, which E01 shows is difficult and seed-unstable.

The anchor asks about objective-dependent learning speed, not generalization. E02 therefore supplies a usable behavioral surface, but the scientific interpretation must remain narrow. The threshold audit further refines the candidate phenomenon: MTP does not broadly accelerate the learning curve; it may reduce the time required to eliminate the final supported errors in two-step tasks.

## 11. Claim Boundary

**Can claim:** E02 passes in-support capability; E01 failure localizes mainly to pair-support shift; exact-fit completion has a positive calibration interaction at formal scales.

**Cannot claim:** the exact-fit interaction is confirmed; MTP improves broad convergence; increased composition depth generally increases MTP advantage; an intermediate state is required, formed, or causally used; results transfer beyond this finite synthetic distribution.

## 12. Next Decision

The user must choose the semantic target before confirmation:

- exact deterministic mastery, implying \(\tau=1.0\) and a narrow last-mile hypothesis; or
- broad learning speed, implying a lower threshold and currently no positive calibration premise.

Only after that choice may the untouched confirmation seeds be run.

## 13. Links and Artifact Map

```text
anchor:
  Projects/from-attention-to-search/main/problem_anchors/
    12_structured_compositional_mtp_workload/
    12_0_short_range_single_vs_two_step_composition/
    12_0_short_range_single_vs_two_step_composition_anchor.md

protocol / summary / detailed:
  Projects/from-attention-to-search/main/experiments/A12/
    12_0_short_range_single_vs_two_step_composition/
    A12_0_E02_in_support_capability_calibration/

code workspace:
  Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/

runner:
  active/synthetic_data_understanding/scripts/
    run_a12_0_short_range_single_vs_two_step_calibration.py

threshold analysis:
  active/synthetic_data_understanding/scripts/
    analyze_a12_0_e02_threshold_surface.py

config:
  active/synthetic_data_understanding/configs/
    a12_0_in_support_capability_calibration.json

submitter:
  active/synthetic_data_understanding/scripts/
    submit_a12_0_in_support_capability_calibration_4gpu_acp.sh

result directory:
  active/synthetic_data_understanding/results/
    a12_0_in_support_capability_calibration/
    a12_0_in_support_full_20260714_181202/

key raw outputs:
  calibration_summary.json
  calibration_curves.csv
  final_metrics.csv
  data_manifest.json
  learning_curves.png
  threshold_surface.csv
  threshold_selected_checkpoints.csv
  threshold_interaction.png

logs:
  active/synthetic_data_understanding/logs/acp/
    a12_0_in_support_full_20260714_181202/

job:
  pt-s9fu4zsd
```
