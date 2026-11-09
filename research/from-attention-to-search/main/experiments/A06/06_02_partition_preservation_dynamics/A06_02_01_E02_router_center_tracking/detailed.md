---
experiment_id: A06_02_01_E02_router_center_tracking
anchor_id: A06_02_01_E02_router_center_tracking
status: completed
run_name: a06_17_02_router_center_tracking_full_20260626_024804
job_id: local-two-gpu
canonical_language: en
---

# Detailed: A06_02_01_E02 Router-Center Tracking Preservation

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol:
`protocol.md`

Summary:
`summary.md`

## 0. Quick Recap

Purpose:
classify how feature-center initialization preserves clean routing in the
controlled A06 no-position bridge.

Hypothesis:
successful preservation could come from active center tracking, stable route
margin, random rediscovery, or common / norm drift.

Experiment logic:
run the corrected A06 bridge with center, random, norm-controlled, and shuffled
center initializations, then track router rows, route-position feature centers,
raw margins, common share, and route NMI across training snapshots.

Conclusion:
active tracking is weakened. Pseudo-center and oracle-center initialization
preserve feature-route NMI at 1.0 for all C0-C3 cells and all 8 seeds, but
their movement alignment is negative. The preservation mode is best described
as feature-specific positive-margin preservation.

Evidence:
center initialization has final feature NMI 1.0, positive final raw margins
about 3.5, and low common share about 0.26. Random and equal-norm random reach
task accuracy 1.0 but have lower / unstable feature NMI and negative raw
margins. Label-shuffled centers have high common share and do not cleanly
preserve the partition.

## 1. Anchor Link And Decision Point

Decision question:
in the controlled setting where center initialization preserves routing, does
the router preserve the partition by actively tracking feature centers, by
staying inside a strong initial margin, or by drifting through common /
norm-dominated effects?

Decision after this run:
preservation is real for center initialization, but the active-tracking branch
is not supported. The next decision should target construction and preservation
of positive route margins from label-free route-relevant hidden states.

## 2. Protocol Compliance Audit

| Check | Status | Evidence |
| --- | --- | --- |
| Approved before execution | passed | user approved the protocol before local run |
| Conditions match protocol | passed | C0-C3, pseudo, oracle, random, equal-norm random, shuffled-center guard |
| Seeds match protocol | passed | 8 seeds, 20260623 through 20260630 |
| Snapshots recorded | passed | 0, 1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1600 |
| Primary metric exists | passed | `a_move_mean` in `router_center_metrics_by_step.csv` |
| Guard metrics exist | passed | NMI, margins, dot products, common share, norm growth, matching guards |
| Figures exist and render | passed | 7 nonblank PNGs in `figures/` |
| Known good case reviewed | passed | center initialization keeps feature NMI 1.0 |
| Known bad / confusing cases reviewed | passed | random and shuffled guards learn target but do not preserve clean route partition |

## 3. Setup

