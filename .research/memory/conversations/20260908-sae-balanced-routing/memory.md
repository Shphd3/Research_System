# Conversation Memory: SAE/GMM online routing and post-training analysis

## Objective

Execute the complete S0--S6 post-training track on the lower, linearly decayed A6R1 checkpoints and return auditable results. First finish all missing smoke coverage, then make S6 constructible, then submit the unified track on one reserved four-H100 node. This file is non-canonical working context; the Focus, Anchor, Protocols, Summary, and Detailed records own scientific state and approval.

## Current State

- A6 constant-`0.1` training completed 12/12 trajectories and full internal evaluation. Every regularized-minus-task-only delta was positive; the best A6 arm was SAE-B, still worse by `+0.005936` nats/token on average. Its Summary remains `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.
- A6R1 changed only the structural-weight schedule to `0.01` at update 1, linearly decaying to `0.001` at update 512. All four arms x seeds 17/29/43 completed 512 updates and full internal evaluation. Against task-only, SAE-A and GMM-A were worse in every seed; SAE-B and GMM-B improved the mean but reversed at seed 43. GMM-B had the lowest mean test NLL, `0.694560`, versus task-only `0.696578`, with paired deltas `-0.003897/-0.002480/+0.000322`. This is eligible measurement, not yet a researcher-confirmed mechanism judgment.
- A6R1 result figure and table exist under `A6R1_online_regularized_router_decay/figures/` and `tables/`; the figure excludes old constant-`0.1` arms. Canonical A6R1 Summary/Detailed and Focus/Anchor result updates are still absent.
- Existing S0--S3 artifacts under `runs/local-smoke-20260908T2210Z` are for the OLD constant-`0.1` A6 checkpoints. Their local stage files say S0, S1, S2, and S3 `COMPLETE`; no ACP submission or formal-run receipt was found. They cannot be reused as A6R1 S0--S3 evidence.
- S4 and S5 each have implementation source and one recorded unit test with no cached failures, but no S4/S5 run directory, stage result, or submission receipt. S6 was explicitly out of scope and has no implementation or result. No S0--S6 stage has yet run on A6R1 checkpoints.

## Working Understanding

The A6R1 B schemes show an average loss signal but not an all-seed ordering. Post-training analysis must therefore keep every seed and retain both successful-looking B arms and worse A arms: the A arms are needed negative controls for distinguishing route change from task benefit. Old A6 local diagnostics may inform implementation debugging only; model-dependent locks, routing relations, interventions, and stage gates must be recomputed from A6R1 starting at S0.

Working model list selected for protocol canonicalization:

- S0--S3 input matrix: task-only, SAE-A-decay, GMM-A-decay, SAE-B-decay, GMM-B-decay x seeds 17/29/43 = 15 final checkpoints.
- S4/S5 selected pair: matched task-only plus GMM-B-decay, all three seeds. GMM-B is selected by the existing frozen rule, lowest equal-seed mean NLL among the four regularized A6R1 arms. S4 candidate discovery may begin on seed 17 but confirmatory effects must retain all three seeds.
- S5 derived variants are not independent pretrained models: K (no update), R (router-only), U (old experts), and conditional C/G correction-growth variants. Keep them as isolated copies of the selected checkpoints.
- S6 starts only from frozen S5 outputs selected by its predeclared development rule and must compare against the corresponding no-adaptation and best old-capacity controls. Its exact task stream, replay budget, metric, and stop rule are pending canonical S6 design before submission.
- Exclude old constant-`0.1` A6 checkpoints, random, Dense, and unrelated external benchmark models from the new execution matrix.

## Decisions And Constraints

Researcher-confirmed in conversation: complete S0--S6; first finish missing smoke, write S6, then run the unified track on one reserved four-H100 node. Record the selected model list and complete S6 contract in a canonical A6R1 post-training Protocol before submission. Preserve all old checkpoints and artifacts; no commit, push, Graph edit, root sync, or external publication was requested. A legitimate stage stop/insufficient status is a completed decision-tree branch, but must not be mislabeled as a positive result.

## Open Loops

1. Canonicalize the approved A6R1 S0--S6 contract. The existing post-training Protocol points to old A6 and cannot silently authorize new checkpoints.
2. Define S6's continual-learning task stream, comparison models, replay/update budget, metric, and stop rule without using S6 confirmation data for selection.
3. Revalidate/adapt S0--S5 source against A6R1 paths, implement S6, authenticate model hashes, and complete missing CPU/GPU smoke checks.
4. Submit the unified S0--S6 job on the approved reserved four-H100 node and supervise it to a terminal, auditable result.
5. After results, write Summary/Detailed, then ask the researcher for the bounded judgment before updating Anchor/Focus.

## Resume Point

Write the A6R1 S0--S6 Protocol and S6 stage contract, then adapt and test the implementation. Finish the missing smoke matrix before preparing one immutable run directory and submitting the reserved four-H100 unified job. Restart scientific execution at S0; old A6 local S0--S3 outputs are implementation references only.

## Canonical References

- `Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6R1_online_regularized_router_decay/protocol.md` -- owns A6R1 training scope and completion ledger.
- `Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6R1_online_regularized_router_decay/tables/loss_comparison.csv` -- current A6R1 seed-level task-loss measurements.
- `Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6_online_regularized_router/post_training_analysis/protocol.md` -- frozen OLD-A6 S0--S6 decision tree; requires explicit A6R1 adaptation.
- `Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6_online_regularized_router/summary.md` -- canonical first reading for constant-`0.1` A6.
- `daily_research_reports/0907/focus_sae_flat_router_functional_training.md` and the linked A15_13_10 Anchor -- current canonical question; both still stop before post-training execution and need alignment after model-list confirmation.
- `/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay/runs/full-20260909T020300Z/` -- immutable A6R1 checkpoints and raw evaluation evidence.
- `/data/250010109/MoE_Router/experiments/20260909_a6_post_training_analysis/runs/local-smoke-20260908T2210Z/stage_status.json` -- non-canonical old-A6 local S0--S3 status only.
