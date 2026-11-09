> **Current result:** complete registered matrix; Γ does not support the preset isolation-order effect, format trend and dynamic bridge remain insufficient. Posthoc uniform-letter comparison does not establish content competence. See [Summary](summary.md) / [中文](summary_cn.md). The earlier NOT RUN / blocked entries below are historical snapshots, not current status.

# Detailed: human semantic updates — engineering qualification

Anchor: [anchor_cn.md](../../../../problem_anchors/17_shared_and_interference_learning/17_07_human_semantic_updates/17_07_human_semantic_updates_anchor_cn.md). Contract: [protocol.md](protocol.md).
Execution root: `/data/250010109/MoE_Router/experiments/20260925_human_semantic_updates`.
Scientific result: **NOT RUN**. This record concerns implementation and engineering checks; no new scientific judgment or Focus transition is made.

## 1. Question and authorized scope

Test whether the specified final-projection LoRA implementation can execute the registered answer-only, template-mixture experiment with correct counting, frozen backbone, cache numerics, and recovery. The current user explicitly requested immediate smoke completion and subsequent parallel implementation planning. Formal scientific use remains conditional on data and human-review gates. The execution approval is recorded in `receipts/authorization.json`; the original protocol snapshot is `configs/protocol_registered_snapshot.md`.

## 2. Setup and controlled variables

Frozen S7 checkpoint: exact 21,000,000,000 training tokens, not 21 billion parameters. The checkpoint SHA256 is `edd781c8f747477e9f236128d26423d435c800d37da2d446c85e4a6ebc206f33`. The loader verifies the complete manifest, token count, sidecar configuration and final down shape 1024×3072. Each GPU process also verifies the state-file hash. Tokenizer: `/data/share/Qwen3-0.6B-Base`.

Only last-block down LoRA parameters are trainable: A_ONLY, B_ONLY, S8, S16, S32, D8, D16, R8. FP32 adapters/Adam, BF16 frozen backbone, original normalization and full vocabulary output head. A32 is sampled once per seed, lower ranks take literal prefixes. Training loss denominators are 16 answer targets for Solo and 32 for mixed arms. No EOS or prompt loss. Smoke seed 17; formal seeds 17/29/43 remain planned.

The adapter and cache code is new in the execution root. Model identity/loading and answer-only masking conventions were inspected in the old task-update package. The old source-selection code and its hardcoded 64/128-target, nonrepeating training loop were not reused. Old experiment files were not modified.

## 3. Data and confirmation boundary

`prepare_data.py` read all 15,858 raw MMLU rows, fingerprinted three parquet files, globally merged exact and 5-gram-Jaccard candidate families, checked rotations and both-template lengths, and generated provisional seven-role records. No formal CONFIRM model evaluation or cache exists. This preprocessing access to raw records is distinct from unsealing confirmation outcomes.

| Subject | Candidate families before completed history/human qualification |
| --- | ---: |
| High-school mathematics | 296 |
| College mathematics | 109 |
| High-school biology | 339 |
| College biology | 165 |
| US history | 154 |
| World history | 194 |

These are **candidate counts**, not a final eligibility PASS. Automated order-dependence filtering and 527 global near-duplicate candidate links need review. Two independent human topic ratings and template-equivalence reviews are absent. Blank review forms and blind questions are under `data`.

`audit_history.py` verified that the same exact S7 had already processed 128 MMLU SCREEN questions in the prior task. Seven candidate-role families overlap this known use; four conflict with protected roles: M1 READOUT, B2 DEV, H1 CONFIRM and H2 CONFIRM. Exact identities are in `data/history_audit.json`. The provisional split is ineligible for direct formal execution. Do not inherit the prior task's historical PASS, which preceded its own SCREEN execution.

PILOT model checks use only M1/M2 four families each; other exported PILOT subjects were not fed to a model. Preserve these eight used identities when repairing roles. A deliberately conservative preview excluding *all* known SCREEN families and all eight used PILOT families leaves college mathematics at 103 fresh candidates. This is **not** proof that the registered role-specific eligibility is impossible: the Protocol permits some prior-use roles and the engineering PILOT can remain reserved. It shows why blind global exclusion/repartition would require care; do not silently reduce 104, refill by model score, or move old PILOT into protected roles.

