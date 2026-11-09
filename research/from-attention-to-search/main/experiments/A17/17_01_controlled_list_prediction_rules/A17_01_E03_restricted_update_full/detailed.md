# Detailed: A17_01_E03 Restricted Projection Full

[Summary](summary.md) · [Protocol](protocol.md)

## 0. Quick Recall

- Smoke: `pt-fleom0t0`, platform `SUCCEEDED`, engineering `PASS`, 64/64 gates; [run](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106).
- Full: `pt-ujjb8f7a`, platform `SUCCEEDED`, engineering `PASS`, 96/96 gates; [run](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z).

## 1. Question, Hypothesis And Boundary

These are actual stage states and per-trajectory facts; researcher mechanism judgment is Unknown. Three independent training seeds are descriptive; source batches are not independent experiments, and local help/harm does not establish long-term utility.

## 2. Setup And Controls

Original Qwen Base; layer27 o_proj1024×2048. L2097152 trainables; R824576,alpha8/scale1,zero-output initialization. Others frozen. AdamW1e-4,betas(.9,.95),eps1e-8,decay0,clip1,constantLR; micro5×accum4,20valid answers/update. Three seeds per variant,100updates,12000totalFull answers. Same LR is not matched functional displacement. Smoke four arms17/19,10updates,no test. Four reserved H100 GPUs,default shphd-lite-0911 image,one node,independent workers,max4 concurrently.

## 3. Data And Confirmation Boundary

Registered model_qwen3_0p6b_base and data_a17_list_rules_v1; exact release train4000/dev800/test800. Train/dev hashes checked before use; source IDs frozen before model outputs. Sources train-only; recipient full dev800. Test first-model-opened at final100 under frozen rule,not for choice. Source batches may overlap; content groups and two novelty panels retained. Dev-only Smoke does not confirm mechanism.

## 4. Implementation, Telemetry And Saves

Reuse E02 wrapper/LoRA/freeze/save/resume; adapt fixed perturbation and constant LR,retain old source/results. CPU8 tests PASS. Seven required TB tags and independent counters; no auxiliary training objective. Checkpoint states include trainables/AdamW/scheduler/RNG/cursor/counts; original Base separate. Digests verified; final restore NOT_CHECKED unless own receipt states otherwise. Update8 external restore and continuous next9 receive separate evidence. Every effective matrix perturbation saved with hash,source,eta/full-half. Family registration requests enumerate actual members,never planned saves; root owns shared registry writes.

## 5. Stage Results And Raw Evidence

| Phase | Arm | Step | Panel/reader | Order-new | Combination-new | Combined | CE | Raw |
|---|---|---:|---|---:|---:|---:|---:|---|
| Smoke | l_s17 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/l_s17/capability/update_00000.json) |
| Smoke | l_s17 | 10 | dev | 80.25% | 82.25% | 81.25% | 0.82358977 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/l_s17/capability/update_00010.json) |
| Smoke | r8_s17 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/r8_s17/capability/update_00000.json) |
| Smoke | r8_s17 | 10 | dev | 73.75% | 73.50% | 73.62% | 1.02663286 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/r8_s17/capability/update_00010.json) |
| Smoke | l_s19 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/l_s19/capability/update_00000.json) |
| Smoke | l_s19 | 10 | dev | 76.75% | 79.50% | 78.12% | 0.82121537 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/l_s19/capability/update_00010.json) |
| Smoke | r8_s19 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/r8_s19/capability/update_00000.json) |
| Smoke | r8_s19 | 10 | dev | 73.50% | 73.50% | 73.50% | 1.02643462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/smoke_20261010_0106/r8_s19/capability/update_00010.json) |
| Full | l_s29 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s29/capability/update_00000.json) |
| Full | l_s29 | 100 | dev | 89.00% | 84.25% | 86.62% | 0.55138834 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s29/capability/update_00100.json) |
| Full | l_s29 | 100 | test_fp32 | 91.00% | 86.25% | 88.62% | 0.52499711 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s29/confirmation_test_endpoint.json) |
| Full | r8_s29 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s29/capability/update_00000.json) |
| Full | r8_s29 | 100 | dev | 76.50% | 77.00% | 76.75% | 0.84565399 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s29/capability/update_00100.json) |
| Full | r8_s29 | 100 | test_fp32 | 80.75% | 76.75% | 78.75% | 0.83281099 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s29/confirmation_test_endpoint.json) |
| Full | l_s43 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s43/capability/update_00000.json) |
| Full | l_s43 | 100 | dev | 86.75% | 87.25% | 87.00% | 0.54475833 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s43/capability/update_00100.json) |
| Full | l_s43 | 100 | test_fp32 | 90.25% | 92.50% | 91.38% | 0.51536036 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s43/confirmation_test_endpoint.json) |
| Full | r8_s43 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s43/capability/update_00000.json) |
| Full | r8_s43 | 100 | dev | 76.25% | 76.50% | 76.38% | 0.84303762 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s43/capability/update_00100.json) |
| Full | r8_s43 | 100 | test_fp32 | 82.25% | 76.50% | 79.38% | 0.82925014 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s43/confirmation_test_endpoint.json) |
| Full | l_s71 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s71/capability/update_00000.json) |
| Full | l_s71 | 100 | dev | 86.00% | 84.75% | 85.38% | 0.56136077 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s71/capability/update_00100.json) |
| Full | l_s71 | 100 | test_fp32 | 90.50% | 88.00% | 89.25% | 0.52728926 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/l_s71/confirmation_test_endpoint.json) |
| Full | r8_s71 | 0 | dev | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s71/capability/update_00000.json) |
| Full | r8_s71 | 100 | dev | 78.50% | 77.50% | 78.00% | 0.83906893 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s71/capability/update_00100.json) |
| Full | r8_s71 | 100 | test_fp32 | 83.50% | 78.50% | 81.00% | 0.82661910 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/r8_s71/confirmation_test_endpoint.json) |


