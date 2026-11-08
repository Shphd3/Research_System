派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/execution_record.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/execution_record.md)；研究修改仍回到原件。

---

# Execution record: R01 expert allocation

[Protocol](protocol.md) · [Chinese](execution_record_cn.md) · [Three-part audit](audit_review.md)

## Submission fact — 2026-11-06T16:17:35.445885+00:00

**Job `pt-ds9bdaxb` was accepted for scheduling at 2026-11-06T16:15:07Z. GPU allocation, smoke success and training completion have not yet been verified.** Submission is an execution fact, not a scientific result. Scientific acceptance and mechanism judgment remain Unknown.

The [actual submission receipt](../../../../../../../../UNAVAILABLE.md) has status SUBMITTED, exit_code0, and the platform text “submitted successfully, please wait for scheduling”. Its SHA-256 is `9e7dcef3cb0efbff23ffbe8f6617f5273ea88c2c0d74cd597854ccf7405ab7ed`. The requested resource tuple is envelope profile `h100-4-reserved`: one node, four H100 GPUs/processes, worker spec `n6ls.iu.i40.4`, reserved quota, current default `shphd-lite-0911` image. This is a requested tuple; device identity must come from the running pod.

The authorized entry embeds joint A/B smoke, save/reload/external-process replay, an immutable common-budget/frequency freeze, formal A/B training and complete evaluation. The current user authorized the full bounded scope. Passing smoke remains an engineering gate rather than a result or a request for repeated approval. No C/second seed is scheduled. A queued job alone does not satisfy the user's start requirement.

## Verified construction before submission

[Actual parameter ledger](../../../../../../../../UNAVAILABLE.md) and [machine accounting](../../../../../../../../UNAVAILABLE.md) enumerate the isolated adapted model. A uses `[8,8,8,8,8,8,8,8]`; B `[6,6,6,8,8,10,10,10]`; both have 64 experts, residual width1024, intermediate width1536 and top-2. Every layer has E>k. Each expert has4,718,592 parameters; total experts301,989,888 and routers65,536 in both arms. The unique full-model total is507,988,992; all are trainable. Tied embedding/head count once. Per-layer attention including QK normalization is6,291,712; block norms2,048. Layer numbers in the execution CSV are zero-based; the readable report uses one-based numbers.

The [initial tensor hashes](../../../../../../../../UNAVAILABLE.md) support common-start verification; a CPU check found242 common same-shape tensors and42 overlapping rows across6 differing router shapes equal. This audit does not establish finite GPU training or exact continuation.

The [data manifest](../../../../../../../../UNAVAILABLE.md) has SHA-256`3c0dc6748978ca190ba3334d77799ead1f485da3e1a242d2e4c579d940769ace`; its [small byte-preserved copy](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/data_manifest.json) records the actual source. It scans a deterministic67,108,864-token prefix, recovers boundary-delimited documents, discards8,827 fragment/short tokens and removes16 exact duplicate documents. Train/dev/test are53,813/528/544 documents and65,766,910/630,980/700,308 token IDs. Final predicted positions are700,307. Split uses exact document-byte SHA-256 modulo100, with dev0/test1/train2..99. Near duplicates are NOT_CHECKED; the source prefix is not the full corpus. Full dev/test overall NLL is the general validation; the old115M holdout is NOT EVALUATED.

Current [prepared-input access evidence](../../../../../../../../UNAVAILABLE.md) is distinct from later checkpoint-output registration. Source review and meeting attribution are in[source_review.md](source_review.md). Test metadata/examples have been inspected; final-test model metrics have not selected the design.

## Freeze, evidence and eligibility

Protocol English SHA-256`bdb407cc750afb2ca8920755be364886a59fdaf33f0bcd8e6a0099130d966820`; Chinese SHA-256`04ca3d5cac3216701399402385a2576852b8278093a160efa0dc7baca4485585`. The actual common steps, thresholds and runtime hashes remain pending the successful joint smoke/freeze receipt. Smoke and formal frequency files have separate directories. They are not inferred from this submission record.

No measured losses, trained checkpoints, finite gradients, route-load acceptance, save/replay success, throughput, ETA or allocation are claimed here. The next operational action is to inspect this same job's durable startup evidence. Later entries append actual state and preserve any failed attempt; they do not rewrite the frozen scientific plan.

## Verified GPU entry — 2026-11-06T16:43:07.344306+00:00

This appended fact supersedes the earlier unverified-allocation state without editing that submission-time history. Job `pt-ds9bdaxb` started its durable pod log at 2026-11-06T16:41:44Z; the execution certificate was verified at 2026-11-06T16:42:23.410039+00:00. The [actual GPU startup record](../../../../../../../../UNAVAILABLE.md) reports four `NVIDIA H100 80GB HBM3` devices, each with 85,017,624,576 bytes, on profile `h100-4-reserved`. The actual runtime is torch `2.3.0a0+6ddf5cf85e.nv24.04`, CUDA `12.4`. Startup-record SHA-256: `73b9eefc8397ade8bde07cd54d6e16256b625e4271187b54f69a6ca3fc5e8c35`.