## 4. Engineering checks and deviations

- CPU: exact per-update and per-family F1 proportions across all 16 epochs; 32/16 targets; R8 balanced routes; eight-arm parameter counts and nested A32; option rotation; gradient mixing before cosine; rival null and nonmonotonic fixtures; 720 logical versus 640 physical mapping.
- Structural CPU checks: tied branches reproduce shared-rank forward and gradients; unselected D16 branch receives no gradient; weighted loss/accuracy fixtures. FP32 tied-branch Adam is numerically close, not bitwise identical: maximum coordinate difference reached 1.405e-6. The initially invented per-coordinate 1e-6 check failed; the repair reports the discrepancy and tests full-update L2 relative to lr×sqrt(parameter count) below 1e-3. This is an engineering acceptance scope, not a scientific threshold revision. Same-path external-process recovery retains strict bitwise equality.
- A bare-Python structural invocation failed because it omitted the registered protobuf runtime environment; sourcing `runtime.sh` repaired it. A q=0 integer-weight fixture required explicit float weights. Failure details are preserved in receipts; no model result was involved.
- Local H100 MIG: all eight arms, eight updates, separate process after update 4. Adapter and Adam states are bitwise equal to uninterrupted references. Cache loss difference 0; maximum gradient relative L2 difference 3.1112e-7.
- Four-card H100: all four independent workers passed cache checks; eight arms passed external-process recovery and TensorBoard counter/finite checks. Maximum cache loss difference 0, gradient relative L2 difference 3.08071e-4, within registered 1e-3. Observed single-Adam-step adapter maximum coordinate difference 3.1024e-6; do not call full-forward and cached Adam bitwise identical. The protocol gives explicit tolerances for loss/gradient but no separate Adam-state norm tolerance; trajectory-level cache/full-forward qualification remains a formal-implementation acceptance item.
- Additional real-model guards: zero adapters, full-matrix E gradient/cache/no-op restoration, real Adam full/half-lr branches versus zero-new-gradient momentum branches, and frozen-backbone no-gradient check passed on H100.

There is no DDP qualification claim. Each GPU worker computes its whole 32/16-target update; it does not divide loss by four. The schedule has a full CPU 16-epoch identity audit; the real eight-step smoke uses deliberate PILOT repetition and is not the formal 32-family schedule. The formal trainer and complete analysis remain to be integrated and qualified as specified in the parallel implementation plan.

## 5. Execution and timing

| Profile | Job | Last verified evidence |
| --- | --- | --- |
| Local H100 MIG | local bounded process | Eight-arm smoke and recovery PASS |
| h100-4-reserved | pt-cntnbvur | Four-worker smoke and 128-step benchmarks PASS |
| 5090-4-spot | pt-bfia7m6s | Four-worker smoke, optimizer guards and 128-step benchmarks PASS |

Both ACP jobs use `shphd-lite-0911`, the execution-envelope resolver/template, one node and four GPUs. Exact tuples and image URLs are in `receipts/submissions` and execution certificates. Runtime: the S7 package's `scripts/runtime.sh`, plus `activate_5090_runtime.sh` for RTX5090. Each job is bounded by `timeout 2700`; combined remote ceiling is six GPU hours, below the eight-GPU-hour smoke allocation. Persistent pod logs are under `acp_receipts/pod`.

H100 four concurrent workers: S16 128-step loops took 8.031–9.193 seconds; D16 took 10.805–11.323 seconds. These include evaluation every eight updates and adapter/Adam saving. Each evaluation repeats the four PILOT families four times to emulate 16-family DEV compute, without claiming 16 independent PILOT families. Model loading, checkpoint hashing, cache preparation, queue time, initial/dynamic diagnostics and final confirmation are excluded. This is not the complete experiment ETA.

