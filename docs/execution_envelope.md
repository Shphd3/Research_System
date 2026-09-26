# Execution Envelope

This file is the only canonical owner of where an experiment runs, in which
image and runtime environment, through which entry point, and what a submitted
job must leave behind as an execution certificate. It does not own the research question,
the protocol, or the result.

Protocols, Skills, and execution workspaces reference the keys below. They must
not keep a second copy of these values, and an agent must not invent a profile
key, an image URL, or a submission command.

## 1. Precedence

```text
protocol.md explicit declaration
  > this envelope's default
  > sco-control platform default
```

An exception (a run that must not use the default profile, quota, or image) is
valid only when the researcher writes it into the protocol together with its
reason. An agent must not introduce an exception on its own and must not
silently fall back to another profile.

This envelope's default is not an execution approval. A full or expensive run
still requires its protocol execution scope to be authorized.

## 2. Registry

This block is the only copy of these values.

```yaml
updated: "2026-09-25"
default_profile: h100-4-reserved
default_image: shphd-lite-0911

researcher_decisions:
  - date: "2026-09-25"
    scope: resource_selection
    decision: "For human_semantic_update_alignment only, the researcher explicitly selected multiple independent single-node 5090-4-spot allocations plus one h100-4-reserved allocation and requested maximum feasible parallelism. This supersedes the single-allocation draft within this experiment; it does not change the separate task_update_compatibility H100 prohibition. Keep comparison blocks and Solo references hardware-matched, qualify both runtime paths, and obey the experiment aggregate budget. The researcher plans to start execution in a new task; this records resource/concurrency selection, not a job submission in the current task."
  - date: "2026-09-25"
    scope: resource_selection
    decision: "For the proposed task_update_compatibility experiment only, the researcher selected single-node 5090-4-spot per task and explicitly prohibited h100-4-reserved. Task count is unrestricted and independent qualified tasks may be submitted concurrently to use available Spot capacity. This selects a profile and concurrency policy; the experiment Protocol still owns scientific approval, stage gates, and any aggregate GPU-hour ceiling. The researcher said they would submit Smoke and formal service after clarifying the design; this entry does not record that either job has been submitted."
  - date: "2026-09-23"
    scope: resource_and_execution
    decision: "For A15_17_02_E01, the researcher explicitly selected one single-node 5090-4-spot full read-only exact-17B Dense/fresh-S7/reweighted-S7 N8 separability audit and requested direct submission without any additional Spot Smoke. Reuse the passed bounded local H100 engineering Smoke plus the existing exact-17B S7 and Dense 5090 runtime qualifications; the full job must keep embedded target-GPU, identity, numerical, immutability, artifact and terminal-receipt guards. Submit exactly one full job; no extra Spot job, training, checkpoint mutation, resource fallback, automatic retry, commit, push, or publication is authorized."
  - date: "2026-09-22"
    scope: resource_and_execution
    decision: "For A15_17_01_E01 only, after the corrected four-RTX5090 engineering Smoke passes, the researcher authorizes the complete frozen 21B S7/SALL 192-example native-support audit on the same 5090-4-spot and shphd-lite-0911 tuple. The exact cosine/paired-bootstrap criterion is explicitly confirmed. Follow the bounded measurement through completion; no training, new conditions, resource fallback, commit or push. Protocol A2 owns the full scope."
  - date: "2026-09-22"
    scope: resource_and_execution
    decision: "For A15_17_01_E01 shared-direction reuse only, the researcher explicitly resumed implementation and requested a single-node four-RTX5090 engineering Smoke. Select 5090-4-spot with shphd-lite-0911 and the existing mounted SM120 runtime. Frozen 21B S7/SALL only; no optimization, full scientific analysis, automatic retry, resource fallback, commit or push is authorized. Exact scientific metric confirmation remains separate from this bounded engineering scope."
  - date: "2026-09-10"
    scope: resource
    decision: "h100-4-reserved has first priority for experiments. H100 SPOT and 5090 SPOT are deferred: do not submit them and do not offer them as a fallback."
  - date: "2026-09-10"
    scope: image
    decision: "The default image is the self-maintained shphd image. ngc-pytorch is retired as a default and kept only to reproduce earlier runs."
  - date: "2026-09-10"
    scope: image
    decision: "The researcher saves new images and announces them; an agent registers the new key here after that announcement and never promotes or guesses an image on its own."
  - date: "2026-09-11"
    scope: image
    decision: "shphd-lite-0911:shphd-mig-20260910161423 is the newest image and becomes the default. Earlier images stay registered so old runs remain reproducible; they are not the default."
  - date: "2026-09-11"
    scope: submission
    decision: "The ACP submission entry point is verified working from the new container. The private CCR image listing hangs there, so an image URL is registered only from the researcher's announcement, never discovered by listing."
  - date: "2026-09-13"
    scope: resource
    decision: "The researcher explicitly reactivated 5090-8-spot for the native Dense baseline Smoke and, only after that Smoke passes, its matched 10B run. The profile requires explicit selection and does not replace h100-4-reserved as the default."
  - date: "2026-09-13"
    scope: image
    decision: "New 5090 jobs must use the current default shphd-lite-0911 image. ngc-pytorch-25-06 is prohibited for new submissions and remains registered only as immutable provenance for earlier runs. If shphd-lite-0911 lacks SM120 support, activate an isolated /data runtime layer inside the job; never modify the base image."
  - date: "2026-09-13"
    scope: resource
    decision: "Use 5090-4-spot for the transitional native Dense baseline Smoke. Keep the formal baseline at the matched 5090-8-spot topology and check live eight-GPU capacity only after the four-GPU Smoke passes."
  - date: "2026-09-13"
    scope: resource
    decision: "For the fixed-heldout SAE checkpoint audit only, the researcher explicitly authorized either two H100 or two RTX 5090 GPUs under SPOT quota. Use h100-2-spot first because it runs the qualified H100 software path without the 5090 SM120 runtime layer; do not treat this as a general profile change."
  - date: "2026-09-13"
    scope: resource
    decision: "For analysis1 only, the researcher explicitly authorized a checkpoint-only Smoke followed by the full semantic analysis on 5090-2-spot. Supervise through normal cluster startup, then stop polling without stopping the job. This authorization excludes training, checkpoint mutation, and interruption of any existing run."
  - date: "2026-09-14"
    scope: resource
    decision: "The researcher explicitly authorized the native Dense baseline to resume from its exact complete 10B checkpoint on 5090-8-spot and extend the same trajectory to a cumulative 50B-token target. Preserve the eight-rank global batch and checkpoint lineage; this does not authorize a fresh initialization or another profile."

  - date: "2026-09-15"
    scope: resource
    decision: "For the 0915 four-layer online SAE sidecar exploration, the researcher explicitly made h100-1-spot and TWO independent 5090-2-spot jobs available (four RTX5090 GPUs total). Each 5090 job remains one node with two GPUs; this is not a cross-node distributed job. This supersedes older Spot deferral within this scope, preserves the default profile, and does not approve a token budget or submission."
  - date: "2026-09-15"
    scope: resource_and_execution
    decision: "For the independent 0915 three-model existing-checkpoint representation audit, the researcher explicitly replaced h100-2-spot with one single-node 5090-4-spot full run and authorized submission after local correctness checks. The job must execute all registered S2-S6 analyses, including 0B evolution figures and fit-only first-singular-direction removal; ETA is not a scale-reduction gate. This authorization excludes new training, checkpoint mutation, automatic resource fallback, commit, and push."
  - date: "2026-09-15"
    scope: resource_and_execution
    decision: "For the same independent 0915 three-model audit, the researcher stopped the still-pending 5090-4-spot attempt after observing competing eight-RTX5090 usage and explicitly returned the full S2-S6 submission to one single-node h100-2-spot job. This latest decision supersedes the immediately preceding 5090-4 choice; analysis scope, 0B figures, common-direction removal, no-training boundary, and no ETA scale gate remain unchanged."
  - date: "2026-09-16"
    scope: resource_and_execution
    decision: "After the h100-2-spot attempt pt-20q3i7pd failed during S2 before any qualification unit completed, the researcher explicitly replaced it with one single-node h100-4-reserved full run and authorized immediate submission. Use four independent checkpoint workers with whole-task assignment; preserve the complete S2-S6 scope, 0B figures, B2/B3 common-direction removal, no-training boundary, and registered evidence rules."

  - date: "2026-09-16"
    scope: resource_and_execution
    decision: "For the eight-layer native-forward SAE sidecar C/T pair, the researcher explicitly authorized one two-RTX5090 Spot qualification job followed, only after Smoke PASS, by TWO independent single-node eight-RTX5090 Spot runs, each 50B valid prediction tokens. Both arms share the existing training contract except reconstruction-input detach. Observe formal startup only; no ongoing supervision. This does not replace the default profile."

  - date: "2026-09-16"
    scope: resource_and_execution
    decision: "The researcher superseded the old post-Norm2 C/T plan with one final-layer raw Attention-output sidecar: no side Norm, one h100-4-reserved Smoke, then only after Smoke PASS one fresh 50B full run on the same reserved node. Once that full run is submitted, the later first-layer raw Attention-output sidecar Smoke must use 5090-2-spot and must not use the reserved H100 node. This does not authorize an eight-RTX5090 run or any old C/T launcher."
  - date: "2026-09-16"
    scope: resource_and_execution
    decision: "After the final-layer full run was submitted, the researcher authorized implementation and sequential engineering Smokes for two plugin variants on 5090-2-spot only: independent raw Attention-output SAEs at blocks 3 and 7, followed by independent SAEs at all eight blocks. This authorizes the two Smokes, not an old C/T launcher or an unregistered long-run loss aggregation."
  - date: "2026-09-16"
    scope: resource_and_execution
    decision: "The researcher confirmed layer-mean multi-SAE loss aggregation and authorized one fresh 50B formal run for the block-3-plus-block-7 raw Attention-output plugin model on one single-node 5090-8-spot job, followed by the all-eight-layer engineering Smoke on 5090-2-spot. Preserve 262,144 valid prediction tokens per complete update by using accumulation 8 on eight ranks and accumulation 32 on two ranks. The all-eight-layer 50B run remains unauthorized until its Smoke passes; no old C/T launcher, resource fallback, or checkpoint reuse is allowed."
  - date: "2026-09-16"
    scope: resource_and_execution
    decision: "Before any multi-site eight-RTX5090 formal submission occurred, the researcher superseded the immediately preceding execution order: run and complete the all-eight-layer engineering Smoke on 5090-2-spot first, then discuss eight-card submissions separately. No 5090-8-spot multi-site full run is authorized in this stage."
  - date: "2026-09-16"
    scope: resource_and_execution
    decision: "The researcher superseded the immediately preceding deferral and authorized continuous supervision of the all-eight-layer 5090-2-spot Smoke through audited PASS, followed by two separate single-node 5090-8-spot 50B submissions in order: first blocks 3+7, then all eight blocks after the first job shows eight healthy ranks, finite first-update telemetry, and durable logs. Both start fresh and retain matched 262,144-token updates; any Smoke failure or first-job startup failure stops the sequence."
  - date: "2026-09-16"
    scope: resource_and_execution
    decision: "After the common all-layer Smoke reached audited PASS and the blocks-3+7 8x5090 job was accepted but remained queued, the researcher explicitly superseded the first-job startup gate and authorized immediate submission of the separate all-eight-layer 8x5090 job. Both jobs remain fresh, independent 50B runs with matched 262,144-token updates and may coexist in the Spot queue; no fallback, checkpoint sharing, or old C/T launcher is allowed."
  - date: "2026-09-17"
    scope: resource_and_execution
    decision: "While both multi-site 8x5090 formal jobs remained STARTING with zero allocated replicas, the researcher explicitly authorized two additional fresh single-node 8xH100 Spot submissions for the same blocks-3+7 and all-eight-layer 50B conditions. Keep both 5090 jobs untouched. The H100 jobs use separate run directories and receipts, preserve eight ranks and 262,144-token updates, and do not share checkpoints or optimizer state with any sibling job."
  - date: "2026-09-17"
    scope: resource_and_execution
    decision: "For A15_17_E03 only, the researcher explicitly selected one single-node 5090-4-spot Smoke followed after audited PASS by one 5090-4-spot full read-only analysis of the single block-7/eighth-block Attention-output sidecar S7 against the qualified Dense control at common 0/0.5/1/3/5/10B checkpoints. Rebuild the prior representation figures, include 0B, fit-only first-direction removal, fixed-atom contribution figures, and token-aligned loss curves. No training, checkpoint mutation, profile fallback, commit, or push is authorized."
  - date: "2026-09-17"
    scope: resource_and_execution
    decision: "For the reweighted raw-Attention-output SAE sidecar training line, the researcher explicitly authorized stopping final-layer job pt-xs9xol7b, one four-H100 Reserved capacity Smoke, and a PASS-gated fork continuation from its complete step-59000 checkpoint with reconstruction coefficient 0.1 while preserving 262,144 tokens/update. The researcher also authorized two separate two-RTX5090 Spot Smokes followed by two separate PASS-gated eight-RTX5090 Spot fresh 50B jobs for blocks 3+7 and all eight blocks, using layer-mean reconstruction weights 0.2 and 0.8 respectively and layer-mean AuxK coefficient 1/32. Observe each formal submission for at most five minutes; a still-queued job remains scheduled. No resource fallback or batch-size grid is authorized."
  - date: "2026-09-18"
    scope: resource_and_execution
    decision: "For A15_17_E05 after exact SALL 10B became available, the researcher resumed the overall five-model read-only measurement on one single-node 5090-4-spot Smoke, followed only after audited PASS by one same-profile full run. The scope includes exact 0/0.5/1/3/5/10B representation, held-out loss, feature, activation-gradient, and shared-parameter-gradient measurements. No training, checkpoint mutation, profile fallback, commit, push, or publication is authorized."
  - date: "2026-09-18"
    scope: resource_and_execution
    decision: "For the post-hoc P-panel mean-token representation and fixed outlier-sensitivity audit only, the researcher explicitly selected one single-node 5090-2-spot Smoke followed after audited PASS by one same-profile full read-only extraction across M0/M2/S7/S37/SALL at exact 0/0.5/1/3/5/10B. This authorization excludes training, checkpoint mutation, profile fallback, commit, push, publication, and replacement of the registered last-token primary result."
  - date: "2026-09-20"
    scope: resource_and_execution
    decision: "For A15_17_E06, the researcher explicitly selected one single-node 5090-4-spot Smoke for the exact-21B Dense, original SALL, and reweighted S7 frozen representation audit, with last and mean pooling on each dataset. After audited Smoke PASS, estimate full duration from measured throughput and submit one same-profile full read-only task. Supervise the formal task for at most five minutes; if still not started, stop polling and hand supervision to the researcher. This excludes training, checkpoint mutation, profile fallback, automatic resubmission, functional intervention, commit, push, and publication."
  - date: "2026-09-20"
    scope: resource_and_execution
    decision: "For A15_17_E06 Smoke only, after four-RTX5090 Spot job pt-lzhq7zvx reached SUSPENDED with its worker Deleted and no pod output, the researcher selected one single-node h100-2-spot attempt. Observe startup for at most three minutes; if it has not started, submit one h100-1-spot Smoke with the same three 21B checkpoints and dual-pooling site checks. The implementation must partition independent case workers so a later four-GPU formal task can run in parallel. This does not select the later four-GPU formal profile, authorize duplicate active Smokes, or authorize training."
  - date: "2026-09-20"
    scope: resource_and_execution
    decision: "For A15_17_E06, after the Spot Smoke attempts produced no model output and were suspended, the researcher explicitly selected a sequential local Smoke on the visible single H100 40GB MIG slice, followed after audited PASS and ETA by one single-node 5090-4-spot full read-only analysis. The local H100 result does not prove RTX5090 runtime or 32GB memory behavior; the full job must fail closed on its own target-GPU/runtime preflight. This replaces the earlier H100 Spot Smoke transport choice for new attempts, does not authorize a new model-training run or another fallback, and preserves the at-most-five-minute full startup supervision rule."
  - date: "2026-09-20"
    scope: resource_and_execution
    decision: "For A15_17_E07 and E08, the researcher explicitly ordered local Smoke of exact-15B models first and exact common 0/0.5/1/3/5/10B models second. Only after both Smokes pass, submit two distinct single-node 5090-4-spot read-only full analysis tasks. Do not observe whether the 21B or either new formal task enters running state; successful submission ends this conversation's supervision. This supersedes E06's earlier five-minute startup supervision request, but does not alter its submitted scope or automatically resubmit it. No model/offline-SAE training, checkpoint mutation, resource fallback, commit, push, or publication is authorized."

  - date: "2026-09-22"
    scope: resource_and_execution
    decision: "For A15_17_01_E02, the researcher requested the same ongoing four-5090 frozen audit on two named exact17B S7 fresh0.1/reweighted checkpoints and explicitly waived new Smoke, requesting direct full. Reuse5090-4-spot/shphd-lite-0911 with embedded identity/numerical guards. Record NOT_RUN_USER_WAIVED, not Smoke PASS. Stop polling after submission/startup handoff; later analysis only on researcher follow-up. No training, resource fallback or automatic retry."
  - date: "2026-09-22"
    scope: resource_and_execution
    decision: "For A15_17_01_E03, the researcher selected the exact 15B pre-reduction lambda_rec=1.0 milestone and exact 17B post-reduction lambda_rec=0.1 milestone, then requested one read-only direct full audit on 5090-4-spot with shphd-lite-0911. The direct full run uses embedded GPU/loader/numerical/immutability guards; record NOT_RUN_DIRECT_FULL_USER_REQUEST for the separate Smoke status. No training, checkpoint mutation, profile fallback, retry, commit, or push."
  - date: "2026-09-22"
    scope: resource_and_execution
    decision: "For A15_17_01_E04, the researcher requested a direct full read-only comparison of the two distinct exact-15B S7 checkpoints: lambda_rec=0.1 from-scratch versus lambda_rec=1.0 original S7. Use 5090-4-spot with shphd-lite-0911 and embedded identity/numerical/immutability guards; record NOT_RUN_DIRECT_FULL_USER_REQUEST for separate Smoke. No training, checkpoint mutation, fallback, retry, commit, or push."
  - date: "2026-09-22"
    scope: resource_and_execution
    decision: "After E04 direct-full job pt-qyze07hl reached SUSPENDED with its worker Deleted, the researcher explicitly requested one separate two-RTX5090 engineering Smoke for the same exact-15B checkpoints. Use 5090-2-spot with shphd-lite-0911; run one checkpoint per GPU and record NOT_EVALUATED scientific status. This does not retry or replace the four-card full scope and does not authorize a scientific two-card full run."

profiles:
  h100-1-spot:
    status: requires_explicit_selection
    selected_on: "2026-09-15"
    allowed_scope: "0915 four-layer online SAE sidecar exploration; A15_17_E06 exact-21B three-model dual-pooling Smoke only as the user-selected fallback after a h100-2-spot attempt has not started within three minutes"
    selection_source: "Researcher explicitly stated one H100 Spot can be submitted in 0914-training scheduling on 2026-09-15"
    verified_by: "2026-09-15 read-only AEC2 list-workerspec: n6ls.iu.i40.1 exists with one 80GB GPU; Spot availability and queue time are not guaranteed"
    surface: acp
    workspace: share-space
    aec2: share-cluster
    worker_spec: n6ls.iu.i40.1
    worker_nodes: 1
    worker_processes: 1
    gpus: "1x H100 80GB SXM5"
    quota_type: spot
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
    gpu_used: true
  h100-4-reserved:
    status: default
    surface: acp
    workspace: share-space
    aec2: share-cluster
    worker_spec: n6ls.iu.i40.4
    worker_nodes: 1
    worker_processes: 4
    gpus: "4x H100 80GB SXM5"
    quota_type: reserved
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
    gpu_used: true
  h100-1-reserved:
    status: requires_explicit_selection
    surface: acp
    workspace: share-space
    aec2: share-cluster
    worker_spec: n6ls.iu.i40.1
    worker_nodes: 1
    worker_processes: 1
    gpus: "1x H100 80GB"
    quota_type: reserved
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
    gpu_used: true
  h100-2-spot:
    status: requires_explicit_selection
    selected_on: "2026-09-13"
    scope_extended_on: "2026-09-15"
    allowed_scope: "fixed-heldout SAE checkpoint audit; 0915 three-model common-checkpoint 0-10B representation audit; A15_17_E06 exact-21B three-model dual-pooling Smoke with a three-minute startup window and h100-1-spot fallback if not started"
    selection_source: "Researcher selected remote two-H100 execution and explicitly corrected the quota to Spot for the 0915 three-model audit"
    verified_by: "2026-09-15 read-only AEC2 list-workerspec: n6ls.iu.i40.2 has two 80GB GPUs, 44 vCPUs and 480 GiB host memory; Spot availability, queue time and uninterrupted runtime are not guaranteed"
    surface: acp
    workspace: share-space
    aec2: share-cluster
    worker_spec: n6ls.iu.i40.2
    worker_nodes: 1
    worker_processes: 2
    gpus: "2x H100 80GB SXM5"
    quota_type: spot
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
    gpu_used: true
  "5090-2-spot":
    status: requires_explicit_selection
    selected_on: "2026-09-13"
    scope_extended_on: "2026-09-15"
    allowed_scope: "fixed-heldout SAE checkpoint audits; analysis1 checkpoint-only semantic evaluation; 0915 four-layer online SAE sidecar exploration under separately adopted execution scope; retired 0916 paired sidecar Smoke; sequential 0916 raw Attention-output plugin Smokes for blocks 3+7 and all eight blocks after the final-layer 4H100 full run submission"
    surface: acp
    workspace: share-space
    aec2: computing-cluster-5090-01g
    worker_spec: n12lp.nn.i10a.2
    worker_nodes: 1
    worker_processes: 2
    gpus: "2x RTX 5090 32GB"
    quota_type: spot
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
    gpu_used: true
  h100-4-spot:
    status: deferred
    deferred_on: "2026-09-10"
    surface: acp
    workspace: share-space
    aec2: share-cluster
    worker_spec: n6ls.iu.i40.4
    worker_nodes: 1
    worker_processes: 4
    gpus: "4x H100 80GB SXM5"
    quota_type: spot
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
  h100-8-spot:
    status: requires_explicit_selection
    selected_on: "2026-09-17"
    allowed_scope: "0916 raw Attention-output SAE sidecar duplicate formal submissions for blocks 3+7 and all eight blocks while retaining the queued 8x5090 jobs"
    selection_source: "Researcher explicitly requested both additional 8xH100 Spot submissions without stopping the two queued 8x5090 jobs"
    verified_by: "2026-09-17 read-only AEC2 list-workerspec: n6ls.iu.i40.8 has eight NVIDIA N6LS-80G-SXM5 GPUs, 176 vCPUs and 1920 GiB host memory in share-cluster; Spot availability is not guaranteed"
    surface: acp
    workspace: share-space
    aec2: share-cluster
    worker_spec: n6ls.iu.i40.8
    worker_nodes: 1
    worker_processes: 8
    gpus: "8x H100 80GB SXM5"
    quota_type: spot
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
    gpu_used: true
  "5090-8-spot":
    status: requires_explicit_selection
    reactivated_on: "2026-09-13"
    surface: acp
    workspace: share-space
    aec2: computing-cluster-5090-01g
    worker_spec: n12lp.nn.i10a.8
    worker_nodes: 1
    worker_processes: 8
    gpus: "8x RTX 5090 32GB"
    quota_type: spot
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
    gpu_used: true
  "5090-4-spot":
    status: requires_explicit_selection
    selected_on: "2026-09-13"
    scope_extended_on: "2026-09-25"
    allowed_scope: "native Dense baseline scopes already registered; 0915/0917 existing-checkpoint representation audits; A15_17_E05 exact-10B five-model read-only Smoke and pass-gated full measurement; A15_17_E06 exact-21B three-model dual-pooling frozen audit; A15_17_E07 exact-15B and E08 verified common 0-10B two-model frozen read-only analyses after ordered local Smoke passes; A15_17_01_E01 frozen 21B S7/SALL implementation, engineering Smoke and smoke-pass-gated 192-example full read-only audit under its 2026-09-22 Protocol A2; A15_17_01_E02 user-authorized direct-full17B S7 history comparison with explicit Smoke waiver; A15_17_01_E03 user-authorized direct-full exact-15B pre-lambda1 versus exact-17B post-lambda0.1 transition audit; A15_17_01_E04 user-authorized direct-full exact-15B S7 lambda0.1 versus lambda1 comparison with embedded guards; A15_17_02_E01 one user-authorized exact-17B Dense/fresh-S7/reweighted-S7 N8 full read-only audit with no additional Spot Smoke and embedded guards; task_update_compatibility researcher-selected four-card Spot target with parallel independent task permission, subject to its own Protocol execution gates; human_semantic_update_alignment multiple independent four-card Spot allocations alongside one four-card H100 Reserved allocation under hardware-matched block and aggregate-budget gates"
    selection_source: "Researcher explicitly selected the single-node four-RTX5090 Spot profile for scoped audits on 2026-09-15, 2026-09-18, and A15_17_E06 on 2026-09-20; researcher selected it for task_update_compatibility on 2026-09-25; each run still requires its own Protocol gates"
    surface: acp
    workspace: share-space
    aec2: computing-cluster-5090-01g
    worker_spec: n12lp.nn.i10a.4
    worker_nodes: 1
    worker_processes: 4
    gpus: "4x RTX 5090 32GB"
    quota_type: spot
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
    gpu_used: true
  cpu-only-local:
    status: restricted
    surface: local_or_container
    limit: "smoke, environment checks, and read-only analysis of at most 60 minutes"
    gpu_used: false

images:
  shphd-lite-0911:
    status: default
    url: "registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423"
    interpreter: "Python 3.10"
    torch: "2.3"
    cuda: "12.4"
    numpy: "1.24.4"
    os: "Ubuntu 22.04"
    activation: "the experiment runtime.sh or the shared activation script; never install into the base environment"
    announced_by: "researcher, 2026-09-11: shphd-lite-0911:shphd-mig-20260910161423"
    verified_by: "2026-09-11 ACP job pt-qk9pkesv on h100-4-reserved: URL accepted, image pulled, 4x H100 80GB HBM3 visible, Python 3.10.12, torch 2.3.0a0+6ddf5cf85e.nv24.04, CUDA 12.4, torch.cuda.is_available True, numpy 1.24.4, /data mounted, exit 0"
    note: "The private CCR image listing hangs in this container, so this URL cannot be re-derived by listing. It is confirmed by the run above; if a future pull fails, ask the researcher for the full URL instead of editing it here."
  shphd-lite-0710:
    status: superseded
    url: "registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0710:container1-20260710154849"
    interpreter: "Python 3.10"
    torch: "2.3"
    cuda: "12.4"
    numpy: "1.24.4"
    activation: "the experiment runtime.sh or the shared activation script; never install into the base environment"
    verified_by: "A15_08 E02/E06 H100 pair; 2026-09-10 reserved analysis pod"
    note: "Replaced by shphd-lite-0911 as the default. Runs that were qualified under it keep reproducing with it."
  ngc-pytorch-25-06:
    status: prohibited_for_new_runs
    url: "registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04"
    interpreter: "Python 3.12"
    torch: "2.8"
    cuda: "12.9"
    note: "Used by A6R1 pt-b9r9id8m and earlier A15 protocols. Registry entry is provenance only. The resolver rejects it for every new submission."

legacy_profiles: [local-2xh100, local-2xh100-remote-8x5090-fallback, cpu_cached_activation_analysis_no_gpu, h100-1-spot-user-selected]

legacy_images:
  shphd-private-lite:
    url: "registry.cn-sh-01.sensecore.cn/ccr-zhicheng-03/shphd-private-lite:container1-20260523142552"
    note: "replaced by shphd-lite-0710 in the A15_08 E01 to E02 change; history only"

submission:
  entry_point: "/data/250010109/MoE_Router/experiments/20260808_online_spectral_router_30b_v1/scripts/sco_acp_compat.sh"
  resolver: "python3 templates/execution/resolve_execution_envelope.py [--profile KEY] [--image KEY] [--format shell]"
  template: "templates/execution/acp_submit_template.sh"
  note: "sco is not on PATH. The entry point starts a local management proxy, sets SCO_ZONE=cn-sh-01g with the subscription and resource group, then calls the ACP component. Verified working 2026-09-11. The private CCR image listing hangs in this container, so never try to discover an image URL by listing; read it here."
  required_gates: [DRY_RUN=0, ALLOW_SUBMIT=1, PROTOCOL_APPROVED=1, SMOKE_GATE_PASSED=1 for a full run]
  preflight: "print the resolved tuple and compare it field by field with the selected profile; refuse any mismatch"
  default_mode: "the template's default is DRY_RUN=1, which prints the tuple and the command and creates nothing"
```

