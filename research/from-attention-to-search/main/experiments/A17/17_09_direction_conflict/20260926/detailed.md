# Detailed: 20260926_direction_conflict

Primary [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_09_direction_conflict/17_09_direction_conflict_anchor.md); frozen [Protocol](protocol.md); [Summary](summary.md), [Chinese Summary](summary_cn.md).

Execution root: /data/250010109/MoE_Router/experiments/20260926_direction_conflict.
Job: pt-hef6bdtm. Human scientific judgment: Unknown. AI implements the explicit delegation; no Focus/project-state transition.

## 0. Quick Recap

Purpose: separate target-direction effects from generic step size/source progress.
Hypothesis and logic: target reflection versus matched reflection, plus component deletion versus matched-norm shrinkage.
Direct result:

| Relative step | M: extra harm | T: actual harm | Z: targeted relief |
|---|---|---|---|
| 0.0001 | 8.0197655e-05 [6.8449829e-05, 9.199544e-05] | -7.3055722e-05 [-9.266376e-05, -5.4101735e-05] | 4.4049894e-05 [3.8070249e-05, 5.0201894e-05] |
| 5e-05 | 4.0176776e-05 [3.4313122e-05, 4.6057625e-05] | -3.6642887e-05 [-4.645446e-05, -2.712728e-05] | 2.2023582e-05 [1.9048497e-05, 2.5094452e-05] |

Eligibility: ELIGIBLE for the registered exploratory comparison. All four workers completed with finite outputs, cache/derivative checks, exact zero/reset repetition and unchanged model/buffers.
Verdict: INSUFFICIENT_OR_HETEROGENEOUS. Source qualification: 152/152. Failed/uncertain gates: rho=0.0001: T lower95%=-9.266376e-05; rho=5e-05: T lower95%=-4.645446e-05.
Boundary: Constructed local directional sufficiency on one fixed model and previously exposed readout panel; not the natural origin or prevalence of data interference, SAE identification, or long-run training benefit.
Human scientific judgment: Unknown. AI interpretation: The full registered support criterion is not met. The specific failed or uncertain gates are retained below; a positive contrast alone is not upgraded to harmful-interference evidence.

## 1. Terminology / Definitions

| Term | Plain meaning | Computation / unit | Why it matters | Cannot prove |
|---|---|---|---|---|
| Target harm | B becomes harder to predict | after minus baseline mean cross-entropy, nats/prediction | Independent task consequence | Why natural data produced the update |
| Source help | A benefits | baseline minus updated mean loss | Distinguishes learning conflict from arbitrary damage | Identical finite-step source benefit |
| Target reflection | Flip the original step's target-gradient component | Protocol section9 | Controlled orientation intervention | Ordinary source SGD |
| Matched reflection | Same magnitude, distance and source fit derivative; alternative direction | Three orthogonal random controls | Tests strongest size/progress rivals | Equal per-record representation displacement |
| Rescue / shrink | Delete target component / uniformly reduce update to same norm | Protocol sections9–10 | Tests generic shrinkage rival | All paths of mediation |
| M / T / Z | Extra harm / actual reflection harm / targeted relief | Equal mean of twelve ordered domain pairs | Joint registered decision | Natural incidence or long-run benefit |

## 2. Anchor Link And Decision Point

The shared-learning question remains unchanged. This bounded test asks whether a deliberately changed update direction transfers its predicted harmful effect to other records. It does not repurpose the older stopped compatibility SCREEN or modify the completed atom-enrichment design. Next scientific decision remains researcher-owned; AI proposes a bounded reading after measurement.

## 3. Protocol Freeze, Conformance, And Deviations

Frozen UTC: 2026-09-26T15:40:39.415863+00:00; Protocol SHA256: 20c0e68bdb55902253c530987e81950ee42e3d0e90fb2c668316709b87bbee8f.
The46-file [registration](/data/250010109/MoE_Router/experiments/20260926_direction_conflict/registration.json) was verified before full execution. Exact original document bytes remain in registration_documents/. No scientific amendment, runtime retry, excluded pair, changed seed or selected step.