Additional planning checks: the queue scaffold passed 32 concurrent claims with exactly one owner and fails closed on absent formal gates. The dynamic manifest contains 270 S16 snapshots and 2,160 virtual branches, all PLANNED. The entrypoint-routing check reported five pre-existing untracked A15_17 entries outside this workstream; this was not treated as a scientific verdict or repaired by committing unrelated work.

RTX5090 four concurrent workers: S16 11.159–11.692 seconds, D16 15.571–16.715 seconds. Maximum cache loss difference 0 and gradient relative difference 3.40062e-4, within the registered bounds. All eight adapter/Adam recoveries are bitwise equal. Both device benchmark and extra-guard receipts are now complete; aggregate `receipts/smoke_receipt.json` is PASS for bounded engineering only.

## 6. Parallel implementation and next action

The physical manifest contains 100 hardware-matched Solo and 540 mixed trajectories: H100 75 and RTX5090 565. A four-Spot-node scenario assigns 142/141/141/141 trajectories and 75 to H100; it is a planning scenario, not five formal jobs already submitted. `plan_parallel.py` derives compute-only ETA from receipts when available.

See [runtime_parallel_cn.md](runtime_parallel_cn.md) for the independent data/review, formal trainer/scheduler, mechanism-diagnostic and confirmation-analysis work packages and their acceptance gates. Target-hardware qualification is complete. The immediate operational next action is to repair data eligibility and complete formal pipeline acceptance before execution. The researcher owns scientific judgment; Γ, Ω, M and their interpretation are NOT RUN. No SAE routing test or scientific claim is inferred from smoke.

## 7. Evidence and artifact map

All paths below are relative to the execution root. `receipts/artifact_manifest.json` records exact SHA256 hashes of small provenance and decision-bearing receipts when assembled.

| Artifact | Producer / input | Scope |
| --- | --- | --- |
| `data/source_audit.json`, `family_ledger.jsonl`, `excluded.jsonl` | `scripts/prepare_data.py`; source revision and parquet hashes included | Candidate inventory only |
| `data/history_audit.json`, `repair_inventory.json` | Identity comparison with prior completed SCREEN receipt and role ledger | Known history conflicts, not total-history proof |
| `data/pilot.json` | Provisional split, only M1/M2 consumed | Engineering only; reserve used identities |
| `data/human_review_cn.md`, `human_ratings_reviewer{1,2}.csv` | Blind rendering and blank forms | No human scores supplied |
| `configs/training_manifest.json`, `parallel_4spot.json` | `contract.py`, `plan_parallel.py` | Planned, not executed |
| `receipts/cpu_smoke.json`, `structure_smoke.json`, `failure_repair.json` | CPU deterministic fixtures | Engineering validity and failure lineage |
| `receipts/local_h100/smoke_receipt.json`, `extra_guards.json` | Local real-S7 smoke and optimizer guards | H100 MIG only |
| `receipts/h100-4-reserved_smoke_v1` | `run_smoke.sh`, `gpu_smoke.py`, `audit_gpu.py`, `run_extra.py` | GPU runtime, numerical, recovery, timing, events and optimizer snapshots |
| `receipts/5090-4-spot_smoke_v1` | Same launcher on registered mounted SM120 runtime | Bounded engineering PASS |
| `receipts/submissions`, `execution_certificate_*.json`, `acp_receipts/pod` | Envelope submission template and runtime | Submission and durable execution provenance |

Round 2026-09-25: question = implementation eligibility; controlled setup/data = above; testing = PILOT and synthetic fixtures only; scientific result = NOT RUN; engineering evidence = receipts above; boundary = no semantic/rival/SAE conclusion; next action = remaining target qualification and explicit data/human gate repair.

## 8. Conditional full-run preflight after smoke acceptance

The researcher accepted the smoke and authorized full submission if eligible, followed by at most 120 seconds of supervision after successful submission, then no polling until researcher follow-up. Preflight found both reviewer forms still at 0/15 ratings, four protected-role history conflicts unresolved, and the formal trainer/registered diagnostics/analysis and complete stage-budget certificate incomplete. No full job was submitted. See `receipts/full_preflight_20260925.json` for the verified gate snapshot and preserved authorization. Future result delivery is decisive data and tables first; figure generation is reserved for the researcher’s subsequent decision.

