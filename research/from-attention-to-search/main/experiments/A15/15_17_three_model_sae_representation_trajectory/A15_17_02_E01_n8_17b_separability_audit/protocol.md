# A15_17_02_E01 Protocol: Exact-17B N8 Native Separability Audit

```yaml
document_state: APPROVED_FOR_IMPLEMENTATION_AND_SMOKE
approved_scopes: [implementation, smoke]
full_run_approved: false
approval_source: researcher instruction, 2026-09-22
anchor: ../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_02_sae_n8_separability_anchor.md
focus: ../../../../../../../Projects/from-attention-to-search/main/focus/focus_sae_n8_separability.md
execution_surface: acp
resource_profile: h100-4-reserved
image_id: shphd-lite-0911
env_layer: /data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/scripts/runtime.sh
execution_workspace: /data/250010109/MoE_Router/experiments/20260923_sae_n8_separability_audit
```

Scientific content and registered criteria freeze when the authorized Smoke is
submitted. Post-start edits are limited to execution receipts, result links, or
an append-only amendment that records eligibility impact.

## Purpose

Determine whether the concentration difference already observed among exact-17B
SAE histories is accompanied by stronger held-out N8 domain readability in the
native layer-8 attention write, and whether either SAE condition is better than
an exact-17B Dense checkpoint.

## Hypothesis

The primary hypothesis is that fresh coefficient-0.1 S7 has higher N8 test
accuracy than Dense. The strongest rival is that SAE history changes shared
directions, scale or dictionary use without improving native domain distinctions.
The secondary history contrast is reweighted 1→0.1 minus fresh 0.1. It is
directional only after measurement and is not an isolated coefficient effect.

## Analysis Method

Extract identical frozen N8 inputs through the three exact-17B checkpoints and
cache native layer-8 mean and last-body-token writes. Fit a frozen L2 multiclass
linear reader on fit data, choose `C` on development data, and evaluate test
accuracy. Report same-test effective dimension and between/within scatter;
fit fixed K-means without labels and report test adjusted Rand index. Use paired
class-stratified bootstrap intervals for model differences. Smoke uses a
preselected 16-record subset and synthetic arrays only.

## Pre-registered Conclusion Branches

- A positive primary interval supports a bounded linear-readability advantage;
  distance grouping requires concordant ARI or scatter evidence separately.
- A negative interval under greater concentration opposes the claim that
  concentration is inherently useful for N8 separability.
- An interval crossing zero leaves direction unresolved and is not equivalence.
- Identity, data, hook, mutation, leakage or analysis-invariant failure yields
  `INELIGIBLE` and no scientific verdict.

## A. Question And Claim Boundary — CONFIRMED

The Anchor's sole question, H1/H2 split, primary contrast and cannot-claim
boundary govern. Smoke is engineering evidence only. It may not be reported as
model quality, semantic improvement, clustering improvement or mechanism evidence.

## B. Data Construction And Provenance — CONFIRMED

Primary data are the immutable files under
`20260920_sae_representation_21b_audit/data/N8_v1`: eight named categories,
fit/dev/test counts 2,400/800/1,600 and 256 frozen input tokens per record. The
implementation records file hashes, manifest hash, label map, input-token hash,
sample ID, source-group ID and content mask. It must prove split disjointness for
IDs and available hashes. Test labels are forbidden from preprocessing, `C`
selection, clustering fit or initialization selection. The old 192-record panel
is not a substitute. If `N8_v1` fails identity, the full experiment stops; this
Protocol does not authorize constructing `N8_sep_v2`.

## C. Learning Task And Supervision — CONFIRMED

The analysis-only learning task maps a frozen native write to one of eight N8
source categories. Inputs are only cached vectors; fit labels train the reader,
development labels select `C`, and test labels are confirmation-only. Invalid,
nonfinite, zero-scale or nonconverged candidates are rejected under the fixed
rules. No backbone, SAE or tokenizer parameter receives gradients.

## D. Model And Architecture — CONFIRMED

Roles are exact-17B Dense, exact-17B final-layer S7 trained with coefficient 0.1
throughout, and exact-17B final-layer S7 reweighted from 1 to 0.1 near 15.47B.
All are the custom eight-layer, width-1,024 model lineage. The native tensor is
layer index 7 after attention output projection and before residual addition.
Mean over 256 body positions is primary; last body position is sensitivity-only.
S7 reconstruction mean may be collected in the same forward pass; Dense receives
no newly fitted dictionary.

## E. Objective And Optimization — CONFIRMED

