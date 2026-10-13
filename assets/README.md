# Research asset registry

This directory maintains **storage addresses, identities, purposes and access evidence**. It registers **468 entries and 10 project/storage roots** for current sharing/routing/SAE research, original pretrained Qwen3-0.6B assets and the inspected 109 cache. Entries include checkpoint families, revisions, case aliases and prepared formats, not an equal number of distinct datasets. Payloads remain in their original storage.

[中文](README_cn.md) · [Sole machine-readable catalog](catalog.json) · [Historical whole-library access snapshot](checks/2026-10-09_access_v4.json) · [Checker](../tools/check_assets.py) · [Project access](../docs/project_access.md)

[Original Qwen3-0.6B SAE guide](qwen3_0p6b_sae.md) explains its standalone weights,
historical adapters and caches separately from fresh S7.

## Lookup before pausing

1. Select the required asset IDs. For a named address, match that address first. An unregistered asset requires a bounded search of its named owner/cache and source metadata; absence from the catalog is not evidence that the file is absent.
2. Run a current check of the required IDs. Do not rely on an old snapshot or directory name. `--list` only lists identities and cannot qualify access.
3. Before using contents, bind the parent checkpoint, layer/tensor interface, data revision/splits, field definitions and actual loader. Strict success qualifies registered read/list conditions, not complete downloads, content hashes, runtime loading, contamination freedom or experiment approval.
4. On failure, inspect registered locations, original manifests/configs, actual mounts/symlinks and the project-access legacy resolver. Register alternatives only after verifying identity. Do not guess-replace `/data/share` with `/mnt/bucket`, switch models or switch datasets.
5. If a required asset remains missing, unreadable, known-incomplete or fails loading, **pause dependent work** and report its ID, exact paths, error, time/user context and attempted locations. Optional auxiliary failures do not block unrelated work. Do not independently download, retrain or recreate missing assets.
6. Once access/identity are sufficient, continue the original authorized task. Availability, saved states or execution completion grant no new training/scientific approval.

```sh
python tools/check_assets.py --list --category model_checkpoint
python tools/check_assets.py --strict \
  --asset model_s7_fresh_lambda0p1_33b \
  --asset sae_fresh_s7_33b_embedded \
  --asset eighttask_audited_data
python tools/check_assets.py --project from-attention-to-search \
  --output /tmp/assets-access-NEW-TIMESTAMP.json
```

The checker performs stat, one-byte reads, directory traversal/listing and registered probes. It does not deserialize tensors, decode entire datasets, hash GB payloads, use a network or run a GPU. New snapshots refuse overwrite. Strict exit codes: 0 means selected required access passes; 1 means unresolved selected dependencies; 2 means ID/config/command error. An unknown ID calls for lookup rather than an absence claim.

## Current access and core assets

Checked **2026-10-09 16:03:00, Asia/Shanghai, effective UID 0**. All 10 roots and 150 of 151 registered asset addresses/required probes were accessible in this context. **Nine entries are metadata-only, one model download is incomplete, and one historical exact-SFT dataset is missing**; these 11 entries do not qualify as data/weights in strict mode. Project checks cover entrypoints, not whole repositories or permissions on another host/user/GPU pod.

The tables below provide navigation; detailed identities, revisions, probes and claim boundaries remain in the catalog and original owners.

| Project/storage | Address | Observed access |
|---|---|---|
| `research-system` | `/data/250010109/Research_System` | entrypoint accessible |
| `from-attention-to-search` | `/data/250010109/Research_System/Projects/from-attention-to-search` | entrypoint accessible |
| `router-representation-coupling` | `/data/250010109/Research_System/Projects/router-representation-coupling` | entrypoint accessible |
| `diffusion-language-models` | `/data/250010109/Research_System/Projects/diffusion-language-models` | entrypoint accessible |
| `decommon-router-training` | `/data/250010109/Research_System/Projects/decommon-router-training` | entrypoint accessible |
| `decommon-router-evaluation` | `/data/250010109/Research_System/Projects/decommon-router-evaluation` | entrypoint accessible |
| `kv_cache` | `/data/250010109/Research_System/Projects/kv_cache` | entrypoint accessible |
| `academic_writing` | `/data/250010109/Research_System/Projects/academic_writing` | entrypoint accessible |
| `moe-router-execution` | `/data/250010109/MoE_Router` | entrypoint accessible |
| `shared-data-cache` | `/data/share/109_cache_dir` | entrypoint accessible |

