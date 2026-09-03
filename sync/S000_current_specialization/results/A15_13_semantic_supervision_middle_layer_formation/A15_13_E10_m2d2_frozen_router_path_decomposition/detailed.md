# Detailed Record: A15_13_E10 Frozen Router Forward-Path Decomposition

## Provenance

- ACP job: `pt-uxy9mnud`
- Resource: one reserved `n6ls.iu.i40.4` worker with four H100 GPUs
- Run root: `/data/250010109/MoE_Router/experiments/20260902_a15_13_e10_m2d2_frozen_router_path_decomposition/runs/full-20260902T174226Z`
- Scientific completion: all `232/232` registered evaluations exist; every required array is finite.
- The enclosing shell job later failed after E10 because its next orchestration script was edited while running. That shell failure occurred after E10 analysis, figures, and completion audit and does not affect E10 eligibility.
- Aggregate SHA-256: `3de61ca71637e4a51cb04d83da8d227b7301d3dc3333ee472912077cc4863c58`
- Completion-audit SHA-256: `7afcc320dc5f85ce58ec4179c7be372027f367b74dfd34111663d0ddec7e8edc`

## What Actually Ran

This was an evaluation-only factorial audit with zero optimizer updates. Qwen3-0.6B-Base, block-14 LoRA experts, parent and child Routers, language head, data order, target-token mask, and checkpoints were frozen.

- Hierarchy: three checkpoint families (`LEARNED_TASK_ONLY`, `LEARNED_SEMANTIC`, `LEARNED_SHUFFLED`) x two seeds x sixteen independently crossed forward paths. The four factors were coarse index, coarse coefficient, fine index, and fine coefficient.
- Flat: two checkpoint families (`FLAT_TASK_R24`, `FLAT_GOLD9_R24`) x two seeds x four index/coefficient paths.
- Registered hierarchy and flat cells also received active-expert deletion and cyclic wrong-expert substitutions.
- Confirmation data: 512 windows per each of nine M2D2 fine domains; 192 target positions per 256-token window; equal-domain aggregation.

## Exact Central Results

All effects are Shapley NLL recovery in nats per target token. Positive is better. Intervals are 2,000 paired bootstrap replicates, resampling windows within fine domain.

| Condition | Factor | Mean | Paired 95% interval |
| --- | --- | ---: | ---: |
| Semantic hierarchy | coarse index | `-0.0006749` | `[-0.0007598,-0.0005933]` |
| Semantic hierarchy | coarse coefficient | `-0.0013030` | `[-0.0013751,-0.0012325]` |
| Semantic hierarchy | fine index | `-0.0003833` | `[-0.0004269,-0.0003396]` |
| Semantic hierarchy | fine coefficient | `+0.0003068` | `[+0.0002646,+0.0003498]` |
| Semantic hierarchy | total repair | `-0.0019518` | `[-0.0020739,-0.0018276]` |
| Flat task-only | index | `-0.0724623` | `[-0.0738829,-0.0710618]` |
| Flat task-only | coefficient | `+0.0011613` | `[+0.0010954,+0.0012276]` |
| Flat task-only | total repair | `-0.0713010` | `[-0.0727396,-0.0698998]` |
| Flat gold-nine | index | `-0.0339604` | `[-0.0349356,-0.0330033]` |
| Flat gold-nine | coefficient | `+0.0130646` | `[+0.0125922,+0.0135384]` |
| Flat gold-nine | total repair | `-0.0208958` | `[-0.0215798,-0.0202177]` |

Learned-semantic child interventions remained positive but small on the original path: active-child deletion cost `+0.0012913` NLL, while the two cyclic substitutions cost `+0.0006686` and `+0.0008054`. This supports non-zero child expert function but does not overturn the negative repair result.

## Eligibility And Deviation Audit

- Required evaluation count: pass (`232`).
- Aggregate exists: pass.
- Finite-array guard: pass.
- Both seeds present: pass.
- Scientific logic changed after results: no.
- Resource deviation: the frozen body retained an obsolete eight-RTX5090 sentence, but Amendment C002 and the actual receipt both specify four reserved H100 GPUs. This documentation inconsistency does not change data, checkpoints, cells, aggregation, or result eligibility.

## Artifact Map

- Aggregate: `/data/250010109/MoE_Router/experiments/20260902_a15_13_e10_m2d2_frozen_router_path_decomposition/runs/full-20260902T174226Z/analysis/aggregate.json`
- Completion audit: `/data/250010109/MoE_Router/experiments/20260902_a15_13_e10_m2d2_frozen_router_path_decomposition/runs/full-20260902T174226Z/completion_audit.json`
- Per-cell arrays: `.../evaluations/*.npz`
- Curated figures: [hierarchical decomposition](figures/hierarchical_path_contributions.png), [flat decomposition](figures/flat_path_decomposition.png)

## Bounded Interpretation

The data falsify both simple explanations: “only learned probabilities attenuate useful experts” and “the Router merely chooses the wrong semantic expert.” The strongest remaining rival is training responsibility: experts and Routers were optimized jointly under the learned soft path, so changing the path after training creates an out-of-training-distribution composition. Only a retraining control can test whether hard or loss-free routing avoids that co-adaptation.
