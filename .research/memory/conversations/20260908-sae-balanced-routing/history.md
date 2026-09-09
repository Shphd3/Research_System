# Conversation History: SAE balanced routing

## 2026-09-08 -- Evaluation handoff requested

- Change: User requested evaluation planning and a new task `0908-evaluation` with gpt-5.6-sol / high; current memory now includes the minimum reading order and concrete implementation resume point.
- Why it matters: Evaluation preparation may proceed, but full/expensive remote evaluation scope still needs a concrete budget; task creation is unavailable through the current tool surface.
- Supersedes: Reporting-only objective; does not supersede frozen experiment contracts or authorize new scientific conclusions.
- References: memory.md Resume Point; A5 detailed.md section 10 and frozen run evaluation_manifest.json.

## 2026-09-08 12:42:04 UTC -- Completed training to bounded benchmark planning

- Change: Created the requested memory checkpoint after live verification of full A5 training and internal evaluation; result figures and mean tables now exist.
- Why it matters: The seed reversal prevents a stable SAE advantage claim; benchmark runtime must be measured before a large evaluation.
- Supersedes: This conversation's earlier operational state of formal training just started, not the old E20 result record.
- References: Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A5_balanced_h/summary.md and detailed.md; run manifest /data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/manifest.json.

## 2026-09-08 16:16:12 UTC -- Matched online-router objective clarified

- Change: User confirmed online joint router/expert training with identical initialization; compare task-only, SAE regularization and GMM regularization only, excluding random and Dense. User requests explanation of A (fixed-target alignment) versus B (pairwise separation), not a run in this turn.
- Why it matters: Old frozen-teacher arms versus online task-only do not isolate structural regularization. Teacher labels may remain fixed while the router learns online. Desired separation concerns routing, not automatically moving frozen features or semantic centers.
- Supersedes: Earlier five-arm proposal as the next-training scope; no old results or other task execution is overwritten or cancelled. Scientific intent is pending canonicalization; exact regularizer and remote execution scope remain unset.
- References: memory.md; frozen run source/model.py and train.py; existing Protocol A5.6–A5.9 remains the owner of the old experiment only.

## 2026-09-08 -- Four-condition overnight implementation handoff

- Change: User confirmed alignment purpose and requested explicit A and B for both SAE/GMM, memory and a prompt for an experiment Agent to implement and submit full training by next morning. Wrote A6 protocol and launch_prompt.md; no job launched in the authoring task.
- Why it matters: Four new conditions replace the earlier A-first suggestion. Protocol defaults specify three seeds, online teacher targets, loss normalization, one bounded smoke and four-H100/six-node-hour scope. The launch prompt accepts defaults and authorizes implementation through internal results without repeated approval rounds.
- Supersedes: Earlier next step of choosing A or B; both are now requested. Existing task-only is reusable only if matched. Historical external-evaluation plans do not automatically apply to this overnight run.
- References: A6_online_regularized_router/protocol.md; launch_prompt.md; memory.md.

## 2026-09-09 03:19:57 UTC -- Lower-decay result and S0--S5 objective

- Change: A6 and A6R1 training/internal evaluations are complete. The researcher now requires complete S0--S5 execution after the model list is frozen; S6 is excluded. The recommended new list is all five matched A6R1/task-only conditions x three seeds for S0--S3, then task-only plus selected GMM-B-decay x three seeds for S4/S5, with K/R/U and conditional C/G as isolated S5 variants.
- Why it matters: Existing local S0--S3 artifacts used old constant-`0.1` A6 checkpoints; S4/S5 have source only and S6 is out of scope. None of those artifacts establishes post-training behavior for A6R1, so the new execution must restart at S0 after a canonical model-list amendment.
- Supersedes: The earlier resume point of launching A6 training and the old-A6 post-training target. It does not erase old A6 results or authorize silent reuse of old stage locks.
- References: A6R1_online_regularized_router_decay/protocol.md and tables/loss_comparison.csv; A6_online_regularized_router/post_training_analysis/protocol.md; memory.md.

## 2026-09-09 03:33:06 UTC -- Scope expanded to unified S0--S6 execution

- Change: The researcher expanded the target from S0--S5 to S0--S6, directed completion of missing smoke first, required S6 to be fully specified and implemented, and authorized one unified reserved four-H100 execution after those gates pass.
- Why it matters: S6 was previously undefined and unauthorized, so its task stream, controls, metric, and stop rule must be canonicalized before submission. Old A6 smoke/results remain non-substitutable for A6R1.
- Supersedes: The prior exclusion of S6 and the plan to stop at S5; it preserves the selected A6R1/task-only model matrix and all evidence boundaries.
- References: memory.md Objective, Decisions And Constraints, Open Loops, and Resume Point; pending A6R1 post-training Protocol.