Complete Full effects: [descriptive_effect_cells.json](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/descriptive_effect_cells.json)

## 6. Deviations, Failure And Eligibility

Current artifact-derived state is preserved; failed outputs are never silently dropped. Precision floor is an engineering resolution guard,not scientific utility threshold. Useful source,recipient sign and dual-reader consistency are separate; ineffective source or contradictory readers is insufficient. A half LoRA-factor step need not halve matrix displacement. Later repairs require append-only Protocol ledger and preserved old sources/hashes/failure outputs.

## 7. Insight, Boundary And Next Decision

Researcher scientific interpretation Unknown. Native exact update identity and finite loss are measured before SAE. Three seeds provide descriptive repetition,not population inference. Later SAE must qualify rawhook,parent,displacement/loss-weighted reconstruction residual and finite controls; failed proxy does not overturn native evidence. Frequency is independently owned and follows root GPU-slot handoff. No architecture-utility conclusion.

## 8. Complete Source Paths

- [Execution source](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/source/runner.py), [Full config](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/configs/full.json), [Smoke config](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/configs/smoke.json).
- [Managed supervisor](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/supervise.py); monitor owner /root/stage1_full;60second polling,state-change logs only.
- [Supervision ledger](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/supervision.jsonl); each run frozen_sources.json/config_frozen.json/protocol_frozen.md, submission receipts,latest_platform.json, durable pod+arm logs,terminal_verification.json and actual registration_request.json.

## 9. Final factual synthesis / 最终事实归纳


The main native observation for direct matrices is cross-rule help: at states0/16 and eta0.01 full step,both directions,all three seeds and five sources pass source/numeric guards and lower recipient loss. Effects shrink after learning; current evidence does not establish stable net interference. All three LOCAL_HARM readouts among4320 cells trace to one L43/state100/LAST sourcebatch0 at full/half scale and different panels,not three independent discoveries. Researcher mechanism judgment remains Unknown.

Platform `SUCCEEDED`,terminal96/96PASS,six arms12000answers,42actual saved members. [Platform receipt](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/platform_terminal.json),[terminal audit](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/terminal_verification.json),[registered outputs](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/registered_outputs.json),[source means](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/native_cross_rule_seed_summary.json). The same L43/state100/LASTbatch0 has combined FIRST delta+0.000471232 ateta.01full,combination panel+0.000792480full and+0.000378446half; own-rule delta−0.000620750full/−0.000329380half. These overlapping readouts are one source/state case,not independent replications. All registered means remain negative but some individual sources/readers are insufficient. Gradient tensors and direct gradient-inner-product arrays were NOT_SAVED; gradient norms/effective matrices are actual saved evidence. Additional native/SAE replays may compute them under a separate declared stage; do not relabel ΔW/eta as exact original G.

## 10. Actual-Exposure Panel Qualification (Append-only Postprocessing)

Root authorized this audit after all learning choices were frozen. Original nominal split labels,full800primary,training,test access and native effects remain untouched. For eachstate0/16/100,only completed trajectory presentation records define seen unordered groups; virtual source probes never count. Dev/test orders have no training-order overlap. Group/record counts,per-rule cells and all source/readers are reaggregated in [actual_exposure_panel_qualification.json](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/actual_exposure_panel_qualification.json):24capability records and1440probe-reader records. L/R8 use exactly identical100-step presentation IDs per seed. Finaldev nominal-order seen records are394/386/392 of400,and finaltest392/390/388 of400 for29/43/71. Nominalcombination false-seen=0. This is a qualification sensitivity,not a newly preregistered primary result or a retraining trigger. State0 has no task exposure,so all actual groups are unseen then.

## 11. Static Figure And Full Maps

