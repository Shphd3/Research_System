---
experiment_id: A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer
status: EVIDENCE_COMPLETE_AI_INTERPRETATION_AWAITING_HUMAN_CONFIRMATION
completed: 2026-08-28
---

# Detailed: Cross-Parent Fine-Function Transfer

Primary Anchor: [A15_10 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_10_cross_parent_fine_function_transfer/15_10_cross_parent_fine_function_transfer_anchor.md)  
Frozen execution-time Protocol: [protocol.md](protocol.md), preflight SHA-256
`44dc03f29fb17f3f4654b630aaef2e2e161fcee80031d1c9d69fd7dc0614334d`;
the same file's current SHA-256 is
`fa8b59125aff580538151568681c656de3f471791f7728212095e574bfd1d0d7`
after the append-only completion ledger was added  
Summary: [summary.md](summary.md)  
Result eligibility: 18 eligible cells, 6 ineligible cells retained, full run
complete; interpretation awaits human confirmation.

## 0. Quick Recap

- **Purpose:** distinguish cross-parent functional interchangeability from
  passive low geometric overlap.
- **Hypothesis:** at least one fixed layer has bidirectional mathematics--physics
  Cross function beyond a full source-label-permutation null in both C4 and C5.
- **Direct result:** 0/6 layers passed. Only C5 Block 36 mathematics to physics
  exceeded its Cross null; the corresponding C4 direction did not and the
  reverse C5 cell was ineligible.
- **Eligibility:** Blocks 4 and 12 had four eligible directions each and failed
  to establish transfer. Later layers were insufficient at the layer level.
- **Boundary:** lack of replicated excess weakens a shared-fine-space premise;
  it does not prove strict parent locality or Router utility.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Own | target parent's own fine space | target Fisher basis, target head, other-half test | held-out NLL | functional admission and reference | native Router use |
| Cross | other parent's fine space | source Fisher basis, target head, other-half test | held-out NLL | tests cross-parent interchangeability | label transfer |
| CrossPerm | matched randomization control | permute source labels by complete family and rerun source space, target head, test | 200 NLL values per cell | controls the full estimator pipeline | a population random-space law |
| RR | relative retention | \((L_{null,50}-L_{Cross})/(L_{null,50}-L_{Own})\) | dimensionless, unclipped | continuous Cross position between null and Own | a causal percentage of information |
| Eligible | every registered cell guard passed | inherited rank/stability, Own function, convergence, positive RR denominator | Boolean | separates evidence from diagnostics | scientific truth outside this contract |

## 2. Anchor Link And Decision Point

A15_09 established that the common coarse Fisher space and each
parent-conditional fine Fisher space have low, null-subordinate overlap. That
geometry could still have hidden functional interchangeability. A15_10 changes
only the input space supplying a matched target head, so its decision point is
whether shared-fine or parent-conditioned-local routing remains the better
candidate for a later causal architecture test.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Execution approval | implementation, smoke, full run | explicitly approved before submission | pass | Protocol Section 17 | none |
| Model / activations | frozen Qwen3-30B-A3B native states | predecessor C4/C5 hashes and `[6,1920,2048]` shapes matched | pass | `preflight.json` | none |
| Layers / parents | 4/12/20/28/36/44; mathematics/physics only | exact match | pass | `results.json` | none |
| Shared Fisher metric | same pooled within-leaf metric per panel/layer/split | implemented and unit tested | pass | `geometry.py`, tests | none |
| Cross-fit | A space + A target head to B, then reverse | exact match | pass | prediction row identities and tests | none |
| Head selection | fixed C grid, train-only family folds | exact match | pass | null ledger and selected-C fields | none |
| Randomization | 200 complete-family full-pipeline permutations | 4,800 Cross and 4,800 Own pipelines | pass | `null_ledger.json` | none |
| Bootstrap | 10,000 complete-family paired draws | exact match | pass | RR quantiles in `results.json` | none |
| Registered cells | 24, invalid retained | 24 present; 18 eligible, 6 ineligible | pass | completion audit | invalid cells excluded from eligible aggregates |
| Required figures | three registered figures | all present and hash-audited | pass | completion audit | none |
| Code revision receipt | code revision and dirty-state receipt | worker tree is not a Git repository; no pre-run dirty-state artifact | deviation | live filesystem check after run | no numerical eligibility change; provenance is bounded to file hashes |
| Code file identity | exact executed files recoverable | post-run aggregate SHA-256 `0c18276c...a11bc82`; no worker code was edited after submission | bounded pass | file hash audit | future reproduction should use the archived worker tree |

