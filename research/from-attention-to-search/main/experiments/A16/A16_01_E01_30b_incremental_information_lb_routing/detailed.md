# Detailed: A16_01_E01 30B Incremental-Information Routing Under Differentiable LB

Primary Anchor: [A16_01 Incremental-Information Routing](../../../problem_anchors/16_load_control_gradient_interference/16_01_incremental_information_lb_routing/16_01_incremental_information_lb_routing_anchor.md)  
Frozen Protocol and registered revision: [Protocol](protocol.md), pre-amendment SHA-256 `99882058e0cf6bff4334fb435eff5d9a9e7dfeaa700e36a820f9c26f8ba0e9cb`; current append-only revision `bdbfb0708c601288e79589b38d62c09734dfca283178bd1aa3c854688ec34a0d`  
Summary: `NOT CREATED` -- no 30B decision evidence exists  
Result eligibility: `INTERIM_ONLY` through the common complete 20B checkpoint; both registered endpoint verdicts remain `NOT RUN`

## 0. Quick Recap

**Purpose.** Preserve the complete execution and provenance ledger for the approved four-arm, two-seed 30B experiment.  
**Hypotheses.** Trainable-Innovation may improve over Native; if and only if a common E1+E2 certificate exists, Certified may improve over both Haar and Native.  
**Experiment logic.** All eight jobs start from step 0 under differentiable Switch LB. Certified/Haar remain dormant until a two-seed common certificate is admitted at 2B, 5B, or 10B.  
**Direct result.** All eight trajectories have complete, paired 2B/5B/10B/20B evaluations. Trainable minus Native is negative for seed 17 and positive for seed 29 at 20B, with both paired document intervals crossing zero. The early seed-17 effect does not replicate in seed 29. E1 representation readability sometimes passes, but E2 expert-choice regret admits zero layers at every registered gate; Certified and Haar therefore remain dormant and exactly reproduce Native.  
**Eligibility.** These are valid stage observations, not the registered 30B endpoint verdict.  
**Verdict.** `engineering_utility=INTERIM_NO_REPLICATED_ADVANTAGE`; `certified_direction_identity=INSUFFICIENT_NO_CERTIFICATE`; `execution_validity=20B_COMPLETE_RESUME_TO_30B_RUNNING`.  
**Claim boundary.** The ledger supports a 20B stage reading and exact-resume provenance. It does not establish the 30B arm ranking or prove that the trainable branch is unused.

### 0.2 Verified interim evaluation and 20B-to-30B continuation (2026-08-12)

This subsection supersedes Section 0.1's 2026-08-11 execution snapshot. All eight prior ACP jobs were found `SUSPENDED`, not complete. Their last telemetry ranged from 20.652B to 22.936B tokens, but every arm and seed shared one complete registered checkpoint: `checkpoint-25432`, equal to 20,000,538,624 tokens. Uncheckpointed work after 20B is intentionally discarded so all paired trajectories resume from the same state boundary.

| Arm / seed | 20B NLL | Stage comparison with same-seed Native | Continuation job |
| --- | ---: | --- | --- |
| Native 17 | 3.460888 | reference | `om-6k24u1a7` |
| Trainable 17 | 3.460141 | \(-0.000747\), 95% CI \([-0.001695,+0.000230]\) | `om-ahqbmepx` |
| Native 29 | 3.452455 | reference | `om-pqdx5ujl` |
| Trainable 29 | 3.452972 | \(+0.000517\), 95% CI \([-0.000555,+0.001538]\) | `om-5t3altuc` |
| Certified/Haar 17 | 3.460888 | dormant; documentwise identical to Native | `om-32036ovp` / `om-z3emtbdl` |
| Certified/Haar 29 | 3.452455 | dormant; documentwise identical to Native | `om-5vuythze` / `om-o5znurih` |

Each NLL uses the same 1,024 held-out documents. At 20B, Native/Trainable busiest-expert share is 13.33%--14.30% versus the eight-expert equal-share reference of 12.5%; normalized routing entropy is 0.99881--0.99952 and capacity drop is zero. Thus the absent replicated NLL advantage is not confounded by a load-collapse failure.

The eight continuation jobs use one 8×RTX 5090 SPOT node each and target step 38,147 (30,000,021,504 tokens). The approximately ten-minute platform inspection at 2026-08-12T14:42Z returned `RUNNING`, zero retries for all eight. Every log directly records loading `checkpoint-25432`, optimizer/scheduler state, continuation RNG, and the DCLM data offset; every job then executed beyond optimizer step 25,432 with finite LM and LB values. The audited post-resume steps ranged from 25,540 to 25,582 (20.086B--20.119B tokens). Certified/Haar correctly restored `active_rank=0` because no certificate had been admitted. The 20B-to-30B continuation therefore passes its initial exact-resume and finite-step guards.