## 9. Researcher-approved full execution (2026-09-25)

Researcher quote: “审核通过，可以执行。不行我们会后验分析调整”. Protocol A1 owns direct overall review in place of the unprovided independent forms; A2 owns the frozen execution envelope. Posthoc changes must remain separate from this registered analysis. No scientific judgment has been inferred.

Data: `data/formal_v1/role_manifest.json` preserves all original HUMAN/PILOT identities, excludes known S7 SCREEN families from remaining roles, and retains 104 families per subject. Protected-role historical overlap is zero within the documented known-history scope; pretraining decontamination is not established.

Implementation acceptance: `receipts/formal_integration_v1/receipt.json` verifies independent-process restart and bitwise adapter/Adam continuity, with eight dynamic branches restored without changing the training trajectory. `receipts/initial_integration_v1/integration_receipt.json` exercises 96 blocks/61 states using explicitly synthetic PILOT identities (56.37 seconds local H100 MIG). `receipts/full_schedule_audit.json` checks all640 trajectory streams; `receipts/analysis_cpu_audit.json` and `final_analysis_fixture.json` protect the registered estimators and same-hardware Solo mapping. These remain engineering evidence only.

Reuse: the accepted loader, LoRA module and cache arithmetic are retained; new `formal_train.py`, `diagnostics.py`, `full_worker.py`, `final_analysis.py` implement the full pipeline. Code, protocol, plan, role files, tokenizer and reused sources are hashed by `full_v1/freeze.json`; exact source copies live in `full_v1/source_snapshot`. Queues use atomic ownership; no automatic stale takeover or cross-hardware resume.

| Allocation | Profile | Job |
| --- | --- | --- |
| h100 | h100-4-reserved | pt-f91r7z02 |
| spot01 | 5090-4-spot | pt-n0zdzo5q |
| spot02 | 5090-4-spot | pt-8xk3ezij |
| spot03 | 5090-4-spot | pt-cs800c2g |
| spot04 | 5090-4-spot | pt-947ae82w |

Submission entry point: `Research_System/templates/execution/acp_submit_template.sh`, image key `shphd-lite-0911`; expanded tuple and commands are in `full_v1/submit_*.log` and `receipts/submissions`. Both dry-run resolutions were inspected before submission. Each command runs `timeout --signal=TERM --kill-after=10s 3600s bash scripts/run_full.sh PROFILE ALLOCATION`; 20 allocated GPUs imply a hard batch bound of20 GPU hours. Global final-stage deadline is1200 seconds after unsealing (at most6.67 GPU hours). Stage upper bounds are below their original limits; no extra scientific conditions or automatic retries.

ACP worker-spec query did not return metadata; availability is not claimed. Four Spot allocations are an explicit bounded launch plan, with actual readiness owned by startup snapshots. Engineering throughput suggests about15–30 minutes once all allocations run, excluding queue delays; runtime cache, IO and Spot interruptions can change this. Each allocation still stops at the one-hour cap with recoverable checkpoints.

Outputs: `full_v1/runs/RUN_ID` owns adapter/Adam/RNG/cursor checkpoints, target counters, DEV curves, TensorBoard and conditional CONFIRM per-family values; `full_v1/initial` owns Gram and transfer states; `full_v1/analysis` owns primary training, capacity, six-cell, headroom, per-subject, geometry and dynamic tables. `workers`, `failures`, durable per-worker logs and pod logs preserve execution status. CONFIRM unseal requires640 complete trajectories,270 dynamic snapshots and61 initial states plus unchanged frozen inputs, regardless of scientific sign.

The repository entrypoint checker still reports the same five unrelated untracked A15_17 files; these were neither changed nor used as approval. No commit, push, figure generation or scientific-state transition was performed.

### Final bounded startup observation

