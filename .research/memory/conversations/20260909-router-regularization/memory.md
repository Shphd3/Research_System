# Conversation Memory: 0909-Router Regularization

## Objective

Index the completed A6R1 Router-regularization training and S0--S6
post-training mechanism-evaluation artifacts for retrieval and independent
analysis in other conversations. This is non-canonical working context;
scientific truth and authority remain with the Anchor, Protocol, and evidence.

## Current State

- A6R1 training/internal evaluation is complete at
  `/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay/runs/full-20260909T020300Z/`.
- Formal post-training evaluation is complete at
  `/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/runs/full-20260909T052900Z/`.
  Read `completion.json` and `stage_status.json` first. The run records
  `COMPLETE` at `2026-09-09T06:03:55Z`.
- S0, S1, S2, S3, S5, all six known-boundary S6 jobs, and all six automatic
  S6 jobs completed. S4 is a typed `INSUFFICIENT` branch with reason
  `NO_D_PAIR_WITH_REQUIRED_U_D_SUPPORT`.
- `S6/registered_verdict.json` records the frozen machine mapping as
  `INSUFFICIENT`: task-only seed 43, HumanEval, support 4 lacks an eligible
  fixed-versus-growth comparator. This status is not a researcher-confirmed
  mechanism interpretation.
- Canonical `summary.md` and `detailed.md` are not yet written. Interpretation,
  claim boundary, and next decision remain researcher-owned.

## Working Understanding

Read each evidence object separately: S1 is task loss; S2 is routing; S3 is
current expert intervention/function; S4 is update-compatibility support; S5
is isolated local action; S6 is sequential adaptation and growth. Routing
agreement cannot substitute for expert utility, current function cannot
substitute for update compatibility, and internal next-token NLL is not
official HumanEval/MBPP generation performance.

## Decisions And Constraints

The researcher requested only a new cross-conversation memory named
`0909-Router Regularization` containing result locations and will analyze the
results independently. This checkpoint authorizes no rerun, scientific state
change, canonical result writing, commit, push, publication, or external sync.

## Open Loops

1. Researcher interpretation of the formal evidence.
2. Researcher decision on whether the single invalid S6 cell requires repair.
3. If separately requested after judgment, write canonical Summary/Detailed
   and update the owning Anchor/Focus.

## Resume Point

Open the formal run's `completion.json`, `stage_status.json`, and
`S6/registered_verdict.json`; then inspect only the stage tables needed for the
question. Verify conclusions against the frozen Protocol and Anchor.

## Canonical References

- `Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_11_structural_routing_incremental_learning_anchor.md` -- question and verdict rules.
- `Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6R1_online_regularized_router_decay/post_training_analysis/protocol.md` -- frozen S0--S6 contract.
- `/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/runs/full-20260909T052900Z/completion.json` -- completion and verdict pointer.
- `/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/runs/full-20260909T052900Z/stage_status.json` -- compact stage map.
- `/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/runs/full-20260909T052900Z/evidence_ledger.csv` and `artifact_manifest.json` -- evidence hashes and full inventory.
- Formal-run `S1/` -- task NLL/contrasts; `S2/` -- routing relations; `S3/` -- ablations/counterfactuals/functional contrasts; `S4/stage_status.json`; `S5/` -- local-action evidence.
- Formal-run `S6/known_boundary/` and `S6/automatic/` -- candidate, selection, detector, control, and retention tables.
- Formal-run `S6/registered_verdict.json` -- frozen machine verdict and invalid-cell record.
- `/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/submissions/pt-ah8lbe46.json` -- ACP run receipt.
