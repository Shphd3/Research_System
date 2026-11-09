# Protocol: A15_17_01_E01 Shared Direction Reuse Audit

> Current operative scope: **APPROVED_FOR_FULL_FROZEN_AUDIT**, Amendment A2 below.
> The original smoke-only registration is preserved verbatim for provenance.

## 0. Approval Snapshot

- Document status: `APPROVED_FOR_IMPLEMENTATION_AND_ENGINEERING_SMOKE_ONLY`.
- Scientific full-analysis body: `DRAFT_NOT_EXECUTABLE`; metric and decision rule
  remain `AI_PROPOSAL`. No full-panel reuse contrast or mechanism verdict is authorized.
- Authority: researcher instruction on 2026-09-22 to continue the named memory,
  write Anchor/Protocol/scripts, and submit a four-5090 smoke. This supersedes the
  previous operational stop only for implementation and bounded smoke.
- Active [Focus](../../../../focus/focus_sae_shared_direction_reuse.md)
  confirms the question, candidate mechanism, rival, and next scientific decision.
- Primary [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md):
  does lower S7 native dimension accompany stronger cross-example same-ID reuse?
- Role: root-cause audit with a prerequisite measurement-identity smoke.
- Treatment/control: diagnostic S7/SALL contrast, not a randomized intervention.
  Architecture and training history differ; coefficient causality is not tested.
- Held fixed: exact 21B checkpoint coordinate, inputs, token masks, layer 8,
  width 30,000, K=32, native attention-write site, mean pooling and dtype policy.
- Scientific primary proposal: difference in mean cosine similarity between
  example-level atom-frequency vectors. No final decision is evaluated in smoke.
- Smoke purpose: demonstrate exact native encoder extraction, same-pass geometry,
  paired identities, finite statistics, CPU/GPU agreement and no model mutation.
- Smoke Pass: every engineering gate in §§11–15 passes on four workers;
  Fail: any required guard fails; incomplete/preempted: no eligibility conclusion.
- Cannot claim: a smoke pass is not H1 support, scientific design confirmation,
  approval for full analysis, training, publication, commit or push.
- Frozen revision: `E01-smoke-v1`, 2026-09-22; pre-submission absolute-file SHA256
  list is `manifests/freeze_sha256.txt` in the execution root below.
- A–G for smoke: scope delegated by the current request; identities locally
  verified, runtime identities checked again in the pod; cross-block engineering
  consistency PASS. Full analysis: F remains PROPOSED; B/D need native-support
  qualification; G has no full execution approval. See §17.

## 1. Terminology / Definitions

Native attention write \(a\): output of `blocks[7].attn.o`, after projection and
before residual addition. Normal inference uses \(a\), not the SAE reconstruction.
S7: final-block sidecar, reweighted 1→0.1 continuation. SALL: original all-eight-
block sidecar with coefficient 1. Neither name encodes a matched strength effect.
Atom: a column of the model-local decoder. Support: 32 IDs returned by
`sae.encode(a_token)`; selected slots need not be nonzero mathematically.
Usage profile: normalized per-example counts of selected IDs across valid tokens.
Effective dimension: participation ratio of centered native covariance, not
number of meanings. Smoke: bounded engineering qualification, not hypothesis testing.

## 2. Anchor Alignment

H1 needs increased cross-example same-ID reuse on the panel that exhibits lower
S7 native dimension. Smoke establishes whether that measurement can be made
faithfully. It does not resolve the Anchor's scientific decision. The strongest
rival remains low dimension from decoder collinearity or coefficient covariance.

## 3. Tested Hypothesis

Scientific H1 (future scope): \(R_{S7}>R_{SALL}\) and \(d_{eff,S7}<d_{eff,SALL}\) on
identical examples. Engineering claim (authorized): native supports and pooled
native writes can be extracted without changing checkpoint parameters, and the
registered statistic implementation is numerically correct.

## 4. Rival Explanations

Different IDs can encode aligned directions; broad IDs can have low-rank joint
coefficient variation. Both can coexist with support reuse. Popular atoms are
not a rival to global same-ID reuse. Do not use a popularity-preserving null or
excess-overlap primary metric from superseded portions of the chat export.