Legacy keys are recognized historical values. They do not warn, and they must
not be reused for a new run. A protocol that records neither a registry key nor
a legacy key is a drift case, not an exception.

## 3. Routing

| Work | Profile | Note |
| --- | --- | --- |
| GPU training, condition matrices, formal full runs | `h100-4-reserved` | The default, and the researcher's stated first choice. No separate confirmation is needed once the protocol's execution scope is authorized. |
| Single-GPU evaluation or reproduction | `h100-1-reserved` | Only when the protocol or the current instruction names it. |
| Long CPU chain over 60 minutes: analysis, bootstrap, clustering, rendering | `h100-4-reserved` | The reserved node is used for its core count and because it is not recycled every four hours. The receipt must record `gpu_used: false`. |
| Local or container work | `cpu-only-local` | Smoke, environment checks, and read-only analysis of at most 60 minutes. A collaboration container is recycled after about four hours, so no long computation belongs inside it. |

The 2026-09-10 record that the SFT matrix analysis chain never used its four
H100, and that the reserved node was worth re-submitting only for a new training
batch, is why the CPU row states `gpu_used: false` instead of claiming GPU
value. It is not a reason to route CPU work elsewhere.

## 4. Protocol fields

A protocol that will be executed declares:

```yaml
execution_surface: acp
resource_profile: h100-4-reserved   # a key in Section 2
image_id: shphd-lite-0911           # a key in Section 2; omit to inherit default_image
env_layer: <activation script or dependency layer>   # optional
```

