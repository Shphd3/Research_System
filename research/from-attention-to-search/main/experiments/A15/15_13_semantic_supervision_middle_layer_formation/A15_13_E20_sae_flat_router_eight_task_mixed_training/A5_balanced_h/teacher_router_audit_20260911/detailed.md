# A5 teacher and frozen-router audit: evidence ledger

[Summary](summary.md) · [Chinese reading](summary_cn.md) · [Contract](protocol.md) · [Text examples](teacher_examples_cn.md)

## Execution and authority

Execution status: COMPLETE for the two requested local stages. The researcher authorized this narrow audit in conversation. Interpretations remain AI audit judgments; no Focus or Anchor scientific transition was made. No expert, backbone, or SAE training, remote submission, or downstream capability evaluation occurred.

The implementation used an already attached H100 MIG 3g.40GB device, eight CPU threads, Python 3.10 and PyTorch 2.3, with TF32 disabled. This was isolated cached-representation analysis. The contract is retrospective with respect to previously visible A5 diagnostics, not a preregistration.

## Frozen inputs and provenance

Original A5 run: `/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z`.

Inherited cache/group lineage: `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z`.

The audit verified 55 relevant frozen source/group/router assets against the A5 manifest, matching inherited group digests and cache manifests. All 78 router and 34 development shards were hash-checked when consumed. Discovery/router/development/test record IDs and content hashes are disjoint. Full base-model weights were not rehashed: provenance verification covers the cached inputs and listed assets, not bitwise identity of the entire historical environment.

The captured representation is the layer-27 MLP pre-input, dimension 1024, matching the original SAE training hook. The fixed SAE has 30,000 features and top-32 activation. Eight groups contain 29,471 features; 529 features are excluded. Discovery contains 19,784 records / 23,520 nonpadding segments; router training contains 19,787 records / 1,303,384 answer-prediction positions; development contains 8,480 records / 572,496 positions.

For each position, group mass is the sum of retained positive SAE activations in the group; q is this mass divided by total retained mass. Every development position has a valid target. Retained activation mass is 0.9136420432 of all positive activation mass. No balancing bias modifies q or the fresh router.

## Stage 1: structure and readable examples

Five clustering seeds (17, 29, 43, 59, 71) rerun clustering on the fixed affinity; feature ARI ranges from 0.9997932541 to 1. These are clustering seeds, not independently trained SAE seeds.

Three full-record bootstrap repetitions (20260907–20260909) reconstruct the original grouping pipeline. Feature ARIs are 0.7578525947, 0.7312082397 and 0.7797423588. Feature retention exceeds 99.74%. Group labels are aligned by Hungarian matching on feature contingency; on 8,192 fixed development positions, maximum-q label agreement is 0.9592285156, 0.9718017578 and 0.9588623047. Mean absolute change in pairwise teacher cosine similarity on 20,000 fixed pairs is 0.018304819, 0.015292194 and 0.018357620. These pair samples are descriptive, not independent statistical replicates.

These three bootstrap seeds reproduce the first three historical repetitions, rather than adding three independent historical replicates. The older audit has 14 recorded repetitions and an AUDIT_RUNNING label; this record does not claim that its planned 20 completed. Its unproven graph-rewiring null is not used here.

Twenty random feature partitions (seeds 2718–2737) preserve group sizes and approximately match feature frequency through ten frequency bins. On the same 1,329,290 discovery-selected held-out feature edges, the original within-minus-between coactivation correlation is 0.0592515533; random gaps range from −0.0034168387 to −0.0000507680. The rank 1/21 is descriptive and is not evidence of semantic validity. Accelerated correlation calculation matches the original within/between values within 4e-10.

Text extraction selects 12 distinct records per group by raw activation mass, plus five by relative q. The Chinese example document displays the first three raw-mass examples and one relative-q example, with causal prefix, target token and position identifiers. The target token aids reading and is not an input to the router. Formula markers and drawing-code patterns are visible, but coherent task semantics are not established for all eight groups. In particular, the highest raw-mass group-1 examples all have a colon/newline visible prefix.

Group-1 and group-3 account for 98.587% of development maximum-q labels. Equal weighting of records still places almost all labels in these groups, so long math answers alone do not explain the imbalance. Development group counts are [126, 241037, 5859, 323371, 1961, 116, 24, 2].

The operational gate allows a bounded imitation test because provenance, nonrandom coactivation structure and target stability are supported. It does not certify eight semantic categories. A stricter requirement that every group be semantically named is unresolved, not passed.

An ancillary SAE reconstruction/parity check uses the first 1,024 positions of the sorted random probe: cosine 0.92621, reconstruction energy ratio 0.13597, q maximum absolute difference 9.37e-5 and maximum-q agreement 1.0. Sorting before truncation biases this subset toward earlier positions; these are local implementation checks, not a representative held-out SAE quality estimate.

## Stage 2: isolated linear imitation

