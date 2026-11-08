# Predefined fact-level analysis interface (qualification amendment v2)

This CPU-only code aggregates frozen scores. It does not load a model, alter a
score rule, select methods, or make an architecture judgment. It was implemented
from `../user_execution_contract.md`, `../dev_execution_plan.json`, evaluator
source schemas, and the training observability contract **without reading any
actual model outputs**. NumPy is the sole non-standard dependency.

```bash
python analysis_tools/v2/aggregate_facts.py --manifest MAPPING.json --out NEW_STATISTICS_DIRECTORY
python -m unittest -v test_aggregate_facts.py
```

The test command runs from `analysis_tools/v2`. The root v1 files and their original hashes are preserved unchanged. Only synthetic CPU fixtures are
created in temporary directories and automatically removed. An existing
nonempty statistics output directory is never overwritten. Input paths in a
mapping are relative to that mapping's location, or absolute. Missing path globs
are errors. `example_mapping.json` is a schema example with deliberately
placeholder paths, not an assertion that formal runs already exist.

## Frozen endpoints and strata

The primary endpoint is **both fixed held-out forms correct for a fact**.
`original`, the training wording, is secondary. Raw rank outputs reconstruct
True/False/Unknown; `fact_scores.jsonl` is checked but never accepted as a
substitute for the two expected views. In particular, one available correct view
and one missing view is Unknown, not success. A known wrong view makes the joint
event certainly false even if another view is unresolved. The upstream summary's
`all()` may otherwise obscure missing-view uncertainty.

Expected data rows define the denominator. Multiple forms never increase it.
Missing generation, ambiguous scoring and unresolved cases remain in the fixed
roster. Conservative accuracy counts Unknown as nonsuccess; identification
bounds also allow each Unknown to be either0or1. Per-fact score statuses and
missing-view lists remain in `fact_table.jsonl`; summaries count unresolved and
format/status categories separately. This code does not rescore ambiguous raw
answers or invent adjudication.

Rows retain **seed / teacher_mode / cohort / scale / stage / fact_phase /
assigned_quota**. A/B facts are trained facts; sentinel is a separate0-supervision
control. `assigned_quota`1or8 is a planned design label. `actual_exposures` comes
from committed checkpoint state. AfterA, B facts have0 actual exposure even though
their future quota label is known. AfterB, A and B have their own committed
quotas. Frozen none always has0 actual exposures and updates; sharing a schedule
only assigns comparable subgroup labels. It never creates baseline training.

`teacher_mode=candidate` in a preparation row is replaced by the explicit mapping
label. Other per-row teacher modes remain separately stratified; a contradictory
mapping receives a matching audit. Never label source-conditioned supervision as
teacher closed-book knowledge. Use only pretraining-frozen cohort membership;
this script does not choose candidates or drop unsuccessful examples.

## Paired comparisons and uncertainty

Default pairs within the same seed/cohort/mode/scale/stage/intervention are:

- Every arm minus frozen none (or explicit `baseline_id`, allowing the same
  untrained baseline scores to be reused at A/B checkpoints).
- memory_head minus memory_kl, memory_random and adapter.
- memory_kl minus memory_ce.
- memory_head minus memory_l2 when the optional L2 arm exists.

Explicit `comparisons` can additionally name run IDs. Primary differences are
**left minus right**. Accuracy improvement is positive; NLL degradation is
positive. They must not be confused.

Intervals are source-family paired percentile bootstrap, **5000 resamples**, base
seed11050031. Each contrast/stratum/metric receives a deterministic hash-derived
seed stored in output. A sampled family contributes all its paired facts. The
estimate is an overall fact ratio, not an unweighted mean of family means;
next-token NLL uses total loss divided by total valid prediction tokens. Cluster
sizes may vary. The implementation bounds memory while drawing clusters. NumPy
version and exact seeds are recorded. A one-family bootstrap is degenerate and
explicitly cautioned; no-family intervals are absent.

Two accuracy intervals are reported: one for the prespecified conservative
Unknown=0 point, plus a worst-case interval combining unresolved outcome bounds
and family bootstrap. They are not a missingness model. Intervals are unadjusted
95% descriptive intervals, not an implied multiplicity correction or an automatic
scientific acceptance rule. Training seeds remain separate. Fact bootstrap does
**not** measure training-seed variation.

`retention_before_id` pairs afterB with the same arm afterA. It reports allA
postB-minus-postA change, plus retention conditional on **known afterA success**.
Those are different populations. Previously unresolved facts are not silently
counted as learned. Known forgetting, postB uncertainty and conditional
denominators/families remain visible. A-exposure changes, wrong stages/arm or
missing continuation phase history receive an audit.

## NLL, matching and audit files

For answer-content probability, `kind=facts`; for independent untrained
next-token text, `kind=general_lm`. The latter has no generation-accuracy
endpoint. Both use `metrics_rank*.jsonl` from the existing evaluator. CE includes
actual valid prediction tokens only, with natural logs. It is never a mean of
rank or paragraph means. Missing NLL records make the full-roster estimate
unavailable; an observed-only value is explicitly named. The code does not invent
a finite missing-loss upper bound. No cached evaluation input is `NOT_RUN`, not
a failed generation score.