Amendments A1 and A2 were recorded before any A15_10 result visibility. There
were no retries, condition exclusions, layer replacements, or post-hoc changes
to methods or thresholds. ACP job `pt-9dwr9q52` succeeded on the first attempt.

## 4. Actual Setup

- **Data:** existing C4 primary and C5 independent controlled natural-language
  panels; each has 8 parents, 8 children per parent, and 30 complete template
  families. A/B contain 15 families each.
- **Representation:** frozen native Qwen3-30B-A3B MoE-input state, 2048
  dimensions, Blocks 4/12/20/28/36/44.
- **Targets:** mathematics and physics only; eight fine labels per target.
- **Fisher space:** seven Euclidean-orthonormal directions using the shared
  pooled Ledoit--Wolf within-leaf metric for a fixed panel/layer/split.
- **Head:** multinomial L2 logistic regression, `lbfgs`, maximum 5,000
  iterations, tolerance \(10^{-8}\), C grid
  \(10^{-4},10^{-3},10^{-2},10^{-1},1,10,100\); five deterministic complete-family
  folds and train-only NLL selection.
- **Preprocessing:** target-train-half mean centering only. No coordinatewise
  scaling, preserving orthonormal basis-rotation invariance.
- **Held-out unit:** complete template family. Each fold trains on 120 target
  rows and tests on 120 target rows.
- **Resource:** ACP `share-space` / `share-cluster`, one `n6ls.iu.i40.4`
  reserved worker, 4 H100-80GB GPUs, 88 CPUs, 960 GiB memory.
- **Runtime:** NumPy 1.26.4, SciPy 1.15.3, scikit-learn 1.6.1, joblib 1.5.1,
  matplotlib 3.10.3.
- **Elapsed:** 540.3 seconds for analysis; job start 03:25:55Z and final update
  03:35:25Z.

## 5. Metrics And Registered Decision Rules

Lower NLL is better. A direction is eligible only if inherited rank/separate
split stability, Own below its OwnPerm 2.5th percentile, all head convergence,
and a finite positive RR denominator pass. Cross excess requires observed
Cross NLL below its CrossPerm 2.5th percentile. A layer passes only when both
directions pass in C4 and C5. The \(RR=0.9\) line is descriptive only.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation | Aggregation / uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Complete run | 24 cells and all required artifacts | predictions, null ledger, figures | completion audit | exact row and hash checks | 24 cells; 17,280 prediction rows | eligible | complete | no Git revision receipt |
| Cross-parent transfer | bidirectional C4/C5 Cross excess at a layer | per-example held-out probabilities and 200 Cross nulls/cell | NLL and empirical 2.5th percentile | A/B average; family randomization | 1/24 directional excess; 0/6 layer pass | mixed per-cell eligibility | not established | later layers partly insufficient |
| Relative retention | continuous RR | Own, Cross, CrossPerm NLL | registered formula | 10,000 paired family bootstraps | eligible range 0.0339--0.1810; median 0.0743 | eligible cells only | small retention | empirical normalization, not causal fraction |
| Fine-space geometry | diagnostic only | A/B Fisher bases | mean cross-half projector overlap | no angle-wise null registered | 0.0060--0.0219 | diagnostic | low raw overlap | cannot determine function by itself |

## 7. Main Results

### 7.1 Full registered matrix

`E` means eligible, `I` means insufficient; `*` means Cross passed its matched
2.5th-percentile null gate.