Code workspace:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`

Runner:
`scripts/run_a06_17_02_router_center_tracking_preservation.py`

Config:
`configs/a06_17_02_router_center_tracking_preservation.json`

Run:
`a06_17_02_router_center_tracking_full_20260626_024804`

Execution:
local two-GPU run with shards on `CUDA_VISIBLE_DEVICES=0` and
`CUDA_VISIBLE_DEVICES=1`.

Data:

- vocabulary size 4096;
- sequence length 32;
- 4 features, 4 nuisance ids, 4 experts;
- feature slot length 4;
- slot starts `[2, 10, 18]`;
- route position is the last token of the feature slot;
- balanced audit population over feature id, nuisance id, and slot start.

Model:

- one-layer Transformer + top-1 MoE;
- `d_model=128`;
- 4 attention heads;
- MoE `ffn_dim=256`;
- dot-product router;
- no learned absolute positional embedding;
- dropout 0.0.

Training:

- objective: `slot_end_target_ce`;
- steps: 1600;
- batch size: 512;
- learning rate: 0.0008;
- weight decay: 0.01;
- gradient clipping: 1.0.

## 4. Metrics And Decision Rules

Primary metric:

\[
A_{\mathrm{move}}(t)=
\frac{1}{F}\sum_e
\cos\left(\Delta w_e(t),\Delta \tilde{\mu}_{\pi(e)}(t)\right).
\]

This metric decides active tracking because it directly asks whether router-row
movement points with matched common-centered feature-center movement.

Main guards:

- feature-route NMI, used to check that the partition is actually preserved;
- raw route margin at feature centers, used to test whether centers remain
inside intended router regions;
- matched router-center dot and cosine, used to test feature-specific logit
alignment;
- common share, used to test whether common projection dominates;
- row-norm growth, used to test whether norm growth alone explains logit
changes;
- matching-change guard, used to detect expert permutation artifacts.

Decision rules:

- active tracking requires preserved feature NMI and high positive
  \(A_{\mathrm{move}}\) without common / norm dominance;
- positive-margin preservation requires preserved feature NMI and positive raw
  margins under correct center initialization;
- random rediscovery requires random or equal-norm random to reach the same
  NMI, margin, and center-dot profile as center initialization;
- common / norm drift requires common share or norm growth to explain the
  successful preservation better than feature-specific margins.

## 5. Main Results

### 5.1 Decision Evidence

Final-step decision table, averaged over 8 seeds:

| Cell | Condition | Feature NMI mean | Feature NMI min | \(A_{\mathrm{move}}\) mean | Raw margin min mean | Common share mean |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| C0 | pseudo-center | 1.000 | 1.000 | -0.407 | 3.344 | 0.277 |
| C0 | oracle-center | 1.000 | 1.000 | -0.411 | 3.581 | 0.275 |
| C0 | random Gaussian | 0.763 | 0.000 | -0.126 | -2.362 | 0.374 |
| C0 | equal-norm random | 0.746 | 0.000 | -0.110 | -2.954 | 0.396 |
| C0 | shuffled center | 0.837 | 0.637 | -0.126 | -1.696 | 0.808 |
| C1 | pseudo-center | 1.000 | 1.000 | -0.401 | 3.671 | 0.259 |
| C1 | oracle-center | 1.000 | 1.000 | -0.381 | 3.678 | 0.256 |
| C1 | random Gaussian | 0.818 | 0.637 | -0.107 | -4.037 | 0.420 |
| C1 | equal-norm random | 0.818 | 0.637 | -0.107 | -4.111 | 0.420 |
| C1 | shuffled center | 0.863 | 0.707 | -0.144 | -1.500 | 0.767 |
| C2 | pseudo-center | 1.000 | 1.000 | -0.397 | 3.622 | 0.258 |
| C2 | oracle-center | 1.000 | 1.000 | -0.379 | 3.743 | 0.255 |
| C2 | random Gaussian | 0.789 | 0.637 | -0.121 | -3.975 | 0.443 |
| C2 | equal-norm random | 0.789 | 0.637 | -0.092 | -4.186 | 0.451 |
| C2 | shuffled center | 0.863 | 0.707 | -0.148 | -1.523 | 0.768 |
| C3 | pseudo-center | 1.000 | 1.000 | -0.441 | 3.539 | 0.267 |
| C3 | oracle-center | 1.000 | 1.000 | -0.422 | 3.586 | 0.262 |
| C3 | random Gaussian | 0.818 | 0.637 | -0.121 | -4.276 | 0.472 |
| C3 | equal-norm random | 0.818 | 0.637 | -0.124 | -4.264 | 0.466 |
| C3 | shuffled center | 0.883 | 0.866 | -0.165 | -1.715 | 0.777 |

Interpretation:

- Pseudo-center and oracle-center are indistinguishable for the mechanism
  decision.
- Both center conditions preserve the partition perfectly but do not show
  active tracking.
- Random and equal-norm random learn the supervised target, but do not recover
  the same route partition or positive margins.
- Label-shuffled centers show that center-like row scale is insufficient when
  row-feature matching is wrong.

### 5.2 Stage-Level Profiling Evidence

Across C0-C3 and all seeds, pseudo-center and oracle-center keep feature NMI at
1.0 at steps 5, 10, 100, and 1600. Their raw margin remains positive through
training.

Random and equal-norm random reach target accuracy 1.0 by step 10, but their
raw margins become more negative by step 1600. This separates task learning
from feature-specialized route preservation.

### 5.3 Failed Or Ambiguous Evidence

The automatic mode classifier labels center-initialized runs as
`preserved_unclassified`, not `static_margin`, because row displacement is not
tiny under the strict static threshold. This is a useful warning: the result is
not "rows never move." The stronger interpretation is "row movement is not
co-directional with center drift, while feature-specific route margins remain
positive."

Therefore the final mechanism label used in the report is
positive-margin preservation, not strict static-margin preservation.

## 6. Visualization Results

### Feature NMI Trajectory

![Feature NMI trajectory](figures/feature_nmi_trajectory.png)

Purpose:
test whether clean route partition is preserved.

Setup:
route-position audit batch, C0-C3, 8 seeds, all initialization conditions.

How to read:
higher feature NMI means stronger agreement between feature id and top-1
expert assignment.

Observed result:
pseudo-center and oracle-center remain perfect. Random and equal-norm random
are lower and seed-sensitive.

Take-home:
center initialization preserves the controlled route partition.

Remaining uncertainty:
NMI alone cannot say how preservation happens.

What this figure does not prove:
it does not prove active tracking or expert utility.

Anchor update implication:
use movement and margin metrics to classify the mechanism.

### Movement Alignment Trajectory

![Movement alignment trajectory](figures/movement_alignment_trajectory.png)

Purpose:
test active router-center tracking.

Setup:
fixed step-0 row-feature matching, then compare row displacement with matched
common-centered feature-center displacement.

How to read:
positive high values support active tracking. Negative values weaken it.

Observed result:
center-initialized rows have negative final movement alignment in every C0-C3
cell.

Take-home:
active center tracking is not the preservation mechanism in this bridge.

Remaining uncertainty:
movement alignment can be difficult to interpret when center drift includes
curved or nonlocal movement, but the sign is consistently opposite rather than
weakly positive.

What this figure does not prove:
it does not mean the router is geometrically irrelevant, because route margins
remain strongly positive.

Anchor update implication:
the physical prior should focus on stable cone margin, not row-center
co-movement.

### Route Margin Trajectory

![Route margin trajectory](figures/route_margin_trajectory.png)

Purpose:
test whether feature centers remain inside the intended router regions.

Setup:
raw hidden-state feature centers and router rows at each snapshot.

How to read:
positive raw margin means the matched expert beats all other experts at that
feature center.

Observed result:
center initialization keeps positive raw margins. Random, equal-norm random,
and shuffled centers have negative final margins.

Take-home:
the successful preservation branch is feature-specific margin preservation.

Remaining uncertainty:
the metric is center-based and does not by itself prove all within-feature
points have high margins.

What this figure does not prove:
it does not prove utility or semantic specialization.

Anchor update implication:
future preservation anchors should optimize or audit route margin directly.

### Common And Norm Guard

![Common and norm guard](figures/common_norm_guard_trajectory.png)

Purpose:
test whether the preserved partition is dominated by common projection or norm
growth.

Setup:
compute common share and norm growth at every snapshot.

How to read:
high common share means the router logit is more common-component dominated.

Observed result:
center conditions end near common share 0.26, while shuffled centers end near
0.78 and fail clean preservation.

Take-home:
successful center preservation is not primarily a common-direction effect in
this controlled bridge.

Remaining uncertainty:
real-DCLM common components may be stronger and require a separate audit.

What this figure does not prove:
it does not rule out common-component failure in real language data.

Anchor update implication:
common-centering remains a required guard, but it is not the explanation for
this successful bridge run.

### Preservation Mode By Condition

![Preservation mode by condition](figures/preservation_mode_by_condition.png)

Purpose:
summarize automatic preservation-mode labels by condition.

Setup:
mode labels are computed per cell, condition, and seed using NMI, movement
alignment, displacement, margin, and common share thresholds.

How to read:
the plot is a classifier summary, not the primary evidence.

Observed result:
center-initialized runs are consistently preserved but not classified as
active tracking. Most random, equal-norm random, and shuffled runs are not
preserved.

Take-home:
the automatic classifier agrees with the manual conclusion that center
initialization preserves the partition without active tracking.

Remaining uncertainty:
the classifier threshold for "static" is stricter than the mechanism evidence
requires.

What this figure does not prove:
it should not replace the direct NMI, movement, and margin tables.

Anchor update implication:
use the classifier as a summary only; report positive-margin preservation as
the human-read mechanism.

## 7. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| Snapshot audit | required steps and tensors represented in tables | passed | none | missing-snapshot explanation |
| Matching audit | center conditions have stable final feature NMI and no matching changes | passed | none for center conditions | expert permutation as main explanation |
| Movement audit | center final \(A_{\mathrm{move}}\) is negative | failed for active tracking | rows do not move with centers | active tracking as main mechanism |
| Margin audit | center final raw margins remain positive | passed | none | random rediscovery and common-only explanations |
| Common/norm audit | center common share low, shuffled high | passed | none | common / norm drift as main successful-preservation explanation |
| Guard audit | all conditions learn target, but only center preserves feature routing | passed | none | target accuracy as a proxy for specialization |

Falsified physical prior:
the stronger prior that successful preservation requires row-center
co-movement is weakened in this controlled setting.

Falsified mathematical model:
the active-tracking model \(A_{\mathrm{move}} \gg 0\) is not supported.

Falsified operationalization / proxy:
none. Route-position pseudo centers remain a valid controlled proxy.

Falsified implementation:
none found. Smoke, timing, full shard aggregation, table creation, and figure
rendering completed.

Falsified metric:
none, but final NMI is confirmed as insufficient for mechanism classification.

Remaining rival explanations:
within-feature spread and per-example margins may still matter. The current
run uses feature-center margins, so it does not fully audit tail examples
inside each feature.

## 8. Full Experiment Record

Actual run name:
`a06_17_02_router_center_tracking_full_20260626_024804`.

Result directory in code workspace:
`active/synthetic_data_understanding/results/a06_17_02_router_center_tracking_preservation/a06_17_02_router_center_tracking_full_20260626_024804`.

Figure directory in code workspace:
`active/synthetic_data_understanding/figures/a06_17_02_router_center_tracking_preservation/a06_17_02_router_center_tracking_full_20260626_024804`.

Shard logs:

- `logs/local/a06_17_02_router_center_tracking_full_20260626_024804_shard0.log`;
- `logs/local/a06_17_02_router_center_tracking_full_20260626_024804_shard1.log`;
- `logs/local/a06_17_02_router_center_tracking_full_20260626_024804_aggregate.log`.

Repro command:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
export ATTENTION_SEARCH_EXPERIMENTS_ROOT=/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
export PYTHONUNBUFFERED=1
export A061702_TORCH_THREADS=1
export A061702_TORCH_INTEROP_THREADS=1
RUN_NAME=a06_17_02_router_center_tracking_full_20260626_024804
CUDA_VISIBLE_DEVICES=0 python scripts/run_a06_17_02_router_center_tracking_preservation.py \
  --config configs/a06_17_02_router_center_tracking_preservation.json \
  --run-name "$RUN_NAME" --run-stage full --shard-index 0 --num-shards 2 --device cuda &
CUDA_VISIBLE_DEVICES=1 python scripts/run_a06_17_02_router_center_tracking_preservation.py \
  --config configs/a06_17_02_router_center_tracking_preservation.json \
  --run-name "$RUN_NAME" --run-stage full --shard-index 1 --num-shards 2 --device cuda &
wait
python scripts/run_a06_17_02_router_center_tracking_preservation.py \
  --config configs/a06_17_02_router_center_tracking_preservation.json \
  --run-name "$RUN_NAME" --run-stage full --num-shards 2 --aggregate-only --device cpu
```

