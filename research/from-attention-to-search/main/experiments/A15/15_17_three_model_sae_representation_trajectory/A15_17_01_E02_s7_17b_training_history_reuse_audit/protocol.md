# Protocol: A15_17_01_E02 — S7 17B training-history reuse comparison

## 0. Approval Snapshot

Document state: **APPROVED_FOR_DIRECT_FULL_FROZEN_AUDIT**. Revision `E02-direct-full-v1`, registered 2026-09-22T09:49:21.676604+00:00 before any E02 model extraction or signed contrast. Authority: researcher requests comparison of two named17B checkpoints and full submission; latest explicit instruction supersedes smoke-first planning: “不用执行smoke直接full run”. **Smoke status NOT_RUN_USER_WAIVED, never PASS.** Full execution authorized; stop polling after submission/startup handoff, researcher will request later analysis.

[Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md); [active Focus](../../../../focus/focus_sae_shared_direction_reuse.md). Local purpose: remove the S7-vs-SALL topology confound from the prior comparison and describe whether two same-topology/current-coefficient S7 checkpoints with different histories differ in reuse and native geometry. Primary contrast uses the already confirmed E01 measurement, now **reweighted minus fresh at17B**. No presumed effect direction, causal mechanism approval or equivalence margin is inferred. Role: bounded training-history comparison / robustness audit.

Fixed:192 identical N8 records×256 tokens, native layer8,30000 atoms,K32,mean pooling,paired-record2000-draw bootstrap. Conditions: fresh lambda0.1 throughout versus lambda1→0.1 reweighted. Known residual confounds: microbatch/accumulation partition, CE chunking, historical sampling/RNG/numerical paths. Same nominal effective batch does not establish identical historical updates. Allowed claim: checkpoint-associated difference or unresolved difference only. No new training, conditions, semantic probes, task evaluation, intervention, resource fallback, commit or push.

Execution PASS means all identity/numerical/artifact gates pass, irrespective of sign. Measurement failure => FAIL with scientific INSUFFICIENT. Scientific reporting labels describe the interval sign; they are **not** a new directional mechanism PASS/FAIL rule. User owns final interpretation.

## 1. Terminology

Native write a: attention output after output projection and before residual addition, not reconstruction. Atom: model-local SAE dictionary column; support:32 indices actually selected by native encode for each valid token. Usage u: per-record counts divided by256×32. R: average cosine of record usage profiles; dimensionless, not semantic similarity. Effective dimension: centered covariance participation ratio of native token-mean writes; variance concentration, not semantic capacity.

## 2. Anchor alignment

The prior E0121B S7/SALL association cannot isolate topology or training history. This user-selected within-S7 comparison retains the same reuse construct and eliminates layer-count differences, not all training confounds. It is not a replication at21B, a matched lambda-history intervention or a geometry ablation. E01 results/contract remain unchanged.

## 3. Hypothesis / alternatives

The researcher identifies unmatched conditions as the present uncertainty. The two explanatory possibilities are: different training histories leave a detectable endpoint reuse/geometry difference despite matched present topology/coefficient; or this panel does not resolve such a difference. No sign is assumed. A resolved difference cannot identify which historical component caused it; an interval spanning zero is not equivalence. The original support-versus-decoder-geometry causal question remains unresolved.

## 4. Rivals and scope

Same-ID reuse, decoder-column collinearity, coefficient covariance and reconstruction residual can coexist. This run removes the SALL architecture alternative but does not adjudicate all of them. Historical numerical/SAE token-sampling differences are remaining alternatives; no fresh article or seed independence is assumed.

## 5. Data and provenance

Reuse byte-identical E01 `manifests/full_inputs.json` and `smoke_inputs.json` as provenance only; no smoke will execute. Full panel has192 unique IDs with256 pretokenized body tokens and source_group IDs,48 original batches of4. Hash every input list. Labels were removed and cannot enter model/threshold selection. Historically stratified, previously analyzed observer panel; not untouched confirmation. No filtering, label usage, new training/dev split or result-dependent exclusions. Metadata equality does not prove independent articles. Sources and25 external identity hashes: [/data/250010109/MoE_Router/experiments/20260922_s7_17b_training_history_reuse_audit/manifests/assets.json](/data/250010109/MoE_Router/experiments/20260922_s7_17b_training_history_reuse_audit/manifests/assets.json).

## 6. Task and supervision