## 5. Data Construction And Provenance

Execution root: `/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit`.
Source root: `/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit`.
Source run: `runs/full_4x5090_retry2_20260921T0200Z` under source root.
Only the N8 layer-8 observer chunks from worker 1 (SALL) and worker 2 (S7) are
identity references. All their manifest/chunk SHA256s and both model manifests
are frozen in execution-root `manifests/assets.json`.

Inherited panel: 192 records, 256 body positions each (49,152 per model), from
fit/development/test splits. Old category-stratified membership is inherited,
not reselected. New code discards labels and does not condition any statistic,
threshold or exclusion on category. Published-record IDs are unique; article
independence is unknown. This is a descriptive existing-checkpoint panel, not a
new sealed confirmation dataset. The earlier whole-N8 dimension numbers cannot
substitute for new same-panel dimension measurements.

Smoke subset: four existing 4-record chunks with smallest SHA256 of their joined
sample IDs. Selected chunk-list indices: 45, 28, 31, 41. Selection uses no labels
or measured values. Exactly 16 paired examples / 4,096 tokens per model; IDs,
input token sequences and source-group IDs are in `manifests/smoke_inputs.json`.
Each worker gets two complete original batches, without truncation or mask changes.

Preflight checks input hashes, all token positions 0–255, chunk checksums,
source files, tokenizer fingerprint, checkpoint manifest and state-file size.
The original checkpoint loader verifies full checkpoint state SHA256 inside
the GPU worker. Local state-file size is not presented as a verified hash.

## 6. Learning Task And Permitted Supervision

No learning task, labels, probe, optimizer, loss computation or model fitting.
Only frozen forward passes and deterministic counting/statistics. Existing
fit/dev/test tags do not grant labels permission or make this confirmatory.

## 7. Model / Architecture And Frozen Variants

Both models: 8 blocks, hidden width 1,024, native sidecar read point, dictionary
width 30,000, K=32, exact 21,000,000,000 valid prediction training tokens.

- SALL source:
  `/data/250010109/MoE_Router/experiments/20260918_attention_output_sidecar_all8_4h100_resume`;
  checkpoint relative to it:
  `runs/formal50b_all8_unit_weight_4h100_mbs16_resume/milestones/token_021000000000`.
- S7 source:
  `/data/250010109/MoE_Router/experiments/20260917_attention_output_sidecar_last_reweighted_resume`;
  checkpoint relative to it:
  `runs/formal50b_last_attention_lambda0p1_mbs16_fork_4h100/milestones/token_021000000000`.

Exact source hashes and checkpoint identities are copied, not inferred, from
the verified original `model_manifest_preflight.json` into `assets.json`.
Separate worker processes preserve each source module namespace. Resolve SALL
dictionary as `model.saes['7']`, S7 as `model.sae`. Validate both layouts and
compare captured write with the model's sidecar-source tensor exactly.

## 8. Training Objective And Optimization

NOT APPLICABLE: zero backward calls, optimizer steps, parameter updates, training
continuation or checkpoint writes. Run `.eval()`, disable parameter gradients,
use inference mode and BF16 CUDA autocast for forward/encoding. Statistics are
FP64; pooled native means are FP32. No training observability tags are fabricated.
Record peak allocated/reserved GPU memory and valid body tokens/sec; these are
inference engineering quantities, not training throughput or predicted LM tokens.

## 9. Conditions, Seeds, And Checkpoints

GPU assignments: 0=SALL/shard0; 1=S7/shard0; 2=SALL/shard1; 3=S7/shard1.
Four independent workers, one node, no DDP or collectives. Each sees 8 examples
in batches of 4. Seed 20260922 for engineering reproducibility. No checkpoint,
layer, K or coefficient selection based on outputs. Dense is not run: it has
no online dictionary and cannot enter the same-ID contrast.

## 10. Primary Metric And Frozen Analysis Plan

### Scientific candidate — NOT authorized for a full-panel result

For token support \(S_{it}\), \(I_{itj}=1[j\in S_{it}]\) and
\(u_{ij}=\sum_t I_{itj}/(T_iK)\). Each \(u_i\) sums to one. Proposed primary:

