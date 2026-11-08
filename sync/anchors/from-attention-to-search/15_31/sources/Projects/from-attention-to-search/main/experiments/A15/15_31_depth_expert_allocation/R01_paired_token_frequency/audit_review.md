# Pre-run audit: identification, data and numerical implementation

Audit stage: source/construction and accepted submission only. Job`pt-ds9bdaxb` is not yet verified inside GPU execution in this record. These audits support interpretability; none confirms the hypotheses.

## 1. Science identification

PASS at design/accounting scope: the comparison changes expert allocation over depth, with exact expert/router parameter totals and unchanged hidden/expert widths, top-2, attention and tied vocabulary interfaces. H1 uses final low-frequency-token NLL; overall/high-frequency costs remain visible. This measures a frequency proxy rather than semantic long-tail representation. Advisor intuition, oral prior reports and new hypotheses are separated in[source_review.md](source_review.md).

Remaining rivals include initialization sensitivity in a single pair, repeated exposure in a small source prefix, optimization/load-control interactions and real dispatch/compute differences. Router/receipt changes are part of the observed architecture behavior; no route-load mediation is identified causally. The width-varying sketch is formula-only, outside A/B.

## 2. Data statistics

PASS for exact-document split/provenance construction: token-byte hashes deduplicate globally before dev/test/train assignment. The complete frozen dev/test split is retained for general loss. Actual cyclic supervised-target counts will determine integer type-tertile buckets, keeping unseen separate. The common budget fixes those counts; final model metrics cannot change rules. Test metadata/examples were inspected, as requested, without using model-test performance for selection.

LIMITED: only a deterministic67,108,864-token source prefix is scanned; near duplicates are not checked. Recovered documents are bootstrap clusters, but packed contexts can cross document boundaries, leaving residual dependence. Type counts/cutoffs/coverage remain pending formal freeze. Fact/entity evaluation is NOT RUN because no independently reliable occurrence/split contract was established. Two thousand paired document resamples describe sampling rather than across-seed uncertainty.

## 3. Implementation and numerics

PASS for CPU parameter enumeration/common-start checks: both totals507,988,992; all64 experts accounted; tied head counted once;242 common tensors and42 overlap-router rows match. See[actual ledger](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/parameter_ledger.json) and[initial hashes](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/initial_parameter_hashes.json).

PENDING GPU evidence: finite forward/backward and gradients, assignment identity/no drop, actual throughput/memory, save/reload, external-process replay and evaluation recomputation. A submitted receipt is not a passed smoke. Full-stage eligibility requires the joint gate and immutable freeze. Theoretical active parameters/FLOPs are accounting; hardware instruction FLOPs must not be labeled measured without actual measurement. Failures and retries are retained; one arm's budget cannot be reduced to force completion.

## Completed three-part audit update

Scientific identification: matched-capacity/exposure pair is complete;B is worse in low/overall NLL,without assigning an SNR cause or closing the question. Data/statistics:all30raw values and independent2000-draw intervals PASS;low1481targets occur in246/544documents,with single-seed/packed-dependence limits. Implementation/numerics:both874-step trajectories pass finite/count/drop0/TensorBoard and all batch hashes match;8frozen sources,5legacy sources and11analysis provenance hashes are unchanged. Actual formal seed20261106 initialization passes after strict access to both families. Formal A/B/analysis assets are registered and strict PASS. These checks establish their bounded facts,not scientific acceptance.

## Final gate update

GPU PENDING above is the pre-execution snapshot. Actual dual smoke, exact external recovery/DEV replay, all 874 matched data/count updates, all formal evaluations, independent intervals, formal initial weights, frozen/legacy source hashes and registered-output strict access have passed. See the [Detailed](detailed.md) and [delivery checks](delivery_completion_checks.json). Scientific acceptance remains Unknown; full hardware FLOPs are unmeasured, with recorded matrix counts and explicit graph estimates retained.
