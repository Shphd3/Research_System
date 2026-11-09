# Detailed: A06_02_01_E08 Noise-Free Full-Slot Preservation

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## 1. Purpose

This experiment tests whether the long full-LM preservation failure from A06_01_05_E04/A06_02_02_E04 requires background or non-feature positions. The test removes background tokens entirely and trains on sequences where every token position is the same feature token.

## 2. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Full-slot | The entire sequence is occupied by the feature token | \(x=(F_f,\ldots,F_f)\) | length 32 | Removes background positions | Natural data behavior |
| Ideal centers | Label-known hidden-state centers by feature | average hidden state by feature | vector | Clean initialization positive control | Label-free method |
| All-position routing | Routing evaluated at every token position | flatten all token routes | assignments | Tests the full-slot surface directly | Expert utility |
| Predictive positions | Positions included in next-token loss | positions 0 to 30 | token positions | Guard against last-token-only artifacts | Full sequence semantics |
| Margin p05 | 5th percentile matched score gap | \(s_{a(f)}-\max_{e\ne a(f)}s_e\) | router logit | Low-tail preservation guard | Correct prediction |

## 3. Data Construction

Four feature tokens are available. For each sample:

\[
f\sim \operatorname{Uniform}\{0,1,2,3\},
\]

and:

\[
x_t=F_f,\quad t=0,\ldots,31.
\]

There are no neutral/background tokens. Calibration and evaluation sets are balanced across the four features. Training batches sample features uniformly.

The supervised LM positions are 0 to 30:

\[
L=\sum_{t=0}^{30}\operatorname{CE}(\ell_t,x_{t+1}).
\]

Because \(x_{t+1}=F_f\) for all supervised positions, every supervised position carries feature identity.

## 4. Model And Training

Model:

- one causal Transformer layer;
- hidden size 64;
- four attention heads;
- one weighted top-1 MoE layer;
- four experts;
- expert FFN size 128.

Training:

- optimizer: AdamW;
- learning rate: 0.002;
- weight decay: 0.0001;
- gradient clip: 1.0;
- batch size: 256;
- training length: 2000 steps;
- checkpoints: 0, 160, 500, 1000, 2000;
- seeds: 0 to 7.

## 5. Conditions

| Condition | Meaning | Why included |
| --- | --- | --- |
| random | no center reinitialization | bad-init guard |
| oracle_allpos | router rows from feature centers over all token positions | main ideal-center test |
| oracle_predpos | router rows from feature centers over positions 0 to 30 | guards against last-position mismatch |
| oracle_lastpred | router rows from feature centers at position 30 | closest analog to old route-position evaluation |

All oracle center rows are equal-norm normalized with router initialization scale 1.5.

## 6. Metrics

Primary metric:

\[
\operatorname{NMI}(\text{feature id}, \text{routed expert})
\]

computed over all token positions.

Preservation guard:

\[
\operatorname{margin}_{p05}
=
\operatorname{percentile}_{5}
\left[
s_{a(f)}(h)-\max_{e\ne a(f)}s_e(h)
\right].
\]

Secondary metrics:

- matched preserve fraction;
- positive margin fraction;
- sign-flip rate;
- predictive-position feature NMI;
- last-predictive-position feature NMI;
- next-token accuracy;
- loss;
- max load and effective experts.

## 7. Result Tables

### 7.1 Step 0

| Condition | All-position NMI | Margin p05 | Matched preserve | Positive margin frac | Max load |
| --- | ---: | ---: | ---: | ---: | ---: |
| oracle_allpos | 1.000 | 11.515 | 1.000 | 1.000 | 0.250 |
| oracle_predpos | 1.000 | 11.515 | 1.000 | 1.000 | 0.250 |
| oracle_lastpred | 1.000 | 11.515 | 1.000 | 1.000 | 0.250 |
| random | 0.789 | -1.003 | 0.656 | 0.656 | 0.562 |

### 7.2 Step 2000

| Condition | All-position NMI | Margin p05 | Matched preserve | Positive margin frac | Max load | Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| oracle_allpos | 1.000 | 4.566 | 1.000 | 1.000 | 0.250 | 1.000 |
| oracle_predpos | 1.000 | 4.566 | 1.000 | 1.000 | 0.250 | 1.000 |
| oracle_lastpred | 1.000 | 4.566 | 1.000 | 1.000 | 0.250 | 1.000 |
| random | 0.789 | -2.964 | 0.594 | 0.594 | 0.562 | 1.000 |

## 8. Visualization Results

### Figure: Margin p05 Trajectory

![Margin p05 trajectory](figures/margin_p05_trajectory.png)

Purpose: test whether ideal-center margins cross zero under long no-background full-LM training.

Setup: 8 seeds, checkpoints 0/160/500/1000/2000, all-position token evaluation.

How to read: positive values mean the low-tail routed tokens remain inside the matched expert region.

Observed result: oracle conditions drop from margin p05 11.515 to 3.051 by step 160, then remain positive and reach 4.566 at step 2000. Random remains negative.

Take-home: no-background full-slot training does not reproduce the prior ideal-center margin collapse.

Remaining uncertainty: the figure does not identify the exact background-gradient component that caused the mixed-setting failure.

### Figure: All-Position Feature NMI

![All-position feature NMI trajectory](figures/allpos_feature_nmi_trajectory.png)

Purpose: test whether feature-to-expert assignment remains pure across every token position.

Observed result: oracle conditions stay at NMI 1.000 throughout training. Random stays at about 0.789.

Take-home: ideal center routing is preserved as a partition, not only as a positive-margin center.

### Figure: Next-Token Accuracy

![Next-token accuracy trajectory](figures/next_token_accuracy_trajectory.png)

Purpose: check whether routing preservation is confounded by failure to learn the repeated-token LM task.

Observed result: all conditions reach next-token accuracy 1.000 after training.

Take-home: task learning does not by itself certify feature routing; random learns the task but remains negative-margin.

## 9. Interpretation

The run supports the user's hypothesis in a bounded form. When the all-position LM objective contains only feature-bearing positions, ideal feature-center routing survives long training. Therefore the prior mixed-setting erosion is not an unavoidable consequence of long training or top-1 gating alone.

However, the result does not prove that "background gradient noise" is the only cause. It only shows that removing background/non-feature positions removes the failure in this synthetic surface. The next mechanism needs a graded intervention that reintroduces background positions while measuring margin-budget terms.

## 10. Claim Boundary

Supported:

- no-background full-slot data preserves ideal feature-center routing under 2000 full-LM steps;
- the mixed full-LM preservation failure requires some ingredient absent from the full-slot data;
- background/non-feature positions are a strong candidate ingredient.

Not supported:

- full causal decomposition of the previous failure;
- real-DCLM preservation;
- utility of the preserved partition;
- label-free initialization.

## 11. Source Map

Anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol:
`protocol.md`

Runner:
`scripts/run_a06_30_noise_free_full_slot_preservation.py`

Run:
`a06_30_full_20260709_090858`

Tables:

- `tables/data_audit.csv`
- `tables/training_trajectory.csv`
- `tables/condition_trajectory_aggregate.csv`
- `tables/condition_aggregate_reinit.csv`
- `tables/condition_aggregate_final.csv`

Figures:

- `figures/margin_p05_trajectory.png`
- `figures/allpos_feature_nmi_trajectory.png`
- `figures/next_token_accuracy_trajectory.png`
- `figures/final_allpos_feature_nmi.png`
- `figures/final_margin_p05.png`

Smoke run:
`a06_30_smoke_20260709_090843`

Full run:
completed locally on one H100 GPU.

