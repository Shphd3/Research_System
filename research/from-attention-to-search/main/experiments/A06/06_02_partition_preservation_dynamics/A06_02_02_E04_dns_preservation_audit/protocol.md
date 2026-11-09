# Protocol: A06_02_02_E04 DNS Routing Preservation Audit

## 0. Approval Snapshot

Approval status: user requested brief anchor card, protocol, and execution.

Purpose: Test whether DNS-style common-subtracted routing and simple router-side interventions preserve feature margins under long full-LM training.

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Anchor decision question: Does DNS-style routing or router-side preservation prevent long full-LM training from eroding feature margins?

Anchor physical prior tested: full-LM training may move router behavior toward common hidden components; removing or constraining that component may preserve feature margins.

Anchor core model term tested: margin trajectory under DNS router input and router-row preservation interventions.

Anchor falsifier: DNS and preservation variants fail to improve margin p05 over raw embedding-gradient top1 without target-accuracy collapse.

Experiment role: preservation mechanism audit.

Primary metric from anchor: margin p05 through 2000 full-LM steps.

Claim boundary from anchor: synthetic uniform no-position bridge only.

Minimal setup: same one-layer causal Transformer, weighted top-1 MoE, no position embeddings, four uniformly sampled features, repeated feature slots, and feature-specific target token as A06_01_05_E04.

Basic configuration: full-sequence LM loss only, warmup 40, seeds 0--7, slot lengths 1/2/4/8, checkpoints 0/160/500/1000/2000.

Conditions to run:
raw oracle, DNS oracle, raw route center, DNS route center, raw embedding-gradient top1, embedding-gradient top1 + DNS, denoised-gradient top1 + DNS, denoised-gradient top1 + DNS + row projection, denoised-gradient top1 + DNS + router LR 0.1, denoised-gradient top1 + DNS + freeze router for 160 steps.

Pass: a DNS or preservation condition improves long-run margin p05 over raw embedding-gradient top1 while target accuracy remains close to the baseline.

Fail: all DNS and preservation variants remain negative-margin or improve margin only by damaging target accuracy.

Insufficient: checkpoint 2000 is missing, seed/slot coverage is incomplete, or clean controls fail at initialization.

Cannot claim: real-DCLM transfer, semantic experts, rare-feature routing, expert utility, or final method optimality.

Approval decision: implement a dedicated runner, smoke locally, then submit a four-GPU full run.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| DNS routing | Route on a common-subtracted hidden state | router input \(h-c\) | hidden vector | Tests whether common components drive margin erosion | True common operator |
| Common direction | Fixed common hidden component | all-position calibration hidden mean at warmup 40 | vector | Operational DNS component | Causal commonness |
| Denoised gradient selector | Gradient selector normalized by position-level score statistics | \(z_{i,p}=(E_{i,p}-\mu_p)/(\sigma_p+\epsilon)\) | z-score | Removes position-wide LM-gradient bias | Feature labels |
| Row projection | Remove common direction from router rows after updates | \(w\leftarrow w-(w^\top \hat c)\hat c\) | row update | Tests row drift into common direction | Optimal constraint |
| Router LR 0.1 | Train router rows with smaller learning rate | router param group lr = 0.1 base lr | learning-rate scale | Tests router drift sensitivity | Cause of drift |
| Early freeze | Keep router rows fixed early after reinit | zero router gradients for first 160 steps | steps | Tests whether early drift breaks margin | Long-run preservation |

## 2. Conditions

| Condition | Router input | Initial rows | Preservation intervention | Role |
| --- | --- | --- | --- | --- |
| `raw_oracle` | \(h\) | oracle feature centers | none | upper bound baseline |
| `dns_oracle` | \(h-c\) | oracle centers in DNS coordinates | none | clean DNS control |
| `raw_route_center` | \(h\) | route-position k-means | none | route-state baseline |
| `dns_route_center` | \(h-c\) | route centers in DNS coordinates | none | route-state DNS control |
| `raw_grad_top1` | \(h\) | raw embedding-gradient top1 | none | A06_01_05_E04 baseline |
| `dns_grad_top1` | \(h-c\) | raw embedding-gradient top1 | none | embedding-gradient top1 + DNS |
| `dns_denoised_grad_top1` | \(h-c\) | position-normalized gradient top1 | none | denoised selector + DNS |
| `dns_denoised_grad_top1_rowproj` | \(h-c\) | position-normalized gradient top1 | row projection | row-common constraint |
| `dns_denoised_grad_top1_lr01` | \(h-c\) | position-normalized gradient top1 | router LR scale 0.1 | low-router-LR preservation |
| `dns_denoised_grad_top1_freeze160` | \(h-c\) | position-normalized gradient top1 | freeze router 160 steps | early-freeze preservation |

## 3. Metrics

Primary: margin p05 at checkpoints 160/500/1000/2000.

Secondary: feature NMI, positive margin fraction, sign flip rate, target accuracy, loss, max load, effective experts, slot-start NMI, router-row common cosine, route-hidden common projection, and selected route/slot fractions.

## 4. Execution

Smoke command:

```bash
CUDA_VISIBLE_DEVICES=0 python \
  Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E04_dns_preservation_audit/scripts/run_a06_29_dns_routing_preservation_audit.py \
  --run-stage smoke \
  --run-name a06_29_dns_smoke_local \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E04_dns_preservation_audit
```

Four-GPU full command:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 torchrun --standalone --nproc_per_node=4 \
  Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E04_dns_preservation_audit/scripts/run_a06_29_dns_routing_preservation_audit.py \
  --run-stage full \
  --run-name a06_29_dns_routing_preservation_full_4gpu_20260706 \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E04_dns_preservation_audit
```

## 5. Expected Artifacts

- `summary.json`
- `tables/training_trajectory.csv`
- `tables/condition_trajectory_aggregate.csv`
- `tables/condition_aggregate_final.csv`
- `figures/a06_29_dns_margin_trajectory.png`
- `figures/a06_29_dns_final_step2000.png`
- `summary.md`
- `detailed.md`
