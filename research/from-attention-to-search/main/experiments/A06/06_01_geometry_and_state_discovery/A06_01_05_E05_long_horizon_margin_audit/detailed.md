# Detailed: A06_01_05_E05 Long-Train Margin Audit

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 0. Quick Recap

Purpose: test whether the negative margin observed for full-LM embedding-gradient initialization at 160 steps is only a short-training artifact.

Hypothesis: if longer optimization can rescue the raw selector, embedding-gradient top-k should regain positive margin p05 by 2000 post-reinit steps.

Conclusion: longer training does not rescue the raw selector. It also shows a broader full-LM preservation failure: even oracle and route-position center initializations lose positive low-tail margin by 2000 steps.

Evidence: embedding-gradient top-1 moves from NMI 0.845 and margin p05 -1.828 at step 160 to NMI 0.717 and margin p05 -9.142 at step 2000. Oracle centers move from NMI 0.996 and margin p05 6.221 at step 160 to NMI 0.845 and margin p05 -5.359 at step 2000.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Long-train audit | Extended training after router reinitialization | post-reinit checkpoints 0/160/500/1000/2000 | optimizer steps | Tests short-training explanation | Infinite-horizon behavior |
| Full-LM objective | Predict all next tokens in the sequence | CE across positions 0..30 | \(\mathcal L^{full}\) | Main optimization pressure | Real data transfer |
| Route position | Last feature-slot token | \(r=\mathrm{slot\_start}+\mathrm{slot\_len}-1\) | token position | Where routing is evaluated | Label-free deployment |
| Feature NMI | Feature-to-expert alignment | NMI(feature id, route assignment) | 0 to 1 | Primary separation metric | Expert utility |
| Margin p05 | Low-tail score gap | 5th percentile of matched expert score minus max competitor | router-logit gap | Preservation guard | Output correctness |
| Sign flip rate | Fraction of initially positive-margin samples that become non-positive | computed against checkpoint-0 margin | 0 to 1 | Measures margin erosion | Cause of erosion |

## 2. Protocol Compliance

Approved setup: full-LM loss, warmup 40, central methods, post-reinit training to 2000 steps.

Actual setup: matched.

Coverage: 32/32 seed-slot cells completed.

Rows: 1120 training trajectory rows.

Remote job: `pt-e1vs7ci9`, `SUCCEEDED`.

Runtime log:
`logs/acp/a06_28_long_train_margin_audit_4gpu_20260706_runtime_20260706_074432.log`

Known good status: oracle and route-position controls are excellent at checkpoint 0 and strong at checkpoint 160, but they no longer satisfy positive margin p05 at 2000. This changes the interpretation from "selector-only failure" to "selector failure plus long-term full-LM preservation failure."

## 3. Data, Model, And Training

Data and model are inherited from A06_01_05_E05:

- four uniformly sampled synthetic features;
- three slot starts: 2, 10, 18;
- slot lengths: 1, 2, 4, 8;
- no position embeddings;
- one causal Transformer layer;
- one weighted top-1 MoE layer;
- four experts.

For feature \(f\), feature token ids are \(32+f\) and target token ids are \(36+f\).

The full-LM objective is:

\[
\mathcal L^{full}_i=\sum_{p=0}^{T-2}\mathrm{CE}(\ell_{i,p},x_{i,p+1}).
\]

Router inputs during training and evaluation are raw hidden states. Centering is used only for row construction:

\[
w_e \leftarrow \mathrm{normalize}(\mu_e-\bar \mu).
\]

## 4. Conditions

| Method | Meaning | Uses route position? | Uses feature labels? | Role |
| --- | --- | --- | --- | --- |
| oracle feature centers | feature means at route position | yes | yes | upper bound |
| route-position centers | k-means on route hidden states | yes | no | route-state control |
| embedding-gradient top-1 | cluster top-1 embedding-gradient selected hidden states | no for selection | no | main raw selector |
| embedding-gradient top-4 | same with top-4 positions | no for selection | no | top-k rescue test |
| embedding-gradient top-8 | same with top-8 positions | no for selection | no | top-k rescue test |
| all-position centers | k-means on all hidden states | no | no | noisy-pool baseline |
| no reinit | keep warmup router | no | no | training baseline |