### 0.1 Current execution update (2026-08-11)

This subsection supersedes the earlier startup-only status statements while preserving them below as historical receipts.

| Arm | Seed | Original job / latest valid state | Current action |
| --- | ---: | --- | --- |
| Trainable | 17 | `om-2vt07e41`; complete `checkpoint-12716`, uninterrupted at 11.43B tokens in the final inspection | keep original job running |
| Trainable | 29 | `om-wqtacbnt`; complete `checkpoint-12716`, uninterrupted at 11.47B tokens in the final inspection | keep original job running |
| Native | 17/29 | complete `checkpoint-2544`; original jobs stopped in canonical-state hashing | recovery jobs `om-0176xpsh`, `om-a9xohv5a` |
| Certified | 17/29 | complete `checkpoint-2544`; original jobs stopped before a scientific certificate verdict | recovery jobs `om-00lyr672`, `om-co6wmc45` |
| Haar | 17/29 | complete `checkpoint-2544`; original jobs stopped in the matched certificate path | recovery jobs `om-el0lp2nk`, `om-a2d0qb15` |

All six recovery jobs use immutable worker `/data/250010109/MoE_Router/experiments/20260811_a16_incremental_information_router_30b_lb_frozen_v8`, manifest-file SHA-256 `1cc908db1e1248df64b474344fefdc896cc26790b6d108559df098fb1d1ce3c3`, unchanged run directories, `RESUME_MODE=latest_registered`, target step 38,147, and LB coefficient 0.01. The display-name suffix `r1-v3` is a legacy recovery-script label; the ledger, launch logs, and worker hash identify v8 unambiguously.

At the final inspection, all six recovery jobs were `RUNNING` on one 8×RTX 5090 node each with zero retries. They had reached 2.578--2.591B tokens, had crossed the original scalar-hash failure point, were writing new TensorBoard events, and had no matches for `RuntimeError`, `Traceback`, `NaN`, or `Inf` in their current logs. These are execution-validity observations only.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Execution-validity evidence | Evidence that the intended program can run and preserve identities | hashes, gradient receipts, save/resume replay, world-size and artifact checks | typed receipt | permits scale-up when complete | any NLL advantage |
| Canonical state digest | Arm-independent identity check at certificate consumption | SHA-256 over parameters, persistent buffers, and registered step | hash | prevents activating a consumer from a different state than same-seed Native | that the certificate is useful |
| Differentiable LB receipt | Proof that the auxiliary load loss reaches the native Gate | LB-only backward gradient norm at each layer | gradient norm | rules out a logged-but-nondifferentiable LB scalar | balanced load or better NLL |
| Scientific certificate | Common layer set admitted by E1 representation and E2 expert-utility gates in both Native seeds | registered E1+E2 decision at 2B/5B/10B | typed gate receipt | authorizes matched Certified/Haar activation | universal semantic directions |

## 2. Anchor Link And Decision Point