\[R_m=\frac{2}{n(n-1)}\sum_{i<q}\cos(u_i,u_q),\quad
\Delta R=R_{S7}-R_{SALL}.\]

AI_PROPOSAL: paired example bootstrap, seed 20260922, 2,000 draws; recompute the
complete statistic per resample; percentile 95% interval. Resample examples,
not pairs or tokens. Repeated original IDs in different resampled positions
are retained; only self-position pairs are excluded. The Gram-index shortcut
must match literal recomputation. Intervals describe record-level resampling
of this inherited panel, not variation over model-training seeds or articles.

AI_PROPOSAL decision: after all identity guards and lower aligned S7 dimension,
CI lower>0 → necessary-condition Pass; CI upper≤0 → Fail; otherwise Insufficient.
Unreproduced dimension ordering also means Insufficient for this local question.
No numerical margin, equivalence claim or null model is supplied by smoke.

### Authorized engineering application

Use the 16-example smoke panel to check computability. Run only 64 bootstrap
draws as an algorithm check. Save scalars as `SMOKE_ONLY_NOT_SCIENTIFIC_EVIDENCE`;
always emit `scientific_verdict: NOT_EVALUATED`. Do not apply the scientific
Pass/Fail rule, generate mechanism claims, or run the complete 192-example contrast.
These smoke records are development-exposed and must be declared in a later
full Protocol; do not describe a full-panel reuse estimate as untouched confirmation.

Native dimension: center the same-pass mean writes and compute
\(d_{eff}=(\operatorname{tr}\Sigma)^2/\operatorname{tr}(\Sigma^2)\).
Implementation uses the centered sample Gram matrix; scalar normalization
cancels. Unit tests cross-check against covariance eigenvalues. No unit-norm
transform, PCA truncation or uncentered second moment is substituted.

## 11. Secondary Metrics And Guards

Global usage distribution \(p_j=n^{-1}\sum_i u_{ij}\), distinct IDs, effective
atom count \(1/\sum_jp_j^2\), and per-example support sizes are descriptive checks.
They cannot change the future primary decision. No amplitude weighting is
substituted for selection frequency.

Engineering acceptance limits (implementation details, not scientific thresholds):

1. Correct checkpoint/site/K/width; 32 distinct in-range IDs per token, nonnegative
   finite values, all selected values positive in this smoke. Zero slots fail
   qualification and require an explicit interpretation decision; never drop them silently.
2. Repeat `sae.encode` on the same tensor: exact IDs and values. Same-score native
   Top-32 versus top128-prefix support differences are counted, not hidden;
   differences on an untied boundary fail. Tied differences do **not** fail the
   corrected native encoder; they invalidate using the older cache as exact native IDs.
3. Same input hashes, unique IDs, token positions/counts, same model-local dictionary
   identity across shards. No cross-model dictionary alignment is assumed.
4. CPU/GPU FP64 pair-cosine matrix maximum absolute error≤1e-9 and participation-
   ratio absolute error≤1e-9. Pooled-write relative RMS difference versus the old
   same-example cache≤0.02, inherited as an engineering BF16 tolerance, not proof
   of exact feature-support reproducibility across hardware.
5. Sharded versus serial usage counts exactly equal; usage rows sum to one to
   absolute tolerance 1e-12. No empty, nonfinite or missing examples.
6. Parameter/buffer version counters, sampled whole-model state fingerprints,
   and complete SAE-state tensor fingerprints unchanged. No checkpoint mutation.

## 12. Known Good / Known Bad / Known Confusing Cases