Read-only model-native supports and same-pass native means. Both conditions see identical inputs; no labels, optimizer, probe fitting, external SAE, gradients, checkpoint write or task-loss evaluation. No loss schedule is introduced by this audit.

## 7. Frozen models

Fresh checkpoint: `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_017000000000`. Manifest state SHA256 `1f36a216c19b83b2b557d17472cfd9742d65c3605d1895052284b5df59bfda73`.
Reweighted checkpoint: `/data/250010109/MoE_Router/experiments/20260917_attention_output_sidecar_last_reweighted_resume/runs/formal50b_last_attention_lambda0p1_mbs16_fork_4h100/milestones/token_017000000000`. Manifest state SHA256 `7bc999ae269f096b6b209131fd00d3c5167df1c56f5042128fa221f5fbb21a49`.

Both manifests complete, tokens_seen17000000000 and optimizer_step64854; source model/config/SAE/loader hashes identical;8-layer hidden1024 backbone; single block7 sidecar, width30000,K32,current reconstruction weight0.1,AuxK1/32. The audited run records share seed17 and identical initial full/backbone parameter hashes. The checkpoint loader independently verifies manifest state integrity before GPU use. No new model inferred from a filename.

## 8. Training history boundary

No training occurs here. Both resolved training contracts have world_size4 and nominal262144 tokens/update. Fresh microbatch32/accumulation1/CE chunk128; reweighted16/2/256. Reweighted fork records lambda1→0.1 at15465567744 tokens (step59000), optimizer continuation and repartitioned data cursor. Data manifest/tokenizer match; exact training sequence, sampled SAE positions and floating-point update identity have not been replayed. The audit must not call this a strict coefficient-only ablation. Detailed differences: [/data/250010109/MoE_Router/experiments/20260922_s7_17b_training_history_reuse_audit/manifests/training_lineage_audit.json](/data/250010109/MoE_Router/experiments/20260922_s7_17b_training_history_reuse_audit/manifests/training_lineage_audit.json).

## 9. Conditions, seed, resources

Two fixed17B conditions only, no checkpoint sweep. Observation RNG20260922. Same ongoing audit resource tuple:5090-4-spot,one node,four independent workers,shphd-lite-0911 image with existing torch2.8.0+cu128 SM120 layer. Workers0/2 fresh,1/3 reweighted; each96 records/24576 tokens in24 original batches. Worker deadline900s after application launch. No replacement resource or automatic retry; failures preserve artifacts and stop.

## 10. Primary analysis

For each example i: u_ij=sum_t1[j in S_it]/(256×32). All selected values must be strictly positive under the inherited eligibility guard. R averages cosine(u_i,u_q) over distinct sample-position pairs. DeltaR=R_reweighted−R_fresh. Use2000 paired draws of192 record indices with replacement,seed20260922; include duplicate originals at distinct resampled positions; percentile95%CI. Use the inherited tested Gram-index implementation, no popularity correction, no cross-model ID alignment.

Reporting rule (two-sided descriptive convention, no new directional scientific hypothesis): CI low>0 => REWEIGHTED_HIGHER_REUSE; CI high<0 => FRESH_HIGHER_REUSE; otherwise UNRESOLVED_REUSE_DIFFERENCE. Invalid identity/nonfinite statistics => INSUFFICIENT. A boundary exactly zero is unresolved. No equivalence or minimum meaningful-effect claim. One primary contrast, no multiplicity selection or outlier trimming. Do not force the old E01 directional necessary-condition label onto this new pair.

## 11. Geometry, secondary diagnostics and guards

Native mean a_i from the same forward/token mask as supports. Compute centered d_eff=tr(Sigma)^2/tr(Sigma²); report both and reweighted−fresh point difference **separately**, with no invented dimension CI or sign gate. Report global distinct/effective atom counts and cumulative frequency/native variance lines, not bars. No mechanism conclusion follows from either sign. Secondary diagnostics cannot override the primary interval.

All4 workers check checkpoint/site/dictionary identity, native support positivity/uniqueness, input/mask alignment, native-vs-prefix32 ties, same native encode repeatability, full state version/fingerprint immutability and CPU/GPU FP64 statistic agreement≤1e-9. There is no17B reference cache: repeat the identical forward and require pooled native means exactly equal, rather than comparing to21B native values. Full aggregation recomputes serial counts exactly and verifies ordered IDs/hashes/all256 positions/dictionary hashes per model across shards. No smoke-overlap receipt may be fabricated.