The experiment tests whether an additive rank-56 path over the actual normalized same-layer attention-visible increment is useful under verified LB, and whether a separately certified direction has value beyond a matched Haar direction. The scientific decision remains frozen in Protocol Section 10. This execution ledger does not update the Anchor claim boundary.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual at ledger creation | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Approved scope | implementation, smoke, eight full jobs | implementation complete; P2 passed; eight P3 jobs running | `PASS_TO_P3` | Protocol status, smoke, ledger, monitor | no result verdict yet |
| Four conditions and seeds | Native, Trainable, Certified, Haar × seeds 17/29 | frozen configs contain all four arms and both seeds | `PASS` | contract validator receipt | none |
| E1 rank | 56 | 56 in model/train/arm configs and validator | `PASS` | config hashes below | none |
| LB objective | differentiable Switch LB, coefficient 0.01 | all four arm probes report `lb_requires_grad=true`; native Gate gradients are finite and nonzero in all layers | `PASS` | v2 `smoke_summary.json` | does not prove useful load or NLL |
| Step-0 identity | same seed matches across arms | all four seed-17 smoke hashes match; all four full hashes match within seed 17 and seed 29 | `PASS` | smoke summary and eight launch logs | none at startup |
| Save/resume | checkpoints 0/2/3 in P2; exact registered state recovery | smoke resume passed; all eight full trajectories loaded complete 20B model plus eight ZeRO-1 optimizer shards and executed new finite steps | `PASS` | v2 `smoke_summary.json`, 2026-08-12 continuation logs | none |
| Certificate coordination | deterministic producer/consumer, digest and timeout semantics | append-only Amendment A16_01_E01-AMEND-20260810-01 | `REGISTERED` | Protocol Section 17 | mismatch/timeout is Insufficient, never no-certificate |
| Projection validation | device-independent guard with unchanged tolerance | append-only Amendment A16_01_E01-AMEND-20260810-02; valid and bad-basis tests pass | `PASS` | v2 unit and distributed smoke | numerical validity only |
| Full startup | eight independent 8×5090 jobs with finite LM+LB telemetry | all eight RUNNING, zero retries, TensorBoard present at ten minutes | `PASS` | immutable job ledger and 32 platform snapshots | not a training or endpoint verdict |
| Stage evaluation | paired per-document arrays at 2B/5B/10B/20B | all four milestones complete for eight arm/seed cells | `INTERIM_ONLY` | curated tables and raw evaluation roots | does not replace 30B verdict |
| Full endpoint evidence | complete 30B per-document arrays for both seeds | absent; continuations are running | `NOT_RUN` | placeholders below | no endpoint verdict |

**Frozen Protocol revision.** English pre-amendment SHA-256 `99882058e0cf6bff4334fb435eff5d9a9e7dfeaa700e36a820f9c26f8ba0e9cb`; English current SHA-256 `bdbfb0708c601288e79589b38d62c09734dfca283178bd1aa3c854688ec34a0d`. Chinese current SHA-256 `8647aa7c3de05be3c529db21ff5647d81d4dc85fdbeccc51d7abea370cadf120`.  
**Execution scope approved.** Implementation, unit and single-GPU smoke, four-arm 8×5090 smoke, all eight 30B full submissions, milestone admission, and matched activation.  
**Amendments.** A16_01_E01-AMEND-20260810-01, A16_01_E01-AMEND-20260810-02, and A16_01_E01-AMEND-20260811-03; scientific conditions, thresholds, metric, and verdict rules are unchanged.  
**Retries and exclusions.** Pre-fix smoke `om-jmdqeig5`, diagnostic v3/v4/v5/v6/v7 smokes, and the six original scalar-hash failures are retained as engineering provenance. Canonical v8 smoke `om-lo6v9cvi` succeeded with zero retries. No scientific data, seed, arm, or checkpoint was excluded.  
**Missing conditions or artifacts.** The 25B/30B checkpoints and 30B endpoint arrays are absent. The full-run telemetry also lacks incremental-branch logit RMS, branch-off paired NLL, Native/Trainable route disagreement, and the branch contribution to Router margin.  
**Post-hoc analyses.** The 2B--20B trajectory reading requested on 2026-08-12 is explicitly interim and does not alter the registered 30B decision rule.

## 4. Actual Setup

**Research question.** Does a trainable actual-increment branch improve 30B NLL, and does a separately admitted rank-56 direction beat matched Haar and Native?  
**Training source.** DCLM binary shard `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10`; sequence length 1,024; global batch 768; 786,432 tokens/optimizer step.  
**Permitted supervision.** Online optimization is next-token LM plus differentiable LB only. E1/E2 labels and counterfactual losses are offline admission evidence and cannot update the 30B model.  
**Model.** Four Transformer blocks, hidden size 768, eight sparse experts plus one shared expert, top-1 routing. The frozen implementation stores 251,373,056 trainable parameters and 198,400 Router parameters in every arm so step-0 shapes match. Executed active parameters at launch are 152,108,800 for Native/Certified/Haar and 152,282,624 for Trainable; dormant branch parameters do not execute in the first three arms.  
**Objective and optimizer.** BF16 AdamW, learning rate \(10^{-4}\), betas \((0.9,0.95)\), weight decay 0.01, warm-up 636 steps, 100B-token scheduler horizon, ZeRO-1, activation checkpointing, and LB coefficient 0.01.  
**Endpoint and checkpoints.** Step 38,147 equals 30,000,021,504 tokens. Full saves occur at steps 2,544, 6,358, 12,716, 25,432, 31,790, and 38,147 (approximately 2B, 5B, 10B, 20B, 25B, 30B).  
**Seeds.** 17 and 29.  
**Conditions.** `native_lb`, `trainable_increment_lb`, `certified_increment_lb`, `haar_increment_lb`.  
**Known setup limitation.** Registered E1/E2 decisions at 2B, 5B, and 10B all returned `no_certificate`: E1 could often read hierarchy variables, but E2 admitted zero layers because the increment directions did not beat old or matched-Haar features for predicting the lower-loss expert. Certified/Haar consequently remain dormant. The production measurement smoke remains measurement-only; no 30B endpoint evidence exists yet.

