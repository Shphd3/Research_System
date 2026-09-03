---
experiment_id: A15_12_E03_tax_c4a_unseen_fact_package_transfer
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN_AFTER_RESOURCE_SELECTION
execution_status: NOT_RUN_RESOURCE_SELECTION_PENDING
created: 2026-08-30
primary_anchor: A15_12_semantic_representation_separability
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
authorization_basis: direct request to execute the separability audit without iterative Anchor or Protocol approval
resource_profile_candidate: four_rtx5090_model_parallel_extraction_then_cpu_frozen_probe_evaluation
forbidden_resource: H100
evidence_role: new_fact_package_transfer_stress_test
---

# Protocol: TAX-C4A New-Fact-Package Transfer

## 0. Decision Question

Do the 60 linear probes frozen in E01 from C4E-A retain multigranular
semantic readout on TAX-C4A, which assigns the same 64 semantic leaf labels
to a different six-atom fact package per leaf?

This is the third and final core experiment of the current representation
audit. It tests whether E01 merely read fixed-fact signatures. It does not test
whether the facts were unseen during Qwen pretraining, and it is not a clean
single-variable intervention because TAX-C4A also changes length and surface
naturalness.

## 1. Frozen Objects

### 1.1 Model and representation

- Model: the same frozen Qwen3-30B-A3B checkpoint used by E01.
- Registered blocks: 4, 12, 20, 28, 36, and 44.
- Representation: `args[0][:, -1, :]` at each registered
  `model.model.layers[layer-1].mlp` forward pre-hook.
- This is the 2,048-dimensional actual MLP/Gate input at the final colon in
  `Classification:`, before native Gate logits, top-k truncation, or experts.
- The decision-token ID must be 25 for every row.

### 1.2 TAX-C4A panel

- Source:
  `/data/250010109/MoE_Router/experiments/20260820_a15_07_e01_dual_track_heldout_spectrum/data_v1/controlled_c4_atom.jsonl`.
- Frozen source SHA-256:
  `cab867c3394d047822b896f6339412aa4b9d2568474715fa3f624767429f8226`.
- Expected composition: 1,920 rows, 8 parents, 8 children per parent, 30
  complete 64-leaf template families, and six new atomic propositions for each
  leaf.
- The 384 TAX-C4A atoms must have zero exact atom-hash overlap with C4E/C5E.
- Each semantic leaf has one new six-atom fact package; its 30 rows vary only
  template and atom order. Therefore family resampling does not estimate
  uncertainty across fact packages.

### 1.3 Frozen probes

- Source run:
  `A15_12_E01_qwen3_30b_fixed_fact_expression_separability/runs/full-20260830T172302Z`.
- Model-ledger SHA-256:
  `8f5485d185745992cd16984c34a005da0458e40b3f9ca62cd0fa7511f621073c`.
- Frozen model-content bundle SHA-256:
  `45343f748b9c81b3feaca5ccb1774edfd6eb788f16dc8031700ccd414c01061b`.
- Evaluate the parent head `P`, global 64-way head `J`, and all eight
  parent-conditional fine heads `F_0` through `F_7` at every registered block.
- Do not fit a normalizer, select a penalty, refit a head, calibrate a
  threshold, or inspect labels to alter the probes.

## 2. Four-Part Experiment Account

### 2.1 Core question

Does a C4E-A semantic readout remain usable when both the concrete fact package
and the generated text surface are replaced by TAX-C4A?

### 2.2 Purpose and completion standard

The experiment is complete only if:

1. extraction identity, hashes, shape, finite values, row order, and a replay
   subset all pass;
2. all 60 frozen heads produce the expected 34,560 prediction rows
   (`6 layers * (1,920 P + 1,920 J + 8 * 240 fine)`);
3. all 60 task cells and six all-task layer bottlenecks are present; and
4. the registered uncertainty and sensitivity artifacts are complete.

### 2.3 Analysis in at most three steps

1. After the researcher confirms the exact resource, extract the six registered
   representations with the audited four-RTX5090 candidate path, first with a
   small replay smoke and then the full 1,920-row panel. An eight-card choice
   requires a separately frozen and audited submission path.
2. Apply the 60 frozen E01 probes and their frozen C4E-A mean/RMS scale without
   any TAX-C4A fitting.
3. Report task-level accuracy and geometric margins, then locate which
   semantic granularity, parent, layer, and template families own any failure.

### 2.4 Outcome branches

- **Transfer established at a layer:** every one of its ten tasks has a
  positive simultaneous lower bound for the all-task fifth-percentile margin.
  This supports transfer to this one additional fact package per leaf despite
  its surface shift. It does not prove general unseen-fact invariance.