## 5. Main Trajectory

| Method | Checkpoint | Feature NMI | Margin p05 | Preserve fraction | Positive margin fraction | Sign flip rate | Target accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| oracle feature centers | 0 | 1.000 | 11.669 | 1.000 | 1.000 | 0.000 | 0.248 |
| route-position centers | 0 | 0.988 | 10.111 | 0.979 | 0.979 | 0.000 | 0.290 |
| embedding-gradient top-1 | 0 | 0.823 | 0.782 | 0.786 | 0.786 | 0.000 | 0.278 |
| embedding-gradient top-4 | 0 | 0.827 | -2.071 | 0.779 | 0.779 | 0.000 | 0.296 |
| embedding-gradient top-8 | 0 | 0.816 | -2.994 | 0.768 | 0.768 | 0.000 | 0.286 |
| all-position centers | 0 | 0.738 | -2.609 | 0.735 | 0.735 | 0.000 | 0.297 |
| no reinit | 0 | 0.800 | -2.459 | 0.688 | 0.688 | 0.000 | 0.408 |
| oracle feature centers | 160 | 0.996 | 6.221 | 0.997 | 0.997 | 0.003 | 0.514 |
| route-position centers | 160 | 0.982 | 5.550 | 0.971 | 0.971 | 0.013 | 0.552 |
| embedding-gradient top-1 | 160 | 0.845 | -1.828 | 0.750 | 0.750 | 0.135 | 0.554 |
| embedding-gradient top-4 | 160 | 0.796 | -5.159 | 0.685 | 0.685 | 0.155 | 0.554 |
| embedding-gradient top-8 | 160 | 0.810 | -5.401 | 0.642 | 0.642 | 0.191 | 0.517 |
| all-position centers | 160 | 0.612 | -5.835 | 0.595 | 0.595 | 0.230 | 0.553 |
| no reinit | 160 | 0.701 | -4.245 | 0.649 | 0.649 | 0.078 | 0.568 |
| oracle feature centers | 500 | 0.948 | 0.705 | 0.969 | 0.969 | 0.031 | 0.761 |
| route-position centers | 500 | 0.938 | 0.282 | 0.943 | 0.943 | 0.041 | 0.736 |
| embedding-gradient top-1 | 500 | 0.776 | -5.184 | 0.711 | 0.711 | 0.193 | 0.740 |
| embedding-gradient top-4 | 500 | 0.665 | -8.592 | 0.634 | 0.634 | 0.220 | 0.752 |
| embedding-gradient top-8 | 500 | 0.676 | -8.779 | 0.598 | 0.598 | 0.242 | 0.733 |
| all-position centers | 500 | 0.552 | -9.363 | 0.559 | 0.559 | 0.278 | 0.750 |
| no reinit | 500 | 0.569 | -6.292 | 0.601 | 0.601 | 0.205 | 0.832 |
| oracle feature centers | 1000 | 0.924 | -1.416 | 0.945 | 0.945 | 0.055 | 0.879 |
| route-position centers | 1000 | 0.905 | -1.522 | 0.921 | 0.921 | 0.064 | 0.906 |
| embedding-gradient top-1 | 1000 | 0.750 | -6.953 | 0.684 | 0.684 | 0.225 | 0.891 |
| embedding-gradient top-4 | 1000 | 0.629 | -10.628 | 0.609 | 0.609 | 0.247 | 0.914 |
| embedding-gradient top-8 | 1000 | 0.641 | -10.556 | 0.601 | 0.601 | 0.247 | 0.887 |
| all-position centers | 1000 | 0.457 | -12.380 | 0.510 | 0.510 | 0.344 | 0.892 |
| no reinit | 1000 | 0.537 | -7.884 | 0.554 | 0.554 | 0.275 | 0.932 |
| oracle feature centers | 2000 | 0.845 | -5.359 | 0.883 | 0.883 | 0.117 | 0.954 |
| route-position centers | 2000 | 0.857 | -4.531 | 0.887 | 0.887 | 0.098 | 0.959 |
| embedding-gradient top-1 | 2000 | 0.717 | -9.142 | 0.657 | 0.657 | 0.263 | 0.971 |
| embedding-gradient top-4 | 2000 | 0.583 | -13.366 | 0.565 | 0.565 | 0.292 | 0.962 |
| embedding-gradient top-8 | 2000 | 0.602 | -13.256 | 0.573 | 0.573 | 0.282 | 0.969 |
| all-position centers | 2000 | 0.449 | -14.249 | 0.501 | 0.501 | 0.356 | 0.976 |
| no reinit | 2000 | 0.473 | -8.819 | 0.520 | 0.520 | 0.323 | 0.969 |