### 4.1 Frozen source, model, and configuration identities

Original worker root: `/data/250010109/MoE_Router/experiments/20260810_a16_incremental_information_router_30b_lb_frozen_v2`. Recovery worker root: `/data/250010109/MoE_Router/experiments/20260811_a16_incremental_information_router_30b_lb_frozen_v8`.

| Frozen object | SHA-256 / identity |
| --- | --- |
| `SOURCE_MANIFEST.sha256` file hash | `a7e1475214aeac02fa763e8c38be135da2de2357409edab93b339002b68f0fb7` |
| Source-manifest entries | 192; `sha256sum -c` exit status 0 |
| Model config `h768_l4_8e.yaml` | `dfe7214f3f6781e708193068916276233472c76f54c9224d8c621a967a14cbb8` |
| Train config `30b.yaml` | `7500f8865c185767b767ec481b2b9ffa9e40e066d1cdcb9946680264be97ed8c` |
| Data config `dclm.yaml` | `652726f1f2609659dab652b3517dc1fb6875cebc7bccd3883470afceb4c47a61` |
| Native arm config | `b8ae9a57762e0edc1b0bd91e786586275deaf4c7b95ba7af372034e4a7bbb31b` |
| Trainable arm config | `0b66915a1eeca49fe473986d3faf40df7b876ef9700aa91c8897af830a09210d` |
| Certified arm config | `a9242c631e02cf87232f62c15cca075fb339ed0942001d67590ef5030fae4fa1` |
| Haar arm config | `fa9c7b5d4613ee8fdc7bb3d5436d610568338483ca209e0fed07c5e4d91990ce` |
| Seed-17 step-0 parameter state | `acbf8cc31086a1ea7a8918f427efae610cf4f28f7b79a37f1a6c80c03ae3d6a5` |
| Seed-29 step-0 parameter state | `e36c50e5675391acdc901e97a638cec42ae76ffc1f184a5608ad994b5ec15fb9` |

The frozen contract validator returned `status=pass`, four arms, two seeds, eight jobs, rank 56, LB coefficient 0.01, from-step-zero execution, and the registered six checkpoint steps.

### 4.2 Frozen data identities

| Data object | SHA-256 / identity |
| --- | --- |
| E1 taxonomy bank, 1,920 records | `ce91dbbd3c5071e17beeccf0d86a280dc8a3e48e0fdbf2178868da45eea18af4` |
| E2 functional tensor, 384 documents | `827129cdf5b1d44af06a034b607e40c98d5353ac8e5276b994b906c917479fd5` |
| E2 functional manifest | `0a8a00d2370735821bb553fcc5f27a8c7c0006a749e4d5b4628c8df2ee6f0192` |
| Endpoint evaluation tensor | `5c8cca2b0821f25b8e7abc50d7653dfba8d71e9ccf167fee61b82624116a52e4` |
| Endpoint evaluation manifest | `bc130d114938ddefeca0b43ff8fb53debd4ce0e5367ce6e3aca71b6a2581a987` |
| Smoke statistics split | `6dd7b83df791c75dd62307b4256acc9d399ed2df8df32ef79e68cb0fb16b930f` |
| Smoke continuity-guard split | `b41faec083b8b350972d357fd82c3c9670ae7133168e809a59b4310c3971d222` |
| Smoke validation split | `91acad820e5521832a4e54033fd062d4d275819856725d9803981c0c972a289c` |
| Production-measurement taxonomy subset | `ee9209a6c3229c2eb9f83611587af7bb353a72e65ecd4403687c8bb75ebcaa34` |
| Production-measurement E2 subset | `0b4db20a2525a9b7a75b689b50f2b24895890066f00f03f154d32eddd9a6d5d8` |

The training binary hashes remain `PENDING` in this curated ledger until the full P0 signed data manifest is mapped; the path and frozen data config are recorded, but a path is not treated as a hash.

## 5. Metrics And Registered Decision Rules