Identical profiles → cosine 1; disjoint profiles → 0; atom-coordinate permutation
leaves reuse unchanged; unequal token counts get per-example normalization;
duplicate/out-of-range/empty support fails; zero covariance fails. Covariance
and Gram dimension computations agree; paired-bootstrap indexing equals full
recomputation including duplicate resampled examples. Globally popular atoms
are real same-ID reuse, not semantic specialization. Equal rank-32/33 values
do not identify a unique feature support without the exact encoder operation.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / input | How and why | Output / handoff | Scope and stop |
|---|---|---|---|---|
| S0 | establish asset identity from prior manifests | hash sources/chunks; align IDs/input/masks; inspect support-producing code | `assets.json`, `smoke_inputs.json`; feed S1 | identity audit only; mismatch stops |
| S1 | qualify actual encoding on frozen models | four workers, same native input and native `encode`; compare old ranking method only diagnostically | each `native_support.npz`, `receipt.json`; feed S2 | 16 paired examples; nonfinite/mutation/identity failure stops |
| S2 | qualify statistics | exact serial/sharded counts; CPU/GPU FP64 checks; 64-draw smoke bootstrap | `engineering_diagnostics.json` | smoke scalars are not a scientific test |
| S3 | certify engineering scope | check all four worker receipts, provenance and outputs | `SMOKE_PASS.json`, durable terminal receipt | Pass is qualification only; failure has no mechanism verdict |
| F1–F4 | future full aligned scientific audit | re-extract all 192 native supports/means; compute proposed statistics; apply confirmed rule | NOT RUN | blocked on metric/design confirmation and separate execution approval |

## 14. Algorithm, Output, And Provenance Contract

Reuse existing `smoke_sites.py` loader/hooks/pooling and `observe_online.py`
dictionary resolver; do not call its old top128 observer as the support source.
New execution scripts: `prepare_assets.py`, `reuse_metrics.py`, `smoke_worker.py`,
`run_smoke.py`, `run_smoke.sh`, plus unit tests. No full-run launch entry exists.
The original source/old experiment files remain unchanged.

Execution keys from repository `docs/execution_envelope.md`:

```yaml
execution_surface: acp
resource_profile: 5090-4-spot
image_id: shphd-lite-0911
execution_scope: frozen_checkpoint_engineering_smoke_only
optimizer_updates: 0
worker_deadline_seconds: 900
```

Reason for non-default profile: the researcher explicitly requested four RTX5090
GPUs for this continuation; use the existing four-card Spot profile, no automatic
H100/eight-card/reserved fallback. The tuple and expanded image URL belong to
the envelope and the submission receipt, not a second registry here.
Activate the existing SM120 layer with the original
`20260918_attention_output_sidecar_all8_4h100_resume/scripts/activate_5090_runtime.sh`;
require its mounted manifest before activation. No installation/base-image mutation.

Submit through `/data/250010109/Research_System/templates/execution/acp_submit_template.sh`,
dry run first. Variables: `SCO_PROFILE=5090-4-spot`, `SCO_IMAGE=shphd-lite-0911`,
`REMOTE_DIR=<execution root>`, `RUN_ROOT=<execution root>/runs/smoke_4x5090_<UTC>`,
`REMOTE_CMD='export RUN_ROOT=<unique run>; bash <execution root>/scripts/run_smoke.sh'`.
Actual submit requires `DRY_RUN=0 ALLOW_SUBMIT=1 PROTOCOL_APPROVED=1`; here the
last flag attests **only** this smoke contract. It cannot authorize a full run.

Artifacts under that run: submission receipt; `pod_logs/`; four worker logs and
directories containing raw support/pooled vectors and identity receipts;
`stages/IDENTITY_PASS.json`, `stages/SMOKE_PASS.json`, engineering diagnostics,
`terminal_receipt.json`. Raw execution artifacts stay outside Research_System.
The owning `detailed.md` records submission and bounded startup; no ongoing
monitoring or auto-resubmission is requested. A Spot interruption is incomplete,
not scientific Fail. The coordinator terminates only its own children on worker
failure/timeout; it never stops other cluster jobs.

## 15. Success / Failure / Insufficient Evidence

Engineering Pass requires successful local unit tests, immutable inputs,
four real RTX5090 workers using GPUs, valid native extraction, all §11 checks,
same-panel aggregation and complete durable receipts. Nonzero exits or failed
guards are engineering Fail; queued/preempted/missing outputs are incomplete.
The technical primary acceptance condition is the conjunction of these guards,
not the sign of \(\Delta R\) or the ordering of dimensions.
Formal scientific results remain NOT RUN regardless of smoke statistics.

## 16. What This Cannot Claim

