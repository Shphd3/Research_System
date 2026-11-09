# Detailed: A06_02_01_E01 Training Basin Preservation

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol:
`protocol.md`

Summary:
`summary.md`

## Decision

A06_02_01_E01 supports the training-basin hypothesis in the synthetic uniform setting. Both oracle feature-centroid initialization and A06_01_03_E02 label-free pseudo-center initialization preserve perfect held-out feature routing while learning the target.

The decision is based on `feature_NMI(t)`, not on accuracy alone. Accuracy reaches `1.0` for all conditions, including random baselines, so accuracy cannot decide whether the route partition is feature-specialized.

## Data Construction

The run uses the synthetic A06 four-feature task:

- four pair features, strictly uniform;
- each example contains one repeated `SLOT_s` span followed by `TARGET_s`;
- `slot_token_len=4`;
- route and metric readout use the last slot token, `pair_start + 3`;
- background tokens are sampled independently of pair id;
- four experts match the four pair features.

The training objective is route-position target cross entropy: the model predicts `TARGET_s` from the last slot position. This objective is used because random background tokens are intentionally unlearnable and would make full-sequence next-token loss a mismatched primary metric.

## Model, Training, And Conditions

Model:

- top-1 dot-product MoE router;
- `d_model=128`;
- `n_heads=4`;
- feed-forward dimension `256`;
- four experts;
- depths `num_layers in {1,2,4}`.

Training:

- seeds `20260521..20260528`;
- steps `1600`;
- learning rate `0.0008`;
- batch size `512`;
- checkpoints `0, 100, 400, 800, 1600`.

Conditions:

| Condition | Role |
| --- | --- |
| `random_gaussian_init` | random baseline |
| `equal_norm_random_init` | row-norm guard |
| `oracle_feature_centroid_init` | positive control for feature-aligned basin |
| `label_shuffled_centroid_guard` | label artifact guard |
| `best_A06_08_pseudo_center_init` | label-free bridge from A06_01_03_E02 |

Dependency audit:
A06_01_03_E02 passed and selected `route_kmeans_residual_K4` for the pseudo-center condition.

## Metrics And Gates

Primary metric:
held-out `feature_NMI(t) = NMI(pair_id, routed_expert)`.

Support gate:

- final `feature_NMI >= 0.80`;
- NMI drop no more than `0.15`;
- final target accuracy at least `0.95`.

Failure gate:

- step-0 `feature_NMI >= 0.95`;
- final `feature_NMI < 0.50`, or drop greater than `0.30`;
- acceptable final target accuracy.

Secondary metrics:
target accuracy, load imbalance \(L\), margin p05, route-change rate, and route heatmaps.

## Main Result

Final aggregate across all depths and seeds:

| Condition | Step-0 NMI | Final NMI | NMI drop | Target acc. | Load \(L\) | Supported |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `best_A06_08_pseudo_center_init` | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 24/24 |
| `oracle_feature_centroid_init` | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 24/24 |
| `random_gaussian_init` | 0.2399 | 0.8100 | -0.5700 | 1.0000 | 1.1277 | 0/24 |
| `equal_norm_random_init` | 0.2394 | 0.8027 | -0.5633 | 1.0000 | 1.1667 | 0/24 |
| `label_shuffled_centroid_guard` | 0.4969 | 0.8409 | -0.3440 | 1.0000 | 1.0000 | 0/24 |

By depth, both oracle and pseudo init have final `feature_NMI=1.0`, NMI drop `0.0`, target accuracy `1.0`, and load \(L=0.0\) for every depth.

Random baselines partially improve NMI during training, but they do not produce the same clean basin. Their minimum final NMI is `0.6369`, and their final load imbalance remains nonzero.

## Visualization Results

### NMI Trajectory

![Feature NMI trajectory](figures/nmi_trajectory.png)

Purpose:
test whether a feature-aligned route partition is preserved during training.

Setup:
mean held-out `feature_NMI` over 8 seeds, separately for depths `{1,2,4}` and initialization conditions.

How to read:
a stable specialization basin should remain high from step 0 to step 1600. A collapse would show high step-0 NMI followed by low final NMI.

Observed result:
oracle and A06_01_03_E02 pseudo init remain at `feature_NMI=1.0` throughout. Random and guard conditions improve after training but do not become clean supported partitions.

Take-home:
the feature-aligned initialization is preserved in this synthetic setting.

Remaining uncertainty:
this does not test full next-token language modeling, nonuniform feature distributions, or real hidden-state feature definitions.

### Accuracy Trajectory

![Target accuracy trajectory](figures/accuracy_trajectory.png)

Purpose:
check whether the high-NMI conditions still learn the supervised target.

Setup:
held-out target accuracy at route-position checkpoints.

How to read:
high NMI without task learning would not support a useful training basin.

Observed result:
all conditions reach target accuracy `1.0` quickly. This includes random baselines.

Take-home:
accuracy is a constraint, not the deciding metric. It cannot distinguish clean routing from weaker routing.

Remaining uncertainty:
the target objective is intentionally simple and does not represent full real-text next-token training.

### Route Heatmaps

![Route heatmaps](figures/route_heatmaps_step0_final.png)

Purpose:
show whether pair features map one-to-one to experts.

Setup:
route assignments summarized by feature pair and expert at step 0 and final checkpoint.

How to read:
a clean specialization partition should show one dominant expert per feature and no feature merge.

Observed result:
oracle and A06_01_03_E02 pseudo init keep clean one-to-one routing. Random and guard conditions are less reliable and retain nonzero load imbalance.