- **Transfer not established at a layer:** at least one task has a non-positive
  all-task lower bound. This shows that the frozen C4E-A readout is not robust
  on the joint TAX-C4A shift. It does not identify whether the cause is fact
  identity, longer context, masked wording, punctuation artifacts, or their
  interaction.

## 3. Extraction Contract

Only 4 or 8 RTX5090 GPUs are allowed; H100 is forbidden. The only currently
frozen operational candidate is 4x RTX5090 because it has a completed
historical extraction receipt and an independently audited submission wrapper.
No GPU job has been created. Execution remains blocked until the researcher
confirms the exact card count. Choosing 8x requires a Protocol operational
amendment plus a separately frozen and audited submission wrapper. For the 4x
candidate, use one process with model parallelism, run a fresh batch-1 or
batch-2 replay smoke, then use batch 4 for the full panel unless the smoke
requires a lower value.

The extractor must be parameterized by panel ID, source path, source hash,
output path, expected GPU count, and batch size. It must not call the old
A15_09 analysis pipeline. Resume is allowed only for an incomplete run whose
source-code bundle, model files, tokenizer files, source data, layer list, and
batch settings match exactly.

Expected activation artifact:

- shape `[6, 1920, 2048]`;
- dtype `float32`;
- exactly 94,371,968 `.npy` file bytes, comprising 94,371,840 array-payload
  bytes and a 128-byte header;
- all values finite;
- row order identical to the frozen metadata;
- decision-token IDs equal to `[25]`;
- observed token-length range recorded (preflight expectation 145--320);
- replay maximum absolute error at most `1e-6`.

Freeze the model `config.json`, weight-index, tokenizer, extractor-source, and
output hashes in the completion manifest.

## 4. Metrics and Uncertainty

For each layer and task report balanced accuracy, chance-corrected gain,
negative log likelihood when recoverable from the frozen model, normalized
geometric margin fifth percentile, median, strict minimum, and non-positive
margin rate. The normalized margin must use the frozen E01 C4E-A isotropic RMS
scale. Also report raw-activation distance as normalized margin multiplied by
that frozen positive scale.

The registered layer statistic is the minimum task-level fifth-percentile
margin across `P`, `J`, and all eight fine tasks. Resample the 30 complete
template families 10,000 times with one shared family draw across every layer
and task. Construct a one-sided simultaneous lower band across the six layer
bottlenecks using the same studentized max-statistic procedure as E02. Fail
closed if any bootstrap standard error is numerically zero.

Report, descriptively:

- the parent and fine tasks owning each bottleneck;
- the largest directed confusions;
- per-family error ranges;
- parent, pooled-fine, and joint trajectories over the six blocks; and
- paired raw-unit bottleneck differences from the frozen E01 C4E-B reference
  using shared task definitions, with the explicit warning that the panels do
  not share template-family identities.

The last comparison is descriptive and is not a paired-family causal contrast.

## 5. Guards and Failure Policy

- Run unit tests and a source-hashed preflight before submission.
- A smoke tests extraction identity only; it is not a scientific result.
- Abort on any source/data/model/tokenizer hash mismatch, wrong GPU type or
  count, H100 allocation, row-order mismatch, wrong tensor shape, non-finite
  activation, decision-token mismatch, or replay failure.
- Preserve an interrupted SPOT run and resume only after validating its
  manifest. Never overwrite a completed run.
- Full stdout/stderr, job ID, resource tuple, timestamps, code hashes, and all
  output hashes belong in the detailed evidence record.

## 6. Claim Boundary

### Allowed

Within this frozen checkpoint, representation position, six layers, taxonomy,
one new six-atom package per leaf, generated TAX-C4A surface, and frozen E01
linear heads, report whether multigranular transfer is established and where
its low-tail bottlenecks occur.

### Forbidden

- that TAX-C4A was unseen during Qwen pretraining;
- clean causal attribution to fact identity;
- universal semantic separability or intrinsic non-separability;
- low-rank or sample-efficient Router realizability;
- native Gate use, top-k accessibility, expert utility, or language-model gain;
- publication readiness from this stress test alone.

## 7. Outputs

- immutable extraction run with manifest and logs;
- immutable frozen-probe evaluation run;
- `summary.md` and `detailed.md` beside this Protocol;
- task cells, six bottlenecks, predictions, confusions, bootstrap draws,
  sensitivity tables, figures, source hashes, and completion audit;
- Chinese white-language explanation in
  `daily_research_reports/backup/2026/08/0830/docs/semantic_representation_separability/`.