Checkpoint sidecar JSON is read; no pickle or model weight is loaded. The code
checks expected rosters, duplicate rank records, source identity, original
question identity when recorded, checkpoint hash, exposure ledgers,
schedule/order equality and common optimization configuration. Config or audit
failures remain visible as `MATCHING_NOT_VERIFIED`; descriptive numbers do not
then justify clean method effects. The training/resume/token audit still owns
proof of actual optimizer correctness and full-state lineage.

Output files:

| File | Meaning |
|---|---|
| `fact_summary.csv` | Primary/secondary fact counts, conservative accuracy and bounds |
| `nll_summary.csv` | Separate answer-probability and generalLM token-weighted NLL |
| `comparison_availability.csv` | Required arm availability; missing arms are NOT_RUN, not silently omitted |
| `paired_contrasts.csv` | Prespecified paired deltas, intervals, matching flags |
| `retention.csv` | AllA change and conditional A retention |
| `fact_table.jsonl` | One row/fact/run, tri-state endpoints and actual exposures |
| `results.json` | Structured tables, audits, all input hashes and code hash |
| `audit_coverage.md` | Denominator, missing views, unresolved and scoring boundary |
| `audit_matching.md` | Exposure, zero-control, schedule/config/lineage boundary |
| `audit_statistics.md` | Cluster, seed, CI, NLL and interpretation boundary |

All birth-year, template, automatic-source-verification, source-family and
controlled-exposure limits remain in force. Neither knowledge gain, activation
spectrum nor a closed memory readout establishes that low singular directions
encode natural long-tail facts. No actual efficacy claim was made while writing
or testing this interface.

Within one seed,the1/8 strata contain different randomly assigned facts. This tool does not mislabel their direct dose difference as a same-fact paired estimate; arms are paired within each quota stratum.

## Conditional configuration qualification amendment

Use this v2 entry point for formal aggregation. The v1 numerical estimands are
unchanged, but v1 did not fully qualify module/objective matching or exact A→B
lineage. `source_manifest_amendment_v2.json` records that limitation rather than
rewriting the old source freeze or old synthetic output.

A global `objective_contract` (or explicit per-run contract) declares the
pre-frozen expected objective. `expected_kl_weight` is0.5 in this experiment;
memory_ce has the explicit0 exception. Head/random use the same declared
`head_spectrum_weight`. L2 uses `head_weight * head_dim / d_model`; the declared
ratio is0.0625 for head64 and d1024. Other trained arms have effective spectral
penalty0, irrespective of an unused raw CLI spectrum_weight. No blanket
coefficient-equality rule is used. No default head weight is treated as a formal
DEV decision: an absent/null formal head weight stays NOT_VERIFIED.

All trained-arm pairs, **including adapter**, compare module_config,
initial_delta_ratio, spectrum_sha256 and head_dim as well as the prior common
optimization/cache/source fields. Adapter does not get an automatic architecture
exception. Actual trainable parameter counts must come from a mapped
`parameter_count_receipt` (normally that run's initialization.json,
`parameters` field); a naked number in the mapping is not proof. The receipt
must be in the checkpoint's run directory. Its measured count is checked against
the module dimensions and the declared parameter budget. Config/parameter
inequality or unavailable proof stays in qualification flags. A future adapter
with a different configuration would require an explicit new qualification
amendment; this v2 does not silently waive it.

## Exact A→B receipt bridge

Each afterB run with a retention comparison supplies:

```json
"continuation": {
  "launch_receipt": "/actual/parallel_receipts/ARM_B.json",
  "argv_field": "argv",
  "input_checkpoint_field": "input_checkpoints.--continue-from",
  "launch_cwd": "/actual/execution/root",
  "parent_checkpoint": "/actual/ARM/A/checkpoints/final.pt",
  "parent_checkpoint_sha256": "SHA_OF_THE_EVALUATED_A_CHECKPOINT"
}
```

The launch receipt must record the actual argv, COMPLETE/exit_code0, and the
launch-time `input_checkpoints["--continue-from"]` path/hash. The existing
`run_parallel.py` interface produces that receipt and checks input hashes again
after execution. The statistics reader checks one unambiguous --continue-from,
no simultaneous --resume, explicit cwd for relative paths, the recorded parent
path/hash, current parent-file bytes, the mapping's frozen parent hash, and the
A checkpoint manifest used for the afterA evaluation. It also verifies B argv
--arm/--phase/--out against the evaluated B checkpoint directory. No checkpoint
pickle is loaded; parent bytes are hashed only. All receipt/parameter/checkpoint
input paths and hashes enter the result provenance.

An A entry in phase_history is only an auxiliary consistency check. It cannot
prove which A checkpoint B actually consumed. Missing receipt, launch-time hash,
parent bytes or any mismatch yields MATCHING_NOT_VERIFIED while preserving the
numerical retention records. Continuation also requires common module/objective/
optimization/basis/source configuration across A/B; schedule SHA and phase differ
by design. This bridge is bounded to the supplied immutable execution receipts;
it does not replace the optimizer/RNG/resume qualification owned by training.

Fourteen CPU synthetic tests include wrong module/init/basis/head/parameter
settings; accepted CE/KL/head/random/L2 differences; wrong or missing continuation
argv/hash/parent file/output directory; and a regression test proving v1 and v2
produce identical numeric estimates/intervals on the same synthetic fixture.
No actual model outputs were accessed in implementing this amendment.