Snapshot UTC epoch 1790309580.3044014; observed startup window 146.0 seconds. Polling is now stopped; remote allocations remain autonomous.

- `pt-f91r7z02` (h100): RUNNING.
- `pt-n0zdzo5q` (spot01): RUNNING.
- `pt-8xk3ezij` (spot02): STARTING.
- `pt-cs800c2g` (spot03): STARTING.
- `pt-947ae82w` (spot04): STARTING.

Persistent worker receipts: 8; completed trajectories: 13/640; immediate failure artifacts: 0; CONFIRM unsealed: False. This is startup evidence, not scientific completion. Exact GPU names, phases and timestamps are in `full_v1/startup_snapshot_final.json`; no subsequent polling is authorized in this startup window.

## 10. Completed registered evidence and requested analysis

### Completion and eligibility before interpretation

Frozen code aggregate: `2a6fe29e2679e65a00552bada3a2751a10dbc9d389a30bca56a6dc7f613c07ed`; protocol SHA256 `b943ca0d3ce3ea74bb42feb9c9d7dc0f22f6144cf6cfc5ca4182e7c5aff27727`; role-manifest SHA256 `49cf78496996544e22ebd9d6498dd6b1fbca7e3e1fce0331565757a7820e7875`. The frozen source remains unchanged; exact copies and hashes are in `full_v1/freeze.json` and `source_snapshot`. Protocol A1/A2 precede formal observations. The initial `DRAFT` fields in the Anchor/protocol historical body do not constitute result judgment; this report follows appended execution authorization without promoting the Anchor or Focus.

| Contract item | Expected | Observed | Eligibility / evidence |
| --- | --- | --- | --- |
| Fixed physical matrix |100 Solo +540 mixed |640 complete,75 H100/565 RTX5090 |PASS; completion_audit.json |
| Updates / source exposure |128 /2048 per source |All match; mixed4096 vs Solo2048 global targets |PASS; per-run complete.json |
| DEV coordinates |0,8,...,128 |All17 records per run match |PASS; completion_audit.json |
| Dynamic rollback |90 S16 trajectories ×3 states ×8 branches |270 snapshots,2160 branches; bitwise restoration |PASS; diagnostic_*.json |
| Initial diagnostics |96 gradient blocks;61 states |Complete |PASS; initial/complete.json |
| CONFIRM access |Only after all endpoints/diagnostics and hash check |640 results after global unseal |PASS; confirm_unsealed.json and per-run confirmation |
| Human review |Original independent forms; A1 direct researcher replacement |Researcher approved; independent identities/scores absent |BOUNDED construct reliability; no fabricated raters |
| Historical overlap |No known prior SCREEN in protected roles |0 under recorded history scope |PASS for known history, not proof of pretraining decontamination |
| Statistical units |Synchronized subject families/blocks, fixed seeds |Frozen code and synthetic counterexamples checked |Conditional uncertainty only |
| New supplementary analyses |Explicit latest request to analyze further |Uniform-letter, quality, six-cell intervals and sign counts |POSTHOC_DESCRIPTIVE; no registered decision changes |
| SAE prediction |Not in this frozen execution matrix |NOT_RUN |Cannot adjudicate screenshot's SAE prediction claim |

All five ACP jobs SUCCEEDED. Training endpoint wall time was25.33 minutes from first submission; final registered analysis artifact timestamp2026-09-25T04:37:57Z, about27.5 minutes after submission. Platform allocated start/end durations sum7.472222 GPU hours, below the20 GPU-hour batch bound. Spot allocations2–4 started several minutes later than allocation1; trajectory runtime was about25.53s median/34.38s p90 on5090 and17.03s/22.14s onH100 in the inspected completion snapshot. No failures, retries, early-stop selection or new remote submissions. The follow-up request resumed inspection after the earlier startup window; no completion monitor was installed.

### Evidence lineage and registered readout