Take-home:
the supported conditions preserve the intended feature-to-expert partition.

Remaining uncertainty:
heatmaps are synthetic feature evidence only; they do not define real semantic experts.

## Validity Audits

Dependency:
`tables/dependency_audit.csv` confirms that the A06_01_03_E02 source table exists, the dependency passed, and the selected pseudo method is `route_kmeans_residual_K4`.

Initialization:
`tables/initialization_audit.csv` records condition, seed, depth, alpha, pseudo method, and whether pair labels were used. The pseudo condition uses A06_01_03_E02 discovered centers, not oracle labels in A06_02_01_E01.

Checkpoint completeness:
`tables/checkpoint_audit.csv` has 600 evaluated rows: 5 conditions times 8 seeds times 3 depths times 5 checkpoints.

Run completeness:
`tables/final_summary.csv` has 120 final cells: 5 conditions times 8 seeds times 3 depths.

## Failed Or Partial Runs

An earlier ACP job, `pt-t0ooxyp4`, was stopped after a submit-script heredoc bug left `${RUN_NAME}` unresolved inside the runtime command. It produced no decision evidence.

The corrected ACP job `pt-epdfv6pd` completed successfully and is the only full-run evidence used here.

## Artifact Map

Code workspace:
`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`

Runner:
`scripts/run_a06_09_training_basin_preservation.py`

Config:
`configs/a06_09_training_basin_preservation.json`

Submit script:
`scripts/submit_a06_09_training_basin_preservation_4gpu_acp.sh`

ACP job:
`pt-epdfv6pd`

Run name:
`a06_09_training_basin_full_20260622_2`

Raw result directory:
`results/a06_09_training_basin_preservation/a06_09_training_basin_full_20260622_2`

Raw figure directory:
`figures/a06_09_training_basin_preservation/a06_09_training_basin_full_20260622_2`

Project-local tables:
`tables/`

Project-local figures:
`figures/`

Key tables:

- `tables/dependency_audit.csv`
- `tables/final_summary.csv`
- `tables/final_aggregate.csv`
- `tables/training_trajectory.csv`
- `tables/trajectory_aggregate.csv`
- `tables/route_heatmap.csv`
- `tables/initialization_audit.csv`
- `tables/checkpoint_audit.csv`

Key figures:

- `figures/nmi_trajectory.png`
- `figures/accuracy_trajectory.png`
- `figures/route_heatmaps_step0_final.png`

Four-GPU execution command:

```bash
bash scripts/submit_a06_09_training_basin_preservation_4gpu_acp.sh
```

Shard command template:

```bash
CUDA_VISIBLE_DEVICES=<gpu_id> python scripts/run_a06_09_training_basin_preservation.py \
  --config configs/a06_09_training_basin_preservation.json \
  --run-name a06_09_training_basin_full_20260622_2 \
  --run-stage full \
  --seeds 20260521,20260522,20260523,20260524,20260525,20260526,20260527,20260528 \
  --num-layers 1,2,4 \
  --conditions random_gaussian_init,equal_norm_random_init,oracle_feature_centroid_init,label_shuffled_centroid_guard,best_A06_08_pseudo_center_init \
  --a06-08-summary results/a06_08_label_free_feature_discovery_initialization/a06_08_discovery_full_20260622_1/tables/discovery_summary.csv \
  --num-shards 4 \
  --shard-index <0..3> \
  --device cuda
```

Aggregation command:

```bash
python scripts/run_a06_09_training_basin_preservation.py \
  --config configs/a06_09_training_basin_preservation.json \
  --run-name a06_09_training_basin_full_20260622_2 \
  --run-stage full \
  --seeds 20260521,20260522,20260523,20260524,20260525,20260526,20260527,20260528 \
  --num-layers 1,2,4 \
  --conditions random_gaussian_init,equal_norm_random_init,oracle_feature_centroid_init,label_shuffled_centroid_guard,best_A06_08_pseudo_center_init \
  --a06-08-summary results/a06_08_label_free_feature_discovery_initialization/a06_08_discovery_full_20260622_1/tables/discovery_summary.csv \
  --num-shards 4 \
  --aggregate-only \
  --device cpu
```

## Interpretation

The experiment separates three claims:

1. Task learning:
all conditions learn the synthetic target.

2. Clean feature routing:
only oracle and A06_01_03_E02 pseudo init give perfect final feature routing with balanced load.

3. Label-free bridge:
A06_01_03_E02 k-means residual centers are sufficient to initialize the same basin as oracle centers in this controlled setting.

The result supports continuing the initialization route. It weakens the need to immediately move to anti-lockin for the current synthetic setting, because the aligned route partition did not collapse.

## Claim Boundary

Can claim:
feature-aligned initialization alone preserves specialization through route-position target training in the synthetic uniform `slot_token_len=4` setting. A06_01_03_E02 `route_kmeans_residual_K4` pseudo-centers enter the same preserved basin as oracle centers here.

Cannot claim:
real DCLM transfer, full next-token language-model training stability, semantic feature discovery, expert usefulness, top-k behavior, deployable routing method, or that anti-lockin is unnecessary in harder settings.

## Next Decision

Continue along initialization-based feature discovery. The next test should weaken one controlled assumption at a time: noisier feature proxies, nonuniform or mixed features, more realistic objectives, or real-DCLM proxy metrics. Anti-lockin should become the main branch only when a good initial partition collapses under one of those harder settings.