| Asset ID | Object | Address |
|---|---|---|
| `model_s7_fresh_lambda0p1_33b` | model_checkpoint | [token_033000000000](/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000) |
| `sae_fresh_s7_33b_embedded` | sae_checkpoint_embedded | [state.pt](/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000/state.pt) |
| `model_dense_33b` | model_checkpoint | [token_033000000000](/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090/milestones/token_033000000000) |
| `model_sall_unit_weight_33b` | model_checkpoint | [token_033000000000](/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/sall_unit_weight_continue_from_23b_8x5090/milestones/token_033000000000) |
| `sae_fresh_s7_step_zero` | sae_initial_checkpoint | [step_zero_sae.pt](/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/analysis/step_zero_sae.pt) |
| `model_qwen3_0p6b_base` | pretrained_hf_model | [Qwen3-0.6B-Base](/data/share/Qwen3-0.6B-Base) |
| `model_qwen3_0p6b_base_official_a5` | historical pretrained parent | [Qwen3-0.6B-Base-official](/data/250010109/model_cache/Qwen3-0.6B-Base-official) |
| `sae_qwen3_0p6b_e16_layer27_final_1b` | standalone SAE on layer27 MLP input | [sae_full_final.pt](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt) |
| `model_rrc_a3_a_endpoint` | model_checkpoint | [token_001999896576](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/runs/formal_coupled/milestones/token_001999896576) |
| `model_rrc_a3_b_endpoint` | model_checkpoint | [token_001999896576](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/runs/formal_router_input_detached/milestones/token_001999896576) |
| `representation_probe_33b_three_model` | representation_cache | [dense_33b](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/probe_33b_01/dense_33b) |
| `representation_common_rule_controlled_0927` | representation_cache | [full_h100_20260928T010310Z](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z) |
| `representation_retention_smoke_1007` | representation_cache_smoke | [20261007T145134Z](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/runs/20261007T145134Z) |
| `adapter_checkpoint_retention_smoke_1007` | adapter_checkpoint_smoke | [20261007T145134Z](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/runs/20261007T145134Z) |
| `dclm_token_bins_global01` | dataset_token_bins | [global-shard_01_of_10](/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10) |
| `dclm_pair_v1` | dataset_training_view | [dclm_pair_v1](/data/250010109/training_data_views/dclm_pair_v1) |
| `dclm_raw_holdout_global02` | dataset_raw_compressed | [shard_00000000_processed.jsonl.zst](/mnt/bucket/109_cache_dir/hf_data/dclm_eval_holdout/global-shard_02_of_10/local-shard_0_of_10/shard_00000000_processed.jsonl.zst) |
| `eighttask_audited_data` | dataset_training_tensor | [data](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/data) |
| `m2d2_n8_v1` | dataset_prepared_panel | [N8_v1](/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit/data/N8_v1) |
| `ntp_statistics_panel_2048` | dataset_prepared_panel | [data](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/data) |
| `data_rrc_a3_locked_analysis_documents` | locked_analysis_dataset | [analysis_documents.jsonl](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/inputs/analysis_documents.jsonl) |
| `shared_109_cache_root` | shared_cache_root | [109_cache_dir](/data/share/109_cache_dir) |

The fresh-S7 and Dense/SALL checkpoint families register only actual milestones. Planned 35–50B configurations do not prove files exist. A mutable latest pointer does not replace an exact checkpoint identity.

## Shared cache and incomplete entries

`/data/share/109_cache_dir/hf_data/hub` contains 42 dataset repo aliases and one Qwen2.5 tokenizer repo; `hf_data/datasets` contributes 39 prepared Arrow entries. Registered families include GSM8K, MMLU, HumanEval, MBPP, ARC, HellaSwag, PIQA, RACE, LAMBADA, SocialIQA, CommonsenseQA, Winogrande, SciQ, OpenBookQA, IFEval, UltraChat/UltraFeedback, Tulu, Magpie, Orca-DPO, Magicoder, Code-Feedback, MetaMathQA and OpenHermes. M2D2/PAWS/P_rel and eight-task prepared assets are separately registered from execution storage.