The primary unit is one held-out document. For arm \(A\), control \(B\), seed \(s\), and document \(j\), the registered contrast is \(Δ_{s,j}(A-B)=NLL^A_{s,j}-NLL^B_{s,j}\) in nat/token. Documents are equally weighted and resampled as complete paired units 2,000 times for a two-sided 95% interval.

- Engineering Pass requires Trainable minus Native to have a negative mean and a 95% upper bound below zero separately in both seeds.
- Scientific Pass requires an eligible common certificate and both Certified minus Haar and Certified minus Native to satisfy that same rule separately in both seeds.
- Complete eligible evidence missing a Pass rule is Fail. A hard guard failure is Insufficient. No common certificate by 10B is `INSUFFICIENT_NO_CERTIFICATE`.

The same computation is reported at 2B/5B/10B/20B as stage evidence. Only the 30B values are eligible for the registered endpoint verdict.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen worker integrity | P0 source identity | `SOURCE_MANIFEST.sha256` | SHA-256 verification over 192 files | none | check exit status 0 | engineering guard only | `PASS` | says nothing about runtime behavior |
| Real measurement path is constructible | P1 real-model measurement smoke | `production_measurements/seed-17.json`, `seed-29.json` | schema validator over actual 4-layer hooks and target-token-local counterfactual | seed-specific receipts, no inference | both status `pass`; no certificate emitted | engineering guard only | `PASS` | tiny deterministic subset; measurement only |
| LB is differentiable and resumable on 8 GPUs | P2 arm-specific guards | v2 `smoke_summary.json` | typed smoke validator | four arms, seed 17, three smoke steps | all four pass; checkpoints 0/2/3 and resumed step 3; Trainable projection/upstream gradients nonzero; Certified/Haar frozen projections have zero gradient while Gate/upstream gradients are nonzero | engineering guard only | `PASS` | does not prove LB improves training |
| Four-arm distributed smoke permits scale-up | all four typed arm verdicts plus aggregate identity | v2 `smoke_summary.json` | registered P2 validator | four arms, seed 17 | `status=pass`; common step-0 and three common rank-0 batch hashes; world size 8 | engineering guard only | `PASS` | three-step smoke cannot substitute for 30B |
| Full startup is healthy | P3 job identity and ten-minute supervision | full job ledger, snapshots, launch logs, TensorBoard | direct identity and finite-value audit | eight jobs at 0/2/5/10 minutes | all RUNNING at ten minutes, zero retries; finite LM+LB; one TensorBoard file per job | engineering guard only | `PASS` | early loss cannot rank arms |
| Stage Trainable effect is not replicated | interim profile only | 2B/5B/10B/20B per-document arrays | paired document bootstrap | 1,024 documents separately within both seeds | at 20B: seed 17 \(-0.000747\) \([-0.001695,+0.000230]\); seed 29 \(+0.000517\) \([-0.000555,+0.001538]\) | stage evidence only | `INTERIM_NO_REPLICATED_ADVANTAGE` | not the 30B verdict; mechanism telemetry incomplete |
| No certified direction was admitted | registered E1+E2 gate at 2B/5B/10B | `certificate_gate/step-*/joint_decision.json` | common two-seed gate | layers within each milestone and seed | E1 passed some layers; E2 passed zero eligible layers at every gate | certificate gate | `INSUFFICIENT_NO_CERTIFICATE` | does not prove all increment information is functionless |
| 20B continuation is exact and finite | checkpoint/resume guard | eight `checkpoint-25432` states and continuation logs | direct structural and runtime audit | all arms and both seeds | all loaded identical milestone boundary and executed steps 25,445--25,455 with finite LM+LB | engineering validity | `PASS` | 30B completion still pending |
| Engineering utility | Protocol Section 10 | future 30B per-document arrays | registered paired bootstrap | documents within each of two seeds | `NOT RUN` | `NOT_RUN` | `NOT_RUN` | smoke cannot substitute |
| Certified direction identity | Protocol Section 10 | future gate ledger and 30B arrays | registered gate plus paired bootstrap | documents within each of two seeds | `NOT RUN` | `NOT_RUN` | `NOT_RUN` | requires eligible certificate |

## 7. Main Results

### Eligible decision evidence

None. The registered endpoint analysis remains sealed until 30B.

### Stage-level profiling evidence