| Block | C4 math→physics RR | C4 physics→math RR | C5 math→physics RR | C5 physics→math RR | Layer verdict |
| ---: | ---: | ---: | ---: | ---: | --- |
| 4 | 0.0389 E | 0.0528 E | 0.0588 E | 0.0708 E | Fail to establish |
| 12 | 0.0555 E | 0.0967 E | 0.0339 E | 0.0974 E | Fail to establish |
| 20 | 0.0547 E | 0.1810 E | 0.0895 E | 0.1138 I | Insufficient |
| 28 | 0.0713 E | 0.1732 I | 0.0797 E | 0.1501 E | Insufficient |
| 36 | 0.0989 E | 0.0997 I | 0.1324 E* | 0.1457 I | Insufficient |
| 44 | 0.0611 E | 0.0988 I | 0.0736 I | 0.0772 E | Insufficient |

### 7.2 Ineligible evidence

Five cells failed only the Own functional-admission gate: C4 physics to
mathematics at Blocks 28/36/44, C5 physics to mathematics at Block 36, and C5
mathematics to physics at Block 44. Their observed Own NLL missed the OwnPerm
2.5th percentile by \(3.7\times10^{-6}\) to \(5.3\times10^{-4}\), so they are kept
but not rescued by closeness. C5 Block 20 physics to mathematics had one
non-converged Cross null fit and one non-converged Own null fit among the
registered permutations; the all-convergence gate therefore failed.

### 7.3 Why high Cross accuracy is not the conclusion

Cross balanced accuracy ranges from 0.7125 to 1.0000, while the per-cell median
CrossPerm balanced accuracy ranges from 0.7167 to 1.0000 and the common coarse
control ranges from 0.8583 to 1.0000. This means fine labels are readable from many seven-dimensional views
of the full representation. The specific other-parent space usually gives
better NLL than the null median, hence positive RR, but almost never clears the
pre-registered tail criterion. The correct result is limited transfer beyond
matched redundancy, not “Cross cannot classify.”

## 8. Visualization Results

### 8.1 Raw matched target-head comparison

![Functional transfer ladder](figures/figure1_functional_transfer_ladder.png)

- **Metric:** held-out NLL; lower is better.
- **Source:** `results.json` and 200 Cross permutations per cell.
- **How to read:** green Own is the task-specific reference; red Cross must
  fall below the grey 95% null band to show registered excess. Blue is the
  common coarse-space control. Black crosses mark invalid cells.
- **Observed:** red mostly tracks the null band; only C5 Block 36
  mathematics-to-physics clears its lower edge.
- **Cannot prove:** the blue or red spaces are used by the native Router.

### 8.2 Relative-retention profile

![Relative retention across layers](figures/figure2_rr_trajectory.png)

- **Metric:** empirical RR with 10,000 family-bootstrap intervals.
- **Observed:** all point estimates are near 0 and far below Own=1; no layer
  establishes the required replicated bidirectional effect.
- **Limitation:** trajectories include marked gaps where cells are ineligible;
  layer is not an independent replicate.

### 8.3 Geometry and function are separate

![Geometry versus transfer](figures/figure3_geometry_function_relation.png)

- **Metric:** raw mathematics--physics fine-space overlap versus RR.
- **Observed:** low overlap coexists with nonzero decodability, and no simple
  monotone relation is visually established.
- **Limitation:** this is diagnostic; no correlation test or geometry-based
  decision threshold was registered.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Meaning | What remains live |
| --- | --- | --- | --- | --- |
| Inputs | hashes, shapes, layers | passed | predecessor assets reused exactly | none |
| Estimator smoke | 10/10 tests | passed | cross-fit and invariance identities hold | statistical adequacy remains separate |
| Own admission | 19/24 passed | mixed | five target-own tail gates too close to null | later-layer layer verdicts insufficient |
| Numerical admission | 23/24 passed | mixed | one cell contains null convergence failures | other 23 cells unaffected |
| Directional transfer | 1/24 excess | failed globally | no broad Cross excess | one isolated signal is not replicated |
| Layer replication | 0/6 passed | failed / insufficient | strong shared-fine hypothesis not established | parent-conditioned candidate remains plausible |

The run does not falsify the implementation or the use of a matched null. It
does falsify the registered strong transfer pattern. It also reveals a data /
representation property: generic seven-dimensional projections retain much
fine-label readability, so accuracy alone is an inadequate functional metric.

## 10. Full Experiment Record