Actual revisions, refs, representative files and prepared paths are recorded. No upstream-completeness claim is made. Case aliases, legacy revisions and Arrow configurations retain their exact paths.

DCLM has 2,420 uint32 bins totaling about 1.21 TB. The paired view excludes one validation shard from its 2,419 training shards. Original compressed holdout is on `/mnt/bucket`; the same `/data/share` candidate is absent and cannot silently replace its identity.

| Asset ID | Boundary |
|---|---|
| `hf_hub_magpie_align_magpie_qwen2_pro_200k_chinese` | `METADATA_ONLY` |
| `hf_hub_allenai_social_i_qa` | `METADATA_ONLY` |
| `hf_hub_derek_thomas_scienceqa` | `METADATA_ONLY` |
| `hf_hub_m_a_p_coig_cqia` | `METADATA_ONLY` |
| `hf_hub_piqa` | `METADATA_ONLY` |
| `hf_hub_social_i_qa` | `METADATA_ONLY` |
| `hf_hub_tatsu_lab_alpaca` | `METADATA_ONLY` |
| `hf_hub_ybisk_piqa` | `METADATA_ONLY` |
| `hf_prepared_web_of_science` | `METADATA_ONLY` |
| `qwen3_next_80b_incomplete` | `INCOMPLETE` |
| `data_qwen3_0p6b_senior_exact_sft_legacy_missing` | `PAYLOAD_MISSING`; original external path unavailable, no identity-preserving replacement established |

Qwen3-Next-80B has eight `.incomplete` files and is not registered as complete weights. The evaluate/metrics/modules/NLTK caches are directory-only inventories with runtime dependencies unverified.

## Preserve these distinctions

- S7 is an eight-layer, hidden-1024 model with final Attention-output SAE embedded in `state.pt`; SALL has eight SAEs. Original Qwen3-0.6B is 28-layer. A3 is a separate 12-layer, hidden-512 MoE with no SAE. A random initial SAE is not a trained feature tool.
- In the 1003 cache, `c` is projection input, `a` projection output, `r` native incoming residual and `e` the loss gradient w.r.t. `a`, not SAE reconstruction error. Different model coordinates are not aligned by registration. 0927 displacement is a virtual matrix update; 1007 readouts follow actual short adapter training.
- Eight-task internal splits include official-test-origin data; existing natural panels are exposed. Availability does not create fresh confirmation evidence. M2D2 `math.AG` in N8 differs from legacy `math.AP`. A3's locked panel exists; TEST/function analysis remains NOT_RUN.
- The 0927 worker still hardcodes a moved daily helper. Its verified relocated path/small-source identity is recorded. Saved arrays remain readable; rerunning the worker requires a reference repair without rewriting history.

## Training and analysis lifecycle

### Before training, resume or analysis

Use the lookup procedure above for the **inputs actually needed by this stage**.
Record their stable asset IDs in the Protocol/config or analysis input manifest:
parent model, tokenizer, data view/splits, and any fixed SAE, adapter or saved
representation. For an adapter or embedded SAE, include its required parent
checkpoint. Match the exact layer, tensor location, preprocessing and loader;
equal hidden dimensions do not make different checkpoints or hooks compatible.
An old access snapshot cannot replace the current check. Reading a report or
inspecting job status alone does not require loading all of its raw assets.

The training Protocol/config must name where the final checkpoint and required
milestones will be saved. The authorized implementation saves them in the
execution run directory. A weights-only export and a complete resumable training
state are separate objects; declare which is required rather than implying that
every saved weight file supports exact continuation.

### After training saves a checkpoint

Register actual saved outputs before closing the artifact handoff. Do this for
authorized Smoke as well as formal training, retaining their different purposes.
Use a stable ID for the selected final/reusable checkpoint. A family entry may
enumerate all other actual milestones through an explicit member list or saved
manifest; a planned budget or mutable `latest` pointer is not a member identity.
Do not replace an earlier version with a new run under the same ID.

