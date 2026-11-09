# Detailed: A15_17_01_E01 shared SAE atom reuse

Primary Anchor: [shared atom reuse](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md).  
Frozen contract: [Protocol A2](protocol.md), revision `E01-full-v1-A2`; submitted snapshots remain under [/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/source_snapshot](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/source_snapshot).  
First reading: [Summary](summary.md) / [中文四段式分析](summary_cn.md).  
Execution COMPLETE; measurement ELIGIBLE for the registered existing-panel comparison; necessary-condition PASS. Human mechanism judgment AWAITING_RESEARCHER.

## 0. Quick recap

On identical frozen inputs, greater S7 selection-profile similarity accompanies lower native dimension. Delta R = +0.085788, paired-example bootstrap 95% CI [0.072687, 0.098599]; native effective dimension SALL 17.160447, S7 14.486918. This satisfies the approved necessary prediction, not causality, semantic quality or a matched regularization-effect claim. Full task `pt-5snx2hrj` is platform SUCCEEDED; application terminal PASS at 2026-09-22T07:57:09.644779Z; platform completion 07:57:13Z. Current verification: 2026-09-22T09:11:46.687971+00:00. Independent postrun numerical/artifact audit PASS.

## 1. Terminology and decision point

| Term | Concrete meaning / unit | Decision role and boundary |
|---|---|---|
| Atom / support | Decoder column ID / native encoder selected IDs; within-model only | Counts selections, not semantic concepts; distinct columns need not be independent |
| Usage profile u | Counts divided by 256×32 selected slots per record; sums to 1 | Selection frequency, not coefficient amplitude |
| R | Mean cosine of different records' usage vectors; dimensionless | Across-record same-ID reuse; not token-level semantic equivalence |
| Native a | Post-attention-output-projection, pre-residual vector; body-token mean per record | Measures backbone, not reconstruction |
| Effective dimension | Centered covariance trace squared divided by squared Frobenius norm | Variance concentration, not literal rank or semantic capacity |
| Effective atoms | 1/sum(p_j²), p=mean usage across records | Descriptive frequency concentration, not independent decoder directions |

Anchor clause tested: does the lower-dimension S7 observation have the accompanying increase in model-local support reuse required by the current hypothesis? A negative resolved primary contrast would reject this registered prediction; a positive one leaves geometry/covariance contributions unresolved.

## 2. Protocol freeze, compliance and deviations

Frozen A2 contract and full_config registered before full extraction. [Report-preflight receipt](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/report_preflight_audit.json) verifies all 34 frozen source/input files before documentation changes. Frozen source snapshots, not later living research documents, own submission identity.

| Registered item | Expected and actual | Status / evidence | Eligibility impact |
|---|---|---|---|
| Approval/revision | Explicit full request plus exact metric confirmation; E01-full-v1-A2 | [frozen config](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/full_config.json), Protocol A2 | Eligible scope |
| Dataset/selection | 192 inherited N8 records, 256 body tokens, no exclusions or label analysis | IDENTITY_PASS and ALIGNED_FULL_PANEL_PASS | Same existing panel, not fresh confirmation |
| Models/site | Exact21B SALL original / S7 reweighted, native layer8, width30000/K32 | Four checkpoint/dictionary fingerprints | Measurement matched; training histories not controlled |
| Extraction | Native encode, original batch4, BF16 forward/FP32 pooled means | Four receipts, support NPZ hashes, smoke overlap | No source/caching substitution |
| Read-only task | Frozen state, no optimizer, labels or checkpoint writes | Updates0, state fingerprints/versions unchanged | No training or causal manipulation |
| Computation | FP64 frequency cosine, centered PR, paired 2000-draw bootstrap seed20260922 | full_analysis.py + independent_audit.json | Registered quantities reproduced |
| Resources | 5090-4-spot, one node/four GPUs, existing image/runtime | [platform verification](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/platform_describe_verification_20260922T090416Z.json), worker GPU names | No fallback or full retry |
| Gates/artifacts | Four workers + identity/alignment/full gates, CSV/PNG/PDF/hash manifest/pod log | All present, 22 artifact hashes independently checked | Complete |
| Early engineering failure | First smoke scalar fingerprint failed; repaired under A1 | Historical ledger below, v1 snapshot | Excluded from scientific evidence, not silently removed |
| Top-K tie risk | Native32 vs prefix32 audited | Full mismatches0 both conditions | Risk not observed as a support difference |
| Postrun work | Independent numerical audit added after freeze; no input/code change | Script hash in independent_audit.json | QA only, not a new endpoint or tuned rule |
| Reporting updates | Living Anchor/Focus/result records may change after completion | Submitted snapshots retained | No alteration of registered contract |