| Registered item | Expected | Actual | Status / evidence |
|---|---|---|---|
| Scope | Delegated bounded theory, smoke and full | Current user instruction; no cumulative training | Conformant |
| Data/splits |128 fit +128 other records/domain; four domains | Four identical512-record readout inventories | Conformant, records.json |
| Conditions |152 branches, two steps, three controls/pair |152/152, all12 cross pairs | Conformant, branches.json |
| Construction |All pair cosines in(0,1/sqrt(2)); matching guards | Cosines 0.1055751–0.17358934; max unit matching error 2.22e-16 | PASS, construction.json |
| Readout guards |Finite, cache/derivative agreement, zero/reset, unchanged model | All workers PASS; max cache discrepancy 0 | PASS, complete.json |
| Analytic / smoke |18 exact cases;38 smoke branches on16 records | PASS | Engineering only |
| Resource |4 full H10080GB Reserved, fixed image |4 qualified devices, pt-hef6bdtm | execution_certificate.json + platform receipt |
| Estimator |2000 paired stratified bootstraps, seed2026092601 | Frozen analyze.py, all gates reported | Conformant |

Shared S7 runtime dependency has an additional identity at runtime/runtime_dependency_identity.json; this provenance supplement changed no code or rule. Local smoke used H100 MIG3g.40gb only for qualification. Main execution used the registered full devices.
Result-writing and artifact-audit scripts were added after registration; they read the already frozen estimator output and do not change the scientific analysis. The post-result failure decomposition uses the already registered first-order diagnostic to explain the failed actual-harm gate; it does not replace any primary criterion. No post-hoc metric substitutes for a primary gate.

## 4. Actual Setup

Model: fresh S7 sidecar checkpoint after21,000,000,000 training tokens, not a21B-parameter model. Checkpoint SHA256: edd781c8f747477e9f236128d26423d435c800d37da2d446c85e4a6ebc206f33. Source and checkpoint locations are pinned through the four prior contract.json records.

Updated block: last attention output projection, blocks.7.attn.o.weight,1024×2048. Only virtual deltas are supplied to the linear evaluation; all parameters/buffers remain unchanged. Frozen upstream caches originated from BF16 forward computation; projection, nonlinear tail and loss are FP32. No optimizer, accumulated training trajectory or new checkpoint; TensorBoard training schedules are not applicable.

Data: the previously selected1024 natural-text records from computing, mathematics, physics and biology; two subfields per domain;128 fit and128 test records/domain;256 tokens per record. Sixteen next-token targets at positions14,30,...,254. Gradients use only source/target fit records. The512 test records are shared across all four workers, not2048 independent texts. They have previously been exposed: exploratory independent-record readout, not untouched confirmation.

Full relative steps:1e-4 and5e-5 of the selected matrix norm. Three control seeds17/29/43 and the exact pair seed transform in Protocol. For each source/step: one ordinary branch plus reflection, three matches, rescue and shrink for each of three targets, totaling19;152 branches overall.

Runtime and scripts: scripts/runtime.sh, core.py, run_worker.py, launch_four.py, run_four_h100.sh, analyze.py. Each worker hashes checkpoint/model sources, verifies baseline against prior cache and recomputes four target derivatives; checks finite outputs, repeats zero/reset, and verifies frozen parameter/buffer identity.

## 5. Metrics And Registered Decision Rules

M is target reflection harm minus mean of three matched harms; T is actual target reflection harm; Z is shrink harm minus rescue harm. Equal pair weighting at each step. The2000 bootstrap draws resample records within domain/subfield, reuse the same indices for all source/condition comparisons, and condition on fixed model, construction gradients and controls. No seed or pair is treated as an independent replicate; intervals are not simultaneous per-cell guarantees.

Source qualification requires a strictly positive lower95% bound for every branch's own-source help. SUPPORT requires this and lower95% bounds above zero for M,T,Z at both steps, plus engineering guards. Qualified M upper bounds at or below zero at both steps mean NON_SUPPORT. Other outcomes are INSUFFICIENT_OR_HETEROGENEOUS; numerical failure is INELIGIBLE. A positive M alone is insufficient.

## 6. Evidence Lineage