| Information to register | Concrete record |
|---|---|
| Object and physical access | Category/kind, absolute saved files, required payload probes, `payload_status`, original storage owner |
| Producer | Protocol path/revision, run/job ID when available, actual code/config and source manifest |
| Required inputs | Parent model/adapter/SAE IDs, tokenizer and data view/split identities; historical backfills may name external paths pending registration, which is not an input-check exemption |
| Model/SAE interface | Architecture, exact layer/tensor or state key, adapter insertion, SAE dimensions/TopK/preprocessing, and actual loader source |
| Reached progress | Saved optimizer step and actual valid-token count, counting definition and evidence; do not substitute the planned budget |
| Identity and verification | Manifest-recorded digests/size and their source; identify copied digest evidence versus freshly verified evidence, leaving unavailable fields `Unknown` |
| Resume capability | State actually saved: weights, optimizer/scheduler, RNG, counters and data position; loader/resume evidence or `NOT_CHECKED` |
| Use boundary | Engineering Smoke, random initial state, trained endpoint or partial output; evidence availability is separate from scientific eligibility |

Fields apply to the actual object: use `NOT_APPLICABLE` for inapplicable fields,
`Unknown` for missing evidence and `NOT_CHECKED` for verification not performed.
Before future payload use, register any required historical input without an ID
and check it through the lookup procedure.

These fields belong under each entry's existing `identity`, `source_paths`,
`locations`, `notes_cn` and `payload_status`; this is not another catalog schema.
Keep embedded SAEs tied to their model state and standalone SAEs tied to their
training parent/interface. Keep adapters tied to the base weights needed to load
them. Register reusable saved representations/SAE features with producing model,
SAE, data split and tensor/field definitions when analysis produces them.

Run a current check of the new output IDs and save a **new** access snapshot in
`checks/`. Link the IDs and snapshot from the run's artifact manifest/Detailed
record. Registration neither requires another training run nor a GB-scale hash
or GPU load: preserve existing verification evidence and label what was not
checked. Payloads remain at their execution/storage addresses, not in Git.

If saving or access failed, preserve the failure and register only the actual
partial output with its limitation; use `INCOMPLETE`/`PAYLOAD_MISSING` when
applicable. Do not label a checkpoint saved or resumable from a job-success
message. Do not rerun, download, or change the scientific verdict to complete
the catalog. Report the missing checkpoint as an unfinished artifact handoff.

## Maintenance

`catalog.json` is the sole address/identity register; README owns this procedure; `checks/` stores dated observations. Record ID, category, purpose, associated projects, absolute locations/required probes, parent model/data versions, manifests/loaders and known gaps. `projects` is association; `required_projects` denotes actual access dependencies. Optional paths are auxiliary, not automatic replacements.

Register new versions separately or append reasoned corrections. Save new access snapshots without overwriting old ones. The first `2026-10-09_access.json` misclassified three JSON payload locations as metadata; catalog amendments preserve the correction and its historical v2 snapshot. Qwen asset backfill is in v3; v4 explicitly checks all ten roots and all 151 entries and is the current whole-library snapshot.

This library stores small metadata/evidence, not TB datasets, weights or representation payloads. Git access does not grant physical payload access. Original Anchors/Protocols/Summaries retain scientific and execution authority.

After registration, update the affected reading guide and current-snapshot link;
derive any entry counts from the catalog and state the snapshot's actual scope.
Do not rewrite earlier snapshots or move independent execution assets merely to
keep the index tidy.

[A17 list-rule release and Smoke assets](a17_list_rules.md): newly generated dataset; scoped access checks do not replace the dated whole-library inventory.

## A17 actual additions (2026-10-10)

Six E03 native Full families with42 actual milestones and126 frequency Full families with504 actual milestones are registered, together with their engineering Smoke outputs and versioned analysis selectors. Current checks cover selected IDs, not all historical assets; the old whole-library snapshot cannot qualify these additions.

[E03 access check](checks/2026-10-10_a17_outputs_20261009T173255Z.json) · [Frequency access check](checks/2026-10-10_a17_outputs_20261009T175342Z.json) · [SAE selector v2 check](checks/2026-10-10_a17_outputs_20261009T174031Z.json). Resume evidence, actual member hashes and required parents remain in the catalog/execution receipts; an adapter directory is not a standalone LM.