| Decision | Raw → computation | Aggregation / rule | Observation | Bounded verdict |
| --- | --- | --- | --- | --- |
| Semantic isolation order |640 confirm.json → final_analysis.training / analysis_contract.bootstrap_primary |Three mismatch levels equal; synchronized16-family resampling ×5000; Γ lower95%>0.01 and3 seeds positive |+0.001631 [-0.000521, +0.003821] |Upper bound<0.01; preset magnitude not supported |
| FAR isolation benefit |Same fixed CONFIRM endpoints |FAR S16−D8 lower95%>0.01 |-0.003145 [-0.006031, -0.000276] |Opposite direction: shared16 lower loss |
| Random-group control |R8−D8 on FAR |Same bootstrap; lower95%>0 |+0.007699 [+0.004661, +0.010844] |D8 better than R8; does not make D8 better than shared16 |
| Format trend |Matched hardware/q Solo subtraction |Both adjacent97.5% lower bounds>0.005 and seeds positive |Ω01 +0.002618 [-0.002145, +0.007699]; Ω12 +0.001776 [-0.003354, +0.006920] |Insufficient; endpoint cannot replace adjacency |
| Direction geometry |96 FP32 block gradients → FP64 Gram → mixed-q cosine |5000 paired8-block draws; lower95%>0.05 and stability |M0.053339 [0.046282,0.059684], positive halves/groups |DIRECTION_INSUFFICIENT |
| Initial local transfer |61 states → paired READOUT effects |Both scales J lower95%>0 and all source/q self-gates |J0.005130 [0.004208,0.005988]; J0.002777 [0.002075,0.003494] |Transfer conditions pass; M conjunction does not |
| Real Adam bridge |270 diagnostic snapshots → final_analysis.dynamics |step64 full/half K and new-minus-zero lower95%>0, positive seeds/self effects |Full K0.000115 [−0.002419,0.002578]; excess−0.001107 [−0.002811,0.000588] |Not supported/insufficient; self gates fail |
| Capacity |D8/D16/S16/S32 CONFIRM |Three98.333% intervals; no rescue of Γ |Q +0.003318 [+0.001090, +0.005599]; E +0.000173 [-0.002832, +0.003218]; V -0.004134 [-0.007503, -0.000680] |Higher branch rank helps D8; shared32 beats same-total D16 |
| Content competence (posthoc) |Same640 confirmed outputs → quality_and_conflict.py |Descriptive paired family95% intervals; analytical ln4 and25% reference |S16 NLL1.426884 [1.418424,1.435209]; accuracy24.4376% [23.3832%,25.5245%] |Content learning beyond trivial reference unestablished; no retroactive gate |

Primary loss units are nats per answer target; gradient cosines are dimensionless. Source files: `analysis/primary_training.csv`, `capacity.csv`, `geometry.json`, `transfer.json`, `dynamic.json`, `headroom.csv`, `semantic_format_six_cells.csv`, `per_subject_confirm.csv`. All120 pair-lineage×q×DEV-checkpoint headroom rows pass; minimum lower95% loss improvement0.763673 exceeds0.01. The120 rows reflect six unique subjects appearing in two pair lineages; they are not120 independent experiments.

### Additional read-only diagnosis, explicitly posthoc

`posthoc_scripts/readout.py` adds six-cell descriptive intervals and per-Solo DEV loss/accuracy. `posthoc_scripts/quality_and_conflict.py` reconstructs seven arm arrays with registered level weighting and matched Solo hardware, evaluates the analytic uniform-letter comparator and reports source/cross sign counts. Inputs are already-frozen endpoints and diagnostics; there is no new model inference, data selection, fitting or training. Intervals are descriptive, not a new family of corrected confirmatory tests.

The analytic comparator assigns probability1/4 to each ofA/B/C/D and zero elsewhere; its answer NLL isln4=1.386294 and, because all four answer rotations are balanced, accuracy is25%. All seven aggregate model losses and their descriptive95% lower bounds exceed this value; every accuracy interval covers25%. These statements do not establish statistical equivalence to chance or prove that all loss improvement is formatting. They show why the passed NLL-headroom gate is insufficient to claim learned topic knowledge. The frozen Γ verdict remains intact.