| Claim | Protocol criterion | Raw artifact and estimator | Aggregation / observed result | Eligibility / limitation |
|---|---|---|---|---|
| Direction-specific harm | M lower95%>0 both steps | Four source results.npz, branches.json, records.json → frozen analyze.py | 8.0197655e-05 [6.8449829e-05, 9.199544e-05]; half 4.0176776e-05 [3.4313122e-05, 4.6057625e-05] | ELIGIBLE; fixed construction and exposed panels |
| Actual target harm | T lower95%>0 both steps | Same arrays, target reflection minus baseline | -7.3055722e-05 [-9.266376e-05, -5.4101735e-05]; half -3.6642887e-05 [-4.645446e-05, -2.712728e-05] | ELIGIBLE; distinct from relative inferiority |
| Targeted relief | Z lower95%>0 both steps | Shrink minus rescue on same records | 4.4049894e-05 [3.8070249e-05, 5.0201894e-05]; half 2.2023582e-05 [1.9048497e-05, 2.5094452e-05] | ELIGIBLE; controls norm, not every source effect |
| Continued source learning | All152 lower95%>0 | Baseline minus each branch on own-domain readout | 152/152 | Required joint gate |
| Numeric / identity validity | Protocol11–13 guards | Worker construction/complete records | All complete; no exclusions | Engineering, not mechanism proof |
| Analytic relation | Exact18 examples, error<1e-12 | core.py → analytic_checks.json | PASS | Analytic illustration only |

Decision source: [registered result table](/data/250010109/MoE_Router/experiments/20260926_direction_conflict/analysis/results.json). All intervals use the same2000 within-domain/subfield record draws across sources/conditions. Pairs, control seeds and steps are not independent replications. Article-level independence is not established.

## 7. Main Results

**Actual readout: all12 reflected pair means remain negative at both steps, so targets still benefit.** At the larger step, mean loss decreases by approximately0.0001533 under matched controls and0.0000731 under target reflection. Direction changes weaken help without establishing average target harm. Targeted deletion restores benefit; it is not a demonstrated rescue of an already harmed domain.

Registered decision: INSUFFICIENT_OR_HETEROGENEOUS. The full registered support criterion is not met. The specific failed or uncertain gates are retained below; a positive contrast alone is not upgraded to harmful-interference evidence.
Failed/uncertain gates: rho=0.0001: T lower95%=-9.266376e-05; rho=5e-05: T lower95%=-4.645446e-05. Source qualification 152/152.

| Relative step | M: extra harm | T: actual harm | Z: targeted relief |
|---|---|---|---|
| 0.0001 | 8.0197655e-05 [6.8449829e-05, 9.199544e-05] | -7.3055722e-05 [-9.266376e-05, -5.4101735e-05] | 4.4049894e-05 [3.8070249e-05, 5.0201894e-05] |
| 5e-05 | 4.0176776e-05 [3.4313122e-05, 4.6057625e-05] | -3.6642887e-05 [-4.645446e-05, -2.712728e-05] | 2.2023582e-05 [1.9048497e-05, 2.5094452e-05] |

| Step | Ordinary target harm | Reflection | Matched control | Rescue | Uniform shrink |
|---|---|---|---|---|---|
| 0.0001 | -0.00015964005 [-0.0001824479, -0.0001364471] | -7.3055722e-05 [-9.266376e-05, -5.4101735e-05] | -0.00015325338 [-0.00017511238, -0.00013090236] | -0.00011639633 [-0.00013695048, -9.6143093e-05] | -7.2346438e-05 [-9.1674774e-05, -5.3612132e-05] |
| 5e-05 | -8.0011552e-05 [-9.1407027e-05, -6.8394188e-05] | -3.6642887e-05 [-4.645446e-05, -2.712728e-05] | -7.6819662e-05 [-8.776757e-05, -6.5627165e-05] | -5.837006e-05 [-6.8657644e-05, -4.8235387e-05] | -3.6346479e-05 [-4.6037892e-05, -2.6933203e-05] |