No full-condition exclusions, missing shards, retries, resource changes or post-result metric substitutions. Smoke's 16 records remain development-exposed and are included by A2, not reclassified as untouched confirmation. Semantic baselines, interventions and training seeds beyond the two existing checkpoints were not part of this experiment.

## 3. Actual setup and data

Two fixed checkpoint conditions, one checkpoint each, four independent GPU workers (two shards per condition); no distributed training. Inherited N8 panel is historically category-stratified; original record order and 48 batches of four are frozen in [full_inputs](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/manifests/full_inputs.json), labels stripped from the executable manifest. Each worker processes 24 batches /96 records /24,576 body tokens; 49,152 body tokens per model. Original loader, tokenizer/input hashes and source checksums are in [assets](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/manifests/assets.json). All 16 smoke-overlap supports and means reproduce exactly per model. Article-level independence is not established.

- SALL checkpoint: `/data/250010109/MoE_Router/experiments/20260918_attention_output_sidecar_all8_4h100_resume/runs/formal50b_all8_unit_weight_4h100_mbs16_resume/milestones/token_021000000000`; checkpoint state SHA256 `60eab96f0d8ef5e7327c1712f98730c4e2102d9ab6d34b560efddb7026971f00`.
- S7 checkpoint: `/data/250010109/MoE_Router/experiments/20260917_attention_output_sidecar_last_reweighted_resume/runs/formal50b_last_attention_lambda0p1_mbs16_fork_4h100/milestones/token_021000000000`; checkpoint state SHA256 `127b185a00e660c94b70e42a4b0dacfb8160795ca8318dc4bf720223205d20c4`.
- S7 is coefficient1→0.1 continuation with last-layer sidecar; SALL original all-layer sidecar. Changed conditions include topology and training history, not an isolated regularization coefficient.
- Held fixed: input IDs/tokenization/positions/masks, observation site, dictionary width, K, checkpoint token coordinate, batch shape and measurement precision.
- BF16 forward and native encode; FP32 native mean pooling; FP64 statistical analysis. Native width1024. Decoder columns remain model-specific.
- No train/dev selection, loss, optimizer, learning-rate schedule, training epochs, effective update batch, gradients or trained modules in this audit. Both historical models stay frozen; zero optimizer updates. The source datasets' historical fit/dev/test labels are not used as a new learning split.
- Runtime: `5090-4-spot`, `shphd-lite-0911`, torch2.8.0+cu128 mounted SM120 layer. Exact image/activation/command: [execution certificate](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/execution_certificate.md). Worker safety deadline900s; no timeout.

## 4. Metrics and frozen rule

For record i, atom j, valid token t, support S_it: u_ij=sum_t 1[j in S_it]/(256×32). R averages cosine(u_i,u_q) for i<q, excluding self-pairs in each sample. Delta R=R_S7−R_SALL. No cross-model ID matching or subtraction of a popularity null. Bootstrap resamples the same 192 record indices for both conditions 2000 times with replacement; duplicates at different resampled positions remain valid pairs. Percentile 2.5/97.5 interval, RNG seed20260922. Pairs are dependent; the resampling unit is a record, not a pair/token.

PR dimension uses centered covariance of the 192 same-pass native means: tr(Sigma)^2/tr(Sigma²). All measurement guards must pass. Lower S7 PR plus positive CI lower bound => necessary-condition PASS; lower S7 PR plus nonpositive upper bound => FAIL; otherwise INSUFFICIENT. A zero lower bound is not PASS. Dimension ordering is a point-estimate guard, not a confidence test of dimension. Secondary statistics never override this branch.