- Both real production-measurement receipts passed with the intended `post_attention_rmsnorm_old_and_delta` hook on the 4-layer, hidden-768, 8-expert model.
- The receipts used target-token-local forced-expert intervention while keeping non-target routes native and explicitly set `scientific_certificate_emitted=false`.
- Complete v2 distributed smoke passed actual LB gradients, three-step token hashes, TensorBoard, and exact-resume guards for all four arms.
- Every full job uses LB coefficient 0.01 and the same within-seed step-0 parameter hash; the first LM loss and LB scalar are also identical across arms within seed.
- At the ten-minute snapshot all eight jobs were RUNNING with zero retries; post-snapshot logs had reached optimizer steps 178--191 with finite losses.
- All 2B/5B/10B/20B held-out evaluations use the same 1,024 documents. Seed 17 shows a small Trainable advantage early, but seed 29 does not reproduce it; both 20B intervals cross zero and their point estimates have opposite signs.
- Certified/Haar are documentwise identical to Native because every registered E1+E2 gate returned `no_certificate`; this is dormant-control behavior, not three independently successful methods.
- At 20B, Native and Trainable have busiest-expert shares 13.33%--14.30%, normalized route entropy 0.99881--0.99952, and zero capacity drop. The stage result is therefore not explained by Router collapse.
- Eight immutable continuation jobs resumed the common complete 20B checkpoint and executed finite post-resume steps with zero platform retries at the audit.

### Missing or not-run evidence

The 25B/30B milestones, 30B endpoint arrays, endpoint paired-bootstrap comparisons, and final scientific verdicts. Branch-specific causal telemetry was not registered in the source run and remains unavailable.

## 8. Visualization Results

No decision-relevant figure is eligible or required before full trajectories and endpoint arrays exist.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| P0 frozen contract | source/config/data identities and validator | passed | none observed | accidental arm/rank/checkpoint contract drift | remote full-manifest mapping |
| P1 unit and real measurement smoke | frozen tests plus two production receipts | passed for recorded checks | none observed | wrong hook shape or impossible E2 intervention path | complete raw unit-test receipt mapping |
| P2 8×5090 smoke v1 | valid QR rejected by GPU float32/TF32 Gram guard | failed engineering attempt | device-dependent false rejection | nothing scientific | corrected deterministic guard |
| P2 8×5090 smoke v2 | four typed arm verdicts and aggregate receipt | passed | none | arm-interface, LB-gradient, step-0, data-hash, TensorBoard and resume faults covered by smoke | long-horizon behavior |
| P3 full submission | eight immutable ledger rows and ten-minute monitor | passed startup | none | immediate startup, identity, finite LM/LB, retry and TensorBoard faults | milestones and endpoint |
| P4 stage evaluation | complete through 20B | passed as interim profile | no 25B/30B endpoint yet | rules out a replicated Trainable benefit through 20B and a pre-10B certificate | 30B endpoint; branch mechanism |
| P5 20B continuation | eight exact resumes and finite new steps | passed initial continuation guards | none observed | checkpoint, optimizer, RNG, scheduler, and data-cursor loss at restart | completion to 25B/30B |
| P6 endpoint | no 30B evidence | not run | continuations still running | nothing | registered endpoint decisions |

No physical prior, mathematical model, operationalization, or metric has been falsified by the smoke evidence. The remaining scientific rivals are unchanged from the Protocol.

## 10. Full Experiment Record

### 10.1 Distributed smoke

| Item | Recorded value |
| --- | --- |
| Pre-fix failed job | `om-jmdqeig5`; valid QR false-rejected by GPU TF32 Gram computation |
| Corrected ACP job ID | `om-q7thsp7g` |
| Corrected display name | `a16-inc-smoke-all-s17-remote-v2-20260810` |
| Resource | one node, 8×RTX 5090, SPOT |
| Corrected terminal state | `SUCCEEDED`, zero retries |
| Unit tests before freeze | 84/84 pass |
| Aggregate four-arm verdict | `PASS` |
| Summary SHA-256 | `03b69bc5993b82037aac35a53914984f1c2dd2e13f5a74b080576e01d9325dc0` |

### 10.2 Full-job and ten-minute supervision ledger

