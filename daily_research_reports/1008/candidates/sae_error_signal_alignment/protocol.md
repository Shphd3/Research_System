# Protocol: 20261008_sae_error_signal_alignment

## 0. Approval Snapshot

- Document status: `USER_AUTHORIZED_DIRECT_CANDIDATE_DIAGNOSTIC`.
- Execution authorization: researcher explicitly requested Anchor, Protocol, direct analysis/execution and one four-H100 reserved test, without requiring audit approval. This authorizes the bounded candidate diagnostic; it does not confirm scientific claims or authorize publication.
- A–G human block confirmation: `USER_WAIVED_BLOCK_CONFIRMATION`; no block is represented as individually human-confirmed.
- Cross-block consistency: candidate implementation consistency check required before submission; not a scientific approval gate.
- Primary Anchor: [candidate anchor.md](anchor.md); companion [anchor_cn.md](anchor_cn.md).
- Active Focus: none created or modified, as the researcher specifically requested dated candidate placement.
- Purpose: test whether input-only SAE similarity predicts native next-token loss-gradient direction in two fixed models.
- Role: operationalization/proxy test of H2, not a Router method trial.
- Main comparison: SAE Top-5 fitting neighbors versus twenty matched random reference draws.
- Primary metric: equal-domain, record-averaged δ-cosine advantage S; absolute neighbor δ cosine is the sign guard.
- Pass: both lower 95% interval bounds exceed zero. Fail: S upper bound is nonpositive. Otherwise insufficient; invalid measurements also yield insufficient.
- Scope: one ACP diagnostic, `h100-4-reserved`, `shphd-lite-0911`, maximum four hours / sixteen GPU-hours, four read-only workers.
- Operational freeze time and hash registry: `2026-10-08T08:29:25.982472+00:00`; configs/freeze_manifest.json records exact scientific-body/config/code/data hashes before execution. The execution owner must register actual hashes before submission. No fabricated checksum or freeze timestamp is recorded here.
- Scientific result at freezing and researcher interpretation: `NOT RUN` / `Unknown`.

## 1. Terminology / Definitions

A record is one selected natural-text item. A position is one contextual next-token prediction. Fit records provide the frozen neighbor reference pool; readout records provide query positions. a is the native tensor observed by the SAE; δ=∂ℓ/∂a is its gradient for one true next-token CE. z is its complete nonnegative sparse Top-32 activation code. A “similar atom” group means nearby activation codes, not identical vocabulary tokens or nearby decoder columns.

Each model has its own a and δ. For a secondary linear-projection gradient measurement, `param_input` is projection input u and `param_delta` is output sensitivity κ. They are not automatically a and δ. All cosine quantities are dimensionless; CE is in nats per true target.

## 2. Anchor Alignment

The Anchor’s unresolved clause is H2’s association between SAE similarity and native error direction. Three operations suffice: collect native tensors and loss gradients; select fitting neighbors without targets or gradients; compare readout gradient alignment with controls and uncertainty. Completion means complete eligible measurements and separate support/non-support/insufficient results for both fixed models. No canonical scientific state transition occurs through a job status or implementation check.

## 3. Tested Hypothesis

Readout positions’ five nearest SAE reference positions have a larger mean δ cosine than twenty matched random draws and a positive absolute mean δ cosine. The registered direction is greater alignment, not merely smaller Euclidean distance or lower aggregate loss. S7fresh and Qwen are tested separately; one model cannot rescue the other.

## 4. Rival Explanations

| Rival | Registered comparison | Remaining boundary |
|---|---|---|
| Domain or position drives alignment | Same domain and same floor(position/64) reference pool | Other contextual differences remain |
| Ordinary input similarity explains the effect | Top-5 native-a neighbors in the identical pool | No causal attribution to SAE semantics |
| Current-token identity explains the effect | Strict same-current-token subgroup | Coverage may be small; no silent fallback |
| True next-token identity explains the effect | Same/different-target post-hoc strata | Target never selects neighbors; this is descriptive conditioning |
| Shared stratum bias or implementation error | Matched-stratum δ shuffle and known-case checks | A null is not an intervention on semantics |

## 5. Data Construction And Provenance

Select 1024 records from the existing N8_v1 natural-text population: eight categories across computer science, mathematics, physics and biology; each category contributes 64 fit and 64 readout records. Fix sampling hash key `h2-20261008-v1`. Maintain 256 token IDs per item under the verified Qwen tokenizer. Use prefix IDs 0–254 and sixteen positions `14,30,…,254`; each target is the original ID at position+1. Planned counts are 512 fit / 512 readout records and 8192 positions per split, per model.