## 5. Evidence lineage

| Decision/evidence | Raw observation → computation | Aggregation/uncertainty | Observed | Eligibility / boundary |
|---|---|---|---|---|
| Primary necessary prediction | Four worker native_support.npz → checked full_analysis.py merger → model-local usage → reuse_metrics.py cosine | Paired record bootstrap,2000,seed20260922 | Delta0.0857880765452389; CI[0.07268663342186764,0.09859949700784894] | ELIGIBLE; necessary-condition PASS only |
| Aligned dimension guard | Same four NPZ a_mean → ordered 192×1024 arrays → centered Gram spectrum PR | Point estimate; CPU covariance trace-ratio recheck | SALL17.160447062433036; S7 14.486917591755645 | ELIGIBLE; no dimension-difference CI |
| Coverage/concentration | Native supports → global counts p → distinct IDs and 1/sum(p²) | Whole fixed panel; descriptive only | Distinct17060/142; effective229.3367399171016/73.98933792733355 (SALL/S7) | Bounded descriptive adjunct, not semantics |
| Support-operation consistency | Same pre-topK score vectors → native32 vs prefix32 set comparison | All49152 tokens/model | Ties11716/2545; mismatches0/0 | Guard diagnostic; no observed support error |
| Numerical integrity | Aligned usage/native arrays and 22 artifact hashes → audit_completed.py | Independent sum-vector cosine,1024×1024 covariance,weighted quadratic bootstrap | Delta/CI agree within1e-12; PR within1e-10 | QA, does not add independent data |

Primary curated tables: [primary](tables/primary.csv), [conditions](tables/conditions.csv). Raw→derived exact artifact hashes are in [artifact manifest](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/artifact_manifest.json); producer revisions and input hashes in [full freeze](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/full_freeze.json). [Independent audit](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/independent_audit.json) records its own producer SHA256 and result SHA256.

## 6. Main results and eligibility

Decision-bearing values are above and in [result.json](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/analysis/result.json). Counts:2/2 frozen conditions,1 checkpoint/condition,4/4 worker receipts,192/192 paired records,zero exclusions,3/3 named coordinator gates,12/12 local-and-remote tests. Training-seed replications and interventions:0, not missing required conditions. Measurement and registered-branch PASS are separate from researcher mechanism judgment.

Distinct global atom coverage is not per-token support. SALL has a much longer rare-atom tail; the effective-count statistic shows why 17060 versus142 cannot be read as an equally sized ratio of typical usage diversity or native dimension. Equal K does not force equal global support. These observations do not measure dictionary-angle diversity, coefficient amplitudes or semantic content.

No semantic probes, Dense baseline, end-task performance, cross-layer comparison, training trajectory, K sweep or intervention were executed here. Synthetic plot checks remain debug-only under checks/synthetic_plot_only; no synthetic data enter the report.

## 7. Visualization evidence

![Primary evidence](figures/reuse_necessary_condition.png)

Purpose: expose both parts of the registered conjunction and distinguish frequency concentration from native variance. Left x-axis is Delta R with record-bootstrap95% CI; zero line is the registered null boundary. Center x-axis is descending atom-frequency rank (log scale), y-axis cumulative selected-slot frequency. Right x-axis is descending centered covariance direction rank, y-axis cumulative native variance. Blue SALL/orange S7; ranks independently sorted, not aligned IDs. Only the left panel has inferential uncertainty. Observed positive interval plus lower S7 PR yields the registered branch; the curves describe, not establish causation. Sources: primary/conditions tables and full-run concentration_curves.csv. Remaining uncertainty: contributions of support, decoder geometry, coefficient covariance and residual.

![Hypothesis versus observation](figures/intuition_vs_observation.png)

Purpose: prevent conflation of the hypothesized causal chain (left) and measured association (right). Values come from result.json, not invented projections. Arrow17.16→14.49 is a condition contrast, not time. The proposed reconstruction-pressure→reuse→dimension arrows remain untested; no mechanism promotion follows from this illustration.