| Planned order | Arm | Seed | ACP job ID | Submit receipt | State at 0 min | State at 2 min | State at 5 min | State at 10 min | First finite LM/LB step | TensorBoard | Notes |
| ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Native | 17 | `om-96n3fgqc` | success | RUNNING | RUNNING | RUNNING | RUNNING | loss 12.063609; LB 4.6875; coeff 0.01 | yes | post-monitor step 191, finite |
| 2 | Native | 29 | `om-e8uey2bk` | success | RUNNING | RUNNING | RUNNING | RUNNING | loss 12.050423; LB 4.5000; coeff 0.01 | yes | post-monitor step 186, finite |
| 3 | Trainable | 17 | `om-2vt07e41` | success | RUNNING | RUNNING | RUNNING | RUNNING | loss 12.063609; LB 4.6875; coeff 0.01 | yes | post-monitor step 185, finite |
| 4 | Trainable | 29 | `om-wqtacbnt` | success | RUNNING | RUNNING | RUNNING | RUNNING | loss 12.050423; LB 4.5000; coeff 0.01 | yes | post-monitor step 185, finite |
| 5 | Certified | 17 | `om-uw64a3ps` | success | RUNNING | RUNNING | RUNNING | RUNNING | loss 12.063609; LB 4.6875; coeff 0.01 | yes | post-monitor step 187, finite |
| 6 | Certified | 29 | `om-1b5z5dnr` | success | RUNNING | RUNNING | RUNNING | RUNNING | loss 12.050423; LB 4.5000; coeff 0.01 | yes | post-monitor step 188, finite |
| 7 | Haar | 17 | `om-52ka91rx` | success | STARTING | RUNNING | RUNNING | RUNNING | loss 12.063609; LB 4.6875; coeff 0.01 | yes | post-monitor step 178, finite |
| 8 | Haar | 29 | `om-e3d0bfum` | success | STARTING | RUNNING | RUNNING | RUNNING | loss 12.050423; LB 4.5000; coeff 0.01 | yes | post-monitor step 178, finite |

The monitor ran from 2026-08-10T19:16:07Z for 600 seconds and produced 32 immutable platform snapshots. At ten minutes every job was RUNNING with `current_retries=0`. The later step counts above were read after the monitor collected its eight bounded log streams and are startup-health evidence only, not comparable training outcomes.

## 11. Interpretation

The 20B evidence supports one bounded stage interpretation: the unconstrained trainable increment branch has not produced a seed-replicated held-out NLL advantage, despite healthy and slightly smoother expert load. It also establishes that representation readability is insufficient for direction admission: the decisive functional gate is expert-choice regret, and that gate rejected every eligible layer. These observations motivate a future method that predicts residual expert utility rather than treating a geometric or parameter-derived basis as the routing target. They do not predict the 30B endpoint or prove the current branch is causally unused because branch-off and route-disagreement telemetry were not recorded.

## 12. Claim Boundary

**Can claim now:** all eight trajectories have valid paired evaluations through 20B; Trainable has no replicated advantage at that stage; all registered E1+E2 gates returned no certificate; load remains healthy; and all eight trajectories have exactly resumed from the common complete 20B state toward 30B.  
**Cannot claim now:** which arm wins at 30B; that Trainable is unused or harmful; that all incremental information lacks functional value; that a public parameter basis is a Router basis; or that slightly smoother load improves NLL.

## 13. Next Decision