At step64/full learning rate, self-improves-and-cross-harm point estimates occur in18/90 NEAR directed states and28/90 FAR states. Self improvement occurs in only37/90 and41/90 respectively. These are overlapping state counts without per-cell significance, not independent binomial observations; they cannot override the registered K interval/self-improvement failure. All early/mid/late states remain reported, not cherry-picked.

SAE source lineage: `dense_sae/model/modeling_qwen3_sae.py:134–141` sets sidecar `sae_input=attention_output` before `finish_mlp`; `:66–75` applies the adapted down projection afterward, and `:200–212` feeds that earlier input to SAE. The fixed21B sidecar layer7 configuration is validated by the loader. Therefore identical input has unchanged SAE input under this last-down-only LoRA adaptation. No activation geometry, repeatability estimate, predictor or held-out SAE-to-conflict test exists in this experiment. This is a graph-of-computation fact, not empirical proof of SAE usefulness or uselessness.

### Interpretation and next decision

Direct registered result: no support for the preset semantic isolation advantage; format trend and actual-update bridge are unresolved. Initial direction ordering is positive but misses the registered effect-size support threshold. Capacity and the low-rank split remain material rival explanations.

AI interpretation, pending researcher judgment: this answer-letter task may be dominated by output calibration; the current observations are consistent with that explanation but do not directly decompose probability mass or knowledge. Do not claim the negative result disproves all semantic interference, that SAE predicts conflict, or that the mixture learned the underlying subjects.

One AI-proposed next decision: first qualify independent content generalization beyond the analytic letter reference before another semantic-interference/SAE-prediction experiment. Stop this carrier if it still primarily measures answer-format adaptation. No new experiment or scientific-state transition is authorized by this suggestion alone.

The requested four-part report is in summary.md / summary_cn.md; no new competing report, figures, Focus or Anchor conclusion was created. Artifact digests and sources are in `full_v1/result_artifact_manifest.json`.

## 11. Requested clarification: absolute loss, shared gain and isolation gain

The researcher asked whether higher FAR shared loss implied greater gain, and what worse isolation meant. This warrants a separate matched-Solo contrast rather than relabeling registered Γ. `posthoc_scripts/shared_gain_clarification.py` reads the existing fixed CONFIRM arrays, computes Solo−S16, averages three mismatch levels equally, and resamples16 families per unique subject5,000 times (RNG20260925), with shared draws across pairs/arms/views/seeds. Subjects and seeds remain fixed; descriptive95% intervals have no new multiplicity adjustment.

NEAR shared gain0.0024237929783 [−0.0000678684371,0.0048816343881]; FAR0.0003402233167 [−0.0020761639911,0.0028581871122]; NEAR−FAR0.0020835696616 [−0.0000565996265,0.0041696600245]. Seed contrasts are[0.0015933689945894815, 0.004573413946976265, 8.392604326622357e-05]. Independent six-cell means reproduce the point estimates. This is a directional signal with insufficient paired precision, not an established FAR harm effect, not equivalence, and not a replacement of Γ or its preset effect size. Solo/mixed batch difference remains.

By contrast, Γ compares S16−D8 between FAR and NEAR. Both group-average isolation gains are negative; FAR being numerically higher means a smaller disadvantage of isolation, not a positive isolation benefit. Isolation's inferior net outcome does not identify absence of all gradient conflict: active rank and update structure also differ. At the near-format endpoint, shared-minus-Solo remains negative in the point estimate; the observed trend is reduced sharing advantage, and both registered adjacent intervals remain inconclusive. No new training or selection was performed.

Result: `/data/250010109/MoE_Router/experiments/20260925_human_semantic_updates/full_v1/supplementary/shared_gain_clarification.json`; input arrays SHA256 `32db137b6385c0bcc3f78f7a63c00d782eaae030e2dec1b42dced83eb844ab7d`; producer SHA256 `93b8c5817685f5ccdc77e62d403b7c360e0ce7331a8521b602ce417f6f8155cd`. Researcher-owned scientific state remains unchanged.