The matching raw `o_proj` SAE completed its authorized 1B-valid-position Full. Existing E16 remains the MLP-input dictionary; the new dictionary has a separate asset identity and does not replace it.

The first matched raw-output SAE Smoke (`pt-8bnbcqqj`) failed byte-exact weight/optimizer resume. Six actual SAE/recovery outputs are registered with overall engineering FAIL and scientific NOT_EVALUATED; access passes do not qualify them as a 1B dictionary. [Failure output receipt](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/smoke_20261009T174900Z/registration_request_failure_schema_fixed_registered_outputs.json).

The repaired SAE Smoke (`pt-cr4i6ge9`) succeeded with 21/21 checks and independent byte-exact review. Ten actual weights/recovery assets (including permanent steps 60/61) pass current access and 14 file SHA checks. [Actual Smoke output receipt](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/smoke_fix_20261009T1810Z/registration_request_enriched_root_bound_registered_outputs.json).

Full `pt-h5t3h09w` succeeded at 244,380 updates: 1,000,002,960 valid prediction positions, 1,000,980,480 raw activations, and 999,025,471 eligible SAE positions. Asset `sae_a17_qwen_raw_o_proj_1b_valid_full_20261009t182142z` registers the final dictionary and three actual milestone weights; two recovery states have separate checkpoint IDs. All three IDs pass [current selected access](checks/2026-10-10_a17_outputs_20261009T210301Z.json), and seven payload/manifest SHA checks passed. The [registration receipt](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/full_20261009T182142Z/registration_request_enriched_root_bound_registered_outputs.json) binds the actual job, 15 trainer gates, complete 246-point telemetry, and native saved counts. The 100M/300M milestone eligible counts were not recorded; their raw counts are contract-derived. Full did not execute a continuation. Analysis remains pending; access and reconstruction qualification do not establish functional specialization.


### A17 analysis outputs recovered on 2026-10-10

Current storage/access facts: `pt-h6ke4emg` completed all36 frequency endpoint pairs/28,800 records, registered as `analysis_a17_frequency_sae_actual1b_36pairs_20261009t2118z`. The preceding training report's analysis-pending statement is historical. Original main-SAE job `pt-azc2zkl5` actually FAILED and remains failed. Eight complete Qwen states, S7 list, and the incomplete Qwen71/u100 branch (104/960 interventions) are registered in five scoped representation entries; partial-input access does not qualify complete results. New native-gradient/replay recovery has not yet completed real GPU measurement.

[Five scoped old-job registration receipts](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/provenance/recovery_registration/root_registered_request_index.json) · [Frequency endpoint selected access](checks/2026-10-10_a17_outputs_20261010T093323Z.json). These checks cover selected additions, not a fresh whole-library inventory. Byte integrity, native measurement qualification, SAE reconstruction and functional explanation remain separate.


### A17 current analysis completion

All authorized analysis branches are now engineering-complete and registered; old failed jobs keep their states. S7 reuses its embedded SAE;64 native conditions passed separate CPU summary-finalization recovery. New asset `representation_a17_raw_sae_s7_summary_recovery_20261010t104246z_s7_native_dclm`, [current selected output access](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/completion_audit_20261010T1048Z_access.json) and [completion audit](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/completion_audit_20261010T1048Z.json) bind the completed evidence. This is not a whole-library inventory. Earlier analysis-pending preparation entries are historical; scientific mechanism judgment remains Unknown.

### A17 paired-rule margin output (2026-10-10)

Registered actual analysis asset `representation_a17_paired_rule_margin_20261010t141041z`:7 states,280 finite conditions,60 paired lists per condition;330 input/642 output hashes verified. All18 primary updates help recipient CE,but12 pair margins improve and6 worsen;frozen descriptive verdict heterogeneous/insufficient,mechanism/closure Unknown. [Registration](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/registration_request_registered_outputs.json) · [Selected access](checks/2026-10-10_a17_outputs_20261010T144031Z.json).

### A17_03 actual sequential outputs (Asia/Shanghai2026-10-11)