No regularization-strength causality, trained semantic direction identity,
domain accessibility improvement, causal explanation of dimension, language
loss/data-efficiency benefit, or model use. No fresh confirmation-set inference
from an existing selected panel. No universal natural dimension of 32. No
automatic promotion from implementation or smoke authorization to full execution.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | Engineering smoke | Full scientific audit |
|---|---|---|
| A question/boundary | CONFIRMED by Focus and current bounded instruction | question confirmed |
| B data/provenance | VERIFIED_SOURCE; subset chosen label-blind; runtime hashes mandatory | input panel verified; exact native-support extraction pending |
| C learning/supervision | CONFIRMED none; labels forbidden | same |
| D models/architecture | VERIFIED_SOURCE; frozen 21B identities; runtime loader gates | same models; no native-support full evidence yet |
| E optimization | CONFIRMED none | none |
| F comparison/metric | engineering gates fixed under delegated implementation scope | AI_PROPOSAL cosine, bootstrap and decision rule |
| G execution | HUMAN_AUTHORIZED four-5090 smoke only | NOT AUTHORIZED |

Cross-block consistency: PASS for the engineering claim; NOT PROMOTED for the
scientific audit. All necessary smoke gates are explicit, and none requires
the proposed scientific effect to be present. Engineering constants implement
the current user request; they are not represented as separately human-approved
scientific judgments. Full metric/panel/statistical confirmation remains open.

Post-start freeze: preserve this body and pre-run hashes. Append amendments
with before/after, reason, timing, visible data, approval scope and eligibility
impact; never overwrite a registered metric after viewing outputs. Store
observations and operational receipts in `detailed.md`, not this body.


### Amendment A1 — 2026-09-22T07:29:07.451655+00:00 — bounded engineering repair

Before: state fingerprint used a byte view directly on a zero-dimensional
integer buffer. After: `state_fingerprint.tensor_hash` flattens a contiguous
copy before its byte view and includes dtype/shape; the actual tensor is not
modified. Three CPU regression tests cover scalar counters, BF16/empty tensors,
noncontiguous tensors and non-mutation. Failure telemetry now uses worker
receipts or null for unknown GPU use rather than defaulting false.

Reason: the first authorized smoke `pt-jztyb3sy` terminated at the fingerprint
step with a scalar byte-view RuntimeError. No native support batch or scientific
contrast was completed. Checkpoints and the inherited source caches were
already visible; this patch does not use scientific outcomes to change analysis.
Affected blocks: G engineering instrumentation only. Data, models, sample IDs,
K, dtype, acceptance limits, proposed scientific metric and resource profile
are unchanged. Scope authority: the researcher explicitly said “请继续完成”
after being informed of the failure and the same-config repair plan.
One deliberate corrected smoke submission is authorized; no automatic retry
loop or full run is introduced. New frozen revision: `E01-smoke-v2`.

Eligibility: v1 is failed engineering evidence only; preserve its source
snapshot and receipts under the failed run. v2 must pass all original smoke
gates independently. The v1 terminal `gpu_used=false` was a default-reporting
bug, not proof that GPUs were unused: S7 reached SAE fingerprinting after GPU
model loading. Do not retroactively rewrite that raw terminal receipt.


### Amendment A2 — 2026-09-22T07:43:42.610543+00:00 — researcher-confirmed full-panel audit

**Current operative design/execution status: APPROVED_FOR_FULL_FROZEN_AUDIT.**
The researcher requested completion of smoke, submission of full run, and the
complete experiment. In response to the explicit criterion question, the
researcher confirmed: “确认，按这套判据执行”. This confirms the previously proposed
192-example panel, native Top-32 frequency-profile cosine, 2,000-draw paired
example bootstrap and necessary-condition interpretation. The previous
smoke-only restrictions remain a historical record and are superseded **only**
for this registered full frozen audit. It still authorizes no training, new
conditions, unregistered causal test, commit or push.

