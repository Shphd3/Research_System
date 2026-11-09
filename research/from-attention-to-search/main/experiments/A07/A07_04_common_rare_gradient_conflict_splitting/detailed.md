# Detailed: A07_04 Common / Rare Gradient Conflict Splitting

## Conclusion

The run gives insufficient evidence for the A07_04 claim. It validates the measurement pipeline and shows weak partial movement versus random top-1, but it does not show a useful MoE conflict-splitting result.

## Protocol Compliance Audit

Approved protocol: `protocol.md`.

Actual run: `a07_04_grad_conflict_full_20260624_1`.

Conditions matched protocol: `dense_shared`, `random_top1_moe`, `centered_unsup_split_moe`, `oracle_split_moe`.

Seeds matched protocol: `20260624-20260631`.

Primary metric exists: yes, `tables/common_rare_gradient_conflict.csv`.

Rare-loss guard exists: yes, `tables/common_rare_loss_guard.csv`.

Route/load guards exist: yes, `tables/route_distribution.csv` and `tables/load_guard.csv`.

Central figures exist: yes, `figures/conflict_vs_rare_loss.png` and `figures/weighted_conflict_by_condition.png`.

Deviation: the first CPU full attempt was interrupted for slowness before writing full shard outputs. The completed full run used the same config on local GPU with 4 logical shards.

## Setup

Runner: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a07_04_common_rare_gradient_conflict_splitting.py`

Config: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a07_04_common_rare_gradient_conflict_splitting.json`

Raw result dir: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a07_04_common_rare_gradient_conflict_splitting/a07_04_grad_conflict_full_20260624_1`

ACP dry-run log: `logs/acp/a07_04_common_rare_gradient_conflict_full_20260624_1_submit_*.log`

External job id: none.

## Data And Models

Data: synthetic binary common/rare task. Train split is imbalanced with many common samples and fewer rare samples; evaluation is balanced.

Models:

| Condition | Meaning |
| --- | --- |
| `dense_shared` | one shared logistic classifier |
| `random_top1_moe` | trainable top-1 MoE with four experts |
| `centered_unsup_split_moe` | label-free centered k-means gate with four experts |
| `oracle_split_moe` | upper bound that routes common and rare to separate experts |

No expert utility, ablation damage, or rare-loss value is hand-coded.

## Evidence Ledger

Primary conflict table:

| Condition | Expert overlap | Weighted conflict | Delta vs random |
| --- | ---: | ---: | ---: |
| dense_shared | `1.0000` | `0.9982` | `-0.7341` |
| random_top1_moe | `0.2661` | `0.2641` | `0.0000` |
| centered_unsup_split_moe | `0.2384` | `0.2370` | `0.0271` |
| oracle_split_moe | `0.0000` | `0.0000` | `0.2641` |

Loss guard:

| Condition | Common loss | Rare loss | Common acc | Rare acc |
| --- | ---: | ---: | ---: | ---: |
| dense_shared | `0.1108` | `1.7321` | `0.9878` | `0.1301` |
| random_top1_moe | `0.1157` | `1.8827` | `0.9799` | `0.1449` |
| centered_unsup_split_moe | `0.1112` | `1.8195` | `0.9850` | `0.1373` |
| oracle_split_moe | `0.0003` | `0.0004` | `1.0000` | `1.0000` |

Load guard:

| Condition | Max load | Active experts | Load entropy |
| --- | ---: | ---: | ---: |
| random_top1_moe | `0.3630` | `3.8750` | `0.9318` |
| centered_unsup_split_moe | `0.3239` | `4.0000` | `0.9822` |
| oracle_split_moe | `0.5000` | `2.0000` | `0.5000` |

Gradient audit:

Dense has strong negative common/rare gradient cosine in the shared expert: `-0.9982`.

Random and centered MoE experts also show negative cosines around `-0.86` to `-0.99` where both features share an expert.

Centered routing reduces overlap from `0.2661` to `0.2384`, but this is a small change.

## Visualization Results

### Conflict Versus Rare Loss

![Conflict versus rare loss](figures/conflict_vs_rare_loss.png)

Purpose: test whether measured conflict reduction aligns with rare-loss improvement.

Setup: full aggregate across 8 seeds.

How to read: lower-left is better.

Observed result: centered split is slightly lower conflict and lower rare loss than random top-1. Dense is a counterexample to a simple monotonic story because it has high conflict but lower rare loss than both MoE variants.

Take-home: mechanism measurement works, but the candidate does not close the claim.

Remaining uncertainty: the proxy may make rare learning too hard for non-oracle MoE, or the centered gate may be too weak.

### Weighted Conflict By Condition

![Weighted conflict by condition](figures/weighted_conflict_by_condition.png)

Purpose: compare conflict directly across conditions.

Setup: same full aggregate.

How to read: lower conflict means less route-weighted negative gradient sharing.

Observed result: oracle eliminates conflict; centered split modestly reduces conflict versus random top-1.

Take-home: routing can reduce the measured conflict term, but the reduction is not yet enough to support expert specialization.

Remaining uncertainty: route separation and rare-feature learning need stronger coupling.

## Failure Interpretation

The physical prior is present: common/rare gradients conflict strongly.

The candidate mechanism is weak: centered split reduces conflict by only `0.0271`, with standard deviation `0.0398`.

The rare-loss guard is weak: rare loss improves by `0.0632`, with standard deviation `0.0617`, and rare accuracy remains low.

The dense baseline is a serious boundary: dense rare loss is lower than centered MoE rare loss, so the result does not show MoE functional value beyond shared learning.

The oracle upper bound proves the rare feature is learnable when the split is correct.

## Artifact Map

Curated tables:

- `tables/common_rare_gradient_conflict.csv`
- `tables/common_rare_loss_guard.csv`
- `tables/gradient_cosine_by_expert.csv`
- `tables/load_guard.csv`
- `tables/route_distribution.csv`

Curated figures:

- `figures/conflict_vs_rare_loss.png`
- `figures/weighted_conflict_by_condition.png`

Repro command:

```bash
python scripts/run_a07_04_common_rare_gradient_conflict_splitting.py \
  --config configs/a07_04_common_rare_gradient_conflict_splitting.json \
  --run-name a07_04_grad_conflict_full_20260624_1 \
  --run-stage full \
  --seeds 20260624,20260625,20260626,20260627,20260628,20260629,20260630,20260631 \
  --aggregate-only \
  --device cpu
```

Four-card ACP dry-run:

```bash
scripts/submit_a07_04_common_rare_gradient_conflict_splitting_4gpu_acp.sh
```

## Claim Boundary

Can claim: A07_04 has a working neural gradient-conflict measurement protocol; centered unsupervised routing weakly reduces conflict versus random top-1.

Cannot claim: MoE routing solves rare interference, beats dense shared learning, or provides real expert specialization evidence.

## Next Decision

Revise the proxy or router before making A07_04 a mainline support result.