## 9. Interpretation

The important update is that preservation does not require the router to chase
the moving feature centers. Once a center-initialized router gives each feature
a large enough positive margin, training can move both representations and
router rows while the feature centers remain inside the same router regions.

This explains why pseudo-center and oracle-center behave the same: the proxy
does not need semantic labels once it recovers the correct route-position
feature centers.

It also explains why random initialization can learn the target but fail the
specialization metric: the supervised objective can be solved without keeping
one clean expert region per feature.

## 10. Claim Boundary

Can claim:
in the controlled corrected A06 bridge, feature-center and pseudo-center router
initialization preserve feature routing by maintaining feature-specific
positive route margins, not by active router-center tracking.

Cannot claim:
real-DCLM behavior, semantic features, utility, RoPE behavior, or that this
margin construction is sufficient under ordinary language-model training.

## 11. Next Decision

Next anchor should test margin construction without labels. Specifically:
given label-free route-relevant states, can we initialize router rows so that
each discovered proxy group has a positive raw routing margin that remains
positive during early training?

This is more direct than asking whether rows track centers.

## 12. Links And Artifact Map

anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

protocol:
`protocol.md`

summary:
`summary.md`

code workspace:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`

runner:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_17_02_router_center_tracking_preservation.py`

config:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_17_02_router_center_tracking_preservation.json`

key tables:

- `tables/router_center_metrics_by_step.csv`;
- `tables/router_center_metric_aggregate.csv`;
- `tables/final_step_decision_table.csv`;
- `tables/trajectory_decision_table.csv`;
- `tables/preservation_mode_by_seed.csv`;
- `tables/preservation_mode_aggregate.csv`;
- `tables/discovery_summary.csv`.

figures:

- `figures/feature_nmi_trajectory.png`;
- `figures/movement_alignment_trajectory.png`;
- `figures/route_margin_trajectory.png`;
- `figures/common_norm_guard_trajectory.png`;
- `figures/router_norm_growth_trajectory.png`;
- `figures/row_center_dot_product_trajectory.png`;
- `figures/preservation_mode_by_condition.png`.

logs / checkpoints:
raw logs remain in the code workspace under `logs/local/`. Checkpoints and raw
run outputs were not copied into this research artifact directory.

job id:
local two-GPU run, no cluster job id.