**Scientific design freeze:** `E01-full-v1`. This amendment is registered before
full native-support extraction or full signed contrast. Engineering smoke
outputs (16 development-exposed examples) already exist; their exposure is
explicit and these examples are included without result-dependent exclusions.
This is an existing-panel diagnostic, not a newly sealed confirmation set.
No effect threshold, statistic, sample selection or decision rule was tuned
using smoke statistics. Exact rule below matches the proposed §10 rule.

**Purpose / hypothesis / method / expected conclusion:** test whether lower S7
native dimension accompanies greater same-ID selection reuse, not whether the
method improves semantics. Re-extract native supports and same-pass means on
the entire fixed panel; calculate model-local reuse and its paired contrast;
apply the frozen necessary-condition rule. A positive result keeps H1 viable
without separating it from decoder geometry/covariance; a resolved nonpositive
contrast with lower dimension rejects the registered prediction on this panel;
an unresolved contrast or guard failure is insufficient.

#### A2.1 Exact conditions and sources

- Frozen 21B original SALL and reweighted S7, layer 8, each own 30,000-atom SAE,
  K=32. Same checkpoint/source hashes as §7 and `assets.json`. No new model.
- All 192 inherited N8 records, 256 body tokens each: 49,152 tokens per model.
  `manifests/full_inputs.json` serializes original observer order and original
  4-record batches; strips labels and preserves input hashes and source IDs.
- GPUs 0/1 run SALL/S7 on chunks 0–23; GPUs 2/3 run the same models on chunks
  24–47. Each worker processes 96 records, 24,576 tokens in 24 batches of four.
  This changes total work, not precision, batch shape, pooling or kernel policy.
- Reuse the smoke-qualified extraction algorithm in `full_worker.py`, copied
  from `smoke_worker.py` with only panel source, shard span and mode metadata
  changed. Native `sae.encode`, mask/site checks, repeatability, same-score
  top128 comparison, FP64 CPU/GPU checks and no-mutation checks are retained.
- `full_analysis.py` verifies all worker receipts and raw NPZ checksums before
  aggregation. Verify model-local dictionary fingerprints match across shards,
  merge token-local row indices with correct offsets, and reproduce exact
  serial counts. Revalidate IDs, hashes and all 0–255 positions across models.
- Additional consistency gate: all 16 overlap examples must reproduce the
  qualified smoke's unordered native support and pooled means exactly. Failure
  stops analysis and is insufficient, not a license to exclude those examples.
- The approved uncertainty is record-ID resampling. This does not establish
  article-level independence, unseen semantic generalization or training-seed
  uncertainty. No category labels, classifiers or task-loss comparison.

#### A2.2 Registered metric and complete decision mapping

\(u_{ij}=\sum_t1[j\in S_{it}]/(256\cdot32)\), all selected values must be positive
under the inherited qualification guard. For each model, \(R\) is the mean cosine
of \(u_i,u_q\) over all distinct sample-position pairs. Primary contrast
\(\Delta R=R_{S7}-R_{SALL}\). Bootstrap seed 20260922, 2,000 paired draws of 192
record indices with replacement; recompute R for every draw, including repeated
original IDs at different resampled positions. Percentile 95% CI (2.5/97.5).
Gram-indexing is an exactly tested acceleration, not a different estimator.
Native \(d_{eff}\) uses centered covariance participation ratio of the same
192 means; Gram and covariance-spectrum implementations must agree.

1. Identity or numerical guard fails → measurement FAIL, scientific INSUFFICIENT.
2. Lower S7 dimension does not reproduce → scientific INSUFFICIENT.
3. With lower S7 dimension and eligible measurement: CI lower>0 → PASS of H1's
   necessary condition only; CI upper≤0 → FAIL of that prediction; otherwise
   INSUFFICIENT. A zero CI lower bound is not PASS. Equality of dimensions is
   not lower dimension. No secondary scalar can change this classification.
4. Execution may succeed even when scientific verdict is FAIL or INSUFFICIENT.
   Keep engineering completion and scientific decision as separate fields.
5. Output `human_mechanism_judgment=AWAITING_RESEARCHER`: the deterministic
   criterion does not silently become the researcher's mechanism judgment.