Exclude records matching the earlier 20260925 selected 1024 records by exact sample identity, exact text or exact token-ID sequence. Deduplicate exact identities across current splits. Record, but do not silently exclude, overlap with the historical 20260930 NTP 2048-record panel and prior text exposure. There is no untouched confirmation claim. Paper-level IDs and residual dependencies may be unknown.

Execution-owned inputs are `data/selected.jsonl` and `data/data_manifest.json` under `/data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment`. The prepared manifest reports zero overlap with the old 1024-record panel, overlap of 768 records with the historical 20260930 2048-record NTP-statistics panel, and zero near-duplicate collisions under selected-panel five-token Jaccard ≥0.85. The source is the previously audited N8_v1 corpus, not a fresh holdout. Paper IDs are unavailable. The selected payload hash is `22a8c4d23a29d1508778ba2702c65f724bd022c1f36490735f8ca6679042857a`; source, tokenizer and manifest hashes remain in the actual manifest.

## 6. Learning Task And Permitted Supervision

There is no learning. The measurement task is the unchanged model’s actual next-token CE. Neighbors may use fit a/z, domain, position bin, current token for the registered subgroup, and deterministic tie order. They may not use δ, true next token, loss, source-update consequences or readout outcomes to rank positions. True targets enter CE and post-hoc same/different-target reporting only. No labels are generated or reversed; no SAE reconstruction objective enters δ.

## 7. Model / Architecture And Frozen Variants

**S7fresh:** fixed exact-33B state in `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000/state.pt`. The researcher confirmed “s7fresh.” The selected measurement state is 33,000,000,000 training tokens / optimizer update 125894, not 33B parameters. The backbone has eight layers; the hook is `blocks[7].attn.o` output before residual addition, dimension 1024. SAE width is 30000, Top-K 32, training reconstruction coefficient 0.1. Manifest state hash: `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`.

Reuse the inspected frozen measurement core at `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/scripts/core.py`, adapting batching and selected positions. Native a=Wc, with c dimension 2048; `param_input=c`, `param_delta=δ`. Use the original SAE `encode` and decoder normalization, not the Qwen E16 implementation.

**Qwen:** `/data/250010109/model_cache/Qwen3-0.6B-Base-official`, 28 layers, hidden 1024. Actual model.safetensors SHA-256 is `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`. Its layer-27 MLP-input SAE is `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt`, actual hash `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`. Model config hash `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59` agrees with SAE metadata. Use its original `sae_core.TopKSAE.from_pretrained` / `encode_topk` and Hugging Face base model, adapting native hook capture and downstream replay.

Qwen a is the input to `base.model.layers[27].mlp` after `post_attention_layernorm`, not the Attention output or final hidden state. For the secondary down-projection gradient, u is the gated intermediate activation of dimension 3072 and κ is the gradient at down-projection output of dimension 1024. δ at a must not be substituted for κ.

Both models and dictionaries are float32, frozen and in eval mode. CE uses float64 logsumexp from float32 native logits. Keep TF32 disabled and record versions. The available HF runtime is `/data/250010109/dependency_packages/hf_transformers_qwen3` (4.53.3); actual image/runtime versions are registered with the run. No LoRA branch is added.

## 8. Training Objective And Optimization

Compute ℓ=logsumexp(logits)−logit[y] for each real target. Derive δ from the sum over selected position losses at the last hook; last-layer downstream computation is positionwise, and first-batch qualification verifies this against individual-target gradients. No loss averaging factor is silently incorporated into the retained per-position δ.

Optimizer: none. Schedules, training checkpoints, full-model updates, SAE updates and reconstruction-gradient terms: none. The training observability contract is `NOT_APPLICABLE` because optimizer updates are zero; nevertheless retain valid-target/record counts, device identity, durable progress logs and freeze/no-op evidence. Reconstruction is a diagnostic field and never an adverse-sample exclusion rule. Verify model/SAE state remains unchanged.

## 9. Conditions, Seeds, And Checkpoints

| Condition | Evidence role | Output |
|---|---|---|
| Raw decoder-norm-weighted SAE Top-5 vs random-20 | Primary H2 | Pair / record / domain estimates and S |
| Native-a Top-5 vs its random-20 | Input-similarity rival | Same metrics, secondary |
| Strict same-current-token SAE/native neighbors | Lexical rival, no fallback | Coverage and subgroup metrics |
| Fit-mean centered code and centered-δ sanity | Registered secondary | Centered-code metrics and centered-δ diagnostics |
| Matched-stratum shuffled δ | Negative control | Null-alignment diagnostics |