A protocol does not inline the image URL or the storage mount. Submission
expands the keys, and the receipt records the expanded values. A protocol that
declares none of these keys is not yet executable.

Because a new image becomes the default by moving `default_image`, a protocol
that omits `image_id` follows the default. Name `image_id` explicitly only when
the run must keep reproducing under one exact image.

## 5. Execution certificate

Submit through `templates/execution/acp_submit_template.sh`. Its dedicated
resolver reads this document, prints the selected tuple, defaults to
`DRY_RUN=1`, enforces the gates, and writes a submission receipt. Point `REMOTE_DIR` at the
experiment's own workspace and `RUN_ROOT` at its run root; the repository
defaults exist only for a quick verification.

Every submitted job leaves an execution certificate with the fields of
`templates/execution/execution_certificate_template.md`. It records the expanded
image URL, the resolved tuple, the submission entry point and exact command, the
activation script, the artifact roots, whether the GPUs were used, and which
agent and conversation owns monitoring. A certificate that omits the expanded
image cannot establish what actually ran. A submission receipt returned by the
platform is a different object: it records that a submission was accepted, not
what ran.

The platform keeps no stdout from a finished pod, so `stream-logs` returns only
the scheduling line. The submit template tees each run's output into
`<REMOTE_DIR>/acp_receipts/pod/`; a run without that log has no durable evidence
of what it did.

## 6. Agents

This envelope is written once and is read the same way by every agent. Skills
are discovered from `.agents/skills/`; `.claude/skills` is a symbolic link to
it, and the DeepSeek harness discovers `.agents/skills/` directly. Do not
maintain an agent-specific copy of these values.

- One run root has exactly one monitoring owner. Record that owner in the
  receipt. A conversation that takes over receives the owner role explicitly,
  and the previous owner stops its polling first.
- Monitor with managed background jobs. Do not create a session-local scheduled
  task: a 2026-09-09 record shows such a task re-entering a run root whose
  receipt already existed and racing a new conversation over the same output
  directory.
- Report only a state change, a failure, a required human action, or a deadline
  risk. Silence means unchanged.
- Cross-conversation context stays in
  `.research/memory/conversations/<conversation>/memory.md` with its
  `Processed by` field. A successor never rewrites a predecessor's receipt.