The reader is scikit-learn multiclass logistic regression with `solver=lbfgs`,
L2 penalty, intercept, no class weights, `C=[0.01,0.1,1,10,100]`, `tol=1e-6`
and `max_iter=10000`. Ties in development accuracy select smaller `C`; a
nonconverged candidate is retried once at 20,000 iterations and otherwise
rejected. Fit-only preprocessing subtracts the per-dimension mean and divides by
one global RMS scale. Development is not added back to fit.

## F. Evaluation, Statistics And Decision Rule — CONFIRMED

The primary metric is mean-pooled native test accuracy. Full mode registers
fresh-0.1 minus Dense and reweighted minus fresh-0.1. Each receives a 97.5%
percentile paired-bootstrap interval for directional declarations, using 2,000
draws, seed 20260923 and linear quantiles. A 95% interval is also reported. If
Dense is not identity-qualified before analysis, pair-only mode keeps only the
history contrast with a 95% interval; either missing S7 stops the experiment.

Descriptive test geometry is effective dimension, top-16 variance share, total
variance, and `B/W`. K-means uses eight clusters, k-means++ initialization,
`n_init=20`, `max_iter=300`, `tol=1e-4`, Lloyd algorithm and outer seeds
`[17,29,43,71,97]`; centers fit without labels on fit vectors and assign test
vectors. ARI and `B/W` are explanatory and do not replace the primary rule.

## G. Controls And Failure Handling — CONFIRMED

Guards cover manifest and state identity, exact token coordinate, identical
cross-model sample order/input hashes/masks, native-site residual identity,
manual-versus-helper pooling, single-versus-batch consistency, repeat-forward
determinism, unchanged state tensors and version counters, finite caches, split
leakage, and confirmation isolation. Synthetic tests require scale invariance of
`B/W`, effective dimension and top-16 share; explicit zero-variance status; ARI
invariance to cluster-ID permutation; row/ID mismatch rejection; and successful
linear readout on a known separable array. Failures are recorded, never repaired
by changing samples, layer, pooling, classifier family or thresholds.

## H. Execution And Reproducibility — CONFIRMED

Submission uses `templates/execution/acp_submit_template.sh`, resolves the
declared profile/image, runs one four-worker ACP node, and writes pod logs plus
an execution certificate under the experiment run directory. The Smoke assigns
one exact checkpoint role to each of three GPUs and a deterministic repeat of
one S7 role to the fourth. Each worker checks two development records per class,
for 16 records total; the fourth worker independently repeats the same S7 inputs.
No optimizer is instantiated and `optimizer_updates=0` is required.

Smoke pass requires all G guards; correct role/token identities; all three model
loads; 16 records and 4,096 body tokens per worker; finite mean/last writes;
repeat S7 agreement within the production dtype tolerance; creation and reload
of contract-compliant NPZ caches; all synthetic analysis tests; peak allocated
and reserved memory plus valid-body-tokens/s recorded. Smoke failure blocks any
full submission. Full execution requires a separate explicit authorization.

Expected Smoke artifacts are `resolved_assets.json`, `source_reuse_map.json`,
data and cache manifests, per-worker receipts and caches, `SMOKE_PASS.json` or
`SMOKE_FAIL.json`, pod log, terminal receipt, and execution certificate.

## Cross-Block Consistency Audit — PASS

Data roles match the task; architecture precedes no undefined objective; the
native tensor matches the Anchor; confirmation labels cannot affect fitting;
the primary metric and bootstrap rule adjudicate H1 versus H2; sensitivity and
clustering cannot redefine success; execution is analysis-only and Smoke scope
cannot create a scientific result. All blocks A-H are `CONFIRMED` by the
researcher's explicit authorization of all named components, while full-run
scope remains unapproved.

## Approval And Freeze Record

```text
2026-09-22: researcher authorized Anchor, Protocol, implementation and Smoke.
2026-09-23: canonical Protocol written as APPROVED_FOR_IMPLEMENTATION_AND_SMOKE.
Full analysis: NOT AUTHORIZED by this record.
```

## Amendment A1 — Smoke execution surface after quota rejection

```text
time: 2026-09-22T18:19:05Z
before: one h100-4-reserved ACP node, four roles in parallel
platform result: CREATE_FAILED before job creation; member quota remaining 0 GPU / 0 CPU
after: current local H100 80GB MIG 3g.40gb, the same four roles run in separate sequential processes
reason: complete the already authorized bounded Smoke without changing model, data, metric, threshold or scientific scope
eligibility impact: engineering qualification only; cross-process repeat remains checked; parallel-worker simultaneity is not claimed
full-run impact: none; full execution remains unauthorized
```

## Execution Status