Sampling key is fixed above. Random-pair and bootstrap seed is `20261008`; tie order is deterministic by record ID and position. No seed sweep, checkpoint selection, post-hoc operating-point choice or automatic rerun. Microbatch size is four records; each worker/model first qualifies on its first two records. Each worker receives records by prepared integer record_id modulo four and processes its 256 records first with S7, then Qwen.

## 10. Primary Metric And Frozen Analysis Plan

For each model, weight all 30000 sparse-code coordinates by decoder-column norm and unit-normalize for cosine. The main similarity is uncentered. A readout position selects Top-5 fit positions within its domain and position bin. The random control draws twenty times with replacement from the same pool, excluding that condition’s five selected neighbors. Minimum primary pool size is twenty-five; strict current-token strata require six; deterministic ties cannot depend on δ or y.

Let b_i be the mean δ cosine of the five neighbors, r_i the random mean and s_i=b_i−r_i. Average each quantity over valid positions within each readout record, then records within each domain, then four domains equally. Report S and B, the pooled advantage and absolute-neighbor cosine. Fit references, pair IDs and random draws stay fixed during bootstrap.

Use 2000 record bootstrap samples, with replacement within each readout domain, preserving its eligible record count; seed 20261008. Report two-sided 95% percentile intervals. The independence unit is approximately the selected record, not token or pair; unknown common papers/documents limit the interval interpretation. There are two separate primary model tests, no pooled victory criterion and no family-wise generalization claim. No secondary metric rescues either primary outcome.

Input-only neighbor selection precedes gradient-validity checks. Restrict the main fitting reference pool to nonzero code norm above 1e-12 using input features only. Any nonfinite collected measurement fails qualification or collection; zero-norm δ is masked at scoring only. Use a fixed engineering epsilon 1e-12 for cosine denominators and validity. A position is valid only if all five neighbor and all twenty random comparisons have valid δ vectors; do not reselect using δ or silently fill pairs. Report coverage and missing counts. A valid query record has at least one valid main position. Eligibility requires at least 256 valid query records, all four domains represented, and at least 90% of all 8192 planned readout positions valid.

## 11. Secondary Metrics And Guards

Report mean/quantiles of δ norm, negative δ-cosine proportions, SAE support Jaccard, code cosine, native-a cosine, matched-stratum shuffle result, and same/different-next-target strata. The same-current-token candidate pool must contain at least six fit positions; otherwise mark that query uncovered. Do not fall back to unmatched tokens. If fewer than 64 readout records contribute, use descriptive subgroup reporting only.

Fit-mean code centering uses fit codes only and the same neighbor/control/aggregation rules; centered-δ sanity subtracts the fitting mean δ from both fit and readout δ while retaining the registered input-selected pairs. Neither enters primary neighbor selection or the primary decision. Native-a controls use their own eligible sample, do not alter the SAE primary sample, and cannot fill its missing comparisons. Reconstruction error is reported, not used to drop unfavorable records. Actual projection-gradient cosine is computed as cos(κ_i,κ_j)cos(u_i,u_j), using model-specific u/κ. This implementation identity does not establish H2 or a finite-update benefit.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: equal nonzero δ vectors produce cosine one; orthogonal vectors produce zero.
- Known bad: opposite vectors produce cosine minus one; selecting an identical code must not force δ cosine to one.
- Known confusing: two codes may match while true next-token targets differ; this must remain valid data rather than be discarded.
- Guard: zero vectors and nonfinite arrays produce an explicit invalid result rather than a favorable replacement.
- Guard: native and downstream-replay CE/δ agree; actual linear-projection autodiff gradient agrees with κu^T on first-batch examples. Different Qwen hook tensors remain distinct.

Numerical tolerances are fixed in `configs/h2_v1.json` before submission and checked against existing source tolerances. Qualification checks measurement implementation only; never label them scientific audit `PASS`.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / input | How / why | Output and stop rule |
|---|---|---|---|
| Prepare | Obtain permitted 1024-record panel from N8_v1 | Fixed hash selection, split/category counts and exact old-panel exclusions prevent result-driven selection | selected.jsonl / data_manifest; missing count/hash/target means stop |
| Qualify | Check each model/rank’s first batch of two records | Native/replay CE, δ and projection-gradient identities; no-op state check establish the intended measurement | Qualification receipt; any failure stops that worker and invalidates its dependent data |
| Collect | Measure all assigned records, frozen assets | Four workers, each S7 then Qwen; retain a,δ,z,u,κ and targets | Complete feature shards / receipts; nonfinite or missing data reported, never silently retried as a new experiment |
| Analyze | Compare fit-only neighbors with matched controls | Freeze pairs before outcome aggregation; per-record bootstrap prevents pair-count pseudoreplication | Model-specific CSVs / summary; qualification/coverage failure yields insufficient |
| Deliver | Make evidence reviewable | Tables and clean PNG/SVG figures, concise bounded interpretation | Completion receipt and result links; no publication or new training |