[Figure](figures/cross_rule_effects.png),[PDF](figures/cross_rule_effects.pdf),[complete72-pointCSV](figures/cross_rule_effects.csv),[origins](figures/SOURCES.md),[small curated payload manifest](figures/payload_manifest.json). Figure uses all registereddirectseed/state/eta/fullhalf combinations,five-source means,zero line,qualified markers,noCI/no bestscale. Complete4320source×rule×novelty×state/scale cells stay in [native map](/data/250010109/MoE_Router/experiments/20261010_a17_projection_full/runs/full_20261009T171339Z/descriptive_effect_cells.json); they are dependent cells. Failed source/numeric eligibility remains visible and cannot be rescued by average signs.


## Completed authorized SAE execution and finalization recovery: 2026-10-10

**Purpose / hypothesis.** Finish the existing analysis scope and test whether the last S7 failure is an inconsistent summary reduction rather than missing native measurement. This is engineering qualification; no new scientific hypothesis, feature selection or causal interpretation is introduced.

**Setup and controls.** Preserve the original GPU64-condition output, all matrices/gradients/SAE codes/native endpoints, original failed jobs, and2e-5 endpoint/gradient plus4e-5 delta caps. A06 records the post-result numerical repair. The separate CPU recovery unifies array-backed summary means as NumPy float64, with exact equality in the validator rather than increased tolerance. Four regression tests cover cancellation, changed summaries, altered arrays and nonfinite/invalid input.43 source/config/protocol bindings pass. All275 original exported members are hash-identical before and after recovery; the new export has276 members including explicit lineage.

**Data / evaluation.** No training data were consumed and no model/SAE was retrained. Existing list discovery120/heldout120, full dev800 and all frozen DCLM windows remain unchanged. The nine Qwen states are seeds29/43/71×updates0/16/100. Eight original states and S7 list retain their archived20-row native-versus-tail qualification; the recovered Qwen71/update100 state directly qualifies all120 heldout recipients. These readers must remain distinguished. Original Qwen71 tail failure and one S7 chunk failure remain failed diagnostics.

| Stage | Actual completed scope | Current engineering evidence |
|---|---|---|
| Main E03 learner |6 trajectories;42 saved checkpoint members;96/96 gates|Existing Full unchanged|
| Frequency learner |126 trajectories;504 saved members;1,520/1,520 gates|Existing Full unchanged|
| Matching Qwen SAE |244,380 updates;1,000,002,960 valid prediction positions;15 trainer gates|Existing Full unchanged|
| Qwen list SAE analysis |9 states×80 matrix settings/960 interventions|8 archived reader states plus one registered native recovery|
| S7 list SAE analysis |1 state;40 matrix settings/480 interventions|Archived complete branch; no S7 SAE training|
| S7 native DCLM |64 conditions;16 matrices;4 source-gradient checks|GPU measurement plus CPU finalization;320 exact mean checks|
| Frequency endpoint SAE description |36 pairs;28,800 records|Existing completed registered output|

**Result / provenance.** The [completion audit](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/completion_audit_20261010T1048Z.json) freshly verifies4,549 unique file hashes and142 selected registered output IDs. It also checks exhaustive matrix/intervention tuples, recipient identities, signed and endpoint SAE arrays, finite values, no-op/restoration and applicable native caps. [Prerequisite Smoke/save checks](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/prerequisite_and_save_counts_20261010T1051Z.json) preserve64/64 learner Smoke,56/56 frequency Smoke and21/21 repaired SAE Smoke. No expected authorized condition or required saved member remains missing.

The failed jobs `pt-8bnbcqqj`, `pt-azc2zkl5`, `pt-czzk7rb3` and `pt-f9dhsb6w` keep their historical states. The composite qualified result is not a rewrite of any failed job to SUCCEEDED. Two original S7 linear means differed by3.4106e-12 and5.4570e-12 under GPU/NumPy float32 reductions. Recomputing all array-backed means in float64 changes any recorded mean by at most7.8528e-11. [Recovery lineage](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/payloads/s7_native_dclm/summary_recovery_lineage.json) records every correction; original arrays are unchanged. Exhaustive post-registration validation passes. Registrar bookkeeping was moved outside the immutable payload with a [byte-preserving relocation receipt](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/registration_bookkeeping_relocation.json).

**Artifact manifest.** Recovered S7 asset: `representation_a17_raw_sae_s7_summary_recovery_20261010t104246z_s7_native_dclm`; [actual registration receipt](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/registration/registration_request_registered_outputs.json). The [current selected access snapshot](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/completion_audit_20261010T1048Z_access.json) covers only the audited output IDs. [Recovered qualification](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/summary.json), [source freeze](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/freeze_manifest.json), [postflight](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_summary_recovery_20261010T104246Z/postflight.json), original GPU [failure log](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/s7_fullseq_recovery_20261010T100922Z/podlogs/a17-s7-native-recovery-20261010t100922z-20261010T101533Z.log) and the completion audit bind code/config/inputs/outputs without new GPU submission.

**Boundary / next decision.** All currently authorized execution and artifact recovery is complete. Reconstruction, replay qualification and numerical accounting do not establish common/private functions, atom causality or expert utility. Scientific mechanism judgment and question closure remain Unknown. Overall interpretation is deferred until discussion with the researcher; no additional experiment is selected here.