## 12. Known-good/bad/confusing cases

Unit checks: atom permutation invariance, identical/disjoint usage, usage normalization, shard concatenation with global row offsets, covariance/Gram PR equality, bootstrap reversal, all interval sign and invalid-statistic branches, scalar/BF16 fingerprint. High cosine with high dimension is a valid observation; low dimension with unresolved cosine does not mean equivalence. Zero selected activation or repeat-forward mismatch stops instead of dropping samples.

## 13. Stage contract

| Stage | Input/operation | Why / output | Stop |
|---|---|---|---|
| F0 | frozen contracts,files,model manifests and input hashes; enforce explicit smoke waiver | identity receipt records NOT_RUN_USER_WAIVED | identity drift |
| F1 | four native full-panel workers; repeated same-input forward | qualified support/mean NPZ and4 receipts | any failure/nonfinite/mutation/timeout |
| F2 | merge and align both conditions,hash and serial-count checks | ALIGNED_FULL_PANEL_PASS | mismatch; never exclude a record |
| F3 | fixed metric/bootstrap,aligned native PR and descriptive curves | result.json,CSV,aligned arrays | invalid statistics |
| F4 | figures,hash manifest,terminal | FULL_MEASUREMENT_PASS | missing required output |

## 14. Implementation and output

Reuse E01 metrics, fingerprinting, source-model loader, native hooks, immutable full extraction, orchestration and artifact map. Adapt condition IDs/checkpoints, single-S7 validation, same-input repeated-forward reference and two-sided reporting. Reject21B cached native vectors and old directional verdict. Copy rather than modify the prior qualified execution package.

Code root `/data/250010109/MoE_Router/experiments/20260922_s7_17b_training_history_reuse_audit`; runner `scripts/run_full.sh`; config `manifests/full_config.json`; output unique `runs/full_4x5090_<UTC>`. Freeze source/tests/config/input/Protocol/Anchor/Focus/envelope and checkpoint manifests; copy code/docs into source_snapshot. Preserve raw outputs outside Research_System. Outputs: four native_support.npz/receipt.json and logs; identity/alignment/full receipts; result.json; condition/primary/sample/curve CSVs; two PNG/PDF line/intuition figures; manifests; terminal and durable pod log. Postrun independent audit followed by canonical summary.md/summary_cn.md/detailed.md; no result prose before verification.

Submission uses the repository template. It requires SMOKE_GATE_PASSED=1 for a full-named job; for this explicitly waived run this compatibility flag means **the user waived the gate**, not measured smoke PASS. The executable and certificate record NOT_RUN_USER_WAIVED plus provenance; no SMOKE_ROOT is supplied. Local unit/syntax/identity checks still run. Stop polling after accepted submission and a short startup check; do not wait for terminal or analyze without the researcher's follow-up.

## 15. Completion/failure

Complete execution: all conditions and stages, finite required outputs, verified artifacts,zero updates. Engineering failure/timeout => stop, preserve diagnostic, measurement FAIL/scientific INSUFFICIENT. Successful measurement may yield either sign or unresolved difference. Human mechanism judgment always AWAITING_RESEARCHER. This run cannot produce a causal PASS.

## 16. Cannot claim

No isolated lambda-history effect, matched training-trajectory proof, benefit of lower dimension, semantic separation, language-model utility, optimal K, independent-seed generalization or decoder causal explanation. A single pair does not eliminate every confound. Same initialization is established by recorded hashes, not a new independent seed replication.

## 17. Authorization / freeze ledger

A: user selects bounded same-S7 history comparison; no presumed direction. B/C/E/F measurement panel,read-only task and exact metric reuse inherited from explicitly confirmed E01; comparison changes only the two user-named checkpoints, with neutral sign labels rather than inferred mechanism judgment. D: local manifests/config/source lineage verified,loader rechecks actual states. G: user requests full and explicitly waives smoke; continuation uses established four5090 audit tuple, no fallback. Cross-block consistency PASS for **bounded endpoint comparison**, not for a strict history-only causal estimand. The neutrality of reporting is an AI implementation convention, not an asserted user mechanism belief. No remaining directional scientific choice is needed to produce the requested measurements. Freeze before remote execution; subsequent changes require append-only amendment with eligibility consequences.