One authorized ACP job contains these stages. The two-record qualification is built into that job, not a separate approval or external Smoke stage. Abort on hash/schema mismatch, wrong hook, failed identity/no-op, resource deviation or the four-hour ceiling. No automatic hardware fallback, duplicate submission or continuing monitoring is authorized.

## 14. Algorithm, Output, And Provenance Contract

Execution root: `/data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment`; decision-bearing configuration: `configs/h2_v1.json`.

Ordered algorithm: verify hashes → load frozen model → qualify first batch → collect assigned records for S7 then Qwen → validate and join shards by record ID → construct fit reference pools and input-only pair IDs → compute model-specific δ and parameter-gradient statistics → record/domain aggregate → bootstrap fixed query records → apply registered outcome rules → write tables, figures and receipt.

Expected artifacts:

- `collection/shard_*/{s7,qwen}/features.npz` and corresponding qualification/collection receipts: record IDs, positions, a,δ, sparse indices/values, next/current targets, losses, reconstruction diagnostics, `param_input`, `param_delta`.
- `analysis/<model>/` pair, record and domain CSVs; each model’s `summary.json`; validity, coverage and shuffled-control reports.
- Source-traceable PNG/SVG figures, provenance/complete-artifact manifests, and final completion receipt.
- ACP submission receipt, image/runtime/resource identity, actual source/config/Anchor/Protocol/data hashes and deviations.

This candidate stores only authored text and small selected evidence; raw arrays and checkpoints stay in execution. No font, model checkpoint or duplicated training data is added to Research_System.

## 15. Success / Failure / Insufficient Evidence

Apply independently per model after eligibility:

1. `SUPPORT` if lower95(S)>0 and lower95(B)>0.
2. `NON_SUPPORT` if upper95(S)≤0.
3. `INSUFFICIENT` otherwise, including unqualified measurement, missing artifacts, too few query records or less than 90% valid positions.

If S is resolved positive but B is not positive, report “relative alignment advantage without resolved same-direction evidence” and retain the primary `INSUFFICIENT` branch. Zero is a directional association threshold, not a minimum useful effect. Mechanical completion and empirical verdict are recorded separately; human scientific interpretation remains Unknown until supplied.

## 16. What This Cannot Claim

This cannot establish semantic atom meaning, causality of SAE similarity, finite-loss help, complete-gradient conflict resolution, Expert-sharing policy, routing benefit, long-term training gain, untouched confirmation or general equivalence across hooks/models. True target conditioning remains a diagnostic, not allowed information for a deployable router. Positive alignment is one candidate property; the original phrase “what routing truly needs” is not established as a sufficient routing criterion.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | Meaning | Human confirmation state |
|---|---|---|
| A | H2 question and local claim boundary | User activated H2; detailed numerical design is candidate |
| B | Panel, split and exclusions | AI operationalization under direct execution authorization |
| C | Pure natural next-token measurement | No new supervised training task |
| D | Verified S7fresh/Qwen assets and original SAE hooks | Asset evidence verified; S7fresh name user corrected |
| E | No optimizer / no model or SAE training | Bounded diagnostic scope |
| F | Neighbor comparison, controls and outcome thresholds | AI candidate definitions; no claimed human scientific confirmation |
| G | One four-H100 reserved execution | Explicitly authorized by researcher |

The researcher’s “无需审计通过，直接分析执行，先 candidate” instruction waives the usual A–G confirmation sequence for this bounded candidate diagnostic. It does not retroactively mark blocks `CONFIRMED`, promote this to a canonical approved design, or confirm an outcome. The registered authorization label is `USER_AUTHORIZED_DIRECT_CANDIDATE_DIAGNOSTIC`.

Before submission, the execution owner records actual scientific-body, configuration, code and data hashes and the freeze timestamp, then changes the operational freeze field from pending to registered. This is a reproducibility check, not a request for another user approval. After execution begins, preserve this scientific body. Append any material amendment with time, old/new values, reason, outcomes already visible, affected blocks, authority and evidence-eligibility impact. Results are written in separate result records, not inserted as pre-run predictions here.