PNG/PDF evidence copies are under this experiment's figures/. Date-local reading copies and provenance: [/data/250010109/Research_System/daily_research_reports/0922/figures/e01_reading_copy_manifest.json](../../../../../../../daily_research_reports/backup/2026/09/0922/figures/e01_reading_copy_manifest.json). Both inspected visually, copied byte-for-byte and hash checked; no debug figure promoted.

## 8. Stage evidence and failure decomposition

| Stage | Evidence | Outcome | What remains unresolved |
|---|---|---|---|
| F0 qualification | IDENTITY_PASS + smoke_v2 terminal/SMOKE_PASS +34 frozen files | PASS | Existing panel limits |
| F1 native extraction | Four receipts/support NPZ/checkpoint fingerprints | PASS | No causal manipulation |
| F2 alignment | ALIGNED_FULL_PANEL_PASS, exact smoke overlap and serial count equality | PASS | Article/seed independence |
| F3 registered computation | result.json, primary.csv, conditions.csv | Necessary-condition PASS | Geometry/covariance rival alive |
| F4 artifact closure | FULL_MEASUREMENT_PASS + manifest + durable pod log + platform SUCCEEDED | PASS | Human interpretation pending |
| Independent QA | independent_audit.json | PASS | Recomputing is not replication |

The first-smoke implementation defect was falsified/repaired by scalar/BF16 regression tests; it did not falsify a physical mechanism. Lower-dimension-plus-no-reuse-increase is not the observed result. No physical prior, causal model, or rival geometry mechanism is declared disproved. Same-ID reuse and geometric alignment can coexist.

## 9. Full round record (2026-09-22)

1. Question: whether the registered same-ID reuse prediction accompanies lower native dimension.
2. Setup: two frozen exact21B conditions, same inputs/site/K, native support and native means; no matched coefficient-only intervention.
3. Training data: no new training or update; historical checkpoint lineage recorded above.
4. Testing: inherited fixed192-record panel, including16 smoke-development records; no fresh sealed confirmation or new fit split.
5. Result: engineering PASS, registered necessary-condition PASS; direct contrast and aligned dimension in §5, all raw artifacts and failed-smoke trail retained below.
6. Insight/boundary: the required positive association is observed; this does not quantify or establish a causal contribution. Human judgment and the unchanged design-level next decision remain pending; proposed follow-up below is not an approved run.

## 10. Interpretation and claim boundary

Direct observation: same-panel reuse is higher and native dimension lower in S7. Approved mechanical mapping: necessary-condition PASS. Bounded reading: the registered prediction has not falsified this candidate. Unknown: whether support reuse contributes causally or dominates other mechanisms. Reweighted lineage/topology confounding, inherited-panel reuse, record-level uncertainty and unmeasured reconstruction-error covariance prohibit stronger claims. No statement about semantic improvement, model utility, optimal K, temporal learning dynamics or collapse follows.

## 11. Next decision and human judgment boundary

Exactly one existing decision remains for the researcher: whether same-ID reuse remains a viable candidate worth a discriminating geometry/coefficient-covariance control. AI recommendation: design that minimal control rather than add more descriptive count plots. Completion before new execution requires a constructible control, held-fixed objects, divergent predictions, residual boundary, stopping rule and explicit researcher confirmation. If the proposed control cannot distinguish explanations, stop expansion and redesign. Resume by reading summary_cn.md and completing the existing Focus's own judgment; no new job authorized here.

Researcher scaffold: confirmed/weakened explanation; current mechanism and reason; cannot-claim boundary; exactly one next decision. These are AWAITING_RESEARCHER, not AI-authored human conclusions. No paper-style final report or question closure is produced.

## 12. Artifact and execution map