- Submission: 2026-08-28T03:25:14Z
- Job: `pt-9dwr9q52`, final state `SUCCEEDED`
- Run stamp: `20260828T032514Z`
- Tests: 10 passed in 14.63 seconds remotely
- Cross permutation pipelines: 4,800
- Own-admission permutation pipelines: 4,800
- Total permutation pipelines: 9,600
- Family-bootstrap draws: 10,000 per cell
- Prediction rows: 17,280 = 24 cells × 3 observed conditions × 240 held-out
  predictions
- Retry count: zero
- Excluded or replaced cells: zero

## 11. Interpretation

The 0826 meeting proposed that coarse and fine information might occupy the
same tail subspace, motivating a tree whose parent knowledge is reused by its
children. A15_09 already found that common coarse and conditional fine Fisher
spaces are geometrically distinct. A15_10 now adds that mathematics and
physics fine Fisher spaces are not functionally interchangeable beyond a
matched randomization pipeline.

The combined update is not “semantic information is absent outside the right
space.” The controls show the opposite: fine labels remain broadly decodable.
The narrower statement is that the parent-own Fisher space is substantially
more efficient in held-out NLL, while the other parent's named fine space is
usually no better than other estimator-matched seven-dimensional views. This
supports testing parent-conditioned specialization, but it does not yet
establish that architecture causally improves routing or language modeling.

## 12. Claim Boundary

**Can claim:** no registered layer establishes transferable mathematics--physics
fine function; eligible RR is small; passive geometry and decodability cannot
be collapsed into one conclusion.

**Cannot claim:** strict locality, causal necessity, a universal semantic tree,
native Router use, an optimal layer, or language-model improvement.

## 13. Next Decision

**Decision:** human confirmation of one causal architecture question: with
data, capacity, optimizer, target supervision, and compute matched, does a
correct-parent-conditioned local fine Router outperform one global shared fine
Router on both held-out fine-routing quality and language-model NLL?

**Completion criterion:** one preregistered comparison with parent
conditioning as the only structural change; both routing and end-task losses
reported; no geometric proxy used as the pass condition.

**Resume action:** create a new Focus and Protocol only after the researcher
confirms this result reading and next question. Do not start Router training
from this record.

## 14. Artifact Manifest

| Artifact | Purpose | Hash / identity | Complete | Claim-eligible |
| --- | --- | --- | --- | --- |
| Frozen Protocol | registered execution-time contract | preflight `44dc03f2...4334d`; current append-only record `fa8b5912...d0d7` | yes | yes |
| `preflight.json` | frozen-input gate | `330d99eb...25bf` | yes | yes |
| `smoke_receipt.json` | label-blind implementation gate | `6115777e...ecbc` | yes | yes |
| `results.json` | primary derived metrics | `6b1a5590...f19` | yes | yes |
| `null_ledger.json` | all Own/Cross null runs | `fc1285b3...6f` | yes | yes |
| `predictions.jsonl` | sample-level observed predictions | `57227f13...0a5` | yes | yes |
| `cells.csv` | flat result table | `54cf0fb3...da1` | yes | yes |
| `completion_audit.json` | row / figure / hash closure | `df0973a1...95f` | yes | yes |
| Figure 1 | raw functional ladder | `4eb2343a...9111` | yes | yes |
| Figure 2 | RR trajectory | `d943fdd9...d93c2` | yes | yes |
| Figure 3 | geometry/function diagnostic | `65633cc6...bc16` | yes | diagnostic only |
| Worker code tree | executable implementation | aggregate `0c18276c...bc82` | bounded | yes, with no Git receipt |

## 15. Links

- Code workspace:
  `/data/250010109/MoE_Router/experiments/20260828_a15_10_e01_qwen3_30b_cross_parent_fine_function_transfer`
- Result directory:
  `/data/250010109/MoE_Router/experiments/20260828_a15_10_e01_qwen3_30b_cross_parent_fine_function_transfer/runs/full-20260828T032514Z`
- Runner: `scripts/run_pipeline.sh`
- Submitter: `scripts/submit_h100_4_reserved.sh`
- Reproduction identity: run stamp `20260828T032514Z`, ACP job
  `pt-9dwr9q52`, Protocol SHA above.
