# A5 teacher and router imitation audit — 2026-09-11

Status: APPROVED_FOR_LOCAL_TWO_STEP_AUDIT by the researcher's direct 2026-09-11 request. This is an explicitly requested retrospective root-cause audit, not a reset of the active Focus or a new expert-training experiment. The two-step question, frozen h, KL/argmax metrics, no expert training, and stop-on-teacher-failure rule are researcher-specified. Numerical implementation defaults below are AI-chosen audit settings, not retrospectively registered scientific thresholds. Old audit/validation summaries were inspected before this contract; all new measurements are exploratory.

## Purpose and scope

Determine whether A5's feature groups are reproducible and interpretable enough to act as a teacher; only then diagnose how well a linear router imitates that teacher on fixed causal input states. The owning predecessor is [A5 Summary](../summary.md), with [A5 protocol](../../protocol.md). Current [Anchor](../../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_11_structural_routing_incremental_learning_anchor.md) separates teacher relations, routes, and function. This audit only inspects the first two; it cannot adjudicate expert utility, task gains, or the incremental-learning transition.

## Step 1: teacher

Use the exact A5 groups, fixed E16 SAE and original discovery/router/development caches. Authenticate copied A5 artifacts against its frozen manifest, and caches against their own manifests and group metadata. Each h is layer-27 MLP pre-input at an answer-prediction position; next-token identity is shown only to interpret examples, never added to router input.

- Extract highest raw group-activation texts on the full development answer-position cache; also show normalized group mass, unique-record top examples, representative causal token contexts, source composition, group usage and counterexamples. Feature groups, source labels, predicted token types, and semantic categories are different objects. AI semantic descriptions remain provisional; show counterexamples rather than choosing only agreeable examples.
- Re-read the original five clustering seeds and fourteen completed record-bootstrap measurements, preserving their unfinished 20-repeat receipt status and unproven null mixing. Recompute five seed partitions on the exact saved graph and three record-bootstrap graphs (seeds 20260907/08/09) with full original data. Save new mappings. Compare common-feature adjusted Rand agreement and held-out token-target relations after permutation handling. This tests grouping, not independent SAE dictionary training.
- Compare held-out within-minus-between phi on the SAME discovery-selected edge set with twenty size-preserving, frequency-decile-matched random feature mappings (seeds 2718..2737), keeping original fixed random map separately. Compute empirical null ranks descriptively; no universal semantic significance claim. The old partially mixed graph-rewiring null is not a substitute for this control.
- No backbone, dictionary, router or expert parameter is trained in Step 1. Re-clustering fixed data is analysis.

## Gate

A clear failure of provenance, absence of held-out nonrandom structure, or destructive grouping instability stops new router training. Do not equate cluster imbalance with failure or claim semantic validity just from stability. If evidence supports a bounded reproducible coactivation teacher but semantic labels remain provisional, report that boundary explicitly before using Step 2 as an imitation diagnostic; do not label the teacher a validated semantic taxonomy. No data-dependent hidden stability threshold is introduced.

## Step 2: router only, conditional on Step 1

Reevaluate the three saved offline A5 routers on original router-training and development states. Then fit one fresh seed-17 linear affine 1024→8 softmax router, with ONLY mean KL(q||p), no task loss, experts, balance-bias updates or ridge penalty. Use the complete original router split (19,787 records) and held-out development split (8,480 records), valid answer positions only. The dictionary/group map and cached h/q stay frozen. Adam lr=0.001, batches4096, gradient clipping1.0, maximum20 epochs; record every epoch's train/dev KL, accuracy and group recall. Save the minimum TRAIN-KL epoch (no validation selection) and final epoch. This is a fixed-budget fit check, not a claim of global optimization convergence. Preserve old validation-selected checkpoints as separate observations.

Report constant-prior KL/majority accuracy, micro accuracy, macro recall, per-group support/recall, and q top-two margins. Soft near ties can change argmax while barely affecting KL. A training/validation gap indicates generalization difficulty for this dataset/model/training setting, not intrinsic impossibility of predicting q from h. Poor training fit calls for checking optimization, regularization, position and capacity; do not name capacity as the proven cause.

## Local execution, checks and completion

Run bounded analysis on the already attached container, with at most its one visible GPU and bounded CPU threads; no new ACP allocation or full LM training. User approval is for these two cheap audit steps. Raw outputs/code live in `/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/audits/teacher_router_20260911/`. No original artifact edits. Save input/source hashes, selection rules, stage times, environment, failed stages, all metrics and maps. Assert no record/content overlap, finite normalized q, parameter/optimizer membership, no balancing bias, immutable teacher inputs. If a stage fails, preserve failure and repair only implementation problems within scope; do not train experts or run Steps3/4.

Completion is an evidence-backed answer to each requested question, exact missing boundaries, conditional Step2 run/skip state, and Summary/Detailed. Interpretation is AI-audited wording awaiting researcher confirmation; scientific state remains unchanged. No commit/push/publication.