| Artifact | Purpose / producer | Identity / completion / claim scope |
|---|---|---|
| full_freeze.json and source_snapshot | Submitted code/config/protocol/inputs | 34 SHA256 entries verified before result-document edits; preserve snapshot |
| worker_0..3/native_support.npz + receipt.json | Native extraction by frozen full_worker.py | All4 PASS, checksum verified in manifest |
| analysis/*_aligned.npz | Ordered usage/native mean arrays from checked full_analysis.py |192×30000 usage,192×1024 mean per condition; no labels |
| analysis/result.json | Registered outcome | SHA256 f870065438625f24ffcc3dcc1db5212932ebaa21f5b068dfc0e3e4c10e32ed4e |
| tables/primary.csv,conditions.csv,samples.csv,concentration_curves.csv | Primary plus descriptive tables | All present/hashed; only first2 curated here |
| figures/*.png,*.pdf,figure_manifest.json | Frozen build_full_figures.py | Primary and hypothesis-vs-observation only; hashes in reading_copy_manifest |
| artifact_manifest.json |22 raw/derived file identities | SHA256 a6cb0db097f64638aac7b8fc25ddb7229c6203b317adc2c6b3583f082f93b9ff |
| independent_audit.json | Postrun CPU algebra/hash audit | PASS; producer and result hashes recorded; not a new sample |
| terminal/stages/platform/pod logs | Execution/eligibility receipts | Completed,exit0; operational evidence not scientific mechanism |

Full run root: [/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z). Code workspace: [/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit); runner scripts/run_full.sh; fixed configuration run/full_config.json; data manifest manifests/full_inputs.json; native checkpoints §3; job `pt-5snx2hrj`. Durable pod log is under run/pod_logs/; complete stdout retained after platform exit. Inspect the same job, do not resubmit a completed experiment.

Application elapsed221.676s; four workers used RTX5090. Peak allocated/reserved3407407104/3535798272 bytes. SALL workers end-to-end193.06/193.13s, S7 88.43/88.44s, dominated by checkpoint loading. These are observer-extraction timings, not LM training throughput or model-quality results. No optimizer/checkpoint updates.

Read-only numerical reproduction:
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 /data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/scripts/audit_completed.py --run /data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z`.
No GPU rerun is needed to inspect or reproduce the stored primary statistics.

## 13. Record audit

PASS: contract/scope identified;34 original frozen files and22 outputs checked; both conditions and all guards present; primary values trace to raw observations; failed smoke preserved; primary interval and dimension audited independently; figures have sources and bounds; bilingual summaries agree. Human mechanism judgment remains explicitly scaffolded, not finalized. Frozen Protocol unchanged; current Anchor may receive only verified evidence and unchanged boundaries pending researcher interpretation. No commit, push, publication, unrelated-file edits or new experiment.

## Appendix: preserved chronological engineering ledger

The following is the original append-only execution trail, including superseded STARTING/NOT RUN snapshots and the failed first smoke. It is historical, not the current result state. Current result ownership is §§0–13 above.

### E01 shared-direction reuse audit — execution ledger

#### 0. Quick Recap

目的：确认“跨样本原子复用”的测量是否真正对应原生 SAE Top-32，完成四卡工程检查。

假设：科学问题是 S7 较低有效维数是否伴随更强同-ID复用；本次不裁定它。

实验思路：冻结 21B S7/SALL，在相同 16 个 N8 样本上读取同次前向的原子ID与原生均值表征；检查四 worker、身份、只读性与统计实现。

结论：任务 `pt-jztyb3sy` 已提交，已见四卡 pod 运行、SM120 runtime 与本地/远端单元测试通过、输入身份门通过；完整 smoke 仍待终态。

证据：[执行证书](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/smoke_4x5090_20260922T072342Z/execution_certificate.md)、[身份门](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/smoke_4x5090_20260922T072342Z/stages/IDENTITY_PASS.json)。科学分析 NOT RUN。

#### 1. Question / hypothesis tested

The authorized stage qualifies measurement identity and implementation. It does
not test the proposed scientific effect sign. See the owning [Protocol](protocol.md).
Core question/next decision remain owned by the 0922 Focus and subanchor.

#### 2. Setup and controlled variables

Exact 21B SALL original versus S7 reweighted; layer 8 native attention output
before residual; 30,000 atoms; K=32; 256 valid body tokens per input; batch 4;
BF16 forward/encode, FP32 pooling, FP64 statistics. Four workers are independent,
with two shards per model. No model training, labels, intervention or checkpoint mutation.
Resource profile 5090-4-spot, current registered image, existing mounted runtime.
The requested scope supersedes the prior stop only for implementation and smoke.

#### 3. Data and provenance

The source cache inventory verified 192 shared IDs / 49,152 body positions per
model, complete matching token/input identities, all observer chunk checksums
and the registered source-model files. Scientific reuse was not calculated on
that full panel. Smoke selects four original chunks by hash of their IDs,
indices 45/28/31/41, giving 16 examples per model. The old panel was historically
category-stratified; current selection and computation discard labels.

[Asset inventory](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/manifests/assets.json) preserves exact paths and hashes.
[Smoke inputs](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/manifests/smoke_inputs.json) fixes the bounded sequences.
[Pre-run file freeze](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/manifests/freeze_sha256.txt) covers scripts/config/owning documents.

#### 4. Development / confirmation boundary

This is an engineering development subset of previously inspected data, not a
sealed confirmation set. The candidate cosine metric, 2000-draw paired bootstrap
and future scientific rule remain AI_PROPOSAL. Smoke uses 64 draws only to
exercise the algorithm and always records NOT_EVALUATED for the scientific verdict.
No field in a submission or smoke receipt changes the researcher's scientific judgment.

#### 5. Results and conformance (current snapshot)

- Local: 6 unit tests PASS; Python compilation and shell syntax PASS; new-document
  links PASS; root/project diff whitespace checks PASS.
- Pod: frozen-file hashes PASS; existing torch 2.8.0+cu128/SM120 layer PASS;
  all 6 unit tests PASS; source identity gate PASS.
- GPU worker extraction, numerical checks and final terminal status: PENDING.
- Full scientific comparison: NOT RUN, not authorized.

##### Material measurement finding before execution

Old `observe_online.py` selects IDs with `scores.topk(128)`, then slices 32.
Native `sae.encode` uses `scores.topk(32)`. Rank32 equals rank33 for 11,716/49,152
SALL tokens and 2,545/49,152 S7 tokens in the audited caches; zero selected slots
were absent. This does not itself quantify native-ID mismatch. The new smoke
uses native encode and reports same-score discrepancies; it does not silently
reinterpret old selected-ID statistics as native support evidence.

##### Scope / deviations

This is a pre-execution measurement correction, not a post-result metric change.
No full scientific rule was promoted. No original training/observer code or old
E06 Protocol was modified. Root Focus only gained an explicit smoke-scope note;
execution envelope only gained the requested scoped four-5090 registration.
No commit, push, job stop of unrelated work, resource fallback or automatic retry.
Online `read_thread` is unavailable in this session's tool set. Context was read
from the supplied preview, repository chat export and full named memory; this
is not verification of the live chat or its original attachments.

#### 6. Insight boundary and next decision

Technical insight: atom-support identity is operation-specific at quantized
score ties; sorting more candidates and truncating is not guaranteed equivalent
to the native encoder. The magnitude and effect on reuse require measurement.
No claim about semantic benefit, causal regularization strength, effective-
dimension mechanism or language-model utility follows from this engineering stage.

Next operational action: inspect the same job's durable worker and terminal
receipts. No new submission is needed merely because monitoring ends. After
qualified smoke, return exact metric/panel/bootstrap decisions for researcher
confirmation before any full-panel scientific analysis.

#### 7. Execution receipt and artifact map

- Job: `pt-jztyb3sy`; retry count 0.
- Submission: `/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/smoke_4x5090_20260922T072342Z/submit-sae-reuse-smoke-4x5090-20260922T072342Z-20260922T072401Z.json`.
- Code: `/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/scripts/`; tests: `/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/tests/`.
- Run root: `/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/smoke_4x5090_20260922T072342Z`.
- Durable logs: `/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/smoke_4x5090_20260922T072342Z/pod_logs/` and four worker logs.
- GPU evidence: each worker's `receipt.json` (PENDING at this snapshot).
- Result gates: `stages/SMOKE_PASS.json` and `terminal_receipt.json` (PENDING).
- Monitor: this conversation's bounded startup observation; no recurring monitor.
- Completion-time estimate: no verified full worker timing yet; 900-second worker
  deadline is a safety cap, not a promised ETA.


#### 8. 2026-09-22T07:29:07.451655+00:00 — first smoke failed; scalar fingerprint repaired

Supersedes the startup-only PENDING snapshot above: `pt-jztyb3sy` is FAILED,
terminal exit 1 at 2026-09-22T07:26:36Z. Both S7 workers failed on a zero-dimensional
int64 SAE counter during tensor fingerprinting; the coordinator stopped its
own remaining workers. No support batch or mechanism result was produced.

Correction: flatten before reinterpreting bytes, fingerprint dtype and shape,
and add three regression tests. All nine CPU tests now pass. This does not
change scientific objects or rules. Failed job's original file snapshots are
preserved in `/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/smoke_4x5090_20260922T072342Z/source_snapshot_v1/`. Protocol A1 records the pre-rerun
amendment and the user's renewed “continue” authorization.

The failed terminal reports `gpu_used=false` because v1 defaulted that field
when no success receipt existed. Treat actual use as GPU model loading verified
from the error location, not as a CPU-only run. New failures record worker
GPU-memory evidence or unknown. No checkpoint was written or trained.


#### 9. 2026-09-22T07:32:39.777353+00:00 — corrected smoke submitted

Task `pt-1hi96knu` accepted on the identical 5090-4-spot / shphd-lite-0911 tuple;
latest platform state STARTING. Local regression count is 9 PASS. Same sample
manifest, checkpoints, mask, layer, K and scientific boundary. No full experiment.

[Corrected-run certificate](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/smoke_v2_4x5090_20260922T072907Z/execution_certificate.md).
[Run root](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/smoke_v2_4x5090_20260922T072907Z); pre-submit file hashes and local test receipt are copied there.
The old failed job is retained rather than overwritten or reported as passed.


#### 10. 2026-09-22T07:34:17Z — bounded startup handoff

Latest platform snapshot: corrected job `pt-1hi96knu` is STARTING; its single
four-GPU worker is Pending with a host assigned. No durable pod/worker execution
log or v2 SMOKE_PASS/terminal receipt is available yet. This confirms accepted
submission and scheduling progress, not a passed smoke. Queue/image-startup ETA
is unknown; the 900-second worker cap only begins inside the application.

All 17 frozen files were rechecked and copied into the corrected run's
`source_snapshot_v2/`; local nine-test suite, syntax, whitespace and document
links pass. Stop monitoring after this bounded startup window. Leave this same
job queued/starting; do not resubmit or switch resources. Resume by inspecting
its existing platform snapshot and durable receipts, then decide whether any
further engineering repair is needed. Formal scientific analysis remains NOT RUN.


#### 11. 2026-09-22T07:44:51.205512+00:00 — Smoke qualified and full scope confirmed

Corrected smoke `pt-1hi96knu` completed at 2026-09-22T07:39:42.996634+00:00: terminal PASS,
all four worker receipts PASS, 16 paired records per model, zero optimizer updates.
Application time 186.92s; peak allocated/reserved bytes
3407407104/3535798272. All tested native
Top32 versus top128-prefix32 unordered supports matched (zero mismatched tokens
in 4096 tokens per model). Thus ties were a legitimate risk, **not an observed
support mismatch** in smoke. Native encoder remains the correct measurement path.

The researcher explicitly confirmed the complete proposed metric/panel/bootstrap
criterion and requested the pass-gated full experiment. Protocol A2 and the
Anchor/Focus now own that decision; scientific results remain unobserved.
All 12 local tests pass, full aggregator reproduces the qualified smoke counts
and overlap exactly, and synthetic-only figure rendering passes. Full worker
only expands the qualified original batch list/shard span; model computation
and numerical tolerances are unchanged. No full signed statistic opened locally.


#### 12. 2026-09-22T07:45:42.404950+00:00 — full submitted

Task `pt-5snx2hrj`, current initial state STARTING; approved A2 scope,
4xRTX5090 Spot, registered current image and mounted runtime. Qualified smoke
required and passed. No model/dataset/metric changes since A2 freeze.
[Full execution certificate](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/execution_certificate.md).
Source and contract snapshots are under `/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/source_snapshot`; no scientific
contrast is available yet. The current user requests terminal experiment
completion, so this task is followed through receipts rather than startup only.