The [GPU-entry certificate](../../../../../../../../UNAVAILABLE.md) records stage `EMBEDDED_SMOKE_STARTED`, entrypoint `scripts/run_pair.sh`, and the [durable pod log](../../../../../../../../UNAVAILABLE.md). A smoke has launched. This evidence confirms actual entry on the requested four-H100 reserved allocation; it does **not** establish passed smoke, completed training, a frozen formal token budget or a scientific result. Those states remain pending their own receipts. Continue the existing job and append the eventual joint-freeze facts when verified; do not duplicate or resubmit it from this record.

## Joint freeze and actual audit scope — 2026-11-06T17:03:01.834883+00:00

The [joint freeze](joint_freeze.md) records229,113,856 valid targets per arm,874 updates, midpoint437, and formal type-frequency thresholds49/447. Formal training has started; paired endpoint completion remains PENDING_RESULTS.

**Initialization clarification:** the earlier `initial_parameter_hashes.json` used seed17 to qualify the implementation rule. It was not the experiment's actual saved seed20261106 state. The separate [actual initial-state audit](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/actual_initial_weight_match.json), checked2026-11-06T16:59:42.790524Z, has statusPASS for seed20261106, step0/token0:242 shared parameter tensors and252 shared state tensors match exactly, as do overlapping router rows; load bias is zero and optimizer fresh. Different routing candidate sets still produce different initial functions. This appended clarification preserves the earlier evidence rather than relabeling its seed.

The [actual smoke audit](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/actual_smoke_audit.json) reports finite observed A/B updates, exact eligible-assignment counts and identical batch hashes for steps1–3. Each observed smoke ends at step3/786,432targets under a nominal4-step config; these are smoke qualification tokens, not formal training. A's continuous-versus-external-resume state/next-update replay passes with exact floating equality and no tolerance relaxation. A/dev evaluation after reload matches all JSON values and raw document arrays exactly on8 documents/7,331targets. This does not assert an external recovery test for every B/formal checkpoint.

The [matrix profiler check](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/matrix_flops_formula_check.json) measures `aten::mm`2,000,027,648FLOPs/token, exactly matching6×(active_parameters−norm_parameters)+2×tied_output_head for the profiled rank0 smoke update. Fused SDPA QK/AV/backward, other uncounted kernels and communication remain excluded. This is measured matrix work, **not measured total training FLOPs**.

The [actual registration handoff](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/actual_output_registration_handoff.json) records strict-checked assets `checkpoint_family_depth_expert_allocation_smoke_20261106` and `data_depth_expert_allocation_formal_frequency_20261106`,7 saved smoke checkpoint members, and a current strict access snapshot. No formal endpoint/complete analysis is registered by that receipt. Fresh SHA verification sequentially read34,545,588,066bytes of smoke states around16:55–16:58UTC while formalA was beginning. A systems timing effect from this outside I/O workload was not measured; preserve the boundary when comparing throughput/wall time. It did not change token order, updates or budgets.

The [sample-review timing record](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/sample_review_timing.json) distinguishes pre-formal text/boundary inspection and automatically generated bucket examples from the explicit Codex reading of individual bucket cases after formalA began (about67Mtargets). External human review is NOT_PERFORMED. No threshold/configuration changed after that reading, and no model metric selected cases. This timing deviation must remain in the final report; do not claim complete manual bucket review preceded formal training.

## Full paired completion and independent checks — 2026-11-06T18:01:45.591163+00:00

A completed2026-11-06T17:22:01.217476Z and B17:53:43.402712Z, each874updates/229,113,856valid targets. Pipeline COMPLETE at17:54:07Z and platform SUCCEEDED are verified. All874batch hashes match;12planned evaluations and final numeric/source/statistical/formal-initial audits PASS. Formal A/B checkpoint families and analysis assets are registered/strict PASS.

Final low B−A is+0.2172100729108415,95% interval[+0.12596861910824345,+0.30035089638778223]; overall+0.014258167152949142[+0.006159870644017267,+0.0256768969077061]. No low-frequency benefit appeared and overall is worse; causal/mechanism judgment remains Unknown. Complete evidence, contrary examples, own-low-curve worsening and timing/FLOP limitations are in[Summary](summary.md)/[Detailed](detailed.md). This append does not alter Protocol or close the question.

## 2026-11-06T18:06:31.028556+00:00 — Final paired completion / 最终成对完成

Job pt-ds9bdaxb is SUCCEEDED with durable pipeline COMPLETE. Both arms reached 874 updates and 229,113,856 valid targets; all initial/midpoint/endpoint full-state saves and DEV/TEST evaluations exist. All 874 actual input/target/mask hashes match. Final numeric, independent statistics, frozen/legacy source and actual formal-initial audits passed. Formal A/B checkpoint families and analysis are registered with current strict PASS; see the [Summary](summary.md) and [artifact manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/artifact_manifest.json). Earlier PENDING entries describe their original timestamps rather than the current execution state.

Endpoint B minus A is +0.217210 low-frequency and +0.014258 overall nat/token: no low-frequency advantage in this measured pair. Scientific acceptance, mechanism judgment and question closure remain Unknown; no next training starts automatically. The complete execution certificate is execution-side audit/execution_certificate_completed.json.