| Source → target | M, larger step | T, larger step | Z, larger step | M, half step |
|---|---|---|---|---|
| computer_science → mathematics | 0.00014838607 [0.00011823278, 0.00017861932] | -1.4156569e-05 [-6.1338081e-05, 3.1740195e-05] | 7.6286029e-05 [6.1379932e-05, 9.1562595e-05] | 7.4283375e-05 [5.9431295e-05, 8.9418593e-05] |
| computer_science → physics | 4.689799e-05 [3.4698386e-05, 6.1511334e-05] | -5.5650249e-05 [-9.8344358e-05, -1.048597e-05] | 2.4983659e-05 [1.8622377e-05, 3.2696128e-05] | 2.3523346e-05 [1.7306077e-05, 3.0851628e-05] |
| computer_science → biology | 2.739951e-05 [1.7653569e-05, 3.7175122e-05] | -0.0001074234 [-0.00014802795, -6.6730799e-05] | 1.6007572e-05 [1.0889885e-05, 2.1131127e-05] | 1.3690752e-05 [8.827704e-06, 1.8614127e-05] |
| mathematics → computer_science | 3.2687851e-05 [2.1595958e-05, 4.388763e-05] | -8.0125697e-05 [-0.00014581967, -1.5603798e-05] | 1.8235412e-05 [1.2185003e-05, 2.419299e-05] | 1.6396458e-05 [1.0915217e-05, 2.1952863e-05] |
| mathematics → physics | 6.6068334e-05 [4.7453927e-05, 8.690486e-05] | -9.4336458e-05 [-0.00016676176, -2.2925949e-05] | 3.972277e-05 [2.952707e-05, 5.1833829e-05] | 3.3369909e-05 [2.4084204e-05, 4.3846682e-05] |
| mathematics → biology | 3.9303675e-05 [2.6209544e-05, 5.2755272e-05] | -6.2813051e-05 [-0.00011503792, -1.35493e-05] | 2.3549423e-05 [1.5752017e-05, 3.1303498e-05] | 1.9650906e-05 [1.3088901e-05, 2.6347178e-05] |
| physics → computer_science | 3.5094524e-05 [2.3042703e-05, 4.6977478e-05] | -6.6829612e-05 [-0.00011257799, -2.4018949e-05] | 1.9215629e-05 [1.2725609e-05, 2.5508046e-05] | 1.7632924e-05 [1.1662275e-05, 2.3598584e-05] |
| physics → mathematics | 0.00023028937 [0.00018296359, 0.00027789503] | -7.5693242e-05 [-0.00014057434, -1.4267396e-05] | 0.00012623984 [0.00010196252, 0.00015125042] | 0.00011518116 [9.1657628e-05, 0.00013909286] |
| physics → biology | 3.1159259e-05 [2.0011313e-05, 4.2340082e-05] | -8.9360401e-05 [-0.00012673005, -5.3036818e-05] | 1.8320978e-05 [1.2384262e-05, 2.420228e-05] | 1.5675401e-05 [1.0155126e-05, 2.122183e-05] |
| biology → computer_science | 3.4286932e-05 [2.2368315e-05, 4.6030198e-05] | -9.9907396e-05 [-0.0001409883, -6.2519172e-05] | 1.9696832e-05 [1.3338091e-05, 2.5977047e-05] | 1.7063265e-05 [1.1095084e-05, 2.3030896e-05] |
| biology → mathematics | 0.0002189007 [0.00017459711, 0.00026395002] | -4.8932154e-05 [-9.4293465e-05, -7.7508623e-06] | 0.00011758041 [9.4724447e-05, 0.00014113826] | 0.00010964973 [8.7430289e-05, 0.00013224959] |
| biology → physics | 5.189764e-05 [3.7912287e-05, 6.8745312e-05] | -8.1440434e-05 [-0.00012122048, -3.9641745e-05] | 2.8760172e-05 [2.1478301e-05, 3.7460891e-05] | 2.6004078e-05 [1.8996613e-05, 3.4331592e-05] |

All values are nats/prediction, mean [conditional95% interval]. Per-pair intervals are descriptive, not simultaneous12-cell claims. Full per-arm source qualifications, all seed effects, both-step T/Z and first-order/native-displacement diagnostics are in [registered result table](/data/250010109/MoE_Router/experiments/20260926_direction_conflict/analysis/results.json).
Analytic examples and smoke remain auxiliary. Natural-data origin, SAE identification, optimizer trajectories, isolation training and fresh confirmation are NOT RUN. No failed scientific gate is repaired by auxiliary evidence.

## 8. Visualization Results

The Summary uses the smaller [key result figure](../../../../../../../daily_research_reports/backup/2026/09/0926/figures/directional_conflict_key_result.png), rendered after measurement by analysis/draw_key_result.py from the same registered two-step aggregates. This is a reader-only presentation change, not a new metric or selected pair. The full frozen four-panel figure follows.

![Controlled directional conflict](../../../../../../../daily_research_reports/backup/2026/09/0926/figures/directional_conflict_mechanism.png)