Secondary existing diagnostics: distinct IDs; effective global atom count
\(1/\sum_jp_j^2\) for \(p_j=n^{-1}\sum_iu_{ij}\); per-example support sizes;
frequency and centered variance cumulative curves. They describe concentration
only. No geometric intervention or coefficient-covariance test is added.
Figures use interval/line plots (not bars), with an explicitly hypothetical
intuition panel and a separate real-observation panel. No fabricated result.

#### A2.3 Constructible stages, output and failure rules

| Stage | Goal/input | Operation / why | Output / handoff | Stop |
|---|---|---|---|---|
| F0 | establish smoke and input eligibility | require terminal+SMOKE_PASS from `/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/smoke_v2_4x5090_20260922T072907Z`; verify all frozen source/config hashes | IDENTITY_PASS | fail or incomplete gate stops |
| F1 | native same-panel extraction | four workers, 48 original batches per model, no optimization | four native_support.npz and receipts | nonfinite, identity, mutation, zero support or timeout stops |
| F2 | aggregation/alignment | checksum/ID/mask/dictionary checks, serial count equality, exact smoke overlap | ALIGNED_FULL_PANEL_PASS | any mismatch stops before primary contrast |
| F3 | scientific measurement | R, PR dimension, registered paired bootstrap and rule; descriptive concentration | result.json, primary/conditions/samples/curves CSVs | invalid statistic -> INSUFFICIENT |
| F4 | evidence closure | line figures, artifact hashes, complete receipt | FULL_MEASUREMENT_PASS and terminal | missing required artifact prevents completion |

New scripts: `full_worker.py`, `full_analysis.py`, `run_full.py`, `run_full.sh`,
`build_full_figures.py`; new unit tests cover decision boundaries, full shard
aggregation and known-positive/negative bootstrap cases. All remaining helpers
are the qualified smoke implementation. Code snapshot and SHA256 freeze live
under the full run. No raw outputs are promoted to the research repository.

Full root: execution-root `runs/full_4x5090_<UTC>`; one unique directory, no
resuming by overwriting results. Full config: `manifests/full_config.json`.
Full freeze: `manifests/full_freeze_sha256.txt` (separate from the smoke freeze).
Outputs: `worker_*/native_support.npz`, `worker_*/receipt.json`, durable logs,
`stages/IDENTITY_PASS.json`, `stages/ALIGNED_FULL_PANEL_PASS.json`,
`analysis/result.json`, aligned usage/native matrices, four CSV tables,
`figures/reuse_necessary_condition.*`, `figures/intuition_vs_observation.*`,
figure manifest, artifact manifest, `stages/FULL_MEASUREMENT_PASS.json`, terminal receipt.
Report destinations: this experiment's summary.md / summary_cn.md / detailed.md;
reader figure copies under the 0922 date-local `figures/` directory with provenance.

Resource profile remains `5090-4-spot`, image `shphd-lite-0911`, the existing
mounted SM120 layer. Worker safety deadline 900 seconds; no resource fallback
or automatic retry loop. Same repository submission template, dry-run then
`DRY_RUN=0 ALLOW_SUBMIT=1 PROTOCOL_APPROVED=1 SMOKE_GATE_PASSED=1`, with
`SMOKE_ROOT` set to the qualifying smoke and `RUN_ROOT` to the new unique run.
The command is `bash <execution-root>/scripts/run_full.sh`; no training launcher.
Current request to complete the experiment authorizes following this bounded
measurement job through terminal evidence and reporting, not indefinite future
monitoring. Scheduler delay has no reliable ETA.

#### A2.4 Audit and eligibility ledger

A question/boundary CONFIRMED; B inherited fixed full panel CONFIRMED with local
identity checks and runtime guards; C no supervision CONFIRMED; D frozen
models/site/K CONFIRMED with smoke-qualified code; E no optimization CONFIRMED;
F exact cosine/bootstrap/decision rule HUMAN_CONFIRMED by the explicit answer;
G same-profile full execution HUMAN_AUTHORIZED after smoke PASS. Cross-block
consistency PASS: the computation realizes the registered same-ID prediction,
but does not purport to discriminate geometry contributions after a positive
result. Existing-panel and record-independence limitations remain explicit.
Subsequent changes require a new append-only amendment; no post-result rewrite.