**Decision.** Continue all eight exact-resumed trajectories to the registered 30B endpoint; keep the endpoint decision sealed until both seeds have finite paired arrays.  
**Completion criterion.** Preserve the 25B and 30B checkpoints and telemetry, obtain 1,024-document paired 30B arrays for both seeds, and apply the unchanged Protocol Section 10 rule.  
**Resume action.** No additional action is currently required: all eight continuation jobs passed the initial exact-resume and finite-step audit. Monitor platform retries and artifact creation without changing the frozen scientific configuration.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen source manifest | original worker identity | frozen worker v2 | 192 source/config/data files | `a7e14752...fb7` | yes | engineering only | original 0--2B execution |
| Recovery source manifest | repaired worker identity | frozen worker v8 | unchanged contract plus scalar-hash repair and regressions | `1cc908db...3c3` | yes | engineering only | used only after complete 2B saves |
| English Protocol | registered contract | Research_System | approved design + three amendments | `bdbfb070...a0d` | yes | contract | scientific body preserved |
| Chinese Protocol | review companion | Research_System | same contract | `8647aa7c...120` | yes | contract | mirrors amendments |
| E1/E2 banks | admission data | frozen worker v2 | TAX and DCLM functional documents | hashes in Section 4.2 | yes | future gate only | no LM optimization |
| Production seed-17 receipt | real measurement smoke | frozen worker v1 | fixed subsets + step-0 model | `7e81214937fa7e9c836a01e6e9485543e3b3e9db1be96e7d3527dc5518b87ec4` | yes | engineering only | no certificate emitted |
| Production seed-29 receipt | real measurement smoke | frozen worker v1 | fixed subsets + step-0 model | `b0440bcea29e38006f22c8388a466ed7053126c1f1745886c032f94f11a9a1a2` | yes | engineering only | no certificate emitted |
| Failed pre-fix smoke | engineering provenance | job `om-jmdqeig5` | frozen worker v1 | job ID | yes | no | TF32 false rejection; retained, not reused |
| Four-arm smoke summary | scale-up gate | job `om-q7thsp7g` | four arm verdicts | `03b69bc5...dc0` | yes | engineering only | aggregate PASS, zero retries |
| Scalar-repair four-arm smoke | recovery gate | job `om-lo6v9cvi` | target-runtime hash tests plus four arm verdicts | `360ea52e...a40cc` | yes | engineering only | aggregate PASS, zero retries |
| Full job ledger | P3 provenance | submission script | eight jobs | `c2bc294b...246e` | yes | engineering only | immutable job IDs and launch contract |
| Recovery job ledger | P4 engineering provenance | v8 recovery submitter | six jobs from `checkpoint-2544` | SHA-256 `909bbd70981985930fcf08a085a10ff397f3d89de2387ac3e67b8a2b0aefebb4` | yes | engineering only | six IDs in Section 0.1 |
| 2B--20B NLL table | interim stage evidence | registered evaluator | eight trajectories × four milestones × 1,024 documents | [CSV](tables/interim_nll_2b_20b_20260812.csv) | yes | interim only | 30B decision remains sealed |
| Trainable-minus-Native intervals | interim stage evidence | paired document bootstrap | same-seed paired arrays | [CSV](tables/interim_trainable_vs_native_20260812.csv) | yes | interim only | no cross-seed replicated advantage |
| 20B Router health | mechanism guard | route telemetry | Native/Trainable × two seeds | [CSV](tables/router_health_20b_20260812.csv) | yes | interim only | does not measure branch use |
| 20B-to-30B job map | continuation provenance | 2026-08-12 submitter | eight complete `checkpoint-25432` states | [CSV](tables/resume_20b_to30b_jobs_20260812.csv) | yes | engineering only | all eight initially RUNNING, zero retries |
| Ten-minute snapshots | P3 startup evidence | monitor | 8 jobs × 4 times | `3168fce5...efec` | yes | engineering only | all RUNNING at 10 min, zero retries |
| 30B endpoint arrays | primary evidence | future evaluator | 1,024 paired documents | `NOT RUN` | no | no | analysis remains sealed |

## 15. Links

- Anchor: [A16_01](../../../problem_anchors/16_load_control_gradient_interference/16_01_incremental_information_lb_routing/16_01_incremental_information_lb_routing_anchor.md)
- Protocol: [canonical English](protocol.md), [Chinese companion](protocol_cn.md)
- Original code workspace: `/data/250010109/MoE_Router/experiments/20260810_a16_incremental_information_router_30b_lb_frozen_v2`
- Recovery code workspace: `/data/250010109/MoE_Router/experiments/20260811_a16_incremental_information_router_30b_lb_frozen_v8`
- Recovery smoke artifact root: `/data/250010109/MoE_Router/outputs/a16_incremental_information_lb_routing_smoke/artifacts/scalar-hash-v8-20260811-8gpu`
- Submission ledger: `/data/250010109/MoE_Router/outputs/a16_incremental_information_lb_routing/submission/full_job_ledger.jsonl`
- Recovery submission ledger: `/data/250010109/MoE_Router/outputs/a16_incremental_information_lb_routing/submission/scalar_hash_recovery_v8_job_ledger.jsonl`
- 20B-to-30B submission ledger: `/data/250010109/MoE_Router/outputs/a16_incremental_information_lb_routing/submission/resume_20b_to30b_20260812_job_ledger.jsonl`
- Ten-minute monitor: `/data/250010109/MoE_Router/outputs/a16_incremental_information_lb_routing/submission/monitor_10min_20260810T191607Z/`
- Full result root: `/data/250010109/MoE_Router/outputs/a16_incremental_information_lb_routing/`
- Interim curated tables: [NLL](tables/interim_nll_2b_20b_20260812.csv), [paired contrasts](tables/interim_trainable_vs_native_20260812.csv), [Router health](tables/router_health_20b_20260812.csv), [continuation jobs](tables/resume_20b_to30b_jobs_20260812.csv)
- Summary, figures, and 30B endpoint tables: `NOT CREATED / NOT RUN`