One fresh seed-17 linear layer (1024 inputs, eight outputs; 8,200 parameters) minimizes KL(q||softmax(Wh+b)). Adam learning rate is 0.001, batch size 4,096, gradient clipping 1, no ridge penalty. Twenty epochs give 6,380 updates, with deterministic global position shuffling. Only weight and bias enter the optimizer; h and q have gradients disabled. The best checkpoint is selected by minimum training KL (epoch 20), without development selection. Best/final checkpoints and parameter deltas are recorded.

| Model | Train KL | Development KL | Train argmax agreement | Development argmax agreement |
|---|---:|---:|---:|---:|
| Fresh seed17 | 0.04601031 | 0.04649459 | 0.92152505 | 0.91914878 |
| Original seed17 replay | 0.05535621 | 0.05561557 | 0.90521366 | 0.90395042 |
| Original seed29 replay | 0.05398525 | 0.05418237 | 0.88683458 | 0.88610226 |
| Original seed43 replay | 0.07352705 | 0.07333292 | 0.79178124 | 0.79259418 |

The constant training-mean target has development KL 0.21212237; the majority-label baseline agrees on 0.56484412. Fresh development KL is 78.08% lower than the constant baseline. Initial fresh train/development KL was 2.30706/2.30457. The original three checkpoints are replays, not three new training runs; their historical validation-based selection and ridge settings remain unchanged. Replayed KL differs from saved results by less than 3.1e-9; seed29 changes one argmax among 572,496 positions, consistent with a numerical near tie.

Development recall by group is [0.35714, 0.90021, 0.62127, 0.94144, 0.52371, 0.54310, 0.70833, 0]. Group7 has zero maximum-q training positives but nonzero soft target mean (0.00614557); it has only two development positives. Its zero recall does not establish insufficient model capacity. On the same seven groups with training positives, train/development macro recall is 0.63412/0.65646. The all-eight development macro value is 0.57440 and uses a different denominator.

For development targets with top-two q margin at least 0.1, 439,407 positions have agreement 0.98182094. For margin below 0.01, 13,224 positions have agreement 0.51035994. Thus some argmax errors occur near ambiguous boundaries. Neither these observations nor a single optimization run establish a linear expressivity ceiling or global optimum.

## Failures, corrections and terminal receipts

- Initial teacher extraction failed because tokenizers was not on the process import path. The retry adds the existing local transformer environment to that process path; no package installation occurred. Failure JSON and log are retained.
- The successful extraction initially reported an erroneous zero retained-mass diagnostic because an FP16 sum overflowed. Recalculation from original shards with float64 summation gives 0.9136420432. The correction JSON records the old value and reason. Targets, examples and grouping results were unaffected. The implementation now uses float64 for this statistic.
- Initial router execution replayed old checkpoints, then failed during optimizer import due to ONNX/protobuf descriptor incompatibility, before fresh training. Retrying with `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` completed; no global environment changes occurred. Both logs and failure JSON remain.
- Successful receipt elapsed times: teacher 17.563 s; stability 155.737 s; random comparison 6.064 s; router 43.646 s including input loading and old-checkpoint replay. These are per-stage timings, not total wall time including analysis and failures.
- Each stage receipt identifies the source version used then. The initial input identity and teacher receipt predate import/statistic fixes; they must not be read as hashes of the final source. The completion receipt hashes final code and outputs separately.

Verification includes source compilation, an exact label-permutation toy check (ARI 1, target total variation 0, relation change 0), agreement of reconstructed q with the original soft-target function, full-cache counts and hashes, and saved terminal completion receipts. Plot copies and document links are checked separately at completion.

## Artifact map and evidence boundary

All raw outputs, code, checkpoints and logs remain in the execution workspace:

/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/audits/teacher_router_20260911

| File(s) | Role |
|---|---|
| input_identity.json; *_cache_hashes.json | Frozen asset provenance and full consumed-cache hashes |
| audit.py; router_audit.py; render.py | Audit, isolated training, and presentation implementations |
| teacher_profile.json; teacher_examples.json; source_record_balanced_usage.json | Target usage, source text and record-weighting diagnostic |
| group_stability.json; maps/; teacher_probe.npz | Cluster/bootstrap results, mappings, fixed probe |
| random_comparison.json; heldout_edges.npz | Matched random partitions and held-out edge comparison |
| teacher_gate.json; sae_reconstruction.json | Bounded execution gate and ancillary parity check |
| router_results.json; fresh_router_*.pt | Complete curves, per-group/margin metrics and new checkpoints |
| *_receipt.json; *_failure.json; *.log; retained_mass_correction.json | Completion, failures, stage source hashes and correction trail |
| completion_receipt.json | Final artifact hashes |

[Teacher figure](figures/teacher_audit.png) and [router figure](figures/router_audit.png) are evidence copies. The date-local reading copies and their sources live under `daily_research_reports/0911/0911_a5_teacher_router_audit/figures/`.

Direct evidence supports stable nonrandom coactivation structure and substantial linear imitation without a gross train/development gap. Semantic validity of all groups, expert utility, downstream capability, and the cause of A5 task performance remain unresolved. Any next scientific decision belongs to the researcher; the Summary labels its proposed clarification as AI advice.