## 6. Slot-Length Audit

At step 2000, the negative-margin result is broad across slot lengths.

Feature NMI:

| Slot length | oracle | route-position | emb grad top-1 | emb grad top-4 | emb grad top-8 | all-position | no reinit |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.913 | 0.955 | 0.704 | 0.577 | 0.649 | 0.220 | 0.642 |
| 2 | 0.803 | 0.837 | 0.721 | 0.607 | 0.505 | 0.253 | 0.271 |
| 4 | 0.846 | 0.760 | 0.801 | 0.515 | 0.549 | 0.575 | 0.496 |
| 8 | 0.817 | 0.878 | 0.643 | 0.632 | 0.704 | 0.746 | 0.484 |

Margin p05:

| Slot length | oracle | route-position | emb grad top-1 | emb grad top-4 | emb grad top-8 | all-position | no reinit |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | -1.660 | 0.218 | -11.002 | -9.571 | -9.354 | -12.240 | -6.280 |
| 2 | -7.805 | -8.156 | -8.612 | -14.813 | -16.548 | -17.877 | -9.550 |
| 4 | -5.665 | -8.153 | -6.270 | -17.723 | -16.521 | -18.000 | -9.477 |
| 8 | -6.308 | -2.034 | -10.683 | -11.355 | -10.599 | -8.879 | -9.967 |

Only route-position centers at slot length 1 remain slightly positive at the
5th percentile. This is not enough to rescue the aggregate claim.

## 7. Visualization Results

### Figure: NMI And Margin Trajectory

![NMI and margin trajectory](figures/a06_28_long_train_nmi_margin_trajectory.png)

Purpose: show whether extended full-LM training rescues or erodes margins.

Setup: full-LM loss, warmup 40, post-reinit checkpoints 0/160/500/1000/2000,
mean over 8 seeds and 4 slot lengths.

How to read: the left panel should stay high for feature alignment; the right
panel must remain above zero for low-tail margin preservation.

Observed result: raw gradient-selected methods decline steadily. Oracle and
route-position controls also cross below zero between 500 and 1000 steps.

Take-home: longer full-LM training does not fix raw gradient selection and
introduces a broader preservation problem.

Remaining uncertainty: the figure does not identify which training component
causes margin erosion.

### Figure: Step-2000 Final State

![Step-2000 final state](figures/a06_28_long_train_final_step2000.png)

Purpose: compare final routing quality at 2000 steps.

Setup: same as above, checkpoint 2000 only.

How to read: high NMI with negative margin means the routing partition is
partly aligned but not margin-safe.

Observed result: oracle and route-position controls retain the best NMI, but
all methods have negative aggregate margin p05.

Take-home: clean center initialization is still better than gradient selection,
but it is not sufficient for long full-LM preservation.

### Figure: Step-2000 Slot Boundary

![Step-2000 slot boundary](figures/a06_28_long_train_slot_boundary_step2000.png)

Purpose: check whether the step-2000 result is an artifact of one slot length.