Anchor/Protocol question: does target orientation cause extra harm under matched parameter-space controls?
Sources: [registered result table](/data/250010109/MoE_Router/experiments/20260926_direction_conflict/analysis/results.json); raw four-worker arrays; analytic_checks.json for panelD. Producer: frozen scripts/analyze.py.
PanelA x: ordinary, target-directed, matched, rescue, shrink updates; y: target loss change×100,000. PanelB y: all12 ordered pairs; x: primary extra harm×100,000. PanelC x:76 branches per step, y: source benefit×100,000; dots are means, ticks lower bounds. PanelD x: input overlap; y: error-signal alignment; color: exact squared-loss change.
Aggregation/uncertainty: equal-pair averages and paired conditional95% intervals; analytic panel has no sampling uncertainty.
Expected support: M,T,Z positive with qualified source learning at both steps. Observed: INSUFFICIENT_OR_HETEROGENEOUS; see section7 for exact values. Reading: compare actual harm before interpreting extra harm.
Allowed conclusion: Constructed local directional sufficiency on one fixed model and previously exposed readout panel; not the natural origin or prevalence of data interference, SAE identification, or long-run training benefit.
No automatic Anchor/Focus scientific update: researcher interpretation remains Unknown. Date-copy provenance is recorded in the date figures/SOURCES.md and artifact manifest.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Outcome | Meaning |
|---|---|---|---|
| Analytic identity |18 exact cases and three reflection checks |PASS |Derivation/implementation only |
| Local smoke |38 branches,16 records, computing source |PASS |Engineering only |
| Startup |4 full devices, four processes, durable logs |PASS |Correct resource/runtime |
| Full measurement |152 branches,512 shared readout records |COMPLETE |Eligible arrays |
| Registered adjudication |M,T,Z and source qualification |INSUFFICIENT_OR_HETEROGENEOUS |Failed/uncertain gates: rho=0.0001: T lower95%=-9.266376e-05; rho=5e-05: T lower95%=-4.645446e-05 |

No implementation, physical identity or algebraic model failure was observed. The empirical operationalization is judged only by the named gates above.
Live limitations: targeted construction uses target fit gradients; readout panels were historically exposed; matched parameter norms do not match every representation displacement; finite-step source benefits need not be identical; rescue/shrink controls only norm, not source derivative. These bounds survive a positive result.

## 10. Full Experiment Record

2026-09-26, one round:
1. Question: does target orientation create transferable local harm beyond matched changes?
2. Setup: exact frozen last-attention block, primary norm/distance/source-derivative controls, two steps and rescue/shrink.
3. Construction data:128 fit records/domain, frozen fit gradients; no readout-gradient construction.
4. Readout:128 other records/domain,512 shared records total; previously exposed; no CONFIRM access.
5. Result: pt-hef6bdtm, four full H10080GB Reserved, all152 branches complete; launcher elapsed 119.68s; registered verdict INSUFFICIENT_OR_HETEROGENEOUS; source gate 152/152.
6. Insight/boundary/next decision: The full registered support criterion is not met. The specific failed or uncertain gates are retained below; a positive contrast alone is not upgraded to harmful-interference evidence. Constructed local directional sufficiency on one fixed model and previously exposed readout panel; not the natural origin or prevalence of data interference, SAE identification, or long-run training benefit. AI_PROPOSAL: test whether one pre-specified data/target condition makes an ordinary source update both improve its source and harm fresh target records. This follows because the controlled shift only weakened help and did not supply a stable harmful-interference carrier. Control input reuse, target requirements and update size; if conflict fails to replicate across records, stop that natural-conflict claim. Evaluate SAE identification only after an independent interference readout. Human judgment/decision remains Unknown; no next run starts automatically.

Local smoke elapsed is recorded before its final checkpoint rehash; the console completion includes that extra time. Full launcher elapsed includes worker completion and aggregation, not scheduling. No GPU-hour or ETA is inferred from scheduler startup time.

### Registered first-order diagnostic: why fit harm did not transfer

This post-result decomposition uses already saved, registered first-order readouts; it introduces no new model run or decision criterion. Source: [failure decomposition](/data/250010109/MoE_Router/experiments/20260926_direction_conflict/analysis/failure_decomposition.json), producer analysis/explain_transfer.py.

At the larger step, ordinary target first-order change is −0.00016041014; the reflection adds +0.000086804014, leaving −0.000073606124. The adverse shift cancels54.11% of the original first-order help, insufficient to make the total harmful. All12 reflected pairs remain helpful already in their readout first-order predictions. Aggregate actual-versus-linear discrepancy is0.7534% at full step and0.4371% at half step. Thus the missing harm is principally a failure of the construction-gradient sign to transfer to readout gradients, not a sign reversal caused mainly by finite-step curvature. This does not identify why the fit/readout gradient relation differs or establish an intrinsic data attribute.

Actual FP32 branch metadata also satisfies matched norm and source-derivative relative errors: max1.0907732e−7, below2e−6. Rescue/shrink norm checks pass. This supplements the pre-registered direction-construction guard without changing eligibility.