```text
smoke_status: PASS
smoke_surface: local H100 80GB HBM3 MIG 3g.40gb, four sequential processes
scientific_verdict: NOT_EVALUATED
full_run_status: NOT_RUN
receipt: /data/250010109/MoE_Router/experiments/20260923_sae_n8_separability_audit/runs/smoke_local_h100mig_20260923T0025Z/stages/SMOKE_PASS.json
```

## Amendment A2 — One direct 4×RTX5090 Spot full audit

```text
time: 2026-09-23T01:05:44Z
before: full execution was not authorized; the declared resource profile was h100-4-reserved
after: exactly one full read-only execution is authorized on 5090-4-spot with shphd-lite-0911 and the mounted SM120 runtime layer
reason: the researcher explicitly requested immediate 4-card RTX5090 Spot submission and explicitly declined any additional Spot Smoke
prior engineering evidence: the bounded local H100 Smoke passed all registered correctness guards; an existing exact-17B S7 4xRTX5090 read-only run on the same image/runtime recorded 1,763,197,952 peak allocated bytes, 1,883,242,496 peak reserved bytes, 281.0-286.4 valid body tokens/s end-to-end and zero repeat RMS; the established Dense loader has separately executed on this 4xRTX5090 runtime lineage
target-run guards: assert four RTX5090 devices and >30 GiB/device; revalidate frozen data/source/checkpoint identities; record per-case peak allocated/reserved memory and end-to-end valid-body-token throughput; prove no model-state mutation and zero optimizer updates; fail closed on any worker, cache, alignment, finite-value, analysis or artifact failure
affected blocks: H execution resource and scale-up route only; A-G scientific question, data, conditions, metrics, thresholds, exclusions and claim boundary are unchanged
data visible before amendment: engineering Smoke receipts only; no full N8 scientific outputs existed
approval: researcher instruction in this conversation, 2026-09-23
result eligibility impact: none if all embedded target-run guards and the frozen Protocol pass; any failed or missing guard makes the affected result INELIGIBLE
excluded authority: no extra Spot job, training, checkpoint mutation, resource fallback, automatic retry, commit, push or publication
```

```text
full_run_approved: true
approved_full_scope: one 5090-4-spot full read-only N8 audit
additional_spot_smoke: NOT_RUN_USER_DECLINED
scientific_verdict: NOT_EVALUATED
full_run_status: APPROVED_NOT_YET_SUBMITTED
```

## Execution Receipt A2-R1

```text
submitted_at: 2026-09-23T01:14:59Z
job_id: pt-3nidnrq0
job_name: a15-17-02-e01-n8-17b-full-4x5090
resolved_tuple: 5090-4-spot / computing-cluster-5090-01g / n12lp.nn.i10a.4 / one node / four RTX5090 / Spot / shphd-lite-0911
run_root: /data/250010109/MoE_Router/experiments/20260923_sae_n8_separability_audit/runs/full_4x5090_20260923T011428Z
submission_receipt: /data/250010109/MoE_Router/experiments/20260923_sae_n8_separability_audit/submission_receipts/full_4x5090_20260923T011428Z/submit-a15-17-02-e01-n8-17b-full-4x5090-20260923T011457Z.json
execution_certificate: /data/250010109/MoE_Router/experiments/20260923_sae_n8_separability_audit/submission_receipts/full_4x5090_20260923T011428Z/execution_certificate.md
retry_count: 0
startup_state_at_2026-09-23T01:15:13Z: STARTING; worker Pending
full_run_status: SUBMITTED_STARTING
scientific_verdict: NOT_EVALUATED
```

## Execution Receipt A2-R2 — Terminal Status

```text
completed_at: 2026-09-23T01:30:33.733903Z
platform_state: SUCCEEDED
terminal_status: PASS
exit_code: 0
completed_model_roles: 3/3
records_per_role: 4800
valid_body_tokens_per_role: 1228800
optimizer_updates: 0
execution_deviation: the allocated four-GPU node ran three independent model-extraction processes because the scientific matrix has three model roles; the fourth GPU was unused during extraction
eligibility_impact: none; all registered model conditions, data splits, primary and sensitivity analyses, artifact guards and terminal receipts completed
result_root: /data/250010109/MoE_Router/experiments/20260923_sae_n8_separability_audit/runs/full_4x5090_20260923T011428Z
full_gate: stages/FULL_MEASUREMENT_PASS.json
terminal_receipt: terminal_receipt.json
primary_outputs: analysis/primary_metrics.json; analysis/paired_statistics.json; analysis/test_predictions.jsonl; analysis/cluster_predictions.jsonl
scientific_verdict: AWAITING_RESEARCHER
```