Setup: checkpoint 2000, mean over 8 seeds for each slot length.

How to read: robust preservation should show positive margin across slot
lengths.

Observed result: the margin is negative for almost every method and slot length.

Take-home: the long-train margin failure is broad.

## 8. Failure Decomposition

Result: longer training does not rescue the raw selector.

Evidence: embedding-gradient top-1 margin p05 worsens from -1.828 at 160 steps
to -9.142 at 2000 steps. Top-4 and top-8 worsen further.

Result: full-LM training also erodes clean-center margins.

Evidence: oracle center margin p05 changes from 11.669 at step 0 to 6.221 at
160, 0.705 at 500, -1.416 at 1000, and -5.359 at 2000.

Mechanism interpretation:

\[
\nabla \mathcal L^{full}
=\nabla \mathcal L^{feature-target}
+\nabla \mathcal L^{neutral-background}
+\nabla \mathcal L^{other-token}.
\]

The long-run objective rewards next-token prediction, not preservation of the
initial feature-to-expert partition. As target accuracy rises, the router can
move toward a different solution space where the output is solved but the
feature-specific score gap is thin or inverted.

## 9. Claim Boundary

Can claim:

- The 160-step raw selector failure is not fixed by training to 2000 steps.
- Full-LM long training can erode positive margins even from clean feature or
  route-position centers.
- Feature-center initialization is still meaningful at initialization and early
  training; the new issue is long-run preservation under full-LM optimization.

Cannot claim:

- Full-LM always destroys feature partitions in larger or real models.
- Feature-center initialization is invalid.
- Denoised gradient selection cannot work.
- Preservation interventions are unnecessary.

## 10. Next Decision

The mainline should split the next decision:

1. Selector decision: can a denoised full-LM gradient score choose a cleaner
   state pool than raw top-k?
2. Preservation decision: once a clean center is available, what training-time
   intervention preserves margin under full-LM optimization?

Candidate preservation interventions include router-row freezing for an early
window, routing-time centering, explicit margin regularization, and reduced
router learning rate.

## 11. Artifact Map

Experiment folder:
`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E05_long_horizon_margin_audit/`

Protocol: `protocol.md`

Submission script: `submit_a06_28_long_train_margin_audit_4gpu_acp.sh`

Runner reused:
`../A06_01_05_E04_full_lm_gradient_guard/scripts/run_a06_28_full_sequence_lm_gradient_selector_guard.py`

Remote job:

| Field | Value |
| --- | --- |
| job id | `pt-e1vs7ci9` |
| status | `SUCCEEDED` |
| run name | `a06_28_long_train_margin_audit_4gpu_20260706` |
| runtime log | `logs/acp/a06_28_long_train_margin_audit_4gpu_20260706_runtime_20260706_074432.log` |

Tables:

- `tables/training_trajectory.csv`
- `tables/condition_trajectory_aggregate.csv`
- `tables/condition_aggregate_reinit.csv`
- `tables/condition_aggregate_final.csv`
- `tables/selector_diagnostics_aggregate.csv`
- `tables/data_audit.csv`

Central figures:

- `figures/a06_28_long_train_nmi_margin_trajectory.png`
- `figures/a06_28_long_train_final_step2000.png`
- `figures/a06_28_long_train_slot_boundary_step2000.png`

## 12. Repro Command

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 torchrun --standalone --nproc_per_node=4 \
  Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E04_full_lm_gradient_guard/scripts/run_a06_28_full_sequence_lm_gradient_selector_guard.py \
  --run-stage full \
  --run-name a06_28_long_train_margin_audit_4gpu_20260706 \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E05_long_horizon_margin_audit \
  --loss-modes full_lm \
  --warmup-steps 40 \
  --train-steps 2000 \
  --checkpoints "0 160 500 1000 2000" \
  --methods "no_reinit allpos_centered route_centered oracle_centered grad_emb_top1_centered grad_emb_top4_centered grad_emb_top8_centered" \
  --selector-topks "1 4 8"
```