## 11. Interpretation

Human result judgment: Unknown.
AI_PROPOSAL: The full registered support criterion is not met. The specific failed or uncertain gates are retained below; a positive contrast alone is not upgraded to harmful-interference evidence.
Confirmed as measurements: the values and qualification outcomes in section7. Weakened/rejected: only explanations separated by the registered controls, conditional on all gates. Current mechanism candidate: shared computation transmits an update, and its signed relation to target sensitivity determines local consequences. Fit algebra is not an empirical discovery; readout transfer is the measured part.
Cannot claim: Constructed local directional sufficiency on one fixed model and previously exposed readout panel; not the natural origin or prevalence of data interference, SAE identification, or long-run training benefit.
Exactly one next decision: AI_PROPOSAL: test whether one pre-specified data/target condition makes an ordinary source update both improve its source and harm fresh target records. This follows because the controlled shift only weakened help and did not supply a stable harmful-interference carrier. Control input reuse, target requirements and update size; if conflict fails to replicate across records, stop that natural-conflict claim. Evaluate SAE identification only after an independent interference readout. Human judgment/decision remains Unknown; no next run starts automatically.

## 12. Claim Boundary

Can claim: all registered measurements and their gate outcome; The full registered support criterion is not met. The specific failed or uncertain gates are retained below; a positive contrast alone is not upgraded to harmful-interference evidence.
Cannot claim: Constructed local directional sufficiency on one fixed model and previously exposed readout panel; not the natural origin or prevalence of data interference, SAE identification, or long-run training benefit.
The ordinary source gradient and engineered reflected update must never be conflated. A relatively worse yet still helpful update is not actual harmful interference.

## 13. Next Decision

AI_PROPOSAL: test whether one pre-specified data/target condition makes an ordinary source update both improve its source and harm fresh target records. This follows because the controlled shift only weakened help and did not supply a stable harmful-interference carrier. Control input reuse, target requirements and update size; if conflict fails to replicate across records, stop that natural-conflict claim. Evaluate SAE identification only after an independent interference readout. Human judgment/decision remains Unknown; no next run starts automatically.

## 14. Artifact Manifest

All exact output hashes and sizes: [output artifact manifest](/data/250010109/MoE_Router/experiments/20260926_direction_conflict/analysis/artifact_manifest.json). Pre-readout code/config/data/model identities: [registration](/data/250010109/MoE_Router/experiments/20260926_direction_conflict/registration.json). No raw arrays or logs were copied into the research repository.

| Artifact | Purpose / producer | Source and identity | Complete / claim eligibility |
|---|---|---|---|
| registration.json + snapshots |Frozen contract, freeze.py |46 sources; protocol hash in section3 |Complete, identity |
| runtime/smoke_source_0/ |Engineering qualification |16-record branch arrays and checks |Complete, engineering only |
| runtime/source_<domain>/results.npz + branch/record metadata |Actual losses and diagnostics, run_worker.py |Frozen inputs; hashes in complete.json and output manifest |Complete, primary |
| analysis/results.json |Registered estimator, analyze.py |Four complete workers |Complete, eligible |
| analysis/analytic_checks.json |Exact illustrative cases, core.py |Analytic setup in Protocol12 |Complete, illustration |
| runtime/execution_certificate.json + complete.json |Devices/runtime/completion, launcher |pt-hef6bdtm; durable worker logs |Complete, execution |
| acp_receipts/ |Resolved image/profile/platform state |Reserved4H100; exact image URL in receipt |Execution evidence |
| figures/directional_conflict_mechanism.png / .pdf |Decision figure, analyze.py |Same results/analytic formula; copied to date figures |Complete, derived reading |

Reproduction: use the pinned runtime and run scripts/analyze.py against unchanged completed arrays. Do not rerun model workers in completed output folders. Archived Anchor says NOT RUN at registration; that is a historical snapshot, not present execution state.

## 15. Links

[Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_09_direction_conflict/17_09_direction_conflict_anchor.md), [Protocol](protocol.md), [English Summary](summary.md), [Chinese Summary](summary_cn.md), [core reasoning](../../../../research_notes/shared_updates/20260926/shared_update_reasoning/02_core_question_and_mechanism_cn.md), [theory](../../../../research_notes/shared_updates/20260926/shared_update_reasoning/03_theory_derivation_cn.md).
Execution workspace: /data/250010109/MoE_Router/experiments/20260926_direction_conflict.
