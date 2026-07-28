# Protocol: A06_01_05_E04 Full-Sequence LM Gradient Selector Guard

## 0. Approval Snapshot

Approval status: user requested immediate execution and remote four-GPU full
run.

Purpose: Test whether the A06_01_05_E03 embedding-gradient selector still works when
gradients are computed from full-sequence next-token LM loss instead of
route-position-only loss.

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/subanchors/06_01_05_warmup_spectral_gradient_selector_audit_anchor.md`

Anchor decision question: Can embedding-gradient selection identify
feature-relevant states under full-sequence LM loss?

Anchor physical prior tested: feature tokens that causally affect sequence
prediction should receive structured embedding-gradient energy, but random
neutral-token prediction may add noise.

Anchor core model term tested: feature-center margin induced by selected
hidden-state k-means centers.

Anchor falsifier: full-LM embedding-gradient top-k fails to beat all-position
clustering or fails the positive margin guard.

Experiment role: objective-locality guard for the A06_01_05_E03 method candidate.

Primary metric from anchor: immediate feature NMI after router reinitialization.

Claim boundary from anchor: synthetic uniform no-position bridge only.

Minimal setup: one-layer causal Transformer, one weighted top-1 MoE layer, no
position embeddings, four uniformly sampled features, repeated feature slots,
neutral background, feature-specific target token, and balanced evaluation.

Basic configuration: seeds 0--7, slot lengths 1/2/4/8, warmup steps 0/10/40,
post-reinit train checkpoints 0/10/40/80/160.

Conditions to run: `route_ce` and `full_lm` loss modes; no-reinit,
all-position, route-position, oracle, post-hidden gradient top/direction, and
embedding-gradient top/direction with top-k in 1/4/8.

Pass: a full-LM embedding-gradient top-k condition beats all-position,
approaches route-position control, has positive margin p05, and keeps
slot-start NMI low.

Fail: full-LM top-k conditions do not beat all-position or their gains have
negative margin.

Insufficient: route-position/oracle controls fail, target learning fails, or
full seed/slot coverage is incomplete.

Cannot claim: real-DCLM transfer, semantic experts, common/rare routing,
expert utility, or pure unsupervised discovery.

Approval decision: execute smoke locally, then submit four-GPU remote full run.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Route-position loss | Loss only at supervised route position | CE on final feature-slot token prediction | $\mathcal L^{route}$ | Positive control from A06_01_05_E03 | Full LM validity |
| Full-sequence LM loss | Standard next-token loss over all positions | CE on every next-token prediction | $\mathcal L^{full}$ | Removes route-only locality bias | Real language semantics |
| Embedding-gradient top-k | Select k positions per sample by embedding gradient energy | top-k of $\|\nabla_e\mathcal L\|^2$ | token positions | Tests feature-state selection | Feature labels |
| Feature NMI | Agreement between feature id and routed expert | NMI(feature, route) | 0--1 | Primary separation metric | Utility |
| Margin p05 | Lower-tail matched route gap | 5th percentile of target expert minus competitor score | logit gap | Preservation guard | Optimality |

## 2. Conditions

| Loss mode | Method family | Role |
| --- | --- | --- |
| `route_ce` | embedding-gradient top/direction | A06_01_05_E03 positive control |
| `full_lm` | embedding-gradient top/direction | main validity guard |
| both | all-position centered | failure baseline |
| both | route-position centered | positive control |
| both | oracle centered | upper bound |

Top-k values: `1,4,8`.

## 3. Metrics

Primary: immediate feature NMI.

Guards: margin p05, matched preserve fraction, final feature NMI, sign-flip
rate, max load, slot-start NMI, selected route/slot/target fractions, and route
target accuracy.

## 4. Execution

Smoke command:

```bash
CUDA_VISIBLE_DEVICES=0 python \
  Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E04_full_lm_gradient_guard/scripts/run_a06_28_full_sequence_lm_gradient_selector_guard.py \
  --run-stage smoke \
  --run-name a06_28_full_lm_smoke_local \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E04_full_lm_gradient_guard
```

Four-GPU full command:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 torchrun --standalone --nproc_per_node=4 \
  Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E04_full_lm_gradient_guard/scripts/run_a06_28_full_sequence_lm_gradient_selector_guard.py \
  --run-stage full \
  --run-name a06_28_full_lm_guard_full_4gpu_20260706 \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E04_full_lm_gradient_guard
```

## 5. Expected Artifacts

- `summary.json`
- `tables/training_trajectory.csv`
- `tables/condition_aggregate_reinit.csv`
- `tables/condition_aggregate_final.csv`
- `tables/selector_diagnostics_aggregate.csv`
- `figures/*full_lm*`
- `summary.md` and `detailed.md` after completion