Registered40actualcheckpointfamilies(16Smoke,24Full)plusone native-readout/parameter-subspacefamily,44Smoke/114Fullstates. Parent,data,source,valid-answercounters andmemberhashesare bound inreceipt;registration confers no mechanism judgment. [Receipt](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/registration_request_registered_outputs.json) · [Selected access](checks/2026-10-10_a17_outputs_20261010T172742Z.json).

2026-10-11 A17 component-analysis outputs: [current selected-access check](checks/2026-10-11_a17_component_causality_outputs_0233.json) covers exactly the new Smoke and Full readout families. Both are accessible; this is not a whole-library refresh. Smoke140 cells and Full630 cells, no new trained checkpoints.


### A17 trajectory-state analysis completed (2026-10-11)

Smoke12/replay4 and Full108 actual finite readouts are registered, no new trained checkpoints. [Current selected access](/data/250010109/Research_System/assets/checks/2026-10-11_a17_trajectory_20261011T090921Z.json) covers these two output IDs only. [Canonical Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_03_old_task_sensitive_update/A17_03_E03_trajectory_mechanism/summary_cn.md) preserves state/order heterogeneity and incomplete100-step mechanism boundary.

### A17_04 conditional mapping completed (2026-10-11)

Smoke and Full saved 120 actual states in 28 adapter families and two native-readout families. Derived analysis `analysis_a17_04_mapping_20261011t095038z` has a separate identity. [30-output access](checks/2026-10-11_a17_mapping_output_access.json) and [derived-analysis access](checks/2026-10-11_a17_mapping_analysis_access.json) pass selected checks, not a fresh whole-library inventory. [Canonical Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/summary.md) records insufficient old-mapping acquisition; completion does not establish acquired-rule interference. Checkpoints require the exact registered parent Base.

### A17_04 old-rule acquisition diagnosis (2026-10-11)

E02 registered one derived TRAIN/DEV dataset,20 actual adapter families (30 Smoke states and40 Full states), and two native readout/analysis families. [Selected29-asset delivery access](checks/2026-10-11_a17_acquisition_delivery_access.json) covers these outputs and required inputs, not a fresh whole-library inventory. [Canonical Summary](../Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/summary.md) separates the two qualified acquisition routes from the still-unanswered transfer question. [Delivery manifest](../Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/artifact_manifest.json) binds actual receipts, checkpoints, native predictions, independent tensor checks and numerical boundaries. Model states require the exact Base; actual Full continuation was NOT_RUN.


### A17_04 single-layer acquisition reduction test (2026-10-11)

E03 registers eight actual adapter families (12 Smoke states and16 Full states), plus two native readout/analysis families. [Selected14-asset delivery access](checks/2026-10-11_a17_single_attention_delivery_access.json) covers these outputs and four required inputs/references, not a whole-library inventory. Full independent CPU tensor/optimizer/counter verification and34native readout files pass; all36 frozen source/contract-snapshot/config/data/parent files remain byte-identical. [Canonical Summary](../Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/summary.md) records single-layer AdamW sufficiency and the tested SGD package's failed qualification. [Delivery manifest](../Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/artifact_manifest.json) binds actual saves and receipts. Adapter loading requires the exact Base; Full continuation was NOT_RUN. No new-mode transfer or mechanism result follows from this prerequisite test.

### A17_04 qualified single-layer mapping transfer (2026-10-12 Shanghai)

R02 registers twelve adapter families and four native analysis/readout families across Smoke and Full. Full saved 72 actual states across nine branches; these are adapters requiring the exact registered Base. [Full output access](checks/2026-10-11_a17_transfer_20261011t160256z_full_outputs.json) records selected lifecycle checks. [Canonical Summary](../Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary.md) separates consistent/reversed sequential transfer, joint-learning feasibility and 34 local optimizer interventions. Full within-branch external continuation was NOT_RUN. [Daily reading handoff](../daily_research_reports/1012/a17_mapping_transfer/handoff_report_cn.md) provides portable steps and results without checkpoint payloads.


[CrossCoder phase-one saved cache and analysis](crosscoder_feature_phase1.md): final14-layer completeVAL; selected graphs,texts,heatmaps and scoped current access. No causal or learning-benefit conclusion.
